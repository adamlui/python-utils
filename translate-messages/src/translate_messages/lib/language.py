import os, re, sys
from translate import Translator
from . import data, log

def create_translations(cli, target_msgs, lang_code):

    fail_flags = ['INVALID TARGET LANGUAGE', 'TOO MANY REQUESTS', 'MYMEMORY']
    src_keys = cli.config.keys or cli.en_msgs
    src_keys = [key for key in src_keys if key in cli.en_msgs]
    translated_msgs = {}

    for key in src_keys:

        if key in cli.config.exclude_keys:
            translated_msg = cli.en_msgs[key]['message']
            translated_msgs[key] = { 'message': translated_msg }
            continue

        if key not in target_msgs:
            original_msg = translated_msg = cli.en_msgs[key]['message']
            try:
                translator = Translator(provider='', to_lang=lang_code)
                translated_msg = re.sub(r'&(?:quot|#39);', "'", translator.translate(original_msg))
                if any(flag in translated_msg for flag in fail_flags):
                    translated_msg = original_msg
            except Exception as err:
                log.trunc(f'Translation failed for key "{key}" in {lang_code}/{cli.msgs_filename}: {err}')
                translated_msg = original_msg
            translated_msgs[key] = { 'message': translated_msg }

        else : translated_msgs[key] = target_msgs[key]
    
    return translated_msgs

def write_translations(cli):

    langs_added, langs_skipped, langs_translated, langs_not_translated = [], [], [], []
    for lang_code in cli.config.target_langs:
        lang_added, lang_skipped, lang_translated = False, False, False
        lang_folder = lang_code.replace('-', '_')

        if lang_code.startswith('en'): # skip EN locales
            print(f'\n{log.colors.gry}Skipped {lang_folder}/{cli.msgs_filename}...{log.colors.nc}', end='')
            langs_skipped.append(lang_code) ; langs_not_translated.append(lang_code) ; continue

        if '-' in lang_code: # cap suffix
            sep_idx = lang_folder.index('_')
            lang_folder = lang_folder[:sep_idx] + '_' + lang_folder[sep_idx+1:].upper()

        lang_folder_path = os.path.join(cli.config.locales_dir, lang_folder)
        if not os.path.exists(lang_folder_path): # create lang_folder if missing
            os.makedirs(lang_folder_path) ; langs_added.append(lang_code) ; lang_added = True
        msgs_path = os.path.join(lang_folder_path, cli.msgs_filename)
        msgs = data.json.read(msgs_path)

        log.info(f"{ 'Adding' if not msgs else 'Updating' } {lang_folder}/{cli.msgs_filename}...", end='')
        sys.stdout.flush()
        translated_msgs = create_translations(cli, msgs, lang_code)
        data.json.write(msgs_path, translated_msgs)

        if translated_msgs == msgs : langs_skipped.append(lang_code) ; lang_skipped = True
        elif translated_msgs != msgs : langs_translated.append(lang_code) ; lang_translated = True
        if not lang_translated : langs_not_translated.append(lang_code)
        status = (
            f'{log.colors.dg}Adde' if lang_added else
            f'{log.colors.gry}Skipped' if lang_skipped else
            f'{log.colors.dy}Updated'
        )
        log.overwrite_print(f'{status} {lang_folder}/{cli.msgs_filename}{log.colors.nc}')

    return langs_translated, langs_skipped, langs_added, langs_not_translated
