from os import path
from types import SimpleNamespace as sns
import sys
import tomli, tomli_w

sys.path.insert(0, path.join(path.dirname(__file__), '../src'))
from remove_json_keys.lib import log # type: ignore

pyproject_path = path.join(path.dirname(__file__), '../pyproject.toml')
log.info(f'Loading {pyproject_path}...')
with open(pyproject_path, 'rb') as file : pyproject = tomli.load(file)
project = sns(**pyproject['project'])

def update_changelog_url():
    ver_tag = f'{project.name}-{project.version}'
    changelog_url = f'https://github.com/adamlui/python-utils/releases/tag/{ver_tag}'
    log.data(f'Generated changelog URL: {changelog_url}')
    log.info(f"{ 'Updating' if 'Changelog' in project.urls else 'Adding new' } Changelog URL...")
    project.urls['Changelog'] = changelog_url
    pyproject['project'] = vars(project) # update og dict for dumping
    with open(pyproject_path, 'wb') as file : tomli_w.dump(pyproject, file)
    log.success(f'Bumped changelog URL ver tag to [{ver_tag}]!')

update_changelog_url()
