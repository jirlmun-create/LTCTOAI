from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class PageLogout(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("로그아웃 및 종료"))
        self.setLayout(layout)
