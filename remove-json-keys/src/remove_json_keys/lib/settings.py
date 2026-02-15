import argparse
from types import SimpleNamespace as sn
from . import data

controls = sn(
    json_dir=sn(
        args=['-d', '--json-dir', '--json-folder'],
        type=str, default_val='_locales', help='Name of the folder containing JSON files (default: "_locales")'
    ),
    keys=sn(
        args=['-k', '--keys', '--key', '--remove-keys', '--remove-key', '--delete-keys', '--delete-key'],
        type=str, parser='csv', help='Keys to remove (e.g. "appName,author")'
    ),
    no_wizard=sn(
        args=['-W', '--no-wizard', '--skip-wizard'],
        action='store_true', default=None, help='Skip interactive prompts during start-up'
    ),
    help=sn(
        args=['-h', '--help'],
        action='help', help='Show help screen'
    )
)

def load(cli):

    # Parse CLI args
    argp = argparse.ArgumentParser(
        description="Simply remove JSON keys via CLI command",
        add_help=False # disable default --help to re-create last
    )
    cli.config=sn()
    for attr_name in vars(controls):
        kwargs = getattr(controls, attr_name).__dict__.copy()
        args = kwargs.pop('args')  # separate positional flags
        for forbidden in ('default_val', 'parser'): # remove custom attrs
            kwargs.pop(forbidden, None)
        argp.add_argument(*args, **kwargs)
    cli.config.__dict__.update({ key:val for key,val in vars(argp.parse_args()).items() if val is not None })

    # Init cli.config vals
    for name, ctrl in vars(controls).items():
        val = getattr(cli.config, name, None)
        if getattr(ctrl, 'parser', None) == 'csv':
            val = data.csv.parse(val)
        if getattr(ctrl, 'action', None) == 'store_true':
            val = val if val is not None else False
        if val is None and hasattr(ctrl, 'default_val'):
            val = ctrl.default_val
        setattr(cli.config, name, val)
