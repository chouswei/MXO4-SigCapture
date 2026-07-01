"""Connection bar widget."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget

from mxo4_sigcapture.apps.gui import theme


class ConnectionBar(QWidget):
    connect_clicked = Signal()
    disconnect_clicked = Signal()

    def __init__(self) -> None:
        super().__init__()
        layout = QHBoxLayout(self)
        self.resource_edit = QLineEdit("TCPIP0::localhost::hislip0::INSTR")
        self.resource_edit.setMinimumWidth(320)
        self.connect_btn = QPushButton("Connect")
        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.setEnabled(False)
        self.idn_label = QLabel("")
        self.idn_label.setStyleSheet(f"color: {theme.TEXT_DIM}; font-family: {theme.MONO_FAMILY};")
        self.remote_banner = QLabel("REMOTE")
        self.remote_banner.setStyleSheet(
            f"background: {theme.REMOTE}; color: white; padding: 2px 8px; font-weight: bold;"
        )
        self.remote_banner.hide()
        self.error_lamp = QPushButton("OK")
        self.error_lamp.setStyleSheet(f"color: {theme.TEXT};")
        self.error_lamp.setFlat(True)
        layout.addWidget(QLabel("VISA:"))
        layout.addWidget(self.resource_edit)
        layout.addWidget(self.connect_btn)
        layout.addWidget(self.disconnect_btn)
        layout.addWidget(self.remote_banner)
        layout.addWidget(self.idn_label, stretch=1)
        layout.addWidget(self.error_lamp)
        self.connect_btn.clicked.connect(self.connect_clicked.emit)
        self.disconnect_btn.clicked.connect(self.disconnect_clicked.emit)

    def set_connected(self, connected: bool, idn: str = "") -> None:
        self.connect_btn.setEnabled(not connected)
        self.disconnect_btn.setEnabled(connected)
        self.resource_edit.setEnabled(not connected)
        self.remote_banner.setVisible(connected)
        self.idn_label.setText(idn if connected else "")

    def resource(self) -> str:
        return self.resource_edit.text().strip()

    def set_error_state(self, has_error: bool) -> None:
        if has_error:
            self.error_lamp.setText("ERR")
            self.error_lamp.setStyleSheet(f"color: {theme.ERROR}; font-weight: bold;")
        else:
            self.error_lamp.setText("OK")
            self.error_lamp.setStyleSheet(f"color: {theme.TEXT};")
