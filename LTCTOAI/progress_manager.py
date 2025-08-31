import os
from concurrent.futures import ProcessPoolExecutor, as_completed

class ProgressManager:
    def __init__(self, update_callback=None, error_callback=None):
        self.update_callback = update_callback
        self.error_callback = error_callback

    def analyze_pdfs_parallel(self, pdf_files, analyze_func):
        total_files = len(pdf_files)
        results = []
        errors = []
        with ProcessPoolExecutor() as executor:
            future_to_pdf = {executor.submit(analyze_func, pdf): pdf for pdf in pdf_files}
            for idx, future in enumerate(as_completed(future_to_pdf)):
                pdf_path = future_to_pdf[future]
                if self.update_callback:
                    self.update_callback(idx, total_files, pdf_path)
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    errors.append((pdf_path, str(e)))
                    if self.error_callback:
                        self.error_callback(pdf_path, str(e))
        return results, errors
