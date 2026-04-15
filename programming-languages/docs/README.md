<a id="top"></a>

# > programming-languages

<a href="https://pepy.tech/projects/programming-languages?versions=*">
    <img height=31 src="https://img.shields.io/pepy/dt/programming-languages?logo=weightsandbiases&color=af68ff&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/releases/tag/programming-languages-2.0.3">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-2.0.3-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/programming-languages/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-f99b27.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=vulnerabilities&selected=adamlui_python-utils%3Aprogramming-languages&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%3Aprogramming-languages%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonar&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

> ### _File extensions for programming languages._

It's just a [JSON file](https://cdn.jsdelivr.net/gh/adamlui/python-utils@programming-languages-2.0.3/programming-languages/src/programming_languages/programming-languages.json), so you can use it in any environment. Sourced from GitHub's [Linguist](https://github.com/github-linguist/linguist) project (defines all 500+ programming languages known to GitHub). Data is updated via script and released via new package version.

<hr>

## Installation

```bash
pip install programming-languages
```

<hr>

## Usage

```py
import programming_languages

py_lang_data = programming_languages['Python']

print(py_lang_data['extensions']) # => ['.cgi', '.fcgi', '.gyp', ...]
```

_Note: Most type checkers will falsely warn_ `programming_languages` _is not subscriptable because they are incapable of analyzing runtime behavior (where the module is replaced w/ a dictionary for cleaner, direct access). You can safely suppress such warnings using_ `# type: ignore`.

<hr>

## Examples

Get language from an extension:

```py
def get_lang(file_ext):
    for lang, data in programming_languages.items():
        if file_ext in data['extensions']:
            return lang

print(get_lang('.al')) # => AL
```

Get language from a file path:

```py
def get_lang_from_path(filepath):
    from pathlib import Path
    file_ext = Path(filepath).suffix
    for lang, data in programming_languages.items():
        if file_ext in data['extensions']:
            return lang

print(get_lang_from_path('main.rs')) # => Rust
print(get_lang_from_path('script.kt')) # => Kotlin
print(get_lang_from_path('data.avsc')) # => None (use data-languages pkg)
```

<hr>

## MIT License

Copyright © 2026 [Adam Lui](https://github.com/adamlui)

<hr>

## Related

</> [markup-languages](https://github.com/adamlui/python-utils/tree/main/markup-languages/#readme) - File extensions for markup languages.
<br>## [prose-languages](https://github.com/adamlui/python-utils/tree/main/prose-languages/#readme) - File extensions for prose languages.
<br>{ } [data-languages](https://github.com/adamlui/python-utils/tree/main/data-languages/#readme) - File extensions for data languages.

<a href="#"><img style="height:10px ; width:100%" src="https://cdn.jsdelivr.net/gh/adamlui/python-utils@b8b2932/assets/images/separators/aqua-gradient.png"></a>

<picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/white/icon32x27.png"><img height=13 src="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/dark-gray/icon32x27.png"></picture> <a href=https://github.com/adamlui/python-utils/#readme>**More Python utilities**</a> /
<a href="https://github.com/adamlui/python-utils/discussions">Discuss</a> /
<a href="https://github.com/adamlui/python-utils/issues">Report bug</a> /
<a href="mailto:security@tidelift.com">Report vulnerability</a> /
<a href="#top">Back to top ↑</a>
