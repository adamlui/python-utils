import os, re

def removeKeys(cli):
    keys_removed, keys_skipped, processed_cnt = [], [], 0
    for root, _, files in os.walk(cli.json_dir):
        for filename in files:
            if filename.endswith('.json'):

                # Open found JSON file
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf-8') as f : data = f.read()

                # Remove keys
                modified = False
                for key in cli.remove_keys:
                    re_key = fr'"{re.escape(key)}".*?[,\n]+.*?(?="|$)'
                    data, count = re.subn(re_key, '', data)
                    if count > 0:
                        keys_removed.append((key, os.path.relpath(file_path, cli.json_dir)))
                        modified = True
                    else : keys_skipped.append((key, os.path.relpath(file_path, cli.json_dir)))
                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f : f.write(data)
                processed_cnt += 1

    return keys_removed, keys_skipped, processed_cnt
