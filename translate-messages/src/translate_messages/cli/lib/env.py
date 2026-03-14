import sys

def can_render_non_latin_scripts() -> bool: # e.g. ar, dv, zh
    import json, os, subprocess
    try:
        result = subprocess.run(
            ['ucs-detect', '--quick', '--save-json', '-'], # to stdout vs. file
            capture_output=True, text=True, timeout=0.1
        )
        return json.loads(result.stdout).get('wide', False)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return os.environ.get('WT_SESSION') is not None if sys.platform == 'win32' else True

def is_debug_mode() -> bool:
    return any(arg in ('--debug', '-V') for arg in sys.argv[1:])
