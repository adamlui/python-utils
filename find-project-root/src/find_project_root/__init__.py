import sys

from .api import find_project_root
from . import cli

sys.modules[__name__].cli = cli # type: ignore
sys.modules[__name__] = find_project_root # type: ignore
