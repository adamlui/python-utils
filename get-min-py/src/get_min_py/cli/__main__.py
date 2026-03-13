import sys

from ..api import get_min_py
from .lib import init, log, settings

def main():
    if len(sys.argv) == 1 : sys.argv.append('--help')
    cli = init.cli()

    # Process early-exit args (e.g. --help, --version)
    for ctrl_name, ctrl in vars(settings.controls).items():
        if getattr(ctrl, 'exit', False) and getattr(cli.config, ctrl_name, False):
            if hasattr(ctrl, 'handler') : ctrl.handler(cli)
            sys.exit(0)

    # Process pkgs
    pkgs = []
    for arg in sys.argv[1:]:
        if arg.startswith('-') : continue
        pkgs.extend([pkg.strip() for pkg in arg.split(',') if pkg.strip()])
    if pkgs:
        results = get_min_py(pkgs)
        results = [results] if not isinstance(results, list) else results
        for pkg, version in zip(pkgs, results):
            if version:
                log.info(f'{log.colors.bw}{pkg}:{log.colors.nc} Python {version}')
            else:
                log.dim(f'{pkg}: {cli.msgs.log_NO_REQ_FOUND}', no_newline=True)
        log.line_break()

if __name__ == '__main__' : main()
