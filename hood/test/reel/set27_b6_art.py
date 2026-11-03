

# ---- set 27, batch 6: Namaste, Lock Up, Look at Me, Snowball, Hoverboard -------------------------------------------------

def yoga_mat(size=64):
    """A purple yoga mat rolled out flat (seen from the front, in perspective), the rolled-up end curling at the back."""
    im, d, S = _big(size)
    OUT = (50, 20, 70, 255)
    d.rounded_rectangle([S * .02, S * .7, S * .84, S * .82], 6, fill=(150, 80, 200, 255), outline=OUT, width=6)   # flat mat
    d.line([(S * .06, S * .76), (S * .8, S * .76)], fill=(180, 120, 230, 255), width=3)
    d.ellipse([S * .74, S * .54, S * .98, S * .84], fill=(170, 100, 220, 255), outline=OUT, width=6)              # the roll
    d.ellipse([S * .8, S * .62, S * .92, S * .76], fill=(110, 50, 150, 255), outline=OUT, width=3)
    return _shrink(im, size)


def roll_gate(size=64, tag=True):
    """A corner store's roll-down security gate: corrugated steel slats, a spray-painted tag, the bottom bar."""
    im, d, S = _big(size)
    OUT = (40, 40, 45, 255)
    d.rectangle([S * .02, S * .0, S * .98, S * .96], fill=(160, 165, 170, 255), outline=OUT, width=6)
    for k in range(10):
        y = .06 + k * .09
        d.line([(S * .04, S * y), (S * .96, S * y)], fill=(120, 125, 130, 255), width=4)
        d.line([(S * .04, S * (y + .02)), (S * .96, S * (y + .02))], fill=(190, 195, 200, 255), width=2)
    if tag:
        d.line([(S * x, S * y) for x, y in ((.2, .5), (.3, .3), (.36, .56), (.46, .34), (.54, .58), (.64, .32), (.78, .5))],
               fill=(230, 40, 140, 255), width=8, joint="curve")
        d.line([(S * .18, S * .62), (S * .8, S * .58)], fill=(40, 160, 230, 255), width=5)
    d.rectangle([S * .02, S * .88, S * .98, S * .98], fill=(90, 90, 95, 255), outline=OUT, width=5)
    return _shrink(im, size)


def big_padlock(size=32):
    """A heavy brass padlock, shackle closed."""
    im, d, S = _big(size)
    OUT = (80, 50, 0, 255)
    d.arc([S * .24, S * .04, S * .76, S * .6], 180, 360, fill=(170, 170, 180, 255), width=int(S * .1))
    d.line([(S * .29, S * .32), (S * .29, S * .48)], fill=(170, 170, 180, 255), width=int(S * .1))
    d.line([(S * .71, S * .32), (S * .71, S * .48)], fill=(170, 170, 180, 255), width=int(S * .1))
    d.rounded_rectangle([S * .14, S * .44, S * .86, S * .96], 8, fill=(220, 170, 50, 255), outline=OUT, width=5)
    d.ellipse([S * .44, S * .6, S * .56, S * .72], fill=(40, 30, 10, 255))
    d.line([(S * .5, S * .7), (S * .5, S * .84)], fill=(40, 30, 10, 255), width=4)
    return _shrink(im, size)


def marquee_arrow(size=64, phase=0):
    """A Vegas marquee arrow sign pointing down-left: LOOK in red, chase bulbs round the edge (phase flips which glow)
    (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (60, 20, 0, 255)
    pts = [(S * .1, S * .14), (S * .9, S * .14), (S * .9, S * .52), (S * .4, S * .52), (S * .4, S * .7), (S * .06, S * .5), (S * .4, S * .3), (S * .4, S * .42), (S * .1, S * .42)]
    pts = [(S * .2, S * .1), (S * .96, S * .1), (S * .96, S * .46), (S * .36, S * .46), (S * .36, S * .62), (S * .04, S * .3), (S * .36, S * .0), (S * .36, S * .1)]
    _outline_poly(d, pts, (250, 220, 90, 255), OUT, 6)
    import math
    for k, (x, y) in enumerate(((.42, .14), (.54, .14), (.66, .14), (.78, .14), (.9, .14), (.9, .42), (.78, .42), (.66, .42), (.54, .42), (.42, .42))):
        on = (k + phase) % 2 == 0
        d.ellipse([S * (x - .03), S * (y - .03), S * (x + .03), S * (y + .03)], fill=(255, 255, 230, 255) if on else (170, 120, 40, 255))
    im = _shrink(im, size)
    return _texted(im, [("LOOK", (42, 12))], (220, 30, 30, 255), (255, 240, 200, 255))


def snowball(size=32):
    """A hand-packed snowball: lumpy white with blue shading."""
    im, d, S = _big(size)
    OUT = (90, 120, 160, 255)
    d.ellipse([S * .12, S * .12, S * .88, S * .88], fill=(245, 250, 255, 255), outline=OUT, width=6)
    for x, y in ((.3, .58), (.54, .66), (.62, .4)):
        d.ellipse([S * x, S * y, S * (x + .14), S * (y + .1)], fill=(200, 220, 240, 255))
    d.arc([S * .22, S * .2, S * .56, S * .5], 200, 280, fill=(255, 255, 255, 255), width=5)
    return _shrink(im, size)


def hoverboard(size=64, glow=False):
    """A self-balancing hoverboard: two wheels in fenders, a black deck with blue LED strips - glowing underneath if lit."""
    im, d, S = _big(size)
    OUT = (10, 10, 20, 255)
    if glow:
        d.ellipse([S * .04, S * .72, S * .96, S * .98], fill=(80, 200, 255, 150))
    for x in (.04, .7):                                                                                        # wheels + fenders
        d.chord([S * x, S * .36, S * (x + .26), S * .86], 180, 360, fill=(240, 240, 245, 255), outline=OUT, width=6)
        d.ellipse([S * (x + .03), S * .5, S * (x + .23), S * .82], fill=(40, 40, 46, 255), outline=OUT, width=5)
    d.rounded_rectangle([S * .22, S * .54, S * .78, S * .7], 8, fill=(30, 30, 36, 255), outline=OUT, width=6)
    d.line([(S * .28, S * .66), (S * .72, S * .66)], fill=(60, 180, 255, 255), width=5)
    for x in (.3, .56):
        d.rounded_rectangle([S * x, S * .54, S * (x + .14), S * .6], 3, fill=(80, 80, 90, 255))                 # foot pads
    return _shrink(im, size)


def marquee_down(size=64, phase=0):
    """A Vegas marquee sign pointing straight down: LOOK in red on a gold board, chase bulbs round it, the arrow tip
    below (phase flips which bulbs glow) (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (60, 20, 0, 255)
    pts = [(S * .06, S * .08), (S * .94, S * .08), (S * .94, S * .5), (S * .7, S * .5), (S * .5, S * .82), (S * .3, S * .5), (S * .06, S * .5)]
    _outline_poly(d, pts, (250, 220, 90, 255), OUT, 6)
    bulbs = [(.14 + k * .12, .15) for k in range(7)] + [(.86 - k * .12, .43) for k in range(7)]
    for k, (x, y) in enumerate(bulbs):
        on = (k + phase) % 2 == 0
        d.ellipse([S * (x - .03), S * (y - .03), S * (x + .03), S * (y + .03)], fill=(255, 255, 230, 255) if on else (170, 120, 40, 255))
    d.polygon([(S * .42, S * .54), (S * .58, S * .54), (S * .5, S * .7)], fill=(255, 255, 230, 255) if phase else (220, 60, 40, 255))
    im = _shrink(im, size)
    return _texted(im, [("LOOK", (32, 15))], (220, 30, 30, 255), (255, 240, 200, 255))
