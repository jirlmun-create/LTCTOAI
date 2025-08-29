import tkinter as tk
from tkinter import filedialog

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI 장기요양 평가 보고서 생성기")
        self.geometry("800x600")
        # 폴더 선택 버튼
        btn_select = tk.Button(self, text="분석 폴더 선택", command=self.select_folder)
        btn_select.pack(pady=10)
        # 진행바, 결과 출력 영역 등 추가 구현
        self.result_label = tk.Label(self, text="결과 출력 영역")
        self.result_label.pack(pady=10)

    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.result_label.config(text=f"선택된 폴더: {folder}")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()