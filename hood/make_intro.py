#!/usr/bin/env python3
"""Intro edits: Professor Oak's portrait (wife beater, drawers, powder under the nose) and
the intro Marill (durag + chain). Edits files/demo/intro/intro/*.NCGR/NCLR in place (same sizes).
Originals are read from git HEAD. Run from the repo root:  python hood/make_intro.py [--preview out.png]
"""
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
D = "files/demo/intro/intro/intro_%08d.%s"


def head(rel):
    return bytearray(subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT, capture_output=True, check=True).stdout)


def block(b, magic):
    n = struct.unpack_from("<H", b, 14)[0]
    o = 16
    for _ in range(n):
        if b[o:o + 4] == magic:
            return o
        o += struct.unpack_from("<I", b, o + 4)[0]
    raise KeyError(magic)


def read_pal(b, n=16, row=0):
    o = block(b, b"TTLP") + 0x18 + row * 32
    return [((v & 31) << 3, ((v >> 5) & 31) << 3, ((v >> 10) & 31) << 3) for v in struct.unpack_from(f"<{n}H", b, o)]


def write_pal(b, cols, row=0):
    o = block(b, b"TTLP") + 0x18 + row * 32
    struct.pack_into(f"<{len(cols)}H", b, o, *[(r >> 3) | ((g >> 3) << 5) | ((bl >> 3) << 10) for r, g, bl in cols])


def tiles_to_img(b, tw, th):
    o = block(b, b"RAHC") + 0x20
    img = [[0] * (tw * 8) for _ in range(th * 8)]
    for t in range(tw * th):
        for y in range(8):
            for x in range(8):
                v = b[o + t * 32 + y * 4 + x // 2]
                img[(t // tw) * 8 + y][(t % tw) * 8 + x] = (v >> 4) if x & 1 else (v & 15)
    return img


def img_to_tiles(b, img, tw, th):
    o = block(b, b"RAHC") + 0x20
    for t in range(tw * th):
        for y in range(8):
            for x in range(0, 8, 2):
                lo = img[(t // tw) * 8 + y][(t % tw) * 8 + x]
                hi = img[(t // tw) * 8 + y][(t % tw) * 8 + x + 1]
                b[o + t * 32 + y * 4 + x // 2] = lo | (hi << 4)


def oak():
    g, p = head(D % (10, "NCGR")), head(D % (11, "NCLR"))
    img = tiles_to_img(g, 8, 16)
    pal = read_pal(p)
    # jacket (3, 5, 14, 4 are jacket-only) -> bare skin: arms out, shirt becomes a wife beater
    pal[14], pal[3], pal[5], pal[4] = (248, 224, 200), (224, 188, 156), (192, 152, 120), (120, 80, 64)
    WHITE, GREY, SKIN, SKIN_D, OUT = 1, 2, 12, 11, 13
    for y in range(30, 84):          # torso: white tank top down the middle, bare skin around it
        for x in range(64):
            v = img[y][x]
            if v not in (3, 5, 14, 4, 1, 2):
                continue
            strap = 30 <= x <= 33 or 41 <= x <= 44
            in_top = (29 <= x <= 45 and y >= 40 and y <= 70) or (strap and y < 40)
            if in_top:
                img[y][x] = GREY if v in (4, 5, 2) and (x in (29, 45) or y == 70) else WHITE
            elif v in (3, 14, 1, 2):
                img[y][x] = 14       # flat skin, no jacket seams
            elif v == 5:
                img[y][x] = 3        # skin shade
    for y in range(68, 120):
        for x in range(64):
            v = img[y][x]
            if v in (9, 10, 6):
                if y < 92:   # tighty-whities / boxers
                    img[y][x] = GREY if (v == 6 or (x + y) % 9 == 0) else WHITE
                else:        # bare legs
                    img[y][x] = SKIN_D if v == 6 else SKIN
    for y in range(92, 94):  # leg holes of the drawers
        for x in range(20, 54):
            if img[y][x] in (SKIN, SKIN_D):
                img[y][x] = GREY
    for (x, y) in ((38, 24), (39, 24), (40, 24), (41, 24), (39, 25), (40, 25), (42, 23)):  # powder under the nose
        img[y][x] = WHITE
    img_to_tiles(g, img, 8, 16)
    write_pal(p, pal)
    return g, p, img, pal


def main():
    g, p, img, pal = oak()
    if "--preview" in sys.argv:
        from PIL import Image
        im = Image.new("RGB", (64, 128))
        im.putdata([pal[v] for r in img for v in r])
        im.resize((256, 512), Image.NEAREST).save(sys.argv[sys.argv.index("--preview") + 1])
        print("preview written")
        return
    (ROOT / (D % (10, "NCGR"))).write_bytes(bytes(g))
    (ROOT / (D % (11, "NCLR"))).write_bytes(bytes(p))
    print("intro: Oak redone")


if __name__ == "__main__":
    main()
