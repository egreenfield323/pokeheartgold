

# ---- set 26, batch 5: Weed Whacker, Sledgehammer, Seed Toss, Jet Ski, Back Alley ----------------------------------------

def string_trimmer(size=64):
    """A weed whacker: orange motor at the top, long shaft, the spinning head with the line at the bottom right."""
    im, d, S = _big(size)
    OUT = (20, 15, 5, 255)
    d.line([(S * .2, S * .2), (S * .8, S * .8)], fill=(20, 15, 5, 255), width=int(S * .11))
    d.line([(S * .2, S * .2), (S * .8, S * .8)], fill=(170, 175, 185, 255), width=int(S * .07))
    d.rounded_rectangle([S * .06, S * .06, S * .32, S * .3], 8, fill=(250, 130, 30, 255), outline=OUT, width=6)
    d.line([(S * .42, S * .36), (S * .5, S * .3)], fill=OUT, width=6)                                            # handle
    d.ellipse([S * .66, S * .66, S * .96, S * .96], fill=(60, 60, 66, 255), outline=OUT, width=6)
    for a, b in (((.82, .82), (.98, .7)), ((.82, .82), (.66, .98))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(250, 220, 60, 255), width=7)
    return _shrink(im, size)


def grass_clip(n=16):
    """A grass clipping (alpha only): a short thin blade."""
    return _alpha(n, n, lambda x, y: 1 if abs((x - 3) - (y - 3) * .8) < 1.1 and 2 < y < 14 else 0)




def jet_ski(size=64):
    """A red and white jet ski facing right, handlebars up, spray kicking off the back."""
    im, d, S = _big(size)
    OUT = (30, 10, 10, 255)
    d.polygon([(S * .04, S * .56), (S * .8, S * .5), (S * .98, S * .62), (S * .86, S * .74), (S * .08, S * .74)], fill=(220, 30, 30, 255), outline=OUT)
    d.line([(S * .04, S * .56), (S * .8, S * .5), (S * .98, S * .62), (S * .86, S * .74), (S * .08, S * .74), (S * .04, S * .56)], fill=OUT, width=6)
    d.polygon([(S * .2, S * .5), (S * .56, S * .48), (S * .52, S * .56), (S * .2, S * .58)], fill=(240, 240, 245, 255), outline=OUT)  # seat
    d.line([(S * .62, S * .5), (S * .66, S * .3)], fill=(60, 60, 66, 255), width=6)
    d.line([(S * .58, S * .3), (S * .74, S * .28)], fill=(60, 60, 66, 255), width=7)                              # handlebars
    d.line([(S * .1, S * .68), (S * .8, S * .66)], fill=(250, 250, 250, 255), width=4)
    for x, y in ((.0, .7), (.06, .8), (.02, .62)):
        d.ellipse([S * x, S * y, S * (x + .08), S * (y + .08)], fill=(200, 230, 255, 255))
    return _shrink(im, size)


def shoe_print(n=16):
    """A sneaker footprint (alpha only): sole with a tread gap and the heel."""
    def f(x, y):
        sole = ((x - 7.5) / 3.6) ** 2 + ((y - 5.5) / 4.6) ** 2 < 1
        heel = ((x - 7.5) / 2.8) ** 2 + ((y - 12.5) / 2.4) ** 2 < 1
        return (.85 if y % 3 else .4) if sole else (1 if heel else 0)
    return _alpha(n, n, f)


def mole_hole(size=64):
    """A dirt mound with a dark hole in the top (the whack-a-mole hole)."""
    im, d, S = _big(size)
    OUT = (50, 30, 10, 255)
    d.chord([S * .06, S * .44, S * .94, S * 1.2], 180, 360, fill=(140, 95, 50, 255), outline=OUT, width=6)
    d.ellipse([S * .3, S * .5, S * .7, S * .64], fill=(30, 20, 10, 255))
    for x, y in ((.2, .7), (.76, .74), (.5, .78)):
        d.ellipse([S * x, S * y, S * (x + .06), S * (y + .04)], fill=(110, 75, 40, 255))
    return _shrink(im, size)


def arcade_mole(size=64):
    """A cartoon mole popping up: brown fur, pink nose, buck teeth, beady eyes."""
    im, d, S = _big(size)
    OUT = (40, 20, 10, 255)
    d.rounded_rectangle([S * .28, S * .2, S * .72, S * .9], 22, fill=(140, 90, 60, 255), outline=OUT, width=6)
    for x in (.38, .56):
        d.ellipse([S * x, S * .34, S * (x + .06), S * .42], fill=OUT)
    d.ellipse([S * .44, S * .44, S * .56, S * .54], fill=(255, 140, 170, 255), outline=OUT, width=3)
    d.rectangle([S * .46, S * .54, S * .54, S * .62], fill=(255, 255, 255, 255), outline=OUT, width=2)
    return _shrink(im, size)


def foam_mallet(size=64):
    """A whack-a-mole foam mallet: a big padded red head on a yellow handle."""
    im, d, S = _big(size)
    OUT = (60, 10, 10, 255)
    d.line([(S * .2, S * .9), (S * .56, S * .4)], fill=OUT, width=int(S * .1))
    d.line([(S * .2, S * .9), (S * .56, S * .4)], fill=(250, 210, 40, 255), width=int(S * .06))
    d.rounded_rectangle([S * .4, S * .1, S * .96, S * .44], 18, fill=(220, 40, 40, 255), outline=OUT, width=7)
    d.line([(S * .48, S * .18), (S * .86, S * .18)], fill=(255, 130, 120, 255), width=6)
    return _shrink(im, size)


def chia_fuzz(size=64, stage=0):
    """Chia sprouts growing on top of someone's head: 0 = a few green sprouts, 1 = a fuzzy layer, 2 = a full green afro."""
    import random
    im, d, S = _big(size)
    r = random.Random(4 + stage)
    if stage == 2:
        d.ellipse([S * .06, S * .1, S * .94, S * .84], fill=(70, 160, 60, 255), outline=(30, 90, 30, 255), width=6)
    n = (8, 30, 70)[stage]
    top, bot = ((.62, .9), (.4, .9), (.12, .8))[stage]
    for _ in range(n):
        x, y = r.uniform(.14, .86), r.uniform(top, bot)
        d.line([(S * x, S * (y + .08)), (S * (x + r.uniform(-.04, .04)), S * y)], fill=(60, 170, 60, 255), width=4)
        d.ellipse([S * (x - .03), S * (y - .03), S * (x + .03), S * (y + .03)], fill=(140, 220, 100, 255))
    return _shrink(im, size)


def spray_bottle(size=32):
    """A blue plant mister spray bottle, nozzle right."""
    im, d, S = _big(size)
    OUT = (20, 40, 80, 255)
    d.rounded_rectangle([S * .2, S * .4, S * .6, S * .96], 8, fill=(120, 190, 250, 220), outline=OUT, width=5)
    d.rectangle([S * .26, S * .26, S * .54, S * .4], fill=(250, 250, 250, 255), outline=OUT, width=4)
    d.polygon([(S * .54, S * .26), (S * .9, S * .26), (S * .9, S * .34), (S * .54, S * .34)], fill=(250, 250, 250, 255), outline=OUT)
    d.line([(S * .54, S * .36), (S * .68, S * .5)], fill=OUT, width=5)
    return _shrink(im, size)
