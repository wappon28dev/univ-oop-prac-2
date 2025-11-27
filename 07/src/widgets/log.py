from PySide6.QtWidgets import QTextEdit, QVBoxLayout, QWidget

from mod.state import State


class LogWidget(QWidget):
    def __init__(self, state: State) -> None:
        super().__init__()
        self._state = state
        self.__define_layout()
        self._state.log_changed.connect(self.__update_log)

    def __define_layout(self) -> None:
        layout = QVBoxLayout()
        self._text_edit = QTextEdit()
        self._text_edit.setReadOnly(True)
        self._text_edit.setFixedHeight(30)

        layout.addWidget(self._text_edit)
        self.setLayout(layout)

    def __update_log(self, message: str) -> None:
        self._text_edit.setPlainText(message)
