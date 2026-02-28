import re

def get_next_maj_ver(version: str) -> str: # e.g. '1.2.3' -> '2.0.0'
    major = re.match(r'^(\d+)\..*', version)
    if not major : raise ValueError(f'Invalid version string: {version!r}')
    return f'{ int(major.group(1)) +1 }.0.0'
