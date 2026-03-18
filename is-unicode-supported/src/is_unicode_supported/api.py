import os, sys

import blessed

def is_unicode_supported() -> bool:
    if hasattr(is_unicode_supported, '_cached'):
        return is_unicode_supported._cached

    if sys.platform == 'win32' and not os.environ.get('WT_SESSION'):
        is_unicode_supported._cached = False
        return False # legacy Win consoles don't suport wide chars

    # Measure rendered width of wide CJK char
    terminal = blessed.Terminal()
    with terminal.cbreak(), terminal.hidden_cursor():
        r,g,b = terminal.get_bgcolor()
        if (r,g,b) == (-1,-1,-1) : r = g = b = 0 # get bg failed, init to black
        sys.stdout.write(terminal.color_rgb(r,g,b)) # make text invisible
        _, x1 = terminal.get_location()
        sys.stdout.write('𠀀')
        sys.stdout.flush()
        _, x2 = terminal.get_location()
        sys.stdout.write('\b' * (x2 - x1) + ' ' * (x2 - x1) + '\b' * (x2 - x1))
        sys.stdout.flush()
        sys.stdout.write(terminal.normal) # restore text colors
        result = x2 - x1 > 1 # terminal rendered wide char as 2 col
        is_unicode_supported._cached = result
        return result
