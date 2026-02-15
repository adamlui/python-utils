def main():
    import os, sys
    from .lib import data, init, language, log

    cli = init.cli(__file__)
    if cli.config.init : init.config_file(cli) ; sys.exit(0)

    if not cli.config.no_wizard:
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

    log.info(f'Searching for {cli.config.locales_dir}...')
    cli.config.locales_dir = init.locales_dir(cli.config.locales_dir)
    if cli.config.locales_dir:
        log.success('Directory found!')
        print(f'\n>> {cli.config.locales_dir}')
    else:
        log.warn('Unable to locate directory.')
        sys.exit(1)

    cli.config.msgs_filename = 'messages.json'
    cli.config.en_msgs = data.json.read(os.path.join(cli.config.locales_dir, 'en', cli.config.msgs_filename))
    cli.config.target_langs = list(set(cli.config.target_langs)) # remove dupes

    if not cli.config.target_langs: # merge discovered locales w/ target_langs
        for root, dirs, _ in os.walk(cli.config.locales_dir):
            for lang_folder in dirs:
                msgs_path = os.path.join(root, lang_folder, cli.config.msgs_filename)
                discovered_lang = lang_folder.replace('_', '-')
                if os.path.exists(msgs_path) and discovered_lang not in cli.config.target_langs:
                    cli.config.target_langs.append(discovered_lang)
    cli.config.target_langs.sort()

    langs_translated, langs_skipped, langs_added, langs_not_translated = language.write_translations(cli)

    log.final_summary({
        'translated': langs_translated,
        'skipped': langs_skipped,
        'added': langs_added,
        'not translated': langs_not_translated,
    })

if __name__ == '__main__' : main()
