# Sony A7C II firmware and feature research

[日本語版はこちら](README.md)

Use this at your own risk, I am not responsible for any damages.

Reproducible notes and tools for studying Sony **ILCE-7CM2** (A7C II)
firmware **Ver. 2.01** through official update files and Sony's USB
service mode.

> **Status: preparation only.** Nothing has been verified on an
> A7C II yet. See [docs/A7CII_PREP.md](docs/A7CII_PREP.md) for the
> target definition, what may transfer from the A7 IV research, what
> must be re-derived, and the verification sequence.

## Reference

This repository was newly created using
[leogenot/sony-a7iv-feature-research](https://github.com/leogenot/sony-a7iv-feature-research)
(Sony A7 IV 6.02 service-mode, shutter-angle, LUT and firmware
research) as a template and reference. It is not a fork. The repository
layout, documentation structure, analysis scripts and research method
are based on that work; all A7 IV findings credited there belong to
the original author. The original is MIT-licensed, and its copyright
notice is retained in [LICENSE](LICENSE).

Every A7 IV result inherited through the template — backup property
IDs (`0x02cfXXXX`), the `PRODUCT_MODEL_LS` product-class conclusion,
service-mode authentication, and all feature statuses — is an A7 IV
result only. For the A7C II each of them starts over as *untested*
until re-derived from ILCE-7CM2 firmware or tested on physical
ILCE-7CM2 hardware.

## Target

| Item | Value |
| --- | --- |
| Model | ILCE-7CM2 (A7C II) |
| Firmware | Ver. 2.01 (Sony JP, 2025-11-11) |
| Update file | `BODYDATA.DAT` (~1.1 GB, official Sony download) |
| SoC | CXD90057 (BIONZ XR), same family as ILCE-7M4 |
| FDAT model ID | TBD — to be read from the unpacked 2.01 header |
| Crypter | TBD — `CXD90057_k0` or `CXD90057_k8`, as fwtool reports |

## Research status

| Feature | Status |
| --- | --- |
| Firmware unpacking (fwtool, CXD90057) | Prepared — tooling ready, unpack pending |
| Service mode | Untested on ILCE-7CM2 |
| Settings backup | Untested |
| Decrypted filesystem read | Untested |
| Product class | Unknown — to be determined from ILCE-7CM2 `appFw.so` |
| Shutter angle / Custom LUT / De-Squeeze / Open Gate | Untested — A7 IV property IDs must not be reused |

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
docs/       Setup, extraction, service-mode and feature procedures
            (inherited from the template; A7 IV values are marked in
            docs/A7CII_PREP.md and must be re-derived)
scripts/    Read-only backup/dump and offline property-analysis tools
evidence/   Sanitized property mappings and verification record
            (currently the template's A7 IV 6.02 data, for comparison)
```

This repository intentionally contains no Sony firmware, decrypted
binaries, camera backups, serial numbers, decryption keys, or
extracted proprietary files. Obtain the official update yourself and
keep generated data local.

All camera changes documented here operate on persisted backup
properties, not a repacked firmware update. Test one property at a
time and keep the original backup and hashes outside this repository.
