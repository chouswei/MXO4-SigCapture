"""Horizontal strip of four channel cells."""

from __future__ import annotations

from PySide6.QtWidgets import QHBoxLayout, QWidget

from mxo4_sigcapture.apps.gui import theme
from mxo4_sigcapture.apps.gui.widgets.channel_cell import ChannelCell


class ChannelStrip(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedHeight(theme.CHANNEL_STRIP_HEIGHT)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        self._cells = [ChannelCell(i) for i in range(1, 5)]
        for cell in self._cells:
            layout.addWidget(cell, stretch=1)

    @property
    def cells(self) -> list[ChannelCell]:
        return self._cells
