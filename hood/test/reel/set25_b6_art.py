

# ---- set 25, batch 6: Thumbtacks, Copy Paste, Receipts, Max Out, Hustle ------------------------------------------------

def thumbtack(size=32):
    """A red push pin / thumbtack, point down."""
    im, d, S = _big(size)
    OUT = (80, 0, 0, 255)
    d.line([(S * .5, S * .56), (S * .5, S * .96)], fill=(190, 195, 205, 255), width=int(S * .08))
    d.rounded_rectangle([S * .26, S * .44, S * .74, S * .58], 6, fill=(220, 30, 30, 255), outline=OUT, width=4)
    d.rectangle([S * .38, S * .2, S * .62, S * .46], fill=(220, 30, 30, 255), outline=OUT, width=4)
    d.ellipse([S * .22, S * .04, S * .78, S * .26], fill=(240, 50, 50, 255), outline=OUT, width=4)
    d.ellipse([S * .32, S * .08, S * .44, S * .14], fill=(255, 180, 180, 255))
    return _shrink(im, size)


def tack_box(size=64):
    """A little cardboard box of thumbtacks, flap open, TACKS printed on it (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (80, 50, 20, 255)
    d.rectangle([S * .16, S * .4, S * .84, S * .86], fill=(210, 165, 105, 255), outline=OUT, width=6)
    d.polygon([(S * .16, S * .4), (S * .84, S * .4), (S * .74, S * .24), (S * .26, S * .24)], fill=(190, 145, 90, 255), outline=OUT)
    for x in (.34, .48, .62):
        d.ellipse([S * (x - .05), S * .3, S * (x + .05), S * .38], fill=(220, 30, 30, 255), outline=(80, 0, 0, 255), width=3)
    im = _shrink(im, size)
    return _texted(im, [("TACKS", (32, 36))], (255, 255, 255, 255), (120, 70, 20, 255))


def photocopier(size=64):
    """An office photocopier: grey body, the lid, a control panel with a green start button, the output tray."""
    im, d, S = _big(size)
    OUT = (30, 30, 36, 255)
    d.rectangle([S * .12, S * .3, S * .88, S * .94], fill=(210, 212, 218, 255), outline=OUT, width=7)
    d.rectangle([S * .1, S * .2, S * .9, S * .32], fill=(180, 182, 190, 255), outline=OUT, width=6)
    d.rectangle([S * .56, S * .38, S * .84, S * .5], fill=(90, 92, 100, 255), outline=OUT, width=4)
    d.ellipse([S * .74, S * .4, S * .82, S * .48], fill=(60, 200, 90, 255))
    d.rectangle([S * .02, S * .58, S * .14, S * .64], fill=(170, 172, 180, 255), outline=OUT, width=4)          # out tray
    d.rectangle([S * .2, S * .6, S * .8, S * .86], fill=(195, 197, 205, 255), outline=(150, 150, 160, 255), width=4)
    return _shrink(im, size)


def copy_page(size=32, quality=0):
    """A sheet of paper out of the copier: 0 = blank, 1 = smudged grey mess, 2 = a crisp perfect star icon."""
    im, d, S = _big(size)
    OUT = (60, 60, 70, 255)
    d.rectangle([S * .18, S * .06, S * .82, S * .94], fill=(250, 250, 250, 255), outline=OUT, width=4)
    if quality == 1:
        for x, y in ((.3, .3), (.5, .5), (.42, .66), (.6, .3)):
            d.ellipse([S * x, S * y, S * (x + .2), S * (y + .14)], fill=(120, 120, 130, 160))
    elif quality == 2:
        import math
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            r = .26 if k % 2 == 0 else .11
            pts.append((S * (.5 + r * math.cos(a)), S * (.5 + r * math.sin(a))))
        d.polygon(pts, fill=(20, 20, 24, 255))
    return _shrink(im, size)


def receipt_printer(size=64):
    """A black point-of-sale receipt printer with paper feeding out the top."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rounded_rectangle([S * .14, S * .5, S * .86, S * .94], 10, fill=(40, 40, 46, 255), outline=OUT, width=7)
    d.rectangle([S * .3, S * .44, S * .7, S * .54], fill=(25, 25, 28, 255), outline=OUT, width=4)
    d.rectangle([S * .34, S * .1, S * .66, S * .5], fill=(250, 250, 245, 255), outline=(150, 150, 150, 255), width=3)
    for y in (.18, .26, .34, .42):
        d.line([(S * .38, S * y), (S * .62, S * y)], fill=(170, 170, 170, 255), width=3)
    d.ellipse([S * .74, S * .58, S * .8, S * .64], fill=(60, 200, 90, 255))
    return _shrink(im, size)


def long_receipt(size=64):
    """A ridiculously long receipt, curling at the bottom - CVS long."""
    im, d, S = _big(size)
    d.rectangle([S * .4, S * .0, S * .6, S * .86], fill=(250, 250, 245, 255), outline=(150, 150, 150, 255), width=3)
    d.arc([S * .36, S * .76, S * .7, S * 1.0], 0, 270, fill=(250, 250, 245, 255), width=int(S * .06))
    for k in range(18):
        y = .04 + k * .045
        d.line([(S * .43, S * y), (S * (.5 + (k % 3) * .03), S * y)], fill=(160, 160, 160, 255), width=3)
    return _shrink(im, size)


def dumbbell(size=32):
    """A chrome dumbbell."""
    im, d, S = _big(size)
    OUT = (30, 30, 36, 255)
    d.rectangle([S * .3, S * .44, S * .7, S * .56], fill=(200, 205, 215, 255), outline=OUT, width=4)
    for x in (.12, .7):
        d.rounded_rectangle([S * x, S * .28, S * (x + .18), S * .72], 4, fill=(60, 60, 66, 255), outline=OUT, width=5)
    return _shrink(im, size)


def oly_barbell(size=64):
    """A loaded Olympic barbell: a long bar with big red plates on each end."""
    im, d, S = _big(size)
    OUT = (20, 20, 24, 255)
    d.rectangle([S * .02, S * .47, S * .98, S * .53], fill=(200, 205, 215, 255), outline=OUT, width=3)
    for x in (.08, .8):
        d.rounded_rectangle([S * x, S * .22, S * (x + .1), S * .78], 6, fill=(200, 30, 30, 255), outline=OUT, width=5)
        d.rounded_rectangle([S * (x + (.1 if x < .5 else -.06)), S * .3, S * (x + (.16 if x < .5 else 0)), S * .7], 4, fill=(40, 40, 46, 255), outline=OUT, width=4)
    return _shrink(im, size)


def vending_machine(size=64):
    """A red soda vending machine: rows of cans behind glass, the coin slot and the dispenser."""
    im, d, S = _big(size)
    OUT = (40, 0, 0, 255)
    d.rectangle([S * .14, S * .04, S * .86, S * .96], fill=(210, 30, 30, 255), outline=OUT, width=7)
    d.rectangle([S * .2, S * .1, S * .62, S * .7], fill=(150, 200, 230, 255), outline=OUT, width=5)
    for r in range(4):
        for c in range(3):
            d.rectangle([S * (.24 + c * .13), S * (.14 + r * .14), S * (.32 + c * .13), S * (.24 + r * .14)],
                        fill=((240, 240, 240), (40, 90, 220), (250, 200, 40))[(r + c) % 3] + (255,), outline=OUT, width=2)
    d.rectangle([S * .68, S * .2, S * .8, S * .4], fill=(60, 60, 66, 255), outline=OUT, width=4)
    d.rectangle([S * .22, S * .76, S * .6, S * .88], fill=(30, 30, 34, 255), outline=OUT, width=4)
    return _shrink(im, size)


def moth_wallet(size=64):
    """A brown leather wallet flopped open - completely empty - with a little moth fluttering out."""
    im, d, S = _big(size)
    OUT = (50, 30, 10, 255)
    d.rounded_rectangle([S * .06, S * .44, S * .5, S * .9], 8, fill=(140, 90, 50, 255), outline=OUT, width=6)
    d.rounded_rectangle([S * .5, S * .44, S * .94, S * .9], 8, fill=(150, 100, 55, 255), outline=OUT, width=6)
    d.rectangle([S * .12, S * .52, S * .44, S * .62], fill=(100, 60, 30, 255))
    d.rectangle([S * .56, S * .52, S * .88, S * .62], fill=(100, 60, 30, 255))
    for pts in (((.62, .3), (.48, .12), (.56, .34)), ((.62, .3), (.76, .12), (.68, .34))):
        _outline_poly(d, [(S * x, S * y) for x, y in pts], (200, 180, 140, 255), (60, 50, 30, 255), 4)
    d.ellipse([S * .58, S * .24, S * .66, S * .38], fill=(120, 100, 70, 255))
    return _shrink(im, size)
