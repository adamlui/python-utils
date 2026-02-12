import argparse, os
from lib import data
from types import SimpleNamespace as sns

def cli():

    cli = data.sns.from_dict(data.json.read(os.path.join(os.path.dirname(__file__), '../cli.json')))

    # Parse CLI args
    parser = argparse.ArgumentParser(description='Remove key/value pairs from JSON files')
    parser.add_argument('--remove-keys', type=str, help='Keys to remove (e.g. "appName,author")')
    parser.add_argument('--json-dir', type=str, help='Name of folder containing JSON files')
    parser.add_argument('--no-wizard', action='store_true', default=None, help='Skip start-up prompts')
    cli.config=sns()
    cli.config.__dict__.update({ key:val for key,val in vars(parser.parse_args()).items() if val is not None })

    # Init cli.config vals
    cli.config.remove_keys = data.csv.parse(cli.config.remove_keys) if getattr(cli.config, 'remove_keys', '') else []
    if not hasattr(cli.config, 'json_dir', '') : cli.config.json_dir = '_locales'
    cli.config.no_wizard = getattr(cli.config, 'no_wizard', False)

    return cli

def json_dir(json_dir):
    lib_dir = os.path.abspath(os.path.dirname(__file__))
    for root, dirs, _ in os.walk(lib_dir): # search lib dir recursively
        if json_dir in dirs:
           json_dir = os.path.join(root, json_dir) ; break
    else: # search lib parent dirs recursively
        parent_dir = os.path.dirname(lib_dir)
        while parent_dir and parent_dir != lib_dir:
            for root, dirs, _ in os.walk(parent_dir):
                if json_dir in dirs:
                   json_dir = os.path.join(root, json_dir) ; break
            if json_dir : break
            parent_dir = os.path.dirname(parent_dir)
        else : json_dir = None
    return json_dir
