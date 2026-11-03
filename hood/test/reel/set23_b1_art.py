

# ---- set 23, batch 1: Got Milk, Half Off, Crop Duster, Death Stare, Catch a Fade -----------------------------

def milk_gallon(size=64, level="full", label=True):
    """A plastic gallon jug of whole milk: blue cap, the handle up top, a red label reading MILK (shown at 1:1).
    level: full / half / empty (the clear plastic shows how much is left)."""
    im, d, S = _big(size)
    OUT = (30, 40, 70, 255)
    milk = {"full": .28, "half": .6, "empty": 1.1}[level]
    d.rounded_rectangle([S * .2, S * .22, S * .8, S * .96], 22, fill=(225, 232, 240, 150), outline=OUT, width=8)   # the jug
    if milk < 1:
        d.rounded_rectangle([S * .2, S * milk, S * .8, S * .96], 22, fill=(252, 252, 255, 255), outline=OUT, width=8)
    d.polygon([(S * .3, S * .22), (S * .42, S * .1), (S * .58, S * .1), (S * .58, S * .22)], fill=(230, 235, 242, 200))
    d.line([(S * .3, S * .22), (S * .42, S * .1)], fill=OUT, width=7)
    d.rounded_rectangle([S * .56, S * .1, S * .82, S * .34], 10, outline=OUT, width=9)                             # handle
    d.rounded_rectangle([S * .38, S * .02, S * .56, S * .12], 4, fill=(40, 110, 230, 255), outline=OUT, width=6)  # cap
    if label:
        d.rectangle([S * .2, S * .5, S * .8, S * .76], fill=(220, 40, 40, 255), outline=OUT, width=6)
    d.line([(S * .27, S * .3), (S * .27, S * .44)], fill=(255, 255, 255, 255), width=6)                           # shine
    im = _shrink(im, size)
    return _texted(im, [("MILK", (32, 35))], (255, 255, 255, 255), (120, 10, 10, 255)) if label else im


def milk_chug(size=64):
    """The jug tipped right over (no text: tilted), milk glugging out the spout to the left."""
    im = milk_gallon(size, "half", label=False).rotate(125, resample=Image.BICUBIC, expand=False)
    d = ImageDraw.Draw(im)
    for k, (x, y) in enumerate(((10, 46), (6, 54), (12, 58))):
        d.ellipse([x, y, x + 6 - k, y + 6 - k], fill=(252, 252, 255, 255), outline=(150, 160, 190, 255))
    return im


def price_gun(size=64):
    """An orange price labeler gun: a sticker roll on top, the trigger, a fresh sticker poking out the nose."""
    im, d, S = _big(size)
    OUT = (40, 20, 5, 255)
    d.polygon([(S * .08, S * .3), (S * .74, S * .3), (S * .84, S * .44), (S * .74, S * .56), (S * .08, S * .56)],
              fill=(250, 140, 30, 255), outline=OUT)
    d.line([(S * .08, S * .3), (S * .74, S * .3), (S * .84, S * .44), (S * .74, S * .56), (S * .08, S * .56), (S * .08, S * .3)], fill=OUT, width=7)
    d.ellipse([S * .2, S * .06, S * .52, S * .38], fill=(250, 250, 245, 255), outline=OUT, width=7)              # roll
    d.ellipse([S * .32, S * .18, S * .4, S * .26], fill=(120, 120, 130, 255))
    d.rounded_rectangle([S * .14, S * .54, S * .34, S * .96], 8, fill=(60, 60, 66, 255), outline=OUT, width=7)  # grip
    d.rounded_rectangle([S * .4, S * .56, S * .62, S * .82], 8, fill=(250, 140, 30, 255), outline=OUT, width=7)  # trigger
    d.rectangle([S * .82, S * .36, S * .98, S * .5], fill=(255, 255, 255, 255), outline=OUT, width=4)             # sticker
    d.line([(S * .14, S * .36), (S * .7, S * .36)], fill=(255, 200, 120, 255), width=5)
    return _shrink(im, size)


def price_sticker(text, size=32, fill=(255, 230, 60, 255), ink=(20, 20, 25, 255)):
    """A small price sticker (rounded rectangle) with one word on it (shown at 1:1)."""
    im, d, S = _big(size)
    d.rounded_rectangle([S * .04, S * .22, S * .96, S * .78], 16, fill=fill, outline=(20, 20, 25, 255), width=6)
    return _texted(_shrink(im, size), [(text, (16, 13))], ink, fill)


def half_off_tag(size=64):
    """A huge red clearance tag on a string: 50% / OFF in big white letters (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (60, 0, 0, 255)
    d.polygon([(S * .18, S * .14), (S * .96, S * .14), (S * .96, S * .86), (S * .18, S * .86), (S * .02, S * .5)],
              fill=(220, 30, 30, 255))
    d.line([(S * .18, S * .14), (S * .96, S * .14), (S * .96, S * .86), (S * .18, S * .86), (S * .02, S * .5), (S * .18, S * .14)],
           fill=OUT, width=8)
    d.ellipse([S * .12, S * .44, S * .22, S * .56], fill=(0, 0, 0, 0), outline=OUT, width=5)                       # hole
    im = _shrink(im, size)
    _big_text(im, "50%", (37, 23), (255, 255, 255, 255), scale=2, font=SMALL)
    _big_text(im, "OFF", (37, 41), (255, 240, 120, 255), scale=2, font=SMALL)
    return im


def crop_duster(size=64):
    """A yellow crop-duster biplane facing right: two wings, struts, a red propeller blur, a spray bar under the
    lower wing, the pilot's leather cap in the open cockpit."""
    im, d, S = _big(size)
    OUT = (40, 25, 5, 255)
    Y, YD = (250, 210, 40, 255), (200, 150, 20, 255)
    d.polygon([(S * .06, S * .34), (S * .16, S * .4), (S * .16, S * .5), (S * .06, S * .58)], fill=YD, outline=OUT)  # tail fin
    d.line([(S * .06, S * .34), (S * .16, S * .4), (S * .16, S * .5), (S * .06, S * .58), (S * .06, S * .34)], fill=OUT, width=6)
    d.rounded_rectangle([S * .1, S * .42, S * .84, S * .6], 18, fill=Y, outline=OUT, width=7)                       # fuselage
    d.rounded_rectangle([S * .26, S * .24, S * .76, S * .32], 8, fill=Y, outline=OUT, width=6)                      # top wing
    d.rounded_rectangle([S * .26, S * .6, S * .78, S * .68], 8, fill=YD, outline=OUT, width=6)                      # low wing
    for x in (.34, .66):
        d.line([(S * x, S * .32), (S * x, S * .6)], fill=OUT, width=5)                                               # struts
    d.ellipse([S * .44, S * .3, S * .58, S * .44], fill=(110, 60, 30, 255), outline=OUT, width=5)                   # pilot cap
    d.rectangle([S * .84, S * .44, S * .9, S * .58], fill=(80, 80, 90, 255), outline=OUT, width=4)                  # nose
    d.ellipse([S * .88, S * .26, S * .98, S * .76], fill=(230, 60, 40, 140), outline=(140, 20, 10, 255), width=4)   # prop blur
    d.line([(S * .3, S * .74), (S * .74, S * .74)], fill=(120, 120, 130, 255), width=6)                             # spray bar
    for x in (.36, .5, .64):
        d.line([(S * x, S * .68), (S * x, S * .76)], fill=(120, 120, 130, 255), width=4)
    for x in (.24, .42, .6, .76):
        d.ellipse([S * x, S * .82, S * (x + .08), S * .9], fill=(140, 220, 60, 200))                                 # the dust
    return _shrink(im, size)


def house_fly(size=32):
    """A fat cartoon housefly: black body, big red eyes, two see-through wings up."""
    im, d, S = _big(size)
    OUT = (10, 10, 10, 255)
    for x0 in (.18, .5):
        d.ellipse([S * x0, S * .06, S * (x0 + .34), S * .46], fill=(220, 235, 255, 170), outline=(90, 110, 140, 255), width=6)
    d.ellipse([S * .22, S * .38, S * .82, S * .9], fill=(40, 40, 46, 255), outline=OUT, width=7)
    d.ellipse([S * .14, S * .4, S * .36, S * .62], fill=(200, 30, 30, 255), outline=OUT, width=5)
    d.ellipse([S * .3, S * .46, S * .5, S * .64], fill=(200, 30, 30, 255), outline=OUT, width=5)
    d.line([(S * .5, S * .6), (S * .7, S * .62)], fill=(110, 110, 120, 255), width=4)
    return _shrink(im, size)


def stare_eyes(size=64):
    """Two narrowed eyes glowing in the dark: slanted black brows, red irises, a white glint - the look."""
    im, d, S = _big(size)
    OUT = (10, 0, 0, 255)
    for x0, sgn in ((.06, 1), (.54, -1)):
        x1 = x0 + .4
        d.chord([S * x0, S * .34, S * x1, S * .74], 180, 360, fill=(255, 250, 220, 255), outline=OUT, width=7)
        d.chord([S * x0, S * .5, S * x1, S * .62], 0, 180, fill=(255, 250, 220, 255), outline=OUT, width=7)
        cx = S * (x0 + .2 + sgn * .03)
        d.ellipse([cx - S * .08, S * .44, cx + S * .08, S * .6], fill=(220, 20, 20, 255), outline=OUT, width=5)
        d.ellipse([cx - S * .03, S * .49, cx + S * .03, S * .55], fill=OUT)
        d.ellipse([cx + S * .02, S * .46, cx + S * .05, S * .49], fill=(255, 255, 255, 255))
        a, b = (S * x0, S * .26), (S * x1, S * .42)
        if sgn < 0:
            a, b = (S * x0, S * .42), (S * x1, S * .26)
        d.line([a, b], fill=OUT, width=16)                                                                            # brows
    return _shrink(im, size)


def barber_pole(size=64, phase=0):
    """A barber pole: chrome caps, a glass tube with red, white and blue stripes (phase 0/1 shifts the stripes:
    flip between them and it spins)."""
    im, d, S = _big(size)
    OUT = (20, 20, 30, 255)
    d.rectangle([S * .36, S * .14, S * .64, S * .86], fill=(255, 255, 255, 255))
    step = .18
    for k in range(-2, 8):
        y = .14 + k * step + phase * step / 2
        for c, off in (((220, 30, 30, 255), 0), ((40, 70, 210, 255), step / 2)):
            yy = y + off
            d.polygon([(S * .36, S * yy), (S * .64, S * (yy - .1)), (S * .64, S * (yy - .1 + step / 4)),
                       (S * .36, S * (yy + step / 4))], fill=c)
    d.rectangle([S * 0, S * 0, S * 1, S * .14], fill=(0, 0, 0, 0))
    d.rectangle([S * 0, S * .86, S * 1, S * 1], fill=(0, 0, 0, 0))
    d.rectangle([S * .36, S * .14, S * .64, S * .86], outline=OUT, width=6)
    d.line([(S * .41, S * .18), (S * .41, S * .82)], fill=(255, 255, 255, 200), width=5)                          # glass shine
    for y0, y1 in ((.02, .14), (.86, .98)):
        d.rounded_rectangle([S * .3, S * y0, S * .7, S * y1], 8, fill=(200, 205, 215, 255), outline=OUT, width=6)
        d.line([(S * .36, S * (y0 + .04)), (S * .6, S * (y0 + .04))], fill=(255, 255, 255, 255), width=4)
    return _shrink(im, size)


def hair_clippers(size=64):
    """Barber clippers, blade down: a black body with a silver blade and a little cord."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.line([(S * .5, S * .82), (S * .62, S * .96), (S * .9, S * .98)], fill=(40, 40, 46, 255), width=8)            # cord
    d.rounded_rectangle([S * .32, S * .22, S * .68, S * .86], 26, fill=(40, 40, 46, 255), outline=OUT, width=7)
    d.rounded_rectangle([S * .38, S * .3, S * .46, S * .7], 6, fill=(110, 110, 120, 255))                         # shine
    d.rectangle([S * .44, S * .5, S * .56, S * .58], fill=(220, 180, 60, 255), outline=OUT, width=4)              # switch
    d.rectangle([S * .28, S * .08, S * .72, S * .24], fill=(210, 215, 225, 255), outline=OUT, width=6)            # blade
    for k in range(7):
        x = .3 + k * .065
        d.line([(S * x, S * .02), (S * x, S * .1)], fill=(170, 175, 185, 255), width=5)                            # teeth
    return _shrink(im, size)


def hair_snip(n=16):
    """A little clump of cut hair (alpha only): three short curved strands."""
    def f(x, y):
        for cx, cy, r in ((5, 9, 4), (8, 7, 5), (11, 9, 4)):
            dd = ((x - cx) ** 2 + (y - cy) ** 2) ** .5
            if abs(dd - r) < .8 and y < cy + 1:
                return 1
        return 0
    return _alpha(n, n, f)
