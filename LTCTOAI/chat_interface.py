"""
chat_interface.py
- 장기요양 평가 보고서 생성기 Q&A 및 대화형 프롬프트 기능
- AI/규칙 기반 답변, 주요 질문/답변 기록
"""
import json

class ChatInterface:
    def __init__(self, law_mapping_path="law_mapping.json"):
        with open(law_mapping_path, encoding="utf-8") as f:
            self.law_mapping = json.load(f)

    def answer(self, question, context=None):
        # 예시: 평가지표, 법령, 감점사유 자동 안내
        for area, indicators in self.law_mapping.items():
            for idx, info in indicators.items():
                if idx in question or info["법령"] in question:
                    return f"[{area}] {idx}: 법령={info['법령']}, 지침={info['지침']}, 감점사유={info['감점사유']}"
        # 기타 규칙/AI 답변 확장 가능
        return "질문에 대한 답변을 찾을 수 없습니다."

    def get_faq(self):
        # 주요 Q&A 예시 반환
        return [
            {"Q": "체중 변화 기록 누락 시 감점 기준은?", "A": self.answer("체중 변화")},
            {"Q": "프로그램 참여 서명 누락 시 감점 기준은?", "A": self.answer("프로그램 참여")},
        ]
