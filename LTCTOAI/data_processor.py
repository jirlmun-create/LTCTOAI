import fitz  # PyMuPDF
import os
from datetime import datetime, timedelta

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

def get_period_start(입소일, 평가시작일):
    입소 = datetime.strptime(입소일, "%Y-%m-%d")
    평가 = datetime.strptime(평가시작일, "%Y-%m-%d")
    return max(입소, 평가)

def get_period_end(퇴소일=None):
    today = datetime.today()
    전일 = today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    if 퇴소일:
        퇴소 = datetime.strptime(퇴소일, "%Y-%m-%d")
        return min(전일, 퇴소)
    return 전일

def is_in_period(date_str, 입소일, 평가시작일, 퇴소일=None):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    start = get_period_start(입소일, 평가시작일)
    end = get_period_end(퇴소일)
    return start <= date <= end

def mask_name(name):
    if len(name) == 3:
        return name[0] + '*' + name[2]
    return name

def mask_id(id_number):
    return id_number[:7] + '*' * (len(id_number) - 7)

def find_pdf_files(folder_path):
    pdf_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

def filter_records_by_period(records, 입소일, 평가시작일, 퇴소일=None):
    # records: [{'date': 'YYYY-MM-DD', ...}, ...]
    return [r for r in records if is_in_period(r['date'], 입소일, 평가시작일, 퇴소일)]
