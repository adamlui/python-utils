import os
import json
from sys import stdout
from translate import Translator

locales_folder = '_locales'
target_langs = [
    'af', 'am', 'ar', 'az', 'be', 'bem', 'bg', 'bn', 'bo', 'bs', 'ca', 'ceb', 'cs', 'cy', 'da', 'de', 'dv', 'dz', 'el',
    'en', 'en-GB', 'eo', 'es', 'et', 'eu', 'fa', 'fi', 'fo', 'fr', 'gd', 'gl', 'gu', 'haw', 'he', 'hi', 'hr', 'ht',
    'hu', 'hy', 'id', 'is', 'it', 'ja', 'ka', 'kab', 'kk', 'km', 'kn', 'ko', 'ku', 'ky', 'la', 'lb', 'lo', 'lt', 'lv',
    'mg', 'mi', 'mk', 'ml', 'mn', 'ms', 'mt', 'my', 'ne', 'nl', 'no', 'ny', 'pa', 'pap', 'pl', 'ps', 'pt', 'ro', 'ru',
    'rw', 'sg', 'si', 'sk', 'sl', 'sm', 'sn', 'so', 'sr', 'sv', 'sw', 'ta', 'te', 'tg', 'th', 'ti', 'tk', 'tn', 'to',
    'tpi', 'tr', 'uk', 'ur', 'uz', 'vi', 'xh', 'yi', 'zh', 'zh-CN', 'zh-HK', 'zh-SG', 'zh-TW', 'zu'
]

# UI initializations
terminal_width = os.get_terminal_size()[0]

def print_trunc(msg, end='\n'):
    print(msg if len(msg) < terminal_width else msg[:terminal_width-4] + '...', end=end)

def overwrite_print(msg):
    stdout.write('\r' + msg.ljust(terminal_width)[:terminal_width])

print('')

# Prompt user for keys to ignore
keys_to_ignore = []
while True:
    key = input('Enter key to ignore (or ENTER if done): ')
    if not key:
        break
    keys_to_ignore.append(key)

# Determine closest locales dir
print_trunc(f'\nSearching for {locales_folder}...')
script_dir = os.path.abspath(os.path.dirname(__file__))
locales_dir = None

# Use a single function to find the locales directory
def find_locales_directory(start_dir):
    for root, dirs, _ in os.walk(start_dir):
        if locales_folder in dirs:
            return os.path.join(root, locales_folder)
    return None

locales_dir = find_locales_directory(script_dir) or find_locales_directory(os.path.dirname(script_dir))

# Print result
if locales_dir:
    print_trunc(f'_locales directory found!\n\n>> {locales_dir}\n')
else:
    print_trunc(f'Unable to locate a {locales_folder} directory.')
    exit()

# Load en/messages.json
en_msgs_path = os.path.join(locales_dir, 'en', 'messages.json')
with open(en_msgs_path, 'r', encoding='utf-8') as en_file:
    en_messages = json.load(en_file)

# Combine target_langs with languages discovered in _locales
output_langs = set(target_langs)  # Use a set to avoid duplicates
for root, dirs, _ in os.walk(locales_dir):
    for folder in dirs:
        discovered_lang = folder.replace('_', '-')
        if discovered_lang not in output_langs:
            msgs_path = os.path.join(root, folder, 'messages.json')
            if os.path.exists(msgs_path):
                output_langs.add(discovered_lang)

output_langs = sorted(output_langs)  # Sort the languages

# Create/update/translate messages
langs_added, langs_skipped, langs_translated, langs_not_translated = [], [], [], []

for lang_code in output_langs:
    if lang_code.startswith('en'):
        print_trunc(f'Skipped {lang_code.replace("-", "_")}/messages.json...')
        langs_skipped.append(lang_code)
        langs_not_translated.append(lang_code)
        continue

    folder = lang_code.replace('-', '_')
    folder_path = os.path.join(locales_dir, folder)
    os.makedirs(folder_path, exist_ok=True)  # Create folder if it doesn't exist
    msgs_path = os.path.join(folder_path, 'messages.json')

    # Load existing messages or initialize an empty dict
    messages = {}
    if os.path.exists(msgs_path):
        with open(msgs_path, 'r', encoding='utf-8') as messages_file:
            messages = json.load(messages_file)

    translated_msgs = {}
    print_trunc(f"{ 'Adding' if not messages else 'Updating' } {folder}/messages.json...", end='')
    stdout.flush()

    for key, value in en_messages.items():
        if key in keys_to_ignore:
            translated_msgs[key] = value
            continue

        original_msg = value['message']
        if key not in messages:
            try:
                translator = Translator(to_lang=lang_code)
                translated_msg = translator.translate(original_msg).replace('&quot;', "'").replace('&#39;', "'")
                if any(flag in translated_msg for flag in ['INVALID TARGET LANGUAGE', 'TOO MANY REQUESTS', 'MYMEMORY']):
                    translated_msg = original_msg
            except Exception as e:
                print_trunc(f'Translation failed for key "{key}" in {lang_code}/messages.json: {e}')
                translated_msg = original_msg
            translated_msgs[key] = {'message': translated_msg}
        else:
            translated_msgs[key] = messages[key]

    # Write the translated messages to the file
    with open(msgs_path, 'w', encoding='utf-8') as output_file:
        json.dump(translated_msgs, output_file, ensure_ascii=False, indent=2)

    # Update language status
    if translated_msgs == messages:
        langs_skipped.append(lang_code)
    else:
        langs_translated.append(lang_code)

    overwrite_print(f"{ 'Added' if lang_code not in langs_skipped else 'Skipped' } {folder}/messages.json")

# Print final summary
print_trunc('\nAll messages.json files updated successfully!\n')
for lang_list, status in zip([langs_translated, langs_skipped, langs_added, langs_not_translated], 
                              ['translated', 'skipped', 'added', 'not translated']):
    if lang_list:
        print(f'Languages {status}: {len(lang_list)}\n[ {", ".join(lang_list)} ]\n')
