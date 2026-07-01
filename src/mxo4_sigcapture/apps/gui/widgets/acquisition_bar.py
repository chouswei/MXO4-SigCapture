"""Acquisition control bar with merged status."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from mxo4_sigcapture.apps.gui import theme


def _separator() -> QLabel:
    lbl = QLabel("│")
    lbl.setStyleSheet(f"color: {theme.BORDER}; padding: 0 4px;")
    return lbl


class AcquisitionBar(QWidget):
    run_clicked = Signal()
    stop_clicked = Signal()
    single_clicked = Signal()
    apply_clicked = Signal()
    save_clicked = Signal()
    cancel_clicked = Signal()

    def __init__(self) -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        self.run_btn = QPushButton("Run")
        self.run_btn.setEnabled(False)
        self.run_btn.setToolTip("Continuous acquire in v2")
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)
        self.single_btn = QPushButton("Single")
        self.single_btn.setEnabled(False)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setEnabled(False)
        self.apply_btn = QPushButton("Apply setup")
        self.save_btn = QPushButton("Save HDF5")
        self.save_btn.setEnabled(False)
        self.filename_preview = QLabel("")
        self.filename_preview.setStyleSheet(
            f"color: {theme.TEXT_DIM}; font-family: {theme.MONO_FAMILY}; font-size: 10px;"
        )
        self.state_label = QLabel("Ready")
        self.state_label.setStyleSheet(f"color: {theme.TEXT};")
        self.progress_label = QLabel("")
        self.progress_label.setStyleSheet(
            f"color: {theme.TEXT_DIM}; font-family: {theme.MONO_FAMILY}; font-size: 10px;"
        )
        for btn in (self.run_btn, self.stop_btn, self.single_btn):
            btn.setMinimumWidth(theme.TOOLBAR_BTN_PRIMARY_MIN_WIDTH)
        layout.addWidget(self.run_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.single_btn)
        layout.addWidget(self.cancel_btn)
        layout.addWidget(_separator())
        layout.addWidget(self.apply_btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(_separator())
        layout.addWidget(self.filename_preview, stretch=1)
        layout.addWidget(self.state_label)
        layout.addWidget(self.progress_label)
        self.run_btn.clicked.connect(self.run_clicked.emit)
        self.stop_btn.clicked.connect(self.stop_clicked.emit)
        self.single_btn.clicked.connect(self.single_clicked.emit)
        self.apply_btn.clicked.connect(self.apply_clicked.emit)
        self.save_btn.clicked.connect(self.save_clicked.emit)
        self.cancel_btn.clicked.connect(self.cancel_clicked.emit)

    def set_connected(self, connected: bool) -> None:
        self.stop_btn.setEnabled(connected)
        self.apply_btn.setEnabled(connected)

    def set_single_enabled(self, enabled: bool) -> None:
        self.single_btn.setEnabled(enabled)

    def set_busy(self, busy: bool) -> None:
        self.cancel_btn.setEnabled(busy)
        if busy:
            self.apply_btn.setEnabled(False)
            self.single_btn.setEnabled(False)
        else:
            self.apply_btn.setEnabled(self.stop_btn.isEnabled())

    def set_filename_preview(self, name: str) -> None:
        self.filename_preview.setText(name)

    def set_save_enabled(self, enabled: bool) -> None:
        self.save_btn.setEnabled(enabled)

    def set_state(self, text: str) -> None:
        self.state_label.setText(text)

    def set_progress(self, ch: int, total: int, elapsed_s: float = 0.0) -> None:
        if total <= 0:
            self.progress_label.setText("")
            return
        elapsed = f"  {elapsed_s:.1f}s" if elapsed_s else ""
        self.progress_label.setText(f"CH{ch}/{total}{elapsed}")
