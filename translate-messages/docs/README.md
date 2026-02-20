<a id="top"></a>

# > translate-messages

<a href="https://pypistats.org/packages/translate-messages">
    <img height=31 src="https://img.shields.io/pypi/dm/translate-messages?logo=pypi&color=af68ff&logoColor=white&labelColor=464646&style=for-the-badge"></img></a>
<a href="https://github.com/adamlui/python-utils/releases/tag/translate-messages-1.3.0">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-1.3.0-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/translate-messages/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-f99b27.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=new_vulnerabilities&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonarcloud&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

> ### _Translate `en/messages.json` (in chrome.i18n format) to 100+ locales automatically._

## Installation

```bash
pip install translate-messages
```

## Usage

Run the CLI:
```bash
translate-messages [options] # or translate-msgs
```

If no options are passed, the CLI will:
1. Prompt for message keys to ignore 
2. Auto-discover closest child `_locales` dir
3. Translate found `en/messages.json` to target languages

_Note: Any messages.json in the [`chrome.i18n`](https://developer.chrome.com/docs/extensions/how-to/ui/localization-message-formats) format can be used as a source file._

## Options

Options can be set by using command-line arguments:

| Option                 | Description                                                                                               | Example
| ---------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------
| `-d`, `--locales-dir`  | Name of the folder containing locale files (default: `_locales`)                                          | `--locales-dir=_messages`
| `-t`, `--target-langs` | Comma-separated list of languages to translate to (default: all 100+ [`stable_locales`][stable-locales])  | `--target-langs=es,fr`
| `-k`, `--keys`         | Comma-separated list of keys to translate (default: all found src keys missing in target files)           | `--keys=app_DESC,err_NOT_FOUND`
| `--exclude-langs`      | Comma-separated list of languages to exclude                                                              | `--exclude-langs=es,zh`
| `--exclude-keys`       | Comma-separated list of keys to ignore                                                                    | `--exclude-keys=app_NAME,author`
| `--only-stable`        | Only use stable locales (skip auto-discovery)                                                             |
| `init`, `-i`, `--init` | Create `.translate-msgs.config.json5` in project root to store default options                            |
| `-f`, `--force`        | Force overwrite of existing config file when using `init`                                                 |
| `-n`, `--no-wizard`    | Skip interactive prompts during start-up                                                                  |
| `-h`, `--help`         | Show help screen                                                                                          |
| `-v`, `--version`      | Show version                                                                                              |
| `--docs`               | Open docs URL                                                                                             |

## Examples

Translate all keys except `app_NAME` from `_locales/en/messages.json` to all [`stable_locales`][stable-locales]:

```bash
translate-messages --ignore-keys=app_NAME  # prompts for more keys to ignore
```

Translate `app_DESC` key from `messges/en/messages.json` to French:

```bash
translate-messages -n --keys=app_DESC --locales-dir=messages --target-langs=fr  # no prompts
```

Translate `app_DESC` + `err_NOT_FOUND` keys from `_msgs/en/messages.json` to Spanish and Hindi:

```bash
translate-msgs -n -k app_DESC,err_NOT_FOUND -d _msgs -t es,hi  # no prompts
```

## Config file

Run `translate-msgs init` to create `.translate-msgs.config.json5` in your project root to set default options.

Example defaults:

```json5
{
  "locales_dir": "_locales", // name of the folder containing locale files
  "target_langs": "",        // languages to translate to (e.g. "en,es,fr") (default: all 100+ supported locales)
  "keys": "",                // keys to translate (e.g. "app_DESC,err_NOT_FOUND")
  "exclude_langs": "",       // languages to exclude (e.g. "en,es")
  "exclude_keys": "",        // keys to ignore (e.g. "app_NAME,author")
  "force": false,            // force overwrite existing config file when using init
  "no_wizard": false         // skip interactive prompts during start-up
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

[stable-locales]: https://github.com/adamlui/python-utils/blob/translate-messages-1.3.0/translate-messages/src/translate_messages/assets/data/package_data.json#L22-L27
