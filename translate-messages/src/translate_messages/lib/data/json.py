import json
from pathlib import Path
from typing import Any, Dict, Union

import json5

def flatten(json: Dict[str, Any], key: str = 'message') -> Dict[str, Any]: # eliminate need to ref nested keys
    flat_obj = {}
    for json_key in json:
        val = json[json_key]
        flat_obj[json_key] = val[key] if isinstance(val, dict) and key in val else val
    return flat_obj

def is_valid(file_path, format='json'):
    file_path = Path(file_path)
    if not file_path.exists():
        return False
    try : file_text = file_path.read_text(encoding='utf-8')
    except Exception:
        return False
    if format == 'json':
        try : json.loads(file_text) ; return True
        except Exception : return False
    elif format == 'json5':
        try : json5.loads(file_text) ; return True
        except Exception : return False
    else:
        raise ValueError(f"Unsupported format {format!r}. Expected 'json' or 'json5'")

def read(input: Union[str, Path], encoding: str = 'utf-8') -> Any:
    input_str = str(input)
    if input_str.endswith(('.json', '.json5')):
        with open(input_str, 'r', encoding=encoding) as file:
           return json5.load(file)
    else : return json5.loads(input_str)

def write(file_path, data, encoding='utf-8', ensure_ascii=False, style='pretty', atomic=True):
    from . import file
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    if style == 'pretty': # single key/val spans multi-lines
        json_str = json.dumps(data, indent=2, ensure_ascii=ensure_ascii)
    elif style == 'compact': # single key/val per line
        lines = ['{']
        items = list(data.items())
        for idx, (key, val) in enumerate(items):
            line_end = ',' if idx < len(items) -1 else ''
            inner = f'{{ {json.dumps(val, ensure_ascii=ensure_ascii)[1:-1]} }}'
            lines.append(f'  "{key}": {inner}{line_end}')
        lines.append('}')
        json_str = '\n'.join(lines)
    else: # minified to single line
        json_str = json.dumps(data, separators=(',', ':'), ensure_ascii=ensure_ascii)
    json_str += '\n'
    getattr(file, 'atomic_write' if atomic else 'write')(file_path, json_str, encoding=encoding)
