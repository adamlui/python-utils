<a id="top"></a>

# > is-unicode-supported

<a href="https://pepy.tech/projects/is-unicode-supported?versions=*">
    <img height=31 src="https://img.shields.io/pepy/dt/is-unicode-supported?logo=weightsandbiases&color=af68ff&logoColor=white&labelColor=464646&style=for-the-badge"></img></a>
<a href="https://github.com/adamlui/python-utils/releases/tag/is-unicode-supported-1.2.1">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-1.2.1-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/is-unicode-supported/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-f99b27.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=vulnerabilities&selected=adamlui_python-utils%3Ais-unicode-supported&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%3Ais-unicode-supported%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonar&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

> ### _Detect whether the terminal supports advanced Unicode._

Checks if terminal supports advanced Unicode (CJK, emoji, etc.) by measuring the cursor position of a single, wide char (𠀀). Returns `False` for legacy consoles or `True` if the wide char renders as 2 columns.

## ⚡ Installation

```bash
pip install is-unicode-supported
```

## 💻 Command line usage

```bash
is-unicode-supported  # or supportsunicode
# e.g. => True
```

CLI options:

| Option            | Description
| ----------------- | -----------------
| `-h`, `--help`    | Show help screen
| `-v`, `--version` | Show version
| `--docs`          | Open docs URL

## 🔌 API usage

```py
import is_unicode_supported

if is_unicode_supported():
    print('Advanced Unicode supported!')
else:
    print('Advanced Unicode not supported!')
```

_Note: Most type checkers will falsely warn_ `is_unicode_supported` _is not a callable module because they are incapable of analyzing runtime behavior (where the module is replaced w/ a function for cleaner, direct access). You can safely suppress such warnings using_ `# type: ignore`.

## MIT License

Copyright © 2026 [Adam Lui](https://github.com/adamlui)

## Related

🇪🇸 [latin-locales](https://github.com/adamlui/python-utils/tree/main/latin-locales/#readme) - ISO 639-1 (2-letter) codes for Latin locales.
<br>🇨🇳 [non-latin-locales](https://github.com/adamlui/python-utils/tree/main/non-latin-locales/#readme) - ISO 639-1 (2-letter) codes for non-Latin locales.
<br>🌍 [translate-messages](https://github.com/adamlui/python-utils/tree/main/translate-messages/#readme) - Translate `en/messages.json` (chrome.i18n format) to 100+ locales automatically.

#

<picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/white/icon32x27.png"><img height=13 src="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/dark-gray/icon32x27.png"></picture> <a href=https://github.com/adamlui/python-utils/#readme>**More Python utilities**</a> /
<a href="https://github.com/adamlui/python-utils/discussions">Discuss</a> /
<a href="https://github.com/adamlui/python-utils/issues">Report bug</a> /
<a href="mailto:security@tidelift.com">Report vulnerability</a> /
<a href="#top">Back to top ↑</a>
