

# ---- set 23, batch 3: Sawing Logs, Snuck Him, Fence Hop, Trap House, Muah ---------------------------------------

def log_side(size=64):
    """A chunky firewood log lying on its side: rough brown bark, a knot, and the pale end with growth rings."""
    im, d, S = _big(size)
    OUT = (40, 22, 8, 255)
    d.rectangle([S * .14, S * .34, S * .8, S * .7], fill=(120, 75, 35, 255))
    d.line([(S * .14, S * .34), (S * .8, S * .34)], fill=OUT, width=7)
    d.line([(S * .14, S * .7), (S * .8, S * .7)], fill=OUT, width=7)
    d.ellipse([S * .04, S * .34, S * .24, S * .7], fill=(120, 75, 35, 255), outline=OUT, width=7)
    for y in (.42, .52, .62):
        d.line([(S * .22, S * y), (S * .7, S * (y + .02))], fill=(85, 50, 20, 255), width=4)                       # bark
    d.ellipse([S * .44, S * .44, S * .54, S * .54], fill=(85, 50, 20, 255), outline=OUT, width=3)                 # knot
    d.ellipse([S * .7, S * .32, S * .92, S * .72], fill=(230, 200, 140, 255), outline=OUT, width=7)               # end
    for r in (.06, .11):
        d.ellipse([S * (.81 - r * .55), S * (.52 - r), S * (.81 + r * .55), S * (.52 + r)], outline=(170, 120, 60, 255), width=3)
    return _shrink(im, size)


def log_half(size=64):
    """Half a split log, flying: bark on top, the pale split face underneath."""
    im, d, S = _big(size)
    OUT = (40, 22, 8, 255)
    d.chord([S * .08, S * .2, S * .92, S * .8], 180, 360, fill=(120, 75, 35, 255), outline=OUT, width=7)
    d.rectangle([S * .08, S * .48, S * .92, S * .58], fill=(235, 205, 145, 255), outline=OUT, width=6)
    for x in (.3, .5, .7):
        d.line([(S * x, S * .5), (S * (x + .06), S * .56)], fill=(190, 140, 80, 255), width=3)
    return _shrink(im, size)


def handsaw(size=64):
    """A handsaw: a shiny trapezoid blade with teeth along the bottom and a wooden D-handle."""
    im, d, S = _big(size)
    OUT = (20, 20, 26, 255)
    d.polygon([(S * .3, S * .3), (S * .96, S * .42), (S * .96, S * .56), (S * .3, S * .62)], fill=(205, 210, 220, 255))
    d.line([(S * .3, S * .3), (S * .96, S * .42), (S * .96, S * .56), (S * .3, S * .62)], fill=OUT, width=6)
    for k in range(12):
        x = .32 + k * .053
        d.polygon([(S * x, S * (.62 - k * .005)), (S * (x + .026), S * (.68 - k * .005)), (S * (x + .053), S * (.615 - k * .005))], fill=OUT)
    d.line([(S * .36, S * .36), (S * .9, S * .46)], fill=(255, 255, 255, 255), width=4)
    d.rounded_rectangle([S * .04, S * .26, S * .34, S * .68], 12, fill=(170, 100, 40, 255), outline=OUT, width=7)  # handle
    d.rounded_rectangle([S * .12, S * .38, S * .26, S * .56], 6, fill=(0, 0, 0, 0), outline=OUT, width=5)
    return _shrink(im, size)


def chainsaw(size=64):
    """An orange chainsaw: the engine body with a pull cord and handle, a long bar with the chain round it."""
    im, d, S = _big(size)
    OUT = (20, 12, 5, 255)
    d.rounded_rectangle([S * .44, S * .44, S * .98, S * .6], 14, fill=(170, 175, 185, 255), outline=OUT, width=6)  # bar
    for k in range(10):
        x = .48 + k * .05
        d.rectangle([S * x, S * .42, S * (x + .025), S * .46], fill=OUT)
        d.rectangle([S * x, S * .58, S * (x + .025), S * .62], fill=OUT)
    d.rounded_rectangle([S * .06, S * .32, S * .5, S * .74], 12, fill=(250, 120, 20, 255), outline=OUT, width=7)  # engine
    d.rectangle([S * .12, S * .4, S * .3, S * .52], fill=(40, 40, 46, 255))
    d.arc([S * .14, S * .12, S * .5, S * .48], 180, 360, fill=OUT, width=10)                                      # handle
    d.arc([S * .14, S * .12, S * .5, S * .48], 180, 360, fill=(40, 40, 46, 255), width=6)
    d.line([(S * .1, S * .5), (S * .02, S * .6)], fill=(230, 230, 230, 255), width=4)                             # pull cord
    return _shrink(im, size)


def big_z_snore(size=32):
    """A fat white Z with a dark blue outline, for loud snoring."""
    im, d, S = _big(size)
    z = [(S * .14, S * .12), (S * .86, S * .12), (S * .86, S * .3), (S * .44, S * .7), (S * .86, S * .7), (S * .86, S * .88),
         (S * .14, S * .88), (S * .14, S * .7), (S * .56, S * .3), (S * .14, S * .3)]
    _outline_poly(d, z, (255, 255, 255, 255), (30, 40, 120, 255), 9)
    return _shrink(im, size)


def impact_star(size=64):
    """A jagged yellow-white impact star with a red rim - the sucker punch landing."""
    import math
    im, d, S = _big(size)
    pts = []
    for k in range(16):
        a = k * 2 * math.pi / 16 + .2
        r = .46 if k % 2 == 0 else .2
        pts.append((S * (.5 + r * math.cos(a)), S * (.5 + r * math.sin(a))))
    _outline_poly(d, pts, (255, 235, 60, 255), (200, 30, 20, 255), 10)
    d.ellipse([S * .38, S * .38, S * .62, S * .62], fill=(255, 255, 230, 255))
    return _shrink(im, size)


def chain_fence(size=64):
    """A chain-link fence panel between two steel posts, with a red BEWARE OF DOG plaque (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 40, 46, 255)
    WIRE = (175, 180, 190, 255)
    for k in range(-6, 12):
        x = .08 + k * .1
        d.line([(S * x, S * .1), (S * (x + .8), S * .9)], fill=WIRE, width=3)
        d.line([(S * (x + .8), S * .1), (S * x, S * .9)], fill=WIRE, width=3)
    d.rectangle([0, 0, S * .06, S], fill=(0, 0, 0, 0))
    d.rectangle([S * .94, 0, S, S], fill=(0, 0, 0, 0))
    d.rectangle([0, 0, S, S * .08], fill=(0, 0, 0, 0))
    d.rectangle([0, S * .92, S, S], fill=(0, 0, 0, 0))
    d.line([(S * .08, S * .12), (S * .92, S * .12)], fill=(140, 145, 155, 255), width=8)                          # top rail
    for x in (.06, .9):
        d.rectangle([S * x, S * .04, S * (x + .06), S * .96], fill=(140, 145, 155, 255), outline=OUT, width=5)
    d.rectangle([S * .2, S * .52, S * .8, S * .8], fill=(210, 30, 30, 255), outline=OUT, width=6)                   # plaque
    im = _shrink(im, size)
    return _texted(im, [("BEWARE", (32, 35)), ("OF DOG", (32, 43))], (255, 255, 255, 255), (120, 0, 0, 255))


def guard_dog(size=64):
    """A pit bull's head and front paws popping up, barking: spiked collar, mouth wide, ears back, angry brows."""
    im, d, S = _big(size)
    OUT = (20, 15, 15, 255)
    FUR, FUR_D = (150, 140, 140, 255), (100, 92, 92, 255)
    d.ellipse([S * .16, S * .14, S * .84, S * .76], fill=FUR, outline=OUT, width=8)
    for pts in (((.18, .3), (.06, .12), (.32, .2)), ((.82, .3), (.94, .12), (.68, .2))):
        _outline_poly(d, [(S * x, S * y) for x, y in pts], FUR_D, OUT, 6)                                            # ears
    d.ellipse([S * .3, S * .42, S * .7, S * .74], fill=(220, 210, 205, 255), outline=OUT, width=6)                 # muzzle
    d.chord([S * .36, S * .52, S * .64, S * .76], 0, 180, fill=(160, 30, 40, 255), outline=OUT, width=6)          # open mouth
    for x in (.4, .56):
        d.polygon([(S * x, S * .6), (S * (x + .04), S * .67), (S * (x + .08), S * .6)], fill=(255, 255, 255, 255))   # fangs
    d.ellipse([S * .44, S * .44, S * .56, S * .52], fill=OUT)                                                       # nose
    for x0, a, b in ((.28, (.26, .3), (.44, .38)), (.58, (.56, .38), (.74, .3))):
        d.ellipse([S * x0, S * .34, S * (x0 + .12), S * .44], fill=(255, 255, 255, 255), outline=OUT, width=4)
        d.ellipse([S * (x0 + .04), S * .37, S * (x0 + .08), S * .42], fill=OUT)
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=OUT, width=7)                                       # brows
    d.rounded_rectangle([S * .2, S * .74, S * .8, S * .84], 6, fill=(30, 30, 34, 255), outline=OUT, width=4)       # collar
    for x in (.28, .4, .52, .64):
        d.polygon([(S * x, S * .74), (S * (x + .04), S * .66), (S * (x + .08), S * .74)], fill=(220, 225, 235, 255))
    for x in (.14, .66):
        d.ellipse([S * x, S * .82, S * (x + .2), S * .98], fill=FUR, outline=OUT, width=6)                          # paws
    return _shrink(im, size)


def glue_trap(size=64):
    """A flat cardboard glue trap seen from the front-top: a shiny yellow glue bed, a drip at the edge."""
    im, d, S = _big(size)
    OUT = (60, 40, 10, 255)
    d.polygon([(S * .1, S * .52), (S * .9, S * .52), (S * .98, S * .82), (S * .02, S * .82)], fill=(190, 150, 90, 255), outline=OUT)
    d.line([(S * .1, S * .52), (S * .9, S * .52), (S * .98, S * .82), (S * .02, S * .82), (S * .1, S * .52)], fill=OUT, width=7)
    d.polygon([(S * .16, S * .57), (S * .84, S * .57), (S * .9, S * .78), (S * .1, S * .78)], fill=(250, 220, 60, 255))
    d.line([(S * .22, S * .62), (S * .5, S * .62)], fill=(255, 255, 200, 255), width=5)                            # shine
    d.line([(S * .3, S * .7), (S * .42, S * .7)], fill=(255, 255, 200, 255), width=4)
    d.ellipse([S * .62, S * .78, S * .7, S * .9], fill=(250, 220, 60, 255), outline=OUT, width=3)                 # drip
    return _shrink(im, size)


def cheese_wedge(size=32):
    """A wedge of yellow cheese with holes."""
    im, d, S = _big(size)
    OUT = (90, 60, 0, 255)
    _outline_poly(d, [(S * .06, S * .78), (S * .94, S * .78), (S * .94, S * .44), (S * .06, S * .62)], (255, 210, 40, 255), OUT, 8)
    _outline_poly(d, [(S * .06, S * .62), (S * .94, S * .44), (S * .8, S * .26)], (255, 235, 120, 255), OUT, 8)
    for x, y, r in ((.3, .66, .06), (.6, .62, .08), (.8, .7, .05)):
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], fill=(220, 160, 20, 255))
    return _shrink(im, size)


def glue_strand(n=16):
    """A stretched sticky strand (alpha only): a thin wobbly vertical string with a blob."""
    import math

    def f(x, y):
        xx = 8 + 1.5 * math.sin(y / 2.5)
        return 1 if abs(x - xx) < .9 or ((x - xx) ** 2 + (y - 12) ** 2 < 4) else 0
    return _alpha(n, n, f)


def lipstick_kiss(size=64):
    """A bright red lipstick kiss print: two plump lips with the crease lines."""
    im, d, S = _big(size)
    OUT = (110, 0, 20, 255)
    R, RL = (230, 20, 60, 255), (255, 120, 150, 255)
    d.pieslice([S * .08, S * .26, S * .52, S * .66], 180, 360, fill=R)
    d.pieslice([S * .48, S * .26, S * .92, S * .66], 180, 360, fill=R)
    d.chord([S * .08, S * .3, S * .92, S * .8], 0, 180, fill=R)
    d.polygon([(S * .08, S * .46), (S * .92, S * .46), (S * .92, S * .56), (S * .08, S * .56)], fill=R)
    d.line([(S * .1, S * .52), (S * .3, S * .48), (S * .5, S * .54), (S * .7, S * .48), (S * .9, S * .52)], fill=OUT, width=7)
    for x in (.24, .4, .6, .76):
        d.line([(S * x, S * .62), (S * x, S * .72)], fill=(180, 0, 40, 255), width=4)
    d.ellipse([S * .2, S * .32, S * .34, S * .4], fill=RL)
    return _shrink(im, size)


def phone_who(size=64):
    """A phone in a pink case, the screen showing a text from bae: WHO IS / SHE?? with angry red emoji
    (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 10, 30, 255)
    d.rounded_rectangle([S * .14, S * .02, S * .86, S * .98], 18, fill=(250, 120, 180, 255), outline=OUT, width=8)
    d.rounded_rectangle([S * .2, S * .1, S * .8, S * .9], 8, fill=(250, 250, 255, 255))
    d.rounded_rectangle([S * .24, S * .3, S * .76, S * .62], 14, fill=(230, 40, 60, 255))                          # text bubble
    for x in (.34, .58):
        d.ellipse([S * x, S * .7, S * (x + .12), S * .82], fill=(240, 60, 40, 255), outline=OUT, width=4)          # angry faces
        d.line([(S * (x + .02), S * .72), (S * (x + .1), S * .75)], fill=OUT, width=3)
    d.rectangle([S * .4, S * .12, S * .6, S * .16], fill=OUT)                                                       # notch
    im = _shrink(im, size)
    return _texted(im, [("WHO IS", (32, 21)), ("SHE??", (32, 30))], (255, 255, 255, 255), (230, 40, 60, 255))
