

# ---- set 24, batch 2 (INSANE): Rip Space, Ghost Ride, Mind Blown, Bad Omen, Compactor -----------------------------

SMALL["="] = "...|###|...|###|...|..."


def _galaxy(d, S, box):
    """Paint a little piece of outer space into box (x0, y0, x1, y1): deep purple, a pink-blue nebula, stars."""
    import random
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(20, 10, 45, 255))
    d.ellipse([x0 + (x1 - x0) * .1, y0 + (y1 - y0) * .2, x0 + (x1 - x0) * .9, y0 + (y1 - y0) * .55], fill=(110, 40, 150, 255))
    d.ellipse([x0 + (x1 - x0) * .25, y0 + (y1 - y0) * .45, x0 + (x1 - x0) * .8, y0 + (y1 - y0) * .8], fill=(40, 90, 190, 255))
    r = random.Random(7)
    for _ in range(int((x1 - x0) * (y1 - y0) / (S * S) * 60) + 4):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        s = r.choice((2, 3, 5))
        d.ellipse([x - s, y - s, x + s, y + s], fill=(255, 255, 255, 255))


def space_zipper(size=64, opened=0):
    """A giant zipper running down the screen: opened 0 = zipped shut, 1 = the pull a third of the way down with a
    sliver of outer space showing, 2 = all the way down, a wide V of galaxy between the two rows of teeth."""
    im, d, S = _big(size)
    OUT = (20, 20, 26, 255)
    TEETH = (200, 170, 60, 255)
    pull_y = (.08, .38, .9)[opened]
    gap = (0, .1, .34)[opened]
    if opened:
        poly = [(S * .5, S * pull_y), (S * (.5 - gap), S * .02), (S * (.5 + gap), S * .02)]
        mask = Image.new("L", (S, S), 0)
        ImageDraw.Draw(mask).polygon(poly, fill=255)
        sp = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        _galaxy(ImageDraw.Draw(sp), S, (0, 0, S, S))
        im.paste(sp, (0, 0), mask)
    for k in range(24):
        y = .02 + k * .04
        if y < pull_y and opened:
            t = (pull_y - y) / max(pull_y - .02, .01)
            for sgn in (-1, 1):
                x = .5 + sgn * (gap * t + .02)
                d.rectangle([S * (x - .03), S * y, S * (x + .03), S * (y + .025)], fill=TEETH, outline=OUT, width=3)
        else:
            d.rectangle([S * (.47 if k % 2 else .5), S * y, S * (.5 if k % 2 else .53), S * (y + .03)], fill=TEETH, outline=OUT, width=3)
    d.rounded_rectangle([S * .42, S * (pull_y - .04), S * .58, S * (pull_y + .06)], 6, fill=(220, 220, 230, 255), outline=OUT, width=5)
    d.rounded_rectangle([S * .45, S * (pull_y + .05), S * .55, S * (pull_y + .2)], 8, fill=(200, 200, 210, 255), outline=OUT, width=5)
    d.ellipse([S * .48, S * (pull_y + .12), S * .52, S * (pull_y + .16)], fill=OUT)
    return _shrink(im, size)


def sheet_ghost(size=64):
    """A kid's Halloween ghost: a white bedsheet with two cut-out eye holes, wrinkles, the ragged hem."""
    im, d, S = _big(size)
    OUT = (60, 60, 80, 255)
    pts = [(S * .5, S * .06), (S * .78, S * .22), (S * .86, S * .9), (S * .76, S * .84), (S * .66, S * .94), (S * .56, S * .86),
           (S * .46, S * .95), (S * .36, S * .86), (S * .26, S * .94), (S * .14, S * .88), (S * .22, S * .22)]
    d.polygon(pts, fill=(250, 250, 255, 255))
    d.line(pts + [pts[0]], fill=OUT, width=7)
    for x in (.36, .56):
        d.ellipse([S * x, S * .3, S * (x + .1), S * .44], fill=(15, 15, 25, 255))
    for a, b in (((.3, .55), (.36, .8)), ((.66, .5), (.62, .78))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(200, 200, 220, 255), width=4)
    return _shrink(im, size)


def minivan(size=64, doors_open=True):
    """A beige soccer-mom minivan facing right, sliding door wide open and nobody in it (ghost riding the whip)."""
    im, d, S = _big(size)
    OUT = (30, 25, 20, 255)
    BODY = (220, 200, 160, 255)
    y0, y1 = .34, .72
    d.polygon([(S * .04, S * (y0 + .02)), (S * .62, S * y0), (S * .84, S * (y0 + .14)), (S * .96, S * (y0 + .2)), (S * .96, S * y1),
               (S * .04, S * y1)], fill=BODY, outline=OUT)
    d.line([(S * .04, S * (y0 + .02)), (S * .62, S * y0), (S * .84, S * (y0 + .14)), (S * .96, S * (y0 + .2)), (S * .96, S * y1),
            (S * .04, S * y1), (S * .04, S * (y0 + .02))], fill=OUT, width=6)
    for x0, x1 in ((.08, .24), (.62, .8)):
        d.rectangle([S * x0, S * (y0 + .05), S * x1, S * (y0 + .15)], fill=(110, 150, 190, 255), outline=OUT, width=4)
    if doors_open:
        d.rectangle([S * .3, S * (y0 + .04), S * .56, S * (y1 - .04)], fill=(40, 35, 40, 255), outline=OUT, width=4)   # empty inside
        d.rectangle([S * .14, S * (y0 + .04), S * .3, S * (y1 - .04)], fill=(205, 185, 145, 255), outline=OUT, width=4)  # slid door
    d.line([(S * .04, S * (y1 - .1)), (S * .96, S * (y1 - .1))], fill=(170, 150, 110, 255), width=4)
    d.rectangle([S * .9, S * (y0 + .26), S * .96, S * (y0 + .3)], fill=(255, 250, 200, 255))
    for x in (.2, .78):
        d.ellipse([S * (x - .08), S * (y1 - .08), S * (x + .08), S * (y1 + .08)], fill=(25, 25, 28, 255), outline=OUT, width=4)
        d.ellipse([S * (x - .03), S * (y1 - .03), S * (x + .03), S * (y1 + .03)], fill=(170, 170, 180, 255))
    return _shrink(im, size)


def math_board(size=64, text="2+2=4"):
    """A green classroom chalkboard in a wooden frame with a chalk tray, one line of chalk math (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 25, 10, 255)
    d.rectangle([S * .02, S * .16, S * .98, S * .8], fill=(150, 100, 50, 255), outline=OUT, width=7)
    d.rectangle([S * .08, S * .22, S * .92, S * .74], fill=(40, 90, 60, 255))
    d.rectangle([S * .06, S * .78, S * .94, S * .84], fill=(170, 120, 60, 255), outline=OUT, width=4)
    d.rectangle([S * .7, S * .74, S * .8, S * .78], fill=(250, 250, 245, 255))                                       # chalk
    d.line([(S * .14, S * .64), (S * .4, S * .66)], fill=(110, 150, 120, 255), width=4)                             # smudge
    im = _shrink(im, size)
    _big_text(im, text, (32, 28), (245, 245, 235, 255), scale=2, font=SMALL)
    return im


def question_mark(size=32):
    """A fat purple question mark with a white outline."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    _big_text(im, "?", (16, 16), (170, 80, 230, 255), scale=3)
    return im


def galaxy_burst(size=64):
    """MIND BLOWN: a ragged burst of outer space - purple, pink and blue swirls, stars, a white-hot centre."""
    import math
    im, d, S = _big(size)
    pts = []
    for k in range(22):
        a = k * 2 * math.pi / 22
        r = .47 if k % 2 == 0 else .33
        pts.append((S * (.5 + r * math.cos(a)), S * (.5 + r * math.sin(a))))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    sp = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sp)
    _galaxy(sd, S, (0, 0, S, S))
    for k in range(3):
        sd.arc([S * (.2 + k * .08), S * (.2 + k * .08), S * (.8 - k * .08), S * (.8 - k * .08)], k * 90, k * 90 + 200,
               fill=((255, 120, 220, 255), (120, 220, 255, 255), (255, 240, 140, 255))[k], width=8)
    sd.ellipse([S * .42, S * .42, S * .58, S * .58], fill=(255, 255, 255, 255))
    im.paste(sp, (0, 0), mask)
    d.line(pts + [pts[0]], fill=(255, 255, 255, 255), width=5)
    return _shrink(im, size)


def black_cat(size=64, step=0):
    """A black cat walking left to right, tail up, yellow eyes; step 0/1 swaps the legs."""
    im, d, S = _big(size)
    C = (25, 22, 30, 255)
    d.ellipse([S * .22, S * .42, S * .72, S * .68], fill=C)                                                             # body
    d.ellipse([S * .64, S * .3, S * .88, S * .52], fill=C)                                                              # head
    d.polygon([(S * .66, S * .34), (S * .68, S * .2), (S * .74, S * .32)], fill=C)
    d.polygon([(S * .78, S * .32), (S * .84, S * .2), (S * .86, S * .36)], fill=C)
    d.line([(S * .24, S * .5), (S * .1, S * .36), (S * .12, S * .14)], fill=C, width=int(S * .06))                     # tail
    legs = ((.3, .44), (.56, .7)) if step == 0 else ((.36, .38), (.62, .66))
    for a, b in legs:
        d.line([(S * a, S * .62), (S * (a - .04), S * .86)], fill=C, width=int(S * .06))
        d.line([(S * b, S * .62), (S * (b + .04), S * .86)], fill=C, width=int(S * .06))
    for x in (.72, .8):
        d.ellipse([S * x, S * .37, S * (x + .05), S * .43], fill=(250, 220, 40, 255))
    return _shrink(im, size)


def hand_mirror(size=64, cracked=False):
    """A pink hand mirror (oval glass, handle) - or cracked right across."""
    im, d, S = _big(size)
    OUT = (60, 20, 40, 255)
    d.line([(S * .5, S * .62), (S * .5, S * .96)], fill=OUT, width=int(S * .12))
    d.line([(S * .5, S * .62), (S * .5, S * .96)], fill=(240, 120, 170, 255), width=int(S * .08))
    d.ellipse([S * .2, S * .04, S * .8, S * .66], fill=(240, 120, 170, 255), outline=OUT, width=7)
    d.ellipse([S * .27, S * .1, S * .73, S * .6], fill=(200, 230, 250, 255), outline=OUT, width=4)
    d.line([(S * .35, S * .2), (S * .45, S * .14)], fill=(255, 255, 255, 255), width=5)
    if cracked:
        for a, b in (((.5, .34), (.3, .18)), ((.5, .34), (.7, .14)), ((.5, .34), (.34, .56)), ((.5, .34), (.68, .52)), ((.5, .34), (.72, .34))):
            d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(40, 40, 60, 255), width=4)
    return _shrink(im, size)


def falling_star(size=64):
    """A huge shooting star coming down from the top-right: a fat gold star with a white core and a long rainbow trail."""
    import math
    im, d, S = _big(size)
    for k, c in enumerate(((255, 120, 200), (255, 220, 80), (120, 220, 255))):
        o = (k - 1) * .05
        d.line([(S * (.62 + o), S * (.38 - o)), (S * (.98 + o), S * (.02 - o))], fill=c + (220,), width=int(S * .06))
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        r = .3 if k % 2 == 0 else .13
        pts.append((S * (.4 + r * math.cos(a)), S * (.6 + r * math.sin(a))))
    _outline_poly(d, pts, (255, 220, 50, 255), (160, 100, 0, 255), 8)
    d.ellipse([S * .34, S * .54, S * .46, S * .66], fill=(255, 255, 230, 255))
    return _shrink(im, size)


def compactor_plate(size=64):
    """One wall of a junkyard compactor: a riveted steel plate with yellow-black hazard stripes and a hydraulic
    piston sticking out the back (the left side)."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rectangle([S * .02, S * .44, S * .4, S * .56], fill=(170, 175, 185, 255), outline=OUT, width=6)              # piston
    d.rectangle([S * .4, S * .04, S * .72, S * .96], fill=(120, 125, 135, 255), outline=OUT, width=8)
    for k in range(6):
        y = .1 + k * .15
        d.polygon([(S * .66, S * y), (S * .72, S * (y - .06)), (S * .72, S * (y + .02)), (S * .66, S * (y + .08))], fill=(250, 200, 30, 255))
    d.line([(S * .72, S * .04), (S * .72, S * .96)], fill=OUT, width=6)
    for y in (.12, .5, .88):
        for x in (.46, .6):
            d.ellipse([S * x, S * (y - .02), S * (x + .04), S * (y + .02)], fill=(200, 205, 215, 255), outline=OUT, width=2)
    return _shrink(im, size)


def junk_cube(size=64):
    """A crushed cube of compacted junk: dented metal, a squashed hubcap, a sneaker sticking out, a soda can."""
    im, d, S = _big(size)
    OUT = (20, 20, 24, 255)
    d.polygon([(S * .14, S * .3), (S * .5, S * .14), (S * .9, S * .28), (S * .9, S * .82), (S * .52, S * .96), (S * .14, S * .82)], fill=(110, 110, 120, 255))
    d.polygon([(S * .14, S * .3), (S * .5, S * .44), (S * .52, S * .96), (S * .14, S * .82)], fill=(140, 140, 150, 255))
    d.polygon([(S * .14, S * .3), (S * .5, S * .14), (S * .9, S * .28), (S * .5, S * .44)], fill=(170, 170, 180, 255))
    for pts in (((.14, .3), (.5, .14), (.9, .28), (.9, .82), (.52, .96), (.14, .82), (.14, .3)), ((.14, .3), (.5, .44), (.9, .28)), ((.5, .44), (.52, .96))):
        d.line([(S * x, S * y) for x, y in pts], fill=OUT, width=6)
    d.ellipse([S * .2, S * .5, S * .38, S * .66], fill=(210, 210, 220, 255), outline=OUT, width=4)                 # hubcap
    d.rectangle([S * .62, S * .5, S * .74, S * .7], fill=(220, 40, 40, 255), outline=OUT, width=3)                 # can
    d.polygon([(S * .64, S * .24), (S * .84, S * .2), (S * .86, S * .3), (S * .7, S * .34)], fill=(250, 250, 250, 255), outline=OUT)   # sneaker
    for a, b in (((.3, .74), (.44, .8)), ((.6, .78), (.8, .72))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(80, 80, 88, 255), width=4)                     # dents
    return _shrink(im, size)
