from pathlib import Path
import sys

from .lib import init, language, log, wizard

def main():
    cli = init.cli(__file__)

    if cli.config.init : init.config_file(cli) ; sys.exit(0)
    if not cli.config.no_wizard : wizard.run(cli)

    log.info(f'{cli.msgs.log_SEARCHING_FOR} {cli.config.locales_dir}...')
    init.locales_dir(cli)
    if Path(cli.config.locales_dir).exists():
        log.success(f'{cli.msgs.log_DIR_FOUND}!')
        print(f'\n>> {cli.config.locales_dir}')
    else:
        log.warn(f'{cli.msgs.warn_DIR_NOT_FOUND}.')
        sys.exit(1)

    init.src_msgs(cli)
    init.target_langs(cli)

    langs_translated, langs_skipped, langs_added, langs_not_translated = language.write_translations(cli)

    log.final_summary(cli.msgs, {
        'translated': langs_translated,
        'skipped': langs_skipped,
        'added': langs_added,
        'not translated': langs_not_translated,
    })

if __name__ == '__main__' : main()
