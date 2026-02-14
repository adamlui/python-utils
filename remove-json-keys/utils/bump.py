import os, logging
import tomli, tomli_w

pyproject_path = os.path.join(os.path.dirname(__file__), '../pyproject.toml')
with open(pyproject_path, 'rb') as file:
    pkg_name = tomli.load(file)['project']['name']

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def update_changelog_url():

    logging.debug(f'Loading {pyproject_path}...')
    with open(pyproject_path, 'rb') as file : pyproject = tomli.load(file)

    ver_tag = f"{pkg_name}-{pyproject['project']['version']}"
    changelog_url = f'https://github.com/adamlui/python-utils/releases/tag/{ver_tag}'
    logging.debug(f'Generated changelog URL: {changelog_url}')
    
    if 'urls' not in pyproject['project']:
        logging.debug('Creating [project.urls] section...')
        pyproject['project']['urls'] = {}

    logging.debug(f"{'Updating' if 'Changelog' in pyproject['project']['urls'] else 'Adding new '} Changelog URL...")
    pyproject['project']['urls']['Changelog'] = changelog_url
    with open(pyproject_path, 'wb') as file : tomli_w.dump(pyproject, file)

    logging.info(f"Bumped changelog URL ver tag to [{ver_tag}]!")

update_changelog_url()
