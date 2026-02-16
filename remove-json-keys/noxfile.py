import nox

def session(func) : return nox.session(venv_backend='none')(func)

@session
def bump(session) : session.run('python', 'utils/bump.py', *session.posargs)
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
def clean(session) : session.run('python', 'utils/clean.py')
