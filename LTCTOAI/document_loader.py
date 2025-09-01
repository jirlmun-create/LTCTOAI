import os
import pandas as pd
from typing import Union

def load_document(path: str) -> Union[str, pd.DataFrame, dict]:
    ext = os.path.splitext(path)[-1].lower()
    if ext == '.pdf':
        # PDF 처리 예시
        from pdfminer.high_level import extract_text
        return extract_text(path)
    elif ext in ['.xls', '.xlsx']:
        return pd.read_excel(path)
    elif ext == '.csv':
        return pd.read_csv(path)
    elif ext in ['.doc', '.docx']:
        from docx import Document
        doc = Document(path)
        return '\n'.join([p.text for p in doc.paragraphs])
    elif ext == '.hwp':
        # HWP 처리 예시(라이브러리 설치 필요)
        try:
            import olefile
            # 실제 hwp 텍스트 추출 코드 필요
            return "(HWP 텍스트 추출 예시)"
        except ImportError:
            return "pyhwp/olefile 미설치"
    else:
        return "지원하지 않는 파일 형식입니다."
