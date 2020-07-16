# -*- coding: utf-8 -*-
import sys

import cv2
import numpy as np

from PySide2.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QGridLayout

from util.image import to_q_pixmap
from util.webcam import Webcam

class ThresholdingGui(QWidget):
    width = 480
    height = 480

    def __init__(self):
        super(ThresholdingGui, self).__init__()

        self.webcam = Webcam(0, self.width, self.height)
        self.webcam.acquired_image_signal.connect(self.set_image)

        self.setWindowTitle('Fourier Transform')

        # Start webcam button
        self.start_webcam_button = QPushButton('Start Webcam')
        self.start_webcam_button.clicked.connect(self.start_webcam)

        # Open image button
        self.open_image_button = QPushButton('Open Image', self)
        self.open_image_button.clicked.connect(self.open_image)

        self.src_image_label = QLabel()
        self.dst_image_label = QLabel()

        # Create layout and add widgets
        layout = QGridLayout()
        layout.addWidget(self.start_webcam_button, 0, 0, 1, 2)
        layout.addWidget(self.open_image_button, 1, 0, 1, 2)
        layout.addWidget(self.src_image_label, 2, 0)
        layout.addWidget(self.dst_image_label, 2, 1)

        # Set dialog layout
        self.setLayout(layout)

    def __exit__(self):
        if self.isRunning():
            self.webcam.stop()

    def start_webcam(self):
        # Reassign functionality to pause the webcam on demand
        self.start_webcam_button.setText('Pause / Play')
        self.start_webcam_button.clicked.disconnect()
        self.start_webcam_button.clicked.connect(self.webcam.toggle_pause)
        self.webcam.start()

    def open_image(self):
        if self.webcam.isRunning():
            self.webcam.stop()
            print("stop")
            self.start_webcam_button.setText('Start Webcam')
            self.start_webcam_button.clicked.disconnect()
            self.start_webcam_button.clicked.connect(self.start_webcam)

        image_path, _ = QFileDialog.getOpenFileName(self, "Load Image", filter="Image Files (*.tiff *.png *.jpeg *.jpg *.bmp)")
        if image_path:
            src_image = cv2.imread(image_path)
            self.set_image(src_image)

    def set_image(self, image):
        print(image.shape)
        self.src_image_label.setPixmap(to_q_pixmap(image))

        # Compute phase, magnitude or spectrum
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        f = np.fft.fft2(gray)
        fshift = np.fft.fftshift(f)

        fshift = np.ascontiguousarray(fshift)

        magnitude_spectrum = np.log(np.abs(fshift))
        magnitude_spectrum *= (255.0 / magnitude_spectrum.max())
        magnitude_spectrum = magnitude_spectrum.astype(np.uint8)
        self.dst_image_label.setPixmap(to_q_pixmap(magnitude_spectrum))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ThresholdingGui()
    ex.show()
    sys.exit(app.exec_())
