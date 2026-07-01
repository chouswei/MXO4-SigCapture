"""Matplotlib graticule plot with scope-style readback overlay."""

from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget

from mxo4_sigcapture.apps.gui import theme
from mxo4_sigcapture.config.acquire import AcquireReadback
from mxo4_sigcapture.formatting.units import format_points, format_sample_rate, format_seconds

if TYPE_CHECKING:
    from mxo4_sigcapture.capture.fetch import ChannelWaveform
    from mxo4_sigcapture.config.app import AppConfig


class _ScopeReadbackOverlay(QFrame):
    """Top-right readback stack, scope-style."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        mono = (
            f"font-family: {theme.MONO_FAMILY}; font-size: 11pt; "
            f"color: {theme.TEXT}; background: transparent;"
        )
        self.setStyleSheet(
            f"background: {theme.PANEL}; border: 1px solid {theme.BORDER}; "
            f"border-radius: 4px; padding: 4px 8px;"
        )
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(1)
        self.srat = QLabel("SRAT: —")
        self.poin = QLabel("POIN: —")
        self.scal = QLabel("SCAL: —")
        for lbl in (self.srat, self.poin, self.scal):
            lbl.setStyleSheet(mono)
            layout.addWidget(lbl)
        self.adjustSize()

    def update_readback(self, rb: AcquireReadback | None) -> None:
        if rb is None:
            self.srat.setText("SRAT: —")
            self.poin.setText("POIN: —")
            self.scal.setText("SCAL: —")
        else:
            self.srat.setText(f"SRAT: {format_sample_rate(rb.sample_rate_hz)}")
            self.poin.setText(f"POIN: {format_points(rb.record_length)}")
            self.scal.setText(f"SCAL: {format_seconds(rb.time_scale_s_per_div, per_div=True)}")
        self.adjustSize()


class GraticulePlot(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._canvas = None
        self._fig = None
        self._ax = None
        self._overlay = _ScopeReadbackOverlay(self)
        self._init_canvas()

    def _init_canvas(self) -> None:
        try:
            from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
            from matplotlib.figure import Figure
        except ImportError:
            from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg  # type: ignore[no-redef]
            from matplotlib.figure import Figure

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self._fig = Figure(figsize=(8, 5), facecolor=theme.BG)
        self._ax = self._fig.add_subplot(111)
        self._style_axes()
        self._canvas = FigureCanvasQTAgg(self._fig)
        layout.addWidget(self._canvas)
        self._draw_grid()
        self._position_overlay()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._position_overlay()

    def _position_overlay(self) -> None:
        margin = 10
        self._overlay.adjustSize()
        self._overlay.move(
            max(margin, self.width() - self._overlay.width() - margin),
            margin,
        )
        self._overlay.raise_()

    def update_readback(self, rb: AcquireReadback | None) -> None:
        self._overlay.update_readback(rb)
        self._position_overlay()

    def _style_axes(self) -> None:
        if self._ax is None:
            return
        self._ax.set_facecolor(theme.BG)
        self._ax.tick_params(colors=theme.TEXT)
        for spine in self._ax.spines.values():
            spine.set_color(theme.BORDER)
        self._ax.xaxis.label.set_color(theme.TEXT)
        self._ax.yaxis.label.set_color(theme.TEXT)

    def clear(self) -> None:
        if self._ax is None:
            return
        self._ax.clear()
        self._style_axes()
        self._draw_grid()
        if self._canvas:
            self._canvas.draw_idle()

    def _draw_grid(self) -> None:
        if self._ax is None:
            return
        for i in range(11):
            alpha = 0.6 if i == 5 else 0.25
            self._ax.axvline(i - 5, color=theme.BORDER, alpha=alpha, linewidth=0.5)
        for i in range(9):
            alpha = 0.6 if i == 4 else 0.25
            self._ax.axhline(i - 4, color=theme.BORDER, alpha=alpha, linewidth=0.5)

    def plot_capture(
        self,
        waveforms: list[ChannelWaveform],
        config: AppConfig | None = None,
    ) -> None:
        if self._ax is None or self._canvas is None:
            return
        self._ax.clear()
        self._style_axes()
        self._draw_grid()
        if not waveforms:
            self._canvas.draw_idle()
            self._position_overlay()
            return

        ref = waveforms[0]
        t_span = ref.header.x_stop_s - ref.header.x_start_s
        self._ax.set_xlim(ref.header.x_start_s, ref.header.x_stop_s)

        ymax = 0.0
        for w in waveforms:
            ymax = max(ymax, float(abs(w.y).max()) if len(w.y) else 0)
        self._ax.set_ylim(-ymax * 1.2 if ymax else -1, ymax * 1.2 if ymax else 1)

        if config:
            ref_pct = config.horizontal.reference_percent / 100.0
            trig_t = ref.header.x_start_s + ref_pct * t_span
            self._ax.axvline(trig_t, color=theme.ACCENT, linestyle="--", linewidth=1.2)

        legends: list[str] = []
        for w in waveforms:
            colour = theme.CHANNEL_COLOURS.get(w.channel, "white")
            lbl = theme.CHANNEL_LABELS.get(w.channel, f"C{w.channel}")
            ch_cfg = next((c for c in (config.channels if config else []) if c.channel == w.channel), None)
            scale = f" {ch_cfg.scale_v_per_div}V/div" if ch_cfg else ""
            coup = f" {ch_cfg.coupling.value}" if ch_cfg else ""
            clip = " [CLIP]" if w.clipped else ""
            self._ax.plot(w.time, w.y, color=colour, linewidth=0.8)
            legends.append(f"{lbl}{scale}{coup}{clip}")

        self._ax.set_xlabel("Time (s)")
        self._ax.set_ylabel("Voltage (V)")
        if legends:
            self._ax.legend(
                legends,
                loc="upper left",
                facecolor=theme.PANEL,
                edgecolor=theme.BORDER,
                labelcolor=theme.TEXT,
                fontsize=8,
            )
        self._canvas.draw_idle()
        self._position_overlay()
