<a id="top"></a>

# > sys-lang

<a href="https://pepy.tech/projects/sys-lang?versions=*">
    <img height=31 src="https://img.shields.io/pepy/dt/sys-lang?logo=weightsandbiases&color=af68ff&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/releases/tag/sys-lang-1.0.1">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-1.0.1-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/sys-lang/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-f99b27.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=vulnerabilities&selected=adamlui_python-utils%3Asys-lang&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%3Asys-lang%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonar&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

> ### _Detect the system language._

Returns ISO 639-1 (e.g. `'en'`) or ISO 3166-1 alpha-2-appended (`'en_US'`) code for user's preferred language. On Windows, queries `Get-Culture` via PowerShell. On *nix systems, reads `LC_ALL`, `LC_MESSAGES`, `LANG`, and `LANGUAGE`.

<hr>

## ⚡ Installation

```bash
pip install sys-lang
```

<hr>

## 💻 Command line usage

```bash
sys-lang  # or syslang
# e.g. => 'en_US'
```

CLI options:

| Option              | Description
| ------------------- | ------------------------------------
| `-n`, `--no-region` | Don't include region when available
| `-h`, `--help`      | Show help screen
| `-v`, `--version`   | Show version
| `--docs`            | Open docs URL

<hr>

## 🔌 API usage

```py
from sys_lang import get_sys_lang

print(get_sys_lang()) # e.g. => zh_HK
print(get_sys_lang(region=False)) # e.g. => zh
```

<hr>

## MIT License

Copyright © 2026 [Adam Lui](https://github.com/adamlui)

<hr>

## Related

🇪🇸 [latin-locales](https://github.com/adamlui/python-utils/tree/main/latin-locales/#readme) - ISO 639-1 (2-letter) codes for Latin locales.
<br>🇨🇳 [non-latin-locales](https://github.com/adamlui/python-utils/tree/main/non-latin-locales/#readme) - ISO 639-1 (2-letter) codes for non-Latin locales.
<br>🌍 [translate-messages](https://github.com/adamlui/python-utils/tree/main/translate-messages/#readme) - Translate `en/messages.json` (chrome.i18n format) to 100+ locales automatically.
<br>🈶 [is-unicode-supported](https://github.com/adamlui/python-utils/tree/main/is-unicode-supported/#readme) - Detect whether the terminal supports advanced Unicode.

<a href="#"><img style="height:10px ; width:100%" src="https://cdn.jsdelivr.net/gh/adamlui/python-utils@b8b2932/assets/images/separators/aqua-gradient.png"></a>

<picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/white/icon32x27.png"><img height=13 src="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/dark-gray/icon32x27.png"></picture> <a href=https://github.com/adamlui/python-utils/#readme>**More Python utilities**</a> /
<a href="https://github.com/adamlui/python-utils/discussions">Discuss</a> /
<a href="https://github.com/adamlui/python-utils/issues">Report bug</a> /
<a href="mailto:security@tidelift.com">Report vulnerability</a> /
<a href="#top">Back to top ↑</a>
