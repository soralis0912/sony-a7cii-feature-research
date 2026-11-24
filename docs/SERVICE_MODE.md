# Service mode and backup workflow

> Status: **untested on ILCE-7CM2.** The workflow below is the procedure
> to follow for the first physical-camera session; no backup from an
> ILCE-7CM2 has been taken yet.

## Enter service mode

```bash
cd ~/Documents/Sony-PMCA-RE
sudo ./venv/bin/python ./pmca-console.py serviceshell
```

Useful shell commands include:

```text
info
bk r <ID>
bk w <ID> <HEX_DATA>
bk s
exit
```

`bk r` reads a persisted backup property. `bk w` changes its in-memory value.
`bk s` synchronizes changes to persistent storage.

## Save a backup first

Copy the supplied helper into the PMCA repository or invoke it with that
repository on `PYTHONPATH`:

```bash
cp ~/Documents/sony-a7cii-feature-research/scripts/a7cii_read_backup.py \
  ~/Documents/Sony-PMCA-RE/
cd ~/Documents/Sony-PMCA-RE
sudo ./venv/bin/python ./a7cii_read_backup.py ./a7cii-backup.bin
```

The script refuses to overwrite an existing output. Keep the resulting file
private. It can contain per-camera state and identifiers.

Record a second external hash if desired:

```bash
shasum -a 256 ./a7cii-backup.bin
```

Record the backup's size and SHA-256 locally. Camera backups can contain
per-camera state and identifiers, so do not publish them as reusable artifacts.

## Apply one change at a time

For each experiment:

1. Read and record the original property.
2. Write one documented value.
3. Run `bk s`.
4. Exit the shell.
5. Turn the camera off and disconnect USB.
6. Remove the battery for ten seconds.
7. Reinsert it and test the behavior.
8. Restore the original value before testing an unrelated property.

This produces an interpretable result and a direct rollback path.

