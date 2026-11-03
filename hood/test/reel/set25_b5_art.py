

# ---- set 25, batch 5: Two-Piece, Jump Out, Roll Up, Waffle Iron, Bazooka -----------------------------------------------

def drumstick(size=32):
    """A crispy fried chicken drumstick."""
    im, d, S = _big(size)
    OUT = (90, 45, 10, 255)
    d.line([(S * .62, S * .62), (S * .9, S * .9)], fill=(250, 245, 230, 255), width=int(S * .12))
    d.ellipse([S * .82, S * .82, S * .98, S * .98], fill=(250, 245, 230, 255), outline=OUT, width=3)
    d.ellipse([S * .08, S * .08, S * .7, S * .7], fill=(205, 130, 50, 255), outline=OUT, width=6)
    for x, y in ((.24, .26), (.44, .2), (.3, .46), (.52, .4)):
        d.ellipse([S * x, S * y, S * (x + .1), S * (y + .08)], fill=(230, 170, 80, 255))
    return _shrink(im, size)


def shrub(size=64, rustle=0):
    """A round hedge bush; rustle 1/2 jiggles the leaves (a different leaf pattern)."""
    import random
    im, d, S = _big(size)
    OUT = (20, 60, 20, 255)
    d.ellipse([S * .04, S * .2, S * .96, S * .96], fill=(50, 140, 50, 255), outline=OUT, width=7)
    r = random.Random(11 + rustle)
    for _ in range(16):
        x, y = r.uniform(.14, .82), r.uniform(.3, .82)
        d.ellipse([S * x, S * y, S * (x + .12), S * (y + .09)], fill=(80, 180, 70, 255), outline=(40, 110, 40, 255), width=3)
    return _shrink(im, size)


def roller_skate(size=64):
    """A white quad roller skate: high-top boot, pink wheels, a red toe stop, laces."""
    im, d, S = _big(size)
    OUT = (30, 20, 30, 255)
    d.polygon([(S * .2, S * .1), (S * .5, S * .1), (S * .52, S * .5), (S * .86, S * .56), (S * .88, S * .7), (S * .16, S * .7)],
              fill=(250, 250, 250, 255), outline=OUT)
    d.line([(S * .2, S * .1), (S * .5, S * .1), (S * .52, S * .5), (S * .86, S * .56), (S * .88, S * .7), (S * .16, S * .7), (S * .2, S * .1)], fill=OUT, width=6)
    for y in (.2, .3, .4):
        d.line([(S * .3, S * y), (S * .46, S * (y + .04))], fill=(240, 80, 150, 255), width=4)
    d.rectangle([S * .16, S * .7, S * .88, S * .76], fill=(170, 175, 185, 255), outline=OUT, width=4)
    for x in (.26, .74):
        d.ellipse([S * (x - .1), S * .72, S * (x + .1), S * .92], fill=(250, 100, 170, 255), outline=OUT, width=5)
    d.ellipse([S * .84, S * .64, S * .96, S * .76], fill=(220, 40, 40, 255), outline=OUT, width=4)
    return _shrink(im, size)


def waffle_iron(size=64, shut=False):
    """A waffle iron: open (two gridded plates, hinge at the back) or clamped shut with steam slits."""
    im, d, S = _big(size)
    OUT = (20, 20, 24, 255)
    if not shut:
        d.polygon([(S * .1, S * .66), (S * .9, S * .66), (S * .96, S * .9), (S * .04, S * .9)], fill=(60, 60, 66, 255), outline=OUT)
        d.polygon([(S * .14, S * .68), (S * .86, S * .68), (S * .9, S * .86), (S * .1, S * .86)], fill=(140, 140, 150, 255))
        d.polygon([(S * .1, S * .62), (S * .9, S * .62), (S * .82, S * .1), (S * .18, S * .1)], fill=(60, 60, 66, 255), outline=OUT)
        d.polygon([(S * .16, S * .58), (S * .84, S * .58), (S * .78, S * .16), (S * .22, S * .16)], fill=(140, 140, 150, 255))
        for k in range(1, 5):
            d.line([(S * (.2 + k * .12), S * .18), (S * (.18 + k * .13), S * .56)], fill=(90, 90, 100, 255), width=3)
            d.line([(S * .2, S * (.18 + k * .08)), (S * .8, S * (.18 + k * .08))], fill=(90, 90, 100, 255), width=3)
    else:
        d.rounded_rectangle([S * .06, S * .4, S * .94, S * .86], 14, fill=(60, 60, 66, 255), outline=OUT, width=7)
        d.line([(S * .06, S * .62), (S * .94, S * .62)], fill=(250, 200, 80, 255), width=5)
        d.rectangle([S * .4, S * .26, S * .6, S * .4], fill=(40, 40, 46, 255), outline=OUT, width=4)
    d.rectangle([S * .9, S * .6, S * .99, S * .68], fill=(200, 40, 40, 255), outline=OUT, width=3)                 # light
    return _shrink(im, size)


def gum_bubble(size=64):
    """A big shiny pink bubblegum bubble."""
    im, d, S = _big(size)
    d.ellipse([S * .06, S * .06, S * .94, S * .94], fill=(255, 140, 200, 235), outline=(200, 60, 140, 255), width=6)
    d.ellipse([S * .2, S * .16, S * .44, S * .34], fill=(255, 230, 245, 255))
    d.ellipse([S * .6, S * .66, S * .7, S * .74], fill=(255, 200, 230, 255))
    return _shrink(im, size)


def gum_splat(size=64):
    """Popped bubblegum stuck all over something: pink stringy splat."""
    import math
    im, d, S = _big(size)
    P = (255, 130, 195, 255)
    d.ellipse([S * .26, S * .3, S * .74, S * .7], fill=P)
    for k in range(9):
        a = k * 2 * math.pi / 9 + .3
        r = .4 if k % 2 else .3
        x, y = .5 + r * math.cos(a), .5 + r * .8 * math.sin(a)
        d.line([(S * .5, S * .5), (S * x, S * y)], fill=P, width=int(S * .07))
        d.ellipse([S * (x - .05), S * (y - .05), S * (x + .05), S * (y + .05)], fill=P)
    d.arc([S * .32, S * .34, S * .56, S * .5], 200, 300, fill=(255, 220, 240, 255), width=5)
    return _shrink(im, size)
