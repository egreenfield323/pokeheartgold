#!/usr/bin/env python3
"""Gun-named moves borrow existing projectile animations (move animation scripts, files/a/0/1/0,
one member per move id). Each script loads its own particles and sounds, so copying a whole
member is self-contained. Originals come from git HEAD.
Run from the repo root:  python hood/make_anims.py
"""
import re
import subprocess
import sys
from pathlib import Path

import ndspy.narc

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = "files/a/0/1/0"

# original move name -> original move whose animation it should use
REMAP = {
    "Tackle": "Bullet Seed",        # FMJ
    "Crunch": "Bullet Seed",        # Hollow Point
    "Double Kick": "Bullet Seed",   # Double Tap
    "Triple Kick": "Bullet Seed",   # Triple Tap
    "Iron Head": "Pin Missile",     # Steel Core
    "Fury Attack": "Pin Missile",   # Spray n Pray
}


def move_ids():
    gmm = subprocess.run(["git", "show", "HEAD:files/msgdata/msg/msg_0750.gmm"], cwd=ROOT,
                         capture_output=True, check=True).stdout.decode("utf-8")
    return {m.group(2): int(m.group(1)) for m in re.finditer(r'index="(\d+)".*?English">(.*?)</language>', gmm, re.S)}


def main():
    ids = move_ids()
    narc = ndspy.narc.NARC(subprocess.run(["git", "show", f"HEAD:{ARCHIVE}"], cwd=ROOT,
                                          capture_output=True, check=True).stdout)
    for dst, src in REMAP.items():
        narc.files[ids[dst]] = narc.files[ids[src]]
    (ROOT / ARCHIVE).write_bytes(narc.save())
    print(f"move animations: {len(REMAP)} gun moves remapped")


if __name__ == "__main__":
    main()
