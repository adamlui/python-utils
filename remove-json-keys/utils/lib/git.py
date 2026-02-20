from pathlib import Path
import sys, subprocess, os

sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))
from translate_messages.lib import log # type: ignore

def commit(files, msg) : run('add', *files) ; run('commit', '-n', '-m', msg)

def init_kudo_sync_bot(msgs):
    log.info(f'{msgs.log_SWITCHING_TO_KUDO_SYNC_BOT}...\n')
    with open(Path.home() / '.gitconfig.backup', 'w') as file: # back up git config
        file.write(run('config', '--global', '--list'))
    gpg_keys_path = os.environ.get('GPG_KEYS_PATH')
    if gpg_keys_path:
        key_path = Path(gpg_keys_path) / 'kudo-sync-bot-private-key.asc'
        if key_path.exists() : subprocess.run(['gpg', '--batch', '--import', str(key_path)], check=True)
        key_id_path = Path(gpg_keys_path) / 'kudo-sync-bot-key-id.txt'
        if key_id_path.exists():
            key_id = key_id_path.read_text().strip()
            run('config', '--global', 'user.signingkey', key_id)
    run('config', '--global', 'commit.gpgsign', 'true')
    run('config', '--global', 'user.name', 'kudo-sync-bot')
    run('config', '--global', 'user.email', 'auto-sync@kudoai.com')
    return True

def push() : run('push')

def restore_og_config(msgs):
    log.info(f'{msgs.log_RESTORING_OG_GIT_CONFIG}...')
    backup_path = Path.home() / '.gitconfig.backup'
    if backup_path.exists():
        with open(backup_path) as file:
            for line in file:
                if '=' in line:
                    key, val = line.strip().split('=', 1)
                    run('config', '--global', key, val)
        backup_path.unlink()
    else:
        log.warn(msgs.warn_GIT_CONFIG_BACKUP_NOT_FOUND)

def run(*args):
    result = subprocess.run(['git'] + list(args), capture_output=True, text=True)
    if result.returncode != 0:
        log.error(f"Git command failed: {' '.join(['git'] + list(args))}")
        log.error(result.stderr)
        sys.exit(1)
    return result.stdout.strip()
