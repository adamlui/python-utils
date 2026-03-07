<a id="top"></a>

# > project-markers

<a href="https://pepy.tech/projects/project-markers">
    <img height=31 src="https://img.shields.io/pepy/dt/project-markers?logo=weightsandbiases&color=af68ff&logoColor=white&labelColor=464646&style=for-the-badge"></img></a>
<a href="https://github.com/adamlui/python-utils/releases/tag/project-markers-1.0.0">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-1.0.0-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/project-markers/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-f99b27.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=new_vulnerabilities&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonarcloud&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

> ### _Common project root markers._

It's just a [JSON file](https://github.com/adamlui/python-utils/blob/project-markers-1.0.0/project-markers/src/project_markers/project_markers.json), so you can use it in any environment.

## Installation

```bash
pip install project-markers
```

## Usage

```py
import project_markers

print(project_markers)
# => ['.ansible-lint', '.bazelrc', '.browserslistrc', '.buckconfig', ...]
```

_Note: Most type checkers will falsely warn_ `project_markers` _is not iterable because they cannot analyze runtime behavior (where the module is replaced w/ a list for cleaner, direct access). You can safely suppress such warnings using_ `# type: ignore`.

The list includes hundreds of markers from many tools and ecosystems, including:

- Version control (.git, .hg, .svn)
- Python (pyproject.toml, setup.py, requirements.txt)
- JavaScript (package.json, yarn.lock, tsconfig.json)
- Docker/K8s (Dockerfile, docker-compose.yml)
- CI/CD (.github, .gitlab-ci.yml, Jenkinsfile)

## MIT License

Copyright © 2026 [Adam Lui](https://github.com/adamlui).

#

<a href="#top">Back to top ↑</a>
