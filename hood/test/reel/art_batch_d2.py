

# ---- set 20 redo, batch D2: Peep Game, Zaza Storm, Dip Out, Spit Bars, Post Up -----------------------------

def playbook_clipboard(size=64):
    """A clipboard with the foe's game plan on it: PLAN: / HIT EM, an X-and-O doodle (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 25, 10, 255)
    d.rounded_rectangle([S * .14, S * .06, S * .86, S * .96], 8, fill=(160, 110, 60, 255), outline=OUT, width=7)
    d.rectangle([S * .22, S * .14, S * .78, S * .9], fill=(250, 250, 245, 255), outline=OUT, width=4)
    d.rounded_rectangle([S * .36, S * .02, S * .64, S * .14], 5, fill=(190, 190, 200, 255), outline=OUT, width=5)
    d.line([(S * .3, S * .7), (S * .4, S * .8)], fill=(220, 40, 40, 255), width=5)                          # X
    d.line([(S * .4, S * .7), (S * .3, S * .8)], fill=(220, 40, 40, 255), width=5)
    d.ellipse([S * .56, S * .68, S * .7, S * .82], outline=(40, 80, 200, 255), width=5)                      # O
    d.line([(S * .42, S * .75), (S * .54, S * .75)], fill=(40, 40, 46, 255), width=3)
    im = _shrink(im, size)
    return _texted(im, [("PLAN:", (32, 14)), ("HIT EM", (32, 26))], (20, 20, 25, 255), (250, 250, 245, 255))


def weather_map(size=64, level="LIGHT"):
    """A TV weather report: a map with a green blob over the hood, and a banner reading LIGHT / MODERATE /
    SEVERE (the blob grows and goes red) (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    col = {"LIGHT": (90, 200, 90, 255), "MODERATE": (240, 200, 40, 255), "SEVERE": (230, 40, 40, 255)}[level]
    grow = {"LIGHT": .1, "MODERATE": .18, "SEVERE": .28}[level]
    d.rounded_rectangle([S * .02, S * .04, S * .98, S * .9], 10, fill=(40, 40, 46, 255), outline=OUT, width=8)
    d.rectangle([S * .08, S * .1, S * .92, S * .66], fill=(90, 150, 230, 255))
    d.polygon([(S * .14, S * .6), (S * .2, S * .2), (S * .5, S * .14), (S * .86, S * .26), (S * .8, S * .62)], fill=(170, 200, 120, 255))
    d.ellipse([S * (.5 - grow), S * (.38 - grow * .8), S * (.5 + grow), S * (.38 + grow * .8)], fill=col[:3] + (200,))
    d.rectangle([S * .08, S * .66, S * .92, S * .84], fill=col, outline=OUT, width=4)
    d.rectangle([S * .44, S * .9, S * .56, S * .98], fill=(40, 40, 46, 255))
    im = _shrink(im, size)
    words = [(level, (32, 44))] + ([("ZAZA", (32, 6))] if level == "SEVERE" else [])
    return _texted(im, words, (255, 255, 255, 255), (20, 20, 25, 255))


def window_pane(size=64, broken=False):
    """A wooden window frame with four panes - or smashed out, jagged shards left in the frame."""
    im, d, S = _big(size)
    OUT = (50, 30, 15, 255)
    d.rectangle([S * .1, S * .08, S * .9, S * .92], fill=(140, 90, 50, 255), outline=OUT, width=7)
    for x0, y0 in ((.16, .14), (.52, .14), (.16, .52), (.52, .52)):
        d.rectangle([S * x0, S * y0, S * (x0 + .32), S * (y0 + .34)], fill=(170, 220, 250, 255) if not broken else (40, 40, 50, 255), outline=OUT, width=4)
        if broken:
            d.polygon([(S * x0, S * y0), (S * (x0 + .12), S * y0), (S * x0, S * (y0 + .14))], fill=(170, 220, 250, 255))
            d.polygon([(S * (x0 + .32), S * (y0 + .34)), (S * (x0 + .2), S * (y0 + .34)), (S * (x0 + .32), S * (y0 + .2))], fill=(170, 220, 250, 255))
        else:
            d.line([(S * (x0 + .06), S * (y0 + .24)), (S * (x0 + .2), S * (y0 + .06))], fill=(255, 255, 255, 255), width=4)
    return _shrink(im, size)


def jail_bar(size=64):
    """One heavy steel jail bar, flying."""
    im, d, S = _big(size)
    OUT = (20, 20, 26, 255)
    d.rounded_rectangle([S * .42, S * .02, S * .58, S * .98], 8, fill=(150, 155, 170, 255), outline=OUT, width=6)
    d.line([(S * .47, S * .08), (S * .47, S * .9)], fill=(230, 235, 245, 255), width=5)
    return _shrink(im, size)


def jail_cell(size=64):
    """The front of a jail cell: a steel frame and six bars (the foe shows through behind them)."""
    im, d, S = _big(size)
    OUT = (20, 20, 26, 255)
    d.rectangle([S * .04, S * .04, S * .96, S * .14], fill=(110, 115, 130, 255), outline=OUT, width=6)
    d.rectangle([S * .04, S * .86, S * .96, S * .96], fill=(110, 115, 130, 255), outline=OUT, width=6)
    for k in range(6):
        x = .1 + k * .158
        d.rectangle([S * x, S * .14, S * (x + .06), S * .86], fill=(150, 155, 170, 255), outline=OUT, width=4)
        d.line([(S * (x + .02), S * .16), (S * (x + .02), S * .84)], fill=(230, 235, 245, 255), width=3)
    d.rectangle([S * .4, S * .44, S * .6, S * .58], fill=(200, 170, 60, 255), outline=OUT, width=4)           # the lock
    return _shrink(im, size)


def cooler_box(size=64):
    """A red and white picnic cooler, lid cracked, ice and a soda can peeking out."""
    im, d, S = _big(size)
    OUT = (40, 10, 10, 255)
    d.rounded_rectangle([S * .08, S * .4, S * .92, S * .9], 10, fill=(220, 40, 40, 255), outline=OUT, width=7)
    d.rounded_rectangle([S * .06, S * .26, S * .94, S * .42], 8, fill=(250, 250, 250, 255), outline=OUT, width=7)
    d.rectangle([S * .4, S * .5, S * .6, S * .58], fill=(250, 250, 250, 255), outline=OUT, width=4)             # handle
    for x in (.2, .36):
        d.rectangle([S * x, S * .16, S * (x + .12), S * .28], fill=(200, 235, 255, 255), outline=(120, 160, 200, 255), width=3)
    d.rectangle([S * .6, S * .08, S * .74, S * .28], fill=(40, 120, 220, 255), outline=OUT, width=4)            # a can
    return _shrink(im, size)


def bbq_grill(size=64):
    """A black kettle grill on its legs, lid propped, burgers and dogs sizzling, smoke rolling up."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    for a, b in (((.3, .62), (.18, .96)), ((.7, .62), (.82, .96)), ((.5, .66), (.5, .96))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(60, 60, 66, 255), width=7)
    d.chord([S * .1, S * .3, S * .9, S * .8], 0, 180, fill=(40, 40, 46, 255), outline=OUT, width=7)              # the bowl
    d.ellipse([S * .66, S * .02, S * .98, S * .34], fill=(40, 40, 46, 255), outline=OUT, width=6)              # the lid, propped
    d.line([(S * .12, S * .55), (S * .88, S * .55)], fill=(150, 150, 160, 255), width=4)
    for x in (.2, .44):
        d.ellipse([S * x, S * .44, S * (x + .18), S * .56], fill=(110, 60, 30, 255), outline=OUT, width=4)       # burgers
    d.rounded_rectangle([S * .64, S * .46, S * .82, S * .54], 6, fill=(200, 90, 60, 255), outline=OUT, width=3)  # a dog
    for x in (.3, .5):
        d.ellipse([S * x, S * .18, S * (x + .14), S * .32], fill=(220, 220, 225, 180))
    return _shrink(im, size)
