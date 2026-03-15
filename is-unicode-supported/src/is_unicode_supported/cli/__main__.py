import sys

from ..api import is_unicode_supported
from .lib import init, settings

def main():
    cli = init.cli()

    # Process early-exit args (e.g. --help, --version)
    for ctrl_name, ctrl in vars(settings.controls).items():
        if getattr(ctrl, 'exit', False) and getattr(cli.config, ctrl_name, False):
            if hasattr(ctrl, 'handler') : ctrl.handler(cli)
            sys.exit(0)

    print(is_unicode_supported())

if __name__ == '__main__' : main()
