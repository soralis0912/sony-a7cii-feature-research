# Read-only live filesystem collection

> Status: **untested on ILCE-7CM2.** The traversal behavior and the
> constants below are the working hypothesis for the first session;
> they have not been confirmed against ILCE-7CM2 hardware yet.

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

