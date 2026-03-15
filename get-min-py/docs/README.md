<a id="top"></a>

# > get-min-py

<a href="https://github.com/adamlui/python-utils/releases/tag/get-min-py-1.0.0">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-1.0.0-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/get-min-py/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-f99b27.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=new_vulnerabilities&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonarcloud&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

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
print(result) # => '3.9'

results = get_min_py(['numpy', 'pandas', 'flask'])
print(results) # => ['3.11', '3.11', '3.9']
```

_Note: Most type checkers will falsely warn_ `get_min_py` _is not a callable module because they are incapable of analyzing runtime behavior (where the module is replaced w/ a function for cleaner, direct access). You can safely suppress such warnings using_ `# type: ignore`.

## MIT License

Copyright © 2026 [Adam Lui](https://github.com/adamlui).

#

<a href="#top">Back to top ↑</a>
