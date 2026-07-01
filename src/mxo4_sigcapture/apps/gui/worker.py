"""Background SCPI worker thread."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from PySide6.QtCore import QObject, QThread, Signal


@dataclass
class WorkerRequest:
    op: str
    payload: dict[str, Any]


class ScpiWorker(QObject):
    finished = Signal(object)
    error = Signal(str)
    progress = Signal(int, int, str)
    channel_progress = Signal(int, int)

    def __init__(self) -> None:
        super().__init__()
        self._cancel = False
        self._session = None
        self._service = None

    def set_cancel(self, value: bool) -> None:
        self._cancel = value

    def run_request(self, request: WorkerRequest) -> None:
        try:
            result = self._dispatch(request)
            self.finished.emit(result)
        except Exception as exc:
            self.error.emit(str(exc))

    def _dispatch(self, request: WorkerRequest) -> Any:
        from mxo4_sigcapture.capture.service import CaptureService
        from mxo4_sigcapture.config.app import AppConfig
        from mxo4_sigcapture.scpi.session import Mxo4Session

        op = request.op
        cfg: AppConfig = request.payload["config"]

        if op == "connect":
            resource = cfg.connection.resource
            self._session = Mxo4Session.from_visa(
                resource, timeout_ms=cfg.connection.visa_timeout_ms
            )
            self._service = CaptureService(self._session)
            errs = self._service.connect(cfg)
            return {"idn": self._session.identify(), "errors": errs}

        if self._service is None:
            raise RuntimeError("Not connected")

        if op == "disconnect":
            if self._session:
                self._session.close()
            self._session = None
            self._service = None
            return {"disconnected": True}

        if op == "apply":
            setup = self._service.apply_setup(cfg)
            return {"readback": setup.readback, "errors": setup.errors}

        if op == "stop":
            self._session.stop()
            return {}

        if op == "find_level":
            from mxo4_sigcapture.config.trigger import find_trigger_level
            find_trigger_level(self._session)
            return {}

        if op == "capture":
            self._cancel = False

            def on_ch(ch: int, total: int) -> None:
                self.channel_progress.emit(ch, total)

            def cancel_check() -> bool:
                return self._cancel

            result = self._service.capture_once(
                cfg,
                apply_first=request.payload.get("apply_first", False),
                on_channel_start=on_ch,
                cancel_check=cancel_check,
            )
            return {"result": result}

        raise ValueError(f"Unknown op: {op}")


class WorkerThread(QThread):
    def __init__(self, worker: ScpiWorker, request: WorkerRequest) -> None:
        super().__init__()
        self._worker = worker
        self._request = request

    def run(self) -> None:
        self._worker.run_request(self._request)
