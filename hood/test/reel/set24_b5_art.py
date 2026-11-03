

# ---- set 24, batch 5: Snap Out, Lint Trap, Bait Switch, The Wobble, Claw Machine --------------------------------------

def gym_sock(size=64):
    """A crusty white tube sock with red and blue stripes, a yellowed toe, green stink lines rising off it."""
    im, d, S = _big(size)
    OUT = (60, 60, 50, 255)
    d.line([(S * .5, S * .14), (S * .5, S * .62), (S * .7, S * .82)], fill=OUT, width=int(S * .26))
    d.line([(S * .5, S * .14), (S * .5, S * .62), (S * .7, S * .82)], fill=(245, 245, 235, 255), width=int(S * .2))
    for y, c in ((.2, (220, 40, 40)), (.28, (40, 80, 200))):
        d.line([(S * .41, S * y), (S * .59, S * y)], fill=c + (255,), width=6)
    d.ellipse([S * .58, S * .7, S * .84, S * .92], fill=(220, 210, 130, 255), outline=OUT, width=5)               # yellowed toe
    for x in (.24, .78):
        d.arc([S * (x - .08), S * .06, S * (x + .08), S * .5], 100, 260, fill=(120, 200, 60, 255), width=5)         # stink
    return _shrink(im, size)


def clothes_dryer(size=64, open_door=False):
    """A white front-load dryer: control panel with a dial, the round porthole door (clothes tumbling inside) - or the
    door swung open."""
    im, d, S = _big(size)
    OUT = (40, 45, 55, 255)
    d.rounded_rectangle([S * .1, S * .06, S * .9, S * .96], 8, fill=(240, 242, 246, 255), outline=OUT, width=7)
    d.rectangle([S * .1, S * .06, S * .9, S * .22], fill=(200, 205, 215, 255), outline=OUT, width=5)
    d.ellipse([S * .66, S * .09, S * .8, S * .2], fill=(90, 90, 100, 255), outline=OUT, width=3)                 # dial
    for x in (.2, .28, .36):
        d.ellipse([S * x, S * .12, S * (x + .05), S * .17], fill=(80, 200, 120, 255))
    d.ellipse([S * .24, S * .32, S * .76, S * .84], fill=(170, 175, 185, 255), outline=OUT, width=7)
    if open_door:
        d.ellipse([S * .3, S * .38, S * .7, S * .78], fill=(60, 60, 70, 255))
        d.ellipse([S * .74, S * .34, S * .98, S * .82], fill=(170, 200, 230, 200), outline=OUT, width=6)          # door swung
    else:
        d.ellipse([S * .3, S * .38, S * .7, S * .78], fill=(150, 190, 225, 255))
        d.ellipse([S * .36, S * .5, S * .5, S * .62], fill=(220, 60, 60, 255))                                     # clothes inside
        d.ellipse([S * .48, S * .44, S * .62, S * .58], fill=(60, 120, 220, 255))
    return _shrink(im, size)


def lint_screen(size=64):
    """The dryer's lint trap pulled out: a white plastic frame, mesh, caked with a thick grey felt of lint."""
    im, d, S = _big(size)
    OUT = (60, 60, 70, 255)
    d.rounded_rectangle([S * .2, S * .06, S * .8, S * .94], 10, fill=(240, 240, 245, 255), outline=OUT, width=6)
    d.rectangle([S * .27, S * .14, S * .73, S * .86], fill=(170, 165, 170, 255))
    import random
    r = random.Random(3)
    for _ in range(40):
        x, y = r.uniform(.28, .72), r.uniform(.15, .85)
        d.ellipse([S * (x - .04), S * (y - .03), S * (x + .04), S * (y + .03)], fill=(200, 195, 200, 255))
    d.rectangle([S * .4, S * .02, S * .6, S * .08], fill=(240, 240, 245, 255), outline=OUT, width=4)            # pull tab
    return _shrink(im, size)


def lint_blanket(size=64):
    """A giant fuzzy wad of grey lint (with a stray blue thread and a hair)."""
    import math, random
    im, d, S = _big(size)
    r = random.Random(5)
    for _ in range(26):
        a, rr = r.uniform(0, 2 * math.pi), r.uniform(0, .26)
        x, y = .5 + rr * math.cos(a), .52 + rr * .8 * math.sin(a)
        s = r.uniform(.1, .18)
        d.ellipse([S * (x - s), S * (y - s * .8), S * (x + s), S * (y + s * .8)], fill=(175 + r.randint(-15, 15),) * 3 + (255,))
    d.line([(S * .2, S * .4), (S * .44, S * .5), (S * .7, S * .36)], fill=(60, 100, 220, 255), width=4)
    d.arc([S * .4, S * .5, S * .8, S * .8], 200, 330, fill=(60, 40, 30, 255), width=3)
    return _shrink(im, size)


def solo_cup(size=32):
    """A red party cup turned upside down (the shell game cup)."""
    im, d, S = _big(size)
    OUT = (80, 0, 10, 255)
    d.polygon([(S * .28, S * .1), (S * .72, S * .1), (S * .86, S * .9), (S * .14, S * .9)], fill=(220, 30, 40, 255))
    d.line([(S * .28, S * .1), (S * .72, S * .1), (S * .86, S * .9), (S * .14, S * .9), (S * .28, S * .1)], fill=OUT, width=6)
    d.rectangle([S * .14, S * .8, S * .86, S * .9], fill=(250, 250, 250, 255), outline=OUT, width=4)
    for y in (.3, .48):
        d.line([(S * .24, S * y), (S * .76, S * y)], fill=(180, 20, 30, 255), width=3)
    return _shrink(im, size)


def cardboard_table(size=64):
    """A cardboard box flipped over as a street table."""
    im, d, S = _big(size)
    OUT = (90, 60, 20, 255)
    d.polygon([(S * .04, S * .42), (S * .96, S * .42), (S * .9, S * .56), (S * .1, S * .56)], fill=(215, 170, 110, 255), outline=OUT)
    d.line([(S * .04, S * .42), (S * .96, S * .42), (S * .9, S * .56), (S * .1, S * .56), (S * .04, S * .42)], fill=OUT, width=6)
    d.rectangle([S * .1, S * .56, S * .9, S * .9], fill=(190, 145, 90, 255), outline=OUT, width=6)
    d.line([(S * .5, S * .56), (S * .5, S * .9)], fill=(160, 120, 70, 255), width=4)
    d.rectangle([S * .44, S * .62, S * .56, S * .7], fill=(230, 200, 150, 255))                                     # tape
    return _shrink(im, size)


def gold_watch(size=32):
    """A big gold wristwatch (the foe's item, under one of the cups)."""
    im, d, S = _big(size)
    OUT = (110, 70, 0, 255)
    d.rectangle([S * .38, S * .04, S * .62, S * .96], fill=(240, 190, 50, 255), outline=OUT, width=4)
    d.ellipse([S * .2, S * .26, S * .8, S * .74], fill=(250, 210, 70, 255), outline=OUT, width=6)
    d.ellipse([S * .3, S * .36, S * .7, S * .64], fill=(250, 250, 240, 255))
    d.line([(S * .5, S * .5), (S * .5, S * .4)], fill=OUT, width=3)
    d.line([(S * .5, S * .5), (S * .6, S * .52)], fill=OUT, width=3)
    return _shrink(im, size)


def dance_note(size=32):
    """A pink pair of beamed eighth notes with a white outline."""
    im, d, S = _big(size)
    OUT = (255, 255, 255, 255)
    C = (250, 80, 170, 255)
    for x in (.22, .62):
        d.ellipse([S * x, S * .64, S * (x + .2), S * .82], fill=C, outline=OUT, width=5)
        d.line([(S * (x + .18), S * .72), (S * (x + .18), S * .2)], fill=OUT, width=10)
        d.line([(S * (x + .18), S * .72), (S * (x + .18), S * .2)], fill=C, width=5)
    d.polygon([(S * .38, S * .14), (S * .82, S * .06), (S * .82, S * .18), (S * .38, S * .26)], fill=C, outline=OUT)
    return _shrink(im, size)


def claw_grabber(size=64, shut=False):
    """An arcade claw machine claw hanging from its cable: a chrome hub and three prongs, open wide or clamped shut."""
    im, d, S = _big(size)
    OUT = (30, 30, 40, 255)
    CH = (210, 215, 225, 255)
    d.line([(S * .5, 0), (S * .5, S * .3)], fill=(60, 60, 66, 255), width=6)                                        # cable
    d.rounded_rectangle([S * .38, S * .28, S * .62, S * .44], 6, fill=CH, outline=OUT, width=5)
    prongs = ((.3, .2, .44), (.5, .5, .5), (.7, .8, .56)) if not shut else ((.42, .44, .46), (.5, .5, .5), (.58, .56, .54))
    for x0, x1, x2 in prongs:
        tip_y = .86 if not shut else .78
        d.line([(S * x0 + (S * .08 if x0 < .5 else -S * .08 if x0 > .5 else 0), S * .42), (S * x1, S * .64), (S * x2, S * tip_y)], fill=OUT, width=10)
        d.line([(S * x0 + (S * .08 if x0 < .5 else -S * .08 if x0 > .5 else 0), S * .42), (S * x1, S * .64), (S * x2, S * tip_y)], fill=CH, width=6)
    return _shrink(im, size)
