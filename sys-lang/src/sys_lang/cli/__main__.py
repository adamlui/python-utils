import sys

from ..api import get_sys_lang
from .lib import init, settings

def main():
    cli = init.cli()

    # Process early-exit args (e.g. --help, --version)
    for ctrl_name, ctrl in vars(settings.controls).items():
        if getattr(ctrl, 'exit', False) and getattr(cli.config, ctrl_name, False):
            if hasattr(ctrl, 'handler') : ctrl.handler(cli)
            sys.exit(0)

    print(get_sys_lang(region=not cli.config.no_region))

if __name__ == '__main__' : main()
