import sys

from . import data, log

def run(cli):

    while True: # prompt user for keys to remove

        if getattr(cli.config, 'keys', ''):
            print(f'\n{cli.msgs.log_KEYS_TO_REMOVE}:', cli.config.keys)
        input_keys = input(
            f'\n{log.colors.bw}{cli.msgs.prompt_KEYS_TO_REMOVE}: {log.colors.nc}')

        if not input_keys: # no keys entered
            if cli.config.keys : break # out of wizard
            user_resp = input(F'\n{cli.msgs.prompt_NO_KEYS_EXIT} (Y/n): ').lower()
            if user_resp == 'n' : continue # back to og prompt
            else : print(f'{cli.msgs.log_EXITING} {cli.name}...') ; sys.exit(0)

        new_keys = data.csv.parse(input_keys)
        existing_keys = set(cli.config.keys)
        truly_new_keys = []
        for key in new_keys:
            if key not in existing_keys and key not in truly_new_keys:
                truly_new_keys.append(key)

        if truly_new_keys:
            cli.config.keys.extend(truly_new_keys)
            print(f"{cli.msgs.log_ADDED}: {', '.join(truly_new_keys)}")
        else:
            print(f'{cli.msgs.log_NO_NEW_KEYS_ADDED}')
