import time
from typing import List

PKGS = [
    'computer-languages',
    'data-languages',
    'find-project-root',
    'get-min-py',
    'is-legacy-terminal',
    'is-unicode-supported',
    'latin-locales',
    'markup-languages',
    'non-latin-locales',
    'programming-languages',
    'project-markers',
    'prose-languages',
    'remove-json-keys',
    'translate-messages'
]
STATS_API_URL = 'https://pypistats.org/api/packages/{pkg}/overall'

def format_total(num: int) -> str:  # abbr ints to e.g. 1.5k, 2b
    return f'{num / 1000000000:.1f}B' if num >= 1000000000 \
      else f'{num / 1000000:.1f}M' if num >= 1000000 \
      else f'{num / 1000:.1f}K' if num >= 1000 \
      else str(num)

def get_downloads(pkg: str, max_retries: int = 5, get_delay: int = 2) -> int:
    import json
    from urllib.request import urlopen
    from urllib.error import HTTPError
    url = STATS_API_URL.format(pkg=pkg)
    for idx in range(max_retries):
        try:
            with urlopen(url) as resp:
                return sum(item['downloads'] for item in json.load(resp)['data'])
        except HTTPError as err:
            if err.code == 429:  # Rate limited
                retry_delay = (idx +1) *2  # Exponential backoff
                print(f'{pkg}: Rate limited. Retrying in {retry_delay}s...')
                time.sleep(retry_delay)
            else:
                print(f'{pkg}: ERROR ({err.code})')
                return 0
        except Exception as err:
            print(f'{pkg}: Exception: {err}')
            time.sleep(get_delay)
    print(f'{pkg}: Failed after {max_retries} retries')
    return 0

def read_file(file_path: str) -> List[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def write_file(file_path: str, lines: List[str]) -> None:
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def update_downloads_shield(readme_path: str, downloads: int) -> None:
    import re
    lines = read_file(readme_path)
    shield_re = r'(<img[^>]+src="https://img.shields.io/badge/Downloads-)([\d\.kM]+)(-[a-f0-9]{6})'
    formatted_downloads = format_total(downloads)
    downloads_str = f'{formatted_downloads.lower()}'
    for idx, line in enumerate(lines):
        shield_match = re.search(shield_re, line)
        if shield_match:
            new_line = re.sub(shield_match.group(2), downloads_str, line)
            lines[idx] = new_line
            print(f'>>> {new_line.strip()}')
    write_file(readme_path, lines)

def main() -> None:
    grand_total_dls = 0
    for pkg in PKGS: # get downloads
        downloads = get_downloads(pkg)
        grand_total_dls += downloads
        print(f'{pkg:30} {downloads:,}')
        time.sleep(1)
    print('-' *45)
    print(f"{'TOTAL DOWNLOADS':20} {grand_total_dls:,}\n")
    README_PATH = 'docs/README.md'
    print(f'Updating {README_PATH}...')
    update_downloads_shield(README_PATH, grand_total_dls)
    print('Done!')

if __name__ == '__main__' : main()
