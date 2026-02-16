import shutil
from pathlib import Path
import nox

@nox.session(venv_backend='none')
def bump_patch(session) : session.run('python', 'utils/bump.py', '--patch', *session.posargs)

@nox.session(venv_backend='none')
def bump_minor(session) : session.run('python', 'utils/bump.py', '--minor', *session.posargs)

@nox.session(venv_backend='none')
def bump_major(session) : session.run('python', 'utils/bump.py', '--major', *session.posargs)

@nox.session(venv_backend='none')
def build(session) : clean(session) ; session.run('python', '-m', 'build') ; print('Build complete!')

@nox.session(venv_backend='none')
def publish(session) : session.run('bash', 'utils/publish.sh', *session.posargs)

@nox.session(venv_backend='none')
def release_patch(session) : bump_patch(session) ; build(session) ; publish(session)

@nox.session(venv_backend='none')
def release_minor(session) : bump_minor(session) ; build(session) ; publish(session)

@nox.session(venv_backend='none')
def release_major(session) : bump_major(session) ; build(session) ; publish(session)

@nox.session(venv_backend='none')
def clean(session):
    paths_to_remove = ['dist', 'build']
    for path in paths_to_remove:
        if Path(path).exists() : shutil.rmtree(path) ; print(f'Removed {path}/')
    for item in Path('.').glob('*.egg-info'):
        if item.is_dir() : shutil.rmtree(item) ; print(f'Removed {item}/')
    print('Clean complete!')
