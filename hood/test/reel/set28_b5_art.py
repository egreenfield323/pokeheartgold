

# ---- set 28, batch 5: Flip Script, Cosplay, Guard Swarm, Honey Heal, Edge Up ---------------------------------------------

def script_page(size=64, flipped=False):
    """A movie script page: SCRIPT at the top, ATK over DEF in big type - swapped (DEF over ATK) when flipped
    (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 40, 50, 255)
    d.rectangle([S * .14, S * .04, S * .86, S * .96], fill=(250, 250, 240, 255), outline=OUT, width=6)
    for y in (.62, .7, .78, .86):
        d.line([(S * .24, S * y), (S * .76, S * y)], fill=(180, 180, 190, 255), width=3)
    for y in (.1, .2):
        d.ellipse([S * .18, S * y, S * .24, S * (y + .06)], fill=(120, 120, 130, 255))                           # binder holes
    im = _shrink(im, size)
    a, b = ("DEF", "ATK") if flipped else ("ATK", "DEF")
    return _texted(im, [("SCRIPT", (34, 6)), (a, (34, 17)), (b, (34, 27))], (200, 30, 30, 255) if flipped else (30, 30, 40, 255), (250, 250, 240, 255))


def costume_bag(size=64):
    """A cheap Halloween costume in its plastic bag: a hanger hook up top, COSTUME across, a goofy mask pictured
    (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (30, 30, 40, 255)
    d.arc([S * .4, S * .0, S * .6, S * .16], 180, 360, fill=(160, 160, 170, 255), width=5)
    d.rectangle([S * .12, S * .1, S * .88, S * .96], fill=(240, 120, 30, 230), outline=OUT, width=6)
    d.ellipse([S * .3, S * .4, S * .7, S * .86], fill=(120, 200, 90, 255), outline=OUT, width=5)                  # the mask pic
    for x in (.38, .54):
        d.ellipse([S * x, S * .54, S * (x + .08), S * .62], fill=OUT)
    d.arc([S * .4, S * .62, S * .6, S * .76], 20, 160, fill=OUT, width=4)
    im = _shrink(im, size)
    return _texted(im, [("COSTUME", (32, 12))], (255, 255, 255, 255), (60, 20, 0, 255))


def cheap_mask(size=64):
    """A cheap rubber monster mask: lime green, googly eyes, a lopsided grin, the elastic string."""
    im, d, S = _big(size)
    OUT = (20, 40, 10, 255)
    d.line([(S * .06, S * .44), (S * .94, S * .44)], fill=(240, 240, 240, 255), width=3)
    d.ellipse([S * .16, S * .1, S * .84, S * .92], fill=(130, 210, 80, 255), outline=OUT, width=6)
    for x, r in ((.28, .12), (.56, .1)):
        d.ellipse([S * x, S * .28, S * (x + 2 * r), S * (.28 + 2 * r)], fill=(255, 255, 255, 255), outline=OUT, width=4)
        d.ellipse([S * (x + r * .7), S * (.28 + r * .9), S * (x + r * 1.3), S * (.28 + r * 1.5)], fill=OUT)
    d.chord([S * .3, S * .52, S * .74, S * .8], 0, 180, fill=(60, 20, 20, 255), outline=OUT, width=4)
    d.rectangle([S * .4, S * .66, S * .48, S * .72], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def mall_cop(size=64):
    """A mall cop on a segway, side view facing right: white shirt, cap and badge, the two-wheeled stand-up scooter."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.line([(S * .56, S * .3), (S * .66, S * .84)], fill=(60, 60, 66, 255), width=6)                             # handle bar post
    d.line([(S * .5, S * .3), (S * .64, S * .28)], fill=(60, 60, 66, 255), width=6)
    d.rounded_rectangle([S * .3, S * .24, S * .54, S * .58], 8, fill=(240, 240, 245, 255), outline=OUT, width=5)  # shirt
    d.ellipse([S * .44, S * .32, S * .5, S * .38], fill=(250, 200, 50, 255))                                     # badge
    d.rectangle([S * .3, S * .58, S * .54, S * .84], fill=(40, 50, 80, 255), outline=OUT, width=4)               # pants
    d.ellipse([S * .32, S * .04, S * .52, S * .24], fill=(220, 170, 130, 255), outline=OUT, width=4)              # head
    d.rectangle([S * .3, S * .02, S * .54, S * .1], fill=(40, 50, 80, 255), outline=OUT, width=3)                # cap
    d.line([(S * .5, S * .08), (S * .6, S * .1)], fill=(40, 50, 80, 255), width=4)                                # brim
    d.rectangle([S * .24, S * .84, S * .76, S * .9], fill=(60, 60, 66, 255), outline=OUT, width=3)               # deck
    for x in (.28, .72):
        d.ellipse([S * (x - .08), S * .82, S * (x + .08), S * .98], fill=(30, 30, 30, 255), outline=OUT, width=3)
    return _shrink(im, size)


def honey_bear(size=32):
    """A plastic honey bear squeeze bottle: amber honey, a yellow cap on its head."""
    im, d, S = _big(size)
    OUT = (110, 60, 0, 255)
    d.ellipse([S * .2, S * .44, S * .8, S * .98], fill=(240, 160, 30, 230), outline=OUT, width=5)
    d.ellipse([S * .28, S * .2, S * .72, S * .56], fill=(240, 160, 30, 230), outline=OUT, width=5)
    for x in (.26, .6):
        d.ellipse([S * x, S * .16, S * (x + .14), S * .3], fill=(240, 160, 30, 230), outline=OUT, width=4)
    d.rectangle([S * .42, S * .02, S * .58, S * .2], fill=(250, 220, 50, 255), outline=OUT, width=4)
    d.ellipse([S * .38, S * .32, S * .44, S * .38], fill=OUT)
    d.ellipse([S * .56, S * .32, S * .62, S * .38], fill=OUT)
    return _shrink(im, size)


def tea_mug(size=32):
    """A big white mug of steaming tea with a tea bag tag hanging off it."""
    im, d, S = _big(size)
    OUT = (40, 30, 20, 255)
    d.rounded_rectangle([S * .14, S * .34, S * .74, S * .94], 8, fill=(250, 250, 250, 255), outline=OUT, width=5)
    d.ellipse([S * .14, S * .3, S * .74, S * .42], fill=(170, 100, 40, 255), outline=OUT, width=4)
    d.arc([S * .62, S * .46, S * .92, S * .8], 270, 90, fill=OUT, width=6)
    d.line([(S * .3, S * .36), (S * .26, S * .62)], fill=(200, 200, 200, 255), width=2)
    d.rectangle([S * .2, S * .6, S * .32, S * .72], fill=(250, 210, 60, 255), outline=OUT, width=2)
    for x in (.34, .5):
        d.arc([S * (x - .06), S * .0, S * (x + .06), S * .28], 90, 270, fill=(255, 255, 255, 220), width=4)
    return _shrink(im, size)


def chef_knife(size=64):
    """A big chef's knife pointing up-right: wide steel blade with a shine line, black riveted handle."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.polygon([(S * .38, S * .62), (S * .92, S * .08), (S * .96, S * .16), (S * .5, S * .72)], fill=(215, 220, 230, 255), outline=OUT)
    d.line([(S * .38, S * .62), (S * .92, S * .08), (S * .96, S * .16), (S * .5, S * .72), (S * .38, S * .62)], fill=OUT, width=5)
    d.line([(S * .46, S * .62), (S * .9, S * .18)], fill=(255, 255, 255, 255), width=3)
    d.line([(S * .1, S * .92), (S * .42, S * .66)], fill=OUT, width=int(S * .12))
    d.line([(S * .1, S * .92), (S * .42, S * .66)], fill=(40, 40, 46, 255), width=int(S * .08))
    for t in (.3, .6):
        x, y = .1 + .32 * t, .92 - .26 * t
        d.ellipse([S * (x - .02), S * (y - .02), S * (x + .02), S * (y + .02)], fill=(200, 200, 210, 255))
    return _shrink(im, size)


def honing_steel(size=64):
    """A honing steel: a long ridged steel rod, a guard and a wood handle, pointing up-left."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.line([(S * .1, S * .1), (S * .62, S * .62)], fill=(150, 155, 165, 255), width=int(S * .06))
    for k in range(6):
        t = .1 + k * .14
        x, y = .1 + .52 * t, .1 + .52 * t
        d.line([(S * (x - .02), S * (y + .02)), (S * (x + .02), S * (y - .02))], fill=(100, 105, 115, 255), width=2)
    d.line([(S * .56, S * .68), (S * .68, S * .56)], fill=OUT, width=8)                                          # guard
    d.line([(S * .64, S * .64), (S * .92, S * .92)], fill=OUT, width=int(S * .11))
    d.line([(S * .64, S * .64), (S * .92, S * .92)], fill=(150, 100, 50, 255), width=int(S * .07))
    return _shrink(im, size)
