import sys

from .api import find_project_root

sys.modules[__name__] = find_project_root # type: ignore
