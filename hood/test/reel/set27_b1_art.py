

# ---- set 27, batch 1: Send It, Allergy Szn, Blackout, Aura Farm, Rush Hour --------------------------------------------

def hero_cape(size=64, flap=0):
    """A red bedsheet cape tied at the neck, billowing out to the left (flap 1 = blown higher)."""
    im, d, S = _big(size)
    OUT = (70, 0, 10, 255)
    lift = .16 * flap
    pts = [(S * .62, S * .14), (S * .72, S * .2), (S * .66, S * .5), (S * .5, S * (.92 - lift)), (S * .3, S * (.8 - lift)),
           (S * .12, S * (.86 - lift * 1.6)), (S * .06, S * (.6 - lift * 1.4)), (S * .4, S * .3)]
    _outline_poly(d, pts, (220, 30, 40, 255), OUT, 7)
    d.line([(S * .56, S * .28), (S * .24, S * (.72 - lift))], fill=(250, 90, 100, 255), width=5)                 # fold
    d.line([(S * .5, S * .34), (S * .4, S * (.82 - lift))], fill=(170, 20, 30, 255), width=5)
    d.ellipse([S * .56, S * .08, S * .74, S * .22], fill=(250, 250, 250, 255), outline=OUT, width=4)             # the knot
    return _shrink(im, size)


def dive_goggles(size=32):
    """Big swim/aviator goggles: two round blue lenses with glare, black strap."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.line([(S * .0, S * .5), (S * 1.0, S * .5)], fill=OUT, width=10)
    for x in (.08, .52):
        d.ellipse([S * x, S * .26, S * (x + .4), S * .74], fill=(90, 190, 250, 255), outline=OUT, width=7)
        d.arc([S * (x + .08), S * .34, S * (x + .3), S * .58], 200, 280, fill=(240, 250, 255, 255), width=5)
    return _shrink(im, size)


def roof_ledge(size=64):
    """The edge of a projects rooftop: a brick parapet with a tar cap, a satellite dish on it."""
    im, d, S = _big(size)
    OUT = (40, 15, 10, 255)
    d.rectangle([S * .0, S * .5, S * 1.0, S * 1.0], fill=(160, 70, 50, 255), outline=OUT, width=6)
    for r in range(4):                                                          # bricks
        y = .58 + r * .11
        d.line([(0, S * y), (S, S * y)], fill=(110, 45, 30, 255), width=3)
        for c in range(6):
            x = (c + (r % 2) * .5) / 6
            d.line([(S * x, S * (y - .11)), (S * x, S * y)], fill=(110, 45, 30, 255), width=3)
    d.rectangle([S * .0, S * .44, S * 1.0, S * .52], fill=(70, 70, 75, 255), outline=OUT, width=5)            # cap
    d.chord([S * .66, S * .08, S * .96, S * .38], 120, 300, fill=(220, 220, 225, 255), outline=OUT, width=5)    # dish
    d.line([(S * .82, S * .24), (S * .84, S * .44)], fill=OUT, width=5)
    return _shrink(im, size)


def dive_crater(size=64):
    """A smoking impact crater: a cracked dark bowl with rubble chunks thrown up round the rim."""
    im, d, S = _big(size)
    OUT = (30, 20, 15, 255)
    d.ellipse([S * .04, S * .5, S * .96, S * .94], fill=(120, 95, 70, 255), outline=OUT, width=7)
    d.ellipse([S * .18, S * .58, S * .82, S * .86], fill=(50, 35, 25, 255))
    for a, b in (((.3, .7), (.18, .62)), ((.66, .74), (.82, .64)), ((.5, .62), (.52, .54))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=OUT, width=4)
    for x, y, r in ((.08, .44, .07), (.86, .42, .06), (.3, .42, .05), (.68, .4, .05)):
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], fill=(140, 115, 90, 255), outline=OUT, width=4)
    return _shrink(im, size)


def pollen_board(size=64, level="HIGH"):
    """The TV pollen count graphic: POLLEN COUNT over a level bar, green - orange - red by level (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    col = {"HIGH": (240, 200, 40, 255), "VERY HIGH": (250, 130, 30, 255), "EXTREME": (230, 30, 30, 255)}[level]
    n = {"HIGH": 2, "VERY HIGH": 3, "EXTREME": 4}[level]
    d.rounded_rectangle([S * .02, S * .14, S * .98, S * .86], 14, fill=(30, 40, 80, 255), outline=OUT, width=7)
    for k in range(4):                                                          # the level bar
        x = .12 + k * .2
        d.rectangle([S * x, S * .6, S * (x + .16), S * .76], fill=col if k < n else (70, 80, 110, 255), outline=OUT, width=4)
    im = _shrink(im, size)
    return _texted(im, [("POLLEN", (32, 12)), (level, (32, 23))], (255, 255, 255, 255), (20, 20, 25, 255))


def monster_flower(size=64, open_=1):
    """A giant yellow flower (open_ 0 = a fat bud, 1 = wide open with a pollen-dusted centre)."""
    im, d, S = _big(size)
    OUT = (60, 50, 0, 255)
    d.line([(S * .5, S * .56), (S * .5, S * 1.0)], fill=(40, 120, 40, 255), width=int(S * .08))
    d.ellipse([S * .52, S * .74, S * .8, S * .86], fill=(70, 170, 60, 255), outline=(30, 80, 30, 255), width=4)  # leaf
    if not open_:
        d.ellipse([S * .34, S * .24, S * .66, S * .62], fill=(110, 180, 70, 255), outline=(30, 80, 30, 255), width=6)
        d.polygon([(S * .4, S * .3), (S * .5, S * .14), (S * .6, S * .3)], fill=(250, 210, 60, 255), outline=OUT)
        return _shrink(im, size)
    import math
    for k in range(10):
        a = k * math.tau / 10
        cx, cy = .5 + .3 * math.cos(a), .4 + .3 * math.sin(a)
        d.ellipse([S * (cx - .14), S * (cy - .14), S * (cx + .14), S * (cy + .14)], fill=(250, 210, 40, 255), outline=OUT, width=4)
    d.ellipse([S * .3, S * .2, S * .7, S * .6], fill=(140, 80, 30, 255), outline=OUT, width=6)
    for k in range(14):
        x, y = .36 + (k * 37 % 28) / 100, .26 + (k * 23 % 28) / 100
        d.ellipse([S * x, S * y, S * (x + .04), S * (y + .04)], fill=(255, 240, 120, 255))
    return _shrink(im, size)


def pollen_dot(n=16):
    """A fuzzy pollen grain (alpha only): a soft dot with a spiky rim."""
    c = (n - 1) / 2

    def f(x, y):
        r = ((x - c) ** 2 + (y - c) ** 2) ** .5
        return 1 if r < 3.5 else (.6 if r < 5.5 and (x + y) % 2 == 0 else 0)
    return _alpha(n, n, f)


def city_skyline(size=64, lit=3):
    """A row of project towers at night; `lit` of the 3 blocks still have yellow windows on (0 = all dark)."""
    im, d, S = _big(size)
    OUT = (10, 10, 20, 255)
    towers = [(.0, .3, .3), (.28, .12, .26), (.52, .38, .22), (.72, .2, .28)]
    for i, (x, top, w) in enumerate(towers):
        d.rectangle([S * x, S * top, S * (x + w), S * 1.0], fill=(40, 40, 60, 255), outline=OUT, width=5)
        on = (i * 3) // 4 < lit
        for r in range(int((1 - top) / .1) - 1):
            for c in range(int(w / .08)):
                wx, wy = x + .04 + c * .08, top + .06 + r * .1
                if wx + .04 < x + w:
                    lamp = (250, 220, 90, 255) if on and (r * 7 + c * 3 + i) % 5 else (20, 20, 35, 255)
                    d.rectangle([S * wx, S * wy, S * (wx + .04), S * (wy + .05)], fill=lamp)
    return _shrink(im, size)


def dark_eyes(size=32):
    """Two glowing white eyes with tiny pupils, floating in the dark."""
    im, d, S = _big(size)
    for x in (.1, .56):
        d.ellipse([S * x, S * .3, S * (x + .34), S * .7], fill=(250, 250, 255, 255), outline=(120, 120, 180, 255), width=4)
        d.ellipse([S * (x + .12), S * .42, S * (x + .22), S * .58], fill=(10, 10, 20, 255))
    return _shrink(im, size)


def aura_tag(size=64, n="+100"):
    """A floating gamer-style score popup: "+100" over AURA in glowing purple (shown at 1:1)."""
    im, d, S = _big(size)
    d.rounded_rectangle([S * .04, S * .24, S * .96, S * .76], 16, fill=(60, 20, 100, 230), outline=(200, 140, 255, 255), width=6)
    im = _shrink(im, size)
    return _texted(im, [(n, (32, 18)), ("AURA", (32, 30))], (255, 230, 120, 255), (60, 0, 90, 255), font=SMALL)


def aura_orb(size=64):
    """A huge glowing aura ball: a white-hot core in layered blue-violet rings, crackling rim."""
    im, d, S = _big(size)
    for r, c in ((.48, (90, 60, 220, 140)), (.4, (120, 90, 250, 200)), (.3, (170, 150, 255, 255)), (.18, (235, 230, 255, 255)), (.08, (255, 255, 255, 255))):
        d.ellipse([S * (.5 - r), S * (.5 - r), S * (.5 + r), S * (.5 + r)], fill=c)
    import math
    for k in range(8):
        a = k * math.tau / 8 + .3
        d.line([(S * (.5 + .36 * math.cos(a)), S * (.5 + .36 * math.sin(a))), (S * (.5 + .48 * math.cos(a + .2)), S * (.5 + .48 * math.sin(a + .2)))],
               fill=(255, 255, 255, 255), width=4)
    return _shrink(im, size)


def subway_car(size=64, doors_open=False):
    """The front half of a silver subway car: windows, a lit route sign, sliding doors (open = dark gap)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.rounded_rectangle([S * .0, S * .14, S * 1.0, S * .9], 14, fill=(190, 195, 205, 255), outline=OUT, width=7)
    d.rectangle([S * .0, S * .66, S * 1.0, S * .72], fill=(40, 120, 220, 255))                                  # the stripe
    d.rectangle([S * .06, S * .2, S * .34, S * .3], fill=(20, 20, 20, 255), outline=OUT, width=3)                # route sign
    d.ellipse([S * .1, S * .21, S * .18, S * .29], fill=(250, 140, 30, 255))
    for x in (.42, .8):                                                          # windows
        d.rectangle([S * x, S * .24, S * (x + .14), S * .44], fill=(140, 190, 230, 255), outline=OUT, width=4)
    if doors_open:
        d.rectangle([S * .58, S * .24, S * .76, S * .86], fill=(30, 30, 40, 255), outline=OUT, width=5)
    else:
        d.rectangle([S * .58, S * .24, S * .76, S * .86], fill=(170, 175, 185, 255), outline=OUT, width=5)
        d.line([(S * .67, S * .24), (S * .67, S * .86)], fill=OUT, width=4)
        for x in (.6, .69):
            d.rectangle([S * x, S * .3, S * (x + .06), S * .46], fill=(140, 190, 230, 255), outline=OUT, width=3)
    d.ellipse([S * .1, S * .82, S * .26, S * .98], fill=(50, 50, 55, 255), outline=OUT, width=4)
    return _shrink(im, size)


def commuter(size=32, tint=0):
    """A rush-hour commuter mid-stride: suit (3 colors), briefcase swinging, coffee cup held up."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    suit = [(50, 60, 90, 255), (90, 60, 50, 255), (60, 60, 64, 255)][tint % 3]
    d.ellipse([S * .38, S * .04, S * .62, S * .26], fill=(220, 170, 130, 255) if tint != 1 else (140, 90, 60, 255), outline=OUT, width=4)
    d.rounded_rectangle([S * .34, S * .24, S * .66, S * .62], 6, fill=suit, outline=OUT, width=4)
    d.line([(S * .42, S * .62), (S * .3, S * .96)], fill=OUT, width=7)                                           # legs mid-stride
    d.line([(S * .58, S * .62), (S * .72, S * .96)], fill=OUT, width=7)
    d.rectangle([S * .06, S * .48, S * .32, S * .66], fill=(110, 70, 30, 255), outline=OUT, width=4)            # briefcase
    d.rectangle([S * .68, S * .14, S * .84, S * .34], fill=(250, 250, 245, 255), outline=OUT, width=3)          # coffee
    d.rectangle([S * .68, S * .14, S * .84, S * .18], fill=(40, 30, 20, 255))
    return _shrink(im, size)
