from os import path
import sys
import tomli, tomli_w

sys.path.insert(0, path.join(path.dirname(__file__), '../src'))
from translate_messages.lib import log # type: ignore

pyproject_path = path.join(path.dirname(__file__), '../pyproject.toml')
with open(pyproject_path, 'rb') as file:
    pkg_name = tomli.load(file)['project']['name']

def update_changelog_url():

    log.info(f'Loading {pyproject_path}...')
    with open(pyproject_path, 'rb') as file : pyproject = tomli.load(file)

    ver_tag = f"{pkg_name}-{pyproject['project']['version']}"
    changelog_url = f'https://github.com/adamlui/python-utils/releases/tag/{ver_tag}'
    log.data(f'Generated changelog URL: {changelog_url}')

    if 'urls' not in pyproject['project']:
        log.info('Creating [project.urls] section...')
        pyproject['project']['urls'] = {}

    log.info(f"{ 'Updating' if 'Changelog' in pyproject['project']['urls'] else 'Adding new' } Changelog URL...")
    pyproject['project']['urls']['Changelog'] = changelog_url
    with open(pyproject_path, 'wb') as file : tomli_w.dump(pyproject, file)

    log.success(f"Bumped changelog URL ver tag to [{ver_tag}]!")

update_changelog_url()
