

# ---- set 25, batch 2: Spoon Bend, Pinched, Lights Out, Palm Reader, Jackhammer ---------------------------------------

def bent_spoon(size=64, bent=False):
    """A shiny steel spoon standing up - or bent over in the middle."""
    im, d, S = _big(size)
    OUT = (40, 45, 60, 255)
    M, ML = (200, 205, 220, 255), (250, 252, 255, 255)
    if not bent:
        d.ellipse([S * .38, S * .06, S * .62, S * .38], fill=M, outline=OUT, width=6)
        d.line([(S * .5, S * .36), (S * .5, S * .94)], fill=OUT, width=int(S * .1))
        d.line([(S * .5, S * .36), (S * .5, S * .94)], fill=M, width=int(S * .06))
        d.line([(S * .45, S * .12), (S * .45, S * .28)], fill=ML, width=4)
    else:
        d.line([(S * .5, S * .94), (S * .5, S * .52), (S * .72, S * .36)], fill=OUT, width=int(S * .1))
        d.line([(S * .5, S * .94), (S * .5, S * .52), (S * .72, S * .36)], fill=M, width=int(S * .06))
        d.ellipse([S * .66, S * .18, S * .94, S * .42], fill=M, outline=OUT, width=6)
    return _shrink(im, size)


def bent_fork(size=64, bent=False):
    """A steel fork standing up - or bent over."""
    im, d, S = _big(size)
    OUT = (40, 45, 60, 255)
    M = (200, 205, 220, 255)
    pts = [(S * .5, S * .94), (S * .5, S * .4)] if not bent else [(S * .5, S * .94), (S * .5, S * .56), (S * .72, S * .42)]
    d.line(pts, fill=OUT, width=int(S * .1))
    d.line(pts, fill=M, width=int(S * .06))
    hx, hy = pts[-1]
    for k in range(4):
        if not bent:
            x = hx + (k - 1.5) * S * .05
            d.line([(x, hy), (x, hy - S * .3)], fill=OUT, width=7)
            d.line([(x, hy), (x, hy - S * .3)], fill=M, width=3)
        else:
            y = hy + (k - 1.5) * S * .05
            d.line([(hx, y), (hx + S * .24, y - S * .1)], fill=OUT, width=7)
            d.line([(hx, y), (hx + S * .24, y - S * .1)], fill=M, width=3)
    return _shrink(im, size)


def stop_post(size=64, bent=False):
    """A STOP sign on its pole (shown at 1:1) - or the pole bent right over, the sign hanging upside-down-ish
    (bent version has no readable text)."""
    import math
    im, d, S = _big(size)
    OUT = (20, 20, 24, 255)
    if not bent:
        d.rectangle([S * .47, S * .4, S * .53, S * .98], fill=(160, 165, 175, 255), outline=OUT, width=3)
        cx, cy, r = S * .5, S * .26, S * .24
    else:
        d.line([(S * .5, S * .98), (S * .5, S * .62), (S * .7, S * .5)], fill=OUT, width=int(S * .08))
        d.line([(S * .5, S * .98), (S * .5, S * .62), (S * .7, S * .5)], fill=(160, 165, 175, 255), width=int(S * .05))
        cx, cy, r = S * .78, S * .66, S * .2
    pts = [(cx + r * math.cos(math.pi / 8 + k * math.pi / 4), cy + r * math.sin(math.pi / 8 + k * math.pi / 4)) for k in range(8)]
    _outline_poly(d, pts, (210, 30, 30, 255), (250, 250, 250, 255), 6)
    im = _shrink(im, size)
    if not bent:
        _texted(im, [("STOP", (32, 14))], (255, 255, 255, 255), (210, 30, 30, 255))
    return im


def clothespin(size=64):
    """A wooden clothespin, jaws to the left, the steel spring in the middle."""
    im, d, S = _big(size)
    OUT = (70, 40, 10, 255)
    W = (225, 185, 120, 255)
    d.polygon([(S * .06, S * .4), (S * .94, S * .3), (S * .94, S * .44), (S * .12, S * .5)], fill=W, outline=OUT)
    d.polygon([(S * .06, S * .6), (S * .94, S * .7), (S * .94, S * .56), (S * .12, S * .5)], fill=(210, 170, 105, 255), outline=OUT)
    d.line([(S * .06, S * .4), (S * .94, S * .3), (S * .94, S * .44), (S * .12, S * .5), (S * .06, S * .4)], fill=OUT, width=5)
    d.line([(S * .06, S * .6), (S * .94, S * .7), (S * .94, S * .56), (S * .12, S * .5), (S * .06, S * .6)], fill=OUT, width=5)
    d.ellipse([S * .5, S * .4, S * .66, S * .6], outline=(170, 175, 185, 255), width=6)
    return _shrink(im, size)


def floor_lamp(size=64, on=True):
    """A floor lamp with a drum shade, glowing - or off."""
    im, d, S = _big(size)
    OUT = (30, 25, 20, 255)
    if on:
        d.polygon([(S * .3, S * .36), (S * .7, S * .36), (S * .9, S * .7), (S * .1, S * .7)], fill=(255, 240, 160, 110))
    d.polygon([(S * .32, S * .08), (S * .68, S * .08), (S * .76, S * .36), (S * .24, S * .36)],
              fill=(255, 230, 140, 255) if on else (170, 150, 110, 255), outline=OUT)
    d.line([(S * .32, S * .08), (S * .68, S * .08), (S * .76, S * .36), (S * .24, S * .36), (S * .32, S * .08)], fill=OUT, width=5)
    d.line([(S * .5, S * .36), (S * .5, S * .92)], fill=(90, 80, 70, 255), width=6)
    d.ellipse([S * .34, S * .88, S * .66, S * .98], fill=(90, 80, 70, 255), outline=OUT, width=4)
    return _shrink(im, size)


def breaker_box(size=64, off=False):
    """An open circuit breaker panel: grey box, two rows of switches and the big main lever - up (on) or down (off)."""
    im, d, S = _big(size)
    OUT = (20, 20, 24, 255)
    d.rectangle([S * .14, S * .06, S * .86, S * .94], fill=(170, 175, 185, 255), outline=OUT, width=7)
    d.rectangle([S * .22, S * .14, S * .78, S * .86], fill=(60, 62, 70, 255))
    for r in range(4):
        for c in range(2):
            x, y = .3 + c * .26, .4 + r * .12
            d.rectangle([S * x, S * y, S * (x + .16), S * (y + .08)], fill=(30, 30, 34, 255), outline=(120, 120, 130, 255), width=3)
            d.rectangle([S * (x + (.02 if off else .1)), S * (y + .02), S * (x + (.06 if off else .14)), S * (y + .06)], fill=(240, 240, 245, 255))
    d.rectangle([S * .4, S * .16, S * .6, S * .34], fill=(30, 30, 34, 255), outline=(200, 40, 40, 255), width=4)
    d.rectangle([S * .44, S * (.26 if off else .18), S * .56, S * (.32 if off else .24)], fill=(220, 40, 40, 255))
    return _shrink(im, size)


def psychic_sign(size=64):
    """A neon storefront sign: a pink hand-with-eye outline and PSYCHIC in glowing purple tubes (shown at 1:1)."""
    im, d, S = _big(size)
    d.rounded_rectangle([S * .04, S * .14, S * .96, S * .86], 10, fill=(25, 15, 40, 255), outline=(90, 60, 120, 255), width=6)
    d.ellipse([S * .38, S * .2, S * .62, S * .44], outline=(255, 90, 200, 255), width=6)
    d.ellipse([S * .46, S * .28, S * .54, S * .36], fill=(255, 90, 200, 255))
    im = _shrink(im, size)
    return _texted(im, [("PSYCHIC", (32, 33))], (230, 170, 255, 255), (120, 40, 170, 255))


def seer_ball(size=64, vision=0):
    """A crystal ball on a gold stand; vision 0 = swirling purple mist, 1 = thicker mist, 2 = a red target (the foe
    locked in)."""
    im, d, S = _big(size)
    OUT = (40, 20, 60, 255)
    d.polygon([(S * .3, S * .78), (S * .7, S * .78), (S * .78, S * .94), (S * .22, S * .94)], fill=(220, 170, 50, 255), outline=OUT)
    d.ellipse([S * .18, S * .14, S * .82, S * .8], fill=(170, 140, 240, 220), outline=OUT, width=7)
    if vision < 2:
        for k in range(2 + vision * 2):
            d.arc([S * (.28 + k * .04), S * (.26 + k * .05), S * (.72 - k * .03), S * (.68 - k * .04)], k * 70, k * 70 + 180,
                  fill=(255, 255, 255, 200), width=6)
    else:
        for r, c in ((.22, (230, 30, 30)), (.14, (255, 255, 255)), (.07, (230, 30, 30))):
            d.ellipse([S * (.5 - r), S * (.47 - r), S * (.5 + r), S * (.47 + r)], fill=c + (255,))
    d.arc([S * .26, S * .2, S * .5, S * .44], 200, 260, fill=(255, 255, 255, 255), width=6)
    return _shrink(im, size)


def jackhammer(size=64):
    """A pneumatic jackhammer: T handles, the yellow body, the steel chisel bit at the bottom."""
    im, d, S = _big(size)
    OUT = (20, 15, 5, 255)
    d.rectangle([S * .14, S * .06, S * .86, S * .16], fill=(40, 40, 46, 255), outline=OUT, width=5)
    d.rounded_rectangle([S * .34, S * .14, S * .66, S * .62], 10, fill=(250, 200, 30, 255), outline=OUT, width=7)
    d.rectangle([S * .4, S * .24, S * .6, S * .32], fill=(40, 40, 46, 255))
    d.rectangle([S * .44, S * .62, S * .56, S * .9], fill=(180, 185, 195, 255), outline=OUT, width=5)
    d.polygon([(S * .44, S * .9), (S * .56, S * .9), (S * .5, S * .98)], fill=(180, 185, 195, 255), outline=OUT)
    d.line([(S * .66, S * .3), (S * .9, S * .4)], fill=(40, 40, 46, 255), width=6)                                  # air hose
    return _shrink(im, size)


def apt_window(size=64, lit=False):
    """An apartment window at dawn: dark panes - or the light snapped on (yellow), blinds half up."""
    im, d, S = _big(size)
    OUT = (40, 30, 30, 255)
    d.rectangle([S * .1, S * .08, S * .9, S * .92], fill=(170, 90, 70, 255), outline=OUT, width=7)                 # brick
    glass = (255, 230, 120, 255) if lit else (40, 50, 80, 255)
    d.rectangle([S * .22, S * .2, S * .78, S * .78], fill=glass, outline=(240, 240, 240, 255), width=7)
    d.line([(S * .5, S * .2), (S * .5, S * .78)], fill=(240, 240, 240, 255), width=6)
    d.rectangle([S * .24, S * .22, S * .76, S * .38], fill=(230, 225, 210, 255))                                  # blinds
    for y in (.26, .3, .34):
        d.line([(S * .24, S * y), (S * .76, S * y)], fill=(190, 185, 170, 255), width=2)
    d.rectangle([S * .18, S * .78, S * .82, S * .84], fill=(200, 200, 205, 255), outline=OUT, width=4)
    return _shrink(im, size)
