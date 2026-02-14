import argparse, re, sys
from os import path
from types import SimpleNamespace as sns
import tomli, tomli_w

sys.path.insert(0, path.join(path.dirname(__file__), '../src'))
from translate_messages.lib import log # type: ignore

# Parse args
argp = argparse.ArgumentParser(
    description='Bump versions in pyproject.toml + README.md',
    add_help=False # disable default --help to re-create last
)
argp.add_argument('-M', '--major', action='store_true', help='Bump the major (\033[1mx\033[0m.y.z) version')
argp.add_argument('-m', '--minor', action='store_true', help='Bump the minor (x.\033[1my\033[0m.z) version')
argp.add_argument('-p', '--patch', action='store_true', help='Bump the patch (x.y.\033[1mz\033[0m) version')
argp.add_argument('-h', '--help',  action='help',       help='Show help screen')
args = argp.parse_args()

# Init bump_type
bump_type = 'major' if args.major else 'minor' if args.minor else 'patch' if args.patch else None
if not bump_type:
    log.error('You must pass --<major|minor|patch> as an argument.')
    sys.exit(1)

# Init project data
pyproject_path = path.join(path.dirname(__file__), '../pyproject.toml')
log.info(f'Loading {pyproject_path}...')
with open(pyproject_path, 'rb') as file : pyproject = tomli.load(file)
project = sns(**pyproject['project'])

def bump_pyproject_versions(bump_type): # project.version + .urls['Changelog']

    # Bump project.version
    current_ver = project.version
    major, minor, patch = map(int, current_ver.split('.'))
    if   bump_type == 'major' : patch =  0 ; minor =  0 ; major += 1
    elif bump_type == 'minor' : patch =  0 ; minor += 1 ; 
    elif bump_type == 'patch' : patch += 1
    pyproject['project']['version'] = new_ver = f'{major}.{minor}.{patch}'
    with open(pyproject_path, 'wb') as file : tomli_w.dump(pyproject, file)
    log.success(f'Bumped project.version in pyproject.toml from [{current_ver}] to [{new_ver}]')

    # Bump version tag in project.urls['Changelog']
    new_ver_tag = f'{project.name}-{new_ver}'
    new_changelog_url = f"{project.urls['Releases']}/tag/{new_ver_tag}"
    log.data(f'Generated Changelog URL: {new_changelog_url}')
    log.info(f"{ 'Updating' if 'Changelog' in project.urls else 'Adding new' } Changelog URL in pyproject.toml...")
    project.urls['Changelog'] = new_changelog_url
    with open(pyproject_path, 'wb') as file : tomli_w.dump(pyproject, file)
    log.success(f'Bumped Changelog URL version tag to [{new_ver_tag}]!')

    return new_ver

def update_readme_versions(new_ver): # in URLs
    readme_path = path.join(path.dirname(__file__), '../README.md')
    log.info('Updating versions in README.md...')
    with open(readme_path, 'r', encoding='utf-8') as file : readme_content = file.read()
    updated_readme_content = re.sub(r'\d+\.\d+\.\d+', new_ver, readme_content)
    with open(readme_path, 'w', encoding='utf-8') as file : file.write(updated_readme_content)
    log.success(f'Updated versions in README URLs to [{new_ver}]!')

update_readme_versions(bump_pyproject_versions(bump_type))
