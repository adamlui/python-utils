from pathlib import Path
from types import SimpleNamespace as sn

from ...api import get_sys_lang
from . import data

def cli() -> sn:
    from . import env, language, settings
    cli = data.sns.from_dict(data.json.read(Path(__file__).parent.parent.parent / 'data/package_data.json'))
    cli.msgs = language.get_msgs(cli,
        language.generate_random_lang(excludes=['en']) if env.is_debug_mode() else get_sys_lang())
    settings.load(cli)
    return cli
