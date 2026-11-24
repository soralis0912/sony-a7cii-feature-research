#!/usr/bin/env python3
"""List the Jiritsu service commands defined in libsencore.so.

Each command has a record in libsencore.so holding its name and, three bytes
before the name's '@', a little-endian u32 of (command << 16) | category. The
'@' that starts every name is the u32's top byte, so the pair reads straight
out of the table rather than being inferred from ordering.

Two of the values this prints are confirmed by hardware: the read-only probe
that worked on 2026-11-24 used category 0x1001 with SET_FILE_PATH 0x400f and
GET_FILE2 0x4011.

Usage:
  python3 scripts/jiritsu_commands.py <p15>/lib/libsencore.so [--json FILE]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import re
import struct

NAME = re.compile(rb"@JIRITSU_([A-Z0-9_]+)\x00")
# the library carries the table twice; the first copy is the one to read
SECOND_COPY = 0x40000

WRITES = {"SET_FILE", "SET_FILE2", "FILE_DELETE", "FILE_DELETE2", "FORMAT",
          "MOUNT", "FIRMUP", "FACTORY", "COMPARE_MEDIA", "MODE", "START",
          "DEBUG"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("library", type=pathlib.Path, help="<p15>/lib/libsencore.so")
    ap.add_argument("--json", type=pathlib.Path, default=None)
    args = ap.parse_args()

    if not args.library.is_file():
        print("no such file: %s" % args.library)
        return 2
    blob = args.library.read_bytes()
    rows = []
    for m in NAME.finditer(blob):
        off = m.start()
        if off > SECOND_COPY:
            continue
        packed = struct.unpack_from("<I", blob, off - 3)[0]
        rows.append({"command": packed >> 16, "category": packed & 0xFFFF,
                     "name": m.group(1).decode(), "name_offset": off})
    rows.sort(key=lambda r: r["command"])

    print("%s\nsha256 %s\n" % (args.library, hashlib.sha256(blob).hexdigest()))
    print("%-9s %-9s %-22s %s" % ("command", "category", "name", "reads/writes"))
    for r in rows:
        kind = "writes" if r["name"] in WRITES else "reads"
        print("%#06x    %#06x    %-22s %s" % (r["command"], r["category"],
                                              r["name"], kind))
    cmds = [r["command"] for r in rows]
    if cmds:
        print("\n%d commands, %#06x..%#06x, contiguous: %s"
              % (len(cmds), cmds[0], cmds[-1],
                 cmds == list(range(cmds[0], cmds[-1] + 1))))
        cats = {r["category"] for r in rows}
        print("categories: %s" % ", ".join(hex(c) for c in sorted(cats)))

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(
            {"library": str(args.library),
             "sha256": hashlib.sha256(blob).hexdigest(),
             "commands": [{**r, "command": hex(r["command"]),
                           "category": hex(r["category"]),
                           "name_offset": hex(r["name_offset"])} for r in rows]},
            indent=2) + "\n")
        print("\nwrote %s" % args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
