# -*- coding: utf-8 -*-
from PySide2.QtGui import QImage, QPixmap
import numpy as np

def to_q_image(image):
    if image is None:
        return QImage()

    if image.dtype == np.uint8:
        if len(image.shape) == 2:
            height, width = image.shape
            return QImage(image.data, width, height, width, QImage.Format_Indexed8)

        elif len(image.shape) == 3:
            height, width, ch = image.shape
            if image.shape[2] == 3:
                return QImage(image.data, width, height, width * 3, QImage.Format_BGR888)
            elif image.shape[2] == 4:
                return QImage(image.data, width, height, width * 3, QImage.Format_ARGB32)


def to_q_pixmap(image):
    return QPixmap(to_q_image(image))
