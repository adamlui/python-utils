from pathlib import Path
import sys

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
            log.warn(f'Config already exists at {config_path}! Skipping init.')
            log.tip('Pass --force to overwrite.')
            return
    cli.config_filename = f'.{cli.short_name}.config.json5'
    cli.config_filepath = str(Path(cli.project_root) / cli.config_filename)
    if not getattr(cli, 'default_file_config', None):
        cli.default_file_config = data.url.get(f'{cli.urls.jsdelivr}/{cli.name}/{cli.config_filename}')
    data.file.write(cli.config_filepath, cli.default_file_config)
    log.success(f'Default config created at {cli.config_filepath}')

def locales_dir(cli):
    for path in Path.cwd().rglob(cli.config.locales_dir):
        if path.is_dir():
            cli.config.locales_dir = str(path)
            return
    cli.config.locales_dir = None

def src_msgs(cli):
    cli.msgs_filename = 'messages.json'
    cli.locales_path = Path(cli.config.locales_dir)
    cli.en_path = cli.locales_path / 'en' / cli.msgs_filename
    if not cli.en_path.exists():
        log.error(f'English locale not found at {cli.en_path}.')
        log.tip(f'Make sure {cli.en_path} exists!')
        sys.exit(1)
    try:
        cli.en_msgs = data.json.read(cli.en_path)
    except Exception as err:
        log.error(f'Failed to parse {cli.en_path}: {err}')
        log.tip('Make sure it contains valid JSON')
        sys.exit(1)

def target_langs(cli):
    cli.config.target_langs = list(set(cli.config.target_langs)) # remove dupes
    if not cli.config.target_langs:
        cli.config.target_langs = cli.supported_locales
        for lang_path in cli.locales_path.rglob(f'*/{cli.msgs_filename}'): # merge discovered locales
            discovered_lang = lang_path.parent.name.replace('_', '-')
            if discovered_lang not in cli.config.target_langs:
                cli.config.target_langs.append(discovered_lang)
    cli.config.target_langs.sort()
    if cli.config.exclude_langs:
       cli.config.target_langs = [lang for lang in cli.config.target_langs if lang not in cli.config.exclude_langs]
