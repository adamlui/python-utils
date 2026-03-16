import json, os, sys

with open(os.path.join(os.path.dirname(__file__), 'languages.json')) as file:
    programming_languages = json.load(file)

sys.modules[__name__] = programming_languages
