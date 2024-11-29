'''
Script:       remove-json-keys.py
Version:      2023.9.21
Description:  Remove key/value pairs from json_folder/**.json
Author:       Adam Lui
URL:          https://github.com/adamlui/python-utils
'''

import os
import re

json_folder = '_locales'

# UI initializations
os.system('color')
print('\033[0;92m')  # set font to bright green
terminal_width = os.get_terminal_size()[0]

def print_trunc(msg):
    print(msg if len(msg) < terminal_width else msg[:terminal_width - 4] + '...')

print('')

# Prompt user for keys to remove
keys_to_remove = []
while True:
    key = input("Enter key to remove (or ENTER if done): ")
    if not key:
        break
    keys_to_remove.append(re.escape(key))  # Escape keys for regex

# Determine closest JSON dir
print_trunc(f'Searching for {json_folder}...')
script_dir = os.path.abspath(os.path.dirname(__file__))
json_dir = None

# Search for the JSON directory in the script and its parent directories
for root, dirs, files in os.walk(script_dir):
    if json_folder in dirs:
        json_dir = os.path.join(root, json_folder)
        break

if not json_dir:  # If not found, search parent directories
    parent_dir = os.path.dirname(script_dir)
    while parent_dir and parent_dir != script_dir:
        for root, dirs, files in os.walk(parent_dir):
            if json_folder in dirs:
                json_dir = os.path.join(root, json_folder)
                break
        if json_dir:
            break
        parent_dir = os.path.dirname(parent_dir)

# Print result
if json_dir:
    print_trunc(f'JSON directory found!\n\n>> {json_dir}\n')
else:
    print_trunc(f'Unable to locate a {json_folder} directory.')
    exit()

# Process JSON files and remove specified keys
keys_removed, keys_skipped, processed_count = [], [], 0
key_patterns = [fr'"{key}".*?[,\n]+.*?(?="|$)' for key in keys_to_remove]  # Precompile regex patterns

for root, _, files in os.walk(json_dir):
    for filename in files:
        if filename.endswith('.json'):
            file_path = os.path.join(root, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = f.read()

            modified = False
            for key, pattern in zip(keys_to_remove, key_patterns):
                data, count = re.subn(pattern, '', data)
                if count > 0:
                    keys_removed.append((key, os.path.relpath(file_path, json_dir)))
                    modified = True
                else:
                    keys_skipped.append((key, os.path.relpath(file_path, json_dir)))

            if modified:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(data)
            processed_count += 1

# Print file summaries
if keys_removed:
    print_trunc('\nKeys removed successfully!\n')
    for key, file_path in keys_removed:
        print(f'Removed key "{key}" in {file_path}')
if keys_skipped:
    print_trunc('\nKeys skipped (not found)!\n')
    for key, file_path in keys_skipped:
        print(f'Skipped key "{key}" in {file_path}')

# Print final summary
print_trunc('\nKey removal process completed!\n')
print(f'Processed JSON Files: {processed_count}')
print(f'Keys Removed: {len(keys_removed)}')
print(f'Keys Skipped: {len(keys_skipped)}')
