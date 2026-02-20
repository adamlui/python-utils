from pathlib import Path
import sys

from .lib import data, init, log, wizard

def main():
    cli = init.cli()

    if cli.config.init : init.config_file(cli) ; sys.exit(0)
    if not cli.config.no_wizard : wizard.run(cli)

    log.info(f'{cli.msgs.log_SEARCHING_FOR} {cli.config.json_dir}...')
    init.json_dir(cli)
    if Path(cli.config.json_dir).exists():
        log.success(f'{cli.msgs.log_DIR_FOUND}!')
        print(f'\n>> {cli.config.json_dir}')
    else:
        log.warn(f'{cli.msgs.warn_DIR_NOT_FOUND}.')
        sys.exit(1)

    keys_removed, keys_skipped, files_processed_cnt = data.json.remove_keys(cli.config.json_dir, cli.config.keys)

    log.final_summary(cli.msgs, {
        'removed': [f'{key} ({file_path})' for key, file_path in keys_removed],
        'skipped': [f'{key} ({file_path})' for key, file_path in keys_skipped],
    })
    log.data(f'{cli.msgs.log_TOTAL_JSON_PROCESSED}: {files_processed_cnt}')

if __name__ == '__main__' : main()
