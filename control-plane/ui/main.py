"""
ADRE Control Plane – PySide6 entry point.

Launches a classic early-2000s styled window that embeds the
Cytoscape.js canvas via QWebEngineView.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QFont, QColor, QPalette
from PySide6.QtWidgets import QApplication, QMainWindow, QStatusBar
from PySide6.QtWebEngineWidgets import QWebEngineView


UI_DIR = Path(__file__).resolve().parent


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("ADRE Control Plane  —  early-2000s edition")
        self.resize(1280, 800)

        # Force a darker classic palette so native chrome doesn't fight us
        pal = self.palette()
        pal.setColor(QPalette.Window, QColor(26, 26, 46))
        pal.setColor(QPalette.WindowText, QColor(200, 200, 208))
        pal.setColor(QPalette.Base, QColor(18, 18, 28))
        pal.setColor(QPalette.Text, QColor(200, 200, 208))
        self.setPalette(pal)

        self.view = QWebEngineView()
        index = UI_DIR / "index.html"
        self.view.setUrl(QUrl.fromLocalFile(str(index)))
        self.setCentralWidget(self.view)

        # Classic status bar
        sb = QStatusBar()
        sb.showMessage("ADRE ready  |  REA bridge: not connected  |  theme: early-2000s anti-slop")
        self.setStatusBar(sb)

        # Slightly chunky default font
        font = QFont("Tahoma", 9)
        self.setFont(font)


def main() -> None:
    # High-DPI is fine, but we still want the old-school look inside the page
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app = QApplication(sys.argv)
    app.setApplicationName("ADRE")
    app.setOrganizationName("ScrapYard")

    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
