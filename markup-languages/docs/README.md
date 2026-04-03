<a id="top"></a>

# > markup-languages

<a href="https://pepy.tech/projects/markup-languages?versions=*">
    <img height=31 src="https://img.shields.io/pepy/dt/markup-languages?logo=weightsandbiases&color=af68ff&logoColor=white&labelColor=464646&style=for-the-badge"></img></a>
<a href="https://github.com/adamlui/python-utils/releases/tag/markup-languages-1.0.3">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-1.0.3-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/markup-languages/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-f99b27.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=vulnerabilities&selected=adamlui_python-utils%3Amarkup-languages&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonar&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

> ### _File extensions for markup languages._

It's just a [JSON file](https://cdn.jsdelivr.net/gh/adamlui/python-utils@markup-languages-1.0.3/markup-languages/src/markup_languages/markup-languages.json), so you can use it in any environment. Sourced from GitHub's [Linguist](https://github.com/github-linguist/linguist) project (defines all 69 markup languages known to GitHub). Data is updated via script and released via new package version.

## Installation

```bash
pip install markup-languages
```

## Usage

```py
import markup_languages

html_lang_data = markup_languages['HTML']

print(html_lang_data['extensions']) # => ['.hta', '.htm', '.html', '.html.hl', ...]
```

_Note: Most type checkers will falsely warn_ `markup_languages` _is not subscriptable because they are incapable of analyzing runtime behavior (where the module is replaced w/ a dictionary for cleaner, direct access). You can safely suppress such warnings using_ `# type: ignore`.

## Examples

Get language from an extension:

```py
def get_lang(file_ext):
    for lang, data in markup_languages.items():
        if file_ext in data['extensions']:
            return lang

print(get_lang('.sss')) # => SugarSS
```

Get language from a file path:

```py
def get_lang_from_path(filepath):
    from pathlib import Path
    file_ext = Path(filepath).suffix
    for lang, data in markup_languages.items():
        if file_ext in data['extensions']:
            return lang

print(get_lang_from_path('index.html')) # => HTML
print(get_lang_from_path('style.css'))  # => CSS
print(get_lang_from_path('script.js'))  # => None (use programming-languages pkg)
```

## MIT License

Copyright © 2026 [Adam Lui](https://github.com/adamlui)

## Related

🇨🇳 [non-latin-locales](https://github.com/adamlui/python-utils/tree/main/non-latin-locales/#readme) - ISO 639-1 (2-letter) codes for non-Latin locales.
<br>#! [programming-languages](https://github.com/adamlui/python-utils/tree/main/programming-languages/#readme) - File extensions for programming languages.
<br>🏷️ [project-markers](https://github.com/adamlui/python-utils/tree/main/project-markers/#readme) - Common project root markers.

#

<picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/white/icon32x27.png"><img height=13 src="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/dark-gray/icon32x27.png"></picture> <a href=https://github.com/adamlui/python-utils/#readme>**More Python utilities**</a> /
<a href="#top">Back to top ↑</a>
