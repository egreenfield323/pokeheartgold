#!/usr/bin/env python3
"""Drip for the party / PC box / Pokéwalker-upload icons (files/poketool/icongra/poke_icon/*.png).

Icons are 32x64 (two 32x32 frames) drawn with one of three SHARED 16-colour palettes, so no new
colours can be added: drip uses entries every palette already has (greys, black, white) plus each
palette's own yellow as gold. Each icon gets the hat its species wears in battle, a mini gun of
its gun class, and a chain. Originals are read from the base commit 77565981b.
Run from the repo root:  python hood/make_icons.py [--preview out.png]
"""
import json
import random
import re
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_overworld as mo  # noqa: E402
import make_sprites as ms  # noqa: E402

ICONS = ms.ROOT / "files/poketool/icongra/poke_icon"
GOLD = {0: (5, 4), 1: (10, 9), 2: (9, 8)}          # per shared palette: (gold, dark gold)
FORM_ICONS = [(503, 506, 386), (507, 533, 201), (534, 535, 412), (536, 537, 413), (538, 538, 422),
              (539, 539, 423), (540, 540, 487), (541, 541, 492), (542, 546, 479), (547, 549, 351),
              (550, 550, 421)]


def icon_species(k):
    if 8 <= k <= 500:
        return k - 7
    for lo, hi, sp in FORM_ICONS:
        if lo <= k <= hi:
            return sp
    return None   # 7 = none, 501/502 = eggs


def palette_numbers():
    src = (ms.ROOT / "src/pokemon_icon_idx.c").read_text()
    body = src[src.index("sPokemonPalNoBySpeciesAndForm[]"):]
    body = body[body.index("{") + 1:body.index("}")]
    return [int(x) for x in re.findall(r"\d+", body)]


def shared_palettes():
    lines = (ICONS / "poke_icon_00000000.pal").read_text().split()[3:]
    cols = [tuple(int(v) for v in lines[i:i + 3]) for i in range(0, 48 * 3, 3)]
    return [cols[p * 16:(p + 1) * 16] for p in range(3)]


def icon_eyes(rows, pal):
    """Pupil detection from the battle sprites, run on the icon padded to 80x80."""
    canvas = Image.new("P", (80, 80))
    flat = Image.new("P", (32, 32))
    flat.putdata([v for r in rows for v in r])
    canvas.paste(flat, (0, 0))
    px = canvas.load()
    bb = ms.bbox(px, 0)
    return ms.find_pupils(px, pal, *bb) if bb else None


def main():
    plan, names = ms.gun_plan()
    drip = {k: v for k, v in json.loads(ms.DRIP.read_text(encoding="utf-8")).items() if not k.startswith("_")}
    palno = palette_numbers()
    pals = shared_palettes()
    preview = sys.argv[sys.argv.index("--preview") + 1] if "--preview" in sys.argv else None
    tiles, count = [], 0
    only = {int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")} if "--only" in sys.argv else None
    for path in sorted(ICONS.glob("poke_icon_*.png")):
        k = int(path.stem.split("_")[-1])
        sp = icon_species(k)
        if sp is None or (only and sp not in only):
            continue
        im = ms.git_png(path)
        pn = palno[k - 7] if k - 7 < len(palno) else 0
        pal = pals[pn]
        gun = drip.get(str(sp), {}).get("gun", plan[sp])
        # the same hat the species wears in battle (make_sprites.pick_hat decides it once per species)
        front = next((ms.git_png(ms.SPRITES / f"{sp:04d}" / g / "front.png") for g in ("male", "female")), None)
        if front is not None and front.getbbox():
            fpal = [tuple(front.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
            style, color = ms.pick_hat(front, fpal, random.Random(sp * 104729))
        else:
            style, color = "durag", "k"
        for item in drip.get(str(sp), {}).get("front", []):
            if item["type"] in ("hat", "fitcap"):          # (fitcap: placed in the drip editor)
                style, color = item["style"], item.get("color", color)
        data = im.tobytes()
        used = {v for v in data if v}
        ac = ms.accent_slots(pal, used - {15, 14, 1, 2, 3}) if used - {15, 14, 1, 2, 3} else (15, 15, 15)
        S = {"out": 15, "m": 1, "l": 2, "W": 3, "g": GOLD[pn][0], "b": GOLD[pn][1], "ac": ac[1],
             "r": min(range(1, 16), key=lambda i: ms.dist(pal[i], ms.COLORS["r"]))}
        frames = []
        for f in range(2):
            rows = [list(data[(f * 32 + y) * 32:(f * 32 + y + 1) * 32]) for y in range(32)]
            frames.append(mo.dress_frame(rows, "down", S, style, color, mo.MINI_CLASS.get(gun, "pistol"),
                                         big=False, eyes=icon_eyes(rows, pal)))
        out = Image.new("P", (32, 64))
        out.putdata([v for fr in frames for r in fr for v in r])
        out.putpalette(im.getpalette())
        out.info["transparency"] = 0
        count += 1
        if preview:
            show = out.copy()
            show.putpalette([v for c in pal for v in c])
            tiles.append(show.convert("RGBA"))
        else:
            out.save(path, transparency=0)
    if preview:
        cols = 24
        sheet = Image.new("RGBA", (cols * 34, ((len(tiles) + cols - 1) // cols) * 34), (220, 235, 220, 255))
        for i, t in enumerate(tiles):
            fr = t.crop((0, 0, 32, 32))
            sheet.alpha_composite(fr, ((i % cols) * 34, (i // cols) * 34))
        sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST).save(preview)
        print("preview:", preview)
    else:
        print(f"dressed {count} icons")


if __name__ == "__main__":
    main()
