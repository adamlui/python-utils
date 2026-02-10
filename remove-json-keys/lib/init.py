import argparse
from types import SimpleNamespace as sns

def cli():
    cli = sns(
        name='remove-json-keys',
        version='2026.2.10.26',
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
    parser.add_argument('--remove-keys', type=str, help='Keys to remove')
    parser.add_argument('--json-dir', type=str, help='Name of folder containing JSON files')
    cli.args = parser.parse_args()
    cli.json_dir = cli.args.json_dir or '_locales'

    return cli
