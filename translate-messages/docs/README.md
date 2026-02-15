<a id="top"></a>

# > translate-messages

<a href="#">
    <img height=31 src="https://img.shields.io/pypi/dm/translate-messages?logo=pypi&color=af68ff&logoColor=white&labelColor=464646&style=for-the-badge"></img></a>
<a href="https://github.com/adamlui/python-utils/releases/tag/translate-messages-1.1.0">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-1.1.0-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/translate-messages/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-orange.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=new_vulnerabilities&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonarcloud&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

> ### _Translate `en/messages.json` (in chrome.i18n format) to other locales automatically._

## Installation

```bash
pip install translate-messages
```

## Usage

Run the CLI:
```bash
translate-messages [options] # alias: translate-msgs
```

If no options are provided, the CLI will:
1. Prompt for message keys to ignore 
2. Auto-discover closest child `_locales` dir
3. Translate `en/messages.json` to target languages

_Note: Any messages.json in the [`chrome.i18n`](https://developer.chrome.com/docs/extensions/how-to/ui/localization-message-formats) format can be used as a source file._

## Options

Options can be set by using command-line arguments:

| Option                 | Description                                                                                          | Example
| ---------------------- | ---------------------------------------------------------------------------------------------------- | ------------------------------
| `-d`, `--locales-dir`  | Name of the folder containing locale files (default: `_locales`)                                     | `--locales-dir=_messages`
| `-t`, `--target-langs` | Comma-separated list of languages to include (default: all [`supported_locales`][supported-locales]) | `--target-langs=en,es,fr`
| `--exclude-langs`      | Comma-separated list of languages to exclude                                                         | `--exclude-langs=en,es`
| `-k`, `--keys`         | Comma-separated list of keys to translate                                                            | `--keys=appDesc,err_notFound`
| `--exclude-keys`       | Comma-separated list of keys to ignore                                                               | `--exclude-keys=appName,author`
| `-i`, `--init`         | Create .translate-msgs.config.jsonc in project root to store defaults                                |
| `-f`, `--force`        | Force overwrite of existing config file when using `--init`                                          |
| `-W`, `--no-wizard`    | Skip interactive prompts during start-up                                                             |
| `-h`, `--help`         | Show help screen                                                                                     |

[supported-locales]: https://github.com/adamlui/python-utils/blob/translate-messages-1.1.0/translate-messages/src/translate_messages/package_data.json#L11-L16

## Examples

Translate everything except `appName` from `_locales/en/messages.json` to French and Spanish:

```bash
translate-messages --include-langs=fr,es --ignore-keys=appName -W
```

Translate `appDesc` + `err_notFound` keys from `_msgs/en/messages.json`:

```bash
translate-msgs -k appDesc,err_notFound -d _msgs -W
```

## Config file

Use `--init` to create `.translate-msgs.config.jsonc` in your project root to set default options.

Example defaults:

```jsonc
{
  "locales_dir": "_locales",
  "target_langs": "",
  "keys": "",
  "exclude_langs": "",
  "exclude_keys": "",
  "force": false,
  "no_wizard": false
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
