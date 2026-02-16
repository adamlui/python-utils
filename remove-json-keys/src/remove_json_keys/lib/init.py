import os, urllib.request, urllib.error
from . import data, log, settings

def cli(caller_file):
    cli = data.sns.from_dict(data.json.read(os.path.join(os.path.dirname(__file__), '../package_data.json')))
    settings.load(cli, caller_file)
    return cli

def config_file(cli):
    if os.path.exists(cli.config_filepath):
        if cli.config.force:
            log.info(f'Overwriting existing config at {cli.config_filepath}...')
        else:
            log.warn(f'Config already exists at {cli.config_filepath}. Skipping --init.')
            log.tip('Pass --force to overwrite.')
            return
    cli.config_filename = f'.{cli.name}.config.json5'
    cli.config_filepath = os.path.join(cli.project_root, cli.config_filename)
    if not getattr(cli, 'default_file_config', None):
        try:
            jsd_url = f'{cli.urls.jsdelivr}/{cli.name}/{cli.config_filename}'
            with urllib.request.urlopen(jsd_url, timeout=5) as resp:
                cli.default_file_config = resp.read().decode('utf-8')
        except (urllib.error.URLError, urllib.error.HTTPError, ValueError) as err:
            raise RuntimeError(f'Failed to fetch default config from {jsd_url}: {err}')
    data.file.write(cli.config_filepath, cli.default_file_config)
    log.success(f'Default config created at {cli.config_filepath}')

def json_dir(target_dir):
    for root, dirs, _ in os.walk(os.getcwd()):
        if target_dir in dirs:
            return os.path.join(root, target_dir)
    return None
