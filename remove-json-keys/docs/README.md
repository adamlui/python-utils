<a id="top"></a>

# > remove-json-keys

<a href="https://pepy.tech/projects/remove-json-keys">
    <img height=31 src="https://img.shields.io/pepy/dt/remove-json-keys?logo=weightsandbiases&color=af68ff&logoColor=white&labelColor=464646&style=for-the-badge"></img></a>
<a href="https://github.com/adamlui/python-utils/releases/tag/remove-json-keys-1.6.0">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-1.6.0-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/remove-json-keys/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-f99b27.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=new_vulnerabilities&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonarcloud&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

> ### _Simply remove JSON keys via CLI command._

## Installation

```bash
pip install remove-json-keys
```

## Usage

Run the CLI:
```bash
remove-json-keys [options] # or remove-json
```

If no options are passed, the CLI will:
1. Prompt for keys to delete 
2. Auto-discover closest child `json_dir`
3. Delete keys from found JSON files

_Note: Key/values can span multiple lines and have any amount of whitespace between symbols._

## Options

Options can be set by using command-line arguments:

| Option                 | Description                                                                     | Example
| ---------------------- | ------------------------------------------------------------------------------- | -----------------------------
| `-d`, `--json-dir`     | Name of the folder containing JSON files (default: `_locales`)                  | `--json-dir=data`
| `-k`, `--keys`         | Comma-separated list of keys to remove                                          | `--keys=app_DESC,err_NOT_FOUND`
| `--config`             | Use custom config file                                                          | `--config=path/to/file`
| `init`, `-i`, `--init` | Create .remove-json.config.json5 in project root to store default settings      |
| `-n`, `--no-wizard`    | Skip interactive prompts during start-up                                        |
| `-h`, `--help`         | Show help screen                                                                |
| `-v`, `--version`      | Show version                                                                    |
| `--docs`               | Open docs URL                                                                   |

## Examples

Remove `author` key from JSON files found in default `_locales` dir:

```bash
remove-json-keys --keys=author  # prompts for more keys to remove
```

Remove `info_SUCCESS` key from JSON files found in `messages` dir:

```bash
remove-json-keys -n --keys=err_NOT_FOUND --json-dir=messages  # no prompts
```

Remove `app_DESC` + `app_VER` keys from JSON files found in `data` dir:

```bash
remove-json -n -k app_DESC,app_VER -d data  # no prompts
```

## Config file

Run `remove-json init` to create `.remove-json.config.json5` in your project root to set default options.

Example defaults:

```json5
{
  "json_dir": "_locales", // name of the folder containing JSON files
  "keys": "",             // keys to remove (e.g. "app_NAME,author")
  "force": false,         // force overwrite existing config file when using init
  "no_wizard": false      // skip interactive prompts during start-up
}
```

_Note: CLI arguments always override config file._

## MIT License

**Copyright © 2023–2026 [Adam Lui](https://github.com/adamlui).**

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#

<a href="#top">Back to top ↑</a>
