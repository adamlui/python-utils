import os, sys
from types import SimpleNamespace as sns
import colorama

try:
    terminal_width = os.get_terminal_size()[0]
except OSError:
    terminal_width = 80

colorama.init() # enable compatibility w/ Windows
colors = sns(
    nc='\x1b[0m',        # no color
    br='\x1b[1;91m',     # bright red
    by='\x1b[1;33m',     # bright yellow
    bo='\x1b[38;5;214m', # bright orange
    bg='\x1b[1;92m',     # bright green
    bw='\x1b[1;97m',     # bright white
    dg='\x1b[32m',       # dark green
    dy='\x1b[33m',       # dark yellow
    gry='\x1b[90m'       # gray
)

def data(msg) : print(f'\n{colors.bw}{msg}{colors.nc}')
def dim(msg) : print(f'\n{colors.gry}{msg}{colors.nc}')
def error(msg) : print(f'\n{colors.br}ERROR: {msg}{colors.nc}')
def info(msg, end='') : print(f'\n{colors.by}{msg}{colors.nc}', end=end)
def overwrite_print(msg) : sys.stdout.write('\r' + msg.ljust(terminal_width)[:terminal_width])
def tip(msg) : print(f'\n{colors.by}TIP: {msg}{colors.nc}')
def success(msg) : print(f'\n{colors.bg}{msg}{colors.nc}')
def warn(msg) : print(f'\n{colors.bo}WARNING: {msg}{colors.nc}')

def final_summary(summary_dict):
    success('\nAll JSON files updated successfully!')
    for name, lang_set in summary_dict.items():
        if lang_set:
            status = name.replace('_', ' ')
            status_color = colors.by if status == 'translated' else colors.bg if status == 'added' else colors.gry
            data(f'Languages {status}: {len(lang_set)}')
            print(f"{status_color}[ {', '.join(lang_set)} ]{colors.nc}")

def trunc(msg, end='\n'):
    truncated_lines = [
        line if len(line) < terminal_width else line[:terminal_width -4] + '...' for line in msg.splitlines()]
    print('\n'.join(truncated_lines), end=end)
