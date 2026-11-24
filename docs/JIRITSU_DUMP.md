# Read-only live filesystem collection

> Status: **read-only probe verified on ILCE-7CM2 (2026-11-24).**
> `a7cii_jiritsu_readonly_probe.py` returned `/usr/share/pmbp/DeviceInfo.xml`
> with inner status 0, 517 bytes, SHA-256
> `e44713178fad970870ead845c93abdfcf150c418de11b306da91f2d09d67c1b7` —
> identical to the file in the extracted 2.01 firmware. The full
> recursive dump (`a7cii_jiritsu_dump.py`) remains untested.

## Finding

In service mode, Jiritsu command `SET_FILE_PATH` accepts a path containing
parent-directory components. `GET_FILE2` then returns the referenced file.
The service constructs a path beneath `/tmp/jiritsu`; prefixing an absolute
target with `../../` resolves back to the Linux root.

The command constants, read out of the definition table in
`libsencore.so` by `scripts/jiritsu_commands.py` (not guessed from ordering —
each record holds a little-endian u32 of `(command << 16) | category`):

```text
category: 0x1001   (every command)
0x4001 MODE           0x4002 MOUNT          0x4003 FORMAT
0x4004 START          0x4005 DEBUG          0x4006 FIRMUP
0x4007 SET_FILE       0x4008 GET_FILE       0x4009 FILE_DELETE
0x400a GET_FILELIST   0x400b GET_FILE_HASH  0x400c COMPARE_MEDIA
0x400d GET_VERSION    0x400e FACTORY        0x400f SET_FILE_PATH
0x4010 SET_FILE2      0x4011 GET_FILE2      0x4012 FILE_DELETE2
```

`0x400f` and `0x4011` are confirmed by the probe that ran on hardware.
The rest come from the same table and are not verified on a camera. Note what
sits next to them: `FORMAT`, `FIRMUP`, `FILE_DELETE` and `FILE_DELETE2` are
destructive, so a mistyped command number is not a harmless experiment.

Jiritsu is reached through PFUNC `0x40` AdjustControl, which `libsencore.so`
lists in all three service dispatch tables (levels A, B and C). A working
Jiritsu call therefore says nothing about the privilege level; `TestMode`
(`0xff00`), which is level A only, is a different path.

The included tools issue only path-selection and read commands. They do not
write or delete camera files.

## Fixed probe

Copy the probe into Sony-PMCA-RE:

```bash
cp ~/Documents/sony-a7cii-feature-research/scripts/a7cii_jiritsu_readonly_probe.py \
  ~/Documents/Sony-PMCA-RE/
cd ~/Documents/Sony-PMCA-RE
sudo ./venv/bin/python ./a7cii_jiritsu_readonly_probe.py
```

It reads only:

```text
/usr/share/pmbp/DeviceInfo.xml
```

On ILCE-7CM2, record the returned file's size and SHA-256 and compare
them against the same path in the extracted Ver. 2.01 update.

## Update-backed collection

The collector builds its remote manifest from the extracted official update,
downloads only regular files represented there and checks every returned file
against the update's size and SHA-256.

```bash
cp ~/Documents/sony-a7cii-feature-research/scripts/a7cii_jiritsu_dump.py \
  ~/Documents/Sony-PMCA-RE/
cd ~/Documents/Sony-PMCA-RE
sudo ./venv/bin/python ./a7cii_jiritsu_dump.py \
  --fwtool-root ~/Documents/fwtool.py
```

Use `--all` for all update-backed regular files:

```bash
sudo ./venv/bin/python ./a7cii_jiritsu_dump.py \
  --fwtool-root ~/Documents/fwtool.py \
  --all
```

The manifest is built from the extracted ILCE-7CM2 Ver. 2.01 update, so
its file count and total size are whatever that update contains; record
the numbers from the first successful run here.

The output is resumable through `dump-index.jsonl`. Do not commit or upload the
resulting Sony files.

