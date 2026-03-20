import sys

from .api import is_legacy_terminal
from . import cli

sys.modules[__name__].cli = cli # type: ignore
sys.modules[__name__] = is_legacy_terminal # type: ignore
