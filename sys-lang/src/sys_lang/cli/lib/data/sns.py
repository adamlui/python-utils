from types import SimpleNamespace as sn
from typing import Any, Dict

def from_dict(obj: Dict[str, Any]) -> sn:
    for key, val in obj.items():
        if isinstance(val, dict):
            obj[key] = from_dict(val)
    return sn(**obj)
