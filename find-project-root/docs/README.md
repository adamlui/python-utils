<a id="top"></a>

# > find-project-root

<a href="https://github.com/adamlui/python-utils/releases/tag/find-project-root-1.0.1">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-1.0.1-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/find-project-root/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-f99b27.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=new_vulnerabilities&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonarcloud&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

> ### _Locate project root via custom markers._

## About

**find-project-root** is a lightweight utility that traverses up from a given path until it finds a project marker.

- Minimal dependencies — only uses [project-markers][project-markers-gh] (~6 KB module)
- Path flexibility — accepts strings, `Path` objects, or current working dir
- Customizable markers — provide your own or use defaults
- Multi-Python support — from Python 2.6 thru 3.15+

## Installation

```bash
pip install find-project-root
```

## API usage

```py
import find_project_root

# Find from current dir
root = find_project_root()
print(root) # e.g. /home/user/projects/your-project
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

## MIT License

Copyright © 2026 [Adam Lui](https://github.com/adamlui).

#

<a href="#top">Back to top ↑</a>

[project-markers-gh]: https://github.com/adamlui/python-utils/tree/main/project-markers
[project-markers-json]: https://github.com/adamlui/python-utils/blob/main/project-markers/src/project_markers/project_markers.json
