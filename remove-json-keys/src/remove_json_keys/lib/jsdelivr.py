from types import SimpleNamespace as sn
from typing import Optional

def create_pkg_ver_url(cli: sn, version: Optional[str] = None) -> str:
    version = version or cli.version
    return f'{cli.urls.jsdelivr}@{cli.name}-{cli.version}/{cli.name}'

def create_commit_url(cli: sn, hash: str = 'latest') -> str:
    return f'{cli.urls.jsdelivr}@{hash}/{cli.name}'
