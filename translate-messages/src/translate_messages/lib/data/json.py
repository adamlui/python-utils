import json, os
import json5

def read(file_path):
    with open(file_path, 'r') as file:
        return json5.load(file)

def write(src_data, target_path):
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, 'w', encoding='utf-8') as file:
        json.dump(src_data, file, indent=2, ensure_ascii=False)
