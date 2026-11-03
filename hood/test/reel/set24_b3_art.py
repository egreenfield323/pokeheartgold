

# ---- set 24, batch 3: Flamin Hot, Air Strike, Brick Wall, Triple Tap, Nail Gun, Staple Gun -------------------------

def hot_chips(size=64):
    """A red bag of flaming-hot chips: crimped top, flames up the front, HOT in big letters (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (60, 10, 0, 255)
    d.polygon([(S * .18, S * .14), (S * .82, S * .14), (S * .88, S * .9), (S * .12, S * .9)], fill=(220, 30, 20, 255))
    d.line([(S * .18, S * .14), (S * .82, S * .14), (S * .88, S * .9), (S * .12, S * .9), (S * .18, S * .14)], fill=OUT, width=7)
    d.rectangle([S * .16, S * .06, S * .84, S * .16], fill=(200, 20, 10, 255), outline=OUT, width=5)
    for k in range(7):
        d.line([(S * (.2 + k * .1), S * .07), (S * (.2 + k * .1), S * .15)], fill=OUT, width=3)
    for x, h in ((.24, .4), (.4, .3), (.56, .42), (.72, .32)):
        d.polygon([(S * (x - .08), S * .9), (S * x, S * (.9 - h)), (S * (x + .08), S * .9)], fill=(255, 160, 30, 255))
        d.polygon([(S * (x - .04), S * .9), (S * x, S * (.9 - h * .6)), (S * (x + .04), S * .9)], fill=(255, 240, 80, 255))
    d.rectangle([S * .12, S * .86, S * .88, S * .92], fill=(200, 20, 10, 255))
    im = _shrink(im, size)
    _big_text(im, "HOT", (32, 22), (255, 240, 60, 255), scale=2, font=SMALL)
    return im


def hot_chip(size=32):
    """One curly red-hot cheese puff, dusted with red powder."""
    im, d, S = _big(size)
    OUT = (90, 10, 0, 255)
    d.arc([S * .1, S * .2, S * .9, S * .9], 200, 20, fill=OUT, width=int(S * .26))
    d.arc([S * .12, S * .22, S * .88, S * .88], 200, 20, fill=(230, 40, 20, 255), width=int(S * .2))
    for x, y in ((.24, .5), (.5, .26), (.78, .4)):
        d.ellipse([S * (x - .04), S * (y - .04), S * (x + .04), S * (y + .04)], fill=(255, 120, 80, 255))
    return _shrink(im, size)


def bread_slice(size=32):
    """A slice of white bread: tan crust, puffy top."""
    im, d, S = _big(size)
    OUT = (110, 70, 20, 255)
    d.rounded_rectangle([S * .14, S * .36, S * .86, S * .92], 8, fill=(240, 225, 190, 255), outline=(190, 130, 60, 255), width=int(S * .08))
    d.ellipse([S * .1, S * .1, S * .5, S * .5], fill=(240, 225, 190, 255), outline=(190, 130, 60, 255), width=int(S * .08))
    d.ellipse([S * .5, S * .1, S * .9, S * .5], fill=(240, 225, 190, 255), outline=(190, 130, 60, 255), width=int(S * .08))
    d.rectangle([S * .22, S * .36, S * .78, S * .5], fill=(240, 225, 190, 255))
    for x, y in ((.36, .58), (.6, .7), (.48, .44)):
        d.ellipse([S * x, S * y, S * (x + .04), S * (y + .04)], fill=(210, 190, 150, 255))
    return _shrink(im, size)


def bread_loaf(size=64):
    """A whole sliced loaf in its plastic bag with the twist tie."""
    im, d, S = _big(size)
    OUT = (110, 70, 20, 255)
    d.rounded_rectangle([S * .06, S * .3, S * .82, S * .8], 22, fill=(225, 175, 100, 255), outline=OUT, width=7)
    for k in range(6):
        x = .18 + k * .11
        d.line([(S * x, S * .34), (S * x, S * .76)], fill=(190, 140, 70, 255), width=3)
    d.rounded_rectangle([S * .04, S * .26, S * .84, S * .84], 24, outline=(220, 230, 250, 200), width=5)          # bag
    d.polygon([(S * .84, S * .5), (S * .96, S * .38), (S * .96, S * .66)], fill=(230, 235, 250, 200))
    d.rectangle([S * .82, S * .48, S * .88, S * .58], fill=(40, 120, 220, 255))                                     # twist tie
    return _shrink(im, size)


def pigeon_dive(size=32):
    """A grey city pigeon diving down-right: wings swept back, the green-purple neck shine, orange eye."""
    im, d, S = _big(size)
    OUT = (30, 30, 40, 255)
    d.polygon([(S * .1, S * .1), (S * .5, S * .44), (S * .2, S * .48)], fill=(120, 125, 140, 255), outline=OUT)    # wing
    d.ellipse([S * .3, S * .36, S * .82, S * .74], fill=(150, 155, 170, 255), outline=OUT, width=5)                # body
    d.ellipse([S * .66, S * .6, S * .92, S * .86], fill=(110, 115, 130, 255), outline=OUT, width=5)                # head
    d.arc([S * .6, S * .5, S * .86, S * .76], 90, 200, fill=(90, 170, 130, 255), width=6)                          # neck shine
    d.ellipse([S * .76, S * .68, S * .82, S * .74], fill=(250, 140, 30, 255))
    d.polygon([(S * .88, S * .78), (S * .98, S * .9), (S * .84, S * .86)], fill=(60, 60, 66, 255))                  # beak
    d.polygon([(S * .3, S * .5), (S * .06, S * .62), (S * .3, S * .62)], fill=(100, 105, 120, 255), outline=OUT)   # tail
    return _shrink(im, size)


def brick_wall(size=64, rows=3, tipped=0):
    """A red brick wall built up 1-3 courses from the bottom, grey mortar; tipped = degrees it's falling over."""
    im, d, S = _big(size)
    OUT = (60, 20, 15, 255)
    for r in range(rows):
        y1 = .96 - r * .2
        y0 = y1 - .2
        off = 0 if r % 2 == 0 else .12
        x = .04 - off
        while x < .96:
            a, b = max(x, .04), min(x + .24, .96)
            if b - a > .04:
                d.rectangle([S * a, S * y0, S * b, S * y1], fill=(180, 60, 40, 255), outline=(150, 150, 150, 255), width=6)
                d.line([(S * (a + .02), S * (y0 + .04)), (S * (b - .03), S * (y0 + .04))], fill=(220, 110, 80, 255), width=3)
            x += .24
    d.rectangle([S * .04, S * (.96 - rows * .2), S * .96, S * .96], outline=OUT, width=5)
    if tipped:
        im = im.rotate(-tipped, center=(S * .5, S * .96), resample=Image.BICUBIC)
    return _shrink(im, size)


def tap_shoe(size=64):
    """A black patent tap-dance shoe with a ribbon bow and the silver tap plates on the toe and heel."""
    im, d, S = _big(size)
    OUT = (10, 10, 14, 255)
    d.polygon([(S * .08, S * .36), (S * .36, S * .36), (S * .6, S * .5), (S * .9, S * .54), (S * .94, S * .68), (S * .08, S * .68)],
              fill=(25, 25, 30, 255))
    d.line([(S * .08, S * .36), (S * .36, S * .36), (S * .6, S * .5), (S * .9, S * .54), (S * .94, S * .68), (S * .08, S * .68), (S * .08, S * .36)], fill=OUT, width=6)
    d.line([(S * .14, S * .42), (S * .34, S * .42)], fill=(140, 140, 160, 255), width=4)                            # shine
    d.ellipse([S * .46, S * .36, S * .58, S * .48], fill=(220, 30, 40, 255), outline=OUT, width=3)                 # bow
    d.rectangle([S * .58, S * .68, S * .94, S * .76], fill=(210, 215, 225, 255), outline=OUT, width=4)             # toe tap
    d.rectangle([S * .08, S * .68, S * .26, S * .8], fill=(210, 215, 225, 255), outline=OUT, width=4)              # heel tap
    return _shrink(im, size)


def nail_gun(size=64):
    """A yellow and black pneumatic nail gun pointing right: the long magazine of nails underneath, the air hose."""
    im, d, S = _big(size)
    OUT = (20, 15, 5, 255)
    d.rounded_rectangle([S * .2, S * .24, S * .86, S * .46], 10, fill=(250, 200, 30, 255), outline=OUT, width=6)
    d.rectangle([S * .82, S * .3, S * .96, S * .58], fill=(60, 60, 66, 255), outline=OUT, width=5)                 # nose
    d.polygon([(S * .3, S * .46), (S * .44, S * .46), (S * .38, S * .82), (S * .24, S * .82)], fill=(40, 40, 46, 255), outline=OUT)   # grip
    d.line([(S * .3, S * .46), (S * .44, S * .46), (S * .38, S * .82), (S * .24, S * .82), (S * .3, S * .46)], fill=OUT, width=5)
    d.rectangle([S * .48, S * .46, S * .9, S * .58], fill=(170, 175, 185, 255), outline=OUT, width=4)             # magazine
    for k in range(6):
        d.line([(S * (.52 + k * .06), S * .48), (S * (.52 + k * .06), S * .56)], fill=(90, 90, 100, 255), width=3)
    d.line([(S * .26, S * .82), (S * .1, S * .96)], fill=(220, 40, 40, 255), width=6)                              # hose
    return _shrink(im, size)


def nail_streak(n=16):
    """A flying nail (alpha only): a thin shaft with a flat head at the back."""
    return _alpha(n, n, lambda x, y: 1 if (2 <= x <= 14 and 7 <= y <= 8) or (x in (2, 3) and 5 <= y <= 10) else 0)


def staple_gun(size=64):
    """A big chrome-and-black office staple gun (the heavy-duty kind) pointing right."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.polygon([(S * .1, S * .5), (S * .86, S * .5), (S * .9, S * .66), (S * .1, S * .66)], fill=(200, 205, 215, 255), outline=OUT)   # base
    d.line([(S * .1, S * .5), (S * .86, S * .5), (S * .9, S * .66), (S * .1, S * .66), (S * .1, S * .5)], fill=OUT, width=6)
    d.polygon([(S * .14, S * .5), (S * .3, S * .22), (S * .84, S * .3), (S * .84, S * .48)], fill=(40, 40, 46, 255), outline=OUT)   # handle
    d.line([(S * .14, S * .5), (S * .3, S * .22), (S * .84, S * .3), (S * .84, S * .48)], fill=OUT, width=6)
    d.line([(S * .34, S * .3), (S * .78, S * .36)], fill=(120, 120, 130, 255), width=4)
    d.rectangle([S * .84, S * .56, S * .92, S * .66], fill=(230, 60, 40, 255), outline=OUT, width=3)
    return _shrink(im, size)


def staple_bit(n=16):
    """A flying staple (alpha only): a little squared-off U."""
    return _alpha(n, n, lambda x, y: 1 if ((x in (4, 5, 11, 12) and 5 <= y <= 11) or (4 <= x <= 12 and y in (5, 6))) else 0)


def stuck_staple(size=32):
    """A big silver staple stuck in something (shown on the foe)."""
    im, d, S = _big(size)
    OUT = (40, 40, 50, 255)
    d.line([(S * .2, S * .7), (S * .2, S * .34), (S * .8, S * .34), (S * .8, S * .7)], fill=OUT, width=int(S * .14))
    d.line([(S * .2, S * .7), (S * .2, S * .34), (S * .8, S * .34), (S * .8, S * .7)], fill=(220, 225, 235, 255), width=int(S * .08))
    return _shrink(im, size)
