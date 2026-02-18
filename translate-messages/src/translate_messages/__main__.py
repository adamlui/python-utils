def main():
    import sys
    from pathlib import Path
    from .lib import data, init, language, log, wizard

    cli = init.cli(__file__)

    if cli.config.init:
        init.config_file(cli)
        sys.exit(0)
    if not cli.config.no_wizard:
        wizard.run(cli)

    log.info(f'Searching for {cli.config.locales_dir}...')
    init.locales_dir(cli)

    if Path(cli.config.locales_dir).exists():
        log.success('Directory found!')
        print(f'\n>> {cli.config.locales_dir}')
    else:
        log.warn('Unable to locate directory.')
        sys.exit(1)

    cli.msgs_filename = 'messages.json'
    cli.locales_path = Path(cli.config.locales_dir)
    cli.en_path = cli.locales_path / 'en' / cli.msgs_filename
    if not cli.en_path.exists():
        log.error(f'English locale not found at {cli.en_path}.')
        log.tip(f'Make sure {cli.en_path} exists!')
        sys.exit(1)
    try:
        cli.en_msgs = data.json.read(cli.en_path)
    except Exception as err:
        log.error(f'Failed to parse {cli.en_path}: {err}')
        log.tip('Make sure it contains valid JSON')
        sys.exit(1)

    cli.config.target_langs = list(set(cli.config.target_langs)) # remove dupes

    if not cli.config.target_langs:
        cli.config.target_langs = cli.supported_locales
        for lang_path in cli.locales_path.rglob(f'*/{cli.msgs_filename}'): # merge discovered locales
            discovered_lang = lang_path.parent.name.replace('_', '-')
            if discovered_lang not in cli.config.target_langs:
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
