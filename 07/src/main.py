import sys

from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget

from mod.state import State
from widgets.log import LogWidget
from widgets.record import RecordWidget


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._state = State()
        self.__define_layout()

    def __define_layout(self) -> None:
        self.setWindowTitle("title")

        layout = QVBoxLayout()
        self.button_widget = RecordWidget(self._state)
        layout.addWidget(self.button_widget)

        self.log_widget = LogWidget(self._state)
        layout.addWidget(self.log_widget)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication()
    win = MainWindow()

    win.show()
    app.exec()

    del win
    sys.exit()
