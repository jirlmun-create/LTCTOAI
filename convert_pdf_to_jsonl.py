import os
from pdfminer.high_level import extract_text
import json

# 1. PDF에서 텍스트 추출
def extract_pdf_text(pdf_path):
    return extract_text(pdf_path)

# 2. 텍스트를 문단 단위로 분할 (간단 예시)
def split_paragraphs(text):
    paras = [p.strip() for p in text.split('\n') if len(p.strip()) > 30]
    return paras

# 3. 파인튜닝용 JSONL 생성 (instruction/response)
def make_jsonl(paragraphs, out_path):
    with open(out_path, 'w', encoding='utf-8') as f:
        for para in paragraphs:
            sample = {
                "instruction": "아래 내용을 요약하라.",
                "input": para,
                "output": "(여기에 요약문을 직접 입력 또는 자동 요약 결과를 넣으세요)"
            }
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')

if __name__ == "__main__":
    pdf_path = "주간보호.PDF"
    out_jsonl = "train.jsonl"
    text = extract_pdf_text(pdf_path)
    paragraphs = split_paragraphs(text)
    make_jsonl(paragraphs, out_jsonl)
    print(f"{out_jsonl} 파일이 생성되었습니다. (샘플 개수: {len(paragraphs)})")
