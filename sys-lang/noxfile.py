from pathlib import Path
import sys
from types import SimpleNamespace as sn

import nox

py_cmd = 'py' if sys.platform.startswith('win') else 'python3'
pkg = sn(dir=Path(__file__).parent.name)
pkg.name = pkg.dir.replace('-', '_')

def session(func) : return nox.session(venv_backend='none', name=func.__name__.replace('_', '-'))(func)

@session
def dev(session) : session.run('pip', 'install', '-e', '.') ; session.run(pkg.dir, '--help', *session.posargs)
@session
def debug(session) : session.run(py_cmd, '-m', pkg.name, '--debug', *session.posargs, env={ 'PYTHONPATH': 'src' })

@session
def lint(session): # staged project files
    files = session.run('git', 'diff', '--cached', '--name-only', '--relative', silent=True, log=False).splitlines()
    if files : session.run('pre-commit', 'run', '--files', *files, *session.posargs)
@session
def lint_all(session): # all project files
    files = session.run('git', 'ls-files', '.', silent=True, log=False).splitlines()
    session.run('pre-commit', 'run', '--files', *files, *session.posargs)

bump_cmd_args = (py_cmd, '-m', 'utils.bump')
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
def build(session) : clean(session) ; session.run(py_cmd, '-m', 'build') ; print('Build complete!')
@session
def publish(session) : session.run('bash', 'utils/publish.sh', *session.posargs)

@session
def deploy_patch(session) : bump_patch(session, no_push=False) ; build(session) ; publish(session)
@session
def deploy_minor(session) : bump_minor(session, no_push=False) ; build(session) ; publish(session)
@session
def deploy_feat(session) : deploy_minor(session)
@session
def deploy_major(session) : bump_major(session, no_push=False) ; build(session) ; publish(session)

@session
def clean(session, *args) : session.run(py_cmd, '-m', 'utils.clean', *args)
