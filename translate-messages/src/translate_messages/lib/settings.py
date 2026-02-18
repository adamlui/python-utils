import argparse, sys
from pathlib import Path
from types import SimpleNamespace as sn

from . import data, log

controls = sn(
    locales_dir=sn(
        args=['-d', '--locales-dir', '--locales-folder', '--json-dir', '--json-folder'],
        type=str, default_val='_locales'
    ),
    target_langs=sn(
        args=['-t', '--target-langs', '--include-langs'], type=str, parser='csv' ),
    keys=sn(
        args=['-k', '--keys', '--include-keys', '--translate-keys'], type=str, parser='csv'),
    exclude_langs=sn(
        args=['--exclude-langs', '--ignore-langs'], type=str, parser='csv'),
    exclude_keys=sn(
        args=['--exclude-keys', '--ignore-keys'], type=str, parser='csv'),
    only_stable=sn(
        args=['-s', '--only-stable', '--no-discovery'], action='store_true'),
    init=sn(
        args=['-i', '--init'], action='store_true', subcmd='true'),
    force=sn(
        args=['-f', '--force', '--overwrite'], action='store_true'),
    no_wizard=sn(
        args=['-n', '-W', '--no-wizard', '--skip-wizard'], action='store_true', default=None),
    help=sn(
        args=['-h', '--help'], action='help'),
    debug=sn(
        args=['--debug'], action='store_true')
)

def load(cli, caller_file):

    # Assign help tips from cli.msgs
    for ctrl_key, ctrl in vars(controls).items():
        if not hasattr(ctrl, 'help') : ctrl.help = getattr(cli.msgs, f'help_{ctrl_key.upper()}')

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
    log.debug(f'Config file loaded!\n{log.colors.gry}{cli.config}' if cli.config_filepath else 'No config file found.')

    # Parse CLI args
    argp = argparse.ArgumentParser(description=cli.description, add_help=False)
    for attr_name in vars(controls):
        kwargs = getattr(controls, attr_name).__dict__.copy()
        args = kwargs.pop('args') # separate positional flags
        for custom_attr in ('default_val', 'parser', 'subcmd'): # remove custom attrs from kwargs
            kwargs.pop(custom_attr, None)
        argp.add_argument(*args, **kwargs)
    parsed_args, unknown = argp.parse_known_args()
    for attr_name, ctrl in vars(controls).items(): # process subcmds
        if getattr(ctrl, 'subcmd', False) and next(arg for arg in ctrl.args if arg.startswith('--'))[2:] in sys.argv:
            setattr(parsed_args, attr_name, True)
    for key, val in vars(parsed_args).items(): # apply parsed_args to cli.config
        if not getattr(cli.config, key, ''):
            setattr(cli.config, key, val)
    log.debug(f'Args parsed!\n{log.colors.gry}{cli.config}')

    # Init all cli.config vals
    for name, ctrl in vars(controls).items():
        val = getattr(cli.config, name, None)
        if getattr(ctrl, 'parser', None) == 'csv':
            val = data.csv.parse(val)
        if val is None and hasattr(ctrl, 'default_val'):
            val = ctrl.default_val
        setattr(cli.config, name, val)
    log.debug(f'All cli.config vals set!\n{log.colors.gry}{cli.config}')
