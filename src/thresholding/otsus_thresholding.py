"""
Otsu's thresholding widget
"""
# pylint: disable=R0801

import cv2
import numpy as np

from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QComboBox,
    QLabel,
    QVBoxLayout,
)

from src.util.dialog import open_image_dialog


class OtsusThresholding(QWidget):
    """OtsusThresholding"""

    image: np.ndarray

    titles = ["Original Image", "THRESH_BINARY + cv2.THRESH_OTSU"]

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Otsu's Thresholding")

        open_image_btn = QPushButton("Open Image", self)
        open_image_btn.clicked.connect(self.open_image)

        self.method_combobox = QComboBox()
        for title in self.titles:
            self.method_combobox.addItem(title)
        self.method_combobox.currentIndexChanged.connect(self.update_image)

        self.threshold_label = QLabel("Threshold calculated: -")

        self.image_label = QLabel()

        self.image = np.tile(np.arange(256, dtype=np.uint8).repeat(2), (512, 1))
        q_img = QImage(self.image.data, 512, 512, 512, QImage.Format_Indexed8)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

        layout = QVBoxLayout()
        layout.addWidget(open_image_btn)
        layout.addWidget(self.method_combobox)
        layout.addWidget(self.threshold_label)
        layout.addWidget(self.image_label)

        self.setLayout(layout)

    def open_image(self):
        """Shows a file dialog and displays the selected image."""
        image = open_image_dialog()
        if image is not None:
            self.image = image
            self.update_image()

    def update_image(self):
        """Updates the widget's image."""
        method_idx = self.method_combobox.currentIndex()

        if method_idx == 0:
            ret, image = "-", self.image
        elif method_idx == 1:
            ret, image = cv2.threshold(
                self.image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )
        else:
            return

        self.threshold_label.setText(f"Threshold calculated: {ret}")

        image_h, image_w = image.shape
        q_img = QImage(image.data, image_w, image_h, image_w, QImage.Format_Indexed8)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))
