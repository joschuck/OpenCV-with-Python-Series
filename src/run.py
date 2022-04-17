"""Launcher for all examples in the repository."""

import sys

from PySide6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QMainWindow,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QWidget,
)

from src.fourier_transform.fourier_transform import FourierTransform
from src.thresholding.adaptive_thresholding import AdaptiveThresholding
from src.thresholding.binary_thresholding import BinaryThresholding
from src.thresholding.otsus_thresholding import OtsusThresholding

programs = {
    "Adaptive Thresholding": AdaptiveThresholding,
    "Binary Thresholding": BinaryThresholding,
    "Otsu's Thresholding": OtsusThresholding,
    "Fourier Transform": FourierTransform,
}


class ProgramSelector(QMainWindow):
    """Let's the user select an example."""

    instances = []

    def __init__(self):
        super().__init__()

        self.setWindowTitle("OpenCV with Python")

        layout = QVBoxLayout()
        self.program_list = QListWidget()

        for program in programs:
            self.program_list.addItem(QListWidgetItem(program))

        start_button = QPushButton("Start")
        start_button.clicked.connect(self.start)

        layout.addWidget(self.program_list)
        layout.addWidget(start_button)

        # Set the central widget of the Window.
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start(self):
        """Starts the selected example program."""
        try:
            item = self.program_list.selectedItems()[0]
            instance = programs.get(item.text())()
            self.instances.append(instance)

            instance.show()
        except IndexError:
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)

    ex = ProgramSelector()

    ex.show()

    sys.exit(app.exec())
