from pathlib import Path
import re
from types import SimpleNamespace as sn
from typing import List, Optional

from . import data, log

def format_code(lang_code: str) -> str: # to match locale dir name (e.g., 'zh-tw' -> 'zh_TW')
    return re.sub(
        r'([a-z]{2,8})[-_]([a-z]{2})',
        lambda m: f'{m.group(1).lower()}_{m.group(2).upper()}',
        lang_code, flags=re.IGNORECASE
    )

def generate_random_lang(includes: Optional[List[str]] = None,
                         excludes: Optional[List[str]] = None) -> str:
    import random

    if includes is None : includes = []
    if excludes is None : excludes = []

    def get_locales() -> List[str]:

        # Read cache if found
        cache_dir = Path(__file__).parent.parent / '_cache'
        locale_cache = cache_dir / 'locales.json'
        if locale_cache.exists():
            try : return data.json.read(locale_cache)
            except Exception : pass

        # Discover pkg _locales
        locales_dir = Path(__file__).parent.parent.parent / 'data/_locales'
        if not locales_dir.exists() : return ['en']
        locales = []
        for entry in locales_dir.iterdir():
            if entry.is_dir() and re.match(r'^\w{2}[-_]?\w{0,2}$', entry.name):
                locales.append(entry.name)

        # Cache result
        cache_dir.mkdir(parents=True, exist_ok=True)
        data.json.write(locale_cache, locales)

        return locales

    locales = includes.copy() if includes else get_locales()

    # Filter out excludes
    exclude_set = set(excludes)
    locales = [locale for locale in locales if locale not in exclude_set]

    # Get random language
    random_lang = random.choice(locales) if locales else 'en'
    log.debug(f'Random language: {random_lang}')

    return random_lang

def get_msgs(cli: sn, lang_code: str = 'en') -> sn:
    from . import jsdelivr, url

    lang_code = format_code(lang_code)
    if getattr(get_msgs, 'cached', None) and lang_code == get_msgs.cached_lang:
        return get_msgs.cached # don't re-fetch same msgs

    msgs = data.json.flatten(data.json.read( # local ones
        Path(__file__).parent.parent.parent / 'data/_locales/en/messages.json'))

    if not lang_code.startswith('en'): # fetch non-English msgs from jsDelivr
        import is_unicode_supported, non_latin_locales
        if lang_code.split('_')[0] in non_latin_locales and not is_unicode_supported(): # type: ignore
            return sn(**msgs) # EN ones cuz non-Latin not supported
        msg_base_url = f'{jsdelivr.create_commit_url(cli, cli.commit_hashes.locales)}' \
                        '/src/get_min_py/data/_locales'
        msg_url = f'{msg_base_url}/{lang_code}/messages.json'
        for attempt in range(3):
            try: # fetch remote msgs
                msgs = data.json.flatten(data.json.read(url.get(msg_url)))
                break
            except Exception: # retry up to 2X (region-stripped + EN)
                if attempt == 2 : break
                msg_url = ( re.sub(r'([^_]*)_[^/]*(/.*)', r'\1\2', msg_url) # strip region before retrying
                    if attempt == 0 and '-' in lang_code else f'{msg_base_url}/en/messages.json') # else use EN msgs

    get_msgs.cached = msgs
    get_msgs.cached_lang = lang_code

    return sn(**msgs)
