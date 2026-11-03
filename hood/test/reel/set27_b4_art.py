

# ---- set 27, batch 4: Back Rub, Flu Shot, Bad Wind, Tat Gun, Cut Line ---------------------------------------------------

def back_scratcher(size=64):
    """A bamboo back scratcher: a long jointed cane, the curled little rake of a tip at the top right."""
    im, d, S = _big(size)
    OUT = (70, 45, 10, 255)
    d.line([(S * .08, S * .94), (S * .74, S * .26)], fill=OUT, width=int(S * .11))
    d.line([(S * .08, S * .94), (S * .74, S * .26)], fill=(220, 190, 110, 255), width=int(S * .07))
    for t in (.3, .6):                                                                                           # bamboo joints
        x, y = .08 + .66 * t, .94 - .68 * t
        d.line([(S * (x - .05), S * (y - .05)), (S * (x + .05), S * (y + .05))], fill=OUT, width=6)
    d.line([(S * .7, S * .3), (S * .86, S * .14)], fill=OUT, width=int(S * .11))
    d.line([(S * .7, S * .3), (S * .86, S * .14)], fill=(220, 190, 110, 255), width=int(S * .07))
    d.ellipse([S * .72, S * .0, S * .98, S * .26], fill=(220, 190, 110, 255), outline=OUT, width=6)          # the cupped tip
    for k in range(4):                                                                                           # rake fingers
        a, b = (.74 + k * .07, .04 + k * .07), (.78 + k * .07, -.02 + k * .07)
        d.line([(S * a[0], S * a[1]), (S * (a[0] + .1), S * (a[1] - .02))], fill=OUT, width=6)
    return _shrink(im, size)


def stat_slot(size=64, stat="???"):
    """A tiny slot machine window showing one stat (ATK / DEF / SPD / ???) with a lever (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 20, 0, 255)
    d.rounded_rectangle([S * .06, S * .22, S * .8, S * .78], 12, fill=(220, 40, 40, 255), outline=OUT, width=7)
    d.rectangle([S * .16, S * .34, S * .7, S * .66], fill=(255, 250, 235, 255), outline=OUT, width=5)
    d.line([(S * .88, S * .5), (S * .88, S * .18)], fill=(170, 170, 180, 255), width=6)                         # lever
    d.ellipse([S * .82, S * .08, S * .96, S * .22], fill=(250, 210, 40, 255), outline=OUT, width=4)
    im = _shrink(im, size)
    return _texted(im, [(stat, (28, 27))], (200, 20, 20, 255), (255, 250, 235, 255))


def alcohol_swab(size=32):
    """An alcohol prep pad: a small white square in a torn foil packet."""
    im, d, S = _big(size)
    OUT = (90, 90, 110, 255)
    d.polygon([(S * .1, S * .3), (S * .7, S * .2), (S * .9, S * .7), (S * .3, S * .82)], fill=(200, 210, 225, 255), outline=OUT)
    d.polygon([(S * .2, S * .36), (S * .64, S * .3), (S * .78, S * .64), (S * .34, S * .72)], fill=(255, 255, 255, 255))
    d.line([(S * .3, S * .45), (S * .6, S * .4)], fill=(120, 170, 230, 255), width=4)
    return _shrink(im, size)


def flu_syringe(size=64):
    """A big cartoon syringe pointing right: clear barrel with yellow vaccine, plunger, a long shiny needle."""
    im, d, S = _big(size)
    OUT = (30, 40, 60, 255)
    d.rectangle([S * .02, S * .4, S * .1, S * .6], fill=(220, 220, 230, 255), outline=OUT, width=4)             # plunger end
    d.rectangle([S * .1, S * .47, S * .22, S * .53], fill=(220, 220, 230, 255), outline=OUT, width=3)
    d.rectangle([S * .22, S * .36, S * .64, S * .64], fill=(220, 240, 250, 180), outline=OUT, width=5)          # barrel
    d.rectangle([S * .36, S * .4, S * .62, S * .6], fill=(250, 220, 80, 255))
    for x in (.3, .4, .5):
        d.line([(S * x, S * .36), (S * x, S * .44)], fill=OUT, width=3)
    d.polygon([(S * .64, S * .44), (S * .72, S * .46), (S * .72, S * .54), (S * .64, S * .56)], fill=(200, 200, 210, 255), outline=OUT)
    d.line([(S * .72, S * .5), (S * .98, S * .5)], fill=(210, 215, 230, 255), width=4)                          # the needle
    d.line([(S * .74, S * .48), (S * .92, S * .48)], fill=(255, 255, 255, 255), width=2)
    return _shrink(im, size)


def elevator_door(size=64):
    """One brushed-steel elevator door panel (the right edge is the seam), a little floor-number light up top."""
    im, d, S = _big(size)
    OUT = (40, 45, 55, 255)
    d.rectangle([S * .1, S * .02, S * .96, S * .98], fill=(180, 185, 195, 255), outline=OUT, width=7)
    for k in range(6):                                                                                            # brushed lines
        y = .14 + k * .14
        d.line([(S * .18, S * y), (S * .88, S * (y + .02))], fill=(205, 210, 220, 255), width=3)
    d.line([(S * .94, S * .04), (S * .94, S * .96)], fill=(110, 115, 125, 255), width=5)
    return _shrink(im, size)


def tattoo_gun(size=64):
    """A tattoo machine pointing down-right: coils, the frame, a grip, the needle tip, ink drop."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.line([(S * .5, S * .5), (S * .88, S * .9)], fill=OUT, width=int(S * .1))                                  # grip + tube
    d.line([(S * .5, S * .5), (S * .88, S * .9)], fill=(180, 180, 190, 255), width=int(S * .06))
    d.line([(S * .88, S * .9), (S * .96, S * .98)], fill=(60, 60, 66, 255), width=3)                            # needle
    d.ellipse([S * .92, S * .92, S * 1.0, S * 1.0], fill=(30, 30, 40, 255))
    for x, y in ((.14, .2), (.3, .12)):                                                                           # coils
        d.rounded_rectangle([S * x, S * y, S * (x + .14), S * (y + .3)], 6, fill=(200, 120, 40, 255), outline=OUT, width=5)
    d.polygon([(S * .1, S * .5), (S * .54, S * .3), (S * .6, S * .54), (S * .2, S * .62)], fill=(50, 50, 60, 255), outline=OUT)
    d.line([(S * .1, S * .5), (S * .54, S * .3), (S * .6, S * .54), (S * .2, S * .62), (S * .1, S * .5)], fill=OUT, width=5)
    d.line([(S * .1, S * .5), (S * .02, S * .7)], fill=(60, 60, 66, 255), width=5)                              # clip cord
    return _shrink(im, size)


def mom_tattoo(size=64):
    """A classic heart tattoo: red heart, a banner across it reading MOM (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (20, 20, 40, 255)
    d.ellipse([S * .14, S * .16, S * .52, S * .54], fill=(220, 30, 50, 255), outline=OUT, width=6)
    d.ellipse([S * .48, S * .16, S * .86, S * .54], fill=(220, 30, 50, 255), outline=OUT, width=6)
    d.polygon([(S * .16, S * .42), (S * .84, S * .42), (S * .5, S * .88)], fill=(220, 30, 50, 255))
    d.line([(S * .16, S * .44), (S * .5, S * .88), (S * .84, S * .44)], fill=OUT, width=6)
    d.ellipse([S * .24, S * .22, S * .36, S * .32], fill=(255, 150, 160, 255))
    d.polygon([(S * .02, S * .4), (S * .98, S * .4), (S * .92, S * .5), (S * .98, S * .6), (S * .02, S * .6), (S * .08, S * .5)],
              fill=(250, 240, 200, 255), outline=OUT)
    d.line([(S * .02, S * .4), (S * .98, S * .4), (S * .92, S * .5), (S * .98, S * .6), (S * .02, S * .6), (S * .08, S * .5), (S * .02, S * .4)], fill=OUT, width=5)
    im = _shrink(im, size)
    return _texted(im, [("MOM", (32, 28))], (30, 40, 120, 255), (250, 240, 200, 255))


def deli_sign(size=64, n="48"):
    """The deli counter's red NOW SERVING sign with the number in LED digits (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 0, 0, 255)
    d.rounded_rectangle([S * .04, S * .16, S * .96, S * .84], 10, fill=(200, 30, 30, 255), outline=OUT, width=7)
    d.rectangle([S * .26, S * .46, S * .74, S * .76], fill=(20, 10, 10, 255), outline=OUT, width=4)
    im = _shrink(im, size)
    return _texted(im, [("NOW", (32, 12)), ("SERVING", (32, 20)), (n, (32, 31))], (255, 250, 220, 255), (90, 0, 0, 255))


def deli_ticket(size=32):
    """A pulled deli number ticket: a red paper tab, a big 49 (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (90, 10, 10, 255)
    d.rectangle([S * .1, S * .2, S * .9, S * .8], fill=(250, 90, 90, 255), outline=OUT, width=6)
    for x in (.1, .9):
        d.ellipse([S * (x - .06), S * .44, S * (x + .06), S * .56], fill=(0, 0, 0, 0))
    im = _shrink(im, size)
    return _texted(im, [("49", (16, 12))], (255, 255, 255, 255), OUT)
