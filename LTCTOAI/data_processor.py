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

# 병렬 PDF 분석 함수 (표준 방식)
from concurrent.futures import ProcessPoolExecutor, as_completed

def analyze_pdf(pdf_path):
    try:
        text = extract_text_from_pdf(pdf_path)
        # 여기서 추가 분석/구조화 로직 구현 가능
        return {'pdf_path': pdf_path, 'text': text, 'error': None}
    except Exception as e:
        return {'pdf_path': pdf_path, 'text': None, 'error': str(e)}

def analyze_pdfs_parallel(pdf_files, max_workers=None):
    results = []
    errors = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(analyze_pdf, f) for f in pdf_files]
        for future in as_completed(futures):
            result = future.result()
            if result['error']:
                errors.append(result)
            else:
                results.append(result)
    return results, errors

def evaluate_indicators(records, indicator_rules):
    """
    records: [{'indicator': '지표명', 'value': ..., ...}, ...]
    indicator_rules: {'지표명': {'excellent': 기준값, 'good': 기준값, 'bad': 기준값, ...}}
    """
    results = {}
    for r in records:
        ind = r['indicator']
        rule = indicator_rules.get(ind, {})
        value = r.get('value')
        if value is None:
            grade = '해당없음'
            reason = '데이터 없음'
        elif value >= rule.get('excellent', float('inf')):
            grade = '우수'
            reason = rule.get('excellent_reason', '')
        elif value >= rule.get('good', float('inf')):
            grade = '양호'
            reason = rule.get('good_reason', '')
        elif value >= rule.get('bad', float('-inf')):
            grade = '불량'
            reason = rule.get('bad_reason', '')
        else:
            grade = '해당없음'
            reason = '기준 미달'
        results[ind] = {'grade': grade, 'reason': reason}
    return results

# 파일간 교차점검 및 오류 검출 함수
# pdf_results: [{'pdf_path': ..., 'text': ..., ...}, ...]
def cross_check_errors(pdf_results, required_keywords):
    errors = []
    for kw in required_keywords:
        found = any(kw in r['text'] for r in pdf_results if r['text'])
        if not found:
            errors.append(f"필수 키워드 누락: {kw}")
    return errors
