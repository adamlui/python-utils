PKGS = [
    'ai-personas',
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
    'sys-lang',
    'translate-messages'
]
README_PATH = 'docs/README.md'
STATS_API_URL = 'https://pypistats.org/api/packages/{pkg}/overall'

def get_downloads(pkg: str, max_retries: int = 5, get_delay: int = 1) -> int:
    import json
    from time import sleep
    from urllib.request import urlopen
    from urllib.error import HTTPError

    url = STATS_API_URL.format(pkg=pkg)

    for idx in range(max_retries):
        try:
            with urlopen(url) as resp:
                result = sum(item['downloads'] for item in json.load(resp)['data'])
            sleep(get_delay)
            return result
        except Exception as err:
            retry_delay = (idx +1) * get_delay
            if isinstance(err, HTTPError):
                if err.code == 429:
                    print(f'! {pkg}: Rate limited. Retrying in {retry_delay}s...')
                else:
                    print(f'{pkg}: HTTP ERROR ({err.code}). Retrying in {retry_delay}s...')
            else:
                print(f'{pkg}: Exception: {err}. Retrying in {retry_delay}s...')
            sleep(retry_delay)

    print(f'{pkg}: Failed after {max_retries} retries')
    return 0

def format_total(num: int) -> str:
    first_digit = str(num)[0] if num else '0'
    second_digit = str(num)[1] if num > 9 else '0'
    second_digit_rounded = '0' if int(second_digit) < 5 else '5'
    if num >= 1_000_000_000:
        formatted = f'{num // 1_000_000_000}'
        remainder = (num % 1_000_000_000) // 100_000_000
        if remainder : formatted += f'.{remainder}'
        return formatted + 'B+'
    elif num >= 10_000_000:
        return f'{(num // 1_000_000) * 1_000_000:,}+'
    elif num >= 1_000_000:
        return f'{first_digit},{second_digit}00,000+'
    elif num >= 100_000:
        return f'{first_digit}{second_digit_rounded}0,000+'
    elif num >= 10_000:
        return f'{first_digit}0,000+'
    elif num >= 1_000:
        formatted = f'{num // 1000}'
        remainder = (num % 1000) // 100
        if remainder : formatted += f'.{remainder}'
        return formatted + 'K'
    else:
        return str(num)

def read_file(file_path: str) -> list[str]:
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def write_file(file_path: str, lines: list[str]) -> None:
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(lines)

def update_downloads_shield(readme_path: str, downloads: int) -> None:
    import re
    lines = read_file(readme_path)
    shield_re = r'(?i)(<img[^>]+src="https://img.shields.io/badge/Downloads-)([\d,\.km]+)(-[a-f\d]{6})'
    downloads_str = f'{format_total(downloads).lower()}'
    for idx, line in enumerate(lines):
        shield_match = re.search(shield_re, line)
        if shield_match:
            new_line = re.sub(shield_match.group(2), downloads_str, line)
            lines[idx] = new_line
            print(f'»»» {new_line.strip()}\n')
    write_file(readme_path, lines)

def main() -> None:
    grand_total_dls = 0
    for pkg in PKGS: # get downloads
        downloads = get_downloads(pkg)
        grand_total_dls += downloads
        print(f'{pkg:30} {downloads:,}')
    print('-' *45)
    print(f"{'TOTAL DOWNLOADS':30} {grand_total_dls:,}\n")
    print(f'Updating {README_PATH}...\n')
    update_downloads_shield(README_PATH, grand_total_dls)
    print('Done!')

if __name__ == '__main__' : main()
