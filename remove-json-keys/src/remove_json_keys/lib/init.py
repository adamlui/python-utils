from pathlib import Path

from . import data, language, log, settings, url

data_path = Path(__file__).parent.parent / 'assets/data'

def cli():
    cli = data.sns.from_dict(data.json.read(data_path / 'package_data.json'))
    cli.msgs = language.get_msgs()
    settings.load(cli)
    return cli

def config_file(cli): # for --init
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

def json_path(cli):
    for path in Path.cwd().rglob(cli.config.json_dir):
        if path.is_dir():
            cli.json_path = Path(path)
            return
    cli.json_path = None
