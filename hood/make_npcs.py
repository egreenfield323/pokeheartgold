#!/usr/bin/env python3
"""Overworld people (files/data/mmodel/mmodel/*.NSBTX, models 0-296):
every human gets a hat + chain, gang-ish ones get a gun, the player gets a durag + chain + pistol
in every state, Lyra/Ethan rep a red bandana, and the professors look like they've been up for days:
Oak in a wife beater with bare legs, Elm in a stained coat, both with powder under the nose.
Originals are read from the base commit 77565981b. Run from the repo root:  python hood/make_npcs.py [--preview out.png]
"""
import json
import math
import random
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_overworld as mo  # noqa: E402
import make_sprites as ms  # noqa: E402
import nsbtx  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MM = ROOT / "files/data/mmodel/mmodel"
NOT_PEOPLE = re.compile(r"ROCK|TREE|BALL|DOOR|PIKACHU|GYARADOS|KABIGON|^ICE$|ROTOM|FOLLOWER|YADON|_OBJ|TROPHY|STATUE"
                        r"|SIGN|POKEWALL|SCROLL|MEDAL|MONO_PIP|^STOP$|BONGURI|BONMI|SPPOKE|GINGA|T5_O01|TSURE|R09_O01"
                        r"|AJI_PERU|RAPURASU|^BOZU$|TOROPHY|USOKKY")
ARMED = re.compile(r"BADMAN|GANG|ROCKET|RKANBU|POLICE|FIGHTER|LEADER|BIGFOUR|WATARU|SAKAKI|THIEF|GSRIVEL|RED$|MYSTERY"
                   r"|SUNGLASSES|SEAMAN|BIGMAN|BOARDER|FIRE$|CHAMPION|TOWERBOSS|BRAINS|SEVEN")
PLAYER = re.compile(r"HERO")
FRIEND = re.compile(r"^F_HERO")
OAK, ELM = "OOKIDO", "DOCTOR"
MOM = "GSMAMA"


def models():
    out = {}
    for line in (ROOT / "include/constants/mmodel.h").read_text().splitlines():
        m = re.match(r"#define MMODEL_(\w+)\s+(\d+)$", line.strip())
        if m and int(m.group(2)) < 297 and not NOT_PEOPLE.search(m.group(1)):
            out[int(m.group(2))] = m.group(1)
    return out


def frame_dirs(texs):
    """Frames sorted by number come in blocks per direction: away, toward, left, right. Walking sheets use blocks
    of 4, repeating for the player's running / biking sets (24 or 32 frames); shorter sheets (surfing, ladder,
    ...) have a single block per direction."""
    order = sorted(range(len(texs)), key=lambda i: int(re.sub(r"\D", "", texs[i]["name"].rsplit(".", 1)[-1]) or 0))
    per = 4 if len(texs) >= 16 else max(1, len(texs) // 4)
    dirs = [None] * len(texs)
    for rank, i in enumerate(order):
        dirs[i] = ["up", "down", "left", "right"][(rank // per) % 4 if len(texs) >= 16 else min(3, rank // per)]
    return dirs


def nearest(pal, used, color):
    return min(used, key=lambda i: ms.dist(pal[i], color))


def powder(rows, skin):
    """A couple of white pixels under the nose on camera-facing frames."""
    pts = [(x, y) for y in range(len(rows) // 2 + 4) for x in range(len(rows[0])) if rows[y][x] == skin]
    if not pts:
        return
    xs = sorted(p[0] for p in pts)
    cx = xs[len(xs) // 2]
    bottom = max(p[1] for p in pts if abs(p[0] - cx) <= 2)
    return cx, bottom - 1


DRIP = ROOT / "hood/data/npc_drip.json"
PIECE_COLORS = {"r": (214, 36, 44), "u": (40, 80, 200), "p": (236, 120, 176), "o": (255, 140, 40),
                "e": (78, 168, 58), "pl": (255, 196, 224)}   # k, W, g are always there (outline, white, gold)
FACING = ("down", "up", "left", "right")


def load_drip():
    """Hand-placed overworld drip (the drip editor), keyed by model name: per facing direction ("down", "up",
    "left", "right") a list of pieces - gun {kind}, chain {heavy}, hat {style, color}, bonnet {color},
    powder - each with an optional dx/dy shift; "auto_<dir>": false means the list replaces the automatic one."""
    return json.loads(DRIP.read_text(encoding="utf-8")) if DRIP.exists() else {}


def layer(rows, new, dx, dy, scale=1):
    """Composite what a piece changed (rows -> new) onto rows, scaled about its centre (nearest neighbour) and
    shifted by (dx, dy). Returns (rows, box)."""
    h, w = len(rows), len(rows[0])
    pts = [(x, y) for y in range(h) for x in range(w) if new[y][x] != rows[y][x]]
    if not pts:
        return rows, None
    if scale != 1:
        got = {(x, y): new[y][x] for x, y in pts}
        xs, ys = [x for x, _ in pts], [y for _, y in pts]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        scaled = {}
        for Y in range(math.floor(cy + (min(ys) - cy - .5) * scale), math.ceil(cy + (max(ys) - cy + .5) * scale) + 1):
            for X in range(math.floor(cx + (min(xs) - cx - .5) * scale), math.ceil(cx + (max(xs) - cx + .5) * scale) + 1):
                src = (math.floor(cx + (X - cx) / scale + .5), math.floor(cy + (Y - cy) / scale + .5))
                if src in got:
                    scaled[X, Y] = got[src]
        pts, new = list(scaled), None
    else:
        scaled = {(x, y): new[y][x] for x, y in pts}
    if dx or dy or new is None:
        out = [r[:] for r in rows]
        for (x, y), c in scaled.items():
            if 0 <= x + dx < w and 0 <= y + dy < h:
                out[y + dy][x + dx] = c
        new = out
    xs, ys = [x + dx for x, _ in pts], [y + dy for _, y in pts]
    return new, [max(0, min(xs)), max(0, min(ys)), min(w - 1, max(xs)), min(h - 1, max(ys))]


def dress(num, name, preview=False, spec=None, report=None):
    """Dress overworld model num. spec: its npc_drip.json entry (read from the file when None). report (a dict)
    gets, per facing direction, the pieces drawn, their boxes on that direction's first frame and its frames."""
    for ext in ("NSBTX", "NSBMD"):
        rel = f"files/data/mmodel/mmodel/mmodel_{num:08d}.{ext}"
        r = subprocess.run(["git", "show", f"77565981b:{rel}"], cwd=ROOT, capture_output=True)
        if r.returncode == 0:
            blob = r.stdout
            break
    else:
        return None
    if spec is None:
        spec = load_drip().get(name, {})
    b, texs, pals = nsbtx.parse(blob)
    texs = [t for t in texs if t["fmt"] == 3]
    if not texs or not pals:
        return None
    pal = nsbtx.get_palette(b, pals[0])
    frames = [nsbtx.get_pixels(b, t) for t in texs]
    used = {v for f in frames for r in f for v in r} - {0}
    if len(used) < 4:
        return None
    orig_pal = list(pal)
    rng = random.Random(num * 31337)
    S = {"out": min(used, key=lambda i: sum(pal[i]))}
    for k, col in (("m", (120, 120, 128)), ("l", (200, 200, 210)), ("W", (248, 248, 248)),
                   ("g", (246, 206, 64)), ("b", (176, 120, 36))):
        S[k] = nearest(pal, used, col)
    free = [i for i in range(1, 16) if i not in used]
    def claim(key, col):
        if free:
            i = free.pop(0)
            pal[i] = col
            S[key] = i
    if ms.dist(pal[S["g"]], (246, 206, 64)) > 1500 or (PLAYER.search(name) and not FRIEND.search(name)):
        claim("g", (255, 224, 72))
    S["ac"] = S["out"]
    S["k"] = S["out"]

    style, color, gun = rng.choice(["beanie", "snapback", "durag", "bandana"]), "k", None
    if PLAYER.search(name) and not FRIEND.search(name):
        style, color, gun = "none", "k", None     # keeps his own cap; just a chain, no gun
    elif name == MOM:                             # satin bonnet: she's not leaving the house today
        style = "bonnet"
        claim("p", (236, 120, 176))
        claim("pl", (255, 196, 224))
        if "p" not in S:                          # no spare palette slots: her closest pink/red
            S["p"] = nearest(pal, used - {S["out"]}, (236, 120, 176))
        color = "p"
    elif FRIEND.search(name):
        style = "bandana"
        claim("r", (214, 36, 44))
        color = "r" if "r" in S else "k"
    elif ARMED.search(name):
        gun = rng.choice(["pistol", "mid", "long"])
    if style == "bandana" and not FRIEND.search(name):      # a black band disappears into dark hair: rep a colour
        want = rng.choice([(214, 36, 44), (40, 80, 200)])
        key = "r" if want == (214, 36, 44) else "u"
        claim(key, want)
        if key not in S:
            S[key] = nearest(pal, used - {S["out"]}, want)
        color = key
    if name in (OAK, ELM):
        style = None
    if style in ("snapback", "beanie") and rng.random() < .5 and S["W"] != S["out"]:
        color = "W"
    for d in FACING:                              # colours the hand-placed pieces need
        for item in spec.get(d, []):
            c = item.get("color")
            if c and c not in S and c in PIECE_COLORS:
                claim(c, PIECE_COLORS[c])
                if c not in S:
                    S[c] = nearest(pal, used - {S["out"]}, PIECE_COLORS[c])

    skin = nearest(pal, used, SKIN)
    if name == OAK:      # lab coat -> bare skin, purple shirt -> wife beater, slacks -> bare legs
        for i, col in ((9, (248, 208, 184)), (12, (216, 160, 120)), (10, (184, 128, 100)), (11, (120, 80, 64)),
                       (13, (232, 232, 248)), (14, (200, 200, 216))):
            pal[i] = col
    if name == ELM:      # coat that hasn't been washed since the experiments started
        pal[9], pal[10] = (222, 214, 160), (176, 168, 120)

    dirs = frame_dirs(texs)
    face = face_metrics(frames, dirs, pal, used, S)

    def auto(d):
        items = []
        if gun:
            items.append({"type": "gun", "kind": gun})
        if style and face and d == "down":                      # before the hat: a pom-pom moves the top
            items.append({"type": "chain", "heavy": bool(PLAYER.search(name) and not FRIEND.search(name))})
        if style == "bonnet" and face:
            items.append({"type": "bonnet", "color": color})
        elif style and style != "none" and face:
            items.append({"type": "hat", "style": style, "color": color})
        if name in (OAK, ELM) and d == "down":
            items.append({"type": "powder"})
        return items
    pieces = {d: spec[d] if spec.get("auto_" + d) is False else auto(d) for d in FACING}

    def draw(rows, d, item):
        t, c = item["type"], item.get("color", "k")
        if t == "gun":
            return mo.dress_frame(rows, d, S, "none", color, item.get("kind", "pistol"), big=False, chain=False)
        if t == "chain" and face:
            return collar_chain(rows, S, face, heavy=bool(item.get("heavy")), color=item.get("color", "g"))
        if t == "bonnet" and face:
            return bonnet(rows, dict(S, p=S.get(c, S["out"]), pl=S["pl"] if c == "p" and "pl" in S else S["W"]),
                          face)
        if t == "hat" and face:
            return fitted_hat(rows, d, S, item.get("style", "beanie"), c if c in S else "k", face)
        if t == "powder":
            p = powder(rows, skin)
            out = [r[:] for r in rows]
            if p:
                for dx in (0, 1):
                    if 0 <= p[0] + dx < len(rows[0]):
                        out[p[1]][p[0] + dx] = S["W"]
            return out
        return rows

    order = sorted(range(len(texs)), key=lambda i: int(re.sub(r"\D", "", texs[i]["name"].rsplit(".", 1)[-1]) or 0))
    first = {}
    for i in order:
        first.setdefault(dirs[i], i)
    out_rows = []
    for i, (t, rows, d) in enumerate(zip(texs, frames, dirs)):
        boxes = []
        for item in pieces[d]:
            rows, box = layer(rows, draw(rows, d, item), item.get("dx", 0), item.get("dy", 0), item.get("scale", 1))
            boxes.append(box)
        if report is not None and first.get(d) == i:
            report[d] = {"items": json.loads(json.dumps(pieces[d])), "boxes": boxes, "hand": None, "scale": None,
                         "gun_box": None}
        nsbtx.set_pixels(b, t, rows)
        out_rows.append(rows)
    nsbtx.set_palette(b, pals[0], pal)
    if report is not None:
        for d in report:
            idx = [i for i in order if dirs[i] == d]
            report[d].update(frames=[out_rows[i] for i in idx], orig=[frames[i] for i in idx])
        report["_pal"], report["_orig_pal"] = pal, orig_pal
    if preview:
        return out_rows, pal, dirs
    (ROOT / rel).write_bytes(bytes(b))
    return True


SKIN = (248, 208, 184)


def face_metrics(frames, dirs, pal, used, S):
    """(forehead, chin) as rows below the sprite's top, from the first camera-facing frame: the skin colour is
    the skin-ish palette entry with the most pixels in the middle of the head."""
    down = [f for f, d in zip(frames, dirs) if d == "down"]
    if not down:
        return None
    rows = down[0]
    bb = mo.bbox(rows)
    if not bb:
        return None
    l, t, r, b = bb
    cx, H = (l + r) // 2, b - t + 1
    cands = [i for i in used if i != S["out"] and pal[i][0] > 120 and pal[i][0] >= pal[i][1] >= pal[i][2]
             and pal[i][0] - pal[i][2] > 25]
    def score(i):
        return sum(1 for y in range(t + H * 3 // 10, t + H * 6 // 10) for x in range(cx - 4, cx + 5)
                   if 0 <= x < len(rows[0]) and rows[y][x] == i)
    if not cands:
        return None
    exact = min(cands, key=lambda i: ms.dist(pal[i], SKIN))
    skin = exact if ms.dist(pal[exact], SKIN) < 1200 and score(exact) >= 4 else max(cands, key=score)
    if score(skin) < 4:
        return None
    ys = [y for y in range(t, t + H * 7 // 10) for x in range(cx - 4, cx + 5)
          if 0 <= x < len(rows[0]) and rows[y][x] == skin]
    return min(ys) - t, max(ys) - t


def fitted_hat(rows, d, S, style, color, face):
    """An overlaid hat: its own shape a pixel bigger than the head all round (plus a rounded cap row on top),
    fully outlined and shaded, covering the hair down to just above the forehead - then the style's details:
    a ribbed cuff + pom-pom (beanie), a backwards brim (snapback), tails (durag), a band + knot (bandana)."""
    bb = mo.bbox(rows)
    if not bb:
        return rows
    l, t, r, b = bb
    out = [row[:] for row in rows]
    w, h = len(rows[0]), len(rows)
    main = S["out"] if color == "k" else S[color]
    shine = {"k": S["m"], "W": S["l"], "p": S.get("pl", S["l"]), "r": S["l"]}.get(color, S["l"])
    bottom = t + face[0] - 1                                    # down to just above the forehead
    top = t if style != "bandana" else max(t, bottom - 2)

    def put(x, y, c):
        if 0 <= x < w and 0 <= y < h:
            out[y][x] = c
    spans = {}
    for y in range(top, bottom + 1):
        xs = [x for x in range(w) if rows[y][x]]
        if xs:
            spans[y] = (min(xs) - 1, max(xs) + 1)              # a pixel bigger than the head
    if not spans:
        return rows
    if style != "bandana":                                     # rounded top, one row above the head
        a0, z0 = spans[min(spans)]
        for x in range(a0 + 2, z0 - 1):
            put(x, top - 1, S["out"])
    for y, (a, z) in spans.items():
        for x in range(a, z + 1):
            if x in (a, z) or (style == "bandana" and y in (top, bottom)):
                put(x, y, S["out"])
            elif y == top and style != "bandana" and x in (a + 1, z - 1):
                put(x, y, S["out"])
            elif style == "beanie" and y >= bottom - 1:
                put(x, y, shine if x % 2 else main)            # ribbed cuff
            else:
                put(x, y, shine if (x - a in (2, 3) and y - top in (1, 2)) else main)
    a, z = spans[bottom]
    cx = (a + z) // 2
    back = {"left": 1, "right": -1}.get(d, 0)                  # which side the back of the head is on
    if style == "beanie":                                      # pom-pom
        for dx in (-1, 0, 1):
            put(cx + dx, top - 2, main if dx else shine)
        put(cx, top - 3, S["out"])
        put(cx - 2, top - 2, S["out"])
        put(cx + 2, top - 2, S["out"])
    elif style == "snapback":
        if back:                                               # brim sticking out the back
            bx = z if back > 0 else a
            for k in range(1, 4):
                put(bx + back * k, bottom - 1, main)
                put(bx + back * k, bottom - 2, S["out"])
                put(bx + back * k, bottom, S["out"])
        elif d == "up":
            for x in range(cx - 1, cx + 2):
                put(x, bottom - 1, S["W"])                     # the strap
    elif style == "durag":
        if d == "up" or back:                                  # tails down the back
            tx = cx if d == "up" else (z if back > 0 else a)
            for k in range(1, 6):
                x = tx + (back * (k // 3) if back else 0)
                put(x, bottom + k, main)
                put(x + 1, bottom + k, main if k < 5 else shine)
                put(x - 1, bottom + k, S["out"])
                put(x + 2, bottom + k, S["out"])
    elif style == "bandana":
        if back:                                               # knot + ends at the back
            kx = z + 1 if back > 0 else a - 1
            for k in range(3):
                put(kx + back * k, bottom - 1, main)
                put(kx + back * k, bottom - 1 + k // 2 + 1, main)
        for x in range(a + 2, z - 1, 3):
            put(x, bottom - 1, S["W"])                         # paisley dots
    return out


def collar_chain(rows, S, face, heavy=False, color="g"):
    """A gold chain hanging on the collar, just under the chin, with a pendant. heavy: a thick 2-row Cuban
    link with a 2x2 piece (the player's - it has to read at 32px over a busy jacket)."""
    bb = mo.bbox(rows)
    if not bb:
        return rows
    l, t, r, b = bb
    out = [row[:] for row in rows]
    y0 = t + face[1] + 1
    if y0 + 5 >= len(rows):
        return rows
    xs = [x for x in range(len(rows[0])) if rows[y0][x]]
    if not xs:
        return rows
    cx = (min(xs) + max(xs)) // 2

    def put(x, y, c):
        if 0 <= y < len(rows) and 0 <= x < len(rows[0]) and rows[y][x]:
            out[y][x] = c
    if color != "g":                                            # silver / iced / coloured: (main, shade)
        main, shade = {"l": ("l", "m"), "W": ("W", "l"), "k": ("m", "out")}.get(color, (color, "out"))
        S = dict(S, g=S.get(main, S["g"]), b=S.get(shade, S["b"]))
    if heavy:
        for dx, dy in zip(range(-4, 5), (0, 1, 1, 2, 2, 2, 1, 1, 0)):
            put(cx + dx, y0 + dy, S["g"])
            put(cx + dx, y0 + dy + 1, S["b"])
        for dx in (0, 1):
            for dy in (3, 4):
                put(cx + dx, y0 + dy, S["g"])
        put(cx, y0 + 3, S["W"])                                 # shine on the piece
        put(cx, y0 + 5, S["b"])
        put(cx + 1, y0 + 5, S["b"])
        return out
    for i, (dx, dy) in enumerate(((-3, 0), (-2, 1), (-1, 1), (0, 2), (1, 1), (2, 1), (3, 0))):
        put(cx + dx, y0 + dy, S["g"] if i % 2 == 0 else S["b"])
    put(cx, y0 + 3, S["g"])                                    # pendant
    return out


def bonnet(rows, S, face):
    """Mom's satin bonnet: its own puffy shape over the crown - a pixel bigger than her head all round, outlined,
    with a shine and a lighter elastic band - leaving her hair showing underneath."""
    bb = mo.bbox(rows)
    if not bb:
        return rows
    l, t, r, b = bb
    out = [row[:] for row in rows]
    w, h = len(rows[0]), len(rows)
    main, light = S["p"], S.get("pl", S["W"])
    bottom = t + max(3, face[0] - 3)

    def put(x, y, c):
        if 0 <= x < w and 0 <= y < h:
            out[y][x] = c
    spans = {}
    for y in range(t, bottom + 1):
        xs = [x for x in range(w) if rows[y][x]]
        if xs:
            spans[y] = (min(xs) - 1, max(xs) + 1)              # bulge past the head
    if not spans:
        return rows
    a0, z0 = spans[t]
    for x in range(a0 + 2, z0 - 1):
        put(x, t - 1, S["out"])                                # top edge, one row above the head
    for y, (a, z) in spans.items():
        for x in range(a, z + 1):
            if x in (a, z):
                put(x, y, S["out"])
            elif y == bottom:
                put(x, y, light if x % 2 else main)            # elastic band
            elif y == t and x in (a + 1, z - 1):
                put(x, y, S["out"])                            # rounded top corners
            else:
                put(x, y, light if (x - a in (2, 3) and y - t in (1, 2)) else main)
    return out


def main():
    preview = sys.argv[sys.argv.index("--preview") + 1] if "--preview" in sys.argv else None
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    todo = {n: nm for n, nm in models().items() if not only or nm in only}
    if preview:
        rows = []
        for n, nm in todo.items():
            r = dress(n, nm, preview=True)
            if r:
                rows.append((nm, r))
        sheet = Image.new("RGBA", (16 * 34 + 90, len(rows) * 36), (200, 230, 200, 255))
        dr = ImageDraw.Draw(sheet)
        for k, (nm, (frames, pal, dirs)) in enumerate(rows):
            dr.text((2, k * 36 + 10), nm[:12], fill=(0, 0, 0, 255))
            for j, fr in enumerate(frames[:16]):
                im = Image.new("RGBA", (len(fr[0]), len(fr)))
                im.putdata([(*pal[v], 0 if v == 0 else 255) for r in fr for v in r])
                sheet.alpha_composite(im, (90 + j * 34, k * 36))
        sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST).save(preview)
        print("preview:", preview)
        return
    drip = load_drip()
    n = sum(1 for k, nm in todo.items() if dress(k, nm, spec=drip.get(nm, {})))
    print(f"dressed {n} overworld people")


if __name__ == "__main__":
    main()
