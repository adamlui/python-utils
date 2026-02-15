def main():
    import sys
    from .lib import data, init, log

    cli = init.cli()

    if not cli.config.no_wizard:
        while True: # prompt user for keys to remove
            if getattr(cli.config, 'keys', '') : print('\nCurrent keys to remove:', cli.config.keys)
            input_keys = input(
                f'\n{log.colors.bw}Enter key(s) to remove (comma-separated, or ENTER if done): {log.colors.nc}')
            if not input_keys : break
            new_keys = data.csv.parse(input_keys)
            existing_keys = set(cli.config.keys)
            truly_new_keys = []
            for key in new_keys:
                if key not in existing_keys and key not in truly_new_keys:
                    truly_new_keys.append(key)
            if truly_new_keys:
                cli.config.keys.extend(truly_new_keys)
                print(f"Added: {', '.join(truly_new_keys)}")
            else:
                print('No new keys added (all already present)')

    log.info(f'Searching for {cli.config.json_dir}...')
    cli.config.json_dir = init.json_dir(cli.config.json_dir)
    if cli.config.json_dir:
        log.success('Directory found!')
        print(f'\n>> {cli.config.json_dir}')
    else:
        log.warn('Unable to locate directory.')
        sys.exit(1)

    keys_removed, keys_skipped, files_processed_cnt = data.json.remove_keys(cli)

    log.final_summary({
        'removed': [f'{key} ({file_path})' for key, file_path in keys_removed],
        'skipped': [f'{key} ({file_path})' for key, file_path in keys_skipped],
    })
    log.data(f'Total JSON files processed: {files_processed_cnt}')

if __name__ == '__main__' : main()
