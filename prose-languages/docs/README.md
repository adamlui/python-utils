<a id="top"></a>

# > prose-languages

<a href="https://pepy.tech/projects/prose-languages?versions=*">
    <img height=31 src="https://img.shields.io/pepy/dt/prose-languages?logo=weightsandbiases&color=af68ff&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/releases/tag/prose-languages-1.0.3">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-1.0.3-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/prose-languages/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-f99b27.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=vulnerabilities&selected=adamlui_python-utils%3Aprose-languages&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%3Aprose-languages%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonar&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

> ### _File extensions for prose languages._

It's just a [JSON file](https://cdn.jsdelivr.net/gh/adamlui/python-utils@prose-languages-1.0.3/prose-languages/src/prose_languages/prose-languages.json), so you can use it in any environment. Sourced from GitHub's [Linguist](https://github.com/github-linguist/linguist) project (defines all 18 prose languages known to GitHub). Data is updated via script and released via new package version.

## Installation

```bash
pip install prose-languages
```

## Usage

```py
import prose_languages

md_lang_data = prose_languages['Markdown']

print(md_lang_data['extensions']) # => ['.livemd', '.markdown', '.md', ...]
```

_Note: Most type checkers will falsely warn_ `prose_languages` _is not subscriptable because they are incapable of analyzing runtime behavior (where the module is replaced w/ a dictionary for cleaner, direct access). You can safely suppress such warnings using_ `# type: ignore`.

## Examples

Get language from an extension:

```py
def get_lang(file_ext):
    for lang, data in prose_languages.items():
        if file_ext in data['extensions']:
            return lang

print(get_lang('.gmi')) # => Gemini
```

Get language from a file path:

```py
def get_lang_from_path(filepath):
    from pathlib import Path
    file_ext = Path(filepath).suffix
    for lang, data in prose_languages.items():
        if file_ext in data['extensions']:
            return lang

print(get_lang_from_path('document.adoc')) # => AsciiDoc
print(get_lang_from_path('README.md')) # => Markdown
print(get_lang_from_path('index.mdx')) # => None (use markup-languages pkg)
```

## MIT License

Copyright © 2026 [Adam Lui](https://github.com/adamlui)

## Related

</> [markup-languages](https://github.com/adamlui/python-utils/tree/main/markup-languages/#readme) - File extensions for markup languages.
<br>#! [programming-languages](https://github.com/adamlui/python-utils/tree/main/programming-languages/#readme) - File extensions for programming languages.
<br>{ } [data-languages](https://github.com/adamlui/python-utils/tree/main/data-languages/#readme) - File extensions for data languages.

#

<picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/white/icon32x27.png"><img height=13 src="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/dark-gray/icon32x27.png"></picture> <a href=https://github.com/adamlui/python-utils/#readme>**More Python utilities**</a> /
<a href="https://github.com/adamlui/python-utils/discussions">Discuss</a> /
<a href="https://github.com/adamlui/python-utils/issues">Report bug</a> /
<a href="mailto:security@tidelift.com">Report vulnerability</a> /
<a href="#top">Back to top ↑</a>
