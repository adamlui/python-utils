# > latin-locales

<a href="https://pepy.tech/projects/latin-locales?versions=*">
    <img height=31 src="https://img.shields.io/pepy/dt/latin-locales?logo=weightsandbiases&color=af68ff&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/releases/tag/latin-locales-1.0.4">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-1.0.4-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/latin-locales/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-f99b27.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=vulnerabilities&selected=adamlui_python-utils%3Alatin-locales&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%3Alatin-locales%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonar&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

> ### _ISO 639-1 (2-letter) codes for Latin locales that don't require advanced Unicode support._

It's just a [JSON file](https://cdn.jsdelivr.net/gh/adamlui/python-utils@latin-locales-1.0.4/latin-locales/src/latin_locales/latin-locales.json), so you can use it in any environment.

<a href="#"><img style="height:10px ; width:100%" src="https://cdn.jsdelivr.net/gh/adamlui/js-utils@7da7074/assets/images/separators/aqua-gradient.png"></a>

## Installation

```bash
pip install latin-locales
```

<hr>

## Usage

```py
import latin_locales

print(latin_locales)
# => ['aa', 'ae', 'af', 'ak', 'an', 'ay', 'bi', 'bm', 'br', ...]
```

_Note: Most type checkers will falsely warn_ `latin_locales` _is not iterable because they are incapable of analyzing runtime behavior (where the module is replaced w/ a list for cleaner, direct access). You can safely suppress such warnings using_ `# type: ignore`.

<hr>

## MIT License

Copyright © 2026 [Adam Lui](https://github.com/adamlui)

<hr>

## Related

🇨🇳 [non-latin-locales](https://github.com/adamlui/python-utils/tree/main/non-latin-locales/#readme) - ISO 639-1 (2-letter) codes for non-Latin locales.
<br>🌍 [translate-messages](https://github.com/adamlui/python-utils/tree/main/translate-messages/#readme) - Translate `en/messages.json` (chrome.i18n format) to 100+ locales automatically.
<br>🈶 [is-unicode-supported](https://github.com/adamlui/python-utils/tree/main/is-unicode-supported/#readme) - Detect whether the terminal supports advanced Unicode.

<a href="#"><img style="height:10px ; width:100%" src="https://cdn.jsdelivr.net/gh/adamlui/python-utils@b8b2932/assets/images/separators/aqua-gradient.png"></a>

<picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/white/icon32x27.png"><img height=13 src="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/dark-gray/icon32x27.png"></picture> <a href=https://github.com/adamlui/python-utils/#readme>**More Python utilities**</a> /
<a href="https://github.com/adamlui/python-utils/discussions">Discuss</a> /
<a href="https://github.com/adamlui/python-utils/issues">Report bug</a> /
<a href="mailto:security@tidelift.com">Report vulnerability</a>
