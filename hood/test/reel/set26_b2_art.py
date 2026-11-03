

# ---- set 26, batch 2: Night Night, Dome Piece, Drill, Cold Case, Bat Rush ---------------------------------------------

def music_box(size=64):
    """A little pink music box, lid open, a tiny ballerina on top, the wind-up key on the side."""
    im, d, S = _big(size)
    OUT = (80, 30, 60, 255)
    d.rectangle([S * .16, S * .56, S * .84, S * .92], fill=(250, 170, 210, 255), outline=OUT, width=6)
    d.polygon([(S * .16, S * .56), (S * .84, S * .56), (S * .9, S * .26), (S * .22, S * .26)], fill=(255, 200, 230, 255), outline=OUT)
    d.line([(S * .16, S * .56), (S * .84, S * .56), (S * .9, S * .26), (S * .22, S * .26), (S * .16, S * .56)], fill=OUT, width=5)
    d.line([(S * .5, S * .56), (S * .5, S * .38)], fill=(200, 180, 200, 255), width=4)
    d.ellipse([S * .44, S * .3, S * .56, S * .4], fill=(255, 240, 240, 255), outline=OUT, width=3)
    d.polygon([(S * .4, S * .5), (S * .6, S * .5), (S * .5, S * .4)], fill=(255, 150, 200, 255), outline=OUT)
    d.rectangle([S * .84, S * .68, S * .96, S * .74], fill=(230, 190, 60, 255), outline=OUT, width=3)
    d.ellipse([S * .9, S * .62, S * .98, S * .8], outline=(230, 190, 60, 255), width=4)
    return _shrink(im, size)


def big_pacifier(size=64):
    """A giant baby pacifier: blue shield, ring handle, the nipple pointing left."""
    im, d, S = _big(size)
    OUT = (20, 40, 90, 255)
    d.ellipse([S * .04, S * .38, S * .34, S * .62], fill=(255, 230, 190, 230), outline=OUT, width=5)
    d.rounded_rectangle([S * .3, S * .2, S * .52, S * .8], 18, fill=(90, 160, 240, 255), outline=OUT, width=6)
    d.ellipse([S * .5, S * .26, S * .96, S * .74], outline=OUT, width=int(S * .1))
    d.ellipse([S * .5, S * .26, S * .96, S * .74], outline=(250, 230, 80, 255), width=int(S * .06))
    return _shrink(im, size)


def football_helmet(size=64):
    """A red football helmet facing right, white stripe, grey face mask."""
    im, d, S = _big(size)
    OUT = (40, 0, 0, 255)
    d.chord([S * .06, S * .08, S * .86, S * .88], 150, 420, fill=(220, 30, 30, 255), outline=OUT, width=7)
    d.arc([S * .16, S * .1, S * .76, S * .5], 200, 340, fill=(255, 255, 255, 255), width=8)
    d.ellipse([S * .3, S * .44, S * .44, S * .58], fill=(30, 30, 34, 255))                                        # ear hole
    for y in (.52, .66, .8):
        d.line([(S * .6, S * y), (S * .96, S * y)], fill=(170, 175, 185, 255), width=6)
    d.line([(S * .72, S * .48), (S * .72, S * .84)], fill=(170, 175, 185, 255), width=6)
    return _shrink(im, size)


def power_drill(size=64, big=0):
    """A cordless power drill pointing right; big 1 = a heavier hammer drill, 2 = a giant industrial drill (yellow,
    long auger bit)."""
    im, d, S = _big(size)
    OUT = (20, 15, 5, 255)
    body = ((40, 120, 220), (230, 60, 30), (250, 200, 30))[big]
    bit = (.66, .78, .98)[big]
    d.rounded_rectangle([S * .1, S * .3, S * .56, S * .5], 10, fill=body + (255,), outline=OUT, width=6)
    d.polygon([(S * .22, S * .5), (S * .36, S * .5), (S * .32, S * .84), (S * .18, S * .84)], fill=(40, 40, 46, 255), outline=OUT)
    d.rectangle([S * .14, S * .84, S * .38, S * .94], fill=(40, 40, 46, 255), outline=OUT, width=4)                # battery
    d.rectangle([S * .56, S * .34, S * .64, S * .46], fill=(60, 60, 66, 255), outline=OUT, width=4)                # chuck
    d.line([(S * .64, S * .4), (S * bit, S * .4)], fill=(190, 195, 205, 255), width=int(S * (.04 + big * .02)))
    for k in range(int((bit - .64) / .06)):
        x = .66 + k * .06
        d.line([(S * x, S * .36), (S * (x + .03), S * .44)], fill=(110, 110, 120, 255), width=3)
    return _shrink(im, size)


def evidence_board(size=64):
    """A detective's corkboard: pinned photos and notes connected with red string."""
    im, d, S = _big(size)
    OUT = (60, 35, 15, 255)
    d.rectangle([S * .04, S * .1, S * .96, S * .9], fill=(200, 150, 90, 255), outline=OUT, width=7)
    pins = [(.2, .24), (.7, .22), (.45, .5), (.22, .7), (.76, .7)]
    for a, b in ((0, 2), (1, 2), (2, 3), (2, 4), (0, 1)):
        d.line([(S * pins[a][0], S * pins[a][1]), (S * pins[b][0], S * pins[b][1])], fill=(220, 30, 30, 255), width=3)
    for k, (x, y) in enumerate(pins):
        d.rectangle([S * (x - .09), S * (y - .07), S * (x + .09), S * (y + .07)], fill=(250, 250, 245, 255) if k % 2 else (240, 230, 160, 255), outline=OUT, width=3)
        d.ellipse([S * (x - .02), S * (y - .1), S * (x + .02), S * (y - .06)], fill=(220, 30, 30, 255))
    return _shrink(im, size)


def case_file(size=64):
    """A manila case file with a big red COLD CASE stamp across it (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (90, 60, 20, 255)
    d.rectangle([S * .1, S * .16, S * .9, S * .88], fill=(230, 200, 130, 255), outline=OUT, width=6)
    d.rectangle([S * .1, S * .08, S * .4, S * .18], fill=(230, 200, 130, 255), outline=OUT, width=5)
    d.rectangle([S * .14, S * .42, S * .86, S * .66], outline=(200, 30, 30, 255), width=6)
    im = _shrink(im, size)
    return _texted(im, [("COLD", (32, 28)), ("CASE", (32, 35))], (200, 30, 30, 255), (230, 200, 130, 255))


def case_ice(size=64):
    """A big clear ice block with frosted edges and shine (drawn over a frozen battler)."""
    im, d, S = _big(size)
    d.rounded_rectangle([S * .06, S * .06, S * .94, S * .94], 12, fill=(170, 220, 250, 120), outline=(230, 245, 255, 255), width=8)
    d.line([(S * .2, S * .16), (S * .2, S * .5)], fill=(255, 255, 255, 220), width=8)
    d.line([(S * .3, S * .16), (S * .3, S * .3)], fill=(255, 255, 255, 220), width=5)
    for x, y in ((.7, .8), (.82, .66), (.6, .9)):
        d.line([(S * (x - .04), S * y), (S * (x + .04), S * y)], fill=(255, 255, 255, 255), width=4)
        d.line([(S * x, S * (y - .04)), (S * x, S * (y + .04))], fill=(255, 255, 255, 255), width=4)
    return _shrink(im, size)


def alu_bat(size=64):
    """An aluminum softball bat, silver with a black grip, angled."""
    im, d, S = _big(size)
    OUT = (30, 30, 36, 255)
    d.line([(S * .16, S * .86), (S * .84, S * .18)], fill=OUT, width=int(S * .16))
    d.line([(S * .16, S * .86), (S * .84, S * .18)], fill=(200, 205, 215, 255), width=int(S * .11))
    d.line([(S * .1, S * .92), (S * .34, S * .68)], fill=(30, 30, 34, 255), width=int(S * .1))
    d.line([(S * .4, S * .56), (S * .8, S * .18)], fill=(250, 250, 255, 255), width=4)
    return _shrink(im, size)


def tiny_note(n=16):
    """A single eighth note (alpha only)."""
    def f(x, y):
        head = ((x - 5.5) / 3.2) ** 2 + ((y - 12) / 2.4) ** 2 < 1
        stem = 7.6 <= x <= 8.8 and 2 <= y <= 12
        flag = 8.8 <= x <= 12 and 2 <= y <= 4 + (x - 8.8) * .6
        return 1 if head or stem or flag else 0
    return _alpha(n, n, f)
