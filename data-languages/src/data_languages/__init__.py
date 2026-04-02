import json, os, sys

with open(os.path.join(os.path.dirname(__file__), 'data_languages.json'), encoding='utf-8') as file:
    data_languages = json.load(file)

sys.modules[__name__] = data_languages
