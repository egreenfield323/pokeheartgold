

# ---- set 20 redo, batch D1: Same Smoke, K9 Unit, Hide Out, Bling Beam, Mooch -------------------------------

def hoop_earrings(size=32):
    """A pair of big gold hoop earrings."""
    im, d, S = _big(size)
    OUT = (90, 60, 0, 255)
    for x in (.04, .52):
        d.ellipse([S * x, S * .2, S * (x + .44), S * .64], outline=OUT, width=12)
        d.ellipse([S * x, S * .2, S * (x + .44), S * .64], outline=(250, 200, 40, 255), width=7)
        d.arc([S * (x + .06), S * .26, S * (x + .2), S * .44], 160, 250, fill=(255, 250, 200, 255), width=4)
    return _shrink(im, size)


def rope_chain(size=64):
    """A thick gold rope chain coming off, swinging in a U."""
    im, d, S = _big(size)
    OUT = (90, 60, 0, 255)
    d.arc([S * .06, S * -.3, S * .94, S * .8], 20, 160, fill=OUT, width=18)
    d.arc([S * .06, S * -.3, S * .94, S * .8], 20, 160, fill=(250, 200, 40, 255), width=12)
    import math
    for k in range(14):                                                           # the rope twist
        a = math.radians(24 + k * 9.5)
        x, y = S * .5 + S * .44 * math.cos(a), S * .25 + S * .55 * math.sin(a)
        d.line([(x - 4, y - 5), (x + 4, y + 5)], fill=(255, 245, 190, 255), width=3)
    return _shrink(im, size)


def jelly_jar(size=64):
    """A tub of petroleum jelly, lid off, a big shiny scoop of it, a blue JELLY label - fight prep."""
    im, d, S = _big(size)
    OUT = (20, 30, 60, 255)
    d.rounded_rectangle([S * .2, S * .36, S * .8, S * .94], 10, fill=(235, 240, 250, 255), outline=OUT, width=7)
    d.rectangle([S * .2, S * .52, S * .8, S * .78], fill=(40, 90, 200, 255), outline=OUT, width=5)
    d.ellipse([S * .22, S * .26, S * .78, S * .44], fill=(250, 245, 215, 255), outline=OUT, width=6)
    d.ellipse([S * .38, S * .18, S * .6, S * .34], fill=(255, 250, 225, 255), outline=OUT, width=5)            # the scoop
    d.arc([S * .42, S * .2, S * .52, S * .28], 180, 300, fill=(255, 255, 255, 255), width=4)
    im = _shrink(im, size)
    return _texted(im, [("JELLY", (32, 37))], (255, 255, 255, 255), (20, 40, 100, 255))


def k9_dog(size=64, barking=False):
    """A police German shepherd facing left in a blue K9 vest - trotting, or sat up barking with its mouth open."""
    im, d, S = _big(size)
    OUT = (30, 20, 10, 255)
    TAN, BLK = (200, 140, 70, 255), (45, 35, 30, 255)
    if barking:
        d.ellipse([S * .4, S * .4, S * .86, S * .9], fill=TAN, outline=OUT, width=7)                               # sat body
        d.rectangle([S * .44, S * .46, S * .8, S * .66], fill=(40, 70, 170, 255), outline=OUT, width=5)           # vest
        d.line([(S * .5, S * .8), (S * .5, S * .96)], fill=TAN, width=12)
        head = (.28, .2)
    else:
        d.ellipse([S * .3, S * .4, S * .92, S * .72], fill=TAN, outline=OUT, width=7)
        d.rectangle([S * .4, S * .42, S * .76, S * .62], fill=(40, 70, 170, 255), outline=OUT, width=5)
        for x in (.36, .48, .76, .86):
            d.line([(S * x, S * .68), (S * (x - .02), S * .94)], fill=TAN, width=10)
        d.line([(S * .9, S * .5), (S * .99, S * .36)], fill=BLK, width=9)                                          # tail
        head = (.12, .3)
    hx, hy = head
    d.ellipse([S * hx, S * hy, S * (hx + .3), S * (hy + .26)], fill=TAN, outline=OUT, width=7)
    d.polygon([(S * (hx + .16), S * (hy + .02)), (S * (hx + .2), S * (hy - .14)), (S * (hx + .28), S * (hy + .06))], fill=BLK, outline=OUT)
    d.polygon([(S * (hx + .02), S * (hy + .1)), (S * (hx - .1), S * (hy + .16)), (S * (hx + .02), S * (hy + .22))], fill=TAN, outline=OUT)  # snout
    d.ellipse([S * (hx - .12), S * (hy + .12), S * (hx - .06), S * (hy + .18)], fill=OUT)
    d.ellipse([S * (hx + .08), S * (hy + .08), S * (hx + .13), S * (hy + .13)], fill=OUT)
    if barking:
        d.polygon([(S * (hx - .08), S * (hy + .2)), (S * (hx + .06), S * (hy + .22)), (S * (hx - .04), S * (hy + .32))], fill=(200, 40, 50, 255), outline=OUT)
    im = _shrink(im, size)
    return _texted(im, [("K9", (round(size * (.62 if barking else .58)), round(size * (.5 if barking else .46))))], (255, 255, 255, 255), (20, 30, 90, 255))


def sandwich(size=32):
    """A fat sub sandwich: bread, lettuce, tomato, cheese."""
    im, d, S = _big(size)
    OUT = (80, 45, 10, 255)
    d.rounded_rectangle([S * .04, S * .52, S * .96, S * .72], 12, fill=(220, 160, 80, 255), outline=OUT, width=5)
    d.rectangle([S * .06, S * .44, S * .94, S * .54], fill=(90, 190, 60, 255))
    d.rectangle([S * .08, S * .38, S * .92, S * .46], fill=(250, 210, 50, 255))
    for x in (.16, .42, .68):
        d.ellipse([S * x, S * .32, S * (x + .2), S * .42], fill=(220, 50, 40, 255), outline=OUT, width=3)
    d.rounded_rectangle([S * .04, S * .16, S * .96, S * .36], 12, fill=(230, 175, 90, 255), outline=OUT, width=5)
    for x in (.2, .45, .7):
        d.line([(S * x, S * .2), (S * (x + .08), S * .26)], fill=(255, 225, 160, 255), width=3)
    return _shrink(im, size)


def tiny_cactus(size=32, fallen=False):
    """A tiny potted cactus (way too small to hide behind) - or tipped over on its side."""
    im, d, S = _big(size)
    OUT = (20, 50, 20, 255)
    d.polygon([(S * .26, S * .66), (S * .74, S * .66), (S * .66, S * .96), (S * .34, S * .96)], fill=(200, 100, 50, 255), outline=OUT)
    d.rounded_rectangle([S * .38, S * .14, S * .62, S * .7], 12, fill=(70, 170, 70, 255), outline=OUT, width=5)
    d.rounded_rectangle([S * .16, S * .34, S * .3, S * .56], 8, fill=(70, 170, 70, 255), outline=OUT, width=4)
    d.line([(S * .28, S * .5), (S * .4, S * .5)], fill=(70, 170, 70, 255), width=8)
    for x, y in ((.44, .3), (.56, .42), (.46, .56), (.2, .4)):
        d.line([(S * x, S * y), (S * (x + .04), S * (y - .04))], fill=(255, 255, 220, 255), width=3)
    d.ellipse([S * .46, S * .06, S * .56, S * .16], fill=(250, 100, 160, 255), outline=OUT, width=3)            # a flower
    im = _shrink(im, size)
    return im.rotate(80, resample=Image.NEAREST, center=(size * .5, size * .9)) if fallen else im


def big_chain(size=64):
    """An iced-out chain: a heavy gold rope with a huge diamond-crusted $ medallion."""
    im, d, S = _big(size)
    OUT = (90, 60, 0, 255)
    d.arc([S * .08, S * -.36, S * .92, S * .5], 25, 155, fill=OUT, width=14)
    d.arc([S * .08, S * -.36, S * .92, S * .5], 25, 155, fill=(250, 200, 40, 255), width=9)
    d.ellipse([S * .26, S * .36, S * .74, S * .84], fill=(250, 200, 40, 255), outline=OUT, width=8)
    d.ellipse([S * .32, S * .42, S * .68, S * .78], fill=(200, 240, 255, 255), outline=(120, 160, 200, 255), width=4)
    for k in range(10):                                                           # the ice
        x, y = .36 + (k * 37 % 28) / 100, .46 + (k * 23 % 28) / 100
        d.ellipse([S * x, S * y, S * (x + .04), S * (y + .04)], fill=(255, 255, 255, 255))
    im = _shrink(im, size)
    return _texted(im, [("$", (32, 26))], (250, 200, 40, 255), (90, 60, 0, 255), font=GLYPHS)


def food_tray(size=64, burger=True):
    """A red fast-food tray: a carton of fries, a soda, and a burger (or just the empty wrapper once it's gone)."""
    im, d, S = _big(size)
    OUT = (40, 10, 10, 255)
    d.polygon([(S * .02, S * .7), (S * .98, S * .7), (S * .9, S * .86), (S * .1, S * .86)], fill=(200, 40, 40, 255), outline=OUT)
    d.rectangle([S * .72, S * .3, S * .9, S * .7], fill=(250, 250, 250, 255), outline=OUT, width=5)            # soda
    d.line([(S * .82, S * .3), (S * .86, S * .14)], fill=(220, 40, 40, 255), width=6)
    for k in range(5):                                                            # fries
        x = .1 + k * .05
        d.rectangle([S * x, S * .3, S * (x + .04), S * .5], fill=(250, 210, 60, 255), outline=OUT, width=2)
    d.polygon([(S * .06, S * .44), (S * .38, S * .44), (S * .34, S * .7), (S * .1, S * .7)], fill=(220, 40, 40, 255), outline=OUT)
    if burger:
        d.pieslice([S * .38, S * .3, S * .7, S * .62], 180, 360, fill=(220, 150, 60, 255), outline=OUT, width=5)
        d.rectangle([S * .38, S * .46, S * .7, S * .52], fill=(110, 60, 30, 255))
        d.rectangle([S * .38, S * .52, S * .7, S * .56], fill=(90, 190, 60, 255))
        d.rounded_rectangle([S * .38, S * .56, S * .7, S * .68], 6, fill=(220, 150, 60, 255), outline=OUT, width=5)
    else:
        d.polygon([(S * .4, S * .66), (S * .5, S * .56), (S * .62, S * .62), (S * .68, S * .68)], fill=(240, 230, 210, 255), outline=OUT)
    return _shrink(im, size)


def french_fry(size=32):
    """A single golden fry."""
    im, d, S = _big(size)
    OUT = (120, 70, 0, 255)
    d.rounded_rectangle([S * .4, S * .06, S * .6, S * .94], 6, fill=(250, 210, 60, 255), outline=OUT, width=6)
    d.line([(S * .46, S * .12), (S * .46, S * .5)], fill=(255, 245, 180, 255), width=4)
    return _shrink(im, size)


def burger(size=32):
    """A whole burger: sesame bun, lettuce, cheese, patty."""
    im, d, S = _big(size)
    OUT = (60, 30, 10, 255)
    d.pieslice([S * .06, S * .14, S * .94, S * .66], 180, 360, fill=(220, 150, 60, 255), outline=OUT, width=6)
    for x, y in ((.3, .26), (.5, .22), (.66, .3)):
        d.ellipse([S * x, S * y, S * (x + .06), S * (y + .04)], fill=(255, 245, 210, 255))
    d.rectangle([S * .06, S * .4, S * .94, S * .48], fill=(90, 190, 60, 255))
    d.polygon([(S * .06, S * .48), (S * .94, S * .48), (S * .8, S * .56), (S * .2, S * .56)], fill=(250, 200, 40, 255))
    d.rounded_rectangle([S * .08, S * .54, S * .92, S * .68], 6, fill=(110, 60, 30, 255), outline=OUT, width=4)
    d.rounded_rectangle([S * .06, S * .68, S * .94, S * .84], 8, fill=(220, 150, 60, 255), outline=OUT, width=5)
    return _shrink(im, size)
