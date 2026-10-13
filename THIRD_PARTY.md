# Third-party licenses and attributions

`geany-playdate` is licensed under the [GNU General Public License v3.0 or later](LICENSE)
(GPL-3.0-or-later). That choice covers the licenses of the projects this plugin
draws from: **MIT**, **Apache-2.0**, and the Geany plugin API (GPL-2.0-or-later).

| Project | License | How we use it |
|---------|---------|----------------|
| [geany](https://github.com/geany/geany) / [geany-plugins](https://github.com/geany/geany-plugins) | GPL-2.0-or-later | Plugin API headers; loaded as a Geany module |
| [orta/vscode-playdate](https://github.com/orta/vscode-playdate) | MIT | Behaviour: single Build+Run command, SDK path resolution (`PLAYDATE_SDK_PATH` first), default `Source` / `Output.pdx`, `pdc` + `PlaydateSimulator` invocation |
| [midouest/vscode-playdate-debug](https://github.com/midouest/vscode-playdate-debug) | MIT | Behaviour: `pdc` problem matchers (`warning: file:line: msg`), `pdc` flags (`-s`, `--no-compress`, `-v`, `-q`, `-k`), separation of Build / Run |
| [notpeter/playdate-luacats](https://github.com/notpeter/playdate-luacats) | Apache-2.0 OR MIT | Generated Geany tags from `library/stub.lua` (API names, signatures); vendored into `src/tags_data.h` / `tags/playdate.lua.tags` via `tools/luacats_to_tags.py` |
| [notpeter/playdate-docdef](https://github.com/notpeter/playdate-docdef) | see repo | Upstream of the LuaCATS stub generation pipeline |
| Panic Playdate SDK documentation / API names | [Playdate SDK License 1.0](https://play.date/dev/sdk-license/) | Factual API names and signatures of the public Playdate Lua API (via LuaCATS). Copyright © Panic Inc. Not affiliated with Panic. |
| [cadin/playdate-vscode-template](https://github.com/cadin/playdate-vscode-template) | see repo | Reference only (build/run task layout) |
| [Whitebrim/VSCode-PlaydateTemplate](https://github.com/Whitebrim/VSCode-PlaydateTemplate) | see repo | Reference only (simulator workflow) |

## Why GPL-3.0-or-later

- Geany plugins must be **GPL-compatible** (they link against Geany).
- **MIT** (Orta, midouest) is GPL-compatible.
- **Apache-2.0** (LuaCATS) is compatible with **GPL-3**, not with GPL-2-only.
- Therefore this project is **GPL-3.0-or-later**, which is compatible with all of
  the above and remains a valid license for a Geany plugin (Geany is
  GPL-2.0-**or-later**, so a GPLv3 combined work is allowed).

If you redistribute this plugin, keep this file and the copyright notices in
each source file.

## Playdate trademark

Playdate is a trademark of Panic Inc. This plugin is an unofficial community
tool and is not endorsed by Panic. You need the [Playdate SDK](https://play.date/dev/)
installed separately; it is not included.
