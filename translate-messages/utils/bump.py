from os import path
import re, sys
from types import SimpleNamespace as sns
import tomli, tomli_w

# Init logger
sys.path.insert(0, path.join(path.dirname(__file__), '../src'))
from translate_messages.lib import log # type: ignore

# Init project data
pyproject_path = path.join(path.dirname(__file__), '../pyproject.toml')
log.info(f'Loading {pyproject_path}...')
with open(pyproject_path, 'rb') as file : pyproject = tomli.load(file)
project = sns(**pyproject['project'])

def update_changelog_url():
    new_ver_tag = f'{project.name}-{project.version}'
    new_changelog_url = f"{project.urls['Releases']}/tag/{new_ver_tag}"
    log.data(f'Generated changelog URL: {new_changelog_url}')
    log.info(f"{ 'Updating' if 'Changelog' in project.urls else 'Adding new' } Changelog URL in pyproject.toml...")
    project.urls['Changelog'] = new_changelog_url
    pyproject['project'] = vars(project) # update og dict for dumping
    with open(pyproject_path, 'wb') as file : tomli_w.dump(pyproject, file)
    log.success(f'Bumped Changelog URL version tag to [{new_ver_tag}]!')

def update_readme_versions():
    readme_path = path.join(path.dirname(__file__), '../README.md')
    log.info('Updating versions in README.md...')
    with open(readme_path, 'r', encoding='utf-8') as file : readme_content = file.read()
    updated_readme_content = re.sub(r'\d+\.\d+\.\d+', project.version, readme_content)
    with open(readme_path, 'w', encoding='utf-8') as file : file.write(updated_readme_content)
    log.success(f'Updated versions in README URLs to [{project.version}]!')

update_changelog_url()
update_readme_versions()
