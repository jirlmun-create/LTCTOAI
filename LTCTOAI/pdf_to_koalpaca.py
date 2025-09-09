import os
import json
from pdfminer.high_level import extract_text

PDF_DIR = "data/common_docs"
OUTPUT_JSONL = "datasets/koalpaca_ltc_finetune.jsonl"

def make_instruction(filename, text):
    base = os.path.splitext(os.path.basename(filename))[0]
    return [
        {
            "instruction": f"{base} 문서와 어르신 기록을 비교해 누락/감점 항목과 개선점을 알려줘.",
            "output": f"분석 결과 예시: {text[:100].replace('\n',' ')} ... (실제 기록과 비교 필요)"
        },
        {
            "instruction": f"{base} 문서 기준으로 평가지표별 등급과 감점 사유를 분석해줘.",
            "output": f"평가지표 분석 예시: {text[:100].replace('\n',' ')} ... (실제 기록과 비교 필요)"
        }
    ]

def main():
    samples = []
    for fname in os.listdir(PDF_DIR):
        if fname.lower().endswith('.pdf'):
            fpath = os.path.join(PDF_DIR, fname)
            try:
                text = extract_text(fpath)
                samples.extend(make_instruction(fname, text))
            except Exception as e:
                print(f"{fname} 추출 오류: {e}")
    os.makedirs(os.path.dirname(OUTPUT_JSONL), exist_ok=True)
    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
        for item in samples:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"변환 완료: {OUTPUT_JSONL} (총 {len(samples)}개)")

if __name__ == "__main__":
    main()
