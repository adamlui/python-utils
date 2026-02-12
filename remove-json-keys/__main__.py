import sys
from lib import data, init, log

cli = init.cli()

while True: # prompt user for keys to remove
    if getattr(cli.config, 'remove_keys', '') : print('Key(s) to remove:', cli.config.remove_keys)
    input_key = input("Enter key to remove (or ENTER if done): ")
    if not input_key : break
    cli.config.remove_keys.append(input_key)

log.trunc(f'\nSearching for {cli.config.json_dir}...')
cli.config.json_dir = init.json_dir(cli.config.json_dir)
if cli.config.json_dir : log.trunc(f'JSON directory found!\n\n>> {cli.config.json_dir}\n')
else : log.trunc(f'Unable to locate a {cli.config.json_dir} directory.') ; sys.exit(1)

keys_removed, keys_skipped, files_processed_cnt = data.json.removeKeys(cli)

log.final_summary({
    'removed': [f'{key} ({file_path})' for key, file_path in keys_removed],
    'skipped': [f'{key} ({file_path})' for key, file_path in keys_skipped],
})
log.trunc(f'Total JSON files processed: {files_processed_cnt}\n')
