#!/usr/bin/env python3
"""Strap the trainer battle sprites (files/a/0/5/8): every trainer class gets a gun that fits
its rank and a gold chain.

Per class the NARC holds 5 files: [0] tiled 80x80 char data drawn through cells (battle intro),
[1] palette, [2] cells, [3] animation, [4] 160x80 bitmap encrypted the DP way. The bitmap is
decrypted, dressed with the battle-sprite tools, re-encrypted with its original key, and the
tiled copy is regenerated from it through the cell layout. Every member keeps its exact size,
so the NARC is rewritten in place. Originals are read from git HEAD.
Run from the repo root:  python hood/make_trainers.py [--preview out.png]
"""
import random
import struct
import subprocess
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_hood as ah  # noqa: E402
import make_sprites as ms  # noqa: E402

NARC = "files/a/0/5/8"

# trainer class name (original, msg_0730) keyword -> gun
CLASS_GUNS = [
    (("Champion", "Rocket Boss"), "minigun"),
    (("Leader", "Elite Four", "Tower Tycoon", "Hall Matron", "Factory Head", "Arcade Star", "Castle Valet",
      "Rival", "Mystery Man", "Executive"), "m4"),
    (("Ace Trainer", "Veteran", "Black Belt", "Biker", "Roughneck", "Burglar", "Firebreather", "Ninja Boy",
      "Dragon Tamer", "Battle Girl", "Policeman"), "ar15"),
    (("Team Rocket", "Scientist", "Super Nerd", "Sailor", "Fisherman", "Hiker", "Juggler", "Worker",
      "Gentleman", "Rich Boy", "Cyclist", "Skier", "Boarder", "Guitarist", "Rancher", "Collector"), "mac10"),
]
SMALL = ["rev22", "beretta", "glock", "uzi", "sawedoff", "extendo", "glock_light", "pump"]


def blob_at(d, f, i):
    o, s = f[i]
    return o, d[o:o + s]


def block(data, magic):
    n = struct.unpack_from("<H", data, 0x0E)[0]
    o = 0x10
    for _ in range(n):
        if data[o:o + 4] == magic:
            return o
        o += struct.unpack_from("<I", data, o + 4)[0]
    raise KeyError(magic)


def decrypt(words):
    seed = words[-1]
    out = list(words)
    for i in range(len(out) - 1, -1, -1):
        out[i] ^= seed & 0xFFFF
        seed = (seed * 1103515245 + 24691) & 0xFFFFFFFF
    return out


def encrypt(words, key):
    seed = key
    out = list(words)
    for i in range(len(out) - 1, -1, -1):
        out[i] ^= seed & 0xFFFF
        seed = (seed * 1103515245 + 24691) & 0xFFFFFFFF
    return out


def cell_oams(ncer):
    k = block(ncer, b"KBEC")
    ncell, attr, celloff = struct.unpack_from("<HHI", ncer, k + 8)
    base = k + 8 + celloff
    size = 16 if attr == 1 else 8
    oam_base = base + ncell * size
    sizes = {(0, 0): (8, 8), (0, 1): (16, 16), (0, 2): (32, 32), (0, 3): (64, 64),
             (1, 0): (16, 8), (1, 1): (32, 8), (1, 2): (32, 16), (1, 3): (64, 32),
             (2, 0): (8, 16), (2, 1): (8, 32), (2, 2): (16, 32), (2, 3): (32, 64)}
    cells = []
    for c in range(ncell):
        n, _, off = struct.unpack_from("<HHI", ncer, base + c * size)
        oams = []
        for o in range(n):
            a0, a1, a2 = struct.unpack_from("<HHH", ncer, oam_base + off + o * 6)
            y = a0 & 0xFF
            x = a1 & 0x1FF
            y = y - 256 if y > 127 else y
            x = x - 512 if x > 255 else x
            w, h = sizes[(a0 >> 14, a1 >> 14)]
            oams.append((x, y, w, h, a2 & 0x3FF))
        cells.append(oams)
    return cells


def tiles_from_image(pixels, cells, ntiles, unit, frame_of_cell):
    """Build 4bpp tile data for the cell-drawn copy from the 160x80 bitmap."""
    data = bytearray(ntiles * 32)
    for c, oams in enumerate(cells):
        fx = 80 * frame_of_cell(c)
        for (x, y, w, h, tile) in oams:
            t = tile * unit
            for ty in range(h // 8):
                for tx in range(w // 8):
                    if t >= ntiles:
                        return None
                    for py in range(8):
                        for px in range(0, 8, 2):
                            X, Y = fx + x + 40 + tx * 8 + px, y + 40 + ty * 8 + py
                            lo = pixels[Y][X] if 0 <= X < 160 and 0 <= Y < 80 else 0
                            hi = pixels[Y][X + 1] if 0 <= X + 1 < 160 and 0 <= Y < 80 else 0
                            data[t * 32 + py * 4 + px // 2] = lo | (hi << 4)
                    t += 1
    return bytes(data)


HAND = {30: (21, 19), 69: (22, 51), 25: (47, 33)}   # classes without a Poké Ball in hand


def ball_hand(im, pal):
    """The hand holding the Poké Ball: a small red blob with white right next to it."""
    px = im.load()
    red = {i for i, (r, g, b) in enumerate(pal) if r > 170 and g < 90 and b < 90}
    white = {i for i, (r, g, b) in enumerate(pal) if min(r, g, b) > 200}
    seen, best = set(), None
    for y in range(80):
        for x in range(80):
            if px[x, y] in red and (x, y) not in seen:
                blob, stack = [], [(x, y)]
                seen.add((x, y))
                while stack:
                    cx, cy = stack.pop()
                    blob.append((cx, cy))
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        q = (cx + dx, cy + dy)
                        if 0 <= q[0] < 80 and 0 <= q[1] < 80 and q not in seen and px[q] in red:
                            seen.add(q)
                            stack.append(q)
                if not 3 <= len(blob) <= 30:
                    continue
                bx = sum(p[0] for p in blob) // len(blob)
                by = sum(p[1] for p in blob) // len(blob)
                near_white = sum(1 for dx in range(-4, 5) for dy in range(-4, 5)
                                 if 0 <= bx + dx < 80 and 0 <= by + dy < 80 and px[bx + dx, by + dy] in white)
                if near_white >= 4 and (best is None or len(blob) > best[0]):
                    best = (len(blob), bx, by + 2)
    return best[1:] if best else None


def gun_for(name, rng):
    for keys, gun in CLASS_GUNS:
        if any(k in name for k in keys):
            return gun
    return rng.choice(SMALL)


def class_names():
    gmm = subprocess.run(["git", "show", "HEAD:files/msgdata/msg/msg_0730.gmm"], cwd=ms.ROOT,
                         capture_output=True, check=True).stdout.decode("utf-8")
    import re
    return [ah.xml_unescape(m.group(3)) for m in ah.ROW_RE.finditer(gmm)]


def main():
    data = bytearray(subprocess.run(["git", "show", f"HEAD:{NARC}"], cwd=ms.ROOT, capture_output=True, check=True).stdout)
    files = ah.narc_files(data)
    names = class_names()
    preview = sys.argv[sys.argv.index("--preview") + 1] if "--preview" in sys.argv else None
    shots, done, tiled = [], 0, 0
    for c in range(len(files) // 5):
        o_ncgr, ncgr = blob_at(data, files, 5 * c)
        o_nclr, nclr = blob_at(data, files, 5 * c + 1)
        _, ncer = blob_at(data, files, 5 * c + 2)
        o_bmp, bmp = blob_at(data, files, 5 * c + 4)
        dbo = block(bmp, b"RAHC") + 0x20
        words = list(struct.unpack_from("<3200H", bmp, dbo))
        key = words[-1]
        dec = decrypt(words)
        raw = struct.pack("<3200H", *dec)
        pixels = [[(raw[(y * 160 + x) // 2] >> 4) if x & 1 else (raw[(y * 160 + x) // 2] & 15) for x in range(160)]
                  for y in range(80)]
        po = block(nclr, b"TTLP") + 0x18
        pal = [((v & 31) << 3, ((v >> 5) & 31) << 3, ((v >> 10) & 31) << 3)
               for v in struct.unpack_from("<16H", nclr, po)]
        im = Image.new("P", (160, 80))
        im.putdata([v for r in pixels for v in r])
        im.putpalette([v for col in pal for v in col])
        if ms.bbox(im.load(), 0) is None:
            continue

        # does the tiled copy rebuild exactly from the original bitmap? (find tile unit + frame use)
        tdo = block(ncgr, b"RAHC") + 0x20
        ntiles = (len(ncgr) - tdo) // 32
        cells = cell_oams(ncer)
        layout = None
        for unit in (2, 1, 4):
            for fmap in (lambda k: 0, lambda k: min(k, 1)):
                if tiles_from_image(pixels, cells, ntiles, unit, fmap) == ncgr[tdo:tdo + ntiles * 32]:
                    layout = (unit, fmap)
                    break
            if layout:
                break

        rng = random.Random(c * 104729)
        name = names[c] if c < len(names) else ""
        gun = gun_for(name, rng)
        used = ms.used_indices([im])
        out_idx = min(used, key=lambda i: sum(pal[i]))
        S = {"out": out_idx}
        acc = ms.accent_slots(pal, used - {out_idx})
        S.update(ac_d=acc[0], ac=acc[1], ac_l=acc[2])
        wanted = ["m", "d", "l", "g", "b", "W", "w"]
        need = []
        for k in wanted:
            near = min(used, key=lambda i: ms.dist(pal[i], ms.COLORS[k]))
            if ms.dist(pal[near], ms.COLORS[k]) < ms.REUSE.get(k, 120):
                S[k] = near
            else:
                need.append(k)
        spal = list(pal)
        got, imgs = ms.free_slots([im], pal, spal, len(need), protect={out_idx, *acc})
        im = imgs[0]
        for k, i in zip(need, got):
            S[k] = i
            pal[i] = ms.COLORS[k]

        items = ms.auto_drip(im, "front", rng, 2, False, {"head", "shoe"}, False, pal)
        px = im.load()
        for item in items:
            ms.draw_drip(im, 0, item, S, (0, 0), 0)
        hand = HAND.get(c) or ball_hand(im, pal) or ms.auto_hand(px, 0, "front")
        bb = ms.bbox(px, 0)
        if hand and bb:
            size = max(bb[2] - bb[0], bb[3] - bb[1])
            ms.draw_gun(im, 0, hand, gun, min(1.0, max(.55, size / 80 * .85)), S, flash=False, mirror=True)
        im.putpalette([v for col in pal for v in col])
        new = list(im.tobytes())
        new_pixels = [new[y * 160:(y + 1) * 160] for y in range(80)]
        if new_pixels[79][156:160] != [0, 0, 0, 0]:
            new_pixels[79][156:160] = [0, 0, 0, 0]       # keep the key word intact
        raw = bytes(new_pixels[y][x] | (new_pixels[y][x + 1] << 4) for y in range(80) for x in range(0, 160, 2))
        enc = encrypt(list(struct.unpack("<3200H", raw)), key)
        struct.pack_into("<3200H", data, o_bmp + dbo, *enc)
        struct.pack_into("<16H", data, o_nclr + po, *[(r >> 3) | ((g >> 3) << 5) | ((b >> 3) << 10) for r, g, b in pal])
        if layout:
            tiles = tiles_from_image(new_pixels, cells, ntiles, *layout)
            data[o_ncgr + tdo:o_ncgr + tdo + len(tiles)] = tiles
            tiled += 1
        done += 1
        if preview:
            shot = im.copy()
            shots.append((name, shot.convert("RGBA").crop((0, 0, 80, 80))))
    if preview:
        from PIL import ImageDraw
        cols = 8
        sheet = Image.new("RGBA", (cols * 84, ((len(shots) + cols - 1) // cols) * 94), (205, 225, 205, 255))
        d = ImageDraw.Draw(sheet)
        for i, (name, s) in enumerate(shots):
            x, y = (i % cols) * 84, (i // cols) * 94
            sheet.alpha_composite(s, (x, y + 12))
            d.text((x + 1, y), name[:13], fill=(0, 0, 0, 255))
        sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(preview)
        print("preview:", preview, "classes:", done, "tiled copies rebuilt:", tiled)
    else:
        (ms.ROOT / NARC).write_bytes(bytes(data))
        print(f"strapped {done} trainer classes ({tiled} tiled copies rebuilt)")


if __name__ == "__main__":
    main()
