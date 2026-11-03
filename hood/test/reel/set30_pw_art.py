

# ---- Pistol Whip redo: a pistol in three poses --------------------------------------------------------------------------

def whip_pistol(size=64, pose="aim"):
    """A black semi-auto pistol, side view. aim = pointing right; up = tipped barrel-up (they look at it); whip =
    flipped round, held by the barrel, the grip leading - mid-swing."""
    from PIL import Image as _Im
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    BK, HI = (45, 45, 52, 255), (120, 125, 140, 255)
    d.rectangle([S * .14, S * .3, S * .9, S * .44], fill=BK, outline=OUT, width=6)                               # the slide
    for k in range(4):                                                                                            # slide serrations
        x = .2 + k * .05
        d.line([(S * x, S * .32), (S * x, S * .42)], fill=(80, 80, 90, 255), width=3)
    d.line([(S * .2, S * .33), (S * .86, S * .33)], fill=HI, width=3)                                            # shine
    d.rectangle([S * .86, S * .34, S * .94, S * .4], fill=(30, 30, 34, 255), outline=OUT, width=3)              # muzzle
    d.polygon([(S * .16, S * .44), (S * .4, S * .44), (S * .36, S * .86), (S * .14, S * .86), (S * .1, S * .6)], fill=(60, 55, 50, 255), outline=OUT)
    d.line([(S * .16, S * .44), (S * .4, S * .44), (S * .36, S * .86), (S * .14, S * .86), (S * .1, S * .6), (S * .16, S * .44)], fill=OUT, width=6)   # grip
    for k in range(4):
        y = .52 + k * .08
        d.line([(S * .16, S * y), (S * .34, S * y)], fill=(85, 80, 72, 255), width=3)                           # grip texture
    d.arc([S * .36, S * .4, S * .58, S * .62], 0, 180, fill=OUT, width=6)                                        # trigger guard
    d.line([(S * .46, S * .44), (S * .44, S * .54)], fill=OUT, width=5)                                          # trigger
    if pose == "up":
        im = im.rotate(60, resample=_Im.BICUBIC)
    elif pose == "whip":
        im = im.transpose(_Im.FLIP_LEFT_RIGHT).rotate(-35, resample=_Im.BICUBIC)
    return _shrink(im, size)
