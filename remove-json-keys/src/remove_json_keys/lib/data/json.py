import json, re
from pathlib import Path

import json5

from . import file

def read(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        return json5.load(file)

def remove_keys(json_dir, keys):
    keys_removed, keys_skipped, files_processed_cnt = [], [], 0
    json_dir = Path(json_dir)
    for file_path in json_dir.rglob('*.json'):
        json_data = file.read(file_path)
        modified = False
        for key in keys: # remove matched ones
            re_key = fr'"{re.escape(key)}"\s*:\s*(?:\{{[^}}]*\}}|"[^"]*"|\d+|true|false|null)\s*,?\s*'
            json_data, cnt = re.subn(re_key, '', json_data)
            rel_path = str(file_path.relative_to(json_dir))
            if cnt > 0:
                keys_removed.append((key, rel_path))
                modified = True
            else:
                keys_skipped.append((key, rel_path))
        if modified : file.write(file_path, json_data)
        files_processed_cnt += 1
    return keys_removed, keys_skipped, files_processed_cnt

def write(file_path, data, encoding='utf-8'):
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding=encoding) as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
