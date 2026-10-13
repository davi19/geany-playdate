# Forum post — copy & paste

**Forum:** https://devforum.play.date/  
**Suggested category:** Developer Discussion → Tools / IDEs  
**Suggested title:**

```text
geany-playdate — Playdate support for the ancient artifact known as Geany
```

---

Hey folks!

I wrote a plugin that drags the ancient artifact known as **Geany** (yes, it still boots in 2026; yes, it still opens faster than your browser) into the Playdate world.

Some people want a fancy IDE. Some of us just want an editor that opens before the coffee maker finishes and doesn’t eat 2 GB of RAM. Geany is that editor — and by “that editor” I mean it’s been around so long it probably has a Playdate of its own.

## What you get

- **Build and Run** — one shortcut: `pdc` + Simulator. No Electron required, no 30-second “Activating extensions…” spinner. Just a menu item like a civilized 2005 workflow.
- **Build** / **Run** / **Clean** / **Open Simulator**
- **`pdc` errors in the Compiler tab** — double-click, jump to the line. Geany’s had this Compiler tab since before half of you were writing Lua. It’s old. It works. It is the grandparent of your fancy problem matchers.
- **Preferences** for SDK path, source/output (empty = auto-detect), and `pdc` flags
- **API autocomplete** — ~1800 tags for `playdate.*`, generated from [playdate-luacats](https://github.com/notpeter/playdate-luacats)

Yes, autocomplete. In Geany. The timeline is healing.

It understands the usual `MyGame/source/` + `pdxinfo` layout (and it won’t go looking for `source/Source` like a confused grandparent — that bug is fixed).

## Install (Linux, aka Geany’s natural habitat)

```bash
git clone https://github.com/davi19/geany-playdate.git
cd geany-playdate
make && make install
```

**Tools → Plugin Manager → Playdate**.

Yes, Geany has a plugin system. It predates VS Code extensions by about a decade. We called it “plugins” before it was cool. Get off my lawn.

`F5` = Build and Run (you can rebind it; Geany’s keybinding dialog is also ancient and still fine).

## Why Geany?

Because I can:

- compile a game and open the Simulator before VS Code finishes showing its welcome tab
- leave Geany open for three weeks without it updating itself into a new UI
- run it on a laptop that also runs the Playdate Simulator without the fan achieving flight

Also: if your IDE needs 12 extensions to open a `.lua` file, you don’t have a toolchain, you have a dependency.

## Credits

This is a Geany port of the best parts of the VS Code ecosystem — the kids’ table did good research:

- [orta/vscode-playdate](https://github.com/orta/vscode-playdate) — Build+Run UX and SDK resolution
- [midouest/vscode-playdate-debug](https://github.com/midouest/vscode-playdate-debug) — `pdc` problem matchers (Geany’s Compiler tab walked so these matchers could run)
- [notpeter/playdate-luacats](https://github.com/notpeter/playdate-luacats) — typed API stub → Geany tags

Also: official [Playdate SDK](https://sdk.play.date/), [Whitebrim](https://github.com/Whitebrim/VSCode-PlaydateTemplate) and [cadin](https://github.com/cadin/playdate-vscode-template) templates.

**Repo:** https://github.com/davi19/geany-playdate  
GPL-3.0-or-later. Unaffiliated with Panic, but Geany might be affiliated with dirt — it’s that old.

## Still missing

- Debugging (Geany’s debugger plugin is also from the Jurassic; one thing at a time)
- An AI autocomplete tab (we have a status bar instead; it does one job)

PRs, issues, and “back in my day we used `ed`” comments are welcome.

Cheers!
