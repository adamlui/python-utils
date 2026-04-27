import sys

from ..api import find_project_root
from .lib import init, settings

def main():
    cli = init.cli()

    # Process early-exit args (e.g. --help, --version)
    for ctrl_name, ctrl in vars(settings.controls).items():
        if getattr(ctrl, 'exit', False) and getattr(cli.config, ctrl_name, False):
            if hasattr(ctrl, 'handler') : ctrl.handler(cli)
            sys.exit(0)

    print(find_project_root(
        path=getattr(cli.config, 'path', None),
        max_depth=getattr(cli.config, 'max_depth', 9),
        markers=getattr(cli.config, 'markers', None)
     ))

if __name__ == '__main__' : main()
