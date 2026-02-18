from pathlib import Path

from . import data, language, log, settings

def cli(caller_file):
    cli = data.json.read(Path(__file__).parent.parent / 'assets/data/package_data.json')
    cli.msgs = language.get_msgs()
    settings.load(cli, caller_file)
    return cli

def config_file(cli):
    config_path = Path(cli.config_filepath)
    if config_path.exists():
        if cli.config.force:
            log.info(f'{cli.msgs.log_OVERWRITING_CONFIG_AT} {config_path}...')
        else:
            log.warn(f'{cli.msgs.warn_CONFIG_EXISTS_AT} {config_path}. {cli.msgs.log_SKIPPING} init.')
            log.tip(f'{cli.msgs.tip_PASS_FORCE_TO_OVERWRITE}.')
            return
    cli.config_filename = f'.{cli.short_name}.config.json5'
    cli.config_filepath = str(Path(cli.project_root) / cli.config_filename)
    if not getattr(cli, 'default_file_config', None):
        cli.default_file_config = data.url.get(f'{cli.urls.jsdelivr}/{cli.name}/{cli.config_filename}')
    data.file.write(cli.config_filepath, cli.default_file_config)
    log.success(f'{cli.msgs.log_DEFAULT_CONFIG_CREATED_AT} {cli.config_filepath}')

def json_dir(cli):
    for path in Path.cwd().rglob(cli.config.json_dir):
        if path.is_dir():
            cli.config.json_dir = str(path)
            return
    cli.config.json_dir = None
