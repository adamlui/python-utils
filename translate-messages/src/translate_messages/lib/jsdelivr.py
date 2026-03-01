def create_pkg_ver_url(cli, version=None):
    version = version or cli.version
    return f'{cli.urls.jsdelivr}@{cli.name}-{cli.version}/{cli.name}'

def create_commit_url(cli, hash='latest'):
    return f'{cli.urls.jsdelivr}@{hash}/{cli.name}'
