import nox

def session(func) : return nox.session(venv_backend='none')(func)

@session
def test(session) : session.run('py', '-m', 'translate_messages', *session.posargs, env={'PYTHONPATH': 'src'})
@session
def test_build(session) : session.run('pip', 'install', '-e', '.') ; session.run('translate-messages', *session.posargs)

@session
def bump(session) : session.run('py', 'utils/bump.py', *session.posargs)
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
def deploy_patch(session) : bump_patch(session) ; build(session) ; publish(session)
@session
def deploy_minor(session) : bump_minor(session) ; build(session) ; publish(session)
@session
def deploy_major(session) : bump_major(session) ; build(session) ; publish(session)

@session
def clean(session) : session.run('py', 'utils/clean.py')
