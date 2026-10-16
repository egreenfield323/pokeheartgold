#!/usr/bin/env python3
"""New bag icons for the renamed items: cognac bottles (Hennessy / Henny XO / Patrón),
tall bottles (Ace o Spades / Grey Goose) and a can (Red Bull / Icy Hot).
Several items share one picture with different palettes, so each shape is drawn once and every
palette is recoloured. Edits files/itemtool/itemdata/item_icon/*.NCGR/NCLR in place (same sizes).
Run from the repo root:  python hood/make_items.py [--preview out.png]
"""
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
P = "files/itemtool/itemdata/item_icon/item_icon_%03d.%s"
OUT, CAP, CAP_L, GL_D, GL, GL_L, LABEL, LABEL_T, LIQ = 1, 2, 3, 4, 5, 6, 7, 8, 9


def head(rel):
    return bytearray(subprocess.run(["git", "show", f"77565981b:{rel}"], cwd=ROOT, capture_output=True, check=True).stdout)


def block(b, magic):
    n = struct.unpack_from("<H", b, 14)[0]
    o = 16
    for _ in range(n):
        if b[o:o + 4] == magic:
            return o
        o += struct.unpack_from("<I", b, o + 4)[0]
    raise KeyError(magic)


def body(img, top, profile, label=None, liquid_from=None):
    """Fill a symmetric body: profile[i] = half-width at row top+i. Shaded left->right."""
    cx = 16
    for i, hw in enumerate(profile):
        y = top + i
        for x in range(cx - hw, cx + hw):
            rel = (x - (cx - hw)) / max(1, 2 * hw - 1)
            img[y][x] = GL_D if rel < .3 else (GL if rel < .72 else GL_L)
            if liquid_from is not None and i >= liquid_from and .1 < rel < .9:
                img[y][x] = LIQ if rel < .7 else GL_L
        if label and label[0] <= i <= label[1]:
            for x in range(cx - hw + 2, cx + hw - 2):
                img[y][x] = LABEL
            if i == (label[0] + label[1]) // 2:
                for x in range(cx - hw + 4, cx + hw - 4, 2):
                    img[y][x] = LABEL_T
    for y in range(32):                      # 1px outline
        for x in range(32):
            if img[y][x] == 0 and any(0 <= x + dx < 32 and 0 <= y + dy < 32 and img[y + dy][x + dx] not in (0, OUT)
                                      for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                img[y][x] = OUT


def cap(img, y0, h, hw):
    for y in range(y0, y0 + h):
        for x in range(16 - hw, 16 + hw):
            img[y][x] = CAP_L if x == 16 - hw + 1 else CAP


def cognac():
    img = [[0] * 32 for _ in range(32)]
    cap(img, 2, 3, 2)
    prof = [2, 2, 2, 3, 4, 6, 8, 9, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 9, 8]
    body(img, 5, prof, label=(10, 16), liquid_from=6)
    return img


def tall():
    img = [[0] * 32 for _ in range(32)]
    cap(img, 1, 3, 2)
    prof = [2, 2, 2, 2, 2, 3, 4, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5]
    body(img, 4, prof, label=(13, 19))
    return img


def can():
    img = [[0] * 32 for _ in range(32)]
    for x in range(10, 22):                   # pull tab rim
        img[4][x] = CAP_L
        img[5][x] = CAP
    prof = [6] * 22
    body(img, 6, prof, label=(5, 14))
    return img


SHAPES = {24: cognac, 33: tall, 30: can}
PALETTES = {   # palette file: colours for OUT, CAP, CAP_L, GL_D, GL, GL_L, LABEL, LABEL_T, LIQ
    25: [(24, 16, 8), (16, 16, 16), (90, 90, 90), (96, 44, 8), (160, 80, 16), (232, 168, 72), (24, 20, 16), (232, 200, 96), (128, 56, 8)],      # Hennessy
    37: [(16, 8, 8), (200, 160, 48), (248, 224, 120), (64, 24, 8), (120, 48, 8), (200, 128, 48), (16, 16, 16), (248, 216, 96), (88, 32, 8)],    # Henny XO
    36: [(24, 40, 24), (176, 120, 72), (224, 176, 120), (168, 200, 184), (208, 232, 216), (248, 248, 248), (40, 120, 64), (248, 248, 248), (200, 224, 208)],  # Patrón
    35: [(40, 24, 0), (16, 16, 16), (90, 90, 90), (176, 120, 16), (232, 184, 48), (255, 240, 160), (24, 24, 24), (232, 200, 96), (200, 150, 32)],  # Ace o Spades
    34: [(24, 32, 56), (40, 72, 160), (96, 128, 208), (176, 192, 216), (224, 232, 248), (255, 255, 255), (64, 104, 176), (248, 248, 248), (200, 216, 240)],  # Grey Goose
    31: [(16, 16, 48), (176, 176, 184), (232, 232, 240), (24, 48, 120), (48, 88, 176), (176, 200, 232), (192, 192, 200), (216, 32, 40), (48, 88, 176)],  # Red Bull
    32: [(48, 8, 8), (176, 176, 184), (232, 232, 240), (160, 24, 24), (216, 48, 48), (248, 160, 160), (40, 80, 200), (248, 248, 248), (216, 48, 48)],  # Icy Hot
}


def write_ncgr(b, img):
    o = block(b, b"RAHC") + 0x20
    for t in range(16):
        for y in range(8):
            for x in range(0, 8, 2):
                lo = img[(t // 4) * 8 + y][(t % 4) * 8 + x]
                hi = img[(t // 4) * 8 + y][(t % 4) * 8 + x + 1]
                b[o + t * 32 + y * 4 + x // 2] = lo | (hi << 4)


def write_nclr(b, cols):
    o = block(b, b"TTLP") + 0x18
    old = list(struct.unpack_from("<16H", b, o))
    for i, (r, g, bl) in enumerate(cols, start=1):
        old[i] = (r >> 3) | ((g >> 3) << 5) | ((bl >> 3) << 10)
    struct.pack_into("<16H", b, o, *old)


def main():
    outputs = {}
    for g, fn in SHAPES.items():
        b = head(P % (g, "NCGR"))
        img = fn()
        write_ncgr(b, img)
        outputs[P % (g, "NCGR")] = (b, img)
    pals = {}
    for c, cols in PALETTES.items():
        b = head(P % (c, "NCLR"))
        write_nclr(b, cols)
        outputs[P % (c, "NCLR")] = (b, None)
        pals[c] = [(0, 0, 0)] + cols + [(0, 0, 0)] * 6
    if "--preview" in sys.argv:
        from PIL import Image
        pairs = [(24, 25), (24, 37), (24, 36), (33, 35), (33, 34), (30, 31), (30, 32)]
        sheet = Image.new("RGB", (len(pairs) * 36, 36), (200, 200, 200))
        for k, (g, c) in enumerate(pairs):
            img = SHAPES[g]()
            im = Image.new("RGBA", (32, 32))
            im.putdata([(*pals[c][v], 0 if v == 0 else 255) for r in img for v in r])
            sheet.paste(im, (k * 36, 2), im)
        sheet.resize((sheet.width * 6, sheet.height * 6), Image.NEAREST).save(sys.argv[sys.argv.index("--preview") + 1])
        print("preview written")
        return
    for rel, (b, _) in outputs.items():
        (ROOT / rel).write_bytes(bytes(b))
    print(f"item icons: {len(outputs)} files")


if __name__ == "__main__":
    main()
