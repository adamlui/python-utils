import json
from pathlib import Path

import json5

def read(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        return json5.load(file)

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
