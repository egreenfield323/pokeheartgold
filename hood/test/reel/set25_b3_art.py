

# ---- set 25, batch 3: 360 Deal, Eat Good, Waterworks, Bone Toss, Shmoney ---------------------------------------------

def record_contract(size=64, signed=0):
    """A record deal contract: CONTRACT across the top, fine print, and the SIGN HERE line with a red X; signed 1 =
    a scribbled signature on it, 2 = signature + initials scribbled down the side (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 40, 50, 255)
    d.polygon([(S * .14, S * .04), (S * .76, S * .04), (S * .9, S * .18), (S * .9, S * .96), (S * .14, S * .96)], fill=(250, 250, 245, 255), outline=OUT)
    d.line([(S * .14, S * .04), (S * .76, S * .04), (S * .9, S * .18), (S * .9, S * .96), (S * .14, S * .96), (S * .14, S * .04)], fill=OUT, width=5)
    for k in range(6):
        d.line([(S * .22, S * (.32 + k * .07)), (S * .82, S * (.32 + k * .07))], fill=(170, 170, 180, 255), width=3)
    d.line([(S * .3, S * .86), (S * .8, S * .86)], fill=OUT, width=4)
    d.line([(S * .2, S * .8), (S * .26, S * .88)], fill=(220, 30, 30, 255), width=5)
    d.line([(S * .26, S * .8), (S * .2, S * .88)], fill=(220, 30, 30, 255), width=5)
    if signed:
        d.line([(S * .34, S * .84), (S * .42, S * .76), (S * .48, S * .84), (S * .56, S * .74), (S * .64, S * .84), (S * .76, S * .78)], fill=(40, 60, 200, 255), width=5)
    if signed > 1:
        for y in (.36, .5, .64):
            d.line([(S * .78, S * y), (S * .84, S * (y - .04)), (S * .86, S * (y + .02))], fill=(40, 60, 200, 255), width=4)
    im = _shrink(im, size)
    return _texted(im, [("CONTRACT", (33, 8))], (20, 20, 25, 255), (250, 250, 245, 255))


def fancy_pen(size=32):
    """A shiny black fountain pen, nib down-left."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.line([(S * .2, S * .8), (S * .86, S * .14)], fill=OUT, width=int(S * .16))
    d.line([(S * .2, S * .8), (S * .86, S * .14)], fill=(40, 40, 46, 255), width=int(S * .1))
    d.line([(S * .44, S * .56), (S * .5, S * .5)], fill=(230, 190, 60, 255), width=int(S * .12))
    d.polygon([(S * .2, S * .8), (S * .06, S * .94), (S * .14, S * .74)], fill=(230, 190, 60, 255))
    return _shrink(im, size)


def grandma_plate(size=64, full=False):
    """A paper plate from grandma's kitchen: a scoop of mac and cheese, greens, a piece of fried chicken - or piled
    into a mountain that's falling off the sides."""
    im, d, S = _big(size)
    OUT = (60, 40, 20, 255)
    d.ellipse([S * .04, S * .6, S * .96, S * .92], fill=(250, 250, 245, 255), outline=OUT, width=6)
    if not full:
        d.ellipse([S * .14, S * .56, S * .42, S * .76], fill=(250, 200, 60, 255), outline=OUT, width=4)          # mac
        d.ellipse([S * .44, S * .58, S * .66, S * .76], fill=(60, 120, 50, 255), outline=OUT, width=4)          # greens
        d.ellipse([S * .62, S * .5, S * .88, S * .74], fill=(190, 120, 50, 255), outline=OUT, width=4)          # chicken
    else:
        d.polygon([(S * .08, S * .76), (S * .3, S * .24), (S * .5, S * .08), (S * .7, S * .22), (S * .92, S * .76)], fill=(250, 200, 60, 255), outline=OUT)
        for x, y, c in ((.3, .5, (60, 120, 50)), (.6, .36, (190, 120, 50)), (.5, .6, (60, 120, 50)), (.72, .58, (190, 120, 50)), (.42, .3, (230, 230, 220))):
            d.ellipse([S * (x - .1), S * (y - .07), S * (x + .1), S * (y + .07)], fill=c + (255,), outline=OUT, width=4)
        d.ellipse([S * .86, S * .8, S * .96, S * .9], fill=(250, 200, 60, 255), outline=OUT, width=3)            # spillover
    return _shrink(im, size)


def cook_pot(size=64):
    """A big dented aluminum cooking pot with steam rising, a ladle sticking out."""
    im, d, S = _big(size)
    OUT = (40, 40, 46, 255)
    d.rectangle([S * .14, S * .38, S * .86, S * .9], fill=(190, 195, 205, 255), outline=OUT, width=7)
    d.ellipse([S * .1, S * .3, S * .9, S * .46], fill=(140, 145, 155, 255), outline=OUT, width=6)
    d.ellipse([S * .16, S * .32, S * .84, S * .44], fill=(250, 200, 60, 255))
    for x in (.04, .86):
        d.rectangle([S * x, S * .46, S * (x + .1), S * .52], fill=(60, 60, 66, 255), outline=OUT, width=3)
    d.line([(S * .6, S * .38), (S * .82, S * .04)], fill=(170, 175, 185, 255), width=7)                              # ladle
    for x in (.3, .44):
        d.arc([S * (x - .06), S * .04, S * (x + .06), S * .3], 90, 270, fill=(230, 230, 240, 255), width=5)
    d.line([(S * .22, S * .5), (S * .22, S * .82)], fill=(240, 240, 250, 255), width=5)
    return _shrink(im, size)


def dog_bone(size=64):
    """A big white cartoon dog bone."""
    im, d, S = _big(size)
    OUT = (90, 80, 60, 255)
    W = (250, 245, 230, 255)
    d.rectangle([S * .22, S * .42, S * .78, S * .58], fill=W)
    for x in (.12, .88):
        for y in (.38, .62):
            d.ellipse([S * (x - .1), S * (y - .1), S * (x + .1), S * (y + .1)], fill=W, outline=OUT, width=6)
    d.line([(S * .22, S * .42), (S * .78, S * .42)], fill=OUT, width=6)
    d.line([(S * .22, S * .58), (S * .78, S * .58)], fill=OUT, width=6)
    return _shrink(im, size)


def band_stack(size=32):
    """A stack of cash with a yellow money band."""
    im, d, S = _big(size)
    OUT = (20, 60, 20, 255)
    for k in range(3):
        y = .36 + k * .1
        d.rectangle([S * .1, S * y, S * .9, S * (y + .2)], fill=(110, 190, 100, 255), outline=OUT, width=4)
    d.rectangle([S * .42, S * .34, S * .58, S * .78], fill=(250, 210, 50, 255), outline=OUT, width=3)
    return _shrink(im, size)
