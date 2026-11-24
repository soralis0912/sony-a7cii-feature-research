#!/usr/bin/env python3
"""Enumerate every feature-manager getter in appFw.so, named or not.

`feature_manager_matrix.py` finds the parameters whose `PRM_FEATURE_MANAGER_*`
name survives in the binary. There are more than that. Each parameter is a
six-instruction stub of the shape

    adrp x0, <page>          ; ldrsw x1, [x0, #0x5b0]   <- the product class index
    adrp x0, <page>          ; add   x0, x0, #<off>     <- this parameter's table
    ldr  w0, [x0, x1, lsl #2]; ret                      <- table[class]

so the stubs can be found by shape and their tables read per class, whether or
not a name is left for them. This also counts how many places call each one,
which says how much of the firmware's behaviour is split by product class.

The class index itself is a 32-bit global; its address is printed.

  python3 scripts/feature_manager_getters.py <p15>/lib/appFw.so \
      --evidence evidence/feature-manager-a7cii-201.json \
      --json evidence/feature-manager-getters-a7cii-201.json
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import struct

RET = 0xD65F03C0
SCAN_FROM, SCAN_TO = 0x1797000, 0x179A000     # the stub block in 2.01
CLASS_SLOT = 0x5B0                            # [class-index global + 0x5b0]
CLASS_COUNT = 26


def sections(blob: bytes) -> dict[str, tuple[int, int, int]]:
    shoff = struct.unpack_from("<Q", blob, 0x28)[0]
    shent, shnum, shstrndx = struct.unpack_from("<HHH", blob, 0x3A)
    names = struct.unpack_from("<Q", blob, shoff + shstrndx * shent + 0x18)[0]
    out = {}
    for i in range(shnum):
        b = shoff + i * shent
        at = names + struct.unpack_from("<I", blob, b)[0]
        name = blob[at:blob.index(b"\0", at)].decode("latin1")
        addr, off, size = struct.unpack_from("<QQQ", blob, b + 0x10)
        out[name] = (addr, off, size)
    return out


def adrp_target(word: int, pc: int) -> int:
    imm = (((word >> 5) & 0x7FFFF) << 2) | ((word >> 29) & 3)
    if imm & (1 << 20):
        imm -= 1 << 21
    return (pc & ~0xFFF) + imm * 0x1000


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("appfw", type=pathlib.Path)
    ap.add_argument("--evidence", type=pathlib.Path, default=None,
                    help="feature-manager matrix JSON, to label the named ones")
    ap.add_argument("--json", type=pathlib.Path, default=None)
    ap.add_argument("--dump", type=lambda s: int(s, 16), default=None,
                    help="print one stub's per-class values (stub address)")
    args = ap.parse_args()

    blob = args.appfw.read_bytes()
    mv = memoryview(blob)
    secs = sections(blob)
    text_addr, _, text_size = secs[".text"]

    def word(addr: int) -> int:
        return int.from_bytes(mv[addr:addr + 4], "little")

    stubs: dict[int, int] = {}
    class_global = None
    a = SCAN_FROM
    while a < SCAN_TO:
        w = [word(a + 4 * i) for i in range(6)]
        if (w[5] == RET and (w[1] >> 24) == 0xB9 and (w[4] >> 24) == 0xB8
                and (w[1] >> 10 & 0xFFF) == CLASS_SLOT // 4):
            stubs[a] = adrp_target(w[2], a + 8) + ((w[3] >> 10) & 0xFFF)
            if class_global is None:
                class_global = adrp_target(w[0], a) + CLASS_SLOT
        a += 4

    names = {}
    if args.evidence and args.evidence.is_file():
        for row in json.loads(args.evidence.read_text())["rows"]:
            names[int(row["getter"], 16)] = row["name"].replace(
                "PRM_FEATURE_MANAGER_", "")

    sites = collections.defaultdict(list)
    for off in range(0, text_size - 3, 4):
        at = text_addr + off
        w = word(at)
        if (w >> 26) == 0x25:
            imm = w & 0x3FFFFFF
            if imm & 0x2000000:
                imm -= 0x4000000
            target = at + imm * 4
            if target in stubs:
                sites[target].append(at)

    print("%s\nproduct-class index global: %s" %
          (args.appfw, hex(class_global) if class_global else "(not found)"))
    print("getter stubs: %d (%#x..%#x), named in the evidence: %d"
          % (len(stubs), min(stubs), max(stubs),
             sum(1 for s in stubs if s in names)))
    print("call sites: %d across %d stubs\n"
          % (sum(len(v) for v in sites.values()), len(sites)))

    if args.dump is not None:
        table = stubs.get(args.dump)
        if table is None:
            print("no stub at %#x" % args.dump)
            return 1
        values = struct.unpack_from("<%di" % CLASS_COUNT, blob, table)
        print("stub %#x  table %#x  %s" % (args.dump, table,
                                           names.get(args.dump, "(unnamed)")))
        for i, v in enumerate(values):
            print("   class %2d: %d" % (i, v))
        return 0

    print("%-12s %-12s %-30s %s" % ("stub", "table", "name", "call sites"))
    for stub in sorted(stubs):
        print("%#011x %#011x %-30s %d"
              % (stub, stubs[stub], names.get(stub, "(unnamed)"),
                 len(sites.get(stub, ()))))

    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps({
            "appfw": str(args.appfw),
            "class_index_global": hex(class_global) if class_global else None,
            "class_count": CLASS_COUNT,
            "getters": [{
                "stub": hex(s), "table": hex(stubs[s]),
                "name": names.get(s),
                "call_sites": len(sites.get(s, ())),
                "values": list(struct.unpack_from("<%di" % CLASS_COUNT, blob,
                                                  stubs[s])),
            } for s in sorted(stubs)],
        }, indent=2) + "\n")
        print("\nwrote %s" % args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
