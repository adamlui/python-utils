def main():
    import sys
    from pathlib import Path

    from .lib import init, language, log, wizard

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

    init.src_msgs(cli)
    init.target_langs(cli)

    langs_translated, langs_skipped, langs_added, langs_not_translated = language.write_translations(cli)

    log.final_summary({
        'translated': langs_translated,
        'skipped': langs_skipped,
        'added': langs_added,
        'not translated': langs_not_translated,
    })

if __name__ == '__main__' : main()
