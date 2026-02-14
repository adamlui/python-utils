def main():
    import sys
    from .lib import data, init, log

    cli = init.cli()

    if not cli.config.no_wizard:
        while True: # prompt user for keys to remove
            if getattr(cli.config, 'keys', '') : print('\nKey(s) to remove:', cli.config.keys)
            input_key = input(f'\n{log.colors.bw}Enter key to remove (or ENTER if done): {log.colors.nc}')
            if not input_key : break
            cli.config.keys.append(input_key)

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
