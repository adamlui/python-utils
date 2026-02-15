import argparse, re, sys
from os import path
from types import SimpleNamespace as sn
from lib import toml

sys.path.insert(0, path.join(path.dirname(__file__), '../src'))
from translate_messages.lib import data, log # type: ignore

msgs = sn(
    pkg_DESC='Bump versions in pyproject.toml + README.md',
    help_MAJOR='Bump the major (\033[1mx\033[0m.y.z) version',
    help_MINOR='Bump the minor (x.\033[1my\033[0m.z) version',
    help_PATCH='Bump the patch (x.y.\033[1mz\033[0m) version',
    help_HELP='Show help screen',
    err_INVALID_ARG='You must pass --<major|minor|patch> as an argument.',
    log_LOADING_PYPROJECT='Loading {pyproject_path}',
    log_BUMPED_PROJECT_VER='Bumped project.version in pyproject.toml from [{prev_ver}] to [{new_ver}]',
    log_CREATED_CHANGELOG_URL='Generated Changelog URL',
    log_UPDATING_CHANGELOG_URL_IN='Updating Changelog URL in',
    log_BUMPED_CHANGELOG_URL_VER_TAG='Bumped Changelog URL version tag to [{ver_tag}]',
    log_UPDATING_VERS_IN='Updating versions in',
    log_UPDATED_README_VERS='Updated versions in README URLs to [{new_ver}]!'
)

def parse_args():
    argp = argparse.ArgumentParser(description=msgs.pkg_DESC, add_help=False)
    argp.add_argument('-M', '--major', action='store_true', help=msgs.help_MAJOR)
    argp.add_argument('-m', '--minor', action='store_true', help=msgs.help_MINOR)
    argp.add_argument('-p', '--patch', action='store_true', help=msgs.help_PATCH)
    argp.add_argument('-h', '--help',  action='help', help=msgs.help_HELP)
    return argp.parse_args()

def init_vers(project, bump_type): # <prev|new>_ver
    prev_ver = project.version
    major, minor, patch = map(int, prev_ver.split('.'))
    if   bump_type == 'major' : patch =  0 ; minor =  0 ; major += 1
    elif bump_type == 'minor' : patch =  0 ; minor += 1
    elif bump_type == 'patch' : patch += 1
    new_ver = f'{major}.{minor}.{patch}'
    return prev_ver, new_ver

def bump_pyproject_vers(pyproject_path, pyproject, project, new_ver): # project.version + .urls['Releases']

    # Bump project.version
    pyproject['project']['version'] = new_ver
    toml.write(pyproject_path, pyproject)
    log.success(msgs.log_BUMPED_PROJECT_VER.format(prev_ver=project.version, new_ver=new_ver))

    # Bump project.urls['Releases']
    ver_tag = f'{project.name}-{new_ver}'
    changelog_url = f"{project.urls['Releases']}/tag/{ver_tag}"
    log.data(f"{msgs.log_CREATED_CHANGELOG_URL}: {changelog_url}")
    log.info(f'{msgs.log_UPDATING_CHANGELOG_URL_IN} pyproject.toml...')
    pyproject['project']['urls']['Changelog'] = changelog_url
    toml.write(pyproject_path, pyproject)
    log.success(msgs.log_BUMPED_CHANGELOG_URL_VER_TAG.format(ver_tag=ver_tag))

def update_readme_vers(new_ver): # in URLs
    log.info(f'{msgs.log_UPDATING_VERS_IN} README.md...')
    readme_path = path.join(path.dirname(__file__), '../docs/README.md')
    updated_readme_content = re.sub(r'\b(?>\d{1,3}\.\d{1,3}\.\d{1,3})\b', new_ver, data.file.read(readme_path))
    data.file.write(readme_path, updated_readme_content)
    log.success(msgs.log_UPDATED_README_VERS.format(new_ver=new_ver))

def main():

    # Parse args
    args = parse_args()
    bump_type = 'major' if args.major else 'minor' if args.minor else 'patch' if args.patch else None
    if not bump_type : log.error(msgs.err_INVALID_ARG) ; sys.exit(1)

    # Init project data
    pyproject_path = path.join(path.dirname(__file__), '../pyproject.toml')
    log.info(f'{msgs.log_LOADING_PYPROJECT.format(pyproject_path=pyproject_path)}...')
    pyproject = toml.read(pyproject_path)
    project = sn(**pyproject['project'])

    # Update files
    _, new_ver = init_vers(project, bump_type)
    bump_pyproject_vers(pyproject_path, pyproject, project, new_ver)    
    update_readme_vers(new_ver)

if __name__ == '__main__' : main()
