from types import SimpleNamespace as sn

class flex_ns(sn): # to access by dot or bracket
    def __getitem__(self, key):
        return getattr(self, key)
    def __setitem__(self, key, val):
        setattr(self, key, val)
    def __contains__(self, key):
        return hasattr(self, key)
    def items(self):
        return self.__dict__.items()

def from_dict(obj):
    if isinstance(obj, dict):
        return flex_ns(**{key: from_dict(val) for key, val in obj.items()})
    if isinstance(obj, list):
        return [from_dict(item) for item in obj]
    return obj
