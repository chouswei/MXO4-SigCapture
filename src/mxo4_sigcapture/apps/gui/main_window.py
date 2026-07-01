"""MXO4 SigCapture main window."""

from __future__ import annotations

import subprocess
import sys
import time

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from mxo4_sigcapture.apps.gui import theme
from mxo4_sigcapture.apps.gui.controller import Controller
from mxo4_sigcapture.apps.gui.widgets.acquisition_bar import AcquisitionBar
from mxo4_sigcapture.apps.gui.widgets.channel_strip import ChannelStrip
from mxo4_sigcapture.apps.gui.widgets.connection_bar import ConnectionBar
from mxo4_sigcapture.apps.gui.widgets.dirty_indicator import DirtyIndicator
from mxo4_sigcapture.apps.gui.widgets.graticule_plot import GraticulePlot
from mxo4_sigcapture.apps.gui.widgets.time_acquire_panel import TimeAcquirePanel
from mxo4_sigcapture.apps.gui.widgets.trigger_panel import TriggerPanel
from mxo4_sigcapture.config.app import AppConfig


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("MXO4 SigCapture")
        self.resize(1280, 800)
        self.setMinimumSize(960, 600)
        self.setStyleSheet(f"background: {theme.BG}; color: {theme.TEXT};")
        self._controller = Controller()
        self._channel_strip = ChannelStrip()
        self._capture_start: float = 0.0
        self._splitter: QSplitter | None = None
        self._right_dock: QWidget | None = None
        self._build_ui()
        self._wire_signals()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(6, 6, 6, 6)
        root.setSpacing(4)

        self._conn = ConnectionBar()
        root.addWidget(self._conn)

        self._splitter = QSplitter(Qt.Orientation.Horizontal)
        self._plot = GraticulePlot()
        self._splitter.addWidget(self._plot)

        self._right_dock = QWidget()
        self._right_dock.setMinimumWidth(theme.RIGHT_DOCK_MIN_WIDTH)
        self._right_dock.setMaximumWidth(theme.RIGHT_DOCK_MAX_WIDTH)
        dock_layout = QVBoxLayout(self._right_dock)
        dock_layout.setContentsMargins(4, 0, 0, 0)
        dock_layout.setSpacing(6)

        dock_layout.addWidget(self._channel_strip)
        self._trigger = TriggerPanel()
        dock_layout.addWidget(self._trigger)
        self._time_acq = TimeAcquirePanel()
        dock_layout.addWidget(self._time_acq)
        self._dirty = DirtyIndicator()
        dock_layout.addWidget(self._dirty)
        dock_layout.addStretch()

        self._splitter.addWidget(self._right_dock)
        self._splitter.setStretchFactor(0, 1)
        self._splitter.setStretchFactor(1, 0)
        self._splitter.splitterMoved.connect(self._on_splitter_moved)
        root.addWidget(self._splitter, stretch=1)

        self._acq_bar = AcquisitionBar()
        root.addWidget(self._acq_bar)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self._apply_splitter_sizes()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._apply_splitter_sizes()

    def _apply_splitter_sizes(self) -> None:
        if self._splitter is None:
            return
        total = self._splitter.width()
        dock_w = theme.RIGHT_DOCK_WIDTH
        if self._right_dock is not None:
            dock_w = max(
                theme.RIGHT_DOCK_MIN_WIDTH,
                min(theme.RIGHT_DOCK_MAX_WIDTH, self._right_dock.width() or theme.RIGHT_DOCK_WIDTH),
            )
        plot_w = max(1, total - dock_w)
        self._splitter.setSizes([plot_w, dock_w])

    def _on_splitter_moved(self, pos: int, _index: int) -> None:
        if self._right_dock is None or self._splitter is None:
            return
        sizes = self._splitter.sizes()
        if len(sizes) < 2:
            return
        dock_w = sizes[1]
        clamped = max(theme.RIGHT_DOCK_MIN_WIDTH, min(theme.RIGHT_DOCK_MAX_WIDTH, dock_w))
        if clamped != dock_w:
            self._splitter.setSizes([sizes[0] + dock_w - clamped, clamped])

    def _wire_signals(self) -> None:
        self._conn.connect_clicked.connect(self._on_connect)
        self._conn.disconnect_clicked.connect(self._controller.disconnect)
        self._conn.error_lamp.clicked.connect(self._show_errors)

        for cell in self._channel_strip.cells:
            cell.changed.connect(self._sync_config)
        self._trigger.changed.connect(self._sync_config)
        self._time_acq.changed.connect(self._sync_config)

        self._acq_bar.apply_clicked.connect(self._controller.apply_setup)
        self._acq_bar.single_clicked.connect(self._on_single)
        self._acq_bar.stop_clicked.connect(self._controller.stop_acquisition)
        self._acq_bar.save_clicked.connect(self._on_save)
        self._acq_bar.cancel_clicked.connect(self._controller.cancel_capture)
        self._trigger.find_level_clicked.connect(self._controller.find_level)

        self._controller.connected_changed.connect(self._on_connected)
        self._controller.idn_changed.connect(self._on_idn)
        self._controller.readback_changed.connect(self._plot.update_readback)
        self._controller.dirty_changed.connect(self._on_dirty)
        self._controller.errors_changed.connect(self._on_errors)
        self._controller.capture_done.connect(self._on_capture_done)
        self._controller.status_message.connect(self._acq_bar.set_state)
        self._controller.channel_progress.connect(self._on_channel_progress)
        self._controller.busy_changed.connect(self._on_busy)

    def _gather_config(self) -> AppConfig:
        cfg = self._controller.config.copy()
        cfg.connection.resource = self._conn.resource()
        cfg.channels = [c.to_config() for c in self._channel_strip.cells]
        cfg.horizontal = self._time_acq.horizontal_config()
        cfg.acquire = self._time_acq.acquire_config()
        cfg.trigger = self._trigger.to_config()
        return cfg

    def _sync_config(self) -> None:
        self._controller.update_config(self._gather_config())

    def _on_connect(self) -> None:
        self._sync_config()
        self._controller.connect()

    def _on_idn(self, idn: str) -> None:
        self._conn.set_connected(bool(idn), idn)

    def _on_connected(self, connected: bool) -> None:
        self._acq_bar.set_connected(connected)
        self._on_dirty(self._controller.is_dirty())

    def _on_dirty(self, dirty: bool) -> None:
        self._dirty.set_dirty(dirty)
        connected = self._controller._connected
        self._acq_bar.set_single_enabled(connected and self._controller.can_single())

    def _on_errors(self, errors: list[str]) -> None:
        self._conn.set_error_state(bool(errors))
        if errors:
            self._last_errors = errors

    def _show_errors(self) -> None:
        errors = getattr(self, "_last_errors", [])
        if not errors:
            return
        dlg = QDialog(self)
        dlg.setWindowTitle("SCPI errors")
        layout = QVBoxLayout(dlg)
        layout.addWidget(QLabel("\n".join(errors)))
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(dlg.accept)
        layout.addWidget(buttons)
        dlg.exec()

    def _on_single(self) -> None:
        self._sync_config()
        self._capture_start = time.monotonic()
        self._acq_bar.set_state("Acquiring…")
        self._controller.single_capture()

    def _on_channel_progress(self, ch: int, total: int) -> None:
        elapsed = time.monotonic() - self._capture_start
        self._acq_bar.set_progress(ch, total, elapsed)

    def _on_busy(self, busy: bool) -> None:
        self._acq_bar.set_busy(busy)
        if not busy:
            self._on_dirty(self._controller.is_dirty())

    def _on_capture_done(self, result) -> None:
        self._acq_bar.set_state("Ready")
        self._acq_bar.set_progress(0, 0)
        self._plot.plot_capture(result.waveforms, self._controller.config)
        for w in result.waveforms:
            self._channel_strip.cells[w.channel - 1].set_overload(w.clipped)
        self._acq_bar.set_save_enabled(True)
        self._acq_bar.set_filename_preview(self._controller.preview_filename())
        errs = result.setup_errors + result.capture_errors
        if errs:
            self._controller.errors_changed.emit(errs)

    def _on_save(self) -> None:
        path = self._controller.save_hdf5()
        if path is None:
            return
        n_ch = len(self._controller._last_capture.waveforms)  # noqa: SLF001
        pts = sum(len(w.y) for w in self._controller._last_capture.waveforms)  # noqa: SLF001
        msg = QMessageBox(self)
        msg.setWindowTitle("Saved")
        msg.setText(f"Saved {n_ch} channel(s), {pts} points\n{path.name}")
        open_btn = msg.addButton("Open folder", QMessageBox.ButtonRole.ActionRole)
        msg.addButton(QMessageBox.StandardButton.Ok)
        msg.exec()
        if msg.clickedButton() == open_btn:
            folder = str(path.parent)
            if sys.platform == "win32":
                subprocess.run(["explorer", folder], check=False)
            else:
                subprocess.run(["xdg-open", folder], check=False)
