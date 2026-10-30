"""Testing the catching items' throws with just Nap Sacks: re-skin the Nap Sack (Poké Ball row) as another
tier on the built, padded ROM, so one savestate shows every look.

    python -I hood/test/ball_look.py ROW [rom]     ROW 0 Whole Gang, 1 Rug Roll, 2 Duffel Bag, 3 Nap Sack ...

Only a/0/0/8 and a/0/9/5 are redone (from the original game's files), then the ROM is padded again: same layout,
so the savestate still loads.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import ndspy.rom  # noqa: E402

import ballfx  # noqa: E402
import battlefx  # noqa: E402

BASE = "C:/Users/Evan/Documents/dsume/Roms/4840 - Pokemon - SoulSilver Version (v10) (E).nds"


def main():
    look = int(sys.argv[1])
    path = sys.argv[2] if len(sys.argv) > 2 else str(HERE.parents[1] / "hood-soulsilver.nds")
    rom = ndspy.rom.NintendoDSRom.fromFile(path)
    base = ndspy.rom.NintendoDSRom.fromFile(BASE)
    for p in ("a/0/0/8", "a/0/9/5"):
        rom.setFileByName(p, base.getFileByName(p))
    ballfx.LOOK = {3: look}
    ballfx.patch(rom)
    battlefx.pad(rom, only=("a/0/0/8", "a/0/9/5"))
    rom.saveToFile(path)
    print("Nap Sack looks like row", look, "->", path)


if __name__ == "__main__":
    main()
