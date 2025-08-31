from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class PageFolder(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("폴더 내 파일 리스트 및 상태 표시 영역"))
        self.setLayout(layout)
