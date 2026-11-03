

# ---- set 28, batch 4: Ice Pick, Blocked, Rat Tail, Kickback, Pass It On -----------------------------------------------------

def bar_ice_pick(size=64):
    """A bartender's ice pick pointing down-right: a long steel spike out of a red wood handle."""
    im, d, S = _big(size)
    OUT = (30, 10, 10, 255)
    d.line([(S * .12, S * .12), (S * .4, S * .4)], fill=OUT, width=int(S * .16))
    d.line([(S * .12, S * .12), (S * .4, S * .4)], fill=(200, 40, 40, 255), width=int(S * .1))
    d.rectangle([S * .38, S * .36, S * .46, S * .46], fill=(170, 170, 180, 255), outline=OUT, width=3)        # ferrule
    d.line([(S * .44, S * .44), (S * .94, S * .94)], fill=(210, 215, 225, 255), width=5)
    d.line([(S * .46, S * .44), (S * .9, S * .88)], fill=(255, 255, 255, 255), width=2)
    return _shrink(im, size)


def ice_shard(n=16):
    """A chipped-off ice shard (alpha only): a jagged triangle."""
    return _alpha(n, n, lambda x, y: 1 if y > 3 and abs(x - 7.5 - (y - 9) * .3) < (14 - y) * .55 else 0)


def dm_phone(size=64, stage=0):
    """A phone in a DM: 0 = the foe texts "hey", 1 = "hey??" "hello??", 2 = a red BLOCKED banner (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rounded_rectangle([S * .22, S * .04, S * .78, S * .96], 14, fill=(30, 30, 36, 255), outline=OUT, width=6)
    d.rectangle([S * .27, S * .12, S * .73, S * .86], fill=(245, 245, 250, 255))
    for k in range(min(stage + 1, 2)):
        y = .2 + k * .2
        d.rounded_rectangle([S * .3, S * y, S * .62, S * (y + .14)], 8, fill=(220, 225, 235, 255))
    if stage == 2:
        d.rectangle([S * .22, S * .58, S * .78, S * .76], fill=(220, 30, 30, 255), outline=OUT, width=4)
    im = _shrink(im, size)
    words = [("hey", (29, 14))] + ([("hey??", (29, 27))] if stage >= 1 else [])
    im = _texted(im, words, (20, 20, 25, 255), (245, 245, 250, 255))
    if stage == 2:
        im = _texted(im, [("BLOCKED", (32, 40))], (255, 255, 255, 255), (120, 0, 0, 255))
    return im


def subway_rat(size=64, whip=False):
    """A fat grey subway rat scurrying right: pink ears and nose, beady eye, long pink tail (whipped up overhead when
    whip)."""
    im, d, S = _big(size)
    OUT = (30, 25, 25, 255)
    if whip:
        d.line([(S * .2, S * .62), (S * .1, S * .3), (S * .3, S * .06), (S * .6, S * .1)], fill=(230, 140, 150, 255), width=6, joint="curve")
    else:
        d.line([(S * .2, S * .66), (S * .06, S * .74), (S * .02, S * .6)], fill=(230, 140, 150, 255), width=6, joint="curve")
    d.ellipse([S * .16, S * .46, S * .72, S * .86], fill=(130, 125, 125, 255), outline=OUT, width=6)
    d.polygon([(S * .6, S * .5), (S * .96, S * .7), (S * .62, S * .82)], fill=(140, 135, 135, 255), outline=OUT)
    d.line([(S * .6, S * .5), (S * .96, S * .7), (S * .62, S * .82)], fill=OUT, width=5)
    d.ellipse([S * .56, S * .38, S * .7, S * .54], fill=(240, 160, 170, 255), outline=OUT, width=4)            # ear
    d.ellipse([S * .74, S * .56, S * .8, S * .62], fill=OUT)                                                      # eye
    d.ellipse([S * .92, S * .66, S * 1.0, S * .74], fill=(240, 120, 140, 255))                                    # nose
    for x in (.3, .56):
        d.line([(S * x, S * .84), (S * (x - .04), S * .94)], fill=(230, 140, 150, 255), width=4)                # feet
    return _shrink(im, size)


def interest_envelope(size=64):
    """A fat bank envelope stuffed with cash, bills poking out, WITH INTEREST scrawled on it (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (60, 50, 30, 255)
    for k in range(4):
        x = .2 + k * .14
        d.rectangle([S * x, S * .12, S * (x + .2), S * .4], fill=(120, 190, 100, 255), outline=(30, 80, 30, 255), width=3)
    d.rectangle([S * .06, S * .3, S * .94, S * .84], fill=(240, 225, 190, 255), outline=OUT, width=6)
    d.polygon([(S * .06, S * .3), (S * .5, S * .56), (S * .94, S * .3)], fill=(225, 205, 160, 255), outline=OUT)
    im = _shrink(im, size)
    return _texted(im, [("WITH", (32, 37)), ("INTEREST", (32, 45))], (200, 20, 20, 255), (255, 245, 220, 255))


def hot_potato(size=32):
    """A baked potato so hot it's glowing red at the edges, steam squiggles coming off it."""
    im, d, S = _big(size)
    OUT = (70, 30, 10, 255)
    d.ellipse([S * .08, S * .36, S * .92, S * .9], fill=(200, 120, 60, 255), outline=(230, 40, 20, 255), width=8)
    for x, y in ((.3, .54), (.6, .62), (.46, .72)):
        d.ellipse([S * x, S * y, S * (x + .06), S * (y + .05)], fill=OUT)
    for x in (.3, .5, .7):
        d.arc([S * (x - .08), S * .0, S * (x + .08), S * .34], 90, 270, fill=(255, 255, 255, 230), width=4)
    return _shrink(im, size)
