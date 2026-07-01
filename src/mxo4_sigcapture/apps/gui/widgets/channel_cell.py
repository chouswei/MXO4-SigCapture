"""Compact inline channel control cell."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractSpinBox,
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from mxo4_sigcapture.apps.gui import theme
from mxo4_sigcapture.config.vertical import ChannelConfig, Coupling, Impedance
from mxo4_sigcapture.formatting.units import format_volts, format_volts_parts

SCALE_STEPS = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10]

_IMPEDANCE_LABELS: dict[Impedance, str] = {
    Impedance.FIFTY: "50 Ω",
    Impedance.ONE_MEG: "1 MΩ",
}

_CELL_FONT = f"font-size: {theme.CHANNEL_BODY_PT}pt;"
_HEADER_FONT = f"font-size: {theme.CHANNEL_HEADER_PT}pt; font-weight: bold;"
_VALUE_FONT = (
    f"font-size: {theme.CHANNEL_SCALE_VALUE_PT}pt; font-weight: bold; "
    f"font-family: {theme.MONO_FAMILY};"
)
_UNIT_FONT = f"font-size: {theme.CHANNEL_SCALE_UNIT_PT}pt; color: {theme.TEXT_DIM};"
_CTRL_H = 28
_BTN_W = 24
_ROW_H = 40


class _VoltRow:
    """Hidden spinbox + scope-style − | value | + readout row."""

    def __init__(
        self,
        *,
        tooltip: str,
        less_tip: str,
        more_tip: str,
        per_div: bool,
        initial: float,
        spin_range: tuple[float, float],
        decimals: int = 3,
        on_change,
    ) -> None:
        self.per_div = per_div
        self._on_change = on_change
        self.spin = QDoubleSpinBox()
        self.spin.setRange(spin_range[0], spin_range[1])
        self.spin.setDecimals(decimals)
        self.spin.setValue(initial)
        self.spin.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spin.hide()
        self.value = QLabel()
        self.value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.value.setStyleSheet(f"color: {theme.TEXT}; {_VALUE_FONT}")
        self.unit = QLabel()
        self.unit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.unit.setStyleSheet(_UNIT_FONT)
        readout = QWidget()
        readout.setMinimumHeight(_ROW_H)
        readout.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        readout.setToolTip(tooltip)
        readout_layout = QVBoxLayout(readout)
        readout_layout.setContentsMargins(0, 0, 0, 0)
        readout_layout.setSpacing(0)
        readout_layout.addWidget(self.value)
        readout_layout.addWidget(self.unit)
        self.less = QPushButton("−")
        self.less.setFixedSize(_BTN_W, _ROW_H)
        self.less.setToolTip(less_tip)
        self.more = QPushButton("+")
        self.more.setFixedSize(_BTN_W, _ROW_H)
        self.more.setToolTip(more_tip)
        self.layout = QHBoxLayout()
        self.layout.setSpacing(2)
        self.layout.addWidget(self.less)
        self.layout.addWidget(readout, stretch=1)
        self.layout.addWidget(self.more)
        self.spin.valueChanged.connect(self._on_change)
        self.update_label()

    def update_label(self) -> None:
        value, unit = format_volts_parts(self.spin.value(), per_div=self.per_div)
        self.value.setText(value)
        self.unit.setText(unit)


class ChannelCell(QFrame):
    changed = Signal()

    def __init__(self, channel: int) -> None:
        super().__init__()
        self.channel = channel
        self.setMinimumWidth(theme.CHANNEL_CELL_MIN_WIDTH)
        if theme.CHANNEL_CELL_MAX_WIDTH > 0:
            self.setMaximumWidth(theme.CHANNEL_CELL_MAX_WIDTH)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        colour = theme.CHANNEL_COLOURS[channel]
        header = QLabel(theme.CHANNEL_LABELS[channel])
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet(f"color: {colour}; {_HEADER_FONT}")
        self._enabled = QCheckBox("On")
        self._enabled.setStyleSheet(_CELL_FONT)
        self._enabled.setChecked(channel == 1)
        self._scale = _VoltRow(
            tooltip="Vertical scale (volts per division)",
            less_tip="Less V/div (finer scale, 1-2-5-10 steps)",
            more_tip="More V/div (coarser scale, 1-2-5-10 steps)",
            per_div=True,
            initial=0.5 if channel == 1 else 1.0,
            spin_range=(0.001, 100),
            on_change=self._on_scale_changed,
        )
        self._offset = _VoltRow(
            tooltip="Vertical offset (volts)",
            less_tip="Decrease offset by one division",
            more_tip="Increase offset by one division",
            per_div=False,
            initial=0.0,
            spin_range=(-1000, 1000),
            on_change=self._on_offset_changed,
        )
        self._scale.less.clicked.connect(self._step_scale_down)
        self._scale.more.clicked.connect(self._step_scale_up)
        self._offset.less.clicked.connect(self._offset_step_down)
        self._offset.more.clicked.connect(self._offset_step_up)
        self._coupling = QComboBox()
        self._coupling.addItems([c.value for c in Coupling])
        self._coupling.setMinimumHeight(_CTRL_H)
        self._coupling.setStyleSheet(_CELL_FONT)
        self._coupling.setToolTip("Input coupling")
        self._impedance = QComboBox()
        for imp in Impedance:
            self._impedance.addItem(_IMPEDANCE_LABELS[imp], imp.value)
        self._impedance.setMinimumHeight(_CTRL_H)
        self._impedance.setStyleSheet(_CELL_FONT)
        self._impedance.setToolTip("Input impedance")
        self._overload = QLabel("")
        self._overload.setStyleSheet(f"color: {theme.WARNING}; font-size: {theme.CHANNEL_BODY_PT}pt;")
        self._overload.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(3)
        layout.addWidget(header)
        layout.addWidget(self._enabled)
        layout.addLayout(self._scale.layout)
        layout.addLayout(self._offset.layout)
        layout.addWidget(self._coupling)
        layout.addWidget(self._impedance)
        layout.addWidget(self._overload)
        self._enabled.toggled.connect(self._emit)
        self._coupling.currentTextChanged.connect(self._emit)
        self._impedance.currentIndexChanged.connect(self._emit)
        self._update_enabled_style()

    def _on_scale_changed(self) -> None:
        self._scale.update_label()
        self._emit()

    def _on_offset_changed(self) -> None:
        self._offset.update_label()
        self._emit()

    def _emit(self) -> None:
        self._update_enabled_style()
        self.changed.emit()

    def _update_enabled_style(self) -> None:
        on = self._enabled.isChecked()
        colour = theme.CHANNEL_COLOURS[self.channel]
        border = colour if on else theme.BORDER
        bg = theme.PANEL if on else "#1a1a1a"
        self.setStyleSheet(
            f"ChannelCell {{ border: 2px solid {border}; border-radius: 6px; background: {bg}; }}"
        )

    def _step_scale_down(self) -> None:
        v = self._scale.spin.value()
        below = [s for s in SCALE_STEPS if s < v - 1e-9]
        if below:
            self._scale.spin.setValue(below[-1])

    def _step_scale_up(self) -> None:
        v = self._scale.spin.value()
        above = [s for s in SCALE_STEPS if s > v + 1e-9]
        if above:
            self._scale.spin.setValue(above[0])

    def _offset_step_down(self) -> None:
        self._offset.spin.setValue(self._offset.spin.value() - self._scale.spin.value())

    def _offset_step_up(self) -> None:
        self._offset.spin.setValue(self._offset.spin.value() + self._scale.spin.value())

    def _impedance_value(self) -> Impedance:
        raw = self._impedance.currentData()
        return Impedance(raw) if raw else Impedance.FIFTY

    def to_config(self) -> ChannelConfig:
        return ChannelConfig(
            channel=self.channel,
            enabled=self._enabled.isChecked(),
            scale_v_per_div=self._scale.spin.value(),
            offset_v=self._offset.spin.value(),
            coupling=Coupling(self._coupling.currentText()),
            impedance=self._impedance_value(),
        )

    def from_config(self, cfg: ChannelConfig) -> None:
        self._enabled.setChecked(cfg.enabled)
        self._scale.spin.setValue(cfg.scale_v_per_div)
        self._offset.spin.setValue(cfg.offset_v)
        self._coupling.setCurrentText(cfg.coupling.value)
        idx = self._impedance.findData(cfg.impedance.value)
        if idx >= 0:
            self._impedance.setCurrentIndex(idx)
        self._scale.update_label()
        self._offset.update_label()
        self._update_enabled_style()

    def set_overload(self, clipped: bool) -> None:
        self._overload.setText("CLIP" if clipped else "")

    def scale_label(self) -> str:
        return format_volts(self._scale.spin.value(), per_div=True)
