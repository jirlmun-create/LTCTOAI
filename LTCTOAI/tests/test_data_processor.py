import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from data_processor import filter_records_by_period, evaluate_indicators

def test_filter_records_by_period():
    records = [
        {'date': '2024-01-09', 'indicator': '체중 변화', 'value': 12},
        {'date': '2024-02-01', 'indicator': '체중 변화', 'value': 13},
        {'date': '2025-07-15', 'indicator': '프로그램 참여', 'value': 5},
        {'date': '2025-08-29', 'indicator': '투약 기록', 'value': 10},
    ]
    입소일 = '2024-01-10'
    평가시작일 = '2024-02-01'
    퇴소일 = '2025-07-15'
    filtered = filter_records_by_period(records, 입소일, 평가시작일, 퇴소일)
    assert len(filtered) == 2
    assert filtered[0]['date'] == '2024-02-01'
    assert filtered[1]['date'] == '2025-07-15'

def test_evaluate_indicators():
    records = [
        {'indicator': '체중 변화', 'value': 13},
        {'indicator': '프로그램 참여', 'value': 5},
        {'indicator': '투약 기록', 'value': 10},
    ]
    indicator_rules = {
        '체중 변화': {'excellent': 12, 'excellent_reason': '매월 기록 누락 없음'},
        '프로그램 참여': {'excellent': 5, 'excellent_reason': '5회 이상 참여'},
        '투약 기록': {'excellent': 10, 'excellent_reason': '10회 이상 투약'},
    }
    results = evaluate_indicators(records, indicator_rules)
    assert results['체중 변화']['grade'] == '우수'
    assert results['프로그램 참여']['grade'] == '우수'
    assert results['투약 기록']['grade'] == '우수'

def test_period_filtering():
    # 2024-02-01 ~ 2025-07-15
    from data_processor import is_in_period
    assert is_in_period('2024-02-01', '2024-01-10', '2024-02-01', '2025-07-15')
    assert is_in_period('2025-07-15', '2024-01-10', '2024-02-01', '2025-07-15')
    assert not is_in_period('2025-08-01', '2024-01-10', '2024-02-01', '2025-07-15')

def test_analyze_pdf():
    from data_processor import analyze_pdf
    res = analyze_pdf('샘플_2024-03-01.pdf')
    print('analyze_pdf 반환값:', res)
    assert isinstance(res, tuple)
    result, error = res
    assert error is not None
    assert result is None
