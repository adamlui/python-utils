import sys

from .api import is_unicode_supported
from . import cli

sys.modules[__name__].cli = cli # type: ignore
sys.modules[__name__] = is_unicode_supported # type: ignore
