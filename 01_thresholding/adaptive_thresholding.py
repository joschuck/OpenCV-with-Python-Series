# -*- coding: utf-8 -*-
import sys

import cv2
import numpy as np
from PySide2.QtCore import Qt
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QApplication, QComboBox, QWidget, QLabel, QVBoxLayout, QSlider, QPushButton, QFileDialog


def round_up_to_odd(number):
    return int(np.ceil(number) // 2 * 2 + 1)

class ThresholdingGui(QWidget):
    titles = [
        'Original Image',
        'ADAPTIVE_THRESH_MEAN_C',
        'ADAPTIVE_THRESH_GAUSSIAN_C'
    ]

    block_size = 11
    c_constant = 2

    image: np.ndarray

    def __init__(self):
        super(ThresholdingGui, self).__init__()

        self.setWindowTitle('Adaptive Thresholding')

        open_image_btn = QPushButton('Open Image', self)
        open_image_btn.clicked.connect(self.open_image)

        self.method_combobox = QComboBox()
        for title in self.titles:
            self.method_combobox.addItem(title)
        self.method_combobox.currentIndexChanged.connect(self.update_preview)

        self.block_size_label = QLabel(f"Block Size: {self.block_size}")

        self.block_size_slider = QSlider()
        self.block_size_slider.setOrientation(Qt.Horizontal)
        self.block_size_slider.setTickPosition(QSlider.TicksBelow)
        self.block_size_slider.setMinimum(3)
        self.block_size_slider.setMaximum(255)
        self.block_size_slider.setTickInterval(2)
        self.block_size_slider.setSingleStep(2)
        self.block_size_slider.setValue(self.block_size)
        self.block_size_slider.valueChanged.connect(self.set_block_size)

        self.c_constant_label = QLabel(f"C constant: {self.c_constant}")

        self.c_constant_slider = QSlider()
        self.c_constant_slider.setOrientation(Qt.Horizontal)
        self.c_constant_slider.setTickPosition(QSlider.TicksBelow)
        self.c_constant_slider.setMinimum(0)
        self.c_constant_slider.setMaximum(100)
        self.c_constant_slider.setValue(self.c_constant)
        self.c_constant_slider.valueChanged.connect(self.set_c_constant)

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

    def open_image(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "Load Image", filter="Image Files (*.tiff *.png *.jpeg *.jpg *.bmp)")
        if image_path:
            self.image = cv2.imread(image_path, 0)
            self.update_preview()

    def update_preview(self):
        method_idx = self.method_combobox.currentIndex()

        self.block_size_label.setText(f"Block size: {self.block_size}")

        if method_idx == 0:
            th = self.image
        elif method_idx == 1:
            th = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, self.block_size, self.c_constant)
        elif method_idx == 2:
            th = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, self.block_size, self.c_constant)

        image_h, image_w = th.shape
        q_img = QImage(th.data, image_w, image_h, image_w, QImage.Format_Indexed8)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))

    def set_block_size(self, block_size):
        self.block_size = round_up_to_odd(block_size)
        self.block_size_slider.setValue(self.block_size)
        self.block_size_label.setText(f"Block size: {self.block_size}")
        self.update_preview()

    def set_c_constant(self, c_constant):
        self.c_constant = c_constant
        self.c_constant_label.setText(f"C constant: {self.c_constant}")
        self.update_preview()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ThresholdingGui()
    ex.show()
    sys.exit(app.exec_())


