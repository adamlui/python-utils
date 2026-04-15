from pathlib import Path
import re, sys
from types import SimpleNamespace as sn
from typing import Any, Dict, List, Optional, Tuple

from . import data, log

def create_translations(cli: sn, target_msgs: Dict[str, Any], lang_code: str) -> Dict[str, Dict[str, str]]:
    from translate import Translator

    fail_flags = ['INVALID TARGET LANGUAGE', 'MYMEMORY']
    src_keys = cli.config.keys or cli.en_msgs
    src_keys = [key for key in src_keys if key in cli.en_msgs]
    translated_msgs = {}

    for key in src_keys:

        if cli.config.exclude_keys and key in cli.config.exclude_keys:
            translated_msgs[key] = { 'message': cli.en_msgs[key]['message'] }
            continue

        if key not in target_msgs:
            original_msg = translated_msg = cli.en_msgs[key]['message']
            try:
                translator = Translator(provider='', to_lang=lang_code)
                translated_msg = re.sub(r'&(?:quot|#39);', "'", translator.translate(original_msg))
                if any(fail_flag in translated_msg.upper() for fail_flag in fail_flags):
                    translated_msg = original_msg
            except Exception as err:
                print(f'\n{log.colors.br}{cli.msgs.err_TRANSLATE_FAILED_FOR_KEY} "{key}": {err}')
                if 'TOO MANY REQUESTS' in str(err).upper() : log.tip(f'{cli.msgs.tip_USE_A_VPN}.') ; sys.exit(1)
                translated_msg = original_msg
            translated_msgs[key] = { 'message': translated_msg }
        else:
            translated_msgs[key] = target_msgs[key]

    return translated_msgs

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
                        '/src/translate_messages/data/_locales'
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

def write_translations(cli: sn) -> Tuple[List[str], List[str], List[str], List[str]]:

    langs_added, langs_skipped, langs_translated, langs_not_translated = [], [], [], []
    for lang_code in cli.config.target_langs:
        lang_added, lang_skipped, lang_translated = False, False, False
        lang_dir = lang_code.replace('-', '_')

        if lang_code.startswith('en'): # skip EN locales
            print(f'\n{log.colors.gry}{cli.msgs.log_SKIPPED} {lang_dir}/{cli.msgs_filename}...{log.colors.nc}', end='')
            langs_skipped.append(lang_code) ; langs_not_translated.append(lang_code)
            continue

        if '-' in lang_code: # uppercase suffix
            sep_idx = lang_dir.index('_')
            lang_dir = f'{lang_dir[:sep_idx]}_{lang_dir[sep_idx+1:].upper()}'

        lang_dir_path = cli.locales_path / lang_dir
        msgs_path = lang_dir_path / cli.msgs_filename
        if msgs_path.exists() and data.json.is_valid(msgs_path):
            msgs = data.json.read(msgs_path)
        else:
            msgs = {}
            lang_dir_path.mkdir(parents=True, exist_ok=True)
            langs_added.append(lang_code) ; lang_added = True

        action = cli.msgs.log_ADDING if not msgs else cli.msgs.log_UPDATING
        log.info(f'{action} {lang_dir}/{cli.msgs_filename}...', end='')
        sys.stdout.flush()
        translated_msgs = create_translations(cli, msgs, lang_code)

        if translated_msgs == msgs:
            langs_skipped.append(lang_code) ; lang_skipped = True
        else:
            data.json.write(msgs_path, translated_msgs, style='compact')
            langs_translated.append(lang_code) ; lang_translated = True
        if not lang_translated : langs_not_translated.append(lang_code)

        status = f'{log.colors.dg}{cli.msgs.log_ADDED}' if lang_added else \
                 f'{log.colors.gry}{cli.msgs.log_SKIPPED}' if lang_skipped else \
                 f'{log.colors.dy}{cli.msgs.log_UPDATED}'
        log.overwrite_print(f'{status} {lang_dir}/{cli.msgs_filename}{log.colors.nc}')

    return langs_translated, langs_skipped, langs_added, langs_not_translated
