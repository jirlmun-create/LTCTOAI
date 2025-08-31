from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QApplication
import os
from PyQt5.QtGui import QFont
from progress_manager import ProgressManager

class PageReport(QWidget):
    def load_patient_list(self):
        base_dir = os.path.join(os.path.dirname(__file__), 'data', 'patient_docs')
        self.patient_list.clear()
        if not os.path.exists(base_dir):
            self.patient_list.addItem("(대상자 폴더 없음)")
            return
        for group in os.listdir(base_dir):
            group_path = os.path.join(base_dir, group)
            if os.path.isdir(group_path):
                for name in os.listdir(group_path):
                    name_path = os.path.join(group_path, name)
                    if os.path.isdir(name_path):
                        self.patient_list.addItem(f"[{group}] {name}")
        if self.patient_list.count() == 0:
            self.patient_list.addItem("(대상자 폴더 없음)")
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("보고서 출력 영역 (대상자 선택 후 생성)"))
        self.patient_list = QListWidget()
        self.patient_list.setFont(QFont('Malgun Gothic', 12))
        layout.addWidget(QLabel("대상자 리스트 (소속 포함):"))
        layout.addWidget(self.patient_list)
        self.selected_info_label = QLabel("")
        layout.addWidget(self.selected_info_label)
        self.btn_generate_report = QPushButton("보고서 생성")
        self.btn_generate_report.setFont(QFont('Malgun Gothic', 16))
        self.btn_generate_report.setMinimumHeight(56)
        self.btn_generate_report.setStyleSheet(
            "background-color:#2979ff; color:white; border-radius:12px; font-size:18px; font-weight:bold; margin-top:24px;"
        )
        layout.addWidget(self.btn_generate_report)
        self.loading_label = QLabel("")
        self.loading_label.setStyleSheet("color: #2979ff; font-size: 14px; font-weight: bold; margin-top: 8px;")
        layout.addWidget(self.loading_label)
        self.report_result_label = QLabel("")
        layout.addWidget(self.report_result_label)
        self.setLayout(layout)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("보고서 출력 영역 (대상자 선택 후 생성)"))
        self.patient_list = QListWidget()
        self.patient_list.setFont(QFont('Malgun Gothic', 12))
        layout.addWidget(QLabel("대상자 리스트 (소속 포함):"))
        layout.addWidget(self.patient_list)
        self.selected_info_label = QLabel("")
        layout.addWidget(self.selected_info_label)
        self.btn_generate_report = QPushButton("보고서 생성")
        self.btn_generate_report.setFont(QFont('Malgun Gothic', 16))
        self.btn_generate_report.setMinimumHeight(56)
        self.btn_generate_report.setStyleSheet(
            "background-color:#2979ff; color:white; border-radius:12px; font-size:18px; font-weight:bold; margin-top:24px;"
        )
        layout.addWidget(self.btn_generate_report)
        self.loading_label = QLabel("")
        self.loading_label.setStyleSheet("color: #2979ff; font-size: 14px; font-weight: bold; margin-top: 8px;")
        layout.addWidget(self.loading_label)
        self.report_result_label = QLabel("")
        layout.addWidget(self.report_result_label)
        self.setLayout(layout)

        # 이벤트 연결 및 patient_list 로드
        self.load_patient_list()
        self.patient_list.currentItemChanged.connect(self.show_selected_info)
        self.btn_generate_report.clicked.connect(self.generate_report_for_selected)

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
        import os
        print("[DEBUG] 버튼 클릭됨")
        selected = self.patient_list.currentItem()
        if not selected or selected.text() == "(대상자 폴더 없음)":
            self.report_result_label.setText("보고서 생성할 대상자를 선택하세요.")
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
                from progress_manager import ProgressManager
                import sys, os
                rg_path = os.path.join(os.path.dirname(__file__), "report_generator.py")
                print(f"[DEBUG][ui_page_report] report_generator.py import 경로: {rg_path}")
                print(f"[DEBUG][ui_page_report] sys.path: {sys.path}")
                print(f"[DEBUG][ui_page_report] os.getcwd: {os.getcwd()}")
                print(f"[DEBUG][ui_page_report] .venv: {os.environ.get('VIRTUAL_ENV')}")
                spec_rg = importlib.util.spec_from_file_location("report_generator", rg_path)
                report_gen = importlib.util.module_from_spec(spec_rg)
                spec_rg.loader.exec_module(report_gen)
                print(f"[DEBUG][ui_page_report] 실제 import된 report_generator.__file__: {getattr(report_gen, '__file__', '없음')}")

                def update_callback(idx, total, pdf_path):
                    self.loading_label.setText(f"보고서 생성 중... ({idx+1}/{total}) [{os.path.basename(pdf_path)}]")
                    QApplication.processEvents()

                def error_callback(pdf_path, msg):
                    self.report_result_label.setText(f"오류: {os.path.basename(pdf_path)} - {msg}")
                    QApplication.processEvents()

                pm = ProgressManager(update_callback, error_callback)
                results, errors = pm.analyze_pdfs_parallel(pdf_files, data_processor.analyze_pdf)

                # 오류 파일 리스트 표시
                if errors:
                    error_msgs = '\n'.join([f"오류: {os.path.basename(f)} - {msg}" for f, msg in errors])
                    self.report_result_label.setText(error_msgs)
                else:
                    self.report_result_label.setText("")

                def extract_basic_info(text):
                    import re
                    info = {}
                    info['name_masked'] = name
                    info['facility'] = group
                    info['birth'] = re.search(r'생년월일[:\s]*(\d{4}\.\d{2}\.\d{2})', text)
                    info['birth'] = info['birth'].group(1) if info['birth'] else ''
                    info['admission_date'] = re.search(r'입소일[:\s]*(\d{4}-\d{2}-\d{2})', text)
                    info['admission_date'] = info['admission_date'].group(1) if info['admission_date'] else ''
                    info['discharge_date'] = re.search(r'퇴소일[:\s]*(\d{4}-\d{2}-\d{2})', text)
                    info['discharge_date'] = info['discharge_date'].group(1) if info['discharge_date'] else ''
                    info['program_count'] = len(re.findall(r'프로그램 참여', text))
                    info['medication_count'] = len(re.findall(r'투약기록', text))
                    if not isinstance(info, dict):
                        print(f"[DEBUG] extract_basic_info 반환값 타입 오류: {type(info)}, 값: {info}")
                        return {}
                    return info

                def extract_indicators(text):
                    import re
                    indicators = {}
                    if '신체변화' in text:
                        indicators['신체변화'] = {'grade': '우수', 'reason': '신체변화 기록 있음'}
                    else:
                        indicators['신체변화'] = {'grade': '미흡', 'reason': '신체변화 기록 없음'}
                    med_count = len(re.findall(r'투약기록', text))
                    if med_count >= 10:
                        indicators['투약기록'] = {'grade': '우수', 'reason': f'투약기록 {med_count}회'}
                    prog_count = len(re.findall(r'프로그램 참여', text))
                    if prog_count >= 5:
                        indicators['프로그램참여'] = {'grade': '우수', 'reason': f'프로그램 참여 {prog_count}회'}
                        indicators['프로그램참여'] = {'grade': '양호', 'reason': f'프로그램 참여 {prog_count}회'}
                    else:
                        indicators['프로그램참여'] = {'grade': '미흡', 'reason': '프로그램 참여 없음'}
                    if not isinstance(indicators, dict):
                        print(f"[DEBUG] extract_indicators 반환값 타입 오류: {type(indicators)}, 값: {indicators}")
                        return {}
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
                    data = extract_basic_info(first_text)
                    indicators = extract_indicators(first_text) if isinstance(extract_indicators(first_text), dict) else {}
                else:
                    data = {'name_masked': name, 'facility': group}
                    indicators = {}

                result = report_gen.create_report(data, indicators, cross_errors, period_start, period_end)
                # 오류 반환 시 튜플 구조: (에러코드, 에러메시지)
                if isinstance(result, tuple) and len(result) == 2:
                    err_code, err_msg = result
                    if not isinstance(err_code, str):
                        err_code = str(err_code)
                    if isinstance(err_msg, tuple):
                        err_msg = ', '.join(map(str, err_msg))
                    elif not isinstance(err_msg, str):
                        err_msg = str(err_msg)
                else:
                    err_code = "알수없음"
                    err_msg = str(result)
                if err_code in ["보고서 파일명", "성공", "success"]:
                    filename = err_msg
                    print(f"[DEBUG] indicators 타입: {type(indicators)}, 값: {indicators}")
                    if not isinstance(indicators, dict):
                        msg = f"[오류] 평가지표(indicators) 타입 오류: {type(indicators)} - {indicators}"
                        print(msg)
                        self.report_result_label.setText(f"보고서가 생성되었습니다: {filename}\n{msg}")
                        return
                    summary = f"신체변화: {indicators.get('신체변화', {}).get('grade', '')}, "
                    summary += f"투약기록: {indicators.get('투약기록', {}).get('grade', '')}, "
                    summary += f"프로그램참여: {indicators.get('프로그램참여', {}).get('grade', '')}"
                    if cross_errors:
                        summary += f"\n경고: {', '.join(cross_errors)}"
                    self.report_result_label.setText(f"보고서가 생성되었습니다: {filename}\n{summary}")
                else:
                    debug_msg = f"[DEBUG][ui_page_report] 오류 반환값: err_code={err_code}, err_msg={err_msg}, err_msg 타입={type(err_msg)}\nresult={result}\ntype(result)={type(result)}"
                    print(debug_msg)
                    self.report_result_label.setText(f"{debug_msg}\n보고서 생성 오류: {err_code} - {err_msg}")
            except Exception as e:
                print(f"[ERROR] 보고서 생성 오류: {str(e)}")
                import traceback
                traceback.print_exc()
                # 오류 메시지 덮어쓰기 방지: setText 호출하지 않음
            finally:
                self.loading_label.setText("")
