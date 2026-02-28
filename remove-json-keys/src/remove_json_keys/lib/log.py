import os, sys
from pathlib import Path
from types import SimpleNamespace as sn
if sys.platform == 'win32' : import colorama ; colorama.init() # enable ANSI color support

from . import data as datalib, pkg, settings

try : terminal_width = os.get_terminal_size()[0]
except OSError : terminal_width = 80

current_ver = datalib.json.read(Path(__file__).parent.parent / 'assets/data/package_data.json')['version']
next_maj_ver = pkg.get_next_maj_ver(current_ver)
_warned_keys = { 'cli': set(), 'config': set() }

colors = sn(
    nc='\x1b[0m',        # no color
    br='\x1b[1;91m',     # bright red
    by='\x1b[1;33m',     # bright yellow
    bo='\x1b[38;5;214m', # bright orange
    bg='\x1b[1;92m',     # bright green
    bc='\x1b[1;96m',     # bright cyan
    bw='\x1b[1;97m',     # bright white
    dg='\x1b[32m',       # dark green
    dy='\x1b[33m',       # dark yellow
    gry='\x1b[90m'       # gray
)

def data(msg, *args, **kwargs) : print(f'\n{colors.bw}{msg.format(*args, **kwargs)}{colors.nc}')
def dim(msg, *args, **kwargs) : print(f'\n{colors.gry}{msg.format(*args, **kwargs)}{colors.nc}')
def docs_url(cli) : tip(f'{cli.msgs.tip_FOR_MORE_HELP_VISIT}:\n{cli.urls.docs}')
def error(msg, *args, **kwargs) : print(f'\n{colors.br}ERROR: {msg.format(*args, **kwargs)}{colors.nc}')
def help_cmd(cli) : info(f"{cli.msgs.log_TYPE} '{cli.cmds[0]} --help' {cli.msgs.log_FOR_AVAIL_OPTIONS}\n")
def info(msg, *args, end='', **kwargs) : print(f'\n{colors.by}{msg.format(*args, **kwargs)}{colors.nc}', end=end)
def init_cmd(cli) : info(f"{cli.msgs.log_TYPE} '{cli.cmds[0]} --init' {cli.msgs.log_TO_CREATE_DEFAULT_CONFIG}\n")
def overwrite_print(msg, *args, **kwargs):
    sys.stdout.write('\r' + msg.format(*args, **kwargs).ljust(terminal_width)[:terminal_width])
def success(msg, *args, **kwargs) : print(f'\n{colors.bg}{msg.format(*args, **kwargs)}{colors.nc}')
def tip(msg, *args, **kwargs) : print(f'\n{colors.bc}TIP: {msg.format(*args, **kwargs)}{colors.nc}')
def version(cli):
    print(f'\n{colors.by}{cli.name}\n{colors.bw}{cli.msgs.log_VERSION.lower()}: {cli.version}{colors.nc}')
def warn(msg, *args, **kwargs) : print(f'\n{colors.bo}WARNING: {msg.format(*args, **kwargs)}{colors.nc}')

def warn_legacy_option(cli, flag: str, source: str) -> None:
    warned_set = _warned_keys[source]
    if flag in warned_set : return
    canonical_key = settings.get_canonical_key(flag)
    msg = f"{ cli.msgs.warn_CONFIG_FILE_KEY if source == 'config' else cli.msgs.warn_CLI_OPTION } {flag!r}"
    if canonical_key:
        canonical_ctrl = getattr(settings.controls, canonical_key, None)
        if source == 'cli' and canonical_ctrl:
            flags = [arg for arg in getattr(canonical_ctrl, 'args', []) if arg.startswith('-')]
            if flag.startswith('-') and len(flag) == 2: # show short flag replacement
                display_key = min(flags, key=len) if flags else f"--{canonical_key.replace('_', '-')}"
            else: # show long flag replacement
                long_flags = [flag for flag in flags if flag.startswith('--')]
                display_key = long_flags[0] if long_flags else f"--{canonical_key.replace('_', '-')}"
        else:
            display_key = canonical_key
        msg += f' {cli.msgs.warn_HAS_BEEN_REPLACED_BY} {display_key!r}'
    else:
        msg += f' {cli.msgs.warn_NO_LONGER_HAS_ANY_EFFECT}'
    msg += f' {cli.msgs.warn_AND_WILL_BE_REMOVED} @ v{next_maj_ver}'
    warn(msg) ; warned_set.add(flag)

def cmd_docs_url_exit(cli, msg='', cmd='help'):
    if msg : error(msg)
    help_cmd(cli) if cmd == 'help' else init_cmd(cli)
    docs_url(cli)
    sys.exit(1)

def debug(msg, cli=None, *args, **kwargs):
    if '--debug' not in sys.argv: return

    # Init --debug [target]
    debug_key=None
    debug_argidx = sys.argv.index('--debug')
    if debug_argidx +1 < len(sys.argv) and not sys.argv[debug_argidx +1].startswith('-'):
        debug_key = sys.argv[debug_argidx +1].replace('-', '_')

    if cli: # init data line
        if debug_key:
            data_val = getattr(cli.config, debug_key, f'cli.config key "{debug_key}" {cli.msgs.warn_NOT_FOUND.lower()}')
        else:
            data_val = cli.config
        msg += f'\n{colors.gry}{data_val}{colors.nc}'

    if args: # use 'em
        msg = msg.format(*args, **kwargs)

    print(f'\n{colors.by}DEBUG: {msg}{colors.nc}')

def final_summary(msgs, summary_dict):
    success(f'{msgs.log_ALL_JSON_PROCESSED}!')
    for name, file_set in summary_dict.items():
        if file_set:
            status = name.replace('_', ' ')
            status_color = colors.by if status == msgs.log_REMOVED.lower() else colors.gry
            data(f'{msgs.log_KEYS} {status}: {len(file_set)}')
            print(f'{status_color}[\n    ' + '\n    '.join(file_set) + f'\n]{colors.nc}')

def trunc(msg, end='\n'):
    truncated_lines = [
        line if len(line) < terminal_width else line[:terminal_width -4] + '...' for line in msg.splitlines()]
    print('\n'.join(truncated_lines), end=end)
