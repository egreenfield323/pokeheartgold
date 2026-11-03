

# ---- set 26, batch 3: Speed Bag, Trash Can, Comeback, Wish List, Deep End ---------------------------------------------

def speed_bag(size=64, swing=0):
    """A boxing speed bag hanging under its round wooden platform; swing -1/0/1 tilts it mid-bounce."""
    im, d, S = _big(size)
    OUT = (40, 10, 10, 255)
    d.ellipse([S * .1, S * .04, S * .9, S * .2], fill=(150, 100, 50, 255), outline=OUT, width=6)
    bag = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    b = ImageDraw.Draw(bag)
    b.line([(S * .5, S * .18), (S * .5, S * .26)], fill=(60, 60, 66, 255), width=6)
    b.ellipse([S * .32, S * .24, S * .68, S * .8], fill=(200, 30, 30, 255), outline=OUT, width=6)
    b.arc([S * .36, S * .3, S * .56, S * .6], 200, 280, fill=(255, 140, 130, 255), width=6)
    if swing:
        bag = bag.rotate(-28 * swing, center=(S * .5, S * .2), resample=Image.BICUBIC)
    im.alpha_composite(bag)
    return _shrink(im, size)


def red_glove(size=64):
    """A red boxing glove punching right, white cuff."""
    im, d, S = _big(size)
    OUT = (60, 0, 0, 255)
    d.rounded_rectangle([S * .06, S * .36, S * .3, S * .7], 8, fill=(250, 250, 250, 255), outline=OUT, width=6)
    d.ellipse([S * .24, S * .2, S * .94, S * .84], fill=(220, 30, 30, 255), outline=OUT, width=7)
    d.ellipse([S * .3, S * .56, S * .56, S * .86], fill=(200, 25, 25, 255), outline=OUT, width=6)                  # thumb
    d.arc([S * .36, S * .26, S * .8, S * .56], 200, 300, fill=(255, 140, 130, 255), width=7)
    return _shrink(im, size)


def trash_bag(size=32):
    """A black trash bag, tied at the top, bulging."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.ellipse([S * .12, S * .3, S * .88, S * .96], fill=(40, 40, 46, 255), outline=OUT, width=5)
    d.polygon([(S * .4, S * .32), (S * .3, S * .06), (S * .5, S * .2), (S * .7, S * .06), (S * .6, S * .32)], fill=(40, 40, 46, 255), outline=OUT)
    d.arc([S * .22, S * .4, S * .5, S * .7], 200, 280, fill=(110, 110, 120, 255), width=5)
    return _shrink(im, size)


def garbage_truck(size=64):
    """A green garbage truck facing right, the big compactor body tipped up at the back, dripping."""
    im, d, S = _big(size)
    OUT = (10, 30, 10, 255)
    d.polygon([(S * .02, S * .24), (S * .62, S * .3), (S * .62, S * .72), (S * .06, S * .72)], fill=(60, 150, 70, 255), outline=OUT)
    d.line([(S * .02, S * .24), (S * .62, S * .3), (S * .62, S * .72), (S * .06, S * .72), (S * .02, S * .24)], fill=OUT, width=6)
    for k in range(3):
        d.line([(S * (.14 + k * .14), S * .3), (S * (.16 + k * .14), S * .7)], fill=(40, 110, 50, 255), width=4)
    d.rectangle([S * .62, S * .38, S * .94, S * .72], fill=(240, 240, 240, 255), outline=OUT, width=6)          # cab
    d.rectangle([S * .74, S * .42, S * .9, S * .54], fill=(120, 180, 230, 255), outline=OUT, width=4)
    for x in (.18, .44, .8):
        d.ellipse([S * (x - .08), S * .66, S * (x + .08), S * .82], fill=(25, 25, 28, 255), outline=OUT, width=4)
    d.ellipse([S * .02, S * .7, S * .08, S * .78], fill=(140, 160, 60, 255))                                       # drip
    return _shrink(im, size)


def trash_pile(size=64):
    """A heap of garbage: bags, a pizza box, a banana peel, a fish skeleton, flies."""
    im, d, S = _big(size)
    OUT = (20, 20, 22, 255)
    d.ellipse([S * .04, S * .5, S * .96, S * .98], fill=(70, 70, 76, 255), outline=OUT, width=5)
    for x, y in ((.2, .52), (.5, .42), (.72, .56)):
        d.ellipse([S * (x - .14), S * (y - .12), S * (x + .14), S * (y + .12)], fill=(40, 40, 46, 255), outline=OUT, width=5)
    d.polygon([(S * .32, S * .66), (S * .58, S * .6), (S * .62, S * .72), (S * .36, S * .78)], fill=(210, 170, 110, 255), outline=OUT)   # pizza box
    d.arc([S * .66, S * .66, S * .86, S * .86], 180, 330, fill=(250, 220, 60, 255), width=8)                      # banana peel
    d.line([(S * .1, S * .76), (S * .28, S * .76)], fill=(230, 230, 230, 255), width=4)                            # fish bones
    for x in (.14, .18, .22):
        d.line([(S * x, S * .72), (S * x, S * .8)], fill=(230, 230, 230, 255), width=3)
    return _shrink(im, size)


def scoreboard(size=64, home="0", away="99"):
    """A stadium scoreboard: HOME and AWAY with big amber digits (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (10, 10, 14, 255)
    d.rectangle([S * .02, S * .12, S * .98, S * .8], fill=(20, 20, 26, 255), outline=(120, 120, 130, 255), width=7)
    d.rectangle([S * .44, S * .8, S * .56, S * .96], fill=(90, 90, 96, 255), outline=OUT, width=4)
    d.line([(S * .5, S * .18), (S * .5, S * .74)], fill=(80, 80, 90, 255), width=4)
    im = _shrink(im, size)
    _texted(im, [("HOME", (16, 10)), ("AWAY", (48, 10))], (255, 255, 255, 255), (20, 20, 26, 255))
    _big_text(im, home, (16, 32), (255, 190, 40, 255), scale=2, font=SMALL)
    _big_text(im, away, (48, 32), (255, 190, 40, 255), scale=2, font=SMALL)
    return im


def bday_cake(size=64, lit=True):
    """A birthday cake: pink frosting, sprinkles, three candles - flames on (lit) or smoking out."""
    im, d, S = _big(size)
    OUT = (80, 40, 30, 255)
    d.rectangle([S * .12, S * .5, S * .88, S * .9], fill=(250, 240, 220, 255), outline=OUT, width=6)
    d.rectangle([S * .12, S * .5, S * .88, S * .62], fill=(255, 150, 200, 255), outline=OUT, width=5)
    for x in (.2, .34, .5, .66, .8):
        d.rectangle([S * x, S * .66, S * (x + .04), S * .7], fill=((80, 160, 250), (250, 200, 40), (120, 220, 90))[int(x * 10) % 3] + (255,))
    for x in (.3, .5, .7):
        d.rectangle([S * (x - .03), S * .3, S * (x + .03), S * .5], fill=(120, 190, 250, 255), outline=OUT, width=3)
        if lit:
            d.ellipse([S * (x - .04), S * .16, S * (x + .04), S * .3], fill=(255, 200, 40, 255))
            d.ellipse([S * (x - .02), S * .21, S * (x + .02), S * .29], fill=(255, 250, 200, 255))
        else:
            d.line([(S * x, S * .28), (S * (x + .03), S * .2), (S * (x - .02), S * .12)], fill=(180, 180, 185, 255), width=4)
    return _shrink(im, size)


def kiddie_pool(size=64):
    """An inflatable blue kiddie pool full of water, seen from the side-top."""
    im, d, S = _big(size)
    OUT = (20, 40, 90, 255)
    d.ellipse([S * .04, S * .44, S * .96, S * .9], fill=(60, 130, 230, 255), outline=OUT, width=7)
    d.ellipse([S * .14, S * .5, S * .86, S * .8], fill=(120, 200, 250, 255))
    d.arc([S * .04, S * .44, S * .96, S * .9], 200, 340, fill=(160, 210, 255, 255), width=6)
    d.arc([S * .3, S * .56, S * .6, S * .7], 200, 320, fill=(255, 255, 255, 255), width=4)
    return _shrink(im, size)
