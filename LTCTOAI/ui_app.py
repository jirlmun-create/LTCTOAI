import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel,
    QStackedWidget, QSplitter, QFrame, QListWidget, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import re
from fpdf import FPDF

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
        self.page_report = QWidget()
        self.page_qa = QWidget()
        self.page_folder = QWidget()
        self.page_settings = QWidget()
        self.page_logout = QWidget()

        # 보고서 출력 페이지
        report_layout = QVBoxLayout()
        report_layout.addWidget(QLabel("보고서 출력 영역 (대상자 선택 후 생성)"))
        self.patient_list = QListWidget()
        self.patient_list.setFont(QFont('Malgun Gothic', 12))
        report_layout.addWidget(QLabel("대상자 리스트 (소속 포함):"))
        report_layout.addWidget(self.patient_list)
        self.selected_info_label = QLabel("")
        report_layout.addWidget(self.selected_info_label)
        self.btn_generate_report = QPushButton("보고서 생성")
        self.btn_generate_report.setFont(QFont('Malgun Gothic', 16))
        self.btn_generate_report.setMinimumHeight(56)
        self.btn_generate_report.setStyleSheet(
            "background-color:#2979ff; color:white; border-radius:12px; font-size:18px; font-weight:bold; margin-top:24px;"
        )
        report_layout.addWidget(self.btn_generate_report)
        self.loading_label = QLabel("")
        self.loading_label.setStyleSheet("color: #2979ff; font-size: 14px; font-weight: bold; margin-top: 8px;")
        report_layout.addWidget(self.loading_label)
        self.report_result_label = QLabel("")
        report_layout.addWidget(self.report_result_label)
        self.page_report.setLayout(report_layout)

        # Q/A 페이지
        qa_layout = QVBoxLayout()
        qa_layout.addWidget(QLabel("Q/A 영역 (질문/답변 기록 및 입력)"))
        self.page_qa.setLayout(qa_layout)
        # 폴더 확인 페이지
        folder_layout = QVBoxLayout()
        folder_layout.addWidget(QLabel("폴더 내 파일 리스트 및 상태 표시 영역"))
        self.page_folder.setLayout(folder_layout)
        # 환경설정 페이지
        settings_layout = QVBoxLayout()
        settings_layout.addWidget(QLabel("환경설정 영역 (모델/경로/기타 설정)"))
        self.page_settings.setLayout(settings_layout)
        # 로그아웃 페이지
        logout_layout = QVBoxLayout()
        logout_layout.addWidget(QLabel("로그아웃 및 종료"))
        self.page_logout.setLayout(logout_layout)

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

        # 대상자 리스트 자동 탐색 (소속별 폴더)
        self.load_patient_list()
        self.patient_list.currentItemChanged.connect(self.show_selected_info)
        self.btn_generate_report.clicked.connect(self.generate_report_for_selected)

    def load_patient_list(self):
        base_dir = os.path.join(os.path.dirname(__file__), 'data', 'patient_docs')
        self.patient_list.clear()
        found = False
        if os.path.exists(base_dir):
            for group in ['시설요양', '주간보호', '방문요양']:
                group_dir = os.path.join(base_dir, group)
                if os.path.exists(group_dir):
                    for name in os.listdir(group_dir):
                        full_path = os.path.join(group_dir, name)
                        # 폴더만 표시, 숨김 폴더/파일 무시
                        if os.path.isdir(full_path) and not name.startswith('.'):
                            self.patient_list.addItem(f"[{group}] {name}")
                            found = True
        if not found:
            self.patient_list.addItem("(대상자 폴더 없음)")

    def show_selected_info(self):
        selected = self.patient_list.currentItem()
        if selected:
            text = selected.text()
            if text.startswith('['):
                group, name = text[1:].split('] ', 1)
                self.selected_info_label.setText(f"소속: {group} / 대상자: {name}")
            else:
                self.selected_info_label.setText("")
        else:
            self.selected_info_label.setText("")

    def generate_report_for_selected(self):
        selected = self.patient_list.currentItem()
        if not selected or selected.text() == "(대상자 폴더 없음)":
            QMessageBox.warning(self, "대상자 선택", "보고서 생성할 대상자를 선택하세요.")
            return
        text = selected.text()
        if text.startswith('['):
            group, name = text[1:].split('] ', 1)
            patient_dir = os.path.join(os.path.dirname(__file__), 'data', 'patient_docs', group, name)
            pdf_files = []
            if os.path.exists(patient_dir):
                for f in os.listdir(patient_dir):
                    if f.lower().endswith('.pdf'):
                        pdf_files.append(os.path.join(patient_dir, f))
            if not pdf_files:
                self.report_result_label.setText(f"PDF 자료가 없습니다: {group} / {name}")
                return
            try:
                import data_processor
                import importlib.util
                spec_rg = importlib.util.spec_from_file_location("report_generator", os.path.join(os.path.dirname(__file__), "report_generator.py"))
                report_gen = importlib.util.module_from_spec(spec_rg)
                spec_rg.loader.exec_module(report_gen)

                self.loading_label.setText("보고서 생성 중... 잠시만 기다려주세요.")
                QApplication.processEvents()

                results, errors = data_processor.analyze_pdfs_parallel(pdf_files)

                def extract_basic_info(text):
                    info = {}
                    info['name_masked'] = name
                    info['facility'] = group
                    info['birth'] = re.search(r'생년월일[:\s]*(\d{4}\.\d{2}\.\d{2})', text)
                    info['birth'] = info['birth'].group(1) if info['birth'] else ''
                    info['admission_date'] = re.search(r'입소일[:\s]*(\d{4}-\d{2}-\d{2})', text)
                    info['admission_date'] = info['admission_date'].group(1) if info['admission_date'] else ''
                    info['discharge_date'] = re.search(r'퇴소일[:\s]*(\d{4}-\d{2}-\d{2})', text)
                    info['discharge_date'] = info['discharge_date'].group(1) if info['discharge_date'] else ''
                    # 추가 정보 추출 예시
                    info['program_count'] = len(re.findall(r'프로그램 참여', text))
                    info['medication_count'] = len(re.findall(r'투약기록', text))
                    return info

                def extract_indicators(text):
                    indicators = {}
                    # 신체변화
                    if '신체변화' in text:
                        indicators['신체변화'] = {'grade': '우수', 'reason': '신체변화 기록 있음'}
                    else:
                        indicators['신체변화'] = {'grade': '미흡', 'reason': '신체변화 기록 없음'}
                    # 투약기록
                    med_count = len(re.findall(r'투약기록', text))
                    if med_count >= 10:
                        indicators['투약기록'] = {'grade': '우수', 'reason': f'투약기록 {med_count}회'}
                    elif med_count > 0:
                        indicators['투약기록'] = {'grade': '양호', 'reason': f'투약기록 {med_count}회'}
                    else:
                        indicators['투약기록'] = {'grade': '미흡', 'reason': '투약기록 없음'}
                    # 프로그램 참여
                    prog_count = len(re.findall(r'프로그램 참여', text))
                    if prog_count >= 5:
                        indicators['프로그램참여'] = {'grade': '우수', 'reason': f'프로그램 참여 {prog_count}회'}
                    elif prog_count > 0:
                        indicators['프로그램참여'] = {'grade': '양호', 'reason': f'프로그램 참여 {prog_count}회'}
                    else:
                        indicators['프로그램참여'] = {'grade': '미흡', 'reason': '프로그램 참여 없음'}
                    return indicators

                required_keywords = ['프로그램 서명', '투약 기록', '신체변화']
                cross_errors = data_processor.cross_check_errors(results, required_keywords)

                period_start = '2025-01-01'
                period_end = '2025-08-29'

                first_text = ''
                if results:
                    for item in results:
                        if isinstance(item, dict) and 'text' in item:
                            first_text = item['text']
                            break
                        elif isinstance(item, (list, tuple)):
                            for subitem in item:
                                if isinstance(subitem, dict) and 'text' in subitem:
                                    first_text = subitem['text']
                                    break
                            if first_text:
                                break
                if first_text:
                    info = extract_basic_info(first_text)
                    indicators = extract_indicators(first_text)
                    data = info
                else:
                    data = {'name_masked': name, 'facility': group}
                    indicators = {}

                filename = report_gen.create_report(data, indicators, cross_errors, period_start, period_end)
                # 주요 지표 및 경고 요약 표시
                summary = f"신체변화: {indicators.get('신체변화', {}).get('grade', '')}, "
                summary += f"투약기록: {indicators.get('투약기록', {}).get('grade', '')}, "
                summary += f"프로그램참여: {indicators.get('프로그램참여', {}).get('grade', '')}"
                if cross_errors:
                    summary += f"\n경고: {', '.join(cross_errors)}"
                self.report_result_label.setText(f"보고서가 생성되었습니다: {filename}\n{summary}")
            except Exception as e:
                self.report_result_label.setText(f"보고서 생성 오류: {str(e)}")
            finally:
                self.loading_label.setText("")
        else:
            self.report_result_label.setText("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())