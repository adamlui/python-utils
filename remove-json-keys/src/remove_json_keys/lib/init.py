import argparse, os
from . import data
from types import SimpleNamespace as sns

def cli():

    cli = data.sns.from_dict(data.json.read(os.path.join(os.path.dirname(__file__), '../package_data.json')))

    # Parse CLI args
    argp = argparse.ArgumentParser(
        description="Remove key/value pairs from JSON files",
        add_help=False  # disable default --help arg to re-create last
    )
    argp.add_argument('--remove-keys', type=str, help='Keys to remove (e.g. "appName,author")')
    argp.add_argument('--json-dir', type=str, help='Name of folder containing JSON files')
    argp.add_argument('--no-wizard', action='store_true', default=None, help='Skip interactive prompts during start-up')
    argp.add_argument('-h', '--help', action='help', help="Show help screen")
    cli.config=sns()
    cli.config.__dict__.update({ key:val for key,val in vars(argp.parse_args()).items() if val is not None })

    # Init cli.config vals
    cli.config.remove_keys = data.csv.parse(getattr(cli.config, 'remove_keys', None))
    cli.config.json_dir = getattr(cli.config, 'json_dir', '_locales')
    cli.config.no_wizard = getattr(cli.config, 'no_wizard', False)

    return cli

def json_dir(target_dir):
    lib_dir = os.path.abspath(os.path.dirname(__file__))
    for root, dirs, _ in os.walk(lib_dir): # search lib_dir recursively
        if target_dir in dirs:
            return os.path.join(root, target_dir)
    parent_dir = os.path.dirname(lib_dir)
    while parent_dir and parent_dir != os.path.dirname(parent_dir):
        for root, dirs, _ in os.walk(parent_dir): # search parent dirs recursively
            if target_dir in dirs:
                return os.path.join(root, target_dir)
        parent_dir = os.path.dirname(parent_dir)
    return None
