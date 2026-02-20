from pathlib import Path
import sys
from types import SimpleNamespace as sn

import nox

paths = sn(root=Path(__file__).parent)
sys.path.insert(0, str(paths.root / 'src'))

from remove_json_keys.lib import pkg # type: ignore

def session(func) : return nox.session(venv_backend='none')(func)

project = sn(dir=paths.root.name)
project.name = project.dir.replace('-', '_')

# SESSIONS

@session
def test(session) : session.run('py', '-m', project.name, *session.posargs, env={ 'PYTHONPATH': 'src' })
@session
def test_help(session) : session.run('py', '-m', project.name, '--help', *session.posargs, env={ 'PYTHONPATH': 'src' })
@session
def test_build(session) : session.run('pip', 'install', '-e', '.') ; session.run(project.dir, *session.posargs)

@session
def debug(session) : session.run('py', '-m', project.name, '--debug', *session.posargs, env={ 'PYTHONPATH': 'src' })

@session
def bump_patch(session) : session.run('py', 'utils/bump.py', '--patch', *session.posargs)
@session
def bump_minor(session) : session.run('py', 'utils/bump.py', '--minor', *session.posargs)
@session
def bump_major(session) : session.run('py', 'utils/bump.py', '--major', *session.posargs)

@session
def build(session) : clean(session) ; session.run('py', '-m', 'build') ; print('Build complete!')
@session
def publish(session) : session.run('bash', 'utils/publish.sh', *session.posargs)

@session
def deploy_patch(session) : bump_patch(session) ; push_bump(session) ; build(session) ; publish(session)
@session
def deploy_minor(session) : bump_minor(session) ; push_bump(session) ; build(session) ; publish(session)
@session
def deploy_major(session) : bump_major(session) ; push_bump(session) ; build(session) ; publish(session)

@session
def clean(session) : session.run('py', 'utils/clean.py')

# HELPERS

def push_bump(session):
    new_ver = pkg.get_ver()
    session.run('git', 'pull')
    session.run('git', 'add', '.')
    session.run('git', 'commit', '-m', f'Bumped {project.dir} versions to {new_ver}')
    session.run('git', 'push')
