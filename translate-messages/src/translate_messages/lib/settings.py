import argparse, sys
from types import SimpleNamespace as sn

from . import data, init, log

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
    version=sn(
        args=['-v', '--version'], action='store_true'),
    docs=sn(
        args=['--docs'], action='store_true'),
    debug=sn(
        args=['--debug'], nargs='?', const=True, metavar='TARGET_KEY' )
)

def load(cli):

    # Assign help tips from cli.msgs
    for ctrl_key, ctrl in vars(controls).items():
        if not hasattr(ctrl, 'help') : ctrl.help = getattr(cli.msgs, f'help_{ctrl_key.upper()}')

    # Load from config file
    cli.config = sn()
    init.config_filepath(cli)
    if getattr(cli, 'config_filepath', None):
        cli.config = data.sns.from_dict(data.json.read(cli.config_filepath))
        log.debug('Config file loaded!', cli)
    else:
        log.debug('No config file found.')

    # Parse CLI args
    argp = argparse.ArgumentParser(description=cli.description, add_help=False)
    sys.argv = [arg.replace('_', '-') if arg.startswith('--') and '_' in arg else arg for arg in sys.argv]
    for attr_name in vars(controls): # add args to argp
        kwargs = getattr(controls, attr_name).__dict__.copy()
        args = kwargs.pop('args')
        for custom_attr in ('default_val', 'parser', 'subcmd'):
            kwargs.pop(custom_attr, None)
        argp.add_argument(*args, **kwargs)
    parsed_args, unknown = argp.parse_known_args()
    for attr_name, ctrl in vars(controls).items(): # process subcmds
        if getattr(ctrl, 'subcmd', False) and next(arg for arg in ctrl.args if arg.startswith('--'))[2:] in sys.argv:
            setattr(parsed_args, attr_name, True)
    for key, val in vars(parsed_args).items(): # apply parsed_args to cli.config
        if val : setattr(cli.config, key, val)
    log.debug('Args parsed!', cli)

    # Init all cli.config vals
    for name, ctrl in vars(controls).items():
        val = getattr(cli.config, name, '')
        if getattr(ctrl, 'parser', '') == 'csv':
            val = data.csv.parse(val)
        if not val and hasattr(ctrl, 'default_val'):
            val = ctrl.default_val
        setattr(cli.config, name, val)
    log.debug('All cli.config vals set!', cli)
