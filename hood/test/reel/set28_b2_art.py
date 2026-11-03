

# ---- set 28, batch 2: Mirror Tint, Jump Em, Quick Draw, Bad Vibes, Hood Power ---------------------------------------------

def tint_glass(size=64, tinted=False):
    """A car's side window glass in its rubber frame: clear see-through, or mirror-tinted black with a chrome sheen."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    pts = [(S * .06, S * .9), (S * .2, S * .14), (S * .9, S * .14), (S * .96, S * .9)]
    _outline_poly(d, pts, (20, 20, 30, 255) if tinted else (190, 225, 245, 120), OUT, 8)
    if tinted:
        d.polygon([(S * .3, S * .2), (S * .5, S * .2), (S * .26, S * .84), (S * .1, S * .84)], fill=(140, 150, 180, 255))
        d.polygon([(S * .56, S * .2), (S * .62, S * .2), (S * .4, S * .84), (S * .34, S * .84)], fill=(110, 120, 150, 255))
    else:
        d.line([(S * .34, S * .24), (S * .2, S * .7)], fill=(255, 255, 255, 200), width=5)
    return _shrink(im, size)


def tint_squeegee(size=32):
    """A rubber-bladed squeegee: black blade, orange handle."""
    im, d, S = _big(size)
    OUT = (20, 20, 20, 255)
    d.rectangle([S * .06, S * .14, S * .94, S * .3], fill=(30, 30, 30, 255), outline=OUT, width=4)
    d.rectangle([S * .14, S * .3, S * .86, S * .42], fill=(160, 160, 170, 255), outline=OUT, width=4)
    d.line([(S * .5, S * .42), (S * .5, S * .96)], fill=OUT, width=int(S * .16))
    d.line([(S * .5, S * .42), (S * .5, S * .96)], fill=(250, 140, 30, 255), width=int(S * .1))
    return _shrink(im, size)


def crew_member(size=64, tint=0):
    """One of the crew pulling up: a full figure in a hoodie (hood up, face in shadow), jeans, fresh kicks."""
    im, d, S = _big(size)
    OUT = (10, 10, 15, 255)
    col = [(60, 60, 70, 255), (150, 30, 40, 255), (40, 70, 140, 255)][tint % 3]
    d.polygon([(S * .3, S * .3), (S * .7, S * .3), (S * .76, S * .62), (S * .24, S * .62)], fill=col, outline=OUT)
    d.line([(S * .3, S * .3), (S * .7, S * .3), (S * .76, S * .62), (S * .24, S * .62), (S * .3, S * .3)], fill=OUT, width=5)
    d.ellipse([S * .34, S * .04, S * .66, S * .36], fill=col, outline=OUT, width=5)                               # the hood
    d.ellipse([S * .41, S * .12, S * .59, S * .32], fill=(25, 20, 20, 255))                                       # shadowed face
    d.rectangle([S * .38, S * .46, S * .62, S * .56], fill=tuple(max(0, c - 30) for c in col[:3]) + (255,), outline=OUT, width=3)   # pocket
    d.rectangle([S * .3, S * .62, S * .48, S * .9], fill=(50, 80, 140, 255), outline=OUT, width=4)
    d.rectangle([S * .52, S * .62, S * .7, S * .9], fill=(50, 80, 140, 255), outline=OUT, width=4)
    for x in (.26, .5):
        d.rounded_rectangle([S * x, S * .88, S * (x + .24), S * .98], 4, fill=(250, 250, 250, 255), outline=OUT, width=3)
    return _shrink(im, size)


def cowboy_hat(size=32):
    """A tan cowboy hat with a dark band."""
    im, d, S = _big(size)
    OUT = (60, 35, 10, 255)
    d.chord([S * .02, S * .44, S * .98, S * .86], 180, 360, fill=(200, 150, 90, 255), outline=OUT, width=5)
    d.ellipse([S * .02, S * .54, S * .98, S * .8], fill=(200, 150, 90, 255), outline=OUT, width=5)
    d.rounded_rectangle([S * .26, S * .18, S * .74, S * .64], 12, fill=(210, 160, 100, 255), outline=OUT, width=5)
    d.rectangle([S * .26, S * .5, S * .74, S * .6], fill=(70, 40, 20, 255))
    d.line([(S * .5, S * .2), (S * .5, S * .34)], fill=OUT, width=4)
    return _shrink(im, size)


def noon_clock(size=64, noon=False):
    """A big town clock face: hands at 11:59 - or straight up at 12:00 (noon) with the 12 lit red."""
    im, d, S = _big(size)
    OUT = (40, 25, 10, 255)
    import math
    d.ellipse([S * .06, S * .06, S * .94, S * .94], fill=(250, 240, 210, 255), outline=OUT, width=8)
    for k in range(12):
        a = k * math.tau / 12 - math.pi / 2
        d.line([(S * (.5 + .34 * math.cos(a)), S * (.5 + .34 * math.sin(a))), (S * (.5 + .4 * math.cos(a)), S * (.5 + .4 * math.sin(a)))],
               fill=(220, 30, 30, 255) if (k == 0 and noon) else OUT, width=7 if k % 3 == 0 else 4)
    m = -math.pi / 2 - (0 if noon else math.tau / 60)
    h = -math.pi / 2 - (0 if noon else math.tau / 720)
    d.line([(S * .5, S * .5), (S * (.5 + .22 * math.cos(h)), S * (.5 + .22 * math.sin(h)))], fill=OUT, width=9)
    d.line([(S * .5, S * .5), (S * (.5 + .34 * math.cos(m)), S * (.5 + .34 * math.sin(m)))], fill=OUT, width=6)
    d.ellipse([S * .45, S * .45, S * .55, S * .55], fill=(220, 30, 30, 255))
    return _shrink(im, size)


def air_ring(n=16):
    """A shockwave ring of air (alpha only): a thin bright circle."""
    c = (n - 1) / 2
    return _alpha(n, n, lambda x, y: max(0, 1 - abs(((x - c) ** 2 + (y - c) ** 2) ** .5 - 6) / 1.4))


def vibe_meter(size=64, level=0):
    """A VIBE CHECK gauge: green-yellow-red arc, the needle on GOOD (0), OK (1) or BAD (2) (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    import math
    d.rounded_rectangle([S * .04, S * .1, S * .96, S * .9], 10, fill=(40, 40, 50, 255), outline=OUT, width=6)
    for k, col in enumerate(((80, 200, 90, 255), (240, 210, 50, 255), (230, 50, 50, 255))):
        d.arc([S * .16, S * .3, S * .84, S * .98], 180 + k * 60, 240 + k * 60, fill=col, width=12)
    a = math.pi + (level * 60 + 30) * math.pi / 180
    d.line([(S * .5, S * .64), (S * (.5 + .3 * math.cos(a)), S * (.64 + .3 * math.sin(a)))], fill=(255, 255, 255, 255), width=6)
    d.ellipse([S * .45, S * .59, S * .55, S * .69], fill=(255, 255, 255, 255))
    im = _shrink(im, size)
    word = ("GOOD", "OK", "BAD")[level]
    return _texted(im, [("VIBE CHECK", (32, 9)), (word, (32, 45))], (255, 255, 255, 255) if level < 2 else (255, 90, 90, 255), (20, 20, 25, 255))


def bodega_cat(size=64, swat=False):
    """The bodega cat: a fat orange tabby sat on its haunches, unimpressed - or up on its back legs mid-swat."""
    im, d, S = _big(size)
    OUT = (70, 30, 0, 255)
    OR, LT = (240, 150, 50, 255), (255, 210, 150, 255)
    body = [S * .24, S * (.36 if swat else .46), S * .76, S * .96]
    d.ellipse(body, fill=OR, outline=OUT, width=6)
    d.ellipse([S * .34, S * (.56 if swat else .64), S * .66, S * .94], fill=LT)                                    # belly
    hy = .1 if swat else .2
    d.ellipse([S * .28, S * hy, S * .72, S * (hy + .38)], fill=OR, outline=OUT, width=6)                            # head
    for x in (.3, .62):                                                                                             # ears
        d.polygon([(S * x, S * (hy + .1)), (S * (x + .04), S * (hy - .06)), (S * (x + .1), S * (hy + .06))], fill=OR, outline=OUT)
    for x in (.38, .56):                                                                                            # eyes, half-shut
        d.line([(S * x, S * (hy + .18)), (S * (x + .08), S * (hy + .18))], fill=OUT, width=6)
    d.polygon([(S * .47, S * (hy + .25)), (S * .53, S * (hy + .25)), (S * .5, S * (hy + .29))], fill=(240, 120, 140, 255))
    for k in range(3):                                                                                              # stripes
        d.arc([S * .3, S * (hy + .02 + k * .04), S * .7, S * (hy + .2 + k * .04)], 220, 320, fill=(200, 100, 20, 255), width=4)
    if swat:
        d.line([(S * .72, S * .52), (S * .94, S * .3)], fill=OUT, width=int(S * .13))
        d.line([(S * .72, S * .52), (S * .94, S * .3)], fill=OR, width=int(S * .08))
        d.ellipse([S * .86, S * .2, S * 1.0, S * .34], fill=LT, outline=OUT, width=4)
    d.arc([S * .04, S * .5, S * .34, S * .96], 90, 250, fill=OR, width=int(S * .08))                                # tail
    return _shrink(im, size)
