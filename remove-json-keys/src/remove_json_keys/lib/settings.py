import argparse, sys
from types import SimpleNamespace as sn

from . import data, init, log, url

controls = sn(
    json_dir=sn(
        args=['-d', '--json-dir', '--json-folder'], type=str, default_val='_locales'),
    keys=sn(
        args=['-k', '--keys', '--remove-keys', '--delete-keys'], type=str, parser='csv'),
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
        valid_argparse_params = {
            'action', 'choices', 'const', 'default', 'dest', 'help', 'metavar', 'nargs', 'required', 'type', 'version' }
        argparse_kwargs = { key:val for key,val in kwargs.items() if key in valid_argparse_params}
        argp.add_argument(*args, **argparse_kwargs)
    parsed_args, unknown = argp.parse_known_args()
    subcmd_flags = [] # exempt dashless args from validation
    for ctrl in vars(controls).values():
        if getattr(ctrl, 'subcmd', False):
            for arg in ctrl.args : subcmd_flags.append(arg)
    if unknown and not all(f'--{arg}' in subcmd_flags for arg in unknown):
        log.error(f"{cli.msgs.err_UNRECOGNIZED_ARGS}: {' '.join(unknown)}")
        log.help_cmd_docs_url_exit(cli)
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
