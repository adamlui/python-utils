import json, os, re
from . import file

def read(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def remove_keys(cli):
    keys_removed, keys_skipped, files_processed_cnt = [], [], 0
    for root, _, files in os.walk(cli.config.json_dir):
        for filename in files:
            if filename.endswith('.json'):
                file_path = os.path.join(root, filename)
                json_data = file.read(file_path)

                # Remove keys
                modified = False
                for key in cli.config.keys:
                    re_key = fr'"{re.escape(key)}"\s*:\s*(?:\{{[^}}]*\}}|"[^"]*"|\d+|true|false|null)\s*,?\s*'
                    json_data, cnt = re.subn(re_key, '', json_data)
                    if cnt > 0:
                        keys_removed.append((key, os.path.relpath(file_path, cli.config.json_dir)))
                        modified = True
                    else:
                        keys_skipped.append((key, os.path.relpath(file_path, cli.config.json_dir)))

                # Save modified JSON
                if modified : file.write(file_path, json_data)

                files_processed_cnt += 1

    return keys_removed, keys_skipped, files_processed_cnt
