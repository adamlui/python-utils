from pathlib import Path
import sys

from . import data, language, log, settings, url

data_path = Path(__file__).parent.parent / 'assets/data'

def cli():
    cli = data.sns.from_dict(data.json.read(data_path / 'package_data.json'))
    cli.msgs = language.get_msgs()
    settings.load(cli)
    return cli

def config_file(cli):
    target_path = Path.cwd() / f'.{cli.short_name}.config.json5'
    project_markers = data.json.read(data_path / 'project_markers.json')
    in_project_root = None
    if not any((Path.cwd() / marker).exists() for marker in project_markers):
        log.warn(f'{cli.msgs.warn_NO_PROJECT_ROOT_FOUND_IN} {Path.cwd()}')
        user_resp = input(f'{cli.msgs.prompt_INIT_CONFIG_HERE_ANYWAY}? (y/N): ').strip().lower()
        if not user_resp.startswith('y') : return
        else : in_project_root = True # for move tip

    # Handle existing file
    if target_path.exists():
        if cli.config.force:
            log.info(f'{cli.msgs.log_OVERWRITING_CONFIG_AT} {target_path}...\n')
        else:
            log.warn(f'{cli.msgs.warn_CONFIG_EXISTS_AT} {target_path}. {cli.msgs.log_SKIPPING} init...')
            log.tip(f'{cli.msgs.tip_PASS_FORCE_TO_OVERWRITE}.')
            return

    # Fetch/write from jsDelivr
    if not getattr(cli, 'default_file_config', ''):
        jsd_url = f'{data.jsdelivr.create_pkg_ver_url(cli)}/{target_path.name}'
        log.debug(f'{log.colors.bw}{jsd_url}')
        cli.default_file_config = url.get(jsd_url)
    data.file.write(str(target_path), cli.default_file_config)
    log.success(f'{cli.msgs.log_DEFAULT_CONFIG_CREATED_AT} {target_path}')
    if in_project_root : log.tip(f'{cli.msgs.tip_MOVE_CONFIG_TO_ROOT}.')

def config_filepath(cli): # for settings.load()

    # Check --config <path>
    if getattr(cli.config, 'config', ''):
        cli.config_filepath = Path(cli.config.config).resolve()
        if cli.config_filepath.exists():
            log.debug(f'Config file found: {cli.config_filepath}')
            return
        else:
            log.warn(f'{cli.msgs.warn_SPECIFIED_CONFIG} {cli.config_filepath} {cli.msgs.warn_NOT_FOUND}')

    # Search upwards
    possible_config_filenames = [
        f'{prefix}{name}.config.json{suffix}'
            for prefix in ['.', ''] for name in [cli.short_name, cli.name] for suffix in ['5', '', 'c']
    ]
    current_dir = Path.cwd().resolve()
    for parent in [current_dir, *current_dir.parents]:
        for filename in possible_config_filenames:
            possible_config_filepath = parent / filename
            if possible_config_filepath.exists():
                cli.config_filepath = possible_config_filepath
                return

    cli.config_filepath = None

def locales_path(cli):
    for path in Path.cwd().rglob(cli.config.locales_dir):
        if path.is_dir():
            cli.locales_path = Path(path)
            return
    cli.locales_path = None

def src_msgs(cli):
    cli.msgs_filename = 'messages.json'
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
