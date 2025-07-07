#!/usr/bin/env python3
"""Image Tool with Drag-and-Drop (macOS-friendly)

This single script merges *dndmacos.py* and *main.py*.  
It keeps the original Tk app’s high-level layout / feature set
but is rewritten on **PySide6** so we can use a reliable, native
drag-and-drop area on macOS without tkdnd.

Key points
-----------
* When **no photos are selected**, the preview pane shows a dashed-border
  “Drop an image file here” box (taken from *dndmacos.py*).
* Files (or folders) may be:
  • dropped on that box, **or**  
  • chosen with the **Open Folder or Image** button.
* If the user opens one image → it shows full-size (fit-to-pane).  
  If several → it shows horizontal, scrollable thumbnails.
* The bottom row keeps the original three buttons:
  **Open Folder or Image · Operation · Convert**
* The **Operation** button pops up a small dialog where the user can
  pick “Operation 1/2/3” and press *Run* – matching the skeleton that
  was in *main.py*.  Fill in your own `operation_func_*` bodies.

PySide6 is the only external dependency:

    pip install PySide6 Pillow

"""

import sys, os
from pathlib import Path
from typing import Sequence

from PIL import Image, ImageQt
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QFileDialog,
    QVBoxLayout, QHBoxLayout, QScrollArea, QFrame, QMessageBox,
    QDialog, QComboBox, QStackedLayout
)

###############################################################################
# Constants
###############################################################################

THUMBNAIL_SIZE = QSize(100, 100)
SUPPORTED_FORMATS = (
    '.png', '.jpg', '.jpeg', '.gif', '.bmp',
    '.cr2', '.cr3', '.crw', '.arw', '.tif', '.tiff', '.webp', '.heic'
)


def is_image(path: str | os.PathLike) -> bool:
    return str(path).lower().endswith(SUPPORTED_FORMATS)

###############################################################################
# Drag-and-drop label (verbatim from dndmacos.py, but routed back to MainWindow)
###############################################################################


class ImageDropLabel(QLabel):
    """Dashed-border label that accepts local image files dropped from Finder."""

    def __init__(self, on_files_dropped, parent=None):
        super().__init__("Drop an image file here", parent)
        self._on_files_dropped = on_files_dropped
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setAcceptDrops(True)
        self.setMinimumSize(400, 250)
        self.setStyleSheet("border: 2px dashed #888; font-size: 18px;")

    # Qt drag-and-drop overrides ------------------------------------------------

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            if any(is_image(url.toLocalFile()) for url in event.mimeData().urls()):
                event.acceptProposedAction()

    def dropEvent(self, event):
        paths = [
            url.toLocalFile()
            for url in event.mimeData().urls()
            if url.isLocalFile()
        ]
        img_paths: list[str] = []
        for p in paths:
            if os.path.isdir(p):
                for entry in os.scandir(p):
                    if entry.is_file() and is_image(entry.path):
                        img_paths.append(entry.path)
            elif is_image(p):
                img_paths.append(p)

        if img_paths:
            self._on_files_dropped(img_paths)

###############################################################################
# Preview widget (stacked drag target <--> scroll area)
###############################################################################


class PreviewPane(QWidget):
    """Holds either the ImageDropLabel *or* the image scroll area."""

    def __init__(self, parent, on_files_dropped):
        super().__init__(parent)

        self._stack = QStackedLayout(self)
        self._drop_label = ImageDropLabel(on_files_dropped, self)
        self._stack.addWidget(self._drop_label)

        # Scroll area for thumbnails / single image
        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_content = QWidget()
        self._scroll_layout = QHBoxLayout(self._scroll_content)
        self._scroll_layout.setContentsMargins(10, 10, 10, 10)
        self._scroll_layout.setSpacing(10)
        self._scroll_area.setWidget(self._scroll_content)
        self._stack.addWidget(self._scroll_area)

        self.clear()  # start with drop label visible

    # -------------------------------------------------------------------------
    # Public helpers
    # -------------------------------------------------------------------------

    def clear(self):
        """Remove all image widgets and switch to drop label."""
        while self._scroll_layout.count():
            item = self._scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)  # drop reference
        self._stack.setCurrentWidget(self._drop_label)

    def show_images(self, paths: Sequence[str]):
        if not paths:
            self.clear()
            return

        self.clear()  # make sure pane is empty first, but keep scroll area

        if len(paths) == 1:
            # Single image – scale to fit scroll area width while keeping aspect
            img = Image.open(paths[0])
            # Use preview pane height as max height (~250)
            max_w, max_h = 800, 250
            img.thumbnail((max_w, max_h), Image.LANCZOS)
            qt_img = ImageQt.ImageQt(img)
            pix = QPixmap.fromImage(qt_img)
            lbl = QLabel()
            lbl.setPixmap(pix)
            self._scroll_layout.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignCenter)
        else:
            # Multiple thumbnails horizontal
            for p in paths:
                try:
                    img = Image.open(p)
                    img.thumbnail((THUMBNAIL_SIZE.width(), THUMBNAIL_SIZE.height()), Image.LANCZOS)
                    qt_img = ImageQt.ImageQt(img)
                    pix = QPixmap.fromImage(qt_img)
                    lbl = QLabel()
                    lbl.setPixmap(pix)
                    lbl.setFrameShape(QFrame.Shape.StyledPanel)
                    self._scroll_layout.addWidget(lbl)
                except Exception as exc:
                    print(f"Failed to load {p}: {exc}")

        self._stack.setCurrentWidget(self._scroll_area)

###############################################################################
# Operation popup dialog
###############################################################################


class OperationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Operation")
        self.setMinimumWidth(300)

        vbox = QVBoxLayout(self)

        self.combo = QComboBox()
        self.combo.addItems(["Operation 1", "Operation 2", "Operation 3"])
        vbox.addWidget(self.combo)

        btn_run = QPushButton("Run")
        btn_run.clicked.connect(self.run_selected)
        vbox.addWidget(btn_run)

    def run_selected(self):
        op = self.combo.currentText()
        if op == "Operation 1":
            operation_func_1()
        elif op == "Operation 2":
            operation_func_2()
        elif op == "Operation 3":
            operation_func_3()
        self.accept()

###############################################################################
# Main window
###############################################################################


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Tool")
        self.resize(800, 600)

        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)
        vbox.setContentsMargins(5, 5, 5, 5)
        vbox.setSpacing(5)

        # ---------------- Preview pane ----------------
        self.preview = PreviewPane(self, self.handle_files)
        vbox.addWidget(self.preview, stretch=1)

        # ---------------- Button row ------------------
        btn_row = QHBoxLayout()
        vbox.addLayout(btn_row)

        btn_open = QPushButton("Open Folder or Image")
        btn_open.clicked.connect(self.open_dialog)
        btn_row.addWidget(btn_open)

        btn_op = QPushButton("Operation")
        btn_op.clicked.connect(self.open_operation_dialog)
        btn_row.addWidget(btn_op)

        btn_convert = QPushButton("Convert")
        btn_convert.clicked.connect(self.convert)
        btn_row.addWidget(btn_convert)

        btn_row.addStretch()

    # ---------------------------------------------------------------------
    # Actions
    # ---------------------------------------------------------------------

    def open_dialog(self):
        paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Images",
            "",
            "Images (*.png *.jpg *.jpeg *.gif *.bmp *.tif *.tiff *.webp *.heic *.cr2 *.cr3 *.crw *.arw)"
        )
        self.handle_files(paths)

    def handle_files(self, paths: Sequence[str]):
        if not paths:
            self.preview.clear()
            return

        if len(paths) == 1 and os.path.isdir(paths[0]):
            # Folder dropped – collect images inside
            paths = [
                os.path.join(paths[0], f)
                for f in os.listdir(paths[0])
                if is_image(f)
            ]
        self.preview.show_images(paths)

    def open_operation_dialog(self):
        OperationDialog(self).exec()

    def convert(self):
        QMessageBox.information(self, "Convert", "Conversion started!")

###############################################################################
# Stub operation functions (fill in your own logic)
###############################################################################


def operation_func_1():
    print("Running operation 1")


def operation_func_2():
    print("Running operation 2")


def operation_func_3():
    print("Running operation 3")


###############################################################################
# Entrypoint
###############################################################################

def main():
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
