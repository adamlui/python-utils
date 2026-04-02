import json, os, sys

with open(os.path.join(os.path.dirname(__file__), 'programming-languages.json'), encoding='utf-8') as file:
    programming_languages = json.load(file)

sys.modules[__name__] = programming_languages
