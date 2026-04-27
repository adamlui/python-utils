<a id="top"></a>

# > find-project-root

<a href="https://pepy.tech/projects/find-project-root?versions=*">
    <img height=31 src="https://img.shields.io/pepy/dt/find-project-root?logo=weightsandbiases&color=af68ff&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/releases/tag/find-project-root-2.0.0">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-2.0.0-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/find-project-root/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-f99b27.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=vulnerabilities&selected=adamlui_python-utils%3Afind-project-root&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%3Afind-project-root%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonar&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

> ### _Locate project root via custom markers._

<a href="#"><img style="height:10px ; width:100%" src="https://cdn.jsdelivr.net/gh/adamlui/js-utils@7da7074/assets/images/separators/aqua-gradient.png"></a>

## About

**find-project-root** is a lightweight utility that traverses up from a given path until it finds a project marker.

- Lightweight — < 100 KB
- Path flexibility — accepts strings, `Path` objects, or current working dir
- Customizable markers — provide your own or use defaults
- Multi-env support — use via [API](#api-usage) or [CLI](#command-line-usage)

<hr>

## Installation

```bash
pip install find-project-root
```

<hr>

## API usage

```py
import find_project_root

# Find from current dir
root = find_project_root()
print(root) # e.g. => /home/user/projects/your-project
```

_Note: Most type checkers will falsely warn_ `find_project_root` _is not a callable module because they are incapable of analyzing runtime behavior (where the module is replaced w/ a function for cleaner, direct access). You can safely suppress such warnings using_ `# type: ignore`.

### Available options:

Name        | Type                    | Description                        | Default Value
------------|-------------------------|------------------------------------|------------------------------------------------------------
`path`      | `str`, `Path` or `None` | Starting directory to search from. | `None` (current working dir)
`max_depth` | `int`                   | Max levels to traverse up.         | `9`
`markers`   | `List[str]` or `None`   | Custom marker files to look for.   | [`project-markers`][project-markers-json] list

### Examples:

Start from specific path:

```py
root = find_project_root(path='assets/images')
```

Limit search depth:

```py
root = find_project_root(max_depth=3)
```

Use custom markers:

```py
root = find_project_root(markers=['.git', 'pyproject.toml', 'requirements.txt'])
```

Combine options:

```py
root = find_project_root(path='src', max_depth=5, markers=['manifest.json'])
```

<hr>

## Command line usage

```bash
find-project-root  # or projectroot
# e.g. => 'e:\python\utils\translate-messages'
```

CLI options:

| Option              | Description
| ------------------- | ------------------------------------
| `-h`, `--help`      | Show help screen
| `-v`, `--version`   | Show version
| `--docs`            | Open docs URL

<hr>


## MIT License

Copyright © 2026 [Adam Lui](https://github.com/adamlui)

<hr>

## Related

🏷️ [project-markers][project-markers-gh] - Common project root markers.
<br>📊 [get-min-py](https://github.com/adamlui/python-utils/tree/main/get-min-py/#readme) - Get the minimum Python version required for a PyPI package.

<a href="#"><img style="height:10px ; width:100%" src="https://cdn.jsdelivr.net/gh/adamlui/python-utils@b8b2932/assets/images/separators/aqua-gradient.png"></a>

<picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/white/icon32x27.png"><img height=13 src="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/dark-gray/icon32x27.png"></picture> <a href=https://github.com/adamlui/python-utils/#readme>**More Python utilities**</a> /
<a href="https://github.com/adamlui/python-utils/discussions">Discuss</a> /
<a href="https://github.com/adamlui/python-utils/issues">Report bug</a> /
<a href="mailto:security@tidelift.com">Report vulnerability</a> /
<a href="#top">Back to top ↑</a>

[project-markers-gh]: https://github.com/adamlui/python-utils/tree/main/project-markers/#readme
[project-markers-json]: https://cdn.jsdelivr.net/gh/adamlui/python-utils/project-markers/src/project_markers/project-markers.json
