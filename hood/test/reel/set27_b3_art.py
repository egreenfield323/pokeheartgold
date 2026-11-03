

# ---- set 27, batch 3: Cut Off, Time Out, Swap Bags, Yap Session, Moonwalk -----------------------------------------------

def liquor_glass(size=32):
    """A rocks glass of brown liquor with two ice cubes."""
    im, d, S = _big(size)
    OUT = (30, 20, 10, 255)
    d.polygon([(S * .14, S * .2), (S * .86, S * .2), (S * .78, S * .94), (S * .22, S * .94)], fill=(220, 235, 245, 150))
    d.polygon([(S * .18, S * .46), (S * .82, S * .46), (S * .78, S * .9), (S * .22, S * .9)], fill=(190, 110, 30, 255))
    for x, y in ((.3, .4), (.52, .48)):
        d.rectangle([S * x, S * y, S * (x + .18), S * (y + .16)], fill=(235, 245, 255, 255), outline=(150, 180, 200, 255), width=3)
    d.line([(S * .14, S * .2), (S * .86, S * .2), (S * .78, S * .94), (S * .22, S * .94), (S * .14, S * .2)], fill=OUT, width=5)
    d.line([(S * .24, S * .28), (S * .28, S * .84)], fill=(255, 255, 255, 255), width=4)
    return _shrink(im, size)


def bar_top(size=64):
    """A stretch of dark wood bar counter with a brass rail."""
    im, d, S = _big(size)
    OUT = (30, 15, 5, 255)
    d.rectangle([S * .0, S * .5, S * 1.0, S * .66], fill=(110, 60, 30, 255), outline=OUT, width=6)
    d.rectangle([S * .0, S * .66, S * 1.0, S * 1.0], fill=(70, 35, 15, 255), outline=OUT, width=6)
    d.line([(S * .0, S * .55), (S * 1.0, S * .55)], fill=(160, 100, 50, 255), width=4)
    d.line([(S * .0, S * .88), (S * 1.0, S * .88)], fill=(220, 180, 60, 255), width=7)                         # brass rail
    return _shrink(im, size)


def dunce_cap(size=64):
    """A tall white paper dunce cap with a big D on it (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (30, 30, 40, 255)
    d.polygon([(S * .5, S * .02), (S * .82, S * .92), (S * .18, S * .92)], fill=(250, 250, 245, 255), outline=OUT)
    d.line([(S * .5, S * .02), (S * .82, S * .92), (S * .18, S * .92), (S * .5, S * .02)], fill=OUT, width=7)
    d.line([(S * .2, S * .86), (S * .8, S * .86)], fill=(220, 40, 40, 255), width=6)
    im = _shrink(im, size)
    return _texted(im, [("D", (32, 34))], (220, 40, 40, 255), (255, 255, 255, 255), font=GLYPHS)


def egg_timer(size=32, ring=False):
    """A wind-up kitchen egg timer, white with red numbers - shaking when it rings."""
    im, d, S = _big(size)
    OUT = (40, 20, 20, 255)
    d.ellipse([S * .12, S * .2, S * .88, S * .9], fill=(250, 250, 245, 255), outline=OUT, width=6)
    d.rectangle([S * .4, S * .06, S * .6, S * .24], fill=(220, 40, 40, 255), outline=OUT, width=4)
    for k in range(6):
        import math
        a = k * math.tau / 6
        d.line([(S * (.5 + .26 * math.cos(a)), S * (.55 + .26 * math.sin(a))), (S * (.5 + .32 * math.cos(a)), S * (.55 + .32 * math.sin(a)))],
               fill=(220, 40, 40, 255), width=4)
    d.line([(S * .5, S * .55), (S * .62, S * .4)], fill=OUT, width=4)
    if ring:
        for x0 in (.0, .88):
            d.arc([S * (x0 - .1), S * .2, S * (x0 + .22), S * .7], 120 if x0 else 300, 240 if x0 else 60, fill=OUT, width=4)
    return _shrink(im, size)


def gym_duffel(size=64, open_=None):
    """A red gym duffel bag; open_ "cash" = stuffed with money, "laundry" = dirty socks and stink lines."""
    im, d, S = _big(size)
    OUT = (50, 5, 5, 255)
    if open_ == "cash":
        for k in range(5):
            x = .2 + k * .12
            d.rectangle([S * x, S * (.2 + (k % 2) * .06), S * (x + .14), S * .5], fill=(110, 180, 90, 255), outline=(30, 80, 30, 255), width=3)
    elif open_ == "laundry":
        d.ellipse([S * .26, S * .2, S * .48, S * .5], fill=(230, 225, 200, 255), outline=(120, 110, 80, 255), width=3)
        d.ellipse([S * .5, S * .26, S * .74, S * .5], fill=(200, 200, 190, 255), outline=(120, 110, 80, 255), width=3)
        for x in (.32, .5, .68):                                                     # stink lines
            d.arc([S * (x - .05), S * .0, S * (x + .05), S * .2], 90, 270, fill=(140, 180, 60, 255), width=4)
    d.rounded_rectangle([S * .06, S * .4, S * .94, S * .9], 24, fill=(200, 30, 40, 255), outline=OUT, width=7)
    d.arc([S * .3, S * .2, S * .7, S * .6], 180, 360, fill=OUT, width=8)                                          # handles
    d.line([(S * .1, S * .58), (S * .9, S * .58)], fill=(250, 250, 250, 255), width=5)                           # zipper line
    d.ellipse([S * .1, S * .54, S * .16, S * .62], fill=(200, 200, 200, 255))
    return _shrink(im, size)


def lightup_tile(size=32, lit=False):
    """A dance-floor tile: dark when off, lit glowing white-pink when stepped on."""
    im, d, S = _big(size)
    OUT = (20, 20, 30, 255)
    d.polygon([(S * .12, S * .3), (S * .88, S * .3), (S * .98, S * .78), (S * .02, S * .78)],
              fill=(255, 220, 250, 255) if lit else (130, 110, 170, 255), outline=OUT)
    d.line([(S * .12, S * .3), (S * .88, S * .3), (S * .98, S * .78), (S * .02, S * .78), (S * .12, S * .3)], fill=OUT, width=5)
    if lit:
        d.polygon([(S * .3, S * .4), (S * .7, S * .4), (S * .76, S * .66), (S * .24, S * .66)], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def black_fedora(size=32):
    """A black fedora with a white band."""
    im, d, S = _big(size)
    OUT = (5, 5, 10, 255)
    d.ellipse([S * .02, S * .56, S * .98, S * .82], fill=(25, 25, 30, 255), outline=OUT, width=5)
    d.rounded_rectangle([S * .22, S * .2, S * .78, S * .68], 12, fill=(30, 30, 36, 255), outline=OUT, width=5)
    d.rectangle([S * .22, S * .52, S * .78, S * .62], fill=(245, 245, 245, 255))
    d.line([(S * .5, S * .22), (S * .5, S * .34)], fill=OUT, width=5)                                             # the pinch
    return _shrink(im, size)
