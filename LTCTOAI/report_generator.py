import re
"""
보고서 생성 모듈 (report_generator.py)
- 보고서 파일명 자동 생성 및 버전 관리
- 템플릿/포맷 분리 (기본 PDF)
- 개별 평가지표별 결과 + 파일간 교차점검 오류 포함
- 누락/오류 데이터 자동 하이라이트
- 사용자의 요구사항을 함수/클래스 단위로 쉽게 확장 가능
"""
import os
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
import tempfile

REPORTS_DIR = "reports"

def ensure_reports_dir():
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

def generate_report_filename(name_masked, period_start, period_end):
    def sanitize_filename(s):
        return re.sub(r'[\\/*?:"<>|]', '_', s)
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = sanitize_filename(name_masked)
    safe_start = sanitize_filename(period_start)
    safe_end = sanitize_filename(period_end)
    filename = f"report_{safe_name}_{safe_start}_{safe_end}_{date_str}.pdf"
    return os.path.join(REPORTS_DIR, filename)

class ReportPDF(FPDF):
    def header(self):
        self.set_font("NanumGothic", "", 16)
        self.cell(0, 10, "장기요양 평가 보고서", ln=True, align="C")
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font("NanumGothic", "", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def create_report(data, indicators, cross_errors, period_start, period_end):
    if not isinstance(indicators, dict):
        print(f"[DEBUG][report_generator] 평가지표(indicators) 타입 오류(함수시작): {type(indicators)}, 값: {indicators}")
        return ("평가지표 타입 오류(함수시작)", str(type(indicators)))
    ensure_reports_dir()
    filename = generate_report_filename(data['name_masked'], period_start, period_end)
    pdf = ReportPDF()
    font_path = os.path.join(os.path.dirname(__file__), 'NanumGothic.ttf')
    pdf.add_font('NanumGothic', '', font_path, uni=True)
    pdf.add_page()
    pdf.set_font("NanumGothic", size=12)
    # 이후 모든 PDF 관련 작업은 반드시 pdf 객체 생성 이후에만 실행
    pdf.cell(0, 10, "첨부/참고자료", ln=True)
    pdf.set_font("NanumGothic", size=12)
    # 실제 법령/지침/링크 연동은 추후 구현, 현재는 샘플 텍스트
    pdf.cell(0, 10, "고시 제75조의2, 장기요양급여 제공지침 2025", ln=True)
    pdf.cell(0, 10, "프로그램 참여 지침, 방문요양 서비스 지침", ln=True)
    pdf.cell(0, 10, "참고: https://www.longtermcare.or.kr/", ln=True)
    pdf.ln(5)
    # 질문/답변 기록(대화형 Q&A)
    pdf.set_font("NanumGothic", "", 13)
    pdf.cell(0, 10, "주요 질문/답변 기록", ln=True)
    pdf.set_font("NanumGothic", size=12)
    # 실제 Q&A 연동은 추후 구현, 현재는 샘플 텍스트
    pdf.cell(0, 10, "Q: 프로그램 서명 누락 시 감점 기준은?", ln=True)
    pdf.cell(0, 10, "A: 3회 이상 누락 시 감점 대상입니다.", ln=True)
    pdf.ln(5)
    # AI 분석 요약(자동 평가 결과, 문제점, 개선점, 예상 점수)
    pdf.set_font("NanumGothic", "", 13)
    pdf.cell(0, 10, "AI 분석 요약", ln=True)
    pdf.set_font("NanumGothic", size=12)
    # 실제 AI 분석 결과는 추후 모델 연동, 현재는 샘플 텍스트
    pdf.cell(0, 10, "예상 점수: 92점", ln=True)
    pdf.cell(0, 10, "문제점: 프로그램 서명 누락, 투약 기록 일부 누락", ln=True)
    pdf.cell(0, 10, "개선점: 프로그램 참여 서명 철저, 투약 기록 누락 방지", ln=True)
    pdf.ln(5)
    # 교차점검 결과(법령/지침 기준 누락, 감점 예상, 개선 권고)
    pdf.set_font("NanumGothic", "", 13)
    pdf.cell(0, 10, "교차점검 오류/누락", ln=True)
    pdf.set_font("NanumGothic", size=12)
    if cross_errors:
        for err in cross_errors:
            pdf.set_text_color(255, 0, 0)
            pdf.cell(0, 10, f"오류: {err}", ln=True)
            pdf.set_text_color(0, 0, 0)
    else:
        pdf.cell(0, 10, "없음", ln=True)
    pdf.ln(5)
    # 기록 요약 및 평가지표별 등급/이유
    pdf.set_font("NanumGothic", "", 13)
    pdf.cell(0, 10, "평가지표별 결과", ln=True)
    pdf.set_font("NanumGothic", size=12)
    if not isinstance(indicators, dict):
        print(f"[DEBUG][report_generator] 평가지표(indicators) 타입 오류: {type(indicators)}, 값: {indicators}")
        return ("평가지표 타입 오류", str(type(indicators)))
    for idx, item in indicators.items():
        pdf.cell(0, 10, f"{idx}: {item.get('grade', '')} - {item.get('reason', '')}", ln=True)
    pdf.ln(5)
    # 보고서 필수 항목 출력
    pdf.cell(0, 10, f"성명(마스킹): {data.get('name_masked', '')}", ln=True)
    pdf.cell(0, 10, f"생년월일: {data.get('birth', '')}", ln=True)
    pdf.cell(0, 10, f"성별: {data.get('gender', '')}", ln=True)
    pdf.cell(0, 10, f"입소일: {data.get('admit_date', '')}", ln=True)
    pdf.cell(0, 10, f"퇴소일: {data.get('discharge_date', '-')}", ln=True)
    pdf.cell(0, 10, f"평가기간: {period_start} ~ {period_end}", ln=True)
    pdf.cell(0, 10, f"시설명: {data.get('facility', '')}", ln=True)
    pdf.ln(5)
    ensure_reports_dir()
    filename = generate_report_filename(data['name_masked'], period_start, period_end)
    pdf = ReportPDF()
    # 폰트 파일 경로 지정 (report_generator.py와 같은 폴더에 있다고 가정)
    font_path = os.path.join(os.path.dirname(__file__), 'NanumGothic.ttf')
    pdf.add_font('NanumGothic', '', font_path, uni=True)
    pdf.add_page()
    pdf.set_font("NanumGothic", size=12)
    # 평가지표 등급 시각화(그래프) 생성 및 PDF 삽입
    if not isinstance(indicators, dict):
        print(f"[DEBUG][report_generator] 평가지표(indicators) 타입 오류(시각화): {type(indicators)}, 값: {indicators}")
        return ("평가지표 타입 오류(시각화)", str(type(indicators)))
    indicator_names = list(indicators.keys())
    grades = [1 if v['grade']=='우수' else 2 if v['grade']=='양호' else 3 if v['grade']=='불량' else 4 for v in indicators.values()]
    try:
        plt.figure(figsize=(6,2))
        plt.bar(indicator_names, grades, color=['#2979ff','#4caf50','#ff9800','#e53935'])
        plt.ylim(0.5,4.5)
        plt.yticks([1,2,3,4],['우수','양호','불량','해당없음'])
        plt.title('평가지표별 등급 시각화')
        plt.tight_layout()
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmpfile:
            plt.savefig(tmpfile.name)
            plt.close()
            pdf.image(tmpfile.name, w=170)
        os.unlink(tmpfile.name)
    except Exception as e:
        print(f"[DEBUG][report_generator] 반환: ('시각화 오류', {str(e)}) type: {type(('시각화 오류', str(e)))}")
        return ("시각화 오류", str(e))
    try:
        pdf.output(filename)
        print(f"[DEBUG][report_generator] 반환: (보고서 파일명, {filename}) type: {type(filename)}")
        result = ("보고서 파일명", filename)
        print(f"[DEBUG][report_generator] 최종 반환값: {result}, 타입: {type(result)}, 두번째 요소 타입: {type(result[1])}")
        if not isinstance(result[1], str):
            print(f"[ERROR][report_generator] 반환값 두번째 요소가 문자열이 아님: {result[1]}, 타입: {type(result[1])}")
        return result
    except Exception as e:
        print(f"[DEBUG][report_generator] 반환: ('보고서 저장 오류', {str(e)}) type: {type(('보고서 저장 오류', str(e)))}")
        print(f"[DEBUG][report_generator] 저장 오류 Exception 객체: {e}, 타입: {type(e)}")
        if hasattr(e, '__str__'):
            print(f"[DEBUG][report_generator] e.__str__(): {e.__str__()}")
        if hasattr(e, 'args'):
            print(f"[DEBUG][report_generator] e.args: {e.args}")
        err_msg = str(e)
        if isinstance(err_msg, tuple):
            err_msg = ', '.join(map(str, err_msg))
        return ("보고서 저장 오류", err_msg)

