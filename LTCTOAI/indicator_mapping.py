# 평가지표-법령/지침-감점사유 매핑 모듈
import json

INDICATOR_MAPPING_JSON = '''
{
  "시설요양": {
    "체중 변화 기록": {
      "법령": "고시 제75조의2",
      "지침": "장기요양급여 제공지침 2025",
      "감점사유": "체중 변화 기록 누락 시 감점"
    },
    "프로그램 참여 서명": {
      "법령": "고시 제80조",
      "지침": "프로그램 참여 지침",
      "감점사유": "프로그램 서명 누락 시 감점"
    },
    "투약 기록": {
      "법령": "고시 제90조",
      "지침": "투약 관리 지침",
      "감점사유": "투약 기록 누락 시 감점"
    }
  }
}
'''

INDICATOR_MAPPING = json.loads(INDICATOR_MAPPING_JSON)

def get_mapping(area, indicator):
    return INDICATOR_MAPPING.get(area, {}).get(indicator, {})
