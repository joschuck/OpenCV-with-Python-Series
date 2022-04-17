"""
GUI dialog helpers
"""
from typing import Optional

import cv2
from PySide6.QtWidgets import QFileDialog, QWidget


def open_image_dialog(parent: Optional[QWidget] = None):
    """Open image dialog."""
    image_path, _ = QFileDialog.getOpenFileName(
        parent, "Load Image", filter="Image Files (*.tiff *.png *.jpeg *.jpg *.bmp)"
    )

    if image_path:
        return cv2.imread(image_path, 0)

    return None
