import argparse, os
from . import data
from types import SimpleNamespace as sns

def cli():

    cli = data.sns.from_dict(data.json.read(os.path.join(os.path.dirname(__file__), '../package_data.json')))

    # Parse CLI args
    argp = argparse.ArgumentParser(
        description="Simply remove JSON keys via CLI command",
        add_help=False  # disable default --help arg to re-create last
    )
    argp.add_argument('-d', '--json-dir', '--json-folder',
        type=str, help='Name of the folder containing JSON files (default: "_locales")')
    argp.add_argument('-k', '--keys', '--remove-keys', type=str, help='Keys to remove (e.g. "appName,author")')
    argp.add_argument('-W', '--no-wizard', '--skip-wizard',
        action='store_true', default=None, help='Skip interactive prompts during start-up')
    argp.add_argument('-h', '--help', action='help', help="Show help screen")
    cli.config=sns()
    cli.config.__dict__.update({ key:val for key,val in vars(argp.parse_args()).items() if val is not None })

    # Init cli.config vals
    cli.config.keys = data.csv.parse(getattr(cli.config, 'keys', None))
    cli.config.json_dir = getattr(cli.config, 'json_dir', '_locales')
    cli.config.no_wizard = getattr(cli.config, 'no_wizard', False)

    return cli

def json_dir(target_dir):
    for root, dirs, _ in os.walk(os.getcwd()):
        if target_dir in dirs:
            return os.path.join(root, target_dir)
    return None
