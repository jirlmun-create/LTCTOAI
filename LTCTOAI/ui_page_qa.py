from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class PageQA(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Q/A 영역 (질문/답변 기록 및 입력)"))
        self.setLayout(layout)
