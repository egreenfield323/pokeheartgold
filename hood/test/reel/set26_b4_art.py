

# ---- set 26, batch 4: Pillow Fight, Bad Sushi, Blindside, Uppercut, Sandbag ---------------------------------------------

def fluffy_pillow(size=64):
    """A big white bed pillow with puffy corners and a seam."""
    im, d, S = _big(size)
    OUT = (110, 110, 130, 255)
    d.rounded_rectangle([S * .06, S * .24, S * .94, S * .76], 30, fill=(250, 250, 255, 255), outline=OUT, width=6)
    for x, y in ((.06, .24), (.94, .24), (.06, .76), (.94, .76)):
        d.ellipse([S * (x - .06), S * (y - .06), S * (x + .06), S * (y + .06)], fill=(250, 250, 255, 255), outline=OUT, width=4)
    d.line([(S * .2, S * .5), (S * .8, S * .5)], fill=(210, 210, 225, 255), width=4)
    d.arc([S * .14, S * .3, S * .5, S * .48], 200, 300, fill=(255, 255, 255, 255), width=5)
    return _shrink(im, size)


def sushi_tray(size=64):
    """A gas-station sushi tray: clear plastic lid, six rolls, a fake grass divider, a little wasabi - kind of grey."""
    im, d, S = _big(size)
    OUT = (40, 40, 50, 255)
    d.rounded_rectangle([S * .04, S * .36, S * .96, S * .82], 8, fill=(30, 30, 34, 255), outline=OUT, width=5)
    for k in range(6):
        x = .12 + (k % 3) * .2
        y = .42 + (k // 3) * .18
        d.ellipse([S * x, S * y, S * (x + .16), S * (y + .14)], fill=(40, 50, 40, 255), outline=OUT, width=3)
        d.ellipse([S * (x + .03), S * (y + .03), S * (x + .13), S * (y + .11)], fill=(235, 230, 220, 255))
        d.ellipse([S * (x + .06), S * (y + .05), S * (x + .1), S * (y + .09)], fill=(230, 120, 100, 255))
    d.polygon([(S * .74, S * .48), (S * .9, S * .48), (S * .82, S * .76)], fill=(60, 180, 70, 255))               # plastic grass
    d.ellipse([S * .76, S * .7, S * .88, S * .78], fill=(140, 190, 60, 255))                                       # wasabi
    d.rounded_rectangle([S * .02, S * .26, S * .98, S * .4], 6, fill=(220, 235, 245, 150), outline=OUT, width=4)   # lid
    return _shrink(im, size)


def sushi_roll(size=32):
    """One maki roll, a little off-color."""
    im, d, S = _big(size)
    OUT = (30, 30, 30, 255)
    d.ellipse([S * .1, S * .1, S * .9, S * .9], fill=(40, 50, 40, 255), outline=OUT, width=6)
    d.ellipse([S * .22, S * .22, S * .78, S * .78], fill=(225, 225, 205, 255))
    d.ellipse([S * .38, S * .38, S * .62, S * .62], fill=(200, 140, 110, 255))
    return _shrink(im, size)


def sneak_box(size=64, alert=False):
    """A cardboard box sneaking along (someone's under it) - with a red ! over it when spotted."""
    im, d, S = _big(size)
    OUT = (90, 60, 20, 255)
    d.rectangle([S * .12, S * .4, S * .88, S * .9], fill=(205, 160, 100, 255), outline=OUT, width=6)
    d.polygon([(S * .12, S * .4), (S * .88, S * .4), (S * .8, S * .3), (S * .2, S * .3)], fill=(185, 140, 85, 255), outline=OUT)
    d.rectangle([S * .44, S * .4, S * .56, S * .9], fill=(230, 200, 150, 255))                                     # tape
    d.rectangle([S * .3, S * .56, S * .44, S * .62], fill=(40, 30, 20, 255))                                       # peep slit
    if alert:
        d.rectangle([S * .46, S * .0, S * .56, S * .18], fill=(230, 30, 30, 255))
        d.rectangle([S * .46, S * .21, S * .56, S * .27], fill=(230, 30, 30, 255))
    return _shrink(im, size)


def upper_glove(size=64):
    """A red boxing glove punching straight up, white cuff at the bottom."""
    im, d, S = _big(size)
    OUT = (60, 0, 0, 255)
    d.rounded_rectangle([S * .32, S * .7, S * .68, S * .94], 8, fill=(250, 250, 250, 255), outline=OUT, width=6)
    d.ellipse([S * .18, S * .06, S * .82, S * .76], fill=(220, 30, 30, 255), outline=OUT, width=7)
    d.ellipse([S * .08, S * .36, S * .38, S * .64], fill=(200, 25, 25, 255), outline=OUT, width=6)
    d.arc([S * .26, S * .12, S * .6, S * .5], 200, 300, fill=(255, 140, 130, 255), width=7)
    return _shrink(im, size)


def sandbag(size=32):
    """A tan burlap sandbag, tied."""
    im, d, S = _big(size)
    OUT = (90, 70, 30, 255)
    d.rounded_rectangle([S * .06, S * .3, S * .94, S * .78], 14, fill=(215, 190, 130, 255), outline=OUT, width=5)
    for x in (.26, .5, .74):
        d.line([(S * x, S * .34), (S * (x + .04), S * .74)], fill=(190, 160, 100, 255), width=3)
    d.ellipse([S * .82, S * .44, S * .96, S * .62], fill=(190, 160, 100, 255), outline=OUT, width=3)
    return _shrink(im, size)
