

# ---- set 20 redo, batch D3: Stab Combo, Ride or Die -------------------------------------------------------

def handcuff(size=32):
    """One steel handcuff, snapped shut, a chain link hanging off it."""
    im, d, S = _big(size)
    OUT = (20, 20, 26, 255)
    d.ellipse([S * .1, S * .2, S * .7, S * .8], outline=OUT, width=14)
    d.ellipse([S * .1, S * .2, S * .7, S * .8], outline=(190, 195, 210, 255), width=8)
    d.rectangle([S * .54, S * .36, S * .76, S * .56], fill=(150, 155, 170, 255), outline=OUT, width=4)        # the lock box
    d.ellipse([S * .74, S * .38, S * .96, S * .56], outline=(190, 195, 210, 255), width=6)                    # a link
    d.arc([S * .16, S * .26, S * .4, S * .5], 180, 260, fill=(255, 255, 255, 255), width=4)
    return _shrink(im, size)


def cuff_key(size=32):
    """A little silver handcuff key."""
    im, d, S = _big(size)
    OUT = (20, 20, 26, 255)
    d.ellipse([S * .06, S * .3, S * .4, S * .64], fill=(200, 205, 220, 255), outline=OUT, width=6)
    d.ellipse([S * .16, S * .4, S * .3, S * .54], fill=(0, 0, 0, 0), outline=OUT, width=4)
    d.rectangle([S * .38, S * .42, S * .9, S * .52], fill=(200, 205, 220, 255), outline=OUT, width=4)
    d.rectangle([S * .76, S * .52, S * .86, S * .66], fill=(200, 205, 220, 255), outline=OUT, width=4)
    return _shrink(im, size)
