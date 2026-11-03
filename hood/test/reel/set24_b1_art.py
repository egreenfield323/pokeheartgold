

# ---- set 24, batch 1 (INSANE): Full Auto, 18 Wheeler, Holy Fire, Sentencing, Clock Out --------------------------

def jam_pistol(size=64):
    """A black pistol, slide locked back (jammed), pointing right."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rectangle([S * .14, S * .34, S * .8, S * .48], fill=(50, 50, 56, 255), outline=OUT, width=6)               # slide
    d.rectangle([S * .74, S * .38, S * .92, S * .44], fill=(80, 80, 88, 255), outline=OUT, width=4)              # barrel out
    d.polygon([(S * .2, S * .48), (S * .42, S * .48), (S * .36, S * .86), (S * .16, S * .86)], fill=(40, 40, 46, 255), outline=OUT)
    d.line([(S * .2, S * .48), (S * .42, S * .48), (S * .36, S * .86), (S * .16, S * .86), (S * .2, S * .48)], fill=OUT, width=6)
    d.arc([S * .38, S * .46, S * .58, S * .66], 0, 180, fill=OUT, width=5)                                        # trigger guard
    d.line([(S * .2, S * .37), (S * .7, S * .37)], fill=(140, 140, 150, 255), width=3)
    return _shrink(im, size)


def mini_uzi(size=64):
    """A boxy black uzi: stubby barrel, the long magazine down through the grip, a folding stock."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rectangle([S * .2, S * .32, S * .78, S * .5], fill=(45, 45, 50, 255), outline=OUT, width=6)
    d.rectangle([S * .78, S * .38, S * .94, S * .44], fill=(70, 70, 78, 255), outline=OUT, width=4)
    d.rectangle([S * .42, S * .5, S * .54, S * .96], fill=(35, 35, 40, 255), outline=OUT, width=5)               # mag
    d.line([(S * .2, S * .36), (S * .04, S * .3), (S * .04, S * .5)], fill=(60, 60, 66, 255), width=6)          # stock
    d.line([(S * .24, S * .36), (S * .74, S * .36)], fill=(130, 130, 140, 255), width=3)
    return _shrink(im, size)


def minigun(size=64, phase=0):
    """A minigun on a tripod: six barrels in a rotary cluster (phase shifts the barrel shine so it spins), the
    motor housing, a brass ammo belt hanging off it, three tripod legs."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    for a, b in (((.36, .58), (.14, .96)), ((.36, .58), (.58, .96)), ((.36, .58), (.36, .96))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(60, 60, 66, 255), width=9)                     # tripod
    d.rounded_rectangle([S * .16, S * .3, S * .46, S * .6], 10, fill=(70, 75, 60, 255), outline=OUT, width=7)    # motor
    d.rectangle([S * .46, S * .32, S * .98, S * .56], fill=(55, 55, 60, 255), outline=OUT, width=6)              # barrels
    for k in range(6):
        y = .35 + k * .035
        c = (230, 230, 240, 255) if (k + phase) % 3 == 0 else (110, 110, 120, 255)
        d.line([(S * .48, S * y), (S * .96, S * y)], fill=c, width=3)
    for x in (.58, .8):
        d.rectangle([S * x, S * .3, S * (x + .04), S * .58], fill=(90, 90, 96, 255), outline=OUT, width=3)        # clamps
    for k in range(6):                                                                                             # ammo belt
        d.rectangle([S * (.2 - k * .02), S * (.6 + k * .06), S * (.28 - k * .02), S * (.66 + k * .06)], fill=(230, 180, 60, 255), outline=OUT, width=3)
    d.rectangle([S * .22, S * .18, S * .3, S * .3], fill=(40, 40, 46, 255), outline=OUT, width=4)                # handle
    return _shrink(im, size)


def tracer_streak(n=16):
    """A hot bullet tracer (alpha only): a bright horizontal streak, thicker at the head."""
    def f(x, y):
        w = .6 + x / 16 * 1.4
        return max(0, 1 - abs(y - 7.5) / w) * (x / 15) if x > 1 else 0
    return _alpha(n, n, f)


def brass_shell(n=16):
    """A spent brass casing (alpha only)."""
    return _alpha(n, n, lambda x, y: 1 if 5 <= x <= 10 and 4 <= y <= 12 and not (y < 6 and (x == 5 or x == 10)) else 0)


def muzzle_star(size=32):
    """A big blinding muzzle flash: white core, yellow-orange spikes."""
    import math
    im, d, S = _big(size)
    pts = []
    for k in range(14):
        a = k * 2 * math.pi / 14
        r = .48 if k % 2 == 0 else .18
        pts.append((S * (.5 + r * math.cos(a)), S * (.5 + r * .7 * math.sin(a))))
    d.polygon(pts, fill=(255, 170, 30, 255))
    d.ellipse([S * .3, S * .36, S * .7, S * .64], fill=(255, 240, 120, 255))
    d.ellipse([S * .38, S * .42, S * .62, S * .58], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def semi_truck(size=64):
    """An 18-wheeler facing right: a long silver trailer, a big red cab with a chrome grille, twin exhaust stacks,
    a row of wheels (drawn on a wide canvas: the art fills the width, ~45% of the height)."""
    im, d, S = _big(size)
    OUT = (15, 10, 10, 255)
    y0, y1 = .3, .74
    d.rectangle([S * .02, S * y0, S * .66, S * (y1 - .06)], fill=(215, 220, 230, 255), outline=OUT, width=6)     # trailer
    d.line([(S * .04, S * (y0 + .06)), (S * .64, S * (y0 + .06))], fill=(255, 255, 255, 255), width=4)
    for x in (.2, .4):
        d.line([(S * x, S * y0), (S * x, S * (y1 - .06))], fill=(160, 165, 175, 255), width=3)
    d.rectangle([S * .66, S * (y0 + .08), S * .9, S * (y1 - .04)], fill=(210, 30, 30, 255), outline=OUT, width=6)  # cab
    d.polygon([(S * .74, S * (y0 + .1)), (S * .86, S * (y0 + .1)), (S * .86, S * (y0 + .22)), (S * .74, S * (y0 + .22))], fill=(120, 190, 240, 255), outline=OUT)
    d.rectangle([S * .9, S * (y0 + .14), S * .99, S * (y1 - .04)], fill=(200, 205, 215, 255), outline=OUT, width=5)  # grille
    for k in range(4):
        d.line([(S * .91, S * (y0 + .18 + k * .06)), (S * .98, S * (y0 + .18 + k * .06))], fill=(120, 120, 130, 255), width=3)
    d.ellipse([S * .955, S * (y1 - .14), S * .99, S * (y1 - .09)], fill=(255, 250, 200, 255))                     # headlight
    for x in (.68, .72):
        d.rectangle([S * x, S * (y0 - .12), S * (x + .025), S * (y0 + .08)], fill=(200, 205, 215, 255), outline=OUT, width=3)  # stacks
    for x in (.08, .16, .5, .58, .78, .9):
        d.ellipse([S * (x - .05), S * (y1 - .1), S * (x + .05), S * y1 + S * .02], fill=(25, 25, 28, 255), outline=OUT, width=4)
        d.ellipse([S * (x - .02), S * (y1 - .06), S * (x + .02), S * (y1 - .02)], fill=(180, 180, 190, 255))
    return _shrink(im, size)


def stained_glass(size=64, lit=False):
    """An arched church window of coloured glass in lead lines (a cross in the middle); lit = blazing bright."""
    im, d, S = _big(size)
    OUT = (30, 25, 20, 255)
    k = 1.0 if lit else .7
    cols = [(220, 40, 60), (40, 90, 220), (250, 200, 40), (60, 170, 80), (160, 60, 200)]
    d.rounded_rectangle([S * .14, S * .04, S * .86, S * .96], int(S * .36), fill=(60, 50, 40, 255), outline=OUT, width=8)
    i = 0
    for y in range(4):
        for x in range(3):
            c = cols[i % len(cols)]
            i += 1
            c = tuple(min(255, int(v * k + (60 if lit else 0))) for v in c) + (255,)
            d.rectangle([S * (.22 + x * .19), S * (.2 + y * .19), S * (.39 + x * .19), S * (.37 + y * .19)], fill=c, outline=OUT, width=4)
    d.pieslice([S * .22, S * .1, S * .78, S * .5], 180, 360, fill=(250, 220, 120, 255) if lit else (200, 170, 90, 255), outline=OUT, width=4)
    d.rectangle([S * .46, S * .26, S * .54, S * .86], fill=(255, 245, 210, 255) if lit else (220, 210, 180, 255), outline=OUT, width=3)
    d.rectangle([S * .34, S * .42, S * .66, S * .5], fill=(255, 245, 210, 255) if lit else (220, 210, 180, 255), outline=OUT, width=3)
    return _shrink(im, size)


def holy_ray(n=16):
    """A soft vertical shaft of light (alpha only)."""
    return _alpha(n, n, lambda x, y: max(0, 1 - abs(x - 7.5) / 6.5) ** 1.5)


def gold_halo(size=32):
    """A glowing gold halo ring seen at an angle."""
    im, d, S = _big(size)
    d.ellipse([S * .06, S * .32, S * .94, S * .68], outline=(140, 90, 0, 255), width=int(S * .12))
    d.ellipse([S * .08, S * .34, S * .92, S * .66], outline=(255, 220, 60, 255), width=int(S * .07))
    d.arc([S * .12, S * .36, S * .88, S * .64], 190, 260, fill=(255, 255, 220, 255), width=5)
    return _shrink(im, size)


def judge_gavel(size=64):
    """A judge's wooden gavel, head at the top right, handle down-left, brass bands, on its sound block."""
    im, d, S = _big(size)
    OUT = (40, 20, 5, 255)
    W, WD = (160, 95, 45, 255), (110, 60, 25, 255)
    d.line([(S * .2, S * .86), (S * .6, S * .38)], fill=OUT, width=int(S * .12))
    d.line([(S * .2, S * .86), (S * .6, S * .38)], fill=W, width=int(S * .08))                                   # handle
    head = [(S * .42, S * .3), (S * .7, S * .06), (S * .96, S * .34), (S * .68, S * .58)]
    d.polygon(head, fill=W)
    d.line(head + [head[0]], fill=OUT, width=7)
    for t in (.3, .7):
        a = (head[0][0] + (head[1][0] - head[0][0]) * t, head[0][1] + (head[1][1] - head[0][1]) * t)
        b = (head[3][0] + (head[2][0] - head[3][0]) * t, head[3][1] + (head[2][1] - head[3][1]) * t)
        d.line([a, b], fill=(230, 180, 60, 255), width=6)                                                          # brass bands
    d.line([(S * .5, S * .26), (S * .74, S * .1)], fill=(210, 150, 90, 255), width=4)
    return _shrink(im, size)


def time_clock(size=64, t="4:58"):
    """A punch time clock on the wall: grey box, a red digital readout (shown at 1:1), the card slot and a rack of
    time cards beside it."""
    im, d, S = _big(size)
    OUT = (20, 20, 26, 255)
    d.rounded_rectangle([S * .08, S * .1, S * .74, S * .9], 10, fill=(180, 185, 195, 255), outline=OUT, width=8)
    d.rectangle([S * .16, S * .2, S * .66, S * .44], fill=(20, 10, 10, 255), outline=OUT, width=5)               # display
    d.rectangle([S * .24, S * .58, S * .58, S * .66], fill=(30, 30, 36, 255))                                      # card slot
    d.rectangle([S * .78, S * .18, S * .96, S * .86], fill=(120, 90, 60, 255), outline=OUT, width=5)            # card rack
    for k in range(4):
        d.rectangle([S * .8, S * (.22 + k * .16), S * .94, S * (.32 + k * .16)], fill=(250, 245, 220, 255), outline=OUT, width=3)
    im = _shrink(im, size)
    _big_text(im, t, (26, 21), (255, 50, 40, 255) if t != "5:00" else (80, 255, 120, 255), scale=2)
    return im


def punch_card(size=32):
    """A buff time card with ruled lines."""
    im, d, S = _big(size)
    OUT = (60, 50, 30, 255)
    d.rectangle([S * .28, S * .04, S * .72, S * .96], fill=(250, 240, 200, 255), outline=OUT, width=6)
    for k in range(6):
        d.line([(S * .34, S * (.18 + k * .13)), (S * .66, S * (.18 + k * .13))], fill=(180, 160, 120, 255), width=4)
    d.rectangle([S * .28, S * .04, S * .72, S * .14], fill=(220, 60, 60, 255), outline=OUT, width=5)
    return _shrink(im, size)


def wall_clock(size=32):
    """A round white wall clock with a black rim and two hands (spins as a particle; no text)."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.ellipse([S * .06, S * .06, S * .94, S * .94], fill=(250, 250, 250, 255), outline=OUT, width=int(S * .09))
    for k in range(12):
        import math
        a = k * math.pi / 6
        d.line([(S * (.5 + .34 * math.cos(a)), S * (.5 + .34 * math.sin(a))), (S * (.5 + .4 * math.cos(a)), S * (.5 + .4 * math.sin(a)))], fill=OUT, width=4)
    d.line([(S * .5, S * .5), (S * .5, S * .2)], fill=OUT, width=6)
    d.line([(S * .5, S * .5), (S * .72, S * .58)], fill=(220, 30, 30, 255), width=5)
    return _shrink(im, size)


def holy_flame(n=16):
    """A small teardrop flame lick (alpha only, 16x16): pointed top, round bottom."""
    def f(x, y):
        dx = abs(x - 7.5)
        if y > 9:
            return max(0, 1 - ((dx / 5) ** 2 + ((y - 9.5) / 5) ** 2))
        half = 5 * (y - 1) / 8.5
        return max(0, 1 - dx / max(half, .1)) if y > 1 else 0
    return _alpha(n, n, f)
