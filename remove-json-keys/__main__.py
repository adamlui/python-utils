import os, re
from lib import data, init, log

cli = init.cli()

print('')

# Prompt user for keys to remove
remove_keys = data.parse_csv_val(cli.args.remove_keys or '')
while True:
    if remove_keys : print('Key(s) to remove:', remove_keys)
    key = input("Enter key to remove (or ENTER if done): ")
    if not key : break
    remove_keys.append(key)

# Determine closest locales dir
log.trunc(f'\nSearching for {cli.json_dir}...')
cli.json_dir = init.json_dir(cli.json_dir)
if cli.json_dir : log.trunc(f'JSON directory found!\n\n>> {cli.json_dir}\n')
else : log.trunc(f'Unable to locate a {cli.json_dir} directory.') ; exit()

# Process JSON files and remove specified keys
keys_removed, keys_skipped, processed_cnt = [], [], 0
for root, _, files in os.walk(cli.json_dir):
    for filename in files:
        if filename.endswith('.json'):

            # Open found JSON file
            file_path = os.path.join(root, filename)
            with open(file_path, 'r', encoding='utf-8') as f : data = f.read()

            # Remove keys
            modified = False
            for key in remove_keys:
                re_key = fr'"{re.escape(key)}".*?[,\n]+.*?(?="|$)'
                data, count = re.subn(re_key, '', data)
                if count > 0:
                    keys_removed.append((key, os.path.relpath(file_path, cli.json_dir)))
                    modified = True
                else : keys_skipped.append((key, os.path.relpath(file_path, cli.json_dir)))
            if modified:
                with open(file_path, 'w', encoding='utf-8') as f : f.write(data)
            processed_cnt += 1

# Print file summaries
summary = {
    'removed': [f'{key} ({file_path})' for key, file_path in keys_removed],
    'skipped': [f'{key} ({file_path})' for key, file_path in keys_skipped],
}
log.final_summary(summary)
log.trunc(f'Total JSON files processed: {processed_cnt}\n')
