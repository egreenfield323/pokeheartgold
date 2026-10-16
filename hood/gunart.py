"""Pixel-art guns for Hood HeartGold, drawn parametrically so they can be any size.

Every function draws a gun pointing RIGHT onto an ImageDraw canvas using the local
palette slots below and returns ((grip_x, grip_y), (muzzle_x, muzzle_y)).
make_sprites.py maps these local slots onto each Pokémon's own palette.
"""
from PIL import Image, ImageDraw

T, OUT, SK_D, SK, SK_L, AC_D, AC, AC_L, WD_D, WD, GOLD, GOLD_D, WHITE, FLASH = range(14)


def _guard(d, x, y, s):
    d.rectangle([x, y, x + s, y + max(2, s * 2 // 3)], outline=SK_D)


def pistol(d, L, H, x=4, y=12, mag=0, light=False, compact=False, gold=False):
    body = GOLD if gold else SK
    d.rectangle([x, y, x + L, y + H], fill=body)                           # slide
    d.line([x + 1, y + 1, x + L - 1, y + 1], fill=SK_L if not gold else WHITE)
    for i in range(min(3, H // 3)):                                         # serrations
        d.line([x + 2 + i * 2, y + 2, x + 2 + i * 2, y + H - 1], fill=SK_D)
    fh = max(2, H // 3)
    d.rectangle([x + 1, y + H, x + L - 2, y + H + fh], fill=SK_D)           # frame
    gw = max(4, H)
    gh = H * 2 if not compact else H * 3 // 2
    g0 = x + 1
    d.polygon([(g0, y + H), (g0 + gw, y + H), (g0 + gw - 2, y + H + gh), (g0 - 3, y + H + gh)], fill=AC)
    d.line([g0 + 1, y + H + 2, g0 - 1, y + H + gh - 1], fill=AC_L)
    _guard(d, g0 + gw, y + H + fh, max(3, H // 2))
    if mag:
        d.rectangle([g0 - 3, y + H + gh, g0 + gw - 3, y + H + gh + mag], fill=SK_D)
        d.line([g0 - 2, y + H + gh + 1, g0 - 2, y + H + gh + mag - 1], fill=SK)
    if light:
        lw = max(5, L // 4)
        d.rectangle([x + L - lw - 1, y + H + fh, x + L - 1, y + H + fh + max(3, H // 2)], fill=SK_D)
        d.rectangle([x + L - 1, y + H + fh + 1, x + L, y + H + fh + max(2, H // 2) - 1], fill=WHITE)
    return (g0 + gw // 2 - 1, y + H + 2), (x + L, y + H // 2)


def revolver(d, L, H, x=8, y=12, barrel=0.5, gold=False):
    cw = H + 3
    bl = max(4, round(L * barrel))
    cx = x + 3
    d.rectangle([cx, y, cx + cw, y + H + 2], fill=SK)                      # cylinder
    for i in range(1, 3):
        d.line([cx + i * cw // 3, y + 1, cx + i * cw // 3, y + H + 1], fill=SK_D)
    bh = max(2, H // 2)
    d.rectangle([cx + cw, y + 1, cx + cw + bl, y + bh], fill=SK_L)         # barrel
    d.rectangle([cx + cw, y + bh + 1, cx + cw + bl - 2, y + bh + 2], fill=SK_D)  # ejector rod
    d.rectangle([cx + cw + bl - 2, y - 2, cx + cw + bl, y], fill=SK)       # front sight
    d.polygon([(cx - 3, y), (cx, y - 3), (cx + 2, y)], fill=SK_D)           # hammer
    d.rectangle([x, y + H + 2, cx + cw - 1, y + H + 4], fill=SK_D)
    d.polygon([(x - 1, y + 2), (cx, y + 2), (cx + 2, y + H + 3), (cx - 1, y + H * 2 + 5),
               (x - 6, y + H * 2 + 5), (x - 3, y + H + 3)], fill=WD)        # wood grip
    d.line([x - 1, y + H + 5, x - 3, y + H * 2 + 3], fill=AC)
    if gold:
        d.line([cx, y + H + 2, cx + cw, y + H + 2], fill=GOLD)
        d.line([cx + cw, y + 1, cx + cw + bl, y + 1], fill=GOLD)
    _guard(d, cx + cw - 3, y + H + 4, max(3, H // 2))
    return (x - 1, y + H + 3), (cx + cw + bl, y + bh // 2 + 1)


def rifle(d, L, H, kind, x=4, y=14):
    wood = kind in ("draco", "ak", "drum_ak")
    rec_l = L * 2 // 5 if kind != "draco" else L // 2
    rx = x + (L // 4 if kind != "draco" else 4)
    d.rectangle([rx, y, rx + rec_l, y + H], fill=SK)                        # receiver
    d.line([rx + 1, y + 1, rx + rec_l - 1, y + 1], fill=SK_L)
    hg = max(4, L // 5)
    hx = rx + rec_l
    d.rectangle([hx, y + 1, hx + hg, y + H - 1], fill=WD if wood else SK_D)  # handguard
    bar_y = y + H // 3
    d.rectangle([hx + hg, bar_y, x + L, bar_y + max(1, H // 4)], fill=SK_D)  # barrel
    d.rectangle([x + L - 2, bar_y - 1, x + L, bar_y + max(2, H // 4) + 1], fill=SK)
    d.rectangle([x + L - 7, y - 3, x + L - 6, y], fill=SK_D)                # front sight
    mx = rx + rec_l * 3 // 5
    mh = max(8, H * 3 // 2)
    if kind == "drum_ak":
        r = max(5, H)
        d.ellipse([mx - r // 2, y + H - 2, mx + r * 3 // 2, y + H + r * 2 - 2], fill=AC)
        d.ellipse([mx + r // 4, y + H + r // 2, mx + r * 3 // 4, y + H + r], fill=AC_D)
    elif wood:
        d.polygon([(mx, y + H), (mx + 6, y + H), (mx + 10, y + H + mh), (mx + 4, y + H + mh + 2)], fill=AC)
        d.line([mx + 2, y + H + 2, mx + 5, y + H + mh - 1], fill=AC_L)
    elif kind in ("ar", "bump", "m4"):
        d.polygon([(mx, y + H), (mx + 6, y + H), (mx + 7, y + H + mh), (mx + 1, y + H + mh)], fill=SK_D)
    elif kind == "lmg":
        d.rectangle([mx - 4, y + H, mx + 8, y + H + mh], fill=AC)          # box mag
        d.line([mx - 3, y + H + 2, mx + 7, y + H + 2], fill=AC_L)
        d.line([hx + hg, y + H, hx + hg - 4, y + H + mh], fill=SK_D)        # bipod
        d.line([hx + hg + 2, y + H, hx + hg + 6, y + H + mh], fill=SK_D)
    elif kind == "sniper":
        d.polygon([(mx, y + H), (mx + 5, y + H), (mx + 5, y + H + mh // 2), (mx, y + H + mh // 2)], fill=SK_D)
        d.rectangle([rx + 2, y - 6, rx + rec_l + 4, y - 2], fill=OUT)        # scope
        d.rectangle([rx + rec_l + 2, y - 7, rx + rec_l + 5, y - 1], fill=SK_D)
        d.point((rx + rec_l + 4, y - 5), fill=AC_L)
        d.line([rx + rec_l // 2, y - 2, rx + rec_l // 2, y], fill=SK_D)
    gx = mx - 8
    d.polygon([(gx, y + H), (gx + 5, y + H), (gx + 3, y + H + H + 2), (gx - 2, y + H + H + 2)],
              fill=WD if wood else SK_D)                                    # pistol grip
    _guard(d, gx + 5, y + H, max(3, H // 2))
    if kind in ("ak", "drum_ak", "sniper"):
        d.polygon([(rx, y + 1), (rx, y + H), (x, y + H + 5), (x, y + 2)], fill=WD if kind != "sniper" else AC)
        d.line([x + 2, y + 3, rx - 2, y + 2], fill=WD_D)
    elif kind in ("ar", "lmg"):
        d.rectangle([x + 4, y + 2, rx, y + 4], fill=SK_D)
        d.polygon([(x, y), (x + 8, y), (x + 8, y + H + 3), (x, y + H + 5)], fill=SK_D)
    elif kind == "bump":
        d.polygon([(x - 2, y - 1), (rx + 2, y - 1), (gx + 8, y + H * 2 + 2), (gx - 5, y + H * 2 + 2),
                   (rx - 4, y + H + 1), (x - 2, y + H + 6)], fill=AC_D)     # chunky bump stock
        d.line([x, y + 1, rx, y + 1], fill=AC)
    elif kind == "m4":
        d.rectangle([x + 4, y + 2, rx, y + 4], fill=SK_D)
        d.polygon([(x, y), (x + 9, y), (x + 9, y + H + 2), (x, y + H + 4)], fill=AC)
        d.rectangle([rx + 3, y - 6, rx + rec_l - 2, y - 1], fill=OUT)         # optic
        d.rectangle([rx + rec_l - 3, y - 5, rx + rec_l - 1, y - 2], fill=AC_L)
        d.rectangle([hx + 3, y + H, hx + 5, y + H + 6], fill=OUT)             # foregrip
    if kind in ("ar", "bump"):
        d.rectangle([rx + 3, y - 4, rx + rec_l - 3, y - 1], fill=SK_D)        # carry handle
    return (gx + 2, y + H + 2), (x + L, bar_y)


def shotgun(d, L, H, kind, x=4, y=14):
    bh = max(2, H // 2)
    if kind == "sawedoff":
        d.rectangle([x + L // 3, y, x + L, y + bh], fill=SK_L)               # twin barrels
        d.rectangle([x + L // 3, y + bh + 1, x + L, y + bh * 2], fill=SK)
        d.rectangle([x + L // 4, y - 1, x + L // 3 + 3, y + bh * 2 + 1], fill=SK_D)
        d.polygon([(x + L // 4, y + 1), (x + L // 4, y + bh * 2 + 1), (x, y + bh * 2 + H), (x - 2, y + bh * 2 + H - 3)], fill=WD)
        gp = (x + L // 4 - 2, y + bh * 2 + 2)
    else:
        rx = x + L // 3
        d.rectangle([rx, y, rx + L // 5, y + H], fill=SK)                     # receiver
        d.rectangle([rx + L // 5, y, x + L, y + bh], fill=SK_L)               # barrel
        d.rectangle([rx + L // 5 + 2, y + bh + 1, x + L - 4, y + bh + 2], fill=SK_D)  # mag tube
        d.rectangle([rx + L // 5 + 4, y + bh + 1, rx + L // 5 + L // 4, y + H], fill=WD if kind == "pump" else OUT)
        d.polygon([(rx, y + 1), (rx, y + H), (x, y + H + 4), (x, y + 2)], fill=WD if kind == "pump" else AC)
        if kind == "auto":
            r = max(4, H)
            d.ellipse([rx + 2, y + H - 1, rx + 2 + r * 2, y + H - 1 + r * 2], fill=AC)
            d.ellipse([rx + r // 2 + 2, y + H + r // 2, rx + r * 3 // 2 + 2, y + H + r * 3 // 2], fill=AC_D)
        _guard(d, rx + 1, y + H, max(3, H // 2))
        gp = (rx - 1, y + H)
    return gp, (x + L, y + bh // 2 + 1)


def smg(d, L, H, kind, x=4, y=14):
    d.rectangle([x + 4, y, x + L, y + H], fill=SK)
    d.line([x + 5, y + 1, x + L - 1, y + 1], fill=SK_L)
    d.rectangle([x + L, y + H // 3, x + L + 3, y + H // 3 + 1], fill=SK_D)
    gx = x + L // 2 - 2
    mag = max(10, H * 2) + (6 if kind == "mac10" else 0)
    d.rectangle([gx, y + H, gx + 4, y + H + mag], fill=SK_D)                  # mag through grip
    d.line([gx + 1, y + H + 2, gx + 1, y + H + mag - 1], fill=SK)
    _guard(d, gx + 4, y + H, max(3, H // 2))
    if kind == "uzi":
        d.rectangle([x, y + 1, x + 4, y + 3], fill=SK_D)                      # folded stock
    else:
        d.rectangle([x + L - 6, y + H, x + L - 2, y + H + 3], fill=OUT)        # strap loop
        d.rectangle([x, y + 2, x + 4, y + H - 1], fill=AC)
    return (gx + 2, y + H + 3), (x + L + 3, y + H // 3)


def minigun(d, L, H, x=4, y=12):
    for i in range(4):
        d.rectangle([x + L // 3, y + i * 2, x + L, y + i * 2], fill=SK_L if i % 2 else SK)
    d.rectangle([x, y - 2, x + L // 3, y + 8], fill=SK_D)                    # motor housing
    d.rectangle([x + 2, y - 1, x + L // 3 - 2, y + 2], fill=AC)
    d.rectangle([x + L // 3 - 1, y - 1, x + L // 3 + 1, y + 8], fill=SK)
    d.rectangle([x + 4, y + 9, x + 12, y + 14], fill=GOLD)                   # ammo belt
    for i in range(x + 4, x + 13, 2):
        d.point((i, y + 10), fill=GOLD_D)
    d.rectangle([x + L // 4, y - 6, x + L // 4 + 2, y - 2], fill=SK_D)       # carry handle
    return (x + L // 4, y + 8), (x + L, y + 3)


def rpg(d, L, H, x=4, y=14):
    th = max(3, H // 2)
    d.rectangle([x, y, x + L - 10, y + th], fill=AC)                          # launch tube
    d.line([x, y, x + L - 10, y], fill=AC_L)
    d.polygon([(x + L - 10, y - 3), (x + L - 4, y - 3), (x + L + 2, y + th // 2),
               (x + L - 4, y + th + 3), (x + L - 10, y + th + 3)], fill=WD)  # warhead
    d.line([x + L - 9, y - 2, x + L - 4, y - 2], fill=GOLD)
    d.rectangle([x + L // 3, y + th + 1, x + L // 3 + 2, y + th + 6], fill=SK_D)
    d.rectangle([x + L // 2, y + th + 1, x + L // 2 + 2, y + th + 6], fill=SK_D)
    d.rectangle([x + L // 2 - 2, y - 4, x + L // 2 + 4, y - 1], fill=OUT)      # sight
    return (x + L // 3 + 1, y + th + 3), (x + L + 2, y + th // 2)


def launcher(d, L, H, x=4, y=14):
    d.rectangle([x + L // 3, y, x + L, y + H], fill=SK)                       # fat barrel
    d.line([x + L // 3, y + 1, x + L, y + 1], fill=SK_L)
    r = max(5, H)
    d.ellipse([x + L // 4 - 2, y - 2, x + L // 4 + r * 2, y + r * 2], fill=SK_D)  # drum
    d.ellipse([x + L // 4 + r // 2, y + r // 2, x + L // 4 + r, y + r], fill=SK)
    d.polygon([(x + L // 4, y + 2), (x + L // 4, y + H), (x, y + H + 4), (x, y + 2)], fill=AC)
    _guard(d, x + L // 3 + r, y + H, max(3, H // 2))
    return (x + L // 3 + r - 1, y + H + 1), (x + L, y + H // 2)


# name: (draw function, full-size length, full-size height)
GUNS = {
    "rev22":       (lambda d, L, H: revolver(d, L, H, barrel=0.3), 28, 8),
    "rev38":       (lambda d, L, H: revolver(d, L, H, barrel=0.45), 38, 9),
    "magnum":      (lambda d, L, H: revolver(d, L, H, barrel=0.62, gold=True), 52, 10),
    "beretta":     (lambda d, L, H: pistol(d, L, H, compact=True), 28, 8),
    "extendo":     (lambda d, L, H: pistol(d, L, H, mag=H + 5), 36, 9),
    "draco":       (lambda d, L, H: rifle(d, L, H, "draco"), 50, 8),
    "glock":       (lambda d, L, H: pistol(d, L, H, compact=True), 28, 9),
    "glock_light": (lambda d, L, H: pistol(d, L, H, light=True), 38, 10),
    "drum_ak":     (lambda d, L, H: rifle(d, L, H, "drum_ak"), 64, 9),
    "ar15":        (lambda d, L, H: rifle(d, L, H, "ar"), 56, 8),
    "ar_bump":     (lambda d, L, H: rifle(d, L, H, "bump"), 60, 8),
    "m4":          (lambda d, L, H: rifle(d, L, H, "m4"), 64, 8),
    "sawedoff":    (lambda d, L, H: shotgun(d, L, H, "sawedoff"), 32, 8),
    "pump":        (lambda d, L, H: shotgun(d, L, H, "pump"), 54, 8),
    "auto_shotgun": (lambda d, L, H: shotgun(d, L, H, "auto"), 60, 9),
    "uzi":         (lambda d, L, H: smg(d, L, H, "uzi"), 24, 8),
    "mac10":       (lambda d, L, H: smg(d, L, H, "mac10"), 28, 8),
    "lmg":         (lambda d, L, H: rifle(d, L, H, "lmg"), 66, 9),
    "ak":          (lambda d, L, H: rifle(d, L, H, "ak"), 60, 8),
    "sniper":      (lambda d, L, H: rifle(d, L, H, "sniper"), 72, 7),
    "launcher":    (lambda d, L, H: launcher(d, L, H), 50, 10),
    "minigun":     (lambda d, L, H: minigun(d, L, H), 62, 10),
    "rpg":         (lambda d, L, H: rpg(d, L, H), 66, 10),
}


def render(name, scale):
    """Draw gun `name` at `scale` of full size. Returns (image, grip, muzzle), pointing right."""
    fn, L0, H0 = GUNS[name]
    L, H = max(14, round(L0 * scale)), max(5, round(H0 * scale))
    img = Image.new("P", (L + 40, H * 4 + 40), T)
    d = ImageDraw.Draw(img)
    grip, muzzle = fn(d, L, H)
    # 1px outline
    px = img.load()
    w, h = img.size
    edge = [(x, y) for y in range(h) for x in range(w) if px[x, y] == T and any(
        0 <= x + dx < w and 0 <= y + dy < h and px[x + dx, y + dy] not in (T, OUT)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for x, y in edge:
        px[x, y] = OUT
    return img, grip, muzzle
