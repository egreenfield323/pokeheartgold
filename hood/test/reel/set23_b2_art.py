

# ---- set 23, batch 2: Mall Ninja, M-80, Zip Tie, Onion Breath, Rage Quit ---------------------------------------

def ninja_headband(size=64):
    """A white karate headband (hachimaki) curved round an invisible head: a red rising sun on the front, the
    knot at the side and its two tails flying out."""
    im, d, S = _big(size)
    OUT = (30, 20, 20, 255)
    d.arc([S * .04, S * .1, S * .76, S * .8], 20, 160, fill=OUT, width=int(S * .2))
    d.arc([S * .06, S * .12, S * .74, S * .78], 22, 158, fill=(250, 250, 250, 255), width=int(S * .14))
    d.ellipse([S * .3, S * .62, S * .5, S * .82], fill=(220, 30, 30, 255), outline=OUT, width=5)                   # the sun
    d.ellipse([S * .66, S * .5, S * .82, S * .66], fill=(250, 250, 250, 255), outline=OUT, width=6)               # knot
    for a, b, c in (((.8, .54), (.98, .3), (.92, .5)), ((.8, .62), (.98, .82), (.88, .66))):
        d.polygon([(S * a[0], S * a[1]), (S * b[0], S * b[1]), (S * c[0], S * c[1])], fill=(250, 250, 250, 255))
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1]), (S * c[0], S * c[1]), (S * a[0], S * a[1])], fill=OUT, width=6)
    return _shrink(im, size)


def board_chairs(size=64, broken=False):
    """A pine board laid across two grey folding chairs (the strip-mall dojo setup) - or the board snapped in
    the middle, both halves sagging."""
    im, d, S = _big(size)
    OUT = (30, 20, 10, 255)
    for x0 in (.06, .66):
        d.rectangle([S * x0, S * .5, S * (x0 + .28), S * .58], fill=(150, 155, 165, 255), outline=OUT, width=5)  # seat
        d.line([(S * (x0 + .02), S * .58), (S * (x0 + .26), S * .96)], fill=(110, 115, 125, 255), width=7)
        d.line([(S * (x0 + .26), S * .58), (S * (x0 + .02), S * .96)], fill=(110, 115, 125, 255), width=7)
        d.rectangle([S * (x0 + .2), S * .2, S * (x0 + .26), S * .52], fill=(150, 155, 165, 255), outline=OUT, width=4)  # back
    WOOD, WOOD_D = (230, 190, 120, 255), (170, 120, 60, 255)
    if not broken:
        d.rectangle([S * .04, S * .38, S * .96, S * .5], fill=WOOD, outline=OUT, width=6)
        for x in (.2, .45, .7):
            d.arc([S * x, S * .4, S * (x + .12), S * .48], 200, 340, fill=WOOD_D, width=3)                         # grain
    else:
        d.polygon([(S * .04, S * .38), (S * .46, S * .46), (S * .5, S * .56), (S * .04, S * .5)], fill=WOOD, outline=OUT)
        d.polygon([(S * .96, S * .38), (S * .54, S * .46), (S * .5, S * .56), (S * .96, S * .5)], fill=WOOD, outline=OUT)
        d.line([(S * .04, S * .38), (S * .46, S * .46), (S * .5, S * .56), (S * .04, S * .5), (S * .04, S * .38)], fill=OUT, width=6)
        d.line([(S * .96, S * .38), (S * .54, S * .46), (S * .5, S * .56), (S * .96, S * .5), (S * .96, S * .38)], fill=OUT, width=6)
        for x, y in ((.44, .5), (.56, .5), (.5, .58)):
            d.line([(S * x, S * y), (S * (x + .03), S * (y + .06))], fill=WOOD_D, width=4)                         # splinters
    return _shrink(im, size)


def chop_streak(size=64):
    """A white karate-chop motion arc with speed lines (the hand itself isn't drawn)."""
    im, d, S = _big(size)
    d.arc([S * .08, S * .08, S * .92, S * .92], 200, 300, fill=(255, 255, 255, 255), width=int(S * .1))
    d.arc([S * .16, S * .16, S * .84, S * .84], 205, 295, fill=(180, 220, 255, 255), width=int(S * .04))
    for k in range(3):
        a = .18 + k * .12
        d.line([(S * a, S * (.6 - k * .1)), (S * (a + .14), S * (.74 - k * .1))], fill=(255, 255, 255, 220), width=5)
    return _shrink(im, size)


def m80(size=64):
    """An M-80: a fat red cardboard tube with a black band and a twisted green fuse out the side."""
    im, d, S = _big(size)
    OUT = (40, 5, 5, 255)
    d.rounded_rectangle([S * .3, S * .4, S * .78, S * .86], 12, fill=(200, 30, 30, 255), outline=OUT, width=8)
    d.rectangle([S * .3, S * .56, S * .78, S * .66], fill=(30, 30, 34, 255))
    d.rounded_rectangle([S * .3, S * .4, S * .78, S * .86], 12, outline=OUT, width=8)
    d.line([(S * .38, S * .46), (S * .38, S * .8)], fill=(255, 120, 110, 255), width=6)                         # shine
    d.ellipse([S * .3, S * .34, S * .78, S * .48], fill=(220, 200, 160, 255), outline=OUT, width=6)               # end cap
    d.line([(S * .54, S * .4), (S * .48, S * .22), (S * .56, S * .1)], fill=(40, 150, 60, 255), width=8)          # fuse
    return _shrink(im, size)


def m80_blast(size=64):
    """A cartoon explosion: a yellow-white core, an orange flame burst, a ring of dark smoke puffs."""
    import math
    im, d, S = _big(size)
    OUT = (40, 20, 10, 255)
    for k in range(9):
        a = k * 2 * math.pi / 9
        cx, cy = S * (.5 + .34 * math.cos(a)), S * (.5 + .3 * math.sin(a))
        d.ellipse([cx - S * .14, cy - S * .14, cx + S * .14, cy + S * .14], fill=(90, 85, 85, 255), outline=OUT, width=6)
    pts = []
    for k in range(24):
        a = k * 2 * math.pi / 24
        r = .4 if k % 2 == 0 else .26
        pts.append((S * (.5 + r * math.cos(a)), S * (.5 + r * math.sin(a))))
    d.polygon(pts, fill=(255, 130, 20, 255), outline=OUT)
    d.line(pts + [pts[0]], fill=OUT, width=6)
    d.ellipse([S * .32, S * .32, S * .68, S * .68], fill=(255, 230, 80, 255))
    d.ellipse([S * .4, S * .4, S * .6, S * .6], fill=(255, 255, 230, 255))
    return _shrink(im, size)


def zip_tie(size=64, color=(30, 30, 34, 255), hi=(110, 110, 120, 255)):
    """A zip tie cinched into a wide loop (seen at an angle): ridged strap, the square lock head and a long tail
    sticking out."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255) if color[0] > 100 else (200, 200, 205, 255)
    d.ellipse([S * .04, S * .3, S * .96, S * .66], outline=OUT, width=int(S * .1))
    d.ellipse([S * .05, S * .31, S * .95, S * .65], outline=color, width=int(S * .07))
    import math
    for k in range(18):
        a = k * 2 * math.pi / 18
        x, y = S * (.5 + .44 * math.cos(a)), S * (.48 + .16 * math.sin(a))
        d.line([(x, y - S * .02), (x, y + S * .02)], fill=hi, width=3)                                         # ridges
    d.rectangle([S * .42, S * .56, S * .6, S * .74], fill=color, outline=OUT, width=6)                           # lock head
    d.polygon([(S * .5, S * .72), (S * .6, S * .72), (S * .86, S * .96), (S * .76, S * .98)], fill=color)
    d.line([(S * .5, S * .72), (S * .76, S * .98), (S * .86, S * .96), (S * .6, S * .72)], fill=OUT, width=5)    # tail
    return _shrink(im, size)


def red_onion(size=64, bites=0):
    """A raw red onion, purple-red skin with layer lines, a dry sprout and roots - with 1 or 2 bites out of it
    showing the white rings inside."""
    im, d, S = _big(size)
    OUT = (50, 10, 40, 255)
    d.ellipse([S * .14, S * .24, S * .86, S * .92], fill=(170, 40, 110, 255), outline=OUT, width=8)
    for x0, x1 in ((.26, .74), (.38, .62)):
        d.arc([S * x0, S * .26, S * x1, S * .9], 100, 260, fill=(110, 20, 70, 255), width=5)
        d.arc([S * x0, S * .26, S * x1, S * .9], 280, 80, fill=(110, 20, 70, 255), width=5)
    d.arc([S * .2, S * .32, S * .5, S * .62], 200, 260, fill=(240, 150, 200, 255), width=6)                      # shine
    d.polygon([(S * .44, S * .28), (S * .5, S * .04), (S * .56, S * .28)], fill=(200, 170, 110, 255), outline=OUT)
    d.line([(S * .44, S * .28), (S * .5, S * .04), (S * .56, S * .28)], fill=OUT, width=5)                      # sprout
    for x in (.44, .5, .56):
        d.line([(S * .5, S * .9), (S * x, S * .98)], fill=(220, 200, 160, 255), width=4)                         # roots
    for n in range(bites):
        cx, cy = (S * .8, S * .48) if n == 0 else (S * .74, S * .74)
        d.ellipse([cx - S * .16, cy - S * .14, cx + S * .16, cy + S * .14], fill=(250, 240, 250, 255), outline=OUT, width=5)
        d.arc([cx - S * .1, cy - S * .08, cx + S * .1, cy + S * .08], 120, 240, fill=(220, 160, 210, 255), width=4)
        d.ellipse([cx, cy - S * .2, cx + S * .3, cy + S * .2], fill=(0, 0, 0, 0))
    return _shrink(im, size)


def stink_wave(n=16):
    """A wavy stink line (alpha only), for breath."""
    import math

    def f(x, y):
        yy = 8 + 3 * math.sin(x / 2.2)
        return 1 if abs(y - yy) < 1.3 and 1 < x < 15 else 0
    return _alpha(n, n, f)


def gaming_monitor(size=64, cracked=False):
    """A gaming monitor on its stand, the screen reading GAME OVER in red - or the same with the screen
    smashed (a spiderweb crack) (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (10, 10, 14, 255)
    d.rounded_rectangle([S * .04, S * .1, S * .96, S * .72], 8, fill=(30, 30, 36, 255), outline=OUT, width=7)
    d.rectangle([S * .1, S * .16, S * .9, S * .66], fill=(10, 10, 30, 255))
    d.line([(S * .1, S * .68), (S * .9, S * .68)], fill=(80, 200, 255, 255), width=4)                           # RGB strip
    d.rectangle([S * .44, S * .72, S * .56, S * .86], fill=(50, 50, 56, 255), outline=OUT, width=5)
    d.rounded_rectangle([S * .26, S * .84, S * .74, S * .94], 6, fill=(50, 50, 56, 255), outline=OUT, width=5)
    if cracked:
        import math
        c = (S * .62, S * .36)
        for k in range(7):
            a = k * 2 * math.pi / 7 + .3
            d.line([c, (c[0] + S * .3 * math.cos(a), c[1] + S * .24 * math.sin(a))], fill=(230, 240, 255, 255), width=4)
        d.ellipse([c[0] - S * .1, c[1] - S * .08, c[0] + S * .1, c[1] + S * .08], outline=(230, 240, 255, 255), width=3)
    im = _shrink(im, size)
    # keep the screen dark round the words, crack lines included
    return _texted(im, [("GAME", (30, 15)), ("OVER", (30, 25))], (255, 50, 50, 255), (10, 10, 30, 255))


def gamepad(size=64):
    """A black gamepad: two grips, a d-pad, four coloured face buttons, two sticks."""
    im, d, S = _big(size)
    OUT = (5, 5, 8, 255)
    B = (40, 40, 46, 255)
    d.ellipse([S * .04, S * .3, S * .38, S * .86], fill=B, outline=OUT, width=7)
    d.ellipse([S * .62, S * .3, S * .96, S * .86], fill=B, outline=OUT, width=7)
    d.rounded_rectangle([S * .16, S * .26, S * .84, S * .62], 20, fill=B, outline=OUT, width=7)
    d.rectangle([S * .16, S * .32, S * .84, S * .58], fill=B)
    d.rectangle([S * .14, S * .4, S * .3, S * .46], fill=(120, 120, 130, 255))                                   # d-pad
    d.rectangle([S * .19, S * .35, S * .25, S * .51], fill=(120, 120, 130, 255))
    for (x, y), c in (((.72, .34), (240, 200, 40)), ((.66, .42), (40, 120, 230)), ((.78, .42), (220, 40, 40)), ((.72, .5), (40, 190, 80))):
        d.ellipse([S * (x - .04), S * (y - .04), S * (x + .04), S * (y + .04)], fill=c + (255,), outline=OUT, width=3)
    for x in (.38, .58):
        d.ellipse([S * (x - .06), S * .5, S * (x + .06), S * .62], fill=(90, 90, 100, 255), outline=OUT, width=4)
    d.line([(S * .2, S * .32), (S * .4, S * .3)], fill=(110, 110, 120, 255), width=4)
    return _shrink(im, size)
