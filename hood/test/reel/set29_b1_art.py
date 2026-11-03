

# ---- set 29, batch 1: Blow Dryer, Snow Globe, Spinners, Throw Shade, Burned CD --------------------------------------------

def blow_dryer(size=64):
    """A hot pink salon blow dryer pointing right: round motor body, the nozzle, a handle down, the cord."""
    im, d, S = _big(size)
    OUT = (60, 10, 40, 255)
    d.rectangle([S * .44, S * .3, S * .9, S * .5], fill=(240, 90, 170, 255), outline=OUT, width=6)              # nozzle
    d.rectangle([S * .86, S * .26, S * .96, S * .54], fill=(60, 60, 66, 255), outline=OUT, width=4)
    d.ellipse([S * .1, S * .16, S * .52, S * .62], fill=(240, 90, 170, 255), outline=OUT, width=6)              # motor
    d.ellipse([S * .2, S * .26, S * .42, S * .52], fill=(60, 60, 66, 255))
    for k in range(4):
        d.line([(S * .23, S * (.3 + k * .06)), (S * .39, S * (.3 + k * .06))], fill=(120, 120, 130, 255), width=3)  # vent grille
    d.line([(S * .32, S * .58), (S * .4, S * .92)], fill=OUT, width=int(S * .13))                               # handle
    d.line([(S * .32, S * .58), (S * .4, S * .92)], fill=(240, 90, 170, 255), width=int(S * .09))
    d.rectangle([S * .34, S * .66, S * .4, S * .72], fill=(255, 255, 255, 255))                                  # switch
    d.line([(S * .4, S * .92), (S * .2, S * .98), (S * .04, S * .9)], fill=(60, 60, 66, 255), width=4)          # cord
    return _shrink(im, size)


def gust_slash(n=16):
    """A razor gust (alpha only): a thin curved crescent."""
    def f(x, y):
        r1 = ((x - 4) ** 2 + (y - 8) ** 2) ** .5
        return 1 if 8.5 < r1 < 10.5 and x > 6 else 0
    return _alpha(n, n, f)


def hood_snow_globe(size=64, storm=False):
    """A snow globe of the block on a black base: a little row of buildings and a streetlight inside; storm = snow,
    lightning and a little tornado swirling inside the glass."""
    im, d, S = _big(size)
    OUT = (20, 20, 30, 255)
    d.ellipse([S * .1, S * .04, S * .9, S * .84], fill=(200, 230, 255, 140) if not storm else (110, 120, 160, 200), outline=OUT, width=6)
    for x, h in ((.26, .3), (.4, .22), (.54, .32), (.66, .26)):                                                   # the block
        d.rectangle([S * x, S * (.66 - h), S * (x + .12), S * .66], fill=(150, 80, 60, 255), outline=OUT, width=3)
        d.rectangle([S * (x + .03), S * (.66 - h + .05), S * (x + .06), S * (.66 - h + .09)], fill=(250, 220, 90, 255))
    d.line([(S * .22, S * .66), (S * .22, S * .4)], fill=OUT, width=4)
    d.ellipse([S * .19, S * .36, S * .27, S * .42], fill=(255, 240, 150, 255))
    d.rectangle([S * .14, S * .64, S * .86, S * .72], fill=(240, 245, 250, 255))                                  # snow on the ground
    d.polygon([(S * .14, S * .76), (S * .86, S * .76), (S * .94, S * .98), (S * .06, S * .98)], fill=(30, 30, 36, 255), outline=OUT)
    import random
    r = random.Random(7)
    for _ in range(26 if storm else 10):
        x, y = r.uniform(.2, .8), r.uniform(.12, .62)
        d.ellipse([S * x, S * y, S * (x + .03), S * (y + .03)], fill=(255, 255, 255, 255))
    if storm:
        d.line([(S * .6, S * .14), (S * .54, S * .3), (S * .62, S * .3), (S * .56, S * .46)], fill=(255, 240, 80, 255), width=5)
        for k in range(3):
            d.arc([S * (.3 + k * .03), S * (.16 + k * .08), S * (.48 - k * .02), S * (.24 + k * .08)], 0, 300, fill=(230, 230, 240, 255), width=3)
    d.arc([S * .2, S * .1, S * .5, S * .4], 200, 270, fill=(255, 255, 255, 255), width=5)
    return _shrink(im, size)


def spinner_rim(size=64, angle=0):
    """A chrome spinner rim on a tire: the outer spinner blades rotated by `angle` degrees, sun-glint on the chrome."""
    im, d, S = _big(size)
    import math
    OUT = (20, 20, 25, 255)
    d.ellipse([S * .02, S * .02, S * .98, S * .98], fill=(30, 30, 34, 255), outline=OUT, width=6)               # tire
    d.ellipse([S * .14, S * .14, S * .86, S * .86], fill=(200, 205, 215, 255), outline=OUT, width=5)
    for k in range(5):                                                                                           # spinner blades
        a = math.radians(angle + k * 72)
        b = a + .5
        d.polygon([(S * .5, S * .5), (S * (.5 + .34 * math.cos(a)), S * (.5 + .34 * math.sin(a))), (S * (.5 + .34 * math.cos(b)), S * (.5 + .34 * math.sin(b)))],
                  fill=(235, 240, 250, 255), outline=(120, 125, 140, 255))
    d.ellipse([S * .42, S * .42, S * .58, S * .58], fill=(250, 210, 50, 255), outline=OUT, width=4)
    d.polygon([(S * .3, S * .22), (S * .36, S * .3), (S * .3, S * .38), (S * .24, S * .3)], fill=(255, 255, 255, 255))   # glint
    return _shrink(im, size)


def lampshade(size=64):
    """A fringed living-room lampshade: cream drum shade with a gold trim and little tassels hanging off the rim."""
    im, d, S = _big(size)
    OUT = (90, 60, 20, 255)
    d.polygon([(S * .28, S * .16), (S * .72, S * .16), (S * .9, S * .7), (S * .1, S * .7)], fill=(245, 230, 190, 255), outline=OUT)
    d.line([(S * .28, S * .16), (S * .72, S * .16), (S * .9, S * .7), (S * .1, S * .7), (S * .28, S * .16)], fill=OUT, width=6)
    d.line([(S * .12, S * .64), (S * .88, S * .64)], fill=(220, 170, 50, 255), width=6)
    d.line([(S * .24, S * .24), (S * .76, S * .24)], fill=(220, 170, 50, 255), width=5)
    for k in range(8):                                                                                           # tassels
        x = .14 + k * .103
        d.line([(S * x, S * .7), (S * x, S * .84)], fill=(220, 170, 50, 255), width=3)
        d.ellipse([S * (x - .025), S * .82, S * (x + .025), S * .88], fill=(200, 140, 40, 255))
    d.line([(S * .36, S * .2), (S * .26, S * .6)], fill=(255, 250, 230, 255), width=4)
    return _shrink(im, size)


def burned_cd(size=64):
    """A burned CD-R: rainbow-sheen silver disc with the hole, MIX hand-written on it in sharpie (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (60, 60, 70, 255)
    d.ellipse([S * .04, S * .04, S * .96, S * .96], fill=(215, 220, 230, 255), outline=OUT, width=5)
    for a0, col in ((200, (180, 230, 255, 255)), (250, (255, 200, 240, 255)), (300, (220, 255, 200, 255))):
        d.arc([S * .12, S * .12, S * .88, S * .88], a0, a0 + 40, fill=col, width=10)
    d.ellipse([S * .36, S * .36, S * .64, S * .64], fill=(240, 240, 245, 255), outline=OUT, width=3)
    d.ellipse([S * .44, S * .44, S * .56, S * .56], fill=(0, 0, 0, 0), outline=OUT, width=3)
    im = _shrink(im, size)
    return _texted(im, [("MIX", (32, 10)), ("COPY", (32, 46))], (20, 20, 25, 255), (215, 220, 230, 255))


def cd_boombox(size=64):
    """A silver CD boombox: two big speakers, the CD lid on top popped open, a little LCD."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.line([(S * .2, S * .2), (S * .3, S * .06), (S * .7, S * .06), (S * .8, S * .2)], fill=(80, 80, 90, 255), width=6)   # handle
    d.rounded_rectangle([S * .04, S * .2, S * .96, S * .86], 10, fill=(190, 195, 205, 255), outline=OUT, width=6)
    for x in (.08, .64):
        d.ellipse([S * x, S * .4, S * (x + .28), S * .8], fill=(40, 40, 46, 255), outline=OUT, width=4)
        d.ellipse([S * (x + .09), S * .53, S * (x + .19), S * .67], fill=(90, 90, 100, 255))
    d.ellipse([S * .38, S * .26, S * .62, S * .5], fill=(220, 225, 235, 255), outline=OUT, width=4)             # CD lid
    d.rectangle([S * .4, S * .58, S * .6, S * .7], fill=(120, 200, 140, 255), outline=OUT, width=3)             # LCD
    return _shrink(im, size)
