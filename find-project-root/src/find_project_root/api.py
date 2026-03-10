import os

import project_markers

def find_project_root(path= None, max_depth= 9, markers= None):
    current_dir = os.getcwd() if path is None else str(path)
    if not os.path.exists(current_dir):
        raise ValueError('Path does not exist: %s' % os.path.abspath(current_dir))
    if not markers : markers = project_markers
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
