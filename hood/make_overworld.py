#!/usr/bin/env python3
"""Drip for the overworld: walking followers, overworld legendaries (Ho-Oh, Lugia, ...),
the red Gyarados and the sleeping Snorlax.

Run from the repo root:
    python hood/make_overworld.py                     # rewrite the NSBTX textures in place
    python hood/make_overworld.py --preview out.png   # contact sheet only
    python hood/make_overworld.py --only 6,249 --preview out.png

Each NSBTX holds 8 frames (away x2, toward x2, left x2, right x2), 32x32 or 64x64,
16 colours, with a normal and a shiny palette. Every frame gets the same hat the
Pokémon wears in battle, a mini version of its battle gun, and (facing the camera)
a chain. Originals are read from git HEAD, so re-running is safe.
"""
import json
import random
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import hats  # noqa: E402
import make_sprites as ms  # noqa: E402
import nsbtx  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MMODEL = ROOT / "files/data/mmodel/mmodel"
DIRECTIONS = ["up", "up", "down", "down", "left", "left", "right", "right"]

MINI = {  # pointing LEFT; m metal, d/k dark, b brass/wood, g gold, + grip
    "pistol": "mmmmmd\ndddd+d\n....dd\n....dd",
    "mid": "mmmmmmmd\nddddd+dd\n....ddd.\n....dd..\n....dd..",
    "long": "k...........\nmmmmmmdddbbb\n....ddd+dbbb\n......d...bb",
    "heavy": "..bb...........\nbbbbmmmmmmmmmmm\nbbbbmmmmmmmmmmm\n..bb.....d+....",
}
MINI_CLASS = {
    "rev22": "pistol", "beretta": "pistol", "glock": "pistol", "sawedoff": "pistol", "uzi": "pistol",
    "rev38": "mid", "extendo": "mid", "glock_light": "mid", "pump": "mid", "mac10": "mid", "magnum": "mid",
    "draco": "long", "drum_ak": "long", "ar15": "long", "ar_bump": "long", "m4": "long",
    "auto_shotgun": "long", "lmg": "long", "ak": "long", "sniper": "long",
    "launcher": "heavy", "minigun": "heavy", "rpg": "heavy",
}
EXTRA = {183: "GYARADOS", 194: "SNORLAX"}   # MMODEL_RGYARADOSU, MMODEL_KABIGON
CUTSCENE = [("files/demo/legend/legend_00000075.NSBMD", "CELEBI")]   # Celebi event carries its own copy


def parse_art(art):
    px, anchor = {}, (0, 0)
    for y, row in enumerate(art.split("\n")):
        for x, c in enumerate(row):
            if c == "+":
                anchor, c = (x, y), "d"
            if c != ".":
                px[(x, y)] = c
    return px, anchor


def model_species(names):
    """mmodel file index -> species index, from include/constants/mmodel.h."""
    idx = {n: i for i, n in enumerate(names)}
    out = {}
    for line in (ROOT / "include/constants/mmodel.h").read_text().splitlines():
        m = re.match(r"#define MMODEL_FOLLOWER_MON_(\w+)\s+(\d+)", line)
        if not m:
            continue
        key, num = m.group(1), int(m.group(2))
        best = max((n for n in idx if key == n or key.startswith(n + "_")), key=len, default=None)
        if best:
            out[num] = idx[best]
    for num, name in EXTRA.items():
        out[num] = idx[name]
    return out


def bbox(rows):
    pts = [(x, y) for y, r in enumerate(rows) for x, v in enumerate(r) if v]
    if not pts:
        return None
    return min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)


def head_run(rows, d):
    l, t, r, b = bbox(rows)
    W, H = r - l + 1, b - t + 1
    mid = (l + r) / 2
    if d in ("left", "right") and W >= 10:
        # side view: the head is the front end of the body, so only look at the leading ~45%
        band = range(l, l + max(5, round(W * .45))) if d == "left" else range(r - max(5, round(W * .45)) + 1, r + 1)
        top = next((y for y in range(t, b + 1) if any(rows[y][x] for x in band)), None)
        if top is not None:
            y = min(b, top + 2)
            xs = [x for x in band if rows[y][x]] or [x for x in band if rows[top][x]]
            if xs:
                a, z = min(xs), max(xs)
                if z - a < 5:                      # pad thin crowns so the hat has some width
                    a, z = a - (5 - (z - a)) // 2, z + (5 - (z - a) + 1) // 2
                return top, a, z
    best = None
    for y in range(t, t + max(3, round(H * .45))):
        x, start = l, None
        for x in range(l, r + 2):
            on = x <= r and rows[y][x] != 0
            if on and start is None:
                start = x
            if not on and start is not None:
                a, z = start, x - 1
                start = None
                if z - a + 1 < max(3, W * .2):
                    continue
                c = (a + z) / 2
                lean = {"left": r - c, "right": c - l}.get(d, -abs(c - mid))
                score = (y - t) - .5 * lean
                if best is None or score < best[0]:
                    best = (score, y, a, z)
    return best[1:] if best else None


def frame_eyes(rows, pal):
    """Pupil detection from the battle sprites, on the frame padded to 80x80. Only trusted in the top half."""
    canvas = Image.new("P", (80, 80))
    flat = Image.new("P", (len(rows[0]), len(rows)))
    flat.putdata([v for r in rows for v in r])
    canvas.paste(flat, (0, 0))
    px = canvas.load()
    bb = ms.bbox(px, 0)
    if not bb:
        return None
    e = ms.find_eyes(px, pal, *bb)
    if e and e[1] <= bb[1] + (bb[3] - bb[1]) * .55 and e[0] < len(rows[0]) and e[1] < len(rows):
        return e
    return None


def dress_frame(rows, d, S, hat_style, hat_color, mini, big, eyes=None, chain=True):
    h, w = len(rows), len(rows[0])
    if hat_style == "bandana" and not big:   # a 3px flat band reads as a stripe at 32px; use a cap
        hat_style = "snapback"
    bb = bbox(rows)
    if not bb:
        return rows
    l, t, r, b = bb
    out = [row[:] for row in rows]
    src = rows

    def put(x, y, c):
        if 0 <= x < w and 0 <= y < h:
            out[y][x] = c

    z = 2 if big else 1
    # gun
    art, (ax, ay) = parse_art(MINI[mini])
    gy = t + round((b - t) * .58)
    row = [x for x in range(l, r + 1) if src[gy][x]] or [l]
    mirror = d in ("right", "up")
    hx = (max(row) - 1) if mirror else (min(row) + 1)
    pts = {}
    for (x, y), c in art.items():
        for i in range(z):
            for j in range(z):
                dx = (x - ax) * z + i
                pts[(hx - dx if mirror else hx + dx, gy + (y - ay) * z + j)] = c
    xs = [p[0] for p in pts]
    shift = max(0, 1 - min(xs)) - max(0, max(xs) - (w - 2))
    pts = {(x + shift, y): c for (x, y), c in pts.items()}
    for (x, y) in pts:
        for ex, ey in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + ex, y + ey) not in pts:
                put(x + ex, y + ey, S["out"])
    for (x, y), c in pts.items():
        put(x, y, {"m": S["m"], "d": S["out"], "k": S["out"], "b": S["b"], "g": S["g"]}[c])
    # chain (facing the camera)
    hr = head_run(src, d)
    if chain and d == "down" and hr:
        cy = min(b - 2, hr[0] + round((b - t) * .45))
        xs = [x for x in range(l, r + 1) if src[cy][x]]
        if len(xs) >= 6:
            c = (min(xs) + max(xs)) // 2
            half = max(2, min(5 * z, (max(xs) - min(xs)) // 4))
            for x in range(c - half, c + half + 1):
                yy = cy + (1 if abs(x - c) < half // 2 + 1 else 0)
                put(x, yy, S["g"] if x % 2 else S["b"])
                put(x, yy + 1, S["out"])
            put(c, cy + 2, S["g"])
            put(c, cy + 3, S["out"])
    # hat on top of the head (eyes known: brim sits just above them)
    if eyes:
        ex, ey = eyes
        brow = max(t, ey - 2)
        xs = [x for x in range(l, r + 1) if src[brow][x]]
        runs, start = [], None
        for x in range(l, r + 2):
            on = x <= r and src[brow][x] != 0
            if on and start is None:
                start = x
            if not on and start is not None:
                runs.append((start, x - 1)); start = None
        a, zz = next(((p, q) for p, q in runs if p - 1 <= ex <= q + 1), (ex - 4, ex + 4))
        a, zz = max(a, ex - 7), min(zz, ex + 7)
        hr = (brow - 2 * z, a, zz, True)
    elif hr:
        hr = (*hr, False)
    if hr:
        y, a, zz, from_eyes = hr
        hw = max(8, min(13 if not big else 24, zz - a + 3))
        if d in ("left", "right"):   # side view: hat no wider than the head itself
            hw = max(6, min(hw, zz - a + 2))
        tiny = (b - t) < 16
        if tiny:            # tiny sprites (Pidgey etc.): a small hat perched on top, never over the face
            hw = max(6, min(hw, round((r - l + 1) * .5)))
            if from_eyes:
                y = min(y, eyes[1] - 3 - 2 * z)
            else:
                y += 1 - 2 * z
        elif not from_eyes:  # hr[0] is the very top pixel: sink the hat onto the crown, at most a quarter of the body
            y += min(max(2, round(hw * .45)), max(1, round((b - t) * .25))) - 2 * z
        side = {"left": 1, "right": -1}.get(d, 1 if d == "down" else 0)
        col = S["out"] if hat_color == "k" else S[hat_color]
        roles = {"c": col, "s": S["m"] if hat_color in ("k", "ac") else S["l"], "o": S["out"],
                 "W": S["W"] if hat_color != "W" else S["l"], "g": S["g"]}
        for (dx, dy), role in hats.hat(hat_style, hw, side).items():
            put((a + zz) // 2 + dx, y + 2 * z + dy, roles[role])
    return out


def dress_model(num, species, gun, spec, rel=None):
    rel = rel or f"files/data/mmodel/mmodel/mmodel_{num:08d}.NSBTX"
    blob = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT, capture_output=True, check=True).stdout
    b, texs, pals = nsbtx.parse(blob)
    texs = [t for t in texs if t["fmt"] == 3 and (rel.endswith(".NSBTX") or t["name"].startswith("tsure_"))]
    pals = [p for p in pals if rel.endswith(".NSBTX") or p["name"].startswith("tsure_")]
    if not texs:
        return None
    frames = [nsbtx.get_pixels(b, t) for t in texs]
    pal = nsbtx.get_palette(b, pals[0])
    spal = nsbtx.get_palette(b, pals[1]) if len(pals) > 1 else list(pal)
    imgs = []
    for rows in frames:
        im = Image.new("P", (len(rows[0]), len(rows)))
        im.putdata([v for r in rows for v in r])
        im.putpalette([v for c in pal for v in c])
        imgs.append(im)

    # same hat the Pokémon wears in battle
    rng = random.Random(species * 7919)
    style = rng.choice(["durag", "beanie", "snapback", "snapback", "bandana", "durag"])
    color = rng.choices(["k", "ac", "W", "g"], [40, 30, 15, 15])[0]
    for item in spec.get("front", []):
        if item["type"] == "hat":
            style, color = item["style"], item.get("color", color)

    used = ms.used_indices(imgs)
    out_idx = min(used, key=lambda i: sum(pal[i]))
    acc = ms.accent_slots(pal, used - {out_idx})
    S = {"out": out_idx, "ac": acc[1]}
    need = []
    for k in ["m", "g", "b", "l", "W"] + ([color] if color in ms.COLORS and color not in ("g", "W") else []):
        near = min(used, key=lambda i: ms.dist(pal[i], ms.COLORS[k]))
        if ms.dist(pal[near], ms.COLORS[k]) < ms.REUSE.get(k, 120):
            S[k] = near
        else:
            need.append(k)
    got, imgs = ms.free_slots(imgs, pal, spal, len(need), protect={out_idx, *acc})
    for k, i in zip(need, got):
        S[k] = i
        pal[i] = ms.COLORS[k]
        spal[i] = ms.SHINY.get(k, ms.COLORS[k])

    mini = MINI_CLASS.get(gun, "pistol")
    for k, (t, im) in enumerate(zip(texs, imgs)):
        rows = [list(im.tobytes()[y * t["w"]:(y + 1) * t["w"]]) for y in range(t["h"])]
        d = DIRECTIONS[k] if len(texs) == 8 else "down"
        rows = dress_frame(rows, d, S, style, color, mini, big=t["w"] >= 64,
                           eyes=frame_eyes(rows, pal) if d != "up" else None)
        nsbtx.set_pixels(b, t, rows)
    nsbtx.set_palette(b, pals[0], pal)
    if len(pals) > 1:
        nsbtx.set_palette(b, pals[1], spal)
    return bytes(b), texs, pal


def render(b, texs, pal):
    tiles = []
    for t in texs:
        rows = nsbtx.get_pixels(b, t)
        im = Image.new("RGBA", (t["w"], t["h"]))
        im.putdata([(*pal[v], 0 if v == 0 else 255) for r in rows for v in r])
        tiles.append(im)
    return tiles


def main():
    args = sys.argv[1:]
    opt = lambda name, default=None: args[args.index(name) + 1] if name in args else default
    plan, names = ms.gun_plan()
    drip = {k: v for k, v in json.loads(ms.DRIP.read_text(encoding="utf-8")).items() if not k.startswith("_")}
    for n in range(1, 494):
        plan[n] = drip.get(str(n), {}).get("gun", plan[n])
    models = model_species(names)
    only = {int(x) for x in opt("--only").split(",")} if opt("--only") else None
    todo = sorted(m for m, sp in models.items() if not only or sp in only)
    rows = []
    for num in todo:
        sp = models[num]
        res = dress_model(num, sp, plan[sp], drip.get(str(sp), {}))
        if not res:
            continue
        data, texs, pal = res
        if opt("--preview"):
            rows.append((num, names[sp], render(data, texs, pal)))
        else:
            (MMODEL / f"mmodel_{num:08d}.NSBTX").write_bytes(data)
    if not opt("--preview"):
        idx = {n: i for i, n in enumerate(names)}
        for rel, name in CUTSCENE:
            sp = idx[name]
            res = dress_model(None, sp, plan[sp], drip.get(str(sp), {}), rel)
            if res:
                (ROOT / rel).write_bytes(res[0])
        print(f"dressed {len(todo)} overworld models + {len(CUTSCENE)} cutscene sprite")
        return
    cell = 68
    W = max(len(t) for _, _, t in rows) * cell + 120
    sheet = Image.new("RGBA", (W, len(rows) * cell), (200, 230, 200, 255))
    from PIL import ImageDraw
    dr = ImageDraw.Draw(sheet)
    for k, (num, name, tiles) in enumerate(rows):
        dr.text((2, k * cell + 2), f"{name}", fill=(0, 0, 0, 255))
        for j, im in enumerate(tiles):
            sheet.alpha_composite(im, (120 + j * cell, k * cell + 2))
    z = int(opt("--zoom", 3))
    sheet.resize((sheet.width * z, sheet.height * z), Image.NEAREST).save(opt("--preview"))
    print("preview:", opt("--preview"))


if __name__ == "__main__":
    main()
