

# ---- set 28, batch 1: High Beams, Fog Machine, Order Up, Sag Check, Last Wish -------------------------------------------

def headlights(size=64, on=True):
    """A pair of round car headlights in the dark: chrome rings, glass lit blazing white-yellow (dim grey when off)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    for x in (.04, .56):
        if on:
            d.ellipse([S * (x - .04), S * .22, S * (x + .44), S * .78], fill=(255, 250, 200, 120))
        d.ellipse([S * x, S * .28, S * (x + .4), S * .72], fill=(200, 205, 215, 255), outline=OUT, width=6)        # chrome
        d.ellipse([S * (x + .06), S * .34, S * (x + .34), S * .66], fill=(255, 255, 235, 255) if on else (110, 115, 125, 255))
        if on:
            d.ellipse([S * (x + .12), S * .4, S * (x + .24), S * .52], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def brights_cone(n=16):
    """A soft beam of light (alpha only): bright on the left, fading and widening to the right."""
    return _alpha(n, n, lambda x, y: max(0, (1 - x / 16) * (1 - abs(y - 7.5) / (2 + x * .4))))


def club_fogger(size=64):
    """A club fog machine: black box, a chrome nozzle on the front, a red LED and a hose of fog coming off it."""
    im, d, S = _big(size)
    OUT = (10, 10, 15, 255)
    d.rounded_rectangle([S * .06, S * .44, S * .7, S * .86], 8, fill=(40, 40, 46, 255), outline=OUT, width=6)
    d.rectangle([S * .7, S * .56, S * .86, S * .7], fill=(200, 205, 215, 255), outline=OUT, width=5)            # nozzle
    d.ellipse([S * .14, S * .52, S * .22, S * .6], fill=(255, 40, 40, 255))
    d.line([(S * .3, S * .56), (S * .6, S * .56)], fill=(90, 90, 100, 255), width=4)                              # vents
    d.line([(S * .3, S * .64), (S * .6, S * .64)], fill=(90, 90, 100, 255), width=4)
    for x, y, r in ((.88, .5, .06), (.94, .4, .07), (.86, .3, .08)):                                              # fog curling out
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], fill=(230, 230, 240, 230))
    return _shrink(im, size)


def laser_line(n=16):
    """A thin straight laser beam (alpha only): a hard bright line across the middle."""
    return _alpha(n, n, lambda x, y: 1 if abs(y - 7.5) < .8 else (.4 if abs(y - 7.5) < 1.6 else 0))


def order_phone(size=64, done=False):
    """A phone showing a delivery app: ORDER PLACED with a scooter icon (done: DELIVERED with a check) (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rounded_rectangle([S * .22, S * .04, S * .78, S * .96], 14, fill=(30, 30, 36, 255), outline=OUT, width=6)
    d.rectangle([S * .27, S * .12, S * .73, S * .86], fill=(250, 80, 60, 255) if not done else (60, 190, 90, 255))
    d.ellipse([S * .38, S * .54, S * .62, S * .78], fill=(255, 255, 255, 255))
    if done:
        d.line([(S * .43, S * .66), (S * .49, S * .72), (S * .58, S * .6)], fill=(60, 190, 90, 255), width=6)
    else:
        d.rectangle([S * .44, S * .6, S * .56, S * .7], fill=(250, 80, 60, 255))
    im = _shrink(im, size)
    words = [("DELIV-", (32, 12)), ("ERED", (32, 21))] if done else [("ORDER", (32, 12)), ("PLACED", (32, 21))]
    return _texted(im, words, (255, 255, 255, 255), (40, 20, 20, 255))


def delivery_rider(size=64, tint=0):
    """A delivery rider on a scooter, side view facing right: helmet, the big square insulated bag on the back."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    bag = [(250, 80, 60, 255), (250, 190, 40, 255), (60, 190, 90, 255)][tint % 3]
    d.rectangle([S * .04, S * .14, S * .36, S * .46], fill=bag, outline=OUT, width=6)                            # the bag
    d.line([(S * .1, S * .3), (S * .3, S * .3)], fill=(255, 255, 255, 255), width=4)
    d.rounded_rectangle([S * .3, S * .3, S * .56, S * .62], 8, fill=(60, 70, 90, 255), outline=OUT, width=5)    # rider body
    d.ellipse([S * .42, S * .08, S * .66, S * .32], fill=bag, outline=OUT, width=5)                             # helmet
    d.rectangle([S * .56, S * .16, S * .66, S * .24], fill=(140, 190, 230, 255))                                 # visor
    d.line([(S * .5, S * .44), (S * .74, S * .5)], fill=OUT, width=6)                                            # arm to bars
    d.polygon([(S * .2, S * .7), (S * .78, S * .66), (S * .86, S * .44), (S * .92, S * .44), (S * .84, S * .76), (S * .2, S * .78)],
              fill=(230, 230, 235, 255), outline=OUT)
    for x in (.24, .8):
        d.ellipse([S * (x - .1), S * .7, S * (x + .1), S * .92], fill=(30, 30, 30, 255), outline=OUT, width=4)
    return _shrink(im, size)


def sag_jeans(size=64, stage=0):
    """Baggy blue jeans: 0 = up at the waist with a belt loop line, 1 = sagging with plaid boxers out, 2 = round the knees."""
    im, d, S = _big(size)
    OUT = (15, 25, 60, 255)
    top = (.06, .3, .56)[stage]
    if stage:
        d.rectangle([S * .14, S * .04, S * .86, S * (top + .04)], fill=(220, 60, 60, 255), outline=(90, 10, 10, 255), width=5)   # boxers
        for k in range(4):
            x = .2 + k * .18
            d.line([(S * x, S * .04), (S * x, S * top)], fill=(250, 220, 220, 255), width=3)
        d.line([(S * .14, S * (top * .5)), (S * .86, S * (top * .5))], fill=(250, 220, 220, 255), width=3)
    d.polygon([(S * .1, S * top), (S * .9, S * top), (S * .96, S * .98), (S * .56, S * .98), (S * .5, S * (top + .3)),
               (S * .44, S * .98), (S * .04, S * .98)], fill=(60, 100, 180, 255), outline=OUT)
    d.line([(S * .1, S * top), (S * .9, S * top), (S * .96, S * .98), (S * .56, S * .98), (S * .5, S * (top + .3)), (S * .44, S * .98),
            (S * .04, S * .98), (S * .1, S * top)], fill=OUT, width=6)
    d.line([(S * .1, S * (top + .06)), (S * .9, S * (top + .06))], fill=(40, 70, 140, 255), width=4)            # waistband
    d.line([(S * .3, S * (top + .14)), (S * .26, S * .9)], fill=(110, 150, 220, 255), width=4)                  # fade
    return _shrink(im, size)


def dandelion(size=64, stage=0):
    """A dandelion clock on its stem: 0 = a full white puff, 1 = half blown, 2 = a bare stem."""
    im, d, S = _big(size)
    import math
    d.line([(S * .5, S * .5), (S * .54, S * .98)], fill=(70, 150, 60, 255), width=int(S * .05))
    d.ellipse([S * .44, S * .44, S * .56, S * .56], fill=(170, 160, 90, 255))
    n = (26, 12, 0)[stage]
    for k in range(n):
        a = k * math.tau / 26 + (.6 if stage else 0)
        x, y = .5 + .34 * math.cos(a), .5 + .34 * math.sin(a)
        d.line([(S * .5, S * .5), (S * x, S * y)], fill=(235, 235, 240, 255), width=3)
        d.ellipse([S * (x - .04), S * (y - .04), S * (x + .04), S * (y + .04)], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def dandelion_seed(n=16):
    """A dandelion seed parachute (alpha only): a fluffy fan on top, a thin stalk below."""
    def f(x, y):
        fan = y < 7 and abs(x - 7.5) < (7 - y) * .9 + 1 and (x + y) % 2 == 0
        stalk = abs(x - 7.5) < .7 and 6 <= y <= 14
        return 1 if fan or stalk else 0
    return _alpha(n, n, f)
