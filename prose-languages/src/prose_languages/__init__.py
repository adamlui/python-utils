import io, json, os, sys

with io.open(os.path.join(os.path.dirname(__file__), 'prose-languages.json'), encoding='utf-8') as file:
    prose_languages = json.load(file)

sys.modules[__name__] = prose_languages
