import argparse, os
from types import SimpleNamespace as sns

def cli():

    cli = sns(
        name='remove-json-keys',
        version='2026.2.10.34',
        author=sns(name='Adam Lui', email='adam@kudoa.com', url='https://github.com/adamlui'),
        description='Remove key/value pairs from json_dir/**.json',
        urls=sns(
            github='https://github.com/adamlui/python-utils',
            jsdelivr='https://cdn.jsdelivr.net/gh/adamlui/python-utils',
            sponsor='https://github.com/sponsors/adamlui',
            support='https://github.com/adamlui/python-utils/issues'
        ),
    )

    # Parse CLI args
    parser = argparse.ArgumentParser(description='Remove key/value pairs from JSON files')
    parser.add_argument('--remove-keys', type=str, help='Keys to remove (e.g. "appName,author")')
    parser.add_argument('--json-dir', type=str, help='Name of folder containing JSON files')
    cli.args = parser.parse_args()
    cli.json_dir = cli.args.json_dir or '_locales'

    return cli

def json_dir(json_dir):
    script_dir = os.path.abspath(os.path.dirname(__file__))
    for root, dirs, files in os.walk(script_dir): # search script dir recursively
        if json_dir in dirs:
            json_dir = os.path.join(root, json_dir) ; break
    else: # search script parent dirs recursively
        parent_dir = os.path.dirname(script_dir)
        while parent_dir and parent_dir != script_dir:
            for root, dirs, files in os.walk(parent_dir):
                if json_dir in dirs:
                    json_dir = os.path.join(root, json_dir) ; break
            if json_dir : break
            parent_dir = os.path.dirname(parent_dir)
        else : json_dir = None
    return json_dir
