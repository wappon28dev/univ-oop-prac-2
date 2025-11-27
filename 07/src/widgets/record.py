from pathlib import Path
import subprocess
from typing import Final, Optional

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget, QLabel

from mod.paths import DIR_OUT
from mod.record import record_pc_audio
from mod.state import State


class RecordThread(QThread):
    finished_recording = Signal()

    def __init__(self, duration: int, output_file: Path) -> None:
        super().__init__()
        self.duration = duration
        self.output_file = output_file
        self._process: Optional[subprocess.Popen] = None

    def run(self) -> None:
        self._process = record_pc_audio(self.duration, self.output_file)
        self._process.wait()
        self.finished_recording.emit()

    def stop(self) -> None:
        if self._process and self._process.poll() is None:
            self._process.terminate()
            self._process.wait()


class RecordWidget(QWidget):
    def __init__(self, state: State) -> None:
        super().__init__()
        self._state = state
        self.__define_layout()

    def __define_layout(self) -> None:
        layout = QHBoxLayout()

        label = QLabel("1. ")
        label.setFixedWidth(20)
        layout.addWidget(label)

        self._button_start = QPushButton("● 10 秒録音開始")
        self._button_start.clicked.connect(self.__on_click_start)
        layout.addWidget(self._button_start)

        self._button_stop = QPushButton("■ 停止")
        self._button_stop.setFixedWidth(60)
        self._button_stop.setDisabled(True)
        self._button_stop.clicked.connect(self.__on_click_stop)
        layout.addWidget(self._button_stop)

        self.setLayout(layout)

    def __on_click_start(self) -> None:
        output_file: Final = DIR_OUT / "recorded_audio.wav"

        self._state.log = "録音を開始します..."
        self._button_start.setDisabled(True)
        self._button_stop.setDisabled(False)

        self._thread = RecordThread(10, output_file)
        self._thread.finished_recording.connect(self.__on_finished)
        self._thread.start()

    def __on_click_stop(self) -> None:
        if self._thread and self._thread.isRunning():
            self._state.log = "録音を停止しています..."
            self._thread.stop()

    def __on_finished(self) -> None:
        self._state.log = "録音を停止しました。"
        self._button_start.setDisabled(False)
        self._button_stop.setDisabled(True)
