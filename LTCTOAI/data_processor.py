import concurrent.futures
from datetime import datetime, timedelta

def get_period_start(admit_date, eval_start_date):
    admit = datetime.strptime(admit_date, "%Y-%m-%d")
    eval_start = datetime.strptime(eval_start_date, "%Y-%m-%d")
    return max(admit, eval_start)

def get_period_end(discharge_date=None):
    today = datetime.today()
    prev_day = today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    if discharge_date:
        discharge = datetime.strptime(discharge_date, "%Y-%m-%d")
        return min(prev_day, discharge)
    return prev_day

def is_in_period(date_str, admit_date, eval_start_date, discharge_date=None):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    start = get_period_start(admit_date, eval_start_date)
    end = get_period_end(discharge_date)
    return start <= date <= end

def analyze_pdf(pdf_path):
    # PDF 분석 코드 (샘플)
    import os
    if not os.path.exists(pdf_path):
        return None, f"no such file: '{pdf_path}'"
    try:
        # 실제 분석 로직은 추후 구현
        result = {"pdf_path": pdf_path, "text": "샘플 분석 결과"}
        return result, None
    except Exception as e:
        return None, str(e)

def analyze_pdfs_parallel(pdf_files, admit_date, eval_start_date, discharge_date=None):
    # 기간 필터링
    filtered_files = []
    for f in pdf_files:
        # 파일명에 날짜가 포함되어 있다고 가정 (예: ..._2024-03-01.pdf)
        try:
            date_part = f.split('_')[-1].replace('.pdf','')
            if is_in_period(date_part, admit_date, eval_start_date, discharge_date):
                filtered_files.append(f)
        except:
            pass
    results = []
    errors = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(analyze_pdf, f) for f in filtered_files]
        for future in concurrent.futures.as_completed(futures):
            result, error = future.result()
            if error:
                errors.append(error)
            else:
                results.append(result)
    return results, errors
import fitz  # PyMuPDF
import os
from datetime import datetime, timedelta

def extract_text_from_pdf(pdf_path):
    """
    PDF 파일에서 전체 텍스트를 추출합니다.
    Args:
        pdf_path (str): PDF 파일 경로
    Returns:
        str: 전체 텍스트
    """
    import os
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"no such file: '{pdf_path}'")
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    except Exception as e:
        print(f"[ERROR] PDF 추출 오류: {pdf_path} - {e}")
        raise

def get_period_start(입소일, 평가시작일):
    """
    입소일과 평가시작일 중 더 최근 날짜 반환
    Args:
        입소일 (str): YYYY-MM-DD
        평가시작일 (str): YYYY-MM-DD
    Returns:
        datetime: 시작일
    """
    입소 = datetime.strptime(입소일, "%Y-%m-%d")
    평가 = datetime.strptime(평가시작일, "%Y-%m-%d")
    return max(입소, 평가)

def get_period_end(퇴소일=None):
    """
    퇴소일이 있으면 퇴소일과 전일(어제) 중 더 과거 날짜, 없으면 전일(어제) 반환
    Args:
        퇴소일 (str, optional): YYYY-MM-DD
    Returns:
        datetime: 종료일
    """
    today = datetime.today()
    전일 = today.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    if 퇴소일:
        퇴소 = datetime.strptime(퇴소일, "%Y-%m-%d")
        return min(전일, 퇴소)
    return 전일

def is_in_period(date_str, 입소일, 평가시작일, 퇴소일=None):
    """
    날짜가 점검기간 내에 포함되는지 여부 반환
    Args:
        date_str (str): YYYY-MM-DD
        입소일 (str): YYYY-MM-DD
        평가시작일 (str): YYYY-MM-DD
        퇴소일 (str, optional): YYYY-MM-DD
    Returns:
        bool: 점검기간 포함 여부
    """
    date = datetime.strptime(date_str, "%Y-%m-%d")
    start = get_period_start(입소일, 평가시작일)
    end = get_period_end(퇴소일)
    return start <= date <= end

def mask_name(name):
    """
    이름 마스킹(예: 김*수)
    """
    if len(name) == 3:
        return name[0] + '*' + name[2]
    return name

def mask_id(id_number):
    """
    주민번호 등 마스킹
    """
    return id_number[:7] + '*' * (len(id_number) - 7)

def find_pdf_files(folder_path):
    """
    폴더 내 모든 PDF 파일 경로 반환
    """
    pdf_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(root, file))
    return pdf_files

def filter_records_by_period(records, 입소일, 평가시작일, 퇴소일=None):
    """
    기록 리스트에서 점검기간에 해당하는 것만 필터링
    Args:
        records (list): [{'date': 'YYYY-MM-DD', ...}, ...]
    Returns:
        list: 점검기간 내 기록
    """
    return [r for r in records if is_in_period(r['date'], 입소일, 평가시작일, 퇴소일)]

# 병렬 PDF 분석 함수 (표준 방식)
from concurrent.futures import ProcessPoolExecutor, as_completed

def analyze_pdf(pdf_path):
    """
    PDF 파일 분석 및 텍스트 추출, 오류 반환
    Returns:
        tuple: (result, error)
    """
    try:
        text = extract_text_from_pdf(pdf_path)
        result = {'pdf_path': pdf_path, 'text': text}
        return result, None
    except Exception as e:
        print(f"[ERROR] analyze_pdf: {pdf_path} - {e}")
        return None, str(e)

def analyze_pdfs_parallel(pdf_files, max_workers=None):
    """
    PDF 파일 리스트 병렬 분석
    Returns:
        tuple: (정상 결과 리스트, 오류 리스트)
    """
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
    기록별 평가지표 등급 산출
    Args:
        records (list): [{'indicator': '지표명', 'value': ..., ...}, ...]
        indicator_rules (dict): {'지표명': {'excellent': 기준값, ...}}
    Returns:
        dict: {'지표명': {'grade': 등급, 'reason': 이유}}
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
    """
    PDF 결과에서 필수 키워드 누락 여부 교차점검
    Args:
        pdf_results (list): [{'pdf_path': ..., 'text': ..., ...}, ...]
        required_keywords (list): 필수 키워드 리스트
    Returns:
        list: 누락된 키워드 오류 메시지 리스트
    """
    errors = []
    dict_results = []
    for r in pdf_results:
        if isinstance(r, dict) and 'text' in r:
            dict_results.append(r)
        elif isinstance(r, (list, tuple)) and len(r) > 0 and isinstance(r[0], str):
            dict_results.append({'text': r[0]})
    for kw in required_keywords:
        found = any(kw in r['text'] for r in dict_results if r['text'])
        if not found:
            errors.append(f"필수 키워드 누락: {kw}")
    return errors
