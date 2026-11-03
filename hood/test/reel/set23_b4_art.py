

# ---- set 23, batch 4: Cold Cocked, Last Call, Tanning Bed, Victory Lap, Gift Bomb -------------------------------

def chest_freezer(size=64):
    """A white chest freezer with the lid flung open, frost on the rim and cold mist inside."""
    im, d, S = _big(size)
    OUT = (40, 50, 70, 255)
    d.polygon([(S * .1, S * .36), (S * .9, S * .36), (S * .96, S * .1), (S * .16, S * .1)], fill=(225, 232, 242, 255), outline=OUT)
    d.line([(S * .1, S * .36), (S * .9, S * .36), (S * .96, S * .1), (S * .16, S * .1), (S * .1, S * .36)], fill=OUT, width=7)   # lid up
    d.polygon([(S * .2, S * .32), (S * .82, S * .32), (S * .86, S * .14), (S * .24, S * .14)], fill=(190, 215, 240, 255))
    d.rounded_rectangle([S * .06, S * .44, S * .94, S * .94], 8, fill=(245, 248, 252, 255), outline=OUT, width=8)  # body
    d.rectangle([S * .06, S * .4, S * .94, S * .52], fill=(160, 210, 245, 255), outline=OUT, width=6)              # frosty opening
    for x in (.14, .3, .52, .7, .84):
        d.polygon([(S * x, S * .52), (S * (x + .03), S * .6), (S * (x + .06), S * .52)], fill=(200, 235, 255, 255))   # icicles
    d.rectangle([S * .4, S * .62, S * .6, S * .68], fill=(150, 155, 165, 255), outline=OUT, width=4)              # handle
    d.ellipse([S * .78, S * .82, S * .86, S * .9], fill=(80, 200, 90, 255))                                        # power light
    return _shrink(im, size)


def popsicle(size=32):
    """A red, white and blue rocket popsicle on a stick."""
    im, d, S = _big(size)
    OUT = (30, 20, 40, 255)
    d.rectangle([S * .44, S * .7, S * .56, S * .98], fill=(225, 190, 130, 255), outline=OUT, width=5)
    d.polygon([(S * .5, S * .02), (S * .74, S * .26), (S * .26, S * .26)], fill=(220, 40, 40, 255), outline=OUT)
    d.rectangle([S * .26, S * .26, S * .74, S * .48], fill=(250, 250, 250, 255), outline=OUT, width=5)
    d.rectangle([S * .22, S * .48, S * .78, S * .72], fill=(40, 90, 220, 255), outline=OUT, width=5)
    d.line([(S * .5, S * .02), (S * .74, S * .26), (S * .26, S * .26), (S * .5, S * .02)], fill=OUT, width=5)
    return _shrink(im, size)


def peas_bag(size=32):
    """A frozen bag of peas: a green bag, crimped top, a bowl of peas pictured on the front, frost."""
    im, d, S = _big(size)
    OUT = (10, 50, 20, 255)
    d.rounded_rectangle([S * .14, S * .14, S * .86, S * .94], 10, fill=(40, 170, 70, 255), outline=OUT, width=6)
    d.rectangle([S * .12, S * .06, S * .88, S * .18], fill=(30, 140, 60, 255), outline=OUT, width=5)
    for k in range(6):
        d.line([(S * (.16 + k * .13), S * .07), (S * (.16 + k * .13), S * .17)], fill=OUT, width=3)
    d.ellipse([S * .26, S * .42, S * .74, S * .82], fill=(250, 250, 250, 255), outline=OUT, width=4)
    for x, y in ((.4, .56), (.52, .52), (.6, .62), (.46, .66), (.36, .66)):
        d.ellipse([S * (x - .06), S * (y - .06), S * (x + .06), S * (y + .06)], fill=(120, 220, 80, 255), outline=OUT, width=2)
    d.line([(S * .2, S * .3), (S * .4, S * .24)], fill=(220, 245, 255, 255), width=5)                                # frost
    return _shrink(im, size)


def frozen_turkey(size=64):
    """A whole frozen turkey: a pale icy body, two drumsticks with paper frills, frost and a little icicle."""
    im, d, S = _big(size)
    OUT = (60, 50, 60, 255)
    SKIN = (240, 220, 190, 255)
    d.ellipse([S * .1, S * .3, S * .78, S * .84], fill=SKIN, outline=OUT, width=8)
    for a, b in (((.62, .4), (.9, .2)), ((.66, .62), (.94, .52))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=SKIN, width=int(S * .12))
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=OUT, width=4)
        d.ellipse([S * (b[0] - .07), S * (b[1] - .07), S * (b[0] + .07), S * (b[1] + .07)], fill=(255, 255, 255, 255), outline=OUT, width=4)
    d.ellipse([S * .1, S * .3, S * .78, S * .84], outline=OUT, width=8)
    d.arc([S * .2, S * .36, S * .6, S * .66], 200, 300, fill=(255, 255, 255, 255), width=6)                      # shine
    for x, y in ((.24, .5), (.42, .44), (.36, .66), (.56, .7)):
        d.line([(S * (x - .04), S * y), (S * (x + .04), S * y)], fill=(170, 220, 255, 255), width=4)
        d.line([(S * x, S * (y - .04)), (S * x, S * (y + .04))], fill=(170, 220, 255, 255), width=4)            # frost sparkles
    d.polygon([(S * .4, S * .82), (S * .44, S * .96), (S * .48, S * .82)], fill=(190, 230, 255, 255))           # icicle
    return _shrink(im, size)


def frost_crystal(n=16):
    """A six-armed frost sparkle (alpha only)."""
    import math

    def f(x, y):
        dx, dy = x - 7.5, y - 7.5
        r = math.hypot(dx, dy)
        if r > 7:
            return 0
        a = math.atan2(dy, dx) % (math.pi / 3)
        return 1 if min(a, math.pi / 3 - a) * r < .9 or r < 1.6 else 0
    return _alpha(n, n, f)


def bar_bell(size=64, swing=0):
    """A brass bar bell hanging from a wall bracket with a rope pull; swing -1/0/1 tilts it mid-ring."""
    im, d, S = _big(size)
    OUT = (50, 30, 5, 255)
    d.rectangle([S * .08, S * .06, S * .2, S * .3], fill=(90, 60, 30, 255), outline=OUT, width=5)                  # bracket
    d.line([(S * .2, S * .14), (S * .56, S * .14)], fill=(60, 60, 66, 255), width=7)
    bell = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    b = ImageDraw.Draw(bell)
    b.line([(S * .56, S * .14), (S * .56, S * .26)], fill=(60, 60, 66, 255), width=6)
    b.chord([S * .34, S * .22, S * .78, S * .74], 180, 360, fill=(240, 190, 50, 255), outline=OUT, width=7)
    b.rectangle([S * .34, S * .48, S * .78, S * .66], fill=(240, 190, 50, 255))
    b.polygon([(S * .34, S * .66), (S * .28, S * .74), (S * .84, S * .74), (S * .78, S * .66)], fill=(220, 160, 30, 255))
    b.line([(S * .34, S * .48), (S * .34, S * .66), (S * .28, S * .74), (S * .84, S * .74), (S * .78, S * .66), (S * .78, S * .48)], fill=OUT, width=7)
    b.line([(S * .42, S * .34), (S * .42, S * .6)], fill=(255, 240, 160, 255), width=6)                            # shine
    b.ellipse([S * .5, S * .72, S * .62, S * .84], fill=(120, 90, 40, 255), outline=OUT, width=4)                # clapper
    b.line([(S * .56, S * .84), (S * .5, S * .98)], fill=(200, 170, 110, 255), width=6)                           # rope
    if swing:
        bell = bell.rotate(-14 * swing, center=(S * .56, S * .14), resample=Image.BICUBIC)
    im.alpha_composite(bell)
    return _shrink(im, size)


def mirror_ball(size=64, phase=0):
    """A mirror disco ball on its chain: a grid of grey/white facets; phase 0/1 moves the bright facets so it
    twinkles as it turns."""
    im, d, S = _big(size)
    OUT = (30, 30, 40, 255)
    d.line([(S * .5, 0), (S * .5, S * .16)], fill=(150, 150, 160, 255), width=6)
    d.ellipse([S * .16, S * .14, S * .84, S * .82], fill=(170, 175, 190, 255), outline=OUT, width=7)
    for i in range(7):
        for j in range(7):
            x, y = .2 + i * .09, .18 + j * .09
            if ((x + .045 - .5) ** 2 + (y + .045 - .48) ** 2) > .1:
                continue
            c = (255, 255, 255, 255) if (i + j + phase) % 3 == 0 else ((120, 125, 140, 255) if (i * j + phase) % 2 else (200, 205, 220, 255))
            d.rectangle([S * x, S * y, S * (x + .08), S * (y + .08)], fill=c)
    d.ellipse([S * .16, S * .14, S * .84, S * .82], outline=OUT, width=7)
    return _shrink(im, size)


def tanning_bed(size=64, shut=False):
    """A tanning bed (clamshell): silver shell with the purple-blue UV tubes glowing inside; open (the lid
    raised) or shut (the glow leaking out the seam)."""
    im, d, S = _big(size)
    OUT = (20, 15, 40, 255)
    SHELL, SHELL_D = (200, 205, 220, 255), (140, 145, 165, 255)
    d.rounded_rectangle([S * .04, S * .62, S * .96, S * .86], 14, fill=SHELL, outline=OUT, width=7)               # base
    d.rectangle([S * .1, S * .86, S * .2, S * .96], fill=SHELL_D, outline=OUT, width=5)
    d.rectangle([S * .8, S * .86, S * .9, S * .96], fill=SHELL_D, outline=OUT, width=5)
    if shut:
        d.rounded_rectangle([S * .04, S * .38, S * .96, S * .64], 30, fill=SHELL, outline=OUT, width=7)
        d.rectangle([S * .08, S * .6, S * .92, S * .66], fill=(190, 120, 255, 255))                              # glow seam
        d.line([(S * .14, S * .44), (S * .86, S * .44)], fill=(240, 240, 250, 255), width=5)
    else:
        d.polygon([(S * .04, S * .62), (S * .2, S * .06), (S * .96, S * .2), (S * .96, S * .62)], fill=SHELL_D, outline=OUT)
        d.line([(S * .04, S * .62), (S * .2, S * .06), (S * .96, S * .2), (S * .96, S * .62)], fill=OUT, width=7)
        d.polygon([(S * .14, S * .56), (S * .26, S * .14), (S * .88, S * .26), (S * .88, S * .56)], fill=(120, 60, 220, 255))
        for k in range(4):
            y = .26 + k * .08
            d.line([(S * .24, S * (y - .02)), (S * .84, S * (y + .04))], fill=(220, 190, 255, 255), width=5)       # UV tubes
        d.rectangle([S * .1, S * .62, S * .9, S * .68], fill=(160, 100, 240, 255))
    return _shrink(im, size)


def sun_ray(n=16):
    """A long thin ray of light (alpha only): bright core, soft edges."""
    def f(x, y):
        dy = abs(y - 7.5)
        return max(0, 1 - dy / 3) if 1 < x < 15 else 0
    return _alpha(n, n, f)


def victory_trophy(size=64):
    """A big gold trophy cup: two handles, a star on the front, a black base with a gold plate."""
    im, d, S = _big(size)
    OUT = (60, 40, 0, 255)
    G, GL, GD = (250, 200, 40, 255), (255, 240, 150, 255), (200, 140, 20, 255)
    for x0 in (.06, .7):
        d.ellipse([S * x0, S * .14, S * (x0 + .24), S * .44], outline=OUT, width=12)
        d.ellipse([S * x0, S * .14, S * (x0 + .24), S * .44], outline=G, width=6)
    d.chord([S * .2, S * -.1, S * .8, S * .62], 0, 180, fill=G, outline=OUT, width=8)
    d.rectangle([S * .2, S * .06, S * .8, S * .26], fill=G)
    d.line([(S * .2, S * .06), (S * .8, S * .06)], fill=OUT, width=8)
    d.line([(S * .2, S * .06), (S * .2, S * .26)], fill=OUT, width=8)
    d.line([(S * .8, S * .06), (S * .8, S * .26)], fill=OUT, width=8)
    d.line([(S * .3, S * .14), (S * .32, S * .4)], fill=GL, width=6)                                              # shine
    d.rectangle([S * .44, S * .6, S * .56, S * .74], fill=GD, outline=OUT, width=5)                               # stem
    d.rectangle([S * .26, S * .74, S * .74, S * .96], fill=(40, 30, 30, 255), outline=OUT, width=6)               # base
    d.rectangle([S * .36, S * .8, S * .64, S * .9], fill=G)
    import math
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        r = .1 if k % 2 == 0 else .045
        pts.append((S * (.5 + r * math.cos(a)), S * (.3 + r * math.sin(a))))
    d.polygon(pts, fill=GL, outline=OUT)
    return _shrink(im, size)


def rose_petal(n=16):
    """A single curled rose petal (alpha only)."""
    def f(x, y):
        dx, dy = (x - 7.5) / 6, (y - 8) / 4.5
        return 1 if dx * dx + dy * dy < 1 and not (dx > .3 and dy < -.2) else 0
    return _alpha(n, n, f)


def gift_box(size=64, wrap=(220, 30, 40, 255), ribbon=(255, 210, 40, 255)):
    """A wrapped present: coloured paper, a ribbon cross and a big bow on top."""
    im, d, S = _big(size)
    OUT = (30, 15, 15, 255)
    d.rectangle([S * .14, S * .4, S * .86, S * .94], fill=wrap, outline=OUT, width=7)
    d.rectangle([S * .08, S * .3, S * .92, S * .44], fill=wrap, outline=OUT, width=7)                             # lid
    d.rectangle([S * .44, S * .3, S * .56, S * .94], fill=ribbon, outline=OUT, width=4)
    for pts in (((.5, .3), (.22, .08), (.24, .28)), ((.5, .3), (.78, .08), (.76, .28))):
        _outline_poly(d, [(S * x, S * y) for x, y in pts], ribbon, OUT, 6)                                          # bow
    d.ellipse([S * .44, S * .22, S * .56, S * .34], fill=ribbon, outline=OUT, width=4)
    d.line([(S * .2, S * .5), (S * .2, S * .86)], fill=(255, 255, 255, 120), width=5)
    return _shrink(im, size)


def cartoon_bomb(size=64):
    """A round black cartoon bomb with a shine and a short lit fuse."""
    im, d, S = _big(size)
    OUT = (5, 5, 10, 255)
    d.ellipse([S * .14, S * .3, S * .8, S * .96], fill=(30, 30, 38, 255), outline=OUT, width=8)
    d.rectangle([S * .4, S * .22, S * .58, S * .34], fill=(90, 90, 100, 255), outline=OUT, width=5)
    d.line([(S * .49, S * .22), (S * .6, S * .1), (S * .74, S * .08)], fill=(200, 170, 110, 255), width=6)
    d.ellipse([S * .26, S * .44, S * .4, S * .58], fill=(140, 140, 160, 255))
    return _shrink(im, size)


def confetti_boom(size=64):
    """A party explosion: a white-hot centre, a red/yellow burst, and ribbon and confetti flying out."""
    import math
    im, d, S = _big(size)
    OUT = (40, 10, 10, 255)
    pts = []
    for k in range(20):
        a = k * 2 * math.pi / 20
        r = .44 if k % 2 == 0 else .28
        pts.append((S * (.5 + r * math.cos(a)), S * (.5 + r * math.sin(a))))
    _outline_poly(d, pts, (255, 90, 40, 255), OUT, 7)
    d.ellipse([S * .28, S * .28, S * .72, S * .72], fill=(255, 220, 60, 255))
    d.ellipse([S * .38, S * .38, S * .62, S * .62], fill=(255, 255, 230, 255))
    for k, c in enumerate(((60, 200, 255), (255, 60, 200), (120, 230, 60), (255, 255, 255), (160, 90, 255), (255, 230, 40))):
        a = k * 2 * math.pi / 6 + .5
        x, y = .5 + .4 * math.cos(a), .5 + .4 * math.sin(a)
        d.rectangle([S * (x - .04), S * (y - .025), S * (x + .04), S * (y + .025)], fill=c + (255,), outline=OUT, width=3)
    return _shrink(im, size)


def confetti_bit(n=16):
    """A small confetti rectangle (alpha only)."""
    return _alpha(n, n, lambda x, y: 1 if 4 < x < 12 and 6 < y < 10 else 0)
