import argparse, re, sys
from types import SimpleNamespace as sn

from . import data, init, log, string, url

controls = sn(
    json_dir=sn(
        args=['-d', '--json-dir', '--json-folder'], type=str, default_val='_locales'),
    keys=sn(
        args=['-k', '--keys', '--remove-keys', '--delete-keys'], type=str, parser='csv'),
    config=sn(
        args=['--config'], type=str),
    init=sn(
        args=['-i', '--init'],
        action='store_true', subcmd='true', exit=True, handler=lambda cli: init.config_file(cli)
    ),
    force=sn(
        args=['-f', '--force', '--overwrite'], action='store_true'),
    no_wizard=sn(
        args=['-n', '--no-wizard', '--skip-wizard'], action='store_true', default=None),
    help=sn(
        args=['-h', '--help'], action='help'),
    version=sn(
        args=['-v', '--version'], action='store_true', exit=True, handler=lambda cli: log.version(cli)),
    docs=sn(
        args=['--docs'], action='store_true', exit=True, handler=lambda cli: url.open(cli.urls.docs)),
    debug=sn(
        args=['-V', '--debug'], nargs='?', const=True, metavar='TARGET_KEY'),
    legacy_no_wizard=sn(
        args=['-W'], action='store_true', default=None)
)

def get_canonical_key(key: str) -> str | None:
    if key.startswith('-'): # convert CLI arg to full key name
        for ctrl_key, ctrl in vars(controls).items():
            if key in getattr(ctrl, 'args', []):
                key = ctrl_key
                break
    legacy_key = key if key.startswith('legacy_') else f'legacy_{key}'
    legacy_ctrl = getattr(controls, legacy_key, None)
    stripped_key = string.removeprefix(key, 'legacy_')
    return legacy_ctrl.replaced_by if legacy_ctrl and hasattr(legacy_ctrl, 'replaced_by') \
      else stripped_key if hasattr(controls, stripped_key) \
      else None

def is_neg_key(key: str) -> bool : 
    return bool(re.match(r'^(?:no|disable|exclude)_', string.removeprefix(key, 'legacy_')))

def load(cli):
    cli.config = sn()

    # Assign help tips from cli.msgs
    for ctrl_key, ctrl in vars(controls).items():
        if ctrl_key.startswith('legacy_') or ctrl_key.endswith('entropy') : continue
        if not hasattr(ctrl, 'help') : ctrl.help = getattr(cli.msgs, f'help_{ctrl_key.upper()}')

    # Load from config file
    init.config_filepath(cli)
    if getattr(cli, 'config_filepath', None):
        config_data = data.json.read(cli.config_filepath)
        for config_key in config_data:
            if not get_canonical_key(config_key):
                log.cmd_docs_url_exit(cli,
                    f'{cli.msgs.err_INVALID_KEY} {config_key!r} {cli.msgs.err_FOUND_IN}'
                    f'\n{log.colors.gry}{cli.config_filepath}',
                    cmd='init')
        for config_key, config_val in config_data.items():            
            canonical_key = get_canonical_key(config_key)
            if canonical_key and config_key != canonical_key: # re-map config_key -> canonical_key
                log.warn_legacy_option(cli, config_key, source='config')
                if is_neg_key(config_key) != is_neg_key(canonical_key):
                    config_val = not config_val # flip bool val of opposite keys first
                config_key = canonical_key
            setattr(cli.config, config_key, config_val)
        log.debug(f'Config file loaded! {log.colors.dg}{len(config_data)} keys processed', cli)
    else:
        log.debug('No config file found.')

    # Parse CLI args (overriding config file loads)
    argp = argparse.ArgumentParser(description=cli.description, add_help=False)
    valid_argparse_kwargs = {
        'action', 'choices', 'const', 'default', 'dest', 'help', 'metavar', 'nargs', 'required', 'type', 'version'}
    for ctrl_key, ctrl in vars(controls).items(): # add args to argp
        kwargs = ctrl.__dict__.copy()
        args = kwargs.pop('args')
        argparse_kwargs = { key:val for key,val in kwargs.items() if key in valid_argparse_kwargs }        
        if ctrl_key.startswith('legacy_'): # copy canonical attrs first
            canonical_key = get_canonical_key(ctrl_key)
            if canonical_key: # adjust argparse_kwargs
                canonical_ctrl = getattr(controls, canonical_key)
                argparse_kwargs.update({
                    key:val for key,val in canonical_ctrl.__dict__.items() if key in valid_argparse_kwargs })
                argparse_kwargs['dest'] = canonical_key
                if is_neg_key(ctrl_key) != is_neg_key(canonical_key):
                    argparse_kwargs['action'] = 'store_false' if argparse_kwargs['action'] == 'store_true' \
                                           else 'store_true'
                for arg in args:
                    if arg in sys.argv:
                        log.warn_legacy_option(cli, arg, source='cli')
                        break
        argp.add_argument(*args, **argparse_kwargs)
    parsed_args, unknown_args = argp.parse_known_args()
    exempt_flags = [] # exempt valid dash-less args from validation
    exempt_flags.extend(arg.lstrip('-') for ctrl_key, ctrl in vars(controls).items()
                        if getattr(ctrl, 'subcmd', False)
                        for arg in ctrl.args if len(arg) > 2) # skip short flags
    if unknown_args and not all(any(arg == exempt for exempt in exempt_flags) for arg in unknown_args):
        log.cmd_docs_url_exit(cli, f"{cli.msgs.err_UNRECOGNIZED_ARGS}: {' '.join(unknown_args)}", cmd='help')
    for ctrl_key, ctrl in vars(controls).items(): # process subcmds
        if getattr(ctrl, 'subcmd', False) and next(arg for arg in ctrl.args if arg.startswith('--'))[2:] in sys.argv:
            setattr(parsed_args, ctrl_key, True)
    applied_args = []
    for arg in sys.argv[1:]:
        if not arg.startswith('-') : continue
        base_arg = arg.split('=')[0]
        for ctrl_key, ctrl in vars(controls).items():
            if base_arg in getattr(ctrl, 'args', []):
                dest = get_canonical_key(ctrl_key) or ctrl_key if ctrl_key.startswith('legacy_') else ctrl_key
                parsed_val = getattr(parsed_args, dest, None)
                if parsed_val is not None:
                    setattr(cli.config, dest, parsed_val)
                    applied_args.append(arg)
                break
    log.debug(f'Args parsed! {log.colors.bg}{len(applied_args)} args applied {applied_args}', cli)

    # Apply parsers/default_vals
    for ctrl_key, ctrl in vars(controls).items():
        if not hasattr(cli.config, ctrl_key):
            setattr(cli.config, ctrl_key, ctrl.default_val if hasattr(ctrl, 'default_val') else None)
        config_val = getattr(cli.config, ctrl_key)
        if getattr(ctrl, 'parser', '') == 'csv' and config_val is not None:
            setattr(cli.config, ctrl_key, data.csv.parse(config_val))
    log.debug('All cli.config vals set!', cli)
