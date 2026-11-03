

# ---- set 23, batch 5: Clothesline, Bullhorn, Hype Man, Ring Ya Bell, Heat Check -----------------------------------

def clothesline_rig(size=64):
    """A backyard clothesline: two wooden T-posts and a sagging rope between them with three clothespins."""
    im, d, S = _big(size)
    OUT = (40, 25, 10, 255)
    WOOD = (160, 110, 60, 255)
    for x in (.04, .9):
        d.rectangle([S * x, S * .3, S * (x + .06), S * .98], fill=WOOD, outline=OUT, width=5)
        d.rectangle([S * (x - .03), S * .28, S * (x + .09), S * .34], fill=WOOD, outline=OUT, width=4)
    d.arc([S * .07, S * -.04, S * .93, S * .62], 22, 158, fill=OUT, width=7)
    d.arc([S * .07, S * -.04, S * .93, S * .62], 22, 158, fill=(240, 240, 235, 255), width=3)                      # rope
    for x in (.3, .5, .7):
        y = .56 - .06 * (1 - abs(x - .5) / .5) * -1
        d.rectangle([S * (x - .015), S * (y - .02), S * (x + .015), S * (y + .07)], fill=(220, 190, 130, 255), outline=OUT, width=3)
    return _shrink(im, size)


def white_tee(size=32):
    """A plain white tee hung by the shoulders."""
    im, d, S = _big(size)
    OUT = (60, 60, 70, 255)
    _outline_poly(d, [(S * .3, S * .1), (S * .7, S * .1), (S * .96, S * .3), (S * .82, S * .44), (S * .74, S * .36), (S * .74, S * .94),
                      (S * .26, S * .94), (S * .26, S * .36), (S * .18, S * .44), (S * .04, S * .3)], (250, 250, 250, 255), OUT, 7)
    d.arc([S * .38, S * .02, S * .62, S * .2], 0, 180, fill=OUT, width=5)
    return _shrink(im, size)


def line_boxers(size=32):
    """Red boxer shorts with white hearts, hung on the line."""
    im, d, S = _big(size)
    OUT = (60, 0, 10, 255)
    _outline_poly(d, [(S * .1, S * .16), (S * .9, S * .16), (S * .96, S * .86), (S * .56, S * .86), (S * .5, S * .5), (S * .44, S * .86),
                      (S * .04, S * .86)], (220, 30, 50, 255), OUT, 7)
    d.rectangle([S * .1, S * .14, S * .9, S * .26], fill=(250, 250, 250, 255), outline=OUT, width=5)
    for x, y in ((.24, .46), (.74, .5), (.3, .7), (.8, .74)):
        d.ellipse([S * (x - .05), S * (y - .05), S * (x + .05), S * (y + .05)], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def bullhorn(size=64):
    """A police bullhorn (megaphone): a white flared horn with a red rim, a black pistol grip and trigger."""
    im, d, S = _big(size)
    OUT = (20, 20, 26, 255)
    d.polygon([(S * .14, S * .36), (S * .5, S * .3), (S * .94, S * .1), (S * .94, S * .78), (S * .5, S * .58), (S * .14, S * .52)],
              fill=(245, 245, 245, 255))
    d.line([(S * .14, S * .36), (S * .5, S * .3), (S * .94, S * .1), (S * .94, S * .78), (S * .5, S * .58), (S * .14, S * .52), (S * .14, S * .36)],
           fill=OUT, width=7)
    d.ellipse([S * .86, S * .1, S * .98, S * .78], fill=(220, 30, 30, 255), outline=OUT, width=6)                # rim
    d.ellipse([S * .89, S * .2, S * .95, S * .68], fill=(60, 60, 66, 255))
    d.rectangle([S * .04, S * .36, S * .16, S * .52], fill=(60, 60, 66, 255), outline=OUT, width=5)              # mouthpiece
    d.rounded_rectangle([S * .3, S * .52, S * .44, S * .9], 6, fill=(40, 40, 46, 255), outline=OUT, width=5)     # grip
    d.rectangle([S * .44, S * .58, S * .5, S * .7], fill=(220, 30, 30, 255), outline=OUT, width=3)               # trigger
    d.line([(S * .5, S * .36), (S * .86, S * .2)], fill=(200, 200, 210, 255), width=4)
    return _shrink(im, size)


def feedback_squiggle(n=16):
    """A zig-zag squeal line (alpha only), for mic feedback."""
    def f(x, y):
        t = (x % 4) / 4
        yy = 8 + 6 * (t if t < .5 else 1 - t) - 1.5
        return 1 if abs(y - yy) < 1.2 and 1 < x < 15 else 0
    return _alpha(n, n, f)


def hype_bubble(text, size=64, scale=1):
    """A white shout bubble (spiky at the edges) with one word at 1x or 2x pixel scale (shown at 1:1)."""
    import math
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    pts = []
    for k in range(28):
        a = k * 2 * math.pi / 28
        r = .46 if k % 2 == 0 else .4
        pts.append((S * (.5 + r * math.cos(a)), S * (.46 + r * .7 * math.sin(a))))
    _outline_poly(d, pts, (255, 255, 255, 255), OUT, 8)
    d.polygon([(S * .3, S * .7), (S * .14, S * .96), (S * .42, S * .72)], fill=(255, 255, 255, 255))
    d.line([(S * .3, S * .74), (S * .14, S * .96), (S * .42, S * .74)], fill=OUT, width=7)
    im = _shrink(im, size)
    if scale == 1:
        return _texted(im, [(text, (32, 26))], (20, 20, 25, 255), (255, 255, 255, 255))
    _big_text(im, text, (32, 30), (230, 30, 30, 255), scale=scale, font=SMALL)
    return im


def doorbell_plate(size=64):
    """A doorbell on a slice of brick wall: a brass plate with a glowing round button and a house number."""
    im, d, S = _big(size)
    OUT = (40, 20, 10, 255)
    d.rectangle([S * .1, S * .06, S * .9, S * .94], fill=(170, 70, 50, 255), outline=OUT, width=7)                # brick
    for y in range(6):
        yy = .06 + y * .147
        d.line([(S * .1, S * yy), (S * .9, S * yy)], fill=(120, 50, 35, 255), width=4)
        for x in ((.3, .62) if y % 2 else (.46, .78)):
            d.line([(S * x, S * yy), (S * x, S * (yy + .147))], fill=(120, 50, 35, 255), width=4)
    d.rounded_rectangle([S * .32, S * .22, S * .68, S * .78], 10, fill=(230, 190, 70, 255), outline=OUT, width=6)  # plate
    d.ellipse([S * .4, S * .4, S * .6, S * .6], fill=(255, 250, 200, 255), outline=OUT, width=5)                   # button
    d.ellipse([S * .45, S * .45, S * .55, S * .55], fill=(255, 220, 80, 255))
    return _shrink(im, size)


def dizzy_bird(size=32):
    """A little yellow cartoon bird with its wings up (the ones that circle a knocked-out head)."""
    im, d, S = _big(size)
    OUT = (60, 40, 0, 255)
    d.ellipse([S * .2, S * .3, S * .8, S * .86], fill=(255, 220, 40, 255), outline=OUT, width=6)
    d.polygon([(S * .3, S * .44), (S * .1, S * .1), (S * .5, S * .36)], fill=(255, 240, 120, 255), outline=OUT)
    d.polygon([(S * .7, S * .44), (S * .9, S * .1), (S * .5, S * .36)], fill=(255, 240, 120, 255), outline=OUT)
    d.polygon([(S * .76, S * .56), (S * .98, S * .62), (S * .76, S * .68)], fill=(250, 140, 30, 255), outline=OUT)
    d.ellipse([S * .58, S * .46, S * .68, S * .56], fill=OUT)
    return _shrink(im, size)


def thermostat(size=64, temp="72"):
    """A wall thermostat: a beige box, a dark screen with the temperature in big digits (red at 99), up/down
    buttons (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 35, 30, 255)
    d.rounded_rectangle([S * .14, S * .1, S * .86, S * .9], 14, fill=(235, 225, 205, 255), outline=OUT, width=8)
    d.rectangle([S * .24, S * .2, S * .76, S * .56], fill=(30, 50, 40, 255) if temp != "99" else (60, 10, 10, 255), outline=OUT, width=5)
    for y, up in ((.66, True), (.66, False)):
        x = .36 if up else .64
        d.ellipse([S * (x - .09), S * (y - .07), S * (x + .09), S * (y + .11)], fill=(200, 190, 170, 255), outline=OUT, width=5)
        tri = [(S * x, S * (y - .02)), (S * (x - .05), S * (y + .06)), (S * (x + .05), S * (y + .06))] if up else \
              [(S * x, S * (y + .08)), (S * (x - .05), S * y), (S * (x + .05), S * y)]
        d.polygon(tri, fill=OUT)
    im = _shrink(im, size)
    col = {"72": (120, 255, 160, 255), "85": (255, 200, 60, 255), "99": (255, 60, 40, 255)}[temp]
    _big_text(im, temp, (30, 24), col, scale=2)
    _texted(im, [("F", (44, 16))], col, (30, 50, 40, 255) if temp != "99" else (60, 10, 10, 255))
    return im


def heat_shimmer(n=16):
    """A rising heat-haze ripple (alpha only): two short wavy vertical lines."""
    import math

    def f(x, y):
        for cx in (5, 11):
            if abs(x - (cx + 1.5 * math.sin(y / 2))) < 1 and 2 < y < 14:
                return 1
        return 0
    return _alpha(n, n, f)


def shout_arc(n=16):
    """A sound-wave arc ")" (alpha only), for shouting."""
    import math

    def f(x, y):
        r = math.hypot(x - 2, y - 7.5)
        return 1 if abs(r - 10) < 1.4 and x > 6 else 0
    return _alpha(n, n, f)
