"""Thin GUI controller — no SCPI in widgets."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from PySide6.QtCore import QObject, Signal

from mxo4_sigcapture.apps.gui.worker import ScpiWorker, WorkerRequest, WorkerThread
from mxo4_sigcapture.config.app import AppConfig, UserPrefs
from mxo4_sigcapture.storage.hdf5 import Hdf5Writer, build_filename

PREFS_PATH = Path.home() / ".mxo4_sigcapture_prefs.json"


class Controller(QObject):
    connected_changed = Signal(bool)
    idn_changed = Signal(str)
    readback_changed = Signal(object)
    dirty_changed = Signal(bool)
    errors_changed = Signal(list)
    capture_done = Signal(object)
    status_message = Signal(str)
    channel_progress = Signal(int, int)
    busy_changed = Signal(bool)

    def __init__(self) -> None:
        super().__init__()
        self.config = AppConfig()
        self._last_applied: AppConfig | None = None
        self._last_capture = None
        self._worker_obj = ScpiWorker()
        self._thread: WorkerThread | None = None
        self._connected = False
        self._load_prefs()

    def _load_prefs(self) -> None:
        if PREFS_PATH.exists():
            try:
                data = json.loads(PREFS_PATH.read_text(encoding="utf-8"))
                self.config.prefs = UserPrefs(**{**asdict(UserPrefs()), **data})
            except (json.JSONDecodeError, TypeError):
                pass

    def save_prefs(self) -> None:
        PREFS_PATH.write_text(
            json.dumps(asdict(self.config.prefs), indent=2), encoding="utf-8"
        )

    def is_dirty(self) -> bool:
        if self._last_applied is None:
            return self._connected
        return asdict(self.config) != asdict(self._last_applied)

    def can_single(self) -> bool:
        if not self._connected:
            return False
        if self.config.prefs.auto_apply_before_capture:
            return True
        return not self.is_dirty()

    def update_config(self, config: AppConfig) -> None:
        self.config = config
        self.dirty_changed.emit(self.is_dirty())

    def connect(self) -> None:
        self._run("connect", {})

    def disconnect(self) -> None:
        self._run("disconnect", {})

    def apply_setup(self) -> None:
        self._run("apply", {})

    def stop_acquisition(self) -> None:
        self._run("stop", {})

    def find_level(self) -> None:
        self._run("find_level", {})

    def single_capture(self) -> None:
        apply_first = self.config.prefs.auto_apply_before_capture or self.is_dirty()
        self._run("capture", {"apply_first": apply_first})

    def cancel_capture(self) -> None:
        self._worker_obj.set_cancel(True)

    def save_hdf5(self, directory: Path | None = None) -> Path | None:
        if self._last_capture is None:
            self.status_message.emit("No capture to save")
            return None
        from mxo4_sigcapture.capture.service import CaptureResult

        result: CaptureResult = self._last_capture
        out_dir = Path(directory or self.config.prefs.last_save_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        fname = build_filename(self.config, result)
        path = out_dir / fname
        Hdf5Writer().write(path, self.config, result)
        self.config.prefs.last_save_dir = str(out_dir)
        self.save_prefs()
        self.status_message.emit(f"Saved {path.name}")
        return path

    def preview_filename(self) -> str:
        from mxo4_sigcapture.capture.service import CaptureResult

        if self._last_capture is None:
            stub = CaptureResult(idn="", options="")
            return build_filename(self.config, stub)
        return build_filename(self.config, self._last_capture)

    def _run(self, op: str, extra: dict[str, Any]) -> None:
        if self._thread and self._thread.isRunning():
            self.status_message.emit("Busy — wait for current operation")
            return
        self.busy_changed.emit(True)
        req = WorkerRequest(op=op, payload={"config": self.config.copy(), **extra})
        self._thread = WorkerThread(self._worker_obj, req)
        self._thread.finished.connect(self._on_thread_done)
        self._worker_obj.finished.connect(self._on_worker_finished)
        self._worker_obj.error.connect(self._on_worker_error)
        self._worker_obj.channel_progress.connect(self.channel_progress.emit)
        self._thread.start()

    def _on_thread_done(self) -> None:
        self.busy_changed.emit(False)

    def _on_worker_error(self, msg: str) -> None:
        self.errors_changed.emit([msg])
        self.busy_changed.emit(False)

    def _on_worker_finished(self, payload: Any) -> None:
        if isinstance(payload, dict):
            if "idn" in payload:
                self._connected = True
                self.connected_changed.emit(True)
                self.idn_changed.emit(payload["idn"])
                errs = payload.get("errors", [])
                self.errors_changed.emit([e for e in errs if not str(e).startswith("+0,")])
                self._last_applied = None
                self.dirty_changed.emit(True)
            if "readback" in payload:
                self._last_applied = self.config.copy()
                self.readback_changed.emit(payload["readback"])
                self.dirty_changed.emit(False)
                errs = payload.get("errors", [])
                self.errors_changed.emit([e for e in errs if not str(e).startswith("+0,")])
            if "result" in payload:
                self._last_capture = payload["result"]
                self.capture_done.emit(payload["result"])
                if not self.config.prefs.auto_apply_before_capture:
                    pass
                else:
                    self._last_applied = self.config.copy()
                    self.dirty_changed.emit(False)
            if "disconnected" in payload:
                self._connected = False
                self.connected_changed.emit(False)
                self.idn_changed.emit("")
                self._last_applied = None
                self.dirty_changed.emit(False)
            if payload == {} and not self._connected:
                self._connected = False
                self.connected_changed.emit(False)
                self.idn_changed.emit("")
        self.busy_changed.emit(False)
