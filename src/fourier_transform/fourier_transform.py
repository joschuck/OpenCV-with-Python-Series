"""
Fourier transform demonstration.
"""

import cv2
import numpy as np
from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QGridLayout,
)

from src.util.dialog import open_image_dialog
from src.util.image import to_q_pixmap
from src.util.webcam import Webcam


class FourierTransform(QWidget):
    """FourierTransform"""

    WIDTH = 480
    HEIGHT = 480

    def __init__(self):
        super().__init__()

        self.webcam = Webcam(0, self.WIDTH, self.HEIGHT)
        self.webcam.acquired_image_signal.connect(self.set_image)

        self.setWindowTitle("Fourier Transform")

        # Start webcam button
        self.start_webcam_button = QPushButton("Start Webcam")
        self.start_webcam_button.clicked.connect(self.start_webcam)

        # Open image button
        self.open_image_button = QPushButton("Open Image", self)
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

    # pylint: disable=invalid-name
    def closeEvent(self, event):
        """Makes sure to stop the webcam before we close the widget."""
        self.webcam.stop()
        event.accept()

    def start_webcam(self):
        """Starts the webcam."""
        # Reassign functionality to pause the webcam on demand
        self.start_webcam_button.setText("Pause / Play")
        self.start_webcam_button.clicked.disconnect()
        self.start_webcam_button.clicked.connect(self.webcam.toggle)
        self.webcam.start()

    def open_image(self):
        """Shows a file dialog and displays the selected image."""
        if self.webcam.isRunning():
            self.webcam.stop()

            self.start_webcam_button.setText("Start Webcam")
            self.start_webcam_button.clicked.disconnect()
            self.start_webcam_button.clicked.connect(self.start_webcam)

        image = open_image_dialog()
        if image is not None:
            self.set_image(image)

    def set_image(self, image):
        """Updates the widget's image."""
        self.src_image_label.setPixmap(to_q_pixmap(image))

        # Compute phase, magnitude or spectrum
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        fft = np.fft.fft2(gray)
        fshift = np.fft.fftshift(fft)

        fshift = np.ascontiguousarray(fshift)

        magnitude_spectrum = np.log(np.abs(fshift))
        magnitude_spectrum *= 255.0 / magnitude_spectrum.max()
        magnitude_spectrum = magnitude_spectrum.astype(np.uint8)
        self.dst_image_label.setPixmap(to_q_pixmap(magnitude_spectrum))
