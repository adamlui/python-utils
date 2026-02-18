from pathlib import Path
import sys
from types import SimpleNamespace as sn

import nox

paths = sn(root=Path(__file__).parent)
paths.pyproject = paths.root / 'pyproject.toml'
sys.path.insert(0, str(paths.root / 'utils'))

from lib import toml # type: ignore

def session(func) : return nox.session(venv_backend='none')(func)

pkg = sn(dir=Path(__file__).parent.name)
pkg.name = pkg.dir.replace('-', '_')

# SESSIONS

@session
def test(session) : session.run('py', '-m', pkg.name, *session.posargs, env={ 'PYTHONPATH': 'src' })
@session
def test_help(session) : session.run('py', '-m', pkg.name, '--help', *session.posargs, env={ 'PYTHONPATH': 'src' })
@session
def test_build(session) : session.run('pip', 'install', '-e', '.') ; session.run(pkg.dir, *session.posargs)

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
    new_ver = toml.read('pyproject.toml')['project']['version']
    session.run('git', 'pull')
    session.run('git', 'add', '.')
    session.run('git', 'commit', '-m', f'Bumped {pkg.dir} versions to {new_ver}')
    session.run('git', 'push')
