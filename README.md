# geany-playdate

**Playdate development plugin for [Geany](https://www.geany.org)** — build with
`pdc`, run in the Playdate Simulator, jump to `pdc` errors in the Compiler tab,
and autocomplete the Playdate Lua API.

Unofficial community tool. Not affiliated with [Panic](https://panic.com) or
[Playdate](https://play.date).

| | |
|---|---|
| Editor | Geany ≥ 1.26 (tested on 2.1, GTK3) |
| Language | C (Geany Plugin API) |
| License | [GPL-3.0-or-later](LICENSE) — see [THIRD_PARTY.md](THIRD_PARTY.md) |
| Target SDK | [Playdate SDK](https://play.date/dev/) (`pdc` + Simulator) |

---

## Features

- **Build and Run** — one command: compile with `pdc`, open the `.pdx` in the Simulator
- **Build** / **Run** / **Clean** / **Open Simulator** — separate actions
- **Compiler tab integration** — `pdc` `warning:` / `error:` lines become
  clickable messages (`file:line`) in Geany’s Compiler view
- **Preferences dialog** — SDK path, source dir, output `.pdx`, product name,
  `pdc` flags
- **API autocomplete** — ~1800 Geany tags generated from
  [playdate-luacats](https://github.com/notpeter/playdate-luacats) (`playdate.*`,
  CoreLibs, signatures)
- **Smart project detection** — finds the Playdate project root by locating the
  `Source`/`source` folder (works with `source/pdxinfo` layouts)

### Behaviour sources

We deliberately combine the best of two VS Code plugins:

| From | What we took |
|------|----------------|
| **[orta/vscode-playdate](https://github.com/orta/vscode-playdate)** (MIT) | Simple Build+Run UX; SDK resolution (`PLAYDATE_SDK_PATH` wins over settings); defaults `Source` / `Output.pdx`; `pdc source output` + `PlaydateSimulator output` |
| **[midouest/vscode-playdate-debug](https://github.com/midouest/vscode-playdate-debug)** (MIT) | `pdc` problem matchers; `pdc` flags (`-s`, `--no-compress`, `-v`, `-q`, `-k`); split Build vs Run |
| **[notpeter/playdate-luacats](https://github.com/notpeter/playdate-luacats)** (Apache-2.0 OR MIT) | Machine-readable Playdate API → Geany tags (names + signatures) |

Also referenced (workflow/docs): [cadin/playdate-vscode-template](https://github.com/cadin/playdate-vscode-template),
[Whitebrim/VSCode-PlaydateTemplate](https://github.com/Whitebrim/VSCode-PlaydateTemplate),
the official [Playdate SDK](https://sdk.play.date/), and Geany’s plugin API.

---

## Requirements

1. **Geany** with plugin support and headers (`geany` / `libgeany-dev` or your
   distro equivalent)
2. **Playdate SDK** — download from <https://play.date/dev/>  
   You need `$PLAYDATE_SDK_PATH/bin/pdc` and `PlaydateSimulator`
3. Build tools: `gcc`, `pkg-config`, GTK3 development libraries

On Arch/CachyOS:

```bash
sudo pacman -S geany gcc pkgconf gtk3
```

---

## Build & install

```bash
git clone https://github.com/YOUR/geany-playdate.git
cd geany-playdate
make
make install    # → ~/.config/geany/plugins/playdate.so
make tags       # optional: pre-install API tags
```

Then in Geany: **Tools → Plugin Manager → Playdate** → enable.

Geany loads native plugins from:

1. `~/.config/geany/plugins/` ← `make install` default
2. `$prefix/lib/geany` (system-wide; use `sudo make install GEANY_LIBDIR=/usr/lib/geany`)

If the plugin does not show up, check **Help → Debug Messages**.

### Rebuild tags from LuaCATS (optional)

```bash
curl -fsSL https://raw.githubusercontent.com/notpeter/playdate-luacats/main/library/stub.lua -o /tmp/stub.lua
python3 tools/luacats_to_tags.py /tmp/stub.lua tags/playdate.lua.tags
python3 tools/embed_tags_header.py    # refresh src/tags_data.h
make clean && make && make install
```

---

## Usage

### Menu: Tools → Playdate

| Action | Default keybinding | Description |
|--------|--------------------|-------------|
| **Build and Run** | `F5` | `pdc` then launch Simulator |
| **Build** | `Ctrl+Shift+B` | compile only |
| **Run in Simulator** | `Ctrl+Shift+R` | open existing `.pdx` |
| **Clean** | `Ctrl+Shift+F5` | delete the output `.pdx` |
| **Open Simulator** | — | Simulator without a game |
| **Install API Tags** | — | write `~/.config/geany/tags/playdate.lua.tags` |

Rebind under **Edit → Preferences → Keybindings → Plugin → playdate**.

### Preferences

**Edit → Preferences → Plugins → Playdate**

| Setting | Default | Notes |
|---------|---------|--------|
| SDK path | *(empty)* | Empty → use `PLAYDATE_SDK_PATH` |
| Source directory | *(empty)* | Empty → auto-detect `Source/` or `source/` under the project root |
| Output `.pdx` | *(empty)* | Empty → existing `*.pdx` in the root, else `Output.pdx` |
| Product name | *(empty)* | Optional; mirrors `name` in `pdxinfo` |
| `pdc` flags | all off | `-s` strip, `--no-compress`, `-v`, `-q`, `-k` skip unknown |

Saved to `~/.config/geany/plugins/geany-playdate/playdate.conf`.

**Empty fields mean auto-detect** — clearing Source/Output in the dialog will
*not* re-insert defaults. That is intentional.

### Project layout

The project root is the directory that **contains** `Source/` or `source/`
(not the source folder itself):

```
MyGame/
├── source/                # or Source/
│   ├── main.lua
│   ├── pdxinfo
│   └── ...
├── support/               # anything else
└── MyGame.pdx/            # output (pdc)
```

Example on disk (this is how the bugfix works):

```
/home/you/Projetos/mysteroids/
├── source/
│   ├── main.lua
│   └── pdxinfo
└── teste.pdx/             # auto-detected when Output is empty
```

Resolved paths:

```
project root = /home/you/Projetos/mysteroids
source       = /home/you/Projetos/mysteroids/source
output       = /home/you/Projetos/mysteroids/teste.pdx   (if Output left empty)
```

### Compiler messages

`pdc` output is parsed with the same shapes as midouest’s problem matchers:

```
warning: /path/to/file.lua:12: unused variable 'x'
error:   /path/to/file.lua:40: unexpected symbol
error:   failed to open 'missing.png'
```

These appear in the **Compiler** tab; double-click jumps to the file and line.

### Autocomplete

After **Tools → Playdate → Install API Tags** (or `make tags`), Geany loads
`~/.config/geany/tags/playdate.lua.tags` for Lua files. You get:

- `playdate.*` global API (update, buttons, crank, timers, graphics, sound, …)
- constructors such as `playdate.graphics.sprite.new(image_or_tilemap)`
- class/instance fields (`_Sprite`, `_Image`, …) and method signatures
- optional extra symbols scraped from `$PLAYDATE_SDK_PATH/CoreLibs/*.lua`

Restart Geany (or reload tags) after installing.

---

## Commands under the hood

```
# Build
$SDK/bin/pdc [-s] [--no-compress] [-v] [-q] [-k] "<source>" "<output>"

# Run
$SDK/bin/PlaydateSimulator "<output>"
```

On macOS the simulator is `Playdate Simulator.app` (use `open`); on Windows
`PlaydateSimulator.exe`. The current implementation targets Linux paths and is
easy to extend in `src/build.c`.

---

## Development

```
geany-playdate/
├── Makefile
├── LICENSE                 # GPL-3.0-or-later
├── THIRD_PARTY.md          # attributions
├── README.md
├── src/
│   ├── playdate.c          # menu, keybindings, configure dialog
│   ├── playdate.h
│   ├── config.c            # prefs + project/source/output resolution
│   ├── build.c             # pdc / Simulator / clean
│   ├── errors.c            # pdc → Compiler tab
│   ├── tags.c              # install API tags
│   └── tags_data.h         # generated (LuaCATS) — do not edit
├── tags/
│   └── playdate.lua.tags   # generated tag file
└── tools/
    ├── luacats_to_tags.py  # stub.lua → playdate.lua.tags
    └── embed_tags_header.py
```

```bash
make            # build playdate.so
make install    # install into ~/.config/geany/plugins
make tags       # install tags into ~/.config/geany/tags
make clean
make uninstall
```

### Manual test checklist

1. `make && make install`, enable the plugin
2. Open a file in `MyGame/source/`
3. **Build** → messages in Compiler tab; errors are clickable
4. **Build and Run** → Simulator opens the game
5. **Clean** → `.pdx` removed
6. Preferences: clear Source/Output, confirm auto-detect still finds `source/`
   and the existing `.pdx`
7. In a `.lua` file, type `playdate.` and confirm completions

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Plugin not listed | Check `~/.config/geany/plugins/playdate.so` exists; Geany 2.x loads from configdir `plugins/` |
| `source directory not found: …/source/Source` | Update plugin — old versions nested the source path twice. Leave Source empty (auto) or set it to `source` |
| SDK not configured | `export PLAYDATE_SDK_PATH=/path/to/PlaydateSDK` or set SDK path in preferences |
| `pdc not found` | Install the Playdate SDK; check `$PLAYDATE_SDK_PATH/bin/pdc` |
| No autocomplete | Tools → Playdate → Install API Tags, then restart Geany |
| Sim does not launch | Ensure `PlaydateSimulator` is executable under `$SDK/bin` |

---

## References

### Inspiration / feature sources

- [orta/vscode-playdate](https://github.com/orta/vscode-playdate) — *Simple Playdate support for VSCode* (MIT)
- [midouest/vscode-playdate-debug](https://github.com/midouest/vscode-playdate-debug) — *Unofficial Playdate debug extension* (MIT)
- [notpeter/playdate-luacats](https://github.com/notpeter/playdate-luacats) — *LuaCATS for Panic PlaydateSDK API* (Apache-2.0 OR MIT)
- [cadin/playdate-vscode-template](https://github.com/cadin/playdate-vscode-template) — VS Code build/run template (macOS)
- [Whitebrim/VSCode-PlaydateTemplate](https://github.com/Whitebrim/VSCode-PlaydateTemplate) — VS Code template (Windows/Linux)

### Official docs & tools

- [Playdate SDK](https://play.date/dev/) / [Inside Playdate](https://sdk.play.date/)
- [Playdate developer help links](https://help.play.date/developer/dev-links/)
- [Geany](https://www.geany.org) / [Plugin API](https://www.geany.org/support/)
- [geany-plugins](https://github.com/geany/geany-plugins)

### Related community tools

- [playdate-types](https://github.com/balpha/playdate-types) — Lua type annotations
- [awesome-playdate](https://github.com/sayhiben/awesome-playdate) — resource list

---

## License

This project is licensed under the **GNU General Public License v3.0 or later**
— see [LICENSE](LICENSE) and [THIRD_PARTY.md](THIRD_PARTY.md).

GPL-3.0-or-later is compatible with Geany (GPL-2.0-or-later) and with the MIT
and Apache-2.0 licensed material incorporated from the reference projects.

Playdate® is a trademark of Panic Inc. This project is unaffiliated.
