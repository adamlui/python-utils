import json, os, sys

with open(os.path.join(os.path.dirname(__file__), 'latin_locales.json')) as file:
    latin_locales = json.load(file)

sys.modules[__name__] = latin_locales
