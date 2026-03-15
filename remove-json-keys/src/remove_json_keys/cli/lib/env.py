import sys

def is_debug_mode() -> bool:
    return any(arg in ('--debug', '-V') for arg in sys.argv[1:])
