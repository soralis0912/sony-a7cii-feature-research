# A7C II port — preparation notes

Status: **preparation only. Nothing in this document is verified on an
A7C II yet.** Every A7 IV finding in this repository stays labelled as an
A7 IV finding until it has been re-derived from A7C II firmware or tested
on a physical A7C II.

## Target

| Item | A7 IV (base research) | A7C II (this port) |
| --- | --- | --- |
| Model | ILCE-7M4 | ILCE-7CM2 |
| Firmware studied | 6.02 | Ver. 2.01 (Sony JP, 2025-11-11) |
| Update file | `BODYDATA.DAT` | `BODYDATA.DAT` (~1.1 GB) |
| SoC | CXD90057 (BIONZ XR) | CXD90057 (BIONZ XR) — same family |
| FDAT model ID | `0x01030081` (verified, 6.02) | **TBD — read from the unpacked 2.01 header** |
| Crypter | `CXD90057_k8` (verified, 6.02) | **TBD — k0 or k8, whichever fwtool reports** |

## Already prepared

- This repository was newly created using
  `leogenot/sony-a7iv-feature-research` (base commit `1258245`, MIT)
  as a template and reference — it is not a fork. See the "参考 /
  Reference" section of the README.
- Firmware unpacking: `soralis0912/fwtool.py`, branch `a7cII`, forked
  from DavidBuchanan314's `a7iv` branch (`3955d78`). It already contains
  the `CXD90057_k0` / `CXD90057_k8` crypters, and the upstream author
  lists ILCE-7CM2 as tested-working for unpacking
  (ma1co/fwtool.py PR #52).
- Local workspace is cloned and runnable (venv with pycryptodomex +
  pyyaml); see the fwtool repository.

## Expected to transfer (hypotheses, to verify)

- The extraction flow in `docs/FIRMWARE_EXTRACTION.md`: fwtool unpack,
  then the `nflasha3 / nflasha7 / nflasha8 / nflasha15` partition layout
  and `lib/appFw.so` as the main application. Same SoC family and the
  same update format make this plausible, not proven.
- The offline analysis tools (`scripts/appfw_elf.py`,
  `scripts/bkid_inventory.py`, `scripts/feature_manager_matrix.py`,
  `scripts/analyze_feature_properties.py`) operate on generic AArch64
  ELF / `BKID_APP_*` structures and are the first candidates for reuse
  unchanged.

## Must NOT be carried over

- **Backup property IDs.** The `0x02cfXXXX` identifiers (121 references
  across docs/scripts/evidence) were derived from the A7 IV 6.02
  `appFw.so` plus an A7 IV backup. This includes the shutter-angle IDs
  `0x02cf1702 / 0x02cf1704`, the custom-LUT ID `0x02cf1443` and the
  de-squeeze candidate `0x02cf1bf2`. None of them may be written to an
  A7C II until the inventory has been rebuilt from A7C II data.
- **Product class.** "A7 IV runs as `PRODUCT_MODEL_LS`" is an A7 IV
  result. The A7C II product class is unknown and decides which feature
  gates (Log Shooting / Flexible ISO, LUT, menus) even apply.
- **All Research status rows** in the README (service mode, settings
  backup, decrypted filesystem read, shutter angle, custom LUT,
  Open Gate, de-squeeze, XAVC S-I DCI 4K): each starts over as
  *untested* for the A7C II.
- **Service-mode authentication.** PMCA authenticated on the A7 IV;
  whether the same flow authenticates an ILCE-7CM2 is untested.
- **Model-specific names/defaults**: `scripts/a7iv_*` filenames and
  defaults, `evidence/feature-manager-a7iv-602.json`, and every
  "6.02" reference (40 across the repo).

## Verification sequence

1. Unpack the official ILCE-7CM2 Ver. 2.01 `BODYDATA.DAT` with the
   fwtool `a7cII` branch. Record model ID, version and crypter name.
   Add the resulting `ILCE-7CM2` entry to `devices.yml` in the fwtool
   fork (no guessed model ID before this step).
2. Confirm the partition layout and hash-match the extracted files
   against the update, as was done for the A7 IV.
3. Determine the A7C II product class from its own `appFw.so`
   (`docs/PRODUCT_CLASS.md` method, A7C II inputs).
4. Test PMCA service mode read-only; save a checksum-valid settings
   backup before any experiment.
5. Rebuild the full property inventory from the A7C II backup +
   `appFw.so`; only then compare against the A7 IV inventory.
6. Port feature experiments one at a time, in the base repo's order,
   re-verifying each on hardware before updating any status table.

## Safety and repository policy (inherited, unchanged)

- No Sony firmware, decrypted binaries, camera backups, serial numbers,
  decryption keys or extracted proprietary files in this repository.
  Obtain the official update yourself and keep generated data local.
- Camera changes operate on persisted backup properties, not a
  repacked firmware update. Test one property at a time and keep the
  original backup and its hashes outside this repository.
- Use at your own risk.
