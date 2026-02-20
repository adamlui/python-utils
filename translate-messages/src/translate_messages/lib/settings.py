import argparse, sys
from types import SimpleNamespace as sn

from . import data, init, log, url

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
    config=sn(
        args=['--config'], type=str),
    init=sn(
        args=['-i', '--init'],
        action='store_true', subcmd='true', exit=True, handler=lambda cli: init.config_file(cli)
    ),
    force=sn(
        args=['-f', '--force', '--overwrite'], action='store_true'),
    no_wizard=sn(
        args=['-n', '-W', '--no-wizard', '--skip-wizard'], action='store_true', default=None),
    help=sn(
        args=['-h', '--help'], action='help'),
    version=sn(
        args=['-v', '--version'], action='store_true', exit=True, handler=lambda cli: log.version(cli)  ),
    docs=sn(
        args=['--docs'], action='store_true', exit=True, handler=lambda cli: url.open(cli.urls.docs)),
    debug=sn(
        args=['--debug'], nargs='?', const=True, metavar='TARGET_KEY' )
)

def load(cli):
    cli.config = sn()

    # Assign help tips from cli.msgs
    for ctrl_key, ctrl in vars(controls).items():
        if not hasattr(ctrl, 'help') : ctrl.help = getattr(cli.msgs, f'help_{ctrl_key.upper()}')

    # Parse CLI args
    argp = argparse.ArgumentParser(description=cli.description, add_help=False)
    for ctrl_key in vars(controls): # add args to argp
        kwargs = getattr(controls, ctrl_key).__dict__.copy()
        args = kwargs.pop('args')
        valid_argparse_kwargs = {
            'action', 'choices', 'const', 'default', 'dest', 'help', 'metavar', 'nargs', 'required', 'type', 'version' }
        argparse_kwargs = { key:val for key,val in kwargs.items() if key in valid_argparse_kwargs}
        argp.add_argument(*args, **argparse_kwargs)
    parsed_args, unknown_args = argp.parse_known_args()
    subcmd_flags = [] # exempt dashless args from validation
    for ctrl in vars(controls).values():
        if getattr(ctrl, 'subcmd', False):
            for arg in ctrl.args : subcmd_flags.append(arg)
    if unknown_args and not all(f'--{arg}' in subcmd_flags for arg in unknown_args):
        log.help_cmd_docs_url_exit(cli, f"{cli.msgs.err_UNRECOGNIZED_ARGS}: {' '.join(unknown_args)}")
    for ctrl_key, ctrl in vars(controls).items(): # process subcmds
        if getattr(ctrl, 'subcmd', False) and next(arg for arg in ctrl.args if arg.startswith('--'))[2:] in sys.argv:
            setattr(parsed_args, ctrl_key, True)
    for key, val in vars(parsed_args).items(): # apply parsed_args to cli.config
        setattr(cli.config, key, val)
    log.debug('Args parsed!', cli)

    # Load from config file (w/o overriding args)
    init.config_filepath(cli)
    if getattr(cli, 'config_filepath', None):
        for key, val in data.json.read(cli.config_filepath).items():
            if not getattr(cli.config, key, None):
                if hasattr(cli.config, key):
                    setattr(cli.config, key, val)
                else:
                    log.init_cmd_docs_url_exit(cli,
                        f"{cli.msgs.err_INVALID_KEY} '{key}' {cli.msgs.err_FOUND_IN}"
                        f'\n{log.colors.gry}{cli.config_filepath}'
                    )
        log.debug('Config file loaded!', cli)
    else:
        log.debug('No config file found.')

    # Apply parsers/default_vals
    for ctrl_key, ctrl in vars(controls).items():
        val = getattr(cli.config, ctrl_key, '')
        if not val and hasattr(ctrl, 'default_val'):
            setattr(cli.config, ctrl_key, ctrl.default_val)
        if getattr(ctrl, 'parser', '') == 'csv':
            setattr(cli.config, ctrl_key, data.csv.parse(val))

    log.debug('All cli.config vals set!', cli)
