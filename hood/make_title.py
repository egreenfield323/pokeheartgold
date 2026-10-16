#!/usr/bin/env python3
"""Drip for the 3D Ho-Oh on the title screen: sunglasses (its eye texture) and a gold grill
(its mouth texture). Edits titledemo_00000025.NSBMD in place; originals come from git HEAD.

The title-screen Lugia has no face texture (it is vertex-coloured), so it is left alone.
"""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nsbtx  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
HOOH = "files/demo/title/titledemo/titledemo_00000025.NSBMD"


def spare(rows, n):
    used = {v for r in rows for v in r}
    free = [i for i in range(15, 0, -1) if i not in used]
    assert len(free) >= n, "no spare palette slots"
    return free[:n]


def main():
    data = subprocess.run(["git", "show", f"HEAD:{HOOH}"], cwd=ROOT, capture_output=True, check=True).stdout
    b, texs, pals = nsbtx.parse(data)
    tex = {t["name"]: t for t in texs}
    pal = {p["name"]: p for p in pals}

    # sunglasses over the eye: dark lens, glint, and a frame bar across the brow
    t, p = tex["hou_eye"], pal["hou_eye_pl"]
    rows = nsbtx.get_pixels(b, t)
    cols = nsbtx.get_palette(b, p)
    lens, frame, glint = spare(rows, 3)
    cols[lens], cols[frame], cols[glint] = (24, 24, 32), (8, 8, 8), (200, 210, 230)
    cx, cy, r = 28, 28, 15
    for y in range(t["h"]):
        for x in range(t["w"]):
            d2 = (x - cx) ** 2 + (y - cy) ** 2
            if d2 <= r * r:
                rows[y][x] = frame if d2 > (r - 2) ** 2 else lens
            if 11 <= y <= 14 and 4 <= x <= 52:
                rows[y][x] = frame
    for k in range(-6, 3):                       # diagonal glint
        for w in (0, 1):
            rows[cy - 4 + k][cx + 4 - k + w] = glint
    nsbtx.set_pixels(b, t, rows)
    nsbtx.set_palette(b, p, cols)

    # gold grill along the inside of the beak
    t, p = tex["hou_mouth01"], pal["hou_mouth01_pl"]
    rows = nsbtx.get_pixels(b, t)
    cols = nsbtx.get_palette(b, p)
    gold, shade = spare(rows, 2)
    cols[gold], cols[shade] = (248, 208, 56), (168, 112, 24)
    for y in range(1, 41):
        for x in range(15, 21):
            rows[y][x] = shade if (y % 5 == 0 or x == 20) else gold
    nsbtx.set_pixels(b, t, rows)
    nsbtx.set_palette(b, p, cols)

    (ROOT / HOOH).write_bytes(bytes(b))
    print("title-screen Ho-Oh: shades + gold grill")


if __name__ == "__main__":
    main()
