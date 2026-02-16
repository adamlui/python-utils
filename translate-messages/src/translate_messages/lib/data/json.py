import json, os
import json5

def read(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        return json5.load(file)

def write(file_path, data, encoding='utf-8'):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding=encoding) as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
