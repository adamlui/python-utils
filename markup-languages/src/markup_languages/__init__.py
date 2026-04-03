import io, json, os, sys

with io.open(os.path.join(os.path.dirname(__file__), 'markup-languages.json'), encoding='utf-8') as file:
    markup_languages = json.load(file)

sys.modules[__name__] = markup_languages
