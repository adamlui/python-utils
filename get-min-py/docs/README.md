<a id="top"></a>

# > get-min-py

<a href="https://pepy.tech/projects/get-min-py?versions=*">
    <img height=31 src="https://img.shields.io/pepy/dt/get-min-py?logo=weightsandbiases&color=af68ff&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/releases/tag/get-min-py-1.2.1">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-1.2.1-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/get-min-py/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-f99b27.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=vulnerabilities&selected=adamlui_python-utils%3Aget-min-py&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%3Aget-min-py%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonar&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

> ### _Get the minimum Python version required for a PyPI package._

Uses `python-requires`, or classifiers if not found.

## ⚡ Installation

```bash
pip install get-min-py
```

## 💻 Command line usage

```bash
get-min-py <pkg>[,pkg2,pkg3,...]  # or getminpy
```

Example:

<img src="https://cdn.jsdelivr.net/gh/adamlui/python-utils@f133ea3/get-min-py/assets/images/cli-output.png">

CLI options:

| Option            | Description
| ----------------- | -----------------
| `-h`, `--help`    | Show help screen
| `-v`, `--version` | Show version
| `--docs`          | Open docs URL

## 🔌 API usage

```py
import get_min_py

result = get_min_py('requests')
print(result) # => 3.9

results = get_min_py(['numpy', 'pandas', 'flask'])
print(results) # => ['3.11', '3.11', '3.9']
```

_Note: Most type checkers will falsely warn_ `get_min_py` _is not a callable module because they are incapable of analyzing runtime behavior (where the module is replaced w/ a function for cleaner, direct access). You can safely suppress such warnings using_ `# type: ignore`.

## MIT License

Copyright © 2026 [Adam Lui](https://github.com/adamlui)

## Related

📂 [find-project-root](https://github.com/adamlui/python-utils/tree/main/find-project-root/#readme) - Locate project root via custom markers.

#

<picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/white/icon32x27.png"><img height=13 src="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/dark-gray/icon32x27.png"></picture> <a href=https://github.com/adamlui/python-utils/#readme>**More Python utilities**</a> /
<a href="https://github.com/adamlui/python-utils/discussions">Discuss</a> /
<a href="https://github.com/adamlui/python-utils/issues">Report bug</a> /
<a href="mailto:security@tidelift.com">Report vulnerability</a> /
<a href="#top">Back to top ↑</a>
