

# ---- set 26, batch 6: Finesse, Ext. Cord, Two-by-Four, Kick Back, Slow Jam ----------------------------------------------

def lemme_bubble(size=64):
    """A white speech bubble: LEMME / SEE THAT (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.rounded_rectangle([S * .02, S * .22, S * .98, S * .74], 26, fill=(255, 255, 255, 255), outline=OUT, width=8)
    d.polygon([(S * .22, S * .7), (S * .12, S * .94), (S * .4, S * .72)], fill=(255, 255, 255, 255))
    d.line([(S * .22, S * .74), (S * .12, S * .94), (S * .4, S * .74)], fill=OUT, width=7)
    im = _shrink(im, size)
    return _texted(im, [("LEMME", (32, 19)), ("SEE THAT", (32, 30))], (20, 20, 25, 255), (255, 255, 255, 255))


def fresh_snapback(size=64):
    """A brand-new snapback: black crown, flat red brim with the gold sticker still on it, the button on top."""
    im, d, S = _big(size)
    OUT = (15, 10, 10, 255)
    d.chord([S * .12, S * .14, S * .84, S * .9], 180, 360, fill=(30, 30, 40, 255), outline=OUT, width=7)
    d.rectangle([S * .12, S * .5, S * .84, S * .6], fill=(30, 30, 40, 255), outline=OUT, width=6)
    d.line([(S * .48, S * .16), (S * .48, S * .5)], fill=(70, 70, 85, 255), width=4)                             # panel seam
    d.ellipse([S * .44, S * .1, S * .52, S * .18], fill=(30, 30, 40, 255), outline=OUT, width=3)                 # button
    d.polygon([(S * .5, S * .56), (S * .98, S * .56), (S * .98, S * .68), (S * .5, S * .66)], fill=(220, 30, 40, 255), outline=OUT)
    d.line([(S * .5, S * .56), (S * .98, S * .56), (S * .98, S * .68), (S * .5, S * .66)], fill=OUT, width=6)    # flat brim
    d.ellipse([S * .7, S * .57, S * .82, S * .66], fill=(250, 210, 50, 255), outline=(150, 110, 0, 255), width=3)  # the sticker
    d.arc([S * .2, S * .22, S * .56, S * .56], 200, 260, fill=(110, 110, 130, 255), width=5)                      # shine
    return _shrink(im, size)


def ext_cord(size=64, swung=False):
    """The orange extension cord: coiled up with the plug hanging out - or swung out long, folded over double."""
    im, d, S = _big(size)
    OUT = (90, 30, 0, 255)
    OR = (250, 130, 20, 255)
    if not swung:
        for k in range(4):
            r = .3 - k * .03
            d.ellipse([S * (.5 - r), S * (.48 - r * .9), S * (.5 + r), S * (.48 + r * .9)], outline=OUT, width=13)
            d.ellipse([S * (.5 - r), S * (.48 - r * .9), S * (.5 + r), S * (.48 + r * .9)], outline=OR, width=8)
        d.line([(S * .74, S * .62), (S * .82, S * .84)], fill=OUT, width=12)
        d.line([(S * .74, S * .62), (S * .82, S * .84)], fill=OR, width=7)
        plug = (.82, .84)
    else:                                                                       # folded double: the loop is the business end
        for off in (-.035, .035):
            pts = [(S * (.08 + t * .84), S * (.5 + off + .22 * __import__("math").sin(t * 5.2))) for t in [i / 24 for i in range(25)]]
            d.line(pts, fill=OUT, width=12, joint="curve")
            d.line(pts, fill=OR, width=7, joint="curve")
        d.ellipse([S * .86, S * .2, S * .98, S * .64], outline=OUT, width=12)
        d.ellipse([S * .86, S * .2, S * .98, S * .64], outline=OR, width=7)
        plug = (.08, .5)
    px, py = plug
    d.rectangle([S * (px - .06), S * (py - .02), S * (px + .06), S * (py + .1)], fill=(240, 240, 235, 255), outline=OUT, width=4)
    for x in (-.03, .02):                                                       # the prongs
        d.rectangle([S * (px + x), S * (py + .1), S * (px + x + .015), S * (py + .16)], fill=(200, 200, 200, 255), outline=OUT, width=2)
    return _shrink(im, size)


def tape_measure(size=64):
    """A yellow tape measure, the tape pulled out long to the right with tick marks and the little hook."""
    im, d, S = _big(size)
    OUT = (40, 30, 0, 255)
    d.rectangle([S * .3, S * .56, S * .96, S * .66], fill=(255, 235, 90, 255), outline=OUT, width=4)
    for k in range(16):                                                         # ticks
        x = .33 + k * .04
        d.line([(S * x, S * .56), (S * x, S * (.6 if k % 4 else .63))], fill=OUT, width=3)
    d.rectangle([S * .94, S * .5, S * .98, S * .7], fill=(170, 170, 180, 255), outline=OUT, width=3)          # the hook
    d.rounded_rectangle([S * .02, S * .36, S * .38, S * .76], 12, fill=(250, 200, 30, 255), outline=OUT, width=7)
    d.ellipse([S * .1, S * .44, S * .3, S * .66], fill=(60, 60, 66, 255), outline=OUT, width=4)
    d.rectangle([S * .14, S * .28, S * .26, S * .38], fill=(60, 60, 66, 255), outline=OUT, width=4)            # the lock button
    return _shrink(im, size)


def two_by_four(size=64):
    """A 2x4: a long pale pine board on the diagonal, wood grain, a knot, and a bent nail sticking out the end."""
    im, d, S = _big(size)
    OUT = (90, 55, 20, 255)
    pts = [(S * .06, S * .82), (S * .82, S * .06), (S * .96, S * .2), (S * .2, S * .96)]
    _outline_poly(d, pts, (235, 195, 130, 255), OUT, 7)
    d.polygon([(S * .82, S * .06), (S * .96, S * .2), (S * .9, S * .2), (S * .78, S * .1)], fill=(210, 160, 95, 255))   # end grain
    for k in range(3):                                                          # the grain
        o = .05 + k * .04
        d.line([(S * (.14 + o), S * (.82 + o * .2)), (S * (.84 + o * .2), S * (.12 + o))], fill=(200, 150, 90, 255), width=3)
    d.ellipse([S * .42, S * .5, S * .52, S * .58], fill=(160, 100, 50, 255), outline=OUT, width=3)             # knot
    d.line([(S * .88, S * .12), (S * .98, S * .02), (S * .98, S * .1)], fill=(150, 150, 160, 255), width=5)      # bent nail
    return _shrink(im, size)


def wood_chip(n=16):
    """A splinter (alpha only): a thin jagged sliver."""
    return _alpha(n, n, lambda x, y: 1 if abs((x - 8) - (y - 8) * .35) < 1.3 - abs(y - 8) * .07 and 1 < y < 15 else 0)


def recliner(size=64, stage=0):
    """A brown leather recliner. 0 = upright, 1 = footrest popped out, 2 = laid all the way back."""
    im, d, S = _big(size)
    OUT = (40, 20, 10, 255)
    BR, HI = (130, 75, 40, 255), (170, 105, 60, 255)
    back = [((.1, .08), (.44, .08), (.44, .62), (.1, .62)), ((.02, .2), (.34, .1), (.44, .62), (.1, .66)),
            ((-.02, .5), (.06, .3), (.44, .56), (.4, .68))][stage]
    _outline_poly(d, [(S * x, S * y) for x, y in back], BR, OUT, 7)
    a, b_, c, e = back                                                          # tufted padding: two seams across the back
    lerp = lambda p, q, t: (S * (p[0] + (q[0] - p[0]) * t), S * (p[1] + (q[1] - p[1]) * t))
    for t in (.33, .66):
        d.line([lerp(a, e, t), lerp(b_, c, t)], fill=HI, width=5)
    d.rounded_rectangle([S * .3, S * .52, S * .72, S * .7], 10, fill=HI, outline=OUT, width=7)                  # the seat cushion
    d.rounded_rectangle([S * .26, S * .44, S * .7, S * .54], 8, fill=BR, outline=OUT, width=6)                  # armrest
    d.rectangle([S * .3, S * .7, S * .7, S * .86], fill=(100, 55, 30, 255), outline=OUT, width=6)               # base
    d.line([(S * .66, S * .56), (S * .76, S * .5)], fill=(60, 60, 66, 255), width=6)                             # the lever
    if stage:
        foot = ((.7, .66), (.96, .58), (.98, .7), (.72, .78)) if stage == 1 else ((.7, .6), (.98, .54), (.98, .66), (.72, .72))
        _outline_poly(d, [(S * x, S * y) for x, y in foot], HI, OUT, 6)
    return _shrink(im, size)


def jar_candle(size=32, lit=True):
    """A red jar candle - flame on top when lit."""
    im, d, S = _big(size)
    OUT = (60, 10, 20, 255)
    d.rounded_rectangle([S * .22, S * .44, S * .78, S * .96], 8, fill=(200, 40, 60, 255), outline=OUT, width=6)
    d.rectangle([S * .22, S * .56, S * .78, S * .66], fill=(255, 200, 210, 255))                                # the label band
    if lit:
        d.ellipse([S * .36, S * .06, S * .64, S * .46], fill=(255, 170, 40, 255))
        d.ellipse([S * .43, S * .2, S * .57, S * .44], fill=(255, 250, 200, 255))
    d.line([(S * .5, S * .38), (S * .5, S * .46)], fill=OUT, width=4)
    return _shrink(im, size)


def love_note(n=16):
    """A music note with a heart for a head (alpha only)."""
    def f(x, y):
        heart = ((x - 5) ** 2 + (y - 11) ** 2 < 6.5 or (x - 9) ** 2 + (y - 11) ** 2 < 6.5) and y < 13 or (y >= 12 and abs(x - 7) < 15 - y)
        stem = 10 <= x <= 11 and 1 <= y <= 11
        flag = 11 <= x <= 14 and 1 <= y <= 3 + (x - 11) * .4
        return 1 if heart or stem or flag else 0
    return _alpha(n, n, f)
