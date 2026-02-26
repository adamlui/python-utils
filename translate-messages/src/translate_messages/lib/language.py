from pathlib import Path
import re, sys
from types import SimpleNamespace as sn

from translate import Translator

from . import data, log

def create_translations(cli, target_msgs, lang_code):

    fail_flags = ['INVALID TARGET LANGUAGE', 'MYMEMORY']
    src_keys = cli.config.keys or cli.en_msgs
    src_keys = [key for key in src_keys if key in cli.en_msgs]
    translated_msgs = {}

    for key in src_keys:

        if key in cli.config.exclude_keys:
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
                if 'TOO MANY REQUESTS' in str(err).upper() : log.tip(f'{cli.msgs.tip_USE_A_VPN}.') ; exit(1)
                translated_msg = original_msg
            translated_msgs[key] = { 'message': translated_msg }
        else:
            translated_msgs[key] = target_msgs[key]

    return translated_msgs

def get_msgs():
    msgs_path = Path(__file__).parent.parent / 'assets/data/messages.json'
    return sn(**{ key:val['message'] for key,val in data.json.read(msgs_path).items() })

def write_translations(cli):

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
