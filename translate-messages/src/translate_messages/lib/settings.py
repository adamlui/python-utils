import argparse, os
from types import SimpleNamespace as sns
from . import data

controls = sns(
    locales_dir=sns(
        args=['-d', '--locales-dir', '--locales-folder', '--json-dir', '--json-folder'],
        type=str, default_val='_locales', help='Name of the folder containing locale files (default: "_locales")'
    ),
    target_langs=sns(
        args=['-t', '--target-langs', '--target-lang', '--include-langs', '--include-lang'],
        type=str, parser='csv', help='Languages to include (e.g. "en,es,fr") (default: all supported locales)'
    ),
    keys=sns(
        args=['-k', '--keys', '--key', '--include-keys', '--include-key', '--translate-keys', '--translate-key'],
        type=str, parser='csv', help='Keys to translate (e.g. "appDesc,err_notFound")'
    ),
    exclude_langs=sns(
        args=['--exclude-langs', '--exclude-lang', '--ignore-langs', '--ignore-lang'],
        type=str, parser='csv', help='Languages to exclude (e.g. "en,es")'
    ),
    exclude_keys=sns(
        args=['--exclude-keys', '--exclude-key', '--ignore-keys', '--ignore-key'],
        type=str, parser='csv', help='Keys to ignore (e.g. "appName,author")'
    ),
    init=sns(
        args=['-i', '--init'],
        action='store_true', help='Create .translate-msgs.config.json file to store defaults'
    ),
    force=sns(
        args=['-f', '--force', '--overwrite'],
        action='store_true', help='Force overwrite existing config file when using --init'
    ),
    no_wizard=sns(
        args=['-W', '--no-wizard', '--skip-wizard'],
        action='store_true', default=None, help='Skip interactive prompts during start-up'
    ),
    help=sns(
        args=['-h', '--help'],
        action='help', help='Show help screen'
    )
)

def load(cli, caller_file):

    # Load from config file
    cli.config = sns()
    cli.project_root = os.path.join(os.path.dirname(caller_file),
        f"{ '' if 'src' in os.path.dirname(caller_file) else '../../' }../../")
    possile_config_filenames = [
         '.translate-msgs.config.json', 'translate-msgs.config.json',
        f'.{cli.name}.config.json', f'{cli.name}.config.json'
    ]
    for filename in possile_config_filenames:
        cli.config_path = os.path.join(cli.project_root, filename)
        if os.path.exists(cli.config_path):
            cli.config = data.sns.from_dict(data.json.read(cli.config_path))
            cli.config_filename = filename
            break

    # Parse CLI args
    argp = argparse.ArgumentParser(
        description="Translate en/messages.json (chrome.i18n format) to other locales",
        add_help=False # disable default --help arg to re-create last
    )
    for attr_name in vars(controls):
        kwargs = getattr(controls, attr_name).__dict__.copy()
        args = kwargs.pop('args')  # separate positional flags
        for forbidden in ('default_val', 'parser'): # remove custom attrs
            kwargs.pop(forbidden, None)
        argp.add_argument(*args, **kwargs)
    cli.config.__dict__.update({ key:val for key,val in vars(argp.parse_args()).items() if val is not None})

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

    if cli.config.exclude_langs:
       cli.config.target_langs = [lang for lang in cli.config.target_langs if lang not in cli.config.exclude_langs]
