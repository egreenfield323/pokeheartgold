

# ---- set 26, batch 1 (INSANE): Live Wire, Fire Cart, Wrecker, Headbanger, Super Soaker -------------------------------

def utility_pole(size=64):
    """A wooden utility pole with a crossbar, a grey transformer can, and one power line snapped and hanging down."""
    im, d, S = _big(size)
    OUT = (30, 20, 10, 255)
    d.rectangle([S * .44, S * .04, S * .54, S * .98], fill=(130, 90, 50, 255), outline=OUT, width=5)
    d.rectangle([S * .14, S * .12, S * .86, S * .18], fill=(130, 90, 50, 255), outline=OUT, width=4)
    for x in (.18, .82):
        d.rectangle([S * (x - .02), S * .06, S * (x + .02), S * .12], fill=(200, 230, 240, 255), outline=OUT, width=2)
    d.rounded_rectangle([S * .56, S * .24, S * .76, S * .46], 6, fill=(150, 155, 165, 255), outline=OUT, width=5)
    d.line([(S * .82, S * .1), (S * .9, S * .4), (S * .84, S * .7), (S * .92, S * .92)], fill=(30, 30, 34, 255), width=6)   # the snapped line
    d.line([(S * .18, S * .1), (S * .02, S * .2)], fill=(30, 30, 34, 255), width=5)
    return _shrink(im, size)


def wire_end(size=32):
    """The sparking end of a snapped power line."""
    im, d, S = _big(size)
    d.line([(S * .1, S * .1), (S * .5, S * .5)], fill=(30, 30, 34, 255), width=int(S * .12))
    for a, b in (((.5, .5), (.86, .3)), ((.5, .5), (.9, .62)), ((.5, .5), (.66, .9)), ((.5, .5), (.3, .82))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(255, 250, 120, 255), width=5)
    d.ellipse([S * .4, S * .4, S * .6, S * .6], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def zig_bolt(n=16):
    """A short zig-zag lightning bolt (alpha only)."""
    def f(x, y):
        xx = 8 + (3 if (y // 4) % 2 else -3) * (1 - abs((y % 4) - 2) / 2)
        return 1 if abs(x - xx) < 1.6 and 1 < y < 15 else 0
    return _alpha(n, n, f)


def grocery_cart(size=64):
    """A chrome shopping cart facing right, the red handle at the back, four casters."""
    im, d, S = _big(size)
    OUT = (40, 40, 46, 255)
    C = (200, 205, 215, 255)
    d.polygon([(S * .12, S * .26), (S * .9, S * .3), (S * .8, S * .66), (S * .2, S * .66)], fill=(220, 225, 235, 120), outline=OUT)
    for k in range(6):
        x = .16 + k * .13
        d.line([(S * x, S * .28), (S * (x + .02), S * .66)], fill=C, width=4)
    for k in range(3):
        y = .34 + k * .1
        d.line([(S * .14, S * y), (S * .88, S * (y + .02))], fill=C, width=4)
    d.line([(S * .12, S * .26), (S * .9, S * .3), (S * .8, S * .66), (S * .2, S * .66), (S * .12, S * .26)], fill=OUT, width=6)
    d.line([(S * .12, S * .26), (S * .04, S * .14)], fill=OUT, width=7)
    d.line([(S * .0, S * .14), (S * .1, S * .14)], fill=(220, 30, 30, 255), width=9)                                # handle
    d.line([(S * .2, S * .66), (S * .26, S * .82), (S * .82, S * .82), (S * .8, S * .66)], fill=OUT, width=6)
    for x in (.28, .78):
        d.ellipse([S * (x - .06), S * .82, S * (x + .06), S * .94], fill=(30, 30, 34, 255), outline=OUT, width=3)
    return _shrink(im, size)


def demo_ball(size=64):
    """A huge black wrecking ball on its chain (the chain runs up off the top)."""
    im, d, S = _big(size)
    OUT = (5, 5, 8, 255)
    for k in range(5):
        y = k * .08
        d.ellipse([S * .46, S * y, S * .54, S * (y + .1)], outline=(110, 110, 120, 255), width=5)
    d.rectangle([S * .44, S * .38, S * .56, S * .46], fill=(70, 70, 76, 255), outline=OUT, width=4)
    d.ellipse([S * .14, S * .42, S * .86, S * .98], fill=(40, 40, 46, 255), outline=OUT, width=7)
    d.arc([S * .22, S * .5, S * .6, S * .8], 200, 290, fill=(140, 140, 150, 255), width=8)
    return _shrink(im, size)


def amp_stack(size=64):
    """A tall guitar amp stack: two black speaker cabinets, grille cloth, a gold logo plate, knobs on the head."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rectangle([S * .18, S * .04, S * .82, S * .2], fill=(30, 30, 34, 255), outline=OUT, width=6)
    for k in range(5):
        d.ellipse([S * (.26 + k * .11), S * .1, S * (.32 + k * .11), S * .16], fill=(230, 190, 60, 255))
    for y0 in (.2, .58):
        d.rectangle([S * .14, S * y0, S * .86, S * (y0 + .38)], fill=(30, 30, 34, 255), outline=OUT, width=6)
        d.rectangle([S * .2, S * (y0 + .05), S * .8, S * (y0 + .33)], fill=(70, 70, 76, 255))
        for k in range(6):
            d.line([(S * .2, S * (y0 + .08 + k * .045)), (S * .8, S * (y0 + .08 + k * .045))], fill=(55, 55, 60, 255), width=2)
    d.rectangle([S * .4, S * .24, S * .6, S * .3], fill=(230, 190, 60, 255))
    return _shrink(im, size)


def mega_soaker(size=64, pumped=False):
    """A giant neon water gun: green body, big orange water tank on top, the pump handle under the barrel (slid back
    when pumped)."""
    im, d, S = _big(size)
    OUT = (20, 30, 10, 255)
    d.rounded_rectangle([S * .14, S * .4, S * .84, S * .58], 10, fill=(80, 210, 70, 255), outline=OUT, width=6)
    d.rectangle([S * .84, S * .44, S * .98, S * .54], fill=(250, 230, 40, 255), outline=OUT, width=4)             # nozzle
    d.rounded_rectangle([S * .24, S * .12, S * .66, S * .42], 14, fill=(250, 130, 30, 220), outline=OUT, width=6)  # tank
    d.line([(S * .3, S * .18), (S * .3, S * .36)], fill=(255, 220, 160, 255), width=5)
    d.polygon([(S * .2, S * .58), (S * .34, S * .58), (S * .28, S * .86), (S * .14, S * .86)], fill=(80, 210, 70, 255), outline=OUT)
    px = .5 if pumped else .64
    d.rounded_rectangle([S * px, S * .58, S * (px + .2), S * .7], 6, fill=(250, 230, 40, 255), outline=OUT, width=5)   # pump
    return _shrink(im, size)
