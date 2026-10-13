#!/usr/bin/env python3
"""Generate Geany playdate.lua.tags from playdate-luacats stub.lua.

Usage:
    python3 tools/luacats_to_tags.py [stub.lua] [out.tags]

Default stub: /tmp/luacats/stub.lua  (or pass a path / URL-downloaded file)
Default out:  tags/playdate.lua.tags

Extracts:
  - function definitions: function playdate.foo.bar(a, b)
  - table/module roots:   playdate.graphics = {}
  - class/field names from ---@class / ---@field (as variables)
  - instance methods on _Sprite etc. mapped to sprite:method style
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FN_DEF = re.compile(
    r"^function\s+([A-Za-z_][\w.]*[:.]?[\w]*)\s*\(([^)]*)\)"
)
TABLE = re.compile(r"^([A-Za-z_][\w.]*)\s*=\s*\{\s*\}")
CLASS = re.compile(r"^---@class\s+(\S+)")
FIELD = re.compile(r"^---@field\s+(\S+)")
LOCAL_CLASS = re.compile(r"^local\s+(_\w+)\s*=\s*\{\s*\}")


def norm_params(raw: str) -> str:
    raw = re.sub(r"\s+", " ", raw.strip())
    return raw


def tag(out: list[str], name: str, kind: str, sig: str | None = None) -> None:
    line = f"{name}\t/PlaydateSDK\t1;\"\tkind:{kind}"
    if sig is not None:
        line += f"\tsignature:({sig})"
    out.append(line)


def convert(stub: str) -> list[str]:
    out: list[str] = [
        "!_TAG_FILE_FORMAT\t2\t/extended format/",
        "!_TAG_FILE_SORTED\t0\t/0=unsorted/",
    ]
    seen: set[str] = set()
    current_class: str | None = None
    # map short instance type → official method prefix, e.g. _Sprite → playdate.graphics.sprite
    class_to_ns: dict[str, str] = {
        "_Sprite": "playdate.graphics.sprite",
        "_Image": "playdate.graphics.image",
        "_ImageTable": "playdate.graphics.imagetable",
        "_Timer": "playdate.timer",
        "_FrameTimer": "playdate.frameTimer",
        "_Font": "playdate.graphics.font",
        "_NineSlice": "playdate.graphics.nineslice",
        "_TileMap": "playdate.graphics.tilemap",
        "_Animator": "playdate.graphics.animator",
        "_AnimationLoop": "playdate.graphics.animation.loop",
        "_Blinker": "playdate.graphics.animation.blinker",
        "_SamplePlayer": "playdate.sound.sampleplayer",
        "_FilePlayer": "playdate.sound.fileplayer",
        "_Synth": "playdate.sound.synth",
        "_Channel": "playdate.sound.channel",
        "_Sequence": "playdate.sound.sequence",
        "_Track": "playdate.sound.track",
        "_Sample": "playdate.sound.sample",
        "_Instrument": "playdate.sound.instrument",
        "_File": "playdate.file.file",
        "_Point": "playdate.geometry.point",
        "_Rect": "playdate.geometry.rect",
        "_Arc": "playdate.geometry.arc",
        "_Polygon": "playdate.geometry.polygon",
        "_LineSegment": "playdate.geometry.lineSegment",
        "_Vector2D": "playdate.geometry.vector2D",
        "_AffineTransform": "playdate.geometry.affineTransform",
        "_PathFinderGraph": "playdate.pathfinder.graph",
        "_PathFinderNode": "playdate.pathfinder.node",
    }

    def add(name: str, kind: str, sig: str | None = None) -> None:
        key = f"{name}|{kind}"
        if key in seen:
            return
        seen.add(key)
        tag(out, name, kind, sig)

    for raw in stub.splitlines():
        line = raw.rstrip()

        m = CLASS.match(line)
        if m:
            current_class = m.group(1).split(":")[0]
            add(current_class, "class")
            continue

        m = FIELD.match(line)
        if m and current_class:
            add(m.group(1), "field")
            # also expose as Class.field
            add(f"{current_class}.{m.group(1)}", "field")
            continue

        m = LOCAL_CLASS.match(line)
        if m:
            current_class = m.group(1)
            add(current_class, "class")
            continue

        m = FN_DEF.match(line)
        if m:
            name, params = m.group(1), norm_params(m.group(2))
            add(name, "function", params)

            # instance methods declared as function _Sprite:moveTo(...)
            # also emit sprite:moveTo / playdate.graphics.sprite:moveTo
            if ":" in name:
                obj, meth = name.split(":", 1)
                if obj in class_to_ns:
                    ns = class_to_ns[obj]
                    add(f"{ns}:{meth}", "function", params)
                    add(f"{ns}.{meth}", "function", params)
                    # bare method name for call-tip style autocomplete
                    add(meth, "function", params)
            continue

        m = TABLE.match(line)
        if m:
            add(m.group(1), "variable")
            continue

    # always include the globals people type first
    for extra, kind, sig in [
        ("import", "function", "path"),
        ("playdate", "variable", None),
        ("playdate.update", "function", ""),
    ]:
        add(extra, kind, sig)

    return out


def main() -> int:
    stub_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/luacats/stub.lua")
    out_path = (
        Path(sys.argv[2])
        if len(sys.argv) > 2
        else Path(__file__).resolve().parent.parent / "tags" / "playdate.lua.tags"
    )

    if not stub_path.is_file():
        print(f"error: stub not found: {stub_path}", file=sys.stderr)
        print("download with:", file=sys.stderr)
        print(
            "  curl -fsSL https://raw.githubusercontent.com/notpeter/playdate-luacats/main/library/stub.lua -o stub.lua",
            file=sys.stderr,
        )
        return 1

    lines = convert(stub_path.read_text(encoding="utf-8"))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {len(lines)} lines → {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
