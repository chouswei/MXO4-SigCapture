"""Time / Acquire panel with progressive disclosure."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from mxo4_sigcapture.config.acquire import (
    AcquireConfig,
    AcquireType,
    InterpolationMode,
    RateMode,
)
from mxo4_sigcapture.config.horizontal import HorizontalConfig


class TimeAcquirePanel(QGroupBox):
    changed = Signal()

    def __init__(self) -> None:
        super().__init__("Time / Acquire")
        layout = QVBoxLayout(self)
        simple = QFormLayout()
        self._time_div = QDoubleSpinBox()
        self._time_div.setRange(1e-9, 1000)
        self._time_div.setDecimals(9)
        self._time_div.setValue(1e-3)
        self._time_div.setSuffix(" s/div")
        self._record_len = QSpinBox()
        self._record_len.setRange(1000, 1_000_000_000)
        self._record_len.setValue(100_000)
        self._sample_rate = QDoubleSpinBox()
        self._sample_rate.setRange(1, 20e9)
        self._sample_rate.setDecimals(0)
        self._sample_rate.setValue(1e9)
        self._sample_rate.setSuffix(" Sa/s")
        self._ref_pct = QDoubleSpinBox()
        self._ref_pct.setRange(0, 100)
        self._ref_pct.setValue(50)
        self._ref_pct.setSuffix(" %")
        simple.addRow("Time/div", self._time_div)
        simple.addRow("Record length", self._record_len)
        simple.addRow("Sample rate", self._sample_rate)
        simple.addRow("Ref %", self._ref_pct)
        layout.addLayout(simple)
        self._advanced_toggle = QCheckBox("Advanced")
        layout.addWidget(self._advanced_toggle)
        self._advanced = QWidget()
        adv_form = QFormLayout(self._advanced)
        self._acq_type = QComboBox()
        self._acq_type.addItems([t.value for t in AcquireType])
        self._interp = QComboBox()
        self._interp.addItems([i.value for i in InterpolationMode])
        self._poin_mode = QComboBox()
        self._poin_mode.addItems([m.value for m in RateMode])
        self._srat_mode = QComboBox()
        self._srat_mode.addItems([m.value for m in RateMode])
        adv_form.addRow("Acquire type", self._acq_type)
        adv_form.addRow("Interpolation", self._interp)
        adv_form.addRow("POIN mode", self._poin_mode)
        adv_form.addRow("SRAT mode", self._srat_mode)
        self._advanced.hide()
        layout.addWidget(self._advanced)
        self._advanced_toggle.toggled.connect(self._advanced.setVisible)
        for w in (
            self._time_div, self._record_len, self._sample_rate, self._ref_pct,
            self._acq_type, self._interp, self._poin_mode, self._srat_mode,
        ):
            if hasattr(w, "valueChanged"):
                w.valueChanged.connect(self.changed.emit)  # type: ignore[attr-defined]
            else:
                w.currentTextChanged.connect(self.changed.emit)  # type: ignore[attr-defined]

    def horizontal_config(self) -> HorizontalConfig:
        return HorizontalConfig(
            time_scale_s_per_div=self._time_div.value(),
            reference_percent=self._ref_pct.value(),
        )

    def acquire_config(self) -> AcquireConfig:
        return AcquireConfig(
            acquire_type=AcquireType.from_alias(self._acq_type.currentText()),
            interpolation=InterpolationMode(self._interp.currentText()),
            points_mode=RateMode(self._poin_mode.currentText()),
            record_length=self._record_len.value(),
            sample_rate_mode=RateMode(self._srat_mode.currentText()),
            sample_rate_hz=self._sample_rate.value(),
        )

    def from_configs(self, horiz: HorizontalConfig, acq: AcquireConfig) -> None:
        self._time_div.setValue(horiz.time_scale_s_per_div)
        self._ref_pct.setValue(horiz.reference_percent)
        self._record_len.setValue(acq.record_length)
        self._sample_rate.setValue(acq.sample_rate_hz)
        self._acq_type.setCurrentText(acq.acquire_type.value)
        self._interp.setCurrentText(acq.interpolation.value)
        self._poin_mode.setCurrentText(acq.points_mode.value)
        self._srat_mode.setCurrentText(acq.sample_rate_mode.value)
