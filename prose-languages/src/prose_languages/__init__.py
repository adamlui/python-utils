import json, os, sys

with open(os.path.join(os.path.dirname(__file__), 'prose_languages.json')) as file:
    prose_languages = json.load(file)

sys.modules[__name__] = prose_languages
