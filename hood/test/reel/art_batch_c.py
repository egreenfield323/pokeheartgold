

# ---- set 20 redo, batch C: Vape Cloud, Plug In, Bed Bugs, Shakedown, Loud Pack ---------------------------

def vape_mod(size=64):
    """A chunky box-mod vape held upright: the tank with purple juice, the drip tip, the fire button, a little
    screen reading 80W."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rounded_rectangle([S * .3, S * .44, S * .7, S * .96], 10, fill=(50, 50, 60, 255), outline=OUT, width=7)    # the box
    d.rectangle([S * .38, S * .52, S * .62, S * .64], fill=(120, 220, 140, 255), outline=OUT, width=4)        # screen
    d.ellipse([S * .44, S * .72, S * .56, S * .84], fill=(220, 40, 40, 255), outline=OUT, width=4)            # fire button
    d.rectangle([S * .4, S * .16, S * .6, S * .44], fill=(170, 90, 220, 180), outline=OUT, width=6)          # tank
    d.line([(S * .44, S * .2), (S * .44, S * .4)], fill=(240, 220, 255, 255), width=5)
    d.rounded_rectangle([S * .44, S * .04, S * .56, S * .16], 5, fill=(30, 30, 34, 255), outline=OUT, width=4)   # drip tip
    d.line([(S * .34, S * .5), (S * .34, S * .9)], fill=(110, 110, 125, 255), width=5)
    return _shrink(im, size)


def cool_shades(size=64):
    """Black wraparound shades with a white glint - the only thing you can see in the cloud."""
    im, d, S = _big(size)
    OUT = (5, 5, 8, 255)
    d.line([(S * .04, S * .4), (S * .96, S * .4)], fill=OUT, width=10)
    for x in (.06, .54):
        d.rounded_rectangle([S * x, S * .36, S * (x + .4), S * .62], 14, fill=(20, 20, 26, 255), outline=OUT, width=6)
        d.line([(S * (x + .08), S * .44), (S * (x + .18), S * .44)], fill=(255, 255, 255, 255), width=6)
    return _shrink(im, size)


def phone_charge(size=64, level="1%"):
    """A phone face-on at a battery level: a battery icon with the % (red at 1-3%, green at 100%), the cable
    plugged in at the bottom (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (10, 10, 14, 255)
    full = level == "100%"
    d.rounded_rectangle([S * .2, S * .02, S * .8, S * .86], 16, fill=(30, 30, 36, 255), outline=OUT, width=8)
    d.rounded_rectangle([S * .25, S * .09, S * .75, S * .78], 8, fill=(20, 24, 34, 255))
    d.rounded_rectangle([S * .32, S * .26, S * .64, S * .44], 5, outline=(240, 240, 240, 255), width=5)
    d.rectangle([S * .64, S * .31, S * .68, S * .39], fill=(240, 240, 240, 255))
    fill = (60, 220, 90, 255) if full else (230, 40, 40, 255)
    d.rectangle([S * .35, S * .29, S * (.36 + (.26 if full else .03)), S * .41], fill=fill)
    d.line([(S * .5, S * .86), (S * .5, S * .99)], fill=(240, 240, 240, 255), width=8)                       # the cable
    im = _shrink(im, size)
    return _texted(im, [(level, (32, 33))], fill, font=GLYPHS)


def fast_charger(size=64):
    """A giant brick wall charger, FAST on it in yellow, a lightning bolt, the thick cable whipping off."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rounded_rectangle([S * .16, S * .14, S * .84, S * .76], 12, fill=(245, 245, 245, 255), outline=OUT, width=8)
    for x in (.34, .58):
        d.rectangle([S * x, S * .02, S * (x + .08), S * .16], fill=(190, 190, 200, 255), outline=OUT, width=4)    # prongs
    d.polygon([(S * .52, S * .24), (S * .38, S * .48), (S * .5, S * .48), (S * .44, S * .66), (S * .64, S * .4),
               (S * .52, S * .4), (S * .6, S * .24)], fill=(250, 210, 30, 255), outline=OUT)
    d.line([(S * .5, S * .76), (S * .5, S * .86), (S * .8, S * .96)], fill=(245, 245, 245, 255), width=10)
    d.line([(S * .5, S * .76), (S * .5, S * .86), (S * .8, S * .96)], fill=OUT, width=3)
    return _shrink(im, size)


def motel_bed(size=64):
    """A sad motel bed: brown headboard, a saggy mattress with a stain, a thin floral blanket, one flat pillow."""
    im, d, S = _big(size)
    OUT = (40, 25, 15, 255)
    d.rounded_rectangle([S * .02, S * .22, S * .2, S * .78], 6, fill=(120, 70, 40, 255), outline=OUT, width=6)    # headboard
    d.rectangle([S * .14, S * .5, S * .98, S * .72], fill=(230, 220, 200, 255), outline=OUT, width=6)          # mattress
    d.ellipse([S * .56, S * .54, S * .7, S * .62], fill=(200, 180, 120, 255))                                 # the stain
    d.rectangle([S * .4, S * .44, S * .98, S * .6], fill=(200, 110, 120, 255), outline=OUT, width=5)          # blanket
    for x in (.48, .64, .8, .92):
        d.ellipse([S * x, S * .48, S * (x + .05), S * .53], fill=(250, 220, 90, 255))
    d.rounded_rectangle([S * .18, S * .42, S * .38, S * .52], 8, fill=(250, 250, 245, 255), outline=OUT, width=5)  # pillow
    for x in (.18, .92):
        d.rectangle([S * x, S * .72, S * (x + .05), S * .84], fill=(80, 50, 30, 255))
    return _shrink(im, size)


def key_ring(size=32):
    """A ring of keys: three keys, a bottle opener, a little dice charm."""
    im, d, S = _big(size)
    OUT = (40, 40, 46, 255)
    d.ellipse([S * .3, S * .04, S * .62, S * .36], outline=(200, 200, 210, 255), width=9)
    for k, (a, c) in enumerate(((-.2, (230, 200, 60)), (0, (200, 200, 210)), (.2, (190, 150, 90)))):
        x = .46 + a
        d.line([(S * .46, S * .3), (S * x, S * .7)], fill=c + (255,), width=10)
        d.ellipse([S * (x - .1), S * .64, S * (x + .1), S * .84], fill=c + (255,), outline=OUT, width=4)
    d.rectangle([S * .7, S * .3, S * .9, S * .5], fill=(240, 40, 40, 255), outline=OUT, width=4)
    for x, y in ((.75, .35), (.83, .43)):
        d.ellipse([S * x, S * y, S * (x + .04), S * (y + .04)], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def rubber_chicken(size=64):
    """A yellow rubber chicken, limp, beak open mid-squeak, red comb, orange feet."""
    im, d, S = _big(size)
    OUT = (90, 60, 0, 255)
    d.ellipse([S * .3, S * .3, S * .82, S * .62], fill=(250, 220, 50, 255), outline=OUT, width=7)                 # body
    d.line([(S * .34, S * .42), (S * .16, S * .2)], fill=(250, 220, 50, 255), width=int(S * .12))                 # neck
    d.ellipse([S * .04, S * .06, S * .26, S * .28], fill=(250, 220, 50, 255), outline=OUT, width=6)               # head
    d.polygon([(S * .08, S * .08), (S * .12, S * .0), (S * .18, S * .06), (S * .22, S * .0), (S * .24, S * .1)],
              fill=(230, 40, 40, 255), outline=OUT)
    d.polygon([(S * .04, S * .16), (S * -.0, S * .2), (S * .06, S * .24)], fill=(250, 140, 30, 255), outline=OUT)  # beak
    d.ellipse([S * .12, S * .12, S * .16, S * .16], fill=OUT)
    for x in (.48, .64):
        d.line([(S * x, S * .6), (S * (x + .02), S * .86)], fill=(250, 140, 30, 255), width=7)
        d.line([(S * (x - .04), S * .88), (S * (x + .08), S * .88)], fill=(250, 140, 30, 255), width=6)
    d.arc([S * .4, S * .34, S * .7, S * .5], 200, 320, fill=(255, 245, 180, 255), width=6)
    return _shrink(im, size)


def boombox_pack(size=64):
    """The neon fanny pack unzipped - and a little boombox sticking out of it, speakers thumping."""
    im, d, S = _big(size)
    OUT = (20, 20, 30, 255)
    d.rounded_rectangle([S * .14, S * .12, S * .86, S * .52], 8, fill=(60, 60, 70, 255), outline=OUT, width=7)    # boombox
    d.line([(S * .3, S * .12), (S * .4, S * .02), (S * .6, S * .02), (S * .7, S * .12)], fill=OUT, width=6)       # handle
    for x in (.3, .7):
        d.ellipse([S * (x - .12), S * .18, S * (x + .12), S * .46], fill=(30, 30, 36, 255), outline=(200, 200, 210, 255), width=5)
        d.ellipse([S * (x - .05), S * .26, S * (x + .05), S * .38], fill=(120, 120, 130, 255))
    d.rectangle([S * .44, S * .2, S * .56, S * .3], fill=(120, 220, 255, 255), outline=OUT, width=3)
    d.rounded_rectangle([S * .04, S * .44, S * .96, S * .84], 22, fill=(250, 60, 200, 255), outline=OUT, width=8)  # the pack
    d.line([(S * .1, S * .5), (S * .9, S * .5)], fill=(60, 255, 140, 255), width=7)                               # zip
    d.arc([S * .16, S * .52, S * .5, S * .74], 200, 260, fill=(255, 190, 240, 255), width=7)
    return _shrink(im, size)


def house_slipper(size=32):
    """A fuzzy pink house slipper, flying sole-first."""
    im, d, S = _big(size)
    OUT = (90, 20, 50, 255)
    d.ellipse([S * .06, S * .3, S * .94, S * .76], fill=(250, 150, 190, 255), outline=OUT, width=7)
    d.pieslice([S * .44, S * .24, S * .96, S * .74], 270, 450, fill=(255, 200, 225, 255), outline=OUT, width=6)
    for k in range(6):
        x = .5 + k * .07
        d.ellipse([S * x, S * .28, S * (x + .06), S * .34], fill=(255, 235, 245, 255))
    d.line([(S * .1, S * .6), (S * .5, S * .7)], fill=(160, 60, 110, 255), width=6)
    return _shrink(im, size)
