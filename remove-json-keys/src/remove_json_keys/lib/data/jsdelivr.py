def pkg_ver_url(cli, version=None):
    version = version or cli.version
    return f'{cli.urls.jsdelivr}@{version}/{cli.name}'

def commit_url(cli, hash='latest'):
    return f'{cli.urls.jsdelivr}@{hash}/{cli.name}'
