"""Trigger configuration panel."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QPushButton,
    QVBoxLayout,
)

from mxo4_sigcapture.config.trigger import TriggerConfig, TriggerMode, TriggerSlope, TriggerSource


class TriggerPanel(QGroupBox):
    changed = Signal()
    find_level_clicked = Signal()

    def __init__(self) -> None:
        super().__init__("Trigger")
        layout = QVBoxLayout(self)
        form = QFormLayout()
        self._mode = QComboBox()
        self._mode.addItems([m.value for m in TriggerMode])
        self._mode.setCurrentText(TriggerMode.NORMAL.value)
        self._source = QComboBox()
        self._source.addItems([s.value for s in TriggerSource])
        self._level = QDoubleSpinBox()
        self._level.setRange(-100, 100)
        self._level.setDecimals(4)
        self._level.setSuffix(" V")
        self._slope = QComboBox()
        self._slope.addItems([s.value for s in TriggerSlope])
        form.addRow("Mode", self._mode)
        form.addRow("Source", self._source)
        form.addRow("Level", self._level)
        form.addRow("Slope", self._slope)
        layout.addLayout(form)
        self._find_btn = QPushButton("Find level")
        self._find_btn.clicked.connect(self.find_level_clicked.emit)
        layout.addWidget(self._find_btn)
        for w in (self._mode, self._source, self._level, self._slope):
            if hasattr(w, "currentTextChanged"):
                w.currentTextChanged.connect(self.changed.emit)  # type: ignore[attr-defined]
            else:
                w.valueChanged.connect(self.changed.emit)  # type: ignore[attr-defined]

    def to_config(self) -> TriggerConfig:
        return TriggerConfig(
            mode=TriggerMode(self._mode.currentText()),
            source=TriggerSource(self._source.currentText()),
            level_v=self._level.value(),
            slope=TriggerSlope(self._slope.currentText()),
        )

    def from_config(self, cfg: TriggerConfig) -> None:
        self._mode.setCurrentText(cfg.mode.value)
        self._source.setCurrentText(cfg.source.value)
        self._level.setValue(cfg.level_v)
        self._slope.setCurrentText(cfg.slope.value)
