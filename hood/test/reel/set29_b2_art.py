

# ---- set 29, batch 2: Face Swap, Caricature, Rebrand, B-Side, Take the L ------------------------------------------------

def faceswap_phone(size=64, stage=0):
    """A phone running a face-swap filter: a face outline with tracking dots; 0 = SCAN with a scan line, 1 = SWAP with
    two arrows, 2 = a sparkle and DONE (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rounded_rectangle([S * .22, S * .04, S * .78, S * .96], 14, fill=(30, 30, 36, 255), outline=OUT, width=6)
    d.rectangle([S * .27, S * .12, S * .73, S * .86], fill=(40, 30, 70, 255))
    d.ellipse([S * .36, S * .26, S * .64, S * .62], outline=(120, 255, 200, 255), width=4)
    for x, y in ((.44, .4), (.56, .4), (.5, .48), (.44, .55), (.56, .55)):
        d.ellipse([S * (x - .015), S * (y - .015), S * (x + .015), S * (y + .015)], fill=(120, 255, 200, 255))
    if stage == 0:
        d.line([(S * .28, S * .46), (S * .72, S * .46)], fill=(255, 80, 200, 255), width=4)
    elif stage == 1:
        d.arc([S * .3, S * .2, S * .7, S * .68], 200, 340, fill=(255, 220, 80, 255), width=4)
        d.arc([S * .3, S * .2, S * .7, S * .68], 20, 160, fill=(255, 220, 80, 255), width=4)
    im = _shrink(im, size)
    word = ("SCAN", "SWAP", "DONE")[stage]
    return _texted(im, [(word, (32, 44))], (255, 255, 255, 255), (60, 20, 90, 255))


def art_easel(size=64, stage=0):
    """A street artist's easel with a canvas: 0 = blank, 1 = rough pencil lines, 2 = a finished big-head caricature
    (giant head, tiny body, huge grin)."""
    im, d, S = _big(size)
    OUT = (60, 35, 10, 255)
    for a, b in (((.2, .98), (.42, .1)), ((.8, .98), (.58, .1)), ((.5, .98), (.5, .5))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(170, 110, 50, 255), width=7)
    d.rectangle([S * .14, S * .08, S * .86, S * .7], fill=(252, 250, 240, 255), outline=OUT, width=6)
    d.rectangle([S * .1, S * .68, S * .9, S * .74], fill=(170, 110, 50, 255), outline=OUT, width=3)
    if stage == 1:
        d.arc([S * .3, S * .14, S * .7, S * .5], 30, 330, fill=(120, 120, 130, 255), width=3)
        d.line([(S * .5, S * .5), (S * .5, S * .62)], fill=(120, 120, 130, 255), width=3)
    elif stage == 2:
        d.ellipse([S * .26, S * .12, S * .74, S * .54], fill=(250, 210, 170, 255), outline=(30, 30, 30, 255), width=4)   # the giant head
        for x in (.38, .56):
            d.ellipse([S * x, S * .24, S * (x + .08), S * .34], fill=(255, 255, 255, 255), outline=(30, 30, 30, 255), width=3)
        d.chord([S * .34, S * .32, S * .66, S * .5], 0, 180, fill=(255, 255, 255, 255), outline=(30, 30, 30, 255), width=3)   # grin
        d.rectangle([S * .46, S * .54, S * .54, S * .62], fill=(80, 140, 220, 255), outline=(30, 30, 30, 255), width=2)   # tiny body
        d.line([(S * .47, S * .62), (S * .45, S * .67)], fill=(30, 30, 30, 255), width=3)
        d.line([(S * .53, S * .62), (S * .55, S * .67)], fill=(30, 30, 30, 255), width=3)
    return _shrink(im, size)


def artist_pencil(size=32):
    """A big yellow pencil, point down-left."""
    im, d, S = _big(size)
    OUT = (40, 30, 0, 255)
    d.line([(S * .3, S * .7), (S * .9, S * .1)], fill=OUT, width=int(S * .2))
    d.line([(S * .3, S * .7), (S * .9, S * .1)], fill=(250, 200, 40, 255), width=int(S * .14))
    d.polygon([(S * .22, S * .64), (S * .36, S * .78), (S * .08, S * .92)], fill=(240, 210, 160, 255), outline=OUT)
    d.polygon([(S * .14, S * .82), (S * .18, S * .86), (S * .08, S * .92)], fill=(40, 40, 40, 255))
    d.line([(S * .84, S * .04), (S * .96, S * .16)], fill=(240, 140, 160, 255), width=int(S * .12))
    return _shrink(im, size)


def paint_roller(size=64):
    """A paint roller loaded with wet teal paint, drips coming off, the bent metal frame and black grip."""
    im, d, S = _big(size)
    OUT = (20, 30, 30, 255)
    d.rounded_rectangle([S * .08, S * .1, S * .74, S * .34], 12, fill=(40, 190, 180, 255), outline=OUT, width=6)
    for x in (.2, .44, .62):
        d.ellipse([S * x, S * .3, S * (x + .06), S * .44], fill=(40, 190, 180, 255))
    d.line([(S * .74, S * .22), (S * .86, S * .22), (S * .86, S * .5), (S * .62, S * .62)], fill=(170, 170, 180, 255), width=6)
    d.line([(S * .62, S * .62), (S * .3, S * .94)], fill=OUT, width=int(S * .12))
    d.line([(S * .62, S * .62), (S * .3, S * .94)], fill=(40, 40, 46, 255), width=int(S * .08))
    d.line([(S * .14, S * .16), (S * .6, S * .16)], fill=(150, 240, 230, 255), width=4)
    return _shrink(im, size)


def bside_tape(size=64, side_b=False):
    """A cassette tape: label with SIDE A (or SIDE B, flipped), the two reels, the window (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.rounded_rectangle([S * .04, S * .18, S * .96, S * .82], 8, fill=(40, 40, 46, 255) if not side_b else (220, 60, 80, 255), outline=OUT, width=6)
    d.rectangle([S * .12, S * .24, S * .88, S * .56], fill=(250, 245, 225, 255), outline=OUT, width=4)
    d.rectangle([S * .26, S * .42, S * .74, S * .54], fill=(30, 30, 36, 255))
    for x in (.34, .66):
        d.ellipse([S * (x - .05), S * .43, S * (x + .05), S * .53], fill=(250, 250, 250, 255))
    d.polygon([(S * .24, S * .82), (S * .3, S * .66), (S * .7, S * .66), (S * .76, S * .82)], fill=(90, 90, 100, 255), outline=OUT)
    im = _shrink(im, size)
    return _texted(im, [("SIDE B" if side_b else "SIDE A", (32, 17))], (200, 30, 40, 255) if side_b else (30, 30, 40, 255), (250, 245, 225, 255))


def giant_l(size=64):
    """A giant red letter L, chunky and shiny with a dark outline - the L they're about to take."""
    im, d, S = _big(size)
    OUT = (70, 0, 10, 255)
    pts = [(.22, .06), (.46, .06), (.46, .7), (.82, .7), (.82, .94), (.22, .94)]
    _outline_poly(d, [(S * x, S * y) for x, y in pts], (230, 30, 40, 255), OUT, 8)
    d.line([(S * .28, S * .12), (S * .28, S * .86)], fill=(255, 140, 140, 255), width=6)
    d.line([(S * .32, S * .76), (S * .76, S * .76)], fill=(255, 140, 140, 255), width=5)
    return _shrink(im, size)
