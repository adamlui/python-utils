import argparse, re, sys
from os import path
from types import SimpleNamespace as sns
import tomli, tomli_w

sys.path.insert(0, path.join(path.dirname(__file__), '../src'))
from remove_json_keys.lib import log # type: ignore

msgs = sns(
    pkgDesc='Bump versions in pyproject.toml + README.md',
    help_major='Bump the major (\033[1mx\033[0m.y.z) version',
    help_minor='Bump the minor (x.\033[1my\033[0m.z) version',
    help_patch='Bump the patch (x.y.\033[1mz\033[0m) version',
    help_help='Show help screen',
    err_invalid_arg='You must pass --<major|minor|patch> as an argument.',
    log_loading_pyproject='Loading {pyproject_path}',
    log_bumped_project_ver='Bumped project.version in pyproject.toml from [{prev_ver}] to [{new_ver}]',
    log_created_changelog_url='Generated Changelog URL',
    log_updating_changelog_url_in='Updating Changelog URL in',
    log_bumped_changelog_url_ver_tag='Bumped Changelog URL version tag to [{ver_tag}]',
    log_updating_vers_in='Updating versions in',
    log_updated_readme_vers='Updated versions in README URLs to [{new_ver}]!'
)

def parse_args():
    argp = argparse.ArgumentParser(description=msgs.pkgDesc, add_help=False)
    argp.add_argument('-M', '--major', action='store_true', help=msgs.help_major)
    argp.add_argument('-m', '--minor', action='store_true', help=msgs.help_minor)
    argp.add_argument('-p', '--patch', action='store_true', help=msgs.help_patch)
    argp.add_argument('-h', '--help',  action='help', help=msgs.help_help)
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
    with open(pyproject_path, 'wb') as file : tomli_w.dump(pyproject, file)
    log.success(msgs.log_bumped_project_ver.format(prev_ver=project.version, new_ver=new_ver))

    # Bump project.urls['Releases']
    ver_tag = f'{project.name}-{new_ver}'
    changelog_url = f"{project.urls['Releases']}/tag/{ver_tag}"
    log.data(f"{msgs.log_created_changelog_url}: {changelog_url}")
    log.info(f'{msgs.log_updating_changelog_url_in} pyproject.toml...')
    pyproject['project']['urls']['Changelog'] = changelog_url
    with open(pyproject_path, 'wb') as file : tomli_w.dump(pyproject, file)
    log.success(msgs.log_bumped_changelog_url_ver_tag.format(ver_tag=ver_tag))

def update_readme_vers(new_ver): # in URLs
    log.info(f'{msgs.log_updating_vers_in} README.md...')
    readme_path = path.join(path.dirname(__file__), '../README.md')
    with open(readme_path, 'r', encoding='utf-8') as file : readme_content = file.read()
    updated_readme_content = re.sub(r'\d+\.\d+\.\d+', new_ver, readme_content)
    with open(readme_path, 'w', encoding='utf-8') as file : file.write(updated_readme_content)
    log.success(msgs.log_updated_readme_vers.format(new_ver=new_ver))

def main():

    # Parse args
    args = parse_args()
    bump_type = 'major' if args.major else 'minor' if args.minor else 'patch' if args.patch else None
    if not bump_type : log.error(msgs.err_invalid_arg) ; sys.exit(1)

    # Init project data
    pyproject_path = path.join(path.dirname(__file__), '../pyproject.toml')
    log.info(f'{msgs.log_loading_pyproject.format(pyproject_path=pyproject_path)}...')
    with open(pyproject_path, 'rb') as file : pyproject = tomli.load(file)
    project = sns(**pyproject['project'])

    # Update files
    _, new_ver = init_vers(project, bump_type)
    bump_pyproject_vers(pyproject_path, pyproject, project, new_ver)    
    update_readme_vers(new_ver)

if __name__ == '__main__' : main()
