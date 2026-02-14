import argparse, os, requests
from types import SimpleNamespace as sns
from . import data

def cli(caller_file):

    cli = data.sns.from_dict(data.json.read(os.path.join(os.path.dirname(__file__), '../package_data.json')))

    # Load from config file
    cli.config = sns()
    cli.project_root = os.path.join(os.path.dirname(caller_file),
        f"{ '' if 'src' in os.path.dirname(caller_file) else '../../' }../../")
    possile_config_filenames = [
         '.translate-msgs.config.json', 'translate-msgs.config.json',
        f'.{cli.name}.config.json', f'{cli.name}.config.json'
    ]
    for filename in possile_config_filenames:
        cli.config_path = os.path.join(cli.project_root, filename)
        if os.path.exists(cli.config_path):
            cli.config = data.sns.from_dict(data.json.read(cli.config_path))
            cli.config_filename = filename
            break

    # Parse CLI args
    argp = argparse.ArgumentParser(
        description="Translate en/messages.json (chrome.i18n format) to other locales",
        add_help=False  # disable default --help arg to re-create last
    )
    argp.add_argument('-d', '--locales-dir', '--locales-folder',
        type=str, help='Name of the folder containing locale files (default: "_locales")')
    argp.add_argument('-t', '--target-langs', '--target-lang', '--include-langs', '--include-lang',
        type=str, help='Languages to include (e.g. "en,es,fr") (default: all supported locales)')
    argp.add_argument('-k', '--keys', '--key', '--include-keys', '--include-key',
        type=str, help='Keys to translate (e.g. "appDesc,err_notFound")')
    argp.add_argument('--exclude-langs', '--exclude-lang', type=str, help='Languages to exclude (e.g. "en,es")')
    argp.add_argument('--exclude-keys', '--ignore-keys', type=str, help='Keys to ignore (e.g. "appName,author")')
    argp.add_argument('-i', '--init', action='store_true', help=f'Create {cli.name}.config.json file to store defaults')
    argp.add_argument('-f', '--force', action='store_true', help='Force overwrite existing config file when using --init')
    argp.add_argument('-W', '--no-wizard', '--skip-wizard',
        action='store_true', default=None, help='Skip interactive prompts during start-up')
    argp.add_argument('-h', '--help', action='help', help="Show help screen")
    cli.config.__dict__.update({ key:val for key,val in vars(argp.parse_args()).items() if val is not None })

    # Init cli.config vals
    cli.config.target_langs = data.csv.parse(getattr(cli.config, 'target_langs', None))
    cli.config.target_locales = cli.config.target_langs or cli.supported_locales
    cli.config.exclude_langs = data.csv.parse(getattr(cli.config, 'exclude_langs', None))
    cli.config.keys = data.csv.parse(getattr(cli.config, 'keys', None))
    cli.config.exclude_keys = data.csv.parse(getattr(cli.config, 'exclude_keys', None))
    cli.config.locales_dir = getattr(cli.config, 'locales_dir', '_locales')
    if cli.config.exclude_langs:
       cli.config.target_locales = [lang for lang in cli.config.target_locales if lang not in cli.config.exclude_langs]
    cli.config.force = getattr(cli.config, 'force', False)
    cli.config.no_wizard = getattr(cli.config, 'no_wizard', False)

    return cli

def config_file(cli):
    if os.path.exists(cli.config_path):
        if cli.config.force:
            print(f'Overwriting existing config at {cli.config_path}...')
        else:
            print(f'Config already exists at {cli.config_path}.Skipping --init.')
            print('\nTIP: Pass --force to overwrite.')
            return
    cli.config_filename = '.translate-msgs.config.json'
    cli.config_path = os.path.join(cli.project_root, cli.config_filename)
    try:
        jsd_url = f'{cli.urls.jsdelivr}/{cli.name}/{cli.config_filename}'
        resp = requests.get(jsd_url, timeout=5)
        resp.raise_for_status()
        cli.file_config = resp.json()
    except (requests.RequestException, ValueError) as err:
        raise RuntimeError(f"Failed to fetch default config from {jsd_url}: {err}")
    data.json.write(cli.file_config, cli.config_path)
    print(f'Default config created at {cli.config_path}')

def locales_dir(target_dir):
    for root, dirs, _ in os.walk(os.getcwd()):
        if target_dir in dirs:
            return os.path.join(root, target_dir)
    return None
