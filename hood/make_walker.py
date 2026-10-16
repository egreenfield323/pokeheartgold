#!/usr/bin/env python3
"""Drip for the Pokéwalker's own 4-shade graphics: the 64x48 Pokémon pictures (files/a/2/5/6)
and the 32x24 route icons (files/a/2/4/8). Each member is LZ10-compressed 2bpp data, two frames.

Every Pokémon gets a hat, a mini gun and (if there's room) a chain, drawn in the LCD's shades.
Members change size after recompression, so each NARC is rebuilt. Originals come from the base commit 77565981b.
Run from the repo root:  python hood/make_walker.py [--preview out.png]
"""
import random
import struct
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_hood as ah  # noqa: E402
import make_overworld as mo  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TARGETS = [("files/a/2/5/6", 64, 48), ("files/a/2/4/8", 32, 24)]
SHADES = {"out": 3, "m": 2, "l": 1, "W": 0, "g": 1, "b": 2, "ac": 2}   # 0 = LCD background


def lz10_decompress(b):
    size = b[1] | (b[2] << 8) | (b[3] << 16)
    out, i = bytearray(), 4
    while len(out) < size:
        flags = b[i]
        i += 1
        for bit in range(8):
            if len(out) >= size:
                break
            if flags & (0x80 >> bit):
                n, disp = (b[i] >> 4) + 3, (((b[i] & 15) << 8) | b[i + 1]) + 1
                i += 2
                for _ in range(n):
                    out.append(out[-disp])
            else:
                out.append(b[i])
                i += 1
    return bytes(out)


def lz10_compress(data):
    out = bytearray([0x10, len(data) & 0xFF, (len(data) >> 8) & 0xFF, (len(data) >> 16) & 0xFF])
    i = 0
    while i < len(data):
        flag_pos = len(out)
        out.append(0)
        for bit in range(8):
            if i >= len(data):
                break
            best_len, best_disp = 0, 0
            for disp in range(2, min(i, 4096) + 1):     # disp >= 2 avoids a known decoder quirk
                n = 0
                while n < 18 and i + n < len(data) and data[i + n] == data[i + n - disp]:
                    n += 1
                if n > best_len:
                    best_len, best_disp = n, disp
                    if n == 18:
                        break
            if best_len >= 3:
                out[flag_pos] |= 0x80 >> bit
                d = best_disp - 1
                out += bytes([((best_len - 3) << 4) | (d >> 8), d & 0xFF])
                i += best_len
            else:
                out.append(data[i])
                i += 1
    while len(out) % 4:
        out.append(0)
    return bytes(out)


def decode(data, w, h):
    rows = [[0] * w for _ in range(h)]
    for s in range(h // 8):
        for x in range(w):
            b0, b1 = data[(s * w + x) * 2], data[(s * w + x) * 2 + 1]
            for bit in range(8):
                rows[s * 8 + bit][x] = ((b1 >> bit) & 1) << 1 | ((b0 >> bit) & 1)
    return rows


def encode(rows, w, h):
    out = bytearray(w * h // 4)
    for s in range(h // 8):
        for x in range(w):
            b0 = b1 = 0
            for bit in range(8):
                v = rows[s * 8 + bit][x]
                b0 |= (v & 1) << bit
                b1 |= ((v >> 1) & 1) << bit
            out[(s * w + x) * 2], out[(s * w + x) * 2 + 1] = b0, b1
    return bytes(out)


def rebuild_narc(orig, members):
    """Same header/FNTB as the original, new FATB offsets and GMIF payload."""
    hdr = struct.unpack_from("<H", orig, 12)[0]
    fatb_size = struct.unpack_from("<I", orig, hdr + 4)[0]
    fntb = hdr + fatb_size
    fntb_size = struct.unpack_from("<I", orig, fntb + 4)[0]
    fnt = orig[fntb:fntb + fntb_size]
    fat, img, off = bytearray(), bytearray(), 0
    for m in members:
        fat += struct.pack("<II", off, off + len(m))
        img += m
        while len(img) % 4:
            img.append(0xFF)
        off = len(img)
    fatb = b"BTAF" + struct.pack("<IHH", 12 + len(fat), len(members), 0) + fat
    gmif = b"GMIF" + struct.pack("<I", 8 + len(img)) + img
    body = bytes(fatb) + bytes(fnt) + gmif
    head = bytearray(orig[:hdr])
    struct.pack_into("<I", head, 8, hdr + len(body))
    return bytes(head) + body


def find_eyes(rows):
    """Pupils on the LCD: tiny black blobs with no black around them, enclosed by the body."""
    h, w = len(rows), len(rows[0])
    seen, spots = set(), []
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if rows[y][x] != 3 or (x, y) in seen:
                continue
            blob, stack = [], [(x, y)]
            seen.add((x, y))
            while stack and len(blob) <= 7:
                cx, cy = stack.pop()
                blob.append((cx, cy))
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    q = (cx + dx, cy + dy)
                    if 0 <= q[0] < w and 0 <= q[1] < h and q not in seen and rows[q[1]][q[0]] == 3:
                        seen.add(q)
                        stack.append(q)
            if stack or len(blob) > 6:
                continue
            xs, ys = [p[0] for p in blob], [p[1] for p in blob]
            ring = [(i, j) for i in range(min(xs) - 1, max(xs) + 2) for j in range(min(ys) - 1, max(ys) + 2)
                    if (i, j) not in blob and 0 <= i < w and 0 <= j < h]
            if any(rows[j][i] == 3 for i, j in ring):
                continue
            if sum(1 for i, j in ring if rows[j][i] == 0) < 2:      # must touch eye-white
                continue
            cy, cx = sum(ys) // len(ys), sum(xs) // len(xs)
            left = any(rows[cy][i] for i in range(max(0, min(xs) - 9), min(xs) - 1))
            right = any(rows[cy][i] for i in range(max(xs) + 2, min(w, max(xs) + 10)))
            up = any(rows[j][cx] for j in range(max(0, min(ys) - 9), min(ys) - 1))
            if left and right and up:
                spots.append((cx, cy))
    if not spots:
        return None
    ys = [y for y, r in enumerate(rows) if any(r)]
    t, b = min(ys), max(ys)
    spots = [p for p in spots if p[1] <= t + (b - t) * .6]
    if not spots:
        return None
    return min(spots, key=lambda p: p[1])


def dress(rows, rng, small):
    style = rng.choice(["durag", "beanie", "snapback", "bandana"])
    mini = "pistol" if small else rng.choice(["pistol", "mid", "mid", "long"])
    return mo.dress_frame(rows, "left", SHADES, style, "k", mini, big=False, eyes=find_eyes(rows))


def main():
    preview = sys.argv[sys.argv.index("--preview") + 1] if "--preview" in sys.argv else None
    shots = []
    for rel, w, h in TARGETS:
        orig = subprocess.run(["git", "show", f"77565981b:{rel}"], cwd=ROOT, capture_output=True, check=True).stdout
        files = ah.narc_files(orig)
        members = []
        for k, (o, s) in enumerate(files):
            blob = orig[o:o + s]
            raw = lz10_decompress(blob) if blob[:1] == b"\x10" else None
            frame = w * h // 4
            if not raw or len(raw) % frame:
                members.append(blob)
                continue
            rng = random.Random(k * 7 + w)
            out = bytearray()
            for f in range(len(raw) // frame):
                rows = decode(raw[f * frame:(f + 1) * frame], w, h)
                if any(any(r) for r in rows):
                    rows = dress(rows, random.Random(k * 7 + w), small=(w == 32))
                out += encode(rows, w, h)
                if preview and f == 0 and k < 24:
                    shots.append((w, h, rows))
            packed = lz10_compress(bytes(out))
            assert lz10_decompress(packed) == bytes(out)
            members.append(packed)
        if not preview:
            (ROOT / rel).write_bytes(rebuild_narc(orig, members))
            new = (ROOT / rel).read_bytes()
            assert len(ah.narc_files(new)) == len(files)
            print(f"{rel}: dressed {len(files)} members")
    if preview:
        from PIL import Image
        pal = [(200, 210, 190), (140, 150, 130), (80, 90, 70), (20, 30, 20)]
        sheet = Image.new("RGB", (12 * 68, 4 * 52), (255, 255, 255))
        for i, (w, h, rows) in enumerate(shots[:48]):
            im = Image.new("RGB", (w, h))
            im.putdata([pal[v] for r in rows for v in r])
            sheet.paste(im, ((i % 12) * 68, (i // 12) * 52))
        sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST).save(preview)
        print("preview:", preview)


if __name__ == "__main__":
    main()
