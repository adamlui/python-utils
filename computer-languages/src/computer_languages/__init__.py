import io, json, os, sys

with io.open(os.path.join(os.path.dirname(__file__), 'computer-languages.json'), encoding='utf-8') as file:
    computer_languages = json.load(file)

sys.modules[__name__] = computer_languages
