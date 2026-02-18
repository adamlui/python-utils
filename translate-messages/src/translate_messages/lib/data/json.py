import json
from pathlib import Path

import json5

def read(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        return json5.load(file)

def write(file_path, data, encoding='utf-8'):
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding=encoding) as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
