import argparse, os
from types import SimpleNamespace as sns

def cli():
    cli = sns(
        name='remove-json-keys',
        urls=sns(jsdelivr='https://cdn.jsdelivr.net/gh/adamlui/python-utils')
    )

    # Parse CLI args
    parser = argparse.ArgumentParser(description='Remove key/value pairs from JSON files')
    parser.add_argument('--remove-keys', type=str, help='Keys to remove')
    parser.add_argument('--json-dir', type=str, help='Name of folder containing JSON files')
    cli.args = parser.parse_args()
    cli.json_dir = cli.args.json_dir or '_locales'

    return cli

def env():
    env = sns()
    try:
        env.terminal_width = os.get_terminal_size()[0]
    except OSError:
        env.terminal_width = 80

    return env
