

# ---- set 24, batch 6: Hat Trick, Reverse Card, Rise n Grind, Sinkhole -------------------------------------------------

def fitted_cap(size=64, color=(220, 40, 40, 255), emblem="fire"):
    """A fitted baseball cap from the side, flat brim pointing right, the sticker still on the brim; the front panel
    has an emblem: fire (flame), ice (snowflake) or zap (lightning bolt)."""
    im, d, S = _big(size)
    OUT = (20, 15, 15, 255)
    d.chord([S * .14, S * .2, S * .74, S * .84], 180, 360, fill=color, outline=OUT, width=7)
    d.rectangle([S * .14, S * .5, S * .74, S * .58], fill=color)
    d.line([(S * .14, S * .52), (S * .74, S * .52)], fill=OUT, width=5)
    d.polygon([(S * .66, S * .5), (S * .98, S * .52), (S * .98, S * .6), (S * .66, S * .6)], fill=color, outline=OUT)   # flat brim
    d.line([(S * .66, S * .5), (S * .98, S * .52), (S * .98, S * .6), (S * .66, S * .6)], fill=OUT, width=5)
    d.ellipse([S * .84, S * .52, S * .92, S * .58], fill=(220, 200, 60, 255))                                          # sticker
    d.ellipse([S * .4, S * .18, S * .48, S * .24], fill=color, outline=OUT, width=3)                                    # button
    c = (255, 255, 255, 255)
    if emblem == "fire":
        d.polygon([(S * .44, S * .3), (S * .36, S * .46), (S * .44, S * .44), (S * .52, S * .46)], fill=(255, 210, 40, 255), outline=OUT)
    elif emblem == "ice":
        for a, b in (((.44, .28), (.44, .48)), ((.35, .33), (.53, .43)), ((.35, .43), (.53, .33))):
            d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=c, width=5)
    else:
        d.polygon([(S * .46, S * .26), (S * .38, S * .38), (S * .45, S * .38), (S * .4, S * .5), (S * .52, S * .34), (S * .45, S * .34)], fill=(40, 40, 46, 255))
    return _shrink(im, size)


def game_card(size=64, label="+2", color=(220, 40, 40, 255)):
    """A card from THAT card game: coloured face, a white oval, a big label (+2, +4) or the two reverse arrows
    (label="rev") (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rounded_rectangle([S * .2, S * .06, S * .8, S * .94], 12, fill=(250, 250, 250, 255), outline=OUT, width=6)
    d.rounded_rectangle([S * .25, S * .11, S * .75, S * .89], 8, fill=color)
    d.ellipse([S * .26, S * .26, S * .74, S * .74], fill=(250, 250, 250, 255))
    if label == "rev":
        for sgn in (1, -1):
            cx, cy = S * .5 + sgn * S * .06, S * .5 - sgn * S * .06
            d.line([(cx - sgn * S * .1, cy + sgn * S * .1), (cx + sgn * S * .08, cy - sgn * S * .08)], fill=color, width=int(S * .07))
            tip = (cx + sgn * S * .12, cy - sgn * S * .12)
            d.polygon([tip, (tip[0] - sgn * S * .12, tip[1]), (tip[0], tip[1] + sgn * S * .12)], fill=color)
    im = _shrink(im, size)
    if label != "rev":
        _big_text(im, label, (32, 32), color, scale=2, font=SMALL)
    return im


def bedside_clock(size=64, t="6:00", ringing=False):
    """A black bedside alarm clock with a big red digital time (shown at 1:1); ringing adds little shake lines."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.polygon([(S * .1, S * .3), (S * .9, S * .3), (S * .96, S * .82), (S * .04, S * .82)], fill=(35, 35, 40, 255))
    d.line([(S * .1, S * .3), (S * .9, S * .3), (S * .96, S * .82), (S * .04, S * .82), (S * .1, S * .3)], fill=OUT, width=6)
    d.rectangle([S * .14, S * .38, S * .86, S * .72], fill=(15, 5, 5, 255))
    d.rounded_rectangle([S * .3, S * .2, S * .7, S * .3], 6, fill=(120, 120, 130, 255), outline=OUT, width=4)          # snooze bar
    if ringing:
        for x0, sgn in ((.02, -1), (.98, 1)):
            for k in range(2):
                d.line([(S * (x0 - sgn * .02), S * (.36 + k * .14)), (S * (x0 + sgn * .0), S * (.42 + k * .14))], fill=(255, 220, 60, 255), width=5)
    im = _shrink(im, size)
    _big_text(im, t, (32, 35), (255, 40, 30, 255), scale=2)
    return im


def coffee_mug(size=32):
    """A white coffee mug, steam curling up."""
    im, d, S = _big(size)
    OUT = (40, 30, 20, 255)
    d.rounded_rectangle([S * .2, S * .42, S * .68, S * .94], 8, fill=(250, 250, 245, 255), outline=OUT, width=6)
    d.ellipse([S * .58, S * .52, S * .86, S * .8], outline=OUT, width=7)
    d.ellipse([S * .22, S * .4, S * .66, S * .5], fill=(110, 60, 30, 255), outline=OUT, width=4)
    for x in (.32, .5):
        d.arc([S * (x - .06), S * .06, S * (x + .06), S * .36], 90, 270, fill=(220, 220, 230, 255), width=5)
    return _shrink(im, size)


def sunrise(size=64):
    """A big rising sun: orange-yellow half disc with rays fanning up."""
    import math
    im, d, S = _big(size)
    for k in range(9):
        a = math.pi + k * math.pi / 8
        d.polygon([(S * .5, S * .8), (S * (.5 + .5 * math.cos(a - .1)), S * (.8 + .5 * math.sin(a - .1))),
                   (S * (.5 + .5 * math.cos(a + .1)), S * (.8 + .5 * math.sin(a + .1)))], fill=(255, 210, 80, 180))
    d.pieslice([S * .18, S * .48, S * .82, S * 1.12], 180, 360, fill=(255, 170, 40, 255))
    d.pieslice([S * .26, S * .56, S * .74, S * 1.04], 180, 360, fill=(255, 220, 90, 255))
    return _shrink(im, size)


def road_crack(size=64, big=False):
    """A jagged crack splitting the asphalt (seen flat on the ground) - bigger and wider with big=True."""
    im, d, S = _big(size)
    w = .1 if big else .05
    pts = [(.06, .5), (.22, .44), (.34, .56), (.5, .46), (.64, .58), (.8, .48), (.94, .54)]
    d.polygon([(S * .02, S * .38), (S * .98, S * .38), (S * .98, S * .66), (S * .02, S * .66)], fill=(70, 70, 76, 200))
    up = [(S * x, S * (y - w)) for x, y in pts]
    dn = [(S * x, S * (y + w)) for x, y in reversed(pts)]
    d.polygon(up + dn, fill=(15, 12, 10, 255))
    for x, y in pts[1:-1:2]:
        d.line([(S * x, S * y), (S * (x + .06), S * (y - .16))], fill=(15, 12, 10, 255), width=5)
    return _shrink(im, size)


def sinkhole(size=64):
    """A sinkhole opening in the street: a deep black pit with a ragged ring of broken asphalt chunks round the rim."""
    import math
    im, d, S = _big(size)
    d.ellipse([S * .04, S * .3, S * .96, S * .78], fill=(70, 70, 76, 255))
    d.ellipse([S * .12, S * .36, S * .88, S * .72], fill=(5, 5, 8, 255))
    d.ellipse([S * .2, S * .36, S * .8, S * .56], fill=(60, 40, 30, 255))
    for k in range(10):
        a = k * 2 * math.pi / 10
        x, y = S * (.5 + .44 * math.cos(a)), S * (.54 + .22 * math.sin(a))
        d.polygon([(x - 10, y), (x, y - 8), (x + 12, y - 2), (x + 4, y + 8)], fill=(110, 110, 118, 255), outline=(30, 30, 34, 255))
    return _shrink(im, size)
