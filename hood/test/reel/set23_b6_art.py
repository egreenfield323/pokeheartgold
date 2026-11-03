

# ---- set 23, batch 6: Gas Up, Door Kick, Getaway, Bug Zapper, Split Bill ---------------------------------------

def gas_pump(size=64, amount="$5.00"):
    """A red gas pump: the price screen reading `amount`, the octane buttons, the hose looping out the right side
    (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (30, 10, 10, 255)
    d.rectangle([S * .08, S * .9, S * .7, S * .98], fill=(120, 120, 130, 255), outline=OUT, width=5)            # island
    d.rounded_rectangle([S * .12, S * .06, S * .66, S * .92], 10, fill=(210, 30, 30, 255), outline=OUT, width=8)
    d.rectangle([S * .18, S * .14, S * .6, S * .38], fill=(20, 30, 20, 255), outline=OUT, width=5)              # screen
    for k, c in enumerate(((240, 240, 240), (240, 200, 40), (60, 180, 80))):
        d.rectangle([S * (.2 + k * .13), S * .46, S * (.3 + k * .13), S * .54], fill=c + (255,), outline=OUT, width=3)
    d.rectangle([S * .22, S * .62, S * .56, S * .84], fill=(250, 250, 250, 255), outline=OUT, width=4)          # logo panel
    d.line([(S * .3, S * .7), (S * .48, S * .7)], fill=(210, 30, 30, 255), width=6)
    d.line([(S * .3, S * .77), (S * .44, S * .77)], fill=(210, 30, 30, 255), width=6)
    d.arc([S * .56, S * .3, S * .98, S * .9], 270, 90, fill=OUT, width=10)
    d.arc([S * .56, S * .3, S * .98, S * .9], 270, 90, fill=(40, 40, 46, 255), width=6)                         # hose
    im = _shrink(im, size)
    col = (255, 60, 40, 255) if amount.startswith("$99") else (120, 255, 140, 255)
    return _texted(im, [(amount, (25, 13))], col, (20, 30, 20, 255))


def gas_nozzle(size=64):
    """A gas pump nozzle: black grip and trigger guard, the silver spout pointing left, a bit of hose."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.line([(S * .74, S * .5), (S * .98, S * .3)], fill=(40, 40, 46, 255), width=int(S * .1))                    # hose
    d.polygon([(S * .4, S * .36), (S * .78, S * .36), (S * .82, S * .58), (S * .44, S * .58)], fill=(40, 40, 46, 255), outline=OUT)
    d.line([(S * .4, S * .36), (S * .78, S * .36), (S * .82, S * .58), (S * .44, S * .58), (S * .4, S * .36)], fill=OUT, width=6)
    d.arc([S * .44, S * .46, S * .76, S * .86], 0, 180, fill=OUT, width=8)                                        # guard
    d.rectangle([S * .54, S * .56, S * .62, S * .72], fill=(220, 40, 40, 255), outline=OUT, width=3)             # trigger
    d.polygon([(S * .42, S * .4), (S * .04, S * .5), (S * .04, S * .56), (S * .42, S * .52)], fill=(200, 205, 215, 255), outline=OUT)
    d.line([(S * .42, S * .4), (S * .04, S * .5), (S * .04, S * .56), (S * .42, S * .52)], fill=OUT, width=5)      # spout
    return _shrink(im, size)


def front_door(size=64, flying=False):
    """A blue front door in its white frame: raised panels, a brass knob and knocker, a peephole - or (flying)
    the door alone, off its hinges, hinge plates showing."""
    im, d, S = _big(size)
    OUT = (20, 20, 40, 255)
    if not flying:
        d.rectangle([S * .12, S * .02, S * .88, S * .98], fill=(245, 245, 240, 255), outline=OUT, width=7)       # frame
    d.rectangle([S * .2, S * .08, S * .8, S * .98], fill=(40, 80, 170, 255), outline=OUT, width=7)
    for y0, y1 in ((.16, .46), (.56, .9)):
        d.rectangle([S * .28, S * y0, S * .48, S * y1], fill=(60, 100, 190, 255), outline=(20, 40, 110, 255), width=5)
        d.rectangle([S * .52, S * y0, S * .72, S * y1], fill=(60, 100, 190, 255), outline=(20, 40, 110, 255), width=5)
    d.ellipse([S * .64, S * .5, S * .74, S * .6], fill=(240, 190, 50, 255), outline=OUT, width=4)                # knob
    d.ellipse([S * .46, S * .2, S * .54, S * .28], fill=(30, 30, 40, 255), outline=(240, 190, 50, 255), width=3)   # peephole
    d.arc([S * .42, S * .3, S * .58, S * .44], 0, 180, fill=(240, 190, 50, 255), width=6)                         # knocker
    if flying:
        for y in (.2, .76):
            d.rectangle([S * .17, S * y, S * .23, S * (y + .08)], fill=(170, 170, 180, 255), outline=OUT, width=3)
    return _shrink(im, size)


def rental_scooter(size=64):
    """A green rental e-scooter seen from the side, facing right: tall stem, handlebar, low deck, two small
    wheels, a QR plate on the stem."""
    im, d, S = _big(size)
    OUT = (10, 30, 15, 255)
    G = (60, 200, 90, 255)
    d.line([(S * .14, S * .82), (S * .78, S * .82)], fill=OUT, width=int(S * .1))
    d.line([(S * .14, S * .82), (S * .78, S * .82)], fill=(40, 40, 46, 255), width=int(S * .06))                # deck
    d.line([(S * .76, S * .82), (S * .68, S * .14)], fill=OUT, width=int(S * .08))
    d.line([(S * .76, S * .82), (S * .68, S * .14)], fill=G, width=int(S * .05))                                 # stem
    d.line([(S * .56, S * .14), (S * .84, S * .12)], fill=OUT, width=10)                                          # handlebar
    d.rectangle([S * .66, S * .36, S * .78, S * .48], fill=(250, 250, 250, 255), outline=OUT, width=4)          # QR plate
    for x in (.18, .78):
        d.ellipse([S * (x - .09), S * .78, S * (x + .09), S * .96], fill=(30, 30, 34, 255), outline=OUT, width=5)
        d.ellipse([S * (x - .03), S * .84, S * (x + .03), S * .9], fill=G)
    return _shrink(im, size)


def battery_low(size=32, full=False):
    """A battery icon: red with one sliver of charge - or full green (turbo)."""
    im, d, S = _big(size)
    OUT = (20, 20, 20, 255)
    d.rounded_rectangle([S * .06, S * .26, S * .84, S * .74], 6, fill=(250, 250, 250, 255), outline=OUT, width=7)
    d.rectangle([S * .84, S * .4, S * .96, S * .6], fill=OUT)
    if full:
        d.rectangle([S * .14, S * .34, S * .76, S * .66], fill=(60, 220, 80, 255))
    else:
        d.rectangle([S * .14, S * .34, S * .24, S * .66], fill=(230, 30, 30, 255))
    return _shrink(im, size)


def loot_sack(size=32):
    """A tied canvas money sack with a big green $ on it."""
    im, d, S = _big(size)
    OUT = (50, 35, 15, 255)
    d.ellipse([S * .12, S * .3, S * .88, S * .96], fill=(210, 180, 120, 255), outline=OUT, width=7)
    d.polygon([(S * .36, S * .32), (S * .28, S * .06), (S * .5, S * .2), (S * .72, S * .06), (S * .64, S * .32)], fill=(210, 180, 120, 255), outline=OUT)
    d.rectangle([S * .34, S * .26, S * .66, S * .34], fill=(120, 80, 40, 255))
    im = _shrink(im, size)
    _big_text(im, "$", (16, 21), (40, 160, 60, 255), scale=1)
    return im


def bug_zapper(size=64, lit=True):
    """A porch bug zapper hanging from its hook: a black wire cage round a glowing purple-blue UV tube."""
    im, d, S = _big(size)
    OUT = (10, 10, 16, 255)
    d.arc([S * .42, S * .0, S * .58, S * .14], 180, 360, fill=OUT, width=6)                                       # hook
    d.line([(S * .5, S * .07), (S * .5, S * .16)], fill=OUT, width=6)
    d.rounded_rectangle([S * .24, S * .14, S * .76, S * .24], 6, fill=(40, 40, 46, 255), outline=OUT, width=5)
    d.rounded_rectangle([S * .24, S * .84, S * .76, S * .94], 6, fill=(40, 40, 46, 255), outline=OUT, width=5)
    glow = (140, 60, 255, 255) if lit else (80, 70, 100, 255)
    d.rectangle([S * .3, S * .24, S * .7, S * .84], fill=glow[:3] + (200,))
    d.rounded_rectangle([S * .42, S * .26, S * .58, S * .82], 8, fill=(230, 220, 255, 255) if lit else (120, 110, 140, 255), outline=glow, width=4)
    for k in range(7):
        x = .3 + k * .066
        d.line([(S * x, S * .24), (S * x, S * .84)], fill=(30, 30, 36, 255), width=3)                            # cage wires
    for y in (.4, .6):
        d.line([(S * .28, S * y), (S * .72, S * y)], fill=(30, 30, 36, 255), width=3)
    return _shrink(im, size)


def porch_moth(size=32):
    """A fuzzy brown moth, wings spread."""
    im, d, S = _big(size)
    OUT = (40, 30, 15, 255)
    for pts in (((.5, .5), (.06, .2), (.14, .7)), ((.5, .5), (.94, .2), (.86, .7))):
        _outline_poly(d, [(S * x, S * y) for x, y in pts], (180, 150, 100, 255), OUT, 6)
    for x in (.24, .76):
        d.ellipse([S * (x - .06), S * .36, S * (x + .06), S * .48], fill=(110, 80, 50, 255))
    d.ellipse([S * .42, S * .3, S * .58, S * .8], fill=(120, 90, 55, 255), outline=OUT, width=5)
    d.line([(S * .46, S * .32), (S * .36, S * .14)], fill=OUT, width=3)
    d.line([(S * .54, S * .32), (S * .64, S * .14)], fill=OUT, width=3)
    return _shrink(im, size)


def check_folder(size=64):
    """A restaurant check presenter, open: the black folder with the bill clipped in - TOTAL / $200 (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rounded_rectangle([S * .04, S * .14, S * .96, S * .86], 8, fill=(30, 30, 34, 255), outline=OUT, width=7)
    d.line([(S * .5, S * .16), (S * .5, S * .84)], fill=(70, 70, 76, 255), width=5)
    d.rectangle([S * .5, S * .2, S * .96, S * .8], fill=(250, 250, 245, 255), outline=OUT, width=4)             # the bill
    for y in (.56, .64, .72):
        d.line([(S * .56, S * y), (S * .9, S * y)], fill=(170, 170, 170, 255), width=3)
    d.rectangle([S * .12, S * .3, S * .4, S * .5], fill=(240, 240, 235, 255), outline=OUT, width=4)            # a card slot
    im = _shrink(im, size)
    return _texted(im, [("TOTAL", (47, 17)), ("$200", (47, 26))], (20, 20, 25, 255), (250, 250, 245, 255))


def receipt_half(size=32, right=False):
    """Half of a torn receipt: white paper, grey print lines, a ragged torn edge."""
    im, d, S = _big(size)
    OUT = (60, 60, 66, 255)
    pts = [(S * .2, S * .04), (S * .8, S * .04)]
    for k in range(8):
        pts.append((S * (.8 if k % 2 == 0 else .7), S * (.1 + k * .11)))
    pts += [(S * .2, S * .96)]
    if right:
        pts = [(S - x, y) for x, y in pts]
    _outline_poly(d, pts, (250, 250, 245, 255), OUT, 5)
    for y in (.2, .32, .44, .56, .7):
        x0, x1 = (.28, .6) if not right else (.4, .72)
        d.line([(S * x0, S * y), (S * x1, S * y)], fill=(170, 170, 170, 255), width=4)
    return _shrink(im, size)
