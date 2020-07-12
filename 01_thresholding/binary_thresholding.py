# -*- coding: utf-8 -*-
import sys

import cv2
import numpy as np
from PySide2.QtCore import Qt
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QApplication, QComboBox, QWidget, QLabel, QVBoxLayout, QSlider, QPushButton, QFileDialog


class ThresholdingGui(QWidget):
    titles = [
        'Original Image',
        'THRESH_BINARY',
        'THRESH_BINARY_INV',
        'THRESH_TRUNC',
        'THRESH_TOZERO',
        'THRESH_TOZERO_INV',
    ]

    image: np.ndarray

    def __init__(self):
        super(ThresholdingGui, self).__init__()

        self.setWindowTitle('OpenCV Binary Thresholding')

        open_image_btn = QPushButton('Open Image', self)
        open_image_btn.clicked.connect(self.open_image)

        self.method_combobox = QComboBox()
        for title in self.titles:
            self.method_combobox.addItem(title)
        self.method_combobox.currentIndexChanged.connect(self.update_preview)

        self.threshold_label = QLabel('Threshold Value: 127')

        self.threshold_slider = QSlider()
        self.threshold_slider.setOrientation(Qt.Horizontal)
        self.threshold_slider.setTickPosition(QSlider.TicksBelow)
        self.threshold_slider.setTickInterval(10)
        self.threshold_slider.setMinimum(0)
        self.threshold_slider.setMaximum(255)
        self.threshold_slider.setValue(127)
        self.threshold_slider.valueChanged.connect(self.update_preview)

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
        image_path, _ = QFileDialog.getOpenFileName(self, "Load Image", filter="Image Files (*.tiff *.png *.jpeg *.jpg *.bmp)")
        if image_path:
            self.image = cv2.imread(image_path, 0)
            self.update_preview()

    def update_preview(self):
        method_idx = self.method_combobox.currentIndex()
        threshold = self.threshold_slider.value()

        self.threshold_label.setText(f"Threshold value: {threshold}")

        if method_idx == 0:
            th = self.image
        elif method_idx == 1:
            ret, th = cv2.threshold(self.image, threshold, 255, cv2.THRESH_BINARY)
        elif method_idx == 2:
            ret, th = cv2.threshold(self.image, threshold, 255, cv2.THRESH_BINARY_INV)
        elif method_idx == 3:
            ret, th = cv2.threshold(self.image, threshold, 255, cv2.THRESH_TRUNC)
        elif method_idx == 4:
            ret, th = cv2.threshold(self.image, threshold, 255, cv2.THRESH_TOZERO)
        elif method_idx == 5:
            ret, th = cv2.threshold(self.image, threshold, 255, cv2.THRESH_TOZERO_INV)
        elif method_idx == 6:
            th = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        elif method_idx == 7:
            th = cv2.adaptiveThreshold(self.image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)


        image_h, image_w = th.shape
        q_img = QImage(th.data, image_w, image_h, image_w, QImage.Format_Indexed8)
        self.image_label.setPixmap(QPixmap.fromImage(q_img))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ThresholdingGui()
    ex.show()
    sys.exit(app.exec_())


