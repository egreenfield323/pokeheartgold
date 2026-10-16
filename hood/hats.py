"""Overlay headwear for Hood HeartGold: new pixel art drawn on top of a sprite, not recoloured pixels.

hat(style, w, side) returns {(dx, dy): role} relative to the hat's bottom-centre (dy <= 0 is up).
Roles: "c" main colour, "s" shine, "o" outline, "W" white detail, "g" gold detail.
side = +1 / -1 is the back of the head (where brims, knots and tails go); 0 = seen from behind.
"""
import math


def _dome(w, h):
    pts = set()
    half = w / 2
    for dy in range(h):
        hw = half * math.sqrt(max(0.0, 1 - (dy / h) ** 2)) if dy else half
        for dx in range(-math.floor(hw), math.ceil(hw)):
            pts.add((dx, -dy))
    return pts


def _outline(px):
    out = dict(px)
    for (x, y) in px:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
            if (x + dx, y + dy) not in px:
                out.setdefault((x + dx, y + dy), "o")
    return out


def hat(style, w, side=1):
    if style == "none":          # chain-only looks (e.g. the player keeps his own cap)
        return {}
    w = max(6, min(28, w))
    px = {}
    if style == "snapback":
        h = max(4, round(w * .42))
        for p in _dome(w, h):
            px[p] = "c"
        for dy in range(-h + 1, 1):                         # front panel seam
            px[(0, dy)] = "s" if dy % 2 else "c"
        px[(0, -h)] = "s"                                   # button
        if side:
            bl = max(4, w // 3)
            for i in range(bl):                              # backwards brim
                x = side * (w // 2 + i)
                px[(x, 0)] = "c"
                px[(x, -1)] = "c" if i < bl - 1 else px.get((x, -1), "c")
            px[(side * (w // 2 - 2), -2)] = "W"            # sticker
        else:
            for dx in range(-2, 3):                          # snap strap from behind
                px[(dx, -1)] = "W" if abs(dx) < 2 else "o"
    elif style == "beanie":
        h = max(5, round(w * .5))
        for p in _dome(w, h):
            px[p] = "c"
        for dx in range(-w // 2, w // 2 + 1):                # ribbed cuff
            for dy in (0, -1, -2):
                px[(dx, dy)] = "s" if dx % 2 else "c"
            px[(dx, -3)] = "o"
        for dx in range(-1, 2):                              # pom-pom
            for dy in range(-h - 2, -h + 1):
                px[(dx, dy)] = "c" if (dx, dy) != (0, -h - 1) else "s"
    elif style == "durag":
        h = max(4, round(w * .4))
        for p in _dome(w, h):
            px[p] = "c"
        for i in range(-w // 2 + 2, w // 4):                 # silky shine
            px[(i, -h + 2 + (i % 3 == 0))] = "s"
        for dx in range(-w // 2, w // 2 + 1):                # tight band at the brow
            px[(dx, 0)] = "c"
        tx = side * (w // 2 - 1) if side else 0
        tl = max(6, round(w * .5))
        for k in range(tl):                                  # tails
            for t in (0, 1):
                px[(tx + side * (k // 3) + t * (1 if side >= 0 else -1), 1 + k)] = "c" if k < tl - 1 else "s"
            if side == 0:
                px[(tx + 2, 1 + k)] = "c"
        px[(tx, 0)] = "s"                                    # knot
    else:  # bandana
        for dx in range(-w // 2, w // 2 + 1):
            for dy in (0, -1, -2):
                px[(dx, dy)] = "c"
            if dx % 3 == 0:
                px[(dx, -1)] = "W"
        if side:
            kx = side * (w // 2 + 1)
            for dx in range(3):
                for dy in range(-3, 1):
                    px[(kx + side * dx, dy)] = "c"
            px[(kx + side, -1)] = "s"
            for k in range(4):                               # knot tails
                px[(kx + side * (2 + k // 2), 1 + k)] = "c"
    return _outline(px)
