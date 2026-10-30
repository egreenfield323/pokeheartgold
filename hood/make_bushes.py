#!/usr/bin/env python3
"""Apricorn trees -> bushes. In Hood HeartGold the apricorns are material scraps (Gator Hide, Velvet Scrap ...)
that people stash in bushes, and Kurt stitches custom bags out of them; you dig through the bush instead of
shaking a tree.

    python hood/make_bushes.py                    # rewrite the NSBTX textures in place
    python hood/make_bushes.py --preview out.png  # contact sheet only

mmodel 251 is the empty bush (7 frames), 252-258 the bushes with something stashed in them (3 frames each),
259-265 the scrap you pull out. Each texture keeps its size and palette length; originals are read from the base
commit 77565981b, so re-running is safe.
"""
import random
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nsbtx  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MMODEL = "files/data/mmodel/mmodel/mmodel_%08d.NSBTX"
BASE = "77565981b"

OUT = (20, 40, 20)
LEAF, LEAF_D, LEAF_L = (50, 120, 50), (30, 80, 35), (100, 170, 80)
# colour letter -> (mmodel bush, mmodel scrap, material colour, its dark shade, accent): the same materials as
# the bags (ballfx.MATERIAL)
SCRAPS = {"b": (252, 259, (40, 90, 70), (20, 55, 40), (90, 150, 110)),          # Croc Hide
          "bk": (253, 260, (60, 90, 150), (35, 55, 100), (240, 150, 40)),       # Denim Scrap: orange stitching
          "g": (254, 261, (170, 120, 70), (120, 80, 45), (200, 160, 110)),      # Suede Scrap
          "r": (255, 262, (110, 130, 50), (70, 85, 30), (150, 170, 80)),        # Gator Hide
          "w": (256, 263, (40, 70, 180), (25, 40, 120), (250, 250, 250)),       # Nylon Scrap: white stripe
          "p": (257, 264, (140, 20, 75), (90, 10, 45), (200, 80, 130)),         # Velvet Scrap
          "y": (258, 265, (200, 200, 225), (140, 140, 170), (255, 255, 255))}   # Satin Scrap


def _bush(d, seed, squash=1.0, grow=0):
    """A scraggly hedge sitting on the bottom of a 32x32 frame: lumpy clumps, a dark underside, a few lighter
    leaves on top."""
    rnd = random.Random(seed)
    h = int(16 * squash) + grow
    top = 31 - h
    clumps = [(6, top + 8, 7), (13, top + 4, 8), (20, top + 5, 8), (26, top + 9, 6), (16, top + 9, 9)]
    for cx, cy, r in clumps:                                  # outline pass
        d.ellipse([cx - r - 1, cy - r - 1, cx + r + 1, min(31, cy + r + 1)], fill=OUT)
    for cx, cy, r in clumps:
        d.ellipse([cx - r, cy - r, cx + r, min(30, cy + r)], fill=LEAF)
    d.rectangle([2, 27, 29, 30], fill=LEAF_D)                 # shadowed bottom
    for _ in range(14):                                       # leaf texture
        x, y = rnd.randint(3, 28), rnd.randint(top + 2, 28)
        d.point([(x, y), (x + 1, y)], fill=LEAF_D if y > top + 9 else LEAF_L)
    for cx, cy, r in clumps[:3]:                              # light on top
        d.arc([cx - r + 2, cy - r + 1, cx + r - 2, cy + r], 200, 320, fill=LEAF_L)
    return top


def bush_frame(k, scrap=None):
    """Frame k of a bush (the empty bush has 7: idle, rustling, and the regrowth stages)."""
    im = Image.new("RGB", (32, 32), (0, 0, 0))
    d = ImageDraw.Draw(im)
    squash = {4: .85}.get(k, 1.0)
    grow = {5: 2, 6: 4}.get(k, 0)
    top = _bush(d, 7 + k % 3, squash, grow)
    if scrap:                                                 # a corner of the stash poking out the top
        body, dark, accent = scrap
        x = 18 + (k % 3) - 1
        d.polygon([(x - 7, top + 6), (x + 4, top - 6), (x + 10, top), (x + 2, top + 9)], fill=OUT)
        d.polygon([(x - 6, top + 6), (x + 4, top - 5), (x + 9, top), (x + 2, top + 8)], fill=body)
        d.polygon([(x + 4, top - 5), (x + 9, top), (x + 5, top + 2)], fill=dark)
        d.line([(x - 3, top + 5), (x + 3, top - 1)], fill=accent)
    elif k == 0:                                              # the empty bush: a lone sock
        d.rectangle([22, 23, 24, 27], fill=(240, 240, 240))
        d.rectangle([22, 27, 26, 28], fill=(240, 240, 240))
        d.line([(22, 23), (24, 23)], fill=(200, 40, 40))
    return _fit(im, FOOTPRINT)


# the tree's footprint in its 32x32 texture (x 7-24, y 8-31): the bush has to stay inside it or it spills onto
# the next tiles in game
FOOTPRINT = (7, 10, 25, 32)
SCRAP_BOX = (10, 14, 23, 26)                                  # about the size the apricorn was


def _fit(im, box):
    """Shrink a full-frame drawing into box (x0, y0, x1, y1), keeping hard pixels (black = transparent)."""
    x0, y0, x1, y1 = box
    small = im.resize((x1 - x0, y1 - y0), Image.NEAREST)
    out = Image.new("RGB", (32, 32), (0, 0, 0))
    out.paste(small, (x0, y0))
    return out


def scrap_frame(scrap):
    """The scrap you pull out: a crumpled square of material, a stitch line on it."""
    body, dark, accent = scrap
    im = Image.new("RGB", (32, 32), (0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(9, 14), (16, 9), (24, 12), (23, 21), (15, 24), (8, 21)]
    d.polygon([(x + (1 if x > 16 else -1), y + (1 if y > 16 else -1)) for x, y in pts], fill=OUT)
    d.polygon(pts, fill=body)
    d.polygon([(16, 9), (24, 12), (19, 16)], fill=dark)                  # a fold
    for x in range(10, 22, 3):                                           # stitching
        d.point([(x, 19 + (x % 2))], fill=accent)
    return _fit(im.crop((6, 7, 27, 27)).resize((32, 32), Image.NEAREST), SCRAP_BOX)


def _palette_sizes(b, pals):
    offs = sorted(p["off"] for p in pals) + [len(b)]
    return {o: min(16, (n - o) // 2) for o, n in zip(offs, offs[1:])}


def _write(b, tex, pal, im, n):
    """Quantize im to n-1 colours (+ index 0 transparent: pure black pixels are background)."""
    mask = [px != (0, 0, 0) for px in im.getdata()]
    q = im.quantize(colors=n - 1, method=Image.MEDIANCUT, dither=Image.NONE)
    cols = q.getpalette()[:3 * (n - 1)]
    cols += [0] * (3 * (n - 1) - len(cols))
    nsbtx.set_palette(b, pal, [(0, 0, 0)] + [tuple(cols[i:i + 3]) for i in range(0, len(cols), 3)])
    data = list(q.getdata())
    rows = [[(data[y * 32 + x] + 1) if mask[y * 32 + x] else 0 for x in range(32)] for y in range(32)]
    nsbtx.set_pixels(b, tex, rows)


def build():
    """{mmodel index: (new NSBTX bytes, [frame images])}."""
    jobs = {251: [bush_frame(k) for k in range(7)]}
    for letter, (bush, scrap_m, body, dark, accent) in SCRAPS.items():
        jobs[bush] = [bush_frame(k, (body, dark, accent)) for k in range(3)]
        jobs[scrap_m] = [scrap_frame((body, dark, accent))]
    out = {}
    for m, frames in jobs.items():
        rel = MMODEL % m
        data = subprocess.run(["git", "show", f"{BASE}:{rel}"], cwd=ROOT, capture_output=True, check=True).stdout
        b, texs, pals = nsbtx.parse(data)
        assert len(texs) == len(frames), (m, len(texs))
        sizes = _palette_sizes(b, pals)
        for tex, pal, im in zip(texs, pals, frames):
            _write(b, tex, pal, im, sizes[pal["off"]])
        out[m] = (bytes(b), frames)
    return out


def main():
    built = build()
    if "--preview" in sys.argv:
        frames = [im for _, ims in built.values() for im in ims]
        sheet = Image.new("RGB", (len(frames) * 34, 34), (90, 140, 90))
        for k, im in enumerate(frames):
            mask = Image.eval(im.convert("L"), lambda v: 255 if v else 0)
            sheet.paste(im, (k * 34 + 1, 1), mask)
        sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST).save(sys.argv[sys.argv.index("--preview") + 1])
        return
    for m, (data, _) in built.items():
        (ROOT / (MMODEL % m)).write_bytes(data)
    print(f"bushes: {len(built)} textures")


if __name__ == "__main__":
    main()
