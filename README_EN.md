# Sony A7C II firmware and feature research

[日本語版はこちら](README.md)

Use this at your own risk, I am not responsible for any damages.

Reproducible notes and tools for studying Sony **ILCE-7CM2** (A7C II)
firmware **Ver. 2.01** through official update files and Sony's USB
service mode.

> **Status: firmware unpacking verified; physical-camera work
> (service mode etc.) not yet tested.** See
> [docs/A7CII_PREP.md](docs/A7CII_PREP.md) for the target definition
> and the research plan and progress.

## Reference

This repository was newly created using
[leogenot/sony-a7iv-feature-research](https://github.com/leogenot/sony-a7iv-feature-research)
(Sony A7 IV 6.02 service-mode, shutter-angle, LUT and firmware
research) as a template and reference. It is not a fork. The repository
layout, documentation structure, analysis scripts and research method
are based on that work; all A7 IV findings credited there belong to
the original author. The original is MIT-licensed, and its copyright
notice is retained in [LICENSE](LICENSE).

All values recorded in this repository come from ILCE-7CM2 firmware
or hardware only. The other model's findings documents that came with
the template have been removed, and the content is being replaced
with ILCE-7CM2 material.

## Target

| Item | Value |
| --- | --- |
| Model | ILCE-7CM2 (A7C II) |
| Firmware | Ver. 2.01 (Sony JP, 2025-11-11) |
| Update file | `BODYDATA.DAT` (~1.1 GB, official Sony download) |
| SoC | CXD90057 (BIONZ XR) |
| FDAT model ID | `0x20030014` (verified by unpacking 2.01) |
| Crypter | `CXD90057_k8` (verified by unpacking 2.01) |

## Research status

| Feature | Status |
| --- | --- |
| Firmware unpacking (fwtool, CXD90057) | **Verified** — official 2.01 `BODYDATA.DAT` unpacked (model `0x20030014`, crypter `CXD90057_k8`) |
| Service mode | Untested on ILCE-7CM2 |
| Settings backup | Untested |
| Decrypted filesystem read | Untested |
| Product class | Analyzed — 26-class matrix decoded; which class the camera runs needs hardware (docs/PRODUCT_CLASS.md) |
| Shutter angle / Custom LUT / De-Squeeze | Property IDs identified from ILCE-7CM2 firmware (docs/FEATURE_INVENTORY.md); on-camera change tests not yet done |

## Upstream and related projects

- [leogenot/sony-a7iv-feature-research](https://github.com/leogenot/sony-a7iv-feature-research):
  the template and reference for this repository (A7 IV research).
- [ma1co/Sony-PMCA-RE](https://github.com/ma1co/Sony-PMCA-RE):
  USB service-mode transport and backup shell.
- [soralis0912/fwtool.py](https://github.com/soralis0912/fwtool.py/tree/a7cII),
  branch `a7cII`: Sony firmware unpacking with CXD90057 support,
  forked from DavidBuchanan314's `a7iv` branch of fwtool.py.
- [ma1co/fwtool.py PR #52](https://github.com/ma1co/fwtool.py/pull/52):
  upstream CXD90057 extraction work; ILCE-7CM2 listed as tested.

## Repository layout

```
docs/       Setup, extraction (verified), service-mode and live
            filesystem-read procedures, and the research plan
scripts/    Read-only backup/dump and offline property-analysis
            tools (renamed to a7cii_*)
evidence/   Sanitized property mappings and verification record
            (to be added once ILCE-7CM2 data exists)
```

This repository intentionally contains no Sony firmware, decrypted
binaries, camera backups, serial numbers, decryption keys, or
extracted proprietary files. Obtain the official update yourself and
keep generated data local.

All camera changes documented here operate on persisted backup
properties, not a repacked firmware update. Test one property at a
time and keep the original backup and hashes outside this repository.
