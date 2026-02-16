import json, os, re
import json5
from . import file

def read(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json5.load(file)

def remove_keys(json_dir, keys):
    keys_removed, keys_skipped, files_processed_cnt = [], [], 0
    for root, _, files in os.walk(json_dir):
        for filename in files:
            if filename.endswith('.json'):
                file_path = os.path.join(root, filename)
                json_data = file.read(file_path)

                # Remove keys
                modified = False
                for key in keys:
                    re_key = fr'"{re.escape(key)}"\s*:\s*(?:\{{[^}}]*\}}|"[^"]*"|\d+|true|false|null)\s*,?\s*'
                    json_data, cnt = re.subn(re_key, '', json_data)
                    if cnt > 0:
                        keys_removed.append((key, os.path.relpath(file_path, json_dir)))
                        modified = True
                    else:
                        keys_skipped.append((key, os.path.relpath(file_path, json_dir)))

                # Save modified JSON
                if modified : file.write(file_path, json_data)

                files_processed_cnt += 1

    return keys_removed, keys_skipped, files_processed_cnt

def write(src_data, target_path):
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, 'w', encoding='utf-8') as file:
        json.dump(src_data, file, indent=2, ensure_ascii=False)
