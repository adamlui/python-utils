<a id="top"></a>

# > translate-messages

<a href="https://pepy.tech/projects/translate-messages?versions=*">
    <img height=31 src="https://img.shields.io/pepy/dt/translate-messages?logo=weightsandbiases&color=af68ff&logoColor=white&labelColor=464646&style=for-the-badge"></img></a>
<a href="https://github.com/adamlui/python-utils/releases/tag/translate-messages-1.10.1">
    <img height=31 src="https://img.shields.io/badge/Latest_Build-1.10.1-32fcee.svg?logo=icinga&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://github.com/adamlui/python-utils/blob/main/translate-messages/docs/LICENSE.md">
    <img height=31 src="https://img.shields.io/badge/License-MIT-f99b27.svg?logo=internetarchive&logoColor=white&labelColor=464646&style=for-the-badge"></a>
<a href="https://www.codefactor.io/repository/github/adamlui/python-utils">
    <img height=31 src="https://img.shields.io/codefactor/grade/github/adamlui/python-utils?label=Code+Quality&logo=codefactor&logoColor=white&labelColor=464646&color=a0fc55&style=for-the-badge"></a>
<a href="https://sonarcloud.io/component_measures?metric=vulnerabilities&selected=adamlui_python-utils%3Atranslate-messages&id=adamlui_python-utils">
    <img height=31 src="https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fsonarcloud.io%2Fapi%2Fmeasures%2Fcomponent%3Fcomponent%3Dadamlui_python-utils%3Atranslate-messages%26metricKeys%3Dvulnerabilities&query=%24.component.measures.0.value&style=for-the-badge&logo=sonar&logoColor=white&labelColor=464646&label=Vulnerabilities&color=fafc74"></a>

> ### _Translate `en/messages.json` (chrome.i18n format) to 100+ locales automatically._

## Installation

```bash
pip install translate-messages
```

## Usage

Run the CLI:

```bash
translate-messages [options]  # or translatemsgs
```

If no options are passed, the CLI will:

1. Prompt for message keys to ignore
2. Auto-discover closest child `_locales` dir
3. Translate found `en/messages.json` to target languages

_Note: Any messages.json in the [`chrome.i18n`](https://developer.chrome.com/docs/extensions/how-to/ui/localization-message-formats) format can be used as a source file._

## Options

Options can be set by using command-line arguments:

| Option                              | Description                                                                                               | Example
| ----------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------
| `-d`, `--locales-dir`               | Name of the folder containing locale files (default: `_locales`)                                          | `--locales-dir=_messages`
| `-t`, `--target-langs`              | Comma-separated list of languages to translate to (default: all 100+ [`stable_locales`][stable-locales])  | `--target-langs=es,fr`
| `-k`, `--keys`                      | Comma-separated list of keys to translate (default: all found src keys missing in target files)           | `--keys=app_DESC,err_NOT_FOUND`
| `--exclude-langs`                   | Comma-separated list of languages to exclude                                                              | `--exclude-langs=es,zh`
| `--exclude-keys`                    | Comma-separated list of keys to ignore                                                                    | `--exclude-keys=app_NAME,author`
| `--only-stable`                     | Only use stable locales (skip auto-discovery)                                                             |
| `--config`                          | Use custom config file                                                                                    | `--config=path/to/file`
| `init`, `-i`, `--init`              | Create `.translate-msgs.config.json5` in project root to store default options                            |
| `-f`, `--force`                     | Force overwrite of existing config file when using `init`                                                 |
| `-n`, `--no-wizard`                 | Skip interactive prompts during start-up                                                                  |
| `-h`, `--help`                      | Show help screen                                                                                          |
| `-v`, `--version`                   | Show version                                                                                              |
| `-V`, `--debug [target_config_key]` | Show debug logs                                                                                           |
| `--docs`                            | Open docs URL                                                                                             |

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

Copyright © 2023–2026 [Adam Lui](https://github.com/adamlui).

## Related

🈶 [is-unicode-supported](https://github.com/adamlui/python-utils/tree/main/is-unicode-supported/#readme) - Detect whether the terminal supports advanced Unicode.
<br>🇨🇳 [non-latin-locales](https://github.com/adamlui/python-utils/tree/main/non-latin-locales/#readme) - ISO 639-1 (2-letter) codes for non-Latin locales.
<br>🇪🇸 [latin-locales](https://github.com/adamlui/python-utils/tree/main/latin-locales/#readme) - ISO 639-1 (2-letter) codes for Latin locales.
<br><b>{ }</b> [remove-json-keys](https://github.com/adamlui/python-utils/tree/main/remove-json-keys/#readme) - Simply remove JSON keys via CLI command.

#

<picture><source media="(prefers-color-scheme: dark)" srcset="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/white/icon32x27.png"><img height=13 src="https://cdn.jsdelivr.net/gh/adamlui/python-utils@760599e/assets/images/icons/home/dark-gray/icon32x27.png"></picture> <a href=https://github.com/adamlui/python-utils/#readme>**More Python utilities**</a> /
<a href="https://github.com/adamlui/python-utils/discussions">Discuss</a> /
<a href="https://github.com/adamlui/python-utils/issues">Report bug</a> /
<a href="mailto:security@tidelift.com">Report vulnerability</a> /
<a href="#top">Back to top ↑</a>

[stable-locales]: https://github.com/adamlui/python-utils/blob/translate-messages-1.10.1/translate-messages/src/translate_messages/data/package_data.json#L23-L28
