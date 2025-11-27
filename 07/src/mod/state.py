from PySide6.QtCore import QObject, Signal


class State(QObject):
    log_changed = Signal(str)

    def __init__(self) -> None:
        super().__init__()
        self._log: str = ""

    @property
    def log(self) -> str:
        return self._log

    @log.setter
    def log(self, value: str) -> None:
        self._log = value
        self.log_changed.emit(value)
