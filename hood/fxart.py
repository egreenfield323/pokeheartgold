"""Pixel art for Hood HeartGold's battle effects (particle textures), drawn in code.

Each function returns an RGBA PIL image; to_a3i5() packs one into a paletted A3I5 particle texture.
"""
from PIL import Image, ImageDraw


def to_a3i5(im, ncolors):
    """RGBA -> (texels, BGR555 palette) for an A3I5 texture with ncolors palette entries (index 0 unused)."""
    w, h = im.size
    rgb = Image.new("RGB", im.size, (0, 0, 0))
    rgb.paste(im, mask=im.split()[3])
    q = rgb.quantize(colors=ncolors - 1, method=Image.MEDIANCUT, dither=Image.NONE)
    pal = q.getpalette()[:3 * (ncolors - 1)]
    px, qa = im.load(), q.load()
    texels = bytearray()
    for y in range(h):
        for x in range(w):
            a = px[x, y][3]
            if a < 40:
                texels.append(0)
            else:
                texels.append(min(7, round(a / 255 * 7)) << 5 | (qa[x, y] + 1))
    bgr = [0] + [(pal[i + 2] >> 3) << 10 | (pal[i + 1] >> 3) << 5 | pal[i] >> 3 for i in range(0, len(pal), 3)]
    return bytes(texels), bgr + [0] * (ncolors - len(bgr))


def lowrider(size=64):
    """Side view of a candy-purple lowrider facing right, gold wire rims, a sleeve + gun out the window."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (20, 10, 30, 255)
    BODY, BODY_L, BODY_D = (150, 40, 190, 255), (210, 110, 240, 255), (90, 20, 120, 255)
    CHROME, CHROME_D = (235, 235, 245, 255), (150, 150, 165, 255)
    GOLD, GOLD_D = (255, 210, 60, 255), (190, 140, 20, 255)
    TINT, TINT_L = (25, 25, 45, 255), (70, 80, 120, 255)
    TIRE = (25, 25, 25, 255)
    y0 = 24                                                   # roof line
    # cabin
    d.polygon([(18, y0 + 9), (23, y0), (41, y0), (47, y0 + 9)], fill=BODY_D, outline=OUT)
    d.polygon([(21, y0 + 9), (25, y0 + 2), (31, y0 + 2), (31, y0 + 9)], fill=TINT)           # back window
    d.polygon([(33, y0 + 9), (33, y0 + 2), (40, y0 + 2), (44, y0 + 9)], fill=TINT)            # front window (down)
    d.line([(25, y0 + 3), (28, y0 + 3)], fill=TINT_L)
    # long low body
    d.rectangle([3, y0 + 9, 61, y0 + 18], fill=BODY, outline=OUT)
    d.line([(4, y0 + 10), (60, y0 + 10)], fill=BODY_L)                                         # shine
    d.line([(4, y0 + 17), (60, y0 + 17)], fill=BODY_D)
    d.line([(6, y0 + 13), (58, y0 + 13)], fill=GOLD)                                           # pinstripe
    d.line([(32, y0 + 10), (32, y0 + 17)], fill=BODY_D)                                        # door seam
    d.rectangle([60, y0 + 11, 62, y0 + 13], fill=(255, 245, 160, 255))                         # headlight
    d.rectangle([2, y0 + 11, 3, y0 + 13], fill=(230, 30, 30, 255))                             # taillight
    d.rectangle([1, y0 + 16, 63, y0 + 18], fill=CHROME, outline=OUT)                           # bumpers
    d.line([(2, y0 + 17), (62, y0 + 17)], fill=CHROME_D)
    # wire wheels, slammed low
    for cx in (14, 50):
        cy = y0 + 19
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=TIRE, outline=OUT)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=GOLD_D)
        for k in range(8):                                                                    # spokes
            import math
            a = k * math.pi / 4
            d.line([(cx, cy), (cx + round(4 * math.cos(a)), cy + round(4 * math.sin(a)))], fill=GOLD)
        d.point((cx, cy), fill=CHROME)
    # sleeve + hand + gun out of the front window, aimed up-forward
    SK, SLEEVE, GUN = (240, 190, 140, 255), (240, 240, 240, 255), (40, 40, 45, 255)
    d.line([(37, y0 + 7), (44, y0 - 1)], fill=SLEEVE, width=3)
    d.ellipse([43, y0 - 4, 47, y0], fill=SK, outline=OUT)
    d.line([(46, y0 - 3), (53, y0 - 8)], fill=GUN, width=2)                                    # barrel
    d.rectangle([44, y0 - 3, 46, y0 + 1], fill=GUN)                                            # grip
    # little gold chain on the rear-view mirror
    d.point((35, y0 + 3), fill=GOLD)
    d.point((35, y0 + 4), fill=GOLD)
    return im


def chain(size=64):
    """A gold Cuban-link chain hanging from the top, iced-out '$' medallion at the bottom-centre."""
    import math
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (60, 35, 5, 255)
    G, GL, GD = (250, 200, 40, 255), (255, 245, 170, 255), (175, 120, 15, 255)
    ICE_L = (255, 255, 255, 255)
    FACE, FACE_D = (255, 215, 70, 255), (215, 160, 25, 255)
    cx, my = size // 2, 34                                     # medallion centre
    # two strands running up from the bail to the top corners (worn around a neck we can't see)
    for side in (-1, 1):
        n = 9
        for k in range(n):
            t = k / (n - 1)
            x = cx + side * (3 + t * 15)
            y = my - 12 - t * 27
            w = 3 if k % 2 else 2
            d.ellipse([x - w, y - 2, x + w, y + 2], fill=G, outline=OUT)
            d.point((round(x) - side, round(y) - 1), fill=GL)
    d.rectangle([cx - 2, my - 14, cx + 2, my - 10], fill=GD, outline=OUT)        # bail
    # medallion: solid gold with a darker inner ring, diamonds round the rim, raised $
    R = 11
    d.ellipse([cx - R, my - R, cx + R, my + R], fill=G, outline=OUT)
    d.ellipse([cx - R + 2, my - R + 2, cx + R - 2, my + R - 2], fill=FACE_D)
    d.ellipse([cx - R + 3, my - R + 3, cx + R - 3, my + R - 3], fill=FACE)
    for k in range(10):                                                          # diamonds on the rim
        a = k * math.pi / 5
        d.point((cx + round((R - 1) * math.cos(a)), my + round((R - 1) * math.sin(a))), fill=ICE_L)
    # the $
    d.line([(cx, my - 8), (cx, my + 8)], fill=OUT, width=1)
    d.arc([cx - 5, my - 7, cx + 5, my + 1], 90, 360, fill=OUT, width=2)
    d.arc([cx - 5, my - 1, cx + 5, my + 7], 270, 540, fill=OUT, width=2)
    d.point((cx - 4, my - 4), fill=ICE_L)
    d.point((cx + 6, my + 5), fill=ICE_L)
    return im


def bill(size=16):
    """A tiny dollar bill (3 greens), lying flat across the texture."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    D, M, L = (20, 90, 30, 255), (70, 170, 70, 255), (170, 230, 150, 255)
    d.rectangle([1, 4, 14, 11], fill=M, outline=D)
    d.ellipse([5, 5, 10, 10], fill=L)
    d.line([(7, 6), (8, 6)], fill=D)                          # a tiny $
    d.line([(7, 7), (8, 8)], fill=D)
    d.line([(7, 9), (8, 9)], fill=D)
    d.point((3, 6), fill=L)
    d.point((12, 9), fill=L)
    return im


def cash_stack(size=64):
    """A fat stack of hundreds with a gold band, fanned a little - the 'make it rain' bankroll."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (15, 50, 20, 255)
    G, GL, GD = (80, 175, 80, 255), (175, 235, 160, 255), (40, 120, 50, 255)
    BAND, BAND_D = (250, 205, 50, 255), (180, 130, 20, 255)
    for k in range(6, -1, -1):                                 # bills stacked, slightly fanned
        y = 22 + k * 3
        dx = (k - 3) * 1
        d.rectangle([10 + dx, y, 53 + dx, y + 14], fill=G if k else GL, outline=OUT)
        d.line([(12 + dx, y + 13), (51 + dx, y + 13)], fill=GD)
    top = 22
    d.ellipse([24, top + 2, 39, top + 12], fill=GL, outline=GD)            # portrait oval
    d.line([(31, top + 4), (31, top + 10)], fill=OUT)                        # $
    d.arc([28, top + 4, 34, top + 8], 90, 360, fill=OUT)
    d.arc([28, top + 6, 34, top + 10], 270, 540, fill=OUT)
    d.rectangle([13, top + 3, 16, top + 6], fill=GD)                         # 100s in the corners
    d.rectangle([47, top + 8, 50, top + 11], fill=GD)
    d.rectangle([40, top - 1, 45, top + 34], fill=BAND, outline=BAND_D)      # money band
    d.line([(42, top), (42, top + 33)], fill=(255, 245, 170, 255))
    return im



def rocket(size=32, angle=-26.6):
    """An RPG rocket in flight, nose pointing along `angle` degrees (screen space, default player -> enemy),
    with its exhaust flame behind it."""
    big = 4                                                    # draw large, rotate, shrink: clean edges
    S = size * big
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cy = S // 2
    OLIVE, OLIVE_L, OLIVE_D = (95, 110, 50, 255), (150, 165, 85, 255), (55, 65, 30, 255)
    OUT = (25, 25, 15, 255)
    d.polygon([(S * .18, cy - 9), (S * .02, cy), (S * .18, cy + 9)], fill=(255, 140, 20, 255))    # flame
    d.polygon([(S * .2, cy - 5), (S * .09, cy), (S * .2, cy + 5)], fill=(255, 240, 120, 255))
    d.polygon([(S * .2, cy - 6), (S * .3, cy - 6), (S * .24, cy - 15)], fill=OLIVE_D, outline=OUT)  # fins
    d.polygon([(S * .2, cy + 6), (S * .3, cy + 6), (S * .24, cy + 15)], fill=OLIVE_D, outline=OUT)
    d.rectangle([S * .2, cy - 6, S * .62, cy + 6], fill=OLIVE, outline=OUT)                       # body
    d.line([(S * .21, cy - 4), (S * .61, cy - 4)], fill=OLIVE_L, width=3)
    d.ellipse([S * .55, cy - 11, S * .82, cy + 11], fill=OLIVE, outline=OUT)                      # warhead
    d.polygon([(S * .8, cy - 7), (S * .96, cy), (S * .8, cy + 7)], fill=OLIVE_D, outline=OUT)
    d.line([(S * .6, cy - 7), (S * .75, cy - 7)], fill=OLIVE_L, width=3)
    d.rectangle([S * .4, cy - 6, S * .43, cy + 6], fill=(200, 40, 30, 255))                       # red band
    im = im.rotate(-angle, resample=Image.BICUBIC)
    return im.resize((size, size), Image.LANCZOS)



def molotov(size=32):
    """A brown liquor bottle with a burning rag stuffed in the neck."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (30, 15, 5, 255)
    G, GL, GD = (140, 75, 25, 255), (205, 140, 70, 255), (90, 45, 15, 255)
    d.rounded_rectangle([11, 14, 21, 29], 3, fill=G, outline=OUT)            # body
    d.rectangle([14, 8, 18, 14], fill=G, outline=OUT)                         # neck
    d.line([(13, 16), (13, 26)], fill=GL)                                     # glint
    d.rectangle([12, 19, 20, 24], fill=(235, 225, 190, 255), outline=GD)      # label
    d.line([(14, 21), (18, 21)], fill=(180, 40, 30, 255))
    d.rectangle([15, 5, 17, 8], fill=(225, 215, 200, 255), outline=OUT)       # rag
    d.polygon([(13, 5), (16, 0), (19, 5), (16, 7)], fill=(255, 140, 20, 255))  # flame
    d.polygon([(15, 5), (16, 2), (17, 5)], fill=(255, 240, 120, 255))
    return im


def brick(size=32):
    """A red house brick with mortar crumbs."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (50, 15, 10, 255)
    R, RL, RD = (180, 60, 40, 255), (220, 110, 80, 255), (120, 35, 25, 255)
    d.rectangle([5, 10, 26, 21], fill=R, outline=OUT)
    d.line([(6, 11), (25, 11)], fill=RL)
    d.line([(6, 20), (25, 20)], fill=RD)
    for x, y in ((9, 14), (16, 17), (21, 13), (12, 18)):                     # pits
        d.point((x, y), fill=RD)
    d.point((7, 9), fill=(200, 200, 190, 255))                              # mortar crumbs
    d.point((24, 22), fill=(200, 200, 190, 255))
    return im


def egg(size=32):
    """A plain white egg."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([10, 7, 22, 25], fill=(245, 240, 225, 255), outline=(90, 80, 60, 255))
    d.ellipse([12, 10, 15, 15], fill=(255, 255, 255, 255))
    d.arc([10, 7, 22, 25], 20, 120, fill=(200, 190, 165, 255))
    return im
