from pathlib import Path
from types import SimpleNamespace as sn

import nox

pkg = sn(dir=Path(__file__).parent.name)
pkg.name = pkg.dir.replace('-', '_')
paths = sn(utils=sn(bump='utils/bump.py', clean='utils/clean.py', publish='utils/publish.sh'))

def session(func) : return nox.session(venv_backend='none')(func)

# SESSIONS

@session
def test(session) : session.run('py', '-m', pkg.name, *session.posargs, env={ 'PYTHONPATH': 'src' })
@session
def test_help(session) : session.run('py', '-m', pkg.name, '--help', *session.posargs, env={ 'PYTHONPATH': 'src' })
@session
def test_docs(session) : session.run('py', '-m', pkg.name, '--docs', *session.posargs, env={ 'PYTHONPATH': 'src' })
@session
def test_build(session) : session.run('pip', 'install', '-e', '.') ; session.run(pkg.dir, *session.posargs)

@session
def debug(session) : session.run('py', '-m', pkg.name, '--debug', *session.posargs, env={ 'PYTHONPATH': 'src' })

@session
def bump_patch(session, no_push=True):
    cmd = ['py', paths.utils.bump, '--patch']
    if no_push : cmd.append('--no-push')
    session.run(*cmd, *session.posargs)
@session
def bump_minor(session, no_push=True):
    cmd = ['py', paths.utils.bump, '--minor']
    if no_push : cmd.append('--no-push')
    session.run(*cmd, *session.posargs)
@session
def bump_feat(session, no_push=True): 
    bump_minor(session, no_push)
@session
def bump_major(session, no_push=True):
    cmd = ['py', paths.utils.bump, '--major']
    if no_push : cmd.append('--no-push')
    session.run(*cmd, *session.posargs)

@session
def build(session) : clean(session) ; session.run('py', '-m', 'build') ; print('Build complete!')
@session
def publish(session) : session.run('bash', paths.utils.publish, *session.posargs)

@session
def deploy_patch(session) : bump_patch(session, no_push=False) ; build(session) ; publish(session)
@session
def deploy_minor(session) : bump_minor(session, no_push=False) ; build(session) ; publish(session)
@session
def deploy_feat(session) : deploy_minor(session)
@session
def deploy_major(session) : bump_major(session, no_push=False) ; build(session) ; publish(session)

@session
def clean(session) : session.run('py', paths.utils.clean)
