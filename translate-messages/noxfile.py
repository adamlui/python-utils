import nox

@nox.session(venv_backend='none')

def bump(session):
    session.run('python', 'utils/bump.py', *session.posargs)
