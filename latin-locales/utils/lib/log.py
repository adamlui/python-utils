import os, sys
from types import SimpleNamespace as sn
from typing import Optional
if sys.platform == 'win32' : import colorama ; colorama.init() # enable ANSI color support

try : terminal_width = os.get_terminal_size()[0]
except OSError : terminal_width = 80

def data(msg: str, *args, no_newline: bool = False, **kwargs) -> None:
    print(f'\n{colors.bw}{msg.format(*args, **kwargs)}{colors.nc}', end='' if no_newline else None)
def dim(msg: str, *args, no_newline: bool = False, **kwargs) -> None:
    print(f'\n{colors.gry}{msg.format(*args, **kwargs)}{colors.nc}', end='' if no_newline else None)
def error(msg: str, *args, **kwargs) -> None : print(f'\n{colors.br}ERROR: {msg.format(*args, **kwargs)}{colors.nc}')
def info(msg: str, *args, end: str = '', **kwargs) -> None:
    print(f'\n{colors.by}{msg.format(*args, **kwargs)}{colors.nc}', end=end)
def line_break() : print()
def overwrite_print(msg: str, *args, **kwargs) -> None:
    sys.stdout.write('\r' + msg.format(*args, **kwargs).ljust(terminal_width)[:terminal_width])
def success(msg: str, *args, **kwargs) -> None : print(f'\n{colors.bg}{msg.format(*args, **kwargs)}{colors.nc}')
def tip(msg: str, *args, **kwargs) -> None : print(f'\n{colors.bc}TIP: {msg.format(*args, **kwargs)}{colors.nc}')
def warn(msg: str, *args, **kwargs) -> None : print(f'\n{colors.bo}WARNING: {msg.format(*args, **kwargs)}{colors.nc}')

def debug(msg: str, cli: Optional[sn] = None, *args, **kwargs) -> None:
    from . import env
    if not env.is_debug_mode() : return

    # Init --debug [target]
    debug_key=None
    debug_argidx = sys.argv.index('--debug') if '--debug' in sys.argv else sys.argv.index('-V')
    if debug_argidx +1 < len(sys.argv) and not sys.argv[debug_argidx +1].startswith('-'):
        debug_key = sys.argv[debug_argidx +1].replace('-', '_')

    if cli: # init data line
        if debug_key:
            data_val = getattr(cli.config, debug_key, f'cli.config key {debug_key!r} {cli.msgs.warn_NOT_FOUND.lower()}')
        else:
            data_val = cli.config
        msg += f'\n{colors.gry}{data_val}{colors.nc}'

    if args: # use 'em
        msg = msg.format(*args, **kwargs)

    print(f'\n{colors.by}DEBUG: {msg}{colors.nc}')

def trunc(msg: str, end: str = '\n') -> None:
    truncated_lines = [
        line if len(line) < terminal_width else line[:terminal_width -4] + '...' for line in msg.splitlines()]
    print('\n'.join(truncated_lines), end=end)
