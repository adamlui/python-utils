# > latin-locales

<a href="https://github.com/adamlui/python-utils/releases/tag/latin-locales-1.0.0">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-1.0.0-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/latin-locales/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-f99b27.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=new_vulnerabilities&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonarcloud&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

> ### _ISO 639-1 (2-letter) codes for Latin locales that don't require advanced Unicode support._

It's just a [JSON file](https://github.com/adamlui/python-utils/blob/latin-locales-1.0.0/latin-locales/src/latin_locales/latin_locales.json), so you can use it in any environment.

## Installation

```bash
pip install latin-locales
```

## Usage

```py
import latin_locales

print(latin_locales)
# => ['aa', 'ae', 'af', 'ak', 'an', 'ay', 'bi', 'bm', 'br', ...]
```

_Note: Most type checkers will falsely warn_ `latin_locales` _is not iterable because they are incapable of analyzing runtime behavior (where the module is replaced w/ a list for cleaner, direct access). You can safely suppress such warnings using_ `# type: ignore`.

## MIT License

Copyright © 2026 [Adam Lui](https://github.com/adamlui).
