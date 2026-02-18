from pathlib import Path
from types import SimpleNamespace as sn

from . import data

def get_msgs():
    msgs_path = Path(__file__).parent.parent / 'assets' / 'data' / 'messages.json'
    return sn(**{ key: val.message for key, val in data.json.read(msgs_path).items() })
