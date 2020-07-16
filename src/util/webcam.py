# -*- coding: utf-8 -*-
import cv2
import numpy as np
from PySide2.QtCore import QThread, Signal


class Webcam(QThread):
    is_paused: bool = False
    acquired_image_signal: Signal = Signal(np.ndarray)

    def __init__(self, source, width, height, parent=None):
        QThread.__init__(self, parent)

        self.width = width
        self.height = height

        self.cap = cv2.VideoCapture(source)
        if self.cap is None or not self.cap.isOpened():
            self.stop()

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def run(self):
        while not self.isInterruptionRequested():
            # Capture frame-by-frame
            ret, frame = self.cap.read()

            if self.is_paused:
               continue

            if ret:
                frame = cv2.resize(frame, (self.width, self.height))
                self.acquired_image_signal.emit(frame)  # send image to gui

        self.cap.release()

    def stop(self):
        self.requestInterruption()
        self.wait(100)
        self.quit()
        #self.terminate()

    def set_pause(self, pause):
        self.is_paused = pause

    def toggle_pause(self):
        self.is_paused = not self.is_paused
