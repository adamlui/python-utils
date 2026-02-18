import argparse
from pathlib import Path
from types import SimpleNamespace as sn

from . import data

controls = sn(
    locales_dir=sn(
        args=['-d', '--locales-dir', '--locales-folder', '--json-dir', '--json-folder'],
        type=str, default_val='_locales', help='Name of the folder containing locale files (default: "_locales")'
    ),
    target_langs=sn(
        args=['-t', '--target-langs', '--include-langs'],
        type=str, parser='csv', help='Languages to translate to (e.g. "en,es,fr") (default: all 100+ supported locales)'
    ),
    keys=sn(
        args=['-k', '--keys', '--include-keys', '--translate-keys'],
        type=str, parser='csv', help='Keys to translate (e.g. "app_DESC,err_NOT_FOUND") (default: all found src keys missing in target files)'
    ),
    exclude_langs=sn(
        args=['--exclude-langs', '--ignore-langs'],
        type=str, parser='csv', help='Languages to exclude (e.g. "en,es")'
    ),
    exclude_keys=sn(
        args=['--exclude-keys', '--ignore-keys'],
        type=str, parser='csv', help='Keys to ignore (e.g. "app_NAME,author")'
    ),
    init=sn(
        args=['-i', '--init'],
        action='store_true', help='Create .translate-msgs.config.json5 file to store default options'
    ),
    force=sn(
        args=['-f', '--force', '--overwrite'],
        action='store_true', help='Force overwrite existing config file when using --init'
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

def load(cli, caller_file):

    # Load from config file
    cli.config = sn()
    caller_path = Path(caller_file)
    cli.project_root = str(caller_path.parent.parent.parent if 'src' in str(caller_path)
                      else caller_path.parent.parent)
    possible_config_filenames = [
        f'{prefix}{name}.config.json{suffix}'
            for prefix in ['.', ''] for name in [cli.short_name, cli.name] for suffix in ['5', '', 'c']
    ]
    for filename in possible_config_filenames:
        config_path = Path(cli.project_root) / filename
        if config_path.exists():
            cli.config_filepath = str(config_path)
            cli.config = data.sns.from_dict(data.json.read(cli.config_filepath))
            cli.config_filename = filename
            break

    # Parse CLI args
    argp = argparse.ArgumentParser(description=cli.description, add_help=False)
    for attr_name in vars(controls):
        kwargs = getattr(controls, attr_name).__dict__.copy()
        args = kwargs.pop('args') # separate positional flags
        for custom_attr in ('default_val', 'parser'): # remove custom attrs for argp
            kwargs.pop(custom_attr, None)
        argp.add_argument(*args, **kwargs)
    for key, val in vars(argp.parse_args()).items():
        if getattr(cli.config, key, None) is None:
            setattr(cli.config, key, val)

    # Init all cli.config vals
    for name, ctrl in vars(controls).items():
        val = getattr(cli.config, name, None)
        if getattr(ctrl, 'parser', None) == 'csv':
            val = data.csv.parse(val)
        if val is None and hasattr(ctrl, 'default_val'):
            val = ctrl.default_val
        setattr(cli.config, name, val)
