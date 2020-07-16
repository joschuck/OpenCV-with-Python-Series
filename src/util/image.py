# -*- coding: utf-8 -*-
"""
Common task with image data.
==================================

20.07.20.
Conversion to QImage and QPixmap
"""

__author__ = 'Johannes Schuck'
__email__ = 'johannes.schuck@gmail.com'

__all__ = ['to_q_image',
           'to_q_pixmap']


from PySide2.QtGui import QImage, QPixmap
import numpy as np


def to_q_image(image: np.ndarray):
    """
    Converts a OpenCV / NumPy array to a QImage.
    Expects the image to be 8 bit.
    Is able to convert Grayscale, BGR and ARGG images.

    Parameters
    ----------
    image : np.ndarray
        Input Image

    Returns
    -------
    QImage
        The converted image. If image is None, returns an empty QImage.
    """
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


def to_q_pixmap(image: QPixmap):
    """
    Converts a OpenCV / NumPy array to a QPixmap.
    Expects the image to be 8 bit.
    Is able to convert Grayscale, BGR and ARGG images.

    Parameters
    ----------
    image : np.ndarray
        Input Image

    Returns
    -------
    QPixmap
        The converted QPixmap. If image is None, returns an empty QPixmap.
    """
    return QPixmap(to_q_image(image))
