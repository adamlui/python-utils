import json, os
import json5

def read(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json5.load(file)

def write(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
