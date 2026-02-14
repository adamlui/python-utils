import os, logging
import tomli, tomli_w

pkg_name = 'remove-json-keys'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def update_changelog_url():
    pyproject_path = os.path.join(os.path.dirname(__file__), '../pyproject.toml')
    logging.debug(f'Reading pyproject.toml from: {pyproject_path}')
    if not os.path.exists(pyproject_path):
        return logging.error(f'pyproject.toml file not found at {pyproject_path}')

    try: # load pyproject.toml
        with open(pyproject_path, 'rb') as file : pyproject = tomli.load(file)
        logging.debug('Successfully loaded pyproject.toml!')
    except Exception as err:
        return logging.exception(f'Error loading pyproject.toml: {err}')

    version = pyproject.get('project', {}).get('version')
    if not version:
        return logging.error('Version not found in pyproject.toml.')

    changelog_url = f'https://github.com/adamlui/python-utils/releases/tag/{pkg_name}-{version}'
    logging.debug(f'Generated changelog URL: {changelog_url}')
    
    if 'urls' not in pyproject['project']:
        logging.debug('Adding [project.urls] section to pyproject.toml...')
        pyproject['project']['urls'] = {}

    if 'Changelog' in pyproject['project']['urls']:
        logging.debug('Replacing existing Changelog URL...')
    else:
        logging.debug('Adding new Changelog URL...')
    pyproject['project']['urls']['Changelog'] = changelog_url

    try: # write to pyproject.toml
        with open(pyproject_path, 'wb') as file : tomli_w.dump(pyproject, file)
        logging.info('Updated changelog URL successfully in pyproject.toml!')
    except Exception as err:
        logging.exception(f'Error writing to pyproject.toml: {err}')

update_changelog_url()
