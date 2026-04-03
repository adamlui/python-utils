import io, json, os, sys

with io.open(os.path.join(os.path.dirname(__file__), 'data-languages.json'), encoding='utf-8') as file:
    data_languages = json.load(file)

sys.modules[__name__] = data_languages
