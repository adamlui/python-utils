from pathlib import Path
import shutil, sys
from types import SimpleNamespace as sn

def main():
    paths = sn(root=Path(__file__).parent.parent)
    paths.util_msgs = paths.root / 'utils/data/messages.json'
    sys.path.insert(0, str(paths.root / 'src'))

    from translate_messages.lib import data, log # type: ignore

    msgs = sn(**{ key:val['message'] for key,val in data.json.read(paths.util_msgs)['clean'].items() })

    for target in ['dist', 'build', '*_cache', '__pycache__', '*.egg-info']:
        for path in Path('.').rglob(target):
            if path.is_dir() : shutil.rmtree(path) ; log.info(f'{msgs.log_REMOVED} {path}/')

    log.success(f'{msgs.log_CLEAN_COMPLETE}!')

if __name__ == '__main__' : main()
