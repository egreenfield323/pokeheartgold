

# ---- set 28, batch 3: Tag In, Bounce Back, Hold Grudge, Tickle Fight, Galaxy Rag ------------------------------------------

def ring_corner(size=64):
    """A wrestling ring corner: a padded red turnbuckle post with three ropes running off to the right."""
    im, d, S = _big(size)
    OUT = (20, 10, 10, 255)
    d.rectangle([S * .06, S * .06, S * .18, S * .98], fill=(170, 170, 180, 255), outline=OUT, width=5)
    for k, y in enumerate((.18, .4, .62)):
        d.line([(S * .18, S * (y + .04)), (S * 1.0, S * (y + .1))], fill=OUT, width=8)
        d.line([(S * .18, S * (y + .04)), (S * 1.0, S * (y + .1))], fill=(250, 250, 250, 255) if k != 1 else (220, 40, 40, 255), width=5)
        d.rounded_rectangle([S * .02, S * (y - .02), S * .24, S * (y + .1)], 6, fill=(220, 30, 40, 255), outline=OUT, width=4)
    return _shrink(im, size)


def luchador(size=64):
    """A tag-team partner in a luchador mask, mid flying-elbow: arms tucked, knee up, cape-less, all business."""
    im, d, S = _big(size)
    OUT = (10, 10, 15, 255)
    d.ellipse([S * .34, S * .04, S * .66, S * .36], fill=(40, 90, 200, 255), outline=OUT, width=5)            # the mask
    d.polygon([(S * .38, S * .14), (S * .48, S * .18), (S * .4, S * .24)], fill=(255, 255, 255, 255))         # eye holes
    d.polygon([(S * .62, S * .14), (S * .52, S * .18), (S * .6, S * .24)], fill=(255, 255, 255, 255))
    d.line([(S * .5, S * .04), (S * .5, S * .12)], fill=(250, 210, 40, 255), width=6)                          # mask stripe
    d.ellipse([S * .44, S * .27, S * .56, S * .33], fill=(220, 60, 60, 255))                                    # mouth hole
    d.rounded_rectangle([S * .3, S * .34, S * .7, S * .66], 10, fill=(200, 150, 110, 255), outline=OUT, width=5)
    d.rectangle([S * .3, S * .6, S * .7, S * .74], fill=(40, 90, 200, 255), outline=OUT, width=4)             # trunks
    d.line([(S * .38, S * .74), (S * .26, S * .96)], fill=OUT, width=int(S * .1))
    d.line([(S * .38, S * .74), (S * .26, S * .96)], fill=(200, 150, 110, 255), width=int(S * .06))
    d.line([(S * .62, S * .74), (S * .78, S * .62)], fill=OUT, width=int(S * .1))                              # knee up
    d.line([(S * .62, S * .74), (S * .78, S * .62)], fill=(200, 150, 110, 255), width=int(S * .06))
    d.line([(S * .7, S * .4), (S * .9, S * .28)], fill=OUT, width=int(S * .1))                                  # the elbow
    d.line([(S * .7, S * .4), (S * .9, S * .28)], fill=(200, 150, 110, 255), width=int(S * .06))
    return _shrink(im, size)


def bouncy_castle(size=64):
    """A kids' inflatable bouncy castle: red and yellow puffy turrets, a blue mesh doorway."""
    im, d, S = _big(size)
    OUT = (60, 10, 10, 255)
    d.rounded_rectangle([S * .06, S * .36, S * .94, S * .96], 16, fill=(230, 50, 50, 255), outline=OUT, width=6)
    for x in (.04, .74):                                                                                          # turrets
        d.rounded_rectangle([S * x, S * .1, S * (x + .22), S * .5], 12, fill=(250, 210, 40, 255), outline=OUT, width=6)
        d.ellipse([S * (x + .02), S * .02, S * (x + .2), S * .18], fill=(40, 120, 230, 255), outline=OUT, width=5)
    d.rounded_rectangle([S * .32, S * .5, S * .68, S * .9], 20, fill=(80, 150, 240, 255), outline=OUT, width=5)
    for k in range(4):
        x = .38 + k * .08
        d.line([(S * x, S * .52), (S * x, S * .88)], fill=(40, 90, 180, 255), width=3)
    for x in (.18, .82):
        d.line([(S * x, S * .5), (S * x, S * .92)], fill=(200, 30, 30, 255), width=4)                           # puffy seams
    return _shrink(im, size)


def grudge_dartboard(size=64):
    """A pub dartboard with a photo of the foe pinned dead center - a big X already drawn on it."""
    im, d, S = _big(size)
    OUT = (15, 15, 15, 255)
    import math
    d.ellipse([S * .04, S * .04, S * .96, S * .96], fill=(20, 20, 20, 255), outline=OUT, width=6)
    for k in range(20):
        a0, a1 = k * 18 - 9, k * 18 + 9
        d.pieslice([S * .1, S * .1, S * .9, S * .9], a0, a1, fill=(240, 220, 170, 255) if k % 2 else (30, 30, 30, 255))
    d.ellipse([S * .1, S * .1, S * .9, S * .9], outline=(200, 40, 40, 255), width=5)
    d.rectangle([S * .32, S * .3, S * .68, S * .72], fill=(250, 250, 245, 255), outline=OUT, width=4)        # the photo
    d.ellipse([S * .42, S * .36, S * .58, S * .5], fill=(120, 110, 100, 255))
    d.chord([S * .36, S * .48, S * .64, S * .76], 180, 360, fill=(120, 110, 100, 255))
    d.line([(S * .34, S * .32), (S * .66, S * .7)], fill=(220, 20, 20, 255), width=5)
    d.line([(S * .66, S * .32), (S * .34, S * .7)], fill=(220, 20, 20, 255), width=5)
    d.ellipse([S * .47, S * .02, S * .53, S * .08], fill=(170, 170, 180, 255))                                  # the tack
    return _shrink(im, size)


def throw_dart(size=32):
    """A dart pointing right: steel tip, knurled barrel, red flights."""
    im, d, S = _big(size)
    OUT = (20, 20, 20, 255)
    d.polygon([(S * .02, S * .3), (S * .26, S * .44), (S * .26, S * .56), (S * .02, S * .7)], fill=(220, 30, 40, 255), outline=OUT)
    d.rectangle([S * .24, S * .44, S * .66, S * .56], fill=(170, 170, 180, 255), outline=OUT, width=4)
    d.line([(S * .66, S * .5), (S * .98, S * .5)], fill=(210, 210, 220, 255), width=4)
    return _shrink(im, size)


def feather_duster(size=64):
    """A rainbow feather duster: a fat fluffy head of colored plumes on a wood handle."""
    im, d, S = _big(size)
    OUT = (40, 20, 10, 255)
    d.line([(S * .1, S * .92), (S * .5, S * .5)], fill=OUT, width=int(S * .09))
    d.line([(S * .1, S * .92), (S * .5, S * .5)], fill=(180, 120, 60, 255), width=int(S * .05))
    import math
    cols = [(250, 80, 120, 255), (250, 180, 40, 255), (80, 200, 230, 255), (150, 90, 230, 255), (90, 210, 110, 255)]
    for k in range(16):
        a = -math.pi * .9 + k * math.pi * 1.1 / 15
        x, y = .66 + .26 * math.cos(a), .34 + .26 * math.sin(a)
        d.ellipse([S * (x - .1), S * (y - .1), S * (x + .1), S * (y + .1)], fill=cols[k % 5])
    d.ellipse([S * .5, S * .2, S * .8, S * .5], fill=(250, 240, 250, 255))
    return _shrink(im, size)


def galaxy_durag(size=64):
    """A galaxy-print durag: deep purple-blue satin printed with stars and a nebula swirl, long tails flowing."""
    im, d, S = _big(size)
    OUT = (20, 10, 40, 255)
    d.chord([S * .12, S * .1, S * .88, S * .9], 180, 360, fill=(50, 30, 120, 255), outline=OUT, width=6)
    d.rectangle([S * .12, S * .46, S * .88, S * .56], fill=(40, 25, 100, 255), outline=OUT, width=5)
    for pts in (((.8, .5), (.98, .66), (.9, .96)), ((.76, .54), (.88, .8), (.74, .98))):                        # tails
        d.line([(S * x, S * y) for x, y in pts], fill=OUT, width=int(S * .1), joint="curve")
        d.line([(S * x, S * y) for x, y in pts], fill=(70, 40, 150, 255), width=int(S * .06), joint="curve")
    d.ellipse([S * .3, S * .18, S * .62, S * .4], fill=(200, 80, 200, 140))                                     # nebula
    for x, y in ((.24, .3), (.4, .16), (.56, .36), (.7, .24), (.46, .42), (.34, .4)):
        d.ellipse([S * (x - .02), S * (y - .02), S * (x + .02), S * (y + .02)], fill=(255, 255, 255, 255))
    d.line([(S * .66, S * .28), (S * .74, S * .28)], fill=(255, 255, 220, 255), width=3)
    d.line([(S * .7, S * .24), (S * .7, S * .32)], fill=(255, 255, 220, 255), width=3)
    return _shrink(im, size)
