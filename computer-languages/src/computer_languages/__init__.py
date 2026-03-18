import json, os, sys

with open(os.path.join(os.path.dirname(__file__), 'computer_languages.json')) as file:
    computer_languages = json.load(file)

sys.modules[__name__] = computer_languages
