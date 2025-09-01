import os
import pandas as pd
import json
from datetime import datetime

def save_to_dataset(result, file_path, meta=None, format='csv'):
    """
    분석 결과(result)를 datasets 폴더에 AI 학습용 데이터로 저장
    - result: str, pd.DataFrame, dict 등
    - file_path: 원본 파일 경로
    - meta: 추가 메타데이터(dict)
    - format: 'csv' 또는 'json'
    """
    dataset_dir = os.path.join(os.path.dirname(__file__), 'datasets')
    os.makedirs(dataset_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    meta = meta or {}
    meta.update({
        'source_file': file_path,
        'saved_at': timestamp
    })
    if isinstance(result, pd.DataFrame):
        out_path = os.path.join(dataset_dir, f'{base_name}_{timestamp}.csv')
        result.to_csv(out_path, index=False)
        # 메타데이터 저장
        with open(out_path + '.meta.json', 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        return out_path
    elif isinstance(result, dict):
        out_path = os.path.join(dataset_dir, f'{base_name}_{timestamp}.json')
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump({'meta': meta, 'data': result}, f, ensure_ascii=False, indent=2)
        return out_path
    elif isinstance(result, str):
        out_path = os.path.join(dataset_dir, f'{base_name}_{timestamp}.txt')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(result)
        with open(out_path + '.meta.json', 'w', encoding='utf-8') as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        return out_path
    else:
        # 기타 타입은 json으로 저장
        out_path = os.path.join(dataset_dir, f'{base_name}_{timestamp}.json')
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump({'meta': meta, 'data': str(result)}, f, ensure_ascii=False, indent=2)
        return out_path
