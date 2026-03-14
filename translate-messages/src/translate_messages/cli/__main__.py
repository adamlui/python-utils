from pathlib import Path
import sys

from .lib import init, language, log, settings, wizard

def main():
    cli = init.cli()

    # Process early-exit args (e.g. init, --version)
    for ctrl_name, ctrl in vars(settings.controls).items():
        if getattr(ctrl, 'exit', False) and getattr(cli.config, ctrl_name, False):
            if hasattr(ctrl, 'handler') : ctrl.handler(cli)
            sys.exit(0)

    if not cli.config.no_wizard : wizard.run(cli)

    log.info(f'{cli.msgs.log_SEARCHING_FOR} {cli.config.locales_dir}...')
    init.locales_path(cli)
    if Path(cli.locales_path).exists():
        log.success(f'{cli.msgs.log_DIR_FOUND}!')
        print(f'\n>> {cli.locales_path}')
    else:
        log.warn(f'{cli.msgs.warn_DIR_NOT_FOUND}.')
        sys.exit(1)

    init.src_msgs(cli)
    init.target_langs(cli)

    langs_translated, langs_skipped, langs_added, langs_not_translated = language.write_translations(cli)

    log.final_summary(cli.msgs, {
        cli.msgs.log_TRANSLATED.lower(): langs_translated,
        cli.msgs.log_SKIPPED.lower(): langs_skipped,
        cli.msgs.log_ADDED.lower(): langs_added,
        cli.msgs.log_NOT_TRANSLATED.lower(): langs_not_translated,
    })

if __name__ == '__main__' : main()
