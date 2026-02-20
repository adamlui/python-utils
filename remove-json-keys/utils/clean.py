from pathlib import Path
import shutil
from types import SimpleNamespace as sn

from remove_json_keys.lib import data, log

def main():
    msgs_path = Path(__file__).parent.parent / 'utils/data/messages.json'
    msgs = sn(**{ key:val['message'] for key,val in data.json.read(msgs_path)['clean'].items() })

    for target in ['dist', 'build', '*_cache', '__pycache__', '*.egg-info']:
        for path in Path('.').rglob(target):
            if path.is_dir() : shutil.rmtree(path) ; log.info(f'{msgs.log_REMOVED} {path}/')

    log.success(f'{msgs.log_CLEAN_COMPLETE}!')

if __name__ == '__main__' : main()
