

# ---- set 28, batch 6: Blend In, Night Vision, Paranoia, Fresh Scent, Mood Swap ----------------------------------------------

def hivis_vest(size=64):
    """A hi-vis safety vest: neon yellow-green with two silver reflective stripes, open front."""
    im, d, S = _big(size)
    OUT = (60, 70, 0, 255)
    d.rectangle([S * .28, S * .1, S * .72, S * .96], fill=(170, 200, 30, 255), outline=OUT, width=5)   # the back, seen through the front
    d.arc([S * .3, S * -.04, S * .7, S * .24], 0, 180, fill=OUT, width=6)                                      # neckline
    for flip in (False, True):
        xs = (lambda x: 1 - x) if flip else (lambda x: x)
        pts = [(xs(.1), .1), (xs(.32), .1), (xs(.44), .5), (xs(.44), .96), (xs(.08), .96), (xs(.04), .4)]
        _outline_poly(d, [(S * x, S * y) for x, y in pts], (210, 250, 40, 255), OUT, 6)
        for y in (.6, .78):
            d.line([(S * xs(.06), S * y), (S * xs(.44), S * y)], fill=(210, 215, 225, 255), width=7)
    return _shrink(im, size)


def work_clipboard(size=32):
    """A brown clipboard with a checklist - looks official."""
    im, d, S = _big(size)
    OUT = (60, 35, 10, 255)
    d.rounded_rectangle([S * .14, S * .1, S * .86, S * .96], 6, fill=(180, 120, 60, 255), outline=OUT, width=5)
    d.rectangle([S * .22, S * .2, S * .78, S * .88], fill=(250, 250, 245, 255))
    d.rectangle([S * .36, S * .04, S * .64, S * .16], fill=(170, 170, 180, 255), outline=OUT, width=4)
    for y in (.34, .5, .66):
        d.line([(S * .28, S * y), (S * .36, S * (y + .06)), (S * .44, S * (y - .04))], fill=(40, 160, 60, 255), width=4)
        d.line([(S * .5, S * y), (S * .72, S * y)], fill=(150, 150, 160, 255), width=3)
    return _shrink(im, size)


def nv_goggles(size=64):
    """Night vision goggles: a black binocular housing on a head strap, two glowing green lenses."""
    im, d, S = _big(size)
    OUT = (10, 10, 10, 255)
    d.line([(S * .0, S * .5), (S * 1.0, S * .5)], fill=(40, 40, 40, 255), width=8)
    d.rounded_rectangle([S * .14, S * .3, S * .86, S * .7], 12, fill=(40, 45, 40, 255), outline=OUT, width=6)
    for x in (.2, .54):
        d.ellipse([S * x, S * .32, S * (x + .26), S * .68], fill=(30, 30, 30, 255), outline=OUT, width=5)
        d.ellipse([S * (x + .04), S * .36, S * (x + .22), S * .64], fill=(80, 255, 110, 255))
        d.ellipse([S * (x + .06), S * .38, S * (x + .12), S * .46], fill=(220, 255, 220, 255))
    d.rectangle([S * .44, S * .16, S * .56, S * .32], fill=(40, 45, 40, 255), outline=OUT, width=4)          # the mount
    return _shrink(im, size)


def thought_cloud(size=64, lines=("?",)):
    """A cloud-shaped thought bubble with trailing puffs bottom-left, holding a 3 a.m. thought (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (30, 30, 40, 255)
    blobs = [(.06, .3, .4, .64), (.24, .16, .62, .52), (.5, .18, .9, .54), (.62, .34, .98, .68), (.3, .42, .74, .76), (.06, .46, .4, .76)]
    for b in blobs:
        d.ellipse([S * v for v in b], fill=OUT)
    for b in blobs:
        d.ellipse([S * (b[0] + .03), S * (b[1] + .03), S * (b[2] - .03), S * (b[3] - .03)], fill=(255, 255, 255, 255))
    for x, y, r in ((.18, .84, .05), (.08, .94, .03)):
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], fill=(255, 255, 255, 255), outline=OUT, width=4)
    im = _shrink(im, size)
    y0 = 31 - 4 * len(lines)
    return _texted(im, [(t, (33, y0 + k * 8)) for k, t in enumerate(lines)], (30, 30, 40, 255), (255, 255, 255, 255))


def freshener_tree(size=32, col=0):
    """A little pine-tree car air freshener on its string (green, red or black ice)."""
    im, d, S = _big(size)
    c = [(60, 170, 70, 255), (220, 50, 60, 255), (30, 30, 40, 255)][col % 3]
    OUT = (20, 40, 20, 255)
    d.line([(S * .5, S * .0), (S * .5, S * .22)], fill=(250, 250, 250, 255), width=3)
    pts = [(.5, .18), (.66, .4), (.58, .4), (.76, .6), (.64, .6), (.84, .84), (.56, .84), (.56, .96), (.44, .96), (.44, .84),
           (.16, .84), (.36, .6), (.24, .6), (.42, .4), (.34, .4)]
    _outline_poly(d, [(S * x, S * y) for x, y in pts], c, OUT, 4)
    return _shrink(im, size)


def mood_ring(size=32, col=0):
    """A mood ring: a silver band with a big oval stone (0 = red angry, 1 = blue chill, 2 = purple swapped)."""
    im, d, S = _big(size)
    OUT = (60, 60, 70, 255)
    stone = [(220, 40, 50, 255), (40, 130, 240, 255), (160, 60, 220, 255)][col % 3]
    d.ellipse([S * .14, S * .4, S * .86, S * .96], outline=(200, 205, 215, 255), width=int(S * .1))
    d.ellipse([S * .14, S * .4, S * .86, S * .96], outline=OUT, width=3)
    d.ellipse([S * .28, S * .04, S * .72, S * .5], fill=stone, outline=OUT, width=5)
    d.ellipse([S * .36, S * .1, S * .5, S * .24], fill=(255, 255, 255, 200))
    return _shrink(im, size)
