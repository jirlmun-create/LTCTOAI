import indicator_mapping

def test_get_mapping():
    m1 = indicator_mapping.get_mapping('시설요양', '체중 변화 기록')
    assert m1['법령'] == '고시 제75조의2'
    assert m1['감점사유'] == '체중 변화 기록 누락 시 감점'
    m2 = indicator_mapping.get_mapping('시설요양', '투약 기록')
    assert m2['지침'] == '투약 관리 지침'
    assert m2['감점사유'] == '투약 기록 누락 시 감점'
    m3 = indicator_mapping.get_mapping('시설요양', '없는지표')
    assert m3 == {}
