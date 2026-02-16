import shutil
from pathlib import Path
import nox

@nox.session(venv_backend='none')
def bump(session):
    session.run('python', 'utils/bump.py', *session.posargs)

@nox.session(venv_backend='none')
def clean(session):
    paths_to_remove = ['dist', 'build']

    for path in paths_to_remove:
        if Path(path).exists():
            shutil.rmtree(path)
            print(f'Removed {path}/')
    
    for item in Path('.').glob('*.egg-info'):
        if item.is_dir():
            shutil.rmtree(item)
            print(f'Removed {item}/')
    
    print('Clean complete!')

@nox.session(venv_backend='none')
def build(session):
    clean(session)
    session.run('python', '-m', 'build')
    print('Build complete!')
