<a id="top"></a>

# > 📟 is-legacy-terminal

<a href="https://pepy.tech/projects/is-legacy-terminal?versions=*">
    <img height=31 src="https://img.shields.io/pepy/dt/is-legacy-terminal?logo=weightsandbiases&color=af68ff&logoColor=white&labelColor=464646&style=for-the-badge"></img></a>
<a href="https://github.com/adamlui/python-utils/releases/tag/is-legacy-terminal-1.0.2">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-1.0.2-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/is-legacy-terminal/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-f99b27.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=vulnerabilities&selected=adamlui_python-utils%3Ais-legacy-terminal&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonar&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

> ### _Detect whether the terminal is legacy._

Checks if terminal is legacy (limited rendering, flicker-prone on rapid redraws, etc.). On Windows, returns `True` if CMD or PowerShell ISE not hosted in modern shell. On *nix systems, returns `True` if `env.TERM` is `'dumb'` or `'unknown'` (indicating a very basic terminal).

## ⚡ Installation

```bash
pip install is-legacy-terminal
```

## 💻 Command line usage

```bash
is-legacy-terminal  # or islegacy
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
import is_legacy_terminal

if is_legacy_terminal():
    print('Is legacy terminal!')
else:
    print('Is modern terminal!')
```

_Note: Most type checkers will falsely warn_ `is_legacy_terminal` _is not a callable module because they are incapable of analyzing runtime behavior (where the module is replaced w/ a function for cleaner, direct access). You can safely suppress such warnings using_ `# type: ignore`.

## MIT License

Copyright © 2026 [Adam Lui](https://github.com/adamlui).

## Related

🈶 [is-unicode-supported](https://github.com/adamlui/python-utils/tree/main/is-unicode-supported/#readme) - Detect whether the terminal supports advanced Unicode.

#

<picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/white/icon32x27.png"><img height=13 src="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/dark-gray/icon32x27.png"></picture> <a href=https://github.com/adamlui/python-utils/#readme>**More Python utilities**</a> /
<a href="#top">Back to top ↑</a>
