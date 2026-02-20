import os, sys
from types import SimpleNamespace as sn
if sys.platform == 'win32' : import colorama ; colorama.init() # enable ANSI color support

try : terminal_width = os.get_terminal_size()[0]
except OSError : terminal_width = 80

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
def error(msg, *args, **kwargs) : print(f'\n{colors.br}ERROR: {msg.format(*args, **kwargs)}{colors.nc}')
def info(msg, *args, end='', **kwargs) : print(f'\n{colors.by}{msg.format(*args, **kwargs)}{colors.nc}', end=end)
def overwrite_print(msg, *args, **kwargs):
    sys.stdout.write('\r' + msg.format(*args, **kwargs).ljust(terminal_width)[:terminal_width])
def success(msg, *args, **kwargs) : print(f'\n{colors.bg}{msg.format(*args, **kwargs)}{colors.nc}')
def tip(msg, *args, **kwargs) : print(f'\n{colors.bc}TIP: {msg.format(*args, **kwargs)}{colors.nc}')
def version(cli) : print(f'\n{colors.by}{cli.name}\n{colors.bw}version: {cli.version}{colors.nc}')
def warn(msg, *args, **kwargs) : print(f'\n{colors.bo}WARNING: {msg.format(*args, **kwargs)}{colors.nc}')

def debug(msg, cli=None, *args, **kwargs):
    if '--debug' not in sys.argv: return

    # Init --debug [target]
    debug_key=None
    debug_argidx = sys.argv.index('--debug')
    if debug_argidx +1 < len(sys.argv) and not sys.argv[debug_argidx +1].startswith('-'):
        debug_key = sys.argv[debug_argidx +1].replace('-', '_')

    if cli: # init data line
        data_val = getattr(cli.config, debug_key, f'cli.config key "{debug_key}" not found') if debug_key \
              else cli.config
        msg += f'\n{colors.gry}{data_val}{colors.nc}'
    
    if args: # use 'em
        msg = msg.format(*args, **kwargs)
    
    print(f'\n{colors.by}DEBUG: {msg}{colors.nc}')

def final_summary(msgs, summary_dict):
    success(f'\n{msgs.log_ALL_JSON_UPDATED}!')
    for name, lang_set in summary_dict.items():
        if lang_set:
            status = name.replace('_', ' ')
            status_color = colors.by if status == 'translated' else colors.bg if status == 'added' else colors.gry
            data(f'{msgs.log_LANGUAGES} {status}: {len(lang_set)}')
            print(f"{status_color}[ {', '.join(lang_set)} ]{colors.nc}")

def trunc(msg, end='\n'):
    truncated_lines = [
        line if len(line) < terminal_width else line[:terminal_width -4] + '...' for line in msg.splitlines()]
    print('\n'.join(truncated_lines), end=end)
