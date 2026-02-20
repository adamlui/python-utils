from pathlib import Path
import sys

from . import data, language, log, settings

data_path = Path(__file__).parent.parent / 'assets/data'

def cli():
    cli = data.sns.from_dict(data.json.read(data_path / 'package_data.json'))
    cli.msgs = language.get_msgs()
    settings.load(cli)
    return cli

def config_file(cli):
    target_path = Path.cwd() / f'.{cli.short_name}.config.json5'
    project_markers = data.json.read(data_path / 'project_markers.json')
    if not any((Path.cwd() / marker).exists() for marker in project_markers):
        log.warn(f'{cli.msgs.warn_NO_PROJECT_ROOT_FOUND_IN} {Path.cwd()}')
        user_resp = input(f'{cli.msgs.prompt_INIT_CONFIG_HERE_ANYWAY}? (y/N): ').strip().lower()
        if not user_resp.startswith('y') : return
        else : not_in_root = True # for move tip

    # Handle existing file
    if target_path.exists():
        if cli.config.force:
            log.info(f'{cli.msgs.log_OVERWRITING_CONFIG_AT} {target_path}...')
        else:
            log.warn(f'{cli.msgs.warn_CONFIG_EXISTS_AT} {target_path}. {cli.msgs.log_SKIPPING} init...')
            log.tip(f'{cli.msgs.tip_PASS_FORCE_TO_OVERWRITE}.')
            return

    # Fetch/write from jsDelivr
    if not getattr(cli, 'default_file_config', ''):
        cli.default_file_config = data.url.get(f'{cli.urls.jsdelivr}/{cli.name}/{target_path.name}')
    data.file.write(str(target_path), cli.default_file_config)
    log.success(f'{cli.msgs.log_DEFAULT_CONFIG_CREATED_AT} {target_path}')
    if not_in_root : log.tip(f'{cli.msgs.tip_MOVE_CONFIG_TO_ROOT}.')

def config_filepath(cli): # for settings.load()

    # Check --config <path>
    for idx, arg in enumerate(sys.argv):
        if arg == '--config' and idx +1 < len(sys.argv):
            cli.config_filepath = Path(sys.argv[idx + 1]).resolve()
            if cli.config_filepath.exists(): return
            else : log.warn(f'{cli.msgs.warn_SPECIFIED_CONFIG} {cli.config_filepath} {cli.msgs.warn_NOT_FOUND.lower()}')

    # Search upwards
    possible_config_filenames = [
        f'{prefix}{name}.config.json{suffix}'
            for prefix in ['.', ''] for name in [cli.short_name, cli.name] for suffix in ['5', '', 'c']
    ]
    current_dir = Path.cwd().resolve()
    for parent in [current_dir, *current_dir.parents]:
        for filename in possible_config_filenames:
            possible_config_file = parent / filename
            if possible_config_file.exists():
                cli.config_filepath = possible_config_file
                return

def locales_dir(cli):
    for path in Path.cwd().rglob(cli.config.locales_dir):
        if path.is_dir():
            cli.config.locales_dir = str(path)
            return
    cli.config.locales_dir = ''

def src_msgs(cli):
    cli.msgs_filename = 'messages.json'
    cli.locales_path = Path(cli.config.locales_dir)
    cli.en_path = cli.locales_path / 'en' / cli.msgs_filename
    if not cli.en_path.exists():
        log.error(f'{cli.msgs.err_EN_LOC_NOT_FOUND_AT} {cli.en_path}.')
        log.tip(f'{cli.msgs.tip_MAKE_SURE} {cli.en_path} {cli.msgs.tip_EXISTS}!')
        sys.exit(1)
    try:
        cli.en_msgs = data.json.read(cli.en_path)
    except Exception as err:
        log.error(f'{cli.msgs.err_PARSE_FAILED} {cli.en_path}: {err}')
        log.tip(f'{cli.msgs.tip_MAKE_SURE} {cli.msgs.tip_IT_HAS_VALID_JSON}')
        sys.exit(1)

def target_langs(cli):
    cli.config.target_langs = list(set(cli.config.target_langs)) # remove dupes
    if not cli.config.target_langs: # init to stable ones
        cli.config.target_langs = cli.stable_locales
    if not cli.config.only_stable: # merge discovered locales
        for lang_path in cli.locales_path.rglob(f'*/{cli.msgs_filename}'):
            discovered_lang = lang_path.parent.name.replace('_', '-')
            if discovered_lang not in cli.config.target_langs:
                cli.config.target_langs.append(discovered_lang)
    cli.config.target_langs.sort()
    if cli.config.exclude_langs:
       cli.config.target_langs = [lang for lang in cli.config.target_langs if lang not in cli.config.exclude_langs]
    log.debug(f"cli.config.target_langs init'd!\n{log.colors.gry}{cli.config.target_langs}")
