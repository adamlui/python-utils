import argparse
from os import path
from types import SimpleNamespace as sn
from . import data

controls = sn(
    locales_dir=sn(
        args=['-d', '--locales-dir', '--locales-folder', '--json-dir', '--json-folder'],
        type=str, default_val='_locales', help='Name of the folder containing locale files (default: "_locales")'
    ),
    target_langs=sn(
        args=['-t', '--target-langs', '--target-lang', '--include-langs', '--include-lang'],
        type=str, parser='csv', help='Languages to translate to (e.g. "en,es,fr") (default: all supported locales)'
    ),
    keys=sn(
        args=['-k', '--keys', '--key', '--include-keys', '--include-key', '--translate-keys', '--translate-key'],
        type=str, parser='csv', help='Keys to translate (e.g. "appDesc,err_notFound")'
    ),
    exclude_langs=sn(
        args=['--exclude-langs', '--exclude-lang', '--ignore-langs', '--ignore-lang'],
        type=str, parser='csv', help='Languages to exclude (e.g. "en,es")'
    ),
    exclude_keys=sn(
        args=['--exclude-keys', '--exclude-key', '--ignore-keys', '--ignore-key'],
        type=str, parser='csv', help='Keys to ignore (e.g. "appName,author")'
    ),
    init=sn(
        args=['-i', '--init'],
        action='store_true', help='Create .translate-msgs.config.jsojson5nc file to store default options'
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
    cli.project_root = path.join(path.dirname(caller_file),
        f"../../{ '' if 'src' in path.dirname(caller_file) else '../../' }")
    possible_config_filenames = [
        f'{prefix}{name}.config.{ext}'
            for prefix in ['.', ''] for name in [cli.short_name, cli.name] for ext in ['json5', 'json', 'jsonc']
    ]
    for filename in possible_config_filenames:
        cli.config_filepath = path.join(cli.project_root, filename)
        if path.exists(cli.config_filepath):
            cli.config = data.sns.from_dict(data.json.read(cli.config_filepath))
            cli.config_filename = filename
            break

    # Parse CLI args
    argp = argparse.ArgumentParser(
        description="Translate en/messages.json (chrome.i18n format) to 100+ locales", add_help=False)
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

    if cli.config.exclude_langs: # trim cli.config.target_langs
       cli.config.target_langs = [lang for lang in cli.config.target_langs if lang not in cli.config.exclude_langs]
