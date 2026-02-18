from pathlib import Path
import sys

from .lib import data, init, log, wizard

def main():
    cli = init.cli(__file__)

    if cli.config.init : init.config_file(cli) ; sys.exit(0)
    if not cli.config.no_wizard : wizard.run(cli)

    log.info(f'Searching for {cli.config.json_dir}...')
    init.json_dir(cli)
    if Path(cli.config.json_dir).exists():
        log.success('Directory found!')
        print(f'\n>> {cli.config.json_dir}')
    else:
        log.warn('Unable to locate directory!')
        sys.exit(1)

    keys_removed, keys_skipped, files_processed_cnt = data.json.remove_keys(cli.config.json_dir, cli.config.keys)

    log.final_summary({
        'removed': [f'{key} ({file_path})' for key, file_path in keys_removed],
        'skipped': [f'{key} ({file_path})' for key, file_path in keys_skipped],
    })
    log.data(f'Total JSON files processed: {files_processed_cnt}')

if __name__ == '__main__' : main()
