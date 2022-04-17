"""
Binary thresholding demonstration.
"""
# pylint: disable=R0801

import cv2
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QComboBox,
    QLabel,
    QSlider,
    QVBoxLayout,
)

from src.util.dialog import open_image_dialog


class BinaryThresholding(QWidget):
    """BinaryThresholding widget."""

    titles = [
        "Original Image",
        "THRESH_BINARY",
        "THRESH_BINARY_INV",
        "THRESH_TRUNC",
        "THRESH_TOZERO",
        "THRESH_TOZERO_INV",
    ]

    image: np.ndarray

    def __init__(self):
        super().__init__()

        self.setWindowTitle("OpenCV Binary Thresholding")

        open_image_btn = QPushButton("Open Image", self)
        open_image_btn.clicked.connect(self.open_image)

        self.method_combobox = QComboBox()
        for title in self.titles:
            self.method_combobox.addItem(title)
        self.method_combobox.currentIndexChanged.connect(self.update_image)

        self.threshold_label = QLabel("Threshold Value: 127")

        self.threshold_slider = QSlider()
        self.threshold_slider.setOrientation(Qt.Horizontal)
        self.threshold_slider.setTickPosition(QSlider.TicksBelow)
        self.threshold_slider.setTickInterval(10)
        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(255)
        self.threshold_slider.setValue(127)
        self.threshold_slider.valueChanged.connect(self.update_image)

        self.image_label = QLabel()
        self.image = np.tile(np.arange(256, dtype=np.uint8).repeat(2), (512, 1))
        q_img = QImage(self.image.data, 512, 512, 512, QImage.Format_Indexed8)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(open_image_btn)
        layout.addWidget(self.method_combobox)
        layout.addWidget(self.threshold_label)
        layout.addWidget(self.threshold_slider)
        layout.addWidget(self.image_label)

        # Set dialog layout
        self.setLayout(layout)

    def open_image(self):
        """Shows a file dialog and displays the selected image."""
        image = open_image_dialog()
        if image:
            self.image = image
            self.update_image()

    def update_image(self):
        """Updates the widget's image."""
        method_idx = self.method_combobox.currentIndex()
        threshold = self.threshold_slider.value()

        self.threshold_label.setText(f"Threshold value: {threshold}")
        if method_idx == 1:
            _, image = cv2.threshold(self.image, threshold, 255, cv2.THRESH_BINARY)
        elif method_idx == 2:
            _, image = cv2.threshold(self.image, threshold, 255, cv2.THRESH_BINARY_INV)
        elif method_idx == 3:
            _, image = cv2.threshold(self.image, threshold, 255, cv2.THRESH_TRUNC)
        elif method_idx == 4:
            _, image = cv2.threshold(self.image, threshold, 255, cv2.THRESH_TOZERO)
        elif method_idx == 5:
            _, image = cv2.threshold(self.image, threshold, 255, cv2.THRESH_TOZERO_INV)
        elif method_idx == 6:
            image = cv2.adaptiveThreshold(
                self.image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
            )
        elif method_idx == 7:
            image = cv2.adaptiveThreshold(
                self.image,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11,
                2,
            )
        else:
            image = self.image

        image_h, image_w = image.shape
        q_img = QImage(image.data, image_w, image_h, image_w, QImage.Format_Indexed8)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))
