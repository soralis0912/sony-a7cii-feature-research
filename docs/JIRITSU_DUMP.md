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

The command constants to verify first on ILCE-7CM2 are:

```text
category:      0x1001
SET_FILE_PATH: 0x400f
GET_FILE2:     0x4011
```

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

