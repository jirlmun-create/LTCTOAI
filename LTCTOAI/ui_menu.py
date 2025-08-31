from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QFont

class MenuButton(QPushButton):
    def __init__(self, text, color=None):
        super().__init__(text)
        self.setMinimumHeight(48)
        self.setFont(QFont('Malgun Gothic', 13))
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {color if color else '#f5f6fa'};
                color: #222;
                border: none;
                border-radius: 8px;
                margin-bottom: 8px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: #e1e7f5;
                color: #0052cc;
            }}
        """)
