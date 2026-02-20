from types import SimpleNamespace as sn

def from_dict(obj):
    for key, val in obj.items():
        if isinstance(val, dict):
            obj[key] = from_dict(val)
    return sn(**obj)
