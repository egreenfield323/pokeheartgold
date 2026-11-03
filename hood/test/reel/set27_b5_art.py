

# ---- set 27, batch 5: Glow Up, Stomach Bug, Rabbit Foot, Stiff Arm, Hype Howl -------------------------------------------

def gas_hot_dog(size=64):
    """A gas station roller-grill hot dog in a paper boat: wrinkly shiny dog, grill stripes, mustard zigzag."""
    im, d, S = _big(size)
    OUT = (60, 20, 10, 255)
    d.polygon([(S * .04, S * .5), (S * .96, S * .5), (S * .86, S * .8), (S * .14, S * .8)], fill=(250, 250, 245, 255), outline=OUT)
    d.line([(S * .04, S * .5), (S * .96, S * .5), (S * .86, S * .8), (S * .14, S * .8), (S * .04, S * .5)], fill=OUT, width=5)
    d.rounded_rectangle([S * .1, S * .36, S * .9, S * .6], 20, fill=(230, 180, 110, 255), outline=OUT, width=6)  # bun
    d.rounded_rectangle([S * .04, S * .3, S * .96, S * .46], 18, fill=(170, 60, 40, 255), outline=OUT, width=6)  # the dog
    for x in (.24, .44, .64, .84):
        d.line([(S * x, S * .31), (S * (x - .04), S * .45)], fill=(110, 30, 20, 255), width=4)                  # grill stripes
    d.line([(S * .14, S * .34), (S * .34, S * .32)], fill=(255, 180, 160, 255), width=4)                        # sheen
    d.line([(S * x, S * (.34 if k % 2 else .4)) for k, x in enumerate([.16, .26, .36, .46, .56, .66, .76, .86])], fill=(250, 210, 30, 255), width=5)
    return _shrink(im, size)


def out_of_order(size=64):
    """A hand-written OUT OF ORDER sign on cardboard, hung on a string (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (80, 50, 20, 255)
    d.line([(S * .2, S * .3), (S * .5, S * .06), (S * .8, S * .3)], fill=(60, 60, 60, 255), width=4)
    d.rectangle([S * .06, S * .28, S * .94, S * .78], fill=(215, 175, 115, 255), outline=OUT, width=6)
    im = _shrink(im, size)
    return _texted(im, [("OUT OF", (32, 25)), ("ORDER", (32, 35))], (200, 20, 20, 255), (255, 235, 200, 255))


def rabbit_foot(size=32):
    """A lucky rabbit foot keychain: dyed-green fuzzy foot, a gold cap and ring."""
    im, d, S = _big(size)
    OUT = (20, 60, 20, 255)
    d.ellipse([S * .2, S * .34, S * .74, S * .96], fill=(80, 200, 90, 255), outline=OUT, width=5)
    for x, y in ((.3, .78), (.46, .84), (.62, .78)):
        d.ellipse([S * x, S * y, S * (x + .1), S * (y + .1)], fill=(140, 230, 140, 255))
    d.rectangle([S * .34, S * .24, S * .6, S * .38], fill=(250, 210, 50, 255), outline=(120, 90, 0, 255), width=4)
    d.ellipse([S * .38, S * .02, S * .56, S * .24], outline=(250, 210, 50, 255), width=5)
    return _shrink(im, size)


def scratch_ticket(size=64, stage=0):
    """A scratch-off lottery ticket: LUCKY 7s, three silver panels scratched off one by one; stage 3 = WINNER $2
    (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 20, 60, 255)
    d.rectangle([S * .04, S * .12, S * .96, S * .88], fill=(250, 230, 90, 255), outline=OUT, width=6)
    d.rectangle([S * .04, S * .12, S * .96, S * .3], fill=(200, 40, 140, 255), outline=OUT, width=6)
    for k in range(3):
        x = .12 + k * .27
        d.rectangle([S * x, S * .4, S * (x + .22), S * .66], fill=(255, 255, 255, 255) if k < stage else (190, 195, 205, 255), outline=OUT, width=4)
    im = _shrink(im, size)
    words = [("LUCKY 7", (32, 9))] + [("7", (round(S / 4 * 0 + 12 + k * 17.3) + 2, 29)) for k in range(min(stage, 3))]
    if stage >= 3:
        words.append(("WIN $2", (32, 45)))
    return _texted(im, words, (40, 20, 60, 255), (255, 255, 255, 255))


def heisman_statue(size=64):
    """A gold football trophy figure mid stiff-arm: one leg kicked up, ball tucked, the arm straight out, on a base."""
    im, d, S = _big(size)
    OUT = (110, 70, 0, 255)
    G = (250, 200, 50, 255)
    d.rectangle([S * .26, S * .84, S * .74, S * .98], fill=(60, 40, 20, 255), outline=OUT, width=5)            # base
    d.ellipse([S * .44, S * .06, S * .58, S * .2], fill=G, outline=OUT, width=4)                                 # helmet
    d.polygon([(S * .42, S * .2), (S * .6, S * .2), (S * .62, S * .5), (S * .4, S * .5)], fill=G, outline=OUT)  # body
    d.line([(S * .42, S * .26), (S * .1, S * .24)], fill=OUT, width=int(S * .09))                               # the stiff arm
    d.line([(S * .42, S * .26), (S * .1, S * .24)], fill=G, width=int(S * .05))
    d.ellipse([S * .58, S * .26, S * .76, S * .4], fill=(200, 140, 30, 255), outline=OUT, width=4)               # ball
    d.line([(S * .46, S * .5), (S * .44, S * .84)], fill=OUT, width=int(S * .09))                               # plant leg
    d.line([(S * .46, S * .5), (S * .44, S * .84)], fill=G, width=int(S * .05))
    d.line([(S * .56, S * .5), (S * .82, S * .62), (S * .78, S * .44)], fill=OUT, width=int(S * .09))          # kicked leg
    d.line([(S * .56, S * .5), (S * .82, S * .62), (S * .78, S * .44)], fill=G, width=int(S * .05))
    return _shrink(im, size)


def howl_crowd(size=64, howl=False):
    """A row of fans in the stands (silhouettes in team colors) - heads thrown back, mouths open when they howl."""
    im, d, S = _big(size)
    OUT = (15, 15, 25, 255)
    for k in range(5):
        x = .02 + k * .2
        col = [(200, 40, 50, 255), (40, 80, 200, 255), (230, 180, 40, 255), (40, 160, 80, 255), (150, 60, 180, 255)][k]
        d.rounded_rectangle([S * x, S * .58, S * (x + .16), S * 1.0], 8, fill=col, outline=OUT, width=4)
        hy = .36 if howl else .42
        d.ellipse([S * (x + .01), S * hy, S * (x + .15), S * (hy + .18)], fill=(170, 120, 90, 255) if k % 2 else (230, 190, 150, 255), outline=OUT, width=4)
        if howl:
            d.ellipse([S * (x + .05), S * (hy + .02), S * (x + .11), S * (hy + .09)], fill=(60, 10, 20, 255))
    d.rectangle([S * .0, S * .88, S * 1.0, S * 1.0], fill=(120, 120, 130, 255), outline=OUT, width=4)        # the rail
    return _shrink(im, size)


def satin_bonnet(size=64):
    """A shiny pink satin bonnet, puffed round with an elastic band."""
    im, d, S = _big(size)
    OUT = (110, 20, 70, 255)
    d.ellipse([S * .1, S * .14, S * .9, S * .78], fill=(240, 120, 190, 255), outline=OUT, width=7)
    d.chord([S * .1, S * .5, S * .9, S * .86], 0, 180, fill=(250, 160, 210, 255), outline=OUT, width=6)
    for k in range(5):
        x = .2 + k * .15
        d.line([(S * x, S * .7), (S * (x + .02), S * .78)], fill=OUT, width=3)                                 # elastic gathers
    d.arc([S * .22, S * .22, S * .6, S * .56], 200, 290, fill=(255, 220, 240, 255), width=7)                    # satin shine
    return _shrink(im, size)


def edge_gel(size=32):
    """A tub of edge control: squat jar, black lid, orange label."""
    im, d, S = _big(size)
    OUT = (20, 20, 20, 255)
    d.rounded_rectangle([S * .14, S * .36, S * .86, S * .92], 8, fill=(240, 235, 225, 255), outline=OUT, width=5)
    d.rectangle([S * .1, S * .2, S * .9, S * .38], fill=(30, 30, 30, 255), outline=OUT, width=4)
    d.rectangle([S * .2, S * .5, S * .8, S * .76], fill=(250, 140, 30, 255))
    return _shrink(im, size)


def edge_brush(size=32):
    """A little edge brush: a skinny black handle with a tiny bristle head."""
    im, d, S = _big(size)
    OUT = (10, 10, 10, 255)
    d.line([(S * .1, S * .9), (S * .66, S * .34)], fill=(30, 30, 30, 255), width=7)
    d.rounded_rectangle([S * .6, S * .1, S * .92, S * .4], 6, fill=(240, 240, 240, 255), outline=OUT, width=4)
    for k in range(4):
        x = .64 + k * .07
        d.line([(S * x, S * .14), (S * x, S * .36)], fill=(120, 120, 120, 255), width=2)
    return _shrink(im, size)
