"""MXO4 SigCapture GUI entry point."""

from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    try:
        from PySide6.QtWidgets import QApplication
    except ImportError:
        print("PySide6 required: pip install 'mxo4-sigcapture[gui]'", file=sys.stderr)
        return 1

    from mxo4_sigcapture.apps.gui.main_window import MainWindow

    app = QApplication(argv or sys.argv)
    app.setApplicationName("MXO4 SigCapture")
    win = MainWindow()
    win.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
