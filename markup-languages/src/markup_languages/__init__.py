import json, os, sys

with open(os.path.join(os.path.dirname(__file__), 'markup_languages.json')) as file:
    markup_languages = json.load(file)

sys.modules[__name__] = markup_languages
