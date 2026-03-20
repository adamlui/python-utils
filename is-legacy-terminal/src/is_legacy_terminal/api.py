import os, sys

def is_legacy_terminal() -> bool:
    if sys.platform == 'win32':
        modern = any(os.environ.get(env_var) for env_var in ('WT_SESSION', 'ConEmuPID', 'VSCODE_TERM', 'TERM_PROGRAM'))
        legacy = os.environ.get('COMSPEC', '').lower().endswith('cmd.exe') or bool(os.environ.get('PSISE'))
        return legacy and not modern # since host shell can override
    else:
        return os.environ.get('TERM', '') in ('dumb', 'unknown')
