import json, os, sys

with open(os.path.join(os.path.dirname(__file__), 'data_languages.json')) as file:
    data_languages = json.load(file)

sys.modules[__name__] = data_languages
