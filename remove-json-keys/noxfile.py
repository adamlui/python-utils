import shutil
from pathlib import Path
import nox

def session(func) : return nox.session(venv_backend='none')(func)

@session
def bump_patch(session) : session.run('python', 'utils/bump.py', '--patch', *session.posargs)
@session
def bump_minor(session) : session.run('python', 'utils/bump.py', '--minor', *session.posargs)
@session
def bump_major(session) : session.run('python', 'utils/bump.py', '--major', *session.posargs)
@session
def build(session) : clean(session) ; session.run('python', '-m', 'build') ; print('Build complete!')
@session
def publish(session) : session.run('bash', 'utils/publish.sh', *session.posargs)
@session
def deploy_patch(session) : bump_patch(session) ; build(session) ; publish(session)
@session
def deploy_minor(session) : bump_minor(session) ; build(session) ; publish(session)
@session
def deploy_major(session) : bump_major(session) ; build(session) ; publish(session)

@session
def clean(session):
    paths_to_remove = ['dist', 'build']
    for path in paths_to_remove:
        if Path(path).exists() : shutil.rmtree(path) ; print(f'Removed {path}/')
    for item in Path('.').glob('*.egg-info'):
        if item.is_dir() : shutil.rmtree(item) ; print(f'Removed {item}/')
    print('Clean complete!')
