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


def house(size=64):
    """A little suburban house - somebody's about to get their house egged."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (35, 25, 25, 255)
    WALL, WALL_D = (236, 226, 200, 255), (196, 182, 150, 255)
    ROOF, ROOF_L, ROOF_D = (176, 52, 44, 255), (214, 92, 70, 255), (120, 30, 28, 255)
    d.rectangle([40, 8, 46, 22], fill=(150, 80, 60, 255), outline=OUT)                    # chimney
    d.polygon([(4, 30), (32, 8), (60, 30)], fill=ROOF, outline=OUT)                         # roof
    d.line([(10, 28), (32, 11)], fill=ROOF_L)
    d.line([(6, 30), (58, 30)], fill=ROOF_D)
    d.rectangle([9, 30, 55, 58], fill=WALL, outline=OUT)                                   # walls
    d.line([(10, 57), (54, 57)], fill=WALL_D)
    for y in range(34, 57, 4):                                                              # siding
        d.line([(10, y), (54, y)], fill=WALL_D)
    d.rectangle([27, 41, 37, 58], fill=(110, 70, 40, 255), outline=OUT)                    # door
    d.point((35, 50), fill=(250, 210, 70, 255))                                             # knob
    for x0 in (13, 42):                                                                     # windows, lights on
        d.rectangle([x0, 37, x0 + 9, 46], fill=(255, 236, 140, 255), outline=OUT)
        d.line([(x0 + 4, 37), (x0 + 4, 46)], fill=OUT)
        d.line([(x0, 41), (x0 + 9, 41)], fill=OUT)
    d.rectangle([4, 58, 60, 60], fill=(90, 150, 70, 255))                                  # lawn
    return im


def hydrant(size=32):
    """A red fire hydrant with its cap knocked off."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (50, 10, 10, 255)
    R, RL, RD = (210, 40, 40, 255), (245, 110, 100, 255), (140, 20, 20, 255)
    d.rectangle([11, 10, 21, 29], fill=R, outline=OUT)                         # barrel
    d.ellipse([10, 5, 22, 13], fill=R, outline=OUT)                            # dome
    d.rectangle([14, 3, 18, 6], fill=RD, outline=OUT)                          # top nut
    for x0 in (5, 21):                                                          # both side caps knocked off
        d.rectangle([x0, 15, x0 + 5, 20], fill=(200, 200, 210, 255), outline=OUT)
        d.ellipse([x0 + 1, 16, x0 + 4, 19], fill=(30, 30, 40, 255))
    d.rectangle([9, 27, 23, 30], fill=RD, outline=OUT)                         # base
    d.line([(13, 11), (13, 27)], fill=RL)
    d.line([(19, 12), (19, 27)], fill=RD)
    return im


def bat(size=32):
    """A wooden baseball bat, handle at the bottom-left, barrel up-right."""
    big = 4
    S = size * big
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (50, 30, 10, 255)
    W, WL = (200, 150, 85, 255), (240, 200, 140, 255)
    d.line([(S * .18, S * .82), (S * .5, S * .5)], fill=OUT, width=14)       # handle
    d.line([(S * .18, S * .82), (S * .5, S * .5)], fill=W, width=8)
    d.line([(S * .45, S * .55), (S * .82, S * .18)], fill=OUT, width=28)     # barrel
    d.line([(S * .45, S * .55), (S * .82, S * .18)], fill=W, width=20)
    d.line([(S * .5, S * .46), (S * .78, S * .18)], fill=WL, width=6)
    d.ellipse([S * .12, S * .78, S * .24, S * .9], fill=OUT)                    # knob
    d.rectangle([S * .22, S * .7, S * .3, S * .78], fill=(40, 40, 40, 255))    # tape
    return im.resize((size, size), Image.LANCZOS)


def bat_swing(size=64):
    """A baseball bat with its HANDLE AT THE CENTRE of the texture, barrel pointing right: rotating the particle
    swings it from the hands like a real swing."""
    big = 4
    S = size * big
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = S // 2
    OUT = (50, 30, 10, 255)
    W, WL = (205, 155, 90, 255), (245, 210, 150, 255)
    d.line([(c - 10, c), (c + 40, c)], fill=OUT, width=14)                    # handle (from the hands)
    d.line([(c - 10, c), (c + 40, c)], fill=W, width=8)
    d.rectangle([c - 6, c - 6, c + 6, c + 6], fill=(40, 40, 40, 255))         # grip tape
    d.ellipse([c - 16, c - 9, c - 4, c + 9], fill=OUT)                        # knob
    d.line([(c + 36, c), (c + 120, c)], fill=OUT, width=30)                   # barrel
    d.line([(c + 36, c), (c + 120, c)], fill=W, width=22)
    d.line([(c + 40, c - 6), (c + 118, c - 6)], fill=WL, width=6)
    d.ellipse([c + 108, c - 15, c + 126, c + 15], fill=W, outline=OUT, width=4)
    return im.resize((size, size), Image.LANCZOS)


def taser(size=32):
    """A yellow-and-black taser, pointing right, with the cartridge glowing."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (20, 20, 20, 255)
    Y, YD = (250, 220, 40, 255), (190, 150, 10, 255)
    d.rectangle([6, 11, 24, 18], fill=Y, outline=OUT)                         # body
    d.polygon([(8, 18), (14, 18), (12, 27), (6, 27)], fill=(40, 40, 40, 255), outline=OUT)   # grip
    d.rectangle([24, 10, 29, 19], fill=(40, 40, 40, 255), outline=OUT)        # cartridge
    d.point((29, 12), fill=(140, 220, 255, 255)); d.point((29, 17), fill=(140, 220, 255, 255))
    d.line([(8, 13), (22, 13)], fill=(255, 245, 160, 255))
    d.line([(8, 17), (22, 17)], fill=YD)
    d.rectangle([12, 18, 13, 21], fill=OUT)                                   # trigger
    return im


def bolt(size=32):
    """A jagged white-yellow lightning bolt (spawned at random angles it reads as crackling electricity)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(3, 15), (10, 10), (13, 17), (20, 9), (23, 16), (29, 12)]
    d.line(pts, fill=(255, 220, 60, 255), width=4)
    d.line(pts, fill=(255, 255, 230, 255), width=2)
    d.line([(13, 17), (15, 25)], fill=(255, 230, 90, 255), width=2)           # a fork
    return im


def keyfob(size=32):
    """A car key fob with a big red panic button."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (15, 15, 20, 255)
    d.rounded_rectangle([9, 8, 23, 27], 4, fill=(45, 45, 55, 255), outline=OUT)
    d.ellipse([12, 11, 20, 19], fill=(230, 30, 30, 255), outline=OUT)         # panic button
    d.point((14, 13), fill=(255, 170, 170, 255))
    d.rectangle([13, 21, 19, 24], fill=(90, 90, 110, 255))
    d.ellipse([13, 2, 19, 8], outline=(200, 200, 210, 255), width=2)          # key ring
    return im


def speaker(size=64):
    """A giant subwoofer box: wood cabinet, big black cone, chrome ring."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (15, 10, 10, 255)
    d.rectangle([6, 6, 57, 60], fill=(40, 40, 45, 255), outline=OUT)          # cabinet
    d.rectangle([8, 8, 55, 11], fill=(70, 70, 80, 255))
    d.ellipse([12, 14, 51, 53], fill=(190, 190, 200, 255), outline=OUT)       # chrome surround
    d.ellipse([15, 17, 48, 50], fill=(25, 25, 30, 255))                       # cone
    d.ellipse([22, 24, 41, 43], fill=(45, 45, 52, 255))
    d.ellipse([27, 29, 36, 38], fill=(70, 70, 80, 255), outline=OUT)          # dust cap
    d.arc([15, 17, 48, 50], 200, 260, fill=(90, 90, 100, 255), width=2)
    for x, y in ((9, 57), (54, 57), (9, 9), (54, 9)):                         # bolts
        d.point((x, y), fill=(200, 200, 210, 255))
    return im


def ground_crack(size=64):
    """Dark cracks splitting the ground (lies flat under the target)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    D, L = (45, 30, 20, 255), (120, 95, 60, 255)
    main = [(2, 34), (14, 30), (22, 36), (32, 29), (42, 35), (52, 30), (62, 33)]
    d.line(main, fill=L, width=5)
    d.line(main, fill=D, width=3)
    for a, b in (((22, 36), (18, 46)), ((32, 29), (36, 20)), ((42, 35), (47, 45)), ((14, 30), (10, 22))):
        d.line([a, b], fill=D, width=2)
    return im


def ring_quarter(n=32):
    """Quarter of a sound-wave ring (the hardware mirrors it into the full ring); returns A5I3 alpha only."""
    import math
    out = bytearray()
    c = n - .5
    for y in range(n):
        for x in range(n):
            r = math.hypot(c - x, c - y) / n
            a = max(0.0, 1 - abs(r - .82) / .09)
            a = max(a, max(0.0, 1 - abs(r - .55) / .06) * .6)
            out.append(round(min(1, a) * 31) << 3)
    return bytes(out)


# ------------------------------------------------------------------ set 3: Hot Shot, Stare Down, Talk Trash,
#                                                                     Pocket Sand, Fan Blast

def _alpha(w, h, f):
    """A5I3 alpha-only texture (w x h) from f(x, y) -> 0..1 (the particle colour tints it)."""
    out = bytearray()
    for y in range(h):
        for x in range(w):
            out.append(round(max(0.0, min(1.0, f(x, y))) * 31) << 3)
    return bytes(out)


def flame_tongue(w=16, h=32):
    """A single licking flame, wide at the bottom, flickering to a point (alpha only)."""
    import math

    def f(x, y):
        t = y / (h - 1)                                    # 0 top .. 1 bottom
        half = (w / 2 - 1) * (t ** .7)
        cx = (w - 1) / 2 + math.sin(t * 7) * (1 - t) * 2.2
        e = 1 - abs(x - cx) / max(.6, half)
        return e * 1.6 if t > .05 else 0
    return _alpha(w, h, f)


def speck(n=16):
    """A tiny hard grain (ember / sand), alpha only."""
    c = (n - 1) / 2
    return _alpha(n, n, lambda x, y: 1.0 if (x - c) ** 2 + (y - c) ** 2 <= 4.5 else 0)


def speech_bubble(size=32):
    """A white speech bubble full of cussing: #@$%!"""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (15, 15, 20, 255)
    d.rounded_rectangle([1, 5, 30, 22], 6, fill=(255, 255, 255, 255), outline=OUT, width=2)
    d.polygon([(7, 21), (4, 29), (13, 21)], fill=(255, 255, 255, 255), outline=OUT)               # tail
    d.line([(8, 21), (12, 21)], fill=(255, 255, 255, 255), width=2)
    R = (220, 20, 30, 255)
    glyphs = {"#": ["0101", "1111", "0101", "1111", "0101"], "$": ["0110", "1100", "0110", "0011", "0110"],
              "%": ["1001", "0010", "0100", "1001", "0000"], "!": ["0100", "0100", "0100", "0000", "0100"],
              "@": ["0110", "1001", "1011", "1000", "0111"]}
    for k, ch in enumerate("#@$%!"):
        for yy, row in enumerate(glyphs[ch]):
            for xx, bit in enumerate(row):
                if bit == "1":
                    d.point((4 + k * 5 + xx, 11 + yy), fill=R)
    return im


def bang(n=16):
    """A big '!' (alpha only, tinted red)."""
    c = (n - 1) / 2

    def f(x, y):
        if abs(x - c) <= 1.6 and 1 <= y <= 9:
            return 1
        return 1 if (x - c) ** 2 + (y - 12.5) ** 2 <= 3 else 0
    return _alpha(n, n, f)


def dust_cloud(w=16, h=32):
    """A lumpy dust cloud (alpha only): three overlapping puffs."""
    blobs = [(5, 22, 5), (10, 18, 5.5), (8, 12, 4.5)]
    return _alpha(w, h, lambda x, y: max(1.3 - ((x - bx) ** 2 + (y - by) ** 2) ** .5 / r for bx, by, r in blobs))


def box_fan(size=64):
    """A cheap white box fan: square frame, round dark grill (the blades spin separately), feet."""
    import math
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (20, 25, 35, 255)
    d.rounded_rectangle([4, 4, 59, 55], 6, fill=(235, 238, 242, 255), outline=OUT, width=2)        # frame
    d.ellipse([9, 7, 54, 52], fill=(40, 50, 65, 255), outline=OUT, width=2)                        # opening
    for r in (21, 15, 9):
        d.ellipse([31.5 - r, 29.5 - r, 31.5 + r, 29.5 + r], outline=(150, 160, 175, 255))           # grill rings
    for a in range(0, 360, 30):
        x, y = 31.5 + 22 * math.cos(math.radians(a)), 29.5 + 22 * math.sin(math.radians(a))
        d.line([(31.5, 29.5), (x, y)], fill=(120, 130, 145, 255))
    d.rectangle([44, 48, 56, 53], fill=(200, 205, 215, 255), outline=OUT)                          # knob panel
    d.ellipse([47, 48, 52, 53], fill=(60, 140, 230, 255))
    d.rectangle([10, 56, 20, 61], fill=(90, 95, 105, 255), outline=OUT)                            # feet
    d.rectangle([43, 56, 53, 61], fill=(90, 95, 105, 255), outline=OUT)
    return im


def fan_blades(n=16):
    """Three swept fan blades around a hub (alpha only; tinted, scaled up and spun by the emitter)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        r = math.hypot(x - c, y - c)
        if r < 1.8:
            return 1
        if r > c + .3:
            return 0
        a = math.atan2(y - c, x - c)
        for k in range(3):
            if (a - k * 2 * math.pi / 3 - r * .12) % (2 * math.pi) < .8:
                return .95
        return 0
    return _alpha(n, n, f)


def wind_streak(n=16, angle=-26.6):
    """A thin gust line along the attack line, fading at both ends (alpha only)."""
    import math
    a = math.radians(angle)
    c = (n - 1) / 2

    def f(x, y):
        u = (x - c) * math.cos(a) + (y - c) * math.sin(a)
        v = -(x - c) * math.sin(a) + (y - c) * math.cos(a)
        return (1 - abs(u) / 7.5) * 1.4 if abs(v) <= .8 and abs(u) <= 7.5 else 0
    return _alpha(n, n, f)


# ------------------------------------------------------------------ set 3, take 2: big readable props

# Text signs show at exactly 2 screen px per texel: a 64px texture at particle scale 1.0 is ~0.745 px per texel
# in battle (measured in game), and any uneven ratio doubles some pixel rows and not others - lumpy letters.
# The pop grows to 1.0 and stays there (the out-phase never starts), so the held size is exactly 2:1.
SIGN_SCALE = 2 / .745
SIGN_POP = (.2, 1.0, 1.0, 35, 255)

# A hand-drawn 5x7 pixel font for every sign. (PIL's load_default() is a vector font now: forced to hard
# pixels its curves come out ragged, and that's what made the signs look chewed up.)
GLYPHS = {
    "A": ".###.|#...#|#...#|#####|#...#|#...#|#...#", "B": "####.|#...#|#...#|####.|#...#|#...#|####.",
    "C": ".###.|#...#|#....|#....|#....|#...#|.###.", "D": "####.|#...#|#...#|#...#|#...#|#...#|####.",
    "E": "#####|#....|#....|####.|#....|#....|#####", "F": "#####|#....|#....|####.|#....|#....|#....",
    "G": ".###.|#...#|#....|#.###|#...#|#...#|.####", "H": "#...#|#...#|#...#|#####|#...#|#...#|#...#",
    "I": "###|.#.|.#.|.#.|.#.|.#.|###", "J": "..###|...#.|...#.|...#.|#..#.|#..#.|.##..",
    "K": "#...#|#..#.|#.#..|##...|#.#..|#..#.|#...#", "L": "#....|#....|#....|#....|#....|#....|#####",
    "M": "#...#|##.##|#.#.#|#.#.#|#...#|#...#|#...#", "N": "#...#|##..#|##..#|#.#.#|#..##|#..##|#...#",
    "O": ".###.|#...#|#...#|#...#|#...#|#...#|.###.", "P": "####.|#...#|#...#|####.|#....|#....|#....",
    "Q": ".###.|#...#|#...#|#...#|#.#.#|#..#.|.##.#", "R": "####.|#...#|#...#|####.|#.#..|#..#.|#...#",
    "S": ".####|#....|#....|.###.|....#|....#|####.", "T": "#####|..#..|..#..|..#..|..#..|..#..|..#..",
    "U": "#...#|#...#|#...#|#...#|#...#|#...#|.###.", "V": "#...#|#...#|#...#|#...#|#...#|.#.#.|..#..",
    "W": "#...#|#...#|#...#|#.#.#|#.#.#|##.##|#...#", "X": "#...#|#...#|.#.#.|..#..|.#.#.|#...#|#...#",
    "Y": "#...#|#...#|.#.#.|..#..|..#..|..#..|..#..", "Z": "#####|....#|...#.|..#..|.#...|#....|#####",
    "0": ".###.|#...#|#..##|#.#.#|##..#|#...#|.###.", "1": "..#..|.##..|..#..|..#..|..#..|..#..|.###.",
    "2": ".###.|#...#|....#|...#.|..#..|.#...|#####", "3": "####.|....#|....#|.###.|....#|....#|####.",
    "4": "...#.|..##.|.#.#.|#..#.|#####|...#.|...#.", "5": "#####|#....|####.|....#|....#|#...#|.###.",
    "6": ".###.|#....|#....|####.|#...#|#...#|.###.", "7": "#####|....#|...#.|..#..|.#...|.#...|.#...",
    "8": ".###.|#...#|#...#|.###.|#...#|#...#|.###.", "9": ".###.|#...#|#...#|.####|....#|....#|.###.",
    "!": "#|#|#|#|#|.|#", "?": ".###.|#...#|....#|...#.|..#..|.....|..#..", "'": "#|#|.|.|.|.|.",
    ".": ".|.|.|.|.|.|#", ",": ".|.|.|.|.|#|#", ":": ".|#|.|.|.|#|.", "-": "...|...|...|###|...|...|...",
    "+": ".....|..#..|..#..|#####|..#..|..#..|.....", "/": "....#|...#.|...#.|..#..|.#...|.#...|#....",
    "$": "..#..|.####|#.#..|.###.|..#.#|####.|..#..", " ": "...|...|...|...|...|...|...",
}
GLYPHS["’"] = GLYPHS["'"]

# the sign font: 4x6 (M, W, V, T 5 wide), a size smaller - signs show at 2:1 and still read at this size
SMALL = {
    "A": ".##.|#..#|#..#|####|#..#|#..#", "B": "###.|#..#|###.|#..#|#..#|###.", "C": ".###|#...|#...|#...|#...|.###",
    "D": "###.|#..#|#..#|#..#|#..#|###.", "E": "####|#...|###.|#...|#...|####", "F": "####|#...|###.|#...|#...|#...",
    "G": ".###|#...|#...|#.##|#..#|.###", "H": "#..#|#..#|####|#..#|#..#|#..#", "I": "###|.#.|.#.|.#.|.#.|###",
    "J": "..##|...#|...#|...#|#..#|.##.", "K": "#..#|#.#.|##..|##..|#.#.|#..#", "L": "#...|#...|#...|#...|#...|####",
    "M": "#...#|##.##|#.#.#|#...#|#...#|#...#", "N": "#..#|##.#|##.#|#.##|#.##|#..#", "O": ".##.|#..#|#..#|#..#|#..#|.##.",
    "P": "###.|#..#|#..#|###.|#...|#...", "Q": ".##.|#..#|#..#|#..#|#.#.|.#.#", "R": "###.|#..#|#..#|###.|#.#.|#..#",
    "S": ".###|#...|.##.|...#|...#|###.", "T": "#####|..#..|..#..|..#..|..#..|..#..", "U": "#..#|#..#|#..#|#..#|#..#|.##.",
    "V": "#...#|#...#|#...#|.#.#.|.#.#.|..#..", "W": "#...#|#...#|#...#|#.#.#|##.##|#...#", "X": "#..#|#..#|.##.|.##.|#..#|#..#",
    "Y": "#...#|#...#|.#.#.|..#..|..#..|..#..", "Z": "####|...#|..#.|.#..|#...|####",
    "0": ".##.|#..#|#.##|##.#|#..#|.##.", "1": ".#.|##.|.#.|.#.|.#.|###", "2": ".##.|#..#|..#.|.#..|#...|####",
    "3": "###.|...#|.##.|...#|...#|###.", "4": "#..#|#..#|####|...#|...#|...#", "5": "####|#...|###.|...#|...#|###.",
    "6": ".##.|#...|###.|#..#|#..#|.##.", "7": "####|...#|..#.|.#..|.#..|.#..", "8": ".##.|#..#|.##.|#..#|#..#|.##.",
    "9": ".##.|#..#|#..#|.###|...#|.##.", "!": "#|#|#|#|.|#", "?": ".##.|#..#|..#.|.#..|....|.#..",
    "'": "#|#|.|.|.|.", ".": ".|.|.|.|.|#", ",": ".|.|.|.|#|#", ":": ".|#|.|.|#|.", "-": "...|...|###|...|...|...",
    "+": "...|.#.|###|.#.|...|...", "/": "...#|..#.|..#.|.#..|.#..|#...", "$": ".###|#.#.|.##.|..##|..##|###.",
    " ": "..|..|..|..|..|..",
}
SMALL["’"] = SMALL["'"]
SMALL.update({                                                # a few lowercase letters (logos): x-height 4, p descends
    "s": "....|.###|#...|.##.|...#|###.", "p": "....|###.|#..#|#..#|###.|#...", "i": "#|.|#|#|#|#",
    "r": "...|#.#|##.|#..|#..|#..", "t": ".#..|####|.#..|.#..|.#..|..##",
})


def _text_mask(text, font=SMALL):
    """The text as a 1-bit L image (255 = ink), glyphs 1 texel apart."""
    rows = [font[c if c in font else c.upper()].split("|") for c in text]
    w = sum(len(g[0]) for g in rows) + max(0, len(rows) - 1)
    m = Image.new("L", (max(w, 1), len(rows[0]) if rows else 1), 0)
    x = 0
    for g in rows:
        for y, row in enumerate(g):
            for dx, c in enumerate(row):
                if c == "#":
                    m.putpixel((x + dx, y), 255)
        x += len(g[0]) + 1
    return m


def _outlined_text(d, xy, text, fill, outline=(15, 10, 10, 255), font=None):
    """Pixel text (GLYPHS) with a 1px outline all round (readable on anything); xy = top-left of the ink."""
    im = d._image
    m = _text_mask(text)
    x, y = round(xy[0]), round(xy[1])
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx or dy:
                im.paste(outline, (x + dx, y + dy), m)
    im.paste(fill, (x, y), m)


def _text_w(d, text):
    return _text_mask(text).width


def chip_bag(size=64):
    """A big red foil bag of HOT CHIPS, torn open at the top, fire logo, chips peeking out."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (25, 5, 5, 255)
    body = [(12, 12), (52, 12), (55, 56), (9, 56)]
    d.polygon(body, fill=(205, 25, 25, 255), outline=OUT)
    for x in range(9, 56, 4):                                        # crimped bottom
        d.polygon([(x, 56), (x + 2, 60), (x + 4, 56)], fill=(160, 15, 15, 255), outline=OUT)
    d.polygon([(12, 12), (16, 6), (22, 11), (28, 5), (34, 11), (40, 5), (46, 10), (52, 12)],
              fill=(150, 15, 15, 255), outline=OUT)                  # torn top
    for x, y in ((20, 8), (27, 4), (34, 7), (42, 5)):               # chips sticking out
        d.rounded_rectangle([x, y, x + 5, y + 9], 2, fill=(255, 90, 30, 255), outline=OUT)
    d.line([(15, 16), (17, 52)], fill=(250, 120, 120, 255), width=2)          # foil shine
    d.polygon([(32, 20), (24, 38), (28, 36), (26, 46), (38, 32), (33, 34), (36, 20)],
              fill=(255, 200, 40, 255), outline=OUT)                 # flame logo
    d.polygon([(31, 28), (28, 37), (31, 36), (30, 42), (35, 33)], fill=(255, 120, 20, 255))
    _outlined_text(d, (32 - _text_w(d, "HOT") // 2, 40), "HOT", (255, 235, 60, 255))
    return im


def chip(n=16):
    """A rolled-up chip (alpha only; tinted red-orange by the emitter)."""
    c = (n - 1) / 2

    def f(x, y):
        u, v = (x - c) * .8 + (y - c) * .6, -(x - c) * .6 + (y - c) * .8
        return 1 if abs(u) <= 6 and abs(v) <= 2.6 else 0
    return _alpha(n, n, f)


def deal_shades(size=64):
    """Big black pixel 'deal with it' shades: chunky lenses, white glints, bridge, arms."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    K, W = (10, 10, 14, 255), (245, 245, 255, 255)
    d.rectangle([2, 24, 61, 29], fill=K)                             # top bar
    d.rectangle([6, 30, 28, 37], fill=K)                             # left lens, stepped bottom
    d.rectangle([10, 38, 26, 41], fill=K)
    d.rectangle([35, 30, 57, 37], fill=K)                            # right lens
    d.rectangle([39, 38, 55, 41], fill=K)
    d.rectangle([28, 30, 35, 32], fill=K)                            # bridge
    for x0 in (9, 38):                                               # pixel glints
        d.rectangle([x0, 31, x0 + 3, 32], fill=W)
        d.rectangle([x0 + 4, 33, x0 + 7, 34], fill=W)
    return im


def glint(n=16):
    """A four-point sparkle (alpha only)."""
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = abs(x - c), abs(y - c)
        return 1 if (dx < 1.2 and dy < 7.5) or (dy < 1.2 and dx < 7.5) or (dx + dy < 3.2) else 0
    return _alpha(n, n, f)


def sweat_drop(size=32):
    """A big blue cartoon sweat drop."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (20, 40, 90, 255)
    d.polygon([(16, 3), (9, 16), (23, 16)], fill=(110, 180, 255, 255))
    d.ellipse([8, 11, 24, 27], fill=(110, 180, 255, 255), outline=OUT)
    d.line([(16, 3), (9, 16)], fill=OUT)
    d.line([(16, 3), (23, 16)], fill=OUT)
    d.ellipse([11, 15, 15, 21], fill=(235, 248, 255, 255))
    return im


def pocket_sand_sign(size=64):
    """A comic-book burst yelling POCKET SAND!"""
    import math
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (20, 10, 10, 255)
    pts = []
    for k in range(28):
        a = k * math.pi * 2 / 28
        r = 31 if k % 2 == 0 else 22
        pts.append((31.5 + r * math.cos(a), 31.5 + r * .78 * math.sin(a)))
    d.polygon(pts, fill=(255, 215, 40, 255), outline=OUT)
    inner = [(31.5 + (x - 31.5) * .78, 31.5 + (y - 31.5) * .78) for x, y in pts]
    d.polygon(inner, fill=(255, 245, 140, 255))
    red = (225, 25, 25, 255)
    _outlined_text(d, (32 - _text_w(d, "POCKET") // 2, 21), "POCKET", red)
    _outlined_text(d, (32 - _text_w(d, "SAND!") // 2, 29), "SAND!", red)
    return im


# ------------------------------------------------------------------ set 4: fifteen more moves

def burst_sign(lines, fill=(255, 215, 40, 255), text=(225, 25, 25, 255), spikes=22, size=64, cy=31.5, flat=.8):
    """A comic-book burst with shouted text (WHAM!, HONK!, STOMP!, HI-YAH!). cy / flat move the burst up and
    squash it (a sign that has to sit above something), the text stays full size."""
    import math
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (20, 10, 10, 255)
    # the burst hugs the words (signs show at 2:1, so every spare texel is 2 screen px of sign)
    tw = max(_text_w(d, line) for line in lines) + 2
    th = len(lines) * 8
    rx, ry = min(27, tw / 2 + 2), min(27, th / 2 + 3)          # the valleys just clear the text
    pts = []
    for k in range(spikes):
        a = k * math.pi * 2 / spikes
        grow = 4 if k % 2 == 0 else 0                         # spike tips
        pts.append((31.5 + (rx + grow) * math.cos(a), cy + (ry + grow) * math.sin(a)))
    d.polygon(pts, fill=fill, outline=OUT)
    light = tuple(min(255, c + 60) for c in fill[:3]) + (255,)
    d.polygon([(31.5 + (x - 31.5) * .75, cy + (y - cy) * .75) for x, y in pts], fill=light)
    y0 = round(cy + .5 - (len(lines) * 8 - 2) / 2)          # 6-tall glyphs, 2 between lines (the outlines)
    for k, line in enumerate(lines):
        _outlined_text(d, (32 - _text_w(d, line) // 2, y0 + k * 8), line, text)
    return im


def soft_puff(n=16, hard=1.25):
    """A round soft puff (alpha only): steam, smoke, dust, foam."""
    c = (n - 1) / 2
    return _alpha(n, n, lambda x, y: hard - ((x - c) ** 2 + (y - c) ** 2) ** .5 / (n / 2))


def tall_puff(w=16, h=32):
    """A billowing column of smoke (alpha only): four soft lumps stacked."""
    blobs = [(8, 25, 6), (6, 18, 5.5), (10, 12, 5), (7, 6, 4.5)]
    return _alpha(w, h, lambda x, y: max(1.4 - ((x - bx) ** 2 + (y - by) ** 2) ** .5 / r for bx, by, r in blobs))


def ring(n=16):
    """A thin ring (alpha only): ripples in the air."""
    c = (n - 1) / 2
    return _alpha(n, n, lambda x, y: 1 - abs(((x - c) ** 2 + (y - c) ** 2) ** .5 - 6.2) / 1.3)


def heart(n=16):
    """A little heart (alpha only)."""
    def f(x, y):
        u, v = (x - 7.5) / 7, (8 - y) / 7
        return 1 if (u * u + v * v - 1) ** 3 - u * u * v ** 3 <= 0 else 0
    return _alpha(n, n, f)


def weed_leaf(n=16):
    """A seven-fingered weed leaf (alpha only; tinted green)."""
    import math
    c, base = (n - 1) / 2, (7.5, 14.0)

    def f(x, y):
        dx, dy = x - base[0], base[1] - y
        r, a = math.hypot(dx, dy), math.degrees(math.atan2(dx, dy))
        for ang, ln in ((0, 13), (-30, 11), (30, 11), (-62, 8), (62, 8), (-95, 5), (95, 5)):
            da = abs(a - ang)
            if r <= ln and da < 11 * (1 - r / (ln + 1)) + 2:
                return 1
        return 1 if abs(dx) < .8 and 0 <= -dy < 2 else 0
    return _alpha(n, n, f)


def flame_blob(w=16, h=32):
    """A fat licking flame for breath and trails (alpha only)."""
    import math

    def f(x, y):
        t = y / (h - 1)
        half = (w / 2) * (t ** .5)
        cx = (w - 1) / 2 + math.sin(t * 9) * (1 - t) * 1.6
        return (1 - abs(x - cx) / max(.6, half)) * 1.8 if t > .04 else 0
    return _alpha(w, h, f)


def chunk(n=16):
    """A jagged chunk of brick (alpha only)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        a = math.atan2(y - c, x - c)
        r = 4.2 + 1.4 * math.sin(a * 3 + 1) + .8 * math.sin(a * 5)
        return 1 if math.hypot(x - c, y - c) <= r else 0
    return _alpha(n, n, f)


def jet(size=64):
    """A bright-yellow ultra-budget airliner (Spirit Airlines style), side view, nose right, duct tape holding it
    together - with a rope ladder hanging off it."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (20, 20, 20, 255)
    Y, YD = (255, 222, 0, 255), (210, 170, 0, 255)
    d.polygon([(6, 27), (52, 25), (61, 30), (52, 36), (8, 36), (3, 31)], fill=Y, outline=OUT)
    d.polygon([(8, 27), (2, 13), (10, 13), (20, 27)], fill=Y, outline=OUT)                        # tail fin
    d.polygon([(26, 34), (38, 34), (30, 50), (22, 50)], fill=YD, outline=OUT)                       # wing
    d.rectangle([24, 44, 34, 48], fill=(90, 90, 100, 255), outline=OUT)                             # engine
    d.line([(8, 35), (52, 35)], fill=YD)
    for x in range(42, 51, 3):
        d.rectangle([x, 28, x + 1, 29], fill=(40, 40, 50, 255))                                     # windows
    d.polygon([(52, 27), (57, 28), (58, 30), (53, 30)], fill=(40, 60, 90, 255))                    # cockpit
    tape = (175, 180, 185, 255)                                                                     # duct tape
    d.line([(4, 18), (9, 24)], fill=tape, width=2)
    d.line([(9, 18), (4, 24)], fill=tape, width=2)
    m = _text_mask("spirit")
    im.paste(OUT, (14, 27), m)                                                                     # the logo
    rope = (200, 160, 90, 255)                                                                      # rope ladder
    for x in (38, 44):
        d.line([(x, 36), (x + 1, 62)], fill=rope, width=1)
    for y in range(40, 63, 4):
        d.line([(38 + (y - 36) // 26, y), (44 + (y - 36) // 26, y)], fill=rope)
    return im


def suitcase(size=32):
    """A beat-up purple hard-shell suitcase, handle up, stickers and a luggage tag (32px, shown at 2:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (20, 15, 30, 255)
    d.rectangle([11, 4, 20, 8], outline=OUT, width=2)                                              # handle
    d.rounded_rectangle([3, 8, 28, 29], 3, fill=(150, 60, 200, 255), outline=OUT)
    d.line([(4, 10), (27, 10)], fill=(195, 120, 240, 255))
    for x in (10, 21):                                                                             # ridges
        d.line([(x, 9), (x, 28)], fill=(110, 40, 150, 255))
    d.rectangle([5, 13, 9, 17], fill=(255, 220, 40, 255))                                          # stickers
    d.ellipse([22, 20, 26, 24], fill=(60, 200, 120, 255))
    d.rectangle([13, 18, 18, 22], fill=(240, 80, 80, 255))
    d.line([(20, 8), (24, 4)], fill=(240, 240, 240, 255))                                          # luggage tag
    d.rectangle([23, 1, 28, 5], fill=(255, 255, 255, 255), outline=OUT)
    return im


def wave_crest(size=64):
    """A big curling wave of water with foam on top (symmetric: it rolls either way)."""
    import math
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(0, 63)]
    for x in range(0, 64, 2):
        pts.append((x, 63 - 44 * math.exp(-((x - 32) / 18) ** 2) - 4 * math.sin(x / 3)))
    pts.append((63, 63))
    d.polygon(pts, fill=(40, 110, 220, 255), outline=(15, 40, 110, 255))
    d.polygon([(x, y + 8) for x, y in pts[1:-1]] + [(63, 63), (0, 63)], fill=(30, 85, 190, 255))
    for x, y in pts[1:-1:2]:
        if y < 50:
            d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=(240, 250, 255, 255))                       # foam
    for x in range(8, 60, 9):
        d.arc([x - 4, 40, x + 4, 48], 200, 340, fill=(140, 200, 255, 255))
    return im


def rubber_duck(size=32):
    """A yellow rubber duck."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (90, 60, 0, 255)
    d.ellipse([4, 15, 26, 29], fill=(255, 215, 30, 255), outline=OUT)                               # body
    d.ellipse([14, 4, 27, 17], fill=(255, 215, 30, 255), outline=OUT)                               # head
    d.polygon([(26, 10), (31, 12), (26, 14)], fill=(255, 120, 20, 255), outline=OUT)                # beak
    d.ellipse([20, 8, 23, 11], fill=(10, 10, 10, 255))
    d.point((21, 8), fill=(255, 255, 255, 255))
    d.arc([8, 18, 18, 26], 180, 330, fill=OUT)                                                      # wing
    return im


def power_cable(size=64):
    """A snapped power line hanging down from the top, frayed live end sparking."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.line([(4, 0), (14, 20), (30, 38), (34, 50)], fill=(15, 15, 20, 255), width=5)
    d.line([(4, 0), (14, 20), (30, 38), (34, 50)], fill=(60, 60, 70, 255), width=2)
    for a, b in (((34, 50), (29, 57)), ((34, 50), (37, 58)), ((34, 50), (41, 54))):
        d.line([a, b], fill=(200, 120, 60, 255), width=1)                                           # copper strands
    Y = (255, 245, 90, 255)
    for a, b in (((34, 52), (24, 62)), ((36, 52), (48, 63)), ((35, 51), (52, 48)), ((33, 51), (18, 50))):
        d.line([a, b], fill=Y, width=2)                                                            # sparks
    d.ellipse([30, 47, 39, 56], fill=(255, 255, 220, 255))
    return im


def skeleton(size=64):
    """A cartoon x-ray skeleton (the target, electrocuted)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    B, K = (250, 250, 240, 255), (10, 10, 30, 255)
    d.ellipse([20, 2, 44, 24], fill=B, outline=K)                                                   # skull
    d.ellipse([25, 9, 31, 15], fill=K)
    d.ellipse([33, 9, 39, 15], fill=K)
    d.polygon([(31, 17), (33, 17), (32, 19)], fill=K)
    d.rectangle([26, 20, 38, 24], fill=B, outline=K)                                                # teeth
    for x in range(28, 38, 2):
        d.line([(x, 20), (x, 24)], fill=K)
    d.line([(32, 25), (32, 48)], fill=B, width=3)                                                   # spine
    for y in range(28, 44, 4):
        d.arc([20, y - 3, 44, y + 7], 200, 340, fill=B, width=2)                                    # ribs
    d.line([(22, 28), (8, 40), (6, 52)], fill=B, width=3)                                           # arms up-ish
    d.line([(42, 28), (56, 40), (58, 52)], fill=B, width=3)
    d.ellipse([24, 46, 40, 54], fill=B, outline=K)                                                  # hips
    d.line([(27, 53), (22, 63)], fill=B, width=3)
    d.line([(37, 53), (42, 63)], fill=B, width=3)
    return im


def traffic_cone(size=32):
    """An orange traffic cone."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (60, 20, 0, 255)
    d.polygon([(16, 3), (24, 25), (8, 25)], fill=(255, 110, 20, 255), outline=OUT)
    d.polygon([(12.5, 13), (19.5, 13), (21.2, 18), (10.8, 18)], fill=(250, 250, 250, 255))       # reflective band
    d.rectangle([4, 25, 28, 29], fill=(230, 90, 15, 255), outline=OUT)                              # base
    return im


def liquor_bottle(size=32):
    """A fifth of brown liquor: dark glass, gold label 'XO'."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (25, 10, 5, 255)
    d.rectangle([13, 2, 18, 9], fill=(60, 30, 10, 255), outline=OUT)                                 # neck
    d.rectangle([12, 1, 19, 3], fill=(200, 170, 60, 255), outline=OUT)                               # cap
    d.rounded_rectangle([8, 9, 23, 30], 4, fill=(110, 50, 15, 255), outline=OUT)                     # body
    d.rectangle([10, 16, 21, 24], fill=(230, 195, 80, 255), outline=OUT)                             # label
    d.text((11, 15), "XO", fill=(60, 20, 0, 255))
    d.line([(10, 11), (10, 28)], fill=(200, 120, 60, 255))                                           # shine
    return im


def work_boot(size=64):
    """A giant tan work boot, stomping down (sole at the bottom)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (40, 20, 5, 255)
    d.polygon([(18, 2), (40, 2), (42, 30), (60, 38), (61, 50), (6, 50), (8, 34), (16, 28)],
              fill=(205, 150, 70, 255), outline=OUT)                                                 # upper
    d.rectangle([4, 50, 62, 58], fill=(70, 40, 20, 255), outline=OUT)                                # sole
    for x in range(8, 60, 6):
        d.line([(x, 58), (x + 3, 61)], fill=OUT, width=2)                                            # tread
    d.rectangle([16, 2, 42, 7], fill=(180, 125, 55, 255), outline=OUT)                               # collar
    for y in range(12, 32, 5):
        d.line([(22, y), (36, y + 2)], fill=(250, 240, 220, 255), width=2)                           # laces
    d.line([(10, 44), (58, 44)], fill=(160, 110, 45, 255), width=2)                                  # stitching
    return im


def jaw(top, size=64):
    """Half of a giant grinning mouth: lips and a row of gold grillz (top: teeth point down)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (40, 10, 10, 255)
    lip, gold, hi = (150, 50, 60, 255), (245, 195, 50, 255), (255, 245, 170, 255)
    if top:
        d.chord([2, 6, 61, 50], 180, 360, fill=lip, outline=OUT)
        for k in range(8):
            x = 6 + k * 7
            d.polygon([(x, 28), (x + 6, 28), (x + 5, 42), (x + 1, 42)], fill=gold, outline=OUT)
            d.line([(x + 2, 30), (x + 2, 38)], fill=hi)
    else:
        d.chord([2, 14, 61, 58], 0, 180, fill=lip, outline=OUT)
        for k in range(8):
            x = 6 + k * 7
            d.polygon([(x + 1, 22), (x + 5, 22), (x + 6, 36), (x, 36)], fill=gold, outline=OUT)
            d.line([(x + 2, 26), (x + 2, 33)], fill=hi)
    return im


def bullet(size=64, angle=-26.6):
    """A big copper hollow-point round, pre-rotated along the attack line (nose up-right)."""
    im = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (40, 20, 5, 255)
    d.rectangle([22, 38, 58, 58], fill=(200, 160, 60, 255), outline=OUT)                             # brass case
    d.line([(24, 41), (56, 41)], fill=(250, 220, 130, 255), width=2)
    d.polygon([(58, 38), (70, 40), (76, 44), (76, 52), (70, 56), (58, 58)], fill=(190, 100, 50, 255), outline=OUT)
    d.ellipse([71, 44, 77, 52], fill=(40, 15, 5, 255))                                              # hollow point
    d.rectangle([18, 36, 22, 60], fill=(180, 140, 50, 255), outline=OUT)                             # rim
    im = im.rotate(-angle, resample=Image.NEAREST, center=(48, 48))
    return im.crop((16, 16, 80, 80))


def glass_crack(size=64):
    """A spider-web crack (like shattered glass) - their defense, broken."""
    import math
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    W, D = (255, 255, 255, 255), (150, 170, 190, 255)
    c = (30, 30)
    for k in range(9):
        a = k * 2 * math.pi / 9 + .3
        p = [c]
        r = 0
        while r < 34:
            r += 7
            p.append((c[0] + r * math.cos(a + .18 * math.sin(r)), c[1] + r * math.sin(a + .18 * math.sin(r))))
        d.line(p, fill=D, width=3)
        d.line(p, fill=W, width=1)
    for r in (8, 16, 25):
        pts = [(c[0] + r * math.cos(k * 2 * math.pi / 9 + .3), c[1] + r * math.sin(k * 2 * math.pi / 9 + .3)) for k in range(10)]
        d.line(pts, fill=W, width=1)
    return im


def tire(size=32):
    """A car tire with a chrome rim."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([2, 2, 29, 29], fill=(30, 30, 35, 255), outline=(5, 5, 8, 255))
    d.ellipse([9, 9, 22, 22], fill=(200, 205, 215, 255), outline=(90, 95, 110, 255))
    d.ellipse([13, 13, 18, 18], fill=(120, 125, 140, 255))
    for k in range(0, 360, 30):
        import math
        x, y = 15.5 + 12 * math.cos(math.radians(k)), 15.5 + 12 * math.sin(math.radians(k))
        d.point((x, y), fill=(70, 70, 80, 255))                                                     # tread
    return im


def slash_arc(size=64):
    """A bright crescent slash streak."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.arc([4, 8, 60, 64], 200, 340, fill=(255, 120, 140, 255), width=7)
    d.arc([4, 8, 60, 64], 205, 335, fill=(255, 255, 255, 255), width=4)
    return im


def cough_bubble(size=32):
    """A thought-cloud reading *cough*."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (40, 40, 40, 255)
    for bx, by, r in ((8, 13, 7), (16, 10, 8), (24, 13, 7), (16, 17, 8)):
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=(235, 235, 225, 255), outline=OUT)
    for bx, by, r in ((8, 13, 6), (16, 10, 7), (24, 13, 6), (16, 17, 7)):
        d.ellipse([bx - r, by - r, bx + r, by + r], fill=(235, 235, 225, 255))
    d.ellipse([4, 25, 8, 29], fill=(235, 235, 225, 255), outline=OUT)
    glyphs = {"c": ["011", "100", "100", "011"], "o": ["010", "101", "101", "010"], "u": ["101", "101", "101", "011"],
              "g": ["011", "101", "011", "001", "110"], "h": ["100", "110", "101", "101"]}
    for k, ch in enumerate("cough"):
        for yy, row in enumerate(glyphs[ch]):
            for xx, bit in enumerate(row):
                if bit == "1":
                    d.point((4 + k * 5 + xx, 11 + yy), fill=(60, 60, 60, 255))
    return im


def flame_wheel(size=64):
    """A tire wrapped in fire (spins)."""
    import math
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for k in range(12):                                                                              # flames round it
        a = k * math.pi / 6
        tip = (32 + 31 * math.cos(a + .25), 32 + 31 * math.sin(a + .25))
        l = (32 + 20 * math.cos(a - .2), 32 + 20 * math.sin(a - .2))
        r = (32 + 20 * math.cos(a + .45), 32 + 20 * math.sin(a + .45))
        d.polygon([l, tip, r], fill=(255, 130, 20, 255))
        d.polygon([l, (32 + 26 * math.cos(a + .2), 32 + 26 * math.sin(a + .2)), r], fill=(255, 225, 70, 255))
    d.ellipse([12, 12, 52, 52], fill=(30, 30, 35, 255), outline=(5, 5, 8, 255))
    d.ellipse([22, 22, 42, 42], fill=(205, 210, 220, 255), outline=(90, 95, 110, 255))
    for k in range(5):
        a = k * 2 * math.pi / 5
        d.line([(32, 32), (32 + 9 * math.cos(a), 32 + 9 * math.sin(a))], fill=(90, 95, 110, 255), width=2)
    return im


def cinder_blocks(size=64):
    """A stack of three red bricks on top of each other (for a karate chop)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (50, 15, 10, 255)
    for k in range(3):
        y = 22 + k * 13
        d.rectangle([6, y, 57, y + 11], fill=(185, 65, 45, 255), outline=OUT)
        d.line([(8, y + 2), (55, y + 2)], fill=(220, 110, 85, 255))
        for hx in (18, 32, 46):
            d.rectangle([hx - 3, y + 4, hx + 3, y + 8], fill=(120, 35, 25, 255))
    return im


def karate_hand(size=32):
    """A flat karate-chop hand, blade edge down, with a red wristband."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (60, 30, 15, 255)
    d.polygon([(6, 4), (24, 4), (26, 26), (8, 26)], fill=(235, 185, 140, 255), outline=OUT)
    d.polygon([(24, 8), (30, 12), (28, 18), (25, 16)], fill=(235, 185, 140, 255), outline=OUT)      # thumb
    for y in (10, 15, 20):
        d.line([(9, y), (22, y)], fill=(200, 145, 105, 255))                                         # fingers
    d.rectangle([5, 0, 25, 5], fill=(220, 30, 30, 255), outline=OUT)                                 # wristband
    return im


def eight_ball(size=64):
    """A glossy black Magic 8-Ball."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([3, 3, 60, 60], fill=(20, 20, 28, 255), outline=(60, 40, 110, 255), width=2)
    d.ellipse([10, 8, 30, 22], fill=(70, 70, 90, 255))                                              # gloss
    d.ellipse([13, 10, 22, 16], fill=(160, 160, 190, 255))
    d.ellipse([20, 20, 44, 44], fill=(250, 250, 250, 255), outline=(10, 10, 10, 255))
    d.ellipse([27, 22, 37, 31], outline=(10, 10, 10, 255), width=2)                                  # the 8
    d.ellipse([26, 30, 38, 41], outline=(10, 10, 10, 255), width=2)
    return im


def eight_answer(size=64):
    """The 8-Ball's answer window: a blue triangle saying OUTLOOK NOT GOOD."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.ellipse([1, 1, 62, 62], fill=(15, 15, 25, 255), outline=(90, 60, 160, 255), width=2)
    d.polygon([(32, 54), (6, 12), (58, 12)], fill=(40, 70, 200, 255), outline=(120, 160, 255, 255))
    for k, line in enumerate(("OUTLOOK", "NOT", "GOOD")):
        _outlined_text(d, (32 - _text_w(d, line) // 2, 13 + k * 11), line, (255, 255, 255, 255),
                       outline=(20, 30, 90, 255))
    return im


def heart_pendant(size=64):
    """A gold heart pendant engraved RIDE OR DIE, on a chain."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (90, 50, 0, 255)
    for x in range(10, 54, 4):                                                                       # the chain
        d.ellipse([x, 2 + abs(x - 32) // 3, x + 4, 6 + abs(x - 32) // 3], outline=(245, 200, 60, 255))
    hp = []
    import math
    for k in range(64):
        t = k / 64 * 2 * math.pi
        hp.append((32 + 26 * math.sin(t) ** 3 * 1.0, 34 - (17 * math.cos(t) - 6 * math.cos(2 * t) - 3 * math.cos(3 * t)
                                                          - math.cos(4 * t)) * 1.3))
    d.polygon(hp, fill=(245, 190, 40, 255), outline=OUT)
    d.polygon([(32 + (x - 32) * .8, 34 + (y - 34) * .8) for x, y in hp], fill=(255, 220, 90, 255))
    _outlined_text(d, (32 - _text_w(d, "RIDE") // 2, 20), "RIDE", (200, 20, 40, 255), outline=(255, 245, 200, 255))
    _outlined_text(d, (32 - _text_w(d, "OR DIE") // 2, 31), "OR DIE", (200, 20, 40, 255), outline=(255, 245, 200, 255))
    return im


def big_weed_leaf(size=64):
    """A big glowing weed leaf (the intro to the leaf storm)."""
    import math
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    base = (32, 58)
    for ang, ln, wd in ((0, 52, 9), (-30, 44, 8), (30, 44, 8), (-62, 32, 6), (62, 32, 6), (-95, 18, 4), (95, 18, 4)):
        a = math.radians(ang)
        tip = (base[0] + ln * math.sin(a), base[1] - ln * math.cos(a))
        l = (base[0] + ln * .45 * math.sin(a - .22), base[1] - ln * .45 * math.cos(a - .22))
        r = (base[0] + ln * .45 * math.sin(a + .22), base[1] - ln * .45 * math.cos(a + .22))
        d.polygon([base, l, tip, r], fill=(60, 170, 50, 255), outline=(20, 70, 20, 255))
        d.line([base, tip], fill=(140, 220, 110, 255))
    d.line([base, (32, 63)], fill=(20, 70, 20, 255), width=2)
    return im


def half_stack(size=64):
    """The left half of a stack of three bricks, broken down the middle (jagged right edge at the centre).
    The right half is this turned 180 degrees: both drawn at the same spot make the whole stack."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (50, 15, 10, 255)
    for k in range(3):
        y = 14 + k * 12                                     # rows 14-49: centred, so the turned half lines up
        jag = [(32, y), (30, y + 3), (33, y + 6), (31, y + 9), (32, y + 11)] if k % 2 == 0 else \
              [(31, y), (33, y + 3), (30, y + 6), (32, y + 9), (31, y + 11)]
        d.polygon([(4, y), *jag, (4, y + 11)], fill=(190, 70, 48, 255), outline=OUT)
        d.line([(6, y + 2), (28, y + 2)], fill=(225, 115, 90, 255))
        d.rectangle([12, y + 4, 18, y + 8], fill=(120, 35, 25, 255))                               # the hole
        d.line([(5, y + 10), (29, y + 10)], fill=(140, 45, 30, 255))
    return im


def big_hand(size=64):
    """A giant flat karate-chop hand coming down blade-first, with motion lines and a red wristband."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (70, 35, 15, 255)
    for x in (14, 24, 34, 44):                                                                       # motion lines
        d.line([(x, 0), (x, 12)], fill=(255, 255, 255, 255), width=2)
    d.rectangle([16, 10, 46, 18], fill=(220, 30, 30, 255), outline=OUT)                              # wristband
    d.polygon([(18, 18), (44, 18), (46, 52), (20, 60), (16, 52)], fill=(240, 190, 145, 255), outline=OUT)
    d.polygon([(44, 24), (54, 30), (52, 40), (45, 36)], fill=(240, 190, 145, 255), outline=OUT)      # thumb
    for x in (24, 30, 36):
        d.line([(x, 22), (x + 1, 50)], fill=(205, 150, 110, 255))                                    # fingers
    d.line([(17, 53), (20, 61)], fill=(255, 235, 200, 255), width=2)                                 # the blade edge
    return im


def bullet_hole(size=64):
    """A fresh bullet hole: dark hole, torn bright rim, cracks shooting out, a wisp of smoke."""
    import math
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = (32, 33)
    for k in range(10):                                                                              # cracks
        a = k * 2 * math.pi / 10 + .2
        p, r = [c], 0
        while r < 26:
            r += 6
            p.append((c[0] + r * math.cos(a + .25 * math.sin(r * 1.7)), c[1] + r * math.sin(a + .25 * math.sin(r * 1.7))))
        d.line(p, fill=(40, 30, 30, 255), width=2)
        d.line(p[:3], fill=(255, 240, 220, 255), width=1)
    d.ellipse([22, 23, 42, 43], fill=(255, 230, 190, 255))                                           # hot rim
    d.ellipse([24, 25, 40, 41], fill=(120, 60, 30, 255))
    d.ellipse([26, 27, 38, 39], fill=(15, 10, 10, 255))                                              # the hole
    d.ellipse([28, 29, 31, 32], fill=(60, 40, 40, 255))
    for x, y, r in ((40, 18, 4), (44, 12, 3), (41, 7, 2)):                                           # smoke
        d.ellipse([x - r, y - r, x + r, y + r], fill=(200, 200, 205, 200))
    return im


def laser_dot(n=16):
    """A laser-sight dot: a tiny hot core with a faint glow round it (alpha only, tinted red)."""
    c = (n - 1) / 2

    def f(x, y):
        r = ((x - c) ** 2 + (y - c) ** 2) ** .5
        return 1 if r < 1.6 else .35 * (1 - (r - 1.6) / 3) if r < 4.6 else 0
    return _alpha(n, n, f)


# ------------------------------------------------------------------ set 5: the everyday moves

def _big(size, k=4):
    """A transparent canvas k times the texture size (draw big, then `_shrink` for clean edges)."""
    S = size * k
    im = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im), S


def _shrink(im, size):
    return im.resize((size, size), Image.LANCZOS)


def _big_text(im, text, centre, fill, scale=2, font=None):
    """Pixel text blown up `scale` times (nearest neighbour), with a 1px dark outline, centred at `centre`."""
    m = _text_mask(text, font or GLYPHS)
    t = Image.new("RGBA", m.size, (0, 0, 0, 0))
    t.paste(fill, (0, 0), m)
    t = t.resize((t.width * scale, t.height * scale), Image.NEAREST)
    x, y = round(centre[0] - t.width / 2), round(centre[1] - t.height / 2)
    out = Image.new("RGBA", t.size, (20, 10, 10, 255))
    mask = t.split()[3]
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx or dy:
                im.paste(out, (x + dx, y + dy), mask)
    im.alpha_composite(t, (x, y))


def flashlight(size=64):
    """A big black police flashlight pointing right, lens blazing."""
    im, d, S = _big(size)
    OUT = (10, 10, 14, 255)
    cy = S // 2
    d.rounded_rectangle([S * .02, cy - 30, S * .6, cy + 30], 14, fill=(45, 45, 55, 255), outline=OUT, width=7)
    for x in range(int(S * .08), int(S * .46), 16):                                                # knurled grip
        d.line([(x, cy - 24), (x, cy + 24)], fill=(25, 25, 30, 255), width=6)
    d.line([(S * .05, cy - 18), (S * .58, cy - 18)], fill=(130, 130, 150, 255), width=8)           # shine
    d.polygon([(S * .58, cy - 32), (S * .76, cy - 62), (S * .84, cy - 62), (S * .84, cy + 62),
               (S * .76, cy + 62), (S * .58, cy + 32)], fill=(60, 60, 72, 255), outline=OUT)         # flared head
    d.line([(S * .61, cy - 30), (S * .77, cy - 56)], fill=(160, 160, 180, 255), width=8)
    d.ellipse([S * .78, cy - 62, S * .97, cy + 62], fill=(255, 250, 200, 255), outline=OUT, width=7)  # lens
    d.ellipse([S * .83, cy - 42, S * .94, cy + 42], fill=(255, 255, 255, 255))
    d.rounded_rectangle([S * .3, cy - 44, S * .42, cy - 28], 5, fill=(220, 30, 30, 255), outline=OUT, width=5)
    return _shrink(im, size)


def light_cone(size=64):
    """A blinding cone of light: tip at the left edge, opening to the right, hot spot where it lands."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = im.load()
    c = (size - 1) / 2
    for y in range(size):
        for x in range(size):
            t = x / (size - 1)
            half = 2 + 26 * t
            v = abs(y - c) / half
            if v > 1:
                continue
            a = (110 + 120 * (1 - v) ** 1.5) * min(1, t * 6)
            hot = max(0, 1 - ((x - (size - 7)) ** 2 / 60 + (y - c) ** 2 / 300))
            r, g, b = 255, 250 - round(30 * v), 190 - round(80 * v)
            if hot:
                r, g, b, a = 255, 255, 255 - round(50 * (1 - hot)), max(a, 255 * min(1, hot * 1.5))
            px[x, y] = (r, g, b, round(min(255, a)))
    return im


def dizzy_swirl(n=16):
    """A spiral (alpha only): the hypnotised-eyes swirl."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        r, a = math.hypot(x - c, y - c), math.atan2(y - c, x - c) % (2 * math.pi)
        if r > 7.6:
            return 0
        best = min(abs(r - 2.6 * (a + 2 * math.pi * k) / (2 * math.pi)) for k in range(3))
        return 1.4 - best / 1.0
    return _alpha(n, n, f)


def stun_gun(size=64):
    """A black handheld stun gun pointing right, a fat blue arc snapping between its two prongs."""
    im, d, S = _big(size)
    OUT = (8, 8, 12, 255)
    d.rounded_rectangle([S * .08, S * .36, S * .7, S * .6], 14, fill=(40, 40, 48, 255), outline=OUT, width=6)
    d.polygon([(S * .14, S * .56), (S * .34, S * .56), (S * .3, S * .9), (S * .1, S * .9)],
              fill=(30, 30, 36, 255), outline=OUT)                                                  # grip
    for y in range(int(S * .62), int(S * .88), 14):
        d.line([(S * .14, y), (S * .3, y)], fill=(70, 70, 80, 255), width=4)
    d.line([(S * .12, S * .42), (S * .66, S * .42)], fill=(110, 110, 125, 255), width=6)
    d.rectangle([S * .3, S * .45, S * .5, S * .53], fill=(250, 210, 30, 255), outline=OUT, width=3)  # warning strip
    for yy in (.39, .57):                                                                            # prongs
        d.rectangle([S * .7, S * yy - 6, S * .8, S * yy + 6], fill=(200, 205, 215, 255), outline=OUT, width=3)
    pts = [(S * .8, S * .39), (S * .9, S * .3), (S * .84, S * .45), (S * .97, S * .43), (S * .86, S * .52),
           (S * .93, S * .66), (S * .8, S * .57)]
    d.line(pts, fill=(60, 140, 255, 255), width=16)
    d.line(pts, fill=(230, 245, 255, 255), width=6)
    return _shrink(im, size)


def _seg_dist(p, a, b):
    import math
    ax, ay, bx, by = *a, *b
    t = max(0, min(1, ((p[0] - ax) * (bx - ax) + (p[1] - ay) * (by - ay)) / ((bx - ax) ** 2 + (by - ay) ** 2)))
    return math.hypot(p[0] - ax - t * (bx - ax), p[1] - ay - t * (by - ay))


def crackle(n=16):
    """A little snapping electric spark (alpha only): a jagged X."""
    lines = [((1, 3), (6, 7), (5, 9), (14, 13)), ((13, 1), (9, 6), (11, 8), (2, 14))]
    return _alpha(n, n, lambda x, y: 1.4 - min(_seg_dist((x, y), a, b) for ln in lines
                                               for a, b in zip(ln, ln[1:])) / 1.1)


def static_ring(size=64):
    """A ring of crackling electricity (cyan with a white-hot core) - it paralyses whatever's inside."""
    import math
    im, d, S = _big(size)
    c = S / 2
    pts = []
    for k in range(37):
        a = k * 2 * math.pi / 36
        r = S * (.4 if k % 2 else .46) + (S * .03 if k % 3 == 0 else 0)
        pts.append((c + r * math.cos(a), c + r * .8 * math.sin(a)))
    d.line(pts, fill=(40, 120, 255, 255), width=26)
    d.line(pts, fill=(140, 230, 255, 255), width=14)
    d.line(pts, fill=(255, 255, 255, 255), width=5)
    for k in range(0, 36, 6):                                                                       # sparks off it
        a = k * 2 * math.pi / 36 + .2
        p0 = (c + S * .44 * math.cos(a), c + S * .35 * math.sin(a))
        p1 = (c + S * .5 * math.cos(a + .08), c + S * .41 * math.sin(a + .08))
        d.line([p0, p1], fill=(220, 250, 255, 255), width=8)
    return _shrink(im, size)


def boombox(size=64):
    """A chrome-and-black 80s boombox: two big speakers, tape deck, handle, BASS label."""
    im, d, S = _big(size)
    OUT = (10, 10, 14, 255)
    d.rounded_rectangle([S * .2, S * .1, S * .8, S * .3], 14, outline=(200, 200, 215, 255), width=14)   # handle
    d.rounded_rectangle([S * .03, S * .26, S * .97, S * .86], 18, fill=(205, 208, 220, 255), outline=OUT, width=7)
    d.rectangle([S * .06, S * .29, S * .94, S * .34], fill=(245, 245, 255, 255))
    for cx in (.23, .77):                                                                            # speakers
        d.ellipse([S * (cx - .17), S * .39, S * (cx + .17), S * .83], fill=(30, 30, 36, 255), outline=OUT, width=6)
        d.ellipse([S * (cx - .12), S * .46, S * (cx + .12), S * .76], fill=(55, 55, 65, 255))
        d.ellipse([S * (cx - .05), S * .56, S * (cx + .05), S * .66], fill=(150, 150, 165, 255), outline=OUT, width=3)
    d.rectangle([S * .42, S * .44, S * .58, S * .6], fill=(40, 40, 50, 255), outline=OUT, width=4)     # tape deck
    d.ellipse([S * .445, S * .49, S * .49, S * .55], outline=(200, 200, 215, 255), width=4)
    d.ellipse([S * .51, S * .49, S * .555, S * .55], outline=(200, 200, 215, 255), width=4)
    for k in range(4):                                                                               # buttons
        d.rectangle([S * (.42 + k * .04), S * .65, S * (.45 + k * .04), S * .7],
                    fill=((230, 40, 40, 255) if k == 0 else (60, 60, 70, 255)), outline=OUT, width=2)
    d.rectangle([S * .4, S * .74, S * .6, S * .82], fill=(230, 40, 40, 255), outline=OUT, width=3)    # EQ lights
    im = _shrink(im, size)
    d = ImageDraw.Draw(im)
    _outlined_text(d, (32 - _text_w(d, "BASS") // 2, 9), "BASS", (255, 220, 40, 255))
    return im


def music_note(n=16):
    """An eighth note (alpha only)."""
    def f(x, y):
        if (x - 5) ** 2 / 9 + (y - 12) ** 2 / 5 <= 1:
            return 1
        if 7 <= x <= 8 and 2 <= y <= 12:
            return 1
        if 8 <= x <= 13 and 2 + (x - 8) // 2 <= y <= 4 + (x - 8) // 2:
            return 1
        return 0
    return _alpha(n, n, f)


def sound_arc(w=16, h=32):
    """A sound-wave arc ")" - two nested bands bulging right (alpha only)."""
    import math

    def f(x, y):
        r = math.hypot(x + 10, (y - (h - 1) / 2) * .9)
        return max(1 - abs(r - 23) / 2.2, .7 * (1 - abs(r - 17) / 1.5))
    return _alpha(w, h, f)


def _hoodie(d, S, cap=False, arms_up=False):
    INK, OUT, RIM = (34, 28, 48, 255), (8, 6, 12, 255), (150, 110, 230, 255)
    cx = S / 2
    d.polygon([(cx - S * .28, S * .98), (cx - S * .26, S * .42), (cx + S * .26, S * .42), (cx + S * .28, S * .98)],
              fill=INK, outline=OUT)                                                                # body
    d.line([(cx - S * .26, S * .44), (cx - S * .28, S * .97)], fill=RIM, width=6)                    # rim light
    d.line([(cx + S * .26, S * .44), (cx + S * .28, S * .97)], fill=RIM, width=6)
    if arms_up:                                                                                     # throwing it up
        for s in (-1, 1):
            arm = [(cx + s * S * .22, S * .5), (cx + s * S * .4, S * .32), (cx + s * S * .36, S * .1)]
            d.line(arm, fill=OUT, width=34)
            d.line(arm, fill=INK, width=24)
            d.ellipse([cx + s * S * .36 - 16, S * .02, cx + s * S * .36 + 16, S * .14], fill=INK, outline=RIM,
                      width=4)
    if not cap:
        d.chord([cx - S * .21, S * .05, cx + S * .21, S * .5], 160, 380, fill=INK, outline=OUT)        # hood up
    d.ellipse([cx - S * .17, S * .1, cx + S * .17, S * .46], fill=INK, outline=OUT)                   # head
    if cap:
        d.chord([cx - S * .18, S * .06, cx + S * .18, S * .36], 180, 360, fill=(200, 30, 40, 255), outline=OUT)
        d.polygon([(cx - S * .18, S * .2), (cx - S * .36, S * .25), (cx - S * .18, S * .27)],
                  fill=(200, 30, 40, 255), outline=OUT)                                              # backwards brim
    else:
        d.arc([cx - S * .21, S * .05, cx + S * .21, S * .5], 190, 350, fill=RIM, width=6)
    for ex in (-.07, .07):                                                                          # glowing eyes
        d.ellipse([cx + S * ex - S * .035, S * .26, cx + S * ex + S * .035, S * .31], fill=(255, 255, 255, 255))
    d.arc([cx - S * .12, S * .4, cx + S * .12, S * .64], 20, 160, fill=(250, 200, 40, 255), width=8)  # gold chain
    if not arms_up:                                                                                 # arms crossed
        d.rounded_rectangle([cx - S * .3, S * .6, cx + S * .3, S * .74], 18, fill=(50, 42, 70, 255), outline=OUT,
                            width=5)
        d.line([(cx - S * .26, S * .62), (cx + S * .26, S * .72)], fill=RIM, width=4)


def squad_hoodie(size=64):
    """One of the squad: a shadowy figure, hood up, glowing eyes, arms crossed, gold chain."""
    im, d, S = _big(size)
    _hoodie(d, S)
    return _shrink(im, size)


def squad_cap(size=64):
    """Another of the squad: backwards red cap, both arms up throwing it up."""
    im, d, S = _big(size)
    _hoodie(d, S, cap=True, arms_up=True)
    return _shrink(im, size)


def water_balloon(size=32):
    """A fat blue water balloon with a tied knot."""
    im, d, S = _big(size)
    OUT = (10, 30, 90, 255)
    d.ellipse([S * .14, S * .08, S * .86, S * .8], fill=(50, 140, 255, 255), outline=OUT, width=6)
    d.ellipse([S * .26, S * .18, S * .44, S * .4], fill=(200, 235, 255, 255))
    d.polygon([(S * .44, S * .78), (S * .56, S * .78), (S * .6, S * .92), (S * .4, S * .92)], fill=(30, 110, 230, 255),
              outline=OUT)
    return _shrink(im, size)


def splash_crown(size=64):
    """A big splash of water bursting up: a crown of spikes and droplets, white foam rim."""
    import math
    im, d, S = _big(size)
    base = S * .78
    pts = [(S * .04, base)]
    for k in range(9):
        x = S * (.08 + k * .105)
        h = S * (.5 + .22 * math.sin(k * 1.9) + (.15 if k == 4 else 0))
        pts += [(x - S * .03, base - S * .08), (x + S * .01, base - h)]
    pts += [(S * .96, base - S * .08), (S * .96, base), (S * .5, S * .95)]
    d.polygon(pts, fill=(60, 150, 255, 255), outline=(15, 50, 140, 255))
    d.polygon([(x, y + (base - y) * .35) for x, y in pts], fill=(140, 205, 255, 255))
    d.ellipse([S * .1, base - S * .1, S * .9, base + S * .14], fill=(235, 248, 255, 255), outline=(15, 50, 140, 255),
              width=5)                                                                               # foam
    for x, y, r in ((.12, .12, .05), (.8, .08, .045), (.5, .03, .04), (.32, .18, .03), (.65, .2, .035)):
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], fill=(100, 180, 255, 255),
                  outline=(15, 50, 140, 255), width=4)
    return _shrink(im, size)


def droplet(n=16):
    """A falling water drop (alpha only)."""
    def f(x, y):
        if y >= 8:
            return 1 if (x - 7.5) ** 2 + (y - 10) ** 2 <= 16 else 0
        return 1 if abs(x - 7.5) <= (y - 1) * .55 else 0
    return _alpha(n, n, f)


def diss_bubble(size=64):
    """A big speech bubble: UR MID."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rounded_rectangle([S * .03, S * .08, S * .97, S * .7], 50, fill=(255, 255, 255, 255), outline=OUT, width=8)
    d.polygon([(S * .62, S * .66), (S * .82, S * .95), (S * .46, S * .68)], fill=(255, 255, 255, 255))
    d.line([(S * .62, S * .69), (S * .82, S * .95), (S * .46, S * .7)], fill=OUT, width=8)
    im = _shrink(im, size)
    _big_text(im, "UR", (32, 17), (225, 25, 30, 255))
    _big_text(im, "MID", (32, 33), (225, 25, 30, 255))
    return im


def slap_hand(size=64):
    """A giant open palm, fingers up (it comes down on the back of their head)."""
    im, d, S = _big(size)
    OUT, SKIN, SKIN_D = (80, 40, 20, 255), (245, 195, 150, 255), (215, 155, 115, 255)
    for x, top in ((.2, .08), (.33, .02), (.46, .04), (.59, .14)):                                    # fingers
        d.rounded_rectangle([S * x, S * top, S * (x + .12), S * .55], 24, fill=SKIN, outline=OUT, width=7)
    d.rounded_rectangle([S * .66, S * .46, S * .92, S * .62], 24, fill=SKIN, outline=OUT, width=7)   # thumb
    d.rounded_rectangle([S * .18, S * .4, S * .72, S * .96], 44, fill=SKIN, outline=OUT, width=8)    # palm
    d.arc([S * .28, S * .5, S * .62, S * .82], 200, 330, fill=SKIN_D, width=7)                       # palm lines
    d.arc([S * .26, S * .64, S * .64, S * .94], 210, 320, fill=SKIN_D, width=6)
    return _shrink(im, size)


def pow_lines(n=16):
    """Short impact lines bursting out of a point (alpha only)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        r, a = math.hypot(x - c, y - c), math.atan2(y - c, x - c)
        return 1 if 3.5 < r < 7.5 and (a % (math.pi / 4)) < .3 else 0
    return _alpha(n, n, f)


def double_cup(size=32):
    """A styrofoam double cup of purple drank, lid and straw."""
    im, d, S = _big(size)
    OUT = (40, 20, 60, 255)
    d.polygon([(S * .2, S * .28), (S * .8, S * .28), (S * .7, S * .96), (S * .3, S * .96)], fill=(250, 250, 250, 255),
              outline=OUT)                                                                           # outer cup
    d.line(((S * .2, S * .28), (S * .3, S * .96)), fill=OUT, width=5)
    d.line(((S * .8, S * .28), (S * .7, S * .96)), fill=OUT, width=5)
    d.line([(S * .25, S * .48), (S * .75, S * .48)], fill=(190, 190, 205, 255), width=5)               # double rim
    d.line([(S * .29, S * .86), (S * .71, S * .86)], fill=(190, 190, 205, 255), width=4)
    d.line([(S * .56, S * .22), (S * .7, S * .02)], fill=(230, 40, 60, 255), width=12)                 # straw
    d.rounded_rectangle([S * .14, S * .2, S * .86, S * .3], 6, fill=(240, 240, 248, 255), outline=OUT, width=5)  # lid
    for k in range(3):                                                                               # drank drips
        x = S * (.34 + k * .16)
        d.line([(x, S * .3), (x, S * (.42 + .1 * (k % 2)))], fill=(160, 60, 230, 255), width=9)
    d.ellipse([S * .38, S * .58, S * .62, S * .8], fill=(170, 70, 235, 255), outline=OUT, width=4)  # logo
    return _shrink(im, size)


def goop(w=16, h=32):
    """A thick drip of goo running down (alpha only)."""
    def f(x, y):
        if (x - 7.5) ** 2 / 49 + (y - 7) ** 2 / 36 <= 1:
            return 1
        for cx, bot in ((4, 22), (8, 30), (12, 18)):
            if abs(x - cx) <= 1.6 and y <= bot:
                return 1
            if (x - cx) ** 2 + (y - bot) ** 2 <= 5:
                return 1
        return 0
    return _alpha(w, h, f)


def bubble(n=16):
    """A bubble: ring with a shine (alpha only)."""
    c = (n - 1) / 2

    def f(x, y):
        r = ((x - c) ** 2 + (y - c) ** 2) ** .5
        shine = 1 if (x - 5) ** 2 + (y - 5) ** 2 <= 2 else 0
        return max(shine, 1 - abs(r - 5.8) / 1.4, .25 if r < 5.8 else 0)
    return _alpha(n, n, f)


def trash_lid(size=64):
    """A dented galvanised trash-can lid held up as a shield, handle in the middle."""
    import math
    im, d, S = _big(size)
    OUT = (20, 25, 30, 255)
    c = S / 2
    d.ellipse([S * .03, S * .03, S * .97, S * .97], fill=(170, 178, 188, 255), outline=OUT, width=8)
    for r in (.4, .3, .2):                                                                           # ridges
        d.ellipse([c - S * r, c - S * r, c + S * r, c + S * r], outline=(120, 128, 140, 255), width=6)
        d.arc([c - S * r, c - S * r, c + S * r, c + S * r], 200, 290, fill=(235, 240, 248, 255), width=4)
    d.ellipse([S * .62, S * .58, S * .82, S * .76], fill=(135, 142, 155, 255))                       # the dent
    d.arc([S * .62, S * .58, S * .82, S * .76], 180, 300, fill=(80, 85, 95, 255), width=5)
    d.rounded_rectangle([c - S * .2, c - S * .06, c + S * .2, c + S * .06], 18, fill=(95, 100, 110, 255),
                        outline=OUT, width=6)                                                        # handle
    d.line([(S * .17, S * .26), (S * .3, S * .14)], fill=(255, 255, 255, 255), width=10)             # glare
    for k in range(6):                                                                               # rivets
        a = k * math.pi / 3
        x, y = c + S * .44 * math.cos(a), c + S * .44 * math.sin(a)
        d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(220, 225, 232, 255))
    return _shrink(im, size)


def ping(n=16):
    """A deflection ping: a sharp 8-point star (alpha only)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        r, a = math.hypot(x - c, y - c), math.atan2(y - c, x - c)
        spike = 2 + 5.5 * abs(math.cos(a * 2)) ** 6
        return 1.3 - r / spike
    return _alpha(n, n, f)


def folding_chair(size=64):
    """A grey steel folding chair - wrestling's finest weapon."""
    im, d, S = _big(size)
    OUT, STEEL, STEEL_L, STEEL_D = (15, 15, 20, 255), (150, 155, 165, 255), (220, 225, 235, 255), (90, 95, 105, 255)
    for a, b in (((.3, .06), (.26, .96)), ((.74, .5), (.8, .96))):                                   # legs
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=OUT, width=22)
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=STEEL_D, width=11)
    d.line([(S * .5, S * .56), (S * .2, S * .96)], fill=OUT, width=18)                               # cross brace
    d.line([(S * .5, S * .56), (S * .2, S * .96)], fill=STEEL, width=8)
    d.rounded_rectangle([S * .18, S * .04, S * .54, S * .34], 14, fill=STEEL, outline=OUT, width=7)  # backrest
    d.line([(S * .25, S * .11), (S * .47, S * .11)], fill=STEEL_L, width=8)
    d.polygon([(S * .2, S * .48), (S * .86, S * .43), (S * .9, S * .56), (S * .22, S * .61)], fill=STEEL,
              outline=OUT)                                                                           # seat
    d.line([(S * .24, S * .5), (S * .84, S * .46)], fill=STEEL_L, width=7)
    d.line([(S * .2, S * .48), (S * .86, S * .43), (S * .9, S * .56), (S * .22, S * .61), (S * .2, S * .48)],
           fill=OUT, width=6)
    return _shrink(im, size)


def impact_burst(size=64):
    """A jagged white-hot impact flash with red-orange edges (no text)."""
    import math
    im, d, S = _big(size)
    c = S / 2
    for scale, col in ((1.0, (220, 40, 30, 255)), (.78, (255, 150, 30, 255)), (.55, (255, 240, 120, 255)),
                       (.3, (255, 255, 255, 255))):
        pts = []
        for k in range(24):
            a = k * math.pi / 12
            r = S * .49 * scale * (1 if k % 2 == 0 else .55 + .1 * math.sin(k * 3))
            pts.append((c + r * math.cos(a), c + r * math.sin(a)))
        d.polygon(pts, fill=col)
    return _shrink(im, size)


def star5(n=16):
    """A five-point star (alpha only): seeing stars."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        r, a = math.hypot(x - c, y - c), math.atan2(y - c, x - c) + math.pi / 2
        edge = 3.2 + 4 * abs(math.cos(a * 2.5)) ** 3
        return 1.2 - r / edge
    return _alpha(n, n, f)


def big_taser(size=64, flip=False):
    """A comically huge yellow taser, XL on the side, the cartridge glowing blue, pointing right (left if flip,
    with the XL still reading the right way)."""
    im, d, S = _big(size)
    OUT = (15, 15, 15, 255)
    Y, YL, YD = (250, 215, 30, 255), (255, 245, 150, 255), (190, 145, 10, 255)
    d.polygon([(S * .1, S * .52), (S * .32, S * .52), (S * .28, S * .94), (S * .06, S * .94)], fill=(35, 35, 40, 255),
              outline=OUT)                                                                           # grip
    d.line([(S * .1, S * .52), (S * .32, S * .52), (S * .28, S * .94), (S * .06, S * .94), (S * .1, S * .52)],
           fill=OUT, width=6)
    d.line([(S * .34, S * .54), (S * .42, S * .72), (S * .3, S * .72)], fill=OUT, width=7)           # trigger guard
    d.rounded_rectangle([S * .04, S * .22, S * .72, S * .54], 16, fill=Y, outline=OUT, width=7)
    d.line([(S * .08, S * .28), (S * .68, S * .28)], fill=YL, width=8)
    d.line([(S * .08, S * .5), (S * .68, S * .5)], fill=YD, width=6)
    d.rectangle([S * .72, S * .18, S * .92, S * .58], fill=(35, 35, 40, 255), outline=OUT, width=7)   # cartridge
    d.rectangle([S * .9, S * .24, S * .97, S * .52], fill=(120, 210, 255, 255), outline=OUT, width=5)
    d.ellipse([S * .76, S * .26, S * .86, S * .5], fill=(70, 160, 255, 255))
    im = _shrink(im, size)
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    _big_text(im, "XL", (size - 23 if flip else 23, 26), (225, 30, 30, 255))
    return im


def zigzag(n=16):
    """A short jagged bolt fragment (alpha only)."""
    pts = [(2, 1), (9, 6), (6, 8), (13, 14)]
    return _alpha(n, n, lambda x, y: 1.5 - min(_seg_dist((x, y), a, b) for a, b in zip(pts, pts[1:])) / 1.2)


def mega_bolt(size=64):
    """A giant lightning bolt striking straight down: thick, jagged, yellow with a white core."""
    im, d, S = _big(size)
    pts = [(S * .62, 0), (S * .28, S * .44), (S * .5, S * .46), (S * .22, S * .99), (S * .78, S * .36),
           (S * .55, S * .35), (S * .84, 0)]
    d.polygon(pts, fill=(255, 225, 40, 255))
    d.line([(S * .7, S * .03), (S * .42, S * .4), (S * .6, S * .41), (S * .34, S * .84)], fill=(255, 255, 230, 255),
           width=14)
    d.line(pts + [pts[0]], fill=(60, 30, 0, 255), width=7)
    return _shrink(im, size)


def side_eye(size=64):
    """The eyes emoji: two big white eyeballs, pupils hard to the right (turned 180 they look left)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    for cx in (.3, .7):
        d.ellipse([S * (cx - .19), S * .2, S * (cx + .19), S * .8], fill=(255, 255, 255, 255), outline=OUT, width=10)
        d.ellipse([S * (cx + .02), S * .38, S * (cx + .17), S * .62], fill=(25, 25, 30, 255))                # pupil
        d.ellipse([S * (cx + .06), S * .41, S * (cx + .11), S * .48], fill=(255, 255, 255, 255))            # shine
        d.arc([S * (cx - .15), S * .26, S * (cx + .1), S * .74], 120, 220, fill=(200, 210, 225, 255), width=8)
    return _shrink(im, size)


def clocked_circle(size=64):
    """The thumbnail treatment: a sloppy hand-drawn red circle, a fat red arrow pointing into it."""
    import math
    im, d, S = _big(size)
    RED, W = (235, 20, 20, 255), (255, 255, 255, 255)
    c, r = (S * .58, S * .58), S * .36
    pts = []
    for k in range(70):                                          # a bit more than one lap, wobbling
        a = -2.2 + k * (2 * math.pi + .5) / 69
        rr = r * (1 + .05 * math.sin(k * .35)) * (1 + .03 * k / 69)
        pts.append((c[0] + rr * math.cos(a), c[1] + rr * .92 * math.sin(a)))
    d.line(pts, fill=W, width=22, joint="curve")
    d.line(pts, fill=RED, width=12, joint="curve")
    shaft = [(S * .03, S * .03), (S * .2, S * .2)]               # the arrow, from the top-left corner
    head = [(S * .3, S * .3), (S * .11, S * .27), (S * .27, S * .11)]
    d.line(shaft, fill=W, width=30)
    d.polygon(head, fill=W, outline=W, width=10)
    d.line(shaft, fill=RED, width=16)
    d.polygon(head, fill=RED)
    return _shrink(im, size)


# ------------------------------------------------------------------ set 6: Belt Whip, Shiv, Twerk On Em, Tax,
#                                                                     Silly String, Spit

def belt_swing(size=64):
    """A leather belt held at the TEXTURE CENTRE, the strap whipping out to the right, the big gold buckle at
    the far end (rotating the particle swings it like the bat)."""
    import math
    im, d, S = _big(size)
    c = S / 2
    OUT, LEATHER, LEATHER_L = (35, 18, 8, 255), (120, 65, 30, 255), (175, 110, 60, 255)
    pts = [(c + t * S * .3, c + math.sin(t * 5.2) * S * .05 * t) for t in [k / 30 for k in range(31)]]
    d.line(pts, fill=OUT, width=48, joint="curve")                                                   # the strap
    d.line(pts, fill=LEATHER, width=34, joint="curve")
    d.line([(x, y - 9) for x, y in pts], fill=LEATHER_L, width=7)
    for x, y in pts[3:-2:3]:                                                                         # stitching
        d.line([(x - 4, y + 10), (x + 4, y + 10)], fill=(230, 200, 140, 255), width=4)
    for x, y in pts[6:16:4]:                                                                         # holes
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=OUT)
    bx, by = pts[-1]
    GOLD, GOLD_L, GOLD_D = (255, 205, 40, 255), (255, 245, 170, 255), (180, 120, 10, 255)
    d.rounded_rectangle([bx - 6, by - 52, bx + 48, by + 52], 18, fill=GOLD, outline=OUT, width=9)    # buckle
    d.rounded_rectangle([bx + 6, by - 38, bx + 36, by + 38], 10, fill=GOLD_D)
    d.line([(bx + 4, by - 42), (bx + 38, by - 42)], fill=GOLD_L, width=7)
    d.ellipse([c - 24, c - 24, c + 24, c + 24], fill=(240, 195, 150, 255), outline=OUT, width=7)    # the fist
    return _shrink(im, size)


def whip_snap(n=16):
    """A whip-crack: a sharp crescent with sparks flying off it (alpha only)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        r, a = math.hypot(x - c, y - c), math.atan2(y - c, x - c)
        arc = 1 - abs(r - 5.5) / 1.1 if -2.4 < a < .8 else 0
        tick = 1 if 1.4 < a % 1.05 < 1.6 and 2 < r < 7.5 else 0
        return max(arc, tick * .9)
    return _alpha(n, n, f)


def belt_welt(size=64):
    """A raised red welt across them, the buckle's '$' printed right in it."""
    im, d, S = _big(size)
    OUT, RED, PINK = (90, 10, 15, 255), (230, 50, 55, 255), (255, 140, 140, 255)
    d.rounded_rectangle([S * .04, S * .38, S * .96, S * .62], 50, fill=RED, outline=OUT, width=10)
    d.line([(S * .1, S * .44), (S * .9, S * .44)], fill=PINK, width=10)
    d.rounded_rectangle([S * .34, S * .26, S * .66, S * .74], 22, fill=(200, 25, 35, 255), outline=OUT, width=10)
    im = _shrink(im, size)
    _big_text(im, "$", (32, 32), (255, 220, 220, 255))
    return im.rotate(-14, resample=Image.BICUBIC)


def shiv(size=64):
    """A jailhouse toothbrush shiv pointing right: taped handle, filed-down point dipped in green."""
    im, d, S = _big(size)
    OUT = (20, 25, 20, 255)
    d.polygon([(S * .42, S * .42), (S * .97, S * .5), (S * .42, S * .58)], fill=(205, 225, 240, 255), outline=OUT)
    d.line([(S * .42, S * .42), (S * .97, S * .5), (S * .42, S * .58), (S * .42, S * .42)], fill=OUT, width=7)
    d.line([(S * .46, S * .46), (S * .9, S * .5)], fill=(255, 255, 255, 255), width=5)               # filed edge
    d.rounded_rectangle([S * .03, S * .38, S * .46, S * .62], 20, fill=(70, 150, 230, 255), outline=OUT, width=7)
    for k in range(5):                                                                               # tape wraps
        x = S * (.08 + k * .075)
        d.line([(x, S * .38), (x + S * .03, S * .62)], fill=(230, 230, 220, 255), width=10)
    TOX = (110, 235, 60, 255)
    d.polygon([(S * .66, S * .45), (S * .9, S * .5), (S * .66, S * .55)], fill=TOX)                  # dipped
    return _shrink(im, size)


def skull(n=16):
    """A little skull (alpha only, tinted toxic green): eye holes and teeth cut out."""
    def f(x, y):
        head = (x - 7.5) ** 2 / 36 + (y - 6.5) ** 2 / 30 <= 1
        jaw = 4 <= x <= 11 and 9 <= y <= 14
        eyes = (x - 5) ** 2 + (y - 7) ** 2 <= 2.6 or (x - 10) ** 2 + (y - 7) ** 2 <= 2.6
        teeth = y >= 12 and x in (6, 9)
        return 1 if (head or jaw) and not eyes and not teeth else 0
    return _alpha(n, n, f)


def wiggle_lines(n=16):
    """Two curved motion lines, ")" ")", bowing right (alpha only): something shaking fast. Turned 180 they bow left."""
    import math

    def f(x, y):
        v = 0
        for cx in (2.5, 7.5):
            r = math.hypot(x - cx, y - 7.5)
            if x >= cx - .5 and abs(y - 7.5) < 6.5:
                v = max(v, 1.4 - abs(r - 5.5) / .9)
        return v
    return _alpha(n, n, f)


def cracked_shield(size=64):
    """A blue DEF shield cracked through, a fat red arrow pointing down beside it."""
    im, d, S = _big(size)
    OUT = (15, 20, 40, 255)
    sh = [(S * .06, S * .14), (S * .34, S * .04), (S * .62, S * .14), (S * .58, S * .62), (S * .34, S * .9),
          (S * .1, S * .62)]
    d.polygon(sh, fill=(80, 150, 255, 255))
    d.polygon([(x * .7 + S * .1, y * .7 + S * .08) for x, y in sh], fill=(150, 200, 255, 255))
    d.line(sh + [sh[0]], fill=OUT, width=10)
    d.line([(S * .3, S * .05), (S * .38, S * .3), (S * .26, S * .46), (S * .4, S * .66), (S * .32, S * .88)],
           fill=OUT, width=12)                                                                       # the crack
    RED = (235, 30, 35, 255)
    arrow = [(S * .72, S * .18), (S * .88, S * .18), (S * .88, S * .62), (S * .98, S * .62), (S * .8, S * .92),
             (S * .62, S * .62), (S * .72, S * .62)]
    d.polygon(arrow, fill=RED)
    d.line(arrow + [arrow[0]], fill=(80, 0, 0, 255), width=9)
    im = _shrink(im, size)
    _big_text(im, "DEF", (22, 30), (255, 255, 255, 255), scale=1)
    return im


def rubber_stamp(size=64):
    """A big office rubber stamp coming down: wooden knob, red rubber, IRS on the side."""
    im, d, S = _big(size)
    OUT = (30, 15, 10, 255)
    WOOD, WOOD_L = (170, 105, 50, 255), (220, 160, 95, 255)
    d.ellipse([S * .3, S * .02, S * .7, S * .3], fill=WOOD, outline=OUT, width=9)                     # knob
    d.ellipse([S * .37, S * .06, S * .5, S * .14], fill=WOOD_L)
    d.rectangle([S * .43, S * .26, S * .57, S * .52], fill=WOOD, outline=OUT, width=8)               # neck
    d.rounded_rectangle([S * .06, S * .5, S * .94, S * .78], 14, fill=(60, 60, 70, 255), outline=OUT, width=9)
    d.rectangle([S * .1, S * .78, S * .9, S * .94], fill=(220, 30, 35, 255), outline=OUT, width=8)   # rubber
    im = _shrink(im, size)
    _big_text(im, "IRS", (32, 41), (255, 255, 255, 255))
    return im


def taxed_mark(size=64):
    """Red ink: TAXED in a worn double box."""
    import random
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    RED = (225, 25, 30, 255)
    d.rectangle([1, 17, 62, 46], outline=RED, width=3)
    d.rectangle([5, 21, 58, 42], outline=RED, width=1)
    rnd = random.Random(5)
    px = im.load()
    for _ in range(70):                                                                              # worn ink
        x, y = rnd.randrange(size), rnd.randrange(16, 48)
        if px[x, y][0] > 150 and px[x, y][3]:
            px[x, y] = (0, 0, 0, 0)
    _big_text(im, "TAXED", (32, 32), RED, scale=2, font=SMALL)                                     # (straight and
    return im                                                                                        #  unworn: legible)


def coin(n=16):
    """A coin (alpha only, tinted gold): solid disc, its rim and a '$' stamped lighter."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        r = math.hypot(x - c, y - c)
        if r > 6.6:
            return 0
        if abs(r - 5.3) < .7:
            return .55
        s = (abs(x - c) < .6 and 2 < y < 13) or (abs(y - 4.5) < .7 and 5.5 < x < 10) or \
            (abs(y - 7.5) < .7 and 5.5 < x < 10) or (abs(y - 10.5) < .7 and 5.5 < x < 10) or \
            (abs(x - 5.5) < .7 and 4 < y < 8) or (abs(x - 9.5) < .7 and 7 < y < 11)
        return .5 if s else 1
    return _alpha(n, n, f)


def money_bag(size=64):
    """A fat sack of money tied at the top, '$' on the front."""
    im, d, S = _big(size)
    OUT = (40, 30, 10, 255)
    SACK, SACK_L, SACK_D = (130, 175, 80, 255), (185, 220, 130, 255), (85, 120, 50, 255)
    d.ellipse([S * .08, S * .3, S * .92, S * .97], fill=SACK, outline=OUT, width=9)
    d.ellipse([S * .2, S * .4, S * .5, S * .62], fill=SACK_L)
    d.arc([S * .12, S * .5, S * .88, S * .95], 20, 160, fill=SACK_D, width=10)
    d.polygon([(S * .3, S * .06), (S * .7, S * .06), (S * .58, S * .3), (S * .42, S * .3)], fill=SACK, outline=OUT)
    d.line([(S * .3, S * .06), (S * .42, S * .3)], fill=OUT, width=8)
    d.line([(S * .7, S * .06), (S * .58, S * .3)], fill=OUT, width=8)
    d.rounded_rectangle([S * .34, S * .26, S * .66, S * .34], 8, fill=(200, 40, 40, 255), outline=OUT, width=5)
    im = _shrink(im, size)
    _big_text(im, "$", (32, 42), (255, 220, 40, 255), scale=3)
    return im


def silly_can(size=64):
    """An upright neon-pink can of silly string, lime spray cap, the nozzle straight up."""
    im, d, S = _big(size)
    OUT = (25, 15, 30, 255)
    d.rounded_rectangle([S * .24, S * .22, S * .76, S * .97], 26, fill=(255, 60, 170, 255), outline=OUT, width=9)
    d.line([(S * .32, S * .3), (S * .32, S * .9)], fill=(255, 170, 220, 255), width=12)              # shine
    d.rounded_rectangle([S * .3, S * .08, S * .7, S * .26], 14, fill=(150, 255, 60, 255), outline=OUT, width=8)
    d.rectangle([S * .44, S * .0, S * .56, S * .1], fill=(150, 255, 60, 255), outline=OUT, width=6)  # nozzle
    d.rectangle([S * .24, S * .44, S * .76, S * .74], fill=(255, 240, 60, 255), outline=OUT, width=7)
    im = _shrink(im, size)
    _big_text(im, "SILLY", (32, 33), (230, 30, 140, 255), scale=1)
    _big_text(im, "STRING", (32, 42), (40, 120, 230, 255), scale=1)
    return im


def squiggle(n=16):
    """A curly scrap of string (alpha only, tinted neon)."""
    import math
    pts = [(1 + t * 13, 7.5 + math.sin(t * 13) * 4 * (1 - abs(t - .5))) for t in [k / 20 for k in range(21)]]
    return _alpha(n, n, lambda x, y: 1.5 - min(_seg_dist((x, y), a, b) for a, b in zip(pts, pts[1:])) / 1.1)


def string_tangle(size=64):
    """A big mess of neon silly string draped over them: pink, lime, yellow, cyan loops."""
    import math
    import random
    im, d, S = _big(size)
    rnd = random.Random(11)
    cols = [(255, 60, 170, 255), (150, 255, 60, 255), (255, 235, 50, 255), (60, 220, 255, 255)]
    for k in range(13):
        col = cols[k % 4]
        x0, y0 = rnd.uniform(.15, .85) * S, rnd.uniform(.1, .5) * S
        a0, r = rnd.uniform(0, math.pi * 2), rnd.uniform(.05, .1) * S
        pts = []
        for j in range(40):
            t = j / 39
            pts.append((x0 + (t - .5) * S * .6 * math.cos(a0) + r * math.cos(t * 14),
                        y0 + t * S * .45 + r * math.sin(t * 14)))
        pts = [(min(S - 12, max(12, x)), min(S - 12, max(12, y))) for x, y in pts]
        d.line(pts, fill=(30, 15, 35, 255), width=17, joint="curve")
        d.line(pts, fill=col, width=9, joint="curve")
    return _shrink(im, size)


def loogie(size=32):
    """A big glob of spit mid-air: frothy pale green, bubbles, a shine, a little tail."""
    im, d, S = _big(size)
    OUT = (40, 70, 40, 255)
    GOB, GOB_L = (205, 240, 175, 255), (245, 255, 235, 255)
    d.polygon([(S * .12, S * .62), (S * .5, S * .34), (S * .5, S * .78)], fill=GOB)                 # the tail
    d.ellipse([S * .3, S * .2, S * .94, S * .84], fill=GOB, outline=OUT, width=6)
    d.line([(S * .12, S * .62), (S * .4, S * .38)], fill=OUT, width=5)
    d.line([(S * .12, S * .62), (S * .4, S * .76)], fill=OUT, width=5)
    for x, y, r in ((.55, .62, .07), (.74, .66, .05), (.46, .44, .05)):                             # bubbles
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], outline=(130, 185, 120, 255), width=4)
    d.ellipse([S * .62, S * .3, S * .8, S * .44], fill=GOB_L)
    return _shrink(im, size)


def spit_splat(size=64):
    """A big wet splat of spit: frothy, bubbly, running."""
    import math
    im, d, S = _big(size)
    OUT = (45, 75, 40, 255)
    GOB = (205, 240, 175, 255)
    c = S / 2
    pts = []
    for k in range(18):
        a = k * math.pi * 2 / 18
        r = S * (.36 if k % 2 == 0 else .25 + .05 * math.sin(k * 2.3))
        pts.append((c + r * math.cos(a), c * .9 + r * .85 * math.sin(a)))
    runs = ((.3, .72), (.52, .86), (.7, .7))
    for x, y in runs:
        d.line([(S * x, S * .5), (S * x, S * y)], fill=OUT, width=26)
    d.polygon(pts, fill=GOB, outline=OUT)
    d.line(pts + [pts[0]], fill=OUT, width=9)
    for x, y in runs:                                                                                # running down
        d.line([(S * x, S * .5), (S * x, S * y)], fill=GOB, width=14)
        d.ellipse([S * x - 12, S * y - 6, S * x + 12, S * y + 14], fill=GOB, outline=OUT, width=5)
    for x, y, r in ((.4, .36, .07), (.6, .5, .09), (.56, .3, .04), (.34, .54, .05)):                 # froth
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], fill=(240, 255, 230, 255),
                  outline=(140, 190, 125, 255), width=5)
    return _shrink(im, size)


def gob_drip(n=16):
    """A stringy drip hanging off them (alpha only): a long thread ending in a fat drop."""
    def f(x, y):
        if abs(x - 7.5) < 1.1 and y < 10:
            return 1
        return 1 if (x - 7.5) ** 2 + (y - 11) ** 2 / 1.5 <= 9 else 0
    return _alpha(n, n, f)


# ------------------------------------------------------------------ set 7: Lace Up, Go Out Loud, Roll Out,
#                                                                     Lock In, Dome Check, Pickpocket

def sneaker(size=64):
    """A fresh high-top sneaker, side view, toe to the right: white leather, red swoosh-free panels, fat laces."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    WHITE, GREY, RED, RED_D = (250, 250, 250, 255), (205, 210, 220, 255), (225, 35, 45, 255), (150, 20, 30, 255)
    d.rounded_rectangle([S * .04, S * .74, S * .97, S * .9], 20, fill=WHITE, outline=OUT, width=9)    # sole
    d.line([(S * .07, S * .84), (S * .94, S * .84)], fill=GREY, width=8)
    upper = [(S * .1, S * .76), (S * .1, S * .18), (S * .38, S * .12), (S * .48, S * .4), (S * .74, S * .5),
             (S * .94, S * .62), (S * .95, S * .76)]
    d.polygon(upper, fill=WHITE)
    d.polygon([(S * .1, S * .2), (S * .36, S * .14), (S * .38, S * .4), (S * .1, S * .48)], fill=RED)   # collar
    d.polygon([(S * .6, S * .46), (S * .74, S * .5), (S * .94, S * .62), (S * .95, S * .76), (S * .6, S * .76)],
              fill=RED)                                                                                 # toe cap
    d.polygon([(S * .1, S * .56), (S * .36, S * .54), (S * .3, S * .76), (S * .1, S * .76)], fill=RED_D)  # heel
    d.line(upper + [upper[0]], fill=OUT, width=9)
    for k in range(4):                                                                               # laces
        x, y = S * (.4 + k * .065), S * (.2 + k * .075)
        d.line([(x - 22, y + 4), (x + 22, y - 4)], fill=OUT, width=12)
        d.line([(x - 18, y + 3), (x + 18, y - 3)], fill=(255, 230, 60, 255), width=6)
    d.line([(S * .16, S * .26), (S * .16, S * .4)], fill=(255, 140, 150, 255), width=8)                # shine
    return _shrink(im, size)


def speed_lines(n=16):
    """Three horizontal speed streaks of different lengths (alpha only)."""
    def f(x, y):
        for row, x0, x1 in ((3, 1, 14), (8, 4, 15), (12, 0, 10)):
            if abs(y - row) < 1 and x0 <= x <= x1:
                return .5 + .5 * (x - x0) / (x1 - x0)
        return 0
    return _alpha(n, n, f)


def fireworks_crate(size=64):
    """A wooden crate stuffed with fat fireworks rockets, one long fuse curling out the top."""
    im, d, S = _big(size)
    OUT = (30, 15, 10, 255)
    for x, top, col in ((.2, .12, (225, 40, 50, 255)), (.36, .04, (60, 120, 240, 255)), (.52, .14, (255, 205, 40, 255)),
                        (.68, .08, (90, 210, 80, 255))):                                             # rockets
        d.rectangle([S * x, S * top + 30, S * (x + .13), S * .6], fill=col, outline=OUT, width=7)
        d.polygon([(S * x, S * top + 32), (S * (x + .065), S * top), (S * (x + .13), S * top + 32)], fill=col,
                  outline=OUT)
        d.line([(S * x, S * top + 32), (S * (x + .065), S * top), (S * (x + .13), S * top + 32)], fill=OUT, width=7)
        d.line([(S * (x + .03), S * top + 50), (S * (x + .03), S * .58)], fill=(255, 255, 255, 120), width=6)
    WOOD, WOOD_D = (190, 130, 70, 255), (130, 85, 40, 255)
    d.rectangle([S * .06, S * .5, S * .94, S * .97], fill=WOOD, outline=OUT, width=9)                 # crate
    for y in (.66, .82):
        d.line([(S * .08, S * y), (S * .92, S * y)], fill=WOOD_D, width=6)
    d.line([(S * .1, S * .54), (S * .9, S * .93)], fill=WOOD_D, width=10)
    d.arc([S * .76, S * .02, S * 1.0, S * .3], 160, 300, fill=OUT, width=10)                          # fuse
    im = _shrink(im, size)
    _big_text(im, "BOOM", (32, 48), (255, 230, 60, 255), scale=1)
    return im


def twinkle(n=16):
    """A 4-ray firework twinkle with a hot core (alpha only)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = abs(x - c), abs(y - c)
        r = math.hypot(dx, dy)
        ray = max(1 - dx / 1.1, 0) * (1 - dy / 8) + max(1 - dy / 1.1, 0) * (1 - dx / 8)
        return max(ray, 1.3 - r / 2.5)
    return _alpha(n, n, f)


def firework_burst(size=64):
    """A full firework shell bursting: rings of coloured sparks shooting out from a white-hot centre."""
    import math
    im, d, S = _big(size)
    c = S / 2
    cols = [(255, 60, 90, 255), (255, 210, 50, 255), (80, 200, 255, 255), (150, 255, 90, 255), (220, 110, 255, 255)]
    for k in range(20):
        a = k * math.pi / 10
        col = cols[k % 5]
        x0, y0 = c + S * .1 * math.cos(a), c + S * .1 * math.sin(a)
        x1, y1 = c + S * .42 * math.cos(a), c + S * .42 * math.sin(a)
        d.line([(x0, y0), (x1, y1)], fill=col, width=10)
        d.ellipse([x1 - 13, y1 - 13, x1 + 13, y1 + 13], fill=(255, 255, 255, 255), outline=col, width=6)
    for k in range(10):
        a = k * math.pi / 5 + .3
        x, y = c + S * .26 * math.cos(a), c + S * .26 * math.sin(a)
        d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=cols[(k + 2) % 5])
    d.ellipse([c - S * .1, c - S * .1, c + S * .1, c + S * .1], fill=(255, 255, 230, 255))
    return _shrink(im, size)


def shopping_cart(size=64, left=False):
    """A shopping cart rolling right (left=True: mirrored, rolling left): wire basket, handle at the back."""
    im, d, S = _big(size)
    OUT, STEEL, STEEL_L = (20, 25, 35, 255), (175, 185, 200, 255), (235, 240, 248, 255)
    basket = [(S * .14, S * .22), (S * .96, S * .26), (S * .84, S * .66), (S * .24, S * .66)]
    d.polygon(basket, fill=(175, 185, 200, 90))
    for k in range(1, 7):                                                                            # the wires
        t = k / 7
        d.line([(S * (.14 + .82 * t), S * (.22 + .04 * t)), (S * (.24 + .6 * t), S * .66)], fill=STEEL, width=6)
    for k in range(1, 4):
        t = k / 4
        d.line([(S * (.14 + .1 * t), S * (.22 + .44 * t)), (S * (.96 - .12 * t), S * (.26 + .4 * t))], fill=STEEL,
               width=6)
    d.line(basket + [basket[0]], fill=OUT, width=10)
    d.line(basket[:2], fill=STEEL_L, width=4)
    d.line([(S * .14, S * .22), (S * .04, S * .12)], fill=OUT, width=12)                               # handle
    d.rounded_rectangle([S * .0, S * .06, S * .1, S * .16], 8, fill=(220, 40, 40, 255), outline=OUT, width=6)
    d.line([(S * .24, S * .66), (S * .2, S * .8), (S * .9, S * .8), (S * .84, S * .66)], fill=OUT, width=10)
    for x in (.24, .82):                                                                             # wheels
        d.ellipse([S * (x - .07), S * .78, S * (x + .07), S * .92], fill=(40, 40, 45, 255), outline=OUT, width=6)
        d.ellipse([S * (x - .025), S * .83, S * (x + .025), S * .87], fill=STEEL_L)
    im = _shrink(im, size)
    return im.transpose(Image.FLIP_LEFT_RIGHT) if left else im


def headphones(size=64):
    """Big over-ear studio headphones (seen from the front): red cups, black band, a glowing ring on each cup."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.arc([S * .14, S * .06, S * .86, S * .86], 180, 360, fill=OUT, width=40)                         # band
    d.arc([S * .14, S * .06, S * .86, S * .86], 180, 360, fill=(60, 60, 70, 255), width=22)
    d.arc([S * .2, S * .1, S * .8, S * .82], 205, 250, fill=(140, 140, 155, 255), width=8)
    for x in (.04, .7):                                                                              # the cups
        d.rounded_rectangle([S * x, S * .4, S * (x + .26), S * .9], 30, fill=(225, 30, 40, 255), outline=OUT,
                            width=9)
        d.rounded_rectangle([S * (x + .05), S * .46, S * (x + .21), S * .84], 20, fill=(150, 15, 25, 255))
        d.ellipse([S * (x + .07), S * .56, S * (x + .19), S * .74], outline=(255, 230, 80, 255), width=8)
    return _shrink(im, size)


def focus_mote(n=16):
    """A small sharp diamond of light (alpha only): focus being pulled in."""
    c = (n - 1) / 2
    return _alpha(n, n, lambda x, y: 1.4 - (abs(x - c) / 3 + abs(y - c) / 6))


def dome_bump(size=64):
    """A big cartoon bump swelling up on their head: a pink lump with a shine and throb lines."""
    import math
    im, d, S = _big(size)
    OUT = (90, 20, 30, 255)
    d.pieslice([S * .22, S * .3, S * .78, S * 1.14], 180, 360, fill=(255, 120, 140, 255), outline=OUT, width=10)
    d.line([(S * .2, S * .72), (S * .8, S * .72)], fill=OUT, width=10)
    d.ellipse([S * .34, S * .4, S * .48, S * .52], fill=(255, 220, 230, 255))
    for a in (-150, -115, -65, -30):                                                                 # throbbing
        r0, r1 = S * .34, S * .46
        x0, y0 = S * .5 + r0 * math.cos(math.radians(a)), S * .72 + r0 * math.sin(math.radians(a))
        x1, y1 = S * .5 + r1 * math.cos(math.radians(a)), S * .72 + r1 * math.sin(math.radians(a))
        d.line([(x0, y0), (x1, y1)], fill=(255, 240, 80, 255), width=12)
    return _shrink(im, size)


def grab_hand(size=64):
    """A sneaky hand reaching down out of a hoodie sleeve, fingers spread (dipping into a pocket)."""
    im, d, S = _big(size)
    OUT, SKIN, SLEEVE = (60, 30, 20, 255), (240, 190, 145, 255), (70, 70, 85, 255)
    d.rectangle([S * .3, S * .0, S * .7, S * .3], fill=SLEEVE, outline=(20, 20, 25, 255), width=8)      # sleeve
    d.rectangle([S * .28, S * .26, S * .72, S * .36], fill=(50, 50, 62, 255), outline=(20, 20, 25, 255), width=7)
    d.rounded_rectangle([S * .3, S * .32, S * .7, S * .66], 30, fill=SKIN, outline=OUT, width=8)       # palm
    for x, bot in ((.3, .9), (.42, .97), (.54, .95), (.64, .86)):                                    # fingers
        d.rounded_rectangle([S * x, S * .56, S * (x + .1), S * bot], 18, fill=SKIN, outline=OUT, width=7)
    d.rounded_rectangle([S * .16, S * .4, S * .32, S * .6], 18, fill=SKIN, outline=OUT, width=7)       # thumb
    return _shrink(im, size)


def hand_wallet(size=64):
    """The same hand coming back up, fist clutching a fat brown wallet with cash sticking out."""
    im, d, S = _big(size)
    OUT, SKIN, SLEEVE = (60, 30, 20, 255), (240, 190, 145, 255), (70, 70, 85, 255)
    d.rectangle([S * .3, S * .0, S * .7, S * .3], fill=SLEEVE, outline=(20, 20, 25, 255), width=8)
    d.rectangle([S * .28, S * .26, S * .72, S * .36], fill=(50, 50, 62, 255), outline=(20, 20, 25, 255), width=7)
    d.polygon([(S * .32, S * .64), (S * .5, S * .5), (S * .74, S * .74), (S * .56, S * .9)], fill=(120, 220, 110, 255),
              outline=(30, 80, 30, 255))                                                             # cash
    d.rounded_rectangle([S * .14, S * .56, S * .86, S * .94], 16, fill=(120, 70, 35, 255), outline=(40, 20, 10, 255),
                        width=9)                                                                     # wallet
    d.line([(S * .18, S * .7), (S * .82, S * .7)], fill=(170, 110, 60, 255), width=6)
    d.rounded_rectangle([S * .3, S * .32, S * .7, S * .66], 30, fill=SKIN, outline=OUT, width=8)       # fist
    for k in range(3):
        x = S * (.36 + k * .11)
        d.line([(x, S * .5), (x, S * .64)], fill=OUT, width=6)
    return _shrink(im, size)


# ------------------------------------------------------------------ set 8: Pool Float, Block Off, Cheap Shot,
#                                                                     Jam the Gun, Sleeper (cigar), Reload

def pool_float(size=64):
    """A pink frosted-donut pool float with sprinkles, seen a little from above (they sit in the hole)."""
    import math
    import random
    im, d, S = _big(size)
    OUT = (90, 30, 60, 255)
    d.ellipse([S * .02, S * .3, S * .98, S * .86], fill=(235, 190, 130, 255), outline=OUT, width=9)   # dough
    d.ellipse([S * .04, S * .28, S * .96, S * .78], fill=(255, 120, 190, 255), outline=OUT, width=8)  # frosting
    for k in range(9):                                                                               # drips
        a = math.pi * (.1 + .8 * k / 8)
        x, y = S * .5 + S * .44 * math.cos(a), S * .53 + S * .23 * math.sin(a)
        d.ellipse([x - 12, y - 6, x + 12, y + 22], fill=(255, 120, 190, 255))
    d.ellipse([S * .3, S * .44, S * .7, S * .62], fill=(60, 160, 230, 255), outline=OUT, width=8)     # the hole
    d.arc([S * .1, S * .32, S * .6, S * .58], 190, 250, fill=(255, 210, 235, 255), width=10)          # shine
    rnd = random.Random(3)
    cols = [(255, 255, 255, 255), (90, 210, 255, 255), (255, 230, 60, 255), (130, 230, 90, 255)]
    for k in range(26):                                                                              # sprinkles
        a, r = rnd.uniform(0, 2 * math.pi), rnd.uniform(.28, .43)
        x, y = S * .5 + S * r * math.cos(a), S * .53 + S * r * .55 * math.sin(a)
        if abs(x - S * .5) < S * .22 and abs(y - S * .53) < S * .1:
            continue
        t = rnd.uniform(0, math.pi)
        d.line([(x - 7 * math.cos(t), y - 7 * math.sin(t)), (x + 7 * math.cos(t), y + 7 * math.sin(t))],
               fill=cols[k % 4], width=6)
    return _shrink(im, size)


def ripple(n=16):
    """A flat water ripple: a thin ellipse ring (alpha only)."""
    c = (n - 1) / 2
    return _alpha(n, n, lambda x, y: 1 - abs((((x - c) / 7) ** 2 + ((y - c) / 3.2) ** 2) ** .5 - .85) / .13)


def caution_tape(size=64):
    """A strip of yellow CAUTION tape running straight across (rotate the particle to angle it)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 22, 63, 41], fill=(255, 220, 30, 255), outline=(30, 25, 10, 255))
    for x in range(-8, 64, 10):                                                                      # hazard edges
        d.line([(x, 41), (x + 3, 38)], fill=(30, 25, 10, 255), width=2)
        d.line([(x, 25), (x + 3, 22)], fill=(30, 25, 10, 255), width=2)
    _outlined_text(d, (32 - _text_w(d, "CAUTION") // 2, 26), "CAUTION", (25, 20, 10, 255), outline=(255, 220, 30, 255))
    return im


def barricade(size=64):
    """An orange-and-white striped road barricade on two legs, ROAD CLOSED."""
    im, d, S = _big(size)
    OUT = (30, 20, 15, 255)
    for x in (.14, .8):                                                                              # legs
        d.rectangle([S * x, S * .4, S * (x + .06), S * .98], fill=(200, 200, 205, 255), outline=OUT, width=6)
        d.rectangle([S * (x - .06), S * .92, S * (x + .12), S * .98], fill=(60, 60, 65, 255))
    for y in (.16, .5):                                                                              # boards
        d.rectangle([S * .02, S * y, S * .98, S * (y + .2)], fill=(255, 255, 255, 255), outline=OUT, width=7)
        for k in range(-1, 8):
            x = S * (.02 + k * .14)
            d.polygon([(x, S * (y + .2)), (x + S * .07, S * (y + .2)), (x + S * .14, S * y), (x + S * .07, S * y)],
                      fill=(255, 120, 20, 255))
        d.rectangle([S * .02, S * y, S * .98, S * (y + .2)], outline=OUT, width=7)
    im = _shrink(im, size)
    d = ImageDraw.Draw(im)
    for text, y in (("ROAD", 17), ("CLOSED", 39)):
        w = _text_w(d, text)
        d.rectangle([32 - w // 2 - 2, y - 5, 32 + w // 2 + 1, y + 5], fill=(255, 255, 255, 255))
        _outlined_text(d, (32 - w // 2, y - 3), text, (220, 20, 20, 255), outline=(255, 255, 255, 255))
    return im


def look_bubble(size=64):
    """A shouty speech bubble: YO LOOK!! (they point the foe somewhere else)."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.ellipse([S * .03, S * .06, S * .97, S * .74], fill=(255, 250, 200, 255), outline=OUT, width=8)
    d.polygon([(S * .38, S * .68), (S * .28, S * .97), (S * .56, S * .7)], fill=(255, 250, 200, 255))
    d.line([(S * .38, S * .71), (S * .28, S * .97), (S * .56, S * .72)], fill=OUT, width=8)
    im = _shrink(im, size)
    _big_text(im, "YO", (32, 20), (40, 90, 230, 255))
    _big_text(im, "LOOK!!", (32, 35), (230, 30, 30, 255))
    return im


def fist_front(size=64):
    """A fist coming straight at you: four knuckles, thumb across, a little wrist band."""
    im, d, S = _big(size)
    OUT, SKIN, SKIN_D = (70, 35, 20, 255), (240, 190, 145, 255), (210, 150, 110, 255)
    d.rounded_rectangle([S * .12, S * .14, S * .88, S * .86], 60, fill=SKIN, outline=OUT, width=10)
    for k in range(4):                                                                               # knuckles
        x = S * (.16 + k * .18)
        d.rounded_rectangle([x, S * .16, x + S * .17, S * .46], 26, fill=SKIN, outline=OUT, width=8)
        d.ellipse([x + S * .05, S * .2, x + S * .11, S * .26], fill=(255, 230, 205, 255))
    d.rounded_rectangle([S * .14, S * .5, S * .72, S * .66], 26, fill=SKIN_D, outline=OUT, width=8)  # thumb
    d.rectangle([S * .24, S * .86, S * .76, S * .98], fill=(230, 40, 40, 255), outline=OUT, width=7)
    return _shrink(im, size)


def pistol_up(size=64):
    """A black pistol held barrel-up (side view, so it reads both ways), slide stuck half open."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    BODY, BODY_L = (55, 55, 62, 255), (120, 120, 135, 255)
    d.rectangle([S * .4, S * .04, S * .62, S * .58], fill=BODY, outline=OUT, width=8)                 # slide
    d.line([(S * .45, S * .08), (S * .45, S * .54)], fill=BODY_L, width=7)
    for k in range(5):                                                                               # serrations
        d.line([(S * .5, S * (.38 + k * .035)), (S * .6, S * (.38 + k * .035))], fill=OUT, width=4)
    d.rectangle([S * .36, S * .16, S * .4, S * .3], fill=(255, 205, 60, 255), outline=OUT, width=4)  # stuck casing
    d.polygon([(S * .4, S * .56), (S * .62, S * .56), (S * .7, S * .96), (S * .48, S * .96)], fill=(40, 40, 45, 255),
              outline=OUT)                                                                           # grip
    d.line([(S * .4, S * .56), (S * .62, S * .56), (S * .7, S * .96), (S * .48, S * .96), (S * .4, S * .56)],
           fill=OUT, width=8)
    d.arc([S * .22, S * .5, S * .44, S * .74], 90, 270, fill=OUT, width=9)                            # guard
    d.line([(S * .38, S * .58), (S * .32, S * .64)], fill=OUT, width=8)                               # trigger
    return _shrink(im, size)


def sputter(n=16):
    """A dud's sad little sputter: three small puffs in a row (alpha only)."""
    return _alpha(n, n, lambda x, y: max(1.3 - ((x - cx) ** 2 + (y - cy) ** 2) ** .5 / r
                                         for cx, cy, r in ((4, 11, 3), (8, 7, 3.4), (12, 3.5, 2.6))))


def cigar(size=64):
    """A fat lit cigar lying across, chewed end on the left (in their mouth), red-and-gold band, glowing ash end
    on the right. Turned 180 it points the other way and still reads (it's symmetric top to bottom)."""
    im, d, S = _big(size)
    OUT = (35, 18, 8, 255)
    d.rounded_rectangle([S * .04, S * .4, S * .84, S * .6], 40, fill=(140, 80, 40, 255), outline=OUT, width=9)
    d.line([(S * .1, S * .45), (S * .8, S * .45)], fill=(185, 120, 65, 255), width=7)                 # sheen
    for x in (.3, .48, .64):                                                                         # leaf seams
        d.line([(S * x, S * .42), (S * (x + .06), S * .58)], fill=(105, 58, 28, 255), width=5)
    d.rectangle([S * .14, S * .4, S * .24, S * .6], fill=(200, 30, 40, 255), outline=OUT, width=6)   # band
    d.rectangle([S * .17, S * .45, S * .21, S * .55], fill=(255, 210, 60, 255))
    d.rounded_rectangle([S * .78, S * .4, S * .9, S * .6], 14, fill=(170, 170, 165, 255), outline=OUT, width=7)  # ash
    d.rounded_rectangle([S * .88, S * .42, S * .97, S * .58], 14, fill=(255, 90, 20, 255), outline=OUT, width=6)
    d.ellipse([S * .9, S * .46, S * .95, S * .54], fill=(255, 230, 120, 255))                        # ember
    return _shrink(im, size)


def smoke_ring(n=16):
    """A blown smoke ring: a thick soft wobbly O (alpha only)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        r, a = math.hypot((x - c) / 1.1, y - c), math.atan2(y - c, x - c)
        return 1.2 - abs(r - 4.6 - .5 * math.sin(a * 3)) / 1.8
    return _alpha(n, n, f)


def zee(n=16):
    """A fat letter Z (alpha only): snoring."""
    def f(x, y):
        if 2 <= y <= 4 and 3 <= x <= 12:
            return 1
        if 11 <= y <= 13 and 3 <= x <= 12:
            return 1
        return 1 if 4 < y < 11 and abs(x - (12 - (y - 4) * 9 / 7)) < 1.6 else 0
    return _alpha(n, n, f)


def magazine(size=64):
    """A fat pistol magazine standing up, brass rounds showing at the top lips."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    for k, y in enumerate((.04, .1)):                                                                # rounds
        x = S * (.4 + .04 * k)
        d.rounded_rectangle([x, S * y, x + S * .22, S * (y + .14)], 20, fill=(255, 205, 70, 255), outline=OUT,
                            width=6)
        d.rectangle([x, S * (y + .1), x + S * .22, S * (y + .14)], fill=(200, 140, 40, 255))
    d.polygon([(S * .34, S * .18), (S * .66, S * .18), (S * .7, S * .88), (S * .3, S * .88)], fill=(50, 50, 58, 255))
    d.line([(S * .34, S * .18), (S * .66, S * .18), (S * .7, S * .88), (S * .3, S * .88), (S * .34, S * .18)],
           fill=OUT, width=8)
    d.line([(S * .4, S * .24), (S * .38, S * .82)], fill=(130, 130, 145, 255), width=7)
    for k in range(4):                                                                               # witness holes
        d.ellipse([S * .55, S * (.3 + k * .13), S * .61, S * (.36 + k * .13)], fill=(255, 205, 70, 255))
    d.rounded_rectangle([S * .24, S * .86, S * .76, S * .97], 10, fill=(35, 35, 40, 255), outline=OUT, width=7)
    return _shrink(im, size)


def plus_cross(n=16):
    """A soft healing plus sign (alpha only)."""
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = abs(x - c), abs(y - c)
        return 1.0 if (dx <= 1.6 and dy <= 5.5) or (dy <= 1.6 and dx <= 5.5) else 0
    return _alpha(n, n, f)


# ------------------------------------------------------------------ effect animations (status, items, stats)

def henny_bottle(size=64):
    """A squat Hennessy-style cognac bottle: amber glass, black-and-gold label, gold cap."""
    im, d, S = _big(size)
    OUT = (20, 10, 6, 255)
    AMBER, AMBER_D, AMBER_L = (196, 104, 24, 255), (140, 64, 14, 255), (250, 180, 80, 255)
    d.rounded_rectangle([S * .4, S * .04, S * .6, S * .16], 14, fill=(230, 180, 50, 255), outline=OUT, width=7)  # cap
    d.rectangle([S * .43, S * .15, S * .57, S * .3], fill=AMBER_D, outline=OUT, width=7)                        # neck
    d.polygon([(S * .43, S * .28), (S * .57, S * .28), (S * .8, S * .44), (S * .2, S * .44)], fill=AMBER, outline=OUT)
    d.rounded_rectangle([S * .18, S * .4, S * .82, S * .96], 40, fill=AMBER, outline=OUT, width=8)               # body
    d.rounded_rectangle([S * .24, S * .46, S * .36, S * .9], 20, fill=AMBER_L)                                  # shine
    d.rectangle([S * .2, S * .56, S * .8, S * .82], fill=(25, 20, 18, 255), outline=(230, 180, 50, 255), width=6)
    _big_text(im, "VS", (S * .5, S * .69), (240, 200, 70, 255), scale=5)
    return _shrink(im, size)


def qmark(n=16):
    """A fat question mark (alpha only): confusion."""
    c = (n - 1) / 2

    def f(x, y):
        r = ((x - c) ** 2 + (y - 5) ** 2) ** .5
        if 2.4 <= r <= 5 and (y <= 5 or x >= c):
            return 1
        if c - 1.4 <= x <= c + 1.4 and 8 <= y <= 10.5:
            return 1
        return 1 if ((x - c) ** 2 + (y - 13.2) ** 2) ** .5 <= 1.7 else 0
    return _alpha(n, n, f)


def ice_glint(n=16):
    """A four-point diamond twinkle (alpha only): iced out."""
    c = (n - 1) / 2
    return _alpha(n, n, lambda x, y: 1.3 - (abs(x - c) ** .6 + abs(y - c) ** .6) / 2.6)


def spark_jag(n=16):
    """A jagged little lightning zig (alpha only): tased."""
    pts = [(10, 0), (5, 7), (9, 8), (4, 15)]

    def f(x, y):
        return max(1.2 - _seg_dist((x, y), a, b) / 1.5 for a, b in zip(pts, pts[1:]))
    return _alpha(n, n, f)


def fat_heart(n=16):
    """A plump heart (alpha only): crushin'."""
    def f(x, y):
        u, v = (x - 7.5) / 5.4, (6.5 - y) / 5.4
        return 1 if (u * u + v * v - 1) ** 3 - u * u * v ** 3 <= 0 else 0
    return _alpha(n, n, f)


def arrow(n=16, up=True):
    """A chunky arrow (alpha only): stats up / down."""
    def f(x, y):
        yy = y if up else n - 1 - y
        if yy <= 7:
            return 1 if abs(x - 7.5) <= yy + .5 else 0
        return 1 if abs(x - 7.5) <= 2.6 else 0
    return _alpha(n, n, f)


def amber_drip(n=16):
    """A teardrop (alpha only): a drop of Henny."""
    def f(x, y):
        if y >= 7:
            return 1.3 - ((x - 7.5) ** 2 + (y - 10) ** 2) ** .5 / 4.5
        return 1 if abs(x - 7.5) <= (y - 1) * .55 else 0
    return _alpha(n, n, f)


def snore_z(n=16):
    """A slanted italic z (alpha only): snoring."""
    def f(x, y):
        if 3 <= y <= 5 and 5 <= x <= 14:
            return 1
        if 11 <= y <= 13 and 1 <= x <= 10:
            return 1
        return 1 if 5 < y < 11 and abs(x - (13 - (y - 5) * 11 / 6)) < 1.5 else 0
    return _alpha(n, n, f)


def toxic_bubble(n=16):
    """A bubble with a bright rim and a highlight (alpha only): bad batch."""
    c = (n - 1) / 2

    def f(x, y):
        r = ((x - c) ** 2 + (y - c) ** 2) ** .5
        if ((x - c + 2.5) ** 2 + (y - c + 2.5) ** 2) ** .5 < 1.6:
            return 1
        return 1 if 5 <= r <= 7 else (.35 if r < 5 else 0)
    return _alpha(n, n, f)


def dogpile(size=64):
    """The Whole Gang landing on somebody: three hoodies piled up, the top one still diving in."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    for angle, (x, y), cap, up in ((90, (0, 30), False, False), (-30, (22, 18), True, True),
                                   (60, (12, 0), False, True)):
        fig, d, S = _big(34)
        _hoodie(d, S, cap=cap, arms_up=up)
        fig = _shrink(fig, 34).rotate(angle, resample=Image.BICUBIC, expand=True)
        fig = fig.crop((0, 0, min(fig.width, size - x), min(fig.height, size - y)))
        im.alpha_composite(fig, (x, y))
    return im


def dollar(n=16):
    """A fat dollar sign (alpha only): money raining on a glow-up."""
    def f(x, y):
        if 6.5 <= x <= 8.5 and 0 <= y <= 15:                       # the bar through it
            return 1
        r = ((x - 7.5) ** 2 + ((y - 4.6) * 1.15) ** 2) ** .5          # top bowl, open bottom-right
        top = 2.2 <= r <= 4.6 and not (x > 8 and 4.6 < y < 7)
        r = ((x - 7.5) ** 2 + ((y - 10.4) * 1.15) ** 2) ** .5         # bottom bowl, open top-left
        bot = 2.2 <= r <= 4.6 and not (x < 7 and 8 < y < 10.4)
        return 1 if top or bot else 0
    return _alpha(n, n, f)


def thank_you_bag(size=64):
    """The corner-store plastic bag: white, handles tied up top, red THANK YOU and a smiley on the front."""
    im, d, S = _big(size)
    OUT, WHITE, SHADE, RED = (20, 20, 24, 255), (246, 246, 246, 255), (200, 200, 210, 255), (220, 30, 40, 255)
    d.polygon([(S * .2, S * .3), (S * .8, S * .3), (S * .86, S * .96), (S * .14, S * .96)], fill=WHITE, outline=OUT)
    d.line([(S * .2, S * .3), (S * .8, S * .3), (S * .86, S * .96), (S * .14, S * .96), (S * .2, S * .3)],
           fill=OUT, width=8)
    for x0 in (.22, .58):                                     # the handles, tied up in a knot
        d.arc([S * x0, S * .04, S * (x0 + .2), S * .4], 180, 360, fill=OUT, width=14)
        d.arc([S * x0, S * .04, S * (x0 + .2), S * .4], 180, 360, fill=WHITE, width=7)
    d.ellipse([S * .44, S * .14, S * .56, S * .26], fill=WHITE, outline=OUT, width=6)
    d.polygon([(S * .66, S * .36), (S * .8, S * .36), (S * .83, S * .9), (S * .72, S * .9)], fill=SHADE)  # wrinkles
    d.line([(S * .3, S * .4), (S * .27, S * .9)], fill=SHADE, width=6)
    d.ellipse([S * .4, S * .74, S * .6, S * .94], outline=RED, width=7)    # the smiley
    d.arc([S * .44, S * .78, S * .56, S * .9], 20, 160, fill=RED, width=6)
    d.ellipse([S * .45, S * .79, S * .48, S * .82], fill=RED)
    d.ellipse([S * .52, S * .79, S * .55, S * .82], fill=RED)
    im = _shrink(im, size)
    d = ImageDraw.Draw(im)                                    # the text at full size: crisp, not shrunk
    for k, word in enumerate(("THANK", "YOU")):
        _outlined_text(d, (size // 2 - _text_w(d, word) // 2, size * 34 // 64 + k * 10 - 4), word, RED,
                       outline=WHITE)
    return im


# ---- set 9 -------------------------------------------------------------------------------------------------
SMALL.update({                                                # cuss-out symbols (grawlix)
    "#": ".#.#.|#####|.#.#.|#####|.#.#.|.....", "@": ".###.|#...#|#.###|#.#.#|#.##.|.####",
    "%": "##..#|##.#.|..#..|.#...|#.##.|#..##", "&": ".##..|#..#.|.##..|#.#.#|#..#.|.##.#",
})


def tumbleweed(size=64):
    """A dry tumbleweed: a scraggly ball of tangled brown twigs (nothing happened here)."""
    import math
    import random
    im, d, S = _big(size)
    rnd = random.Random(7)
    c, R = S / 2, S * .4
    d.ellipse([c - R, c - R, c + R, c + R], fill=(150, 105, 55, 90))
    for k in range(70):                                       # twigs looping all over
        a0 = rnd.uniform(0, math.tau)
        r0, r1 = R * rnd.uniform(.1, 1), R * rnd.uniform(.3, 1)
        a1 = a0 + rnd.uniform(1.2, 2.6)
        col = rnd.choice([(95, 60, 25, 255), (150, 100, 45, 255), (190, 140, 75, 255), (120, 80, 35, 255)])
        d.line([(c + r0 * math.cos(a0), c + r0 * math.sin(a0)), (c + r1 * math.cos(a1), c + r1 * math.sin(a1))],
               fill=col, width=7)
    d.ellipse([c - R, c - R, c + R, c + R], outline=(70, 45, 20, 255), width=8)
    return _shrink(im, size)


def scorecard(size=64):
    """A judge's scorecard on a stick: 0/10."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (20, 20, 25, 255)
    d.rectangle([29, 34, 34, 63], fill=(170, 115, 60, 255), outline=OUT)                    # the stick
    d.rectangle([4, 6, 59, 38], fill=(255, 255, 255, 255), outline=OUT, width=2)
    d.rectangle([6, 8, 57, 12], fill=(230, 40, 40, 255))
    _big_text(im, "O/1O", (32, 25), (230, 30, 30, 255))             # (round Os: the 0 glyph has a slash)
    return im


def windmill_arms(size=64):
    """Two arms windmilling through the middle (a propeller of hoodie sleeves with fists on the ends): spin it."""
    im, d, S = _big(size)
    OUT, SLEEVE, SLEEVE_L = (20, 15, 15, 255), (60, 60, 75, 255), (110, 110, 130, 255)
    SKIN, SKIN_D = (240, 190, 145, 255), (200, 140, 100, 255)
    for sx in (1, -1):
        x0, x1, y1 = S / 2, S / 2 + sx * S * .32, S / 2 - sx * S * .04
        d.line([(x0, S / 2), (x1, y1)], fill=OUT, width=int(S * .2))
        d.line([(x0, S / 2), (x1, y1)], fill=SLEEVE, width=int(S * .16))
        d.line([(x0, S / 2 - S * .03), (x1, y1 - S * .03)], fill=SLEEVE_L, width=int(S * .03))
        fx = S / 2 + sx * S * .34
        d.ellipse([fx - S * .15, y1 - S * .15, fx + S * .15, y1 + S * .15], fill=SKIN, outline=OUT, width=9)
        for k in range(3):                                                                           # knuckles
            y = y1 + S * (k - 1) * .06
            d.line([(fx + sx * S * .03, y), (fx + sx * S * .13, y)], fill=SKIN_D, width=8)
    d.ellipse([S * .42, S * .42, S * .58, S * .58], fill=SLEEVE, outline=OUT, width=8)            # the shoulder
    for r in (.47, .495):                                                                            # motion arcs
        box = [S * (.5 - r), S * (.5 - r), S * (.5 + r), S * (.5 + r)]
        d.arc(box, 200, 250, fill=(255, 255, 255, 220), width=6)
        d.arc(box, 20, 70, fill=(255, 255, 255, 220), width=6)
    return _shrink(im, size)


def smack_star(n=16):
    """A chunky 4-point impact star (alpha only)."""
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = abs(x - c), abs(y - c)
        return 1 if (dx * .35 + dy <= 2.2) or (dy * .35 + dx <= 2.2) or (dx + dy <= 4.2) else 0
    return _alpha(n, n, f)


def money_gun(size=64):
    """A neon-green money gun pointing right, a fat wad of bills loaded in the top."""
    im, d, S = _big(size)
    OUT, BODY, BODY_L = (15, 25, 15, 255), (60, 220, 90, 255), (170, 255, 170, 255)
    GREEN, GREEN_D = (150, 200, 120, 255), (80, 150, 70, 255)
    for k in range(4):                                                                               # the wad
        y = S * (.16 + k * .055)
        d.rectangle([S * .2, y, S * .68, y + S * .1], fill=GREEN if k % 2 else GREEN_D, outline=OUT, width=5)
    d.ellipse([S * .38, S * .2, S * .5, S * .28], outline=(230, 255, 220, 255), width=5)
    d.rounded_rectangle([S * .12, S * .38, S * .9, S * .6], 24, fill=BODY, outline=OUT, width=9)  # the body
    d.rectangle([S * .86, S * .42, S * .97, S * .56], fill=(40, 40, 45, 255), outline=OUT, width=7)   # the slot
    d.line([(S * .9, S * .49), (S * .97, S * .49)], fill=GREEN, width=6)
    d.polygon([(S * .18, S * .56), (S * .4, S * .56), (S * .34, S * .94), (S * .12, S * .94)], fill=BODY)  # grip
    d.line([(S * .18, S * .56), (S * .12, S * .94), (S * .34, S * .94), (S * .4, S * .56)], fill=OUT, width=9)
    d.arc([S * .36, S * .5, S * .56, S * .76], 0, 180, fill=OUT, width=8)                         # trigger guard
    d.line([(S * .2, S * .42), (S * .82, S * .42)], fill=BODY_L, width=6)
    return _shrink(im, size)


def bill_flutter(n=16):
    """A dollar bill seen flat (alpha only): border, a darker portrait oval in the middle."""
    def f(x, y):
        if not (1 <= x <= 14 and 4 <= y <= 11):
            return 0
        if x in (1, 14) or y in (4, 11):
            return 1
        r = ((x - 7.5) / 2.6) ** 2 + ((y - 7.5) / 2.2) ** 2
        return .55 if r < 1 else .8
    return _alpha(n, n, f)


CASH_FONT = dict(SMALL, **{"$": "..#..|.####|#.#..|.###.|..#.#|####."})   # (SMALL's $ reads as a 3 in prices)


def novelty_check(size=64):
    """A giant novelty check: PAY, $1000000, signed (44 texels wide: shown at 2:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT, INK, PAPER = (20, 40, 25, 255), (25, 70, 30, 255), (215, 245, 210, 255)
    d.rectangle([10, 20, 53, 43], fill=PAPER, outline=OUT)
    d.rectangle([11, 21, 52, 22], fill=(70, 160, 80, 255))
    _outlined_text(d, (13, 24), "PAY", INK, outline=PAPER)
    d.line([(28, 29), (51, 29)], fill=INK)
    d.rectangle([11, 31, 52, 40], fill=(255, 255, 255, 255), outline=OUT)
    m = _text_mask("$1000000", CASH_FONT)
    im.paste((20, 130, 45, 255), (32 - m.width // 2, 33), m)
    d.line([(36, 42), (39, 41), (42, 42), (45, 41), (49, 42)], fill=(30, 30, 140, 255))     # signed
    return im


def cash_twinkle(n=16):
    """A 4-point twinkle with a ring (alpha only): cha-ching."""
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = abs(x - c), abs(y - c)
        r = (dx * dx + dy * dy) ** .5
        if (dx < .8 and dy < 7.5) or (dy < .8 and dx < 7.5) or dx + dy < 2.5:
            return 1
        return .7 if 4.2 < r < 5.2 else 0
    return _alpha(n, n, f)


def body_bag(size=64):
    """A black zip-up body bag standing up, zipper down the middle, a toe tag: DOA (shown at 2:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (5, 5, 8, 255)
    d.rounded_rectangle([17, 4, 46, 58], 10, fill=(40, 40, 48, 255), outline=OUT)
    d.rounded_rectangle([19, 7, 25, 55], 3, fill=(72, 72, 84, 255))                                # sheen
    d.line([(32, 8), (32, 54)], fill=(150, 150, 160, 255))                                         # zipper
    for y in range(9, 54, 2):
        d.point((31, y), fill=(110, 110, 120, 255))
        d.point((33, y + 1), fill=(110, 110, 120, 255))
    d.rectangle([30, 6, 34, 10], fill=(200, 200, 210, 255), outline=OUT)                           # pull tab
    d.line([(44, 50), (48, 52)], fill=(230, 230, 230, 255))                                         # the string
    d.rectangle([47, 49, 63, 59], fill=(250, 240, 200, 255), outline=OUT)                          # toe tag
    _outlined_text(d, (49, 52), "DOA", (200, 20, 20, 255), outline=(250, 240, 200, 255))
    return im


def slam_dust(n=16):
    """A low, wide lumpy dust cloud (alpha only)."""
    def f(x, y):
        v = 0
        for cx, cy, r in ((4, 10, 3.6), (8, 9, 4.6), (12, 10, 3.6), (6, 12, 3), (10, 12, 3)):
            v = max(v, 1.3 - ((x - cx) ** 2 + (y - cy) ** 2) ** .5 / r)
        return v
    return _alpha(n, n, f)


def street_hydrant(size=64):
    """A big chunky yellow street hydrant, its top bonnet blown clean off (the open main, water about to blow)."""
    im, d, S = _big(size)
    OUT, Y, YL, YD = (40, 25, 5, 255), (255, 205, 30, 255), (255, 240, 140, 255), (200, 140, 10, 255)
    d.rounded_rectangle([S * .28, S * .3, S * .72, S * .9], 26, fill=Y, outline=OUT, width=10)    # barrel
    d.rectangle([S * .58, S * .34, S * .68, S * .86], fill=YD)
    d.rectangle([S * .33, S * .34, S * .4, S * .86], fill=YL)
    d.rounded_rectangle([S * .22, S * .22, S * .78, S * .34], 14, fill=Y, outline=OUT, width=10)  # top flange
    d.ellipse([S * .36, S * .16, S * .64, S * .28], fill=(40, 70, 130, 255), outline=OUT, width=9)  # open main
    d.ellipse([S * .42, S * .18, S * .58, S * .24], fill=(140, 200, 255, 255))
    for x0 in (.1, .72):                                                                             # side nozzles
        d.rounded_rectangle([S * x0, S * .46, S * (x0 + .18), S * .62], 10, fill=Y, outline=OUT, width=9)
        d.ellipse([S * (x0 + .04), S * .49, S * (x0 + .14), S * .59], fill=YD, outline=OUT, width=6)
    d.line([(S * .2, S * .62), (S * .3, S * .72)], fill=(90, 90, 100, 255), width=7)                # the chain
    d.rounded_rectangle([S * .18, S * .86, S * .82, S * .97], 10, fill=YD, outline=OUT, width=9)  # base
    for x in (.26, .5, .74):                                                                         # bolts
        d.ellipse([S * (x - .03), S * .89, S * (x + .03), S * .94], fill=YL)
    return _shrink(im, size)


def hydrant_bonnet(size=32):
    """The hydrant's yellow top bonnet, blown off: a dome with the pentagon nut."""
    im, d, S = _big(size)
    OUT, Y, YL, YD = (40, 25, 5, 255), (255, 205, 30, 255), (255, 240, 140, 255), (200, 140, 10, 255)
    d.pieslice([S * .1, S * .3, S * .9, S * 1.1], 180, 360, fill=Y, outline=OUT, width=8)
    d.rectangle([S * .06, S * .66, S * .94, S * .82], fill=YD, outline=OUT, width=8)
    d.rectangle([S * .38, S * .14, S * .62, S * .34], fill=YD, outline=OUT, width=7)              # the nut
    d.arc([S * .22, S * .42, S * .6, S * .8], 200, 260, fill=YL, width=8)
    return _shrink(im, size)


def gush_drop(n=16):
    """A long streaky water drop flying straight up (alpha only)."""
    def f(x, y):
        w = 2.6 - abs(y - 9) * .18 if y >= 3 else 0
        core = abs(x - 7.5) < w
        return (1 if abs(x - 7.5) < w * .5 else .7) if core and y <= 14 else 0
    return _alpha(n, n, f)


def water_column(w=16, h=32):
    """A chunk of a gushing water column (alpha only): soft edges, brighter streaks running up it."""
    def f(x, y):
        edge = 1.4 - abs(x - 7.5) / 5.5
        streak = .25 if int(x) in (5, 9) else 0
        fade = min(1, y / 6, (h - 1 - y) / 6)
        return max(0, min(1, edge * .8 + streak)) * fade
    return _alpha(w, h, f)


def splash_glob(n=16):
    """A fat teardrop of water with a highlight (alpha only)."""
    def f(x, y):
        r = (((x - 7.5) / 5) ** 2 + ((y - 8.5) / 6) ** 2) ** .5
        top = 1 <= y < 5 and abs(x - 7.5) < (y - 1) * 1.1           # the pointed tip
        if r < 1 or top:
            return .65 if ((x - 6) ** 2 + (y - 7) ** 2) < 2.3 else 1
        return 0
    return _alpha(n, n, f)


def pointing_hand(size=64):
    """A hand pointing right, index finger out (poke), a gold ring and a red sleeve cuff."""
    im, d, S = _big(size)
    OUT, SKIN, SKIN_D = (70, 35, 20, 255), (240, 190, 145, 255), (205, 145, 105, 255)
    d.rounded_rectangle([S * .48, S * .38, S * .97, S * .5], 40, fill=SKIN, outline=OUT, width=9)   # the finger
    d.line([(S * .9, S * .41), (S * .9, S * .47)], fill=(255, 225, 205, 255), width=8)              # nail
    d.rounded_rectangle([S * .22, S * .36, S * .62, S * .76], 40, fill=SKIN, outline=OUT, width=9)  # the fist
    for k in range(3):                                                                               # curled fingers
        y = S * (.5 + k * .085)
        d.rounded_rectangle([S * .42, y, S * .66, y + S * .09], 20, fill=SKIN, outline=OUT, width=7)
    d.rounded_rectangle([S * .3, S * .3, S * .56, S * .42], 20, fill=SKIN_D, outline=OUT, width=7)  # thumb
    d.rectangle([S * .55, S * .37, S * .6, S * .51], fill=(255, 205, 40, 255), outline=OUT, width=4)  # ring
    d.rectangle([S * .02, S * .34, S * .24, S * .78], fill=(220, 35, 40, 255), outline=OUT, width=9)  # cuff
    d.line([(S * .06, S * .4), (S * .06, S * .72)], fill=(255, 110, 110, 255), width=6)
    return _shrink(im, size)


def poke_lines(n=16):
    """Eight short dashes bursting out round a point (alpha only): boop."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = x - c, y - c
        r = (dx * dx + dy * dy) ** .5
        if not 3.5 <= r <= 7.5:
            return 0
        a = math.degrees(math.atan2(dy, dx)) % 45
        return 1 if min(a, 45 - a) < 7 else 0
    return _alpha(n, n, f)


def hop_ticks(n=16):
    """Two little bounce marks either side, like a cartoon landing (alpha only)."""
    def f(x, y):
        for sx in (-1, 1):
            t = (x - 7.5) * sx
            if 3 <= t <= 7 and abs((y - 11) + (t - 3) * .9) < .9:
                return 1
        return 0
    return _alpha(n, n, f)


def duct_tape_roll(size=64):
    """A roll of silver duct tape, seen face on: the hole, the layers, a loose end flapping."""
    im, d, S = _big(size)
    OUT, GREY, GREY_D, GREY_L = (20, 20, 25, 255), (170, 175, 185, 255), (120, 125, 135, 255), (225, 230, 240, 255)
    d.polygon([(S * .62, S * .82), (S * .9, S * .9), (S * .84, S * .98), (S * .56, S * .9)], fill=GREY, outline=OUT)
    d.ellipse([S * .1, S * .1, S * .9, S * .9], fill=GREY, outline=OUT, width=10)
    for r in (.34, .3, .26):
        d.ellipse([S * (.5 - r), S * (.5 - r), S * (.5 + r), S * (.5 + r)], outline=GREY_D, width=4)
    d.arc([S * .16, S * .16, S * .84, S * .84], 200, 260, fill=GREY_L, width=12)
    d.ellipse([S * .32, S * .32, S * .68, S * .68], fill=(210, 170, 110, 255), outline=OUT, width=9)   # cardboard
    d.ellipse([S * .39, S * .39, S * .61, S * .61], fill=(0, 0, 0, 0), outline=OUT, width=6)
    return _shrink(im, size)


def duct_strip(size=64):
    """A strip of silver duct tape running across, torn zig-zag ends, the cloth weave showing."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT, GREY, GREY_D, GREY_L = (20, 20, 25, 255), (175, 180, 190, 255), (130, 135, 145, 255), (230, 235, 245, 255)
    top, bot = 25, 38
    right = [(63 - (k % 2) * 3, top + k * (bot - top) / 6) for k in range(7)]
    left = [((k % 2) * 3, bot - k * (bot - top) / 6) for k in range(7)]
    d.polygon(right + left, fill=GREY, outline=OUT)
    for x in range(5, 60, 3):                                                                        # the weave
        d.line([(x, top + 2), (x, bot - 2)], fill=GREY_D)
    d.line([(4, top + 2), (59, top + 2)], fill=GREY_L)
    d.line([(4, bot - 1), (59, bot - 1)], fill=GREY_D)
    return im


def kevlar_vest(size=64):
    """A black tactical vest, shoulder straps, pouches, KEVLAR on the chest plate (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT, BLACK, BLACK_L = (5, 5, 8, 255), (38, 40, 46, 255), (70, 74, 84, 255)
    shape = [(10, 12), (22, 6), (27, 16), (37, 16), (42, 6), (54, 12), (56, 58), (8, 58)]
    d.polygon(shape, fill=BLACK)
    d.line(shape + [shape[0]], fill=OUT, width=2)
    d.line([(14, 14), (12, 54)], fill=BLACK_L, width=2)
    d.rectangle([12, 22, 52, 34], fill=(240, 240, 240, 255), outline=OUT)                          # the plate label
    _outlined_text(d, (32 - _text_w(d, "KEVLAR") // 2, 25), "KEVLAR", (20, 20, 25, 255), outline=(240, 240, 240, 255))
    for x in (12, 26, 40):                                                                           # pouches
        d.rectangle([x, 40, x + 11, 54], fill=(55, 58, 66, 255), outline=OUT)
        d.line([(x + 1, 43), (x + 10, 43)], fill=OUT)
        d.rectangle([x + 4, 44, x + 7, 46], fill=(120, 125, 135, 255))
    return im


def ricochet(n=16):
    """A sharp spark burst: thin rays of different lengths (alpha only)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = x - c, y - c
        r = (dx * dx + dy * dy) ** .5
        if r < 1.6:
            return 1
        a = math.degrees(math.atan2(dy, dx)) % 360
        for ang, ln in ((20, 7.5), (75, 5), (130, 7), (200, 5.5), (250, 7.5), (310, 5)):
            if abs((a - ang + 180) % 360 - 180) < 9 and r < ln:
                return 1
        return 0
    return _alpha(n, n, f)


def flat_slug(w=16, h=32):
    """A spent, mushroomed bullet (alpha only): a flattened head on a stubby base, mid-texture."""
    def f(x, y):
        y -= 10
        if 3 <= y <= 7 and abs(x - 7.5) <= 6 - abs(y - 5) * .8:
            return 1
        if 7 <= y <= 12 and 5 <= x <= 10:
            return .7
        return 0
    return _alpha(w, h, f)


def swear_jar(size=64):
    """A glass SWEAR JAR, a few coins in the bottom, a slot lid (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT, GLASS, GLASS_L = (20, 30, 40, 255), (170, 215, 235, 170), (240, 250, 255, 230)
    d.rounded_rectangle([12, 12, 51, 61], 8, fill=GLASS, outline=OUT, width=2)
    d.rectangle([16, 4, 47, 12], fill=(200, 160, 60, 255), outline=OUT)                            # the lid
    d.rectangle([26, 7, 37, 8], fill=OUT)                                                            # coin slot
    for x, y in ((18, 54), (26, 56), (34, 54), (42, 56), (22, 49), (31, 50), (39, 49)):            # coins
        d.ellipse([x - 4, y - 3, x + 4, y + 3], fill=(255, 205, 50, 255), outline=(150, 100, 20, 255))
    d.line([(16, 16), (16, 42)], fill=GLASS_L, width=2)
    d.rectangle([13, 21, 50, 40], fill=(255, 255, 255, 255), outline=OUT)                          # the label
    for k, word in enumerate(("SWEAR", "JAR")):
        _outlined_text(d, (32 - _text_w(d, word) // 2, 24 + k * 8), word, (210, 25, 30, 255),
                       outline=(255, 255, 255, 255))
    return im


def coin_disc(n=16):
    """A coin (alpha only): a fat disc with a brighter rim."""
    def f(x, y):
        r = (((x - 7.5) / 5.5) ** 2 + ((y - 7.5) / 5.5) ** 2) ** .5
        return 0 if r > 1 else (.75 if r < .6 else 1)
    return _alpha(n, n, f)


# ---- set 10 ------------------------------------------------------------------------------------------------
def fizz_drop(n=16):
    """A round droplet with a bright rim (alpha only): soda / water spray."""
    def f(x, y):
        r = (((x - 7.5) / 4.5) ** 2 + ((y - 7.5) / 4.5) ** 2) ** .5
        return 0 if r > 1 else (.65 if r < .55 else 1)
    return _alpha(n, n, f)


def air_horn(size=64):
    """A handheld air horn pointing right: red can, black trumpet, white button."""
    im, d, S = _big(size)
    OUT, RED, RED_L = (20, 10, 10, 255), (225, 35, 40, 255), (255, 120, 120, 255)
    d.rounded_rectangle([S * .06, S * .34, S * .44, S * .7], 18, fill=RED, outline=OUT, width=9)      # the can
    d.line([(S * .1, S * .42), (S * .4, S * .42)], fill=RED_L, width=6)
    d.rectangle([S * .14, S * .5, S * .36, S * .6], fill=(255, 255, 255, 255), outline=OUT, width=5)  # label
    d.rectangle([S * .42, S * .44, S * .56, S * .58], fill=(60, 60, 65, 255), outline=OUT, width=7)   # valve
    d.rounded_rectangle([S * .44, S * .26, S * .56, S * .36], 8, fill=(250, 250, 250, 255), outline=OUT, width=6)
    d.line([(S * .5, S * .36), (S * .5, S * .44)], fill=OUT, width=6)
    d.polygon([(S * .56, S * .46), (S * .82, S * .32), (S * .98, S * .26), (S * .98, S * .78), (S * .82, S * .7),
               (S * .56, S * .56)], fill=(35, 35, 40, 255), outline=OUT)                              # the trumpet
    d.line([(S * .97, S * .27), (S * .97, S * .77)], fill=(120, 120, 130, 255), width=8)
    return _shrink(im, size)


def blast_ring(n=16):
    """A thick ring (alpha only): a blast of sound pushing out."""
    c = (n - 1) / 2
    return _alpha(n, n, lambda x, y: 1 - abs(((x - c) ** 2 + (y - c) ** 2) ** .5 - 5.5) / 1.6)


def mud_pie(size=32):
    """A mud pie in its foil tin, seen from the side (lobbed)."""
    im, d, S = _big(size)
    OUT = (30, 15, 5, 255)
    d.polygon([(S * .06, S * .5), (S * .94, S * .5), (S * .82, S * .78), (S * .18, S * .78)], fill=(200, 200, 210, 255),
              outline=OUT)
    d.line([(S * .06, S * .5), (S * .94, S * .5), (S * .82, S * .78), (S * .18, S * .78), (S * .06, S * .5)], fill=OUT,
           width=6)
    for x in range(3, 9):                                                                              # crimps
        d.line([(S * x / 10, S * .54), (S * (x / 10 - .03), S * .74)], fill=(150, 150, 160, 255), width=4)
    d.chord([S * .08, S * .22, S * .92, S * .76], 180, 360, fill=(110, 70, 35, 255), outline=OUT, width=6)  # mud
    for x, y in ((.3, .36), (.55, .3), (.7, .42)):                                                     # lumps
        d.ellipse([S * (x - .07), S * (y - .05), S * (x + .07), S * (y + .05)], fill=(150, 100, 55, 255))
    return _shrink(im, size)


def mud_splat(size=64):
    """A big splat of mud with the foil tin stuck in it, crumbs flying (pied)."""
    import math
    import random
    im, d, S = _big(size)
    rnd = random.Random(4)
    OUT, MUD, MUD_L = (30, 15, 5, 255), (110, 70, 35, 255), (160, 110, 60, 255)
    pts = []
    for k in range(18):
        a = k * math.tau / 18
        r = S * (.3 + (.12 if k % 2 else 0) + rnd.uniform(0, .06))
        pts.append((S / 2 + r * math.cos(a), S / 2 + r * .8 * math.sin(a)))
    d.polygon(pts, fill=MUD, outline=OUT)
    d.line(pts + [pts[0]], fill=OUT, width=8)
    for _ in range(8):                                                                                 # lumps
        x, y = rnd.uniform(.3, .7) * S, rnd.uniform(.32, .66) * S
        d.ellipse([x - S * .05, y - S * .035, x + S * .05, y + S * .035], fill=MUD_L)
    d.ellipse([S * .36, S * .3, S * .64, S * .52], fill=(205, 205, 215, 255), outline=OUT, width=7)   # the tin
    d.ellipse([S * .42, S * .35, S * .58, S * .46], outline=(150, 150, 160, 255), width=5)
    return _shrink(im, size)


def mud_drip(n=16):
    """A drip of mud running down (alpha only)."""
    def f(x, y):
        if abs(x - 7.5) <= 1.6 and 1 <= y <= 9:
            return 1
        return 1 if ((x - 7.5) ** 2 + (y - 10.5) ** 2) < 7 else 0
    return _alpha(n, n, f)


def impact_ring(n=16):
    """A jagged impact ring (alpha only)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = x - c, y - c
        r = (dx * dx + dy * dy) ** .5
        a = math.atan2(dy, dx)
        rr = 5 + 1.6 * math.cos(a * 8)
        return 1 if abs(r - rr) < 1.1 else 0
    return _alpha(n, n, f)


def acid_glob(n=16):
    """A bubbly glob of acid (alpha only): a blob with two holes."""
    def f(x, y):
        r = (((x - 7.5) / 5.5) ** 2 + ((y - 8) / 4.8) ** 2) ** .5
        if r > 1:
            return 0
        for cx, cy in ((5.5, 7), (9.5, 9.5)):
            if (x - cx) ** 2 + (y - cy) ** 2 < 1.6:
                return .4
        return 1
    return _alpha(n, n, f)


def hose_nozzle(size=64):
    """A firefighter's brass hose nozzle pointing right, the fat red hose curling off behind it."""
    im, d, S = _big(size)
    OUT, RED, RED_L, BRASS, BRASS_L = (25, 10, 5, 255), (200, 30, 30, 255), (250, 110, 100, 255), (220, 170, 50, 255), (255, 230, 140, 255)
    d.arc([S * -.1, S * .4, S * .5, S * 1.1], 180, 300, fill=OUT, width=int(S * .2))                 # the hose
    d.arc([S * -.1, S * .4, S * .5, S * 1.1], 180, 300, fill=RED, width=int(S * .14))
    d.rounded_rectangle([S * .14, S * .4, S * .44, S * .6], 14, fill=RED, outline=OUT, width=9)
    d.line([(S * .18, S * .45), (S * .4, S * .45)], fill=RED_L, width=6)
    d.rectangle([S * .42, S * .38, S * .52, S * .62], fill=BRASS, outline=OUT, width=8)               # coupling
    d.polygon([(S * .52, S * .38), (S * .92, S * .44), (S * .92, S * .56), (S * .52, S * .62)], fill=BRASS)
    d.line([(S * .52, S * .38), (S * .92, S * .44), (S * .92, S * .56), (S * .52, S * .62)], fill=OUT, width=8)
    d.line([(S * .55, S * .43), (S * .88, S * .47)], fill=BRASS_L, width=6)
    d.rectangle([S * .58, S * .22, S * .66, S * .4], fill=(60, 60, 65, 255), outline=OUT, width=6)    # the bale
    d.line([(S * .62, S * .24), (S * .78, S * .4)], fill=OUT, width=8)
    return _shrink(im, size)


def alarm_clock(size=64):
    """A red twin-bell alarm clock: two bells, the hammer between, white face reading 6:00, little feet."""
    import math
    im, d, S = _big(size)
    OUT, RED, RED_L = (25, 8, 8, 255), (220, 35, 40, 255), (255, 120, 120, 255)
    for x in (.18, .62):                                                                               # the bells
        d.chord([S * x, S * .06, S * (x + .2), S * .3], 180, 360, fill=(230, 230, 235, 255), outline=OUT, width=8)
        d.line([(S * x, S * .18), (S * (x + .2), S * .18)], fill=OUT, width=8)
    d.line([(S * .5, S * .08), (S * .5, S * .2)], fill=OUT, width=8)                                  # the hammer
    d.ellipse([S * .44, S * .04, S * .56, S * .12], fill=(230, 230, 235, 255), outline=OUT, width=6)
    for x in (.24, .66):                                                                               # feet
        d.line([(S * (x + .05), S * .82), (S * x, S * .96)], fill=OUT, width=12)
    d.ellipse([S * .14, S * .16, S * .86, S * .88], fill=RED, outline=OUT, width=10)                  # the body
    d.arc([S * .2, S * .22, S * .8, S * .82], 200, 260, fill=RED_L, width=8)
    d.ellipse([S * .24, S * .26, S * .76, S * .78], fill=(255, 252, 235, 255), outline=OUT, width=8)  # the face
    for k in range(12):
        a = k * math.tau / 12
        d.ellipse([S * (.5 + .21 * math.cos(a)) - 5, S * (.52 + .21 * math.sin(a)) - 5,
                   S * (.5 + .21 * math.cos(a)) + 5, S * (.52 + .21 * math.sin(a)) + 5], fill=OUT)
    d.line([(S * .5, S * .52), (S * .5, S * .33)], fill=OUT, width=9)                                 # 6:00
    d.line([(S * .5, S * .52), (S * .5, S * .66)], fill=OUT, width=12)
    return _shrink(im, size)


def ring_lines(n=16):
    """Two little ringing wiggle marks either side (alpha only)."""
    def f(x, y):
        for sx in (-1, 1):
            t = 7.5 + sx * 5
            if abs(x - t) < .9 and 3 <= y <= 12 and (y % 4 < 2) == (sx > 0):
                return 1
            if abs(x - (t + sx)) < .9 and 3 <= y <= 12 and (y % 4 >= 2) == (sx > 0):
                return 1
        return 0
    return _alpha(n, n, f)


def chancla(size=64):
    """The chancla: a blue flip-flop sole-first, white thong strap, coming down."""
    im, d, S = _big(size)
    OUT, SOLE, SOLE_L = (10, 15, 40, 255), (40, 90, 220, 255), (120, 170, 255, 255)
    d.rounded_rectangle([S * .3, S * .04, S * .7, S * .96], 90, fill=SOLE, outline=OUT, width=10)
    d.rounded_rectangle([S * .35, S * .1, S * .65, S * .9], 70, outline=SOLE_L, width=7)
    d.line([(S * .5, S * .26), (S * .34, S * .54)], fill=OUT, width=18)                               # the strap
    d.line([(S * .5, S * .26), (S * .66, S * .54)], fill=OUT, width=18)
    d.line([(S * .5, S * .26), (S * .34, S * .54)], fill=(250, 250, 250, 255), width=10)
    d.line([(S * .5, S * .26), (S * .66, S * .54)], fill=(250, 250, 250, 255), width=10)
    d.ellipse([S * .46, S * .22, S * .54, S * .3], fill=(250, 250, 250, 255), outline=OUT, width=5)
    return _shrink(im, size)


def fly_bug(n=16):
    """A little housefly (alpha only): a body and two wings."""
    def f(x, y):
        if ((x - 7.5) / 2.2) ** 2 + ((y - 9) / 3) ** 2 < 1:
            return 1
        for sx in (-1, 1):
            if ((x - 7.5 - sx * 3.2) / 2.4) ** 2 + ((y - 6) / 1.8) ** 2 < 1:
                return .55
        return 0
    return _alpha(n, n, f)


def salt_shaker(size=64):
    """A big glass salt shaker: white salt inside, a silver cap with holes (no text: it gets tipped)."""
    im, d, S = _big(size)
    OUT, GLASS, SALT, METAL = (25, 30, 40, 255), (200, 225, 240, 255), (250, 250, 250, 255), (190, 195, 205, 255)
    d.rounded_rectangle([S * .26, S * .26, S * .74, S * .94], 24, fill=GLASS, outline=OUT, width=9)
    d.rounded_rectangle([S * .3, S * .44, S * .7, S * .9], 18, fill=SALT)
    for k in range(8):                                                                                 # grains
        d.point((S * (.34 + k * .045), S * (.5 + (k % 3) * .1)), fill=(210, 215, 225, 255))
    d.line([(S * .32, S * .32), (S * .32, S * .86)], fill=(255, 255, 255, 255), width=8)               # shine
    d.rounded_rectangle([S * .22, S * .1, S * .78, S * .3], 24, fill=METAL, outline=OUT, width=9)    # the cap
    for x in (.38, .5, .62):
        d.ellipse([S * (x - .025), S * .15, S * (x + .025), S * .2], fill=OUT)
    d.line([(S * .26, S * .26), (S * .74, S * .26)], fill=(130, 135, 145, 255), width=6)
    return _shrink(im, size)


def salt_grains(n=16):
    """A pinch of salt (alpha only): a few tiny square grains."""
    pts = {(3, 3), (8, 2), (12, 5), (5, 8), (10, 10), (2, 12), (13, 13), (7, 13)}

    def f(x, y):
        return 1 if any(abs(x - px) <= .6 and abs(y - py) <= .6 for px, py in pts) else 0
    return _alpha(n, n, f)


def slop_ball(size=32):
    """A glob of gutter slop: brown-green muck with a fish skeleton and a banana peel sticking out."""
    im, d, S = _big(size)
    OUT = (20, 20, 10, 255)
    d.ellipse([S * .1, S * .2, S * .9, S * .86], fill=(100, 105, 45, 255), outline=OUT, width=7)
    d.ellipse([S * .2, S * .3, S * .5, S * .5], fill=(140, 140, 70, 255))
    d.polygon([(S * .5, S * .26), (S * .74, S * .02), (S * .82, S * .1), (S * .62, S * .32)], fill=(250, 220, 60, 255),
              outline=OUT)                                                                              # banana peel
    d.line([(S * .3, S * .66), (S * .74, S * .6)], fill=(240, 240, 230, 255), width=5)                # fish bones
    for k in range(3):
        x = S * (.38 + k * .1)
        d.line([(x, S * .56), (x + S * .02, S * .72)], fill=(240, 240, 230, 255), width=4)
    return _shrink(im, size)


def stink_lines(n=16):
    """Three wavy stink lines rising (alpha only)."""
    import math

    def f(x, y):
        for cx in (3.5, 7.5, 11.5):
            if abs(x - (cx + 1.2 * math.sin(y / 2.2))) < .9 and 1 <= y <= 14:
                return 1
        return 0
    return _alpha(n, n, f)


def crackle(n=16):
    """A zig-zag electric crackle (alpha only)."""
    pts = [(1, 9), (5, 4), (7, 10), (10, 3), (12, 9), (15, 6)]

    def f(x, y):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            dx, dy = x1 - x0, y1 - y0
            t = max(0, min(1, ((x - x0) * dx + (y - y0) * dy) / (dx * dx + dy * dy)))
            if (x - x0 - t * dx) ** 2 + (y - y0 - t * dy) ** 2 < 1.1:
                return 1
        return 0
    return _alpha(n, n, f)


def zap_ring(n=16):
    """A jittery electric ring (alpha only)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = x - c, y - c
        r = (dx * dx + dy * dy) ** .5
        a = math.atan2(dy, dx)
        rr = 6 + .9 * math.sin(a * 11) + .5 * math.sin(a * 5)
        return 1 if abs(r - rr) < .8 else 0
    return _alpha(n, n, f)


def blankie(size=64):
    """A blue security blanket with yellow stars, draped over a curled-up lump (shown at 1:1)."""
    im, d, S = _big(size)
    OUT, BLUE, BLUE_L, BLUE_D = (15, 20, 50, 255), (90, 140, 230, 255), (160, 200, 255, 255), (60, 100, 190, 255)
    d.chord([S * .06, S * .14, S * .94, S * 1.5], 180, 360, fill=BLUE, outline=OUT, width=10)
    d.rectangle([S * .06, S * .8, S * .94, S * .96], fill=BLUE, outline=OUT, width=10)
    d.rectangle([S * .08, S * .76, S * .92, S * .9], fill=BLUE)
    for x in (.3, .5, .7):                                                                             # folds
        d.line([(S * x, S * .36), (S * (x - .04), S * .92)], fill=BLUE_D, width=7)
    d.arc([S * .14, S * .2, S * .7, S * .8], 200, 250, fill=BLUE_L, width=10)
    for x, y in ((.28, .5), (.6, .34), (.72, .66), (.44, .74)):                                        # stars
        r = S * .05
        d.polygon([(S * x, S * y - r), (S * x + r * .35, S * y - r * .3), (S * x + r, S * y), (S * x + r * .35, S * y + r * .3),
                   (S * x, S * y + r), (S * x - r * .35, S * y + r * .3), (S * x - r, S * y), (S * x - r * .35, S * y - r * .3)],
                  fill=(255, 225, 70, 255))
    d.line([(S * .06, S * .96), (S * .94, S * .96)], fill=OUT, width=10)
    return _shrink(im, size)


def choke_collar(size=64):
    """A spiked dog choke-collar snapped round a neck, the leash pulled taut off to the left."""
    import math
    im, d, S = _big(size)
    OUT, LEATHER, LEATHER_L, STEEL = (15, 10, 5, 255), (40, 35, 35, 255), (90, 80, 80, 255), (210, 215, 225, 255)
    d.line([(S * .0, S * .5), (S * .16, S * .62)], fill=OUT, width=int(S * .09))                     # the leash
    d.line([(S * .0, S * .5), (S * .16, S * .62)], fill=(200, 40, 40, 255), width=int(S * .05))
    d.ellipse([S * .14, S * .46, S * .86, S * .78], outline=OUT, width=int(S * .09))                  # the collar
    d.ellipse([S * .16, S * .48, S * .84, S * .76], outline=LEATHER, width=int(S * .05))
    d.arc([S * .16, S * .48, S * .84, S * .76], 200, 330, fill=LEATHER_L, width=6)
    for k in range(9):                                                                                 # spikes
        a = math.radians(200 + k * 17.5)
        cx, cy = S * .5 + S * .36 * math.cos(a), S * .62 + S * .16 * math.sin(a)
        tx, ty = S * .5 + S * .46 * math.cos(a), S * .62 + S * .26 * math.sin(a)
        nx, ny = -math.sin(a) * S * .04, math.cos(a) * S * .04
        d.polygon([(cx + nx, cy + ny), (tx, ty), (cx - nx, cy - ny)], fill=STEEL, outline=OUT)
    d.ellipse([S * .1, S * .56, S * .22, S * .68], fill=STEEL, outline=OUT, width=6)                  # the ring
    return _shrink(im, size)


def gasp_puff(n=16):
    """A little puff of breath (alpha only): three bumps."""
    def f(x, y):
        v = 0
        for cx, cy, r in ((5, 9, 3.2), (9, 7, 3.6), (11, 10, 2.6)):
            v = max(v, 1.3 - ((x - cx) ** 2 + (y - cy) ** 2) ** .5 / r)
        return v
    return _alpha(n, n, f)


def trash_tornado(size=64):
    """A grey trash tornado: a twisting funnel with streaks, a can and a bag caught in it."""
    import math
    im, d, S = _big(size)
    OUT, G, GL, GD = (30, 30, 35, 200), (150, 150, 160, 230), (205, 205, 215, 230), (100, 100, 110, 230)
    for k in range(9):                                                                                 # the bands
        y = S * (.06 + k * .1)
        hw = S * (.44 - k * .042)
        cx = S * (.5 + .05 * math.sin(k * 1.3))
        d.ellipse([cx - hw, y, cx + hw, y + S * .12], fill=G if k % 2 else GD, outline=OUT, width=6)
        d.arc([cx - hw * .8, y + 3, cx + hw * .6, y + S * .1], 190, 290, fill=GL, width=6)
    d.rectangle([S * .18, S * .2, S * .28, S * .32], fill=(220, 40, 40, 255), outline=(20, 10, 10, 255), width=5)   # can
    d.polygon([(S * .66, S * .36), (S * .8, S * .32), (S * .78, S * .46), (S * .64, S * .48)], fill=(250, 250, 245, 255),
              outline=(20, 20, 20, 255))                                                                # a bag
    return _shrink(im, size)


def trash_bit(n=16):
    """A crushed can / scrap of trash tumbling (alpha only)."""
    def f(x, y):
        if 4 <= x <= 11 and 3 <= y <= 12 and not (x > 9 and y < 6):
            return 1 if x not in (4, 11) else .7
        return 0
    return _alpha(n, n, f)


def microwave(size=64):
    """A microwave seen from the front: a foil ball inside, sparks, the keypad, 0:03 on the clock."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (15, 15, 18, 255)
    d.rectangle([3, 14, 60, 50], fill=(225, 225, 230, 255), outline=OUT)
    d.rectangle([7, 18, 42, 46], fill=(40, 40, 50, 255), outline=OUT)                                 # the window
    d.ellipse([18, 30, 30, 42], fill=(200, 205, 215, 255), outline=(110, 110, 120, 255))              # the foil
    d.line([(20, 33), (28, 39)], fill=(255, 255, 255, 255))
    for x0, y0, x1, y1 in ((16, 26, 20, 22), (30, 28, 35, 24), (14, 40, 10, 44), (32, 40, 37, 43)):    # sparks
        d.line([(x0, y0), (x1, y1)], fill=(120, 220, 255, 255), width=1)
    d.rectangle([46, 18, 57, 24], fill=(20, 40, 20, 255), outline=OUT)                                # the clock
    _outlined_text(d, (47, 19), "0:03"[:3], (90, 255, 90, 255), outline=(20, 40, 20, 255))
    for k in range(9):                                                                                 # keypad
        d.rectangle([46 + (k % 3) * 4, 28 + (k // 3) * 4, 48 + (k % 3) * 4, 30 + (k // 3) * 4], fill=(150, 150, 160, 255))
    d.rectangle([3, 50, 60, 53], fill=(150, 150, 160, 255), outline=OUT)
    return im


def kaboom_cloud(size=64):
    """A huge cartoon explosion: a fiery cloud, smoky top, white-hot core."""
    import math
    import random
    im, d, S = _big(size)
    rnd = random.Random(9)
    for col, sc in (((70, 60, 60, 255), 1.0), ((230, 70, 20, 255), .82), ((255, 160, 30, 255), .62),
                    ((255, 240, 150, 255), .38)):
        pts = []
        for k in range(20):
            a = k * math.tau / 20
            r = S * .46 * sc * (1 + (.18 if k % 2 else 0) + rnd.uniform(-.05, .05))
            pts.append((S / 2 + r * math.cos(a), S / 2 + r * math.sin(a)))
        d.polygon(pts, fill=col)
    return _shrink(im, size)


def acid_splat(size=64):
    """A bright green splat of battery acid, bubbling (holes eaten through it), dripping."""
    import math
    import random
    im, d, S = _big(size)
    rnd = random.Random(12)
    OUT, GOO, GOO_L = (20, 60, 10, 255), (110, 230, 40, 255), (200, 255, 140, 255)
    pts = []
    for k in range(20):
        a = k * math.tau / 20
        r = S * (.26 + (.14 if k % 2 else 0) + rnd.uniform(0, .05))
        pts.append((S / 2 + r * math.cos(a), S / 2 + r * .85 * math.sin(a)))
    d.polygon(pts, fill=GOO)
    d.line(pts + [pts[0]], fill=OUT, width=8)
    for x in (.36, .52, .64):                                                                          # drips
        d.rounded_rectangle([S * (x - .03), S * .6, S * (x + .03), S * (.8 + rnd.uniform(0, .1))], 10, fill=GOO,
                            outline=OUT, width=5)
    for _ in range(7):                                                                                 # bubbles
        x, y, r = rnd.uniform(.32, .68) * S, rnd.uniform(.32, .62) * S, rnd.uniform(.03, .06) * S
        d.ellipse([x - r, y - r, x + r, y + r], fill=GOO_L, outline=OUT, width=4)
    return _shrink(im, size)


def magnifier(size=64):
    """A big magnifying glass, the lens up-left, the handle down-right."""
    im, d, S = _big(size)
    OUT = (20, 15, 10, 255)
    d.line([(S * .6, S * .6), (S * .92, S * .92)], fill=OUT, width=int(S * .14))                    # the handle
    d.line([(S * .6, S * .6), (S * .92, S * .92)], fill=(120, 70, 30, 255), width=int(S * .09))
    d.ellipse([S * .06, S * .06, S * .66, S * .66], fill=(190, 230, 255, 150), outline=OUT, width=12)
    d.ellipse([S * .1, S * .1, S * .62, S * .62], outline=(200, 200, 210, 255), width=10)             # the rim
    d.arc([S * .16, S * .16, S * .5, S * .5], 200, 260, fill=(255, 255, 255, 255), width=10)
    return _shrink(im, size)


def audit_folder(size=64):
    """A fat manila case folder stuffed with paper, AUDIT stamped on it in red (shown at 2:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT, MANILA, MANILA_D = (60, 40, 10, 255), (240, 205, 120, 255), (200, 160, 80, 255)
    d.rectangle([12, 18, 51, 21], fill=(250, 250, 245, 255), outline=OUT)                             # papers
    d.polygon([(10, 21), (22, 21), (25, 18), (34, 18), (34, 21), (53, 21), (53, 46), (10, 46)], fill=MANILA,
              outline=OUT)
    d.line([(11, 44), (52, 44)], fill=MANILA_D)
    d.rectangle([17, 28, 46, 38], outline=(210, 25, 30, 255))
    m = _text_mask("AUDIT")
    im.paste((210, 25, 30, 255), (32 - m.width // 2, 30), m)
    return im


def receipt(n=16):
    """A curling receipt (alpha only): a slip with lines of print, a torn end."""
    def f(x, y):
        if not (4 <= x <= 11 and 1 <= y <= 14):
            return 0
        if y == 14 and x % 2:
            return 0
        return .55 if (y % 3 == 0 and 5 <= x <= 10) else 1
    return _alpha(n, n, f)


def drumsticks(size=64):
    """A pair of wooden drumsticks, side by side, tips to the right (rotate it to swing)."""
    im, d, S = _big(size)
    OUT, WOOD, WOOD_L = (50, 25, 5, 255), (225, 180, 110, 255), (250, 225, 170, 255)
    for y in (.4, .58):
        d.line([(S * .04, S * y), (S * .86, S * (y - .04))], fill=OUT, width=int(S * .1))
        d.line([(S * .04, S * y), (S * .86, S * (y - .04))], fill=WOOD, width=int(S * .06))
        d.ellipse([S * .84, S * (y - .09), S * .96, S * (y + .01)], fill=WOOD_L, outline=OUT, width=6)
    return _shrink(im, size)


def box_dust(n=16):
    """A little puff of cardboard dust knocked off (alpha only)."""
    def f(x, y):
        v = 0
        for cx, cy, r in ((5, 10, 3), (8, 7, 3.6), (11, 10, 3)):
            v = max(v, 1.25 - ((x - cx) ** 2 + (y - cy) ** 2) ** .5 / r)
        return v
    return _alpha(n, n, f)


def stink_puff(n=16):
    """A lumpy cloud of gas (alpha only), denser in the middle."""
    def f(x, y):
        v = 0
        for cx, cy, r in ((5, 8, 4), (10, 7, 4.2), (8, 11, 3.6), (7.5, 5, 3)):
            v = max(v, 1.4 - ((x - cx) ** 2 + (y - cy) ** 2) ** .5 / r)
        return v * .9
    return _alpha(n, n, f)


def stench_wave(w=16, h=32):
    """Two tall wavy stench lines (alpha only)."""
    import math

    def f(x, y):
        for cx in (5, 11):
            if abs(x - (cx + 1.5 * math.sin(y / 3))) < .9 and 2 <= y <= h - 3:
                return 1
        return 0
    return _alpha(w, h, f)


def water_flick(n=16):
    """A tiny spatter of drops (alpha only)."""
    pts = ((4, 4, 1.6), (10, 3, 1.2), (12, 9, 1.8), (6, 11, 1.4), (8, 7, 1.0))

    def f(x, y):
        return 1 if any((x - px) ** 2 + (y - py) ** 2 <= r * r for px, py, r in pts) else 0
    return _alpha(n, n, f)


def nap_z(n=16):
    """A puffy rounded Z (alpha only)."""
    def f(x, y):
        if 3 <= y <= 5 and 3 <= x <= 12:
            return 1
        if 10 <= y <= 12 and 3 <= x <= 12:
            return 1
        return 1 if 5 <= y <= 10 and abs((x - 3) - (12 - 3) * (10 - y) / 5) < 1.4 else 0
    return _alpha(n, n, f)


def speed_streak(n=16):
    """Three horizontal speed lines (alpha only)."""
    def f(x, y):
        for cy, x0 in ((4, 2), (8, 0), (12, 4)):
            if abs(y - cy) < .8 and x0 <= x <= 15:
                return 1 - (x - x0) / 20
        return 0
    return _alpha(n, n, f)


def cut_mark(n=16):
    """A thin diagonal paper-cut slash (alpha only)."""
    def f(x, y):
        d = abs((x - 7.5) + (y - 7.5)) / 1.414
        along = abs((x - 7.5) - (y - 7.5)) / 1.414
        return 1 if d < .8 and along < 6 else 0
    return _alpha(n, n, f)


def pepper_can(size=64):
    """A pepper spray canister pointing right: orange can, black cap, red trigger, the nozzle."""
    im, d, S = _big(size)
    OUT, ORANGE, ORANGE_L = (20, 10, 5, 255), (240, 120, 20, 255), (255, 190, 120, 255)
    d.rounded_rectangle([S * .1, S * .36, S * .6, S * .66], 20, fill=ORANGE, outline=OUT, width=9)
    d.line([(S * .14, S * .42), (S * .56, S * .42)], fill=ORANGE_L, width=6)
    d.rectangle([S * .24, S * .48, S * .46, S * .58], fill=(255, 255, 255, 255), outline=OUT, width=5)   # label
    d.line([(S * .28, S * .53), (S * .42, S * .53)], fill=(220, 40, 40, 255), width=6)
    d.rectangle([S * .58, S * .38, S * .76, S * .64], fill=(30, 30, 35, 255), outline=OUT, width=8)   # the cap
    d.rectangle([S * .62, S * .26, S * .72, S * .38], fill=(220, 30, 30, 255), outline=OUT, width=7)  # trigger
    d.rectangle([S * .76, S * .46, S * .86, S * .54], fill=(30, 30, 35, 255), outline=OUT, width=6)   # nozzle
    return _shrink(im, size)


def pepper_mist(n=16):
    """A soft cloud of spray (alpha only)."""
    c = (n - 1) / 2
    return _alpha(n, n, lambda x, y: 1.1 - ((x - c) ** 2 + (y - c) ** 2) ** .5 / 7)


def microphone(size=64):
    """A handheld mic tipped up to the right: chrome ball grille, black handle, a gold band."""
    im, d, S = _big(size)
    OUT, CHROME, CHROME_L, CHROME_D = (10, 10, 12, 255), (190, 195, 205, 255), (245, 248, 255, 255), (120, 125, 135, 255)
    d.line([(S * .14, S * .86), (S * .5, S * .5)], fill=OUT, width=int(S * .2))                     # the handle
    d.line([(S * .14, S * .86), (S * .5, S * .5)], fill=(35, 35, 40, 255), width=int(S * .14))
    d.line([(S * .44, S * .56), (S * .52, S * .48)], fill=(240, 190, 40, 255), width=int(S * .16))   # gold band
    d.ellipse([S * .44, S * .1, S * .9, S * .56], fill=CHROME, outline=OUT, width=10)                # the ball
    for k in range(5):                                                                                 # the mesh
        d.line([(S * (.5 + k * .08), S * .14), (S * (.5 + k * .08), S * .52)], fill=CHROME_D, width=4)
        d.line([(S * .48, S * (.18 + k * .08)), (S * .86, S * (.18 + k * .08))], fill=CHROME_D, width=4)
    d.arc([S * .5, S * .14, S * .76, S * .4], 200, 260, fill=CHROME_L, width=10)
    return _shrink(im, size)


def roast_flame(n=16):
    """A little licking flame (alpha only): someone just got roasted."""
    import math

    def f(x, y):
        if y < 2:
            return 0
        t = (y - 2) / 13
        half = 5.5 * math.sin(t * math.pi * .9) * (.55 + .45 * t)
        cx = 7.5 + 1.5 * math.sin(y / 2.5) * (1 - t)
        return 1 if abs(x - cx) < half else 0
    return _alpha(n, n, f)


def super_soaker(size=64):
    """A neon water blaster pointing right: orange body, green pump, a fat clear tank of water on top."""
    im, d, S = _big(size)
    OUT, ORANGE, GREEN, TANK = (20, 10, 5, 255), (255, 130, 20, 255), (90, 220, 60, 255), (120, 190, 255, 200)
    d.rounded_rectangle([S * .28, S * .14, S * .66, S * .34], 26, fill=TANK, outline=OUT, width=9)   # the tank
    d.line([(S * .34, S * .2), (S * .58, S * .2)], fill=(230, 245, 255, 255), width=6)
    d.rounded_rectangle([S * .08, S * .36, S * .84, S * .54], 16, fill=ORANGE, outline=OUT, width=9) # the body
    d.rectangle([S * .84, S * .41, S * .97, S * .49], fill=GREEN, outline=OUT, width=7)               # the nozzle
    d.rounded_rectangle([S * .52, S * .54, S * .8, S * .66], 12, fill=GREEN, outline=OUT, width=8)   # the pump
    d.polygon([(S * .14, S * .52), (S * .34, S * .52), (S * .3, S * .9), (S * .1, S * .9)], fill=ORANGE)  # grip
    d.line([(S * .14, S * .52), (S * .1, S * .9), (S * .3, S * .9), (S * .34, S * .52)], fill=OUT, width=9)
    d.line([(S * .12, S * .4), (S * .8, S * .4)], fill=(255, 200, 140, 255), width=6)
    return _shrink(im, size)


def phone_rec(size=64):
    """A phone held up filming: black phone, the scene on screen, a red REC dot (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (8, 8, 10, 255)
    d.rounded_rectangle([18, 4, 45, 60], 4, fill=(30, 30, 36, 255), outline=OUT)
    d.rectangle([20, 9, 43, 53], fill=(120, 200, 255, 255))                                            # the screen
    d.rectangle([20, 40, 43, 53], fill=(90, 190, 90, 255))
    d.ellipse([27, 26, 37, 42], fill=(140, 90, 50, 255))                                               # (them, pied)
    d.ellipse([22, 12, 26, 16], fill=(230, 30, 30, 255))
    _outlined_text(d, (28, 11), "REC", (255, 255, 255, 255), outline=(30, 30, 36, 255))
    d.rectangle([29, 56, 34, 57], fill=(90, 90, 100, 255))
    return im


def pimp_hand(size=64):
    """The pimp hand: back of the hand, a fat gem ring on every finger, a white fur cuff."""
    im, d, S = _big(size)
    OUT, SKIN, SKIN_D, GOLD = (70, 35, 20, 255), (240, 190, 145, 255), (205, 145, 105, 255), (255, 205, 40, 255)
    GEMS = ((230, 40, 60, 255), (60, 200, 255, 255), (80, 220, 80, 255), (200, 80, 255, 255))
    for k in range(4):                                                                                 # fingers
        x = S * (.24 + k * .14)
        top = S * (.06 + abs(k - 1.5) * .05)
        d.rounded_rectangle([x, top, x + S * .13, S * .56], 30, fill=SKIN, outline=OUT, width=9)
        d.rectangle([x - S * .01, S * .3, x + S * .14, S * .38], fill=GOLD, outline=OUT, width=5)       # rings
        d.ellipse([x + S * .025, S * .26, x + S * .105, S * .34], fill=GEMS[k], outline=OUT, width=4)
    d.rounded_rectangle([S * .2, S * .44, S * .82, S * .8], 40, fill=SKIN, outline=OUT, width=9)     # the back
    for k in range(3):
        x = S * (.33 + k * .14)
        d.arc([x - S * .04, S * .48, x + S * .04, S * .56], 200, 340, fill=SKIN_D, width=6)
    d.polygon([(S * .06, S * .56), (S * .24, S * .5), (S * .28, S * .68), (S * .1, S * .74)], fill=SKIN, outline=OUT)
    d.line([(S * .06, S * .56), (S * .24, S * .5), (S * .28, S * .68), (S * .1, S * .74)], fill=OUT, width=8)
    for k in range(9):                                                                                 # fur cuff
        x = S * (.16 + k * .08)
        d.ellipse([x - S * .06, S * .76, x + S * .06, S * .98], fill=(250, 250, 250, 255), outline=(170, 170, 180, 255),
                  width=4)
    return _shrink(im, size)


def nine_volt(size=32):
    """A 9-volt battery, standing up: black body, a copper band with 9V on it, the two snap terminals on top
    (one round, one hex). Drawn straight at full size: the 9V has to read."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (10, 10, 14, 255)
    d.rectangle([8, 9, 23, 30], fill=(35, 35, 40, 255), outline=OUT)                                   # the body
    d.rectangle([9, 15, 22, 23], fill=(215, 125, 40, 255))                                             # copper band
    m = _text_mask("9V")
    im.paste((255, 255, 255, 255), (16 - m.width // 2, 16), m)
    d.ellipse([10, 3, 14, 8], fill=(200, 200, 210, 255), outline=OUT)                                 # round snap
    d.polygon([(17, 4), (21, 4), (22, 6), (21, 8), (17, 8), (16, 6)], fill=(200, 200, 210, 255), outline=OUT)  # hex
    d.rectangle([11, 8, 13, 9], fill=OUT)
    d.rectangle([18, 8, 20, 9], fill=OUT)
    d.line([(10, 11), (21, 11)], fill=(90, 90, 100, 255))
    return im


def shank_spoon(size=64):
    """A commissary spoon filed into a shank, pointing right: tape-wrapped handle, rusty tip, crud."""
    im, d, S = _big(size)
    OUT, STEEL, STEEL_L, TAPE, RUST = (20, 20, 25, 255), (170, 175, 185, 255), (230, 235, 245, 255), (90, 90, 100, 255), (180, 90, 40, 255)
    d.rounded_rectangle([S * .04, S * .42, S * .44, S * .58], 20, fill=TAPE, outline=OUT, width=9)   # taped handle
    for x in (.12, .2, .28, .36):
        d.line([(S * x, S * .43), (S * (x + .04), S * .57)], fill=(60, 60, 68, 255), width=5)
    d.polygon([(S * .42, S * .44), (S * .66, S * .4), (S * .98, S * .5), (S * .66, S * .6), (S * .42, S * .56)],
              fill=STEEL, outline=OUT)                                                                   # the blade
    d.line([(S * .42, S * .44), (S * .66, S * .4), (S * .98, S * .5), (S * .66, S * .6), (S * .42, S * .56)], fill=OUT,
           width=8)
    d.line([(S * .48, S * .46), (S * .9, S * .5)], fill=STEEL_L, width=5)
    d.polygon([(S * .8, S * .46), (S * .98, S * .5), (S * .8, S * .55)], fill=RUST)                  # the dirty tip
    d.ellipse([S * .56, S * .5, S * .64, S * .56], fill=(130, 200, 60, 255))
    return _shrink(im, size)


def acrylic_nail(n=16):
    """A long coffin-shaped press-on acrylic nail (alpha only), a glint stripe."""
    def f(x, y):
        u, v = (x - 7.5) * .8 + (y - 7.5) * .6, -(x - 7.5) * .6 + (y - 7.5) * .8
        if -6 <= u <= 6 and abs(v) <= 2.4 - (u + 6) * .08:
            return .6 if abs(v) < .6 and u < 3 else 1
        return 0
    return _alpha(n, n, f)


def glitter_tall(w=16, h=32):
    """A column of glitter specks twinkling (alpha only)."""
    pts = ((3, 4), (11, 7), (6, 12), (12, 16), (4, 20), (9, 24), (13, 28), (6, 28))

    def f(x, y):
        for px, py in pts:
            if (abs(x - px) < .6 and abs(y - py) < 2) or (abs(y - py) < .6 and abs(x - px) < 2):
                return 1
        return 0
    return _alpha(w, h, f)


def parking_boot(size=64):
    """The yellow parking boot: a clamp hugging a wheel-sized foot, the arm and the padlock (shown at 1:1)."""
    im, d, S = _big(size)
    OUT, Y, YL, YD = (20, 15, 5, 255), (255, 210, 20, 255), (255, 240, 140, 255), (200, 150, 10, 255)
    d.ellipse([S * .14, S * .3, S * .74, S * .9], fill=(30, 30, 35, 255), outline=OUT, width=10)    # the hub
    d.ellipse([S * .3, S * .46, S * .58, S * .74], fill=Y, outline=OUT, width=10)                     # the disc
    for a in (0, 90, 180, 270):
        import math
        x, y = S * .44 + S * .1 * math.cos(math.radians(a)), S * .6 + S * .1 * math.sin(math.radians(a))
        d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=YD)
    d.rectangle([S * .56, S * .2, S * .7, S * .62], fill=Y, outline=OUT, width=9)                     # the arm
    d.rectangle([S * .56, S * .14, S * .94, S * .28], fill=Y, outline=OUT, width=9)
    d.line([(S * .6, S * .24), (S * .9, S * .24)], fill=YL, width=6)
    d.rounded_rectangle([S * .78, S * .3, S * .96, S * .5], 8, fill=(190, 190, 200, 255), outline=OUT, width=8)  # lock
    d.arc([S * .8, S * .2, S * .94, S * .38], 180, 360, fill=OUT, width=8)
    return _shrink(im, size)


def dumpster(size=64):
    """A green dumpster, the lid propped open, trash spilling over the rim."""
    im, d, S = _big(size)
    OUT, G, GL, GD = (10, 25, 10, 255), (50, 130, 60, 255), (100, 180, 100, 255), (30, 90, 40, 255)
    d.polygon([(S * .06, S * .42), (S * .94, S * .42), (S * .88, S * .9), (S * .12, S * .9)], fill=G)
    d.line([(S * .06, S * .42), (S * .94, S * .42), (S * .88, S * .9), (S * .12, S * .9), (S * .06, S * .42)], fill=OUT,
           width=10)
    for x in (.3, .5, .7):
        d.line([(S * x, S * .46), (S * x, S * .86)], fill=GD, width=8)
    d.polygon([(S * .06, S * .42), (S * .5, S * .42), (S * .4, S * .1), (S * 0, S * .14)], fill=GD, outline=OUT)  # lid
    d.line([(S * .06, S * .42), (S * .5, S * .42), (S * .4, S * .1), (S * 0, S * .14), (S * .06, S * .42)], fill=OUT,
           width=9)
    for x, col in ((.6, (250, 250, 245, 255)), (.74, (40, 40, 45, 255)), (.84, (200, 60, 40, 255))):  # trash
        d.ellipse([S * (x - .08), S * .3, S * (x + .08), S * .46], fill=col, outline=OUT, width=6)
    d.line([(S * .1, S * .48), (S * .9, S * .48)], fill=GL, width=6)
    for x in (.18, .82):                                                                               # wheels
        d.ellipse([S * (x - .05), S * .88, S * (x + .05), S * .98], fill=(40, 40, 45, 255), outline=OUT, width=6)
    return _shrink(im, size)


def raccoon(size=64):
    """A trash panda popping up, arms up, a fistful of slop, the bandit mask."""
    im, d, S = _big(size)
    OUT, GREY, GREY_L, DARK = (15, 15, 18, 255), (130, 130, 140, 255), (215, 215, 220, 255), (40, 40, 45, 255)
    d.ellipse([S * .26, S * .44, S * .74, S * .98], fill=GREY, outline=OUT, width=10)                # the body
    d.ellipse([S * .36, S * .58, S * .64, S * .9], fill=GREY_L)
    for x in (.24, .62):                                                                               # ears
        d.polygon([(S * x, S * .2), (S * (x + .08), S * .04), (S * (x + .16), S * .2)], fill=GREY, outline=OUT)
    d.ellipse([S * .2, S * .1, S * .8, S * .56], fill=GREY, outline=OUT, width=10)                    # the head
    d.ellipse([S * .26, S * .26, S * .74, S * .42], fill=DARK)                                         # the mask
    for x in (.34, .56):
        d.ellipse([S * x, S * .28, S * (x + .1), S * .38], fill=(255, 255, 255, 255))
        d.ellipse([S * (x + .03), S * .3, S * (x + .07), S * .36], fill=OUT)
    d.ellipse([S * .46, S * .42, S * .54, S * .48], fill=OUT)                                          # nose
    d.line([(S * .3, S * .6), (S * .1, S * .36)], fill=OUT, width=14)                                  # arm up
    d.ellipse([S * .0, S * .2, S * .2, S * .4], fill=(110, 115, 45, 255), outline=OUT, width=8)       # the slop
    return _shrink(im, size)


def outlet_cords(size=64):
    """One wall outlet with six plugs and a rat's nest of extension cords, scorched: a fire hazard."""
    import random
    im, d, S = _big(size)
    rnd = random.Random(3)
    OUT = (20, 20, 22, 255)
    for k in range(8):                                                                                 # the cords
        x0, y0 = S * (.3 + rnd.uniform(0, .4)), S * (.36 + rnd.uniform(0, .3))
        x1, y1 = S * rnd.choice((.0, .1, .9, 1.0)), S * rnd.uniform(.1, 1.0)
        mx, my = (x0 + x1) / 2 + rnd.uniform(-60, 60), (y0 + y1) / 2 + rnd.uniform(-60, 60)
        col = rnd.choice(((250, 140, 20, 255), (240, 240, 235, 255), (30, 30, 35, 255), (60, 140, 230, 255)))
        d.line([(x0, y0), (mx, my), (x1, y1)], fill=OUT, width=14)
        d.line([(x0, y0), (mx, my), (x1, y1)], fill=col, width=8)
    d.rounded_rectangle([S * .3, S * .22, S * .7, S * .78], 16, fill=(240, 235, 220, 255), outline=OUT, width=9)  # plate
    for k in range(6):                                                                                 # plugs
        x, y = S * (.36 + (k % 2) * .16), S * (.28 + (k // 2) * .16)
        d.rectangle([x, y, x + S * .12, y + S * .12], fill=(40, 40, 45, 255), outline=OUT, width=6)
    d.ellipse([S * .24, S * .1, S * .5, S * .3], fill=(60, 50, 40, 160))                                # scorch
    return _shrink(im, size)


def rain_cloud(size=64):
    """A little grey storm cloud, sagging (it follows sad people around)."""
    im, d, S = _big(size)
    OUT, G, GL, GD = (40, 45, 55, 255), (150, 155, 170, 255), (200, 205, 215, 255), (110, 115, 130, 255)
    for x, y, r in ((.3, .5, .18), (.5, .4, .22), (.7, .5, .18), (.42, .58, .16), (.6, .58, .16)):
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], fill=OUT)
    for x, y, r in ((.3, .5, .15), (.5, .4, .19), (.7, .5, .15), (.42, .58, .13), (.6, .58, .13)):
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], fill=G)
    d.arc([S * .34, S * .24, S * .62, S * .5], 200, 280, fill=GL, width=10)
    d.line([(S * .2, S * .66), (S * .8, S * .66)], fill=GD, width=8)
    return _shrink(im, size)


def raindrop(n=16):
    """A falling raindrop streak (alpha only)."""
    def f(x, y):
        return 1 if abs(x - 7.5) < 1 and 3 <= y <= 12 else (.6 if abs(x - 7.5) < 1.6 and 12 < y <= 13 else 0)
    return _alpha(n, n, f)


def sad_blankie(size=64):
    """Curled up under a blue blankie: a pint of ice cream and a spoon poking out of the front."""
    im = blankie(size)
    d = ImageDraw.Draw(im)
    OUT = (15, 20, 50, 255)
    d.rectangle([36, 40, 48, 54], fill=(250, 245, 235, 255), outline=OUT)                              # the pint
    d.rectangle([36, 40, 48, 43], fill=(200, 90, 150, 255), outline=OUT)
    d.rectangle([39, 46, 45, 50], fill=(140, 80, 40, 255))
    d.line([(44, 39), (49, 30)], fill=(200, 200, 210, 255), width=2)                                   # the spoon
    d.ellipse([47, 27, 52, 31], fill=(200, 200, 210, 255), outline=OUT)
    return im


def auntie_chair(size=64):
    """Auntie in her lawn chair, head wrap and shades, cup in hand, completely unbothered."""
    im, d, S = _big(size)
    OUT, SKIN, WRAP, CHAIR = (25, 15, 10, 255), (150, 95, 60, 255), (230, 60, 140, 255), (60, 170, 220, 255)
    d.rectangle([S * .14, S * .5, S * .86, S * .66], fill=CHAIR, outline=OUT, width=8)                # the seat
    for x in (.16, .3, .44, .58, .72):
        d.line([(S * x, S * .5), (S * x, S * .66)], fill=(250, 250, 250, 255), width=6)
    d.line([(S * .2, S * .66), (S * .8, S * .96)], fill=(200, 200, 210, 255), width=10)               # the legs
    d.line([(S * .8, S * .66), (S * .2, S * .96)], fill=(200, 200, 210, 255), width=10)
    d.rounded_rectangle([S * .3, S * .3, S * .7, S * .6], 20, fill=(240, 200, 40, 255), outline=OUT, width=8)  # dress
    d.ellipse([S * .34, S * .08, S * .66, S * .36], fill=SKIN, outline=OUT, width=8)                  # the head
    d.chord([S * .3, S * .0, S * .7, S * .3], 180, 360, fill=WRAP, outline=OUT, width=8)               # head wrap
    d.rectangle([S * .38, S * .18, S * .62, S * .24], fill=OUT)                                        # shades
    d.line([(S * .68, S * .42), (S * .84, S * .34)], fill=SKIN, width=12)                              # arm + cup
    d.rectangle([S * .8, S * .24, S * .9, S * .36], fill=(220, 30, 40, 255), outline=OUT, width=5)
    return _shrink(im, size)


def empty_wallet(size=64):
    """A brown wallet flopped open - empty - and a moth fluttering out of it."""
    im, d, S = _big(size)
    OUT, LEATHER, LEATHER_D = (40, 20, 5, 255), (150, 90, 45, 255), (110, 60, 25, 255)
    d.rounded_rectangle([S * .08, S * .44, S * .92, S * .9], 16, fill=LEATHER, outline=OUT, width=9)
    d.line([(S * .5, S * .46), (S * .5, S * .88)], fill=LEATHER_D, width=8)                            # the fold
    for x in (.14, .56):                                                                               # empty slots
        d.rectangle([S * x, S * .54, S * (x + .3), S * .66], fill=LEATHER_D, outline=OUT, width=5)
    d.ellipse([S * .42, S * .1, S * .58, S * .26], fill=(160, 150, 130, 255), outline=OUT, width=6)    # the moth
    d.polygon([(S * .44, S * .16), (S * .2, S * .04), (S * .26, S * .28)], fill=(200, 190, 170, 255), outline=OUT)
    d.polygon([(S * .56, S * .16), (S * .8, S * .04), (S * .74, S * .28)], fill=(200, 190, 170, 255), outline=OUT)
    for k in range(3):                                                                                 # dust
        d.ellipse([S * (.4 + k * .1), S * (.34 + (k % 2) * .04), S * (.43 + k * .1), S * (.37 + (k % 2) * .04)],
                  fill=(200, 190, 170, 255))
    return _shrink(im, size)


def paint_bucket(size=64):
    """An orange paint bucket flipped upside down: the street drummer's drum."""
    im, d, S = _big(size)
    OUT, OR, ORL, ORD = (30, 15, 5, 255), (255, 130, 20, 255), (255, 190, 110, 255), (200, 90, 10, 255)
    d.polygon([(S * .22, S * .2), (S * .78, S * .2), (S * .86, S * .9), (S * .14, S * .9)], fill=OR)
    d.line([(S * .22, S * .2), (S * .78, S * .2), (S * .86, S * .9), (S * .14, S * .9), (S * .22, S * .2)], fill=OUT,
           width=10)
    d.ellipse([S * .2, S * .12, S * .8, S * .28], fill=ORD, outline=OUT, width=9)                      # the top
    for y in (.44, .7):                                                                                # ribs
        d.line([(S * .18, S * y), (S * .82, S * y)], fill=ORD, width=8)
    d.line([(S * .3, S * .3), (S * .26, S * .84)], fill=ORL, width=8)
    return _shrink(im, size)


def dollar_fold(n=16):
    """A folded dollar bill (alpha only): a tent of paper with a fold line."""
    def f(x, y):
        if not (2 <= x <= 13 and 5 <= y <= 11):
            return 0
        return .6 if x in (7, 8) or (y == 8 and 4 <= x <= 11) else 1
    return _alpha(n, n, f)


def busted_sneaker(size=32):
    """A beat-up low-top sneaker side-on, toe to the right: grimy upper, laces, a hole, the sole peeling off."""
    im, d, S = _big(size)
    OUT, DIRT, DIRT_D, SOLE = (25, 20, 10, 255), (210, 195, 160, 255), (150, 130, 90, 255), (245, 240, 230, 255)
    d.rounded_rectangle([S * .04, S * .66, S * .96, S * .84], 12, fill=SOLE, outline=OUT, width=6)    # the sole
    d.polygon([(S * .74, S * .84), (S * .98, S * .86), (S * .96, S * .96), (S * .7, S * .9)], fill=SOLE, outline=OUT)
    d.polygon([(S * .06, S * .68), (S * .08, S * .3), (S * .36, S * .26), (S * .5, S * .44), (S * .82, S * .5),
               (S * .94, S * .66)], fill=DIRT, outline=OUT)
    d.line([(S * .06, S * .68), (S * .08, S * .3), (S * .36, S * .26), (S * .5, S * .44), (S * .82, S * .5),
            (S * .94, S * .66)], fill=OUT, width=6)
    for k in range(3):                                                                                 # laces
        x = S * (.38 + k * .1)
        d.line([(x, S * (.36 + k * .04)), (x + S * .08, S * (.44 + k * .04))], fill=OUT, width=5)
    d.ellipse([S * .14, S * .44, S * .28, S * .58], fill=(120, 100, 70, 255), outline=OUT, width=4)   # a hole
    d.line([(S * .1, S * .62), (S * .9, S * .62)], fill=DIRT_D, width=4)
    return _shrink(im, size)


def dirt_bike(size=64):
    """A red dirt bike side-on, facing right, popping a wheelie-ready stance: knobby tires, high fender."""
    im, d, S = _big(size)
    OUT, RED, REDL = (15, 10, 10, 255), (220, 35, 40, 255), (255, 120, 120, 255)
    for x in (.2, .8):                                                                                 # tires
        d.ellipse([S * (x - .17), S * .5, S * (x + .17), S * .84], fill=(30, 30, 35, 255), outline=OUT, width=10)
        d.ellipse([S * (x - .07), S * .6, S * (x + .07), S * .74], fill=(180, 180, 190, 255), outline=OUT, width=6)
    d.polygon([(S * .2, S * .66), (S * .44, S * .4), (S * .72, S * .4), (S * .8, S * .66), (S * .56, S * .62)],
              fill=(80, 80, 90, 255), outline=OUT)                                                       # the frame
    d.polygon([(S * .36, S * .4), (S * .7, S * .34), (S * .74, S * .44), (S * .4, S * .5)], fill=RED, outline=OUT)  # tank
    d.line([(S * .4, S * .38), (S * .66, S * .34)], fill=REDL, width=6)
    d.polygon([(S * .1, S * .42), (S * .4, S * .4), (S * .34, S * .46), (S * .06, S * .48)], fill=RED, outline=OUT)  # seat
    d.line([(S * .74, S * .42), (S * .82, S * .14)], fill=OUT, width=12)                               # forks
    d.line([(S * .74, S * .16), (S * .92, S * .12)], fill=OUT, width=10)                               # bars
    d.polygon([(S * .78, S * .44), (S * .98, S * .48), (S * .96, S * .54)], fill=RED, outline=OUT)    # fender
    d.rectangle([S * .48, S * .52, S * .6, S * .6], fill=(200, 200, 210, 255), outline=OUT, width=5)  # engine
    return _shrink(im, size)


def durag(size=64):
    """A black satin durag, the long tail whipping out to the right, a shine on it."""
    import math
    im, d, S = _big(size)
    OUT, BLACK, SHINE = (5, 5, 8, 255), (40, 40, 50, 255), (130, 130, 160, 255)
    d.chord([S * .02, S * .2, S * .4, S * .7], 90, 270, fill=BLACK, outline=OUT, width=9)               # the cap
    d.rectangle([S * .2, S * .2, S * .36, S * .7], fill=BLACK)
    d.arc([S * .06, S * .26, S * .34, S * .6], 120, 220, fill=SHINE, width=8)
    pts = [(S * (.3 + .68 * t), S * (.42 - .22 * math.sin(t * math.pi * 1.5))) for t in (k / 18 for k in range(19))]
    for k, (a, b) in enumerate(zip(pts, pts[1:])):                                                     # the tail
        wdt = int(S * (.16 - .1 * k / 18))
        d.line([a, b], fill=OUT, width=wdt + 10)
    for k, (a, b) in enumerate(zip(pts, pts[1:])):
        wdt = int(S * (.16 - .1 * k / 18))
        d.line([a, b], fill=BLACK, width=wdt)
    d.line(pts[2:9], fill=SHINE, width=5)
    return _shrink(im, size)


def shades_zip(size=64):
    """Black shades up top, a zipper across the mouth below: lips zipped (worn over their face)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (5, 5, 8, 255)
    for x in (12, 34):                                                                                 # the shades
        d.rounded_rectangle([x, 14, x + 18, 26], 3, fill=(20, 20, 26, 255), outline=OUT)
        d.line([(x + 3, 17), (x + 8, 17)], fill=(140, 150, 180, 255))
    d.line([(30, 18), (34, 18)], fill=OUT, width=2)
    d.rectangle([16, 40, 48, 46], fill=(180, 60, 60, 255), outline=OUT)                                # the lips
    for x in range(18, 47, 3):                                                                          # the zipper
        d.line([(x, 41), (x + 1, 45)], fill=(220, 220, 230, 255))
    d.rectangle([46, 39, 51, 47], fill=(220, 220, 230, 255), outline=OUT)
    return im


def who_bubble(size=64):
    """A speech bubble from off-screen: WHO DID IT? (shown at 2:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (15, 15, 25, 255)
    d.rounded_rectangle([12, 18, 51, 41], 6, fill=(255, 255, 255, 255), outline=OUT)
    d.polygon([(44, 40), (52, 48), (38, 41)], fill=(255, 255, 255, 255), outline=OUT)
    d.line([(39, 41), (44, 41)], fill=(255, 255, 255, 255))
    for k, word in enumerate(("WHO DID", "IT?")):
        m = _text_mask(word)
        im.paste((30, 60, 200, 255), (32 - m.width // 2, 21 + k * 8), m)
    return im


def soul_plate(size=64):
    """A heaping plate: fried chicken, mac and cheese, collard greens, a square of cornbread."""
    im, d, S = _big(size)
    OUT = (30, 20, 10, 255)
    d.ellipse([S * .02, S * .3, S * .98, S * .9], fill=(245, 245, 250, 255), outline=OUT, width=9)    # the plate
    d.ellipse([S * .1, S * .36, S * .9, S * .84], outline=(200, 200, 215, 255), width=6)
    d.ellipse([S * .14, S * .34, S * .48, S * .64], fill=(250, 200, 50, 255), outline=OUT, width=7)    # mac n cheese
    for x, y in ((.24, .44), (.34, .5), (.3, .4), (.4, .44)):
        d.ellipse([S * x, S * y, S * (x + .05), S * (y + .03)], fill=(255, 235, 140, 255))
    d.ellipse([S * .48, S * .52, S * .82, S * .8], fill=(50, 120, 40, 255), outline=OUT, width=7)      # greens
    d.rectangle([S * .2, S * .62, S * .42, S * .78], fill=(240, 190, 80, 255), outline=OUT, width=7)   # cornbread
    d.ellipse([S * .5, S * .16, S * .86, S * .5], fill=(190, 110, 40, 255), outline=OUT, width=8)      # chicken
    d.line([(S * .56, S * .44), (S * .44, S * .58)], fill=(245, 240, 225, 255), width=12)
    d.ellipse([S * .38, S * .54, S * .48, S * .64], fill=(245, 240, 225, 255), outline=OUT, width=5)
    d.arc([S * .56, S * .2, S * .8, S * .4], 200, 270, fill=(230, 160, 80, 255), width=8)
    return _shrink(im, size)


def helicopter(size=64):
    """A police helicopter side-on (FEDS on the tail), the spotlight under its nose (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT, BLUE, BLUE_L = (10, 10, 20, 255), (40, 60, 140, 255), (110, 140, 220, 255)
    d.line([(4, 10), (60, 10)], fill=(90, 90, 100, 255), width=2)                                       # the rotor
    d.line([(30, 10), (30, 16)], fill=OUT, width=2)
    d.ellipse([16, 14, 44, 34], fill=BLUE, outline=OUT)                                                 # the cabin
    d.chord([28, 16, 44, 30], 270, 90, fill=(170, 220, 255, 255), outline=OUT)                          # windshield
    d.rectangle([2, 20, 20, 25], fill=BLUE, outline=OUT)                                                # the tail
    d.line([(2, 16), (2, 28)], fill=OUT, width=2)
    _outlined_text(d, (4, 19), "FEDS", (255, 255, 255, 255))
    d.line([(20, 36), (40, 36)], fill=OUT, width=2)                                                     # skids
    d.line([(24, 33), (24, 36)], fill=OUT)
    d.line([(36, 33), (36, 36)], fill=OUT)
    d.ellipse([38, 30, 44, 35], fill=(255, 255, 180, 255), outline=OUT)                                # the light
    return im


def spotlight(size=64):
    """A tall cone of searchlight (translucent yellow-white), widening downward."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = im.load()
    for y in range(size):
        half = 3 + y * .42
        for x in range(size):
            dx = abs(x - 31.5)
            if dx < half:
                a = int(150 * (1 - dx / half) ** .5 * min(1, y / 6))
                px[x, y] = (255, 250, 190, a)
    return im


def past_due(size=64):
    """A bill: white sheet, lines of print, PAST DUE stamped in red (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (30, 30, 40, 255)
    d.rectangle([14, 12, 49, 52], fill=(252, 252, 255, 255), outline=OUT)
    for k, y in enumerate((16, 19, 22, 46, 49)):
        d.line([(17, y), (46 - (k % 2) * 8, y)], fill=(150, 160, 190, 255))
    d.rectangle([16, 26, 47, 42], outline=(220, 25, 30, 255))
    for k, word in enumerate(("PAST", "DUE")):
        m = _text_mask(word)
        im.paste((220, 25, 30, 255), (32 - m.width // 2, 28 + k * 7), m)
    return im


def milk_carton(size=64):
    """A gallon of milk: white jug, blue cap, a handle (no label text: it gets tipped)."""
    im, d, S = _big(size)
    OUT, WHITE, SHADE = (30, 40, 60, 255), (250, 250, 255, 255), (200, 210, 230, 255)
    d.rounded_rectangle([S * .22, S * .3, S * .78, S * .94], 20, fill=WHITE, outline=OUT, width=9)
    d.polygon([(S * .3, S * .3), (S * .4, S * .14), (S * .6, S * .14), (S * .7, S * .3)], fill=WHITE, outline=OUT)
    d.rectangle([S * .4, S * .04, S * .6, S * .16], fill=(60, 120, 230, 255), outline=OUT, width=7)   # the cap
    d.rounded_rectangle([S * .64, S * .34, S * .86, S * .6], 12, outline=OUT, width=9)                # the handle
    d.rectangle([S * .3, S * .5, S * .7, S * .7], fill=(80, 140, 240, 255), outline=OUT, width=6)     # blue band
    d.line([(S * .28, S * .36), (S * .28, S * .88)], fill=SHADE, width=8)
    return _shrink(im, size)


def rock_chunk(size=32):
    """A lumpy grey pebble with a lighter top (lobbed)."""
    im, d, S = _big(size)
    OUT = (25, 25, 30, 255)
    d.polygon([(S * .2, S * .5), (S * .34, S * .3), (S * .62, S * .28), (S * .8, S * .44), (S * .76, S * .68),
               (S * .5, S * .76), (S * .26, S * .7)], fill=(140, 135, 130, 255), outline=OUT)
    d.line([(S * .2, S * .5), (S * .34, S * .3), (S * .62, S * .28), (S * .8, S * .44), (S * .76, S * .68),
            (S * .5, S * .76), (S * .26, S * .7), (S * .2, S * .5)], fill=OUT, width=6)
    d.polygon([(S * .34, S * .36), (S * .6, S * .34), (S * .68, S * .46), (S * .4, S * .48)], fill=(200, 195, 190, 255))
    return _shrink(im, size)


def nine_volt_lick(size=64):
    """A tongue on the 9-volt's terminals - ZAP: the battery (9V on it), a pink tongue on the snaps, sparks
    flying off (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    bat = nine_volt(32).resize((32, 32), Image.NEAREST)
    im.alpha_composite(bat, (16, 26))
    d = ImageDraw.Draw(im)
    OUT = (90, 20, 40, 255)
    d.ellipse([20, 4, 44, 18], fill=(60, 15, 25, 255), outline=OUT)                                    # the mouth
    d.arc([20, 4, 44, 18], 200, 340, fill=(200, 90, 90, 255), width=2)
    d.arc([20, 4, 44, 18], 20, 160, fill=(200, 90, 90, 255), width=2)
    d.rounded_rectangle([26, 10, 38, 31], 6, fill=(245, 120, 150, 255), outline=OUT)                   # the tongue
    d.line([(32, 13), (32, 27)], fill=(205, 75, 105, 255))
    for x0, y0, x1, y1 in ((20, 18, 12, 10), (44, 20, 54, 12), (22, 30, 10, 32), (44, 28, 56, 30), (32, 16, 32, 6)):
        mx, my = (x0 + x1) // 2 + 2, (y0 + y1) // 2 - 2                                                # zig-zag sparks
        d.line([(x0, y0), (mx, my), (x1, y1)], fill=(255, 240, 60, 255), width=2)
    return im


def process_server(size=64):
    """A process server bursting out of a hedge: slicked hair, wide crazy eyes and a big grin, dark suit, white
    shirt, red tie, one arm up waving a manila envelope."""
    im, d, S = _big(size)
    OUT, SUIT, SUIT_L, SKIN, HAIR = (10, 10, 12, 255), (45, 50, 70, 255), (90, 100, 130, 255), (235, 175, 125, 255), (40, 25, 15, 255)
    BUSH, BUSH_L = (50, 140, 50, 255), (110, 200, 90, 255)
    d.polygon([(S * .2, S * .62), (S * .3, S * .4), (S * .7, S * .4), (S * .8, S * .62)], fill=SUIT, outline=OUT)   # shoulders
    d.line([(S * .2, S * .62), (S * .3, S * .4), (S * .7, S * .4), (S * .8, S * .62)], fill=OUT, width=9)
    d.polygon([(S * .42, S * .4), (S * .58, S * .4), (S * .5, S * .62)], fill=(250, 250, 250, 255))  # the shirt
    d.polygon([(S * .47, S * .42), (S * .53, S * .42), (S * .51, S * .6), (S * .49, S * .6)], fill=(220, 30, 40, 255))  # tie
    d.line([(S * .42, S * .4), (S * .48, S * .52)], fill=SUIT_L, width=6)                               # lapels
    d.line([(S * .58, S * .4), (S * .52, S * .52)], fill=SUIT_L, width=6)
    d.line([(S * .74, S * .46), (S * .86, S * .2)], fill=OUT, width=24)                                 # the arm up
    d.line([(S * .74, S * .46), (S * .86, S * .2)], fill=SUIT, width=16)
    d.ellipse([S * .8, S * .12, S * .92, S * .24], fill=SKIN, outline=OUT, width=6)                    # the hand
    d.rectangle([S * .74, S * .0, S * .99, S * .16], fill=(235, 200, 120, 255), outline=OUT, width=7)  # the papers
    d.line([(S * .78, S * .06), (S * .95, S * .06)], fill=(160, 120, 60, 255), width=5)
    d.ellipse([S * .32, S * .06, S * .66, S * .42], fill=SKIN, outline=OUT, width=8)                    # the head
    d.chord([S * .3, S * .02, S * .68, S * .26], 180, 360, fill=HAIR, outline=OUT, width=7)             # slicked hair
    for x in (.38, .52):                                                                                # crazy eyes
        d.ellipse([S * x, S * .16, S * (x + .1), S * .26], fill=(255, 255, 255, 255), outline=OUT, width=4)
        d.ellipse([S * (x + .03), S * .19, S * (x + .07), S * .23], fill=OUT)
    for x in (.37, .53):
        d.line([(S * x, S * .14), (S * (x + .1), S * .12)], fill=HAIR, width=5)                         # eyebrows up
    d.chord([S * .39, S * .28, S * .61, S * .38], 0, 180, fill=(255, 255, 255, 255), outline=OUT, width=5)  # grin
    import random
    rnd = random.Random(2)
    for _ in range(16):                                                                                 # the hedge
        x, y, r = rnd.uniform(.08, .92) * S, rnd.uniform(.62, .92) * S, rnd.uniform(.09, .14) * S
        d.ellipse([x - r, y - r, x + r, y + r], fill=BUSH, outline=OUT, width=6)
    for _ in range(7):
        x, y = rnd.uniform(.12, .88) * S, rnd.uniform(.62, .86) * S
        d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=BUSH_L)
    return _shrink(im, size)


def pa_speaker(size=64):
    """A tall PA speaker on a tripod stand: black cabinet, a tweeter horn up top, a big woofer cone."""
    im, d, S = _big(size)
    OUT, BLACK, GREY = (8, 8, 10, 255), (35, 35, 40, 255), (90, 90, 100, 255)
    d.line([(S * .5, S * .62), (S * .5, S * .86)], fill=GREY, width=10)                               # the stand
    for x in (.3, .7):
        d.line([(S * .5, S * .84), (S * x, S * .98)], fill=GREY, width=9)
    d.rounded_rectangle([S * .26, S * .02, S * .74, S * .66], 14, fill=BLACK, outline=OUT, width=9)   # the cabinet
    d.rectangle([S * .36, S * .08, S * .64, S * .2], fill=(60, 60, 68, 255), outline=OUT, width=6)    # tweeter horn
    d.ellipse([S * .32, S * .26, S * .68, S * .62], fill=(70, 70, 78, 255), outline=OUT, width=8)     # the woofer
    d.ellipse([S * .38, S * .32, S * .62, S * .56], fill=(45, 45, 52, 255), outline=(110, 110, 120, 255), width=5)
    d.ellipse([S * .46, S * .4, S * .54, S * .48], fill=(130, 130, 140, 255))
    d.line([(S * .3, S * .06), (S * .3, S * .6)], fill=(70, 70, 80, 255), width=5)
    return _shrink(im, size)


def eighth_notes(w=16, h=32):
    """A pair of beamed eighth notes (alpha only), tall."""
    def f(x, y):
        y -= 6
        if 1 <= x <= 5 and 15 <= y <= 19 and ((x - 3) ** 2 + (y - 17) ** 2) < 5.5:
            return 1
        if 9 <= x <= 13 and 13 <= y <= 17 and ((x - 11) ** 2 + (y - 15) ** 2) < 5.5:
            return 1
        if 4 <= x <= 5 and 2 <= y <= 17:
            return 1
        if 12 <= x <= 13 and 0 <= y <= 15:
            return 1
        if 4 <= x <= 13 and abs(y - (2 - (x - 4) * 2 / 9)) < 1.3:
            return 1
        return 0
    return _alpha(w, h, f)


def spit_fleck(n=16):
    """A streak of spit flying up-right at about the aim angle: a droplet with a trail (alpha only)."""
    import math
    a = math.radians(-26)
    ux, uy = math.cos(a), math.sin(a)

    def f(x, y):
        px, py = x - 7.5, y - 7.5
        along, across = px * ux + py * uy, -px * uy + py * ux
        if along > 2.5 or along < -6.5:
            return 0
        if (along - 1.3) ** 2 + across ** 2 < 2.2:
            return 1
        return max(0, (1 - abs(across) / 1.0)) * (along + 6.5) / 8 if along < 1.3 else 0
    return _alpha(n, n, f)


# ---- set 11 ------------------------------------------------------------------------------------------------
def diving_board(size=64):
    """A pool diving board sticking out to the right: white plank with grip tape, the springboard base and
    ladder rails at the back."""
    im, d, S = _big(size)
    OUT, WHITE, BLUE, STEEL = (20, 25, 40, 255), (245, 248, 255, 255), (60, 140, 230, 255), (180, 185, 200, 255)
    for x in (.08, .2):                                                                                # ladder rails
        d.line([(S * x, S * .3), (S * x, S * .98)], fill=OUT, width=14)
        d.line([(S * x, S * .3), (S * x, S * .98)], fill=STEEL, width=8)
        d.arc([S * (x - .06), S * .22, S * (x + .06), S * .38], 180, 360, fill=STEEL, width=8)
    for y in (.56, .72, .88):
        d.line([(S * .08, S * y), (S * .2, S * y)], fill=STEEL, width=8)
    d.polygon([(S * .22, S * .6), (S * .46, S * .6), (S * .4, S * .98), (S * .28, S * .98)], fill=BLUE, outline=OUT)  # base
    d.line([(S * .22, S * .6), (S * .46, S * .6), (S * .4, S * .98), (S * .28, S * .98), (S * .22, S * .6)], fill=OUT,
           width=8)
    d.polygon([(S * .14, S * .5), (S * .98, S * .44), (S * .98, S * .52), (S * .14, S * .6)], fill=WHITE)   # the board
    d.line([(S * .14, S * .5), (S * .98, S * .44), (S * .98, S * .52), (S * .14, S * .6), (S * .14, S * .5)], fill=OUT,
           width=8)
    d.line([(S * .5, S * .49), (S * .94, S * .46)], fill=(120, 140, 170, 255), width=6)                 # grip tape
    return _shrink(im, size)


def splash_crown_big(size=64):
    """A huge belly-flop splash: a wall of water exploding up and out, foam on top, drops flying."""
    import math
    import random
    im, d, S = _big(size)
    rnd = random.Random(21)
    OUT, BLUE, BLUE_L, FOAM = (20, 60, 140, 255), (60, 150, 255, 255), (150, 210, 255, 255), (240, 250, 255, 255)
    pts = [(S * .04, S * .96)]
    for k in range(13):                                                                                # the crown
        x = S * (.08 + k * .07)
        tip = S * (.1 + .25 * abs(math.sin(k * 1.7)) + (.0 if k % 2 else .18))
        pts += [(x, tip), (x + S * .035, S * (.5 + rnd.uniform(0, .1)))]
    pts += [(S * .96, S * .96)]
    d.polygon(pts, fill=BLUE, outline=OUT)
    d.line(pts, fill=OUT, width=7)
    inner = [(x, y + (S * .96 - y) * .3) for x, y in pts]
    d.polygon(inner, fill=BLUE_L)
    for x, y in pts[1:-1:2]:                                                                           # foam tips
        d.ellipse([x - S * .04, y - S * .03, x + S * .04, y + S * .05], fill=FOAM, outline=OUT, width=4)
    for _ in range(9):                                                                                 # drops
        x, y, r = rnd.uniform(.05, .95) * S, rnd.uniform(.0, .3) * S, rnd.uniform(.015, .03) * S
        d.ellipse([x - r, y - r, x + r, y + r], fill=BLUE_L, outline=OUT, width=3)
    d.rectangle([S * .04, S * .86, S * .96, S * .96], fill=FOAM, outline=OUT, width=6)               # foam floor
    return _shrink(im, size)


def pigeon(size=64, wings_up=True):
    """A fat city pigeon flying right: grey body, shiny green-purple neck, orange eye, wings up or down."""
    im, d, S = _big(size)
    OUT, G, GL, GD = (20, 20, 25, 255), (150, 155, 170, 255), (200, 205, 215, 255), (95, 100, 115, 255)
    d.polygon([(S * .06, S * .5), (S * .22, S * .42), (S * .26, S * .6), (S * .06, S * .62)], fill=GD, outline=OUT)  # tail
    d.ellipse([S * .18, S * .36, S * .72, S * .7], fill=G, outline=OUT, width=9)                       # the body
    d.ellipse([S * .3, S * .5, S * .66, S * .68], fill=GL)
    d.ellipse([S * .58, S * .26, S * .84, S * .5], fill=G, outline=OUT, width=8)                       # the head
    d.chord([S * .56, S * .38, S * .8, S * .58], 0, 180, fill=(110, 170, 140, 255))                    # neck sheen
    d.chord([S * .58, S * .42, S * .76, S * .56], 0, 180, fill=(150, 110, 190, 255))
    d.polygon([(S * .82, S * .36), (S * .96, S * .4), (S * .82, S * .44)], fill=(60, 50, 50, 255), outline=OUT)   # beak
    d.ellipse([S * .7, S * .32, S * .78, S * .4], fill=(255, 140, 30, 255), outline=OUT, width=3)    # the eye
    d.ellipse([S * .73, S * .34, S * .76, S * .38], fill=OUT)
    if wings_up:                                                                                       # the wing
        d.polygon([(S * .32, S * .44), (S * .2, S * .04), (S * .48, S * .12), (S * .58, S * .44)], fill=GD, outline=OUT)
        for k in range(3):
            d.line([(S * (.26 + k * .08), S * .1), (S * (.4 + k * .05), S * .42)], fill=OUT, width=4)
    else:
        d.polygon([(S * .32, S * .5), (S * .16, S * .92), (S * .46, S * .86), (S * .58, S * .52)], fill=GD, outline=OUT)
        for k in range(3):
            d.line([(S * (.22 + k * .08), S * .86), (S * (.4 + k * .05), S * .54)], fill=OUT, width=4)
    for x in (.4, .48):                                                                                # feet
        d.line([(S * x, S * .68), (S * (x - .02), S * .76)], fill=(230, 120, 120, 255), width=6)
    return _shrink(im, size)


def poop_splat(size=64):
    """A fat white bird-dropping splat with a grey center and drips running down."""
    import math
    import random
    im, d, S = _big(size)
    rnd = random.Random(8)
    OUT, WHITE, GREY = (90, 90, 100, 255), (250, 250, 245, 255), (170, 170, 160, 255)
    pts = []
    for k in range(16):
        a = k * math.tau / 16
        r = S * (.2 + (.1 if k % 2 else 0) + rnd.uniform(0, .04))
        pts.append((S * .5 + r * math.cos(a), S * .4 + r * .7 * math.sin(a)))
    d.polygon(pts, fill=WHITE, outline=OUT)
    d.line(pts + [pts[0]], fill=OUT, width=6)
    for x, ln in ((.38, .3), (.52, .44), (.62, .24)):                                                  # drips
        d.rounded_rectangle([S * (x - .035), S * .42, S * (x + .035), S * (.42 + ln)], 12, fill=WHITE, outline=OUT,
                            width=5)
    d.ellipse([S * .42, S * .32, S * .58, S * .46], fill=GREY)
    d.ellipse([S * .46, S * .35, S * .52, S * .41], fill=(120, 120, 110, 255))
    return _shrink(im, size)


def glob_drop(n=16):
    """A falling glob, fat at the bottom (alpha only)."""
    def f(x, y):
        if ((x - 7.5) / 3.6) ** 2 + ((y - 10) / 3.6) ** 2 < 1:
            return 1
        return 1 if 3 <= y < 10 and abs(x - 7.5) < (y - 3) * .5 else 0
    return _alpha(n, n, f)


def beach_chair(size=64):
    """A striped low beach chair, reclined."""
    im, d, S = _big(size)
    OUT, WOOD = (25, 20, 15, 255), (190, 140, 80, 255)
    d.line([(S * .12, S * .96), (S * .3, S * .56)], fill=WOOD, width=14)                               # legs
    d.line([(S * .9, S * .96), (S * .62, S * .62)], fill=WOOD, width=14)
    d.polygon([(S * .2, S * .6), (S * .72, S * .64), (S * .66, S * .76), (S * .16, S * .7)], fill=(250, 250, 250, 255),
              outline=OUT)                                                                              # the seat
    d.polygon([(S * .66, S * .66), (S * .9, S * .14), (S * .98, S * .2), (S * .76, S * .72)], fill=(250, 250, 250, 255),
              outline=OUT)                                                                              # the back
    for k in range(3):                                                                                 # stripes
        t = (k + .5) / 3.5
        d.line([(S * (.7 + .24 * t), S * (.62 - .48 * t)), (S * (.78 + .2 * t), S * (.7 - .5 * t))],
               fill=(240, 60, 70, 255), width=12)
        x = S * (.24 + k * .16)
        d.line([(x, S * .62), (x - S * .02, S * .72)], fill=(60, 140, 240, 255), width=12)
    d.line([(S * .2, S * .6), (S * .72, S * .64), (S * .98, S * .2)], fill=OUT, width=7)
    return _shrink(im, size)


def tan_reflector(size=64):
    """A fold-out foil tanning reflector, held up under the chin: three shiny panels."""
    im, d, S = _big(size)
    OUT = (40, 45, 60, 255)
    for k, (x0, sh) in enumerate(((.06, (170, 180, 200, 255)), (.36, (235, 240, 255, 255)), (.66, (170, 180, 200, 255)))):
        d.polygon([(S * x0, S * (.3 if k != 1 else .26)), (S * (x0 + .3), S * (.26 if k != 0 else .3)),
                   (S * (x0 + .3), S * (.74 if k != 0 else .7)), (S * x0, S * (.7 if k != 1 else .74))],
                  fill=sh, outline=OUT)
        d.line([(S * (x0 + .05), S * .36), (S * (x0 + .12), S * .62)], fill=(255, 255, 255, 255), width=6)   # glare
    d.line([(S * .36, S * .26), (S * .36, S * .74)], fill=OUT, width=6)
    d.line([(S * .66, S * .26), (S * .66, S * .74)], fill=OUT, width=6)
    return _shrink(im, size)


def cool_sun(size=64):
    """A blazing cartoon sun wearing shades, smirking."""
    import math
    im, d, S = _big(size)
    OUT, Y, YL, OR = (120, 60, 0, 255), (255, 210, 40, 255), (255, 245, 150, 255), (255, 140, 20, 255)
    for k in range(12):                                                                                # rays
        a = k * math.tau / 12
        r0, r1 = S * .3, S * (.48 if k % 2 else .42)
        w = .12
        d.polygon([(S * .5 + r0 * math.cos(a - w), S * .5 + r0 * math.sin(a - w)), (S * .5 + r1 * math.cos(a), S * .5 + r1 * math.sin(a)),
                   (S * .5 + r0 * math.cos(a + w), S * .5 + r0 * math.sin(a + w))], fill=OR, outline=OUT)
    d.ellipse([S * .2, S * .2, S * .8, S * .8], fill=Y, outline=OUT, width=10)
    d.arc([S * .26, S * .26, S * .6, S * .6], 200, 260, fill=YL, width=10)
    d.rounded_rectangle([S * .28, S * .38, S * .48, S * .5], 8, fill=(20, 20, 26, 255))                 # the shades
    d.rounded_rectangle([S * .52, S * .38, S * .72, S * .5], 8, fill=(20, 20, 26, 255))
    d.line([(S * .46, S * .42), (S * .54, S * .42)], fill=(20, 20, 26, 255), width=6)
    d.line([(S * .32, S * .41), (S * .38, S * .41)], fill=(120, 130, 160, 255), width=4)
    d.arc([S * .38, S * .5, S * .66, S * .68], 10, 150, fill=OUT, width=8)                             # smirk
    return _shrink(im, size)


def heat_wave(w=16, h=32):
    """Two wobbly rising heat lines (alpha only)."""
    import math

    def f(x, y):
        for cx in (5, 11):
            if abs(x - (cx + 1.6 * math.sin(y / 2.6 + cx))) < .8 and 3 <= y <= h - 3:
                return .9
        return 0
    return _alpha(w, h, f)


def grill_smile(size=64):
    """A huge grinning mouth flashing a full gold grill, diamonds in two teeth (shown big over their face)."""
    im, d, S = _big(size)
    OUT, LIP, GOLD, GOLD_L, GOLD_D = (40, 15, 15, 255), (170, 70, 70, 255), (255, 200, 40, 255), (255, 245, 170, 255), (190, 130, 20, 255)
    d.chord([S * .04, S * .14, S * .96, S * .9], 0, 180, fill=LIP, outline=OUT, width=10)              # lower lip
    d.chord([S * .04, S * .1, S * .96, S * .5], 180, 360, fill=LIP, outline=OUT, width=10)              # upper lip
    d.rectangle([S * .1, S * .28, S * .9, S * .62], fill=(60, 20, 20, 255))
    for row, (y0, y1) in enumerate(((.28, .44), (.46, .62))):                                          # the grill
        for k in range(7):
            x = S * (.12 + k * .11)
            d.rectangle([x, S * y0, x + S * .1, S * y1], fill=GOLD, outline=GOLD_D, width=4)
            d.line([(x + S * .02, S * (y0 + .02)), (x + S * .02, S * (y1 - .03))], fill=GOLD_L, width=4)
    for x, y in ((.35, .32), (.68, .5)):                                                               # diamonds
        d.polygon([(S * x, S * y), (S * (x + .03), S * (y + .04)), (S * x, S * (y + .08)), (S * (x - .03), S * (y + .04))],
                  fill=(220, 250, 255, 255), outline=(120, 180, 220, 255))
    return _shrink(im, size)


def light_ray(size=64):
    """A long wedge of blinding light, bright at the narrow end (rotate it to sweep)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = im.load()
    for x in range(size):
        half = 1 + x * .16
        for y in range(size):
            dy = abs(y - 31.5)
            if dy < half:
                a = int(220 * (1 - x / size * .6) * (1 - dy / half) ** .6)
                px[x, y] = (255, 250, 200, a)
    return im


def sweat_bead(n=16):
    """A nervous sweat drop (alpha only), a highlight."""
    def f(x, y):
        r = (((x - 7.5) / 3.6) ** 2 + ((y - 10) / 3.8) ** 2) ** .5
        if r < 1:
            return .6 if (x - 6.5) ** 2 + (y - 9) ** 2 < 1.5 else 1
        return 1 if 2 <= y < 9 and abs(x - 7.5) < (y - 2) * .5 else 0
    return _alpha(n, n, f)


def car_trunk_subs(size=64):
    """The back of a candy-red car, trunk popped: a wall of four subwoofers inside, tail lights, rims."""
    im, d, S = _big(size)
    OUT, RED, RED_L, RED_D = (15, 8, 8, 255), (200, 30, 50, 255), (255, 110, 120, 255), (130, 15, 30, 255)
    d.polygon([(S * .14, S * .02), (S * .86, S * .02), (S * .9, S * .3), (S * .1, S * .3)], fill=RED_D, outline=OUT)   # the lid
    d.line([(S * .14, S * .02), (S * .86, S * .02), (S * .9, S * .3), (S * .1, S * .3), (S * .14, S * .02)], fill=OUT,
           width=8)
    d.rectangle([S * .04, S * .3, S * .96, S * .82], fill=RED, outline=OUT, width=9)                  # the body
    d.rectangle([S * .1, S * .34, S * .9, S * .66], fill=(40, 40, 46, 255), outline=OUT, width=7)     # the box
    for k in range(4):                                                                                 # the subs
        x = S * (.2 + k * .2)
        d.ellipse([x - S * .085, S * .38, x + S * .085, S * .62], fill=(70, 70, 78, 255), outline=OUT, width=6)
        d.ellipse([x - S * .05, S * .44, x + S * .05, S * .56], fill=(25, 25, 30, 255), outline=(140, 140, 150, 255), width=4)
        d.ellipse([x - S * .018, S * .48, x + S * .018, S * .52], fill=(160, 160, 170, 255))
    for x in (.04, .84):                                                                               # tail lights
        d.rectangle([S * x, S * .68, S * (x + .12), S * .78], fill=(255, 60, 60, 255), outline=OUT, width=5)
    d.rectangle([S * .38, S * .7, S * .62, S * .78], fill=(240, 220, 120, 255), outline=OUT, width=5)  # plate
    d.line([(S * .08, S * .32), (S * .92, S * .32)], fill=RED_L, width=6)
    for x in (.18, .82):                                                                               # tires + rims
        d.ellipse([S * (x - .13), S * .74, S * (x + .13), S * .99], fill=(25, 25, 30, 255), outline=OUT, width=7)
        d.ellipse([S * (x - .07), S * .8, S * (x + .07), S * .94], fill=(255, 210, 60, 255), outline=OUT, width=5)
    return _shrink(im, size)


def bass_ring(n=16):
    """A thick throbbing ring (alpha only)."""
    c = (n - 1) / 2
    return _alpha(n, n, lambda x, y: 1.2 - abs(((x - c) ** 2 + (y - c) ** 2) ** .5 - 5.6) / 1.5)


def feather(n=16):
    """A loose feather drifting (alpha only): a quill with vanes."""
    def f(x, y):
        u, v = (x - 7.5) * .8 + (y - 7.5) * .6, -(x - 7.5) * .6 + (y - 7.5) * .8
        if abs(v) < .5 and -6.5 < u < 6.5:
            return 1
        if -4.5 < u < 6 and abs(v) < 2.6 * (1 - abs(u - .7) / 5.6):
            return .65
        return 0
    return _alpha(n, n, f)


def hooptie_rear(size=64):
    """A beat-up hooptie from the back, facing away to the left: one tail light out, primer patches, a bungee
    cord holding the trunk shut, a rusty tailpipe sticking out on the right with duct tape."""
    im, d, S = _big(size)
    OUT, TEAL, TEAL_D, PRIMER, RUST = (15, 15, 15, 255), (90, 150, 140, 255), (55, 100, 95, 255), (150, 150, 145, 255), (160, 80, 30, 255)
    d.polygon([(S * .14, S * .2), (S * .82, S * .2), (S * .9, S * .4), (S * .06, S * .4)], fill=TEAL_D, outline=OUT)   # the roof/glass
    d.polygon([(S * .2, S * .24), (S * .76, S * .24), (S * .82, S * .38), (S * .14, S * .38)], fill=(120, 160, 190, 255))
    d.line([(S * .3, S * .26), (S * .6, S * .36)], fill=OUT, width=4)                                  # cracked glass
    d.rectangle([S * .02, S * .4, S * .94, S * .78], fill=TEAL, outline=OUT, width=9)                 # the body
    d.rectangle([S * .56, S * .44, S * .84, S * .6], fill=PRIMER)                                      # primer patch
    d.ellipse([S * .14, S * .62, S * .26, S * .7], fill=RUST)                                          # rust
    d.rectangle([S * .04, S * .46, S * .16, S * .56], fill=(255, 60, 60, 255), outline=OUT, width=5)  # one tail light
    d.rectangle([S * .8, S * .46, S * .92, S * .56], fill=(60, 50, 50, 255), outline=OUT, width=5)    # (busted)
    d.line([(S * .3, S * .4), (S * .36, S * .7)], fill=(240, 60, 60, 255), width=6)                    # the bungee
    d.rectangle([S * .4, S * .62, S * .58, S * .7], fill=(240, 220, 120, 255), outline=OUT, width=5)  # plate
    d.rectangle([S * .82, S * .76, S * 1.0, S * .84], fill=(120, 110, 100, 255), outline=OUT, width=6)  # tailpipe
    d.rectangle([S * .88, S * .75, S * .93, S * .85], fill=(180, 180, 190, 255))                      # duct tape
    for x in (.18, .76):                                                                               # bald tires
        d.rectangle([S * (x - .1), S * .78, S * (x + .1), S * .98], fill=(30, 30, 34, 255), outline=OUT, width=7)
    return _shrink(im, size)


def soot_puff(n=16):
    """A lumpy black exhaust cloud (alpha only)."""
    def f(x, y):
        v = 0
        for cx, cy, r in ((5, 9, 4), (10, 7, 4.4), (8, 11, 3.8), (11, 11, 3)):
            v = max(v, 1.35 - ((x - cx) ** 2 + (y - cy) ** 2) ** .5 / r)
        return v
    return _alpha(n, n, f)


def backfire(w=16, h=32):
    """A jagged backfire flash (alpha only), tall."""
    import math
    c = (w - 1) / 2

    def f(x, y):
        dx, dy = (x - c) / 7, (y - 15.5) / 14
        r = (dx * dx + dy * dy) ** .5
        a = math.atan2(dy, dx)
        return 1 if r < .55 + .4 * abs(math.cos(a * 4)) else 0
    return _alpha(w, h, f)


def riot_shield(size=64):
    """A clear riot shield: FEDS stenciled on it, crossed out in red marker, MINE scrawled over it (1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (20, 30, 50, 255)
    d.rounded_rectangle([12, 2, 51, 62], 6, fill=(160, 200, 240, 150), outline=OUT)
    d.rounded_rectangle([14, 4, 49, 60], 5, outline=(230, 245, 255, 220))
    d.line([(16, 8), (20, 56)], fill=(240, 250, 255, 220), width=2)                                    # glare
    m = _text_mask("FEDS")
    im.paste((25, 30, 45, 255), (32 - m.width // 2, 16), m)
    d.line([(20, 15), (44, 24)], fill=(230, 30, 30, 255), width=2)                                     # crossed out
    d.line([(20, 24), (44, 15)], fill=(230, 30, 30, 255), width=2)
    m = _text_mask("MINE")
    im.paste((230, 30, 30, 255), (32 - m.width // 2, 30), m)
    d.line([(21, 38), (43, 37)], fill=(230, 30, 30, 255))                                              # underlined
    d.rectangle([28, 46, 36, 50], fill=(70, 70, 80, 255), outline=OUT)                                 # the grip
    return im


def tomato(size=32):
    """A ripe red tomato with a green stem (thrown)."""
    im, d, S = _big(size)
    OUT = (80, 10, 10, 255)
    d.ellipse([S * .14, S * .24, S * .86, S * .9], fill=(230, 40, 40, 255), outline=OUT, width=7)
    d.arc([S * .24, S * .32, S * .6, S * .66], 200, 260, fill=(255, 150, 140, 255), width=8)
    d.polygon([(S * .5, S * .26), (S * .32, S * .16), (S * .44, S * .3), (S * .58, S * .14), (S * .56, S * .3),
               (S * .72, S * .2)], fill=(70, 170, 60, 255), outline=(20, 60, 20, 255))
    return _shrink(im, size)


def tomato_splat(size=64):
    """A tomato splattered flat on glass: red pulp, seeds, drips running down."""
    import math
    import random
    im, d, S = _big(size)
    rnd = random.Random(31)
    OUT, RED, RED_L = (90, 10, 10, 255), (220, 40, 40, 255), (255, 120, 110, 255)
    pts = []
    for k in range(18):
        a = k * math.tau / 18
        r = S * (.16 + (.12 if k % 2 else 0) + rnd.uniform(0, .05))
        pts.append((S * .5 + r * math.cos(a), S * .4 + r * math.sin(a)))
    d.polygon(pts, fill=RED, outline=OUT)
    d.line(pts + [pts[0]], fill=OUT, width=6)
    for x, ln in ((.4, .3), (.56, .4)):
        d.rounded_rectangle([S * (x - .03), S * .44, S * (x + .03), S * (.44 + ln)], 10, fill=RED, outline=OUT, width=4)
    d.ellipse([S * .4, S * .3, S * .6, S * .48], fill=RED_L)
    for _ in range(6):                                                                                 # seeds
        x, y = rnd.uniform(.38, .62) * S, rnd.uniform(.3, .5) * S
        d.ellipse([x - 6, y - 4, x + 6, y + 4], fill=(255, 230, 150, 255))
    return _shrink(im, size)


def phone_signal(size=64, bars=0):
    """A phone held up, screen showing the signal: no bars and an X, or full bars and wifi (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (8, 8, 10, 255)
    d.rounded_rectangle([20, 6, 43, 58], 4, fill=(30, 30, 36, 255), outline=OUT)
    d.rectangle([22, 11, 41, 51], fill=(40, 60, 90, 255) if not bars else (90, 200, 120, 255))
    for k in range(4):                                                                                 # the bars
        x, h = 24 + k * 4, 4 + k * 4
        d.rectangle([x, 44 - h, x + 2, 44], fill=(255, 255, 255, 255) if bars else (80, 90, 110, 255))
    if not bars:
        d.line([(26, 18), (37, 29)], fill=(240, 50, 50, 255), width=3)
        d.line([(37, 18), (26, 29)], fill=(240, 50, 50, 255), width=3)
    else:
        for r in (4, 8, 12):                                                                           # wifi
            d.arc([31.5 - r, 28 - r, 31.5 + r, 28 + r], 220, 320, fill=(255, 255, 255, 255), width=2)
        d.ellipse([30, 26, 33, 29], fill=(255, 255, 255, 255))
    d.rectangle([29, 54, 34, 55], fill=(90, 90, 100, 255))
    return im


def wifi_arc(n=16):
    """A wifi wave: a fat arc opening to the right (alpha only)."""
    import math

    def f(x, y):
        r = ((x - 2) ** 2 + (y - 7.5) ** 2) ** .5
        a = abs(math.degrees(math.atan2(y - 7.5, x - 2)))
        return 1 if abs(r - 9) < 1.5 and a < 50 else 0
    return _alpha(n, n, f)


def store_glass(size=64, closed=False):
    """Corner-store bulletproof glass: thick plexi in a steel frame, the lazy-susan tray at the bottom, a little
    placard hanging: OPEN / CLOSED (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT, STEEL = (20, 22, 30, 255), (150, 155, 170, 255)
    d.rectangle([4, 2, 59, 60], fill=STEEL, outline=OUT)
    d.rectangle([8, 6, 55, 50], fill=(170, 210, 235, 140), outline=OUT)                                # the glass
    for x, y in ((14, 10), (20, 10), (14, 16)):                                                        # glare
        d.line([(x, y + 14), (x + 8, y)], fill=(240, 250, 255, 200), width=2)
    d.rectangle([4, 50, 59, 60], fill=(120, 125, 140, 255), outline=OUT)                               # the counter
    d.ellipse([22, 51, 42, 59], fill=(200, 200, 210, 255), outline=OUT)                                # lazy susan
    d.rectangle([20, 29, 43, 38], fill=(255, 255, 255, 255) if not closed else (230, 40, 40, 255), outline=OUT)
    d.line([(31, 24), (27, 30)], fill=OUT)                                                             # the string
    d.line([(31, 24), (36, 30)], fill=OUT)
    word = "OPEN" if not closed else "SHUT"
    m = _text_mask(word)
    im.paste((30, 120, 40, 255) if not closed else (255, 255, 255, 255), (32 - m.width // 2, 31), m)
    return im


def crack_star(n=16):
    """A spidery impact crack (alpha only)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = x - c, y - c
        r = (dx * dx + dy * dy) ** .5
        if r < 1.2:
            return 1
        a = math.degrees(math.atan2(dy, dx)) % 360
        for ang in (10, 70, 135, 190, 250, 310):
            if abs((a - ang + 180) % 360 - 180) < 5 and r < 7.5:
                return 1
        return 1 if abs(r - 4.5) < .5 and int(a / 30) % 2 else 0
    return _alpha(n, n, f)


def punch_clock(size=64):
    """A wall punch clock: a clock face, the card slot, a time card sticking out (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (20, 20, 25, 255)
    d.rounded_rectangle([14, 6, 49, 56], 4, fill=(110, 120, 135, 255), outline=OUT)
    d.ellipse([20, 10, 43, 33], fill=(250, 250, 240, 255), outline=OUT)                                # the face
    d.line([(31, 21), (31, 13)], fill=OUT)
    d.line([(31, 21), (37, 24)], fill=OUT)
    d.rectangle([20, 38, 43, 41], fill=(30, 30, 35, 255))                                              # the slot
    d.rectangle([24, 34, 39, 52], fill=(240, 220, 160, 255), outline=OUT)                              # the card
    for y in (44, 47):
        d.line([(26, y), (37, y)], fill=(170, 140, 80, 255))
    m = _text_mask("IN")
    im.paste((210, 30, 30, 255), (32 - m.width // 2, 36), m)
    return im


def crescent_moon(size=64):
    """A fat yellow crescent moon with a sleepy closed eye."""
    im, d, S = _big(size)
    OUT = (90, 70, 10, 255)
    d.ellipse([S * .1, S * .1, S * .9, S * .9], fill=(255, 230, 120, 255), outline=OUT, width=10)
    d.ellipse([S * .34, S * .02, S * 1.06, S * .78], fill=(0, 0, 0, 0))
    im2 = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d2 = ImageDraw.Draw(im2)
    d2.ellipse([S * .34, S * .02, S * 1.06, S * .78], fill=(255, 255, 255, 255))
    im.paste((0, 0, 0, 0), (0, 0), im2)
    d = ImageDraw.Draw(im)
    d.arc([S * .34, S * .02, S * 1.06, S * .78], 100, 230, fill=OUT, width=10)
    d.arc([S * .2, S * .44, S * .34, S * .56], 0, 180, fill=OUT, width=7)                              # sleepy eye
    return _shrink(im, size)


def mop(size=64):
    """A wet mop: a long wooden handle, the grey string head flopped out to the right."""
    im, d, S = _big(size)
    OUT, WOOD, GREY = (30, 20, 10, 255), (200, 150, 90, 255), (190, 190, 180, 255)
    d.line([(S * .1, S * .06), (S * .56, S * .66)], fill=OUT, width=18)                                # the handle
    d.line([(S * .1, S * .06), (S * .56, S * .66)], fill=WOOD, width=10)
    d.rectangle([S * .5, S * .6, S * .66, S * .7], fill=(90, 100, 120, 255), outline=OUT, width=6)    # the clamp
    for k in range(9):                                                                                 # the strings
        a = S * (.5 + k * .05)
        d.line([(S * .58, S * .68), (a + S * .1, S * (.9 + (k % 3) * .03))], fill=OUT, width=12)
        d.line([(S * .58, S * .68), (a + S * .1, S * (.9 + (k % 3) * .03))], fill=GREY, width=7)
    return _shrink(im, size)


def wet_floor_sign(size=64):
    """The yellow A-frame WET FLOOR sign with the little slipping man (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT, Y = (30, 25, 10, 255), (255, 215, 30, 255)
    d.polygon([(24, 4), (40, 4), (50, 60), (14, 60)], fill=Y, outline=OUT)
    d.rectangle([28, 0, 36, 4], fill=Y, outline=OUT)                                                   # the handle
    for k, word in enumerate(("WET", "FLOOR")):
        m = _text_mask(word)
        im.paste(OUT, (32 - m.width // 2, 10 + k * 8), m)
    d.ellipse([28, 30, 33, 35], fill=OUT)                                                              # the slipping man
    d.line([(30, 35), (34, 44)], fill=OUT, width=2)
    d.line([(32, 39), (25, 37)], fill=OUT, width=2)
    d.line([(32, 39), (38, 35)], fill=OUT, width=2)
    d.line([(34, 44), (40, 42)], fill=OUT, width=2)
    d.line([(34, 44), (28, 50)], fill=OUT, width=2)
    d.line([(20, 54), (44, 54)], fill=OUT)
    return im


def puddle(n=16):
    """A flat shiny puddle (alpha only)."""
    def f(x, y):
        r = ((x - 7.5) / 7) ** 2 + ((y - 10) / 3) ** 2
        return 0 if r > 1 else (.6 if ((x - 5) / 2.5) ** 2 + ((y - 9) / 1) ** 2 < 1 else .9)
    return _alpha(n, n, f)


def ceiling_fan(size=64, angle=0):
    """A cheap ceiling fan seen a little from below: the downrod from the top, the motor, the light globe, four
    wooden blades (angle: how far the blades have turned, for the spin poses)."""
    import math
    im, d, S = _big(size)
    OUT, WOOD, WOOD_L, BRASS = (25, 15, 5, 255), (150, 95, 45, 255), (200, 140, 80, 255), (210, 170, 70, 255)
    d.line([(S * .5, S * .0), (S * .5, S * .34)], fill=OUT, width=14)                                  # the downrod
    d.line([(S * .5, S * .0), (S * .5, S * .34)], fill=BRASS, width=8)
    for k in range(4):                                                                                 # the blades
        a = math.radians(angle + k * 90)
        ux, uy = math.cos(a), math.sin(a) * .35
        px, py = -uy, ux * .35
        cx, cy = S * .5, S * .44
        tip = (cx + ux * S * .48, cy + uy * S * .48)
        root = (cx + ux * S * .1, cy + uy * S * .1)
        wdt = S * .09
        poly = [(root[0] + px * wdt, root[1] + py * wdt * 3), (tip[0] + px * wdt * 1.3, tip[1] + py * wdt * 3.6),
                (tip[0] - px * wdt * 1.3, tip[1] - py * wdt * 3.6), (root[0] - px * wdt, root[1] - py * wdt * 3)]
        d.polygon(poly, fill=WOOD if k % 2 else WOOD_L, outline=OUT)
        d.line(poly + [poly[0]], fill=OUT, width=6)
    d.ellipse([S * .36, S * .32, S * .64, S * .52], fill=BRASS, outline=OUT, width=8)                 # the motor
    d.ellipse([S * .42, S * .5, S * .58, S * .66], fill=(255, 250, 220, 255), outline=OUT, width=6)    # the globe
    d.line([(S * .56, S * .54), (S * .6, S * .78)], fill=OUT, width=4)                                 # pull chain
    d.ellipse([S * .58, S * .76, S * .63, S * .81], fill=BRASS)
    return _shrink(im, size)


def fan_blade(size=32):
    """One wooden fan blade, ripped off, flying (spinning)."""
    im, d, S = _big(size)
    OUT = (25, 15, 5, 255)
    d.polygon([(S * .1, S * .42), (S * .9, S * .3), (S * .96, S * .5), (S * .9, S * .7), (S * .1, S * .58)],
              fill=(160, 100, 50, 255), outline=OUT)
    d.line([(S * .1, S * .42), (S * .9, S * .3), (S * .96, S * .5), (S * .9, S * .7), (S * .1, S * .58), (S * .1, S * .42)],
           fill=OUT, width=6)
    d.rectangle([S * .04, S * .4, S * .18, S * .6], fill=(210, 170, 70, 255), outline=OUT, width=5)   # the bracket
    d.line([(S * .2, S * .46), (S * .86, S * .4)], fill=(210, 150, 90, 255), width=5)
    return _shrink(im, size)


def whoosh_arc(n=16):
    """A curved motion swoosh (alpha only)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        r = ((x - c) ** 2 + (y - c) ** 2) ** .5
        a = math.degrees(math.atan2(y - c, x - c)) % 360
        return (1 - a / 140) if abs(r - 6) < .9 and a < 140 else 0
    return _alpha(n, n, f)


def bic_lighter(size=64):
    """A cheap red lighter held upright, thumb wheel and the metal hood up top, a spark flying off."""
    im, d, S = _big(size)
    OUT, RED, RED_L, STEEL = (30, 8, 8, 255), (220, 40, 50, 255), (255, 130, 130, 255), (190, 195, 205, 255)
    d.rounded_rectangle([S * .36, S * .3, S * .64, S * .96], 18, fill=RED, outline=OUT, width=9)
    d.line([(S * .42, S * .36), (S * .42, S * .9)], fill=RED_L, width=8)
    d.rectangle([S * .36, S * .14, S * .64, S * .32], fill=STEEL, outline=OUT, width=8)               # the hood
    for x in (.42, .5, .58):
        d.ellipse([S * (x - .02), S * .18, S * (x + .02), S * .22], fill=OUT)
    d.ellipse([S * .3, S * .2, S * .44, S * .34], fill=(120, 120, 130, 255), outline=OUT, width=6)    # the wheel
    d.rectangle([S * .56, S * .3, S * .66, S * .42], fill=(240, 240, 240, 255), outline=OUT, width=5)  # the button
    return _shrink(im, size)


def tiny_spark(n=16):
    """A tiny 4-point spark (alpha only)."""
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = abs(x - c), abs(y - c)
        return 1 if (dx < .6 and dy < 5) or (dy < .6 and dx < 5) or dx + dy < 1.8 else 0
    return _alpha(n, n, f)


def cash_register(size=64, open_=False):
    """An old cash register: the price display, keys, the cash drawer shut - or shot open full of bills."""
    im, d, S = _big(size)
    OUT, BODY, BODY_L, KEY = (20, 20, 25, 255), (90, 95, 110, 255), (150, 155, 175, 255), (240, 240, 230, 255)
    d.rectangle([S * .3, S * .02, S * .7, S * .2], fill=(30, 30, 35, 255), outline=OUT, width=8)      # the display
    d.rectangle([S * .34, S * .06, S * .66, S * .16], fill=(60, 220, 90, 255))
    d.polygon([(S * .1, S * .24), (S * .9, S * .24), (S * .96, S * .64), (S * .04, S * .64)], fill=BODY, outline=OUT)
    d.line([(S * .1, S * .24), (S * .9, S * .24), (S * .96, S * .64), (S * .04, S * .64), (S * .1, S * .24)], fill=OUT,
           width=9)
    for r in range(3):                                                                                 # the keys
        for k in range(6):
            x, y = S * (.16 + k * .12 + r * .01), S * (.3 + r * .1)
            d.rectangle([x, y, x + S * .08, y + S * .07], fill=KEY, outline=OUT, width=4)
    d.rectangle([S * .04, S * .64, S * .96, S * .8], fill=BODY_L, outline=OUT, width=8)               # the drawer
    if open_:
        d.rectangle([S * .0, S * .78, S * 1.0, S * .98], fill=BODY_L, outline=OUT, width=8)
        for k in range(5):                                                                             # bills
            x = S * (.06 + k * .18)
            d.rectangle([x, S * .8, x + S * .14, S * .9], fill=(110, 200, 100, 255), outline=(30, 90, 30, 255), width=4)
    d.ellipse([S * .46, S * .68, S * .54, S * .76], fill=(60, 60, 70, 255))
    return _shrink(im, size)


def receipt_strip(size=64):
    """A long strip of receipt paper running across, lines of print, a dotted tear edge (rotate it to wrap)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (120, 120, 130, 255)
    d.rectangle([0, 25, 63, 38], fill=(252, 252, 248, 255), outline=OUT)
    for x in range(3, 62, 6):                                                                          # print
        d.line([(x, 29), (x + 3, 29)], fill=(110, 110, 130, 255))
        d.line([(x + 1, 33), (x + 4, 33)], fill=(110, 110, 130, 255))
    for x in range(0, 64, 2):
        d.point((x, 38), fill=(200, 200, 205, 255))
    return im


def dime(n=16):
    """A small coin (alpha only), a rim."""
    def f(x, y):
        r = (((x - 7.5) / 4.5) ** 2 + ((y - 7.5) / 4.5) ** 2) ** .5
        return 0 if r > 1 else (.7 if r < .6 else 1)
    return _alpha(n, n, f)


def mud_tub(size=64):
    """A wooden spa tub full of bubbling mud, a rolled towel on the rim."""
    im, d, S = _big(size)
    OUT, WOOD, WOOD_D, MUD, MUD_L = (35, 20, 8, 255), (190, 130, 70, 255), (140, 90, 45, 255), (110, 75, 45, 255), (150, 110, 70, 255)
    d.rounded_rectangle([S * .04, S * .44, S * .96, S * .96], 20, fill=WOOD, outline=OUT, width=9)
    for x in (.24, .44, .64, .84):                                                                     # staves
        d.line([(S * x, S * .5), (S * x, S * .92)], fill=WOOD_D, width=6)
    for y in (.58, .82):                                                                               # hoops
        d.line([(S * .04, S * y), (S * .96, S * y)], fill=(80, 80, 90, 255), width=8)
    d.ellipse([S * .04, S * .36, S * .96, S * .54], fill=MUD, outline=OUT, width=9)                   # the mud
    for x, y in ((.3, .44), (.56, .42), (.74, .46)):                                                   # bubbles
        d.ellipse([S * (x - .04), S * (y - .03), S * (x + .04), S * (y + .03)], fill=MUD_L, outline=OUT, width=4)
    d.rounded_rectangle([S * .7, S * .3, S * .98, S * .42], 14, fill=(250, 250, 255, 255), outline=OUT, width=6)   # towel
    return _shrink(im, size)


def spa_face(size=64):
    """Spa gear worn on their head: a white towel turban, two cucumber slices over the eyes (shown at 1:1)."""
    im, d, S = _big(size)
    OUT, WHITE, SHADE = (40, 45, 60, 255), (250, 250, 255, 255), (200, 205, 220, 255)
    d.chord([S * .14, S * .0, S * .86, S * .56], 180, 360, fill=WHITE, outline=OUT, width=9)           # the turban
    d.rectangle([S * .14, S * .26, S * .86, S * .36], fill=WHITE, outline=OUT, width=8)
    for k in range(3):
        d.arc([S * (.2 + k * .18), S * .06, S * (.44 + k * .18), S * .34], 200, 330, fill=SHADE, width=8)
    for x in (.24, .56):                                                                               # cucumbers
        d.ellipse([S * x, S * .46, S * (x + .2), S * .66], fill=(110, 190, 80, 255), outline=(40, 100, 30, 255), width=7)
        d.ellipse([S * (x + .03), S * .49, S * (x + .17), S * .63], fill=(210, 245, 190, 255))
        for k in range(3):
            d.ellipse([S * (x + .07 + k * .03), S * .55, S * (x + .08 + k * .03), S * .57], fill=(150, 200, 120, 255))
    return _shrink(im, size)


def steam_wisp(w=16, h=32):
    """A soft curling wisp of steam (alpha only)."""
    import math

    def f(x, y):
        cx = 7.5 + 2.6 * math.sin(y / 4)
        fade = min(1, (h - y) / 8, y / 4)
        return max(0, 1.1 - abs(x - cx) / 2.6) * fade * .8
    return _alpha(w, h, f)


def hype_man(size=64):
    """The hype man: snapback, gold chain, mouth wide open yelling into a megaphone pointed up-right."""
    im, d, S = _big(size)
    OUT, SKIN, SHIRT, CAP, GOLD = (15, 10, 8, 255), (150, 95, 60, 255), (230, 40, 40, 255), (30, 30, 36, 255), (255, 205, 40, 255)
    d.rounded_rectangle([S * .14, S * .56, S * .66, S * .98], 20, fill=SHIRT, outline=OUT, width=9)   # the tee
    for k in range(7):                                                                                 # the chain
        d.ellipse([S * (.26 + k * .04), S * (.6 + abs(k - 3) * -.01 + .04), S * (.3 + k * .04), S * (.64 + abs(k - 3) * -.01 + .04)],
                  outline=GOLD, width=6)
    d.ellipse([S * .2, S * .2, S * .58, S * .6], fill=SKIN, outline=OUT, width=9)                      # the head
    d.chord([S * .18, S * .14, S * .6, S * .42], 180, 360, fill=CAP, outline=OUT, width=8)              # snapback
    d.rectangle([S * .16, S * .3, S * .7, S * .36], fill=CAP, outline=OUT, width=6)                    # (brim)
    d.ellipse([S * .28, S * .4, S * .36, S * .46], fill=(255, 255, 255, 255), outline=OUT, width=3)    # the eyes
    d.ellipse([S * .42, S * .4, S * .5, S * .46], fill=(255, 255, 255, 255), outline=OUT, width=3)
    d.ellipse([S * .34, S * .48, S * .48, S * .58], fill=(80, 20, 20, 255), outline=OUT, width=5)     # yelling
    d.polygon([(S * .46, S * .5), (S * .9, S * .18), (S * .98, S * .3), (S * .56, S * .58)], fill=(250, 250, 250, 255),
              outline=OUT)                                                                              # megaphone
    d.line([(S * .46, S * .5), (S * .9, S * .18), (S * .98, S * .3), (S * .56, S * .58), (S * .46, S * .5)], fill=OUT,
           width=7)
    d.line([(S * .9, S * .18), (S * .98, S * .3)], fill=(230, 40, 40, 255), width=10)
    return _shrink(im, size)


def foam_finger(size=64):
    """A giant foam #1 finger (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT, F, F_D = (20, 20, 40, 255), (40, 110, 230, 255), (25, 70, 170, 255)
    d.rounded_rectangle([28, 2, 38, 30], 4, fill=F, outline=OUT)                                       # the finger
    d.rounded_rectangle([16, 24, 46, 52], 6, fill=F, outline=OUT)                                      # the fist
    for y in (30, 36, 42):
        d.line([(18, y), (27, y)], fill=F_D)
    d.rectangle([20, 52, 42, 62], fill=F_D, outline=OUT)                                               # the cuff
    m = _text_mask("#1")
    im.paste((255, 255, 255, 255), (32 - m.width // 2, 36), m)
    return im


def confetti(n=16):
    """A twisty strip of confetti (alpha only)."""
    def f(x, y):
        u, v = (x - 7.5) * .7 + (y - 7.5) * .7, -(x - 7.5) * .7 + (y - 7.5) * .7
        return 1 if abs(u) < 4 and abs(v) < 1.5 else 0
    return _alpha(n, n, f)


# ---- set 12 ------------------------------------------------------------------------------------------------
def fidget_spinner(size=64):
    """A big gold fidget spinner: three round lobes with chrome bearings, the center cap (spin it)."""
    import math
    im, d, S = _big(size)
    OUT, GOLD, GOLD_L, GOLD_D, CHROME = (60, 35, 5, 255), (255, 200, 40, 255), (255, 240, 150, 255), (200, 140, 20, 255), (200, 205, 215, 255)
    pts = [(S * .5 + S * .3 * math.cos(math.radians(a)), S * .5 + S * .3 * math.sin(math.radians(a))) for a in (-90, 30, 150)]
    for (x, y) in pts:                                                                                 # the arms
        d.line([(S * .5, S * .5), (x, y)], fill=OUT, width=int(S * .26))
        d.line([(S * .5, S * .5), (x, y)], fill=GOLD, width=int(S * .2))
    for (x, y) in pts:                                                                                 # the lobes
        d.ellipse([x - S * .17, y - S * .17, x + S * .17, y + S * .17], fill=GOLD, outline=OUT, width=9)
        d.ellipse([x - S * .1, y - S * .1, x + S * .1, y + S * .1], fill=CHROME, outline=OUT, width=6)
        d.ellipse([x - S * .04, y - S * .04, x + S * .04, y + S * .04], fill=(120, 125, 135, 255))
        d.arc([x - S * .14, y - S * .14, x + S * .14, y + S * .14], 200, 260, fill=GOLD_L, width=6)
    d.ellipse([S * .38, S * .38, S * .62, S * .62], fill=GOLD_D, outline=OUT, width=8)                # the cap
    d.ellipse([S * .44, S * .44, S * .56, S * .56], fill=GOLD_L)
    return _shrink(im, size)


def neon_sign(size=64, lit=True):
    """A corner-store neon sign: LIQUOR in pink tube letters over a blue tube border, on a dark backing
    (unlit: grey dead tubes). Shown at 2:1."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (10, 10, 20, 255)
    d.rounded_rectangle([6, 18, 57, 45], 3, fill=(25, 20, 40, 255), outline=OUT)
    border = (60, 200, 255, 255) if lit else (70, 75, 90, 255)
    glow = (40, 100, 160, 255) if lit else (40, 38, 55, 255)
    d.rounded_rectangle([8, 20, 55, 43], 3, outline=glow)
    d.rounded_rectangle([9, 21, 54, 42], 3, outline=border)
    pink, pink_glow = ((255, 90, 200, 255), (160, 50, 130, 255)) if lit else ((95, 90, 105, 255), (50, 46, 62, 255))
    m = _text_mask("LIQUOR")
    x0 = 32 - m.width // 2
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx or dy:
                im.paste(pink_glow, (x0 + dx, 28 + dy), m)
    im.paste(pink, (x0, 28), m)
    for x in (16, 47):                                                                                 # hanging chains
        d.line([(x, 8), (x, 18)], fill=(120, 120, 130, 255))
    return im


def glow_dot(n=16):
    """A soft glowing dot with a hot core (alpha only)."""
    c = (n - 1) / 2
    return _alpha(n, n, lambda x, y: 1.25 - ((x - c) ** 2 + (y - c) ** 2) ** .5 / 6)


def tos_book(size=64, open_=False):
    """The most boring book ever: a thick TERMS & CONDITIONS binder (closed), or open on pages of tiny print
    (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (20, 25, 40, 255)
    if not open_:
        d.rectangle([12, 6, 51, 58], fill=(60, 80, 140, 255), outline=OUT)                             # the cover
        d.rectangle([12, 6, 17, 58], fill=(40, 55, 100, 255), outline=OUT)                             # the spine
        d.rectangle([47, 8, 52, 57], fill=(245, 245, 235, 255), outline=OUT)                           # pages edge
        for k, word in enumerate(("TERMS", "&", "CONDI-", "TIONS")):
            m = _text_mask(word)
            im.paste((255, 255, 255, 255), (32 - m.width // 2, 13 + k * 8), m)
        d.rectangle([20, 47, 44, 52], fill=(250, 220, 60, 255))                                        # "VOL. 37"
        m = _text_mask("V37")
        im.paste(OUT, (32 - m.width // 2, 47), m)
    else:
        d.polygon([(4, 14), (31, 18), (31, 56), (4, 52)], fill=(250, 250, 240, 255), outline=OUT)      # left page
        d.polygon([(33, 18), (60, 14), (60, 52), (33, 56)], fill=(250, 250, 240, 255), outline=OUT)    # right page
        for k in range(9):                                                                             # tiny print
            y = 22 + k * 3.6
            d.line([(7, y), (28, y + 1)], fill=(150, 150, 170, 255))
            d.line([(36, y + 1), (57, y)], fill=(150, 150, 170, 255))
        d.line([(32, 18), (32, 56)], fill=OUT, width=2)
    return im


def cologne_bottle(size=64):
    """A fancy cologne bottle pointing right: a chunky purple glass body, a gold collar, the atomizer nozzle."""
    im, d, S = _big(size)
    OUT, GLASS, GLASS_L, GOLD = (25, 10, 35, 255), (150, 70, 210, 230), (220, 180, 255, 255), (255, 205, 60, 255)
    d.rounded_rectangle([S * .1, S * .28, S * .62, S * .86], 22, fill=GLASS, outline=OUT, width=10)
    d.rounded_rectangle([S * .18, S * .52, S * .54, S * .8], 16, fill=(110, 40, 170, 230))             # the juice
    d.line([(S * .18, S * .36), (S * .18, S * .76)], fill=GLASS_L, width=8)
    d.rectangle([S * .62, S * .44, S * .74, S * .62], fill=GOLD, outline=OUT, width=7)                # the collar
    d.rectangle([S * .74, S * .48, S * .86, S * .58], fill=(30, 30, 35, 255), outline=OUT, width=6)  # the nozzle
    d.ellipse([S * .3, S * .1, S * .52, S * .3], fill=GOLD, outline=OUT, width=7)                      # the bulb cap
    d.rectangle([S * .22, S * .4, S * .5, S * .48], fill=GOLD, outline=OUT, width=5)                  # gold label
    return _shrink(im, size)


def bmx_bike(size=64):
    """A kid's BMX side-on, riding right: little wheels with pegs, a banana seat, handlebar streamers."""
    im, d, S = _big(size)
    OUT, RED, RED_L = (15, 10, 10, 255), (230, 50, 60, 255), (255, 130, 140, 255)
    for x in (.22, .78):                                                                               # wheels
        d.ellipse([S * (x - .18), S * .5, S * (x + .18), S * .86], fill=(0, 0, 0, 0), outline=OUT, width=12)
        d.ellipse([S * (x - .15), S * .53, S * (x + .15), S * .83], outline=(180, 180, 190, 255), width=4)
        d.ellipse([S * (x - .03), S * .65, S * (x + .03), S * .71], fill=OUT)
        d.rectangle([S * (x - .06), S * .66, S * (x + .06), S * .7], fill=(200, 200, 210, 255))       # pegs
    for a, b in (((.22, .68), (.46, .44)), ((.46, .44), (.72, .44)), ((.46, .44), (.5, .68)), ((.22, .68), (.5, .68)),
                 ((.72, .44), (.78, .68))):                                                            # the frame
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=OUT, width=14)
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=RED, width=8)
    d.rounded_rectangle([S * .3, S * .36, S * .52, S * .42], 10, fill=(250, 220, 60, 255), outline=OUT, width=5)  # banana seat
    d.line([(S * .72, S * .44), (S * .76, S * .2)], fill=OUT, width=10)                                # the stem
    d.line([(S * .66, S * .18), (S * .86, S * .2)], fill=OUT, width=10)                                # the bars
    for k, col in enumerate(((255, 80, 200, 255), (80, 220, 255, 255), (255, 230, 60, 255))):          # streamers
        d.line([(S * .66, S * .18), (S * (.52 - k * .04), S * (.12 + k * .05))], fill=col, width=5)
    d.ellipse([S * .44, S * .62, S * .56, S * .74], fill=RED_L, outline=OUT, width=5)                 # the crank
    return _shrink(im, size)
