from os import path
import sys
from types import SimpleNamespace as sns
import tomli, tomli_w

# Init logger
sys.path.insert(0, path.join(path.dirname(__file__), '../src'))
from remove_json_keys.lib import log # type: ignore

# Init project data
pyproject_path = path.join(path.dirname(__file__), '../pyproject.toml')
log.info(f'Loading {pyproject_path}...')
with open(pyproject_path, 'rb') as file : pyproject = tomli.load(file)
project = sns(**pyproject['project'])

def update_changelog_url():
    new_ver_tag = f'{project.name}-{project.version}'
    new_changelog_url = f"{project.urls['Releases']}/tag/{new_ver_tag}"
    log.data(f'Generated changelog URL: {new_changelog_url}')
    log.info(f"{ 'Updating' if 'Changelog' in project.urls else 'Adding new' } Changelog URL...")
    project.urls['Changelog'] = new_changelog_url
    pyproject['project'] = vars(project) # update og dict for dumping
    with open(pyproject_path, 'wb') as file : tomli_w.dump(pyproject, file)
    log.success(f'Bumped changelog URL ver tag to [{new_ver_tag}]!')

update_changelog_url()
