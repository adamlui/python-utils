from . import data, log

def run(cli):

    while True: # prompt user for keys to ignore

        if getattr(cli.config, 'exclude_keys', ''):
            print(f'\n{cli.msgs.log_IGNORED_KEYS}:', cli.config.exclude_keys)
        input_keys = input(
            f'\n{log.colors.bw}{cli.msgs.prompt_KEYS_TO_IGNORE}: {log.colors.nc}')
        if not input_keys : break

        new_keys = data.csv.parse(input_keys)
        existing_keys = set(cli.config.exclude_keys)
        truly_new_keys = []
        for key in new_keys:
            if key not in existing_keys and key not in truly_new_keys:
                truly_new_keys.append(key)

        if truly_new_keys:
            cli.config.exclude_keys.extend(truly_new_keys)
            print(f"{cli.msgs.log_ADDED}: {', '.join(truly_new_keys)}")
        else:
            print(cli.msgs.log_NO_NEW_KEYS_ADDED)
