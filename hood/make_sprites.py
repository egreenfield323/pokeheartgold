#!/usr/bin/env python3
"""Strap every Pokémon: draw an evolving gun (and drip) onto the ORIGINAL battle sprites.

Run from the repo root:
    python hood/make_sprites.py                      # write all sprites
    python hood/make_sprites.py --preview out.png    # contact sheet only
    python hood/make_sprites.py --only 155,16,74 --preview out.png

Guns come in families that upgrade as a Pokémon evolves (see FAMILIES); legendaries
carry heavy weapons. Guns are drawn by hood/gunart.py. Hand-placed drip (chains,
grillz, shades, kicks, jeans, durags, cigs, ...) lives in hood/data/drip.json.

Sprite format: 160x80 = two 80x80 frames, 16-colour palette, index 0 transparent.
front.png's palette is the normal palette, back.png's palette is the shiny palette,
and both share one index layout. Originals are always read from git HEAD.
"""
import colorsys
import hashlib
import json
import math
import random
import subprocess
import sys
from io import BytesIO
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gunart  # noqa: E402
import hats  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SPRITES = ROOT / "files/poketool/pokegra/pokegra"
DRIP = ROOT / "hood/data/drip.json"

# ------------------------------------------------------------------ which gun

FAMILIES = {
    "revolver": ["rev22", "rev38", "magnum"],
    "pistol":   ["beretta", "extendo", "draco"],
    "glock":    ["glock", "glock_light", "drum_ak"],
    "rifle":    ["ar15", "ar_bump", "m4"],
    "shotgun":  ["sawedoff", "pump", "auto_shotgun"],
    "smg":      ["uzi", "mac10", "lmg"],
}
FAMILY_ORDER = list(FAMILIES)
HEAVY = [(600, "sniper"), (640, "launcher"), (680, "minigun"), (10_000, "rpg")]
FIXED_FAMILY = {"CHIKORITA": "revolver", "CYNDAQUIL": "pistol", "TOTODILE": "glock", "LARVITAR": "rifle"}
STAGES, BST = {}, {}
LEGENDARY = {144, 145, 146, 150, 151, 243, 244, 245, 249, 250, 251, 377, 378, 379, 380, 381, 382, 383,
             384, 385, 386, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493}


def git_blob(rel):
    return subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT, capture_output=True, check=True).stdout


def git_png(path):
    blob = git_blob(path.relative_to(ROOT).as_posix())
    return Image.open(BytesIO(blob)) if blob else None


def gun_plan():
    """species index -> gun. Each evolution line shares a family; its stage picks the rung."""
    stats = json.loads(git_blob("files/poketool/personal/personal.json"))["baseStats"]
    names = [s["species"] for s in stats]
    bst = [sum(s[k] for k in ("hp", "atk", "def", "speed", "spatk", "spdef")) for s in stats]
    idx = {n: i for i, n in enumerate(names)}
    parent = {}
    for e in json.loads(git_blob("files/poketool/personal/evo.json"))["evoTable"]:
        base = e["baseSpecies"].replace("SPECIES_", "")
        for t in e["evos"]:
            tgt = t["target"].replace("SPECIES_", "")
            if tgt in idx and tgt != base:
                parent.setdefault(tgt, base)

    def root_and_stage(n):
        s = 1
        while n in parent and s < 4:
            n, s = parent[n], s + 1
        return n, s

    depth = {}
    for n in names:
        r, s = root_and_stage(n)
        depth[r] = max(depth.get(r, 1), s)
    plan = {}
    for i, n in enumerate(names):
        r, s = root_and_stage(n)
        STAGES[i], BST[i] = s, bst[i]
        if i in LEGENDARY:
            plan[i] = next(g for limit, g in HEAVY if bst[i] < limit)
            continue
        fam = FIXED_FAMILY.get(r) or FAMILY_ORDER[int(hashlib.md5(r.encode()).hexdigest(), 16) % len(FAMILY_ORDER)]
        length = depth[r]
        if length >= 3:
            rung = min(s, 3) - 1
        elif length == 2:
            rung = 0 if s == 1 else (2 if bst[i] >= 480 else 1)
        else:
            rung = 0 if bst[i] < 350 else (1 if bst[i] < 460 else 2)
        plan[i] = FAMILIES[fam][rung]
    return plan, names

# ------------------------------------------------------------------ palette

COLORS = {
    "d": (44, 44, 52), "m": (96, 98, 108), "l": (176, 180, 190),     # gun steel
    "g": (246, 206, 64), "b": (176, 120, 36),                         # gold / brass
    "w": (140, 84, 40), "W": (248, 248, 248),                         # wood / white
    "r": (214, 36, 44), "e": (78, 168, 58), "E": (36, 100, 30),       # red / weed greens
    "o": (255, 140, 40), "s": (214, 214, 224), "t": (200, 164, 98),   # ember / smoke / tape
    "j": (66, 104, 170), "J": (40, 64, 112),                          # denim
}
REUSE = {"d": 900, "l": 900, "m": 300, "W": 700, "w": 2500, "s": 700, "b": 400, "r": 3500, "j": 2500}  # default 120
SHINY = {"d": (176, 120, 36), "m": (246, 206, 64), "l": (255, 240, 170)}            # gold-plated guns
ITEM_COLORS = {"shoe": "W", "cig": "Wobs", "pipe": "lWs", "brick": "Wt", "weed": "eE",
               "durag": "l", "beanie": "", "cap": "", "bandana": "W", "jeans": "jJl", "chain": "gbl", "grill": "gbl",
               "shades": "l", "sparkles": "W", "chain_back": "gb", "recolor": ""}


def dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def remap(im, table):
    """Rewrite pixel indices (Image.point would rewrite the palette instead)."""
    out = Image.frombytes("P", im.size, im.tobytes().translate(table))
    out.putpalette(im.getpalette())
    out.info["transparency"] = 0
    return out


def used_indices(images):
    used = set()
    for im in images:
        used |= set(im.tobytes())
    used.discard(0)
    return used


def free_slots(images, pal, spal, need, protect):
    """Return `need` unused palette indices, merging the most similar colour pairs if required."""
    used = used_indices(images)
    free = [i for i in range(1, 16) if i not in used]
    while len(free) < need:
        counts = [0] * 256
        for im in images:
            for v in im.tobytes():
                counts[v] += 1
        cand = sorted(used)
        best = None
        for a, i in enumerate(cand):
            for j in cand[a + 1:]:
                for keep, drop in ((i, j), (j, i)):
                    if drop in protect:
                        continue
                    cost = (dist(pal[i], pal[j]) + dist(spal[i], spal[j])) * (counts[drop] + 15)
                    if best is None or cost < best[0]:
                        best = (cost, keep, drop)
        _, keep, drop = best
        table = bytes(keep if v == drop else v for v in range(256))
        images = [remap(im, table) for im in images]
        used.discard(drop)
        free.append(drop)
    return free[:need], images


def accent_slots(pal, used):
    """The Pokémon's most characterful colour (for grips and mags), plus a darker and a lighter shade."""
    def hls(i):
        return colorsys.rgb_to_hls(*[v / 255 for v in pal[i]])

    ac = max(used, key=lambda i: hls(i)[2] * (1 - abs(hls(i)[1] - .5) * 1.4))
    same = [i for i in used if abs(hls(i)[0] - hls(ac)[0]) < .08] or [ac]
    return min(same, key=lambda i: sum(pal[i])), ac, max(same, key=lambda i: sum(pal[i]))

# ------------------------------------------------------------------ geometry helpers

def bbox(px, x0):
    pts = [(x, y) for y in range(80) for x in range(x0, x0 + 80) if px[x, y]]
    if not pts:
        return None
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def auto_hand(px, x0, view):
    """Front: grab the sprite's left edge ~60% down. Back: its right edge ~72% down."""
    bb = bbox(px, x0)
    if not bb:
        return None
    l, t, r, b = bb
    y = t + round((b - t) * (0.6 if view == "front" else 0.62))
    row = [x for x in range(l, r + 1) if px[x, y]]
    if not row:
        return (l + 3, y)
    return (min(row) + 3, y) if view == "front" else (min(max(row) - 1, x0 + 70), y)


def put(px, x, y, c, x0):
    if x0 <= x < x0 + 80 and 0 <= y < 80:
        px[x, y] = c

# ------------------------------------------------------------------ gun

def draw_gun(im, x0, hand, gun, scale, S, flash, mirror, clip=False):
    px = im.load()
    g, (gx, gy), (mx, my) = gunart.render(gun, scale)
    gpx = g.load()
    k = gunart
    lut = {k.OUT: S["out"], k.SK_D: S["d"], k.SK: S["m"], k.SK_L: S["l"], k.AC_D: S["ac_d"], k.AC: S["ac"],
           k.AC_L: S["ac_l"], k.WD_D: S["b"], k.WD: S["w"], k.GOLD: S["g"], k.GOLD_D: S["b"], k.WHITE: S["W"],
           k.FLASH: S["g"]}
    hx, hy = hand

    def place(x, y):
        return (hx - (x - gx) if mirror else hx + (x - gx)), hy + (y - gy)

    pts = {}
    for y in range(g.size[1]):
        for x in range(g.size[0]):
            if gpx[x, y]:
                pts[place(x, y)] = lut[gpx[x, y]]
    if flash:  # muzzle flash on the second animation frame
        for kx in range(1, 7):
            r = (6 - kx) // 2
            for dy in range(-r, r + 1):
                pts[place(mx + kx, my + dy)] = S["W"] if kx <= 2 and dy == 0 else S["g"]
    xs = [p[0] for p in pts]  # keep the gun inside its frame (back view: let the muzzle run off-screen)
    shift = 0 if clip else max(0, x0 + 1 - min(xs)) - max(0, max(xs) - (x0 + 78))
    for (x, y), c in pts.items():
        put(px, x + shift, y, c, x0)

# ------------------------------------------------------------------ drip

def crown(opaque, x1, x2, ceiling, floor, win=3):
    """Top edge of the head across x1..x2, ignoring thin spikes (ears, tufts, horns): each column takes the
    lowest top within +-win columns, so anything narrower than 2*win+1 pokes through instead of lifting it."""
    tops = {}
    for x in range(x1 - win, x2 + win + 1):
        tops[x] = next((y for y in range(ceiling, floor + 1) if opaque(x, y)), None)
    out = {}
    for x in range(x1, x2 + 1):
        near = [tops[k] for k in range(x - win, x + win + 1) if tops[k] is not None]
        if near:
            out[x] = max(near)
    return out


def draw_fitcap(item, S, P, opaque):
    """An overlaid hat on the head: a shell one pixel outside the head's crown (ears and tufts poke through,
    see crown()), at least a few pixels tall, fully outlined and shaded, down to the brow line - then the
    style's details (durag tails, beanie cuff + pom, snapback brim, bandana knot)."""
    out = S["out"]
    ck = item.get("color", "k")
    col = out if ck == "k" else S[ck]
    shine = S["m"] if ck in ("k", "ac", "r", "j") else S["l"]
    if ck == "W":
        shine = S["l"]
    style, cx, band, w = item["style"], item["cx"], item["band"], item["w"]
    half = w // 2
    x1, x2 = cx - half, cx + half
    top = crown(opaque, x1, x2, max(0, band - 2 * w), band)
    if not top:
        return
    mid = sorted(top.values())[len(top) // 2]
    band = min(band, mid + max(3, round(w * .35)))            # a hat sits on the crown - never down the face
    tall = max(4, round(w * .38)) if style != "bandana" else 3
    shell = {}
    for x, y in top.items():
        k = (x - cx) / max(1, half + 1)
        dome = band - round(tall * max(0.0, 1 - k * k) ** .5)   # an elliptical dome over the brow line...
        shell[x] = min(y - 1, max(dome, band - tall)) if style != "bandana" else band - tall
        shell[x] = min(shell[x], band - 2)                      # ...never thinner than a band
        if style != "bandana":
            shell[x] = min(y - 1, dome) if y - 1 < band - 1 else dome
    lo, hi = min(shell), max(shell)
    shell[lo - 1] = shell[lo] + 1                              # outset sides, rounded
    shell[hi + 1] = shell[hi] + 1
    lo, hi = lo - 1, hi + 1
    peak = min(shell.values())
    for x, y in shell.items():
        for yy in range(y, band + 1):
            if x in (lo, hi) or yy == y:
                P(x, yy, out)
            elif yy == band:
                P(x, yy, (shine if x % 2 else col) if style == "beanie" else out)
            elif style == "beanie" and yy == band - 1:
                P(x, yy, shine if x % 2 else col)
            else:
                P(x, yy, shine if (0 <= x - lo - 2 <= 1 and yy - y in (1, 2)) else col)
    side = item.get("side", 1)
    if style == "durag":                                       # tails off the back of the head
        tx = (hi if side >= 0 else lo) if side else cx
        for k in range(1, 7):
            x = tx + (side * (k // 2) if side else 0)
            P(x, band + k, col)
            P(x + 1, band + k, col if k < 6 else shine)
            P(x - 1, band + k, out)
            P(x + 2, band + k, out)
    elif style == "beanie":                                    # pom-pom
        for dx in range(-2, 3):
            for dy in range(-3, 0):
                P(cx + dx, peak + dy, col if abs(dx) < 2 and dy > -3 else out)
        P(cx, peak - 2, shine)
    elif style == "snapback":                                  # backwards brim
        if side:
            bx = hi if side > 0 else lo
            for k in range(1, max(4, w // 3)):
                P(bx + side * k, band - 1, col)
                P(bx + side * k, band - 2, out)
                P(bx + side * k, band, out)
        P(cx, peak + 1, shine)                                 # button
    elif style == "bandana" and side:                          # knot + ends at the back
        kx = (hi + 1) if side > 0 else (lo - 1)
        for k in range(3):
            P(kx + side * k, band - 1, col)
            P(kx + side * k, band + k // 2, col)
        P(kx + side * 3, band + 2, col)


def draw_drip(im, x0, item, S, off, frame):
    """Hand-placed accessories from drip.json, in frame-1 coordinates."""
    px = im.load()
    out = S["out"]

    def P(x, y, c):
        put(px, x0 + x + off[0], y + off[1], c, x0)

    def opaque(x, y):
        X, Y = x0 + x + off[0], y + off[1]
        return x0 <= X < x0 + 80 and 0 <= Y < 80 and px[X, Y] != 0

    t = item["type"]
    if t == "chain":
        x1, x2, y, sag = item["x1"], item["x2"], item["y"], item.get("sag", 4)
        mid, half = (x1 + x2) / 2, max(1, (x2 - x1) / 2)
        for x in range(x1, x2 + 1):
            yy = y + round(sag * (1 - ((x - mid) / half) ** 2))
            P(x, yy - 1, out)
            P(x, yy, S["g"] if x % 3 else S["l"])
            P(x, yy + 1, S["b"] if x % 2 else S["g"])
            P(x, yy + 2, out)
        mx, my = round(mid), y + sag + 2
        for dx in range(-2, 3):
            for dy in range(4):
                P(mx + dx, my + dy, S["g"] if abs(dx) < 2 else S["b"])
        P(mx - 1, my, S["l"])
        for dx in range(-3, 4):
            P(mx + dx, my + 4, out)
        for dy in range(4):
            P(mx - 3, my + dy, out)
            P(mx + 3, my + dy, out)
    elif t == "chain_back":
        for x in range(item["x1"], item["x2"] + 1):
            P(x, item["y"], S["g"] if x % 2 else S["b"])
            P(x, item["y"] + 1, out)
    elif t == "grill":
        x1, x2, y = item["x1"], item["x2"], item["y"]
        for x in range(x1, x2 + 1):
            P(x, y, S["g"])
            P(x, y + 1, S["g"] if x % 2 else S["b"])
        P(x1 + 1, y, S["l"])
    elif t == "shades":
        x1, x2, y, h = item["x1"], item["x2"], item["y"], item.get("h", 3)
        for x in range(x1, x2 + 1):
            for dy in range(h):
                P(x, y + dy, out)
        P(x1 + 1, y, S["l"])
        P((x1 + x2) // 2 + 2, y, S["l"])
    elif t == "jeans":
        x1, x2, y1, y2 = item["x1"], item["x2"], item["y1"], item["y2"]
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                P(x, y, S["j"] if (x + 2 * y) % 7 else S["J"])
        for x in range(x1, x2 + 1):  # boxers over the waistband
            P(x, y1 - 1, S["l"] if x % 3 else S["J"])
            P(x, y1 - 2, S["l"])
            P(x, y1 - 3, out)
            P(x, y2 + 1, out)
        for y in range(y2 - 3, y2 + 1):
            P((x1 + x2) // 2, y, S["J"])
        for y in range(y1 - 3, y2 + 2):
            P(x1 - 1, y, out)
            P(x2 + 1, y, out)
    elif t == "shoe":
        x, y, w = item["x"], item["y"], item.get("w", 8)
        jordan = item.get("style", "white") in ("jordan", "concord")
        if item.get("style") == "concord":
            S = dict(S, r=S["out"])
        for i in range(w):
            toe = i < w * 0.45
            if not toe:
                P(x + i, y, S["r"] if jordan else S["W"])
            P(x + i, y + 1, (S["W"] if toe else S["r"]) if jordan else S["W"])
            P(x + i, y + 2, S["W"] if not jordan or toe else S["r"])
            P(x + i, y + 3, S["W"])
            P(x + i, y + 4, out)
        for i in range(w // 3, w - 1):  # swoosh
            P(x + i, y + 2 - (1 if i > w * 0.7 else 0), out)
        for yy in range(y, y + 5):
            P(x - 1, yy, out)
            P(x + w, yy, out)
        for i in range(w):
            if i >= w * 0.45:
                P(x + i, y - 1, out)
            else:
                P(x + i, y, out)
    elif t in ("cig", "pipe"):
        x, y, dirn = item["x"], item["y"], item.get("dir", -1)
        if t == "cig":
            for i in range(6):
                P(x + dirn * i, y, S["b"] if i < 2 else S["W"])
                P(x + dirn * i, y - 1, out)
                P(x + dirn * i, y + 1, out)
            P(x + dirn * 6, y, S["o"])
            P(x + dirn * 7, y, out)
            tip = x + dirn * 6
        else:
            for i in range(5):
                P(x + dirn * i, y, S["l"])
                P(x + dirn * i, y - 1, out)
                P(x + dirn * i, y + 1, out)
            bx = x + dirn * 7
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx * dx + dy * dy <= 5:
                        P(bx + dx, y + dy, S["W"] if dx * dx + dy * dy <= 2 else out)
            P(bx, y - 1, S["l"])
            tip = bx
        puff = ([(0, -3), (1, -5), (0, -7), (-1, -8), (1, -10)] if frame == 0
                else [(1, -3), (0, -5), (1, -7), (2, -9), (0, -11)])
        for dx, dy in puff:
            for ex, ey in ((0, 0), (1, 0), (0, 1)):
                P(tip + dx + ex, y + dy + ey, S["s"])
    elif t == "brick":
        x, y, w, h = item["x"], item["y"], item.get("w", 11), item.get("h", 7)
        for xx in range(x, x + w):
            for yy in range(y, y + h):
                P(xx, yy, S["W"])
        for yy in range(y, y + h):
            P(x + w // 2, yy, S["t"])
        for xx in range(x, x + w):
            P(xx, y + h // 2, S["t"])
        for xx in range(x - 1, x + w + 1):
            P(xx, y - 1, out)
            P(xx, y + h, out)
        for yy in range(y, y + h):
            P(x - 1, yy, out)
            P(x + w, yy, out)
    elif t == "weed":
        cx, cy, s = item["x"], item["y"], item.get("size", 8)
        cells = {}
        for ang, frac in ((0, 1), (-32, .85), (32, .85), (-64, .62), (64, .62), (-100, .35), (100, .35)):
            a = math.radians(ang + item.get("tilt", 0))
            n = max(2, round(s * frac))
            for k in range(n + 1):
                wdt = 2 if 0 < k < n * .8 else 1
                bx, by = cx + math.sin(a) * k, cy - math.cos(a) * k
                for o in range(-wdt + 1, wdt):
                    p = (round(bx + math.cos(a) * o * .8), round(by + math.sin(a) * o * .8))
                    if o == 0:
                        cells[p] = S["E"]
                    else:
                        cells.setdefault(p, S["e"])
        for (x, y) in list(cells):
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if (x + dx, y + dy) not in cells:
                    P(x + dx, y + dy, out)
        for (x, y), c in cells.items():
            P(x, y, c)
        for k in range(1, 4):
            P(cx, cy + k, S["E"])
    elif t in ("durag", "beanie", "cap", "bandana"):
        x1, x2, y, h = item["x1"], item["x2"], item["y"], item.get("h", 6)
        ck = item.get("color", "r")
        col = S["out"] if ck == "k" else S[ck]
        shine = S["m"] if ck in ("k", "r", "j", "ac") else S["l"]
        for yy in range(y, y + h):
            for xx in range(x1, x2 + 1):
                if opaque(xx, yy):
                    P(xx, yy, col)
        for xx in range(x1, x2 + 1):
            if t == "durag" and xx % 4 == 0 and opaque(xx, y + 2):
                P(xx, y + 2, shine)                       # silky shine
            if t == "bandana" and xx % 3 == 0 and opaque(xx, y + 1 + (xx % 2) * 2):
                P(xx, y + 1 + (xx % 2) * 2, S["W"])       # paisley dots
            if t == "cap" and opaque(xx, y + h - 1):
                P(xx, y + h - 1, out)
            if t == "beanie" and opaque(xx, y + h - 1):
                P(xx, y + h - 1, out)                     # ribbed brim line
        if t == "cap":                                    # backwards brim, or the snapback strap from behind
            side = item.get("brim", "right")
            if side == "none":
                cx = (x1 + x2) // 2
                for dx in range(-2, 3):
                    P(cx + dx, y + h - 2, out if abs(dx) == 2 else S["W"])
            else:
                bx = list(range(x2 - 1, x2 + 6)) if side == "right" else list(range(x1 - 5, x1 + 2))
                for xx in bx:
                    P(xx, y + h - 3, out)
                    P(xx, y + h - 2, col)
                    P(xx, y + h - 1, out)
                P(bx[-1] + 1 if side == "right" else bx[0] - 1, y + h - 2, out)
        elif t == "bandana":                              # knot
            kx = x2 + 1 if item.get("knot", "right") == "right" else x1 - 3
            for dx in range(3):
                for dy in range(3):
                    P(kx + dx, y + h - 3 + dy, col if (dx, dy) != (1, 1) else shine)
            for dy in range(-1, 4):
                P(kx - 1, y + h - 3 + dy, out)
                P(kx + 3, y + h - 3 + dy, out)
        elif t == "durag":                                # tails hanging off the back
            tx = item.get("tail_x", x2)
            for k in range(item.get("tail", 8)):
                for dx in (0, 1):
                    P(tx + dx + k // 4, y + h - 2 + k, col)
                P(tx + 2 + k // 4, y + h - 2 + k, out)
                P(tx - 1 + k // 4, y + h - 2 + k, out)
            P(tx + (item.get("tail", 8) - 1) // 4, y + h - 2 + item.get("tail", 8), out)
        elif t == "beanie":                               # pom-pom
            cx = (x1 + x2) // 2
            for dx in range(-2, 3):
                for dy in range(-3, 0):
                    P(cx + dx, y + dy, col if abs(dx) < 2 and dy > -3 else out)
    elif t == "hat":
        ck = item.get("color", "k")
        col = out if ck == "k" else S[ck]
        roles = {"c": col, "s": S["m"] if ck in ("k", "ac", "r", "j") else S["l"], "o": out,
                 "W": S["W"], "g": S["g"]}
        if ck == "W":
            roles["W"] = S["l"]
        for (dx, dy), role in hats.hat(item["style"], item["w"], item.get("side", 1)).items():
            P(item["cx"] + dx, item["by"] + dy, roles[role])
    elif t == "fitcap":
        draw_fitcap(item, S, P, opaque)
    elif t == "sparkles":
        rng = random.Random(item.get("seed", 1) + frame)
        bb = bbox(px, x0)
        if bb:
            for _ in range(item.get("n", 10)):
                for _try in range(30):
                    x, y = rng.randint(bb[0], bb[2]), rng.randint(bb[1], bb[3])
                    if px[x, y] not in (0, out):
                        px[x, y] = S["W"]
                        break


def find_pupils(px, pal, l, t, r, b):
    """Pupils = small isolated dark spots surrounded by lighter, opaque skin (outlines are long, so they fail)."""
    lum = [sum(c) for c in pal]
    H = b - t + 1
    seen, spots = set(), []
    for y in range(t + 1, t + round(H * .6)):
        for x in range(l + 1, r):
            v = px[x, y]
            if (x, y) in seen or not v or lum[v] >= 330:
                continue
            blob, stack = [], [(x, y)]
            seen.add((x, y))
            while stack and len(blob) <= 10:
                cx, cy = stack.pop()
                blob.append((cx, cy))
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        q = (cx + dx, cy + dy)
                        if q not in seen and 0 <= q[0] < 80 and 0 <= q[1] < 80 and px[q] and lum[px[q]] < 330:
                            seen.add(q)
                            stack.append(q)
            if len(blob) > 8 or stack:
                continue
            xs, ys = [p[0] for p in blob], [p[1] for p in blob]
            ring = [(xx, yy) for xx in range(min(xs) - 1, max(xs) + 2) for yy in range(min(ys) - 1, max(ys) + 2)
                    if (xx, yy) not in blob and 0 <= xx < 80 and 0 <= yy < 80]
            if any(px[q] == 0 for q in ring):
                continue
            if max(lum[px[q]] for q in ring) < 520:
                continue
            spots.append((sum(xs) / len(xs), sum(ys) / len(ys)))
    if not spots:
        return None
    pairs = [((a[0] + c[0]) / 2, (a[1] + c[1]) / 2) for i, a in enumerate(spots) for c in spots[i + 1:]
             if abs(a[1] - c[1]) <= 4 and 3 <= abs(a[0] - c[0]) <= 24]
    x, y = min(pairs or spots, key=lambda q: q[1])
    return round(x), round(y)


def find_eyes(px, pal, l, t, r, b):
    found = find_pupils(px, pal, l, t, r, b)
    if found:
        return found
    return find_highlights(px, pal, l, t, r, b)


def find_highlights(px, pal, l, t, r, b):
    """Eyes = light pixels touching a dark pupil, well inside the body. Returns (x, y) or None."""
    lum = [sum(c) for c in pal]
    H = b - t + 1
    cand = []
    for y in range(t + 2, t + round(H * .6)):
        for x in range(l + 2, r - 1):
            v = px[x, y]
            if not v or lum[v] < 560:
                continue
            if any(px[x + dx, y + dy] == 0 for dx in (-2, 0, 2) for dy in (-2, 0, 2)):
                continue
            if any(px[x + dx, y + dy] != 0 and lum[px[x + dx, y + dy]] < min(340, lum[v] - 300)
                   for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
                cand.append((x, y))
    if not cand:
        return None
    clusters = []
    for x, y in cand:
        for c in clusters:
            if any(abs(x - a) <= 2 and abs(y - b2) <= 2 for a, b2 in c):
                c.append((x, y))
                break
        else:
            clusters.append([(x, y)])
    cents = [(sum(p[0] for p in c) / len(c), sum(p[1] for p in c) / len(c), len(c)) for c in clusters if len(c) <= 12]
    if not cents:
        return None
    pairs = [((a[0] + b2[0]) / 2, (a[1] + b2[1]) / 2) for i, a in enumerate(cents) for b2 in cents[i + 1:]
             if abs(a[1] - b2[1]) <= 4 and 3 <= abs(a[0] - b2[0]) <= 24]
    if pairs:
        x, y = min(pairs, key=lambda q: q[1])
    else:
        x, y, _ = min(cents, key=lambda q: q[1])
    return round(x), round(y)


def track(px, x, y, r=7, search=8):
    """Where did the pixels around (x, y) in frame 1 move to in frame 2? Returns (dx, dy)."""
    import numpy as np
    a = np.array([[px[i, j] for i in range(160)] for j in range(80)], dtype=np.int16)
    f1 = np.pad(a[:, :80], search + r, constant_values=0)
    f2 = np.pad(a[:, 80:], search + r, constant_values=0)
    o = search + r
    patch = f1[o + y - r:o + y + r + 1, o + x - r:o + x + r + 1]
    best = (None, 0, 0)
    for dy in range(-search, search + 1):
        for dx in range(-search, search + 1):
            win = f2[o + y + dy - r:o + y + dy + r + 1, o + x + dx - r:o + x + dx + r + 1]
            nz = (patch != 0) | (win != 0)
            score = int(2 * ((patch == win) & nz).sum() - ((patch != win) & nz).sum()) - abs(dx) - abs(dy)
            if best[0] is None or score > best[0]:
                best = (score, dx, dy)
    return best[1], best[2]


def anchor(item):
    if "cx" in item:
        return item["cx"], item.get("by", item.get("band"))
    if "x" in item:
        return item["x"] + item.get("w", 0) // 2, item["y"] + item.get("h", 0) // 2
    if "x1" in item:
        y = item.get("y", item.get("y1", 40))
        return (item["x1"] + item["x2"]) // 2, y + item.get("h", 2) // 2
    return None


def runs(px, y, l, r, x0):
    found, start = [], None
    for x in range(l, r + 2):
        on = x <= r and px[x0 + x, y] != 0
        if on and start is None:
            start = x
        if not on and start is not None:
            found.append((start, x - 1))
            start = None
    return found


def head_point(px, pal, view, override=None):
    """Eye-level point of the head: hand-set override, detected pupils, or a silhouette guess."""
    bb = bbox(px, 0)
    if not bb:
        return None
    if override:
        return tuple(override)
    l, t, r, b = bb
    W, H = r - l + 1, b - t + 1
    eyes = find_eyes(px, pal, l, t, r, b) if (pal and view == "front") else None
    if eyes:
        return eyes
    # no eyes: heads face the opponent -- upper-left on fronts, upper-right on backs
    best = None
    for y in range(t, t + max(4, round(H * .45))):
        for a, z in runs(px, y, l, r, 0):
            if z - a + 1 < max(6, W * .18):
                continue
            c = (a + z) / 2
            lean = (r - c) if view == "front" else (c - l)
            score = (y - t) - .6 * lean
            if best is None or score < best[0]:
                best = (score, round(c), y)
    return (best[1], min(b, best[2] + 5)) if best else None


def neck_chain(px, l, r, b, hx, hy, w, hand=None):
    """Hang the chain on the neck: below the head, the narrowest point of the silhouette around the head's
    centre column (no visible neck: just under the chin). Width comes from the neck, so it wraps the neck
    instead of spanning the belly like a belt."""
    def run_at(y):
        rr = runs(px, y, l, r, 0)
        if not rr:
            return None
        return min(rr, key=lambda q: 0 if q[0] <= hx <= q[1] else min(abs(q[0] - hx), abs(q[1] - hx)))
    lo, hi = hy + 3, min(b - 5, hy + max(9, round(w * .8)))   # head to upper chest - not down to the legs
    if hand:
        hi = min(hi, hand[1] - 5)                                 # and above the gun hand, or the gun hides it
    rows = [(y, run_at(y)) for y in range(lo, hi + 1)]
    rows = [(y, q) for y, q in rows if q and q[1] - q[0] >= 5]
    if not rows:
        return None
    head_w = max(q[1] - q[0] for _, q in rows[:4])
    y, (a, z) = min(rows, key=lambda yq: (yq[1][1] - yq[1][0], yq[0]))
    if (z - a) > head_w * .85:                                  # no real neck: just under the chin
        y = min(hi, hy + max(6, round(w * .45)))
        q = run_at(y)
        if not q:
            return None
        a, z = q
    c = (a + z) // 2
    half = max(4, min(11, round((z - a) * .42)))
    return {"type": "chain", "x1": c - half, "x2": c + half, "y": y + 1, "sag": max(2, min(4, half // 2))}


def auto_drip(im, view, rng, stage, iced, skip, has_red=False, pal=None, head=None, hat_w=None, hand=None):
    """Dress the Pokémon up around its head point: overlaid hat, chain, kicks, ice."""
    px = im.load()
    bb = bbox(px, 0)
    if not bb:
        return []
    l, t, r, b = bb
    W, H = r - l + 1, b - t + 1
    items = []
    hp = head_point(px, pal, view, head)
    style = rng.choice(["durag", "beanie", "snapback", "snapback", "durag"])   # (a bandana reads as a stripe here)
    color = rng.choices(["k", "W", "r", "g"], [45, 20, 20, 15])[0]
    if pal is not None:                                        # never the same colour as the body: it'd vanish
        from collections import Counter
        body = Counter(v for v in im.getdata() if v and pal[v] != (0, 0, 0)).most_common(1)
        if body:
            main = pal[body[0][0]]
            options = [c for c in ("k", "W", "r", "g") if dist({"k": (24, 24, 28)}.get(c) or COLORS[c], main) > 9000]
            if color not in options and options:
                color = options[0]
    if hp:
        hx, hy = hp
        brow = max(t, hy - 3)
        rr = [q for q in runs(px, brow, l, r, 0) if q[0] - 2 <= hx <= q[1] + 2] or [(hx - 5, hx + 5)]
        a, z = rr[0]
        a, z = max(a, hx - 12), min(z, hx + 12)
        w = hat_w or max(10, min(24, z - a + 3))
        cx = (a + z) // 2
        if "head" not in skip:
            items.append({"type": "fitcap", "style": style, "cx": cx, "band": brow, "w": w, "color": color,
                          "side": 1 if view == "front" else 0})
        if "chain" not in skip and view == "front":
            chain = neck_chain(px, l, r, b, hx, hy, w, hand)
            if chain:
                items.append(chain)

    if view == "front" and "shoe" not in skip and b < 77 and H > 18:
        feet = [q for q in runs(px, b, l, r, 0) if 2 <= q[1] - q[0] <= max(14, W * .3)]
        if 1 <= len(feet) <= 4:
            for a, z in feet:
                items.append({"type": "shoe", "x": a - 1, "y": b - 3, "w": z - a + 3,
                              "style": ("jordan" if has_red else "concord") if stage >= 2 else "white"})
    if iced:
        items.append({"type": "sparkles", "n": 6 + 2 * stage, "seed": rng.randint(0, 999)})
    return items


def recolor(pal, spal, used, item, keep):
    """Re-tint every colour (e.g. Onix -> blue crystal) while keeping its lightness."""
    h_new, s_new, lift = item.get("hue", .53), item.get("sat", .7), item.get("lift", .1)
    for p in (pal, spal):
        for i in used:
            if i in keep:
                continue
            h, l, s = colorsys.rgb_to_hls(*[v / 255 for v in p[i]])
            r, g, b = colorsys.hls_to_rgb(h_new, min(.95, l + lift), s_new)
            p[i] = (round(r * 255), round(g * 255), round(b * 255))

# ------------------------------------------------------------------ one species

def frame_offset(px):
    a, b = bbox(px, 0), bbox(px, 80)
    if not a or not b:
        return (0, 0)
    return (b[0] - 80 - a[0], b[1] - a[1])


def arm(n, gun, drip, paths=None):
    """Dress species n. `paths` overrides the sprite files (used for alternate forms)."""
    folder = SPRITES / f"{n:04d}"
    paths = paths or [folder / s / v for s in ("male", "female") for v in ("front.png", "back.png")]
    live = [(p, im) for p, im in ((p, git_png(p)) for p in paths) if im is not None]
    if not live:
        return None
    front_src = next(im for p, im in live if p.name == "front.png")
    back_src = next(im for p, im in live if p.name == "back.png")
    pal = [tuple(front_src.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
    spal = [tuple(back_src.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
    spec = drip.get(str(n), {})
    stage = STAGES.get(n, 1)
    iced = n in LEGENDARY or (stage >= 2 and BST.get(n, 0) >= 480)
    per_view = {}
    pal0 = [tuple(front_src.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
    used0 = used_indices([im for _, im in live])
    has_red = any(dist(pal0[i], COLORS["r"]) < 3500 for i in used0)
    for path, im in live:
        view = "front" if path.name == "front.png" else "back"
        manual = spec.get(view, [])
        kinds = {i["type"] for i in manual}
        skip = set()
        if kinds & {"durag", "beanie", "cap", "bandana", "hat", "fitcap"}:
            skip.add("head")
        if kinds & {"chain", "chain_back"}:
            skip.add("chain")
        if "shoe" in kinds:
            skip.add("shoe")
        hand0 = spec.get("hand_" + view)
        hand0 = tuple(hand0) if hand0 else auto_hand(im.load(), 0, view)
        auto = [] if spec.get("auto") is False else auto_drip(
            im, view, random.Random(n * 7919), stage, iced and "sparkles" not in kinds, skip, has_red, pal0,
            spec.get("head_" + view), spec.get("hat_w"), hand0)
        per_view[path] = auto + manual
    items = [i for v in per_view.values() for i in v]

    images = [im for _, im in live]
    used = used_indices(images)
    out_idx = min(used, key=lambda i: sum(pal[i]))
    for item in items:
        if item["type"] == "recolor":
            recolor(pal, spal, used, item, keep={out_idx})
    acc = accent_slots(pal, used - {out_idx})

    # only ask for the colours this gun and this drip actually use
    k = gunart
    gun_slots = set(gunart.render(gun, .6)[0].tobytes())
    wanted = ["m", "d", "l", "g", "W"]
    if gun_slots & {k.WD, k.WD_D, k.GOLD_D}:
        wanted += ["w", "b"]
    for item in items:
        cols = ITEM_COLORS.get(item["type"], "")
        if item["type"] == "shoe" and item.get("style") == "jordan":
            cols += "r"
        if item["type"] in ("durag", "beanie", "cap", "bandana", "hat", "fitcap") and item.get("color", "r") in COLORS:
            cols += item.get("color", "r")
        for c in cols:
            if c not in wanted:
                wanted.append(c)
    S = {"out": out_idx, "ac_d": acc[0], "ac": acc[1], "ac_l": acc[2]}
    need = []
    for k in wanted:  # reuse the sprite's own colours where they're close enough
        near = min(used, key=lambda i: dist(pal[i], COLORS[k]))
        if dist(pal[near], COLORS[k]) < REUSE.get(k, 120):
            S[k] = near
        else:
            need.append(k)
    got, images = free_slots(images, pal, spal, len(need), protect={out_idx, *acc})
    for k, i in zip(need, got):
        S[k] = i
        pal[i] = COLORS[k]
        spal[i] = SHINY.get(k, COLORS[k])
    for key in ("w", "b"):
        S.setdefault(key, S["d"])

    out = {}
    for (path, _), im in zip(live, images):
        view = "front" if path.name == "front.png" else "back"
        im = im.copy()
        px = im.load()
        src = im.copy().load()          # untouched pixels for motion tracking
        f2 = frame_offset(px)
        moves = {}
        for k2, item in enumerate(per_view[path]):
            a = anchor(item)
            moves[k2] = track(src, *a) if a else f2
        hand1 = spec.get("hand_" + view)
        hand1 = tuple(hand1) if hand1 else auto_hand(src, 0, view)
        hand_move = track(src, *hand1) if hand1 else (0, 0)
        for f, x0 in enumerate((0, 80)):
            bb = bbox(px, x0)
            if bb is None:              # blank frame (e.g. Unown has no 2nd frame): leave it blank
                continue
            for k2, item in enumerate(per_view[path]):
                if item["type"] != "recolor":
                    draw_drip(im, x0, item, S, moves[k2] if f else (0, 0), f)
            hand = (hand1[0] + x0 + (hand_move[0] if f else 0), hand1[1] + (hand_move[1] if f else 0)) if hand1 else None
            if hand and bb:
                size = max(bb[2] - bb[0], bb[3] - bb[1])
                scale = spec.get("gun_scale") or (min(1.0, max(.42, size / 80 * .85)) if view == "front"
                                                  else min(1.2, max(.85, size / 80 * 1.25)))
                if view == "back":  # sprites are a fixed 80x80: shrink a little if the muzzle runs way off
                    while scale > .7:
                        g, (gx, _), _ = gunart.render(gun, scale)
                        gw = max(x for x in range(g.size[0]) if any(g.getpixel((x, y)) for y in range(g.size[1])))
                        if hand[0] + (gw - gx) <= x0 + 79:
                            break
                        scale -= .05
                draw_gun(im, x0, hand, gun, scale, S, flash=(f == 1 and view == "front"),
                         mirror=(view == "front"))
        im.putpalette([v for c in (pal if view == "front" else spal) for v in c])
        im.info["transparency"] = 0
        out[path] = im
    return out, pal

# ------------------------------------------------------------------ main

def main():
    args = sys.argv[1:]
    opt = lambda name, default=None: args[args.index(name) + 1] if name in args else default
    preview = opt("--preview")
    only = [int(x) for x in opt("--only").split(",")] if opt("--only") else None
    plan, names = gun_plan()
    drip = {k: v for k, v in json.loads(DRIP.read_text(encoding="utf-8")).items() if not k.startswith("_")}
    ids = only or list(range(1, 494))
    sheet = []
    for n in ids:
        plan[n] = drip.get(str(n), {}).get("gun", plan[n])   # per-Pokémon override
        res = arm(n, plan[n], drip)
        if not res:
            continue
        out, pal = res
        if preview:
            imgs = {p.parent.name + "/" + p.name: im for p, im in out.items()}
            f = imgs.get("male/front.png") or imgs.get("female/front.png")
            b = (imgs.get("male/back.png") or imgs.get("female/back.png")).copy()
            b.putpalette([v for c in pal for v in c])  # battle shows backs in the normal palette
            b.info["transparency"] = 0
            sheet.append((n, names[n], plan[n], f, b))
        else:
            for p, im in out.items():
                im.save(p, transparency=0)
    if not preview:
        print(f"strapped {len(ids)} species")
        return
    cols, cw, ch = int(opt("--cols", 4)), 330, 96
    img = Image.new("RGB", (cols * cw, ((len(sheet) + cols - 1) // cols) * ch), (205, 225, 205))
    d = ImageDraw.Draw(img)
    for k, (n, name, gun, f, b) in enumerate(sheet):
        x, y = (k % cols) * cw, (k // cols) * ch
        fr, br = f.convert("RGBA"), b.convert("RGBA").crop((0, 0, 80, 80))
        img.paste(fr, (x, y + 12), fr)
        img.paste(br, (x + 165, y + 12), br)
        d.text((x + 2, y), f"{n} {name} - {gun}", fill=(0, 0, 0))
    z = int(opt("--zoom", 2))
    img = img.resize((img.width * z, img.height * z), Image.NEAREST)
    img.save(preview)
    print("preview:", preview)


if __name__ == "__main__":
    main()
