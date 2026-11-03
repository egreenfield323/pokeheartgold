

# ---- set 25, batch 1 (INSANE): Burn It Down, Hydrant Bomb, Gun Garden, Meteor Drop, Blow Up -----------------------

def barrel_grill(size=64):
    """A cookout barrel grill on legs: black drum cut in half, lid propped open, charcoal glowing, a spatula hanging."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    for a, b in (((.2, .62), (.12, .96)), ((.8, .62), (.88, .96))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(50, 50, 56, 255), width=7)
    d.chord([S * .06, S * .32, S * .94, S * .78], 0, 180, fill=(40, 40, 46, 255), outline=OUT, width=7)
    d.chord([S * .06, S * .02, S * .94, S * .48], 180, 360, fill=(55, 55, 62, 255), outline=OUT, width=7)     # lid up
    d.line([(S * .1, S * .55), (S * .9, S * .55)], fill=(160, 160, 170, 255), width=5)                         # grate
    for x in (.2, .34, .48, .62, .76):
        d.ellipse([S * x, S * .52, S * (x + .1), S * .6], fill=(255, 120, 30, 255))                             # coals
    d.line([(S * .9, S * .4), (S * .98, S * .7)], fill=(170, 170, 180, 255), width=5)                         # spatula
    return _shrink(im, size)


def lighter_fluid(size=32):
    """A can of charcoal lighter fluid: a squeeze bottle, red cap and a flame logo."""
    im, d, S = _big(size)
    OUT = (40, 20, 0, 255)
    d.rounded_rectangle([S * .26, S * .26, S * .74, S * .96], 8, fill=(250, 210, 40, 255), outline=OUT, width=6)
    d.polygon([(S * .4, S * .26), (S * .46, S * .04), (S * .54, S * .04), (S * .6, S * .26)], fill=(220, 40, 30, 255), outline=OUT)
    d.polygon([(S * .5, S * .44), (S * .38, S * .74), (S * .62, S * .74)], fill=(230, 60, 20, 255))
    d.polygon([(S * .5, S * .56), (S * .44, S * .74), (S * .56, S * .74)], fill=(255, 220, 60, 255))
    return _shrink(im, size)


def fireball_cloud(size=64):
    """A mushroom-shaped fireball: a churning orange-red cap of flame on a smoky stalk."""
    import math
    im, d, S = _big(size)
    d.rectangle([S * .4, S * .5, S * .6, S * .96], fill=(90, 80, 80, 255))
    d.ellipse([S * .26, S * .82, S * .74, S * .98], fill=(110, 100, 100, 255))
    for k in range(10):
        a = math.pi + k * math.pi / 9
        cx, cy = S * (.5 + .34 * math.cos(a)), S * (.42 + .26 * math.sin(a))
        d.ellipse([cx - S * .14, cy - S * .14, cx + S * .14, cy + S * .14], fill=(230, 70, 20, 255))
    d.ellipse([S * .14, S * .2, S * .86, S * .6], fill=(250, 120, 30, 255))
    d.ellipse([S * .26, S * .26, S * .74, S * .52], fill=(255, 200, 60, 255))
    d.ellipse([S * .38, S * .32, S * .62, S * .46], fill=(255, 250, 200, 255))
    return _shrink(im, size)


def red_hydrant(size=64, capless=False):
    """A big red fire hydrant: the bonnet, side nozzle caps, the chains - or with the top blown off (a dark hole)."""
    im, d, S = _big(size)
    OUT = (60, 0, 0, 255)
    R, RL = (220, 30, 30, 255), (255, 110, 100, 255)
    d.rectangle([S * .3, S * .86, S * .7, S * .96], fill=(180, 20, 20, 255), outline=OUT, width=6)
    d.rounded_rectangle([S * .32, S * .36, S * .68, S * .88], 8, fill=R, outline=OUT, width=7)
    d.rectangle([S * .2, S * .5, S * .32, S * .64], fill=R, outline=OUT, width=5)
    d.rectangle([S * .68, S * .5, S * .8, S * .64], fill=R, outline=OUT, width=5)
    d.line([(S * .38, S * .42), (S * .38, S * .82)], fill=RL, width=6)
    d.rectangle([S * .28, S * .3, S * .72, S * .38], fill=(200, 25, 25, 255), outline=OUT, width=5)
    if capless:
        d.ellipse([S * .34, S * .24, S * .66, S * .36], fill=(20, 10, 10, 255), outline=OUT, width=5)
    else:
        d.chord([S * .34, S * .14, S * .66, S * .44], 180, 360, fill=R, outline=OUT, width=6)
        d.rectangle([S * .46, S * .08, S * .54, S * .16], fill=(200, 25, 25, 255), outline=OUT, width=4)
    return _shrink(im, size)


def pipe_wrench(size=32):
    """A heavy red pipe wrench."""
    im, d, S = _big(size)
    OUT = (20, 15, 15, 255)
    d.line([(S * .2, S * .9), (S * .62, S * .32)], fill=OUT, width=int(S * .16))
    d.line([(S * .2, S * .9), (S * .62, S * .32)], fill=(200, 40, 40, 255), width=int(S * .1))
    d.polygon([(S * .5, S * .26), (S * .76, S * .06), (S * .9, S * .2), (S * .66, S * .42)], fill=(170, 175, 185, 255), outline=OUT)
    d.line([(S * .5, S * .26), (S * .76, S * .06), (S * .9, S * .2), (S * .66, S * .42), (S * .5, S * .26)], fill=OUT, width=5)
    return _shrink(im, size)


def water_jet(n=16):
    """A blob of rushing water (alpha only): a fat rounded streak."""
    return _alpha(n, n, lambda x, y: max(0, 1 - ((x - 7.5) / 7) ** 2 - ((y - 7.5) / 4) ** 2))


def flower_bed(size=64, stage=0):
    """A little flower bed of dirt with a white picket edge; stage 0 = just dirt with bullets planted, 1 = sprouts,
    2 = taller stems with leaves."""
    im, d, S = _big(size)
    OUT = (40, 25, 10, 255)
    d.rectangle([S * .04, S * .7, S * .96, S * .92], fill=(110, 70, 35, 255), outline=OUT, width=6)
    for k in range(9):
        x = .06 + k * .1
        d.polygon([(S * x, S * .7), (S * (x + .03), S * .62), (S * (x + .06), S * .7)], fill=(250, 250, 250, 255), outline=OUT)
    for x in (.22, .5, .78):
        if stage == 0:
            d.rectangle([S * (x - .03), S * .64, S * (x + .03), S * .72], fill=(230, 180, 60, 255), outline=OUT, width=3)
        else:
            h = .5 if stage == 1 else .3
            d.line([(S * x, S * .72), (S * x, S * h)], fill=(60, 160, 60, 255), width=6)
            d.ellipse([S * (x - .1), S * (h + .06), S * x, S * (h + .14)], fill=(80, 190, 80, 255), outline=OUT, width=3)
            if stage == 2:
                d.ellipse([S * x, S * (h + .14), S * (x + .1), S * (h + .22)], fill=(80, 190, 80, 255), outline=OUT, width=3)
    return _shrink(im, size)


def watering_can(size=32):
    """A green watering can, spout to the right."""
    im, d, S = _big(size)
    OUT = (10, 40, 10, 255)
    d.rounded_rectangle([S * .14, S * .4, S * .62, S * .9], 8, fill=(60, 170, 80, 255), outline=OUT, width=6)
    d.line([(S * .6, S * .78), (S * .94, S * .4)], fill=OUT, width=int(S * .12))
    d.line([(S * .6, S * .78), (S * .94, S * .4)], fill=(60, 170, 80, 255), width=int(S * .07))
    d.arc([S * .16, S * .14, S * .56, S * .56], 180, 360, fill=OUT, width=6)
    return _shrink(im, size)


def gun_flower(size=64):
    """A tall flower on a green stem with leaves - but the bloom is a black pistol pointing right, petals round the grip."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.line([(S * .4, S * .98), (S * .4, S * .44)], fill=(60, 160, 60, 255), width=8)
    for y, sgn in ((.78, -1), (.62, 1)):
        d.ellipse([S * (.4 + (0 if sgn > 0 else -.18)), S * y, S * (.4 + (.18 if sgn > 0 else 0)), S * (y + .08)], fill=(80, 190, 80, 255), outline=OUT, width=3)
    for k in range(6):
        import math
        a = k * math.pi / 3
        cx, cy = S * (.4 + .12 * math.cos(a)), S * (.36 + .12 * math.sin(a))
        d.ellipse([cx - S * .07, cy - S * .07, cx + S * .07, cy + S * .07], fill=(250, 120, 180, 255), outline=OUT, width=3)
    d.rectangle([S * .34, S * .26, S * .86, S * .36], fill=(40, 40, 46, 255), outline=OUT, width=5)                 # slide
    d.polygon([(S * .34, S * .36), (S * .48, S * .36), (S * .44, S * .52), (S * .32, S * .52)], fill=(40, 40, 46, 255), outline=OUT)
    d.ellipse([S * .34, S * .3, S * .46, S * .42], fill=(255, 220, 60, 255))
    return _shrink(im, size)


def meteor_rock(size=64):
    """A flaming meteor coming down from the top-right: a cratered grey-brown rock, flames streaming behind it."""
    im, d, S = _big(size)
    OUT = (30, 20, 15, 255)
    for k, (c, w) in enumerate((((255, 90, 20), .24), ((255, 170, 40), .16), ((255, 240, 140), .08))):
        d.polygon([(S * .5, S * (.5 - w)), (S * .98, S * .02), (S * (.5 + w), S * .5)], fill=c + (255,))
    d.ellipse([S * .2, S * .42, S * .62, S * .84], fill=(120, 100, 85, 255), outline=OUT, width=7)
    for x, y, r in ((.34, .56, .06), (.48, .7, .05), (.3, .72, .04)):
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], fill=(80, 65, 55, 255))
    d.arc([S * .24, S * .46, S * .58, S * .8], 200, 280, fill=(255, 150, 60, 255), width=5)
    return _shrink(im, size)


def notif_phone(size=64, count="1"):
    """A phone lit up with notifications: a red badge with the count (1 / 12 / 99+) in the corner and message bars
    on the screen (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rounded_rectangle([S * .24, S * .06, S * .76, S * .96], 14, fill=(30, 30, 36, 255), outline=OUT, width=7)
    d.rectangle([S * .29, S * .14, S * .71, S * .86], fill=(60, 120, 220, 255))
    n = {"1": 1, "12": 3, "99+": 5}[count]
    for k in range(n):
        d.rounded_rectangle([S * .32, S * (.34 + k * .1), S * .68, S * (.42 + k * .1)], 5, fill=(250, 250, 255, 255))
    bw = {"1": .16, "12": .22, "99+": .32}[count]
    d.ellipse([S * (.82 - bw), S * .02, S * .9, S * .2], fill=(230, 30, 30, 255), outline=(255, 255, 255, 255), width=5)
    im = _shrink(im, size)
    _texted(im, [(count, (round(64 * (.86 - bw / 2)), 3))], (255, 255, 255, 255), (230, 30, 30, 255))
    return im


def notif_bell(size=32):
    """A little yellow notification bell with a red dot."""
    im, d, S = _big(size)
    OUT = (80, 50, 0, 255)
    d.chord([S * .2, S * .14, S * .8, S * .9], 180, 360, fill=(255, 210, 40, 255), outline=OUT, width=6)
    d.rectangle([S * .2, S * .52, S * .8, S * .72], fill=(255, 210, 40, 255), outline=OUT, width=6)
    d.ellipse([S * .42, S * .7, S * .58, S * .86], fill=(255, 210, 40, 255), outline=OUT, width=4)
    d.ellipse([S * .62, S * .08, S * .86, S * .32], fill=(230, 30, 30, 255), outline=(255, 255, 255, 255), width=4)
    return _shrink(im, size)
