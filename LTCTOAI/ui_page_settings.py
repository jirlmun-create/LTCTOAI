from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class PageSettings(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("환경설정 영역 (모델/경로/기타 설정)"))
        self.setLayout(layout)
