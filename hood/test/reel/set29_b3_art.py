

# ---- set 29, batch 3: Power Trade, Guard Trade, Shove Off, Dirty Cross, Open Window ----------------------------------------

def preworkout_tub(size=32):
    """A tub of pre-workout: black with a red lightning bolt and a scoop lid."""
    im, d, S = _big(size)
    OUT = (10, 10, 10, 255)
    d.rounded_rectangle([S * .16, S * .3, S * .84, S * .96], 8, fill=(30, 30, 34, 255), outline=OUT, width=5)
    d.rectangle([S * .12, S * .16, S * .88, S * .32], fill=(230, 40, 40, 255), outline=OUT, width=4)
    d.polygon([(S * .56, S * .38), (S * .36, S * .66), (S * .5, S * .66), (S * .42, S * .9), (S * .66, S * .58), (S * .52, S * .58)], fill=(250, 220, 40, 255))
    return _shrink(im, size)


def chamomile_box(size=32):
    """A soft yellow box of chamomile tea with a little daisy on it."""
    im, d, S = _big(size)
    OUT = (110, 90, 30, 255)
    d.rectangle([S * .12, S * .2, S * .88, S * .9], fill=(250, 235, 160, 255), outline=OUT, width=5)
    for k in range(6):
        import math
        a = k * math.tau / 6
        x, y = .5 + .14 * math.cos(a), .52 + .14 * math.sin(a)
        d.ellipse([S * (x - .08), S * (y - .08), S * (x + .08), S * (y + .08)], fill=(255, 255, 255, 255))
    d.ellipse([S * .43, S * .45, S * .57, S * .59], fill=(250, 190, 40, 255))
    d.line([(S * .5, S * .66), (S * .5, S * .84)], fill=(90, 160, 70, 255), width=4)
    return _shrink(im, size)


def big_umbrella(size=64, busted=False):
    """A big black golf umbrella, open - or a busted bodega umbrella: spokes snapped, canopy flipped inside out."""
    im, d, S = _big(size)
    OUT = (10, 10, 15, 255)
    if busted:
        d.polygon([(S * .5, S * .5), (S * .08, S * .1), (S * .3, S * .3), (S * .48, S * .04), (S * .62, S * .3), (S * .9, S * .14)],
                  fill=(60, 60, 70, 255), outline=OUT)
        for x, y in ((.08, .1), (.48, .04), (.9, .14), (.2, .4)):
            d.line([(S * .5, S * .5), (S * x, S * y)], fill=(160, 160, 170, 255), width=3)
    else:
        d.chord([S * .02, S * .1, S * .98, S * .8], 180, 360, fill=(30, 30, 40, 255), outline=OUT, width=6)
        for x in (.26, .5, .74):
            d.line([(S * .5, S * .14), (S * x, S * .45)], fill=(90, 90, 110, 255), width=3)
        d.arc([S * .1, S * .16, S * .5, S * .6], 200, 260, fill=(120, 120, 140, 255), width=5)
    d.line([(S * .5, S * .44), (S * .5, S * .9)], fill=(170, 170, 180, 255), width=5)
    d.arc([S * .5, S * .82, S * .66, S * .98], 0, 180, fill=(120, 70, 30, 255), width=7)                        # the hook handle
    return _shrink(im, size)


def push_broom(size=64):
    """A wide push broom pointing right: long wood handle, a fat black bristle head."""
    im, d, S = _big(size)
    OUT = (20, 15, 10, 255)
    d.line([(S * .02, S * .2), (S * .66, S * .5)], fill=OUT, width=int(S * .08))
    d.line([(S * .02, S * .2), (S * .66, S * .5)], fill=(200, 150, 90, 255), width=int(S * .05))
    d.rectangle([S * .62, S * .16, S * .78, S * .84], fill=(150, 100, 50, 255), outline=OUT, width=5)          # block
    for k in range(10):                                                                                           # bristles
        y = .2 + k * .065
        d.line([(S * .78, S * y), (S * .96, S * y)], fill=(30, 30, 30, 255), width=4)
    return _shrink(im, size)


def spray_can(size=64):
    """A spray paint can: toxic green, white cap and nozzle, a drip down the side."""
    im, d, S = _big(size)
    OUT = (10, 30, 10, 255)
    d.rounded_rectangle([S * .3, S * .3, S * .7, S * .96], 10, fill=(90, 210, 60, 255), outline=OUT, width=6)
    d.rectangle([S * .3, S * .52, S * .7, S * .68], fill=(30, 30, 30, 255))
    d.chord([S * .3, S * .14, S * .7, S * .46], 180, 360, fill=(240, 240, 240, 255), outline=OUT, width=5)
    d.rectangle([S * .44, S * .06, S * .56, S * .18], fill=(240, 240, 240, 255), outline=OUT, width=4)
    d.line([(S * .38, S * .3), (S * .38, S * .42)], fill=(90, 210, 60, 255), width=5)
    d.line([(S * .36, S * .36), (S * .36, S * .5)], fill=(160, 255, 120, 255), width=3)
    return _shrink(im, size)


def paint_x(size=64):
    """A dripping spray-painted X tag in toxic green."""
    im, d, S = _big(size)
    G, OUT = (110, 230, 60, 255), (30, 70, 10, 255)
    for a, b in (((.12, .12), (.88, .82)), ((.86, .1), (.14, .84))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=OUT, width=int(S * .18))
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=G, width=int(S * .12))
    for x, y in ((.2, .84), (.84, .86), (.5, .54)):                                                              # drips
        d.line([(S * x, S * y), (S * x, S * (y + .12))], fill=G, width=5)
        d.ellipse([S * (x - .03), S * (y + .1), S * (x + .03), S * (y + .16)], fill=G)
    return _shrink(im, size)


def sash_window(size=64, opened=False):
    """An apartment sash window in a brick wall: closed, or the bottom pane pushed up with the night air coming in."""
    im, d, S = _big(size)
    OUT = (30, 20, 15, 255)
    d.rectangle([S * .0, S * .0, S * 1.0, S * 1.0], fill=(160, 70, 50, 255))
    for r in range(8):
        y = r * .125
        d.line([(0, S * y), (S, S * y)], fill=(120, 50, 35, 255), width=3)
    d.rectangle([S * .14, S * .08, S * .86, S * .92], fill=(240, 240, 235, 255), outline=OUT, width=6)
    top = (.14, .08, .86, .5)
    d.rectangle([S * .2, S * .14, S * .8, S * .46], fill=(150, 190, 220, 255), outline=OUT, width=4)
    if opened:
        d.rectangle([S * .2, S * .52, S * .8, S * .86], fill=(20, 20, 40, 255))                                  # open air
        d.rectangle([S * .18, S * .4, S * .82, S * .5], fill=(240, 240, 235, 255), outline=OUT, width=4)        # the pane pushed up
    else:
        d.rectangle([S * .2, S * .54, S * .8, S * .86], fill=(150, 190, 220, 255), outline=OUT, width=4)
        d.line([(S * .14, S * .5), (S * .86, S * .5)], fill=OUT, width=6)
    return _shrink(im, size)


def pizza_box_fan(size=64):
    """A greasy flat pizza box being waved like a fan, a grease spot on the lid."""
    im, d, S = _big(size)
    OUT = (90, 60, 20, 255)
    d.polygon([(S * .06, S * .3), (S * .9, S * .14), (S * .96, S * .64), (S * .12, S * .82)], fill=(225, 195, 140, 255), outline=OUT)
    d.line([(S * .06, S * .3), (S * .9, S * .14), (S * .96, S * .64), (S * .12, S * .82), (S * .06, S * .3)], fill=OUT, width=6)
    d.ellipse([S * .5, S * .34, S * .72, S * .5], fill=(190, 140, 70, 255))                                     # grease spot
    d.line([(S * .12, S * .82), (S * .96, S * .64), (S * .96, S * .7), (S * .14, S * .88)], fill=OUT, width=4)
    return _shrink(im, size)
