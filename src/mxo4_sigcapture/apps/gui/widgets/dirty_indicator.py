"""Dirty state indicator."""

from __future__ import annotations

from PySide6.QtWidgets import QLabel

from mxo4_sigcapture.apps.gui import theme


class DirtyIndicator(QLabel):
    def __init__(self) -> None:
        super().__init__("")
        self.set_dirty(False)

    def set_dirty(self, dirty: bool) -> None:
        if dirty:
            self.setText("Pending changes")
            self.setStyleSheet(f"color: {theme.WARNING}; font-weight: bold;")
        else:
            self.setText("Synced")
            self.setStyleSheet(f"color: {theme.TEXT_DIM};")
