from pathlib import Path
from . import data, log, settings

def cli(caller_file):
    cli = data.sns.from_dict(data.json.read(Path(__file__).parent.parent / 'assets/data/package_data.json'))
    settings.load(cli, caller_file)
    return cli

def config_file(cli):
    config_path = Path(cli.config_filepath)
    if config_path.exists():
        if cli.config.force:
            log.info(f'Overwriting existing config at {config_path}...')
        else:
            log.warn(f'Config already exists at {config_path}. Skipping --init.')
            log.tip('Pass --force to overwrite.')
            return
    cli.config_filename = f'.{cli.short_name}.config.json5'
    cli.config_filepath = str(Path(cli.project_root) / cli.config_filename)
    if not getattr(cli, 'default_file_config', None):
        cli.default_file_config = data.url.get(f'{cli.urls.jsdelivr}/{cli.name}/{cli.config_filename}')
    data.file.write(cli.config_filepath, cli.default_file_config)
    log.success(f'Default config created at {cli.config_filepath}')

def locales_dir(target_dir):
    for path in Path.cwd().rglob(target_dir):
        if path.is_dir() : return str(path)
    return None
