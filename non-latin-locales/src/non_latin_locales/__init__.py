import json, os, sys

with open(os.path.join(os.path.dirname(__file__), 'non_latin-locales.json'), encoding='utf-8') as file:
    non_latin_locales = json.load(file)

sys.modules[__name__] = non_latin_locales
