from typing import List

def parse(val: str) -> List[str]:
    if not val : return []
    return [item.strip() for item in val.split(',') if item.strip()]
