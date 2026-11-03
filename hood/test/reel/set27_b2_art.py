

# ---- set 27, batch 2: RIP Shirt, Fresh Fit, Hotfoot, Space Jam, Dirty Water -------------------------------------------

def rip_tee(size=64):
    """An airbrushed memorial tee: white shirt, a sky-blue cloud with a gold halo and wings, R.I.P. across the top
    (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 40, 50, 255)
    pts = [(S * .3, S * .06), (S * .42, S * .1), (S * .58, S * .1), (S * .7, S * .06), (S * .98, S * .24), (S * .88, S * .42),
           (S * .78, S * .36), (S * .78, S * .98), (S * .22, S * .98), (S * .22, S * .36), (S * .12, S * .42), (S * .02, S * .24)]
    _outline_poly(d, pts, (250, 250, 250, 255), OUT, 7)
    d.arc([S * .4, S * .02, S * .6, S * .18], 0, 180, fill=OUT, width=5)                                         # collar
    d.ellipse([S * .3, S * .46, S * .7, S * .9], fill=(150, 200, 250, 255))                                       # the airbrush cloud
    for x in (.24, .62):                                                                                          # wings
        d.ellipse([S * x, S * .56, S * (x + .14), S * .78], fill=(255, 255, 255, 255), outline=(180, 200, 230, 255), width=3)
    d.ellipse([S * .42, S * .58, S * .58, S * .8], fill=(60, 50, 70, 255))                                         # a silhouette
    d.ellipse([S * .4, S * .5, S * .6, S * .58], outline=(250, 200, 40, 255), width=5)                            # halo
    im = _shrink(im, size)
    return _texted(im, [("R.I.P.", (32, 17))], (60, 120, 220, 255), (255, 255, 255, 255))


def lint_roller(size=64):
    """A lint roller: the sticky white roll with lint stuck on, red handle."""
    im, d, S = _big(size)
    OUT = (40, 10, 10, 255)
    d.line([(S * .5, S * .52), (S * .7, S * .96)], fill=OUT, width=int(S * .12))
    d.line([(S * .5, S * .52), (S * .7, S * .96)], fill=(220, 40, 40, 255), width=int(S * .07))
    d.rounded_rectangle([S * .08, S * .14, S * .92, S * .5], 14, fill=(250, 250, 240, 255), outline=OUT, width=6)
    for x, y in ((.2, .26), (.36, .38), (.6, .22), (.78, .36), (.48, .3)):
        d.ellipse([S * x, S * y, S * (x + .06), S * (y + .05)], fill=(150, 140, 130, 255))
    d.line([(S * .1, S * .2), (S * .9, S * .2)], fill=(220, 220, 210, 255), width=3)
    return _shrink(im, size)


def lint_ball(n=16):
    """A lint fuzzball (alpha only): a scruffy clump."""
    c = (n - 1) / 2
    return _alpha(n, n, lambda x, y: 1 if ((x - c) ** 2 + (y - c) ** 2) ** .5 < 3 + ((x * 7 + y * 3) % 4) * .6 else 0)


def amber_cologne(size=32):
    """A fancy cologne bottle: faceted amber glass, gold cap, a black label."""
    im, d, S = _big(size)
    OUT = (40, 25, 0, 255)
    d.polygon([(S * .2, S * .4), (S * .8, S * .4), (S * .9, S * .7), (S * .7, S * .96), (S * .3, S * .96), (S * .1, S * .7)],
              fill=(230, 150, 40, 230), outline=OUT)
    d.line([(S * .2, S * .4), (S * .8, S * .4), (S * .9, S * .7), (S * .7, S * .96), (S * .3, S * .96), (S * .1, S * .7), (S * .2, S * .4)], fill=OUT, width=5)
    d.rectangle([S * .38, S * .14, S * .62, S * .4], fill=(250, 210, 60, 255), outline=OUT, width=5)
    d.rectangle([S * .32, S * .6, S * .68, S * .76], fill=(20, 20, 20, 255))
    d.line([(S * .26, S * .5), (S * .34, S * .84)], fill=(255, 230, 170, 255), width=4)
    return _shrink(im, size)


def hot_asphalt(size=64):
    """A patch of black summer asphalt baking: a yellow road line, wavy heat shimmer rising off it."""
    im, d, S = _big(size)
    d.polygon([(S * .0, S * .62), (S * 1.0, S * .62), (S * .9, S * .96), (S * .1, S * .96)], fill=(40, 40, 46, 255), outline=(15, 15, 20, 255))
    d.line([(S * .3, S * .8), (S * .7, S * .8)], fill=(250, 210, 40, 255), width=7)
    import math
    for k in range(4):                                                           # heat shimmer
        x0 = .16 + k * .22
        pts = [(S * (x0 + .04 * math.sin(t * 2.4)), S * (.56 - t * .1)) for t in range(5)]
        d.line(pts, fill=(255, 150, 80, 200), width=5, joint="curve")
    return _shrink(im, size)


def hood_slide(size=64, lit=False):
    """A black slide sandal with a white strap stripe, a white tube sock still in it - and on fire if lit."""
    im, d, S = _big(size)
    OUT = (10, 10, 15, 255)
    if lit:
        for x, h in ((.2, .1), (.42, .0), (.64, .06), (.84, .2)):
            d.polygon([(S * (x - .12), S * .6), (S * x, S * h), (S * (x + .12), S * .6)], fill=(250, 120, 20, 255))
            d.polygon([(S * (x - .06), S * .6), (S * x, S * (h + .2)), (S * (x + .06), S * .6)], fill=(255, 230, 90, 255))
    d.rounded_rectangle([S * .04, S * .72, S * .96, S * .88], 10, fill=(30, 30, 35, 255), outline=OUT, width=5)  # sole
    d.ellipse([S * .1, S * .3, S * .66, S * .78], fill=(250, 250, 250, 255), outline=(150, 150, 160, 255), width=5)  # the sock
    d.rectangle([S * .2, S * .1, S * .54, S * .44], fill=(250, 250, 250, 255), outline=(150, 150, 160, 255), width=5)
    for y in (.16, .24):
        d.line([(S * .22, S * y), (S * .52, S * y)], fill=(220, 40, 40, 255), width=4)                          # sock stripes
    d.chord([S * .42, S * .5, S * .94, S * .9], 180, 360, fill=(30, 30, 35, 255), outline=OUT, width=5)         # strap
    d.line([(S * .5, S * .64), (S * .86, S * .64)], fill=(250, 250, 250, 255), width=5)
    return _shrink(im, size)


def meteor_ball(size=64):
    """A basketball coming in from orbit: the ball bottom-right, a long flaming re-entry tail up-left."""
    im, d, S = _big(size)
    OUT = (40, 15, 0, 255)
    d.polygon([(S * .02, S * .1), (S * .2, S * .02), (S * .74, S * .5), (S * .5, S * .74)], fill=(250, 120, 20, 230))
    d.polygon([(S * .2, S * .24), (S * .3, S * .2), (S * .7, S * .56), (S * .56, S * .68)], fill=(255, 230, 100, 255))
    d.ellipse([S * .5, S * .5, S * .96, S * .96], fill=(235, 120, 30, 255), outline=OUT, width=6)
    d.line([(S * .73, S * .5), (S * .73, S * .96)], fill=OUT, width=4)
    d.line([(S * .5, S * .73), (S * .96, S * .73)], fill=OUT, width=4)
    d.arc([S * .58, S * .5, S * 1.0, S * .96], 120, 240, fill=OUT, width=4)
    d.arc([S * .46, S * .5, S * .88, S * .96], 300, 60, fill=OUT, width=4)
    return _shrink(im, size)


def street_hoop(size=64):
    """A street basketball hoop: white backboard with the red square, orange rim, a chain net."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.rectangle([S * .14, S * .04, S * .86, S * .46], fill=(245, 245, 250, 255), outline=OUT, width=6)
    d.rectangle([S * .38, S * .2, S * .62, S * .4], outline=(220, 30, 30, 255), width=5)
    d.ellipse([S * .28, S * .4, S * .72, S * .54], outline=(250, 110, 20, 255), width=7)
    for k in range(5):                                                           # chain net
        x = .3 + k * .1
        d.line([(S * x, S * .5), (S * (.42 + k * .04), S * .82)], fill=(170, 170, 180, 255), width=3)
    d.line([(S * .36, S * .66), (S * .64, S * .66)], fill=(170, 170, 180, 255), width=3)
    return _shrink(im, size)


def bus_stop(size=64):
    """A bus stop sign on a pole: the blue BUS STOP plate with a bus icon (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (15, 20, 40, 255)
    d.line([(S * .5, S * .4), (S * .5, S * 1.0)], fill=(140, 140, 150, 255), width=int(S * .06))
    d.rounded_rectangle([S * .2, S * .02, S * .8, S * .44], 8, fill=(30, 80, 200, 255), outline=OUT, width=6)
    d.rectangle([S * .36, S * .28, S * .64, S * .38], fill=(255, 255, 255, 255))
    im = _shrink(im, size)
    return _texted(im, [("BUS", (32, 3)), ("STOP", (32, 11))], (255, 255, 255, 255), OUT)


def curb_car(size=64):
    """A boxy old sedan doing 40 down the block: maroon body, chrome bumper, side view facing right."""
    im, d, S = _big(size)
    OUT = (20, 10, 10, 255)
    d.polygon([(S * .02, S * .5), (S * .24, S * .48), (S * .34, S * .3), (S * .7, S * .3), (S * .8, S * .48), (S * .98, S * .52),
               (S * .98, S * .74), (S * .02, S * .74)], fill=(130, 30, 40, 255), outline=OUT)
    d.line([(S * .02, S * .5), (S * .24, S * .48), (S * .34, S * .3), (S * .7, S * .3), (S * .8, S * .48), (S * .98, S * .52),
            (S * .98, S * .74), (S * .02, S * .74), (S * .02, S * .5)], fill=OUT, width=6)
    d.polygon([(S * .38, S * .35), (S * .52, S * .35), (S * .52, S * .48), (S * .3, S * .48)], fill=(160, 210, 240, 255))
    d.polygon([(S * .56, S * .35), (S * .68, S * .35), (S * .76, S * .48), (S * .56, S * .48)], fill=(160, 210, 240, 255))
    d.rectangle([S * .9, S * .6, S * .99, S * .7], fill=(220, 220, 225, 255), outline=OUT, width=3)             # bumper
    for x in (.2, .76):
        d.ellipse([S * (x - .1), S * .64, S * (x + .1), S * .86], fill=(25, 25, 25, 255), outline=OUT, width=4)
        d.ellipse([S * (x - .04), S * .7, S * (x + .04), S * .8], fill=(200, 200, 205, 255))
    return _shrink(im, size)


def city_bus(size=64):
    """A big city bus, side view facing right: white and blue, a row of windows, the route sign lit up."""
    im, d, S = _big(size)
    OUT = (15, 20, 40, 255)
    d.rounded_rectangle([S * .0, S * .16, S * 1.0, S * .82], 10, fill=(240, 240, 245, 255), outline=OUT, width=6)
    d.rectangle([S * .0, S * .6, S * 1.0, S * .7], fill=(30, 90, 210, 255))
    for k in range(5):
        x = .04 + k * .17
        d.rectangle([S * x, S * .26, S * (x + .13), S * .46], fill=(130, 180, 220, 255), outline=OUT, width=3)
    d.rectangle([S * .88, S * .2, S * .99, S * .56], fill=(110, 160, 210, 255), outline=OUT, width=3)          # windshield
    d.rectangle([S * .6, S * .18, S * .86, S * .24], fill=(250, 180, 30, 255))                                  # route sign
    for x in (.18, .8):
        d.ellipse([S * (x - .09), S * .72, S * (x + .09), S * .92], fill=(25, 25, 25, 255), outline=OUT, width=4)
    return _shrink(im, size)


def mud_splash(n=16):
    """A splatter of dirty water (alpha only): a blob with a couple of drops."""
    def f(x, y):
        return 1 if ((x - 7) / 5) ** 2 + ((y - 9) / 4) ** 2 < 1 or (x - 12) ** 2 + (y - 3) ** 2 < 3 or (x - 3) ** 2 + (y - 2) ** 2 < 2 else 0
    return _alpha(n, n, f)
