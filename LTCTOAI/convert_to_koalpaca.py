# KoAlpaca 파인튜닝용 데이터셋 변환 예시

import os
import json
import csv

def convert_to_koalpaca_format(input_path, output_path):
    """
    기존 분석 결과 파일(CSV/JSON/TXT)을 KoAlpaca 파인튜닝용 JSONL로 변환합니다.
    input_path: 원본 데이터 파일 경로
    output_path: 변환된 JSONL 파일 경로
    """
    data_list = []
    ext = os.path.splitext(input_path)[-1].lower()
    if ext == '.csv':
        with open(input_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                prompt = row.get('prompt') or row.get('input') or row.get('question')
                completion = row.get('completion') or row.get('output') or row.get('answer')
                if prompt and completion:
                    data_list.append({"instruction": prompt, "output": completion})
    elif ext == '.json':
        with open(input_path, encoding='utf-8') as f:
            items = json.load(f)
            for item in items:
                prompt = item.get('prompt') or item.get('input') or item.get('question')
                completion = item.get('completion') or item.get('output') or item.get('answer')
                if prompt and completion:
                    data_list.append({"instruction": prompt, "output": completion})
    elif ext == '.txt':
        with open(input_path, encoding='utf-8') as f:
            for line in f:
                if '\t' in line:
                    prompt, completion = line.strip().split('\t', 1)
                    data_list.append({"instruction": prompt, "output": completion})
    else:
        raise ValueError('지원하지 않는 파일 형식입니다.')
    # KoAlpaca 포맷(JSONL)으로 저장
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in data_list:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
    print(f"변환 완료: {output_path} (총 {len(data_list)}개)")

if __name__ == "__main__":
    # 예시 경로: datasets/sample.csv → datasets/koalpaca_train.jsonl
    convert_to_koalpaca_format('datasets/sample.csv', 'datasets/koalpaca_train.jsonl')
