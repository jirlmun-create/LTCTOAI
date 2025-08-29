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

REPORTS_DIR = "reports"

def ensure_reports_dir():
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

# 보고서 파일명 자동 생성 (어르신명, 평가기간, 버전)
def generate_report_filename(name_masked, period_start, period_end):
    # Windows 파일명에 사용할 수 없는 문자(:, *, ?, <, >, |, ", /, \\)를 모두 '_'로 대체
    def sanitize_filename(s):
        return re.sub(r'[\\/*?:"<>|]', '_', s)
    date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = sanitize_filename(name_masked)
    safe_start = sanitize_filename(period_start)
    safe_end = sanitize_filename(period_end)
    filename = f"report_{safe_name}_{safe_start}_{safe_end}_{date_str}.pdf"
    return os.path.join(REPORTS_DIR, filename)

# PDF 보고서 템플릿 클래스 (확장 가능)
class ReportPDF(FPDF):
    def header(self):
        self.set_font("NanumGothic", "", 16)
        self.cell(0, 10, "장기요양 평가 보고서", ln=True, align="C")
        self.ln(5)
    def footer(self):
        self.set_y(-15)
        self.set_font("NanumGothic", "", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

# 보고서 생성 함수 (핵심 정보, 평가지표, 교차점검, 오류 하이라이트)
def create_report(data, indicators, cross_errors, period_start, period_end):
    ensure_reports_dir()
    filename = generate_report_filename(data['name_masked'], period_start, period_end)
    pdf = ReportPDF()
    # 한글 폰트 등록 (폰트 파일은 프로젝트 폴더에 있어야 함)
    pdf.add_font('NanumGothic', '', 'NanumGothic.ttf', uni=True)
    pdf.add_page()
    pdf.set_font("NanumGothic", size=12)
    # 기본 정보
    pdf.cell(0, 10, f"성명(마스킹): {data['name_masked']}", ln=True)
    pdf.cell(0, 10, f"생년월일: {data.get('birth')}", ln=True)
    pdf.cell(0, 10, f"성별: {data.get('gender')}", ln=True)
    pdf.cell(0, 10, f"입소일: {data.get('admit_date')}", ln=True)
    pdf.cell(0, 10, f"퇴소일: {data.get('discharge_date', '-')}", ln=True)
    pdf.cell(0, 10, f"평가기간: {period_start} ~ {period_end}", ln=True)
    pdf.cell(0, 10, f"시설명: {data.get('facility')}", ln=True)
    pdf.ln(5)
    # 평가지표별 결과
    pdf.set_font("NanumGothic", "", 13)
    pdf.cell(0, 10, "평가지표별 결과", ln=True)
    pdf.set_font("NanumGothic", size=12)
    for idx, item in indicators.items():
        pdf.cell(0, 10, f"{idx}: {item['grade']} - {item['reason']}", ln=True)
    pdf.ln(5)
    # 교차점검 오류
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
    # 기타 확장 영역(시각화, Q&A 등)
    # ...추후 확장...
    pdf.output(filename)
    return filename

if __name__ == "__main__":
    # 샘플 데이터
    data = {
        'name_masked': '김*수',
        'birth': '1940-01-01',
        'gender': '여',
        'admit_date': '2024-01-10',
        'discharge_date': '2025-07-15',
        'facility': '행복요양원'
    }
    period_start = '2024-02-01'
    period_end = '2025-07-15'
    indicators = {
        '체중 변화 기록': {'grade': '우수', 'reason': '매월 기록 누락 없음'},
        '프로그램 참여 서명': {'grade': '불량', 'reason': '3회 이상 누락'},
        '투약 기록': {'grade': '양호', 'reason': '1회 누락, 경미'}
    }
    cross_errors = [
        '프로그램 서명 누락: 3회',
        '투약 기록 누락: 1회'
    ]
    filename = create_report(data, indicators, cross_errors, period_start, period_end)
    print(f"보고서가 생성되었습니다: {filename}")
