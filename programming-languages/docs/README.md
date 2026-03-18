<a id="top"></a>

# > programming-languages

<a href="https://github.com/adamlui/python-utils/releases/tag/programming-languages-1.0.0">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-1.0.0-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/programming-languages/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-f99b27.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=new_vulnerabilities&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonarcloud&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

> ### _File extensions for programming languages._

It's just a [JSON file](https://github.com/adamlui/python-utils/blob/programming-languages-1.0.0/programming-languages/src/programming_languages/programming_languages.json), so you can use it in any environment. Sourced from GitHub's [Linguist](https://github.com/github-linguist/linguist) project (defines all 500+ programming languages known to GitHub). Data is updated via script and released via new package version.

## Installation

```bash
pip install programming-languages
```

## Usage

```py
import programming_languages

py_lang_data = programming_languages['Python']

print(py_lang_data['extensions']) # => ['.cgi', '.fcgi', '.gyp', ...]
```

_Note: Most type checkers will falsely warn_ `programming_languages` _is not subscriptable because they are incapable of analyzing runtime behavior (where the module is replaced w/ a dictionary for cleaner, direct access). You can safely suppress such warnings using_ `# type: ignore`.

## Examples

Get language from an extension:

```py
def get_lang(file_ext):
    for lang, data in programming_languages.items():
        if file_ext in data['extensions']:
            return lang

print(get_lang('.al')) # => 'AL'
```

Get language from a file path:

```py
def get_lang_from_path(filepath):
    from pathlib import Path
    file_ext = Path(filepath).suffix
    for lang, data in programming_languages.items():
        if file_ext in data['extensions']:
            return lang

print(get_lang_from_path('main.rs')) # => 'Rust'
print(get_lang_from_path('script.kt')) # => 'Kotlin'
print(get_lang_from_path('data.avsc')) # => None (use data-languages pkg)
```

## MIT License

Copyright © 2026 [Adam Lui](https://github.com/adamlui).

## Related

</> [markup-languages](https://github.com/adamlui/python-utils/tree/main/markup-languages/#readme) - File extensions for markup languages.
<br>## [prose-languages](https://github.com/adamlui/python-utils/tree/main/prose-languages/#readme) - File extensions for prose languages.
<br>{ } [data-languages](https://github.com/adamlui/python-utils/tree/main/data-languages/#readme) - File extensions for data languages.

#

<a href="#top">Back to top ↑</a>
