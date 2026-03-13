import sys

from .api import get_min_py
from . import cli

sys.modules[__name__].cli = cli # type: ignore
sys.modules[__name__] = get_min_py # type: ignore
