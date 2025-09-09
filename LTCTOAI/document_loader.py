import os
import pandas as pd
from typing import Union

def load_document(path: str, cancel_callback=None) -> Union[str, pd.DataFrame, dict]:
    ext = os.path.splitext(path)[-1].lower()
    if ext == '.pdf':
        # PDF 앞 2페이지만 샘플링
        try:
            from pdfminer.pdfpage import PDFPage
            from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
            from pdfminer.converter import TextConverter
            from pdfminer.layout import LAParams
            from io import StringIO
            output = StringIO()
            with open(path, 'rb') as f:
                rsrcmgr = PDFResourceManager()
                device = TextConverter(rsrcmgr, output, laparams=LAParams())
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                for i, page in enumerate(PDFPage.get_pages(f)):
                    if cancel_callback and cancel_callback():
                        return "분석이 취소되었습니다."
                    if i >= 2:
                        break
                    interpreter.process_page(page)
                device.close()
            preview = output.getvalue().strip()
            if not preview:
                return "PDF 파일에서 미리보기로 추출할 내용이 없습니다."
            if len(preview) < 20:
                return f"PDF 미리보기 내용이 너무 짧습니다: {preview}"
            return preview
        except Exception as e:
            return f"PDF 샘플링 오류: {str(e)}"
    elif ext in ['.xls', '.xlsx']:
        # 엑셀 앞 100행만 샘플링
        try:
            df = pd.read_excel(path)
            if cancel_callback:
                for i in range(min(100, len(df))):
                    if cancel_callback():
                        return "분석이 취소되었습니다."
            if df.empty:
                return "엑셀 파일에서 미리보기로 추출할 내용이 없습니다."
            return df.head(100)
        except Exception as e:
            return f"엑셀 파일 분석 오류: {str(e)}"
    elif ext == '.csv':
        try:
            df = pd.read_csv(path)
            if cancel_callback:
                for i in range(min(100, len(df))):
                    if cancel_callback():
                        return "분석이 취소되었습니다."
            if df.empty:
                return "CSV 파일에서 미리보기로 추출할 내용이 없습니다."
            return df.head(100)
        except Exception as e:
            return f"CSV 파일 분석 오류: {str(e)}"
    elif ext in ['.doc', '.docx']:
        try:
            from docx import Document
            doc = Document(path)
            texts = []
            for i, p in enumerate(doc.paragraphs):
                if cancel_callback and cancel_callback():
                    return "분석이 취소되었습니다."
                if i >= 30:
                    break
                texts.append(p.text)
            preview = '\n'.join(texts).strip()
            if not preview:
                return "워드 파일에서 미리보기로 추출할 내용이 없습니다."
            if len(preview) < 20:
                return f"워드 미리보기 내용이 너무 짧습니다: {preview}"
            return preview
        except Exception as e:
            return f"워드 파일 분석 오류: {str(e)}"
    else:
        if cancel_callback and cancel_callback():
            return "분석이 취소되었습니다."
        return "지원하지 않는 파일 형식입니다."
