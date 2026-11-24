#!/usr/bin/env python3
"""Read one fixed ILCE-7CM2 file through the Jiritsu traversal behavior."""

import hashlib
import os
import struct
import sys
from pathlib import Path


def _bootstrap_pmca():
    """Make the pmca package importable.

    Accepts --pmca-root PATH or the PMCA_ROOT environment variable,
    like the PTP scripts. Note: sudo strips PYTHONPATH, so pass the
    root explicitly when running under sudo.
    """
    root = os.environ.get("PMCA_ROOT")
    argv = sys.argv[1:]
    if "--pmca-root" in argv:
        i = argv.index("--pmca-root")
        root = argv[i + 1]
        del argv[i : i + 2]
        sys.argv[1:] = argv
    if root:
        sys.path.insert(0, str(Path(root).expanduser().resolve()))


_bootstrap_pmca()

from pmca.commands.usb import senserShellCommand  # noqa: E402


JIRITSU_CATEGORY = 0x1001
JIRITSU_SET_FILE_PATH = 0x400F
JIRITSU_GET_FILE2 = 0x4011
FIXED_PATH = b"../../usr/share/pmbp/DeviceInfo.xml"
EXPECTED_SHA256_602 = "e44713178fad970870ead845c93abdfcf150c418de11b306da91f2d09d67c1b7"


def probe(camera):
    camera.readHasp()
    set_response = camera._sendAdjustControlPacket(
        JIRITSU_CATEGORY,
        JIRITSU_SET_FILE_PATH,
        b"\x00" + FIXED_PATH,
    )
    if set_response:
        print(
            "SET_FILE_PATH returned %d byte(s): %s"
            % (len(set_response), set_response.hex())
        )

    response = camera._sendAdjustControlPacket(
        JIRITSU_CATEGORY,
        JIRITSU_GET_FILE2,
        b"\x00\xff\x00",
    )
    if len(response) < 4:
        raise RuntimeError(
            "GET_FILE2 response is shorter than its 4-byte status: %r" % response
        )

    status = struct.unpack_from("<I", response)[0]
    payload = response[4:]
    print("GET_FILE2 inner status: 0x%08x" % status)
    print("Returned file bytes: %d" % len(payload))
    if status:
        print("Raw response: %s" % response.hex())
        return

    digest = hashlib.sha256(payload).hexdigest()
    print("SHA256: %s" % digest)
    print(
        "Matches extracted firmware file: %s"
        % ("yes" if digest == EXPECTED_SHA256_602 else "no")
    )
    print(payload.decode("utf-8", errors="replace").rstrip())


if __name__ == "__main__":
    completed = False

    def run(camera):
        global completed
        probe(camera)
        completed = True

    senserShellCommand(complete=run)
    if not completed:
        raise SystemExit("Probe did not run; rerun after the camera reconnects")

