"""SI-formatted readback bar (vertical stack for narrow dock)."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from mxo4_sigcapture.apps.gui import theme
from mxo4_sigcapture.config.acquire import AcquireReadback
from mxo4_sigcapture.formatting.units import format_points, format_sample_rate, format_seconds


class ReadbackBar(QWidget):
    def __init__(self) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)
        layout.setSpacing(2)
        mono = f"font-family: {theme.MONO_FAMILY}; color: {theme.TEXT}; font-size: 10px;"
        self.srat = QLabel("SRAT: —")
        self.poin = QLabel("POIN: —")
        self.scal = QLabel("SCAL: —")
        for lbl in (self.srat, self.poin, self.scal):
            lbl.setStyleSheet(mono)
            layout.addWidget(lbl)

    def update_readback(self, rb: AcquireReadback | None) -> None:
        if rb is None:
            self.srat.setText("SRAT: —")
            self.poin.setText("POIN: —")
            self.scal.setText("SCAL: —")
            return
        self.srat.setText(f"SRAT: {format_sample_rate(rb.sample_rate_hz)}")
        self.poin.setText(f"POIN: {format_points(rb.record_length)}")
        self.scal.setText(f"SCAL: {format_seconds(rb.time_scale_s_per_div, per_div=True)}")
