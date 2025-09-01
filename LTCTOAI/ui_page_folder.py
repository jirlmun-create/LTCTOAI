from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QHBoxLayout, QFileDialog, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QThread, pyqtSignal
import sys

class AnalyzerThread(QThread):
    result_ready = pyqtSignal(str)
    error_ready = pyqtSignal(str)
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.path = path
        self._cancel = False
    def run(self):
        try:
            from document_loader import load_document
            if self._cancel:
                return
            result = load_document(self.path, cancel_callback=lambda: self._cancel)
            if self._cancel:
                return
            if isinstance(result, str):
                preview = result[:5000] + ("..." if len(result) > 5000 else "")
            elif hasattr(result, 'head'):
                preview = str(result.head())
            elif isinstance(result, dict):
                preview = str(result)
            else:
                preview = str(result)
            self.result_ready.emit(f"분석 결과 미리보기:\n{preview}")
        except Exception as e:
            self.error_ready.emit(f"오류: {str(e)}")
    def cancel(self):
        self._cancel = True
class PageFolder(QWidget):
    def analyze_selected_file(self, item):
        import os
        folder = self.path_input.text().strip()
        filename = item.text()
        path = os.path.join(folder, filename)
        if not os.path.exists(path):
            self.result_textedit.setText("(파일 경로가 올바르지 않습니다)")
            return
        # 분석 결과 표시 예시
        self.result_textedit.setText(f"선택한 파일: {filename}\n경로: {path}")
    def refresh_file_list(self):
        import os
        path = self.path_input.text().strip()
        self.file_list.clear()
        if not path or not os.path.exists(path):
            self.file_list.addItem("(폴더 경로가 올바르지 않습니다)")
            return
        try:
            for f in os.listdir(path):
                self.file_list.addItem(f)
        except Exception as e:
            self.file_list.addItem(f"오류: {str(e)}")
    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "폴더 선택", "")
        if folder:
            self.path_input.setText(folder)
            self.refresh_file_list()
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText(r"폴더 경로 입력 또는 UNC 경로 입력 (예: \\server\share)")
        self.btn_browse = QPushButton("폴더 선택")
        self.btn_refresh = QPushButton("새로고침")
        self.btn_convert = QPushButton("데이터셋 변환 (KoAlpaca)")
        self.btn_pdf_convert = QPushButton("PDF → 파인튜닝 데이터 변환")
        self.btn_finetune = QPushButton("파인튜닝 실행 (KoAlpaca)")
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.path_input)
        hlayout.addWidget(self.btn_browse)
        hlayout.addWidget(self.btn_refresh)
        hlayout.addWidget(self.btn_convert)
        hlayout.addWidget(self.btn_pdf_convert)
        hlayout.addWidget(self.btn_finetune)
        layout.addLayout(hlayout)
        self.file_list = QListWidget()
        layout.addWidget(QLabel("파일 리스트:"))
        layout.addWidget(self.file_list)
        self.result_textedit = QTextEdit()
        self.result_textedit.setReadOnly(True)
        self.result_textedit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.result_textedit.setLineWrapMode(QTextEdit.WidgetWidth)
        layout.addWidget(self.result_textedit)
        self.setLayout(layout)

    def run_pdf_to_koalpaca(self):
        import sys
        import subprocess
        self.result_textedit.setText("PDF → 파인튜닝 데이터 변환 중... 잠시만 기다려주세요.")
        try:
            result = subprocess.run([
                sys.executable, "pdf_to_koalpaca.py"
            ], capture_output=True, text=True, cwd=".")
            if result.returncode == 0:
                self.result_textedit.setText("PDF 변환 완료!\n" + result.stdout)
            else:
                self.result_textedit.setText("PDF 변환 오류:\n" + result.stderr)
        except Exception as e:
            self.result_textedit.setText(f"PDF 변환 중 예외 발생: {str(e)}")


    def run_convert_dataset(self):
        import sys
        import subprocess
        self.result_textedit.setText("데이터셋 변환 중... 잠시만 기다려주세요.")
        try:
            result = subprocess.run([
                sys.executable, "convert_to_koalpaca.py"
            ], capture_output=True, text=True, cwd=".")
            if result.returncode == 0:
                self.result_textedit.setText("데이터셋 변환 완료!\n" + result.stdout)
            else:
                self.result_textedit.setText("데이터셋 변환 오류:\n" + result.stderr)
        except Exception as e:
            self.result_textedit.setText(f"데이터셋 변환 중 예외 발생: {str(e)}")

    def run_finetune(self):
        import sys
        import subprocess
        self.result_textedit.setText("파인튜닝 실행 중... 잠시만 기다려주세요.")
        try:
            result = subprocess.run([
                sys.executable, "finetune_koalpaca.py"
            ], capture_output=True, text=True, cwd=".")
            if result.returncode == 0:
                self.result_textedit.setText("파인튜닝 완료!\n" + result.stdout)
            else:
                self.result_textedit.setText("파인튜닝 오류:\n" + result.stderr)
        except Exception as e:
            self.result_textedit.setText(f"파인튜닝 중 예외 발생: {str(e)}")
    def run_convert_dataset(self):
        import subprocess
        self.result_textedit.setText("데이터셋 변환 중... 잠시만 기다려주세요.")
        try:
            # 예시: datasets/sample.csv → datasets/koalpaca_train.jsonl
            result = subprocess.run([
                sys.executable, "convert_to_koalpaca.py"
            ], capture_output=True, text=True, cwd=".")
            if result.returncode == 0:
                self.result_textedit.setText("데이터셋 변환 완료!\n" + result.stdout)
            else:
                self.result_textedit.setText("데이터셋 변환 오류:\n" + result.stderr)
        except Exception as e:
            self.result_textedit.setText(f"데이터셋 변환 중 예외 발생: {str(e)}")

    def run_finetune(self):
        import subprocess
        self.result_textedit.setText("파인튜닝 실행 중... 잠시만 기다려주세요.")
        try:
            result = subprocess.run([
                sys.executable, "finetune_koalpaca.py"
            ], capture_output=True, text=True, cwd=".")
            if result.returncode == 0:
                self.result_textedit.setText("파인튜닝 완료!\n" + result.stdout)
            else:
                self.result_textedit.setText("파인튜닝 오류:\n" + result.stderr)
        except Exception as e:
            self.result_textedit.setText(f"파인튜닝 중 예외 발생: {str(e)}")

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText(r"폴더 경로 입력 또는 UNC 경로 입력 (예: \\server\share)")
        self.btn_browse = QPushButton("폴더 선택")
        self.btn_refresh = QPushButton("새로고침")
        self.btn_convert = QPushButton("데이터셋 변환 (KoAlpaca)")
        self.btn_pdf_convert = QPushButton("PDF → 파인튜닝 데이터 변환")
        self.btn_finetune = QPushButton("파인튜닝 실행 (KoAlpaca)")
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.path_input)
        hlayout.addWidget(self.btn_browse)
        hlayout.addWidget(self.btn_refresh)
        hlayout.addWidget(self.btn_convert)
        hlayout.addWidget(self.btn_pdf_convert)
        hlayout.addWidget(self.btn_finetune)
        layout.addLayout(hlayout)
        self.file_list = QListWidget()
        layout.addWidget(QLabel("파일 리스트:"))
        layout.addWidget(self.file_list)
        self.result_textedit = QTextEdit()
        self.result_textedit.setReadOnly(True)
        self.result_textedit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.result_textedit.setLineWrapMode(QTextEdit.WidgetWidth)
        layout.addWidget(self.result_textedit)
        self.setLayout(layout)
        self.analyzer_thread = None
        self.btn_browse.clicked.connect(self.select_folder)
        self.btn_refresh.clicked.connect(self.refresh_file_list)
        self.path_input.returnPressed.connect(self.refresh_file_list)
        self.file_list.itemClicked.connect(self.analyze_selected_file)
        self.btn_convert.clicked.connect(self.run_convert_dataset)
        self.btn_pdf_convert.clicked.connect(self.run_pdf_to_koalpaca)
        self.btn_finetune.clicked.connect(self.run_finetune)

