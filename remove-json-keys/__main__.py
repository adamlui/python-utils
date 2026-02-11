from lib import data, init, log

cli = init.cli()

cli.remove_keys = data.csv.parse(cli.args.remove_keys or '')
print('')
while True: # prompt user for keys to remove
    if cli.remove_keys : print('Key(s) to remove:', cli.remove_keys)
    key = input("Enter key to remove (or ENTER if done): ")
    if not key : break
    cli.remove_keys.append(key)

log.trunc(f'\nSearching for {cli.json_dir}...')
cli.json_dir = init.json_dir(cli.json_dir)
if cli.json_dir : log.trunc(f'JSON directory found!\n\n>> {cli.json_dir}\n')
else : log.trunc(f'Unable to locate a {cli.json_dir} directory.') ; exit()

keys_removed, keys_skipped, processed_cnt = data.json.removeKeys(cli)

summary = {
    'removed': [f'{key} ({file_path})' for key, file_path in keys_removed],
    'skipped': [f'{key} ({file_path})' for key, file_path in keys_skipped],
}
log.final_summary(summary)
log.trunc(f'Total JSON files processed: {processed_cnt}\n')
