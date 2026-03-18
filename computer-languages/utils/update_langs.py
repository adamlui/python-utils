from pathlib import Path
from urllib.request import urlopen
import yaml

from lib import data, log

gh_lang_yml_filename = 'languages.yml'

log.info(f'Downloading {gh_lang_yml_filename}...')
resp_data = urlopen(
    f'https://raw.githubusercontent.com/github-linguist/linguist/main/lib/linguist/{gh_lang_yml_filename}'
).read().decode('utf-8')

log.info('Building language data...')
lang_data = {}
for lang_name, lang_info in yaml.safe_load(resp_data).items():
    if 'extensions' in lang_info:
        lang_data[lang_name] = {
            'type': lang_info.get('type', 'unknown'),
            'extensions': sorted(lang_info['extensions'], key=str.lower)
        }
lang_data = dict(sorted(lang_data.items(), key = lambda item: item[0].lower()))

output_path = Path(__file__).parent.parent / 'src/computer_languages/computer_languages.json'
log.info(f'Saving {len(lang_data)} languages to {output_path}...')
data.json.write(output_path, lang_data, style='compact')

log.success('Done!')
