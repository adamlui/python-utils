from . import data, log

def run(cli):

    while True: # prompt user for keys to ignore

        if getattr(cli.config, 'exclude_keys', '') : print('\nIgnored key(s):', cli.config.exclude_keys)
        input_keys = input(
            f'\n{log.colors.bw}Enter key(s) to ignore (comma-separated, or ENTER if done): {log.colors.nc}')
        if not input_keys : break

        new_keys = data.csv.parse(input_keys)
        existing_keys = set(cli.config.exclude_keys)
        truly_new_keys = []
        for key in new_keys:
            if key not in existing_keys and key not in truly_new_keys:
                truly_new_keys.append(key)

        if truly_new_keys:
            cli.config.exclude_keys.extend(truly_new_keys)
            print(f"Added: {', '.join(truly_new_keys)}")
        else:
            print('No new keys added (all already present)')
