import os

def get_patient_list():
    base_dir = os.path.join(os.path.dirname(__file__), 'data', 'patient_docs')
    folders = ['시설요양', '주간보호', '방문요양']
    patient_list = []
    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        if os.path.exists(folder_path):
            for root, dirs, files in os.walk(folder_path):
                pdf_exists = any(fname.lower().endswith('.pdf') for fname in files)
                if pdf_exists:
                    rel_path = os.path.relpath(root, folder_path)
                    if rel_path == '.':
                        display_name = f"{folder}"
                    else:
                        display_name = f"{folder}/{rel_path}"
                    patient_list.append(display_name)
    return patient_list
