#!/usr/bin/env python3
"""
Drag-and-drop image viewer using PySide 6.
Save as image_drop_viewer.py and run with:  python image_drop_viewer.py
"""
import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout
from PySide6.QtGui import QPixmap, Qt


class ImageDropLabel(QLabel):
    """A QLabel that accepts image files dropped from Finder."""

    IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".bmp", ".gif",
                  ".tif", ".tiff", ".webp", ".heic")

    def __init__(self):
        super().__init__("Drop an image file here")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAcceptDrops(True)
        self.setMinimumSize(400, 300)
        # Simple dashed border so the drop target is obvious
        self.setStyleSheet("border: 2px dashed #888; font-size: 18px;")

    # === Drag-and-Drop overrides ===========================================

    def dragEnterEvent(self, event):
        """Accept only local image files."""
        if event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            if url.isLocalFile() and Path(url.toLocalFile()).suffix.lower() in self.IMAGE_EXTS:
                event.acceptProposedAction()
                return
        event.ignore()

    def dropEvent(self, event):
        """Load and display the dropped image."""
        file_path = event.mimeData().urls()[0].toLocalFile()
        pix = QPixmap(file_path)
        if pix.isNull():
            self.setText("The dropped file is not a supported image 😕")
        else:
            self.setPixmap(pix.scaled(self.size(),
                                      Qt.AspectRatioMode.KeepAspectRatio,
                                      Qt.TransformationMode.SmoothTransformation))
        event.acceptProposedAction()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag-and-Drop Image Viewer")
        layout = QVBoxLayout(self)
        layout.addWidget(ImageDropLabel())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.resize(640, 480)
    win.show()
    sys.exit(app.exec())