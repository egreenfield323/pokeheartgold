

# ---- set 25, batch 4: Moon Bath, Slime Down, Last Verse, Lip Gloss, Bottle Rain ---------------------------------------

def big_moon(size=64):
    """A big pale full moon with grey craters and a soft glow ring."""
    im, d, S = _big(size)
    d.ellipse([S * .02, S * .02, S * .98, S * .98], fill=(255, 255, 220, 70))
    d.ellipse([S * .12, S * .12, S * .88, S * .88], fill=(250, 248, 225, 255), outline=(200, 195, 160, 255), width=6)
    for x, y, r in ((.36, .36, .1), (.6, .56, .13), (.42, .68, .07), (.66, .3, .06)):
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], fill=(215, 210, 180, 255))
    return _shrink(im, size)


def sun_reflector(size=64):
    """A fold-out silver tanning reflector (three panels), held open."""
    im, d, S = _big(size)
    OUT = (60, 65, 80, 255)
    for x0, x1, c in ((.06, .36, (200, 210, 230)), (.36, .64, (240, 245, 255)), (.64, .94, (200, 210, 230))):
        d.polygon([(S * x0, S * (.3 if x0 < .3 or x0 > .6 else .24)), (S * x1, S * (.24 if x1 < .7 else .3)),
                   (S * x1, S * (.7 if x1 < .7 else .64)), (S * x0, S * (.64 if x0 < .3 or x0 > .6 else .7))], fill=c + (255,), outline=OUT)
    for x in (.36, .64):
        d.line([(S * x, S * .24), (S * x, S * .7)], fill=OUT, width=4)
    d.line([(S * .44, S * .32), (S * .5, S * .5)], fill=(255, 255, 255, 255), width=5)
    return _shrink(im, size)


def beach_lounger(size=64):
    """A striped folding beach lounger, reclined."""
    im, d, S = _big(size)
    OUT = (40, 30, 20, 255)
    for x, c in ((.0, (240, 80, 80)), (.12, (250, 250, 250)), (.24, (60, 140, 230)), (.36, (250, 250, 250)), (.48, (240, 80, 80))):
        d.polygon([(S * (.08 + x), S * .62), (S * (.2 + x), S * .62), (S * (.2 + x * .3 + .5), S * (.3 + x * .1)), (S * (.08 + x * .3 + .5), S * (.3 + x * .1))], fill=c + (255,)) if False else None
    d.polygon([(S * .06, S * .64), (S * .62, S * .64), (S * .62, S * .72), (S * .06, S * .72)], fill=(60, 140, 230, 255), outline=OUT)   # seat
    d.polygon([(S * .62, S * .64), (S * .94, S * .22), (S * .98, S * .28), (S * .66, S * .72)], fill=(240, 80, 80, 255), outline=OUT)   # back
    for k in range(3):
        d.line([(S * (.16 + k * .16), S * .64), (S * (.16 + k * .16), S * .72)], fill=(250, 250, 250, 255), width=6)
    for a, b in (((.12, .72), (.06, .92)), ((.56, .72), (.66, .92)), ((.8, .48), (.9, .92))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(170, 175, 185, 255), width=6)
    return _shrink(im, size)


def slime_bucket(size=64, tipped=False):
    """A metal bucket brimming with bright green slime, dripping down the side - or tipped over, slime pouring out."""
    im, d, S = _big(size)
    OUT = (30, 40, 30, 255)
    bucket = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    b = ImageDraw.Draw(bucket)
    b.polygon([(S * .2, S * .3), (S * .8, S * .3), (S * .72, S * .92), (S * .28, S * .92)], fill=(170, 175, 185, 255), outline=OUT)
    b.line([(S * .2, S * .3), (S * .8, S * .3), (S * .72, S * .92), (S * .28, S * .92), (S * .2, S * .3)], fill=OUT, width=6)
    b.ellipse([S * .2, S * .22, S * .8, S * .38], fill=(120, 230, 60, 255), outline=OUT, width=5)
    b.ellipse([S * .3, S * .3, S * .4, S * .52], fill=(120, 230, 60, 255))
    b.arc([S * .16, S * .04, S * .84, S * .5], 200, 340, fill=OUT, width=5)                                        # handle
    if tipped:
        bucket = bucket.rotate(130, center=(S * .5, S * .5), resample=Image.BICUBIC)
        b = ImageDraw.Draw(bucket)
        b.polygon([(S * .4, S * .7), (S * .2, S * .98), (S * .7, S * .98), (S * .56, S * .7)], fill=(120, 230, 60, 255))
    im.alpha_composite(bucket)
    return _shrink(im, size)


def slime_goo(size=64):
    """A big blob of green slime dripping down over something (to cover a battler)."""
    im, d, S = _big(size)
    G, GL = (110, 220, 50, 230), (200, 255, 150, 255)
    d.ellipse([S * .1, S * .04, S * .9, S * .5], fill=G)
    for x, h in ((.16, .78), (.3, .62), (.44, .9), (.58, .7), (.72, .84), (.84, .6)):
        d.rounded_rectangle([S * (x - .06), S * .3, S * (x + .06), S * h], 10, fill=G)
        d.ellipse([S * (x - .07), S * (h - .06), S * (x + .07), S * (h + .06)], fill=G)
    d.arc([S * .2, S * .1, S * .6, S * .36], 200, 300, fill=GL, width=8)
    return _shrink(im, size)


def stage_mic(size=64):
    """A handheld mic held upright: a silver mesh ball head on top, a tapered black handle, a gold band."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.polygon([(S * .4, S * .42), (S * .6, S * .42), (S * .55, S * .96), (S * .45, S * .96)], fill=(40, 40, 46, 255), outline=OUT)
    d.line([(S * .4, S * .42), (S * .6, S * .42), (S * .55, S * .96), (S * .45, S * .96), (S * .4, S * .42)], fill=OUT, width=6)
    d.rectangle([S * .4, S * .42, S * .6, S * .5], fill=(230, 190, 60, 255), outline=OUT, width=4)
    d.ellipse([S * .3, S * .06, S * .7, S * .46], fill=(200, 205, 215, 255), outline=OUT, width=6)
    for k in range(4):
        d.line([(S * (.37 + k * .09), S * .1), (S * (.37 + k * .09), S * .42)], fill=(140, 145, 155, 255), width=3)
    d.line([(S * .3, S * .26), (S * .7, S * .26)], fill=(140, 145, 155, 255), width=3)
    d.arc([S * .36, S * .12, S * .56, S * .3], 200, 280, fill=(255, 255, 255, 255), width=5)
    return _shrink(im, size)


def lip_gloss(size=32):
    """A tube of pink lip gloss with the wand pulled out."""
    im, d, S = _big(size)
    OUT = (80, 20, 50, 255)
    d.rounded_rectangle([S * .14, S * .46, S * .44, S * .96], 8, fill=(255, 140, 200, 255), outline=OUT, width=5)
    d.rectangle([S * .14, S * .46, S * .44, S * .58], fill=(240, 240, 245, 255), outline=OUT, width=4)
    d.line([(S * .5, S * .5), (S * .82, S * .12)], fill=OUT, width=7)
    d.ellipse([S * .72, S * .04, S * .9, S * .22], fill=(255, 100, 180, 255), outline=OUT, width=4)
    d.line([(S * .2, S * .62), (S * .2, S * .86)], fill=(255, 220, 240, 255), width=4)
    return _shrink(im, size)


def glossy_lips(size=64):
    """Big glossy pink lips with white shine spots - so shiny they sparkle."""
    im, d, S = _big(size)
    OUT = (110, 0, 50, 255)
    R = (250, 80, 160, 255)
    d.pieslice([S * .08, S * .24, S * .52, S * .64], 180, 360, fill=R)
    d.pieslice([S * .48, S * .24, S * .92, S * .64], 180, 360, fill=R)
    d.chord([S * .08, S * .3, S * .92, S * .8], 0, 180, fill=R)
    d.polygon([(S * .08, S * .44), (S * .92, S * .44), (S * .92, S * .56), (S * .08, S * .56)], fill=R)
    d.line([(S * .1, S * .5), (S * .3, S * .46), (S * .5, S * .52), (S * .7, S * .46), (S * .9, S * .5)], fill=OUT, width=6)
    for x, y, r in ((.28, .36, .06), (.66, .36, .05), (.48, .66, .07), (.3, .64, .03)):
        d.ellipse([S * (x - r), S * (y - r * .6), S * (x + r), S * (y + r * .6)], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def sleep_z16(n=16):
    """A small Z (alpha only)."""
    return _alpha(n, n, lambda x, y: 1 if (3 <= y <= 4 and 3 <= x <= 12) or (11 <= y <= 12 and 3 <= x <= 12) or
                  (4 < y < 11 and abs(x - (12 - (y - 4) * 9 / 7)) < 1.3) else 0)


def water_bottle(size=32):
    """A plastic water bottle: clear with a blue label and cap."""
    im, d, S = _big(size)
    OUT = (40, 60, 90, 255)
    d.rounded_rectangle([S * .32, S * .22, S * .68, S * .94], 10, fill=(200, 230, 250, 200), outline=OUT, width=5)
    d.rectangle([S * .4, S * .06, S * .6, S * .2], fill=(40, 100, 220, 255), outline=OUT, width=4)
    d.rectangle([S * .32, S * .5, S * .68, S * .7], fill=(40, 120, 230, 255))
    d.line([(S * .4, S * .28), (S * .4, S * .46)], fill=(255, 255, 255, 255), width=4)
    return _shrink(im, size)
