

# ---- set 24, batch 4: Petty, Bad Trip, Wildin Out, Bite Style, Bounced Out ------------------------------------------

def grey_hoodie(size=64):
    """A grey pullover hoodie, hood up, drawstrings, the front pocket."""
    im, d, S = _big(size)
    OUT = (40, 40, 46, 255)
    G = (150, 150, 158, 255)
    _outline_poly(d, [(S * .3, S * .2), (S * .7, S * .2), (S * .96, S * .5), (S * .84, S * .6), (S * .76, S * .5), (S * .76, S * .94),
                      (S * .24, S * .94), (S * .24, S * .5), (S * .16, S * .6), (S * .04, S * .5)], G, OUT, 7)
    d.ellipse([S * .32, S * .04, S * .68, S * .36], fill=(130, 130, 138, 255), outline=OUT, width=6)                # hood
    d.ellipse([S * .4, S * .12, S * .6, S * .3], fill=(60, 60, 66, 255))
    for x in (.44, .56):
        d.line([(S * x, S * .34), (S * x, S * .52)], fill=(240, 240, 240, 255), width=4)                            # strings
    d.rounded_rectangle([S * .34, S * .66, S * .66, S * .84], 6, outline=OUT, width=4)                               # pocket
    return _shrink(im, size)


def cuban_link(size=32):
    """A thick gold Cuban-link chain, a loop."""
    im, d, S = _big(size)
    OUT = (110, 70, 0, 255)
    import math
    for k in range(14):
        a = k * 2 * math.pi / 14
        cx, cy = S * (.5 + .36 * math.cos(a)), S * (.46 + .3 * math.sin(a))
        d.ellipse([cx - S * .1, cy - S * .07, cx + S * .1, cy + S * .07], fill=(250, 200, 50, 255), outline=OUT, width=4)
    return _shrink(im, size)


def cheap_lighter(size=32):
    """A neon green 99-cent lighter."""
    im, d, S = _big(size)
    OUT = (10, 40, 10, 255)
    d.rounded_rectangle([S * .34, S * .3, S * .66, S * .94], 6, fill=(90, 230, 70, 255), outline=OUT, width=5)
    d.rectangle([S * .36, S * .14, S * .64, S * .3], fill=(190, 195, 205, 255), outline=OUT, width=4)
    d.ellipse([S * .46, S * .16, S * .58, S * .28], fill=(90, 90, 96, 255))
    d.line([(S * .42, S * .4), (S * .42, S * .84)], fill=(200, 255, 190, 255), width=4)
    return _shrink(im, size)


def dream_cloud(size=64, what="cash"):
    """A dream thought-bubble (with the little trailing bubbles at the bottom-left) holding a picture: cash (a stack
    of bills), bills (a pile of envelopes stamped red) or rent (a front door with a RENT DUE notice, shown at 1:1)."""
    import math
    im, d, S = _big(size)
    OUT = (60, 50, 90, 255)
    for k in range(9):
        a = k * 2 * math.pi / 9
        cx, cy = S * (.54 + .3 * math.cos(a)), S * (.42 + .24 * math.sin(a))
        d.ellipse([cx - S * .16, cy - S * .16, cx + S * .16, cy + S * .16], fill=(245, 240, 255, 255), outline=OUT, width=6)
    d.ellipse([S * .26, S * .16, S * .82, S * .68], fill=(245, 240, 255, 255))
    for x, y, r in ((.14, .82, .06), (.06, .94, .04)):
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], fill=(245, 240, 255, 255), outline=OUT, width=4)
    if what == "cash":
        for k in range(4):
            d.rectangle([S * .38, S * (.5 - k * .06), S * .72, S * (.56 - k * .06)], fill=(90, 190, 90, 255), outline=(20, 80, 20, 255), width=3)
        d.ellipse([S * .5, S * .26, S * .6, S * .34], fill=(250, 200, 40, 255), outline=(120, 80, 0, 255), width=3)
    elif what == "bills":
        for k, (x, y) in enumerate(((.36, .48), (.5, .42), (.42, .32), (.56, .28))):
            d.rectangle([S * x, S * y, S * (x + .2), S * (y + .13)], fill=(250, 250, 245, 255), outline=(80, 70, 60, 255), width=3)
            d.rectangle([S * (x + .12), S * (y + .02), S * (x + .18), S * (y + .06)], fill=(220, 40, 40, 255))
    else:
        d.rectangle([S * .42, S * .2, S * .66, S * .62], fill=(150, 90, 50, 255), outline=(60, 30, 10, 255), width=4)   # door
        d.ellipse([S * .6, S * .4, S * .64, S * .44], fill=(240, 190, 50, 255))
        d.rectangle([S * .3, S * .3, S * .78, S * .5], fill=(255, 250, 240, 255), outline=(200, 30, 30, 255), width=4)  # notice
    im = _shrink(im, size)
    if what == "rent":
        _texted(im, [("RENT", (34, 20)), ("DUE", (34, 27))], (220, 30, 30, 255), (255, 250, 240, 255))
    return im


def prize_wheel(size=64, turn=0):
    """A game-show prize wheel: coloured wedges, one black wedge with a white ?, gold rim pegs; turn = how far it's
    rotated (degrees), so a few frames make it spin. The red pointer at the top doesn't turn."""
    import math
    im, d, S = _big(size)
    OUT = (20, 15, 10, 255)
    cols = [(230, 40, 40), (250, 200, 40), (40, 120, 230), (60, 190, 80), (230, 120, 30), (160, 60, 200), (30, 30, 34), (250, 250, 250)]
    wheel = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    w = ImageDraw.Draw(wheel)
    for k, c in enumerate(cols):
        w.pieslice([S * .08, S * .12, S * .92, S * .96], k * 45, (k + 1) * 45, fill=c + (255,), outline=OUT, width=4)
    q = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    _big_text(q, "?", (int(S * .7), int(S * .66)), (255, 255, 255, 255), scale=6)
    wheel.alpha_composite(q)
    wheel = wheel.rotate(turn, center=(S * .5, S * .54), resample=Image.BICUBIC)
    im.alpha_composite(wheel)
    d.ellipse([S * .08, S * .12, S * .92, S * .96], outline=(220, 170, 40, 255), width=int(S * .05))
    for k in range(16):
        a = k * math.pi / 8
        x, y = S * (.5 + .42 * math.cos(a)), S * (.54 + .42 * math.sin(a))
        d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(255, 240, 160, 255))
    d.ellipse([S * .44, S * .48, S * .56, S * .6], fill=(220, 170, 40, 255), outline=OUT, width=4)
    d.polygon([(S * .42, S * .02), (S * .58, S * .02), (S * .5, S * .2)], fill=(220, 30, 30, 255), outline=OUT)      # pointer
    return _shrink(im, size)


def club_rope(size=64):
    """A nightclub velvet rope between two brass stanchions."""
    im, d, S = _big(size)
    OUT = (60, 40, 0, 255)
    for x in (.12, .82):
        d.rectangle([S * x, S * .3, S * (x + .06), S * .9], fill=(230, 180, 50, 255), outline=OUT, width=5)
        d.ellipse([S * (x - .02), S * .22, S * (x + .08), S * .32], fill=(250, 210, 80, 255), outline=OUT, width=4)
        d.ellipse([S * (x - .06), S * .86, S * (x + .12), S * .96], fill=(230, 180, 50, 255), outline=OUT, width=4)
    d.arc([S * .15, S * .1, S * .85, S * .6], 20, 160, fill=(120, 0, 20, 255), width=int(S * .09))
    d.arc([S * .15, S * .1, S * .85, S * .6], 20, 160, fill=(200, 20, 50, 255), width=int(S * .06))
    return _shrink(im, size)


def list_clipboard(size=64):
    """The bouncer's clipboard: THE LIST at the top, names, and lots crossed out (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (20, 15, 10, 255)
    d.rounded_rectangle([S * .16, S * .06, S * .84, S * .96], 8, fill=(40, 40, 46, 255), outline=OUT, width=6)
    d.rectangle([S * .22, S * .14, S * .78, S * .9], fill=(250, 250, 245, 255))
    d.rounded_rectangle([S * .38, S * .02, S * .62, S * .12], 4, fill=(190, 190, 200, 255), outline=OUT, width=4)
    for k in range(5):
        y = .44 + k * .09
        d.line([(S * .28, S * y), (S * .72, S * y)], fill=(80, 80, 90, 255), width=4)
        if k % 2 == 0:
            d.line([(S * .26, S * (y - .02)), (S * .74, S * (y + .01))], fill=(220, 30, 30, 255), width=4)
    im = _shrink(im, size)
    return _texted(im, [("THE", (32, 11)), ("LIST", (32, 18))], (20, 20, 25, 255), (250, 250, 245, 255))
