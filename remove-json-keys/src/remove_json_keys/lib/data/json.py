import json, re
from pathlib import Path

import json5

from . import file

def read(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        return json5.load(file)

def remove_keys(json_path, keys):
    keys_removed, keys_skipped, files_processed_cnt = [], [], 0
    for file_path in json_path.rglob('*.json'):
        json_data = file.read(file_path)
        modified = False
        for key in keys: # remove matched ones
            re_key = fr'"{re.escape(key)}"\s*:\s*(?:\{{[^}}]*\}}|"[^"]*"|\d+|true|false|null)\s*,?\s*'
            json_data, cnt = re.subn(re_key, '', json_data)
            rel_path = str(file_path.relative_to(json_path))
            if cnt > 0:
                keys_removed.append((key, rel_path))
                modified = True
            else:
                keys_skipped.append((key, rel_path))
        if modified : file.write(file_path, json_data)
        files_processed_cnt += 1
    return keys_removed, keys_skipped, files_processed_cnt

def write(file_path, data, encoding='utf-8', ensure_ascii=False, style='pretty'):
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding=encoding) as file:
        if style == 'pretty': # single key/val spans multi-lines
            json.dump(data, file, indent=2, ensure_ascii=ensure_ascii)
        elif style == 'compact': # single key/val per line
            file.write('{\n')
            items = list(data.items())
            for i, (key, val) in enumerate(items):
                line_end = ',' if i < len(items) - 1 else ''
                inner = json.dumps(val, ensure_ascii=ensure_ascii)
                inner = '{ ' + inner[1:-1] + ' }' # pad braces
                file.write(f'  "{key}": {inner}{line_end}\n')
            file.write('}')
        else: # minified to single line
            json.dump(data, file, separators=(',', ':'), ensure_ascii=ensure_ascii)
        file.write('\n') # trailing newline
