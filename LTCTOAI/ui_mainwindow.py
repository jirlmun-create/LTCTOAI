from PyQt5.QtWidgets import QMainWindow, QSplitter, QWidget, QVBoxLayout, QFrame, QStackedWidget
from PyQt5.QtCore import Qt
from ui_menu import MenuButton
from ui_page_report import PageReport
from ui_page_qa import PageQA
from ui_page_folder import PageFolder
from ui_page_settings import PageSettings
from ui_page_logout import PageLogout

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI 기반 장기요양 평가 보고서 생성기")
        self.setGeometry(100, 100, 1200, 800)

        splitter = QSplitter(Qt.Horizontal)
        menu_widget = QWidget()
        menu_layout = QVBoxLayout()
        menu_widget.setLayout(menu_layout)
        menu_widget.setStyleSheet("background-color: #f0f4fb; border-right: 2px solid #d0d6e1;")

        self.btn_report = MenuButton("보고서 출력", '#4a90e2')
        self.btn_qa = MenuButton("Q/A", '#7b8fa1')
        self.btn_folder = MenuButton("폴더 확인", '#7b8fa1')
        line1 = QFrame()
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        line1.setStyleSheet("margin: 12px 0; background-color: #dbe4f3; height:2px;")
        self.btn_settings = MenuButton("환경설정", '#bfc9d9')
        self.btn_logout = MenuButton("로그아웃", '#bfc9d9')
        for btn in [self.btn_report, self.btn_qa, self.btn_folder]:
            menu_layout.addWidget(btn)
        menu_layout.addWidget(line1)
        for btn in [self.btn_settings, self.btn_logout]:
            menu_layout.addWidget(btn)
        menu_layout.addStretch(1)

        self.stack = QStackedWidget()
        self.page_report = PageReport()
        self.page_qa = PageQA()
        self.page_folder = PageFolder()
        self.page_settings = PageSettings()
        self.page_logout = PageLogout()

        self.stack.addWidget(self.page_report)
        self.stack.addWidget(self.page_qa)
        self.stack.addWidget(self.page_folder)
        self.stack.addWidget(self.page_settings)
        self.stack.addWidget(self.page_logout)

        self.btn_report.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_report))
        self.btn_qa.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_qa))
        self.btn_folder.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_folder))
        self.btn_settings.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_settings))
        self.btn_logout.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_logout))

        splitter.addWidget(menu_widget)
        splitter.addWidget(self.stack)
        splitter.setSizes([220, 980])
        self.setCentralWidget(splitter)
