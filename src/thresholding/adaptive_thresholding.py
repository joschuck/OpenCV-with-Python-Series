"""
Adaptive thresholding demonstration
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
from src.util.math import round_up_to_odd


class AdaptiveThresholding(QWidget):
    """AdaptiveThresholding"""

    titles = ["Original Image", "ADAPTIVE_THRESH_MEAN_C", "ADAPTIVE_THRESH_GAUSSIAN_C"]
    image: np.ndarray

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Adaptive Thresholding")

        open_image_btn = QPushButton("Open Image", self)
        open_image_btn.clicked.connect(self.open_image)

        self.method_combobox = QComboBox()
        for title in self.titles:
            self.method_combobox.addItem(title)
        self.method_combobox.currentIndexChanged.connect(self.update_image)

        self.block_size_label = QLabel(f"Block Size: {self.block_size}")

        self.block_size_slider = QSlider()
        self.block_size_slider.setOrientation(Qt.Horizontal)
        self.block_size_slider.setTickPosition(QSlider.TicksBelow)
        self.block_size_slider.setMinimum(3)
        self.block_size_slider.setMaximum(255)
        self.block_size_slider.setTickInterval(2)
        self.block_size_slider.setSingleStep(2)
        self.block_size_slider.setValue(11)
        self.block_size_slider.valueChanged.connect(self.block_size)

        self.c_constant_label = QLabel(f"C constant: {self.c_constant}")

        self.c_constant_slider = QSlider()
        self.c_constant_slider.setOrientation(Qt.Horizontal)
        self.c_constant_slider.setTickPosition(QSlider.TicksBelow)
        self.c_constant_slider.setMinimum(0)
        self.c_constant_slider.setMaximum(100)
        self.c_constant_slider.setValue(2)
        self.c_constant_slider.valueChanged.connect(self.c_constant)

        self.image_label = QLabel()
        self.image = np.tile(np.arange(256, dtype=np.uint8).repeat(2), (512, 1))
        q_img = QImage(self.image.data, 512, 512, 512, QImage.Format_Indexed8)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

        # Create layout and add widgets
        layout = QVBoxLayout()
        layout.addWidget(open_image_btn)
        layout.addWidget(self.method_combobox)
        layout.addWidget(self.block_size_label)
        layout.addWidget(self.block_size_slider)
        layout.addWidget(self.c_constant_label)
        layout.addWidget(self.c_constant_slider)
        layout.addWidget(self.image_label)

        # Set dialog layout
        self.setLayout(layout)

    def update_image(self):
        """Updates the widget's image."""
        method_idx = self.method_combobox.currentIndex()

        block_size = self.block_size_slider.value()
        c_constant = self.c_constant_slider.value()

        if method_idx == 1:
            image = cv2.adaptiveThreshold(
                self.image,
                255,
                cv2.ADAPTIVE_THRESH_MEAN_C,
                cv2.THRESH_BINARY,
                block_size,
                c_constant,
            )
        elif method_idx == 2:
            image = cv2.adaptiveThreshold(
                self.image,
                255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                block_size,
                c_constant,
            )
        else:
            image = self.image

        image_h, image_w = image.shape
        q_img = QImage(image.data, image_w, image_h, image_w, QImage.Format_Indexed8)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def open_image(self):
        """Shows a file dialog and displays the selected image."""
        image = open_image_dialog()
        if image is not None:
            self.image = image
            self.update_image()

    def block_size(self, block_size):
        """Sets the block size."""
        block_size = round_up_to_odd(block_size)
        self.block_size_slider.setValue(block_size)
        self.block_size_label.setText(f"Block size: {self.block_size_slider.value()}")
        self.update_image()

    def c_constant(self, c_constant):
        """Sets the c constant."""
        self.c_constant_slider.setValue(c_constant)
        self.c_constant_label.setText(f"C constant: {self.c_constant_slider.value()}")
        self.update_image()
