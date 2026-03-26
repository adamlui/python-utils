from pathlib import Path
from types import SimpleNamespace as sn

import nox

pkg = sn(dir=Path(__file__).parent.name)
pkg.name = pkg.dir.replace('-', '_')
paths = sn(utils=sn(bump='utils/bump.py', clean='utils/clean.py', publish='utils/publish.sh'))

def session(func) : return nox.session(venv_backend='none', name=func.__name__.replace('_', '-'))(func)

@session
def dev(session) : session.run('pip', 'install', '-e', '.') ; session.run(pkg.dir, '--help', *session.posargs)
@session
def debug(session) : session.run('py', '-m', pkg.name, '--debug', *session.posargs, env={ 'PYTHONPATH': 'src' })

@session
def lint(session): # staged project files
    files = session.run('git', 'diff', '--cached', '--name-only', '--relative', silent=True, log=False).splitlines()
    if files : session.run('pre-commit', 'run', '--files', *files, *session.posargs)
@session
def lint_all(session): # all project files
    files = session.run('git', 'ls-files', '.', silent=True, log=False).splitlines()
    session.run('pre-commit', 'run', '--files', *files, *session.posargs)

bump_cmd_args = ('py', paths.utils.bump)
@session
def bump_patch(session, no_push=True):
    cmd_args = bump_cmd_args + ('--patch',)
    if no_push : cmd_args += ('--no-push',)
    session.run(*cmd_args, *session.posargs)
@session
def bump_minor(session, no_push=True):
    cmd_args = bump_cmd_args + ('--minor',)
    if no_push : cmd_args += ('--no-push',)
    session.run(*cmd_args, *session.posargs)
@session
def bump_feat(session, no_push=True):
    bump_minor(session, no_push)
@session
def bump_major(session, no_push=True):
    cmd_args = bump_cmd_args + ('--major',)
    if no_push : cmd_args += ('--no-push',)
    session.run(*cmd_args, *session.posargs)

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
def clean(session, *args) : session.run('py', paths.utils.clean, *args)
