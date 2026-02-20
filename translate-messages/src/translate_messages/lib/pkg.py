from pathlib import Path

from . import data

def get_ver() : return data.toml.read(Path(__file__).parent.parent / 'pyproject.toml')
