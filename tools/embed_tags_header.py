#!/usr/bin/env python3
"""Regenerate src/tags_data.h from tags/playdate.lua.tags."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAGS = ROOT / "tags" / "playdate.lua.tags"
OUT = ROOT / "src" / "tags_data.h"


def main() -> int:
    if not TAGS.is_file():
        print(f"missing {TAGS} — run tools/luacats_to_tags.py first")
        return 1
    lines = TAGS.read_text(encoding="utf-8").splitlines(True)
    parts = [
        "/* Generated from notpeter/playdate-luacats stub.lua — do not edit by hand. */\n",
        "#ifndef PD_TAGS_DATA_H\n#define PD_TAGS_DATA_H\n\n",
        "static const char PD_TAGS_DATA[] =\n",
    ]
    for ln in lines:
        esc = ln.replace("\\", "\\\\").replace('"', '\\"').rstrip("\n")
        parts.append(f'"{esc}\\n"\n')
    parts.append(";\n\n#endif\n")
    OUT.write_text("".join(parts), encoding="utf-8")
    print(f"wrote {OUT} ({OUT.stat().st_size} bytes, {len(lines)} tag lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
