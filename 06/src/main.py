import sys
from typing import Final

from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from my_report.model import report_model


class MDReportMakerApp(QMainWindow):
    """マークダウン記法でレポートを作成するアプリ(主に表示機能)

    - 利用前にstatus_orig.jsonを参考にstatus.jsonファイルを作成してください
    - 左側のボタンを押して編集画面を表示
    - 右側の表示で内容を確認
    - saveボタンで内容をレポートをファイルに保存(履歴も保存)
    - save without historyボタンでレポートをファイルに保存（履歴は更新しない）
    """

    def __init__(self, my_model: report_model):
        super().__init__()
        # アプリ内でreport_modelを使い回すことでデータを共有する
        self.report_model = my_model
        self.setWindowTitle("Markdown Report Maker")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        left_panel_layout = QVBoxLayout()
        v_layout = QVBoxLayout()
        self.input_buttons = [InputButton(x, self) for x in report_model.KEY_LIST]
        [v_layout.addWidget(b) for b in self.input_buttons]
        q_group = QGroupBox()
        q_group.setLayout(v_layout)
        left_panel_layout.addWidget(q_group)
        h_layout = QHBoxLayout()
        self.save_buttons = [SaveButton(x, self) for x in ["Save", "Save without history"]]
        [h_layout.addWidget(b) for b in self.save_buttons]
        left_panel_layout.addLayout(h_layout)

        self.report_window = MDTextEdit(self)
        self.report_window.setReadOnly(True)

        layout = QGridLayout()
        layout.addLayout(left_panel_layout, 0, 0)
        layout.addWidget(self.report_window, 0, 1)
        self.central_widget.setLayout(layout)

        self.report_window.update_text_edit()
        # 内容をテキストで確認（これをファイルに保存すれば良い）
        print(self.report_window.toMarkdown())


class MDTextEdit(QTextEdit):
    def __init__(self, main_window: MDReportMakerApp):
        super().__init__()
        self.main_window = main_window

    def update_text_edit(self) -> None:
        self.main_window.report_window.setMarkdown(self.main_window.report_model.get_body())
        self.resize_text_edit()

    def resize_text_edit(self) -> None:
        num_lines = self.document().lineCount()
        max_line_length = max(len(line) for line in self.toPlainText().splitlines())
        width = (self.fontMetrics().horizontalAdvance("あ") + 2) * max_line_length + 10

        self.setMinimumWidth(width)
        self.setMinimumHeight(self.fontMetrics().height() * num_lines)


class InputButton(QPushButton):
    def __init__(self, init_text: str, main_window: MDReportMakerApp):
        super().__init__(init_text)
        self.main_window = main_window
        self.clicked.connect(self.__button_dialog)

    def __button_dialog(self) -> None:
        b_index = report_model.KEY_LIST.index(self.text())
        print(b_index)

        dialog = QDialog(self)
        dialog.setWindowTitle(f"This is a QDialog for {self.text()}")
        layout = QVBoxLayout()

        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(self.main_window.report_model.get_text_by_key(self.text()))
        num_lines = self.text_edit.document().lineCount()
        max_line_length = max(len(line) for line in self.text_edit.toPlainText().splitlines())
        width = self.text_edit.fontMetrics().horizontalAdvance("あ") * max_line_length + 10
        self.text_edit.setMinimumWidth(width)
        self.text_edit.setMinimumHeight(self.fontMetrics().height() * num_lines)
        self.text_edit.textChanged.connect(self.__update_dialog_text)
        layout.addWidget(self.text_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(dialog.accept)
        layout.addWidget(button_box)

        dialog.setLayout(layout)
        dialog.exec()

    def __update_dialog_text(self) -> None:
        window: Final = self.main_window.report_window
        model: Final = self.main_window.report_model

        model.set_text_by_key(self.text(), self.text_edit.toPlainText())

        window.update_text_edit()
        # 編集箇所へのジャンプは長い長いレポートになると調整が必要
        if model.KEY_LIST.index(self.text()) > 2:
            window.verticalScrollBar().setValue(
                window.verticalScrollBar().maximum(),
            )


class SaveButton(QPushButton):
    """編集後のマークダウンファイルを保存するボタン"""

    def __init__(self, initial_text: str, main_window: MDReportMakerApp):
        super().__init__(initial_text)
        self.main_window = main_window
        self.setStyleSheet(
            "SaveButton {background-color: #4169e1; \
                                        color: yellow; \
                                        border-radius: 3px;} \
                           SaveButton:pressed {background: #000080}",
        )
        self.clicked.connect(self.__click)

    def __click(self) -> None:
        rm = self.main_window.report_model
        if self.text() == self.main_window.save_buttons[0].text():
            print(f"{self.text()} button is pushed")
            "ヒント：ここでファイルを開いてテキストを保存するが，テキストを管理しているreport_modelに任せること"
            "ヒント：historyの保存も，テキストを管理しているreport_modelに任せること"
            rm.save_file(self.main_window.report_window.toMarkdown())
        else:
            print(f"{self.text()} button is pushed")
            "implement me"
            "ヒント：ここでファイルを開いてテキストを保存するが，テキストを管理しているreport_modelに任せること"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MDReportMakerApp(report_model())
    mw.show()
    app.exec()
