import nox

def session(func) : return nox.session(venv_backend='none', name=func.__name__.replace('_', '-'))(func)

@session
def lint(session): # staged monorepo files
    files = session.run('git', 'diff', '--cached', '--name-only', '--relative', silent=True, log=False).splitlines()
    if files : session.run('pre-commit', 'run', '--files', *files, *session.posargs)
@session
def lint_all(session): # all monorepo files
    session.run('pre-commit', 'run', '--all-files', *session.posargs)

@session
def update_langs(session): # update lang pkg data
    from pathlib import Path
    start_dir = Path.cwd()
    for subdir in Path(__file__).parent.glob('*-languages'):
        if subdir.is_dir():
            session.chdir(subdir)
            session.run('nox', '-s', 'update', *session.posargs, external=True)
            session.chdir(start_dir)
