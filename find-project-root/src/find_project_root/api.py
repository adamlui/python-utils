import os, sys
if sys.version_info >= (3, 4) : from pathlib import Path
else : Path = str
from typing import Optional, Union, List

import project_markers

def find_project_root(
    path: Optional[Union[str, Path]] = None,
    max_depth: int = 9,
    markers: Optional[List[str]] = None
) -> Optional[str]:
    current_dir = os.getcwd() if path is None else str(path)
    if not os.path.exists(current_dir):
        raise ValueError(f'Path does not exist: {os.path.abspath(current_dir)}')
    if not markers: markers = project_markers # type: ignore
    for _ in range(max_depth):
        try : dir_files = os.listdir(current_dir)
        except (OSError, IOError, PermissionError):
            return None
        if any(marker in dir_files for marker in markers): # type: ignore
            return str(current_dir)
        parent = os.path.dirname(current_dir)
        if parent == current_dir : break # at fs root
        current_dir = parent
    return None
