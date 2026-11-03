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


# ---- set 13: Lugia's moves (legendary - over the top) ---------------------------------------------------------
def fighter_jet(size=64):
    """A grey fighter jet side-on, nose to the right: swept wings, the tail fin, canopy, afterburner glow."""
    im, d, S = _big(size)
    OUT, G, GL, GD = (15, 18, 25, 255), (150, 160, 175, 255), (210, 218, 230, 255), (95, 105, 120, 255)
    d.polygon([(S * .14, S * .46), (S * .82, S * .44), (S * .98, S * .5), (S * .82, S * .56), (S * .14, S * .56)],
              fill=G, outline=OUT)                                                                       # fuselage
    d.line([(S * .14, S * .46), (S * .82, S * .44), (S * .98, S * .5), (S * .82, S * .56), (S * .14, S * .56),
            (S * .14, S * .46)], fill=OUT, width=7)
    d.polygon([(S * .38, S * .54), (S * .62, S * .54), (S * .36, S * .82), (S * .26, S * .82)], fill=GD, outline=OUT)  # wing
    d.polygon([(S * .16, S * .46), (S * .3, S * .46), (S * .18, S * .2), (S * .1, S * .2)], fill=GD, outline=OUT)      # tail fin
    d.polygon([(S * .14, S * .54), (S * .26, S * .54), (S * .16, S * .64), (S * .08, S * .64)], fill=GD, outline=OUT)  # stabilizer
    d.chord([S * .56, S * .36, S * .82, S * .54], 180, 360, fill=(90, 170, 255, 255), outline=OUT, width=6)          # canopy
    d.line([(S * .62, S * .42), (S * .74, S * .41)], fill=(220, 240, 255, 255), width=4)
    d.line([(S * .2, S * .48), (S * .8, S * .47)], fill=GL, width=5)
    d.ellipse([S * .0, S * .45, S * .16, S * .57], fill=(255, 160, 40, 255), outline=(255, 240, 160, 255), width=4)  # burner
    return _shrink(im, size)


def contrail(n=16):
    """A soft streak of contrail (alpha only), long and thin."""
    def f(x, y):
        return max(0, 1 - abs(y - 7.5) / 3) * (.5 + .5 * x / 15)
    return _alpha(n, n, f)


def mega_sneaker(size=64):
    """A GIANT crispy white low-top sneaker side-on, toe to the right: gum sole, the tongue sticking up, crossed
    laces, a red heel tab and side stripe, not a crease on it."""
    im, d, S = _big(size)
    OUT, WHITE, SHADE, GUM, RED = (25, 25, 30, 255), (252, 252, 255, 255), (205, 210, 225, 255), (205, 150, 80, 255), (220, 40, 50, 255)
    d.polygon([(S * .34, S * .36), (S * .38, S * .16), (S * .5, S * .18), (S * .5, S * .38)], fill=WHITE, outline=OUT)  # tongue
    d.line([(S * .34, S * .36), (S * .38, S * .16), (S * .5, S * .18), (S * .5, S * .38)], fill=OUT, width=7)
    up = [(S * .05, S * .72), (S * .05, S * .34), (S * .18, S * .28), (S * .3, S * .36), (S * .38, S * .32),
          (S * .62, S * .48), (S * .86, S * .54), (S * .97, S * .66), (S * .97, S * .72)]
    d.polygon(up, fill=WHITE)
    d.line(up, fill=OUT, width=8)
    d.polygon([(S * .05, S * .4), (S * .14, S * .34), (S * .14, S * .64), (S * .05, S * .66)], fill=RED)     # heel tab
    d.line([(S * .24, S * .64), (S * .44, S * .5), (S * .7, S * .58)], fill=OUT, width=14)                 # side stripe
    d.line([(S * .24, S * .64), (S * .44, S * .5), (S * .7, S * .58)], fill=RED, width=8)
    d.arc([S * .62, S * .5, S * 1.0, S * .84], 200, 270, fill=SHADE, width=7)                           # toe box
    for k in range(4):                                                                                 # laces
        x, y = S * (.4 + k * .055), S * (.36 + k * .035)
        d.line([(x - S * .03, y - S * .02), (x + S * .03, y + S * .03)], fill=OUT, width=6)
        d.line([(x - S * .03, y + S * .03), (x + S * .03, y - S * .02)], fill=OUT, width=6)
    d.rounded_rectangle([S * .02, S * .7, S * .99, S * .88], 18, fill=GUM, outline=OUT, width=9)      # gum sole
    d.line([(S * .06, S * .82), (S * .95, S * .82)], fill=(170, 115, 55, 255), width=5)
    for k in range(15):                                                                                # stitching
        d.point((S * (.08 + k * .058), S * .67), fill=(170, 175, 190, 255))
    return _shrink(im, size)


def shock_ring(n=16):
    """A flattened shockwave ring along the ground (alpha only)."""
    def f(x, y):
        r = (((x - 7.5) / 7) ** 2 + ((y - 7.5) / 3) ** 2) ** .5
        return max(0, 1 - abs(r - .85) / .15)
    return _alpha(n, n, f)


def sky_eye(size=64, state=0):
    """A giant eye in the sky: 0 closed (a lashed lid), 1 half open, 2 wide open looking down-right."""
    im, d, S = _big(size)
    OUT, LID, WHITE, IRIS = (30, 10, 50, 255), (130, 70, 200, 255), (250, 245, 255, 255), (230, 40, 180, 255)
    box = [S * .04, S * .26, S * .96, S * .74]
    if state == 0:
        d.chord(box, 180, 360, fill=LID, outline=OUT, width=10)
        d.line([(S * .04, S * .5), (S * .96, S * .5)], fill=OUT, width=10)
        for k in range(7):                                                                             # lashes
            x = S * (.14 + k * .12)
            d.line([(x, S * .5), (x - S * .03, S * .64)], fill=OUT, width=8)
    else:
        d.ellipse(box if state == 2 else [S * .04, S * .36, S * .96, S * .64], fill=WHITE, outline=OUT, width=10)
        ir = S * (.18 if state == 2 else .12)
        cx, cy = S * .58, S * (.56 if state == 2 else .52)
        d.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], fill=IRIS, outline=OUT, width=7)
        d.ellipse([cx - ir * .45, cy - ir * .45, cx + ir * .45, cy + ir * .45], fill=OUT)
        d.ellipse([cx - ir * .7, cy - ir * .7, cx - ir * .3, cy - ir * .3], fill=WHITE)
        if state == 1:
            d.chord([S * .04, S * .2, S * .96, S * .6], 180, 360, fill=LID, outline=OUT, width=10)
        for k in range(7):                                                                             # lashes up
            x = S * (.14 + k * .12)
            y = S * (.26 if state == 2 else .36)
            d.line([(x, y + S * .02), (x - S * .02, y - S * .1)], fill=OUT, width=8)
        for a in range(4):                                                                             # veins
            d.line([(S * (.12 + a * .02), S * .46), (S * (.22 + a * .03), S * .5)], fill=(230, 120, 140, 255), width=3)
    return _shrink(im, size)


def crystal_ball(size=64):
    """A glowing crystal ball on a gold stand, purple mist swirling inside - and in it, a tiny tombstone."""
    im, d, S = _big(size)
    OUT, GOLD = (30, 15, 45, 255), (230, 180, 60, 255)
    d.polygon([(S * .26, S * .96), (S * .74, S * .96), (S * .64, S * .78), (S * .36, S * .78)], fill=GOLD, outline=OUT)
    d.line([(S * .26, S * .96), (S * .74, S * .96), (S * .64, S * .78), (S * .36, S * .78), (S * .26, S * .96)],
           fill=OUT, width=8)
    d.ellipse([S * .12, S * .1, S * .88, S * .84], fill=(150, 90, 230, 210), outline=OUT, width=10)
    d.ellipse([S * .2, S * .18, S * .8, S * .76], fill=(190, 140, 255, 200))
    d.arc([S * .22, S * .2, S * .7, S * .66], 120, 300, fill=(230, 200, 255, 255), width=10)          # swirl
    d.rounded_rectangle([S * .42, S * .36, S * .58, S * .58], 14, fill=(170, 170, 180, 255), outline=OUT, width=6)  # tomb
    d.line([(S * .5, S * .4), (S * .5, S * .5)], fill=OUT, width=5)
    d.line([(S * .45, S * .44), (S * .55, S * .44)], fill=OUT, width=5)
    d.ellipse([S * .26, S * .2, S * .4, S * .32], fill=(255, 255, 255, 230))                           # shine
    return _shrink(im, size)


def tarot_death(size=32):
    """A tarot card flying: purple back border, a skull on it (the Death card)."""
    im, d, S = _big(size)
    OUT = (25, 10, 35, 255)
    d.rounded_rectangle([S * .22, S * .04, S * .78, S * .96], 10, fill=(250, 240, 210, 255), outline=OUT, width=7)
    d.rounded_rectangle([S * .28, S * .1, S * .72, S * .9], 6, outline=(150, 70, 200, 255), width=6)
    d.ellipse([S * .34, S * .26, S * .66, S * .56], fill=(250, 250, 250, 255), outline=OUT, width=6)  # skull
    d.rectangle([S * .4, S * .52, S * .6, S * .64], fill=(250, 250, 250, 255), outline=OUT, width=5)
    for x in (.42, .54):
        d.ellipse([S * x, S * .36, S * (x + .06), S * .44], fill=OUT)
    d.line([(S * .34, S * .76), (S * .66, S * .76)], fill=(150, 70, 200, 255), width=6)
    return _shrink(im, size)


def psy_ring(n=16):
    """A double psychic ring (alpha only)."""
    c = (n - 1) / 2

    def f(x, y):
        r = ((x - c) ** 2 + (y - c) ** 2) ** .5
        return 1 if abs(r - 6.4) < .8 or abs(r - 3.6) < .6 else 0
    return _alpha(n, n, f)


def glint_tall(w=16, h=32):
    """A tall 4-point glint (alpha only): a star sparkle on something brand new."""
    def f(x, y):
        dx, dy = abs(x - 7.5), abs(y - 15.5)
        return 1 if (dx < .7 and dy < 14) or (dy < .7 and dx < 7) or dx * 2 + dy < 4 else 0
    return _alpha(w, h, f)


# ---- set 14 ------------------------------------------------------------------------------------------------
def wind_teeth(size=64, open_=True):
    """Gold wind-up chattering teeth on little orange feet, a wind-up key on the back: open, or chomped shut."""
    im, d, S = _big(size)
    OUT, GOLD, GOLD_L, GOLD_D, GUM = (60, 30, 5, 255), (255, 200, 40, 255), (255, 240, 150, 255), (190, 130, 20, 255), (230, 90, 110, 255)
    d.rectangle([S * .06, S * .44, S * .16, S * .52], fill=(200, 200, 210, 255), outline=OUT, width=5)  # the key
    d.ellipse([S * .0, S * .3, S * .12, S * .44], outline=(200, 200, 210, 255), width=8)
    d.ellipse([S * .0, S * .48, S * .12, S * .62], outline=(200, 200, 210, 255), width=8)
    for x in (.32, .66):                                                                               # feet
        d.ellipse([S * (x - .1), S * .86, S * (x + .1), S * .98], fill=(255, 130, 30, 255), outline=OUT, width=6)
    gap = .16 if open_ else .0
    top_y, bot_y = .5 - gap, .5 + gap
    d.chord([S * .14, S * (top_y - .32), S * .94, S * (top_y + .16)], 0, 180, fill=GUM, outline=OUT, width=8)   # upper gum
    d.chord([S * .14, S * (bot_y - .14), S * .94, S * (bot_y + .34)], 180, 360, fill=GUM, outline=OUT, width=8)  # lower gum
    for k in range(6):                                                                                 # gold teeth
        x = S * (.2 + k * .115)
        d.rectangle([x, S * (top_y - .02), x + S * .1, S * (top_y + .1)], fill=GOLD, outline=GOLD_D, width=4)
        d.rectangle([x, S * (bot_y - .1), x + S * .1, S * (bot_y + .02)], fill=GOLD, outline=GOLD_D, width=4)
        d.line([(x + S * .02, S * (top_y + .0)), (x + S * .02, S * (top_y + .06))], fill=GOLD_L, width=4)
    if open_:
        d.rectangle([S * .2, S * (top_y + .1), S * .88, S * (bot_y - .1)], fill=(80, 20, 30, 255))
    return _shrink(im, size)


def dish_towel(size=64):
    """A checkered dish towel being whipped round (rotate it)."""
    im, d, S = _big(size)
    OUT = (40, 20, 20, 255)
    d.polygon([(S * .1, S * .3), (S * .9, S * .2), (S * .94, S * .56), (S * .14, S * .72)], fill=(250, 250, 250, 255), outline=OUT)
    for r in range(4):
        for c in range(6):
            if (r + c) % 2:
                x0, y0 = S * (.14 + c * .13), S * (.3 + r * .1 - c * .016)
                d.polygon([(x0, y0), (x0 + S * .13, y0 - S * .016), (x0 + S * .13, y0 + S * .084), (x0, y0 + S * .1)],
                          fill=(220, 50, 60, 255))
    d.line([(S * .1, S * .3), (S * .9, S * .2), (S * .94, S * .56), (S * .14, S * .72), (S * .1, S * .3)], fill=OUT, width=7)
    return _shrink(im, size)


def air_freshener(size=64):
    """An air freshener spray can, nozzle on top, a tropical flower on the label (no text: it's held at an angle)."""
    im, d, S = _big(size)
    OUT = (20, 30, 30, 255)
    d.rounded_rectangle([S * .3, S * .24, S * .7, S * .94], 14, fill=(60, 200, 190, 255), outline=OUT, width=9)
    d.rectangle([S * .36, S * .12, S * .64, S * .26], fill=(240, 240, 240, 255), outline=OUT, width=7)  # the cap
    d.rectangle([S * .46, S * .04, S * .56, S * .14], fill=(250, 250, 250, 255), outline=OUT, width=6)
    d.ellipse([S * .36, S * .44, S * .64, S * .72], fill=(255, 250, 240, 255), outline=OUT, width=6)    # the label
    for k in range(5):                                                                                 # a flower
        import math
        a = k * math.tau / 5
        x, y = S * .5 + S * .07 * math.cos(a), S * .58 + S * .07 * math.sin(a)
        d.ellipse([x - S * .05, y - S * .05, x + S * .05, y + S * .05], fill=(255, 90, 160, 255))
    d.ellipse([S * .47, S * .55, S * .53, S * .61], fill=(255, 220, 60, 255))
    d.line([(S * .34, S * .3), (S * .34, S * .88)], fill=(170, 250, 240, 255), width=6)
    return _shrink(im, size)


def couch(size=64):
    """A beat-up brown couch shoved in, side-on: cushions, an arm, a rip with stuffing poking out."""
    im, d, S = _big(size)
    OUT, BROWN, BROWN_L, BROWN_D = (35, 20, 10, 255), (150, 95, 55, 255), (195, 140, 95, 255), (105, 65, 35, 255)
    d.rounded_rectangle([S * .04, S * .3, S * .96, S * .58], 24, fill=BROWN_D, outline=OUT, width=9)  # back
    d.rounded_rectangle([S * .04, S * .5, S * .96, S * .82], 18, fill=BROWN, outline=OUT, width=9)    # seat
    for x in (.04, .82):
        d.rounded_rectangle([S * x, S * .42, S * (x + .14), S * .84], 18, fill=BROWN_D, outline=OUT, width=8)  # arms
    for x in (.18, .5):
        d.rounded_rectangle([S * x, S * .52, S * (x + .32), S * .68], 14, fill=BROWN_L, outline=OUT, width=6)  # cushions
    d.ellipse([S * .56, S * .58, S * .66, S * .64], fill=(250, 245, 230, 255))                         # stuffing
    for x in (.1, .86):
        d.rectangle([S * x, S * .82, S * (x + .05), S * .92], fill=OUT)
    return _shrink(im, size)


def mattress(size=64):
    """A stained old mattress standing on its end."""
    im, d, S = _big(size)
    OUT = (40, 40, 50, 255)
    d.rounded_rectangle([S * .2, S * .04, S * .8, S * .96], 20, fill=(240, 240, 250, 255), outline=OUT, width=9)
    for r in range(5):
        for c in range(3):
            d.ellipse([S * (.3 + c * .17) - 6, S * (.14 + r * .17) - 6, S * (.3 + c * .17) + 6, S * (.14 + r * .17) + 6],
                      fill=(190, 190, 210, 255))
    d.ellipse([S * .36, S * .5, S * .56, S * .64], fill=(225, 205, 150, 255))                          # a stain
    d.rectangle([S * .2, S * .04, S * .8, S * .1], fill=(120, 150, 220, 255), outline=OUT, width=5)
    return _shrink(im, size)


def dresser(size=64):
    """A wooden three-drawer dresser, one drawer hanging open with a sock sticking out."""
    im, d, S = _big(size)
    OUT, WOOD, WOOD_L, WOOD_D = (35, 20, 8, 255), (170, 110, 60, 255), (215, 160, 105, 255), (120, 75, 35, 255)
    d.rectangle([S * .12, S * .12, S * .88, S * .9], fill=WOOD_D, outline=OUT, width=9)
    for k in range(3):
        y = S * (.18 + k * .24)
        off = S * .06 if k == 1 else 0
        d.rectangle([S * .18 - off, y, S * .82 - off, y + S * .2], fill=WOOD, outline=OUT, width=7)
        d.ellipse([S * .46 - off, y + S * .08, S * .54 - off, y + S * .12], fill=(240, 220, 120, 255))
        d.line([(S * .2 - off, y + S * .03), (S * .8 - off, y + S * .03)], fill=WOOD_L, width=5)
    d.polygon([(S * .14, S * .46), (S * .04, S * .5), (S * .06, S * .58), (S * .16, S * .52)], fill=(250, 250, 250, 255), outline=OUT)  # sock
    for x in (.16, .78):
        d.rectangle([S * x, S * .9, S * (x + .06), S * .98], fill=OUT)
    return _shrink(im, size)


def singing_bowl(size=64):
    """A brass singing bowl on a cushion, two incense sticks smoking in a holder beside it."""
    im, d, S = _big(size)
    OUT, BRASS, BRASS_L = (50, 30, 5, 255), (220, 170, 60, 255), (255, 225, 140, 255)
    d.rounded_rectangle([S * .06, S * .78, S * .7, S * .94], 14, fill=(170, 40, 60, 255), outline=OUT, width=7)  # cushion
    d.chord([S * .1, S * .42, S * .66, S * .92], 0, 180, fill=BRASS, outline=OUT, width=8)            # the bowl
    d.ellipse([S * .1, S * .6, S * .66, S * .72], fill=(150, 110, 40, 255), outline=OUT, width=6)
    d.arc([S * .16, S * .64, S * .5, S * .86], 120, 170, fill=BRASS_L, width=8)
    d.rectangle([S * .74, S * .84, S * .94, S * .92], fill=(90, 60, 30, 255), outline=OUT, width=5)   # holder
    for x, top in ((.8, .22), (.88, .3)):                                                              # incense
        d.line([(S * x, S * .86), (S * x, S * top)], fill=(120, 70, 40, 255), width=6)
        d.ellipse([S * x - 6, S * top - 6, S * x + 6, S * top + 6], fill=(255, 120, 40, 255))
    return _shrink(im, size)


def om_ring(n=16):
    """A thin glowing calm ring (alpha only)."""
    c = (n - 1) / 2
    return _alpha(n, n, lambda x, y: 1 - abs(((x - c) ** 2 + (y - c) ** 2) ** .5 - 6.5) / .9)


def freeloader(size=64):
    """The freeloading cousin, sitting cross-legged, too comfortable: backward red cap, half-shut chill eyes,
    a backpack, and a GIANT 64oz soda cup with a straw held up in one hand."""
    im, d, S = _big(size)
    OUT, SKIN, SHIRT, PACK, JEANS = (15, 10, 8, 255), (160, 105, 70, 255), (90, 170, 80, 255), (230, 120, 40, 255), (50, 70, 140, 255)
    d.rounded_rectangle([S * .08, S * .42, S * .3, S * .76], 14, fill=PACK, outline=OUT, width=8)    # backpack
    d.rounded_rectangle([S * .14, S * .78, S * .66, S * .94], 20, fill=JEANS, outline=OUT, width=8)  # crossed legs
    for x in (.12, .6):                                                                                # sneakers
        d.ellipse([S * x, S * .82, S * (x + .14), S * .96], fill=(250, 250, 250, 255), outline=OUT, width=6)
    d.rounded_rectangle([S * .2, S * .46, S * .6, S * .82], 18, fill=SHIRT, outline=OUT, width=8)   # body
    d.ellipse([S * .22, S * .14, S * .56, S * .48], fill=SKIN, outline=OUT, width=8)                  # head
    d.chord([S * .2, S * .1, S * .58, S * .34], 180, 360, fill=(220, 40, 40, 255), outline=OUT, width=6)  # cap
    d.rectangle([S * .1, S * .22, S * .26, S * .28], fill=(220, 40, 40, 255), outline=OUT, width=4)  # (backward brim)
    d.line([(S * .32, S * .3), (S * .38, S * .31)], fill=OUT, width=5)                                # chill eyes
    d.line([(S * .44, S * .31), (S * .5, S * .3)], fill=OUT, width=5)
    d.arc([S * .32, S * .32, S * .48, S * .42], 20, 160, fill=OUT, width=5)                           # smirk
    d.line([(S * .56, S * .58), (S * .7, S * .44)], fill=SHIRT, width=16)                              # the arm up
    d.polygon([(S * .62, S * .14), (S * .92, S * .14), (S * .88, S * .6), (S * .66, S * .6)],
              fill=(250, 250, 250, 255), outline=OUT)                                                  # the BIG cup
    d.line([(S * .62, S * .14), (S * .92, S * .14), (S * .88, S * .6), (S * .66, S * .6), (S * .62, S * .14)], fill=OUT, width=7)
    d.rectangle([S * .64, S * .26, S * .9, S * .4], fill=(220, 40, 40, 255))                          # red band
    d.rectangle([S * .6, S * .1, S * .94, S * .16], fill=(240, 240, 240, 255), outline=OUT, width=5)  # the lid
    d.line([(S * .8, S * .12), (S * .86, S * .0)], fill=(255, 220, 60, 255), width=7)                  # straw
    return _shrink(im, size)

def full_mirror(size=64):
    """A tall full-length mirror on a stand, gold frame, a big shine across the glass."""
    im, d, S = _big(size)
    OUT, GOLD = (50, 35, 10, 255), (230, 185, 60, 255)
    d.rounded_rectangle([S * .26, S * .02, S * .74, S * .86], 30, fill=GOLD, outline=OUT, width=9)
    d.rounded_rectangle([S * .32, S * .08, S * .68, S * .8], 24, fill=(190, 225, 245, 255), outline=OUT, width=6)
    d.line([(S * .38, S * .5), (S * .56, S * .14)], fill=(250, 255, 255, 255), width=12)
    d.line([(S * .44, S * .6), (S * .6, S * .28)], fill=(240, 250, 255, 255), width=6)
    for x in (.34, .66):
        d.line([(S * .5, S * .86), (S * x, S * .98)], fill=OUT, width=10)
    return _shrink(im, size)


def price_tag(size=32):
    """A designer price tag on a string (thrown), $$$ on it."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (40, 30, 10, 255)
    d.polygon([(4, 10), (10, 4), (28, 4), (28, 20), (10, 20)], fill=(255, 245, 210, 255), outline=OUT)
    d.ellipse([7, 10, 10, 13], fill=OUT)
    m = _text_mask("$$$", CASH_FONT)
    im.paste((30, 130, 50, 255), (19 - m.width // 2, 9), m)
    d.line([(8, 12), (2, 26)], fill=(200, 40, 40, 255))
    return im


def bouncer(size=64):
    """A huge bouncer, arms crossed, shades, black SECURITY tee, an earpiece (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT, SKIN, TEE = (10, 8, 6, 255), (120, 75, 45, 255), (25, 25, 30, 255)
    d.rounded_rectangle([8, 24, 55, 63], 8, fill=TEE, outline=OUT)                                     # the body
    d.rectangle([24, 15, 39, 26], fill=SKIN, outline=OUT)                                              # neck
    d.ellipse([20, 1, 43, 24], fill=SKIN, outline=OUT)                                                 # bald head
    d.rectangle([23, 9, 40, 14], fill=OUT)                                                             # shades
    d.line([(28, 19), (35, 19)], fill=OUT)                                                             # not smiling
    d.line([(43, 12), (47, 20)], fill=(200, 200, 210, 255))                                            # earpiece
    d.rounded_rectangle([10, 42, 53, 52], 4, fill=SKIN, outline=OUT)                                    # crossed arms
    d.line([(31, 42), (31, 52)], fill=OUT)
    m = _text_mask("SECURITY")
    im.paste((255, 255, 255, 255), (32 - m.width // 2, 30), m)
    return im


def velvet_rope(size=64):
    """Two gold stanchions with a red velvet rope swagged between them."""
    im, d, S = _big(size)
    OUT, GOLD = (50, 35, 10, 255), (240, 195, 60, 255)
    for x in (.12, .88):
        d.rectangle([S * (x - .03), S * .3, S * (x + .03), S * .92], fill=GOLD, outline=OUT, width=6)
        d.ellipse([S * (x - .06), S * .22, S * (x + .06), S * .34], fill=GOLD, outline=OUT, width=6)
        d.ellipse([S * (x - .12), S * .9, S * (x + .12), S * .98], fill=GOLD, outline=OUT, width=6)
    d.arc([S * .12, S * .1, S * .88, S * .66], 20, 160, fill=OUT, width=20)
    d.arc([S * .12, S * .1, S * .88, S * .66], 20, 160, fill=(200, 20, 40, 255), width=12)
    return _shrink(im, size)


def status_bubble(size=32):
    """A floating status-condition bubble: purple, a skull and a Zzz in it (gets turned away at the rope)."""
    im, d, S = _big(size)
    OUT = (40, 10, 50, 255)
    d.ellipse([S * .08, S * .08, S * .92, S * .92], fill=(190, 120, 240, 200), outline=OUT, width=7)
    d.ellipse([S * .3, S * .3, S * .58, S * .56], fill=(250, 250, 250, 255), outline=OUT, width=5)    # skull
    d.rectangle([S * .36, S * .52, S * .52, S * .62], fill=(250, 250, 250, 255), outline=OUT, width=4)
    for x in (.36, .46):
        d.ellipse([S * x, S * .38, S * (x + .07), S * .45], fill=OUT)
    d.arc([S * .2, S * .16, S * .5, S * .4], 200, 270, fill=(255, 255, 255, 255), width=6)
    return _shrink(im, size)


def police_light(size=64, red=True):
    """A rotating police dome light on a little base: the red side lit, or the blue side lit."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    on, off = ((255, 50, 50, 255), (60, 40, 120, 255)) if red else ((60, 140, 255, 255), (120, 30, 40, 255))
    d.rectangle([S * .22, S * .7, S * .78, S * .84], fill=(60, 60, 70, 255), outline=OUT, width=8)
    d.chord([S * .26, S * .22, S * .74, S * .94], 180, 360, fill=off, outline=OUT, width=8)
    d.pieslice([S * .26, S * .22, S * .74, S * .94], 180, 270, fill=on, outline=OUT, width=8)
    d.arc([S * .32, S * .3, S * .58, S * .56], 200, 260, fill=(255, 255, 255, 255), width=8)
    for k in range(5):                                                                                 # rays
        import math
        a = math.radians(200 + k * 14)
        d.line([(S * .5 + S * .3 * math.cos(a), S * .58 + S * .3 * math.sin(a)),
                (S * .5 + S * .48 * math.cos(a), S * .58 + S * .48 * math.sin(a))], fill=on, width=8)
    return _shrink(im, size)


def woop_wave(n=16):
    """A loud sound wave: three nested arcs opening right (alpha only)."""
    import math

    def f(x, y):
        r = ((x - 1) ** 2 + (y - 7.5) ** 2) ** .5
        a = abs(math.degrees(math.atan2(y - 7.5, x - 1)))
        return 1 if a < 55 and any(abs(r - rr) < .9 for rr in (5, 9, 13)) else 0
    return _alpha(n, n, f)


def orbital_buffer(size=64):
    """A car-detailing orbital buffer: a big fluffy pad on a grey motor body with a handle."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.ellipse([S * .1, S * .5, S * .9, S * .82], fill=(250, 250, 250, 255), outline=OUT, width=9)    # the pad
    d.ellipse([S * .2, S * .56, S * .8, S * .76], fill=(225, 225, 235, 255))
    d.rounded_rectangle([S * .3, S * .3, S * .7, S * .56], 16, fill=(220, 50, 50, 255), outline=OUT, width=9)  # body
    d.rounded_rectangle([S * .38, S * .08, S * .62, S * .32], 12, fill=(60, 60, 70, 255), outline=OUT, width=8)  # handle
    d.line([(S * .36, S * .38), (S * .64, S * .38)], fill=(255, 140, 140, 255), width=6)
    return _shrink(im, size)


def wax_swirl(n=16):
    """A buffing swirl (alpha only): a spiral."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = x - c, y - c
        r = (dx * dx + dy * dy) ** .5
        a = math.atan2(dy, dx) % math.tau
        target = 1.2 + a / math.tau * 5.5
        return 1 if abs(r - target) < .8 or abs(r - target - 5.5) < .8 else 0
    return _alpha(n, n, f)


def tbone_steak(size=64):
    """A big grilled T-bone steak, the classic cartoon way: a browned slab with dark diagonal grill marks, a
    creamy fat edge, the white T-bone running through it, a sprig of parsley on top."""
    import math
    im, d, S = _big(size)
    OUT, MEAT, MEAT_L, MEAT_D, FAT, BONE, GRILL = ((45, 20, 10, 255), (170, 85, 45, 255), (205, 120, 70, 255),
                                                  (125, 55, 25, 255), (245, 225, 180, 255), (250, 248, 238, 255),
                                                  (70, 30, 15, 255))
    pts = []
    for k in range(24):                                                                                # the slab
        a = k * math.tau / 24
        r = .44 + .04 * math.sin(a * 3) - (.08 if 0.3 < a < 1.6 else 0)
        pts.append((S * (.5 + r * math.cos(a)), S * (.52 + r * .78 * math.sin(a))))
    d.polygon(pts, fill=FAT)
    d.line(pts + [pts[0]], fill=OUT, width=9)
    inner = [(S * .5 + (x - S * .5) * .84, S * .52 + (y - S * .52) * .8) for x, y in pts]
    d.polygon(inner, fill=MEAT)
    d.polygon([(S * .5 + (x - S * .5) * .6, S * .5 + (y - S * .52) * .55) for x, y in pts], fill=MEAT_L)
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))                                                 # (clipped to the meat)
    dl = ImageDraw.Draw(layer)
    for k in range(6):                                                                                 # grill marks
        x0 = S * (.06 + k * .15)
        dl.line([(x0, S * .2), (x0 + S * .26, S * .86)], fill=GRILL, width=12)
    dl.line([(S * .56, S * .1), (S * .54, S * .96)], fill=OUT, width=22)                               # the T-bone
    dl.line([(S * .56, S * .1), (S * .54, S * .96)], fill=BONE, width=13)
    dl.line([(S * .55, S * .52), (S * .98, S * .5)], fill=OUT, width=18)
    dl.line([(S * .55, S * .52), (S * .98, S * .5)], fill=BONE, width=10)
    mask = Image.new('L', im.size, 0)
    ImageDraw.Draw(mask).polygon(inner, fill=255)
    im.paste(layer, (0, 0), Image.composite(layer.split()[3], Image.new('L', im.size, 0), mask))
    d = ImageDraw.Draw(im)
    for x, y in ((.24, .3), (.3, .26), (.27, .22)):                                                    # parsley
        d.ellipse([S * (x - .04), S * (y - .04), S * (x + .04), S * (y + .04)], fill=(70, 170, 60, 255), outline=OUT, width=4)
    return _shrink(im, size)


def anger_steam(n=16):
    """A puff of anger steam (alpha only)."""
    def f(x, y):
        v = 0
        for cx, cy, r in ((6, 10, 3.4), (10, 8, 3.8), (8, 5, 3)):
            v = max(v, 1.3 - ((x - cx) ** 2 + (y - cy) ** 2) ** .5 / r)
        return v
    return _alpha(n, n, f)


def bass_fish(size=64):
    """A GIANT largemouth bass side-on, facing right: green back, pale belly, the dark stripe, a huge open mouth."""
    im, d, S = _big(size)
    OUT, G, GL, BELLY, STRIPE = (15, 30, 10, 255), (90, 140, 60, 255), (150, 190, 100, 255), (235, 230, 190, 255), (45, 70, 30, 255)
    d.polygon([(S * .04, S * .3), (S * .2, S * .5), (S * .04, S * .72)], fill=G, outline=OUT)          # tail
    d.line([(S * .04, S * .3), (S * .2, S * .5), (S * .04, S * .72), (S * .04, S * .3)], fill=OUT, width=7)
    d.ellipse([S * .14, S * .24, S * .86, S * .78], fill=G, outline=OUT, width=9)                      # body
    d.chord([S * .18, S * .44, S * .84, S * .78], 0, 180, fill=BELLY)
    d.line([(S * .22, S * .5), (S * .76, S * .48)], fill=STRIPE, width=10)                             # the stripe
    d.polygon([(S * .38, S * .26), (S * .5, S * .08), (S * .62, S * .26)], fill=G, outline=OUT)       # dorsal fin
    d.polygon([(S * .76, S * .4), (S * .98, S * .3), (S * .98, S * .72), (S * .78, S * .62)], fill=(140, 40, 50, 255), outline=OUT)  # mouth
    d.line([(S * .76, S * .4), (S * .98, S * .3), (S * .98, S * .72), (S * .78, S * .62)], fill=OUT, width=7)
    d.ellipse([S * .68, S * .32, S * .78, S * .42], fill=(255, 220, 60, 255), outline=OUT, width=5)    # eye
    d.ellipse([S * .72, S * .35, S * .76, S * .39], fill=OUT)
    d.arc([S * .22, S * .3, S * .6, S * .5], 200, 300, fill=GL, width=8)
    for k in range(4):                                                                                 # scales
        d.arc([S * (.3 + k * .1), S * .52, S * (.38 + k * .1), S * .6], 0, 180, fill=GL, width=4)
    return _shrink(im, size)


def foam_cup(size=64):
    """A styrofoam cup heaped with ice cubes."""
    im, d, S = _big(size)
    OUT, FOAM = (60, 60, 70, 255), (250, 250, 245, 255)
    d.polygon([(S * .2, S * .34), (S * .8, S * .34), (S * .7, S * .96), (S * .3, S * .96)], fill=FOAM, outline=OUT)
    d.line([(S * .2, S * .34), (S * .8, S * .34), (S * .7, S * .96), (S * .3, S * .96), (S * .2, S * .34)], fill=OUT, width=8)
    for y in (.5, .66, .82):
        d.line([(S * (.24 + (y - .34) * .1), S * y), (S * (.76 - (y - .34) * .1), S * y)], fill=(220, 220, 215, 255), width=4)
    for x, y in ((.3, .26), (.48, .2), (.64, .26), (.4, .32), (.56, .32)):                              # the ice
        d.rounded_rectangle([S * (x - .07), S * (y - .07), S * (x + .07), S * (y + .07)], 8, fill=(200, 235, 255, 255),
                            outline=(90, 150, 200, 255), width=5)
        d.line([(S * (x - .03), S * (y - .03)), (S * x, S * (y - .04))], fill=(255, 255, 255, 255), width=4)
    return _shrink(im, size)


def ice_cube(n=16):
    """A little ice cube with a glint (alpha only)."""
    def f(x, y):
        if 3 <= x <= 12 and 3 <= y <= 12:
            if (x - 5) ** 2 + (y - 5) ** 2 < 2.5:
                return .55
            return 1 if x in (3, 12) or y in (3, 12) else .8
        return 0
    return _alpha(n, n, f)


def the_list(size=64, open_=False):
    """THE LIST: a black notebook (closed: THE LIST on the cover in red), or open: rows of names scribbled, one
    circled in red and X'd out (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (10, 10, 12, 255)
    if not open_:
        d.rectangle([14, 6, 49, 58], fill=(30, 30, 35, 255), outline=OUT)
        d.rectangle([14, 6, 18, 58], fill=(60, 60, 70, 255))
        for k, word in enumerate(("THE", "LIST")):
            m = _text_mask(word)
            im.paste((230, 30, 40, 255), (33 - m.width // 2, 22 + k * 8), m)
        d.line([(22, 40), (44, 40)], fill=(230, 30, 40, 255))
    else:
        d.polygon([(4, 12), (31, 16), (31, 56), (4, 52)], fill=(250, 248, 235, 255), outline=OUT)
        d.polygon([(33, 16), (60, 12), (60, 52), (33, 56)], fill=(250, 248, 235, 255), outline=OUT)
        for k in range(6):                                                                             # names
            y = 20 + k * 5
            d.line([(8, y), (8 + 14 + (k * 5) % 8, y + 1)], fill=(40, 40, 60, 255))
            d.line([(38, y + 1), (38 + 12 + (k * 3) % 8, y)], fill=(40, 40, 60, 255))
            if k in (1, 3):
                d.line([(7, y), (26, y + 1)], fill=(200, 30, 30, 255))                                 # crossed off
        d.ellipse([35, 33, 58, 43], outline=(230, 30, 40, 255), width=2)                               # circled
        d.line([(36, 32), (57, 44)], fill=(230, 30, 40, 255), width=2)
        d.line([(36, 44), (57, 32)], fill=(230, 30, 40, 255), width=2)
    return im


def horseshoe_magnet(size=64):
    """A big red horseshoe magnet, silver tips, pointing right (the poles facing the foe)."""
    im, d, S = _big(size)
    OUT, RED, RED_L = (40, 5, 5, 255), (220, 35, 45, 255), (255, 120, 120, 255)
    d.arc([S * .06, S * .14, S * .78, S * .86], 90, 270, fill=OUT, width=int(S * .26))
    d.arc([S * .06, S * .14, S * .78, S * .86], 90, 270, fill=RED, width=int(S * .2))
    d.rectangle([S * .42, S * .14, S * .72, S * .28], fill=RED, outline=OUT, width=8)
    d.rectangle([S * .42, S * .72, S * .72, S * .86], fill=RED, outline=OUT, width=8)
    d.rectangle([S * .72, S * .14, S * .94, S * .28], fill=(220, 225, 235, 255), outline=OUT, width=8)  # silver tips
    d.rectangle([S * .72, S * .72, S * .94, S * .86], fill=(220, 225, 235, 255), outline=OUT, width=8)
    d.arc([S * .14, S * .22, S * .6, S * .5], 180, 240, fill=RED_L, width=8)
    return _shrink(im, size)


def magnet_lines(n=16):
    """Curved magnetic pull lines (alpha only)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        r = ((x - c) ** 2 + (y - c) ** 2) ** .5
        a = abs(math.degrees(math.atan2(y - c, x - c)))
        return 1 if (abs(r - 4) < .7 or abs(r - 7) < .7) and a < 60 else 0
    return _alpha(n, n, f)


def hubcap(size=32):
    """A chrome hubcap spinning through the air."""
    im, d, S = _big(size)
    OUT = (30, 30, 40, 255)
    d.ellipse([S * .06, S * .06, S * .94, S * .94], fill=(210, 215, 225, 255), outline=OUT, width=7)
    d.ellipse([S * .3, S * .3, S * .7, S * .7], fill=(150, 155, 170, 255), outline=OUT, width=5)
    import math
    for k in range(6):
        a = k * math.tau / 6
        d.line([(S * .5 + S * .2 * math.cos(a), S * .5 + S * .2 * math.sin(a)),
                (S * .5 + S * .42 * math.cos(a), S * .5 + S * .42 * math.sin(a))], fill=OUT, width=5)
    d.arc([S * .14, S * .14, S * .6, S * .6], 200, 260, fill=(255, 255, 255, 255), width=6)
    return _shrink(im, size)


def boxing_glove(size=64):
    """A red boxing glove punching right, white cuff, the laces."""
    im, d, S = _big(size)
    OUT, RED, RED_L, RED_D = (40, 5, 5, 255), (220, 30, 40, 255), (255, 120, 120, 255), (160, 15, 25, 255)
    d.rectangle([S * .04, S * .34, S * .3, S * .7], fill=(250, 250, 250, 255), outline=OUT, width=8)  # cuff
    d.line([(S * .1, S * .42), (S * .24, S * .62)], fill=OUT, width=5)                                 # laces
    d.line([(S * .1, S * .62), (S * .24, S * .42)], fill=OUT, width=5)
    d.ellipse([S * .22, S * .16, S * .96, S * .86], fill=RED, outline=OUT, width=10)                    # the glove
    d.ellipse([S * .34, S * .54, S * .62, S * .84], fill=RED_D, outline=OUT, width=8)                   # thumb
    d.arc([S * .34, S * .24, S * .82, S * .6], 200, 290, fill=RED_L, width=12)
    return _shrink(im, size)


def boxing_bell(size=64):
    """A brass ring bell on a wooden plaque, the little hammer striking it."""
    im, d, S = _big(size)
    OUT, BRASS, BRASS_L = (50, 30, 5, 255), (230, 180, 50, 255), (255, 235, 150, 255)
    d.rounded_rectangle([S * .2, S * .1, S * .8, S * .9], 16, fill=(150, 90, 45, 255), outline=OUT, width=9)  # plaque
    d.ellipse([S * .28, S * .22, S * .72, S * .66], fill=BRASS, outline=OUT, width=9)                   # the bell
    d.ellipse([S * .44, S * .38, S * .56, S * .5], fill=(180, 130, 30, 255), outline=OUT, width=5)
    d.arc([S * .32, S * .26, S * .62, S * .56], 200, 260, fill=BRASS_L, width=10)
    d.line([(S * .5, S * .86), (S * .62, S * .64)], fill=OUT, width=10)                                 # the hammer
    d.ellipse([S * .58, S * .58, S * .7, S * .68], fill=(120, 120, 130, 255), outline=OUT, width=5)
    return _shrink(im, size)


def phone_battery(size=64, level=0):
    """A phone screen showing the battery: 0 = 1% red, 1 = half yellow, 2 = 100% green with the charging bolt
    (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (8, 8, 10, 255)
    d.rounded_rectangle([18, 4, 45, 60], 4, fill=(30, 30, 36, 255), outline=OUT)
    d.rectangle([20, 9, 43, 55], fill=(20, 30, 45, 255))
    d.rectangle([24, 22, 39, 46], outline=(230, 230, 240, 255))                                        # the battery
    d.rectangle([29, 19, 34, 22], fill=(230, 230, 240, 255))
    col, fill = (((230, 40, 40, 255), 1), ((250, 210, 40, 255), 11), ((70, 230, 90, 255), 22))[level]
    d.rectangle([25, 46 - fill, 38, 45], fill=col)
    word = ("1%", "50%", "100%")[level]
    m = _text_mask(word)
    im.paste((255, 255, 255, 255), (32 - m.width // 2, 11), m)
    if level:
        d.polygon([(32, 26), (28, 34), (31, 34), (29, 42), (35, 32), (32, 32), (34, 26)], fill=(255, 255, 255, 255))
    return im


def power_bank(size=64):
    """A chunky power bank brick with blue LEDs and a cable snaking off it."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rounded_rectangle([S * .1, S * .4, S * .7, S * .86], 14, fill=(45, 45, 55, 255), outline=OUT, width=9)
    for k in range(4):
        d.ellipse([S * (.18 + k * .1), S * .48, S * (.24 + k * .1), S * .54], fill=(80, 200, 255, 255))
    d.line([(S * .7, S * .6), (S * .84, S * .6), (S * .86, S * .3), (S * .96, S * .2)], fill=OUT, width=12)
    d.line([(S * .7, S * .6), (S * .84, S * .6), (S * .86, S * .3), (S * .96, S * .2)], fill=(240, 240, 240, 255), width=6)
    return _shrink(im, size)


def clothes_rack(size=64):
    """A round store clothing rack crammed with hanging shirts (someone could hide in there)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.line([(S * .5, S * .2), (S * .5, S * .94)], fill=(170, 170, 180, 255), width=10)                  # the pole
    d.ellipse([S * .3, S * .9, S * .7, S * .98], fill=(120, 120, 130, 255), outline=OUT, width=5)
    d.ellipse([S * .06, S * .18, S * .94, S * .3], outline=(190, 190, 200, 255), width=8)               # the ring
    cols = ((220, 60, 70, 255), (60, 140, 230, 255), (250, 210, 60, 255), (90, 190, 90, 255), (240, 240, 240, 255),
            (160, 80, 200, 255), (250, 140, 40, 255))
    for k, col in enumerate(cols):                                                                     # the shirts
        x = S * (.08 + k * .12)
        d.polygon([(x, S * .26), (x + S * .14, S * .26), (x + S * .16, S * .82), (x - S * .02, S * .82)], fill=col, outline=OUT)
        d.line([(x + S * .07, S * .2), (x + S * .07, S * .27)], fill=OUT, width=5)
    return _shrink(im, size)


def peek_eyes(size=32):
    """Two eyes peeking out of the dark (between the shirts)."""
    im, d, S = _big(size)
    for x in (.18, .54):
        d.ellipse([S * x, S * .34, S * (x + .28), S * .66], fill=(255, 255, 255, 255), outline=(10, 10, 10, 255), width=5)
        d.ellipse([S * (x + .12), S * .44, S * (x + .22), S * .58], fill=(10, 10, 10, 255))
    return _shrink(im, size)


def slushie(size=64):
    """A giant blue slushie: a clear cup, an icy blue dome, a red spoon-straw."""
    im, d, S = _big(size)
    OUT = (15, 25, 45, 255)
    d.polygon([(S * .24, S * .36), (S * .76, S * .36), (S * .68, S * .96), (S * .32, S * .96)], fill=(200, 230, 250, 200), outline=OUT)
    d.line([(S * .24, S * .36), (S * .76, S * .36), (S * .68, S * .96), (S * .32, S * .96), (S * .24, S * .36)], fill=OUT, width=8)
    d.polygon([(S * .27, S * .42), (S * .73, S * .42), (S * .67, S * .9), (S * .33, S * .9)], fill=(60, 150, 255, 255))
    d.chord([S * .2, S * .14, S * .8, S * .56], 180, 360, fill=(90, 180, 255, 255), outline=OUT, width=8)  # the dome
    for x, y in ((.36, .28), (.5, .22), (.62, .3)):
        d.ellipse([S * (x - .04), S * (y - .03), S * (x + .04), S * (y + .03)], fill=(200, 235, 255, 255))
    d.line([(S * .56, S * .3), (S * .74, S * .0)], fill=(230, 40, 40, 255), width=10)                   # straw
    return _shrink(im, size)


def icicle(n=16):
    """A hanging icicle (alpha only)."""
    def f(x, y):
        return 1 if 1 <= y <= 14 and abs(x - 7.5) < (14 - y) * .3 + .3 else 0
    return _alpha(n, n, f)


def frost_jaws(size=64, shut=False):
    """Jaws made of ice: two rows of icicle fangs, open wide - or chomped shut."""
    im, d, S = _big(size)
    OUT, ICE, ICE_L, ICE_D = (20, 50, 90, 255), (170, 220, 255, 255), (235, 250, 255, 255), (100, 170, 230, 255)
    gap = .02 if shut else .2
    top, bot = .5 - gap, .5 + gap
    d.rounded_rectangle([S * .06, S * (top - .22), S * .94, S * top], 18, fill=ICE_D, outline=OUT, width=8)
    d.rounded_rectangle([S * .06, S * bot, S * .94, S * (bot + .22)], 18, fill=ICE_D, outline=OUT, width=8)
    for k in range(6):
        x = S * (.12 + k * .13)
        d.polygon([(x, S * top), (x + S * .12, S * top), (x + S * .06, S * (top + .16))], fill=ICE, outline=OUT)
        d.polygon([(x + S * .06, S * bot), (x + S * .18, S * bot), (x + S * .12, S * (bot - .16))], fill=ICE, outline=OUT)
        d.line([(x + S * .03, S * top), (x + S * .05, S * (top + .08))], fill=ICE_L, width=4)
    return _shrink(im, size)


def binoculars(size=64):
    """A pair of black binoculars seen from the side, held up to the eyes, lenses pointing right."""
    im, d, S = _big(size)
    OUT, BLACK, GREY = (5, 5, 8, 255), (40, 40, 48, 255), (90, 95, 110, 255)
    for y in (.3, .54):
        d.rounded_rectangle([S * .1, S * y, S * .78, S * (y + .2)], 16, fill=BLACK, outline=OUT, width=8)
        d.rectangle([S * .78, S * (y - .02), S * .94, S * (y + .22)], fill=GREY, outline=OUT, width=7)   # lens hood
        d.ellipse([S * .88, S * (y + .02), S * .98, S * (y + .18)], fill=(120, 200, 255, 255), outline=OUT, width=5)
        d.line([(S * .16, S * (y + .05)), (S * .7, S * (y + .05))], fill=GREY, width=5)
    d.rectangle([S * .38, S * .46, S * .5, S * .58], fill=GREY, outline=OUT, width=6)                # the hinge
    return _shrink(im, size)


def scope_reticle(size=64):
    """A red lock-on reticle: two thin rings, crosshair ticks, little corner brackets (crisp, no fill)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    RED = (240, 30, 40, 255)
    d.ellipse([8, 8, 55, 55], outline=RED, width=2)
    d.ellipse([20, 20, 43, 43], outline=RED, width=1)
    for a, b in (((31, 2), (31, 16)), ((31, 47), (31, 61)), ((2, 31), (16, 31)), ((47, 31), (61, 31))):
        d.line([a, b], fill=RED, width=2)
    d.rectangle([30, 30, 33, 33], fill=RED)
    for x, y, dx, dy in ((4, 4, 1, 1), (59, 4, -1, 1), (4, 59, 1, -1), (59, 59, -1, -1)):
        d.line([(x, y), (x + 7 * dx, y)], fill=RED, width=2)
        d.line([(x, y), (x, y + 7 * dy)], fill=RED, width=2)
    return im

def glow_eyes(size=32):
    """Two glowing eyes in the dark."""
    im, d, S = _big(size)
    for x in (.14, .56):
        d.ellipse([S * x, S * .36, S * (x + .3), S * .62], fill=(255, 250, 160, 255))
        d.ellipse([S * (x + .1), S * .42, S * (x + .2), S * .56], fill=(255, 140, 20, 255))
    return _shrink(im, size)


def claw_slashes(size=64):
    """Three glowing slash marks, ripped diagonally (left behind in the dark)."""
    im, d, S = _big(size)
    for k in range(3):
        x0 = S * (.18 + k * .2)
        d.line([(x0, S * .12), (x0 + S * .34, S * .88)], fill=(255, 70, 70, 140), width=18)
        d.line([(x0 + S * .02, S * .16), (x0 + S * .32, S * .84)], fill=(255, 255, 255, 255), width=6)
    return _shrink(im, size)


def flashlight_click(size=64):
    """A flashlight beam cone (translucent warm white), widening to the right."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = im.load()
    for x in range(size):
        half = 3 + x * .42
        for y in range(size):
            dy = abs(y - 31.5)
            if dy < half:
                px[x, y] = (255, 250, 210, int(140 * (1 - dy / half) ** .4 * min(1, x / 6)))
    return im


def whistle_note(n=16):
    """A single music note (alpha only): somebody whistling, innocent."""
    def f(x, y):
        if ((x - 5) / 3) ** 2 + ((y - 11.5) / 2.4) ** 2 < 1:
            return 1
        if 7 <= x <= 8 and 2 <= y <= 11:
            return 1
        return 1 if 8 <= x <= 12 and abs(y - (2 + (x - 8) * .8)) < 1.2 else 0
    return _alpha(n, n, f)


def handshake(size=64, step=0):
    """Two hands mid secret handshake: 0 = palms slapping, 1 = fingers hooked, 2 = fists bumping."""
    im, d, S = _big(size)
    OUT, A, B = (60, 30, 15, 255), (240, 190, 145, 255), (150, 95, 60, 255)
    sleeves = ((220, 40, 40, 255), (40, 90, 220, 255))
    for side, skin, sleeve in ((-1, A, sleeves[0]), (1, B, sleeves[1])):
        x0 = S * (.5 + side * .46)
        d.rectangle([min(x0, S * .5 + side * .3), S * .4, max(x0, S * .5 + side * .3), S * .64], fill=sleeve, outline=OUT, width=7)
        cx = S * (.5 + side * .16)
        if step == 2:                                                                                  # fists
            d.rounded_rectangle([cx - S * .14, S * .34, cx + S * .14, S * .7], 22, fill=skin, outline=OUT, width=8)
            for k in range(3):
                d.line([(cx - S * .06 * side, S * (.42 + k * .08)), (cx + S * .1 * -side, S * (.42 + k * .08))], fill=OUT, width=4)
        else:
            d.rounded_rectangle([cx - S * .12, S * .3, cx + S * .12, S * .72], 22, fill=skin, outline=OUT, width=8)
            if step == 1:                                                                              # hooked fingers
                d.arc([S * .42, S * .3, S * .58, S * .5], 180, 360, fill=OUT, width=8)
    if step == 0:                                                                                      # SLAP
        import math
        for k in range(8):
            a = k * math.tau / 8
            d.line([(S * .5 + S * .3 * math.cos(a), S * .5 + S * .3 * math.sin(a)),
                    (S * .5 + S * .42 * math.cos(a), S * .5 + S * .42 * math.sin(a))], fill=(255, 220, 60, 255), width=8)
    return _shrink(im, size)


def diamond(n=16):
    """A cut diamond (alpha only): crown and pavilion facets."""
    def f(x, y):
        if 3 <= y <= 6 and abs(x - 7.5) <= 2 + (y - 3) * 1.5:
            return .7 if (x + y) % 3 else 1
        if 6 < y <= 14 and abs(x - 7.5) <= 6.5 - (y - 6) * .8:
            return 1 if (x - y) % 3 else .7
        return 0
    return _alpha(n, n, f)


def ice_block(size=64):
    """A block of clear ice encrusted in diamonds (iced out) - someone's frozen inside it."""
    im, d, S = _big(size)
    OUT, ICE, ICE_L = (40, 80, 130, 255), (170, 220, 255, 190), (240, 250, 255, 230)
    d.rounded_rectangle([S * .1, S * .06, S * .9, S * .96], 18, fill=ICE, outline=OUT, width=9)
    d.line([(S * .2, S * .16), (S * .2, S * .7)], fill=ICE_L, width=12)
    d.line([(S * .3, S * .14), (S * .5, S * .14)], fill=ICE_L, width=8)
    import random
    rnd = random.Random(5)
    for _ in range(12):                                                                                # diamonds
        x, y = rnd.uniform(.16, .84) * S, rnd.uniform(.12, .9) * S
        r = S * rnd.uniform(.03, .05)
        d.polygon([(x, y - r), (x + r, y), (x, y + r * 1.4), (x - r, y)], fill=(255, 255, 255, 255), outline=(120, 190, 240, 255))
    return _shrink(im, size)


def rock_spike(size=64):
    """A big jagged rock spike bursting up out of the ground."""
    im, d, S = _big(size)
    OUT, G, GL, GD = (30, 25, 20, 255), (140, 125, 110, 255), (195, 180, 160, 255), (95, 85, 75, 255)
    d.polygon([(S * .14, S * .98), (S * .36, S * .3), (S * .5, S * .04), (S * .62, S * .36), (S * .86, S * .98)], fill=G, outline=OUT)
    d.line([(S * .14, S * .98), (S * .36, S * .3), (S * .5, S * .04), (S * .62, S * .36), (S * .86, S * .98)], fill=OUT, width=9)
    d.polygon([(S * .5, S * .04), (S * .52, S * .98), (S * .86, S * .98), (S * .62, S * .36)], fill=GD)
    d.line([(S * .42, S * .3), (S * .36, S * .8)], fill=GL, width=8)
    d.line([(S * .3, S * .6), (S * .46, S * .66)], fill=OUT, width=5)                                  # cracks
    d.line([(S * .6, S * .5), (S * .7, S * .62)], fill=OUT, width=5)
    return _shrink(im, size)


def deal_shades_small(size=32):
    """Black shades, put on slow (stone cold)."""
    im, d, S = _big(size)
    OUT = (5, 5, 8, 255)
    d.rectangle([S * .04, S * .36, S * .96, S * .46], fill=OUT)
    for x in (.08, .54):
        d.polygon([(S * x, S * .4), (S * (x + .38), S * .4), (S * (x + .34), S * .66), (S * (x + .04), S * .66)], fill=(20, 20, 26, 255), outline=OUT)
        d.line([(S * (x + .08), S * .46), (S * (x + .18), S * .46)], fill=(140, 150, 190, 255), width=5)
    return _shrink(im, size)


def date_table(size=64):
    """A candlelit table for two: white tablecloth, a plate of spaghetti, a red rose in a vase, two candles."""
    im, d, S = _big(size)
    OUT = (40, 20, 20, 255)
    d.polygon([(S * .04, S * .56), (S * .96, S * .56), (S * .9, S * .96), (S * .1, S * .96)], fill=(250, 248, 240, 255), outline=OUT)
    d.line([(S * .04, S * .56), (S * .96, S * .56), (S * .9, S * .96), (S * .1, S * .96), (S * .04, S * .56)], fill=OUT, width=8)
    d.ellipse([S * .28, S * .48, S * .62, S * .64], fill=(245, 245, 250, 255), outline=OUT, width=6)    # plate
    d.ellipse([S * .34, S * .48, S * .56, S * .58], fill=(240, 200, 80, 255))                          # spaghetti
    for k in range(4):
        d.arc([S * (.34 + k * .04), S * .48, S * (.44 + k * .04), S * .56], 0, 180, fill=(220, 170, 50, 255), width=4)
    d.ellipse([S * .42, S * .46, S * .5, S * .52], fill=(200, 40, 30, 255))                            # meatball
    for x in (.14, .84):                                                                               # candles
        d.rectangle([S * (x - .03), S * .3, S * (x + .03), S * .56], fill=(250, 245, 220, 255), outline=OUT, width=5)
        d.ellipse([S * (x - .03), S * .18, S * (x + .03), S * .3], fill=(255, 200, 60, 255))
    d.rectangle([S * .68, S * .4, S * .74, S * .56], fill=(150, 220, 240, 200), outline=OUT, width=4)  # vase
    d.line([(S * .71, S * .4), (S * .71, S * .2)], fill=(60, 140, 60, 255), width=5)
    d.ellipse([S * .66, S * .12, S * .76, S * .22], fill=(220, 30, 50, 255), outline=OUT, width=4)     # rose
    return _shrink(im, size)


def pickup_bubble(size=64):
    """A smooth speech bubble: U FROM TENNESSEE? (shown at 2:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (60, 20, 50, 255)
    d.rounded_rectangle([3, 16, 60, 43], 8, fill=(255, 235, 245, 255), outline=OUT)
    d.polygon([(14, 42), (8, 50), (22, 42)], fill=(255, 235, 245, 255), outline=OUT)
    d.line([(15, 42), (21, 42)], fill=(255, 235, 245, 255))
    for k, word in enumerate(("U FROM", "TENNESSEE?")):
        m = _text_mask(word)
        im.paste((210, 30, 110, 255), (32 - m.width // 2, 20 + k * 9), m)
    return im


def window_ac(size=64):
    """A window AC unit cranked to max: beige box, grille, the dial turned all the way to MAX (red)."""
    im, d, S = _big(size)
    OUT = (30, 30, 30, 255)
    d.rounded_rectangle([S * .06, S * .2, S * .94, S * .84], 10, fill=(225, 220, 200, 255), outline=OUT, width=9)
    d.rectangle([S * .12, S * .28, S * .64, S * .76], fill=(180, 175, 160, 255), outline=OUT, width=6)  # grille
    for k in range(7):
        y = S * (.32 + k * .064)
        d.line([(S * .14, y), (S * .62, y)], fill=(120, 115, 105, 255), width=4)
    d.ellipse([S * .7, S * .3, S * .88, S * .48], fill=(240, 240, 240, 255), outline=OUT, width=6)      # dial
    d.line([(S * .79, S * .39), (S * .86, S * .32)], fill=(230, 30, 30, 255), width=6)
    d.ellipse([S * .74, S * .58, S * .84, S * .68], fill=(60, 200, 255, 255), outline=OUT, width=5)     # on light
    return _shrink(im, size)


def snowflake(n=16):
    """A six-arm snowflake (alpha only)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = x - c, y - c
        r = (dx * dx + dy * dy) ** .5
        if r > 7:
            return 0
        a = math.degrees(math.atan2(dy, dx)) % 60
        return 1 if min(a, 60 - a) < 6 or r < 1.5 else 0
    return _alpha(n, n, f)


def pothole(size=64):
    """A huge city pothole cracked open, flat on the ground: dark hole, broken asphalt edge, steam."""
    im, d, S = _big(size)
    OUT, ASPH, ASPH_L = (15, 15, 18, 255), (70, 70, 75, 255), (120, 120, 125, 255)
    import math, random
    rnd = random.Random(6)
    pts = []
    for k in range(18):
        a = k * math.tau / 18
        r = S * (.42 + rnd.uniform(-.05, .05))
        pts.append((S * .5 + r * math.cos(a), S * .56 + r * .42 * math.sin(a)))
    d.polygon(pts, fill=ASPH, outline=OUT)
    d.line(pts + [pts[0]], fill=OUT, width=8)
    inner = [(S * .5 + (x - S * .5) * .72, S * .58 + (y - S * .56) * .66) for x, y in pts]
    d.polygon(inner, fill=(20, 15, 15, 255))
    d.ellipse([S * .3, S * .56, S * .7, S * .68], fill=(255, 120, 30, 200))                            # magma glow
    for k in range(6):                                                                                 # cracks
        a = k * math.tau / 6 + .3
        d.line([(S * .5 + S * .42 * math.cos(a), S * .56 + S * .18 * math.sin(a)),
                (S * .5 + S * .52 * math.cos(a), S * .56 + S * .24 * math.sin(a))], fill=OUT, width=6)
    d.line([(S * .14, S * .48), (S * .3, S * .44)], fill=ASPH_L, width=6)
    return _shrink(im, size)


def traffic_cone_s(size=32):
    """A little orange traffic cone, flying."""
    im, d, S = _big(size)
    OUT = (40, 15, 5, 255)
    d.polygon([(S * .5, S * .06), (S * .78, S * .82), (S * .22, S * .82)], fill=(255, 120, 20, 255), outline=OUT)
    d.line([(S * .5, S * .06), (S * .78, S * .82), (S * .22, S * .82), (S * .5, S * .06)], fill=OUT, width=6)
    d.polygon([(S * .4, S * .38), (S * .6, S * .38), (S * .66, S * .56), (S * .34, S * .56)], fill=(250, 250, 250, 255))
    d.rectangle([S * .12, S * .82, S * .88, S * .94], fill=(240, 100, 10, 255), outline=OUT, width=6)
    return _shrink(im, size)


def pickup_tailgate(size=64):
    """The back of a pickup with the tailgate down: a grill smoking on it, a cooler, a foam finger."""
    im, d, S = _big(size)
    OUT, BLUE, BLUE_L = (15, 15, 25, 255), (40, 90, 200, 255), (110, 160, 240, 255)
    d.rectangle([S * .06, S * .32, S * .94, S * .7], fill=BLUE, outline=OUT, width=9)                  # the bed
    d.rectangle([S * .02, S * .7, S * .98, S * .8], fill=(170, 170, 180, 255), outline=OUT, width=7)  # tailgate down
    d.line([(S * .1, S * .38), (S * .9, S * .38)], fill=BLUE_L, width=6)
    d.rectangle([S * .12, S * .52, S * .36, S * .7], fill=(220, 40, 40, 255), outline=OUT, width=6)   # cooler
    d.rectangle([S * .12, S * .52, S * .36, S * .58], fill=(250, 250, 250, 255), outline=OUT, width=5)
    d.ellipse([S * .44, S * .44, S * .74, S * .62], fill=(30, 30, 35, 255), outline=OUT, width=6)     # the grill
    for x in (.5, .58, .66):
        d.line([(S * x, S * .48), (S * x, S * .58)], fill=(150, 150, 160, 255), width=4)
    d.line([(S * .52, S * .62), (S * .48, S * .7)], fill=OUT, width=5)
    d.line([(S * .66, S * .62), (S * .7, S * .7)], fill=OUT, width=5)
    d.rounded_rectangle([S * .8, S * .18, S * .9, S * .54], 6, fill=(255, 210, 40, 255), outline=OUT, width=5)  # foam finger
    for x in (.12, .82):                                                                               # tires
        d.rectangle([S * x, S * .8, S * (x + .14), S * .96], fill=(30, 30, 34, 255), outline=OUT, width=6)
    return _shrink(im, size)


def shaved_ice_machine(size=64):
    """A shaved-ice machine going haywire: a clear dome full of snow, the blade housing, a crank, snow pouring."""
    im, d, S = _big(size)
    OUT = (20, 30, 50, 255)
    d.rounded_rectangle([S * .2, S * .54, S * .8, S * .96], 12, fill=(240, 60, 90, 255), outline=OUT, width=9)  # base
    d.rectangle([S * .3, S * .66, S * .7, S * .86], fill=(200, 235, 255, 255), outline=OUT, width=6)   # the cup slot
    d.chord([S * .22, S * .24, S * .78, S * .84], 180, 360, fill=(190, 225, 255, 200), outline=OUT, width=8)  # dome
    d.ellipse([S * .32, S * .36, S * .68, S * .5], fill=(250, 250, 255, 255))                          # snow inside
    d.line([(S * .8, S * .66), (S * .96, S * .5)], fill=OUT, width=8)                                  # crank
    d.ellipse([S * .92, S * .44, S * 1.0, S * .52], fill=(240, 60, 90, 255), outline=OUT, width=4)
    return _shrink(im, size)


def ring_light(size=64):
    """A ring light on a stand with a phone clipped in the middle."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.line([(S * .5, S * .62), (S * .5, S * .96)], fill=(60, 60, 70, 255), width=10)
    for x in (.3, .7):
        d.line([(S * .5, S * .9), (S * x, S * .98)], fill=(60, 60, 70, 255), width=8)
    d.ellipse([S * .14, S * .04, S * .86, S * .76], outline=OUT, width=int(S * .16))
    d.ellipse([S * .16, S * .06, S * .84, S * .74], outline=(255, 250, 220, 255), width=int(S * .1))
    d.rounded_rectangle([S * .42, S * .24, S * .58, S * .56], 6, fill=(30, 30, 36, 255), outline=OUT, width=6)  # phone
    d.rectangle([S * .45, S * .28, S * .55, S * .5], fill=(120, 190, 255, 255))
    return _shrink(im, size)


def camera_flash(n=16):
    """A big camera-flash starburst (alpha only)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = x - c, y - c
        r = (dx * dx + dy * dy) ** .5
        a = math.atan2(dy, dx)
        return 1 if r < 3 + 3.5 * abs(math.cos(a * 4)) ** 6 else (.5 if r < 4.5 else 0)
    return _alpha(n, n, f)


def manhole_flat(size=64):
    """A manhole cover lying in the street, seen at an angle: a flattened iron disc with the grid pattern, a ring
    of asphalt round it."""
    im, d, S = _big(size)
    OUT, IRON, IRON_L, IRON_D = (15, 15, 18, 255), (95, 95, 105, 255), (150, 150, 160, 255), (60, 60, 68, 255)
    d.ellipse([S * .02, S * .3, S * .98, S * .78], fill=(70, 70, 75, 255), outline=OUT, width=7)     # asphalt
    d.ellipse([S * .14, S * .36, S * .86, S * .72], fill=IRON, outline=OUT, width=8)                 # the cover
    for k in range(-3, 4):                                                                             # grid
        d.line([(S * (.5 + k * .08), S * .38), (S * (.5 + k * .08), S * .7)], fill=IRON_D, width=5)
    for k in (-1, 0, 1):
        d.line([(S * .16, S * (.54 + k * .07)), (S * .84, S * (.54 + k * .07))], fill=IRON_D, width=5)
    d.ellipse([S * .14, S * .36, S * .86, S * .72], outline=OUT, width=8)
    d.arc([S * .2, S * .38, S * .6, S * .56], 200, 280, fill=IRON_L, width=6)
    return _shrink(im, size)


def manhole_disc(size=32):
    """The manhole cover face-on, flying: a round iron disc, grid pattern, two pry holes."""
    im, d, S = _big(size)
    OUT, IRON, IRON_D = (15, 15, 18, 255), (110, 110, 120, 255), (65, 65, 72, 255)
    d.ellipse([S * .04, S * .04, S * .96, S * .96], fill=IRON, outline=OUT, width=8)
    for k in range(-2, 3):
        d.line([(S * (.5 + k * .14), S * .1), (S * (.5 + k * .14), S * .9)], fill=IRON_D, width=6)
        d.line([(S * .1, S * (.5 + k * .14)), (S * .9, S * (.5 + k * .14))], fill=IRON_D, width=6)
    d.ellipse([S * .04, S * .04, S * .96, S * .96], outline=OUT, width=8)
    for x in (.3, .66):
        d.ellipse([S * x, S * .44, S * (x + .06), S * .52], fill=OUT)
    return _shrink(im, size)


# ---- set 17: common moves --------------------------------------------------------------------------------

def _texted(im, words, fill, outline=(15, 10, 10, 255), font=None):
    """Paste pixel words onto a finished (native-size) image: [(text, (centre x, top y))] - drawn after the
    shrink so the letters stay crisp (shown at 1:1)."""
    for text, (cx, y) in words:
        m = _text_mask(text, font or SMALL)
        x = round(cx - m.width / 2)
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx or dy:
                    im.paste(outline, (x + dx, y + dy), m)
        im.paste(fill, (x, y), m)
    return im


def _outline_poly(d, pts, fill, out, width):
    d.polygon(pts, fill=fill)
    d.line(pts + [pts[0]], fill=out, width=width, joint="curve")


def fragile_box(size=64):
    """A big cardboard shipping box, taped shut: FRAGILE in red, a this-way-up arrow, a shipping label
    (shown at 1:1)."""
    im, d, S = _big(size)
    OUT, CARD, CARD_D, CARD_L = (45, 25, 10, 255), (205, 150, 85, 255), (160, 110, 55, 255), (235, 190, 125, 255)
    _outline_poly(d, [(S * .06, S * .3), (S * .7, S * .3), (S * .7, S * .96), (S * .06, S * .96)], CARD, OUT, 9)
    _outline_poly(d, [(S * .7, S * .3), (S * .94, S * .14), (S * .94, S * .8), (S * .7, S * .96)], CARD_D, OUT, 9)
    _outline_poly(d, [(S * .06, S * .3), (S * .3, S * .14), (S * .94, S * .14), (S * .7, S * .3)], CARD_L, OUT, 9)
    d.line([(S * .2, S * .22), (S * .8, S * .22)], fill=CARD_D, width=4)                              # flap seam
    TAPE = (225, 200, 140, 255)
    d.polygon([(S * .36, S * .3), (S * .58, S * .14), (S * .66, S * .14), (S * .44, S * .3)], fill=TAPE)  # tape
    d.rectangle([S * .36, S * .3, S * .44, S * .46], fill=TAPE)
    d.rectangle([S * .1, S * .74, S * .36, S * .92], fill=(250, 250, 245, 255), outline=OUT, width=5)  # label
    for k in range(3):
        d.line([(S * .14, S * (.79 + k * .04)), (S * .32, S * (.79 + k * .04))], fill=(90, 90, 90, 255), width=3)
    d.polygon([(S * .54, S * .72), (S * .46, S * .82), (S * .51, S * .82), (S * .51, S * .92), (S * .57, S * .92),
               (S * .57, S * .82), (S * .62, S * .82)], fill=(40, 40, 40, 255))                       # this way up
    im = _shrink(im, size)
    return _texted(im, [("FRAGILE", (24, 34))], (235, 40, 40, 255), (250, 235, 215, 255))


def fragile_box_open(size=64):
    """The same box sliced open: the front cut down jagged, the top flaps flopped out to the sides, packing
    peanuts spilling over."""
    im, d, S = _big(size)
    OUT, CARD, CARD_D, CARD_L = (45, 25, 10, 255), (205, 150, 85, 255), (160, 110, 55, 255), (235, 190, 125, 255)
    _outline_poly(d, [(S * .74, S * .58), (S * .92, S * .48), (S * .92, S * .86), (S * .74, S * .98)], CARD_D, OUT, 8)
    _outline_poly(d, [(S * .1, S * .58), (S * -.02, S * .38), (S * .14, S * .34), (S * .26, S * .62)], CARD_L, OUT, 8)
    _outline_poly(d, [(S * .74, S * .58), (S * .99, S * .36), (S * .99, S * .5), (S * .82, S * .66)], CARD_L, OUT, 8)
    rnd = __import__("random").Random(3)
    for k in range(16):                                                                               # peanuts
        x, y = S * rnd.uniform(.16, .8), S * rnd.uniform(.48, .66)
        d.ellipse([x - S * .05, y - S * .03, x + S * .05, y + S * .03], fill=(250, 248, 235, 255), outline=OUT, width=4)
    front = [(S * .1, S * .58), (S * .26, S * .7), (S * .42, S * .6), (S * .58, S * .72), (S * .74, S * .58),
             (S * .74, S * .98), (S * .1, S * .98)]
    _outline_poly(d, front, CARD, OUT, 9)
    d.rectangle([S * .14, S * .82, S * .4, S * .94], fill=(250, 250, 245, 255), outline=OUT, width=5)
    return _shrink(im, size)


def box_cutter(size=64, out=True):
    """A yellow box cutter pointing right, the silver segmented blade clicked all the way out (or tucked in)."""
    im, d, S = _big(size)
    OUT, YEL, YEL_L, YEL_D = (30, 25, 5, 255), (255, 205, 30, 255), (255, 240, 140, 255), (200, 150, 10, 255)
    if out:
        blade = [(S * .52, S * .41), (S * .98, S * .39), (S * .84, S * .57), (S * .52, S * .57)]
        _outline_poly(d, blade, (215, 220, 230, 255), OUT, 7)
        for k in range(4):                                                                            # snap lines
            x = S * (.6 + k * .08)
            d.line([(x + S * .04, S * .42), (x, S * .56)], fill=(140, 145, 160, 255), width=4)
        d.line([(S * .56, S * .45), (S * .9, S * .43)], fill=(255, 255, 255, 255), width=4)
    else:
        _outline_poly(d, [(S * .52, S * .43), (S * .64, S * .43), (S * .6, S * .55), (S * .52, S * .55)],
                      (215, 220, 230, 255), OUT, 6)
    _outline_poly(d, [(S * .04, S * .38), (S * .58, S * .35), (S * .62, S * .63), (S * .04, S * .67)], YEL, OUT, 9)
    d.line([(S * .1, S * .43), (S * .54, S * .4)], fill=YEL_L, width=6)
    d.rectangle([S * .12, S * .57, S * .54, S * .62], fill=YEL_D)
    d.rounded_rectangle([S * .28, S * .29, S * .44, S * .4], 6, fill=(60, 60, 65, 255), outline=OUT, width=5)  # slider
    for k in range(3):
        d.line([(S * (.32 + k * .04), S * .31), (S * (.32 + k * .04), S * .38)], fill=(150, 150, 160, 255), width=3)
    return _shrink(im, size)


def x_slash(size=64):
    """Two fresh cuts crossed in an X: bright white gashes with a dark edge."""
    im, d, S = _big(size)
    for (x0, y0, x1, y1) in ((.12, .14, .88, .86), (.86, .12, .14, .88)):
        d.line([(S * x0, S * y0), (S * x1, S * y1)], fill=(30, 20, 20, 255), width=int(S * .13))
        d.line([(S * x0, S * y0), (S * x1, S * y1)], fill=(255, 255, 255, 255), width=int(S * .07))
        d.line([(S * (x0 * .7 + x1 * .3), S * (y0 * .7 + y1 * .3)), (S * (x0 * .3 + x1 * .7), S * (y0 * .3 + y1 * .7))],
               fill=(255, 255, 210, 255), width=int(S * .1))
    return _shrink(im, size)


def peanut(n=16):
    """A packing peanut: a fat little S-curve (alpha only)."""
    def f(x, y):
        for cx, cy in ((5, 6), (8, 8), (11, 10)):
            if (x - cx) ** 2 + (y - cy) ** 2 <= 8:
                return 1
        return 0
    return _alpha(n, n, f)


def barbell(size=64, plates=3):
    """An Olympic barbell seen from the front, chrome bar with `plates` plates a side (0-3): the big black
    45s, blue 25s, red 10s; spring collars."""
    im, d, S = _big(size)
    OUT = (15, 15, 18, 255)
    d.rectangle([S * .0, S * .465, S * 1.0, S * .535], fill=(205, 210, 220, 255), outline=OUT, width=5)  # the bar
    d.line([(S * .02, S * .485), (S * .98, S * .485)], fill=(250, 250, 255, 255), width=3)
    d.rectangle([S * .4, S * .47, S * .6, S * .53], fill=(150, 155, 165, 255))                        # knurl
    specs = [(.34, (35, 35, 40, 255), (100, 100, 110, 255)), (.27, (40, 80, 210, 255), (130, 170, 255, 255)),
             (.2, (210, 40, 40, 255), (255, 140, 140, 255))]
    for k in range(plates):
        h, col, hi = specs[k]
        for side in (-1, 1):
            x = .5 + side * (.25 + k * .075)
            d.rounded_rectangle([S * (x - .035), S * (.5 - h), S * (x + .035), S * (.5 + h)], 8, fill=col, outline=OUT, width=6)
            d.line([(S * (x - .012), S * (.5 - h + .04)), (S * (x - .012), S * (.5 + h - .04))], fill=hi, width=4)
    for side in (-1, 1):                                                                               # collars
        x = .5 + side * (.25 + plates * .075 - .01)
        d.rectangle([S * (x - .015), S * .43, S * (x + .015), S * .57], fill=(230, 200, 60, 255), outline=OUT, width=4)
    return _shrink(im, size)


def weight_plate(size=32):
    """A red 10 bumper plate face-on, rolling: rim, the grip holes, the centre hole (no text: it spins)."""
    import math
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.ellipse([S * .04, S * .04, S * .96, S * .96], fill=(210, 40, 40, 255), outline=OUT, width=7)
    d.ellipse([S * .14, S * .14, S * .86, S * .86], outline=(150, 20, 25, 255), width=5)
    for a in range(30, 390, 120):                                                                      # grips
        cx, cy = S * (.5 + .27 * math.cos(math.radians(a))), S * (.5 + .27 * math.sin(math.radians(a)))
        d.ellipse([cx - S * .09, cy - S * .06, cx + S * .09, cy + S * .06], fill=OUT)
    d.ellipse([S * .4, S * .4, S * .6, S * .6], fill=(200, 205, 215, 255), outline=OUT, width=5)
    d.arc([S * .1, S * .1, S * .9, S * .9], 200, 260, fill=(255, 150, 150, 255), width=6)
    return _shrink(im, size)


def jewelry_case(size=64, broken=False):
    """A glass jewelry display case on a wooden stand: gold chains, a watch and a ring on red velvet behind the
    glass - or smashed: jagged glass, the velvet cleaned out."""
    im, d, S = _big(size)
    OUT = (20, 15, 15, 255)
    GOLD, GOLD_D = (255, 205, 40, 255), (220, 160, 20, 255)
    d.rectangle([S * .08, S * .62, S * .92, S * .96], fill=(120, 70, 35, 255), outline=OUT, width=8)   # stand
    d.line([(S * .12, S * .7), (S * .88, S * .7)], fill=(165, 105, 60, 255), width=5)
    d.rectangle([S * .1, S * .5, S * .9, S * .62], fill=(170, 25, 40, 255), outline=OUT, width=7)       # velvet
    if not broken:
        d.rectangle([S * .08, S * .12, S * .92, S * .62], fill=(170, 220, 255, 255), outline=OUT, width=8)  # glass
        d.rectangle([S * .1, S * .5, S * .9, S * .6], fill=(170, 25, 40, 255))
        d.arc([S * .14, S * .2, S * .46, S * .62], 15, 165, fill=OUT, width=13)                         # chains
        d.arc([S * .14, S * .2, S * .46, S * .62], 15, 165, fill=GOLD, width=8)
        d.arc([S * .2, S * .28, S * .5, S * .64], 15, 165, fill=OUT, width=11)
        d.arc([S * .2, S * .28, S * .5, S * .64], 15, 165, fill=GOLD_D, width=6)
        d.rounded_rectangle([S * .54, S * .36, S * .68, S * .54], 4, fill=GOLD, outline=OUT, width=5)   # watch
        d.ellipse([S * .565, S * .39, S * .655, S * .51], fill=(250, 250, 255, 255), outline=OUT, width=3)
        d.ellipse([S * .72, S * .44, S * .86, S * .56], outline=OUT, width=10)                         # ring
        d.ellipse([S * .73, S * .45, S * .85, S * .55], outline=GOLD, width=5)
        d.polygon([(S * .79, S * .32), (S * .74, S * .4), (S * .79, S * .45), (S * .84, S * .4)], fill=(220, 250, 255, 255), outline=OUT)
        d.line([(S * .14, S * .2), (S * .3, S * .2)], fill=(255, 255, 255, 255), width=6)               # shine
        d.line([(S * .16, S * .3), (S * .36, S * .16)], fill=(255, 255, 255, 255), width=5)
        d.line([(S * .76, S * .2), (S * .86, S * .16)], fill=(255, 255, 255, 255), width=4)
    else:
        jag = [(S * .08, S * .5), (S * .08, S * .3), (S * .16, S * .4), (S * .22, S * .24), (S * .28, S * .42),
               (S * .36, S * .5)]
        _outline_poly(d, jag, (170, 220, 255, 255), OUT, 6)
        jag2 = [(S * .92, S * .5), (S * .92, S * .2), (S * .84, S * .34), (S * .78, S * .26), (S * .74, S * .42),
                (S * .66, S * .38), (S * .62, S * .5)]
        _outline_poly(d, jag2, (170, 220, 255, 255), OUT, 6)
        d.line([(S * .12, S * .42), (S * .16, S * .34)], fill=(255, 255, 255, 255), width=4)
        d.line([(S * .86, S * .3), (S * .88, S * .4)], fill=(255, 255, 255, 255), width=4)
        d.rectangle([S * .08, S * .48, S * .92, S * .52], fill=OUT)                                       # the frame left
    return _shrink(im, size)


def crowbar(size=64):
    """A red crowbar swung down-right: the hooked claw end up top, the flat end down (pre-tilted)."""
    im, d, S = _big(size)
    OUT, RED, RED_L = (30, 5, 5, 255), (210, 35, 35, 255), (255, 140, 130, 255)
    d.arc([S * .06, S * .02, S * .4, S * .34], 110, 330, fill=OUT, width=int(S * .13))             # the hook
    d.line([(S * .34, S * .24), (S * .86, S * .86)], fill=OUT, width=int(S * .13))
    d.arc([S * .06, S * .02, S * .4, S * .34], 110, 330, fill=RED, width=int(S * .075))
    d.line([(S * .34, S * .24), (S * .86, S * .86)], fill=RED, width=int(S * .075))
    d.line([(S * .38, S * .26), (S * .84, S * .8)], fill=RED_L, width=int(S * .025))
    d.line([(S * .84, S * .86), (S * .97, S * .84)], fill=OUT, width=int(S * .1))                   # flat end
    d.line([(S * .84, S * .86), (S * .95, S * .84)], fill=(200, 200, 210, 255), width=int(S * .05))
    return _shrink(im, size)


def glass_shard(n=16):
    """A jagged sliver of broken glass (alpha only)."""
    def f(x, y):
        u, v = x - 3, y - 2
        inside = u >= 0 and v >= 0 and u * .9 + v * .45 <= 10 and v <= 12 - u * .4
        edge = inside and (u < 1.5 or v < 1.5)
        return 1 if edge else (.65 if inside else 0)
    return _alpha(n, n, f)


def gold_chain_loot(size=32):
    """A thick gold Cuban link chain with a big dollar-sign medallion, flying."""
    import math
    im, d, S = _big(size)
    OUT, GOLD, GOLD_L, GOLD_D = (60, 35, 0, 255), (255, 200, 30, 255), (255, 245, 160, 255), (200, 140, 10, 255)
    for k in range(11):
        a = math.radians(180 + k * 18)
        x, y = S * (.5 + .4 * math.cos(a)), S * (.4 - .32 * math.sin(a))
        d.ellipse([x - S * .08, y - S * .06, x + S * .08, y + S * .06], fill=GOLD, outline=OUT, width=4)
    d.ellipse([S * .28, S * .48, S * .72, S * .92], fill=GOLD, outline=OUT, width=7)
    d.ellipse([S * .35, S * .55, S * .65, S * .85], fill=GOLD_D)
    d.line([(S * .5, S * .54), (S * .5, S * .86)], fill=GOLD_L, width=5)
    d.arc([S * .41, S * .58, S * .59, S * .7], 90, 300, fill=GOLD_L, width=5)
    d.arc([S * .41, S * .68, S * .59, S * .8], 270, 480, fill=GOLD_L, width=5)
    return _shrink(im, size)


def shovel_dig(size=64):
    """A shovel stuck in a fresh dirt pile, handle up at an angle (the D-grip), clods round it."""
    im, d, S = _big(size)
    OUT, DIRT, DIRT_L, DIRT_D = (30, 18, 8, 255), (130, 85, 45, 255), (175, 125, 75, 255), (90, 55, 25, 255)
    d.line([(S * .58, S * .56), (S * .78, S * .12)], fill=OUT, width=int(S * .09))                  # shaft
    d.line([(S * .58, S * .56), (S * .78, S * .12)], fill=(200, 150, 85, 255), width=int(S * .05))
    d.rounded_rectangle([S * .68, S * .02, S * .9, S * .13], 8, outline=OUT, width=int(S * .05))     # D-grip
    d.rounded_rectangle([S * .69, S * .03, S * .89, S * .12], 8, outline=(200, 150, 85, 255), width=int(S * .02))
    _outline_poly(d, [(S * .46, S * .5), (S * .68, S * .58), (S * .62, S * .8), (S * .46, S * .74)], (165, 170, 180, 255), OUT, 7)
    pile = [(S * .02, S * .97), (S * .14, S * .76), (S * .3, S * .66), (S * .48, S * .64), (S * .66, S * .72),
            (S * .84, S * .82), (S * .98, S * .97)]
    _outline_poly(d, pile, DIRT, OUT, 8)
    for x, y in ((.24, .8), (.4, .74), (.7, .86), (.52, .88), (.32, .91), (.84, .92)):
        d.ellipse([S * x - S * .045, S * y - S * .03, S * x + S * .045, S * y + S * .03], fill=DIRT_D)
        d.ellipse([S * x - S * .03, S * y - S * .03, S * x + S * .01, S * y], fill=DIRT_L)
    return _shrink(im, size)


def dirt_hole(size=64):
    """A freshly dug hole, flat on the ground: black inside, a rim of thrown dirt round it."""
    im, d, S = _big(size)
    OUT = (25, 15, 5, 255)
    d.ellipse([S * .02, S * .36, S * .98, S * .9], fill=(140, 92, 48, 255), outline=OUT, width=8)
    rnd = __import__("random").Random(9)
    for k in range(14):
        x, y = S * rnd.uniform(.1, .9), S * rnd.uniform(.42, .84)
        d.ellipse([x - S * .05, y - S * .03, x + S * .05, y + S * .03], fill=(105, 66, 32, 255))
    d.ellipse([S * .18, S * .48, S * .82, S * .8], fill=(15, 10, 8, 255), outline=OUT, width=6)
    d.arc([S * .18, S * .48, S * .82, S * .8], 190, 350, fill=(80, 52, 28, 255), width=10)
    return _shrink(im, size)


def sawhorse(size=64):
    """A road-work barricade: an orange-and-white striped board on two legs, a flashing amber light on top."""
    im, d, S = _big(size)
    OUT = (25, 20, 15, 255)
    for x0, x1 in ((.2, .1), (.2, .3), (.8, .7), (.8, .9)):                                            # legs
        d.line([(S * x0, S * .5), (S * x1, S * .96)], fill=OUT, width=int(S * .07))
        d.line([(S * x0, S * .5), (S * x1, S * .96)], fill=(240, 240, 235, 255), width=int(S * .035))
    d.rectangle([S * .04, S * .36, S * .96, S * .58], fill=(250, 250, 245, 255))
    for k in range(5):
        x = S * (.04 + k * .2)
        d.polygon([(x, S * .58), (x + S * .1, S * .36), (x + S * .2, S * .36), (x + S * .1, S * .58)], fill=(255, 120, 20, 255))
    d.rectangle([S * .04, S * .36, S * .96, S * .58], outline=OUT, width=8)
    d.rectangle([S * .44, S * .26, S * .56, S * .36], fill=(50, 50, 55, 255), outline=OUT, width=5)    # the light
    d.ellipse([S * .36, S * .04, S * .64, S * .3], fill=(255, 190, 30, 255), outline=OUT, width=7)
    d.ellipse([S * .43, S * .09, S * .52, S * .18], fill=(255, 250, 200, 255))
    return _shrink(im, size)


def dirt_clod(n=16):
    """A lumpy clod of dirt (alpha only)."""
    def f(x, y):
        r = ((x - 7.5) ** 2 + (y - 8) ** 2 * 1.3) ** .5
        bump = .9 * ((x * 7 + y * 3) % 4 == 0)
        return 1 if r < 5.2 + bump else 0
    return _alpha(n, n, f)


def coil_burner(size=64):
    """An electric stovetop coil burner seen at an angle, glowing red-hot on the black stovetop, the knob on
    HI."""
    im, d, S = _big(size)
    OUT = (10, 10, 10, 255)
    d.rounded_rectangle([S * .02, S * .44, S * .98, S * .96], 12, fill=(35, 35, 40, 255), outline=OUT, width=8)  # stovetop
    d.line([(S * .06, S * .5), (S * .94, S * .5)], fill=(100, 100, 110, 255), width=4)
    d.ellipse([S * .08, S * .5, S * .8, S * .9], fill=(75, 75, 82, 255), outline=OUT, width=6)          # drip pan
    for k in range(4):                                                                                 # the coil
        r = .3 - k * .07
        box = [S * (.44 - r), S * (.7 - r * .55), S * (.44 + r), S * (.7 + r * .55)]
        d.ellipse(box, outline=OUT, width=int(S * .065))
        d.ellipse(box, outline=(255, 60 + k * 40, 20 + k * 10, 255), width=int(S * .035))
    d.ellipse([S * .38, S * .67, S * .5, S * .73], fill=(255, 220, 90, 255))
    d.ellipse([S * .82, S * .58, S * .96, S * .72], fill=(225, 225, 230, 255), outline=OUT, width=6)    # knob on HI
    d.line([(S * .89, S * .65), (S * .94, S * .6)], fill=(220, 30, 30, 255), width=5)
    return _shrink(im, size)


def flaming_glove(size=64):
    """A boxing glove punching right, scorched orange-red and ON FIRE: flames streaming back off it."""
    im, d, S = _big(size)
    OUT = (40, 8, 0, 255)
    for k, (y, ln) in enumerate(((.26, .5), (.42, .6), (.58, .55), (.72, .42))):                       # flames trailing
        d.polygon([(S * .5, S * (y - .08)), (S * (.5 - ln), S * (y + .02)), (S * .5, S * (y + .11))], fill=(255, 130, 20, 255))
        d.polygon([(S * .5, S * (y - .03)), (S * (.5 - ln * .6), S * (y + .02)), (S * .5, S * (y + .06))], fill=(255, 235, 80, 255))
    d.rectangle([S * .14, S * .36, S * .36, S * .68], fill=(250, 240, 220, 255), outline=OUT, width=8)  # cuff
    d.ellipse([S * .28, S * .16, S * .96, S * .86], fill=(235, 70, 20, 255), outline=OUT, width=10)    # the glove
    d.ellipse([S * .38, S * .54, S * .64, S * .84], fill=(190, 40, 10, 255), outline=OUT, width=8)      # thumb
    d.arc([S * .4, S * .24, S * .86, S * .6], 200, 290, fill=(255, 210, 120, 255), width=12)
    d.polygon([(S * .66, S * .16), (S * .72, S * .0), (S * .79, S * .17)], fill=(255, 200, 40, 255))   # licking up
    d.polygon([(S * .48, S * .2), (S * .53, S * .05), (S * .59, S * .2)], fill=(255, 150, 30, 255))
    return _shrink(im, size)


def hot_glove(size=64):
    """The boxing glove sitting ON the burner heating up: plain red, glowing orange at the bottom, sweat-steam
    wisps (no flames yet)."""
    im, d, S = _big(size)
    OUT = (40, 8, 0, 255)
    d.rectangle([S * .14, S * .36, S * .36, S * .68], fill=(250, 240, 220, 255), outline=OUT, width=8)
    d.ellipse([S * .28, S * .16, S * .96, S * .86], fill=(200, 30, 35, 255), outline=OUT, width=10)
    d.chord([S * .3, S * .18, S * .94, S * .84], 20, 160, fill=(255, 110, 30, 255))                    # glowing hot
    d.ellipse([S * .28, S * .16, S * .96, S * .86], outline=OUT, width=10)
    d.ellipse([S * .38, S * .54, S * .64, S * .84], fill=(160, 25, 25, 255), outline=OUT, width=8)
    d.arc([S * .4, S * .24, S * .86, S * .6], 200, 290, fill=(255, 140, 140, 255), width=12)
    return _shrink(im, size)


def taser_glove(size=64):
    """A blue boxing glove punching right with a black taser duct-taped to the top of it (silver tape X),
    the prongs sticking out past the knuckles, sparking."""
    im, d, S = _big(size)
    OUT = (10, 10, 25, 255)
    d.rectangle([S * .08, S * .4, S * .3, S * .72], fill=(250, 250, 250, 255), outline=OUT, width=8)  # cuff
    d.ellipse([S * .22, S * .3, S * .86, S * .94], fill=(40, 90, 220, 255), outline=OUT, width=10)    # glove
    d.ellipse([S * .3, S * .64, S * .56, S * .92], fill=(25, 60, 170, 255), outline=OUT, width=8)      # thumb
    d.arc([S * .34, S * .38, S * .78, S * .7], 200, 290, fill=(140, 180, 255, 255), width=12)
    d.rounded_rectangle([S * .26, S * .12, S * .84, S * .42], 8, fill=(35, 35, 40, 255), outline=OUT, width=8)  # taser
    d.rectangle([S * .4, S * .19, S * .52, S * .25], fill=(255, 220, 40, 255))                        # its label stripe
    d.ellipse([S * .6, S * .18, S * .68, S * .26], fill=(230, 40, 40, 255))                            # the button
    for y in (.2, .3):                                                                                 # prongs
        d.line([(S * .82, S * y), (S * .94, S * y)], fill=OUT, width=7)
        d.line([(S * .82, S * y), (S * .93, S * y)], fill=(210, 215, 225, 255), width=3)
    d.polygon([(S * .93, S * .14), (S * 1.0, S * .2), (S * .95, S * .24), (S * 1.0, S * .32), (S * .92, S * .36)],
              fill=(255, 250, 120, 255))                                                               # spark
    for x in (.4, .68):                                                                                # the tape
        d.rectangle([S * (x - .06), S * .1, S * (x + .06), S * .46], fill=(200, 205, 215, 255), outline=OUT, width=6)
        d.line([(S * (x - .03), S * .14), (S * (x - .03), S * .42)], fill=(250, 250, 255, 255), width=4)
    return _shrink(im, size)


def zap_burst(size=64):
    """A big electric starburst: jagged yellow lightning rays round a white-hot centre."""
    import math
    im, d, S = _big(size)
    OUT = (60, 40, 0, 255)
    for k in range(8):
        a = k * math.tau / 8 + .2
        pts = [(S * .5, S * .5)]
        r = 0
        for j in range(1, 5):
            r = j * .11
            off = (.06 if j % 2 else -.06)
            pts.append((S * (.5 + r * math.cos(a) + off * math.cos(a + 1.57)), S * (.5 + r * math.sin(a) + off * math.sin(a + 1.57))))
        d.line(pts, fill=OUT, width=int(S * .07), joint="curve")
        d.line(pts, fill=(255, 235, 40, 255), width=int(S * .04), joint="curve")
    d.ellipse([S * .3, S * .3, S * .7, S * .7], fill=(255, 245, 120, 255), outline=OUT, width=6)
    d.ellipse([S * .38, S * .38, S * .62, S * .62], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def zig_spark(n=16):
    """A little zigzag electric spark (alpha only)."""
    pts = [(2, 3), (7, 6), (5, 9), (13, 13)]

    def f(x, y):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            dx, dy = x1 - x0, y1 - y0
            t = max(0, min(1, ((x - x0) * dx + (y - y0) * dy) / (dx * dx + dy * dy)))
            if (x - x0 - t * dx) ** 2 + (y - y0 - t * dy) ** 2 < 1.6:
                return 1
        return 0
    return _alpha(n, n, f)


def bolt_tall(w=16, h=32):
    """A tall jagged lightning bolt (alpha only)."""
    pts = [(9, 1), (4, 12), (10, 14), (5, 30)]

    def f(x, y):
        for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
            dx, dy = x1 - x0, y1 - y0
            t = max(0, min(1, ((x - x0) * dx + (y - y0) * dy) / (dx * dx + dy * dy)))
            dd = (x - x0 - t * dx) ** 2 + (y - y0 - t * dy) ** 2
            if dd < 1.2:
                return 1
            if dd < 3.5:
                return .5
        return 0
    return _alpha(w, h, f)


def brick_phone(size=64):
    """An 80s brick cell phone, standing up: chunky grey body, a long antenna, a tiny green LCD, the keypad."""
    im, d, S = _big(size)
    OUT = (15, 15, 18, 255)
    d.rounded_rectangle([S * .58, S * .0, S * .66, S * .3], 6, fill=(40, 40, 45, 255), outline=OUT, width=5)  # antenna
    d.rounded_rectangle([S * .3, S * .18, S * .7, S * .98], 14, fill=(150, 150, 158, 255), outline=OUT, width=9)
    d.line([(S * .36, S * .26), (S * .36, S * .9)], fill=(200, 200, 210, 255), width=6)
    d.rectangle([S * .38, S * .26, S * .62, S * .4], fill=(120, 190, 90, 255), outline=OUT, width=5)  # LCD
    d.line([(S * .42, S * .33), (S * .54, S * .33)], fill=(40, 80, 30, 255), width=4)
    for r in range(4):                                                                                 # keypad
        for c in range(3):
            x, y = S * (.4 + c * .08), S * (.48 + r * .1)
            d.rounded_rectangle([x, y, x + S * .05, y + S * .06], 3, fill=(60, 60, 66, 255))
    d.rectangle([S * .4, S * .88, S * .6, S * .92], fill=(60, 60, 66, 255))
    return _shrink(im, size)


def vhs_tape(size=64):
    """A black VHS tape, face on: the two window reels, a white label reading VHS (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (8, 8, 10, 255)
    d.rounded_rectangle([S * .02, S * .22, S * .98, S * .78], 8, fill=(30, 30, 34, 255), outline=OUT, width=8)
    d.rectangle([S * .1, S * .3, S * .9, S * .48], fill=(245, 245, 235, 255), outline=OUT, width=5)   # label
    d.line([(S * .12, S * .45), (S * .88, S * .45)], fill=(220, 50, 50, 255), width=5)
    d.rounded_rectangle([S * .26, S * .54, S * .74, S * .72], 6, fill=(70, 70, 80, 255), outline=OUT, width=5)  # window
    for x in (.36, .64):
        d.ellipse([S * (x - .07), S * .56, S * (x + .07), S * .7], fill=(20, 20, 22, 255))
        d.ellipse([S * (x - .03), S * .6, S * (x + .03), S * .66], fill=(230, 230, 235, 255))
    d.line([(S * .06, S * .26), (S * .94, S * .26)], fill=(80, 80, 90, 255), width=4)
    im = _shrink(im, size)
    return _texted(im, [("VHS", (32, 21))], (40, 40, 160, 255), (245, 245, 235, 255))


def cassette(size=64):
    """A mixtape cassette, face on: clear smoke shell, two reels of brown tape, an orange-striped label."""
    im, d, S = _big(size)
    OUT = (15, 10, 5, 255)
    d.rounded_rectangle([S * .02, S * .22, S * .98, S * .8], 8, fill=(200, 200, 205, 255), outline=OUT, width=8)
    d.rectangle([S * .08, S * .28, S * .92, S * .62], fill=(255, 245, 225, 255), outline=OUT, width=5)  # label
    for k, col in enumerate(((240, 120, 30, 255), (230, 60, 40, 255))):
        d.rectangle([S * .08, S * (.3 + k * .05), S * .92, S * (.34 + k * .05)], fill=col)
    d.rounded_rectangle([S * .24, S * .42, S * .76, S * .58], 8, fill=(90, 60, 40, 255), outline=OUT, width=5)
    for x in (.36, .64):
        d.ellipse([S * (x - .06), S * .44, S * (x + .06), S * .56], fill=(240, 240, 240, 255), outline=OUT, width=4)
        for k in range(3):
            d.line([(S * x, S * .5), (S * (x + .05 * (k - 1)), S * (.45 + .05 * (k % 2)))], fill=OUT, width=3)
    d.polygon([(S * .24, S * .8), (S * .3, S * .68), (S * .7, S * .68), (S * .76, S * .8)], fill=(160, 160, 168, 255), outline=OUT)
    return _shrink(im, size)


def light_shaft(w=16, h=32):
    """A tall soft shaft of light, brightest in the middle (alpha only)."""
    def f(x, y):
        return max(0, 1 - abs(x - 7.5) / 4) * min(1, y / 6, (h - 1 - y) / 6)
    return _alpha(w, h, f)


def laser_pointer(size=64):
    """A silver laser pointer pen aimed right, the red button pressed, a red glow at the tip."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rounded_rectangle([S * .06, S * .42, S * .84, S * .58], 10, fill=(195, 200, 212, 255), outline=OUT, width=8)
    d.line([(S * .1, S * .46), (S * .8, S * .46)], fill=(250, 250, 255, 255), width=5)
    d.rectangle([S * .06, S * .44, S * .14, S * .56], fill=(80, 80, 90, 255))                         # end cap
    d.rounded_rectangle([S * .4, S * .34, S * .52, S * .44], 4, fill=(225, 30, 30, 255), outline=OUT, width=5)  # button
    d.polygon([(S * .84, S * .44), (S * .92, S * .47), (S * .92, S * .53), (S * .84, S * .56)], fill=(120, 120, 130, 255), outline=OUT)
    d.ellipse([S * .88, S * .42, S * 1.0, S * .58], fill=(255, 60, 60, 200))
    d.ellipse([S * .91, S * .46, S * .97, S * .54], fill=(255, 220, 220, 255))
    d.line([(S * .2, S * .54), (S * .36, S * .54)], fill=(150, 150, 160, 255), width=4)               # pocket clip
    return _shrink(im, size)


def pointer_dot(n=16):
    """A laser dot: a hard bright core in a soft glow ring (alpha only)."""
    c = (n - 1) / 2

    def f(x, y):
        r = ((x - c) ** 2 + (y - c) ** 2) ** .5
        return 1 if r < 2.6 else max(0, .7 - (r - 2.6) / 5)
    return _alpha(n, n, f)


def wavy_ring(n=16):
    """A wobbly psychedelic ring (alpha only)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        r = ((x - c) ** 2 + (y - c) ** 2) ** .5
        a = math.atan2(y - c, x - c)
        return 1 if abs(r - (5.3 + .9 * math.sin(a * 5))) < 1.3 else 0
    return _alpha(n, n, f)


def hypno_swirl(size=64):
    """A rainbow hypno-spiral, seen at an angle over someone's head."""
    import math
    im, d, S = _big(size)
    cols = [(255, 60, 60, 255), (255, 160, 30, 255), (255, 240, 60, 255), (60, 220, 90, 255), (60, 140, 255, 255),
            (200, 80, 255, 255)]
    pts = []
    for k in range(160):
        t = k / 159
        a = t * math.tau * 3
        r = .06 + t * .4
        pts.append((S * (.5 + r * math.cos(a)), S * (.5 + r * .55 * math.sin(a))))
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=(20, 10, 30, 255), width=int(S * .085))
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=cols[i * 6 // len(pts)], width=int(S * .05))
    return _shrink(im, size)


def monster_tire(size=64):
    """A huge lifted-truck tire, side on: chunky knobby tread all round, a chrome rim, caked with mud."""
    import math
    im, d, S = _big(size)
    OUT = (8, 8, 10, 255)
    for k in range(16):                                                                                # tread lugs
        a = k * math.tau / 16
        cx, cy = S * (.5 + .44 * math.cos(a)), S * (.5 + .44 * math.sin(a))
        d.ellipse([cx - S * .07, cy - S * .07, cx + S * .07, cy + S * .07], fill=(35, 35, 38, 255), outline=OUT, width=5)
    d.ellipse([S * .08, S * .08, S * .92, S * .92], fill=(45, 45, 50, 255), outline=OUT, width=8)
    d.ellipse([S * .26, S * .26, S * .74, S * .74], fill=(205, 210, 220, 255), outline=OUT, width=7)  # rim
    for k in range(5):
        a = k * math.tau / 5 - 1.57
        d.line([(S * .5, S * .5), (S * (.5 + .2 * math.cos(a)), S * (.5 + .2 * math.sin(a)))], fill=(130, 135, 145, 255), width=int(S * .07))
    d.ellipse([S * .42, S * .42, S * .58, S * .58], fill=(240, 240, 245, 255), outline=OUT, width=5)
    d.arc([S * .3, S * .3, S * .7, S * .7], 200, 260, fill=(255, 255, 255, 255), width=6)
    for (x, y, r) in ((.2, .7, .1), (.66, .82, .08), (.82, .4, .07), (.3, .2, .06)):                   # mud
        d.ellipse([S * (x - r), S * (y - r * .7), S * (x + r), S * (y + r * .7)], fill=(115, 75, 35, 255))
    return _shrink(im, size)


def mud_puddle(size=64):
    """A wide brown mud puddle lying flat in the street, a shine on it."""
    im, d, S = _big(size)
    OUT = (40, 25, 10, 255)
    d.ellipse([S * .02, S * .5, S * .62, S * .86], fill=(105, 70, 35, 255), outline=OUT, width=7)
    d.ellipse([S * .4, S * .44, S * .98, S * .82], fill=(105, 70, 35, 255), outline=OUT, width=7)
    d.ellipse([S * .06, S * .54, S * .58, S * .82], fill=(105, 70, 35, 255))
    d.ellipse([S * .44, S * .48, S * .94, S * .78], fill=(105, 70, 35, 255))
    d.ellipse([S * .2, S * .6, S * .8, S * .76], fill=(85, 55, 25, 255))
    d.arc([S * .3, S * .56, S * .7, S * .66], 200, 330, fill=(190, 160, 120, 255), width=6)
    d.line([(S * .66, S * .54), (S * .8, S * .54)], fill=(210, 185, 150, 255), width=5)
    return _shrink(im, size)


def mud_glob(w=16, h=32):
    """A tall splashing glob of mud with drips (alpha only)."""
    def f(x, y):
        body = ((x - 7.5) / 6) ** 2 + ((y - 18) / 12) ** 2 <= 1
        top = (x - 7.5) ** 2 + (y - 6) ** 2 <= 14
        drip = abs(x - 4) < 1.4 and 26 < y < 31
        return 1 if body or top or drip else 0
    return _alpha(w, h, f)


def contact_grill(size=64, shut=False):
    """A George Foreman-style contact grill: the slanted ridged black plates, white body, red light - open
    like a mouth with the lid up, or slammed shut."""
    im, d, S = _big(size)
    OUT = (15, 15, 18, 255)
    WHITE, WHITE_D = (240, 240, 245, 255), (185, 185, 195, 255)
    if not shut:
        d.polygon([(S * .08, S * .08), (S * .92, S * .08), (S * .88, S * .44), (S * .12, S * .44)], fill=WHITE, outline=OUT)
        d.line([(S * .08, S * .08), (S * .92, S * .08), (S * .88, S * .44), (S * .12, S * .44), (S * .08, S * .08)], fill=OUT, width=8)
        d.rectangle([S * .16, S * .14, S * .84, S * .4], fill=(35, 35, 40, 255), outline=OUT, width=5)  # lid plate
        for k in range(6):
            x = S * (.2 + k * .12)
            d.line([(x, S * .16), (x - S * .04, S * .38)], fill=(90, 90, 98, 255), width=5)
        d.rectangle([S * .42, S * .44, S * .58, S * .52], fill=WHITE_D, outline=OUT, width=5)          # hinge
        d.polygon([(S * .04, S * .58), (S * .96, S * .58), (S * .9, S * .84), (S * .1, S * .84)], fill=(35, 35, 40, 255))
        for k in range(6):                                                                             # bottom plate
            x = S * (.14 + k * .14)
            d.line([(x, S * .6), (x + S * .04, S * .82)], fill=(255, 110, 40, 255), width=6)
        d.line([(S * .04, S * .58), (S * .96, S * .58), (S * .9, S * .84), (S * .1, S * .84), (S * .04, S * .58)], fill=OUT, width=8)
        d.rectangle([S * .08, S * .84, S * .92, S * .96], fill=WHITE, outline=OUT, width=7)
    else:
        d.polygon([(S * .06, S * .34), (S * .94, S * .34), (S * .9, S * .64), (S * .1, S * .64)], fill=WHITE)
        d.line([(S * .06, S * .34), (S * .94, S * .34), (S * .9, S * .64), (S * .1, S * .64), (S * .06, S * .34)], fill=OUT, width=8)
        d.line([(S * .1, S * .4), (S * .9, S * .4)], fill=(255, 255, 255, 255), width=5)
        d.rectangle([S * .08, S * .64, S * .92, S * .72], fill=(35, 35, 40, 255), outline=OUT, width=6)  # the seam
        d.rectangle([S * .08, S * .72, S * .92, S * .88], fill=WHITE_D, outline=OUT, width=7)
        d.rounded_rectangle([S * .3, S * .2, S * .7, S * .3], 6, fill=(40, 40, 45, 255), outline=OUT, width=6)  # handle
        d.line([(S * .34, S * .3), (S * .34, S * .36)], fill=OUT, width=6)
        d.line([(S * .66, S * .3), (S * .66, S * .36)], fill=OUT, width=6)
        for dx in (-.1, 0, .1):                                                                        # steam
            d.line([(S * (.5 + dx), S * .58), (S * (.5 + dx), S * .66)], fill=(255, 120, 40, 255), width=4)
    d.ellipse([S * .78, S * .76 if not shut else S * .76, S * .86, S * .84], fill=(255, 50, 40, 255), outline=OUT, width=4)  # light
    return _shrink(im, size)


def grill_marks(size=64):
    """Seared grill marks: four dark diagonal stripes with a hot orange edge, a bit see-through."""
    im, d, S = _big(size)
    for k in range(4):
        x = S * (.16 + k * .2)
        d.line([(x, S * .14), (x + S * .14, S * .86)], fill=(255, 130, 40, 170), width=int(S * .11))
        d.line([(x, S * .14), (x + S * .14, S * .86)], fill=(60, 30, 15, 230), width=int(S * .07))
    return _shrink(im, size)


def car_battery(size=64):
    """A car battery: black box, red + post with its cap, black - post, a yellow 12V label (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rounded_rectangle([S * .06, S * .3, S * .94, S * .94], 8, fill=(40, 40, 46, 255), outline=OUT, width=9)
    d.rectangle([S * .06, S * .3, S * .94, S * .42], fill=(60, 60, 68, 255), outline=OUT, width=7)    # lid
    for x, col in ((.24, (220, 30, 30, 255)), (.76, (30, 30, 34, 255))):                              # posts
        d.rectangle([S * (x - .07), S * .18, S * (x + .07), S * .32], fill=(200, 200, 210, 255), outline=OUT, width=6)
        d.rectangle([S * (x - .09), S * .14, S * (x + .09), S * .22], fill=col, outline=OUT, width=6)
    d.rectangle([S * .16, S * .52, S * .84, S * .82], fill=(255, 210, 40, 255), outline=OUT, width=6)  # label
    d.line([(S * .1, S * .36), (S * .9, S * .36)], fill=(100, 100, 110, 255), width=4)
    im = _shrink(im, size)
    _texted(im, [("12V", (32, 37))], (30, 30, 34, 255), (255, 230, 120, 255), font=GLYPHS)
    _texted(im, [("+", (15, 4)), ("-", (49, 4))], (255, 255, 255, 255))
    return im


def jumper_clamps(size=64, shut=False):
    """Jumper-cable clamps as a pair of jaws facing right: the red clamp on top, the black one below, copper
    teeth - wide open, or CHOMPED shut. The cables trail off to the left."""
    import math
    im, d, S = _big(size)
    OUT = (15, 10, 10, 255)
    gap = 0 if shut else .17
    d.line([(S * .0, S * .3), (S * .2, S * (.42 - gap * .6))], fill=OUT, width=int(S * .09))          # cables
    d.line([(S * .0, S * .3), (S * .2, S * (.42 - gap * .6))], fill=(220, 30, 30, 255), width=int(S * .05))
    d.line([(S * .0, S * .74), (S * .2, S * (.58 + gap * .6))], fill=OUT, width=int(S * .09))
    d.line([(S * .0, S * .74), (S * .2, S * (.58 + gap * .6))], fill=(45, 45, 50, 255), width=int(S * .05))
    for top, col, hi in ((True, (220, 35, 35, 255), (255, 140, 130, 255)), (False, (45, 45, 52, 255), (120, 120, 130, 255))):
        y = .5 - gap if top else .5 + gap
        sgn = -1 if top else 1
        jaw = [(S * .18, S * (y + sgn * .14)), (S * .62, S * (y + sgn * .1)), (S * .96, S * (y + sgn * .02)),
               (S * .96, S * y), (S * .18, S * y)]
        _outline_poly(d, jaw, col, OUT, 8)
        d.line([(S * .24, S * (y + sgn * .1)), (S * .6, S * (y + sgn * .07))], fill=hi, width=5)
        for k in range(5):                                                                             # copper teeth
            x = S * (.5 + k * .09)
            d.polygon([(x, S * y), (x + S * .045, S * (y - sgn * .07)), (x + S * .09, S * y)], fill=(230, 150, 60, 255), outline=OUT)
        d.rounded_rectangle([S * .14, S * (y + sgn * .02) - S * .06, S * .34, S * (y + sgn * .02) + S * .06], 6, fill=col, outline=OUT, width=6)
    d.ellipse([S * .2, S * .44, S * .32, S * .56], fill=(190, 195, 205, 255), outline=OUT, width=5)    # the pivot
    return _shrink(im, size)


def gas_roses(size=64):
    """Gas-station roses: three red roses on green stems in a crinkly cellophane cone, the orange $4.99
    sticker still on (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 10, 15, 255)
    for x, y in ((.3, .2), (.5, .12), (.7, .22)):
        d.line([(S * x, S * y), (S * .5, S * .7)], fill=(40, 120, 40, 255), width=int(S * .04))
    for x, y in ((.36, .4), (.62, .38)):                                                               # leaves
        d.ellipse([S * (x - .07), S * (y - .03), S * (x + .07), S * (y + .03)], fill=(60, 160, 60, 255), outline=OUT, width=4)
    for x, y in ((.3, .2), (.5, .12), (.7, .22)):                                                      # roses
        d.ellipse([S * (x - .12), S * (y - .1), S * (x + .12), S * (y + .1)], fill=(210, 20, 45, 255), outline=OUT, width=7)
        d.arc([S * (x - .07), S * (y - .06), S * (x + .07), S * (y + .07)], 180, 450, fill=(140, 10, 30, 255), width=6)
        d.arc([S * (x - .08), S * (y - .08), S * (x + .02), S * (y + .02)], 180, 270, fill=(255, 120, 140, 255), width=5)
    cone = [(S * .08, S * .3), (S * .92, S * .3), (S * .56, S * .98), (S * .44, S * .98)]
    d.polygon(cone, fill=(220, 240, 255, 120))
    d.line(cone + [cone[0]], fill=(120, 150, 180, 255), width=6)
    for k in range(4):                                                                                 # crinkles
        d.line([(S * (.2 + k * .2), S * .34), (S * (.38 + k * .08), S * .6)], fill=(255, 255, 255, 220), width=5)
    d.rounded_rectangle([S * .22, S * .64, S * .78, S * .84], 8, fill=(255, 140, 20, 255), outline=OUT, width=6)  # sticker
    im = _shrink(im, size)
    return _texted(im, [("$4.99", (32, 44))], (255, 255, 255, 255), (150, 50, 0, 255), font=GLYPHS)


def wink_twinkle(n=16):
    """A long four-pointed twinkle (alpha only): the wink."""
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = abs(x - c), abs(y - c)
        return 1 if (dx < 1.1 and dy < 7.5 - dx * 3) or (dy < 1.1 and dx < 7.5 - dy * 3) or dx + dy < 2.2 else 0
    return _alpha(n, n, f)


def puffy_heart(n=16):
    """A plump heart with a shine dot (alpha only)."""
    def f(x, y):
        u, v = (x - 7.5) / 6.2, -(y - 7) / 6.2
        inside = (u * u + v * v - 1) ** 3 - u * u * v ** 3 <= 0
        shine = (x - 4.5) ** 2 + (y - 5) ** 2 < 2
        return .55 if shine and inside else (1 if inside else 0)
    return _alpha(n, n, f)


def protein_tub(size=64):
    """A big tub of protein powder: black tub, red screw lid, GAINZ in big yellow letters (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rounded_rectangle([S * .14, S * .24, S * .86, S * .96], 12, fill=(30, 30, 34, 255), outline=OUT, width=9)
    d.rounded_rectangle([S * .1, S * .1, S * .9, S * .26], 8, fill=(220, 35, 35, 255), outline=OUT, width=8)  # lid
    for k in range(7):
        d.line([(S * (.16 + k * .11), S * .13), (S * (.16 + k * .11), S * .23)], fill=(160, 20, 20, 255), width=4)
    d.rectangle([S * .14, S * .34, S * .86, S * .66], fill=(220, 35, 35, 255))
    d.line([(S * .2, S * .3), (S * .2, S * .9)], fill=(80, 80, 90, 255), width=6)                      # shine
    im = _shrink(im, size)
    _texted(im, [("GAINZ", (32, 23))], (255, 225, 40, 255), (20, 10, 10, 255), font=GLYPHS)
    _texted(im, [("CHOCOLATE", (32, 47))], (200, 200, 205, 255), (20, 10, 10, 255))
    return im


def shaker_bottle(size=64):
    """A protein shaker bottle: see-through blue, a chocolate shake sloshing inside with the whisk ball, black
    screw lid and flip cap."""
    im, d, S = _big(size)
    OUT = (10, 15, 30, 255)
    d.rounded_rectangle([S * .28, S * .26, S * .72, S * .96], 12, fill=(150, 200, 255, 200), outline=OUT, width=8)
    d.rounded_rectangle([S * .32, S * .5, S * .68, S * .92], 8, fill=(130, 85, 50, 255))               # the shake
    d.ellipse([S * .4, S * .6, S * .56, S * .74], outline=(220, 225, 235, 255), width=5)               # whisk ball
    for k in range(3):
        d.line([(S * .34, S * (.36 + k * .1)), (S * .4, S * (.36 + k * .1))], fill=OUT, width=3)        # ml marks
    d.rectangle([S * .26, S * .16, S * .74, S * .28], fill=(30, 30, 36, 255), outline=OUT, width=7)     # lid
    d.rounded_rectangle([S * .38, S * .04, S * .62, S * .17], 6, fill=(30, 30, 36, 255), outline=OUT, width=6)  # cap
    d.line([(S * .34, S * .3), (S * .34, S * .9)], fill=(240, 250, 255, 255), width=5)
    return _shrink(im, size)


def shaker_chug(size=64):
    """The shaker tipped way up for the chug (the same bottle turned over, no text)."""
    big = shaker_bottle(size).resize((size * 4, size * 4), Image.LANCZOS).rotate(-125, resample=Image.BICUBIC)
    return big.resize((size, size), Image.LANCZOS)


def chevron(n=16):
    """An up-arrow chevron (alpha only): stats going up."""
    def f(x, y):
        v = y - 3 - abs(x - 7.5) * .9
        return 1 if 0 <= v <= 4 and 1 <= x <= 14 else 0
    return _alpha(n, n, f)


def white_kicks(size=64, wrecked=False):
    """A pair of fresh all-white sneakers, side on - or stepped on: creased toes, a big gray tread print, scuffs,
    a lace snapped."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    WHITE, GREY = (250, 250, 252, 255), (205, 208, 215, 255)
    for k, (x, y) in enumerate(((.02, .1), (.18, .48))):
        upper = [(S * (x + .08), S * (y + .3)), (S * (x + .26), S * (y + .06)), (S * (x + .44), S * (y + .06)),
                 (S * (x + .5), S * (y + .2)), (S * (x + .78), S * (y + .3)), (S * (x + .8), S * (y + .4)),
                 (S * (x + .04), S * (y + .4))]
        _outline_poly(d, upper, WHITE, OUT, 7)
        d.rectangle([S * (x + .03), S * (y + .4), S * (x + .82), S * (y + .48)], fill=GREY, outline=OUT, width=6)  # sole
        d.arc([S * (x + .1), S * (y + .14), S * (x + .5), S * (y + .5)], 200, 300, fill=GREY, width=5)   # swoosh-ish
        for j in range(3):                                                                             # laces
            lx = S * (x + .32 + j * .06)
            d.line([(lx, S * (y + .12 + j * .04)), (lx + S * .05, S * (y + .1 + j * .04))], fill=OUT if not (wrecked and j == 1) else GREY, width=4)
        if wrecked:
            for j in range(3):                                                                         # creases
                cx = S * (x + .58 + j * .05)
                d.line([(cx, S * (y + .24)), (cx + S * .03, S * (y + .36))], fill=(130, 130, 140, 255), width=4)
            d.line([(S * (x + .06), S * (y + .36)), (S * (x + .2), S * (y + .3))], fill=(120, 110, 100, 255), width=6)  # scuff
    if wrecked:
        for k in range(5):                                                                             # the print
            d.rounded_rectangle([S * (.36 + k * .09), S * .3, S * (.42 + k * .09), S * .6], 4, fill=(90, 120, 80, 200))
        d.ellipse([S * .3, S * .22, S * .86, S * .68], outline=(90, 120, 80, 220), width=7)
    else:
        for x, y in ((.84, .12), (.9, .5)):                                                            # fresh sparkle
            d.polygon([(S * x, S * (y - .07)), (S * (x + .02), S * y), (S * x, S * (y + .07)), (S * (x - .02), S * y)], fill=(255, 255, 255, 255), outline=OUT)
    return _shrink(im, size)


def giant_croc(size=64):
    """A giant lime-green Croc coming down sole-first: the holes, the heel strap flipped forward (sport mode),
    jibbitz charms."""
    im, d, S = _big(size)
    OUT = (20, 40, 10, 255)
    LIME, LIME_D, LIME_L = (150, 220, 40, 255), (100, 170, 20, 255), (210, 250, 140, 255)
    body = [(S * .04, S * .5), (S * .14, S * .24), (S * .5, S * .16), (S * .86, S * .26), (S * .96, S * .5),
            (S * .9, S * .7), (S * .1, S * .7)]
    _outline_poly(d, body, LIME, OUT, 9)
    d.rectangle([S * .06, S * .7, S * .94, S * .86], fill=LIME_D, outline=OUT, width=9)                # thick sole
    for k in range(6):                                                                                 # tread
        d.line([(S * (.12 + k * .14), S * .82), (S * (.18 + k * .14), S * .86)], fill=OUT, width=5)
    for r in range(2):                                                                                 # the holes
        for c in range(5 - r):
            x, y = S * (.22 + c * .12 + r * .06), S * (.32 + r * .12)
            d.ellipse([x - S * .03, y - S * .025, x + S * .03, y + S * .025], fill=LIME_D, outline=OUT, width=3)
    d.arc([S * .62, S * .36, S * 1.0, S * .74], 260, 80, fill=OUT, width=int(S * .08))                 # heel strap
    d.arc([S * .62, S * .36, S * 1.0, S * .74], 260, 80, fill=LIME_D, width=int(S * .045))
    for x, y, col in ((.3, .56, (255, 80, 160, 255)), (.48, .56, (255, 220, 40, 255)), (.66, .55, (80, 160, 255, 255))):
        d.ellipse([S * (x - .04), S * (y - .04), S * (x + .04), S * (y + .04)], fill=col, outline=OUT, width=4)  # jibbitz
    d.line([(S * .2, S * .24), (S * .5, S * .2)], fill=LIME_L, width=6)
    return _shrink(im, size)


def anger_vein(n=16):
    """The anime anger vein: four bulging corner arcs round a gap (alpha only)."""
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = x - c, y - c
        if abs(dx) < 1.5 or abs(dy) < 1.5:
            return 0
        r = ((abs(dx) - 1.5) ** 2 + (abs(dy) - 1.5) ** 2) ** .5
        return 1 if 2.2 < ((abs(dx) - 6) ** 2 + (abs(dy) - 6) ** 2) ** .5 < 4.6 and r < 6 else 0
    return _alpha(n, n, f)


def stuff_box(size=64):
    """A cardboard box with UR STUFF scrawled on it in marker, a sleeve and a shoe spilling out the top
    (shown at 1:1)."""
    im, d, S = _big(size)
    OUT, CARD, CARD_L = (45, 25, 10, 255), (200, 145, 80, 255), (235, 190, 125, 255)
    d.rectangle([S * .3, S * .1, S * .5, S * .34], fill=(220, 40, 40, 255), outline=OUT, width=6)      # a sleeve
    d.polygon([(S * .56, S * .2), (S * .86, S * .14), (S * .9, S * .26), (S * .58, S * .32)], fill=(250, 250, 250, 255), outline=OUT)  # a shoe
    d.line([(S * .56, S * .2), (S * .86, S * .14), (S * .9, S * .26), (S * .58, S * .32), (S * .56, S * .2)], fill=OUT, width=6)
    _outline_poly(d, [(S * .06, S * .3), (S * -.02, S * .14), (S * .2, S * .2), (S * .22, S * .3)], CARD_L, OUT, 7)   # flaps
    _outline_poly(d, [(S * .94, S * .3), (S * 1.0, S * .12), (S * .8, S * .2), (S * .78, S * .3)], CARD_L, OUT, 7)
    _outline_poly(d, [(S * .06, S * .3), (S * .94, S * .3), (S * .9, S * .96), (S * .1, S * .96)], CARD, OUT, 9)
    d.line([(S * .5, S * .3), (S * .5, S * .42)], fill=(225, 200, 140, 255), width=10)
    im = _shrink(im, size)
    return _texted(im, [("UR", (32, 34)), ("STUFF", (32, 42))], (25, 25, 30, 255), (235, 190, 125, 255), font=GLYPHS)


def hoodie(size=64):
    """A grey pullover hoodie flung through the air, arms out, hood and drawstrings, the front pocket."""
    im, d, S = _big(size)
    OUT, GREY, GREY_D, GREY_L = (25, 25, 30, 255), (150, 150, 160, 255), (105, 105, 115, 255), (200, 200, 210, 255)
    _outline_poly(d, [(S * .3, S * .3), (S * .02, S * .52), (S * .1, S * .66), (S * .32, S * .5)], GREY_D, OUT, 8)  # arms
    _outline_poly(d, [(S * .7, S * .3), (S * .98, S * .52), (S * .9, S * .66), (S * .68, S * .5)], GREY_D, OUT, 8)
    _outline_poly(d, [(S * .28, S * .28), (S * .72, S * .28), (S * .74, S * .92), (S * .26, S * .92)], GREY, OUT, 9)
    d.ellipse([S * .36, S * .1, S * .64, S * .36], fill=GREY_D, outline=OUT, width=8)                  # hood
    d.ellipse([S * .42, S * .18, S * .58, S * .34], fill=(60, 60, 68, 255))
    for x in (.45, .55):
        d.line([(S * x, S * .34), (S * x, S * .5)], fill=(250, 250, 250, 255), width=4)                 # drawstrings
    _outline_poly(d, [(S * .34, S * .64), (S * .66, S * .64), (S * .7, S * .8), (S * .3, S * .8)], GREY_D, OUT, 6)  # pocket
    d.rectangle([S * .26, S * .86, S * .74, S * .92], fill=GREY_D)
    d.line([(S * .32, S * .34), (S * .32, S * .6)], fill=GREY_L, width=6)
    return _shrink(im, size)


def game_controller(size=64):
    """A black game controller: two grips, the d-pad, four coloured face buttons, two sticks."""
    im, d, S = _big(size)
    OUT = (8, 8, 10, 255)
    body = [(S * .14, S * .3), (S * .86, S * .3), (S * .98, S * .74), (S * .84, S * .84), (S * .66, S * .64),
            (S * .34, S * .64), (S * .16, S * .84), (S * .02, S * .74)]
    _outline_poly(d, body, (40, 40, 46, 255), OUT, 9)
    d.line([(S * .2, S * .36), (S * .8, S * .36)], fill=(100, 100, 110, 255), width=5)
    d.rectangle([S * .2, S * .44, S * .32, S * .48], fill=(130, 130, 140, 255))                        # d-pad
    d.rectangle([S * .24, S * .4, S * .28, S * .52], fill=(130, 130, 140, 255))
    for (x, y), col in zip(((.74, .4), (.82, .46), (.74, .52), (.66, .46)),
                           ((60, 200, 90, 255), (230, 50, 50, 255), (60, 120, 255, 255), (255, 210, 40, 255))):
        d.ellipse([S * (x - .035), S * (y - .035), S * (x + .035), S * (y + .035)], fill=col, outline=OUT, width=3)
    for x in (.38, .62):
        d.ellipse([S * (x - .06), S * .5, S * (x + .06), S * .62], fill=(70, 70, 78, 255), outline=OUT, width=4)
    return _shrink(im, size)


def heart_boxers(size=32):
    """A pair of red boxers with white hearts, flying."""
    im, d, S = _big(size)
    OUT = (40, 5, 10, 255)
    _outline_poly(d, [(S * .1, S * .2), (S * .9, S * .2), (S * .94, S * .86), (S * .56, S * .86), (S * .5, S * .5),
                      (S * .44, S * .86), (S * .06, S * .86)], (220, 30, 50, 255), OUT, 7)
    d.rectangle([S * .1, S * .16, S * .9, S * .3], fill=(250, 250, 250, 255), outline=OUT, width=6)    # waistband
    for x, y in ((.24, .5), (.72, .48), (.28, .74), (.76, .74), (.5, .38)):
        d.ellipse([S * (x - .07), S * (y - .05), S * x, S * (y + .02)], fill=(255, 255, 255, 255))
        d.ellipse([S * x, S * (y - .05), S * (x + .07), S * (y + .02)], fill=(255, 255, 255, 255))
        d.polygon([(S * (x - .07), S * y), (S * (x + .07), S * y), (S * x, S * (y + .08))], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def torn_photo(size=32):
    """A framed couple photo torn right down the middle: two little heads, a heart, the jagged rip."""
    im, d, S = _big(size)
    OUT = (30, 20, 10, 255)
    d.rectangle([S * .06, S * .1, S * .94, S * .9], fill=(200, 160, 60, 255), outline=OUT, width=7)    # frame
    d.rectangle([S * .16, S * .2, S * .84, S * .8], fill=(150, 210, 250, 255), outline=OUT, width=5)
    for x, col in ((.32, (120, 70, 40, 255)), (.68, (240, 190, 150, 255))):
        d.ellipse([S * (x - .1), S * .32, S * (x + .1), S * .52], fill=col, outline=OUT, width=4)
        d.rectangle([S * (x - .12), S * .52, S * (x + .12), S * .8], fill=(240, 80, 120, 255) if x > .5 else (60, 90, 200, 255), outline=OUT, width=4)
    rip = [(S * .5, S * .06), (S * .44, S * .3), (S * .56, S * .46), (S * .44, S * .66), (S * .54, S * .94)]
    d.line(rip, fill=(255, 255, 255, 255), width=8)
    d.line(rip, fill=OUT, width=3)
    return _shrink(im, size)


def chrome_revolver(size=64):
    """A chrome revolver side on, pointing right, the trigger guard right at the centre (it spins round the
    finger there): long barrel, the cylinder, hammer back, a pearl grip with gold screws."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    CH, CH_L, CH_D = (200, 205, 218, 255), (250, 252, 255, 255), (130, 135, 150, 255)
    _outline_poly(d, [(S * .36, S * .36), (S * .98, S * .36), (S * .98, S * .46), (S * .36, S * .46)], CH, OUT, 7)  # barrel
    d.line([(S * .4, S * .39), (S * .94, S * .39)], fill=CH_L, width=4)
    d.rectangle([S * .9, S * .3, S * .94, S * .36], fill=CH_D, outline=OUT, width=4)                    # front sight
    d.rounded_rectangle([S * .3, S * .32, S * .5, S * .56], 6, fill=CH_D, outline=OUT, width=7)          # cylinder
    for k in range(3):
        d.line([(S * (.34 + k * .05), S * .35), (S * (.34 + k * .05), S * .53)], fill=OUT, width=3)
    _outline_poly(d, [(S * .14, S * .34), (S * .32, S * .32), (S * .32, S * .56), (S * .2, S * .58)], CH, OUT, 7)  # frame
    _outline_poly(d, [(S * .12, S * .3), (S * .2, S * .24), (S * .24, S * .32)], CH_D, OUT, 5)          # hammer
    d.arc([S * .4, S * .46, S * .6, S * .66], 0, 180, fill=OUT, width=int(S * .04))                    # trigger guard
    d.line([(S * .47, S * .5), (S * .5, S * .58)], fill=OUT, width=5)                                  # trigger
    grip = [(S * .14, S * .54), (S * .3, S * .56), (S * .22, S * .92), (S * .04, S * .9)]
    _outline_poly(d, grip, (245, 240, 225, 255), OUT, 8)                                               # pearl grip
    d.line([(S * .16, S * .6), (S * .1, S * .86)], fill=(220, 210, 240, 255), width=5)
    d.ellipse([S * .14, S * .68, S * .2, S * .74], fill=(255, 210, 50, 255), outline=OUT, width=3)
    return _shrink(im, size)


def power_flare(w=16, h=32):
    """A licking flare of power, pointed at the top (alpha only)."""
    def f(x, y):
        half = 6.5 * (y / (h - 1)) ** .6
        return 1 if abs(x - 7.5) < half and y > 1 else 0
    return _alpha(w, h, f)


def spin_arc(n=16):
    """A curved motion line, a quarter circle (alpha only): something spinning fast."""
    c = (n - 1) / 2

    def f(x, y):
        r = ((x - c) ** 2 + (y - c) ** 2) ** .5
        return 1 if abs(r - 6) < 1.1 and x > c and y < c else 0
    return _alpha(n, n, f)


def card_fan(size=64):
    """A deck of cards fanned out in the hand, red backs with a white diamond pattern."""
    import math
    im, d, S = _big(size)
    OUT = (25, 10, 10, 255)
    for k in range(6):
        a = math.radians(-40 + k * 16)
        cx, cy = S * .5, S * .86
        w, h = S * .16, S * .28
        pts = []
        for px, py in ((-w, -h * 2.2), (w, -h * 2.2), (w, 0), (-w, 0)):
            pts.append((cx + px * math.cos(a) - py * math.sin(a), cy + px * math.sin(a) + py * math.cos(a)))
        _outline_poly(d, pts, (250, 250, 250, 255), OUT, 7)
        inner = [((x - cx) * .78 + cx, (y - cy) * .9 + cy - S * .02) for x, y in pts]
        d.polygon(inner, fill=(200, 30, 40, 255))
    return _shrink(im, size)


def ace_card(size=32):
    """The ace of spades, face on: white card, a black A in the corner, the big spade (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (20, 20, 25, 255)
    d.rounded_rectangle([6, 1, 25, 30], 2, fill=(252, 252, 250, 255), outline=OUT)
    d.rectangle([7, 2, 24, 29], outline=(200, 200, 205, 255))
    sp = [(16, 9), (21, 15), (20, 18), (17, 18), (18, 22), (14, 22), (15, 18), (12, 18), (11, 15)]
    d.polygon(sp, fill=OUT)
    d.ellipse([10, 13, 16, 19], fill=OUT)
    d.ellipse([16, 13, 22, 19], fill=OUT)
    m = _text_mask("A")
    im.paste(OUT, (8, 3), m)
    return im


def card_swoosh(n=16):
    """A short white swoosh line (alpha only): the card's trail."""
    def f(x, y):
        return max(0, 1 - abs(y - 8) / 1.6) * min(1, x / 10)
    return _alpha(n, n, f)


def slash_single(size=64):
    """One clean diagonal slice: a white blade-cut with a dark edge, tapering at both ends."""
    im, d, S = _big(size)
    for wdt, col in ((.12, (30, 20, 30, 255)), (.07, (255, 255, 255, 255)), (.03, (255, 250, 200, 255))):
        d.polygon([(S * .1, S * .88), (S * (.5 - wdt), S * (.5 - wdt)), (S * .9, S * .12), (S * (.5 + wdt), S * (.5 + wdt))], fill=col)
    return _shrink(im, size)


def claw_machine(size=64, state=0):
    """An arcade claw-machine claw hanging off its cable: 0 = three prongs wide open, 2 = clamped round a
    designer bag (the strap hanging out)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    CH, CH_L = (200, 205, 215, 255), (250, 250, 255, 255)
    d.line([(S * .5, S * .0), (S * .5, S * .3)], fill=OUT, width=int(S * .05))                       # cable
    d.line([(S * .5, S * .0), (S * .5, S * .3)], fill=(170, 175, 185, 255), width=int(S * .025))
    if state == 2:                                                                                     # the bag, grabbed
        d.rounded_rectangle([S * .3, S * .52, S * .7, S * .86], 8, fill=(140, 90, 45, 255), outline=OUT, width=7)
        for r in range(3):
            for c in range(3):
                x, y = S * (.38 + c * .12), S * (.6 + r * .09)
                d.polygon([(x, y - S * .025), (x + S * .025, y), (x, y + S * .025), (x - S * .025, y)], fill=(225, 190, 110, 255))
        d.arc([S * .62, S * .7, S * .92, S * 1.0], 270, 90, fill=OUT, width=7)                          # strap
    d.rounded_rectangle([S * .36, S * .28, S * .64, S * .42], 6, fill=CH, outline=OUT, width=7)       # the hub
    d.line([(S * .4, S * .32), (S * .6, S * .32)], fill=CH_L, width=4)
    spread = .26 if state == 0 else .16
    for side in (-1, 1):
        x0, x1 = .5 + side * .1, .5 + side * spread
        pts = [(S * x0, S * .4), (S * x1, S * .58), (S * (x1 - side * .06), S * .82)]
        d.line(pts, fill=OUT, width=int(S * .07), joint="curve")
        d.line(pts, fill=CH, width=int(S * .035), joint="curve")
    d.line([(S * .5, S * .42), (S * .5, S * .84 if state == 0 else S * .9)], fill=OUT, width=int(S * .07))  # middle prong
    d.line([(S * .5, S * .42), (S * .5, S * .84 if state == 0 else S * .9)], fill=CH, width=int(S * .035))
    return _shrink(im, size)


def claw_cable(size=64):
    """A length of the claw machine's steel cable, top to bottom."""
    im, d, S = _big(size)
    d.line([(S * .5, 0), (S * .5, S)], fill=(20, 20, 25, 255), width=int(S * .05))
    d.line([(S * .5, 0), (S * .5, S)], fill=(170, 175, 185, 255), width=int(S * .025))
    return _shrink(im, size)


def designer_bag(size=64):
    """A designer handbag: brown monogram canvas (gold flower-diamonds), tan leather handles and trim, gold
    clasp. Glistening."""
    im, d, S = _big(size)
    OUT = (30, 15, 5, 255)
    d.arc([S * .26, S * .1, S * .74, S * .6], 180, 360, fill=OUT, width=int(S * .08))                  # handle
    d.arc([S * .26, S * .1, S * .74, S * .6], 180, 360, fill=(215, 160, 100, 255), width=int(S * .045))
    _outline_poly(d, [(S * .12, S * .38), (S * .88, S * .38), (S * .96, S * .9), (S * .04, S * .9)], (130, 82, 40, 255), OUT, 9)
    for r in range(3):
        for c in range(5):
            x, y = S * (.2 + c * .15 + (r % 2) * .07), S * (.5 + r * .13)
            d.polygon([(x, y - S * .035), (x + S * .035, y), (x, y + S * .035), (x - S * .035, y)], fill=(230, 195, 110, 255))
    d.rectangle([S * .06, S * .82, S * .94, S * .9], fill=(215, 160, 100, 255), outline=OUT, width=5)  # trim
    d.rounded_rectangle([S * .42, S * .36, S * .58, S * .48], 4, fill=(255, 210, 50, 255), outline=OUT, width=5)  # clasp
    d.line([(S * .16, S * .44), (S * .3, S * .44)], fill=(200, 140, 90, 255), width=5)
    return _shrink(im, size)


def retro_mic(size=64):
    """A 50s-style chrome mic on a stand: the big oval grille with its slots, the stand's base."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.line([(S * .5, S * .5), (S * .5, S * .92)], fill=OUT, width=int(S * .07))                      # stand
    d.line([(S * .5, S * .5), (S * .5, S * .92)], fill=(150, 155, 165, 255), width=int(S * .035))
    d.ellipse([S * .3, S * .86, S * .7, S * .98], fill=(60, 60, 68, 255), outline=OUT, width=6)
    d.rounded_rectangle([S * .32, S * .04, S * .68, S * .54], 28, fill=(205, 210, 222, 255), outline=OUT, width=9)
    for k in range(6):                                                                                 # grille slots
        y = S * (.12 + k * .065)
        d.line([(S * .4, y), (S * .6, y)], fill=(90, 95, 110, 255), width=5)
    d.line([(S * .38, S * .1), (S * .38, S * .46)], fill=(255, 255, 255, 255), width=5)
    d.rectangle([S * .3, S * .27, S * .7, S * .31], fill=(255, 210, 50, 255), outline=OUT, width=3)     # gold band
    return _shrink(im, size)


def zippo(size=64):
    """A chrome zippo held up high, lid flipped open, the flame burning tall."""
    im, d, S = _big(size)
    OUT = (20, 15, 10, 255)
    d.polygon([(S * .5, S * .02), (S * .64, S * .3), (S * .58, S * .44), (S * .42, S * .44), (S * .36, S * .3)], fill=(255, 140, 20, 255))
    d.polygon([(S * .5, S * .14), (S * .58, S * .32), (S * .54, S * .42), (S * .46, S * .42), (S * .42, S * .32)], fill=(255, 240, 120, 255))
    d.rectangle([S * .38, S * .42, S * .62, S * .56], fill=(170, 175, 185, 255), outline=OUT, width=5)  # chimney
    for k in range(3):
        d.ellipse([S * (.42 + k * .06), S * .46, S * (.46 + k * .06), S * .5], fill=OUT)
    d.rectangle([S * .62, S * .3, S * .76, S * .56], fill=(200, 205, 215, 255), outline=OUT, width=6)  # lid open
    d.rounded_rectangle([S * .34, S * .56, S * .7, S * .96], 6, fill=(205, 210, 222, 255), outline=OUT, width=8)  # case
    d.line([(S * .34, S * .62), (S * .7, S * .62)], fill=OUT, width=4)
    d.line([(S * .4, S * .66), (S * .4, S * .9)], fill=(255, 255, 255, 255), width=5)
    return _shrink(im, size)


def sleep_mask(size=64):
    """A pink satin sleep mask with closed eyes stitched on (curved lids, lashes) and its strap."""
    im, d, S = _big(size)
    OUT = (60, 20, 40, 255)
    d.line([(S * .0, S * .46), (S * 1.0, S * .46)], fill=(200, 80, 130, 255), width=int(S * .05))     # strap
    _outline_poly(d, [(S * .08, S * .4), (S * .3, S * .26), (S * .5, S * .34), (S * .7, S * .26), (S * .92, S * .4),
                      (S * .9, S * .62), (S * .68, S * .72), (S * .5, S * .62), (S * .32, S * .72), (S * .1, S * .62)],
                  (255, 150, 195, 255), OUT, 8)
    d.line([(S * .16, S * .38), (S * .4, S * .3)], fill=(255, 220, 235, 255), width=6)                  # satin shine
    for cx in (.3, .7):                                                                                # closed eyes
        d.arc([S * (cx - .12), S * .38, S * (cx + .12), S * .58], 20, 160, fill=OUT, width=6)
        for k in range(3):
            x = S * (cx - .07 + k * .07)
            d.line([(x, S * .57), (x + S * (k - 1) * .02, S * .63)], fill=OUT, width=4)
    return _shrink(im, size)


def double_note(n=16):
    """Two beamed eighth notes (alpha only)."""
    def f(x, y):
        heads = ((x - 4) ** 2 / 2.6 + (y - 12) ** 2 / 1.6 <= 1.6) or ((x - 11) ** 2 / 2.6 + (y - 10.5) ** 2 / 1.6 <= 1.6)
        stems = (5.2 <= x <= 6.4 and 3 <= y <= 12) or (12.2 <= x <= 13.4 and 1.5 <= y <= 10.5)
        beam = 5.2 <= x <= 13.4 and abs(y - (3 - (x - 5.2) * .18)) <= 1.2
        return 1 if heads or stems or beam else 0
    return _alpha(n, n, f)


def snore_z(n=16):
    """A chunky Z (alpha only): somebody sleeping."""
    def f(x, y):
        if 3 <= x <= 12 and (3 <= y <= 4.5 or 11.5 <= y <= 13):
            return 1
        return 1 if 3 <= y <= 13 and abs((x - 3) - (12 - 3) * (13 - y) / 10) < 1.4 else 0
    return _alpha(n, n, f)


def leaf_blower(size=64):
    """A gas leaf blower pointing right: the orange engine housing with a pull cord, the handle, the long black
    blower tube."""
    im, d, S = _big(size)
    OUT = (20, 15, 10, 255)
    _outline_poly(d, [(S * .44, S * .5), (S * .98, S * .62), (S * .98, S * .74), (S * .42, S * .66)], (40, 40, 45, 255), OUT, 7)  # tube
    d.line([(S * .5, S * .56), (S * .94, S * .65)], fill=(110, 110, 120, 255), width=4)
    d.rounded_rectangle([S * .06, S * .36, S * .5, S * .82], 14, fill=(250, 120, 20, 255), outline=OUT, width=9)  # engine
    d.ellipse([S * .14, S * .48, S * .34, S * .68], fill=(60, 60, 66, 255), outline=OUT, width=6)       # air intake
    for k in range(3):
        d.line([(S * .17, S * (.53 + k * .05)), (S * .31, S * (.53 + k * .05))], fill=(120, 120, 130, 255), width=3)
    d.arc([S * .16, S * .12, S * .46, S * .46], 180, 360, fill=OUT, width=int(S * .08))                # handle
    d.arc([S * .16, S * .12, S * .46, S * .46], 180, 360, fill=(60, 60, 66, 255), width=int(S * .04))
    d.line([(S * .1, S * .42), (S * .02, S * .3)], fill=(240, 240, 240, 255), width=4)                  # pull cord
    d.ellipse([S * 0, S * .25, S * .06, S * .31], fill=(220, 30, 30, 255), outline=OUT, width=3)
    d.line([(S * .12, S * .4), (S * .44, S * .4)], fill=(255, 190, 120, 255), width=5)
    return _shrink(im, size)


def plastic_bag(size=32):
    """A white plastic grocery bag tumbling in the wind, a red smiley on it."""
    im, d, S = _big(size)
    OUT = (90, 90, 100, 255)
    _outline_poly(d, [(S * .14, S * .3), (S * .86, S * .26), (S * .92, S * .9), (S * .08, S * .92)], (245, 245, 250, 230), OUT, 6)
    for x in (.18, .66):                                                                               # handles
        d.arc([S * x, S * .04, S * (x + .2), S * .4], 180, 360, fill=OUT, width=6)
    d.ellipse([S * .32, S * .44, S * .68, S * .8], outline=(220, 40, 40, 255), width=5)
    d.ellipse([S * .4, S * .52, S * .45, S * .58], fill=(220, 40, 40, 255))
    d.ellipse([S * .55, S * .52, S * .6, S * .58], fill=(220, 40, 40, 255))
    d.arc([S * .4, S * .54, S * .6, S * .72], 20, 160, fill=(220, 40, 40, 255), width=4)
    return _shrink(im, size)


def crushed_can(size=32):
    """A crushed red soda can, tumbling."""
    im, d, S = _big(size)
    OUT = (40, 10, 10, 255)
    _outline_poly(d, [(S * .2, S * .12), (S * .8, S * .1), (S * .66, S * .5), (S * .82, S * .9), (S * .18, S * .92),
                      (S * .34, S * .5)], (210, 30, 35, 255), OUT, 7)
    d.rectangle([S * .22, S * .1, S * .78, S * .18], fill=(200, 205, 215, 255), outline=OUT, width=5)
    d.rectangle([S * .2, S * .84, S * .8, S * .92], fill=(200, 205, 215, 255), outline=OUT, width=5)
    d.line([(S * .3, S * .3), (S * .7, S * .7)], fill=(255, 255, 255, 255), width=6)
    d.line([(S * .3, S * .2), (S * .4, S * .5)], fill=(255, 140, 140, 255), width=4)
    return _shrink(im, size)


def dust_swirl(w=16, h=32):
    """A lumpy, billowing column of dust (alpha only)."""
    import math

    def f(x, y):
        r = 6.5 - 1.6 * math.sin(y * .7) - abs(y - 16) * .12
        return max(0, min(1, (r - abs(x - 7.5)) / 2)) * min(1, y / 4, (h - 1 - y) / 4)
    return _alpha(w, h, f)


# ---- set 18 --------------------------------------------------------------------------------------------

def turntable(size=64):
    """A DJ turntable seen at an angle: silver deck, the black platter, the tonearm, pitch slider, a red light."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    _outline_poly(d, [(S * .04, S * .42), (S * .96, S * .42), (S * .9, S * .9), (S * .1, S * .9)], (190, 195, 205, 255), OUT, 8)
    d.rectangle([S * .1, S * .9, S * .9, S * .96], fill=(120, 125, 135, 255), outline=OUT, width=6)
    d.ellipse([S * .1, S * .46, S * .66, S * .86], fill=(40, 40, 46, 255), outline=OUT, width=7)       # platter
    d.ellipse([S * .3, S * .58, S * .46, S * .74], fill=(220, 40, 50, 255), outline=OUT, width=5)
    d.line([(S * .84, S * .5), (S * .74, S * .74), (S * .5, S * .68)], fill=OUT, width=int(S * .05), joint="curve")  # arm
    d.line([(S * .84, S * .5), (S * .74, S * .74), (S * .5, S * .68)], fill=(230, 230, 240, 255), width=int(S * .025), joint="curve")
    d.ellipse([S * .8, S * .46, S * .9, S * .56], fill=(150, 150, 160, 255), outline=OUT, width=5)
    d.rectangle([S * .76, S * .76, S * .86, S * .86], fill=(60, 60, 66, 255), outline=OUT, width=4)      # slider
    d.ellipse([S * .1, S * .78, S * .16, S * .84], fill=(255, 40, 40, 255))
    return _shrink(im, size)


def vinyl(size=64):
    """A vinyl record face on: black grooves, a red label with a white stripe, the spindle hole (spins)."""
    im, d, S = _big(size)
    OUT = (5, 5, 8, 255)
    d.ellipse([S * .04, S * .04, S * .96, S * .96], fill=(25, 25, 30, 255), outline=OUT, width=6)
    for r in (.4, .34, .28):
        d.ellipse([S * (.5 - r), S * (.5 - r), S * (.5 + r), S * (.5 + r)], outline=(60, 60, 70, 255), width=3)
    d.arc([S * .12, S * .12, S * .88, S * .88], 200, 250, fill=(160, 160, 175, 255), width=7)        # shine
    d.ellipse([S * .34, S * .34, S * .66, S * .66], fill=(220, 40, 50, 255), outline=OUT, width=5)
    d.rectangle([S * .38, S * .46, S * .62, S * .5], fill=(255, 255, 255, 255))
    d.ellipse([S * .47, S * .47, S * .53, S * .53], fill=OUT)
    return _shrink(im, size)


def rewind_arrows(n=16):
    """Two left-pointing triangles, the rewind symbol (alpha only)."""
    def f(x, y):
        for x0 in (1, 8):
            if x0 <= x <= x0 + 7 and abs(y - 7.5) <= (x - x0) * .8:
                return 1
        return 0
    return _alpha(n, n, f)


def cash_duffel(size=64):
    """A black duffel bag stuffed with cash: stacks of green bills poking out the open zipper, the strap."""
    im, d, S = _big(size)
    OUT = (8, 8, 10, 255)
    d.arc([S * .2, S * .06, S * .8, S * .6], 190, 350, fill=OUT, width=int(S * .07))                  # strap
    d.arc([S * .2, S * .06, S * .8, S * .6], 190, 350, fill=(70, 70, 78, 255), width=int(S * .035))
    for k in range(5):                                                                                 # cash
        x = S * (.22 + k * .12)
        _outline_poly(d, [(x, S * .4), (x + S * .14, S * .34 + k % 2 * S * .04), (x + S * .16, S * .46), (x + S * .02, S * .5)],
                      (110, 190, 100, 255), OUT, 5)
        d.ellipse([x + S * .05, S * .4, x + S * .1, S * .45], fill=(70, 140, 70, 255))
    d.rounded_rectangle([S * .06, S * .42, S * .94, S * .9], 22, fill=(35, 35, 40, 255), outline=OUT, width=9)
    d.line([(S * .16, S * .46), (S * .84, S * .46)], fill=(200, 200, 210, 255), width=5)               # zipper
    d.line([(S * .14, S * .56), (S * .86, S * .56)], fill=(70, 70, 80, 255), width=6)
    d.rectangle([S * .44, S * .62, S * .56, S * .72], fill=(200, 160, 40, 255), outline=OUT, width=4)  # logo tag
    for x in (.1, .9):
        d.ellipse([S * (x - .06), S * .58, S * (x + .06), S * .78], fill=(25, 25, 30, 255), outline=OUT, width=6)
    return _shrink(im, size)


def dash_lines(n=16):
    """Three horizontal motion lines (alpha only)."""
    def f(x, y):
        for cy, x0 in ((3, 0), (8, 3), (13, 1)):
            if abs(y - cy) < 1.1 and x >= x0:
                return min(1, (x - x0) / 6 + .2)
        return 0
    return _alpha(n, n, f)


def brass_knuckles(size=64):
    """Gold brass knuckles: four finger rings across the top, the grip bar below, a hard shine (pointing right)."""
    im, d, S = _big(size)
    OUT = (60, 35, 0, 255)
    G, GL, GD = (240, 190, 40, 255), (255, 245, 170, 255), (190, 130, 10, 255)
    _outline_poly(d, [(S * .12, S * .5), (S * .88, S * .5), (S * .8, S * .82), (S * .2, S * .82)], G, OUT, 9)
    for k in range(4):
        cx = S * (.2 + k * .2)
        d.ellipse([cx - S * .11, S * .14, cx + S * .11, S * .52], fill=G, outline=OUT, width=9)
        d.ellipse([cx - S * .06, S * .22, cx + S * .06, S * .44], fill=(0, 0, 0, 0), outline=OUT, width=6)
        d.arc([cx - S * .1, S * .15, cx + S * .1, S * .5], 200, 260, fill=GL, width=6)
    d.line([(S * .22, S * .6), (S * .78, S * .6)], fill=GL, width=6)
    d.line([(S * .24, S * .74), (S * .76, S * .74)], fill=GD, width=6)
    return _shrink(im, size)


def pow_burst(size=64):
    """A jagged comic impact starburst: yellow with an orange core and a white flash (no text)."""
    import math
    im, d, S = _big(size)
    OUT = (70, 20, 0, 255)
    pts = []
    for k in range(24):
        r = .48 if k % 2 == 0 else .3
        a = k * math.tau / 24
        pts.append((S * (.5 + r * math.cos(a)), S * (.5 + r * math.sin(a))))
    _outline_poly(d, pts, (255, 220, 40, 255), OUT, 8)
    inner = [((x - S * .5) * .55 + S * .5, (y - S * .5) * .55 + S * .5) for x, y in pts]
    d.polygon(inner, fill=(255, 130, 30, 255))
    d.ellipse([S * .4, S * .4, S * .6, S * .6], fill=(255, 255, 230, 255))
    return _shrink(im, size)


def muscle_car(size=64):
    """A side-on red muscle car facing right: white racing stripes, fat back tires, chrome bumpers, a hood scoop."""
    im, d, S = _big(size)
    OUT = (15, 10, 10, 255)
    RED, RED_D, RED_L = (210, 30, 35, 255), (150, 15, 20, 255), (255, 120, 110, 255)
    body = [(S * .02, S * .6), (S * .06, S * .46), (S * .3, S * .42), (S * .4, S * .3), (S * .64, S * .3), (S * .74, S * .42),
            (S * .96, S * .48), (S * .98, S * .64), (S * .02, S * .66)]
    _outline_poly(d, body, RED, OUT, 9)
    _outline_poly(d, [(S * .43, S * .34), (S * .62, S * .34), (S * .7, S * .43), (S * .36, S * .43)], (140, 190, 230, 255), OUT, 6)
    d.line([(S * .53, S * .34), (S * .53, S * .43)], fill=OUT, width=5)
    d.line([(S * .04, S * .52), (S * .96, S * .54)], fill=(250, 250, 250, 255), width=7)               # stripes
    d.line([(S * .04, S * .57), (S * .96, S * .59)], fill=(250, 250, 250, 255), width=4)
    d.rectangle([S * .78, S * .4, S * .88, S * .45], fill=RED_D, outline=OUT, width=4)                 # scoop
    d.line([(S * .1, S * .48), (S * .3, S * .46)], fill=RED_L, width=5)
    for x, r in ((.22, .14), (.8, .12)):                                                               # tires
        d.ellipse([S * (x - r), S * (.64 - r), S * (x + r), S * (.64 + r)], fill=(25, 25, 28, 255), outline=OUT, width=7)
        d.ellipse([S * (x - r * .5), S * (.64 - r * .5), S * (x + r * .5), S * (.64 + r * .5)], fill=(210, 215, 225, 255), outline=OUT, width=4)
    d.rectangle([S * .94, S * .58, S * 1.0, S * .64], fill=(220, 225, 235, 255), outline=OUT, width=4)
    return _shrink(im, size)


def diss_cd(size=64):
    """A CD jewel case: the cover art is a cartoon crying face crossed out in red, DISS TRACK across the top and
    an EXPLICIT label in the corner (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rectangle([S * .06, S * .06, S * .94, S * .94], fill=(200, 215, 235, 255), outline=OUT, width=8)
    d.rectangle([S * .12, S * .1, S * .9, S * .9], fill=(30, 25, 45, 255), outline=OUT, width=5)
    d.ellipse([S * .3, S * .32, S * .7, S * .72], fill=(240, 200, 120, 255), outline=OUT, width=6)     # sad face
    for x in (.42, .58):
        d.line([(S * (x - .03), S * .46), (S * (x + .03), S * .46)], fill=OUT, width=5)
        d.line([(S * x, S * .5), (S * x, S * .58)], fill=(90, 170, 255, 255), width=5)
    d.arc([S * .4, S * .58, S * .6, S * .7], 200, 340, fill=OUT, width=5)
    d.line([(S * .26, S * .3), (S * .74, S * .74)], fill=(230, 30, 30, 255), width=9)
    d.line([(S * .74, S * .3), (S * .26, S * .74)], fill=(230, 30, 30, 255), width=9)
    d.rectangle([S * .58, S * .76, S * .88, S * .88], fill=(250, 250, 250, 255), outline=OUT, width=4)  # explicit label
    d.rectangle([S * .58, S * .76, S * .88, S * .8], fill=OUT)
    im = _shrink(im, size)
    _texted(im, [("DISS", (32, 9)), ("TRACK", (32, 16))], (255, 220, 40, 255))
    return im


def angry_note(n=16):
    """A single fat eighth note (alpha only)."""
    def f(x, y):
        head = (x - 5) ** 2 / 3.5 + (y - 12) ** 2 / 2.2 <= 2.2
        stem = 7 <= x <= 8.5 and 2 <= y <= 12
        flag = 8 <= x <= 13 and 2 <= y <= 5 + (x - 8) * .4 and y >= 2 + (x - 8) * .6
        return 1 if head or stem or flag else 0
    return _alpha(n, n, f)


def trench_coat(size=64, open_=True):
    """A tan trench coat hanging off a hanger - flung open, the lining covered in knockoff gold watches with a
    ROLEKS tag; or shut, collar up, real shady (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 25, 10, 255)
    TAN, TAN_D = (200, 160, 100, 255), (150, 115, 65, 255)
    d.line([(S * .5, S * .0), (S * .5, S * .08)], fill=(150, 150, 160, 255), width=6)                  # hanger hook
    d.line([(S * .2, S * .16), (S * .5, S * .06), (S * .8, S * .16)], fill=(150, 150, 160, 255), width=6)
    if open_:
        _outline_poly(d, [(S * .02, S * .18), (S * .3, S * .14), (S * .3, S * .96), (S * .0, S * .9)], TAN, OUT, 8)
        _outline_poly(d, [(S * .98, S * .18), (S * .7, S * .14), (S * .7, S * .96), (S * 1.0, S * .9)], TAN, OUT, 8)
        d.rectangle([S * .28, S * .16, S * .72, S * .96], fill=(120, 30, 40, 255), outline=OUT, width=7)  # lining
        for r in range(3):
            for c in range(2):
                cx, cy = S * (.39 + c * .22), S * (.3 + r * .22)
                d.line([(cx, cy - S * .08), (cx, cy + S * .08)], fill=(220, 170, 30, 255), width=7)  # band
                d.ellipse([cx - S * .06, cy - S * .06, cx + S * .06, cy + S * .06], fill=(255, 215, 60, 255), outline=OUT, width=4)
                d.ellipse([cx - S * .035, cy - S * .035, cx + S * .035, cy + S * .035], fill=(250, 250, 240, 255))
    else:
        _outline_poly(d, [(S * .16, S * .16), (S * .84, S * .16), (S * .9, S * .96), (S * .1, S * .96)], TAN, OUT, 8)
        d.line([(S * .5, S * .2), (S * .5, S * .96)], fill=TAN_D, width=6)
        d.polygon([(S * .2, S * .16), (S * .5, S * .2), (S * .36, S * .4)], fill=TAN_D, outline=OUT)   # collar up
        d.polygon([(S * .8, S * .16), (S * .5, S * .2), (S * .64, S * .4)], fill=TAN_D, outline=OUT)
        d.rectangle([S * .14, S * .54, S * .86, S * .6], fill=TAN_D, outline=OUT, width=4)              # belt
        for y in (.36, .46, .7):
            d.ellipse([S * .43, S * y, S * .48, S * (y + .04)], fill=OUT)
    im = _shrink(im, size)
    if open_:
        _texted(im, [("ROLEKS", (32, 56))], (255, 230, 80, 255))
    return im


def gear_bit(n=16):
    """A little cog wheel (alpha only): a busted watch's guts."""
    import math

    def f(x, y):
        dx, dy = x - 7.5, y - 7.5
        r = (dx * dx + dy * dy) ** .5
        a = math.atan2(dy, dx)
        rim = 5 + (1.5 if math.cos(a * 8) > .3 else 0)
        return 1 if r <= rim and r > 1.8 else 0
    return _alpha(n, n, f)


def grandma_broom(size=64):
    """A straw broom swung down-right: wooden handle, the tied red band, a fan of straw bristles."""
    im, d, S = _big(size)
    OUT = (40, 25, 10, 255)
    d.line([(S * .12, S * .08), (S * .58, S * .54)], fill=OUT, width=int(S * .08))
    d.line([(S * .12, S * .08), (S * .58, S * .54)], fill=(170, 110, 60, 255), width=int(S * .045))
    bristle = [(S * .52, S * .5), (S * .64, S * .44), (S * .98, S * .8), (S * .8, S * .98)]
    _outline_poly(d, bristle, (230, 195, 90, 255), OUT, 8)
    for k in range(6):
        t = k / 5
        d.line([(S * (.58 + t * .02), S * (.5 - t * .02)), (S * (.82 + t * .14), S * (.96 - t * .14))], fill=(190, 150, 60, 255), width=4)
    d.line([(S * .52, S * .5), (S * .64, S * .44)], fill=(210, 40, 40, 255), width=10)                 # the band
    return _shrink(im, size)


def wrestling_ring(size=64):
    """A wrestling ring seen from the front: blue apron, three ropes (red, white, blue) between padded corner
    turnbuckles, the canvas."""
    im, d, S = _big(size)
    OUT = (15, 15, 25, 255)
    _outline_poly(d, [(S * .08, S * .62), (S * .92, S * .62), (S * .98, S * .74), (S * .02, S * .74)], (235, 235, 240, 255), OUT, 7)
    d.rectangle([S * .02, S * .74, S * .98, S * .98], fill=(40, 70, 190, 255), outline=OUT, width=8)   # apron
    d.line([(S * .1, S * .86), (S * .9, S * .86)], fill=(255, 210, 40, 255), width=6)
    for x in (.06, .94):                                                                               # posts
        d.rectangle([S * (x - .03), S * .12, S * (x + .03), S * .74], fill=(200, 200, 210, 255), outline=OUT, width=6)
        for k, col in enumerate(((220, 40, 40, 255), (250, 250, 250, 255), (50, 90, 220, 255))):
            d.rectangle([S * (x - .05), S * (.18 + k * .14), S * (x + .05), S * (.26 + k * .14)], fill=col, outline=OUT, width=4)
    for k, col in enumerate(((220, 40, 40, 255), (250, 250, 250, 255), (50, 90, 220, 255))):
        y = S * (.22 + k * .14)
        d.line([(S * .1, y), (S * .9, y + S * .02)], fill=OUT, width=8)
        d.line([(S * .1, y), (S * .9, y + S * .02)], fill=col, width=4)
    return _shrink(im, size)


def champ_belt(size=64):
    """A championship belt: black leather strap, a giant gold center plate with a jewel, side plates."""
    im, d, S = _big(size)
    OUT = (40, 25, 0, 255)
    d.rounded_rectangle([S * .0, S * .4, S * 1.0, S * .62], 10, fill=(30, 25, 25, 255), outline=OUT, width=7)
    for x in (.14, .86):
        d.rounded_rectangle([S * (x - .1), S * .36, S * (x + .1), S * .66], 8, fill=(240, 195, 50, 255), outline=OUT, width=6)
    d.ellipse([S * .26, S * .18, S * .74, S * .84], fill=(250, 205, 50, 255), outline=OUT, width=9)
    d.ellipse([S * .34, S * .28, S * .66, S * .74], fill=(220, 160, 20, 255), outline=OUT, width=5)
    d.polygon([(S * .5, S * .34), (S * .6, S * .5), (S * .5, S * .66), (S * .4, S * .5)], fill=(220, 30, 60, 255), outline=OUT)
    d.arc([S * .3, S * .22, S * .7, S * .8], 200, 250, fill=(255, 250, 200, 255), width=7)
    return _shrink(im, size)


def wet_floor_aframe(size=64):
    """A yellow A-frame WET FLOOR sign with the little slipping-guy icon (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (30, 25, 0, 255)
    _outline_poly(d, [(S * .5, S * .02), (S * .86, S * .96), (S * .14, S * .96)], (255, 210, 20, 255), OUT, 9)
    d.ellipse([S * .44, S * .02, S * .56, S * .1], fill=(40, 40, 40, 255))
    # the slipping guy: head, body falling back, legs up
    d.ellipse([S * .53, S * .64, S * .61, S * .72], fill=OUT)
    d.line([(S * .56, S * .72), (S * .45, S * .82)], fill=OUT, width=7)
    d.line([(S * .45, S * .82), (S * .39, S * .72)], fill=OUT, width=6)
    d.line([(S * .45, S * .82), (S * .33, S * .86)], fill=OUT, width=6)
    d.line([(S * .51, S * .75), (S * .63, S * .79)], fill=OUT, width=5)
    d.line([(S * .26, S * .91), (S * .74, S * .91)], fill=OUT, width=5)                                 # the floor
    im = _shrink(im, size)
    return _texted(im, [("WET", (32, 25)), ("FLOOR", (32, 32))], (30, 25, 0, 255), (255, 230, 120, 255))


def water_puddle(size=64):
    """A shiny clear-blue puddle flat on the floor."""
    im, d, S = _big(size)
    OUT = (30, 70, 140, 255)
    d.ellipse([S * .02, S * .52, S * .66, S * .86], fill=(120, 190, 255, 220), outline=OUT, width=6)
    d.ellipse([S * .4, S * .5, S * .98, S * .8], fill=(120, 190, 255, 220), outline=OUT, width=6)
    d.ellipse([S * .06, S * .55, S * .62, S * .83], fill=(120, 190, 255, 220))
    d.arc([S * .2, S * .58, S * .5, S * .7], 200, 330, fill=(255, 255, 255, 255), width=6)
    d.line([(S * .66, S * .58), (S * .82, S * .58)], fill=(255, 255, 255, 255), width=5)
    return _shrink(im, size)


def fortune_cookie(size=64, cracked=False):
    """A big golden fortune cookie - whole, or cracked in two with the paper slip poking out."""
    im, d, S = _big(size)
    OUT = (90, 50, 10, 255)
    G, G_D, G_L = (235, 185, 90, 255), (190, 130, 50, 255), (255, 225, 160, 255)
    if not cracked:
        d.chord([S * .04, S * .2, S * .96, S * .96], 180, 360, fill=G, outline=OUT, width=9)            # the fold
        d.pieslice([S * .3, S * .44, S * .7, S * .84], 180, 360, fill=G_D, outline=OUT, width=6)        # the pinch
        d.line([(S * .5, S * .44), (S * .5, S * .58)], fill=OUT, width=6)
        d.arc([S * .1, S * .26, S * .6, S * .9], 200, 250, fill=G_L, width=8)
    else:
        _outline_poly(d, [(S * .0, S * .62), (S * .2, S * .34), (S * .36, S * .46), (S * .3, S * .66), (S * .18, S * .8)], G, OUT, 8)
        _outline_poly(d, [(S * 1.0, S * .62), (S * .8, S * .34), (S * .64, S * .46), (S * .7, S * .66), (S * .82, S * .8)], G, OUT, 8)
        d.rectangle([S * .3, S * .44, S * .7, S * .6], fill=(252, 252, 248, 255), outline=(150, 150, 150, 255), width=4)
        for x in (.38, .46, .54, .62):
            d.line([(S * x, S * .5), (S * (x + .04), S * .5)], fill=(200, 40, 40, 255), width=4)
    return _shrink(im, size)


def fortune_slip(size=64):
    """The fortune, unrolled: a white paper strip, UR TAKIN AN L in red with the lucky numbers (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([1, 18, 62, 44], fill=(252, 252, 246, 255), outline=(120, 110, 100, 255))
    d.line([(4, 41), (59, 41)], fill=(220, 210, 190, 255))
    _texted(im, [("UR TAKIN", (32, 21)), ("AN L", (32, 29))], (210, 30, 30, 255), (252, 252, 246, 255))
    m = _text_mask("4 8 0 0")
    im.paste((120, 120, 120, 255), (32 - m.width // 2, 37), m)
    return im


def basketball(size=32):
    """An orange basketball with its black seams (spins)."""
    im, d, S = _big(size)
    OUT = (40, 15, 0, 255)
    d.ellipse([S * .04, S * .04, S * .96, S * .96], fill=(240, 120, 30, 255), outline=OUT, width=7)
    d.line([(S * .5, S * .04), (S * .5, S * .96)], fill=OUT, width=5)
    d.line([(S * .04, S * .5), (S * .96, S * .5)], fill=OUT, width=5)
    d.arc([S * -.3, S * .1, S * .4, S * .9], 300, 60, fill=OUT, width=5)
    d.arc([S * .6, S * .1, S * 1.3, S * .9], 120, 240, fill=OUT, width=5)
    d.arc([S * .14, S * .14, S * .6, S * .6], 200, 260, fill=(255, 200, 140, 255), width=6)
    return _shrink(im, size)


def conspiracy_board(size=64):
    """A conspiracy corkboard: polaroids of a Pokémon Center, a Ball, a question mark note - all linked with red
    string and push pins."""
    im, d, S = _big(size)
    OUT = (40, 25, 10, 255)
    d.rectangle([S * .02, S * .08, S * .98, S * .92], fill=(190, 140, 80, 255), outline=OUT, width=9)   # frame
    d.rectangle([S * .07, S * .13, S * .93, S * .87], fill=(205, 160, 100, 255))
    for x, y in ((.08, .2), (.5, .5), (.2, .7), (.82, .25), (.7, .78), (.45, .18)):                     # cork specks
        d.ellipse([S * x, S * y, S * (x + .02), S * (y + .02)], fill=(160, 115, 60, 255))
    pins = [(.22, .26), (.7, .22), (.5, .52), (.26, .74), (.76, .7)]
    d.line([(S * x, S * y) for x, y in pins] + [(S * .22, S * .26), (S * .5, S * .52), (S * .76, S * .7)],
           fill=(220, 20, 30, 255), width=4)
    polar = [((.12, .18), (90, 200, 120, 255)), ((.6, .14), (220, 60, 60, 255)), ((.16, .64), (90, 140, 230, 255))]
    for (x, y), col in polar:
        d.rectangle([S * x, S * y, S * (x + .2), S * (y + .22)], fill=(250, 250, 245, 255), outline=OUT, width=4)
        d.rectangle([S * (x + .02), S * (y + .02), S * (x + .18), S * (y + .16)], fill=col)
    d.rectangle([S * .4, S * .42, S * .6, S * .62], fill=(255, 240, 120, 255), outline=OUT, width=4)   # sticky
    d.arc([S * .44, S * .44, S * .56, S * .54], 180, 360, fill=OUT, width=4)
    d.line([(S * .56, S * .49), (S * .5, S * .55)], fill=OUT, width=4)
    d.ellipse([S * .49, S * .57, S * .51, S * .59], fill=OUT)
    d.rectangle([S * .66, S * .62, S * .88, S * .8], fill=(250, 250, 245, 255), outline=OUT, width=4)
    d.ellipse([S * .7, S * .64, S * .84, S * .76], fill=(220, 40, 40, 255), outline=OUT, width=3)    # a Ball
    d.line([(S * .7, S * .7), (S * .84, S * .7)], fill=OUT, width=3)
    for x, y in pins:
        d.ellipse([S * (x - .025), S * (y - .025), S * (x + .025), S * (y + .025)], fill=(240, 40, 40, 255), outline=OUT, width=3)
    return _shrink(im, size)


def pot_helmet(size=64):
    """A dented cooking pot worn as a helmet: steel, a long handle sticking out, a lid knob on top."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.line([(S * .66, S * .5), (S * .98, S * .4)], fill=OUT, width=int(S * .1))                       # handle
    d.line([(S * .66, S * .5), (S * .98, S * .4)], fill=(40, 40, 46, 255), width=int(S * .06))
    d.chord([S * .06, S * .2, S * .74, S * .96], 180, 360, fill=(190, 195, 205, 255), outline=OUT, width=9)
    d.rectangle([S * .04, S * .56, S * .76, S * .66], fill=(160, 165, 175, 255), outline=OUT, width=7)  # rim
    d.line([(S * .16, S * .42), (S * .28, S * .3)], fill=(250, 250, 255, 255), width=7)
    d.arc([S * .44, S * .34, S * .56, S * .46], 20, 160, fill=OUT, width=5)                           # dent
    return _shrink(im, size)


def baking_sheet(size=64):
    """A baking sheet held up as a shield: silver tray, rolled rim, a few burnt cookie stains."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.rounded_rectangle([S * .12, S * .04, S * .88, S * .96], 6, fill=(170, 175, 185, 255), outline=OUT, width=9)
    d.rounded_rectangle([S * .2, S * .12, S * .8, S * .88], 4, fill=(200, 205, 215, 255), outline=(130, 135, 145, 255), width=5)
    for x, y in ((.36, .3), (.6, .5), (.4, .7)):
        d.ellipse([S * (x - .07), S * (y - .05), S * (x + .07), S * (y + .05)], fill=(140, 110, 70, 255))
    d.line([(S * .26, S * .2), (S * .26, S * .8)], fill=(255, 255, 255, 255), width=6)
    return _shrink(im, size)


def disco_ball(size=64):
    """A mirrored disco ball on its chain: grey tiles, a few blazing white ones (spins)."""
    im, d, S = _big(size)
    OUT = (15, 15, 25, 255)
    d.line([(S * .5, S * .0), (S * .5, S * .16)], fill=(150, 150, 160, 255), width=6)
    d.ellipse([S * .14, S * .14, S * .86, S * .86], fill=(150, 160, 180, 255), outline=OUT, width=7)
    for r in range(7):
        for c in range(7):
            x, y = S * (.2 + c * .09), S * (.2 + r * .09)
            if ((x - S * .5) ** 2 + (y - S * .5) ** 2) ** .5 < S * .32:
                col = (255, 255, 255, 255) if (r * 3 + c) % 7 == 0 else ((200, 210, 230, 255) if (r + c) % 2 else (120, 130, 155, 255))
                d.rectangle([x, y, x + S * .07, y + S * .07], fill=col)
    d.ellipse([S * .14, S * .14, S * .86, S * .86], outline=OUT, width=7)
    return _shrink(im, size)


def noise_complaint(size=64):
    """A taped-up NOISE COMPLAINT notice from the neighbors: angry scribbles, underlined twice (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 40, 45, 255)
    d.polygon([(S * .14, S * .06), (S * .88, S * .1), (S * .86, S * .94), (S * .12, S * .9)], fill=(252, 252, 245, 255), outline=OUT)
    d.line([(S * .14, S * .06), (S * .88, S * .1), (S * .86, S * .94), (S * .12, S * .9), (S * .14, S * .06)], fill=OUT, width=6)
    for x, y in ((.1, .04), (.8, .06)):
        d.rectangle([S * x, S * y, S * (x + .12), S * (y + .06)], fill=(230, 220, 160, 220))           # tape
    for k in range(4):
        d.line([(S * .22, S * (.58 + k * .08)), (S * (.78 - k * .05), S * (.58 + k * .08))], fill=(60, 60, 200, 255), width=4)
    d.line([(S * .2, S * .46), (S * .8, S * .46)], fill=(220, 30, 30, 255), width=5)
    im = _shrink(im, size)
    return _texted(im, [("NOISE", (32, 12)), ("COMPLAINT", (32, 20))], (220, 30, 30, 255), (252, 252, 245, 255))


def bandaid(size=32):
    """A tan band-aid, the pad in the middle, little breathing holes."""
    im, d, S = _big(size)
    OUT = (90, 50, 30, 255)
    d.rounded_rectangle([S * .04, S * .32, S * .96, S * .68], 30, fill=(240, 190, 140, 255), outline=OUT, width=6)
    d.rectangle([S * .36, S * .36, S * .64, S * .64], fill=(250, 235, 215, 255), outline=OUT, width=4)
    for x in (.14, .22, .78, .86):
        for y in (.44, .56):
            d.ellipse([S * x, S * y, S * (x + .03), S * (y + .03)], fill=OUT)
    return _shrink(im, size)


def ice_pack(size=64):
    """A blue gel ice pack slapped on top of someone's head, frost sparkles, the cap."""
    im, d, S = _big(size)
    OUT = (10, 30, 70, 255)
    d.rounded_rectangle([S * .08, S * .3, S * .92, S * .74], 18, fill=(90, 170, 255, 255), outline=OUT, width=8)
    d.rounded_rectangle([S * .16, S * .38, S * .84, S * .66], 12, fill=(150, 210, 255, 255))
    d.rectangle([S * .82, S * .4, S * .96, S * .56], fill=(240, 240, 250, 255), outline=OUT, width=5)
    d.line([(S * .22, S * .44), (S * .5, S * .44)], fill=(255, 255, 255, 255), width=6)
    for x, y in ((.3, .2), (.6, .16), (.8, .24)):
        d.polygon([(S * x, S * (y - .05)), (S * (x + .02), S * y), (S * x, S * (y + .05)), (S * (x - .02), S * y)], fill=(255, 255, 255, 255), outline=OUT)
    return _shrink(im, size)


def kitchen_sink(size=64):
    """A whole stainless kitchen sink, ripped out: double basin, the faucet arching over, pipes dangling."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    ST, ST_L, ST_D = (195, 200, 212, 255), (245, 248, 255, 255), (120, 125, 138, 255)
    d.line([(S * .5, S * .2), (S * .5, S * .06), (S * .7, S * .06), (S * .7, S * .16)], fill=OUT, width=int(S * .08))  # faucet
    d.line([(S * .5, S * .2), (S * .5, S * .06), (S * .7, S * .06), (S * .7, S * .16)], fill=ST, width=int(S * .045))
    d.ellipse([S * .38, S * .16, S * .46, S * .24], fill=(220, 40, 40, 255), outline=OUT, width=3)
    d.ellipse([S * .54, S * .16, S * .62, S * .24], fill=(40, 80, 220, 255), outline=OUT, width=3)
    _outline_poly(d, [(S * .04, S * .26), (S * .96, S * .26), (S * .88, S * .7), (S * .12, S * .7)], ST, OUT, 9)
    for x0, x1 in ((.12, .48), (.52, .88)):                                                            # basins
        d.rounded_rectangle([S * x0, S * .32, S * x1, S * .62], 8, fill=ST_D, outline=OUT, width=5)
        d.ellipse([S * ((x0 + x1) / 2 - .03), S * .52, S * ((x0 + x1) / 2 + .03), S * .58], fill=OUT)
    d.line([(S * .1, S * .3), (S * .9, S * .3)], fill=ST_L, width=5)
    for x in (.3, .7):                                                                                  # pipes
        d.line([(S * x, S * .7), (S * x, S * .86), (S * (x + .1), S * .94)], fill=OUT, width=int(S * .07), joint="curve")
        d.line([(S * x, S * .7), (S * x, S * .86), (S * (x + .1), S * .94)], fill=(170, 175, 185, 255), width=int(S * .035), joint="curve")
    return _shrink(im, size)


def fight_cloud(size=64):
    """The cartoon brawl cloud: a big round dust cloud with lumps, motion ticks, stars inside."""
    import math
    im, d, S = _big(size)
    OUT = (60, 50, 40, 255)
    for k in range(10):
        a = k * math.tau / 10
        cx, cy = S * (.5 + .3 * math.cos(a)), S * (.52 + .26 * math.sin(a))
        d.ellipse([cx - S * .18, cy - S * .16, cx + S * .18, cy + S * .16], fill=(225, 215, 195, 255), outline=OUT, width=6)
    d.ellipse([S * .2, S * .24, S * .8, S * .8], fill=(225, 215, 195, 255))
    for x, y in ((.36, .4), (.62, .6), (.5, .34)):
        d.polygon([(S * x, S * (y - .06)), (S * (x + .02), S * (y - .01)), (S * (x + .06), S * y), (S * (x + .02), S * (y + .01)),
                   (S * x, S * (y + .06)), (S * (x - .02), S * (y + .01)), (S * (x - .06), S * y), (S * (x - .02), S * (y - .01))],
                  fill=(255, 220, 40, 255), outline=OUT)
    for k in range(5):
        a = k * 1.3
        d.line([(S * (.5 + .2 * math.cos(a)), S * (.55 + .2 * math.sin(a))), (S * (.5 + .3 * math.cos(a)), S * (.55 + .28 * math.sin(a)))],
               fill=OUT, width=4)
    return _shrink(im, size)


def flying_tooth(size=32):
    """A knocked-out tooth, white with roots."""
    im, d, S = _big(size)
    OUT = (60, 50, 50, 255)
    _outline_poly(d, [(S * .2, S * .14), (S * .8, S * .14), (S * .84, S * .5), (S * .7, S * .9), (S * .56, S * .6),
                      (S * .44, S * .6), (S * .3, S * .9), (S * .16, S * .5)], (252, 252, 245, 255), OUT, 7)
    d.line([(S * .3, S * .24), (S * .3, S * .44)], fill=(255, 255, 255, 255), width=6)
    return _shrink(im, size)


def flying_shoe(size=32):
    """A beat-up sneaker flying out of the fight: red with a white sole, laces undone."""
    im, d, S = _big(size)
    OUT = (30, 10, 10, 255)
    _outline_poly(d, [(S * .06, S * .6), (S * .3, S * .24), (S * .56, S * .24), (S * .62, S * .44), (S * .94, S * .56),
                      (S * .94, S * .72), (S * .06, S * .72)], (210, 40, 40, 255), OUT, 7)
    d.rectangle([S * .04, S * .72, S * .96, S * .84], fill=(250, 250, 250, 255), outline=OUT, width=6)
    d.line([(S * .38, S * .3), (S * .2, S * .1)], fill=(250, 250, 250, 255), width=4)
    d.line([(S * .46, S * .3), (S * .56, S * .08)], fill=(250, 250, 250, 255), width=4)
    return _shrink(im, size)


def cucumber_slice(size=32):
    """A cucumber slice: dark green rind, pale flesh, the seed ring."""
    import math
    im, d, S = _big(size)
    OUT = (20, 60, 20, 255)
    d.ellipse([S * .06, S * .06, S * .94, S * .94], fill=(40, 120, 40, 255), outline=OUT, width=6)
    d.ellipse([S * .14, S * .14, S * .86, S * .86], fill=(200, 235, 160, 255))
    for k in range(8):
        a = k * math.tau / 8
        x, y = S * (.5 + .2 * math.cos(a)), S * (.5 + .2 * math.sin(a))
        d.ellipse([x - S * .04, y - S * .06, x + S * .04, y + S * .06], fill=(240, 250, 210, 255), outline=(150, 190, 110, 255), width=2)
    return _shrink(im, size)


def tea_cup(size=64):
    """A teacup on a saucer, steaming herbal tea, the tag hanging off the side."""
    im, d, S = _big(size)
    OUT = (40, 30, 30, 255)
    d.ellipse([S * .08, S * .74, S * .92, S * .94], fill=(250, 250, 250, 255), outline=OUT, width=6)    # saucer
    d.chord([S * .18, S * .26, S * .82, S * .9], 0, 180, fill=(250, 250, 250, 255), outline=OUT, width=8)
    d.ellipse([S * .18, S * .48, S * .82, S * .64], fill=(170, 210, 120, 255), outline=OUT, width=6)    # the tea
    d.arc([S * .74, S * .54, S * .96, S * .76], 270, 90, fill=OUT, width=8)                            # handle
    d.line([(S * .3, S * .56), (S * .2, S * .8)], fill=(200, 200, 200, 255), width=3)                  # tag
    d.rectangle([S * .14, S * .78, S * .26, S * .88], fill=(240, 160, 60, 255), outline=OUT, width=3)
    d.line([(S * .3, S * .34), (S * .34, S * .3)], fill=(250, 250, 250, 255), width=5)
    return _shrink(im, size)


def scented_candle(size=64):
    """A fancy scented candle in a jar: lavender wax, a little flame, a label with a flower."""
    im, d, S = _big(size)
    OUT = (40, 30, 50, 255)
    d.polygon([(S * .5, S * .02), (S * .58, S * .2), (S * .5, S * .28), (S * .42, S * .2)], fill=(255, 190, 60, 255))
    d.polygon([(S * .5, S * .1), (S * .54, S * .2), (S * .5, S * .25), (S * .46, S * .2)], fill=(255, 250, 200, 255))
    d.line([(S * .5, S * .28), (S * .5, S * .36)], fill=OUT, width=4)
    d.rounded_rectangle([S * .24, S * .34, S * .76, S * .96], 10, fill=(200, 220, 240, 180), outline=OUT, width=7)
    d.rectangle([S * .28, S * .4, S * .72, S * .92], fill=(190, 150, 230, 255))
    d.rectangle([S * .32, S * .56, S * .68, S * .8], fill=(250, 245, 235, 255), outline=OUT, width=4)
    for k in range(5):
        import math
        a = k * math.tau / 5
        d.ellipse([S * (.5 + .05 * math.cos(a)) - S * .03, S * (.68 + .05 * math.sin(a)) - S * .03,
                   S * (.5 + .05 * math.cos(a)) + S * .03, S * (.68 + .05 * math.sin(a)) + S * .03], fill=(160, 100, 220, 255))
    return _shrink(im, size)


def snow_cone(size=64):
    """A snow cone: a paper cone with a heaping dome of shaved ice soaked in rainbow syrup (cherry, blue
    raspberry, lemon)."""
    im, d, S = _big(size)
    OUT = (30, 20, 40, 255)
    _outline_poly(d, [(S * .2, S * .46), (S * .8, S * .46), (S * .5, S * .98)], (250, 250, 245, 255), OUT, 8)
    for k in range(3):
        d.line([(S * (.28 + k * .1), S * .5), (S * (.46 + k * .02), S * .9)], fill=(220, 60, 60, 255), width=4)
    d.chord([S * .14, S * .06, S * .86, S * .66], 180, 360, fill=(240, 240, 255, 255), outline=OUT, width=8)
    d.pieslice([S * .14, S * .06, S * .86, S * .66], 180, 240, fill=(240, 40, 60, 255))
    d.pieslice([S * .14, S * .06, S * .86, S * .66], 240, 300, fill=(40, 120, 255, 255))
    d.pieslice([S * .14, S * .06, S * .86, S * .66], 300, 360, fill=(255, 220, 40, 255))
    d.chord([S * .14, S * .06, S * .86, S * .66], 180, 360, outline=OUT, width=8)
    d.rectangle([S * .14, S * .36, S * .86, S * .46], fill=(240, 240, 255, 255), outline=OUT, width=6)
    for x in (.3, .5, .7):
        d.ellipse([S * (x - .02), S * .18, S * (x + .02), S * .22], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def syrup_splat(size=64):
    """A splat of rainbow snow-cone slush: icy white with red, blue and yellow syrup streaks."""
    import math
    im, d, S = _big(size)
    OUT = (40, 30, 60, 255)
    pts = []
    for k in range(16):
        r = .44 if k % 2 == 0 else .3
        a = k * math.tau / 16 + .2
        pts.append((S * (.5 + r * math.cos(a)), S * (.5 + r * math.sin(a))))
    _outline_poly(d, pts, (235, 245, 255, 255), OUT, 7)
    d.ellipse([S * .3, S * .3, S * .5, S * .5], fill=(240, 40, 60, 255))
    d.ellipse([S * .5, S * .36, S * .68, S * .54], fill=(40, 120, 255, 255))
    d.ellipse([S * .38, S * .52, S * .56, S * .68], fill=(255, 220, 40, 255))
    return _shrink(im, size)


def folding_table(size=64, flipped=False):
    """A cookout table: a red-and-white checkered tablecloth draped over it, a plate of ribs, a red cup, the
    legs showing under the cloth - or mid-flip, upside down."""
    im, d, S = _big(size)
    OUT = (30, 20, 10, 255)
    for x in (.2, .8):                                                                                  # legs
        d.rectangle([S * (x - .025), S * .6, S * (x + .025), S * .96], fill=(150, 150, 160, 255), outline=OUT, width=4)
    cloth = [(S * .02, S * .38), (S * .98, S * .38), (S * .94, S * .66), (S * .06, S * .66)]
    d.polygon(cloth, fill=(250, 250, 250, 255))
    for r in range(4):
        for c in range(12):
            if (r + c) % 2 == 0:
                x0 = S * (.04 + c * .078)
                y0 = S * (.38 + r * .07)
                d.rectangle([x0, y0, x0 + S * .078, y0 + S * .07], fill=(220, 40, 40, 255))
    d.line(cloth + [cloth[0]], fill=OUT, width=7)
    for k in range(10):                                                                                 # fringe
        x = S * (.08 + k * .093)
        d.polygon([(x, S * .66), (x + S * .04, S * .72), (x + S * .08, S * .66)], fill=(220, 40, 40, 255), outline=OUT)
    d.ellipse([S * .24, S * .24, S * .58, S * .4], fill=(250, 250, 245, 255), outline=OUT, width=5)     # plate
    d.ellipse([S * .3, S * .22, S * .52, S * .34], fill=(160, 80, 35, 255), outline=OUT, width=3)       # ribs
    d.polygon([(S * .66, S * .14), (S * .8, S * .14), (S * .78, S * .4), (S * .68, S * .4)], fill=(220, 30, 40, 255), outline=OUT)  # cup
    d.line([(S * .66, S * .14), (S * .8, S * .14), (S * .78, S * .4), (S * .68, S * .4), (S * .66, S * .14)], fill=OUT, width=5)
    d.line([(S * .66, S * .18), (S * .8, S * .18)], fill=(250, 250, 250, 255), width=4)
    im = _shrink(im, size)
    return im.rotate(160, resample=Image.BICUBIC) if flipped else im


def paper_plate(size=32):
    """A paper plate with a smear of mac and cheese, flying (spins)."""
    im, d, S = _big(size)
    OUT = (90, 80, 60, 255)
    d.ellipse([S * .04, S * .04, S * .96, S * .96], fill=(250, 248, 238, 255), outline=OUT, width=6)
    d.ellipse([S * .2, S * .2, S * .8, S * .8], outline=(220, 210, 190, 255), width=5)
    d.ellipse([S * .3, S * .34, S * .64, S * .62], fill=(255, 200, 50, 255))
    return _shrink(im, size)


def pogo_stick(size=64):
    """A pogo stick: red T handlebars, chrome shaft, the foot pegs, a coiled spring, a rubber foot."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rectangle([S * .2, S * .04, S * .8, S * .12], fill=(220, 30, 40, 255), outline=OUT, width=6)       # bars
    d.rectangle([S * .46, S * .08, S * .54, S * .7], fill=(200, 205, 215, 255), outline=OUT, width=6)   # shaft
    d.rectangle([S * .26, S * .56, S * .74, S * .62], fill=(40, 40, 45, 255), outline=OUT, width=5)     # pegs
    for k in range(6):                                                                                  # spring
        y = S * (.28 + k * .045)
        d.ellipse([S * .38, y, S * .62, y + S * .05], outline=(150, 150, 160, 255), width=4)
    d.rectangle([S * .47, S * .7, S * .53, S * .9], fill=(150, 150, 160, 255), outline=OUT, width=4)
    d.rounded_rectangle([S * .42, S * .88, S * .58, S * .98], 6, fill=(30, 30, 30, 255), outline=OUT, width=4)
    return _shrink(im, size)


def salon_scissors(size=64, shut=False):
    """Big silver salon shears with red finger loops - blades wide open in a V, or snipped shut."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    spread = 0 if shut else .2
    for sgn in (-1, 1):
        tip = (S * .96, S * (.5 + sgn * spread))
        blade = [(S * .46, S * (.5 + sgn * .04)), tip, (S * .5, S * (.5 - sgn * .02))]
        _outline_poly(d, blade, (210, 215, 228, 255), OUT, 6)
        d.line([(S * .5, S * .5), (S * .3, S * (.5 - sgn * .16))], fill=OUT, width=int(S * .06))
        d.ellipse([S * .06, S * (.5 - sgn * .16) - S * .1, S * .3, S * (.5 - sgn * .16) + S * .1], outline=OUT, width=int(S * .06))
        d.ellipse([S * .07, S * (.5 - sgn * .16) - S * .09, S * .29, S * (.5 - sgn * .16) + S * .09], outline=(220, 40, 50, 255), width=int(S * .035))
    d.ellipse([S * .45, S * .45, S * .55, S * .55], fill=(240, 200, 60, 255), outline=OUT, width=4)
    return _shrink(im, size)


def hair_tuft(n=16):
    """A curly lock of hair, a fat C-shaped curl (alpha only)."""
    def f(x, y):
        r = ((x - 8) ** 2 + (y - 8) ** 2) ** .5
        return 1 if 3 < r < 6.5 and not (x > 9 and 5 < y < 11) else 0
    return _alpha(n, n, f)


def lava_lamp(size=64):
    """A retro lava lamp: chrome cone base and cap, purple glass, orange wax blobs floating up."""
    im, d, S = _big(size)
    OUT = (25, 15, 30, 255)
    d.polygon([(S * .3, S * .08), (S * .7, S * .08), (S * .62, S * .18), (S * .38, S * .18)], fill=(200, 205, 215, 255), outline=OUT)
    _outline_poly(d, [(S * .38, S * .18), (S * .62, S * .18), (S * .74, S * .7), (S * .26, S * .7)], (150, 60, 200, 255), OUT, 7)
    for x, y, r in ((.5, .32, .06), (.44, .48, .08), (.58, .6, .07), (.52, .24, .04)):
        d.ellipse([S * (x - r), S * (y - r * 1.2), S * (x + r), S * (y + r * 1.2)], fill=(255, 130, 40, 255))
    d.line([(S * .42, S * .24), (S * .34, S * .6)], fill=(220, 160, 255, 255), width=5)
    _outline_poly(d, [(S * .26, S * .7), (S * .74, S * .7), (S * .84, S * .96), (S * .16, S * .96)], (200, 205, 215, 255), OUT, 7)
    return _shrink(im, size)


def lava_blob(n=16):
    """A gooey lava-lamp wax blob (alpha only)."""
    def f(x, y):
        r = ((x - 7.5) / 5.5) ** 2 + ((y - 8) / 6.5) ** 2
        return 1 if r <= 1 else 0
    return _alpha(n, n, f)


def pancake(size=64):
    """One fluffy pancake, side on: golden edge, browned top, a little steam."""
    im, d, S = _big(size)
    OUT = (80, 40, 10, 255)
    d.ellipse([S * .04, S * .36, S * .96, S * .66], fill=(240, 190, 100, 255), outline=OUT, width=7)
    d.ellipse([S * .06, S * .34, S * .94, S * .56], fill=(200, 130, 50, 255), outline=OUT, width=6)
    d.arc([S * .2, S * .38, S * .5, S * .48], 190, 300, fill=(240, 180, 100, 255), width=5)
    return _shrink(im, size)


def butter_syrup(size=64):
    """The topping: a pat of butter melting, syrup pouring down over the edge."""
    im, d, S = _big(size)
    OUT = (80, 40, 10, 255)
    d.ellipse([S * .1, S * .5, S * .9, S * .7], fill=(140, 70, 20, 230))
    for x, ln in ((.18, .24), (.42, .32), (.74, .2)):
        d.rounded_rectangle([S * x, S * .58, S * (x + .06), S * (.58 + ln)], 6, fill=(140, 70, 20, 230))
    d.polygon([(S * .38, S * .36), (S * .62, S * .36), (S * .66, S * .5), (S * .34, S * .5)], fill=(255, 235, 120, 255), outline=OUT)
    d.line([(S * .4, S * .4), (S * .54, S * .4)], fill=(255, 255, 220, 255), width=4)
    return _shrink(im, size)


def clapperboard(size=64, shut=False):
    """A film clapperboard: black and white striped clapstick (open at an angle, or snapped shut), the slate
    reading TAKE 2 (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rectangle([S * .06, S * .36, S * .94, S * .96], fill=(30, 30, 34, 255), outline=OUT, width=8)
    d.line([(S * .1, S * .66), (S * .9, S * .66)], fill=(240, 240, 240, 255), width=4)
    d.line([(S * .5, S * .66), (S * .5, S * .92)], fill=(240, 240, 240, 255), width=4)
    if shut:
        stick = [(S * .06, S * .24), (S * .94, S * .24), (S * .94, S * .36), (S * .06, S * .36)]
    else:
        stick = [(S * .06, S * .32), (S * .9, S * .02), (S * .94, S * .12), (S * .1, S * .42)]
    _outline_poly(d, stick, (250, 250, 250, 255), OUT, 6)
    for k in range(4):                                                                                  # stripes
        t0, t1 = .1 + k * .22, .2 + k * .22
        a = [(stick[0][0] + (stick[1][0] - stick[0][0]) * t, stick[0][1] + (stick[1][1] - stick[0][1]) * t) for t in (t0, t1)]
        b = [(stick[3][0] + (stick[2][0] - stick[3][0]) * t, stick[3][1] + (stick[2][1] - stick[3][1]) * t) for t in (t1, t0)]
        d.polygon(a + b, fill=OUT)
    d.ellipse([S * .04, S * .32, S * .12, S * .4], fill=(180, 180, 190, 255), outline=OUT, width=3)
    im = _shrink(im, size)
    return _texted(im, [("TAKE 2", (32, 30))], (255, 255, 255, 255))


def high_striker(size=64):
    """The carnival high striker: a tall red-and-white tower with a scale, the gold bell on top, the puck at the
    bottom on its strike pad."""
    im, d, S = _big(size)
    OUT = (20, 15, 15, 255)
    d.ellipse([S * .36, S * .0, S * .64, S * .14], fill=(250, 210, 40, 255), outline=OUT, width=6)    # bell
    d.rectangle([S * .44, S * .12, S * .56, S * .9], fill=(250, 250, 245, 255), outline=OUT, width=6)
    for k in range(7):
        d.rectangle([S * .44, S * (.16 + k * .11), S * .56, S * (.21 + k * .11)], fill=(220, 40, 40, 255))
    d.rectangle([S * .44, S * .12, S * .56, S * .9], outline=OUT, width=6)
    d.rectangle([S * .3, S * .88, S * .7, S * .98], fill=(120, 80, 40, 255), outline=OUT, width=6)    # strike pad
    d.rectangle([S * .42, S * .82, S * .58, S * .88], fill=(50, 50, 55, 255), outline=OUT, width=4)   # the puck
    return _shrink(im, size)


def mallet(size=64):
    """A giant carnival mallet swung down-right: a fat wooden head with steel bands, a long handle."""
    im, d, S = _big(size)
    OUT = (40, 25, 10, 255)
    d.line([(S * .1, S * .1), (S * .62, S * .62)], fill=OUT, width=int(S * .09))
    d.line([(S * .1, S * .1), (S * .62, S * .62)], fill=(190, 140, 80, 255), width=int(S * .05))
    head = [(S * .5, S * .78), (S * .78, S * .5), (S * .98, S * .7), (S * .7, S * .98)]
    _outline_poly(d, head, (180, 120, 60, 255), OUT, 8)
    for t in (.25, .75):
        p0 = (S * (.5 + .2 * t * 1.4), S * (.78 - .28 * t))
        d.line([(S * (.5 + .28 * t), S * (.78 - .28 * t)), (S * (.7 + .28 * t), S * (.98 - .28 * t))], fill=(180, 180, 190, 255), width=7)
    return _shrink(im, size)


def chalkboard(size=64):
    """A school chalkboard in a wooden frame with chalk doodles - a stick figure and NO - and a chalk ledge
    (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 25, 10, 255)
    d.rectangle([S * .02, S * .1, S * .98, S * .86], fill=(150, 100, 50, 255), outline=OUT, width=8)
    d.rectangle([S * .08, S * .16, S * .92, S * .8], fill=(40, 80, 60, 255))
    d.rectangle([S * .06, S * .8, S * .94, S * .9], fill=(170, 120, 60, 255), outline=OUT, width=5)
    d.rectangle([S * .6, S * .78, S * .7, S * .82], fill=(250, 250, 250, 255))
    d.ellipse([S * .66, S * .26, S * .74, S * .34], outline=(230, 230, 230, 255), width=4)               # stick guy
    d.line([(S * .7, S * .34), (S * .7, S * .52)], fill=(230, 230, 230, 255), width=4)
    d.line([(S * .62, S * .42), (S * .78, S * .42)], fill=(230, 230, 230, 255), width=4)
    d.line([(S * .7, S * .52), (S * .64, S * .62)], fill=(230, 230, 230, 255), width=4)
    d.line([(S * .7, S * .52), (S * .76, S * .62)], fill=(230, 230, 230, 255), width=4)
    im = _shrink(im, size)
    return _texted(im, [("NO", (21, 18)), ("SHHH", (24, 32))], (240, 240, 240, 255), (40, 80, 60, 255))


def dinner_fork(size=64):
    """A steel dinner fork held tines-down, angled into the board."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.line([(S * .2, S * .06), (S * .52, S * .56)], fill=OUT, width=int(S * .08))
    d.line([(S * .2, S * .06), (S * .52, S * .56)], fill=(200, 205, 215, 255), width=int(S * .045))
    _outline_poly(d, [(S * .46, S * .5), (S * .6, S * .48), (S * .66, S * .62), (S * .54, S * .66)], (200, 205, 215, 255), OUT, 5)
    for k in range(4):
        x = S * (.54 + k * .04)
        d.line([(x, S * (.62 + k * .01)), (x + S * .1, S * (.9 + k * .01))], fill=OUT, width=7)
        d.line([(x, S * (.62 + k * .01)), (x + S * .1, S * (.9 + k * .01))], fill=(220, 225, 235, 255), width=3)
    return _shrink(im, size)


def mosquito(size=32):
    """A mosquito side on: striped body, long needle nose, thin legs, see-through wings."""
    im, d, S = _big(size)
    OUT = (20, 15, 15, 255)
    d.ellipse([S * .3, S * .1, S * .62, S * .44], fill=(220, 235, 255, 150), outline=(120, 140, 170, 255), width=4)  # wings
    d.ellipse([S * .46, S * .06, S * .78, S * .4], fill=(220, 235, 255, 150), outline=(120, 140, 170, 255), width=4)
    d.ellipse([S * .3, S * .4, S * .7, S * .6], fill=(90, 70, 60, 255), outline=OUT, width=5)          # body
    for x in (.4, .5, .6):
        d.line([(S * x, S * .42), (S * x, S * .58)], fill=(230, 220, 200, 255), width=3)
    d.ellipse([S * .66, S * .4, S * .8, S * .54], fill=(60, 50, 45, 255), outline=OUT, width=4)        # head
    d.line([(S * .78, S * .5), (S * 1.0, S * .6)], fill=OUT, width=4)                                    # needle
    for x in (.36, .48, .6):
        d.line([(S * x, S * .58), (S * (x - .08), S * .9)], fill=OUT, width=3)
    d.ellipse([S * .72, S * .42, S * .76, S * .46], fill=(255, 40, 40, 255))
    return _shrink(im, size)


def toilet(size=64):
    """A big white toilet seen from the front: lid up, the tank, the shiny handle, blue water in the bowl."""
    im, d, S = _big(size)
    OUT = (25, 30, 40, 255)
    W, W_D = (250, 252, 255, 255), (200, 210, 225, 255)
    d.rounded_rectangle([S * .24, S * .0, S * .76, S * .34], 8, fill=W, outline=OUT, width=7)          # lid up
    d.rounded_rectangle([S * .2, S * .3, S * .8, S * .46], 6, fill=W, outline=OUT, width=7)            # tank
    d.rectangle([S * .66, S * .34, S * .78, S * .38], fill=(190, 195, 210, 255), outline=OUT, width=3)  # handle
    d.ellipse([S * .08, S * .44, S * .92, S * .76], fill=W, outline=OUT, width=8)                      # bowl rim
    d.ellipse([S * .2, S * .5, S * .8, S * .7], fill=(90, 170, 255, 255), outline=OUT, width=5)
    d.arc([S * .3, S * .54, S * .7, S * .66], 200, 340, fill=(220, 240, 255, 255), width=5)
    _outline_poly(d, [(S * .28, S * .72), (S * .72, S * .72), (S * .64, S * .98), (S * .36, S * .98)], W_D, OUT, 7)
    return _shrink(im, size)


def swirl_water(n=16):
    """A whirl of water, a spiral (alpha only)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = x - c, y - c
        r = (dx * dx + dy * dy) ** .5
        a = math.atan2(dy, dx)
        return 1 if r < 7.5 and abs(((r - a * 1.4) % 4.4) - 2.2) < .9 else 0
    return _alpha(n, n, f)


def tp_roll(size=32):
    """A roll of toilet paper unspooling a ribbon (flies around the bowl)."""
    im, d, S = _big(size)
    OUT = (90, 90, 100, 255)
    d.rectangle([S * .1, S * .3, S * .6, S * .7], fill=(250, 250, 250, 255), outline=OUT, width=6)
    d.ellipse([S * .0, S * .3, S * .2, S * .7], fill=(240, 240, 245, 255), outline=OUT, width=5)
    d.ellipse([S * .06, S * .44, S * .14, S * .56], fill=(170, 140, 110, 255))
    d.line([(S * .6, S * .66), (S * .8, S * .8), (S * .96, S * .6)], fill=(250, 250, 250, 255), width=int(S * .14))
    d.line([(S * .6, S * .66), (S * .8, S * .8), (S * .96, S * .6)], fill=OUT, width=3)
    return _shrink(im, size)


def striker_puck(size=32):
    """The high striker's black puck with a red stripe, flying up the tower."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rounded_rectangle([S * .14, S * .3, S * .86, S * .7], 8, fill=(40, 40, 46, 255), outline=OUT, width=7)
    d.rectangle([S * .14, S * .44, S * .86, S * .56], fill=(220, 40, 40, 255))
    d.line([(S * .24, S * .36), (S * .6, S * .36)], fill=(140, 140, 150, 255), width=5)
    return _shrink(im, size)


def skull_glyph(n=16):
    """A little cartoon skull (alpha only): bad vibes."""
    def f(x, y):
        head = (x - 7.5) ** 2 / 36 + (y - 6.5) ** 2 / 30 <= 1
        jaw = 5 <= x <= 10 and 10 <= y <= 13
        eye = (x - 5.3) ** 2 + (y - 6.5) ** 2 < 2.6 or (x - 9.7) ** 2 + (y - 6.5) ** 2 < 2.6
        return .35 if eye and head else (1 if head or jaw else 0)
    return _alpha(n, n, f)


def black_candle(size=64):
    """A tall black ritual candle dripping wax, a purple flame, on a little iron dish with a skull etched on it."""
    im, d, S = _big(size)
    OUT = (20, 10, 30, 255)
    d.polygon([(S * .5, S * .0), (S * .6, S * .16), (S * .5, S * .24), (S * .4, S * .16)], fill=(170, 80, 255, 255))
    d.polygon([(S * .5, S * .08), (S * .54, S * .16), (S * .5, S * .21), (S * .46, S * .16)], fill=(240, 220, 255, 255))
    d.line([(S * .5, S * .24), (S * .5, S * .3)], fill=OUT, width=4)
    d.rectangle([S * .38, S * .3, S * .62, S * .84], fill=(35, 30, 45, 255), outline=OUT, width=7)
    for x, ln in ((.4, .16), (.52, .26), (.58, .1)):                                                    # drips
        d.rounded_rectangle([S * x, S * .3, S * (x + .05), S * (.3 + ln)], 6, fill=(55, 50, 70, 255))
    d.line([(S * .42, S * .36), (S * .42, S * .78)], fill=(90, 85, 110, 255), width=4)
    d.ellipse([S * .2, S * .8, S * .8, S * .96], fill=(80, 80, 90, 255), outline=OUT, width=6)          # dish
    d.ellipse([S * .46, S * .84, S * .54, S * .9], fill=(200, 200, 210, 255))
    return _shrink(im, size)


# ---- set 19 --------------------------------------------------------------------------------------------

def pineapple(size=32):
    """A whole pineapple, spiky green crown, the diamond rind (tumbling)."""
    im, d, S = _big(size)
    OUT = (60, 35, 5, 255)
    for k, (x0, x1) in enumerate(((.5, .3), (.5, .5), (.5, .7), (.5, .38), (.5, .62))):
        d.polygon([(S * (x0 - .06), S * .36), (S * x1, S * (.0 + k % 2 * .06)), (S * (x0 + .06), S * .36)], fill=(60, 160, 60, 255), outline=(20, 70, 20, 255))
    d.ellipse([S * .22, S * .3, S * .78, S * .98], fill=(240, 180, 40, 255), outline=OUT, width=7)
    for k in range(5):
        d.line([(S * (.24 + k * .12), S * .34), (S * (.12 + k * .12), S * .9)], fill=(190, 120, 20, 255), width=4)
        d.line([(S * (.76 - k * .12), S * .34), (S * (.88 - k * .12), S * .9)], fill=(190, 120, 20, 255), width=4)
    return _shrink(im, size)


def watermelon(size=64):
    """A whole watermelon, dark green stripes, a shine."""
    im, d, S = _big(size)
    OUT = (15, 50, 15, 255)
    d.ellipse([S * .04, S * .2, S * .96, S * .82], fill=(70, 170, 60, 255), outline=OUT, width=8)
    for k in range(5):
        x = S * (.14 + k * .18)
        d.arc([x - S * .1, S * .22, x + S * .1, S * .8], 250, 290, fill=(30, 100, 30, 255), width=int(S * .07))
        d.line([(x, S * .24), (x + S * (.02 if k % 2 else -.02), S * .78)], fill=(30, 100, 30, 255), width=int(S * .06))
    d.ellipse([S * .04, S * .2, S * .96, S * .82], outline=OUT, width=8)
    d.arc([S * .12, S * .26, S * .6, S * .6], 200, 260, fill=(200, 250, 180, 255), width=8)
    return _shrink(im, size)


def melon_splat(size=64):
    """A smashed watermelon: red pulp splattered out, black seeds, green rind chunks."""
    import math
    im, d, S = _big(size)
    OUT = (90, 10, 20, 255)
    pts = []
    for k in range(18):
        r = .46 if k % 2 == 0 else .3
        a = k * math.tau / 18 + .3
        pts.append((S * (.5 + r * math.cos(a)), S * (.52 + r * .8 * math.sin(a))))
    _outline_poly(d, pts, (235, 50, 70, 255), OUT, 7)
    d.ellipse([S * .3, S * .36, S * .7, S * .68], fill=(255, 110, 120, 255))
    for x, y in ((.36, .44), (.5, .5), (.6, .42), (.44, .6), (.66, .58), (.28, .56)):
        d.ellipse([S * (x - .025), S * (y - .035), S * (x + .025), S * (y + .035)], fill=(20, 15, 15, 255))
    for x, y in ((.1, .3), (.86, .74)):
        d.chord([S * (x - .1), S * (y - .06), S * (x + .1), S * (y + .06)], 0, 180, fill=(60, 150, 50, 255), outline=(15, 50, 15, 255), width=5)
    return _shrink(im, size)


def air_mattress(size=64, flat=False):
    """A blue air mattress with its pillow bump and the grid of ribs - puffed up, or lying flat and saggy."""
    im, d, S = _big(size)
    OUT = (15, 30, 70, 255)
    if flat:
        _outline_poly(d, [(S * .04, S * .74), (S * .3, S * .7), (S * .6, S * .74), (S * .96, S * .72), (S * .94, S * .86), (S * .06, S * .86)],
                      (70, 120, 210, 255), OUT, 7)
        d.line([(S * .1, S * .78), (S * .9, S * .8)], fill=(130, 170, 240, 255), width=4)
    else:
        d.rounded_rectangle([S * .02, S * .44, S * .98, S * .86], 20, fill=(80, 140, 230, 255), outline=OUT, width=8)
        d.rounded_rectangle([S * .06, S * .36, S * .3, S * .6], 14, fill=(110, 165, 240, 255), outline=OUT, width=6)  # pillow
        for k in range(5):
            d.line([(S * (.36 + k * .12), S * .5), (S * (.36 + k * .12), S * .8)], fill=(50, 100, 190, 255), width=5)
        d.line([(S * .08, S * .5), (S * .9, S * .5)], fill=(170, 210, 255, 255), width=5)
    return _shrink(im, size)


def crt_tv(size=64):
    """An old box TV: wood-grain sides, a curved grey screen with static, rabbit-ear antenna, two knobs."""
    im, d, S = _big(size)
    OUT = (30, 20, 10, 255)
    d.line([(S * .5, S * .2), (S * .3, S * .02)], fill=(150, 150, 160, 255), width=5)                  # rabbit ears
    d.line([(S * .5, S * .2), (S * .72, S * .04)], fill=(150, 150, 160, 255), width=5)
    d.rounded_rectangle([S * .06, S * .2, S * .94, S * .9], 10, fill=(130, 85, 45, 255), outline=OUT, width=8)
    d.rounded_rectangle([S * .12, S * .28, S * .7, S * .82], 18, fill=(150, 160, 160, 255), outline=OUT, width=6)
    rnd = __import__("random").Random(4)
    for k in range(40):                                                                                 # static
        x, y = S * rnd.uniform(.16, .66), S * rnd.uniform(.32, .78)
        d.rectangle([x, y, x + S * .03, y + S * .02], fill=(230, 230, 230, 255) if k % 2 else (90, 90, 95, 255))
    for y in (.36, .54):
        d.ellipse([S * .75, S * y, S * .87, S * (y + .12)], fill=(60, 60, 66, 255), outline=OUT, width=5)
    d.rectangle([S * .76, S * .74, S * .86, S * .8], fill=(40, 40, 45, 255))
    return _shrink(im, size)


def dream_bubble(size=64):
    """A thought cloud of the foe's dream: a mansion, a stack of cash and a chain, little bubbles trailing down."""
    import math
    im, d, S = _big(size)
    OUT = (90, 90, 130, 255)
    for k in range(9):
        a = k * math.tau / 9
        cx, cy = S * (.52 + .32 * math.cos(a)), S * (.4 + .24 * math.sin(a))
        d.ellipse([cx - S * .15, cy - S * .13, cx + S * .15, cy + S * .13], fill=(250, 250, 255, 255), outline=OUT, width=5)
    d.ellipse([S * .2, S * .16, S * .84, S * .66], fill=(250, 250, 255, 255))
    d.polygon([(S * .3, S * .44), (S * .44, S * .3), (S * .58, S * .44)], fill=(200, 60, 60, 255))    # the mansion
    d.rectangle([S * .32, S * .44, S * .56, S * .58], fill=(240, 220, 170, 255), outline=(120, 90, 50, 255), width=3)
    d.rectangle([S * .42, S * .5, S * .46, S * .58], fill=(120, 80, 40, 255))
    d.rectangle([S * .6, S * .44, S * .76, S * .56], fill=(100, 190, 90, 255), outline=(40, 100, 40, 255), width=3)  # cash
    d.rectangle([S * .6, S * .4, S * .76, S * .46], fill=(120, 210, 110, 255), outline=(40, 100, 40, 255), width=3)
    d.arc([S * .6, S * .24, S * .78, S * .4], 0, 180, fill=(250, 200, 40, 255), width=5)                # chain
    for x, y, r in ((.3, .8, .06), (.22, .9, .04)):
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], fill=(250, 250, 255, 255), outline=OUT, width=4)
    return _shrink(im, size)


def safety_pin(size=32):
    """A big silver pin, needle pointing right-down."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.line([(S * .08, S * .2), (S * .92, S * .8)], fill=OUT, width=int(S * .1))
    d.line([(S * .08, S * .2), (S * .92, S * .8)], fill=(210, 215, 228, 255), width=int(S * .05))
    d.ellipse([S * .0, S * .08, S * .2, S * .3], fill=(230, 40, 50, 255), outline=OUT, width=5)
    return _shrink(im, size)


def lobster_claw(size=64, shut=False):
    """A giant boiled-red lobster claw facing right: the big crusher - wide open, or pinched shut. Bumpy shell."""
    im, d, S = _big(size)
    OUT = (80, 10, 5, 255)
    RED, RED_L = (225, 60, 35, 255), (255, 150, 110, 255)
    gap = 0 if shut else .16
    d.rounded_rectangle([S * .0, S * .42, S * .3, S * .62], 10, fill=RED, outline=OUT, width=7)        # arm
    top = [(S * .26, S * .5), (S * .4, S * (.22 - gap)), (S * .8, S * (.2 - gap)), (S * .98, S * (.44 - gap * .4)), (S * .6, S * (.46 - gap * .3)), (S * .3, S * .56)]
    _outline_poly(d, top, RED, OUT, 8)
    bot = [(S * .3, S * .52), (S * .5, S * (.58 + gap * .3)), (S * .9, S * (.56 + gap * .6)), (S * .84, S * (.78 + gap * .6)), (S * .4, S * .78)]
    _outline_poly(d, bot, RED, OUT, 8)
    for x, y in ((.5, .3), (.66, .28), (.56, .66), (.7, .68)):
        d.ellipse([S * x, S * (y - gap), S * (x + .05), S * (y - gap + .04)], fill=RED_L)
    return _shrink(im, size)


def e_scooter(size=64):
    """A rental e-scooter facing right: green deck, tall stem, handlebars, little wheels, a phone mount."""
    im, d, S = _big(size)
    OUT = (15, 20, 15, 255)
    d.line([(S * .76, S * .84), (S * .66, S * .14)], fill=OUT, width=int(S * .07))                     # stem
    d.line([(S * .76, S * .84), (S * .66, S * .14)], fill=(60, 200, 90, 255), width=int(S * .035))
    d.line([(S * .56, S * .14), (S * .8, S * .1)], fill=OUT, width=int(S * .06))                       # bars
    d.rounded_rectangle([S * .14, S * .76, S * .8, S * .86], 6, fill=(60, 200, 90, 255), outline=OUT, width=6)  # deck
    for x in (.18, .8):
        d.ellipse([S * (x - .08), S * .8, S * (x + .08), S * .96], fill=(40, 40, 45, 255), outline=OUT, width=5)
        d.ellipse([S * (x - .03), S * .85, S * (x + .03), S * .91], fill=(200, 200, 210, 255))
    d.rectangle([S * .62, S * .2, S * .7, S * .3], fill=(30, 30, 36, 255), outline=OUT, width=4)       # phone
    d.line([(S * .2, S * .8), (S * .7, S * .8)], fill=(200, 255, 200, 255), width=3)
    return _shrink(im, size)


def dragon_head(size=64):
    """A parade dragon-dance head facing right: red and gold, bulging eyes, open jaw with a pink tongue, a fringe
    of gold fur."""
    im, d, S = _big(size)
    OUT = (70, 20, 0, 255)
    RED, GOLD = (220, 35, 35, 255), (250, 200, 40, 255)
    _outline_poly(d, [(S * .06, S * .3), (S * .7, S * .2), (S * .96, S * .4), (S * .7, S * .5), (S * .96, S * .62),
                      (S * .6, S * .8), (S * .1, S * .8)], RED, OUT, 8)
    d.polygon([(S * .7, S * .5), (S * .96, S * .52), (S * .78, S * .58)], fill=(255, 140, 170, 255))    # tongue
    d.ellipse([S * .44, S * .14, S * .62, S * .36], fill=(250, 250, 250, 255), outline=OUT, width=6)    # eye
    d.ellipse([S * .52, S * .2, S * .6, S * .3], fill=OUT)
    for k in range(6):                                                                                  # fur
        x = S * (.08 + k * .1)
        d.polygon([(x, S * .78), (x + S * .05, S * .94), (x + S * .1, S * .78)], fill=GOLD, outline=OUT)
    d.line([(S * .2, S * .34), (S * .3, S * .1)], fill=GOLD, width=8)                                   # horn
    d.line([(S * .16, S * .5), (S * .5, S * .44)], fill=GOLD, width=6)
    return _shrink(im, size)


def firecracker_string(n=16):
    """A little firecracker pop (alpha only): a burst of short rays."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        r = ((x - c) ** 2 + (y - c) ** 2) ** .5
        a = math.atan2(y - c, x - c)
        return 1 if r < 2.5 or (r < 7 and abs(math.sin(a * 4)) < .25) else 0
    return _alpha(n, n, f)


def glitter_envelope(size=64, open_=False):
    """A manila envelope addressed in marker - sealed, or torn open with silver glitter puffing out."""
    im, d, S = _big(size)
    OUT = (80, 60, 20, 255)
    d.rectangle([S * .06, S * .28, S * .94, S * .86], fill=(230, 200, 130, 255), outline=OUT, width=8)
    if open_:
        d.polygon([(S * .06, S * .28), (S * .5, S * .02), (S * .94, S * .28)], fill=(210, 180, 110, 255), outline=OUT)
        for k in range(14):
            x, y = S * (.16 + (k * 37 % 70) / 100), S * (.02 + (k * 13 % 26) / 100)
            d.polygon([(x, y - S * .03), (x + S * .015, y), (x, y + S * .03), (x - S * .015, y)], fill=(230, 235, 250, 255))
    else:
        d.polygon([(S * .06, S * .28), (S * .5, S * .56), (S * .94, S * .28)], fill=(210, 180, 110, 255), outline=OUT)
    for k in range(3):
        d.line([(S * .3, S * (.66 + k * .06)), (S * .74, S * (.66 + k * .06))], fill=(40, 40, 60, 255), width=4)
    d.rectangle([S * .74, S * .34, S * .88, S * .48], fill=(220, 60, 60, 255), outline=OUT, width=3)    # stamp
    return _shrink(im, size)


def ice_bag(size=64):
    """A big clear bag of party ice with a blue ICE logo, cubes inside, the twist tie (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 70, 120, 255)
    d.polygon([(S * .42, S * .02), (S * .58, S * .02), (S * .54, S * .14), (S * .46, S * .14)], fill=(220, 235, 250, 230), outline=OUT)
    d.rectangle([S * .42, S * .12, S * .58, S * .16], fill=(220, 40, 40, 255))                         # tie
    _outline_poly(d, [(S * .46, S * .14), (S * .54, S * .14), (S * .9, S * .4), (S * .92, S * .94), (S * .08, S * .94), (S * .1, S * .4)],
                  (225, 240, 255, 220), OUT, 7)
    for x, y in ((.24, .7), (.4, .78), (.58, .72), (.74, .8), (.3, .86), (.66, .88)):
        d.rectangle([S * (x - .06), S * (y - .05), S * (x + .06), S * (y + .05)], fill=(190, 225, 255, 255), outline=(150, 190, 230, 255), width=3)
    d.ellipse([S * .22, S * .4, S * .78, S * .62], fill=(40, 110, 220, 255), outline=OUT, width=5)
    im = _shrink(im, size)
    return _texted(im, [("ICE", (32, 29))], (255, 255, 255, 255), (20, 60, 140, 255), font=GLYPHS)


def ice_cubelet(n=16):
    """A chunky ice cube with a bright edge (alpha only)."""
    def f(x, y):
        inside = 3 <= x <= 12 and 3 <= y <= 12
        edge = inside and (x <= 4 or y <= 4)
        return 1 if edge else (.65 if inside else 0)
    return _alpha(n, n, f)


def evidence_bag(size=64):
    """A clear plastic EVIDENCE bag with the red-striped label and a zip seal (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (60, 60, 70, 255)
    d.rectangle([S * .1, S * .06, S * .9, S * .94], fill=(235, 240, 245, 200), outline=OUT, width=7)
    d.rectangle([S * .1, S * .06, S * .9, S * .14], fill=(200, 60, 60, 255), outline=OUT, width=5)     # seal
    d.rectangle([S * .16, S * .2, S * .84, S * .5], fill=(255, 255, 255, 255), outline=(200, 40, 40, 255), width=5)
    for k in range(3):
        d.line([(S * .2, S * (.62 + k * .08)), (S * .8, S * (.62 + k * .08))], fill=(150, 150, 160, 255), width=3)
    im = _shrink(im, size)
    return _texted(im, [("EVIDENCE", (32, 17))], (220, 30, 30, 255), (255, 255, 255, 255))


def caution_strip(size=64):
    """A strip of yellow CAUTION tape stretched across (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 24, 63, 39], fill=(255, 215, 0, 255), outline=(40, 30, 0, 255))
    for x in range(-8, 64, 12):
        d.polygon([(x, 39), (x + 5, 24), (x + 8, 24), (x + 3, 39)], fill=(30, 30, 30, 255))
    d.rectangle([12, 27, 51, 36], fill=(255, 215, 0, 255))
    _texted(im, [("CAUTION", (32, 29))], (20, 20, 20, 255), (255, 215, 0, 255))
    return im


def matchbox(size=64, lit=False):
    """A matchbox with a red striker strip - and a match in front of it, unlit, or flaring blue-white."""
    im, d, S = _big(size)
    OUT = (40, 20, 10, 255)
    d.rectangle([S * .06, S * .54, S * .7, S * .9], fill=(240, 220, 160, 255), outline=OUT, width=7)
    d.rectangle([S * .06, S * .54, S * .7, S * .62], fill=(150, 60, 40, 255))
    d.ellipse([S * .28, S * .66, S * .48, S * .84], fill=(220, 40, 40, 255), outline=OUT, width=4)     # logo
    d.line([(S * .62, S * .5), (S * .88, S * .16)], fill=(220, 190, 130, 255), width=int(S * .05))     # the match
    d.ellipse([S * .84, S * .1, S * .94, S * .2], fill=(200, 40, 40, 255), outline=OUT, width=3)
    if lit:
        d.polygon([(S * .9, S * -.04), (S * 1.0, S * .14), (S * .89, S * .22), (S * .8, S * .12)], fill=(120, 170, 255, 255))
        d.polygon([(S * .9, S * .04), (S * .95, S * .14), (S * .89, S * .19), (S * .85, S * .13)], fill=(230, 240, 255, 255))
    return _shrink(im, size)


def party_balloon(size=64):
    """A pink party balloon on a curly string, a big shine (it's been rubbed on a head - static)."""
    im, d, S = _big(size)
    OUT = (110, 20, 60, 255)
    d.ellipse([S * .18, S * .04, S * .82, S * .74], fill=(255, 100, 170, 255), outline=OUT, width=8)
    d.polygon([(S * .46, S * .73), (S * .54, S * .73), (S * .5, S * .8)], fill=(255, 100, 170, 255), outline=OUT)
    d.arc([S * .28, S * .12, S * .56, S * .4], 200, 270, fill=(255, 220, 240, 255), width=10)
    d.line([(S * .5, S * .8), (S * .44, S * .86), (S * .56, S * .92), (S * .48, S * .98)], fill=(80, 80, 90, 255), width=4)
    return _shrink(im, size)


def frisbee(size=32):
    """A red frisbee seen tilted, a white ring and a shine (spins)."""
    im, d, S = _big(size)
    OUT = (80, 10, 10, 255)
    d.ellipse([S * .04, S * .28, S * .96, S * .72], fill=(230, 40, 40, 255), outline=OUT, width=7)
    d.ellipse([S * .24, S * .38, S * .76, S * .62], outline=(255, 255, 255, 255), width=5)
    d.arc([S * .1, S * .3, S * .6, S * .56], 190, 250, fill=(255, 170, 170, 255), width=6)
    return _shrink(im, size)


def lone_feather(n=16):
    """One little feather (alpha only), drifting down."""
    def f(x, y):
        on_spine = abs((x - 3) - (y - 2) * .8) < .9 and 2 <= y <= 14
        vane = abs((x - 3) - (y - 2) * .8) < 3.2 - abs(y - 8) * .35 and 3 <= y <= 13
        return 1 if on_spine else (.6 if vane else 0)
    return _alpha(n, n, f)


def crash_dummy(size=64):
    """A crash-test dummy sitting up stiff: yellow, the black-and-yellow target dots on the head and chest, the
    joint bolts."""
    im, d, S = _big(size)
    OUT = (30, 25, 10, 255)
    Y = (250, 210, 40, 255)
    d.ellipse([S * .34, S * .04, S * .66, S * .34], fill=Y, outline=OUT, width=7)                       # head
    d.pieslice([S * .42, S * .12, S * .58, S * .28], 0, 90, fill=OUT)
    d.pieslice([S * .42, S * .12, S * .58, S * .28], 180, 270, fill=OUT)
    d.ellipse([S * .42, S * .12, S * .58, S * .28], outline=OUT, width=4)
    d.rectangle([S * .44, S * .32, S * .56, S * .38], fill=(120, 120, 130, 255), outline=OUT, width=4)  # neck
    d.rounded_rectangle([S * .26, S * .36, S * .74, S * .74], 10, fill=Y, outline=OUT, width=7)        # torso
    d.pieslice([S * .4, S * .46, S * .6, S * .66], 0, 90, fill=OUT)
    d.pieslice([S * .4, S * .46, S * .6, S * .66], 180, 270, fill=OUT)
    d.ellipse([S * .4, S * .46, S * .6, S * .66], outline=OUT, width=4)
    for x in (.12, .78):                                                                                 # arms
        d.rounded_rectangle([S * x, S * .38, S * (x + .1), S * .7], 6, fill=Y, outline=OUT, width=6)
    for x in (.3, .56):                                                                                  # legs
        d.rounded_rectangle([S * x, S * .72, S * (x + .14), S * .98], 6, fill=Y, outline=OUT, width=6)
    for x, y in ((.17, .4), (.83, .4), (.37, .74), (.63, .74)):
        d.ellipse([S * (x - .025), S * (y - .025), S * (x + .025), S * (y + .025)], fill=(150, 150, 160, 255))
    return _shrink(im, size)


def shadow_claws(size=64):
    """Three dark purple claw slashes curling up out of the ground, wispy edges."""
    im, d, S = _big(size)
    for k in range(3):
        x = S * (.2 + k * .26)
        pts = [(x, S * .96), (x + S * .02, S * .6), (x + S * .12, S * .28), (x + S * .24, S * .08)]
        d.line(pts, fill=(30, 0, 50, 230), width=int(S * .12), joint="curve")
        d.line(pts, fill=(140, 60, 220, 255), width=int(S * .06), joint="curve")
        d.line(pts[1:], fill=(220, 180, 255, 255), width=int(S * .02), joint="curve")
    return _shrink(im, size)


def wrecking_ball(size=64):
    """A black iron wrecking ball on a heavy chain, a shine, rivets."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    for k in range(4):                                                                                  # chain
        y = S * (.0 + k * .08)
        d.ellipse([S * .44, y, S * .56, y + S * .1], outline=(150, 150, 160, 255), width=5)
    d.rectangle([S * .44, S * .3, S * .56, S * .38], fill=(90, 90, 100, 255), outline=OUT, width=4)
    d.ellipse([S * .14, S * .34, S * .86, S * .98], fill=(45, 45, 52, 255), outline=OUT, width=8)
    d.arc([S * .22, S * .42, S * .66, S * .86], 200, 260, fill=(150, 150, 165, 255), width=9)
    for x, y in ((.3, .66), (.7, .66), (.5, .9)):
        d.ellipse([S * (x - .02), S * (y - .02), S * (x + .02), S * (y + .02)], fill=(110, 110, 120, 255))
    return _shrink(im, size)


def teddy_bear(size=64, ripped=False):
    """A brown teddy bear sitting up, bow tie - or ripped open down the belly, stuffing bursting out."""
    im, d, S = _big(size)
    OUT = (50, 25, 10, 255)
    B, B_L = (170, 110, 60, 255), (220, 170, 120, 255)
    for x in (.24, .76):
        d.ellipse([S * (x - .1), S * .04, S * (x + .1), S * .24], fill=B, outline=OUT, width=6)       # ears
    d.ellipse([S * .26, S * .08, S * .74, S * .5], fill=B, outline=OUT, width=7)                        # head
    d.ellipse([S * .4, S * .3, S * .6, S * .44], fill=B_L, outline=OUT, width=4)
    d.ellipse([S * .46, S * .3, S * .54, S * .36], fill=OUT)
    for x in (.38, .62):
        d.ellipse([S * (x - .03), S * .2, S * (x + .03), S * .26], fill=OUT)
    d.ellipse([S * .2, S * .46, S * .8, S * .96], fill=B, outline=OUT, width=7)                         # body
    if ripped:
        d.polygon([(S * .4, S * .52), (S * .6, S * .52), (S * .64, S * .9), (S * .36, S * .9)], fill=(250, 250, 250, 255))
        for x, y in ((.3, .6), (.7, .66), (.5, .5), (.36, .84), (.66, .86)):
            d.ellipse([S * (x - .07), S * (y - .05), S * (x + .07), S * (y + .05)], fill=(250, 250, 250, 255), outline=(200, 200, 210, 255), width=3)
    else:
        d.ellipse([S * .34, S * .56, S * .66, S * .88], fill=B_L)
    d.polygon([(S * .38, S * .48), (S * .5, S * .52), (S * .38, S * .56)], fill=(220, 40, 40, 255))   # bow
    d.polygon([(S * .62, S * .48), (S * .5, S * .52), (S * .62, S * .56)], fill=(220, 40, 40, 255))
    return _shrink(im, size)


def seed_bag(size=64):
    """A bag of sunflower seeds: yellow-and-black bag, a big sunflower on it, seeds spilling from the top."""
    im, d, S = _big(size)
    OUT = (40, 30, 0, 255)
    _outline_poly(d, [(S * .14, S * .16), (S * .86, S * .16), (S * .9, S * .96), (S * .1, S * .96)], (40, 40, 45, 255), OUT, 8)
    d.polygon([(S * .14, S * .16), (S * .3, S * .06), (S * .5, S * .14), (S * .7, S * .06), (S * .86, S * .16)], fill=(30, 30, 34, 255), outline=OUT)
    import math
    for k in range(12):
        a = k * math.tau / 12
        x, y = S * (.5 + .2 * math.cos(a)), S * (.56 + .2 * math.sin(a))
        d.ellipse([x - S * .08, y - S * .08, x + S * .08, y + S * .08], fill=(255, 210, 30, 255))
    d.ellipse([S * .38, S * .44, S * .62, S * .68], fill=(110, 70, 30, 255), outline=OUT, width=4)
    for x in (.36, .5, .62):
        d.ellipse([S * (x - .03), S * .04, S * (x + .03), S * .12], fill=(60, 60, 60, 255), outline=(220, 220, 220, 255), width=2)
    return _shrink(im, size)


def seed_shell(n=16):
    """A sunflower seed: a striped teardrop (alpha only)."""
    def f(x, y):
        u, v = (x - 7.5) / 3.2, (y - 8) / 6
        return 1 if u * u + v * v <= 1 - (v * .3) else 0
    return _alpha(n, n, f)


def dump_truck(size=64, tipped=False):
    """A yellow dump truck facing right: the cab, big tires, the bed - level, or tipped up and pouring gravel."""
    im, d, S = _big(size)
    OUT = (40, 30, 0, 255)
    Y, Y_D = (250, 200, 30, 255), (200, 150, 10, 255)
    d.rectangle([S * .62, S * .36, S * .94, S * .74], fill=Y, outline=OUT, width=7)                     # cab
    d.rectangle([S * .74, S * .42, S * .9, S * .56], fill=(150, 200, 240, 255), outline=OUT, width=5)
    if tipped:
        bed = [(S * .02, S * .7), (S * .14, S * .26), (S * .64, S * .02), (S * .66, S * .5), (S * .3, S * .74)]
        _outline_poly(d, bed, Y_D, OUT, 7)
        for k in range(6):
            x = S * (.02 + k * .04)
            d.ellipse([x, S * (.62 + k % 2 * .06), x + S * .06, S * (.68 + k % 2 * .06)], fill=(140, 130, 120, 255), outline=OUT, width=3)
    else:
        _outline_poly(d, [(S * .04, S * .3), (S * .6, S * .3), (S * .6, S * .72), (S * .08, S * .72)], Y_D, OUT, 7)
        for k in range(5):
            d.ellipse([S * (.1 + k * .1), S * .22, S * (.18 + k * .1), S * .32], fill=(140, 130, 120, 255), outline=OUT, width=3)
    d.rectangle([S * .04, S * .72, S * .94, S * .78], fill=(60, 60, 66, 255), outline=OUT, width=4)
    for x in (.2, .44, .82):
        d.ellipse([S * (x - .09), S * .7, S * (x + .09), S * .96], fill=(30, 30, 34, 255), outline=OUT, width=6)
        d.ellipse([S * (x - .04), S * .78, S * (x + .04), S * .88], fill=(200, 200, 210, 255))
    return _shrink(im, size)


def gravel(n=16):
    """A lumpy rock (alpha only)."""
    def f(x, y):
        r = ((x - 7.5) ** 2 * 1.2 + (y - 8) ** 2) ** .5
        return 1 if r < 5 + ((x * 3 + y) % 3 == 0) else 0
    return _alpha(n, n, f)


def toaster(size=64, burnt=False):
    """A chrome two-slot toaster with the lever - and, when it's overcooked, two charred black slices shooting
    out with smoke."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    if burnt:
        for x in (.28, .52):
            d.rounded_rectangle([S * x, S * .04, S * (x + .2), S * .4], 8, fill=(40, 30, 25, 255), outline=OUT, width=5)
            d.line([(S * (x + .04), S * .12), (S * (x + .14), S * .3)], fill=(90, 60, 40, 255), width=4)
    d.rounded_rectangle([S * .1, S * .36, S * .9, S * .92], 16, fill=(200, 205, 215, 255), outline=OUT, width=8)
    for x in (.28, .52):
        d.rectangle([S * x, S * .36, S * (x + .2), S * .42], fill=OUT)
    d.line([(S * .18, S * .46), (S * .18, S * .84)], fill=(250, 250, 255, 255), width=6)
    d.rectangle([S * .88, S * .5, S * .96, S * .58], fill=(40, 40, 46, 255), outline=OUT, width=4)      # lever
    d.ellipse([S * .66, S * .72, S * .78, S * .84], fill=(255, 90, 40, 255) if burnt else (90, 90, 100, 255), outline=OUT, width=4)
    return _shrink(im, size)


def smoke_alarm(size=32):
    """A white smoke detector on the ceiling, its red light blinking."""
    im, d, S = _big(size)
    OUT = (80, 80, 90, 255)
    d.ellipse([S * .06, S * .2, S * .94, S * .8], fill=(245, 245, 245, 255), outline=OUT, width=6)
    d.ellipse([S * .26, S * .34, S * .74, S * .66], outline=(190, 190, 200, 255), width=4)
    d.ellipse([S * .44, S * .44, S * .56, S * .56], fill=(255, 30, 30, 255))
    return _shrink(im, size)


def energy_can(size=64):
    """A tall energy drink can: black with a neon green lightning bolt and ZOOM, beads of cold sweat (shown at
    1:1)."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rounded_rectangle([S * .28, S * .06, S * .72, S * .96], 10, fill=(25, 25, 30, 255), outline=OUT, width=7)
    d.rectangle([S * .3, S * .06, S * .7, S * .12], fill=(190, 195, 205, 255))
    d.polygon([(S * .54, S * .3), (S * .4, S * .58), (S * .5, S * .58), (S * .44, S * .86), (S * .62, S * .5), (S * .52, S * .5), (S * .6, S * .3)],
              fill=(120, 255, 60, 255), outline=OUT)
    for x, y in ((.34, .7), (.66, .4), (.36, .3)):
        d.ellipse([S * x, S * y, S * (x + .03), S * (y + .04)], fill=(220, 240, 255, 255))
    im = _shrink(im, size)
    return _texted(im, [("ZOOM", (32, 10))], (120, 255, 60, 255), (25, 25, 30, 255))


def nightcap(size=64):
    """A floppy striped nightcap with a pom-pom, and a speech-ish sleep bubble trailing Zs."""
    im, d, S = _big(size)
    OUT = (30, 30, 60, 255)
    cap = [(S * .1, S * .74), (S * .5, S * .2), (S * .92, S * .12), (S * .74, S * .4), (S * .9, S * .74)]
    _outline_poly(d, cap, (70, 90, 200, 255), OUT, 7)
    for k in range(3):
        d.line([(S * (.24 + k * .2), S * (.66 - k * .16)), (S * (.4 + k * .18), S * (.72 - k * .14))], fill=(250, 250, 250, 255), width=7)
    d.rectangle([S * .06, S * .72, S * .94, S * .84], fill=(250, 250, 250, 255), outline=OUT, width=6)
    d.ellipse([S * .84, S * .04, S * .98, S * .18], fill=(250, 250, 250, 255), outline=OUT, width=5)
    return _shrink(im, size)


def mumble_bubble(size=64):
    """A sleep-talk speech bubble full of nonsense: squiggles, a pizza slice, a heart and a question mark."""
    im, d, S = _big(size)
    OUT = (60, 60, 90, 255)
    d.rounded_rectangle([S * .06, S * .14, S * .94, S * .7], 18, fill=(250, 250, 255, 255), outline=OUT, width=7)
    d.polygon([(S * .2, S * .68), (S * .12, S * .9), (S * .36, S * .68)], fill=(250, 250, 255, 255), outline=OUT)
    d.line([(S * .2, S * .69), (S * .34, S * .69)], fill=(250, 250, 255, 255), width=8)
    d.polygon([(S * .18, S * .26), (S * .34, S * .3), (S * .22, S * .52)], fill=(250, 190, 60, 255), outline=OUT)  # pizza
    for x, y in ((.22, .32), (.26, .38)):
        d.ellipse([S * x, S * y, S * (x + .03), S * (y + .03)], fill=(220, 50, 40, 255))
    d.ellipse([S * .4, S * .3, S * .5, S * .4], fill=(240, 60, 110, 255))                              # heart
    d.ellipse([S * .48, S * .3, S * .58, S * .4], fill=(240, 60, 110, 255))
    d.polygon([(S * .4, S * .36), (S * .58, S * .36), (S * .49, S * .5)], fill=(240, 60, 110, 255))
    d.arc([S * .62, S * .26, S * .82, S * .44], 180, 400, fill=OUT, width=6)                          # ?
    d.line([(S * .74, S * .44), (S * .72, S * .52)], fill=OUT, width=6)
    d.ellipse([S * .7, S * .56, S * .74, S * .6], fill=OUT)
    return _shrink(im, size)


def trading_card(size=64, n=0):
    """A holo trading card face up: a shiny frame, a cartoon picture (a flame or a wave), stars for rarity."""
    im, d, S = _big(size)
    OUT = (30, 30, 40, 255)
    col = ((240, 90, 40, 255), (40, 140, 240, 255))[n % 2]
    d.rounded_rectangle([S * .2, S * .04, S * .8, S * .96], 8, fill=(250, 220, 70, 255), outline=OUT, width=7)
    d.rectangle([S * .26, S * .12, S * .74, S * .56], fill=(220, 240, 255, 255), outline=OUT, width=4)
    if n % 2 == 0:
        d.polygon([(S * .5, S * .18), (S * .64, S * .46), (S * .5, S * .52), (S * .36, S * .46)], fill=col)
    else:
        d.arc([S * .3, S * .2, S * .7, S * .6], 180, 360, fill=col, width=int(S * .08))
    d.rectangle([S * .26, S * .62, S * .74, S * .86], fill=(250, 245, 230, 255), outline=OUT, width=4)
    for k in range(3):
        x = S * (.36 + k * .14)
        d.polygon([(x, S * .68), (x + S * .02, S * .73), (x + S * .06, S * .74), (x + S * .02, S * .77), (x, S * .82),
                   (x - S * .02, S * .77), (x - S * .06, S * .74), (x - S * .02, S * .73)], fill=(250, 200, 40, 255))
    d.line([(S * .24, S * .1), (S * .4, S * .3)], fill=(255, 255, 255, 255), width=5)
    return _shrink(im, size)


def firework_mortar(size=64):
    """A fat red firework mortar tube on a base, the fuse sparking, ready to go."""
    im, d, S = _big(size)
    OUT = (40, 10, 10, 255)
    d.rectangle([S * .3, S * .2, S * .7, S * .86], fill=(220, 40, 40, 255), outline=OUT, width=7)
    for k in range(3):
        d.line([(S * .3, S * (.34 + k * .18)), (S * .7, S * (.34 + k * .18))], fill=(255, 220, 40, 255), width=6)
    d.ellipse([S * .3, S * .14, S * .7, S * .26], fill=(60, 40, 30, 255), outline=OUT, width=5)
    d.rectangle([S * .16, S * .84, S * .84, S * .96], fill=(120, 90, 50, 255), outline=OUT, width=6)
    d.line([(S * .7, S * .7), (S * .86, S * .6)], fill=(90, 70, 50, 255), width=5)
    d.polygon([(S * .86, S * .52), (S * .94, S * .6), (S * .86, S * .68), (S * .8, S * .6)], fill=(255, 240, 120, 255))
    return _shrink(im, size)


def recycling_bin(size=64):
    """A blue curbside recycling bin, lid flipped open, the three-arrow triangle on the front, junk poking out."""
    im, d, S = _big(size)
    OUT = (10, 30, 70, 255)
    d.polygon([(S * .14, S * .2), (S * .86, S * .2), (S * .8, S * .96), (S * .2, S * .96)], fill=(40, 100, 220, 255), outline=OUT)
    d.line([(S * .14, S * .2), (S * .86, S * .2), (S * .8, S * .96), (S * .2, S * .96), (S * .14, S * .2)], fill=OUT, width=8)
    d.polygon([(S * .1, S * .2), (S * .9, S * .2), (S * .96, S * .06), (S * .2, S * .02)], fill=(30, 80, 190, 255), outline=OUT)  # lid
    d.rectangle([S * .26, S * .1, S * .36, S * .24], fill=(220, 40, 40, 255), outline=OUT, width=3)    # a can
    d.rectangle([S * .54, S * .08, S * .7, S * .22], fill=(200, 160, 100, 255), outline=OUT, width=3)  # a box
    for k in range(3):                                                                                  # arrows
        import math
        a = k * math.tau / 3 - math.pi / 2
        x, y = S * (.5 + .14 * math.cos(a)), S * (.6 + .14 * math.sin(a))
        x2, y2 = S * (.5 + .14 * math.cos(a + 2.1)), S * (.6 + .14 * math.sin(a + 2.1))
        d.line([(x, y), (x2, y2)], fill=(250, 250, 250, 255), width=7)
        d.ellipse([x2 - S * .03, y2 - S * .03, x2 + S * .03, y2 + S * .03], fill=(250, 250, 250, 255))
    return _shrink(im, size)


def old_banana(size=32):
    """A half-eaten old banana, brown spots, flying out of the bin."""
    im, d, S = _big(size)
    OUT = (60, 40, 0, 255)
    d.arc([S * .1, S * -.2, S * .9, S * .8], 30, 150, fill=OUT, width=int(S * .22))
    d.arc([S * .1, S * -.2, S * .9, S * .8], 30, 150, fill=(240, 210, 60, 255), width=int(S * .14))
    for x, y in ((.3, .6), (.5, .68), (.66, .6)):
        d.ellipse([S * x, S * y, S * (x + .06), S * (y + .05)], fill=(120, 80, 20, 255))
    d.line([(S * .82, S * .48), (S * .9, S * .4)], fill=OUT, width=6)
    return _shrink(im, size)


def reacher_grabber(size=64, shut=False):
    """A reacher-grabber pole pointing right: the trigger handle, a long aluminum pole, rubber jaws open or
    pinched (on a berry)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.line([(S * .1, S * .5), (S * .82, S * .5)], fill=OUT, width=int(S * .07))
    d.line([(S * .1, S * .5), (S * .82, S * .5)], fill=(200, 205, 215, 255), width=int(S * .035))
    d.polygon([(S * .02, S * .44), (S * .16, S * .44), (S * .14, S * .74), (S * .06, S * .74)], fill=(40, 40, 46, 255), outline=OUT)  # grip
    d.line([(S * .16, S * .56), (S * .2, S * .66)], fill=(220, 40, 40, 255), width=6)                  # trigger
    gap = .04 if shut else .14
    for sgn in (-1, 1):
        d.line([(S * .8, S * .5), (S * .96, S * (.5 + sgn * gap))], fill=OUT, width=int(S * .06))
        d.line([(S * .8, S * .5), (S * .96, S * (.5 + sgn * gap))], fill=(240, 200, 40, 255), width=int(S * .03))
    if shut:
        d.ellipse([S * .9, S * .4, S * 1.0, S * .6], fill=(80, 70, 220, 255), outline=OUT, width=4)   # the berry
    return _shrink(im, size)


def berry(size=32):
    """A plump blue berry with a green leaf (the foe's snack)."""
    im, d, S = _big(size)
    OUT = (20, 20, 60, 255)
    d.ellipse([S * .14, S * .24, S * .86, S * .96], fill=(80, 70, 220, 255), outline=OUT, width=7)
    d.arc([S * .24, S * .32, S * .6, S * .6], 200, 260, fill=(180, 170, 255, 255), width=7)
    d.ellipse([S * .44, S * .04, S * .74, S * .3], fill=(60, 170, 60, 255), outline=(20, 70, 20, 255), width=5)
    return _shrink(im, size)


def snow_plow(size=64):
    """An orange city snow plow truck facing right, the big angled blade up front, the light bar on top."""
    im, d, S = _big(size)
    OUT = (40, 20, 0, 255)
    O = (250, 130, 20, 255)
    d.rectangle([S * .06, S * .4, S * .64, S * .76], fill=O, outline=OUT, width=7)                    # body
    d.rectangle([S * .44, S * .24, S * .7, S * .54], fill=O, outline=OUT, width=7)                    # cab
    d.rectangle([S * .5, S * .3, S * .66, S * .44], fill=(150, 200, 240, 255), outline=OUT, width=4)
    d.rectangle([S * .48, S * .18, S * .66, S * .24], fill=(255, 220, 40, 255), outline=OUT, width=4)  # light bar
    _outline_poly(d, [(S * .74, S * .34), (S * .98, S * .44), (S * .98, S * .86), (S * .72, S * .8)], (200, 205, 215, 255), OUT, 7)  # blade
    d.line([(S * .64, S * .64), (S * .74, S * .6)], fill=OUT, width=7)
    for x in (.18, .52):
        d.ellipse([S * (x - .1), S * .66, S * (x + .1), S * .94], fill=(30, 30, 34, 255), outline=OUT, width=6)
    return _shrink(im, size)


def tv_remote(size=64):
    """A black TV remote held up, a big glowing SLOW button (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rounded_rectangle([S * .3, S * .04, S * .7, S * .96], 12, fill=(35, 35, 40, 255), outline=OUT, width=7)
    d.ellipse([S * .44, S * .08, S * .56, S * .16], fill=(220, 40, 40, 255))
    for r in range(3):
        for c in range(3):
            d.ellipse([S * (.36 + c * .1), S * (.56 + r * .1), S * (.42 + c * .1), S * (.62 + r * .1)], fill=(110, 110, 120, 255))
    d.rounded_rectangle([S * .34, S * .24, S * .66, S * .46], 6, fill=(250, 200, 40, 255), outline=OUT, width=4)
    im = _shrink(im, size)
    return _texted(im, [("SLOW", (32, 18))], (40, 30, 0, 255), (255, 230, 120, 255))


def disposable_camera(size=64):
    """A yellow disposable camera: the flash bulb, lens, viewfinder, film wheel (pointing at you)."""
    im, d, S = _big(size)
    OUT = (40, 30, 0, 255)
    d.rounded_rectangle([S * .04, S * .26, S * .96, S * .8], 10, fill=(250, 200, 30, 255), outline=OUT, width=8)
    d.rectangle([S * .04, S * .5, S * .96, S * .62], fill=(30, 30, 30, 255))
    d.rectangle([S * .1, S * .3, S * .36, S * .46], fill=(230, 235, 245, 255), outline=OUT, width=5)    # flash
    d.ellipse([S * .44, S * .36, S * .74, S * .66], fill=(60, 60, 70, 255), outline=OUT, width=7)       # lens
    d.ellipse([S * .52, S * .44, S * .66, S * .58], fill=(140, 190, 240, 255))
    d.rectangle([S * .78, S * .3, S * .9, S * .4], fill=(80, 80, 90, 255), outline=OUT, width=4)        # viewfinder
    d.rectangle([S * .8, S * .18, S * .92, S * .26], fill=(60, 60, 66, 255), outline=OUT, width=4)      # wheel
    return _shrink(im, size)


def kettlebell(size=64):
    """A black kettlebell: the round body, the thick handle, 50 LB painted on (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.arc([S * .24, S * .04, S * .76, S * .56], 180, 360, fill=OUT, width=int(S * .14))
    d.arc([S * .24, S * .04, S * .76, S * .56], 180, 360, fill=(60, 60, 66, 255), width=int(S * .08))
    d.line([(S * .3, S * .3), (S * .3, S * .44)], fill=(60, 60, 66, 255), width=int(S * .08))
    d.line([(S * .7, S * .3), (S * .7, S * .44)], fill=(60, 60, 66, 255), width=int(S * .08))
    d.ellipse([S * .1, S * .34, S * .9, S * .98], fill=(40, 40, 46, 255), outline=OUT, width=8)
    d.arc([S * .2, S * .42, S * .6, S * .8], 200, 260, fill=(130, 130, 140, 255), width=8)
    im = _shrink(im, size)
    return _texted(im, [("50LB", (32, 40))], (255, 220, 40, 255), (40, 40, 46, 255))


def sweat_towel(size=64):
    """A gym towel slung over a shoulder, white with a red stripe."""
    im, d, S = _big(size)
    OUT = (60, 60, 70, 255)
    _outline_poly(d, [(S * .2, S * .1), (S * .56, S * .1), (S * .62, S * .9), (S * .4, S * .96), (S * .3, S * .5)], (250, 250, 250, 255), OUT, 7)
    d.line([(S * .24, S * .24), (S * .58, S * .24)], fill=(220, 40, 40, 255), width=7)
    d.line([(S * .32, S * .8), (S * .6, S * .8)], fill=(220, 40, 40, 255), width=7)
    return _shrink(im, size)


def teddy_strap(size=64):
    """The strap that was hiding in the teddy bear: a black compact pistol pointing right with an extended mag
    hanging out the grip, a tuft of stuffing still stuck to it."""
    im, d, S = _big(size)
    OUT = (8, 8, 10, 255)
    BL, BL_L = (45, 45, 52, 255), (120, 120, 132, 255)
    _outline_poly(d, [(S * .14, S * .3), (S * .9, S * .3), (S * .9, S * .46), (S * .14, S * .46)], BL, OUT, 8)   # slide
    for k in range(5):
        d.line([(S * (.2 + k * .04), S * .33), (S * (.2 + k * .04), S * .43)], fill=BL_L, width=3)           # serrations
    d.line([(S * .5, S * .34), (S * .86, S * .34)], fill=BL_L, width=4)
    d.rectangle([S * .84, S * .24, S * .88, S * .3], fill=BL, outline=OUT, width=3)                         # sight
    _outline_poly(d, [(S * .14, S * .46), (S * .4, S * .46), (S * .36, S * .76), (S * .14, S * .76)], (60, 60, 68, 255), OUT, 8)  # grip
    d.arc([S * .36, S * .42, S * .58, S * .62], 0, 180, fill=OUT, width=int(S * .04))                       # guard
    d.line([(S * .44, S * .48), (S * .47, S * .56)], fill=OUT, width=5)
    _outline_poly(d, [(S * .16, S * .76), (S * .34, S * .76), (S * .32, S * .98), (S * .18, S * .98)], (35, 35, 40, 255), OUT, 7)  # ext mag
    for x, y in ((.62, .5), (.7, .56)):                                                                      # stuffing
        d.ellipse([S * (x - .06), S * (y - .04), S * (x + .06), S * (y + .04)], fill=(250, 250, 250, 255), outline=(200, 200, 210, 255), width=3)
    return _shrink(im, size)


# ---- set 20 --------------------------------------------------------------------------------------------

def clown_nose(size=32):
    """A shiny red foam clown nose."""
    im, d, S = _big(size)
    OUT = (90, 0, 10, 255)
    d.ellipse([S * .1, S * .1, S * .9, S * .9], fill=(235, 30, 40, 255), outline=OUT, width=8)
    d.ellipse([S * .24, S * .2, S * .48, S * .42], fill=(255, 170, 170, 255))
    return _shrink(im, size)


def bike_horn(size=64):
    """A clown bike horn: a black rubber bulb on a brass trumpet pointing right."""
    im, d, S = _big(size)
    OUT = (40, 25, 0, 255)
    d.ellipse([S * .02, S * .3, S * .38, S * .7], fill=(30, 30, 34, 255), outline=OUT, width=7)
    d.arc([S * .08, S * .36, S * .26, S * .54], 200, 270, fill=(110, 110, 120, 255), width=6)
    _outline_poly(d, [(S * .36, S * .44), (S * .6, S * .44), (S * .96, S * .2), (S * .96, S * .8), (S * .6, S * .56), (S * .36, S * .56)],
                  (240, 190, 50, 255), OUT, 7)
    d.ellipse([S * .88, S * .2, S * 1.0, S * .8], fill=(255, 230, 140, 255), outline=OUT, width=6)
    return _shrink(im, size)


def card_reader(size=64, approved=False):
    """A countertop card reader: grey terminal, keypad, a swipe slot - its screen reading APPROVED in green
    once it's done (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.rounded_rectangle([S * .14, S * .06, S * .86, S * .96], 10, fill=(90, 92, 100, 255), outline=OUT, width=8)
    d.rectangle([S * .2, S * .14, S * .8, S * .36], fill=(40, 200, 90, 255) if approved else (30, 50, 40, 255), outline=OUT, width=5)
    for r in range(3):
        for c in range(3):
            d.rounded_rectangle([S * (.26 + c * .17), S * (.46 + r * .14), S * (.38 + c * .17), S * (.56 + r * .14)], 3, fill=(200, 200, 210, 255), outline=OUT, width=3)
    d.rectangle([S * .86, S * .3, S * .92, S * .7], fill=(30, 30, 34, 255), outline=OUT, width=3)        # the slot
    im = _shrink(im, size)
    if approved:
        _texted(im, [("APPROVED", (32, 13))], (255, 255, 255, 255), (20, 120, 50, 255))
    return im


def credit_card(size=32):
    """A shiny gold credit card mid-swipe, the chip, a stripe."""
    im, d, S = _big(size)
    OUT = (60, 40, 0, 255)
    d.rounded_rectangle([S * .04, S * .2, S * .96, S * .8], 8, fill=(240, 195, 60, 255), outline=OUT, width=6)
    d.rectangle([S * .12, S * .34, S * .3, S * .5], fill=(200, 200, 210, 255), outline=OUT, width=3)
    for k in range(4):
        d.rectangle([S * (.14 + k * .18), S * .62, S * (.26 + k * .18), S * .68], fill=OUT)
    d.line([(S * .4, S * .28), (S * .9, S * .28)], fill=(255, 245, 190, 255), width=5)
    return _shrink(im, size)


def punch_machine(size=64, maxed=False):
    """An arcade boxing machine: a red cabinet, the score display, the padded punching bag hanging out front -
    the display showing 999 once it's maxed (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (30, 10, 10, 255)
    d.rectangle([S * .2, S * .04, S * .8, S * .96], fill=(200, 30, 40, 255), outline=OUT, width=8)
    d.rectangle([S * .28, S * .1, S * .72, S * .3], fill=(20, 20, 24, 255), outline=OUT, width=5)
    d.line([(S * .5, S * .34), (S * .5, S * .44)], fill=(160, 160, 170, 255), width=6)
    d.ellipse([S * .3, S * .42, S * .7, S * .74], fill=(240, 220, 60, 255), outline=OUT, width=7)        # bag
    d.arc([S * .36, S * .46, S * .58, S * .64], 200, 260, fill=(255, 250, 200, 255), width=6)
    d.rectangle([S * .3, S * .82, S * .7, S * .9], fill=(250, 210, 40, 255), outline=OUT, width=4)
    im = _shrink(im, size)
    return _texted(im, [("999" if maxed else "000", (32, 9))], (255, 60, 40, 255) if maxed else (90, 30, 30, 255), (20, 20, 24, 255), font=GLYPHS)


def piggy_bank(size=64):
    """A pink piggy bank: round body, snout, curly tail, the coin slot on top."""
    im, d, S = _big(size)
    OUT = (110, 40, 70, 255)
    P, P_L = (250, 150, 180, 255), (255, 210, 225, 255)
    for x in (.3, .62):
        d.rectangle([S * x, S * .76, S * (x + .1), S * .94], fill=P, outline=OUT, width=5)               # legs
    d.ellipse([S * .14, S * .26, S * .86, S * .84], fill=P, outline=OUT, width=8)
    d.ellipse([S * .76, S * .44, S * .96, S * .64], fill=P, outline=OUT, width=6)                       # snout
    for y in (.5, .56):
        d.ellipse([S * .84, S * y, S * .88, S * (y + .03)], fill=OUT)
    d.polygon([(S * .6, S * .3), (S * .7, S * .14), (S * .74, S * .34)], fill=P, outline=OUT)           # ear
    d.ellipse([S * .64, S * .4, S * .7, S * .46], fill=OUT)
    d.rectangle([S * .38, S * .26, S * .54, S * .3], fill=OUT)                                          # coin slot
    d.arc([S * .02, S * .4, S * .18, S * .56], 90, 360, fill=OUT, width=5)                              # tail
    d.arc([S * .24, S * .34, S * .5, S * .56], 200, 260, fill=P_L, width=8)
    return _shrink(im, size)


def gold_coin(n=16):
    """A coin seen edge-tilted with a rim (alpha only)."""
    def f(x, y):
        r = ((x - 7.5) / 6) ** 2 + ((y - 7.5) / 6) ** 2
        return 1 if r <= 1 and (r > .55 or (abs(x - 7.5) < 1 and abs(y - 7.5) < 3.5)) else (.6 if r <= 1 else 0)
    return _alpha(n, n, f)


def clothes_iron(size=64):
    """A steam iron pointing right: a blue plastic body, the chrome sole plate, the handle, a dial, steam holes."""
    im, d, S = _big(size)
    OUT = (15, 25, 50, 255)
    _outline_poly(d, [(S * .04, S * .66), (S * .7, S * .66), (S * .98, S * .74), (S * .7, S * .84), (S * .04, S * .84)], (210, 215, 228, 255), OUT, 7)  # plate
    _outline_poly(d, [(S * .06, S * .66), (S * .2, S * .36), (S * .6, S * .3), (S * .9, S * .7)], (60, 120, 220, 255), OUT, 7)
    d.arc([S * .2, S * .1, S * .66, S * .5], 180, 330, fill=OUT, width=int(S * .09))                    # handle
    d.arc([S * .2, S * .1, S * .66, S * .5], 180, 330, fill=(40, 90, 190, 255), width=int(S * .05))
    d.ellipse([S * .3, S * .46, S * .42, S * .58], fill=(240, 240, 250, 255), outline=OUT, width=4)    # dial
    d.line([(S * .3, S * .4), (S * .5, S * .36)], fill=(150, 200, 255, 255), width=5)
    return _shrink(im, size)


def light_switch(size=64, on=False):
    """A big wall light switch plate: the toggle flipped down (off) or up (on), ON / OFF printed (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (60, 60, 60, 255)
    d.rounded_rectangle([S * .24, S * .04, S * .76, S * .96], 10, fill=(245, 240, 225, 255), outline=OUT, width=7)
    d.rectangle([S * .4, S * .32, S * .6, S * .68], fill=(200, 195, 180, 255), outline=OUT, width=5)
    if on:
        d.rectangle([S * .42, S * .24, S * .58, S * .5], fill=(250, 250, 245, 255), outline=OUT, width=5)
    else:
        d.rectangle([S * .42, S * .5, S * .58, S * .76], fill=(250, 250, 245, 255), outline=OUT, width=5)
    for y in (.1, .86):
        d.ellipse([S * .47, S * y, S * .53, S * (y + .05)], fill=OUT)
    im = _shrink(im, size)
    return _texted(im, [("ON" if on else "OFF", (32, 50 if not on else 6))], (40, 40, 40, 255), (245, 240, 225, 255))


def light_bulb(size=64):
    """A huge glowing light bulb: bright yellow glass, the filament, the screw base."""
    im, d, S = _big(size)
    OUT = (90, 70, 0, 255)
    d.ellipse([S * .14, S * .04, S * .86, S * .7], fill=(255, 250, 170, 255), outline=OUT, width=7)
    d.polygon([(S * .34, S * .6), (S * .66, S * .6), (S * .62, S * .76), (S * .38, S * .76)], fill=(255, 250, 170, 255))
    d.line([(S * .4, S * .56), (S * .44, S * .36), (S * .5, S * .48), (S * .56, S * .36), (S * .6, S * .56)], fill=(255, 150, 30, 255), width=5)
    for k in range(3):
        d.rectangle([S * .36, S * (.76 + k * .06), S * .64, S * (.8 + k * .06)], fill=(180, 180, 190, 255), outline=OUT, width=3)
    d.arc([S * .22, S * .1, S * .5, S * .4], 200, 260, fill=(255, 255, 255, 255), width=8)
    return _shrink(im, size)


def lego_brick(size=32):
    """A red toy building brick, the four studs on top - the most painful thing to step on."""
    im, d, S = _big(size)
    OUT = (90, 0, 10, 255)
    d.rectangle([S * .08, S * .4, S * .92, S * .88], fill=(225, 30, 35, 255), outline=OUT, width=7)
    for x in (.2, .4, .6, .8):
        d.rectangle([S * (x - .07), S * .26, S * (x + .07), S * .42], fill=(240, 60, 60, 255), outline=OUT, width=5)
    d.line([(S * .14, S * .48), (S * .86, S * .48)], fill=(255, 150, 150, 255), width=5)
    return _shrink(im, size)


def tied_laces(size=64):
    """Two big white high-top sneakers, side view, toes pointing apart - black soles, a red stripe, the
    tongue and lace holes - and their red laces knotted TOGETHER in a big bow between them."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    RED = (220, 40, 40, 255)
    for flip in (False, True):
        def X(x):
            return S * (1 - x) if flip else S * x
        upper = [(X(.02), S * .78), (X(.04), S * .56), (X(.18), S * .5), (X(.22), S * .22), (X(.4), S * .2),
                 (X(.44), S * .5), (X(.46), S * .78)]
        _outline_poly(d, upper, (250, 250, 250, 255), OUT, 6)
        d.rectangle([min(X(.02), X(.48)), S * .78, max(X(.02), X(.48)), S * .9], fill=(30, 30, 34, 255), outline=OUT, width=5)  # sole
        d.line([(X(.06), S * .66), (X(.42), S * .58)], fill=RED, width=7)                                   # the stripe
        for k in range(3):                                                                                  # lace holes
            y = S * (.28 + k * .08)
            d.ellipse([min(X(.37), X(.41)), y, max(X(.37), X(.41)), y + S * .04], fill=OUT)
        d.line([(X(.22), S * .22), (X(.18), S * .14)], fill=(250, 250, 250, 255), width=8)                 # the tongue
    d.line([(S * .4, S * .3), (S * .5, S * .44), (S * .6, S * .3)], fill=RED, width=6)                      # laces...
    d.line([(S * .4, S * .38), (S * .5, S * .44), (S * .6, S * .38)], fill=RED, width=6)
    for sx_ in (-1, 1):                                                                                     # ...the bow
        d.polygon([(S * .5, S * .44), (S * (.5 + sx_ * .12), S * .36), (S * (.5 + sx_ * .12), S * .52)], fill=RED, outline=OUT)
    d.ellipse([S * .46, S * .4, S * .54, S * .48], fill=RED, outline=OUT, width=3)
    return _shrink(im, size)


def pressure_gauge(size=64, red=False):
    """A boiler pressure gauge: brass ring, white dial with a green-yellow-red arc, the needle - pinned in the RED
    when it's about to blow."""
    import math
    im, d, S = _big(size)
    OUT = (50, 35, 0, 255)
    d.ellipse([S * .06, S * .06, S * .94, S * .94], fill=(220, 170, 50, 255), outline=OUT, width=8)
    d.ellipse([S * .16, S * .16, S * .84, S * .84], fill=(250, 250, 245, 255), outline=OUT, width=5)
    for a0, a1, col in ((150, 230, (60, 200, 80, 255)), (230, 300, (250, 210, 40, 255)), (300, 390, (230, 40, 40, 255))):
        d.arc([S * .22, S * .22, S * .78, S * .78], a0, a1, fill=col, width=int(S * .07))
    a = math.radians(380 if red else 190)
    d.line([(S * .5, S * .5), (S * (.5 + .28 * math.cos(a)), S * (.5 + .28 * math.sin(a)))], fill=OUT, width=6)
    d.ellipse([S * .45, S * .45, S * .55, S * .55], fill=OUT)
    d.rectangle([S * .44, S * .9, S * .56, S * 1.0], fill=(180, 140, 40, 255), outline=OUT, width=4)
    return _shrink(im, size)


def cardboard_lambo(size=64, fallen=False):
    """A life-size cardboard cutout of a yellow Lambo, propped up by a stick - or tipped over, showing the plain
    brown cardboard back and the stick. (The attacker's front.)"""
    im, d, S = _big(size)
    OUT = (40, 30, 0, 255)
    if not fallen:
        body = [(S * .02, S * .7), (S * .1, S * .52), (S * .4, S * .4), (S * .62, S * .4), (S * .96, S * .56), (S * .98, S * .72)]
        _outline_poly(d, body, (250, 200, 30, 255), OUT, 7)
        d.polygon([(S * .42, S * .44), (S * .6, S * .44), (S * .72, S * .54), (S * .36, S * .54)], fill=(40, 40, 50, 255))
        for x in (.22, .78):
            d.ellipse([S * (x - .09), S * .62, S * (x + .09), S * .8], fill=(30, 30, 34, 255), outline=OUT, width=5)
        d.line([(S * .06, S * .6), (S * .9, S * .62)], fill=(255, 240, 140, 255), width=4)
    else:
        _outline_poly(d, [(S * .02, S * .78), (S * .98, S * .78), (S * .98, S * .9), (S * .02, S * .9)], (190, 140, 80, 255), OUT, 7)
        d.line([(S * .5, S * .78), (S * .64, S * .6)], fill=(150, 100, 50, 255), width=6)               # the stick
        d.line([(S * .1, S * .82), (S * .9, S * .84)], fill=(160, 110, 60, 255), width=3)
    return _shrink(im, size)


def wall_safe(size=64, open_=False):
    """A steel wall safe with a combination dial - or swung open with a boxing glove on a spring shooting out
    (it was a prank safe)."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rectangle([S * .08, S * .1, S * .92, S * .9], fill=(120, 125, 135, 255), outline=OUT, width=8)
    if not open_:
        d.rectangle([S * .16, S * .18, S * .84, S * .82], fill=(150, 155, 165, 255), outline=OUT, width=5)
        d.ellipse([S * .34, S * .32, S * .66, S * .64], fill=(60, 60, 66, 255), outline=OUT, width=6)
        for k in range(8):
            import math
            a = k * math.tau / 8
            d.line([(S * (.5 + .12 * math.cos(a)), S * (.48 + .12 * math.sin(a))), (S * (.5 + .15 * math.cos(a)), S * (.48 + .15 * math.sin(a)))], fill=(220, 220, 230, 255), width=3)
        d.rectangle([S * .7, S * .64, S * .8, S * .74], fill=(200, 200, 210, 255), outline=OUT, width=3)
    else:
        d.rectangle([S * .16, S * .18, S * .84, S * .82], fill=(30, 30, 34, 255))
        for k in range(4):                                                                                # the spring
            d.arc([S * (.24 + k * .1), S * .4, S * (.38 + k * .1), S * .58], 0, 360, fill=(200, 200, 210, 255), width=4)
        d.ellipse([S * .62, S * .28, S * 1.0, S * .7], fill=(220, 30, 40, 255), outline=OUT, width=7)  # the glove
        d.ellipse([S * .66, S * .5, S * .82, S * .68], fill=(170, 20, 30, 255), outline=OUT, width=5)
    return _shrink(im, size)


def climbing_wall(size=64):
    """A rock-climbing wall panel: grey textured wall, bright colored holds all over it."""
    im, d, S = _big(size)
    OUT = (30, 30, 35, 255)
    d.rectangle([S * .1, S * .0, S * .9, S * 1.0], fill=(150, 145, 140, 255), outline=OUT, width=7)
    rnd = __import__("random").Random(7)
    cols = [(230, 40, 40, 255), (40, 120, 230, 255), (250, 200, 30, 255), (60, 190, 80, 255), (200, 80, 220, 255)]
    for k in range(14):
        x, y = S * rnd.uniform(.18, .82), S * rnd.uniform(.06, .94)
        r = S * rnd.uniform(.04, .07)
        d.ellipse([x - r, y - r * .8, x + r, y + r * .8], fill=cols[k % 5], outline=OUT, width=4)
    return _shrink(im, size)


def football(size=32):
    """A brown football with white laces (spinning spiral)."""
    im, d, S = _big(size)
    OUT = (50, 20, 5, 255)
    d.ellipse([S * .04, S * .24, S * .96, S * .76], fill=(150, 80, 35, 255), outline=OUT, width=7)
    d.line([(S * .34, S * .5), (S * .66, S * .5)], fill=(250, 250, 250, 255), width=5)
    for x in (.4, .48, .56):
        d.line([(S * x, S * .42), (S * x, S * .58)], fill=(250, 250, 250, 255), width=4)
    d.arc([S * .1, S * .3, S * .5, S * .5], 200, 260, fill=(220, 150, 100, 255), width=5)
    return _shrink(im, size)


def fog_machine(size=64):
    """A black concert fog machine with a nozzle, a power light and a little purple LED strip."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rounded_rectangle([S * .06, S * .44, S * .74, S * .88], 8, fill=(35, 35, 40, 255), outline=OUT, width=8)
    d.rectangle([S * .74, S * .56, S * .96, S * .7], fill=(70, 70, 78, 255), outline=OUT, width=6)       # nozzle
    for k in range(5):
        d.line([(S * (.14 + k * .1), S * .52), (S * (.14 + k * .1), S * .66)], fill=(80, 80, 90, 255), width=4)
    d.rectangle([S * .12, S * .74, S * .6, S * .8], fill=(170, 80, 255, 255))
    d.ellipse([S * .62, S * .5, S * .68, S * .56], fill=(255, 40, 40, 255))
    d.rectangle([S * .14, S * .88, S * .24, S * .96], fill=OUT)
    d.rectangle([S * .56, S * .88, S * .66, S * .96], fill=OUT)
    return _shrink(im, size)


def guitar_amp(size=64):
    """A stack guitar amp: black tolex, a gold-trim control strip with knobs, the speaker grille cloth, and a
    cable jack plugged in."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rounded_rectangle([S * .08, S * .08, S * .92, S * .94], 8, fill=(30, 30, 34, 255), outline=OUT, width=8)
    d.rectangle([S * .14, S * .14, S * .86, S * .3], fill=(220, 180, 70, 255), outline=OUT, width=5)
    for k in range(6):
        d.ellipse([S * (.2 + k * .11), S * .18, S * (.26 + k * .11), S * .26], fill=(30, 30, 34, 255))
    d.rectangle([S * .14, S * .36, S * .86, S * .88], fill=(90, 80, 70, 255), outline=OUT, width=5)
    for k in range(10):
        d.line([(S * .16, S * (.4 + k * .05)), (S * .84, S * (.4 + k * .05))], fill=(70, 62, 55, 255), width=2)
    d.line([(S * .2, S * .22), (S * .02, S * .4)], fill=OUT, width=6)                                  # the cable
    return _shrink(im, size)


def motel_pillow(size=64):
    """A sad flat motel pillow, a mystery stain on it, a ROOM tag."""
    im, d, S = _big(size)
    OUT = (90, 80, 70, 255)
    d.rounded_rectangle([S * .04, S * .34, S * .96, S * .82], 24, fill=(240, 236, 225, 255), outline=OUT, width=7)
    d.ellipse([S * .5, S * .5, S * .74, S * .66], fill=(210, 190, 140, 255))
    d.line([(S * .1, S * .4), (S * .9, S * .4)], fill=(255, 255, 250, 255), width=4)
    d.rectangle([S * .14, S * .58, S * .3, S * .72], fill=(250, 220, 90, 255), outline=OUT, width=3)
    return _shrink(im, size)


def bed_bug(n=16):
    """A little bed bug: oval body, six legs (alpha only)."""
    def f(x, y):
        body = ((x - 7.5) / 4) ** 2 + ((y - 8) / 5) ** 2 <= 1
        legs = any(abs(y - yy) < .7 and 1.5 <= x <= 13.5 for yy in (5, 8, 11)) and not body
        return 1 if body else (.7 if legs else 0)
    return _alpha(n, n, f)


def mop_bucket(size=64):
    """A yellow janitor mop bucket on wheels with the wringer press on top, dirty water sloshing."""
    im, d, S = _big(size)
    OUT = (50, 40, 0, 255)
    _outline_poly(d, [(S * .08, S * .44), (S * .92, S * .44), (S * .86, S * .86), (S * .14, S * .86)], (250, 200, 30, 255), OUT, 8)
    d.rectangle([S * .1, S * .44, S * .9, S * .52], fill=(140, 130, 90, 255))
    d.rectangle([S * .4, S * .18, S * .72, S * .46], fill=(240, 190, 20, 255), outline=OUT, width=6)    # the wringer
    d.line([(S * .72, S * .22), (S * .96, S * .04)], fill=(60, 60, 66, 255), width=8)                   # handle
    for x in (.2, .8):
        d.ellipse([S * (x - .06), S * .84, S * (x + .06), S * .96], fill=(30, 30, 34, 255), outline=OUT, width=4)
    return _shrink(im, size)


def neon_fanny_pack(size=64, open_=False):
    """A loud neon fanny pack: hot pink and lime, the strap, a gold zipper - unzipped with green bills fluttering
    out."""
    im, d, S = _big(size)
    OUT = (40, 10, 40, 255)
    d.line([(S * .0, S * .5), (S * 1.0, S * .5)], fill=(30, 30, 34, 255), width=int(S * .06))
    d.rounded_rectangle([S * .14, S * .36, S * .86, S * .82], 18, fill=(255, 60, 170, 255), outline=OUT, width=8)
    d.rectangle([S * .16, S * .62, S * .84, S * .7], fill=(150, 255, 60, 255))
    if open_:
        d.rectangle([S * .2, S * .32, S * .8, S * .42], fill=(30, 20, 30, 255))
        for k in range(4):
            x = S * (.24 + k * .14)
            _outline_poly(d, [(x, S * .36), (x + S * .08, S * .1 + k % 2 * S * .06), (x + S * .14, S * .14 + k % 2 * S * .06), (x + S * .06, S * .38)],
                          (110, 200, 100, 255), (30, 80, 30, 255), 4)
    d.line([(S * .2, S * .42), (S * .8, S * .42)], fill=(250, 210, 40, 255), width=5)
    return _shrink(im, size)


def money_leaf(n=16):
    """A little bill folded like a leaf (alpha only)."""
    def f(x, y):
        u, v = x - 7.5, y - 7.5
        inside = abs(u) <= 6.5 and abs(v) <= 3.5 and abs(u + v) < 8
        mark = abs(u) < 1.4 and abs(v) < 1.6
        return .6 if mark and inside else (1 if inside else 0)
    return _alpha(n, n, f)


def treadmill(size=64):
    """A treadmill seen side on: the black belt, the frame, the upright with the console and handles."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    _outline_poly(d, [(S * .02, S * .8), (S * .76, S * .74), (S * .8, S * .84), (S * .04, S * .92)], (40, 40, 46, 255), OUT, 7)
    for k in range(5):
        d.line([(S * (.1 + k * .14), S * .8), (S * (.14 + k * .14), S * .86)], fill=(90, 90, 100, 255), width=3)
    d.line([(S * .72, S * .76), (S * .86, S * .2)], fill=OUT, width=int(S * .06))
    d.line([(S * .72, S * .76), (S * .86, S * .2)], fill=(190, 195, 205, 255), width=int(S * .03))
    d.rounded_rectangle([S * .74, S * .1, S * .98, S * .26], 5, fill=(60, 60, 66, 255), outline=OUT, width=5)
    d.rectangle([S * .78, S * .14, S * .94, S * .2], fill=(80, 220, 120, 255))
    d.line([(S * .82, S * .32), (S * .5, S * .38)], fill=(190, 195, 205, 255), width=6)                # handle
    return _shrink(im, size)


def sleuth_glass(size=64):
    """A detective's magnifying glass: brass rim, glinting lens, wooden handle (pointing down-left)."""
    im, d, S = _big(size)
    OUT = (50, 30, 0, 255)
    d.line([(S * .38, S * .62), (S * .08, S * .94)], fill=OUT, width=int(S * .12))
    d.line([(S * .38, S * .62), (S * .08, S * .94)], fill=(150, 90, 40, 255), width=int(S * .07))
    d.ellipse([S * .3, S * .06, S * .94, S * .7], fill=(200, 230, 255, 140), outline=(220, 170, 50, 255), width=int(S * .07))
    d.ellipse([S * .3, S * .06, S * .94, S * .7], outline=OUT, width=5)
    d.arc([S * .4, S * .16, S * .7, S * .44], 200, 270, fill=(255, 255, 255, 255), width=7)
    return _shrink(im, size)


def deerstalker(size=64):
    """A tan plaid deerstalker hat with the ear flaps tied up."""
    im, d, S = _big(size)
    OUT = (60, 40, 20, 255)
    d.chord([S * .14, S * .2, S * .86, S * .84], 180, 360, fill=(190, 150, 100, 255), outline=OUT, width=7)
    d.polygon([(S * .04, S * .56), (S * .2, S * .5), (S * .2, S * .62)], fill=(170, 130, 85, 255), outline=OUT)   # brims
    d.polygon([(S * .96, S * .56), (S * .8, S * .5), (S * .8, S * .62)], fill=(170, 130, 85, 255), outline=OUT)
    for k in range(4):
        d.line([(S * (.24 + k * .16), S * .28), (S * (.24 + k * .16), S * .52)], fill=(130, 90, 50, 255), width=3)
    d.line([(S * .18, S * .42), (S * .82, S * .42)], fill=(130, 90, 50, 255), width=3)
    d.ellipse([S * .46, S * .16, S * .54, S * .24], fill=(130, 90, 50, 255))
    return _shrink(im, size)


def ficus(size=64):
    """A big potted ficus: a terracotta pot, a thin trunk, a bushy round crown of leaves (good for hiding behind)."""
    im, d, S = _big(size)
    OUT = (20, 50, 20, 255)
    _outline_poly(d, [(S * .3, S * .74), (S * .7, S * .74), (S * .64, S * .98), (S * .36, S * .98)], (200, 100, 50, 255), (80, 30, 10, 255), 7)
    d.line([(S * .5, S * .74), (S * .5, S * .5)], fill=(110, 70, 30, 255), width=8)
    for x, y, r in ((.5, .3, .26), (.28, .4, .18), (.72, .4, .18), (.38, .2, .16), (.64, .2, .16)):
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], fill=(60, 150, 60, 255), outline=OUT, width=6)
    for x, y in ((.4, .3), (.6, .36), (.5, .16), (.3, .44), (.7, .44)):
        d.ellipse([S * (x - .03), S * (y - .02), S * (x + .03), S * (y + .02)], fill=(140, 210, 120, 255))
    return _shrink(im, size)


def rock_candy(size=64):
    """A stick of rock candy: a chunky cluster of glowing magenta sugar crystals on a wooden stick."""
    im, d, S = _big(size)
    OUT = (80, 0, 60, 255)
    d.line([(S * .5, S * .6), (S * .5, S * .98)], fill=(200, 160, 100, 255), width=int(S * .05))
    for x, y, r in ((.5, .3, .16), (.36, .42, .13), (.64, .42, .13), (.44, .18, .11), (.58, .54, .12), (.4, .56, .1)):
        d.polygon([(S * x, S * (y - r)), (S * (x + r), S * y), (S * x, S * (y + r)), (S * (x - r), S * y)], fill=(240, 90, 220, 255), outline=OUT)
        d.polygon([(S * x, S * (y - r)), (S * (x + r * .4), S * (y - r * .3)), (S * x, S * y)], fill=(255, 200, 250, 255))
    return _shrink(im, size)


def milkshake(size=64):
    """The foe's big strawberry milkshake: a tall glass, a whipped cream swirl, a cherry - and a second bendy
    straw that ISN'T theirs."""
    im, d, S = _big(size)
    OUT = (90, 30, 50, 255)
    _outline_poly(d, [(S * .28, S * .34), (S * .72, S * .34), (S * .64, S * .94), (S * .36, S * .94)], (255, 170, 200, 255), OUT, 7)
    d.ellipse([S * .24, S * .2, S * .76, S * .42], fill=(255, 250, 245, 255), outline=OUT, width=5)     # whip
    d.ellipse([S * .44, S * .1, S * .56, S * .22], fill=(220, 20, 40, 255), outline=OUT, width=4)       # cherry
    d.line([(S * .4, S * .3), (S * .3, S * .04)], fill=(60, 160, 255, 255), width=7)                    # straw 1
    d.line([(S * .6, S * .3), (S * .7, S * .1), (S * .96, S * .08)], fill=(255, 220, 40, 255), width=7)  # the mooch's
    d.line([(S * .34, S * .5), (S * .36, S * .86)], fill=(255, 220, 230, 255), width=5)
    return _shrink(im, size)


def periscope(size=64):
    """A submarine-style periscope poking up: a green tube, the angled head with a glinting lens facing right."""
    im, d, S = _big(size)
    OUT = (15, 40, 20, 255)
    d.rectangle([S * .4, S * .3, S * .56, S * 1.0], fill=(80, 150, 80, 255), outline=OUT, width=7)
    _outline_poly(d, [(S * .36, S * .3), (S * .36, S * .06), (S * .76, S * .06), (S * .86, S * .2), (S * .6, S * .3)], (90, 170, 90, 255), OUT, 7)
    d.ellipse([S * .74, S * .08, S * .9, S * .24], fill=(160, 220, 255, 255), outline=OUT, width=5)
    d.ellipse([S * .78, S * .11, S * .83, S * .16], fill=(255, 255, 255, 255))
    for y in (.5, .7, .9):
        d.line([(S * .4, S * y), (S * .56, S * y)], fill=OUT, width=4)
    return _shrink(im, size)


def maple_leaf(n=16):
    """A pointy maple-ish leaf (alpha only)."""
    import math
    c = (n - 1) / 2

    def f(x, y):
        dx, dy = x - c, y - c
        r = (dx * dx + dy * dy) ** .5
        a = math.atan2(dy, dx)
        return 1 if r < 3.5 + 3.5 * abs(math.cos(a * 2.5)) ** 2 else 0
    return _alpha(n, n, f)


def exit_door(size=64, open_=False):
    """A door with a glowing green EXIT sign over it - shut, or open onto pure white light (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.rectangle([S * .22, S * .24, S * .78, S * .98], fill=(70, 70, 78, 255), outline=OUT, width=7)     # frame
    if open_:
        d.rectangle([S * .28, S * .3, S * .72, S * .98], fill=(255, 255, 240, 255))
        _outline_poly(d, [(S * .28, S * .3), (S * .14, S * .36), (S * .14, S * .92), (S * .28, S * .98)], (150, 110, 70, 255), OUT, 5)
    else:
        d.rectangle([S * .28, S * .3, S * .72, S * .98], fill=(170, 120, 75, 255), outline=OUT, width=5)
        d.rectangle([S * .58, S * .6, S * .66, S * .66], fill=(220, 200, 80, 255))
    d.rectangle([S * .26, S * .02, S * .74, S * .2], fill=(20, 140, 60, 255), outline=OUT, width=5)
    im = _shrink(im, size)
    return _texted(im, [("EXIT", (32, 3))], (255, 255, 255, 255), (20, 110, 50, 255), font=GLYPHS)


def mouthwash(size=64):
    """A big bottle of blue mouthwash, the cap off."""
    im, d, S = _big(size)
    OUT = (10, 30, 70, 255)
    d.rectangle([S * .42, S * .02, S * .58, S * .14], fill=(250, 250, 250, 255), outline=OUT, width=5)
    _outline_poly(d, [(S * .4, S * .14), (S * .6, S * .14), (S * .76, S * .3), (S * .76, S * .96), (S * .24, S * .96), (S * .24, S * .3)],
                  (60, 160, 240, 230), OUT, 7)
    d.rectangle([S * .3, S * .48, S * .7, S * .76], fill=(250, 250, 250, 255), outline=OUT, width=4)
    d.line([(S * .36, S * .56), (S * .64, S * .56)], fill=(60, 160, 240, 255), width=5)
    d.line([(S * .3, S * .34), (S * .3, S * .9)], fill=(200, 235, 255, 255), width=5)
    return _shrink(im, size)


def lawn_chair(size=64):
    """A folding lawn chair with the woven green-and-white straps, a beach umbrella stuck in the ground over it."""
    im, d, S = _big(size)
    OUT = (30, 30, 35, 255)
    d.line([(S * .82, S * .96), (S * .82, S * .24)], fill=(200, 200, 210, 255), width=6)                # umbrella pole
    d.chord([S * .5, S * .02, S * 1.0, S * .4], 180, 360, fill=(240, 60, 60, 255), outline=OUT, width=6)
    for k in range(3):
        d.pieslice([S * .5, S * .02, S * 1.0, S * .4], 180 + k * 60 + 20, 180 + k * 60 + 40, fill=(250, 250, 250, 255))
    for x0, x1 in ((.1, .36), (.36, .1)):                                                               # legs
        d.line([(S * x0, S * .6), (S * x1, S * .96)], fill=(190, 195, 205, 255), width=6)
    d.polygon([(S * .06, S * .34), (S * .3, S * .3), (S * .44, S * .62), (S * .14, S * .66)], fill=(80, 190, 110, 255), outline=OUT)
    for k in range(4):
        d.line([(S * (.1 + k * .06), S * (.36 + k * .07)), (S * (.34 + k * .03), S * (.32 + k * .08))], fill=(250, 250, 250, 255), width=4)
    d.rectangle([S * .14, S * .6, S * .48, S * .68], fill=(80, 190, 110, 255), outline=OUT, width=4)
    return _shrink(im, size)


def bff_half(size=64, right=False):
    """Half of a split BEST FRIENDS heart necklace on its chain: the left half says BE ST, the right FRI ENDS
    - a jagged break down the middle (shown at 1:1)."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (90, 60, 0, 255)
    G = (250, 205, 60, 255)
    if not right:
        pts = [(32, 22), (26, 14), (16, 14), (10, 22), (12, 32), (32, 52), (28, 44), (34, 38), (28, 30)]
    else:
        pts = [(32, 22), (38, 14), (48, 14), (54, 22), (52, 32), (32, 52), (28, 44), (34, 38), (28, 30)]
    d.polygon(pts, fill=G, outline=OUT)
    d.line([(14, 4), (20, 14)] if not right else [(50, 4), (44, 14)], fill=(200, 160, 40, 255), width=2)
    _texted(im, [("BE", (20, 20)), ("ST", (22, 28))] if not right else [("FRI", (44, 20)), ("ENDS", (42, 28))],
            (120, 60, 0, 255), (250, 205, 60, 255))
    return im


# ---- prototypes: the funnier redo (Rental Lambo, Scam Likely, Crossover) ---------------------------------

def tow_truck(size=64):
    """A red tow truck facing left: the cab, a light bar on top, the boom and hook hanging off the back (right)."""
    im, d, S = _big(size)
    OUT = (30, 10, 10, 255)
    R, R_D = (220, 40, 40, 255), (160, 20, 25, 255)
    d.rectangle([S * .04, S * .36, S * .36, S * .74], fill=R, outline=OUT, width=7)                    # cab
    d.rectangle([S * .08, S * .42, S * .26, S * .56], fill=(150, 200, 240, 255), outline=OUT, width=5)
    d.rectangle([S * .1, S * .3, S * .3, S * .36], fill=(255, 170, 20, 255), outline=OUT, width=4)       # light bar
    d.rectangle([S * .36, S * .5, S * .8, S * .74], fill=R_D, outline=OUT, width=7)                     # bed
    d.line([(S * .5, S * .5), (S * .84, S * .24)], fill=(60, 60, 66, 255), width=12)                    # boom
    d.line([(S * .84, S * .24), (S * .9, S * .56)], fill=(30, 30, 34, 255), width=4)                    # cable
    d.arc([S * .84, S * .52, S * .98, S * .66], 300, 200, fill=(170, 170, 180, 255), width=7)           # hook
    d.rectangle([S * .04, S * .72, S * .82, S * .78], fill=(60, 60, 66, 255), outline=OUT, width=4)
    for x in (.18, .66):
        d.ellipse([S * (x - .1), S * .68, S * (x + .1), S * .96], fill=(30, 30, 34, 255), outline=OUT, width=6)
        d.ellipse([S * (x - .04), S * .77, S * (x + .04), S * .87], fill=(200, 200, 210, 255))
    im = _shrink(im, size)
    return _texted(im, [("TOW", (35, 37))], (255, 255, 255, 255), (120, 10, 10, 255))


def lambo_hooked(size=64):
    """The Lambo with its nose yanked up on the tow hook (the left end high), tilted."""
    return cardboard_lambo(size).rotate(14, resample=Image.BICUBIC, center=(size * .5, size * .62))


def scam_phone(size=64, state="ring"):
    """A big smartphone. ring: SCAM / LIKELY on the screen, green and red buttons. declined: a red DECLINED
    screen. answered: a green CALL 0:01 screen (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (10, 10, 14, 255)
    d.rounded_rectangle([S * .14, S * .02, S * .86, S * .98], 18, fill=(30, 30, 36, 255), outline=OUT, width=8)
    scr = {"ring": (25, 30, 50, 255), "declined": (220, 40, 40, 255), "answered": (60, 190, 90, 255)}[state]
    d.rounded_rectangle([S * .19, S * .1, S * .81, S * .86], 8, fill=scr)
    if state == "ring":
        for x, c in ((.36, (60, 200, 90, 255)), (.64, (230, 50, 50, 255))):
            d.ellipse([S * (x - .07), S * .68, S * (x + .07), S * .82], fill=c, outline=OUT, width=4)
    im = _shrink(im, size)
    words = {"ring": [("SCAM", (32, 12)), ("LIKELY", (32, 20))],
             "declined": [("NOPE", (32, 26))],
             "answered": [("HELLO?", (32, 26))]}[state]
    fill = (255, 60, 50, 255) if state == "ring" else (255, 255, 255, 255)
    return _texted(im, words, fill)


def warranty_bubble(size=64):
    """A speech bubble with the robocall: WE BEEN / TRYIN TO / REACH YOU / UR CARS / WARRANTY (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.rounded_rectangle([S * .02, S * .02, S * .98, S * .8], 26, fill=(255, 255, 255, 255), outline=OUT, width=8)
    d.polygon([(S * .34, S * .76), (S * .12, S * .98), (S * .2, S * .74)], fill=(255, 255, 255, 255), outline=OUT)
    d.line([(S * .34, S * .76), (S * .12, S * .98), (S * .2, S * .74)], fill=OUT, width=7)
    im = _shrink(im, size)
    return _texted(im, [("WE BEEN TRYIN", (32, 5)), ("TO REACH YOU", (32, 13)), ("ABOUT UR CARS", (32, 21)),
                        ("WARRANTY", (32, 30))], (20, 20, 25, 255), (255, 255, 255, 255))


# ---- common-move redo: Pistol Whip, Double Tap, Licked It, Ricochet, Smooth Talk --------------------------

def click_bubble(size=32):
    """A small white speech bubble: *click* - the gun's empty (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.rounded_rectangle([S * .02, S * .14, S * .98, S * .7], 22, fill=(255, 255, 255, 255), outline=OUT, width=7)
    d.polygon([(S * .2, S * .66), (S * .1, S * .92), (S * .38, S * .68)], fill=(255, 255, 255, 255))
    d.line([(S * .2, S * .7), (S * .1, S * .92), (S * .38, S * .7)], fill=OUT, width=6)
    im = _shrink(im, size)
    return _texted(im, [("CLICK", (16, 9))], (20, 20, 25, 255), (255, 255, 255, 255))


def goose_egg(size=32):
    """A big shiny red lump - the bump on the head after a pistol whip."""
    im, d, S = _big(size)
    OUT = (90, 10, 20, 255)
    d.pieslice([S * .06, S * .3, S * .94, S * 1.3], 180, 360, fill=(240, 90, 100, 255), outline=OUT, width=8)   # a dome
    d.pieslice([S * .2, S * .44, S * .8, S * 1.16], 180, 360, fill=(250, 130, 135, 255))
    d.ellipse([S * .3, S * .42, S * .48, S * .56], fill=(255, 235, 235, 255))
    d.line([(S * .06, S * .8), (S * .94, S * .8)], fill=OUT, width=6)
    return _shrink(im, size)


def post_phone(size=64, liked=0, blocked=False):
    """A phone showing a post: a duck-lips selfie, a heart under it (filled red after a like, with +1/+2) - or
    the red U GOT BLOCKED screen (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (10, 10, 14, 255)
    d.rounded_rectangle([S * .16, S * .02, S * .84, S * .98], 18, fill=(30, 30, 36, 255), outline=OUT, width=8)
    d.rounded_rectangle([S * .21, S * .1, S * .79, S * .88], 8, fill=(220, 40, 40, 255) if blocked else (250, 250, 252, 255))
    if not blocked:
        d.rectangle([S * .25, S * .16, S * .75, S * .56], fill=(120, 180, 240, 255), outline=OUT, width=4)     # the pic
        d.ellipse([S * .38, S * .26, S * .62, S * .5], fill=(250, 210, 160, 255), outline=OUT, width=4)
        d.ellipse([S * .53, S * .36, S * .63, S * .44], fill=(240, 120, 140, 255), outline=OUT, width=3)      # duck lips
        for x in (.44, .53):
            d.ellipse([S * x, S * .32, S * (x + .04), S * .36], fill=OUT)
        hx, hy = S * .32, S * .66
        heart = [(hx, hy + S * .04), (hx - S * .06, hy - S * .02), (hx - S * .04, hy - S * .07), (hx, hy - S * .04),
                 (hx + S * .04, hy - S * .07), (hx + S * .06, hy - S * .02)]
        d.polygon(heart, fill=(240, 40, 70, 255) if liked else (250, 250, 252, 255), outline=OUT)
    im = _shrink(im, size)
    if blocked:
        return _texted(im, [("U GOT", (32, 20)), ("BLOCKED", (32, 28))], (255, 255, 255, 255))
    return _texted(im, [(f"+{liked}", (40, 39))], (240, 40, 70, 255), (255, 255, 255, 255)) if liked else im


def like_heart(size=64):
    """A big puffy red like-heart with a white outline and a shine."""
    im, d, S = _big(size)
    OUT = (255, 255, 255, 255)
    d.ellipse([S * .06, S * .14, S * .54, S * .6], fill=(235, 30, 60, 255))
    d.ellipse([S * .46, S * .14, S * .94, S * .6], fill=(235, 30, 60, 255))
    d.polygon([(S * .1, S * .48), (S * .9, S * .48), (S * .5, S * .92)], fill=(235, 30, 60, 255))
    d.arc([S * .06, S * .14, S * .54, S * .6], 140, 330, fill=OUT, width=8)
    d.arc([S * .46, S * .14, S * .94, S * .6], 210, 40, fill=OUT, width=8)
    d.line([(S * .1, S * .5), (S * .5, S * .92), (S * .9, S * .5)], fill=OUT, width=8)
    d.ellipse([S * .16, S * .22, S * .3, S * .36], fill=(255, 200, 210, 255))
    return _shrink(im, size)


def triple_scoop(size=64, licked=False):
    """A triple-scoop cone: chocolate, vanilla, strawberry, sprinkles on top - or with a big lick stripe slurped
    up through all three (wet shine)."""
    im, d, S = _big(size)
    OUT = (60, 30, 20, 255)
    d.polygon([(S * .3, S * .6), (S * .7, S * .6), (S * .5, S * .98)], fill=(220, 160, 80, 255), outline=OUT)
    d.line([(S * .3, S * .6), (S * .5, S * .98), (S * .7, S * .6)], fill=OUT, width=6)
    for k in range(3):
        d.line([(S * (.36 + k * .1), S * .62), (S * (.44 + k * .06), S * .86)], fill=(180, 120, 50, 255), width=4)
    for y, c in ((.46, (120, 70, 40, 255)), (.3, (250, 245, 225, 255)), (.14, (250, 150, 180, 255))):
        d.ellipse([S * .28, S * (y - .02), S * .72, S * (y + .2)], fill=c, outline=OUT, width=6)
    for x, y, c in ((.4, .18, (60, 160, 240)), (.5, .14, (250, 220, 40)), (.58, .2, (60, 200, 90)), (.46, .24, (240, 60, 60))):
        d.rectangle([S * x, S * y, S * (x + .05), S * (y + .02)], fill=c + (255,))
    if licked:                                                         # one long lick right up all three scoops
        for y, c in ((.46, (90, 50, 28, 255)), (.3, (225, 215, 190, 255)), (.14, (220, 115, 150, 255))):
            d.rounded_rectangle([S * .44, S * (y + .0), S * .58, S * (y + .17)], 10, fill=c)
        d.line([(S * .47, S * .16), (S * .47, S * .58)], fill=(255, 255, 255, 230), width=4)                  # wet shine
        d.rounded_rectangle([S * .64, S * .5, S * .7, S * .7], 6, fill=(250, 245, 225, 255), outline=OUT, width=3)  # a drip
    return _shrink(im, size)


def stop_sign(size=64, holed=False):
    """A red octagon STOP sign on a pole (shown at 1:1) - with a bullet hole once it's been pinged."""
    import math
    im, d, S = _big(size)
    OUT = (40, 10, 10, 255)
    d.rectangle([S * .46, S * .56, S * .54, S * .99], fill=(150, 150, 160, 255), outline=OUT, width=4)
    pts = [(S * .5 + S * .3 * math.cos(math.pi / 8 + k * math.pi / 4), S * .32 + S * .3 * math.sin(math.pi / 8 + k * math.pi / 4)) for k in range(8)]
    _outline_poly(d, pts, (220, 30, 35, 255), OUT, 7)
    pts2 = [(S * .5 + S * .25 * math.cos(math.pi / 8 + k * math.pi / 4), S * .32 + S * .25 * math.sin(math.pi / 8 + k * math.pi / 4)) for k in range(8)]
    d.line(pts2 + [pts2[0]], fill=(255, 255, 255, 255), width=4)
    if holed:
        d.ellipse([S * .58, S * .1, S * .7, S * .22], fill=(20, 20, 20, 255), outline=(200, 200, 200, 255), width=3)
    im = _shrink(im, size)
    return _texted(im, [("STOP", (32, 18))], (255, 255, 255, 255), (150, 10, 15, 255))


def metal_trashcan(size=64, dented=False):
    """A ribbed silver garbage can with its lid on - or dented in with the lid popped up off it."""
    im, d, S = _big(size)
    OUT = (30, 30, 36, 255)
    body = [(S * .2, S * .32), (S * .8, S * .32), (S * .74, S * .96), (S * .26, S * .96)]
    if dented:
        body = [(S * .2, S * .32), (S * .8, S * .32), (S * .74, S * .96), (S * .26, S * .96), (S * .34, S * .64), (S * .22, S * .5)]
    _outline_poly(d, body, (170, 175, 185, 255), OUT, 7)
    for k in range(4):
        y = S * (.42 + k * .13)
        d.line([(S * .36, y), (S * .7, y)], fill=(120, 125, 135, 255), width=5)
    d.line([(S * .3, S * .36), (S * .3, S * .46)], fill=(230, 235, 240, 255), width=6)
    if dented:
        d.ellipse([S * .2, S * .02, S * .86, S * .18], fill=(180, 185, 195, 255), outline=OUT, width=6)
    else:
        d.ellipse([S * .14, S * .2, S * .86, S * .36], fill=(180, 185, 195, 255), outline=OUT, width=6)
        d.rounded_rectangle([S * .42, S * .14, S * .58, S * .22], 5, fill=(150, 150, 160, 255), outline=OUT, width=4)
    return _shrink(im, size)


def street_pigeon(size=64):
    """A fat grey city pigeon mid-flap, flying left: green neck shine, orange eye, pink feet."""
    im, d, S = _big(size)
    OUT = (25, 25, 30, 255)
    d.ellipse([S * .2, S * .38, S * .78, S * .74], fill=(150, 155, 170, 255), outline=OUT, width=7)       # body
    d.polygon([(S * .74, S * .5), (S * .98, S * .44), (S * .98, S * .64), (S * .74, S * .64)], fill=(90, 95, 110, 255), outline=OUT)
    d.polygon([(S * .4, S * .46), (S * .66, S * .04), (S * .78, S * .1), (S * .62, S * .5)], fill=(170, 175, 190, 255), outline=OUT)  # wing
    d.line([(S * .5, S * .3), (S * .7, S * .1)], fill=(90, 95, 110, 255), width=6)
    d.ellipse([S * .04, S * .26, S * .34, S * .54], fill=(140, 145, 160, 255), outline=OUT, width=7)     # head
    d.arc([S * .16, S * .4, S * .4, S * .6], 30, 150, fill=(90, 190, 140, 255), width=8)
    d.ellipse([S * .12, S * .32, S * .2, S * .4], fill=(250, 140, 30, 255), outline=OUT, width=3)
    d.polygon([(S * .05, S * .4), (S * 0, S * .44), (S * .06, S * .46)], fill=(60, 60, 66, 255))
    for x in (.42, .54):
        d.line([(S * x, S * .72), (S * (x - .02), S * .84)], fill=(240, 130, 150, 255), width=6)
    return _shrink(im, size)


def long_rose(size=64):
    """A single long-stem red rose, held sideways - the smooth talker's prop."""
    im, d, S = _big(size)
    OUT = (40, 10, 15, 255)
    d.line([(S * .08, S * .78), (S * .66, S * .42)], fill=(50, 140, 50, 255), width=10)
    for x, y in ((.3, .64), (.46, .54)):
        d.ellipse([S * (x - .07), S * (y - .1), S * (x + .05), S * y], fill=(70, 170, 70, 255), outline=(20, 70, 20, 255), width=4)
    d.ellipse([S * .6, S * .18, S * .94, S * .52], fill=(210, 20, 40, 255), outline=OUT, width=7)
    d.arc([S * .66, S * .24, S * .88, S * .46], 180, 450, fill=(140, 0, 20, 255), width=6)
    d.arc([S * .72, S * .3, S * .82, S * .4], 0, 300, fill=(140, 0, 20, 255), width=5)
    return _shrink(im, size)


def line_bubble(lines, size=64):
    """A white speech bubble (tail bottom-left) holding a pickup line, up to 4 short lines (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    h = .22 + .12 * len(lines)
    top = .78 - h
    d.rounded_rectangle([S * .02, S * top, S * .98, S * .8], 26, fill=(255, 255, 255, 255), outline=OUT, width=8)
    d.polygon([(S * .34, S * .76), (S * .12, S * .98), (S * .2, S * .74)], fill=(255, 255, 255, 255))
    d.line([(S * .34, S * .78), (S * .12, S * .98), (S * .2, S * .78)], fill=OUT, width=7)
    im = _shrink(im, size)
    y0 = round(size * top) + 6
    return _texted(im, [(t, (32, y0 + k * 8)) for k, t in enumerate(lines)], (20, 20, 25, 255), (255, 255, 255, 255))


def zzz_drift(size=32):
    """A big blue Z with a white outline, for the foe dozing off."""
    im, d, S = _big(size)
    OUT = (255, 255, 255, 255)
    z = [(S * .18, S * .16), (S * .84, S * .16), (S * .84, S * .3), (S * .42, S * .7), (S * .84, S * .7), (S * .84, S * .86),
         (S * .16, S * .86), (S * .16, S * .72), (S * .58, S * .3), (S * .18, S * .3)]
    _outline_poly(d, z, (70, 120, 240, 255), OUT, 7)
    return _shrink(im, size)


# ---- set 20 redo, batch A: Fair One, Tax Punch, Chicken Wing, Ring Light, Big Mad -------------------------

def fight_bell(size=64):
    """A brass boxing-ring bell on its wooden mount, the little hammer mid-swing."""
    im, d, S = _big(size)
    OUT = (40, 25, 5, 255)
    d.rounded_rectangle([S * .08, S * .06, S * .92, S * .2], 6, fill=(140, 80, 40, 255), outline=OUT, width=6)    # mount
    d.rectangle([S * .46, S * .2, S * .54, S * .3], fill=(90, 90, 96, 255), outline=OUT, width=4)
    d.pieslice([S * .14, S * .26, S * .86, S * .98], 180, 360, fill=(240, 190, 50, 255), outline=OUT, width=8)
    d.line([(S * .14, S * .62), (S * .86, S * .62)], fill=OUT, width=8)
    d.arc([S * .24, S * .34, S * .6, S * .7], 200, 260, fill=(255, 245, 190, 255), width=8)                  # shine
    d.line([(S * .9, S * .3), (S * .7, S * .56)], fill=(110, 70, 40, 255), width=7)                           # hammer
    d.ellipse([S * .62, S * .5, S * .74, S * .62], fill=(60, 60, 66, 255), outline=OUT, width=4)
    return _shrink(im, size)


def paystub(size=64, net=False):
    """A pay stub: green PAY STUB header, ruled lines, and GROSS $1000 - or, after taxes, NET PAY $3.12 in
    red (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (30, 30, 34, 255)
    d.rectangle([S * .1, S * .04, S * .9, S * .96], fill=(250, 250, 245, 255), outline=OUT, width=7)
    d.rectangle([S * .1, S * .04, S * .9, S * .2], fill=(60, 160, 90, 255), outline=OUT, width=7)
    for k in range(4):
        y = S * (.3 + k * .08)
        d.line([(S * .18, y), (S * .82, y)], fill=(190, 190, 195, 255), width=4)
    d.line([(S * .18, S * .68), (S * .82, S * .68)], fill=OUT, width=4)
    im = _shrink(im, size)
    _texted(im, [("PAY STUB", (32, 4))], (255, 255, 255, 255), (20, 80, 40, 255))
    if net:
        return _texted(im, [("NET PAY", (32, 46)), ("$3.12", (32, 54))], (230, 40, 40, 255), (255, 255, 255, 255), font=GLYPHS)
    return _texted(im, [("GROSS", (32, 46)), ("$1000", (32, 54))], (30, 120, 60, 255), (255, 255, 255, 255), font=GLYPHS)


def chicken_wing(size=64):
    """A giant lemon pepper wing (a drumette): the fried meaty end, pepper specks, a lemon wedge, tapering to the
    bone with its double knob."""
    im, d, S = _big(size)
    OUT = (80, 40, 10, 255)
    d.line([(S * .6, S * .52), (S * .86, S * .5)], fill=(250, 245, 230, 255), width=int(S * .1))           # bone
    d.line([(S * .6, S * .52), (S * .86, S * .5)], fill=OUT, width=4)
    for y in (.42, .56):
        d.ellipse([S * .82, S * (y - .06), S * .96, S * (y + .07)], fill=(250, 245, 230, 255), outline=OUT, width=5)
    meat = [(S * .04, S * .5), (S * .1, S * .26), (S * .3, S * .16), (S * .5, S * .26), (S * .66, S * .44),
            (S * .66, S * .6), (S * .5, S * .74), (S * .3, S * .84), (S * .1, S * .76)]
    _outline_poly(d, meat, (220, 150, 55, 255), OUT, 8)
    d.line([(S * .14, S * .34), (S * .3, S * .24), (S * .46, S * .3)], fill=(250, 205, 110, 255), width=7)   # crispy shine
    for k in range(16):                                                          # lemon pepper
        x, y = .1 + (k * 37 % 50) / 100, .3 + (k * 23 % 44) / 100
        d.ellipse([S * x, S * y, S * (x + .025), S * (y + .025)], fill=(50, 40, 25, 255))
    d.pieslice([S * .16, S * .48, S * .46, S * .8], 200, 340, fill=(250, 230, 60, 255), outline=OUT, width=5)  # lemon wedge
    return _shrink(im, size)


def ranch_cup(size=32):
    """A little plastic cup of ranch, filled to the brim, the lid peeled back."""
    im, d, S = _big(size)
    OUT = (40, 40, 46, 255)
    d.polygon([(S * .12, S * .36), (S * .88, S * .36), (S * .76, S * .92), (S * .24, S * .92)], fill=(235, 240, 245, 255), outline=OUT)
    d.line([(S * .12, S * .36), (S * .24, S * .92), (S * .76, S * .92), (S * .88, S * .36)], fill=OUT, width=6)
    d.ellipse([S * .1, S * .28, S * .9, S * .44], fill=(250, 250, 240, 255), outline=OUT, width=6)
    d.ellipse([S * .3, S * .32, S * .44, S * .38], fill=(140, 200, 120, 255))                               # herbs
    d.ellipse([S * .58, S * .31, S * .66, S * .36], fill=(140, 200, 120, 255))
    d.polygon([(S * .7, S * .3), (S * .98, S * .02), (S * .98, S * .2)], fill=(250, 250, 255, 255), outline=OUT)   # the lid
    return _shrink(im, size)


def influencer_light(size=64, level="10%"):
    """An influencer ring light on a tripod, a phone clipped in the middle, the brightness readout on the base
    (10% / 50% / 9000% - the ring glows hotter each step) (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    glow = {"10%": (250, 240, 200, 255), "50%": (255, 250, 170, 255), "9000%": (255, 255, 255, 255)}[level]
    d.line([(S * .5, S * .62), (S * .5, S * .9)], fill=(60, 60, 66, 255), width=8)
    for x in (.24, .76):
        d.line([(S * .5, S * .86), (S * x, S * .99)], fill=(60, 60, 66, 255), width=7)
    if level != "10%":
        d.ellipse([S * .0, S * .0, S * 1.0, S * .66], fill=glow[:3] + (110,))
    d.ellipse([S * .14, S * .04, S * .86, S * .62], fill=(40, 40, 46, 255), outline=OUT, width=6)
    d.ellipse([S * .2, S * .1, S * .8, S * .56], fill=glow)
    d.ellipse([S * .32, S * .2, S * .68, S * .46], fill=(140, 200, 120, 0))
    d.ellipse([S * .32, S * .2, S * .68, S * .46], fill=(90, 160, 90, 255))                                    # the backdrop
    d.rounded_rectangle([S * .42, S * .2, S * .58, S * .46], 5, fill=(30, 30, 36, 255), outline=OUT, width=4)   # phone
    d.rounded_rectangle([S * .3, S * .66, S * .7, S * .8], 5, fill=(30, 30, 36, 255), outline=OUT, width=4)
    im = _shrink(im, size)
    return _texted(im, [(level, (32, 43))], (255, 220, 60, 255) if level != "9000%" else (255, 60, 40, 255), font=SMALL)


def flip_table(size=64):
    """A wooden folding table caught mid-flip: tabletop seen at an angle, the legs kicking up."""
    im, d, S = _big(size)
    OUT = (50, 25, 10, 255)
    top = [(S * .04, S * .5), (S * .62, S * .18), (S * .96, S * .38), (S * .38, S * .72)]
    _outline_poly(d, top, (180, 120, 60, 255), OUT, 8)
    d.line([(S * .12, S * .5), (S * .62, S * .24)], fill=(215, 160, 95, 255), width=6)
    for a, b in (((.16, .56), (.06, .9)), ((.36, .68), (.3, .98)), ((.86, .44), (.96, .78))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(140, 90, 40, 255), width=9)
    return _shrink(im, size)


# ---- set 20 redo, batch B: Clown On, Spike Strip, Got Laced, Inside Job, Parkour --------------------------

def rainbow_wig(size=64):
    """A big curly rainbow clown wig: puffs of red, orange, yellow, green, blue round a bald-cap middle."""
    im, d, S = _big(size)
    OUT = (30, 20, 30, 255)
    cols = [(240, 50, 50), (250, 150, 30), (250, 220, 40), (70, 200, 80), (60, 130, 240), (160, 70, 220)]
    pts = [(.12, .62), (.1, .42), (.2, .24), (.36, .14), (.52, .12), (.68, .16), (.82, .26), (.9, .44), (.88, .62)]
    for k, (x, y) in enumerate(pts):
        c = cols[k % len(cols)]
        d.ellipse([S * (x - .12), S * (y - .12), S * (x + .12), S * (y + .12)], fill=c + (255,), outline=OUT, width=6)
    return _shrink(im, size)                                                    # (open in the middle: their face shows)


def clown_shoes(size=64):
    """A pair of giant floppy red clown shoes with yellow laces, toes pointing out."""
    im, d, S = _big(size)
    OUT = (40, 10, 10, 255)
    for x0, flip in ((.0, True), (.5, False)):
        if flip:
            d.ellipse([S * .0, S * .5, S * .44, S * .86], fill=(220, 30, 40, 255), outline=OUT, width=7)
            d.ellipse([S * .26, S * .46, S * .5, S * .76], fill=(220, 30, 40, 255), outline=OUT, width=7)
            d.line([(S * .3, S * .56), (S * .44, S * .62)], fill=(250, 220, 40, 255), width=6)
            d.arc([S * .06, S * .56, S * .24, S * .7], 200, 290, fill=(255, 150, 150, 255), width=6)
        else:
            d.ellipse([S * .56, S * .5, S * 1.0, S * .86], fill=(220, 30, 40, 255), outline=OUT, width=7)
            d.ellipse([S * .5, S * .46, S * .74, S * .76], fill=(220, 30, 40, 255), outline=OUT, width=7)
            d.line([(S * .56, S * .62), (S * .7, S * .56)], fill=(250, 220, 40, 255), width=6)
            d.arc([S * .76, S * .56, S * .94, S * .7], 250, 340, fill=(255, 150, 150, 255), width=6)
    return _shrink(im, size)


def spike_strip(size=64):
    """A police spike strip unrolled flat: a black accordion strip with a row of silver spikes sticking up."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rectangle([S * .02, S * .58, S * .98, S * .72], fill=(40, 40, 46, 255), outline=OUT, width=6)
    for k in range(10):
        x = S * (.06 + k * .095)
        d.polygon([(x, S * .6), (x + S * .04, S * .36), (x + S * .08, S * .6)], fill=(210, 215, 225, 255), outline=OUT)
        d.line([(x + S * .02, S * .56), (x + S * .04, S * .42)], fill=(255, 255, 255, 255), width=3)
    d.rectangle([S * .02, S * .64, S * .98, S * .66], fill=(240, 200, 40, 255))
    return _shrink(im, size)


def pizza_scooter(size=64, flat=False):
    """A red delivery moped facing left with the PIZZA box on the back rack, nobody on it - or with both tires
    blown flat and the whole thing sagging."""
    im, d, S = _big(size)
    OUT = (30, 10, 10, 255)
    sag = .06 if flat else 0
    body = [(S * .12, S * (.56 + sag)), (S * .3, S * (.4 + sag)), (S * .7, S * (.44 + sag)), (S * .86, S * (.6 + sag)), (S * .2, S * (.66 + sag))]
    _outline_poly(d, body, (220, 40, 40, 255), OUT, 7)
    d.line([(S * .2, S * (.42 + sag)), (S * .14, S * (.2 + sag))], fill=(60, 60, 66, 255), width=8)          # handlebar
    d.line([(S * .06, S * (.2 + sag)), (S * .22, S * (.2 + sag))], fill=(30, 30, 34, 255), width=8)
    d.rectangle([S * .56, S * (.22 + sag), S * .94, S * (.42 + sag)], fill=(250, 245, 235, 255), outline=OUT, width=6)   # pizza box
    for x in (.2, .78):
        if flat:
            d.ellipse([S * (x - .12), S * .78, S * (x + .12), S * .9], fill=(30, 30, 34, 255), outline=OUT, width=6)
        else:
            d.ellipse([S * (x - .1), S * .64, S * (x + .1), S * .9], fill=(30, 30, 34, 255), outline=OUT, width=6)
            d.ellipse([S * (x - .04), S * .73, S * (x + .04), S * .81], fill=(200, 200, 210, 255))
    im = _shrink(im, size)
    return _texted(im, [("PIZZA", (48, round(size * (.25 + sag))))], (220, 40, 40, 255), (255, 255, 255, 255))


def pizza_hat(size=64):
    """A whole pepperoni pizza flopped over like a hat, cheese dripping down the sides."""
    im, d, S = _big(size)
    OUT = (90, 40, 10, 255)
    d.pieslice([S * .04, S * .2, S * .96, S * 1.1], 180, 360, fill=(230, 170, 80, 255), outline=OUT, width=8)   # crust
    d.pieslice([S * .12, S * .28, S * .88, S * 1.02], 180, 360, fill=(250, 220, 110, 255))
    for x, y in ((.3, .44), (.5, .36), (.68, .46), (.42, .56), (.6, .58)):
        d.ellipse([S * (x - .07), S * (y - .06), S * (x + .07), S * (y + .06)], fill=(200, 50, 40, 255), outline=OUT, width=3)
    for x in (.16, .4, .78):
        d.rounded_rectangle([S * x, S * .62, S * (x + .06), S * .84], 8, fill=(250, 220, 110, 255))
    return _shrink(im, size)


def flying_sneaker(size=32):
    """One white sneaker flying off, laces flapping."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    shoe = [(S * .06, S * .7), (S * .2, S * .36), (S * .5, S * .32), (S * .7, S * .5), (S * .96, S * .58), (S * .96, S * .74)]
    _outline_poly(d, shoe, (250, 250, 250, 255), OUT, 6)
    d.rectangle([S * .06, S * .7, S * .96, S * .82], fill=(220, 40, 40, 255), outline=OUT, width=5)
    d.line([(S * .4, S * .36), (S * .56, S * .12)], fill=(220, 40, 40, 255), width=5)
    d.line([(S * .46, S * .38), (S * .7, S * .2)], fill=(220, 40, 40, 255), width=5)
    return _shrink(im, size)


def safe_inside_man(size=64):
    """The wall safe swung open - and a guy in a black ski mask crouched INSIDE it, waving."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rectangle([S * .08, S * .1, S * .92, S * .9], fill=(120, 125, 135, 255), outline=OUT, width=8)
    d.rectangle([S * .16, S * .18, S * .84, S * .82], fill=(30, 30, 34, 255))
    d.ellipse([S * .3, S * .3, S * .66, S * .7], fill=(25, 25, 30, 255), outline=(80, 80, 90, 255), width=5)    # ski mask
    d.rectangle([S * .36, S * .42, S * .6, S * .5], fill=(240, 200, 160, 255))                                  # eye slot
    for x in (.4, .52):
        d.ellipse([S * x, S * .43, S * (x + .05), S * .49], fill=(255, 255, 255, 255))
        d.ellipse([S * (x + .015), S * .445, S * (x + .035), S * .475], fill=OUT)
    d.ellipse([S * .43, S * .56, S * .53, S * .64], fill=(240, 200, 160, 255))                                  # mouth hole
    d.ellipse([S * .66, S * .3, S * .8, S * .44], fill=(25, 25, 30, 255), outline=(80, 80, 90, 255), width=4)  # the wave
    d.rectangle([S * .9, S * .1, S * .99, S * .9], fill=(150, 155, 165, 255), outline=OUT, width=5)            # the door
    return _shrink(im, size)


def spring_glove(size=64):
    """A red boxing glove on the end of a long coiled spring, punching left."""
    im, d, S = _big(size)
    OUT = (40, 10, 10, 255)
    for k in range(6):
        x = S * (.44 + k * .09)
        d.arc([x, S * .38, x + S * .12, S * .62], 0, 360, fill=(200, 200, 210, 255), width=6)
    d.ellipse([S * .04, S * .24, S * .46, S * .76], fill=(220, 30, 40, 255), outline=OUT, width=8)
    d.ellipse([S * .3, S * .34, S * .5, S * .66], fill=(200, 20, 30, 255), outline=OUT, width=6)               # cuff
    d.arc([S * .1, S * .3, S * .3, S * .5], 180, 260, fill=(255, 150, 150, 255), width=7)
    return _shrink(im, size)


def blue_mailbox(size=64):
    """A blue USPS-style street mailbox: rounded top, the pull-down slot, four little legs."""
    im, d, S = _big(size)
    OUT = (10, 20, 50, 255)
    d.rounded_rectangle([S * .2, S * .1, S * .8, S * .82], 30, fill=(40, 80, 180, 255), outline=OUT, width=8)
    d.rectangle([S * .2, S * .4, S * .8, S * .82], fill=(40, 80, 180, 255))
    d.line([(S * .2, S * .4), (S * .2, S * .82), (S * .8, S * .82), (S * .8, S * .4)], fill=OUT, width=8)
    d.rounded_rectangle([S * .3, S * .26, S * .7, S * .38], 6, fill=(90, 130, 220, 255), outline=OUT, width=5)
    d.ellipse([S * .38, S * .5, S * .62, S * .7], fill=(250, 250, 250, 255), outline=OUT, width=4)
    for x in (.24, .7):
        d.rectangle([S * x, S * .82, S * (x + .06), S * .96], fill=(30, 30, 40, 255))
    return _shrink(im, size)


def fire_hydrant(size=64):
    """A red fire hydrant: domed cap, the side nozzles, the chained cap, a bolt on top."""
    im, d, S = _big(size)
    OUT = (50, 10, 10, 255)
    d.rectangle([S * .44, S * .04, S * .56, S * .14], fill=(200, 30, 30, 255), outline=OUT, width=4)
    d.pieslice([S * .26, S * .1, S * .74, S * .46], 180, 360, fill=(220, 40, 40, 255), outline=OUT, width=7)
    d.rectangle([S * .3, S * .28, S * .7, S * .86], fill=(220, 40, 40, 255), outline=OUT, width=7)
    for x in (.12, .7):
        d.rectangle([S * x, S * .44, S * (x + .18), S * .6], fill=(200, 30, 30, 255), outline=OUT, width=6)
    d.ellipse([S * .4, S * .5, S * .6, S * .7], fill=(240, 220, 60, 255), outline=OUT, width=5)
    d.rectangle([S * .22, S * .86, S * .78, S * .96], fill=(180, 25, 25, 255), outline=OUT, width=6)
    d.line([(S * .36, S * .34), (S * .36, S * .8)], fill=(255, 140, 140, 255), width=6)
    return _shrink(im, size)


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
    return _texted(im, [(level, (32, 33))], fill, font=SMALL)


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


# ---- set 20 redo, batch D1: Same Smoke, K9 Unit, Hide Out, Bling Beam, Mooch -------------------------------

def hoop_earrings(size=32):
    """A pair of big gold hoop earrings."""
    im, d, S = _big(size)
    OUT = (90, 60, 0, 255)
    for x in (.04, .52):
        d.ellipse([S * x, S * .2, S * (x + .44), S * .64], outline=OUT, width=12)
        d.ellipse([S * x, S * .2, S * (x + .44), S * .64], outline=(250, 200, 40, 255), width=7)
        d.arc([S * (x + .06), S * .26, S * (x + .2), S * .44], 160, 250, fill=(255, 250, 200, 255), width=4)
    return _shrink(im, size)


def rope_chain(size=64):
    """A thick gold rope chain coming off, swinging in a U."""
    im, d, S = _big(size)
    OUT = (90, 60, 0, 255)
    d.arc([S * .06, S * -.3, S * .94, S * .8], 20, 160, fill=OUT, width=18)
    d.arc([S * .06, S * -.3, S * .94, S * .8], 20, 160, fill=(250, 200, 40, 255), width=12)
    import math
    for k in range(14):                                                           # the rope twist
        a = math.radians(24 + k * 9.5)
        x, y = S * .5 + S * .44 * math.cos(a), S * .25 + S * .55 * math.sin(a)
        d.line([(x - 4, y - 5), (x + 4, y + 5)], fill=(255, 245, 190, 255), width=3)
    return _shrink(im, size)


def jelly_jar(size=64):
    """A tub of petroleum jelly, lid off, a big shiny scoop of it, a blue JELLY label - fight prep."""
    im, d, S = _big(size)
    OUT = (20, 30, 60, 255)
    d.rounded_rectangle([S * .2, S * .36, S * .8, S * .94], 10, fill=(235, 240, 250, 255), outline=OUT, width=7)
    d.rectangle([S * .2, S * .52, S * .8, S * .78], fill=(40, 90, 200, 255), outline=OUT, width=5)
    d.ellipse([S * .22, S * .26, S * .78, S * .44], fill=(250, 245, 215, 255), outline=OUT, width=6)
    d.ellipse([S * .38, S * .18, S * .6, S * .34], fill=(255, 250, 225, 255), outline=OUT, width=5)            # the scoop
    d.arc([S * .42, S * .2, S * .52, S * .28], 180, 300, fill=(255, 255, 255, 255), width=4)
    im = _shrink(im, size)
    return _texted(im, [("JELLY", (32, 37))], (255, 255, 255, 255), (20, 40, 100, 255))


def k9_dog(size=64, barking=False):
    """A police German shepherd facing left in a blue K9 vest - trotting, or sat up barking with its mouth open."""
    im, d, S = _big(size)
    OUT = (30, 20, 10, 255)
    TAN, BLK = (200, 140, 70, 255), (45, 35, 30, 255)
    if barking:
        d.ellipse([S * .4, S * .4, S * .86, S * .9], fill=TAN, outline=OUT, width=7)                               # sat body
        d.rectangle([S * .44, S * .46, S * .8, S * .66], fill=(40, 70, 170, 255), outline=OUT, width=5)           # vest
        d.line([(S * .5, S * .8), (S * .5, S * .96)], fill=TAN, width=12)
        head = (.28, .2)
    else:
        d.ellipse([S * .3, S * .4, S * .92, S * .72], fill=TAN, outline=OUT, width=7)
        d.rectangle([S * .4, S * .42, S * .76, S * .62], fill=(40, 70, 170, 255), outline=OUT, width=5)
        for x in (.36, .48, .76, .86):
            d.line([(S * x, S * .68), (S * (x - .02), S * .94)], fill=TAN, width=10)
        d.line([(S * .9, S * .5), (S * .99, S * .36)], fill=BLK, width=9)                                          # tail
        head = (.12, .3)
    hx, hy = head
    d.ellipse([S * hx, S * hy, S * (hx + .3), S * (hy + .26)], fill=TAN, outline=OUT, width=7)
    d.polygon([(S * (hx + .16), S * (hy + .02)), (S * (hx + .2), S * (hy - .14)), (S * (hx + .28), S * (hy + .06))], fill=BLK, outline=OUT)
    d.polygon([(S * (hx + .02), S * (hy + .1)), (S * (hx - .1), S * (hy + .16)), (S * (hx + .02), S * (hy + .22))], fill=TAN, outline=OUT)  # snout
    d.ellipse([S * (hx - .12), S * (hy + .12), S * (hx - .06), S * (hy + .18)], fill=OUT)
    d.ellipse([S * (hx + .08), S * (hy + .08), S * (hx + .13), S * (hy + .13)], fill=OUT)
    if barking:
        d.polygon([(S * (hx - .08), S * (hy + .2)), (S * (hx + .06), S * (hy + .22)), (S * (hx - .04), S * (hy + .32))], fill=(200, 40, 50, 255), outline=OUT)
    im = _shrink(im, size)
    return _texted(im, [("K9", (round(size * (.62 if barking else .58)), round(size * (.5 if barking else .46))))], (255, 255, 255, 255), (20, 30, 90, 255))


def sandwich(size=32):
    """A fat sub sandwich: bread, lettuce, tomato, cheese."""
    im, d, S = _big(size)
    OUT = (80, 45, 10, 255)
    d.rounded_rectangle([S * .04, S * .52, S * .96, S * .72], 12, fill=(220, 160, 80, 255), outline=OUT, width=5)
    d.rectangle([S * .06, S * .44, S * .94, S * .54], fill=(90, 190, 60, 255))
    d.rectangle([S * .08, S * .38, S * .92, S * .46], fill=(250, 210, 50, 255))
    for x in (.16, .42, .68):
        d.ellipse([S * x, S * .32, S * (x + .2), S * .42], fill=(220, 50, 40, 255), outline=OUT, width=3)
    d.rounded_rectangle([S * .04, S * .16, S * .96, S * .36], 12, fill=(230, 175, 90, 255), outline=OUT, width=5)
    for x in (.2, .45, .7):
        d.line([(S * x, S * .2), (S * (x + .08), S * .26)], fill=(255, 225, 160, 255), width=3)
    return _shrink(im, size)


def tiny_cactus(size=32, fallen=False):
    """A tiny potted cactus (way too small to hide behind) - or tipped over on its side."""
    im, d, S = _big(size)
    OUT = (20, 50, 20, 255)
    d.polygon([(S * .26, S * .66), (S * .74, S * .66), (S * .66, S * .96), (S * .34, S * .96)], fill=(200, 100, 50, 255), outline=OUT)
    d.rounded_rectangle([S * .38, S * .14, S * .62, S * .7], 12, fill=(70, 170, 70, 255), outline=OUT, width=5)
    d.rounded_rectangle([S * .16, S * .34, S * .3, S * .56], 8, fill=(70, 170, 70, 255), outline=OUT, width=4)
    d.line([(S * .28, S * .5), (S * .4, S * .5)], fill=(70, 170, 70, 255), width=8)
    for x, y in ((.44, .3), (.56, .42), (.46, .56), (.2, .4)):
        d.line([(S * x, S * y), (S * (x + .04), S * (y - .04))], fill=(255, 255, 220, 255), width=3)
    d.ellipse([S * .46, S * .06, S * .56, S * .16], fill=(250, 100, 160, 255), outline=OUT, width=3)            # a flower
    im = _shrink(im, size)
    return im.rotate(80, resample=Image.NEAREST, center=(size * .5, size * .9)) if fallen else im


def big_chain(size=64):
    """An iced-out chain: a heavy gold rope with a huge diamond-crusted $ medallion."""
    im, d, S = _big(size)
    OUT = (90, 60, 0, 255)
    d.arc([S * .08, S * -.36, S * .92, S * .5], 25, 155, fill=OUT, width=14)
    d.arc([S * .08, S * -.36, S * .92, S * .5], 25, 155, fill=(250, 200, 40, 255), width=9)
    d.ellipse([S * .26, S * .36, S * .74, S * .84], fill=(250, 200, 40, 255), outline=OUT, width=8)
    d.ellipse([S * .32, S * .42, S * .68, S * .78], fill=(200, 240, 255, 255), outline=(120, 160, 200, 255), width=4)
    for k in range(10):                                                           # the ice
        x, y = .36 + (k * 37 % 28) / 100, .46 + (k * 23 % 28) / 100
        d.ellipse([S * x, S * y, S * (x + .04), S * (y + .04)], fill=(255, 255, 255, 255))
    im = _shrink(im, size)
    return _texted(im, [("$", (32, 26))], (250, 200, 40, 255), (90, 60, 0, 255), font=GLYPHS)


def food_tray(size=64, burger=True):
    """A red fast-food tray: a carton of fries, a soda, and a burger (or just the empty wrapper once it's gone)."""
    im, d, S = _big(size)
    OUT = (40, 10, 10, 255)
    d.polygon([(S * .02, S * .7), (S * .98, S * .7), (S * .9, S * .86), (S * .1, S * .86)], fill=(200, 40, 40, 255), outline=OUT)
    d.rectangle([S * .72, S * .3, S * .9, S * .7], fill=(250, 250, 250, 255), outline=OUT, width=5)            # soda
    d.line([(S * .82, S * .3), (S * .86, S * .14)], fill=(220, 40, 40, 255), width=6)
    for k in range(5):                                                            # fries
        x = .1 + k * .05
        d.rectangle([S * x, S * .3, S * (x + .04), S * .5], fill=(250, 210, 60, 255), outline=OUT, width=2)
    d.polygon([(S * .06, S * .44), (S * .38, S * .44), (S * .34, S * .7), (S * .1, S * .7)], fill=(220, 40, 40, 255), outline=OUT)
    if burger:
        d.pieslice([S * .38, S * .3, S * .7, S * .62], 180, 360, fill=(220, 150, 60, 255), outline=OUT, width=5)
        d.rectangle([S * .38, S * .46, S * .7, S * .52], fill=(110, 60, 30, 255))
        d.rectangle([S * .38, S * .52, S * .7, S * .56], fill=(90, 190, 60, 255))
        d.rounded_rectangle([S * .38, S * .56, S * .7, S * .68], 6, fill=(220, 150, 60, 255), outline=OUT, width=5)
    else:
        d.polygon([(S * .4, S * .66), (S * .5, S * .56), (S * .62, S * .62), (S * .68, S * .68)], fill=(240, 230, 210, 255), outline=OUT)
    return _shrink(im, size)


def french_fry(size=32):
    """A single golden fry."""
    im, d, S = _big(size)
    OUT = (120, 70, 0, 255)
    d.rounded_rectangle([S * .4, S * .06, S * .6, S * .94], 6, fill=(250, 210, 60, 255), outline=OUT, width=6)
    d.line([(S * .46, S * .12), (S * .46, S * .5)], fill=(255, 245, 180, 255), width=4)
    return _shrink(im, size)


def burger(size=32):
    """A whole burger: sesame bun, lettuce, cheese, patty."""
    im, d, S = _big(size)
    OUT = (60, 30, 10, 255)
    d.pieslice([S * .06, S * .14, S * .94, S * .66], 180, 360, fill=(220, 150, 60, 255), outline=OUT, width=6)
    for x, y in ((.3, .26), (.5, .22), (.66, .3)):
        d.ellipse([S * x, S * y, S * (x + .06), S * (y + .04)], fill=(255, 245, 210, 255))
    d.rectangle([S * .06, S * .4, S * .94, S * .48], fill=(90, 190, 60, 255))
    d.polygon([(S * .06, S * .48), (S * .94, S * .48), (S * .8, S * .56), (S * .2, S * .56)], fill=(250, 200, 40, 255))
    d.rounded_rectangle([S * .08, S * .54, S * .92, S * .68], 6, fill=(110, 60, 30, 255), outline=OUT, width=4)
    d.rounded_rectangle([S * .06, S * .68, S * .94, S * .84], 8, fill=(220, 150, 60, 255), outline=OUT, width=5)
    return _shrink(im, size)


# ---- set 20 redo, batch D2: Peep Game, Zaza Storm, Dip Out, Spit Bars, Post Up -----------------------------

def playbook_clipboard(size=64):
    """A clipboard with the foe's game plan on it: PLAN: / HIT EM, an X-and-O doodle (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 25, 10, 255)
    d.rounded_rectangle([S * .14, S * .06, S * .86, S * .96], 8, fill=(160, 110, 60, 255), outline=OUT, width=7)
    d.rectangle([S * .22, S * .14, S * .78, S * .9], fill=(250, 250, 245, 255), outline=OUT, width=4)
    d.rounded_rectangle([S * .36, S * .02, S * .64, S * .14], 5, fill=(190, 190, 200, 255), outline=OUT, width=5)
    d.line([(S * .3, S * .7), (S * .4, S * .8)], fill=(220, 40, 40, 255), width=5)                          # X
    d.line([(S * .4, S * .7), (S * .3, S * .8)], fill=(220, 40, 40, 255), width=5)
    d.ellipse([S * .56, S * .68, S * .7, S * .82], outline=(40, 80, 200, 255), width=5)                      # O
    d.line([(S * .42, S * .75), (S * .54, S * .75)], fill=(40, 40, 46, 255), width=3)
    im = _shrink(im, size)
    return _texted(im, [("PLAN:", (32, 14)), ("HIT EM", (32, 26))], (20, 20, 25, 255), (250, 250, 245, 255))


def weather_map(size=64, level="LIGHT"):
    """A TV weather report: a map with a green blob over the hood, and a banner reading LIGHT / MODERATE /
    SEVERE (the blob grows and goes red) (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    col = {"LIGHT": (90, 200, 90, 255), "MODERATE": (240, 200, 40, 255), "SEVERE": (230, 40, 40, 255)}[level]
    grow = {"LIGHT": .1, "MODERATE": .18, "SEVERE": .28}[level]
    d.rounded_rectangle([S * .02, S * .04, S * .98, S * .9], 10, fill=(40, 40, 46, 255), outline=OUT, width=8)
    d.rectangle([S * .08, S * .1, S * .92, S * .66], fill=(90, 150, 230, 255))
    d.polygon([(S * .14, S * .6), (S * .2, S * .2), (S * .5, S * .14), (S * .86, S * .26), (S * .8, S * .62)], fill=(170, 200, 120, 255))
    d.ellipse([S * (.5 - grow), S * (.38 - grow * .8), S * (.5 + grow), S * (.38 + grow * .8)], fill=col[:3] + (200,))
    d.rectangle([S * .08, S * .66, S * .92, S * .84], fill=col, outline=OUT, width=4)
    d.rectangle([S * .44, S * .9, S * .56, S * .98], fill=(40, 40, 46, 255))
    im = _shrink(im, size)
    words = [(level, (32, 44))] + ([("ZAZA", (32, 6))] if level == "SEVERE" else [])
    return _texted(im, words, (255, 255, 255, 255), (20, 20, 25, 255))


def window_pane(size=64, broken=False):
    """A wooden window frame with four panes - or smashed out, jagged shards left in the frame."""
    im, d, S = _big(size)
    OUT = (50, 30, 15, 255)
    d.rectangle([S * .1, S * .08, S * .9, S * .92], fill=(140, 90, 50, 255), outline=OUT, width=7)
    for x0, y0 in ((.16, .14), (.52, .14), (.16, .52), (.52, .52)):
        d.rectangle([S * x0, S * y0, S * (x0 + .32), S * (y0 + .34)], fill=(170, 220, 250, 255) if not broken else (40, 40, 50, 255), outline=OUT, width=4)
        if broken:
            d.polygon([(S * x0, S * y0), (S * (x0 + .12), S * y0), (S * x0, S * (y0 + .14))], fill=(170, 220, 250, 255))
            d.polygon([(S * (x0 + .32), S * (y0 + .34)), (S * (x0 + .2), S * (y0 + .34)), (S * (x0 + .32), S * (y0 + .2))], fill=(170, 220, 250, 255))
        else:
            d.line([(S * (x0 + .06), S * (y0 + .24)), (S * (x0 + .2), S * (y0 + .06))], fill=(255, 255, 255, 255), width=4)
    return _shrink(im, size)


def jail_bar(size=64):
    """One heavy steel jail bar, flying."""
    im, d, S = _big(size)
    OUT = (20, 20, 26, 255)
    d.rounded_rectangle([S * .42, S * .02, S * .58, S * .98], 8, fill=(150, 155, 170, 255), outline=OUT, width=6)
    d.line([(S * .47, S * .08), (S * .47, S * .9)], fill=(230, 235, 245, 255), width=5)
    return _shrink(im, size)


def jail_cell(size=64):
    """The front of a jail cell: a steel frame and six bars (the foe shows through behind them)."""
    im, d, S = _big(size)
    OUT = (20, 20, 26, 255)
    d.rectangle([S * .04, S * .04, S * .96, S * .14], fill=(110, 115, 130, 255), outline=OUT, width=6)
    d.rectangle([S * .04, S * .86, S * .96, S * .96], fill=(110, 115, 130, 255), outline=OUT, width=6)
    for k in range(6):
        x = .1 + k * .158
        d.rectangle([S * x, S * .14, S * (x + .06), S * .86], fill=(150, 155, 170, 255), outline=OUT, width=4)
        d.line([(S * (x + .02), S * .16), (S * (x + .02), S * .84)], fill=(230, 235, 245, 255), width=3)
    d.rectangle([S * .4, S * .44, S * .6, S * .58], fill=(200, 170, 60, 255), outline=OUT, width=4)           # the lock
    return _shrink(im, size)


def cooler_box(size=64):
    """A red and white picnic cooler, lid cracked, ice and a soda can peeking out."""
    im, d, S = _big(size)
    OUT = (40, 10, 10, 255)
    d.rounded_rectangle([S * .08, S * .4, S * .92, S * .9], 10, fill=(220, 40, 40, 255), outline=OUT, width=7)
    d.rounded_rectangle([S * .06, S * .26, S * .94, S * .42], 8, fill=(250, 250, 250, 255), outline=OUT, width=7)
    d.rectangle([S * .4, S * .5, S * .6, S * .58], fill=(250, 250, 250, 255), outline=OUT, width=4)             # handle
    for x in (.2, .36):
        d.rectangle([S * x, S * .16, S * (x + .12), S * .28], fill=(200, 235, 255, 255), outline=(120, 160, 200, 255), width=3)
    d.rectangle([S * .6, S * .08, S * .74, S * .28], fill=(40, 120, 220, 255), outline=OUT, width=4)            # a can
    return _shrink(im, size)


def bbq_grill(size=64):
    """A black kettle grill on its legs, lid propped, burgers and dogs sizzling, smoke rolling up."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    for a, b in (((.3, .62), (.18, .96)), ((.7, .62), (.82, .96)), ((.5, .66), (.5, .96))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(60, 60, 66, 255), width=7)
    d.chord([S * .1, S * .3, S * .9, S * .8], 0, 180, fill=(40, 40, 46, 255), outline=OUT, width=7)              # the bowl
    d.ellipse([S * .66, S * .02, S * .98, S * .34], fill=(40, 40, 46, 255), outline=OUT, width=6)              # the lid, propped
    d.line([(S * .12, S * .55), (S * .88, S * .55)], fill=(150, 150, 160, 255), width=4)
    for x in (.2, .44):
        d.ellipse([S * x, S * .44, S * (x + .18), S * .56], fill=(110, 60, 30, 255), outline=OUT, width=4)       # burgers
    d.rounded_rectangle([S * .64, S * .46, S * .82, S * .54], 6, fill=(200, 90, 60, 255), outline=OUT, width=3)  # a dog
    for x in (.3, .5):
        d.ellipse([S * x, S * .18, S * (x + .14), S * .32], fill=(220, 220, 225, 180))
    return _shrink(im, size)


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


# ---- set 23, batch 1: Got Milk, Half Off, Crop Duster, Death Stare, Catch a Fade -----------------------------

def milk_gallon(size=64, level="full", label=True):
    """A plastic gallon jug of whole milk: blue cap, the handle up top, a red label reading MILK (shown at 1:1).
    level: full / half / empty (the clear plastic shows how much is left)."""
    im, d, S = _big(size)
    OUT = (30, 40, 70, 255)
    milk = {"full": .28, "half": .6, "empty": 1.1}[level]
    d.rounded_rectangle([S * .2, S * .22, S * .8, S * .96], 22, fill=(225, 232, 240, 150), outline=OUT, width=8)   # the jug
    if milk < 1:
        d.rounded_rectangle([S * .2, S * milk, S * .8, S * .96], 22, fill=(252, 252, 255, 255), outline=OUT, width=8)
    d.polygon([(S * .3, S * .22), (S * .42, S * .1), (S * .58, S * .1), (S * .58, S * .22)], fill=(230, 235, 242, 200))
    d.line([(S * .3, S * .22), (S * .42, S * .1)], fill=OUT, width=7)
    d.rounded_rectangle([S * .56, S * .1, S * .82, S * .34], 10, outline=OUT, width=9)                             # handle
    d.rounded_rectangle([S * .38, S * .02, S * .56, S * .12], 4, fill=(40, 110, 230, 255), outline=OUT, width=6)  # cap
    if label:
        d.rectangle([S * .2, S * .5, S * .8, S * .76], fill=(220, 40, 40, 255), outline=OUT, width=6)
    d.line([(S * .27, S * .3), (S * .27, S * .44)], fill=(255, 255, 255, 255), width=6)                           # shine
    im = _shrink(im, size)
    return _texted(im, [("MILK", (32, 35))], (255, 255, 255, 255), (120, 10, 10, 255)) if label else im


def milk_chug(size=64):
    """The jug tipped right over (no text: tilted), milk glugging out the spout to the left."""
    im = milk_gallon(size, "half", label=False).rotate(125, resample=Image.BICUBIC, expand=False)
    d = ImageDraw.Draw(im)
    for k, (x, y) in enumerate(((10, 46), (6, 54), (12, 58))):
        d.ellipse([x, y, x + 6 - k, y + 6 - k], fill=(252, 252, 255, 255), outline=(150, 160, 190, 255))
    return im


def price_gun(size=64):
    """An orange price labeler gun: a sticker roll on top, the trigger, a fresh sticker poking out the nose."""
    im, d, S = _big(size)
    OUT = (40, 20, 5, 255)
    d.polygon([(S * .08, S * .3), (S * .74, S * .3), (S * .84, S * .44), (S * .74, S * .56), (S * .08, S * .56)],
              fill=(250, 140, 30, 255), outline=OUT)
    d.line([(S * .08, S * .3), (S * .74, S * .3), (S * .84, S * .44), (S * .74, S * .56), (S * .08, S * .56), (S * .08, S * .3)], fill=OUT, width=7)
    d.ellipse([S * .2, S * .06, S * .52, S * .38], fill=(250, 250, 245, 255), outline=OUT, width=7)              # roll
    d.ellipse([S * .32, S * .18, S * .4, S * .26], fill=(120, 120, 130, 255))
    d.rounded_rectangle([S * .14, S * .54, S * .34, S * .96], 8, fill=(60, 60, 66, 255), outline=OUT, width=7)  # grip
    d.rounded_rectangle([S * .4, S * .56, S * .62, S * .82], 8, fill=(250, 140, 30, 255), outline=OUT, width=7)  # trigger
    d.rectangle([S * .82, S * .36, S * .98, S * .5], fill=(255, 255, 255, 255), outline=OUT, width=4)             # sticker
    d.line([(S * .14, S * .36), (S * .7, S * .36)], fill=(255, 200, 120, 255), width=5)
    return _shrink(im, size)


def price_sticker(text, size=32, fill=(255, 230, 60, 255), ink=(20, 20, 25, 255)):
    """A small price sticker (rounded rectangle) with one word on it (shown at 1:1)."""
    im, d, S = _big(size)
    d.rounded_rectangle([S * .04, S * .22, S * .96, S * .78], 16, fill=fill, outline=(20, 20, 25, 255), width=6)
    return _texted(_shrink(im, size), [(text, (16, 13))], ink, fill)


def half_off_tag(size=64):
    """A huge red clearance tag on a string: 50% / OFF in big white letters (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (60, 0, 0, 255)
    d.polygon([(S * .18, S * .14), (S * .96, S * .14), (S * .96, S * .86), (S * .18, S * .86), (S * .02, S * .5)],
              fill=(220, 30, 30, 255))
    d.line([(S * .18, S * .14), (S * .96, S * .14), (S * .96, S * .86), (S * .18, S * .86), (S * .02, S * .5), (S * .18, S * .14)],
           fill=OUT, width=8)
    d.ellipse([S * .12, S * .44, S * .22, S * .56], fill=(0, 0, 0, 0), outline=OUT, width=5)                       # hole
    im = _shrink(im, size)
    _big_text(im, "50%", (37, 23), (255, 255, 255, 255), scale=2, font=SMALL)
    _big_text(im, "OFF", (37, 41), (255, 240, 120, 255), scale=2, font=SMALL)
    return im


def crop_duster(size=64):
    """A yellow crop-duster biplane facing right: two wings, struts, a red propeller blur, a spray bar under the
    lower wing, the pilot's leather cap in the open cockpit."""
    im, d, S = _big(size)
    OUT = (40, 25, 5, 255)
    Y, YD = (250, 210, 40, 255), (200, 150, 20, 255)
    d.polygon([(S * .06, S * .34), (S * .16, S * .4), (S * .16, S * .5), (S * .06, S * .58)], fill=YD, outline=OUT)  # tail fin
    d.line([(S * .06, S * .34), (S * .16, S * .4), (S * .16, S * .5), (S * .06, S * .58), (S * .06, S * .34)], fill=OUT, width=6)
    d.rounded_rectangle([S * .1, S * .42, S * .84, S * .6], 18, fill=Y, outline=OUT, width=7)                       # fuselage
    d.rounded_rectangle([S * .26, S * .24, S * .76, S * .32], 8, fill=Y, outline=OUT, width=6)                      # top wing
    d.rounded_rectangle([S * .26, S * .6, S * .78, S * .68], 8, fill=YD, outline=OUT, width=6)                      # low wing
    for x in (.34, .66):
        d.line([(S * x, S * .32), (S * x, S * .6)], fill=OUT, width=5)                                               # struts
    d.ellipse([S * .44, S * .3, S * .58, S * .44], fill=(110, 60, 30, 255), outline=OUT, width=5)                   # pilot cap
    d.rectangle([S * .84, S * .44, S * .9, S * .58], fill=(80, 80, 90, 255), outline=OUT, width=4)                  # nose
    d.ellipse([S * .88, S * .26, S * .98, S * .76], fill=(230, 60, 40, 140), outline=(140, 20, 10, 255), width=4)   # prop blur
    d.line([(S * .3, S * .74), (S * .74, S * .74)], fill=(120, 120, 130, 255), width=6)                             # spray bar
    for x in (.36, .5, .64):
        d.line([(S * x, S * .68), (S * x, S * .76)], fill=(120, 120, 130, 255), width=4)
    for x in (.24, .42, .6, .76):
        d.ellipse([S * x, S * .82, S * (x + .08), S * .9], fill=(140, 220, 60, 200))                                 # the dust
    return _shrink(im, size)


def house_fly(size=32):
    """A fat cartoon housefly: black body, big red eyes, two see-through wings up."""
    im, d, S = _big(size)
    OUT = (10, 10, 10, 255)
    for x0 in (.18, .5):
        d.ellipse([S * x0, S * .06, S * (x0 + .34), S * .46], fill=(220, 235, 255, 170), outline=(90, 110, 140, 255), width=6)
    d.ellipse([S * .22, S * .38, S * .82, S * .9], fill=(40, 40, 46, 255), outline=OUT, width=7)
    d.ellipse([S * .14, S * .4, S * .36, S * .62], fill=(200, 30, 30, 255), outline=OUT, width=5)
    d.ellipse([S * .3, S * .46, S * .5, S * .64], fill=(200, 30, 30, 255), outline=OUT, width=5)
    d.line([(S * .5, S * .6), (S * .7, S * .62)], fill=(110, 110, 120, 255), width=4)
    return _shrink(im, size)


def stare_eyes(size=64):
    """Two narrowed eyes glowing in the dark: slanted black brows, red irises, a white glint - the look."""
    im, d, S = _big(size)
    OUT = (10, 0, 0, 255)
    for x0, sgn in ((.06, 1), (.54, -1)):
        x1 = x0 + .4
        d.chord([S * x0, S * .34, S * x1, S * .74], 180, 360, fill=(255, 250, 220, 255), outline=OUT, width=7)
        d.chord([S * x0, S * .5, S * x1, S * .62], 0, 180, fill=(255, 250, 220, 255), outline=OUT, width=7)
        cx = S * (x0 + .2 + sgn * .03)
        d.ellipse([cx - S * .08, S * .44, cx + S * .08, S * .6], fill=(220, 20, 20, 255), outline=OUT, width=5)
        d.ellipse([cx - S * .03, S * .49, cx + S * .03, S * .55], fill=OUT)
        d.ellipse([cx + S * .02, S * .46, cx + S * .05, S * .49], fill=(255, 255, 255, 255))
        a, b = (S * x0, S * .26), (S * x1, S * .42)
        if sgn < 0:
            a, b = (S * x0, S * .42), (S * x1, S * .26)
        d.line([a, b], fill=OUT, width=16)                                                                            # brows
    return _shrink(im, size)


def barber_pole(size=64, phase=0):
    """A barber pole: chrome caps, a glass tube with red, white and blue stripes (phase 0/1 shifts the stripes:
    flip between them and it spins)."""
    im, d, S = _big(size)
    OUT = (20, 20, 30, 255)
    d.rectangle([S * .36, S * .14, S * .64, S * .86], fill=(255, 255, 255, 255))
    step = .18
    for k in range(-2, 8):
        y = .14 + k * step + phase * step / 2
        for c, off in (((220, 30, 30, 255), 0), ((40, 70, 210, 255), step / 2)):
            yy = y + off
            d.polygon([(S * .36, S * yy), (S * .64, S * (yy - .1)), (S * .64, S * (yy - .1 + step / 4)),
                       (S * .36, S * (yy + step / 4))], fill=c)
    d.rectangle([S * 0, S * 0, S * 1, S * .14], fill=(0, 0, 0, 0))
    d.rectangle([S * 0, S * .86, S * 1, S * 1], fill=(0, 0, 0, 0))
    d.rectangle([S * .36, S * .14, S * .64, S * .86], outline=OUT, width=6)
    d.line([(S * .41, S * .18), (S * .41, S * .82)], fill=(255, 255, 255, 200), width=5)                          # glass shine
    for y0, y1 in ((.02, .14), (.86, .98)):
        d.rounded_rectangle([S * .3, S * y0, S * .7, S * y1], 8, fill=(200, 205, 215, 255), outline=OUT, width=6)
        d.line([(S * .36, S * (y0 + .04)), (S * .6, S * (y0 + .04))], fill=(255, 255, 255, 255), width=4)
    return _shrink(im, size)


def hair_clippers(size=64):
    """Barber clippers, blade down: a black body with a silver blade and a little cord."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.line([(S * .5, S * .82), (S * .62, S * .96), (S * .9, S * .98)], fill=(40, 40, 46, 255), width=8)            # cord
    d.rounded_rectangle([S * .32, S * .22, S * .68, S * .86], 26, fill=(40, 40, 46, 255), outline=OUT, width=7)
    d.rounded_rectangle([S * .38, S * .3, S * .46, S * .7], 6, fill=(110, 110, 120, 255))                         # shine
    d.rectangle([S * .44, S * .5, S * .56, S * .58], fill=(220, 180, 60, 255), outline=OUT, width=4)              # switch
    d.rectangle([S * .28, S * .08, S * .72, S * .24], fill=(210, 215, 225, 255), outline=OUT, width=6)            # blade
    for k in range(7):
        x = .3 + k * .065
        d.line([(S * x, S * .02), (S * x, S * .1)], fill=(170, 175, 185, 255), width=5)                            # teeth
    return _shrink(im, size)


def hair_snip(n=16):
    """A little clump of cut hair (alpha only): three short curved strands."""
    def f(x, y):
        for cx, cy, r in ((5, 9, 4), (8, 7, 5), (11, 9, 4)):
            dd = ((x - cx) ** 2 + (y - cy) ** 2) ** .5
            if abs(dd - r) < .8 and y < cy + 1:
                return 1
        return 0
    return _alpha(n, n, f)


# ---- set 23, batch 2: Mall Ninja, M-80, Zip Tie, Onion Breath, Rage Quit ---------------------------------------

def ninja_headband(size=64):
    """A white karate headband (hachimaki) curved round an invisible head: a red rising sun on the front, the
    knot at the side and its two tails flying out."""
    im, d, S = _big(size)
    OUT = (30, 20, 20, 255)
    d.arc([S * .04, S * .1, S * .76, S * .8], 20, 160, fill=OUT, width=int(S * .2))
    d.arc([S * .06, S * .12, S * .74, S * .78], 22, 158, fill=(250, 250, 250, 255), width=int(S * .14))
    d.ellipse([S * .3, S * .62, S * .5, S * .82], fill=(220, 30, 30, 255), outline=OUT, width=5)                   # the sun
    d.ellipse([S * .66, S * .5, S * .82, S * .66], fill=(250, 250, 250, 255), outline=OUT, width=6)               # knot
    for a, b, c in (((.8, .54), (.98, .3), (.92, .5)), ((.8, .62), (.98, .82), (.88, .66))):
        d.polygon([(S * a[0], S * a[1]), (S * b[0], S * b[1]), (S * c[0], S * c[1])], fill=(250, 250, 250, 255))
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1]), (S * c[0], S * c[1]), (S * a[0], S * a[1])], fill=OUT, width=6)
    return _shrink(im, size)


def board_chairs(size=64, broken=False):
    """A pine board laid across two grey folding chairs (the strip-mall dojo setup) - or the board snapped in
    the middle, both halves sagging."""
    im, d, S = _big(size)
    OUT = (30, 20, 10, 255)
    for x0 in (.06, .66):
        d.rectangle([S * x0, S * .5, S * (x0 + .28), S * .58], fill=(150, 155, 165, 255), outline=OUT, width=5)  # seat
        d.line([(S * (x0 + .02), S * .58), (S * (x0 + .26), S * .96)], fill=(110, 115, 125, 255), width=7)
        d.line([(S * (x0 + .26), S * .58), (S * (x0 + .02), S * .96)], fill=(110, 115, 125, 255), width=7)
        d.rectangle([S * (x0 + .2), S * .2, S * (x0 + .26), S * .52], fill=(150, 155, 165, 255), outline=OUT, width=4)  # back
    WOOD, WOOD_D = (230, 190, 120, 255), (170, 120, 60, 255)
    if not broken:
        d.rectangle([S * .04, S * .38, S * .96, S * .5], fill=WOOD, outline=OUT, width=6)
        for x in (.2, .45, .7):
            d.arc([S * x, S * .4, S * (x + .12), S * .48], 200, 340, fill=WOOD_D, width=3)                         # grain
    else:
        d.polygon([(S * .04, S * .38), (S * .46, S * .46), (S * .5, S * .56), (S * .04, S * .5)], fill=WOOD, outline=OUT)
        d.polygon([(S * .96, S * .38), (S * .54, S * .46), (S * .5, S * .56), (S * .96, S * .5)], fill=WOOD, outline=OUT)
        d.line([(S * .04, S * .38), (S * .46, S * .46), (S * .5, S * .56), (S * .04, S * .5), (S * .04, S * .38)], fill=OUT, width=6)
        d.line([(S * .96, S * .38), (S * .54, S * .46), (S * .5, S * .56), (S * .96, S * .5), (S * .96, S * .38)], fill=OUT, width=6)
        for x, y in ((.44, .5), (.56, .5), (.5, .58)):
            d.line([(S * x, S * y), (S * (x + .03), S * (y + .06))], fill=WOOD_D, width=4)                         # splinters
    return _shrink(im, size)


def chop_streak(size=64):
    """A white karate-chop motion arc with speed lines (the hand itself isn't drawn)."""
    im, d, S = _big(size)
    d.arc([S * .08, S * .08, S * .92, S * .92], 200, 300, fill=(255, 255, 255, 255), width=int(S * .1))
    d.arc([S * .16, S * .16, S * .84, S * .84], 205, 295, fill=(180, 220, 255, 255), width=int(S * .04))
    for k in range(3):
        a = .18 + k * .12
        d.line([(S * a, S * (.6 - k * .1)), (S * (a + .14), S * (.74 - k * .1))], fill=(255, 255, 255, 220), width=5)
    return _shrink(im, size)


def m80(size=64):
    """An M-80: a fat red cardboard tube with a black band and a twisted green fuse out the side."""
    im, d, S = _big(size)
    OUT = (40, 5, 5, 255)
    d.rounded_rectangle([S * .3, S * .4, S * .78, S * .86], 12, fill=(200, 30, 30, 255), outline=OUT, width=8)
    d.rectangle([S * .3, S * .56, S * .78, S * .66], fill=(30, 30, 34, 255))
    d.rounded_rectangle([S * .3, S * .4, S * .78, S * .86], 12, outline=OUT, width=8)
    d.line([(S * .38, S * .46), (S * .38, S * .8)], fill=(255, 120, 110, 255), width=6)                         # shine
    d.ellipse([S * .3, S * .34, S * .78, S * .48], fill=(220, 200, 160, 255), outline=OUT, width=6)               # end cap
    d.line([(S * .54, S * .4), (S * .48, S * .22), (S * .56, S * .1)], fill=(40, 150, 60, 255), width=8)          # fuse
    return _shrink(im, size)


def m80_blast(size=64):
    """A cartoon explosion: a yellow-white core, an orange flame burst, a ring of dark smoke puffs."""
    import math
    im, d, S = _big(size)
    OUT = (40, 20, 10, 255)
    for k in range(9):
        a = k * 2 * math.pi / 9
        cx, cy = S * (.5 + .34 * math.cos(a)), S * (.5 + .3 * math.sin(a))
        d.ellipse([cx - S * .14, cy - S * .14, cx + S * .14, cy + S * .14], fill=(90, 85, 85, 255), outline=OUT, width=6)
    pts = []
    for k in range(24):
        a = k * 2 * math.pi / 24
        r = .4 if k % 2 == 0 else .26
        pts.append((S * (.5 + r * math.cos(a)), S * (.5 + r * math.sin(a))))
    d.polygon(pts, fill=(255, 130, 20, 255), outline=OUT)
    d.line(pts + [pts[0]], fill=OUT, width=6)
    d.ellipse([S * .32, S * .32, S * .68, S * .68], fill=(255, 230, 80, 255))
    d.ellipse([S * .4, S * .4, S * .6, S * .6], fill=(255, 255, 230, 255))
    return _shrink(im, size)


def zip_tie(size=64, color=(30, 30, 34, 255), hi=(110, 110, 120, 255)):
    """A zip tie cinched into a wide loop (seen at an angle): ridged strap, the square lock head and a long tail
    sticking out."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255) if color[0] > 100 else (200, 200, 205, 255)
    d.ellipse([S * .04, S * .3, S * .96, S * .66], outline=OUT, width=int(S * .1))
    d.ellipse([S * .05, S * .31, S * .95, S * .65], outline=color, width=int(S * .07))
    import math
    for k in range(18):
        a = k * 2 * math.pi / 18
        x, y = S * (.5 + .44 * math.cos(a)), S * (.48 + .16 * math.sin(a))
        d.line([(x, y - S * .02), (x, y + S * .02)], fill=hi, width=3)                                         # ridges
    d.rectangle([S * .42, S * .56, S * .6, S * .74], fill=color, outline=OUT, width=6)                           # lock head
    d.polygon([(S * .5, S * .72), (S * .6, S * .72), (S * .86, S * .96), (S * .76, S * .98)], fill=color)
    d.line([(S * .5, S * .72), (S * .76, S * .98), (S * .86, S * .96), (S * .6, S * .72)], fill=OUT, width=5)    # tail
    return _shrink(im, size)


def red_onion(size=64, bites=0):
    """A raw red onion, purple-red skin with layer lines, a dry sprout and roots - with 1 or 2 bites out of it
    showing the white rings inside."""
    im, d, S = _big(size)
    OUT = (50, 10, 40, 255)
    d.ellipse([S * .14, S * .24, S * .86, S * .92], fill=(170, 40, 110, 255), outline=OUT, width=8)
    for x0, x1 in ((.26, .74), (.38, .62)):
        d.arc([S * x0, S * .26, S * x1, S * .9], 100, 260, fill=(110, 20, 70, 255), width=5)
        d.arc([S * x0, S * .26, S * x1, S * .9], 280, 80, fill=(110, 20, 70, 255), width=5)
    d.arc([S * .2, S * .32, S * .5, S * .62], 200, 260, fill=(240, 150, 200, 255), width=6)                      # shine
    d.polygon([(S * .44, S * .28), (S * .5, S * .04), (S * .56, S * .28)], fill=(200, 170, 110, 255), outline=OUT)
    d.line([(S * .44, S * .28), (S * .5, S * .04), (S * .56, S * .28)], fill=OUT, width=5)                      # sprout
    for x in (.44, .5, .56):
        d.line([(S * .5, S * .9), (S * x, S * .98)], fill=(220, 200, 160, 255), width=4)                         # roots
    for n in range(bites):
        cx, cy = (S * .8, S * .48) if n == 0 else (S * .74, S * .74)
        d.ellipse([cx - S * .16, cy - S * .14, cx + S * .16, cy + S * .14], fill=(250, 240, 250, 255), outline=OUT, width=5)
        d.arc([cx - S * .1, cy - S * .08, cx + S * .1, cy + S * .08], 120, 240, fill=(220, 160, 210, 255), width=4)
        d.ellipse([cx, cy - S * .2, cx + S * .3, cy + S * .2], fill=(0, 0, 0, 0))
    return _shrink(im, size)


def stink_wave(n=16):
    """A wavy stink line (alpha only), for breath."""
    import math

    def f(x, y):
        yy = 8 + 3 * math.sin(x / 2.2)
        return 1 if abs(y - yy) < 1.3 and 1 < x < 15 else 0
    return _alpha(n, n, f)


def gaming_monitor(size=64, cracked=False):
    """A gaming monitor on its stand, the screen reading GAME OVER in red - or the same with the screen
    smashed (a spiderweb crack) (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (10, 10, 14, 255)
    d.rounded_rectangle([S * .04, S * .1, S * .96, S * .72], 8, fill=(30, 30, 36, 255), outline=OUT, width=7)
    d.rectangle([S * .1, S * .16, S * .9, S * .66], fill=(10, 10, 30, 255))
    d.line([(S * .1, S * .68), (S * .9, S * .68)], fill=(80, 200, 255, 255), width=4)                           # RGB strip
    d.rectangle([S * .44, S * .72, S * .56, S * .86], fill=(50, 50, 56, 255), outline=OUT, width=5)
    d.rounded_rectangle([S * .26, S * .84, S * .74, S * .94], 6, fill=(50, 50, 56, 255), outline=OUT, width=5)
    if cracked:
        import math
        c = (S * .62, S * .36)
        for k in range(7):
            a = k * 2 * math.pi / 7 + .3
            d.line([c, (c[0] + S * .3 * math.cos(a), c[1] + S * .24 * math.sin(a))], fill=(230, 240, 255, 255), width=4)
        d.ellipse([c[0] - S * .1, c[1] - S * .08, c[0] + S * .1, c[1] + S * .08], outline=(230, 240, 255, 255), width=3)
    im = _shrink(im, size)
    # keep the screen dark round the words, crack lines included
    return _texted(im, [("GAME", (30, 15)), ("OVER", (30, 25))], (255, 50, 50, 255), (10, 10, 30, 255))


def gamepad(size=64):
    """A black gamepad: two grips, a d-pad, four coloured face buttons, two sticks."""
    im, d, S = _big(size)
    OUT = (5, 5, 8, 255)
    B = (40, 40, 46, 255)
    d.ellipse([S * .04, S * .3, S * .38, S * .86], fill=B, outline=OUT, width=7)
    d.ellipse([S * .62, S * .3, S * .96, S * .86], fill=B, outline=OUT, width=7)
    d.rounded_rectangle([S * .16, S * .26, S * .84, S * .62], 20, fill=B, outline=OUT, width=7)
    d.rectangle([S * .16, S * .32, S * .84, S * .58], fill=B)
    d.rectangle([S * .14, S * .4, S * .3, S * .46], fill=(120, 120, 130, 255))                                   # d-pad
    d.rectangle([S * .19, S * .35, S * .25, S * .51], fill=(120, 120, 130, 255))
    for (x, y), c in (((.72, .34), (240, 200, 40)), ((.66, .42), (40, 120, 230)), ((.78, .42), (220, 40, 40)), ((.72, .5), (40, 190, 80))):
        d.ellipse([S * (x - .04), S * (y - .04), S * (x + .04), S * (y + .04)], fill=c + (255,), outline=OUT, width=3)
    for x in (.38, .58):
        d.ellipse([S * (x - .06), S * .5, S * (x + .06), S * .62], fill=(90, 90, 100, 255), outline=OUT, width=4)
    d.line([(S * .2, S * .32), (S * .4, S * .3)], fill=(110, 110, 120, 255), width=4)
    return _shrink(im, size)


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


# ---- set 23, batch 4: Cold Cocked, Last Call, Tanning Bed, Victory Lap, Gift Bomb -------------------------------

def chest_freezer(size=64):
    """A white chest freezer with the lid flung open, frost on the rim and cold mist inside."""
    im, d, S = _big(size)
    OUT = (40, 50, 70, 255)
    d.polygon([(S * .1, S * .36), (S * .9, S * .36), (S * .96, S * .1), (S * .16, S * .1)], fill=(225, 232, 242, 255), outline=OUT)
    d.line([(S * .1, S * .36), (S * .9, S * .36), (S * .96, S * .1), (S * .16, S * .1), (S * .1, S * .36)], fill=OUT, width=7)   # lid up
    d.polygon([(S * .2, S * .32), (S * .82, S * .32), (S * .86, S * .14), (S * .24, S * .14)], fill=(190, 215, 240, 255))
    d.rounded_rectangle([S * .06, S * .44, S * .94, S * .94], 8, fill=(245, 248, 252, 255), outline=OUT, width=8)  # body
    d.rectangle([S * .06, S * .4, S * .94, S * .52], fill=(160, 210, 245, 255), outline=OUT, width=6)              # frosty opening
    for x in (.14, .3, .52, .7, .84):
        d.polygon([(S * x, S * .52), (S * (x + .03), S * .6), (S * (x + .06), S * .52)], fill=(200, 235, 255, 255))   # icicles
    d.rectangle([S * .4, S * .62, S * .6, S * .68], fill=(150, 155, 165, 255), outline=OUT, width=4)              # handle
    d.ellipse([S * .78, S * .82, S * .86, S * .9], fill=(80, 200, 90, 255))                                        # power light
    return _shrink(im, size)


def popsicle(size=32):
    """A red, white and blue rocket popsicle on a stick."""
    im, d, S = _big(size)
    OUT = (30, 20, 40, 255)
    d.rectangle([S * .44, S * .7, S * .56, S * .98], fill=(225, 190, 130, 255), outline=OUT, width=5)
    d.polygon([(S * .5, S * .02), (S * .74, S * .26), (S * .26, S * .26)], fill=(220, 40, 40, 255), outline=OUT)
    d.rectangle([S * .26, S * .26, S * .74, S * .48], fill=(250, 250, 250, 255), outline=OUT, width=5)
    d.rectangle([S * .22, S * .48, S * .78, S * .72], fill=(40, 90, 220, 255), outline=OUT, width=5)
    d.line([(S * .5, S * .02), (S * .74, S * .26), (S * .26, S * .26), (S * .5, S * .02)], fill=OUT, width=5)
    return _shrink(im, size)


def peas_bag(size=32):
    """A frozen bag of peas: a green bag, crimped top, a bowl of peas pictured on the front, frost."""
    im, d, S = _big(size)
    OUT = (10, 50, 20, 255)
    d.rounded_rectangle([S * .14, S * .14, S * .86, S * .94], 10, fill=(40, 170, 70, 255), outline=OUT, width=6)
    d.rectangle([S * .12, S * .06, S * .88, S * .18], fill=(30, 140, 60, 255), outline=OUT, width=5)
    for k in range(6):
        d.line([(S * (.16 + k * .13), S * .07), (S * (.16 + k * .13), S * .17)], fill=OUT, width=3)
    d.ellipse([S * .26, S * .42, S * .74, S * .82], fill=(250, 250, 250, 255), outline=OUT, width=4)
    for x, y in ((.4, .56), (.52, .52), (.6, .62), (.46, .66), (.36, .66)):
        d.ellipse([S * (x - .06), S * (y - .06), S * (x + .06), S * (y + .06)], fill=(120, 220, 80, 255), outline=OUT, width=2)
    d.line([(S * .2, S * .3), (S * .4, S * .24)], fill=(220, 245, 255, 255), width=5)                                # frost
    return _shrink(im, size)


def frozen_turkey(size=64):
    """A whole frozen turkey: a pale icy body, two drumsticks with paper frills, frost and a little icicle."""
    im, d, S = _big(size)
    OUT = (60, 50, 60, 255)
    SKIN = (240, 220, 190, 255)
    d.ellipse([S * .1, S * .3, S * .78, S * .84], fill=SKIN, outline=OUT, width=8)
    for a, b in (((.62, .4), (.9, .2)), ((.66, .62), (.94, .52))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=SKIN, width=int(S * .12))
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=OUT, width=4)
        d.ellipse([S * (b[0] - .07), S * (b[1] - .07), S * (b[0] + .07), S * (b[1] + .07)], fill=(255, 255, 255, 255), outline=OUT, width=4)
    d.ellipse([S * .1, S * .3, S * .78, S * .84], outline=OUT, width=8)
    d.arc([S * .2, S * .36, S * .6, S * .66], 200, 300, fill=(255, 255, 255, 255), width=6)                      # shine
    for x, y in ((.24, .5), (.42, .44), (.36, .66), (.56, .7)):
        d.line([(S * (x - .04), S * y), (S * (x + .04), S * y)], fill=(170, 220, 255, 255), width=4)
        d.line([(S * x, S * (y - .04)), (S * x, S * (y + .04))], fill=(170, 220, 255, 255), width=4)            # frost sparkles
    d.polygon([(S * .4, S * .82), (S * .44, S * .96), (S * .48, S * .82)], fill=(190, 230, 255, 255))           # icicle
    return _shrink(im, size)


def frost_crystal(n=16):
    """A six-armed frost sparkle (alpha only)."""
    import math

    def f(x, y):
        dx, dy = x - 7.5, y - 7.5
        r = math.hypot(dx, dy)
        if r > 7:
            return 0
        a = math.atan2(dy, dx) % (math.pi / 3)
        return 1 if min(a, math.pi / 3 - a) * r < .9 or r < 1.6 else 0
    return _alpha(n, n, f)


def bar_bell(size=64, swing=0):
    """A brass bar bell hanging from a wall bracket with a rope pull; swing -1/0/1 tilts it mid-ring."""
    im, d, S = _big(size)
    OUT = (50, 30, 5, 255)
    d.rectangle([S * .08, S * .06, S * .2, S * .3], fill=(90, 60, 30, 255), outline=OUT, width=5)                  # bracket
    d.line([(S * .2, S * .14), (S * .56, S * .14)], fill=(60, 60, 66, 255), width=7)
    bell = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    b = ImageDraw.Draw(bell)
    b.line([(S * .56, S * .14), (S * .56, S * .26)], fill=(60, 60, 66, 255), width=6)
    b.chord([S * .34, S * .22, S * .78, S * .74], 180, 360, fill=(240, 190, 50, 255), outline=OUT, width=7)
    b.rectangle([S * .34, S * .48, S * .78, S * .66], fill=(240, 190, 50, 255))
    b.polygon([(S * .34, S * .66), (S * .28, S * .74), (S * .84, S * .74), (S * .78, S * .66)], fill=(220, 160, 30, 255))
    b.line([(S * .34, S * .48), (S * .34, S * .66), (S * .28, S * .74), (S * .84, S * .74), (S * .78, S * .66), (S * .78, S * .48)], fill=OUT, width=7)
    b.line([(S * .42, S * .34), (S * .42, S * .6)], fill=(255, 240, 160, 255), width=6)                            # shine
    b.ellipse([S * .5, S * .72, S * .62, S * .84], fill=(120, 90, 40, 255), outline=OUT, width=4)                # clapper
    b.line([(S * .56, S * .84), (S * .5, S * .98)], fill=(200, 170, 110, 255), width=6)                           # rope
    if swing:
        bell = bell.rotate(-14 * swing, center=(S * .56, S * .14), resample=Image.BICUBIC)
    im.alpha_composite(bell)
    return _shrink(im, size)


def mirror_ball(size=64, phase=0):
    """A mirror disco ball on its chain: a grid of grey/white facets; phase 0/1 moves the bright facets so it
    twinkles as it turns."""
    im, d, S = _big(size)
    OUT = (30, 30, 40, 255)
    d.line([(S * .5, 0), (S * .5, S * .16)], fill=(150, 150, 160, 255), width=6)
    d.ellipse([S * .16, S * .14, S * .84, S * .82], fill=(170, 175, 190, 255), outline=OUT, width=7)
    for i in range(7):
        for j in range(7):
            x, y = .2 + i * .09, .18 + j * .09
            if ((x + .045 - .5) ** 2 + (y + .045 - .48) ** 2) > .1:
                continue
            c = (255, 255, 255, 255) if (i + j + phase) % 3 == 0 else ((120, 125, 140, 255) if (i * j + phase) % 2 else (200, 205, 220, 255))
            d.rectangle([S * x, S * y, S * (x + .08), S * (y + .08)], fill=c)
    d.ellipse([S * .16, S * .14, S * .84, S * .82], outline=OUT, width=7)
    return _shrink(im, size)


def tanning_bed(size=64, shut=False):
    """A tanning bed (clamshell): silver shell with the purple-blue UV tubes glowing inside; open (the lid
    raised) or shut (the glow leaking out the seam)."""
    im, d, S = _big(size)
    OUT = (20, 15, 40, 255)
    SHELL, SHELL_D = (200, 205, 220, 255), (140, 145, 165, 255)
    d.rounded_rectangle([S * .04, S * .62, S * .96, S * .86], 14, fill=SHELL, outline=OUT, width=7)               # base
    d.rectangle([S * .1, S * .86, S * .2, S * .96], fill=SHELL_D, outline=OUT, width=5)
    d.rectangle([S * .8, S * .86, S * .9, S * .96], fill=SHELL_D, outline=OUT, width=5)
    if shut:
        d.rounded_rectangle([S * .04, S * .38, S * .96, S * .64], 30, fill=SHELL, outline=OUT, width=7)
        d.rectangle([S * .08, S * .6, S * .92, S * .66], fill=(190, 120, 255, 255))                              # glow seam
        d.line([(S * .14, S * .44), (S * .86, S * .44)], fill=(240, 240, 250, 255), width=5)
    else:
        d.polygon([(S * .04, S * .62), (S * .2, S * .06), (S * .96, S * .2), (S * .96, S * .62)], fill=SHELL_D, outline=OUT)
        d.line([(S * .04, S * .62), (S * .2, S * .06), (S * .96, S * .2), (S * .96, S * .62)], fill=OUT, width=7)
        d.polygon([(S * .14, S * .56), (S * .26, S * .14), (S * .88, S * .26), (S * .88, S * .56)], fill=(120, 60, 220, 255))
        for k in range(4):
            y = .26 + k * .08
            d.line([(S * .24, S * (y - .02)), (S * .84, S * (y + .04))], fill=(220, 190, 255, 255), width=5)       # UV tubes
        d.rectangle([S * .1, S * .62, S * .9, S * .68], fill=(160, 100, 240, 255))
    return _shrink(im, size)


def sun_ray(n=16):
    """A long thin ray of light (alpha only): bright core, soft edges."""
    def f(x, y):
        dy = abs(y - 7.5)
        return max(0, 1 - dy / 3) if 1 < x < 15 else 0
    return _alpha(n, n, f)


def victory_trophy(size=64):
    """A big gold trophy cup: two handles, a star on the front, a black base with a gold plate."""
    im, d, S = _big(size)
    OUT = (60, 40, 0, 255)
    G, GL, GD = (250, 200, 40, 255), (255, 240, 150, 255), (200, 140, 20, 255)
    for x0 in (.06, .7):
        d.ellipse([S * x0, S * .14, S * (x0 + .24), S * .44], outline=OUT, width=12)
        d.ellipse([S * x0, S * .14, S * (x0 + .24), S * .44], outline=G, width=6)
    d.chord([S * .2, S * -.1, S * .8, S * .62], 0, 180, fill=G, outline=OUT, width=8)
    d.rectangle([S * .2, S * .06, S * .8, S * .26], fill=G)
    d.line([(S * .2, S * .06), (S * .8, S * .06)], fill=OUT, width=8)
    d.line([(S * .2, S * .06), (S * .2, S * .26)], fill=OUT, width=8)
    d.line([(S * .8, S * .06), (S * .8, S * .26)], fill=OUT, width=8)
    d.line([(S * .3, S * .14), (S * .32, S * .4)], fill=GL, width=6)                                              # shine
    d.rectangle([S * .44, S * .6, S * .56, S * .74], fill=GD, outline=OUT, width=5)                               # stem
    d.rectangle([S * .26, S * .74, S * .74, S * .96], fill=(40, 30, 30, 255), outline=OUT, width=6)               # base
    d.rectangle([S * .36, S * .8, S * .64, S * .9], fill=G)
    import math
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        r = .1 if k % 2 == 0 else .045
        pts.append((S * (.5 + r * math.cos(a)), S * (.3 + r * math.sin(a))))
    d.polygon(pts, fill=GL, outline=OUT)
    return _shrink(im, size)


def rose_petal(n=16):
    """A single curled rose petal (alpha only)."""
    def f(x, y):
        dx, dy = (x - 7.5) / 6, (y - 8) / 4.5
        return 1 if dx * dx + dy * dy < 1 and not (dx > .3 and dy < -.2) else 0
    return _alpha(n, n, f)


def gift_box(size=64, wrap=(220, 30, 40, 255), ribbon=(255, 210, 40, 255)):
    """A wrapped present: coloured paper, a ribbon cross and a big bow on top."""
    im, d, S = _big(size)
    OUT = (30, 15, 15, 255)
    d.rectangle([S * .14, S * .4, S * .86, S * .94], fill=wrap, outline=OUT, width=7)
    d.rectangle([S * .08, S * .3, S * .92, S * .44], fill=wrap, outline=OUT, width=7)                             # lid
    d.rectangle([S * .44, S * .3, S * .56, S * .94], fill=ribbon, outline=OUT, width=4)
    for pts in (((.5, .3), (.22, .08), (.24, .28)), ((.5, .3), (.78, .08), (.76, .28))):
        _outline_poly(d, [(S * x, S * y) for x, y in pts], ribbon, OUT, 6)                                          # bow
    d.ellipse([S * .44, S * .22, S * .56, S * .34], fill=ribbon, outline=OUT, width=4)
    d.line([(S * .2, S * .5), (S * .2, S * .86)], fill=(255, 255, 255, 120), width=5)
    return _shrink(im, size)


def cartoon_bomb(size=64):
    """A round black cartoon bomb with a shine and a short lit fuse."""
    im, d, S = _big(size)
    OUT = (5, 5, 10, 255)
    d.ellipse([S * .14, S * .3, S * .8, S * .96], fill=(30, 30, 38, 255), outline=OUT, width=8)
    d.rectangle([S * .4, S * .22, S * .58, S * .34], fill=(90, 90, 100, 255), outline=OUT, width=5)
    d.line([(S * .49, S * .22), (S * .6, S * .1), (S * .74, S * .08)], fill=(200, 170, 110, 255), width=6)
    d.ellipse([S * .26, S * .44, S * .4, S * .58], fill=(140, 140, 160, 255))
    return _shrink(im, size)


def confetti_boom(size=64):
    """A party explosion: a white-hot centre, a red/yellow burst, and ribbon and confetti flying out."""
    import math
    im, d, S = _big(size)
    OUT = (40, 10, 10, 255)
    pts = []
    for k in range(20):
        a = k * 2 * math.pi / 20
        r = .44 if k % 2 == 0 else .28
        pts.append((S * (.5 + r * math.cos(a)), S * (.5 + r * math.sin(a))))
    _outline_poly(d, pts, (255, 90, 40, 255), OUT, 7)
    d.ellipse([S * .28, S * .28, S * .72, S * .72], fill=(255, 220, 60, 255))
    d.ellipse([S * .38, S * .38, S * .62, S * .62], fill=(255, 255, 230, 255))
    for k, c in enumerate(((60, 200, 255), (255, 60, 200), (120, 230, 60), (255, 255, 255), (160, 90, 255), (255, 230, 40))):
        a = k * 2 * math.pi / 6 + .5
        x, y = .5 + .4 * math.cos(a), .5 + .4 * math.sin(a)
        d.rectangle([S * (x - .04), S * (y - .025), S * (x + .04), S * (y + .025)], fill=c + (255,), outline=OUT, width=3)
    return _shrink(im, size)


def confetti_bit(n=16):
    """A small confetti rectangle (alpha only)."""
    return _alpha(n, n, lambda x, y: 1 if 4 < x < 12 and 6 < y < 10 else 0)


# ---- set 23, batch 5: Clothesline, Bullhorn, Hype Man, Ring Ya Bell, Heat Check -----------------------------------

def clothesline_rig(size=64):
    """A backyard clothesline: two wooden T-posts and a sagging rope between them with three clothespins."""
    im, d, S = _big(size)
    OUT = (40, 25, 10, 255)
    WOOD = (160, 110, 60, 255)
    for x in (.04, .9):
        d.rectangle([S * x, S * .3, S * (x + .06), S * .98], fill=WOOD, outline=OUT, width=5)
        d.rectangle([S * (x - .03), S * .28, S * (x + .09), S * .34], fill=WOOD, outline=OUT, width=4)
    d.arc([S * .07, S * -.04, S * .93, S * .62], 22, 158, fill=OUT, width=7)
    d.arc([S * .07, S * -.04, S * .93, S * .62], 22, 158, fill=(240, 240, 235, 255), width=3)                      # rope
    for x in (.3, .5, .7):
        y = .56 - .06 * (1 - abs(x - .5) / .5) * -1
        d.rectangle([S * (x - .015), S * (y - .02), S * (x + .015), S * (y + .07)], fill=(220, 190, 130, 255), outline=OUT, width=3)
    return _shrink(im, size)


def white_tee(size=32):
    """A plain white tee hung by the shoulders."""
    im, d, S = _big(size)
    OUT = (60, 60, 70, 255)
    _outline_poly(d, [(S * .3, S * .1), (S * .7, S * .1), (S * .96, S * .3), (S * .82, S * .44), (S * .74, S * .36), (S * .74, S * .94),
                      (S * .26, S * .94), (S * .26, S * .36), (S * .18, S * .44), (S * .04, S * .3)], (250, 250, 250, 255), OUT, 7)
    d.arc([S * .38, S * .02, S * .62, S * .2], 0, 180, fill=OUT, width=5)
    return _shrink(im, size)


def line_boxers(size=32):
    """Red boxer shorts with white hearts, hung on the line."""
    im, d, S = _big(size)
    OUT = (60, 0, 10, 255)
    _outline_poly(d, [(S * .1, S * .16), (S * .9, S * .16), (S * .96, S * .86), (S * .56, S * .86), (S * .5, S * .5), (S * .44, S * .86),
                      (S * .04, S * .86)], (220, 30, 50, 255), OUT, 7)
    d.rectangle([S * .1, S * .14, S * .9, S * .26], fill=(250, 250, 250, 255), outline=OUT, width=5)
    for x, y in ((.24, .46), (.74, .5), (.3, .7), (.8, .74)):
        d.ellipse([S * (x - .05), S * (y - .05), S * (x + .05), S * (y + .05)], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def bullhorn(size=64):
    """A police bullhorn (megaphone): a white flared horn with a red rim, a black pistol grip and trigger."""
    im, d, S = _big(size)
    OUT = (20, 20, 26, 255)
    d.polygon([(S * .14, S * .36), (S * .5, S * .3), (S * .94, S * .1), (S * .94, S * .78), (S * .5, S * .58), (S * .14, S * .52)],
              fill=(245, 245, 245, 255))
    d.line([(S * .14, S * .36), (S * .5, S * .3), (S * .94, S * .1), (S * .94, S * .78), (S * .5, S * .58), (S * .14, S * .52), (S * .14, S * .36)],
           fill=OUT, width=7)
    d.ellipse([S * .86, S * .1, S * .98, S * .78], fill=(220, 30, 30, 255), outline=OUT, width=6)                # rim
    d.ellipse([S * .89, S * .2, S * .95, S * .68], fill=(60, 60, 66, 255))
    d.rectangle([S * .04, S * .36, S * .16, S * .52], fill=(60, 60, 66, 255), outline=OUT, width=5)              # mouthpiece
    d.rounded_rectangle([S * .3, S * .52, S * .44, S * .9], 6, fill=(40, 40, 46, 255), outline=OUT, width=5)     # grip
    d.rectangle([S * .44, S * .58, S * .5, S * .7], fill=(220, 30, 30, 255), outline=OUT, width=3)               # trigger
    d.line([(S * .5, S * .36), (S * .86, S * .2)], fill=(200, 200, 210, 255), width=4)
    return _shrink(im, size)


def feedback_squiggle(n=16):
    """A zig-zag squeal line (alpha only), for mic feedback."""
    def f(x, y):
        t = (x % 4) / 4
        yy = 8 + 6 * (t if t < .5 else 1 - t) - 1.5
        return 1 if abs(y - yy) < 1.2 and 1 < x < 15 else 0
    return _alpha(n, n, f)


def hype_bubble(text, size=64, scale=1):
    """A white shout bubble (spiky at the edges) with one word at 1x or 2x pixel scale (shown at 1:1)."""
    import math
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    pts = []
    for k in range(28):
        a = k * 2 * math.pi / 28
        r = .46 if k % 2 == 0 else .4
        pts.append((S * (.5 + r * math.cos(a)), S * (.46 + r * .7 * math.sin(a))))
    _outline_poly(d, pts, (255, 255, 255, 255), OUT, 8)
    d.polygon([(S * .3, S * .7), (S * .14, S * .96), (S * .42, S * .72)], fill=(255, 255, 255, 255))
    d.line([(S * .3, S * .74), (S * .14, S * .96), (S * .42, S * .74)], fill=OUT, width=7)
    im = _shrink(im, size)
    if scale == 1:
        return _texted(im, [(text, (32, 26))], (20, 20, 25, 255), (255, 255, 255, 255))
    _big_text(im, text, (32, 30), (230, 30, 30, 255), scale=scale, font=SMALL)
    return im


def doorbell_plate(size=64):
    """A doorbell on a slice of brick wall: a brass plate with a glowing round button and a house number."""
    im, d, S = _big(size)
    OUT = (40, 20, 10, 255)
    d.rectangle([S * .1, S * .06, S * .9, S * .94], fill=(170, 70, 50, 255), outline=OUT, width=7)                # brick
    for y in range(6):
        yy = .06 + y * .147
        d.line([(S * .1, S * yy), (S * .9, S * yy)], fill=(120, 50, 35, 255), width=4)
        for x in ((.3, .62) if y % 2 else (.46, .78)):
            d.line([(S * x, S * yy), (S * x, S * (yy + .147))], fill=(120, 50, 35, 255), width=4)
    d.rounded_rectangle([S * .32, S * .22, S * .68, S * .78], 10, fill=(230, 190, 70, 255), outline=OUT, width=6)  # plate
    d.ellipse([S * .4, S * .4, S * .6, S * .6], fill=(255, 250, 200, 255), outline=OUT, width=5)                   # button
    d.ellipse([S * .45, S * .45, S * .55, S * .55], fill=(255, 220, 80, 255))
    return _shrink(im, size)


def dizzy_bird(size=32):
    """A little yellow cartoon bird with its wings up (the ones that circle a knocked-out head)."""
    im, d, S = _big(size)
    OUT = (60, 40, 0, 255)
    d.ellipse([S * .2, S * .3, S * .8, S * .86], fill=(255, 220, 40, 255), outline=OUT, width=6)
    d.polygon([(S * .3, S * .44), (S * .1, S * .1), (S * .5, S * .36)], fill=(255, 240, 120, 255), outline=OUT)
    d.polygon([(S * .7, S * .44), (S * .9, S * .1), (S * .5, S * .36)], fill=(255, 240, 120, 255), outline=OUT)
    d.polygon([(S * .76, S * .56), (S * .98, S * .62), (S * .76, S * .68)], fill=(250, 140, 30, 255), outline=OUT)
    d.ellipse([S * .58, S * .46, S * .68, S * .56], fill=OUT)
    return _shrink(im, size)


def thermostat(size=64, temp="72"):
    """A wall thermostat: a beige box, a dark screen with the temperature in big digits (red at 99), up/down
    buttons (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 35, 30, 255)
    d.rounded_rectangle([S * .14, S * .1, S * .86, S * .9], 14, fill=(235, 225, 205, 255), outline=OUT, width=8)
    d.rectangle([S * .24, S * .2, S * .76, S * .56], fill=(30, 50, 40, 255) if temp != "99" else (60, 10, 10, 255), outline=OUT, width=5)
    for y, up in ((.66, True), (.66, False)):
        x = .36 if up else .64
        d.ellipse([S * (x - .09), S * (y - .07), S * (x + .09), S * (y + .11)], fill=(200, 190, 170, 255), outline=OUT, width=5)
        tri = [(S * x, S * (y - .02)), (S * (x - .05), S * (y + .06)), (S * (x + .05), S * (y + .06))] if up else \
              [(S * x, S * (y + .08)), (S * (x - .05), S * y), (S * (x + .05), S * y)]
        d.polygon(tri, fill=OUT)
    im = _shrink(im, size)
    col = {"72": (120, 255, 160, 255), "85": (255, 200, 60, 255), "99": (255, 60, 40, 255)}[temp]
    _big_text(im, temp, (30, 24), col, scale=2)
    _texted(im, [("F", (44, 16))], col, (30, 50, 40, 255) if temp != "99" else (60, 10, 10, 255))
    return im


def heat_shimmer(n=16):
    """A rising heat-haze ripple (alpha only): two short wavy vertical lines."""
    import math

    def f(x, y):
        for cx in (5, 11):
            if abs(x - (cx + 1.5 * math.sin(y / 2))) < 1 and 2 < y < 14:
                return 1
        return 0
    return _alpha(n, n, f)


def shout_arc(n=16):
    """A sound-wave arc ")" (alpha only), for shouting."""
    import math

    def f(x, y):
        r = math.hypot(x - 2, y - 7.5)
        return 1 if abs(r - 10) < 1.4 and x > 6 else 0
    return _alpha(n, n, f)


# ---- set 23, batch 6: Gas Up, Door Kick, Getaway, Bug Zapper, Split Bill ---------------------------------------

def gas_pump(size=64, amount="$5.00"):
    """A red gas pump: the price screen reading `amount`, the octane buttons, the hose looping out the right side
    (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (30, 10, 10, 255)
    d.rectangle([S * .08, S * .9, S * .7, S * .98], fill=(120, 120, 130, 255), outline=OUT, width=5)            # island
    d.rounded_rectangle([S * .12, S * .06, S * .66, S * .92], 10, fill=(210, 30, 30, 255), outline=OUT, width=8)
    d.rectangle([S * .18, S * .14, S * .6, S * .38], fill=(20, 30, 20, 255), outline=OUT, width=5)              # screen
    for k, c in enumerate(((240, 240, 240), (240, 200, 40), (60, 180, 80))):
        d.rectangle([S * (.2 + k * .13), S * .46, S * (.3 + k * .13), S * .54], fill=c + (255,), outline=OUT, width=3)
    d.rectangle([S * .22, S * .62, S * .56, S * .84], fill=(250, 250, 250, 255), outline=OUT, width=4)          # logo panel
    d.line([(S * .3, S * .7), (S * .48, S * .7)], fill=(210, 30, 30, 255), width=6)
    d.line([(S * .3, S * .77), (S * .44, S * .77)], fill=(210, 30, 30, 255), width=6)
    d.arc([S * .56, S * .3, S * .98, S * .9], 270, 90, fill=OUT, width=10)
    d.arc([S * .56, S * .3, S * .98, S * .9], 270, 90, fill=(40, 40, 46, 255), width=6)                         # hose
    im = _shrink(im, size)
    col = (255, 60, 40, 255) if amount.startswith("$99") else (120, 255, 140, 255)
    return _texted(im, [(amount, (25, 13))], col, (20, 30, 20, 255))


def gas_nozzle(size=64):
    """A gas pump nozzle: black grip and trigger guard, the silver spout pointing left, a bit of hose."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.line([(S * .74, S * .5), (S * .98, S * .3)], fill=(40, 40, 46, 255), width=int(S * .1))                    # hose
    d.polygon([(S * .4, S * .36), (S * .78, S * .36), (S * .82, S * .58), (S * .44, S * .58)], fill=(40, 40, 46, 255), outline=OUT)
    d.line([(S * .4, S * .36), (S * .78, S * .36), (S * .82, S * .58), (S * .44, S * .58), (S * .4, S * .36)], fill=OUT, width=6)
    d.arc([S * .44, S * .46, S * .76, S * .86], 0, 180, fill=OUT, width=8)                                        # guard
    d.rectangle([S * .54, S * .56, S * .62, S * .72], fill=(220, 40, 40, 255), outline=OUT, width=3)             # trigger
    d.polygon([(S * .42, S * .4), (S * .04, S * .5), (S * .04, S * .56), (S * .42, S * .52)], fill=(200, 205, 215, 255), outline=OUT)
    d.line([(S * .42, S * .4), (S * .04, S * .5), (S * .04, S * .56), (S * .42, S * .52)], fill=OUT, width=5)      # spout
    return _shrink(im, size)


def front_door(size=64, flying=False):
    """A blue front door in its white frame: raised panels, a brass knob and knocker, a peephole - or (flying)
    the door alone, off its hinges, hinge plates showing."""
    im, d, S = _big(size)
    OUT = (20, 20, 40, 255)
    if not flying:
        d.rectangle([S * .12, S * .02, S * .88, S * .98], fill=(245, 245, 240, 255), outline=OUT, width=7)       # frame
    d.rectangle([S * .2, S * .08, S * .8, S * .98], fill=(40, 80, 170, 255), outline=OUT, width=7)
    for y0, y1 in ((.16, .46), (.56, .9)):
        d.rectangle([S * .28, S * y0, S * .48, S * y1], fill=(60, 100, 190, 255), outline=(20, 40, 110, 255), width=5)
        d.rectangle([S * .52, S * y0, S * .72, S * y1], fill=(60, 100, 190, 255), outline=(20, 40, 110, 255), width=5)
    d.ellipse([S * .64, S * .5, S * .74, S * .6], fill=(240, 190, 50, 255), outline=OUT, width=4)                # knob
    d.ellipse([S * .46, S * .2, S * .54, S * .28], fill=(30, 30, 40, 255), outline=(240, 190, 50, 255), width=3)   # peephole
    d.arc([S * .42, S * .3, S * .58, S * .44], 0, 180, fill=(240, 190, 50, 255), width=6)                         # knocker
    if flying:
        for y in (.2, .76):
            d.rectangle([S * .17, S * y, S * .23, S * (y + .08)], fill=(170, 170, 180, 255), outline=OUT, width=3)
    return _shrink(im, size)


def rental_scooter(size=64):
    """A green rental e-scooter seen from the side, facing right: tall stem, handlebar, low deck, two small
    wheels, a QR plate on the stem."""
    im, d, S = _big(size)
    OUT = (10, 30, 15, 255)
    G = (60, 200, 90, 255)
    d.line([(S * .14, S * .82), (S * .78, S * .82)], fill=OUT, width=int(S * .1))
    d.line([(S * .14, S * .82), (S * .78, S * .82)], fill=(40, 40, 46, 255), width=int(S * .06))                # deck
    d.line([(S * .76, S * .82), (S * .68, S * .14)], fill=OUT, width=int(S * .08))
    d.line([(S * .76, S * .82), (S * .68, S * .14)], fill=G, width=int(S * .05))                                 # stem
    d.line([(S * .56, S * .14), (S * .84, S * .12)], fill=OUT, width=10)                                          # handlebar
    d.rectangle([S * .66, S * .36, S * .78, S * .48], fill=(250, 250, 250, 255), outline=OUT, width=4)          # QR plate
    for x in (.18, .78):
        d.ellipse([S * (x - .09), S * .78, S * (x + .09), S * .96], fill=(30, 30, 34, 255), outline=OUT, width=5)
        d.ellipse([S * (x - .03), S * .84, S * (x + .03), S * .9], fill=G)
    return _shrink(im, size)


def battery_low(size=32, full=False):
    """A battery icon: red with one sliver of charge - or full green (turbo)."""
    im, d, S = _big(size)
    OUT = (20, 20, 20, 255)
    d.rounded_rectangle([S * .06, S * .26, S * .84, S * .74], 6, fill=(250, 250, 250, 255), outline=OUT, width=7)
    d.rectangle([S * .84, S * .4, S * .96, S * .6], fill=OUT)
    if full:
        d.rectangle([S * .14, S * .34, S * .76, S * .66], fill=(60, 220, 80, 255))
    else:
        d.rectangle([S * .14, S * .34, S * .24, S * .66], fill=(230, 30, 30, 255))
    return _shrink(im, size)


def loot_sack(size=32):
    """A tied canvas money sack with a big green $ on it."""
    im, d, S = _big(size)
    OUT = (50, 35, 15, 255)
    d.ellipse([S * .12, S * .3, S * .88, S * .96], fill=(210, 180, 120, 255), outline=OUT, width=7)
    d.polygon([(S * .36, S * .32), (S * .28, S * .06), (S * .5, S * .2), (S * .72, S * .06), (S * .64, S * .32)], fill=(210, 180, 120, 255), outline=OUT)
    d.rectangle([S * .34, S * .26, S * .66, S * .34], fill=(120, 80, 40, 255))
    im = _shrink(im, size)
    _big_text(im, "$", (16, 21), (40, 160, 60, 255), scale=1)
    return im


def bug_zapper(size=64, lit=True):
    """A porch bug zapper hanging from its hook: a black wire cage round a glowing purple-blue UV tube."""
    im, d, S = _big(size)
    OUT = (10, 10, 16, 255)
    d.arc([S * .42, S * .0, S * .58, S * .14], 180, 360, fill=OUT, width=6)                                       # hook
    d.line([(S * .5, S * .07), (S * .5, S * .16)], fill=OUT, width=6)
    d.rounded_rectangle([S * .24, S * .14, S * .76, S * .24], 6, fill=(40, 40, 46, 255), outline=OUT, width=5)
    d.rounded_rectangle([S * .24, S * .84, S * .76, S * .94], 6, fill=(40, 40, 46, 255), outline=OUT, width=5)
    glow = (140, 60, 255, 255) if lit else (80, 70, 100, 255)
    d.rectangle([S * .3, S * .24, S * .7, S * .84], fill=glow[:3] + (200,))
    d.rounded_rectangle([S * .42, S * .26, S * .58, S * .82], 8, fill=(230, 220, 255, 255) if lit else (120, 110, 140, 255), outline=glow, width=4)
    for k in range(7):
        x = .3 + k * .066
        d.line([(S * x, S * .24), (S * x, S * .84)], fill=(30, 30, 36, 255), width=3)                            # cage wires
    for y in (.4, .6):
        d.line([(S * .28, S * y), (S * .72, S * y)], fill=(30, 30, 36, 255), width=3)
    return _shrink(im, size)


def porch_moth(size=32):
    """A fuzzy brown moth, wings spread."""
    im, d, S = _big(size)
    OUT = (40, 30, 15, 255)
    for pts in (((.5, .5), (.06, .2), (.14, .7)), ((.5, .5), (.94, .2), (.86, .7))):
        _outline_poly(d, [(S * x, S * y) for x, y in pts], (180, 150, 100, 255), OUT, 6)
    for x in (.24, .76):
        d.ellipse([S * (x - .06), S * .36, S * (x + .06), S * .48], fill=(110, 80, 50, 255))
    d.ellipse([S * .42, S * .3, S * .58, S * .8], fill=(120, 90, 55, 255), outline=OUT, width=5)
    d.line([(S * .46, S * .32), (S * .36, S * .14)], fill=OUT, width=3)
    d.line([(S * .54, S * .32), (S * .64, S * .14)], fill=OUT, width=3)
    return _shrink(im, size)


def check_folder(size=64):
    """A restaurant check presenter, open: the black folder with the bill clipped in - TOTAL / $200 (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rounded_rectangle([S * .04, S * .14, S * .96, S * .86], 8, fill=(30, 30, 34, 255), outline=OUT, width=7)
    d.line([(S * .5, S * .16), (S * .5, S * .84)], fill=(70, 70, 76, 255), width=5)
    d.rectangle([S * .5, S * .2, S * .96, S * .8], fill=(250, 250, 245, 255), outline=OUT, width=4)             # the bill
    for y in (.56, .64, .72):
        d.line([(S * .56, S * y), (S * .9, S * y)], fill=(170, 170, 170, 255), width=3)
    d.rectangle([S * .12, S * .3, S * .4, S * .5], fill=(240, 240, 235, 255), outline=OUT, width=4)            # a card slot
    im = _shrink(im, size)
    return _texted(im, [("TOTAL", (47, 17)), ("$200", (47, 26))], (20, 20, 25, 255), (250, 250, 245, 255))


def receipt_half(size=32, right=False):
    """Half of a torn receipt: white paper, grey print lines, a ragged torn edge."""
    im, d, S = _big(size)
    OUT = (60, 60, 66, 255)
    pts = [(S * .2, S * .04), (S * .8, S * .04)]
    for k in range(8):
        pts.append((S * (.8 if k % 2 == 0 else .7), S * (.1 + k * .11)))
    pts += [(S * .2, S * .96)]
    if right:
        pts = [(S - x, y) for x, y in pts]
    _outline_poly(d, pts, (250, 250, 245, 255), OUT, 5)
    for y in (.2, .32, .44, .56, .7):
        x0, x1 = (.28, .6) if not right else (.4, .72)
        d.line([(S * x0, S * y), (S * x1, S * y)], fill=(170, 170, 170, 255), width=4)
    return _shrink(im, size)


# ---- set 24, batch 1 (INSANE): Full Auto, 18 Wheeler, Holy Fire, Sentencing, Clock Out --------------------------

def jam_pistol(size=64):
    """A black pistol, slide locked back (jammed), pointing right."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rectangle([S * .14, S * .34, S * .8, S * .48], fill=(50, 50, 56, 255), outline=OUT, width=6)               # slide
    d.rectangle([S * .74, S * .38, S * .92, S * .44], fill=(80, 80, 88, 255), outline=OUT, width=4)              # barrel out
    d.polygon([(S * .2, S * .48), (S * .42, S * .48), (S * .36, S * .86), (S * .16, S * .86)], fill=(40, 40, 46, 255), outline=OUT)
    d.line([(S * .2, S * .48), (S * .42, S * .48), (S * .36, S * .86), (S * .16, S * .86), (S * .2, S * .48)], fill=OUT, width=6)
    d.arc([S * .38, S * .46, S * .58, S * .66], 0, 180, fill=OUT, width=5)                                        # trigger guard
    d.line([(S * .2, S * .37), (S * .7, S * .37)], fill=(140, 140, 150, 255), width=3)
    return _shrink(im, size)


def mini_uzi(size=64):
    """A boxy black uzi: stubby barrel, the long magazine down through the grip, a folding stock."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rectangle([S * .2, S * .32, S * .78, S * .5], fill=(45, 45, 50, 255), outline=OUT, width=6)
    d.rectangle([S * .78, S * .38, S * .94, S * .44], fill=(70, 70, 78, 255), outline=OUT, width=4)
    d.rectangle([S * .42, S * .5, S * .54, S * .96], fill=(35, 35, 40, 255), outline=OUT, width=5)               # mag
    d.line([(S * .2, S * .36), (S * .04, S * .3), (S * .04, S * .5)], fill=(60, 60, 66, 255), width=6)          # stock
    d.line([(S * .24, S * .36), (S * .74, S * .36)], fill=(130, 130, 140, 255), width=3)
    return _shrink(im, size)


def minigun(size=64, phase=0):
    """A minigun on a tripod: six barrels in a rotary cluster (phase shifts the barrel shine so it spins), the
    motor housing, a brass ammo belt hanging off it, three tripod legs."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    for a, b in (((.36, .58), (.14, .96)), ((.36, .58), (.58, .96)), ((.36, .58), (.36, .96))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(60, 60, 66, 255), width=9)                     # tripod
    d.rounded_rectangle([S * .16, S * .3, S * .46, S * .6], 10, fill=(70, 75, 60, 255), outline=OUT, width=7)    # motor
    d.rectangle([S * .46, S * .32, S * .98, S * .56], fill=(55, 55, 60, 255), outline=OUT, width=6)              # barrels
    for k in range(6):
        y = .35 + k * .035
        c = (230, 230, 240, 255) if (k + phase) % 3 == 0 else (110, 110, 120, 255)
        d.line([(S * .48, S * y), (S * .96, S * y)], fill=c, width=3)
    for x in (.58, .8):
        d.rectangle([S * x, S * .3, S * (x + .04), S * .58], fill=(90, 90, 96, 255), outline=OUT, width=3)        # clamps
    for k in range(6):                                                                                             # ammo belt
        d.rectangle([S * (.2 - k * .02), S * (.6 + k * .06), S * (.28 - k * .02), S * (.66 + k * .06)], fill=(230, 180, 60, 255), outline=OUT, width=3)
    d.rectangle([S * .22, S * .18, S * .3, S * .3], fill=(40, 40, 46, 255), outline=OUT, width=4)                # handle
    return _shrink(im, size)


def tracer_streak(n=16):
    """A hot bullet tracer (alpha only): a bright horizontal streak, thicker at the head."""
    def f(x, y):
        w = .6 + x / 16 * 1.4
        return max(0, 1 - abs(y - 7.5) / w) * (x / 15) if x > 1 else 0
    return _alpha(n, n, f)


def brass_shell(n=16):
    """A spent brass casing (alpha only)."""
    return _alpha(n, n, lambda x, y: 1 if 5 <= x <= 10 and 4 <= y <= 12 and not (y < 6 and (x == 5 or x == 10)) else 0)


def muzzle_star(size=32):
    """A big blinding muzzle flash: white core, yellow-orange spikes."""
    import math
    im, d, S = _big(size)
    pts = []
    for k in range(14):
        a = k * 2 * math.pi / 14
        r = .48 if k % 2 == 0 else .18
        pts.append((S * (.5 + r * math.cos(a)), S * (.5 + r * .7 * math.sin(a))))
    d.polygon(pts, fill=(255, 170, 30, 255))
    d.ellipse([S * .3, S * .36, S * .7, S * .64], fill=(255, 240, 120, 255))
    d.ellipse([S * .38, S * .42, S * .62, S * .58], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def semi_truck(size=64):
    """An 18-wheeler facing right: a long silver trailer, a big red cab with a chrome grille, twin exhaust stacks,
    a row of wheels (drawn on a wide canvas: the art fills the width, ~45% of the height)."""
    im, d, S = _big(size)
    OUT = (15, 10, 10, 255)
    y0, y1 = .3, .74
    d.rectangle([S * .02, S * y0, S * .66, S * (y1 - .06)], fill=(215, 220, 230, 255), outline=OUT, width=6)     # trailer
    d.line([(S * .04, S * (y0 + .06)), (S * .64, S * (y0 + .06))], fill=(255, 255, 255, 255), width=4)
    for x in (.2, .4):
        d.line([(S * x, S * y0), (S * x, S * (y1 - .06))], fill=(160, 165, 175, 255), width=3)
    d.rectangle([S * .66, S * (y0 + .08), S * .9, S * (y1 - .04)], fill=(210, 30, 30, 255), outline=OUT, width=6)  # cab
    d.polygon([(S * .74, S * (y0 + .1)), (S * .86, S * (y0 + .1)), (S * .86, S * (y0 + .22)), (S * .74, S * (y0 + .22))], fill=(120, 190, 240, 255), outline=OUT)
    d.rectangle([S * .9, S * (y0 + .14), S * .99, S * (y1 - .04)], fill=(200, 205, 215, 255), outline=OUT, width=5)  # grille
    for k in range(4):
        d.line([(S * .91, S * (y0 + .18 + k * .06)), (S * .98, S * (y0 + .18 + k * .06))], fill=(120, 120, 130, 255), width=3)
    d.ellipse([S * .955, S * (y1 - .14), S * .99, S * (y1 - .09)], fill=(255, 250, 200, 255))                     # headlight
    for x in (.68, .72):
        d.rectangle([S * x, S * (y0 - .12), S * (x + .025), S * (y0 + .08)], fill=(200, 205, 215, 255), outline=OUT, width=3)  # stacks
    for x in (.08, .16, .5, .58, .78, .9):
        d.ellipse([S * (x - .05), S * (y1 - .1), S * (x + .05), S * y1 + S * .02], fill=(25, 25, 28, 255), outline=OUT, width=4)
        d.ellipse([S * (x - .02), S * (y1 - .06), S * (x + .02), S * (y1 - .02)], fill=(180, 180, 190, 255))
    return _shrink(im, size)


def stained_glass(size=64, lit=False):
    """An arched church window of coloured glass in lead lines (a cross in the middle); lit = blazing bright."""
    im, d, S = _big(size)
    OUT = (30, 25, 20, 255)
    k = 1.0 if lit else .7
    cols = [(220, 40, 60), (40, 90, 220), (250, 200, 40), (60, 170, 80), (160, 60, 200)]
    d.rounded_rectangle([S * .14, S * .04, S * .86, S * .96], int(S * .36), fill=(60, 50, 40, 255), outline=OUT, width=8)
    i = 0
    for y in range(4):
        for x in range(3):
            c = cols[i % len(cols)]
            i += 1
            c = tuple(min(255, int(v * k + (60 if lit else 0))) for v in c) + (255,)
            d.rectangle([S * (.22 + x * .19), S * (.2 + y * .19), S * (.39 + x * .19), S * (.37 + y * .19)], fill=c, outline=OUT, width=4)
    d.pieslice([S * .22, S * .1, S * .78, S * .5], 180, 360, fill=(250, 220, 120, 255) if lit else (200, 170, 90, 255), outline=OUT, width=4)
    d.rectangle([S * .46, S * .26, S * .54, S * .86], fill=(255, 245, 210, 255) if lit else (220, 210, 180, 255), outline=OUT, width=3)
    d.rectangle([S * .34, S * .42, S * .66, S * .5], fill=(255, 245, 210, 255) if lit else (220, 210, 180, 255), outline=OUT, width=3)
    return _shrink(im, size)


def holy_ray(n=16):
    """A soft vertical shaft of light (alpha only)."""
    return _alpha(n, n, lambda x, y: max(0, 1 - abs(x - 7.5) / 6.5) ** 1.5)


def gold_halo(size=32):
    """A glowing gold halo ring seen at an angle."""
    im, d, S = _big(size)
    d.ellipse([S * .06, S * .32, S * .94, S * .68], outline=(140, 90, 0, 255), width=int(S * .12))
    d.ellipse([S * .08, S * .34, S * .92, S * .66], outline=(255, 220, 60, 255), width=int(S * .07))
    d.arc([S * .12, S * .36, S * .88, S * .64], 190, 260, fill=(255, 255, 220, 255), width=5)
    return _shrink(im, size)


def judge_gavel(size=64):
    """A judge's wooden gavel, head at the top right, handle down-left, brass bands, on its sound block."""
    im, d, S = _big(size)
    OUT = (40, 20, 5, 255)
    W, WD = (160, 95, 45, 255), (110, 60, 25, 255)
    d.line([(S * .2, S * .86), (S * .6, S * .38)], fill=OUT, width=int(S * .12))
    d.line([(S * .2, S * .86), (S * .6, S * .38)], fill=W, width=int(S * .08))                                   # handle
    head = [(S * .42, S * .3), (S * .7, S * .06), (S * .96, S * .34), (S * .68, S * .58)]
    d.polygon(head, fill=W)
    d.line(head + [head[0]], fill=OUT, width=7)
    for t in (.3, .7):
        a = (head[0][0] + (head[1][0] - head[0][0]) * t, head[0][1] + (head[1][1] - head[0][1]) * t)
        b = (head[3][0] + (head[2][0] - head[3][0]) * t, head[3][1] + (head[2][1] - head[3][1]) * t)
        d.line([a, b], fill=(230, 180, 60, 255), width=6)                                                          # brass bands
    d.line([(S * .5, S * .26), (S * .74, S * .1)], fill=(210, 150, 90, 255), width=4)
    return _shrink(im, size)


def time_clock(size=64, t="4:58"):
    """A punch time clock on the wall: grey box, a red digital readout (shown at 1:1), the card slot and a rack of
    time cards beside it."""
    im, d, S = _big(size)
    OUT = (20, 20, 26, 255)
    d.rounded_rectangle([S * .08, S * .1, S * .74, S * .9], 10, fill=(180, 185, 195, 255), outline=OUT, width=8)
    d.rectangle([S * .16, S * .2, S * .66, S * .44], fill=(20, 10, 10, 255), outline=OUT, width=5)               # display
    d.rectangle([S * .24, S * .58, S * .58, S * .66], fill=(30, 30, 36, 255))                                      # card slot
    d.rectangle([S * .78, S * .18, S * .96, S * .86], fill=(120, 90, 60, 255), outline=OUT, width=5)            # card rack
    for k in range(4):
        d.rectangle([S * .8, S * (.22 + k * .16), S * .94, S * (.32 + k * .16)], fill=(250, 245, 220, 255), outline=OUT, width=3)
    im = _shrink(im, size)
    _big_text(im, t, (26, 21), (255, 50, 40, 255) if t != "5:00" else (80, 255, 120, 255), scale=2)
    return im


def punch_card(size=32):
    """A buff time card with ruled lines."""
    im, d, S = _big(size)
    OUT = (60, 50, 30, 255)
    d.rectangle([S * .28, S * .04, S * .72, S * .96], fill=(250, 240, 200, 255), outline=OUT, width=6)
    for k in range(6):
        d.line([(S * .34, S * (.18 + k * .13)), (S * .66, S * (.18 + k * .13))], fill=(180, 160, 120, 255), width=4)
    d.rectangle([S * .28, S * .04, S * .72, S * .14], fill=(220, 60, 60, 255), outline=OUT, width=5)
    return _shrink(im, size)


def wall_clock(size=32):
    """A round white wall clock with a black rim and two hands (spins as a particle; no text)."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.ellipse([S * .06, S * .06, S * .94, S * .94], fill=(250, 250, 250, 255), outline=OUT, width=int(S * .09))
    for k in range(12):
        import math
        a = k * math.pi / 6
        d.line([(S * (.5 + .34 * math.cos(a)), S * (.5 + .34 * math.sin(a))), (S * (.5 + .4 * math.cos(a)), S * (.5 + .4 * math.sin(a)))], fill=OUT, width=4)
    d.line([(S * .5, S * .5), (S * .5, S * .2)], fill=OUT, width=6)
    d.line([(S * .5, S * .5), (S * .72, S * .58)], fill=(220, 30, 30, 255), width=5)
    return _shrink(im, size)


def holy_flame(n=16):
    """A small teardrop flame lick (alpha only, 16x16): pointed top, round bottom."""
    def f(x, y):
        dx = abs(x - 7.5)
        if y > 9:
            return max(0, 1 - ((dx / 5) ** 2 + ((y - 9.5) / 5) ** 2))
        half = 5 * (y - 1) / 8.5
        return max(0, 1 - dx / max(half, .1)) if y > 1 else 0
    return _alpha(n, n, f)


# ---- set 24, batch 2 (INSANE): Rip Space, Ghost Ride, Mind Blown, Bad Omen, Compactor -----------------------------

SMALL["="] = "...|###|...|###|...|..."


def _galaxy(d, S, box):
    """Paint a little piece of outer space into box (x0, y0, x1, y1): deep purple, a pink-blue nebula, stars."""
    import random
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(20, 10, 45, 255))
    d.ellipse([x0 + (x1 - x0) * .1, y0 + (y1 - y0) * .2, x0 + (x1 - x0) * .9, y0 + (y1 - y0) * .55], fill=(110, 40, 150, 255))
    d.ellipse([x0 + (x1 - x0) * .25, y0 + (y1 - y0) * .45, x0 + (x1 - x0) * .8, y0 + (y1 - y0) * .8], fill=(40, 90, 190, 255))
    r = random.Random(7)
    for _ in range(int((x1 - x0) * (y1 - y0) / (S * S) * 60) + 4):
        x, y = r.uniform(x0, x1), r.uniform(y0, y1)
        s = r.choice((2, 3, 5))
        d.ellipse([x - s, y - s, x + s, y + s], fill=(255, 255, 255, 255))


def space_zipper(size=64, opened=0):
    """A giant zipper running down the screen: opened 0 = zipped shut, 1 = the pull a third of the way down with a
    sliver of outer space showing, 2 = all the way down, a wide V of galaxy between the two rows of teeth."""
    im, d, S = _big(size)
    OUT = (20, 20, 26, 255)
    TEETH = (200, 170, 60, 255)
    pull_y = (.08, .38, .9)[opened]
    gap = (0, .1, .34)[opened]
    if opened:
        poly = [(S * .5, S * pull_y), (S * (.5 - gap), S * .02), (S * (.5 + gap), S * .02)]
        mask = Image.new("L", (S, S), 0)
        ImageDraw.Draw(mask).polygon(poly, fill=255)
        sp = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        _galaxy(ImageDraw.Draw(sp), S, (0, 0, S, S))
        im.paste(sp, (0, 0), mask)
    for k in range(24):
        y = .02 + k * .04
        if y < pull_y and opened:
            t = (pull_y - y) / max(pull_y - .02, .01)
            for sgn in (-1, 1):
                x = .5 + sgn * (gap * t + .02)
                d.rectangle([S * (x - .03), S * y, S * (x + .03), S * (y + .025)], fill=TEETH, outline=OUT, width=3)
        else:
            d.rectangle([S * (.47 if k % 2 else .5), S * y, S * (.5 if k % 2 else .53), S * (y + .03)], fill=TEETH, outline=OUT, width=3)
    d.rounded_rectangle([S * .42, S * (pull_y - .04), S * .58, S * (pull_y + .06)], 6, fill=(220, 220, 230, 255), outline=OUT, width=5)
    d.rounded_rectangle([S * .45, S * (pull_y + .05), S * .55, S * (pull_y + .2)], 8, fill=(200, 200, 210, 255), outline=OUT, width=5)
    d.ellipse([S * .48, S * (pull_y + .12), S * .52, S * (pull_y + .16)], fill=OUT)
    return _shrink(im, size)


def sheet_ghost(size=64):
    """A kid's Halloween ghost: a white bedsheet with two cut-out eye holes, wrinkles, the ragged hem."""
    im, d, S = _big(size)
    OUT = (60, 60, 80, 255)
    pts = [(S * .5, S * .06), (S * .78, S * .22), (S * .86, S * .9), (S * .76, S * .84), (S * .66, S * .94), (S * .56, S * .86),
           (S * .46, S * .95), (S * .36, S * .86), (S * .26, S * .94), (S * .14, S * .88), (S * .22, S * .22)]
    d.polygon(pts, fill=(250, 250, 255, 255))
    d.line(pts + [pts[0]], fill=OUT, width=7)
    for x in (.36, .56):
        d.ellipse([S * x, S * .3, S * (x + .1), S * .44], fill=(15, 15, 25, 255))
    for a, b in (((.3, .55), (.36, .8)), ((.66, .5), (.62, .78))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(200, 200, 220, 255), width=4)
    return _shrink(im, size)


def minivan(size=64, doors_open=True):
    """A beige soccer-mom minivan facing right, sliding door wide open and nobody in it (ghost riding the whip)."""
    im, d, S = _big(size)
    OUT = (30, 25, 20, 255)
    BODY = (220, 200, 160, 255)
    y0, y1 = .34, .72
    d.polygon([(S * .04, S * (y0 + .02)), (S * .62, S * y0), (S * .84, S * (y0 + .14)), (S * .96, S * (y0 + .2)), (S * .96, S * y1),
               (S * .04, S * y1)], fill=BODY, outline=OUT)
    d.line([(S * .04, S * (y0 + .02)), (S * .62, S * y0), (S * .84, S * (y0 + .14)), (S * .96, S * (y0 + .2)), (S * .96, S * y1),
            (S * .04, S * y1), (S * .04, S * (y0 + .02))], fill=OUT, width=6)
    for x0, x1 in ((.08, .24), (.62, .8)):
        d.rectangle([S * x0, S * (y0 + .05), S * x1, S * (y0 + .15)], fill=(110, 150, 190, 255), outline=OUT, width=4)
    if doors_open:
        d.rectangle([S * .3, S * (y0 + .04), S * .56, S * (y1 - .04)], fill=(40, 35, 40, 255), outline=OUT, width=4)   # empty inside
        d.rectangle([S * .14, S * (y0 + .04), S * .3, S * (y1 - .04)], fill=(205, 185, 145, 255), outline=OUT, width=4)  # slid door
    d.line([(S * .04, S * (y1 - .1)), (S * .96, S * (y1 - .1))], fill=(170, 150, 110, 255), width=4)
    d.rectangle([S * .9, S * (y0 + .26), S * .96, S * (y0 + .3)], fill=(255, 250, 200, 255))
    for x in (.2, .78):
        d.ellipse([S * (x - .08), S * (y1 - .08), S * (x + .08), S * (y1 + .08)], fill=(25, 25, 28, 255), outline=OUT, width=4)
        d.ellipse([S * (x - .03), S * (y1 - .03), S * (x + .03), S * (y1 + .03)], fill=(170, 170, 180, 255))
    return _shrink(im, size)


def math_board(size=64, text="2+2=4"):
    """A green classroom chalkboard in a wooden frame with a chalk tray, one line of chalk math (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 25, 10, 255)
    d.rectangle([S * .02, S * .16, S * .98, S * .8], fill=(150, 100, 50, 255), outline=OUT, width=7)
    d.rectangle([S * .08, S * .22, S * .92, S * .74], fill=(40, 90, 60, 255))
    d.rectangle([S * .06, S * .78, S * .94, S * .84], fill=(170, 120, 60, 255), outline=OUT, width=4)
    d.rectangle([S * .7, S * .74, S * .8, S * .78], fill=(250, 250, 245, 255))                                       # chalk
    d.line([(S * .14, S * .64), (S * .4, S * .66)], fill=(110, 150, 120, 255), width=4)                             # smudge
    im = _shrink(im, size)
    _big_text(im, text, (32, 28), (245, 245, 235, 255), scale=2, font=SMALL)
    return im


def question_mark(size=32):
    """A fat purple question mark with a white outline."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    _big_text(im, "?", (16, 16), (170, 80, 230, 255), scale=3)
    return im


def galaxy_burst(size=64):
    """MIND BLOWN: a ragged burst of outer space - purple, pink and blue swirls, stars, a white-hot centre."""
    import math
    im, d, S = _big(size)
    pts = []
    for k in range(22):
        a = k * 2 * math.pi / 22
        r = .47 if k % 2 == 0 else .33
        pts.append((S * (.5 + r * math.cos(a)), S * (.5 + r * math.sin(a))))
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).polygon(pts, fill=255)
    sp = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sp)
    _galaxy(sd, S, (0, 0, S, S))
    for k in range(3):
        sd.arc([S * (.2 + k * .08), S * (.2 + k * .08), S * (.8 - k * .08), S * (.8 - k * .08)], k * 90, k * 90 + 200,
               fill=((255, 120, 220, 255), (120, 220, 255, 255), (255, 240, 140, 255))[k], width=8)
    sd.ellipse([S * .42, S * .42, S * .58, S * .58], fill=(255, 255, 255, 255))
    im.paste(sp, (0, 0), mask)
    d.line(pts + [pts[0]], fill=(255, 255, 255, 255), width=5)
    return _shrink(im, size)


def black_cat(size=64, step=0):
    """A black cat walking left to right, tail up, yellow eyes; step 0/1 swaps the legs."""
    im, d, S = _big(size)
    C = (25, 22, 30, 255)
    d.ellipse([S * .22, S * .42, S * .72, S * .68], fill=C)                                                             # body
    d.ellipse([S * .64, S * .3, S * .88, S * .52], fill=C)                                                              # head
    d.polygon([(S * .66, S * .34), (S * .68, S * .2), (S * .74, S * .32)], fill=C)
    d.polygon([(S * .78, S * .32), (S * .84, S * .2), (S * .86, S * .36)], fill=C)
    d.line([(S * .24, S * .5), (S * .1, S * .36), (S * .12, S * .14)], fill=C, width=int(S * .06))                     # tail
    legs = ((.3, .44), (.56, .7)) if step == 0 else ((.36, .38), (.62, .66))
    for a, b in legs:
        d.line([(S * a, S * .62), (S * (a - .04), S * .86)], fill=C, width=int(S * .06))
        d.line([(S * b, S * .62), (S * (b + .04), S * .86)], fill=C, width=int(S * .06))
    for x in (.72, .8):
        d.ellipse([S * x, S * .37, S * (x + .05), S * .43], fill=(250, 220, 40, 255))
    return _shrink(im, size)


def hand_mirror(size=64, cracked=False):
    """A pink hand mirror (oval glass, handle) - or cracked right across."""
    im, d, S = _big(size)
    OUT = (60, 20, 40, 255)
    d.line([(S * .5, S * .62), (S * .5, S * .96)], fill=OUT, width=int(S * .12))
    d.line([(S * .5, S * .62), (S * .5, S * .96)], fill=(240, 120, 170, 255), width=int(S * .08))
    d.ellipse([S * .2, S * .04, S * .8, S * .66], fill=(240, 120, 170, 255), outline=OUT, width=7)
    d.ellipse([S * .27, S * .1, S * .73, S * .6], fill=(200, 230, 250, 255), outline=OUT, width=4)
    d.line([(S * .35, S * .2), (S * .45, S * .14)], fill=(255, 255, 255, 255), width=5)
    if cracked:
        for a, b in (((.5, .34), (.3, .18)), ((.5, .34), (.7, .14)), ((.5, .34), (.34, .56)), ((.5, .34), (.68, .52)), ((.5, .34), (.72, .34))):
            d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(40, 40, 60, 255), width=4)
    return _shrink(im, size)


def falling_star(size=64):
    """A huge shooting star coming down from the top-right: a fat gold star with a white core and a long rainbow trail."""
    import math
    im, d, S = _big(size)
    for k, c in enumerate(((255, 120, 200), (255, 220, 80), (120, 220, 255))):
        o = (k - 1) * .05
        d.line([(S * (.62 + o), S * (.38 - o)), (S * (.98 + o), S * (.02 - o))], fill=c + (220,), width=int(S * .06))
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        r = .3 if k % 2 == 0 else .13
        pts.append((S * (.4 + r * math.cos(a)), S * (.6 + r * math.sin(a))))
    _outline_poly(d, pts, (255, 220, 50, 255), (160, 100, 0, 255), 8)
    d.ellipse([S * .34, S * .54, S * .46, S * .66], fill=(255, 255, 230, 255))
    return _shrink(im, size)


def compactor_plate(size=64):
    """One wall of a junkyard compactor: a riveted steel plate with yellow-black hazard stripes and a hydraulic
    piston sticking out the back (the left side)."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rectangle([S * .02, S * .44, S * .4, S * .56], fill=(170, 175, 185, 255), outline=OUT, width=6)              # piston
    d.rectangle([S * .4, S * .04, S * .72, S * .96], fill=(120, 125, 135, 255), outline=OUT, width=8)
    for k in range(6):
        y = .1 + k * .15
        d.polygon([(S * .66, S * y), (S * .72, S * (y - .06)), (S * .72, S * (y + .02)), (S * .66, S * (y + .08))], fill=(250, 200, 30, 255))
    d.line([(S * .72, S * .04), (S * .72, S * .96)], fill=OUT, width=6)
    for y in (.12, .5, .88):
        for x in (.46, .6):
            d.ellipse([S * x, S * (y - .02), S * (x + .04), S * (y + .02)], fill=(200, 205, 215, 255), outline=OUT, width=2)
    return _shrink(im, size)


def junk_cube(size=64):
    """A crushed cube of compacted junk: dented metal, a squashed hubcap, a sneaker sticking out, a soda can."""
    im, d, S = _big(size)
    OUT = (20, 20, 24, 255)
    d.polygon([(S * .14, S * .3), (S * .5, S * .14), (S * .9, S * .28), (S * .9, S * .82), (S * .52, S * .96), (S * .14, S * .82)], fill=(110, 110, 120, 255))
    d.polygon([(S * .14, S * .3), (S * .5, S * .44), (S * .52, S * .96), (S * .14, S * .82)], fill=(140, 140, 150, 255))
    d.polygon([(S * .14, S * .3), (S * .5, S * .14), (S * .9, S * .28), (S * .5, S * .44)], fill=(170, 170, 180, 255))
    for pts in (((.14, .3), (.5, .14), (.9, .28), (.9, .82), (.52, .96), (.14, .82), (.14, .3)), ((.14, .3), (.5, .44), (.9, .28)), ((.5, .44), (.52, .96))):
        d.line([(S * x, S * y) for x, y in pts], fill=OUT, width=6)
    d.ellipse([S * .2, S * .5, S * .38, S * .66], fill=(210, 210, 220, 255), outline=OUT, width=4)                 # hubcap
    d.rectangle([S * .62, S * .5, S * .74, S * .7], fill=(220, 40, 40, 255), outline=OUT, width=3)                 # can
    d.polygon([(S * .64, S * .24), (S * .84, S * .2), (S * .86, S * .3), (S * .7, S * .34)], fill=(250, 250, 250, 255), outline=OUT)   # sneaker
    for a, b in (((.3, .74), (.44, .8)), ((.6, .78), (.8, .72))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(80, 80, 88, 255), width=4)                     # dents
    return _shrink(im, size)


# ---- set 24, batch 3: Flamin Hot, Air Strike, Brick Wall, Triple Tap, Nail Gun, Staple Gun -------------------------

def hot_chips(size=64):
    """A red bag of flaming-hot chips: crimped top, flames up the front, HOT in big letters (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (60, 10, 0, 255)
    d.polygon([(S * .18, S * .14), (S * .82, S * .14), (S * .88, S * .9), (S * .12, S * .9)], fill=(220, 30, 20, 255))
    d.line([(S * .18, S * .14), (S * .82, S * .14), (S * .88, S * .9), (S * .12, S * .9), (S * .18, S * .14)], fill=OUT, width=7)
    d.rectangle([S * .16, S * .06, S * .84, S * .16], fill=(200, 20, 10, 255), outline=OUT, width=5)
    for k in range(7):
        d.line([(S * (.2 + k * .1), S * .07), (S * (.2 + k * .1), S * .15)], fill=OUT, width=3)
    for x, h in ((.24, .4), (.4, .3), (.56, .42), (.72, .32)):
        d.polygon([(S * (x - .08), S * .9), (S * x, S * (.9 - h)), (S * (x + .08), S * .9)], fill=(255, 160, 30, 255))
        d.polygon([(S * (x - .04), S * .9), (S * x, S * (.9 - h * .6)), (S * (x + .04), S * .9)], fill=(255, 240, 80, 255))
    d.rectangle([S * .12, S * .86, S * .88, S * .92], fill=(200, 20, 10, 255))
    im = _shrink(im, size)
    _big_text(im, "HOT", (32, 22), (255, 240, 60, 255), scale=2, font=SMALL)
    return im


def hot_chip(size=32):
    """One curly red-hot cheese puff, dusted with red powder."""
    im, d, S = _big(size)
    OUT = (90, 10, 0, 255)
    d.arc([S * .1, S * .2, S * .9, S * .9], 200, 20, fill=OUT, width=int(S * .26))
    d.arc([S * .12, S * .22, S * .88, S * .88], 200, 20, fill=(230, 40, 20, 255), width=int(S * .2))
    for x, y in ((.24, .5), (.5, .26), (.78, .4)):
        d.ellipse([S * (x - .04), S * (y - .04), S * (x + .04), S * (y + .04)], fill=(255, 120, 80, 255))
    return _shrink(im, size)


def bread_slice(size=32):
    """A slice of white bread: tan crust, puffy top."""
    im, d, S = _big(size)
    OUT = (110, 70, 20, 255)
    d.rounded_rectangle([S * .14, S * .36, S * .86, S * .92], 8, fill=(240, 225, 190, 255), outline=(190, 130, 60, 255), width=int(S * .08))
    d.ellipse([S * .1, S * .1, S * .5, S * .5], fill=(240, 225, 190, 255), outline=(190, 130, 60, 255), width=int(S * .08))
    d.ellipse([S * .5, S * .1, S * .9, S * .5], fill=(240, 225, 190, 255), outline=(190, 130, 60, 255), width=int(S * .08))
    d.rectangle([S * .22, S * .36, S * .78, S * .5], fill=(240, 225, 190, 255))
    for x, y in ((.36, .58), (.6, .7), (.48, .44)):
        d.ellipse([S * x, S * y, S * (x + .04), S * (y + .04)], fill=(210, 190, 150, 255))
    return _shrink(im, size)


def bread_loaf(size=64):
    """A whole sliced loaf in its plastic bag with the twist tie."""
    im, d, S = _big(size)
    OUT = (110, 70, 20, 255)
    d.rounded_rectangle([S * .06, S * .3, S * .82, S * .8], 22, fill=(225, 175, 100, 255), outline=OUT, width=7)
    for k in range(6):
        x = .18 + k * .11
        d.line([(S * x, S * .34), (S * x, S * .76)], fill=(190, 140, 70, 255), width=3)
    d.rounded_rectangle([S * .04, S * .26, S * .84, S * .84], 24, outline=(220, 230, 250, 200), width=5)          # bag
    d.polygon([(S * .84, S * .5), (S * .96, S * .38), (S * .96, S * .66)], fill=(230, 235, 250, 200))
    d.rectangle([S * .82, S * .48, S * .88, S * .58], fill=(40, 120, 220, 255))                                     # twist tie
    return _shrink(im, size)


def pigeon_dive(size=32):
    """A grey city pigeon diving down-right: wings swept back, the green-purple neck shine, orange eye."""
    im, d, S = _big(size)
    OUT = (30, 30, 40, 255)
    d.polygon([(S * .1, S * .1), (S * .5, S * .44), (S * .2, S * .48)], fill=(120, 125, 140, 255), outline=OUT)    # wing
    d.ellipse([S * .3, S * .36, S * .82, S * .74], fill=(150, 155, 170, 255), outline=OUT, width=5)                # body
    d.ellipse([S * .66, S * .6, S * .92, S * .86], fill=(110, 115, 130, 255), outline=OUT, width=5)                # head
    d.arc([S * .6, S * .5, S * .86, S * .76], 90, 200, fill=(90, 170, 130, 255), width=6)                          # neck shine
    d.ellipse([S * .76, S * .68, S * .82, S * .74], fill=(250, 140, 30, 255))
    d.polygon([(S * .88, S * .78), (S * .98, S * .9), (S * .84, S * .86)], fill=(60, 60, 66, 255))                  # beak
    d.polygon([(S * .3, S * .5), (S * .06, S * .62), (S * .3, S * .62)], fill=(100, 105, 120, 255), outline=OUT)   # tail
    return _shrink(im, size)


def brick_wall(size=64, rows=3, tipped=0):
    """A red brick wall built up 1-3 courses from the bottom, grey mortar; tipped = degrees it's falling over."""
    im, d, S = _big(size)
    OUT = (60, 20, 15, 255)
    for r in range(rows):
        y1 = .96 - r * .2
        y0 = y1 - .2
        off = 0 if r % 2 == 0 else .12
        x = .04 - off
        while x < .96:
            a, b = max(x, .04), min(x + .24, .96)
            if b - a > .04:
                d.rectangle([S * a, S * y0, S * b, S * y1], fill=(180, 60, 40, 255), outline=(150, 150, 150, 255), width=6)
                d.line([(S * (a + .02), S * (y0 + .04)), (S * (b - .03), S * (y0 + .04))], fill=(220, 110, 80, 255), width=3)
            x += .24
    d.rectangle([S * .04, S * (.96 - rows * .2), S * .96, S * .96], outline=OUT, width=5)
    if tipped:
        im = im.rotate(-tipped, center=(S * .5, S * .96), resample=Image.BICUBIC)
    return _shrink(im, size)


def tap_shoe(size=64):
    """A black patent tap-dance shoe with a ribbon bow and the silver tap plates on the toe and heel."""
    im, d, S = _big(size)
    OUT = (10, 10, 14, 255)
    d.polygon([(S * .08, S * .36), (S * .36, S * .36), (S * .6, S * .5), (S * .9, S * .54), (S * .94, S * .68), (S * .08, S * .68)],
              fill=(25, 25, 30, 255))
    d.line([(S * .08, S * .36), (S * .36, S * .36), (S * .6, S * .5), (S * .9, S * .54), (S * .94, S * .68), (S * .08, S * .68), (S * .08, S * .36)], fill=OUT, width=6)
    d.line([(S * .14, S * .42), (S * .34, S * .42)], fill=(140, 140, 160, 255), width=4)                            # shine
    d.ellipse([S * .46, S * .36, S * .58, S * .48], fill=(220, 30, 40, 255), outline=OUT, width=3)                 # bow
    d.rectangle([S * .58, S * .68, S * .94, S * .76], fill=(210, 215, 225, 255), outline=OUT, width=4)             # toe tap
    d.rectangle([S * .08, S * .68, S * .26, S * .8], fill=(210, 215, 225, 255), outline=OUT, width=4)              # heel tap
    return _shrink(im, size)


def nail_gun(size=64):
    """A yellow and black pneumatic nail gun pointing right: the long magazine of nails underneath, the air hose."""
    im, d, S = _big(size)
    OUT = (20, 15, 5, 255)
    d.rounded_rectangle([S * .2, S * .24, S * .86, S * .46], 10, fill=(250, 200, 30, 255), outline=OUT, width=6)
    d.rectangle([S * .82, S * .3, S * .96, S * .58], fill=(60, 60, 66, 255), outline=OUT, width=5)                 # nose
    d.polygon([(S * .3, S * .46), (S * .44, S * .46), (S * .38, S * .82), (S * .24, S * .82)], fill=(40, 40, 46, 255), outline=OUT)   # grip
    d.line([(S * .3, S * .46), (S * .44, S * .46), (S * .38, S * .82), (S * .24, S * .82), (S * .3, S * .46)], fill=OUT, width=5)
    d.rectangle([S * .48, S * .46, S * .9, S * .58], fill=(170, 175, 185, 255), outline=OUT, width=4)             # magazine
    for k in range(6):
        d.line([(S * (.52 + k * .06), S * .48), (S * (.52 + k * .06), S * .56)], fill=(90, 90, 100, 255), width=3)
    d.line([(S * .26, S * .82), (S * .1, S * .96)], fill=(220, 40, 40, 255), width=6)                              # hose
    return _shrink(im, size)


def nail_streak(n=16):
    """A flying nail (alpha only): a thin shaft with a flat head at the back."""
    return _alpha(n, n, lambda x, y: 1 if (2 <= x <= 14 and 7 <= y <= 8) or (x in (2, 3) and 5 <= y <= 10) else 0)


def staple_gun(size=64):
    """A big chrome-and-black office staple gun (the heavy-duty kind) pointing right."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.polygon([(S * .1, S * .5), (S * .86, S * .5), (S * .9, S * .66), (S * .1, S * .66)], fill=(200, 205, 215, 255), outline=OUT)   # base
    d.line([(S * .1, S * .5), (S * .86, S * .5), (S * .9, S * .66), (S * .1, S * .66), (S * .1, S * .5)], fill=OUT, width=6)
    d.polygon([(S * .14, S * .5), (S * .3, S * .22), (S * .84, S * .3), (S * .84, S * .48)], fill=(40, 40, 46, 255), outline=OUT)   # handle
    d.line([(S * .14, S * .5), (S * .3, S * .22), (S * .84, S * .3), (S * .84, S * .48)], fill=OUT, width=6)
    d.line([(S * .34, S * .3), (S * .78, S * .36)], fill=(120, 120, 130, 255), width=4)
    d.rectangle([S * .84, S * .56, S * .92, S * .66], fill=(230, 60, 40, 255), outline=OUT, width=3)
    return _shrink(im, size)


def staple_bit(n=16):
    """A flying staple (alpha only): a little squared-off U."""
    return _alpha(n, n, lambda x, y: 1 if ((x in (4, 5, 11, 12) and 5 <= y <= 11) or (4 <= x <= 12 and y in (5, 6))) else 0)


def stuck_staple(size=32):
    """A big silver staple stuck in something (shown on the foe)."""
    im, d, S = _big(size)
    OUT = (40, 40, 50, 255)
    d.line([(S * .2, S * .7), (S * .2, S * .34), (S * .8, S * .34), (S * .8, S * .7)], fill=OUT, width=int(S * .14))
    d.line([(S * .2, S * .7), (S * .2, S * .34), (S * .8, S * .34), (S * .8, S * .7)], fill=(220, 225, 235, 255), width=int(S * .08))
    return _shrink(im, size)


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


# ---- set 24, batch 5: Snap Out, Lint Trap, Bait Switch, The Wobble, Claw Machine --------------------------------------

def gym_sock(size=64):
    """A crusty white tube sock with red and blue stripes, a yellowed toe, green stink lines rising off it."""
    im, d, S = _big(size)
    OUT = (60, 60, 50, 255)
    d.line([(S * .5, S * .14), (S * .5, S * .62), (S * .7, S * .82)], fill=OUT, width=int(S * .26))
    d.line([(S * .5, S * .14), (S * .5, S * .62), (S * .7, S * .82)], fill=(245, 245, 235, 255), width=int(S * .2))
    for y, c in ((.2, (220, 40, 40)), (.28, (40, 80, 200))):
        d.line([(S * .41, S * y), (S * .59, S * y)], fill=c + (255,), width=6)
    d.ellipse([S * .58, S * .7, S * .84, S * .92], fill=(220, 210, 130, 255), outline=OUT, width=5)               # yellowed toe
    for x in (.24, .78):
        d.arc([S * (x - .08), S * .06, S * (x + .08), S * .5], 100, 260, fill=(120, 200, 60, 255), width=5)         # stink
    return _shrink(im, size)


def clothes_dryer(size=64, open_door=False):
    """A white front-load dryer: control panel with a dial, the round porthole door (clothes tumbling inside) - or the
    door swung open."""
    im, d, S = _big(size)
    OUT = (40, 45, 55, 255)
    d.rounded_rectangle([S * .1, S * .06, S * .9, S * .96], 8, fill=(240, 242, 246, 255), outline=OUT, width=7)
    d.rectangle([S * .1, S * .06, S * .9, S * .22], fill=(200, 205, 215, 255), outline=OUT, width=5)
    d.ellipse([S * .66, S * .09, S * .8, S * .2], fill=(90, 90, 100, 255), outline=OUT, width=3)                 # dial
    for x in (.2, .28, .36):
        d.ellipse([S * x, S * .12, S * (x + .05), S * .17], fill=(80, 200, 120, 255))
    d.ellipse([S * .24, S * .32, S * .76, S * .84], fill=(170, 175, 185, 255), outline=OUT, width=7)
    if open_door:
        d.ellipse([S * .3, S * .38, S * .7, S * .78], fill=(60, 60, 70, 255))
        d.ellipse([S * .74, S * .34, S * .98, S * .82], fill=(170, 200, 230, 200), outline=OUT, width=6)          # door swung
    else:
        d.ellipse([S * .3, S * .38, S * .7, S * .78], fill=(150, 190, 225, 255))
        d.ellipse([S * .36, S * .5, S * .5, S * .62], fill=(220, 60, 60, 255))                                     # clothes inside
        d.ellipse([S * .48, S * .44, S * .62, S * .58], fill=(60, 120, 220, 255))
    return _shrink(im, size)


def lint_screen(size=64):
    """The dryer's lint trap pulled out: a white plastic frame, mesh, caked with a thick grey felt of lint."""
    im, d, S = _big(size)
    OUT = (60, 60, 70, 255)
    d.rounded_rectangle([S * .2, S * .06, S * .8, S * .94], 10, fill=(240, 240, 245, 255), outline=OUT, width=6)
    d.rectangle([S * .27, S * .14, S * .73, S * .86], fill=(170, 165, 170, 255))
    import random
    r = random.Random(3)
    for _ in range(40):
        x, y = r.uniform(.28, .72), r.uniform(.15, .85)
        d.ellipse([S * (x - .04), S * (y - .03), S * (x + .04), S * (y + .03)], fill=(200, 195, 200, 255))
    d.rectangle([S * .4, S * .02, S * .6, S * .08], fill=(240, 240, 245, 255), outline=OUT, width=4)            # pull tab
    return _shrink(im, size)


def lint_blanket(size=64):
    """A giant fuzzy wad of grey lint (with a stray blue thread and a hair)."""
    import math, random
    im, d, S = _big(size)
    r = random.Random(5)
    for _ in range(26):
        a, rr = r.uniform(0, 2 * math.pi), r.uniform(0, .26)
        x, y = .5 + rr * math.cos(a), .52 + rr * .8 * math.sin(a)
        s = r.uniform(.1, .18)
        d.ellipse([S * (x - s), S * (y - s * .8), S * (x + s), S * (y + s * .8)], fill=(175 + r.randint(-15, 15),) * 3 + (255,))
    d.line([(S * .2, S * .4), (S * .44, S * .5), (S * .7, S * .36)], fill=(60, 100, 220, 255), width=4)
    d.arc([S * .4, S * .5, S * .8, S * .8], 200, 330, fill=(60, 40, 30, 255), width=3)
    return _shrink(im, size)


def solo_cup(size=32):
    """A red party cup turned upside down (the shell game cup)."""
    im, d, S = _big(size)
    OUT = (80, 0, 10, 255)
    d.polygon([(S * .28, S * .1), (S * .72, S * .1), (S * .86, S * .9), (S * .14, S * .9)], fill=(220, 30, 40, 255))
    d.line([(S * .28, S * .1), (S * .72, S * .1), (S * .86, S * .9), (S * .14, S * .9), (S * .28, S * .1)], fill=OUT, width=6)
    d.rectangle([S * .14, S * .8, S * .86, S * .9], fill=(250, 250, 250, 255), outline=OUT, width=4)
    for y in (.3, .48):
        d.line([(S * .24, S * y), (S * .76, S * y)], fill=(180, 20, 30, 255), width=3)
    return _shrink(im, size)


def cardboard_table(size=64):
    """A cardboard box flipped over as a street table."""
    im, d, S = _big(size)
    OUT = (90, 60, 20, 255)
    d.polygon([(S * .04, S * .42), (S * .96, S * .42), (S * .9, S * .56), (S * .1, S * .56)], fill=(215, 170, 110, 255), outline=OUT)
    d.line([(S * .04, S * .42), (S * .96, S * .42), (S * .9, S * .56), (S * .1, S * .56), (S * .04, S * .42)], fill=OUT, width=6)
    d.rectangle([S * .1, S * .56, S * .9, S * .9], fill=(190, 145, 90, 255), outline=OUT, width=6)
    d.line([(S * .5, S * .56), (S * .5, S * .9)], fill=(160, 120, 70, 255), width=4)
    d.rectangle([S * .44, S * .62, S * .56, S * .7], fill=(230, 200, 150, 255))                                     # tape
    return _shrink(im, size)


def gold_watch(size=32):
    """A big gold wristwatch (the foe's item, under one of the cups)."""
    im, d, S = _big(size)
    OUT = (110, 70, 0, 255)
    d.rectangle([S * .38, S * .04, S * .62, S * .96], fill=(240, 190, 50, 255), outline=OUT, width=4)
    d.ellipse([S * .2, S * .26, S * .8, S * .74], fill=(250, 210, 70, 255), outline=OUT, width=6)
    d.ellipse([S * .3, S * .36, S * .7, S * .64], fill=(250, 250, 240, 255))
    d.line([(S * .5, S * .5), (S * .5, S * .4)], fill=OUT, width=3)
    d.line([(S * .5, S * .5), (S * .6, S * .52)], fill=OUT, width=3)
    return _shrink(im, size)


def dance_note(size=32):
    """A pink pair of beamed eighth notes with a white outline."""
    im, d, S = _big(size)
    OUT = (255, 255, 255, 255)
    C = (250, 80, 170, 255)
    for x in (.22, .62):
        d.ellipse([S * x, S * .64, S * (x + .2), S * .82], fill=C, outline=OUT, width=5)
        d.line([(S * (x + .18), S * .72), (S * (x + .18), S * .2)], fill=OUT, width=10)
        d.line([(S * (x + .18), S * .72), (S * (x + .18), S * .2)], fill=C, width=5)
    d.polygon([(S * .38, S * .14), (S * .82, S * .06), (S * .82, S * .18), (S * .38, S * .26)], fill=C, outline=OUT)
    return _shrink(im, size)


def claw_grabber(size=64, shut=False):
    """An arcade claw machine claw hanging from its cable: a chrome hub and three prongs, open wide or clamped shut."""
    im, d, S = _big(size)
    OUT = (30, 30, 40, 255)
    CH = (210, 215, 225, 255)
    d.line([(S * .5, 0), (S * .5, S * .3)], fill=(60, 60, 66, 255), width=6)                                        # cable
    d.rounded_rectangle([S * .38, S * .28, S * .62, S * .44], 6, fill=CH, outline=OUT, width=5)
    prongs = ((.3, .2, .44), (.5, .5, .5), (.7, .8, .56)) if not shut else ((.42, .44, .46), (.5, .5, .5), (.58, .56, .54))
    for x0, x1, x2 in prongs:
        tip_y = .86 if not shut else .78
        d.line([(S * x0 + (S * .08 if x0 < .5 else -S * .08 if x0 > .5 else 0), S * .42), (S * x1, S * .64), (S * x2, S * tip_y)], fill=OUT, width=10)
        d.line([(S * x0 + (S * .08 if x0 < .5 else -S * .08 if x0 > .5 else 0), S * .42), (S * x1, S * .64), (S * x2, S * tip_y)], fill=CH, width=6)
    return _shrink(im, size)


# ---- set 24, batch 6: Hat Trick, Reverse Card, Rise n Grind, Sinkhole -------------------------------------------------

def fitted_cap(size=64, color=(220, 40, 40, 255), emblem="fire"):
    """A fitted baseball cap from the side, flat brim pointing right, the sticker still on the brim; the front panel
    has an emblem: fire (flame), ice (snowflake) or zap (lightning bolt)."""
    im, d, S = _big(size)
    OUT = (20, 15, 15, 255)
    d.chord([S * .14, S * .2, S * .74, S * .84], 180, 360, fill=color, outline=OUT, width=7)
    d.rectangle([S * .14, S * .5, S * .74, S * .58], fill=color)
    d.line([(S * .14, S * .52), (S * .74, S * .52)], fill=OUT, width=5)
    d.polygon([(S * .66, S * .5), (S * .98, S * .52), (S * .98, S * .6), (S * .66, S * .6)], fill=color, outline=OUT)   # flat brim
    d.line([(S * .66, S * .5), (S * .98, S * .52), (S * .98, S * .6), (S * .66, S * .6)], fill=OUT, width=5)
    d.ellipse([S * .84, S * .52, S * .92, S * .58], fill=(220, 200, 60, 255))                                          # sticker
    d.ellipse([S * .4, S * .18, S * .48, S * .24], fill=color, outline=OUT, width=3)                                    # button
    c = (255, 255, 255, 255)
    if emblem == "fire":
        d.polygon([(S * .44, S * .3), (S * .36, S * .46), (S * .44, S * .44), (S * .52, S * .46)], fill=(255, 210, 40, 255), outline=OUT)
    elif emblem == "ice":
        for a, b in (((.44, .28), (.44, .48)), ((.35, .33), (.53, .43)), ((.35, .43), (.53, .33))):
            d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=c, width=5)
    else:
        d.polygon([(S * .46, S * .26), (S * .38, S * .38), (S * .45, S * .38), (S * .4, S * .5), (S * .52, S * .34), (S * .45, S * .34)], fill=(40, 40, 46, 255))
    return _shrink(im, size)


def game_card(size=64, label="+2", color=(220, 40, 40, 255)):
    """A card from THAT card game: coloured face, a white oval, a big label (+2, +4) or the two reverse arrows
    (label="rev") (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rounded_rectangle([S * .2, S * .06, S * .8, S * .94], 12, fill=(250, 250, 250, 255), outline=OUT, width=6)
    d.rounded_rectangle([S * .25, S * .11, S * .75, S * .89], 8, fill=color)
    d.ellipse([S * .26, S * .26, S * .74, S * .74], fill=(250, 250, 250, 255))
    if label == "rev":
        for sgn in (1, -1):
            cx, cy = S * .5 + sgn * S * .06, S * .5 - sgn * S * .06
            d.line([(cx - sgn * S * .1, cy + sgn * S * .1), (cx + sgn * S * .08, cy - sgn * S * .08)], fill=color, width=int(S * .07))
            tip = (cx + sgn * S * .12, cy - sgn * S * .12)
            d.polygon([tip, (tip[0] - sgn * S * .12, tip[1]), (tip[0], tip[1] + sgn * S * .12)], fill=color)
    im = _shrink(im, size)
    if label != "rev":
        _big_text(im, label, (32, 32), color, scale=2, font=SMALL)
    return im


def bedside_clock(size=64, t="6:00", ringing=False):
    """A black bedside alarm clock with a big red digital time (shown at 1:1); ringing adds little shake lines."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.polygon([(S * .1, S * .3), (S * .9, S * .3), (S * .96, S * .82), (S * .04, S * .82)], fill=(35, 35, 40, 255))
    d.line([(S * .1, S * .3), (S * .9, S * .3), (S * .96, S * .82), (S * .04, S * .82), (S * .1, S * .3)], fill=OUT, width=6)
    d.rectangle([S * .14, S * .38, S * .86, S * .72], fill=(15, 5, 5, 255))
    d.rounded_rectangle([S * .3, S * .2, S * .7, S * .3], 6, fill=(120, 120, 130, 255), outline=OUT, width=4)          # snooze bar
    if ringing:
        for x0, sgn in ((.02, -1), (.98, 1)):
            for k in range(2):
                d.line([(S * (x0 - sgn * .02), S * (.36 + k * .14)), (S * (x0 + sgn * .0), S * (.42 + k * .14))], fill=(255, 220, 60, 255), width=5)
    im = _shrink(im, size)
    _big_text(im, t, (32, 35), (255, 40, 30, 255), scale=2)
    return im


def coffee_mug(size=32):
    """A white coffee mug, steam curling up."""
    im, d, S = _big(size)
    OUT = (40, 30, 20, 255)
    d.rounded_rectangle([S * .2, S * .42, S * .68, S * .94], 8, fill=(250, 250, 245, 255), outline=OUT, width=6)
    d.ellipse([S * .58, S * .52, S * .86, S * .8], outline=OUT, width=7)
    d.ellipse([S * .22, S * .4, S * .66, S * .5], fill=(110, 60, 30, 255), outline=OUT, width=4)
    for x in (.32, .5):
        d.arc([S * (x - .06), S * .06, S * (x + .06), S * .36], 90, 270, fill=(220, 220, 230, 255), width=5)
    return _shrink(im, size)


def sunrise(size=64):
    """A big rising sun: orange-yellow half disc with rays fanning up."""
    import math
    im, d, S = _big(size)
    for k in range(9):
        a = math.pi + k * math.pi / 8
        d.polygon([(S * .5, S * .8), (S * (.5 + .5 * math.cos(a - .1)), S * (.8 + .5 * math.sin(a - .1))),
                   (S * (.5 + .5 * math.cos(a + .1)), S * (.8 + .5 * math.sin(a + .1)))], fill=(255, 210, 80, 180))
    d.pieslice([S * .18, S * .48, S * .82, S * 1.12], 180, 360, fill=(255, 170, 40, 255))
    d.pieslice([S * .26, S * .56, S * .74, S * 1.04], 180, 360, fill=(255, 220, 90, 255))
    return _shrink(im, size)


def road_crack(size=64, big=False):
    """A jagged crack splitting the asphalt (seen flat on the ground) - bigger and wider with big=True."""
    im, d, S = _big(size)
    w = .1 if big else .05
    pts = [(.06, .5), (.22, .44), (.34, .56), (.5, .46), (.64, .58), (.8, .48), (.94, .54)]
    d.polygon([(S * .02, S * .38), (S * .98, S * .38), (S * .98, S * .66), (S * .02, S * .66)], fill=(70, 70, 76, 200))
    up = [(S * x, S * (y - w)) for x, y in pts]
    dn = [(S * x, S * (y + w)) for x, y in reversed(pts)]
    d.polygon(up + dn, fill=(15, 12, 10, 255))
    for x, y in pts[1:-1:2]:
        d.line([(S * x, S * y), (S * (x + .06), S * (y - .16))], fill=(15, 12, 10, 255), width=5)
    return _shrink(im, size)


def sinkhole(size=64):
    """A sinkhole opening in the street: a deep black pit with a ragged ring of broken asphalt chunks round the rim."""
    import math
    im, d, S = _big(size)
    d.ellipse([S * .04, S * .3, S * .96, S * .78], fill=(70, 70, 76, 255))
    d.ellipse([S * .12, S * .36, S * .88, S * .72], fill=(5, 5, 8, 255))
    d.ellipse([S * .2, S * .36, S * .8, S * .56], fill=(60, 40, 30, 255))
    for k in range(10):
        a = k * 2 * math.pi / 10
        x, y = S * (.5 + .44 * math.cos(a)), S * (.54 + .22 * math.sin(a))
        d.polygon([(x - 10, y), (x, y - 8), (x + 12, y - 2), (x + 4, y + 8)], fill=(110, 110, 118, 255), outline=(30, 30, 34, 255))
    return _shrink(im, size)


# ---- set 25, batch 1 (INSANE): Burn It Down, Hydrant Bomb, Gun Garden, Meteor Drop, Blow Up -----------------------

def barrel_grill(size=64):
    """A cookout barrel grill on legs: black drum cut in half, lid propped open, charcoal glowing, a spatula hanging."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    for a, b in (((.2, .62), (.12, .96)), ((.8, .62), (.88, .96))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(50, 50, 56, 255), width=7)
    d.chord([S * .06, S * .32, S * .94, S * .78], 0, 180, fill=(40, 40, 46, 255), outline=OUT, width=7)
    d.chord([S * .06, S * .02, S * .94, S * .48], 180, 360, fill=(55, 55, 62, 255), outline=OUT, width=7)     # lid up
    d.line([(S * .1, S * .55), (S * .9, S * .55)], fill=(160, 160, 170, 255), width=5)                         # grate
    for x in (.2, .34, .48, .62, .76):
        d.ellipse([S * x, S * .52, S * (x + .1), S * .6], fill=(255, 120, 30, 255))                             # coals
    d.line([(S * .9, S * .4), (S * .98, S * .7)], fill=(170, 170, 180, 255), width=5)                         # spatula
    return _shrink(im, size)


def lighter_fluid(size=32):
    """A can of charcoal lighter fluid: a squeeze bottle, red cap and a flame logo."""
    im, d, S = _big(size)
    OUT = (40, 20, 0, 255)
    d.rounded_rectangle([S * .26, S * .26, S * .74, S * .96], 8, fill=(250, 210, 40, 255), outline=OUT, width=6)
    d.polygon([(S * .4, S * .26), (S * .46, S * .04), (S * .54, S * .04), (S * .6, S * .26)], fill=(220, 40, 30, 255), outline=OUT)
    d.polygon([(S * .5, S * .44), (S * .38, S * .74), (S * .62, S * .74)], fill=(230, 60, 20, 255))
    d.polygon([(S * .5, S * .56), (S * .44, S * .74), (S * .56, S * .74)], fill=(255, 220, 60, 255))
    return _shrink(im, size)


def fireball_cloud(size=64):
    """A mushroom-shaped fireball: a churning orange-red cap of flame on a smoky stalk."""
    import math
    im, d, S = _big(size)
    d.rectangle([S * .4, S * .5, S * .6, S * .96], fill=(90, 80, 80, 255))
    d.ellipse([S * .26, S * .82, S * .74, S * .98], fill=(110, 100, 100, 255))
    for k in range(10):
        a = math.pi + k * math.pi / 9
        cx, cy = S * (.5 + .34 * math.cos(a)), S * (.42 + .26 * math.sin(a))
        d.ellipse([cx - S * .14, cy - S * .14, cx + S * .14, cy + S * .14], fill=(230, 70, 20, 255))
    d.ellipse([S * .14, S * .2, S * .86, S * .6], fill=(250, 120, 30, 255))
    d.ellipse([S * .26, S * .26, S * .74, S * .52], fill=(255, 200, 60, 255))
    d.ellipse([S * .38, S * .32, S * .62, S * .46], fill=(255, 250, 200, 255))
    return _shrink(im, size)


def red_hydrant(size=64, capless=False):
    """A big red fire hydrant: the bonnet, side nozzle caps, the chains - or with the top blown off (a dark hole)."""
    im, d, S = _big(size)
    OUT = (60, 0, 0, 255)
    R, RL = (220, 30, 30, 255), (255, 110, 100, 255)
    d.rectangle([S * .3, S * .86, S * .7, S * .96], fill=(180, 20, 20, 255), outline=OUT, width=6)
    d.rounded_rectangle([S * .32, S * .36, S * .68, S * .88], 8, fill=R, outline=OUT, width=7)
    d.rectangle([S * .2, S * .5, S * .32, S * .64], fill=R, outline=OUT, width=5)
    d.rectangle([S * .68, S * .5, S * .8, S * .64], fill=R, outline=OUT, width=5)
    d.line([(S * .38, S * .42), (S * .38, S * .82)], fill=RL, width=6)
    d.rectangle([S * .28, S * .3, S * .72, S * .38], fill=(200, 25, 25, 255), outline=OUT, width=5)
    if capless:
        d.ellipse([S * .34, S * .24, S * .66, S * .36], fill=(20, 10, 10, 255), outline=OUT, width=5)
    else:
        d.chord([S * .34, S * .14, S * .66, S * .44], 180, 360, fill=R, outline=OUT, width=6)
        d.rectangle([S * .46, S * .08, S * .54, S * .16], fill=(200, 25, 25, 255), outline=OUT, width=4)
    return _shrink(im, size)


def pipe_wrench(size=32):
    """A heavy red pipe wrench."""
    im, d, S = _big(size)
    OUT = (20, 15, 15, 255)
    d.line([(S * .2, S * .9), (S * .62, S * .32)], fill=OUT, width=int(S * .16))
    d.line([(S * .2, S * .9), (S * .62, S * .32)], fill=(200, 40, 40, 255), width=int(S * .1))
    d.polygon([(S * .5, S * .26), (S * .76, S * .06), (S * .9, S * .2), (S * .66, S * .42)], fill=(170, 175, 185, 255), outline=OUT)
    d.line([(S * .5, S * .26), (S * .76, S * .06), (S * .9, S * .2), (S * .66, S * .42), (S * .5, S * .26)], fill=OUT, width=5)
    return _shrink(im, size)


def water_jet(n=16):
    """A blob of rushing water (alpha only): a fat rounded streak."""
    return _alpha(n, n, lambda x, y: max(0, 1 - ((x - 7.5) / 7) ** 2 - ((y - 7.5) / 4) ** 2))


def flower_bed(size=64, stage=0):
    """A little flower bed of dirt with a white picket edge; stage 0 = just dirt with bullets planted, 1 = sprouts,
    2 = taller stems with leaves."""
    im, d, S = _big(size)
    OUT = (40, 25, 10, 255)
    d.rectangle([S * .04, S * .7, S * .96, S * .92], fill=(110, 70, 35, 255), outline=OUT, width=6)
    for k in range(9):
        x = .06 + k * .1
        d.polygon([(S * x, S * .7), (S * (x + .03), S * .62), (S * (x + .06), S * .7)], fill=(250, 250, 250, 255), outline=OUT)
    for x in (.22, .5, .78):
        if stage == 0:
            d.rectangle([S * (x - .03), S * .64, S * (x + .03), S * .72], fill=(230, 180, 60, 255), outline=OUT, width=3)
        else:
            h = .5 if stage == 1 else .3
            d.line([(S * x, S * .72), (S * x, S * h)], fill=(60, 160, 60, 255), width=6)
            d.ellipse([S * (x - .1), S * (h + .06), S * x, S * (h + .14)], fill=(80, 190, 80, 255), outline=OUT, width=3)
            if stage == 2:
                d.ellipse([S * x, S * (h + .14), S * (x + .1), S * (h + .22)], fill=(80, 190, 80, 255), outline=OUT, width=3)
    return _shrink(im, size)


def watering_can(size=32):
    """A green watering can, spout to the right."""
    im, d, S = _big(size)
    OUT = (10, 40, 10, 255)
    d.rounded_rectangle([S * .14, S * .4, S * .62, S * .9], 8, fill=(60, 170, 80, 255), outline=OUT, width=6)
    d.line([(S * .6, S * .78), (S * .94, S * .4)], fill=OUT, width=int(S * .12))
    d.line([(S * .6, S * .78), (S * .94, S * .4)], fill=(60, 170, 80, 255), width=int(S * .07))
    d.arc([S * .16, S * .14, S * .56, S * .56], 180, 360, fill=OUT, width=6)
    return _shrink(im, size)


def gun_flower(size=64):
    """A tall flower on a green stem with leaves - but the bloom is a black pistol pointing right, petals round the grip."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.line([(S * .4, S * .98), (S * .4, S * .44)], fill=(60, 160, 60, 255), width=8)
    for y, sgn in ((.78, -1), (.62, 1)):
        d.ellipse([S * (.4 + (0 if sgn > 0 else -.18)), S * y, S * (.4 + (.18 if sgn > 0 else 0)), S * (y + .08)], fill=(80, 190, 80, 255), outline=OUT, width=3)
    for k in range(6):
        import math
        a = k * math.pi / 3
        cx, cy = S * (.4 + .12 * math.cos(a)), S * (.36 + .12 * math.sin(a))
        d.ellipse([cx - S * .07, cy - S * .07, cx + S * .07, cy + S * .07], fill=(250, 120, 180, 255), outline=OUT, width=3)
    d.rectangle([S * .34, S * .26, S * .86, S * .36], fill=(40, 40, 46, 255), outline=OUT, width=5)                 # slide
    d.polygon([(S * .34, S * .36), (S * .48, S * .36), (S * .44, S * .52), (S * .32, S * .52)], fill=(40, 40, 46, 255), outline=OUT)
    d.ellipse([S * .34, S * .3, S * .46, S * .42], fill=(255, 220, 60, 255))
    return _shrink(im, size)


def meteor_rock(size=64):
    """A flaming meteor coming down from the top-right: a cratered grey-brown rock, flames streaming behind it."""
    im, d, S = _big(size)
    OUT = (30, 20, 15, 255)
    for k, (c, w) in enumerate((((255, 90, 20), .24), ((255, 170, 40), .16), ((255, 240, 140), .08))):
        d.polygon([(S * .5, S * (.5 - w)), (S * .98, S * .02), (S * (.5 + w), S * .5)], fill=c + (255,))
    d.ellipse([S * .2, S * .42, S * .62, S * .84], fill=(120, 100, 85, 255), outline=OUT, width=7)
    for x, y, r in ((.34, .56, .06), (.48, .7, .05), (.3, .72, .04)):
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], fill=(80, 65, 55, 255))
    d.arc([S * .24, S * .46, S * .58, S * .8], 200, 280, fill=(255, 150, 60, 255), width=5)
    return _shrink(im, size)


def notif_phone(size=64, count="1"):
    """A phone lit up with notifications: a red badge with the count (1 / 12 / 99+) in the corner and message bars
    on the screen (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rounded_rectangle([S * .24, S * .06, S * .76, S * .96], 14, fill=(30, 30, 36, 255), outline=OUT, width=7)
    d.rectangle([S * .29, S * .14, S * .71, S * .86], fill=(60, 120, 220, 255))
    n = {"1": 1, "12": 3, "99+": 5}[count]
    for k in range(n):
        d.rounded_rectangle([S * .32, S * (.34 + k * .1), S * .68, S * (.42 + k * .1)], 5, fill=(250, 250, 255, 255))
    bw = {"1": .16, "12": .22, "99+": .32}[count]
    d.ellipse([S * (.82 - bw), S * .02, S * .9, S * .2], fill=(230, 30, 30, 255), outline=(255, 255, 255, 255), width=5)
    im = _shrink(im, size)
    _texted(im, [(count, (round(64 * (.86 - bw / 2)), 3))], (255, 255, 255, 255), (230, 30, 30, 255))
    return im


def notif_bell(size=32):
    """A little yellow notification bell with a red dot."""
    im, d, S = _big(size)
    OUT = (80, 50, 0, 255)
    d.chord([S * .2, S * .14, S * .8, S * .9], 180, 360, fill=(255, 210, 40, 255), outline=OUT, width=6)
    d.rectangle([S * .2, S * .52, S * .8, S * .72], fill=(255, 210, 40, 255), outline=OUT, width=6)
    d.ellipse([S * .42, S * .7, S * .58, S * .86], fill=(255, 210, 40, 255), outline=OUT, width=4)
    d.ellipse([S * .62, S * .08, S * .86, S * .32], fill=(230, 30, 30, 255), outline=(255, 255, 255, 255), width=4)
    return _shrink(im, size)


# ---- set 25, batch 2: Spoon Bend, Pinched, Lights Out, Palm Reader, Jackhammer ---------------------------------------

def bent_spoon(size=64, bent=False):
    """A shiny steel spoon standing up - or bent over in the middle."""
    im, d, S = _big(size)
    OUT = (40, 45, 60, 255)
    M, ML = (200, 205, 220, 255), (250, 252, 255, 255)
    if not bent:
        d.ellipse([S * .38, S * .06, S * .62, S * .38], fill=M, outline=OUT, width=6)
        d.line([(S * .5, S * .36), (S * .5, S * .94)], fill=OUT, width=int(S * .1))
        d.line([(S * .5, S * .36), (S * .5, S * .94)], fill=M, width=int(S * .06))
        d.line([(S * .45, S * .12), (S * .45, S * .28)], fill=ML, width=4)
    else:
        d.line([(S * .5, S * .94), (S * .5, S * .52), (S * .72, S * .36)], fill=OUT, width=int(S * .1))
        d.line([(S * .5, S * .94), (S * .5, S * .52), (S * .72, S * .36)], fill=M, width=int(S * .06))
        d.ellipse([S * .66, S * .18, S * .94, S * .42], fill=M, outline=OUT, width=6)
    return _shrink(im, size)


def bent_fork(size=64, bent=False):
    """A steel fork standing up - or bent over."""
    im, d, S = _big(size)
    OUT = (40, 45, 60, 255)
    M = (200, 205, 220, 255)
    pts = [(S * .5, S * .94), (S * .5, S * .4)] if not bent else [(S * .5, S * .94), (S * .5, S * .56), (S * .72, S * .42)]
    d.line(pts, fill=OUT, width=int(S * .1))
    d.line(pts, fill=M, width=int(S * .06))
    hx, hy = pts[-1]
    for k in range(4):
        if not bent:
            x = hx + (k - 1.5) * S * .05
            d.line([(x, hy), (x, hy - S * .3)], fill=OUT, width=7)
            d.line([(x, hy), (x, hy - S * .3)], fill=M, width=3)
        else:
            y = hy + (k - 1.5) * S * .05
            d.line([(hx, y), (hx + S * .24, y - S * .1)], fill=OUT, width=7)
            d.line([(hx, y), (hx + S * .24, y - S * .1)], fill=M, width=3)
    return _shrink(im, size)


def stop_post(size=64, bent=False):
    """A STOP sign on its pole (shown at 1:1) - or the pole bent right over, the sign hanging upside-down-ish
    (bent version has no readable text)."""
    import math
    im, d, S = _big(size)
    OUT = (20, 20, 24, 255)
    if not bent:
        d.rectangle([S * .47, S * .4, S * .53, S * .98], fill=(160, 165, 175, 255), outline=OUT, width=3)
        cx, cy, r = S * .5, S * .26, S * .24
    else:
        d.line([(S * .5, S * .98), (S * .5, S * .62), (S * .7, S * .5)], fill=OUT, width=int(S * .08))
        d.line([(S * .5, S * .98), (S * .5, S * .62), (S * .7, S * .5)], fill=(160, 165, 175, 255), width=int(S * .05))
        cx, cy, r = S * .78, S * .66, S * .2
    pts = [(cx + r * math.cos(math.pi / 8 + k * math.pi / 4), cy + r * math.sin(math.pi / 8 + k * math.pi / 4)) for k in range(8)]
    _outline_poly(d, pts, (210, 30, 30, 255), (250, 250, 250, 255), 6)
    im = _shrink(im, size)
    if not bent:
        _texted(im, [("STOP", (32, 14))], (255, 255, 255, 255), (210, 30, 30, 255))
    return im


def clothespin(size=64):
    """A wooden clothespin, jaws to the left, the steel spring in the middle."""
    im, d, S = _big(size)
    OUT = (70, 40, 10, 255)
    W = (225, 185, 120, 255)
    d.polygon([(S * .06, S * .4), (S * .94, S * .3), (S * .94, S * .44), (S * .12, S * .5)], fill=W, outline=OUT)
    d.polygon([(S * .06, S * .6), (S * .94, S * .7), (S * .94, S * .56), (S * .12, S * .5)], fill=(210, 170, 105, 255), outline=OUT)
    d.line([(S * .06, S * .4), (S * .94, S * .3), (S * .94, S * .44), (S * .12, S * .5), (S * .06, S * .4)], fill=OUT, width=5)
    d.line([(S * .06, S * .6), (S * .94, S * .7), (S * .94, S * .56), (S * .12, S * .5), (S * .06, S * .6)], fill=OUT, width=5)
    d.ellipse([S * .5, S * .4, S * .66, S * .6], outline=(170, 175, 185, 255), width=6)
    return _shrink(im, size)


def floor_lamp(size=64, on=True):
    """A floor lamp with a drum shade, glowing - or off."""
    im, d, S = _big(size)
    OUT = (30, 25, 20, 255)
    if on:
        d.polygon([(S * .3, S * .36), (S * .7, S * .36), (S * .9, S * .7), (S * .1, S * .7)], fill=(255, 240, 160, 110))
    d.polygon([(S * .32, S * .08), (S * .68, S * .08), (S * .76, S * .36), (S * .24, S * .36)],
              fill=(255, 230, 140, 255) if on else (170, 150, 110, 255), outline=OUT)
    d.line([(S * .32, S * .08), (S * .68, S * .08), (S * .76, S * .36), (S * .24, S * .36), (S * .32, S * .08)], fill=OUT, width=5)
    d.line([(S * .5, S * .36), (S * .5, S * .92)], fill=(90, 80, 70, 255), width=6)
    d.ellipse([S * .34, S * .88, S * .66, S * .98], fill=(90, 80, 70, 255), outline=OUT, width=4)
    return _shrink(im, size)


def breaker_box(size=64, off=False):
    """An open circuit breaker panel: grey box, two rows of switches and the big main lever - up (on) or down (off)."""
    im, d, S = _big(size)
    OUT = (20, 20, 24, 255)
    d.rectangle([S * .14, S * .06, S * .86, S * .94], fill=(170, 175, 185, 255), outline=OUT, width=7)
    d.rectangle([S * .22, S * .14, S * .78, S * .86], fill=(60, 62, 70, 255))
    for r in range(4):
        for c in range(2):
            x, y = .3 + c * .26, .4 + r * .12
            d.rectangle([S * x, S * y, S * (x + .16), S * (y + .08)], fill=(30, 30, 34, 255), outline=(120, 120, 130, 255), width=3)
            d.rectangle([S * (x + (.02 if off else .1)), S * (y + .02), S * (x + (.06 if off else .14)), S * (y + .06)], fill=(240, 240, 245, 255))
    d.rectangle([S * .4, S * .16, S * .6, S * .34], fill=(30, 30, 34, 255), outline=(200, 40, 40, 255), width=4)
    d.rectangle([S * .44, S * (.26 if off else .18), S * .56, S * (.32 if off else .24)], fill=(220, 40, 40, 255))
    return _shrink(im, size)


def psychic_sign(size=64):
    """A neon storefront sign: a pink hand-with-eye outline and PSYCHIC in glowing purple tubes (shown at 1:1)."""
    im, d, S = _big(size)
    d.rounded_rectangle([S * .04, S * .14, S * .96, S * .86], 10, fill=(25, 15, 40, 255), outline=(90, 60, 120, 255), width=6)
    d.ellipse([S * .38, S * .2, S * .62, S * .44], outline=(255, 90, 200, 255), width=6)
    d.ellipse([S * .46, S * .28, S * .54, S * .36], fill=(255, 90, 200, 255))
    im = _shrink(im, size)
    return _texted(im, [("PSYCHIC", (32, 33))], (230, 170, 255, 255), (120, 40, 170, 255))


def seer_ball(size=64, vision=0):
    """A crystal ball on a gold stand; vision 0 = swirling purple mist, 1 = thicker mist, 2 = a red target (the foe
    locked in)."""
    im, d, S = _big(size)
    OUT = (40, 20, 60, 255)
    d.polygon([(S * .3, S * .78), (S * .7, S * .78), (S * .78, S * .94), (S * .22, S * .94)], fill=(220, 170, 50, 255), outline=OUT)
    d.ellipse([S * .18, S * .14, S * .82, S * .8], fill=(170, 140, 240, 220), outline=OUT, width=7)
    if vision < 2:
        for k in range(2 + vision * 2):
            d.arc([S * (.28 + k * .04), S * (.26 + k * .05), S * (.72 - k * .03), S * (.68 - k * .04)], k * 70, k * 70 + 180,
                  fill=(255, 255, 255, 200), width=6)
    else:
        for r, c in ((.22, (230, 30, 30)), (.14, (255, 255, 255)), (.07, (230, 30, 30))):
            d.ellipse([S * (.5 - r), S * (.47 - r), S * (.5 + r), S * (.47 + r)], fill=c + (255,))
    d.arc([S * .26, S * .2, S * .5, S * .44], 200, 260, fill=(255, 255, 255, 255), width=6)
    return _shrink(im, size)


def jackhammer(size=64):
    """A pneumatic jackhammer: T handles, the yellow body, the steel chisel bit at the bottom."""
    im, d, S = _big(size)
    OUT = (20, 15, 5, 255)
    d.rectangle([S * .14, S * .06, S * .86, S * .16], fill=(40, 40, 46, 255), outline=OUT, width=5)
    d.rounded_rectangle([S * .34, S * .14, S * .66, S * .62], 10, fill=(250, 200, 30, 255), outline=OUT, width=7)
    d.rectangle([S * .4, S * .24, S * .6, S * .32], fill=(40, 40, 46, 255))
    d.rectangle([S * .44, S * .62, S * .56, S * .9], fill=(180, 185, 195, 255), outline=OUT, width=5)
    d.polygon([(S * .44, S * .9), (S * .56, S * .9), (S * .5, S * .98)], fill=(180, 185, 195, 255), outline=OUT)
    d.line([(S * .66, S * .3), (S * .9, S * .4)], fill=(40, 40, 46, 255), width=6)                                  # air hose
    return _shrink(im, size)


def apt_window(size=64, lit=False):
    """An apartment window at dawn: dark panes - or the light snapped on (yellow), blinds half up."""
    im, d, S = _big(size)
    OUT = (40, 30, 30, 255)
    d.rectangle([S * .1, S * .08, S * .9, S * .92], fill=(170, 90, 70, 255), outline=OUT, width=7)                 # brick
    glass = (255, 230, 120, 255) if lit else (40, 50, 80, 255)
    d.rectangle([S * .22, S * .2, S * .78, S * .78], fill=glass, outline=(240, 240, 240, 255), width=7)
    d.line([(S * .5, S * .2), (S * .5, S * .78)], fill=(240, 240, 240, 255), width=6)
    d.rectangle([S * .24, S * .22, S * .76, S * .38], fill=(230, 225, 210, 255))                                  # blinds
    for y in (.26, .3, .34):
        d.line([(S * .24, S * y), (S * .76, S * y)], fill=(190, 185, 170, 255), width=2)
    d.rectangle([S * .18, S * .78, S * .82, S * .84], fill=(200, 200, 205, 255), outline=OUT, width=4)
    return _shrink(im, size)


# ---- set 25, batch 3: 360 Deal, Eat Good, Waterworks, Bone Toss, Shmoney ---------------------------------------------

def record_contract(size=64, signed=0):
    """A record deal contract: CONTRACT across the top, fine print, and the SIGN HERE line with a red X; signed 1 =
    a scribbled signature on it, 2 = signature + initials scribbled down the side (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 40, 50, 255)
    d.polygon([(S * .14, S * .04), (S * .76, S * .04), (S * .9, S * .18), (S * .9, S * .96), (S * .14, S * .96)], fill=(250, 250, 245, 255), outline=OUT)
    d.line([(S * .14, S * .04), (S * .76, S * .04), (S * .9, S * .18), (S * .9, S * .96), (S * .14, S * .96), (S * .14, S * .04)], fill=OUT, width=5)
    for k in range(6):
        d.line([(S * .22, S * (.32 + k * .07)), (S * .82, S * (.32 + k * .07))], fill=(170, 170, 180, 255), width=3)
    d.line([(S * .3, S * .86), (S * .8, S * .86)], fill=OUT, width=4)
    d.line([(S * .2, S * .8), (S * .26, S * .88)], fill=(220, 30, 30, 255), width=5)
    d.line([(S * .26, S * .8), (S * .2, S * .88)], fill=(220, 30, 30, 255), width=5)
    if signed:
        d.line([(S * .34, S * .84), (S * .42, S * .76), (S * .48, S * .84), (S * .56, S * .74), (S * .64, S * .84), (S * .76, S * .78)], fill=(40, 60, 200, 255), width=5)
    if signed > 1:
        for y in (.36, .5, .64):
            d.line([(S * .78, S * y), (S * .84, S * (y - .04)), (S * .86, S * (y + .02))], fill=(40, 60, 200, 255), width=4)
    im = _shrink(im, size)
    return _texted(im, [("CONTRACT", (33, 8))], (20, 20, 25, 255), (250, 250, 245, 255))


def fancy_pen(size=32):
    """A shiny black fountain pen, nib down-left."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.line([(S * .2, S * .8), (S * .86, S * .14)], fill=OUT, width=int(S * .16))
    d.line([(S * .2, S * .8), (S * .86, S * .14)], fill=(40, 40, 46, 255), width=int(S * .1))
    d.line([(S * .44, S * .56), (S * .5, S * .5)], fill=(230, 190, 60, 255), width=int(S * .12))
    d.polygon([(S * .2, S * .8), (S * .06, S * .94), (S * .14, S * .74)], fill=(230, 190, 60, 255))
    return _shrink(im, size)


def grandma_plate(size=64, full=False):
    """A paper plate from grandma's kitchen: a scoop of mac and cheese, greens, a piece of fried chicken - or piled
    into a mountain that's falling off the sides."""
    im, d, S = _big(size)
    OUT = (60, 40, 20, 255)
    d.ellipse([S * .04, S * .6, S * .96, S * .92], fill=(250, 250, 245, 255), outline=OUT, width=6)
    if not full:
        d.ellipse([S * .14, S * .56, S * .42, S * .76], fill=(250, 200, 60, 255), outline=OUT, width=4)          # mac
        d.ellipse([S * .44, S * .58, S * .66, S * .76], fill=(60, 120, 50, 255), outline=OUT, width=4)          # greens
        d.ellipse([S * .62, S * .5, S * .88, S * .74], fill=(190, 120, 50, 255), outline=OUT, width=4)          # chicken
    else:
        d.polygon([(S * .08, S * .76), (S * .3, S * .24), (S * .5, S * .08), (S * .7, S * .22), (S * .92, S * .76)], fill=(250, 200, 60, 255), outline=OUT)
        for x, y, c in ((.3, .5, (60, 120, 50)), (.6, .36, (190, 120, 50)), (.5, .6, (60, 120, 50)), (.72, .58, (190, 120, 50)), (.42, .3, (230, 230, 220))):
            d.ellipse([S * (x - .1), S * (y - .07), S * (x + .1), S * (y + .07)], fill=c + (255,), outline=OUT, width=4)
        d.ellipse([S * .86, S * .8, S * .96, S * .9], fill=(250, 200, 60, 255), outline=OUT, width=3)            # spillover
    return _shrink(im, size)


def cook_pot(size=64):
    """A big dented aluminum cooking pot with steam rising, a ladle sticking out."""
    im, d, S = _big(size)
    OUT = (40, 40, 46, 255)
    d.rectangle([S * .14, S * .38, S * .86, S * .9], fill=(190, 195, 205, 255), outline=OUT, width=7)
    d.ellipse([S * .1, S * .3, S * .9, S * .46], fill=(140, 145, 155, 255), outline=OUT, width=6)
    d.ellipse([S * .16, S * .32, S * .84, S * .44], fill=(250, 200, 60, 255))
    for x in (.04, .86):
        d.rectangle([S * x, S * .46, S * (x + .1), S * .52], fill=(60, 60, 66, 255), outline=OUT, width=3)
    d.line([(S * .6, S * .38), (S * .82, S * .04)], fill=(170, 175, 185, 255), width=7)                              # ladle
    for x in (.3, .44):
        d.arc([S * (x - .06), S * .04, S * (x + .06), S * .3], 90, 270, fill=(230, 230, 240, 255), width=5)
    d.line([(S * .22, S * .5), (S * .22, S * .82)], fill=(240, 240, 250, 255), width=5)
    return _shrink(im, size)


def dog_bone(size=64):
    """A big white cartoon dog bone."""
    im, d, S = _big(size)
    OUT = (90, 80, 60, 255)
    W = (250, 245, 230, 255)
    d.rectangle([S * .22, S * .42, S * .78, S * .58], fill=W)
    for x in (.12, .88):
        for y in (.38, .62):
            d.ellipse([S * (x - .1), S * (y - .1), S * (x + .1), S * (y + .1)], fill=W, outline=OUT, width=6)
    d.line([(S * .22, S * .42), (S * .78, S * .42)], fill=OUT, width=6)
    d.line([(S * .22, S * .58), (S * .78, S * .58)], fill=OUT, width=6)
    return _shrink(im, size)


def band_stack(size=32):
    """A stack of cash with a yellow money band."""
    im, d, S = _big(size)
    OUT = (20, 60, 20, 255)
    for k in range(3):
        y = .36 + k * .1
        d.rectangle([S * .1, S * y, S * .9, S * (y + .2)], fill=(110, 190, 100, 255), outline=OUT, width=4)
    d.rectangle([S * .42, S * .34, S * .58, S * .78], fill=(250, 210, 50, 255), outline=OUT, width=3)
    return _shrink(im, size)


# ---- set 25, batch 4: Moon Bath, Slime Down, Last Verse, Lip Gloss, Bottle Rain ---------------------------------------

def big_moon(size=64):
    """A big pale full moon with grey craters and a soft glow ring."""
    im, d, S = _big(size)
    d.ellipse([S * .02, S * .02, S * .98, S * .98], fill=(255, 255, 220, 70))
    d.ellipse([S * .12, S * .12, S * .88, S * .88], fill=(250, 248, 225, 255), outline=(200, 195, 160, 255), width=6)
    for x, y, r in ((.36, .36, .1), (.6, .56, .13), (.42, .68, .07), (.66, .3, .06)):
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], fill=(215, 210, 180, 255))
    return _shrink(im, size)


def sun_reflector(size=64):
    """A fold-out silver tanning reflector (three panels), held open."""
    im, d, S = _big(size)
    OUT = (60, 65, 80, 255)
    for x0, x1, c in ((.06, .36, (200, 210, 230)), (.36, .64, (240, 245, 255)), (.64, .94, (200, 210, 230))):
        d.polygon([(S * x0, S * (.3 if x0 < .3 or x0 > .6 else .24)), (S * x1, S * (.24 if x1 < .7 else .3)),
                   (S * x1, S * (.7 if x1 < .7 else .64)), (S * x0, S * (.64 if x0 < .3 or x0 > .6 else .7))], fill=c + (255,), outline=OUT)
    for x in (.36, .64):
        d.line([(S * x, S * .24), (S * x, S * .7)], fill=OUT, width=4)
    d.line([(S * .44, S * .32), (S * .5, S * .5)], fill=(255, 255, 255, 255), width=5)
    return _shrink(im, size)


def beach_lounger(size=64):
    """A striped folding beach lounger, reclined."""
    im, d, S = _big(size)
    OUT = (40, 30, 20, 255)
    for x, c in ((.0, (240, 80, 80)), (.12, (250, 250, 250)), (.24, (60, 140, 230)), (.36, (250, 250, 250)), (.48, (240, 80, 80))):
        d.polygon([(S * (.08 + x), S * .62), (S * (.2 + x), S * .62), (S * (.2 + x * .3 + .5), S * (.3 + x * .1)), (S * (.08 + x * .3 + .5), S * (.3 + x * .1))], fill=c + (255,)) if False else None
    d.polygon([(S * .06, S * .64), (S * .62, S * .64), (S * .62, S * .72), (S * .06, S * .72)], fill=(60, 140, 230, 255), outline=OUT)   # seat
    d.polygon([(S * .62, S * .64), (S * .94, S * .22), (S * .98, S * .28), (S * .66, S * .72)], fill=(240, 80, 80, 255), outline=OUT)   # back
    for k in range(3):
        d.line([(S * (.16 + k * .16), S * .64), (S * (.16 + k * .16), S * .72)], fill=(250, 250, 250, 255), width=6)
    for a, b in (((.12, .72), (.06, .92)), ((.56, .72), (.66, .92)), ((.8, .48), (.9, .92))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(170, 175, 185, 255), width=6)
    return _shrink(im, size)


def slime_bucket(size=64, tipped=False):
    """A metal bucket brimming with bright green slime, dripping down the side - or tipped over, slime pouring out."""
    im, d, S = _big(size)
    OUT = (30, 40, 30, 255)
    bucket = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    b = ImageDraw.Draw(bucket)
    b.polygon([(S * .2, S * .3), (S * .8, S * .3), (S * .72, S * .92), (S * .28, S * .92)], fill=(170, 175, 185, 255), outline=OUT)
    b.line([(S * .2, S * .3), (S * .8, S * .3), (S * .72, S * .92), (S * .28, S * .92), (S * .2, S * .3)], fill=OUT, width=6)
    b.ellipse([S * .2, S * .22, S * .8, S * .38], fill=(120, 230, 60, 255), outline=OUT, width=5)
    b.ellipse([S * .3, S * .3, S * .4, S * .52], fill=(120, 230, 60, 255))
    b.arc([S * .16, S * .04, S * .84, S * .5], 200, 340, fill=OUT, width=5)                                        # handle
    if tipped:
        bucket = bucket.rotate(130, center=(S * .5, S * .5), resample=Image.BICUBIC)
        b = ImageDraw.Draw(bucket)
        b.polygon([(S * .4, S * .7), (S * .2, S * .98), (S * .7, S * .98), (S * .56, S * .7)], fill=(120, 230, 60, 255))
    im.alpha_composite(bucket)
    return _shrink(im, size)


def slime_goo(size=64):
    """A big blob of green slime dripping down over something (to cover a battler)."""
    im, d, S = _big(size)
    G, GL = (110, 220, 50, 230), (200, 255, 150, 255)
    d.ellipse([S * .1, S * .04, S * .9, S * .5], fill=G)
    for x, h in ((.16, .78), (.3, .62), (.44, .9), (.58, .7), (.72, .84), (.84, .6)):
        d.rounded_rectangle([S * (x - .06), S * .3, S * (x + .06), S * h], 10, fill=G)
        d.ellipse([S * (x - .07), S * (h - .06), S * (x + .07), S * (h + .06)], fill=G)
    d.arc([S * .2, S * .1, S * .6, S * .36], 200, 300, fill=GL, width=8)
    return _shrink(im, size)


def stage_mic(size=64):
    """A handheld mic held upright: a silver mesh ball head on top, a tapered black handle, a gold band."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.polygon([(S * .4, S * .42), (S * .6, S * .42), (S * .55, S * .96), (S * .45, S * .96)], fill=(40, 40, 46, 255), outline=OUT)
    d.line([(S * .4, S * .42), (S * .6, S * .42), (S * .55, S * .96), (S * .45, S * .96), (S * .4, S * .42)], fill=OUT, width=6)
    d.rectangle([S * .4, S * .42, S * .6, S * .5], fill=(230, 190, 60, 255), outline=OUT, width=4)
    d.ellipse([S * .3, S * .06, S * .7, S * .46], fill=(200, 205, 215, 255), outline=OUT, width=6)
    for k in range(4):
        d.line([(S * (.37 + k * .09), S * .1), (S * (.37 + k * .09), S * .42)], fill=(140, 145, 155, 255), width=3)
    d.line([(S * .3, S * .26), (S * .7, S * .26)], fill=(140, 145, 155, 255), width=3)
    d.arc([S * .36, S * .12, S * .56, S * .3], 200, 280, fill=(255, 255, 255, 255), width=5)
    return _shrink(im, size)


def lip_gloss(size=32):
    """A tube of pink lip gloss with the wand pulled out."""
    im, d, S = _big(size)
    OUT = (80, 20, 50, 255)
    d.rounded_rectangle([S * .14, S * .46, S * .44, S * .96], 8, fill=(255, 140, 200, 255), outline=OUT, width=5)
    d.rectangle([S * .14, S * .46, S * .44, S * .58], fill=(240, 240, 245, 255), outline=OUT, width=4)
    d.line([(S * .5, S * .5), (S * .82, S * .12)], fill=OUT, width=7)
    d.ellipse([S * .72, S * .04, S * .9, S * .22], fill=(255, 100, 180, 255), outline=OUT, width=4)
    d.line([(S * .2, S * .62), (S * .2, S * .86)], fill=(255, 220, 240, 255), width=4)
    return _shrink(im, size)


def glossy_lips(size=64):
    """Big glossy pink lips with white shine spots - so shiny they sparkle."""
    im, d, S = _big(size)
    OUT = (110, 0, 50, 255)
    R = (250, 80, 160, 255)
    d.pieslice([S * .08, S * .24, S * .52, S * .64], 180, 360, fill=R)
    d.pieslice([S * .48, S * .24, S * .92, S * .64], 180, 360, fill=R)
    d.chord([S * .08, S * .3, S * .92, S * .8], 0, 180, fill=R)
    d.polygon([(S * .08, S * .44), (S * .92, S * .44), (S * .92, S * .56), (S * .08, S * .56)], fill=R)
    d.line([(S * .1, S * .5), (S * .3, S * .46), (S * .5, S * .52), (S * .7, S * .46), (S * .9, S * .5)], fill=OUT, width=6)
    for x, y, r in ((.28, .36, .06), (.66, .36, .05), (.48, .66, .07), (.3, .64, .03)):
        d.ellipse([S * (x - r), S * (y - r * .6), S * (x + r), S * (y + r * .6)], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def sleep_z16(n=16):
    """A small Z (alpha only)."""
    return _alpha(n, n, lambda x, y: 1 if (3 <= y <= 4 and 3 <= x <= 12) or (11 <= y <= 12 and 3 <= x <= 12) or
                  (4 < y < 11 and abs(x - (12 - (y - 4) * 9 / 7)) < 1.3) else 0)


def water_bottle(size=32):
    """A plastic water bottle: clear with a blue label and cap."""
    im, d, S = _big(size)
    OUT = (40, 60, 90, 255)
    d.rounded_rectangle([S * .32, S * .22, S * .68, S * .94], 10, fill=(200, 230, 250, 200), outline=OUT, width=5)
    d.rectangle([S * .4, S * .06, S * .6, S * .2], fill=(40, 100, 220, 255), outline=OUT, width=4)
    d.rectangle([S * .32, S * .5, S * .68, S * .7], fill=(40, 120, 230, 255))
    d.line([(S * .4, S * .28), (S * .4, S * .46)], fill=(255, 255, 255, 255), width=4)
    return _shrink(im, size)


# ---- set 25, batch 5: Two-Piece, Jump Out, Roll Up, Waffle Iron, Bazooka -----------------------------------------------

def drumstick(size=32):
    """A crispy fried chicken drumstick."""
    im, d, S = _big(size)
    OUT = (90, 45, 10, 255)
    d.line([(S * .62, S * .62), (S * .9, S * .9)], fill=(250, 245, 230, 255), width=int(S * .12))
    d.ellipse([S * .82, S * .82, S * .98, S * .98], fill=(250, 245, 230, 255), outline=OUT, width=3)
    d.ellipse([S * .08, S * .08, S * .7, S * .7], fill=(205, 130, 50, 255), outline=OUT, width=6)
    for x, y in ((.24, .26), (.44, .2), (.3, .46), (.52, .4)):
        d.ellipse([S * x, S * y, S * (x + .1), S * (y + .08)], fill=(230, 170, 80, 255))
    return _shrink(im, size)


def shrub(size=64, rustle=0):
    """A round hedge bush; rustle 1/2 jiggles the leaves (a different leaf pattern)."""
    import random
    im, d, S = _big(size)
    OUT = (20, 60, 20, 255)
    d.ellipse([S * .04, S * .2, S * .96, S * .96], fill=(50, 140, 50, 255), outline=OUT, width=7)
    r = random.Random(11 + rustle)
    for _ in range(16):
        x, y = r.uniform(.14, .82), r.uniform(.3, .82)
        d.ellipse([S * x, S * y, S * (x + .12), S * (y + .09)], fill=(80, 180, 70, 255), outline=(40, 110, 40, 255), width=3)
    return _shrink(im, size)


def roller_skate(size=64):
    """A white quad roller skate: high-top boot, pink wheels, a red toe stop, laces."""
    im, d, S = _big(size)
    OUT = (30, 20, 30, 255)
    d.polygon([(S * .2, S * .1), (S * .5, S * .1), (S * .52, S * .5), (S * .86, S * .56), (S * .88, S * .7), (S * .16, S * .7)],
              fill=(250, 250, 250, 255), outline=OUT)
    d.line([(S * .2, S * .1), (S * .5, S * .1), (S * .52, S * .5), (S * .86, S * .56), (S * .88, S * .7), (S * .16, S * .7), (S * .2, S * .1)], fill=OUT, width=6)
    for y in (.2, .3, .4):
        d.line([(S * .3, S * y), (S * .46, S * (y + .04))], fill=(240, 80, 150, 255), width=4)
    d.rectangle([S * .16, S * .7, S * .88, S * .76], fill=(170, 175, 185, 255), outline=OUT, width=4)
    for x in (.26, .74):
        d.ellipse([S * (x - .1), S * .72, S * (x + .1), S * .92], fill=(250, 100, 170, 255), outline=OUT, width=5)
    d.ellipse([S * .84, S * .64, S * .96, S * .76], fill=(220, 40, 40, 255), outline=OUT, width=4)
    return _shrink(im, size)


def waffle_iron(size=64, shut=False):
    """A waffle iron: open (two gridded plates, hinge at the back) or clamped shut with steam slits."""
    im, d, S = _big(size)
    OUT = (20, 20, 24, 255)
    if not shut:
        d.polygon([(S * .1, S * .66), (S * .9, S * .66), (S * .96, S * .9), (S * .04, S * .9)], fill=(60, 60, 66, 255), outline=OUT)
        d.polygon([(S * .14, S * .68), (S * .86, S * .68), (S * .9, S * .86), (S * .1, S * .86)], fill=(140, 140, 150, 255))
        d.polygon([(S * .1, S * .62), (S * .9, S * .62), (S * .82, S * .1), (S * .18, S * .1)], fill=(60, 60, 66, 255), outline=OUT)
        d.polygon([(S * .16, S * .58), (S * .84, S * .58), (S * .78, S * .16), (S * .22, S * .16)], fill=(140, 140, 150, 255))
        for k in range(1, 5):
            d.line([(S * (.2 + k * .12), S * .18), (S * (.18 + k * .13), S * .56)], fill=(90, 90, 100, 255), width=3)
            d.line([(S * .2, S * (.18 + k * .08)), (S * .8, S * (.18 + k * .08))], fill=(90, 90, 100, 255), width=3)
    else:
        d.rounded_rectangle([S * .06, S * .4, S * .94, S * .86], 14, fill=(60, 60, 66, 255), outline=OUT, width=7)
        d.line([(S * .06, S * .62), (S * .94, S * .62)], fill=(250, 200, 80, 255), width=5)
        d.rectangle([S * .4, S * .26, S * .6, S * .4], fill=(40, 40, 46, 255), outline=OUT, width=4)
    d.rectangle([S * .9, S * .6, S * .99, S * .68], fill=(200, 40, 40, 255), outline=OUT, width=3)                 # light
    return _shrink(im, size)


def gum_bubble(size=64):
    """A big shiny pink bubblegum bubble."""
    im, d, S = _big(size)
    d.ellipse([S * .06, S * .06, S * .94, S * .94], fill=(255, 140, 200, 235), outline=(200, 60, 140, 255), width=6)
    d.ellipse([S * .2, S * .16, S * .44, S * .34], fill=(255, 230, 245, 255))
    d.ellipse([S * .6, S * .66, S * .7, S * .74], fill=(255, 200, 230, 255))
    return _shrink(im, size)


def gum_splat(size=64):
    """Popped bubblegum stuck all over something: pink stringy splat."""
    import math
    im, d, S = _big(size)
    P = (255, 130, 195, 255)
    d.ellipse([S * .26, S * .3, S * .74, S * .7], fill=P)
    for k in range(9):
        a = k * 2 * math.pi / 9 + .3
        r = .4 if k % 2 else .3
        x, y = .5 + r * math.cos(a), .5 + r * .8 * math.sin(a)
        d.line([(S * .5, S * .5), (S * x, S * y)], fill=P, width=int(S * .07))
        d.ellipse([S * (x - .05), S * (y - .05), S * (x + .05), S * (y + .05)], fill=P)
    d.arc([S * .32, S * .34, S * .56, S * .5], 200, 300, fill=(255, 220, 240, 255), width=5)
    return _shrink(im, size)


# ---- set 25, batch 6: Thumbtacks, Copy Paste, Receipts, Max Out, Hustle ------------------------------------------------

def thumbtack(size=32):
    """A red push pin / thumbtack, point down."""
    im, d, S = _big(size)
    OUT = (80, 0, 0, 255)
    d.line([(S * .5, S * .56), (S * .5, S * .96)], fill=(190, 195, 205, 255), width=int(S * .08))
    d.rounded_rectangle([S * .26, S * .44, S * .74, S * .58], 6, fill=(220, 30, 30, 255), outline=OUT, width=4)
    d.rectangle([S * .38, S * .2, S * .62, S * .46], fill=(220, 30, 30, 255), outline=OUT, width=4)
    d.ellipse([S * .22, S * .04, S * .78, S * .26], fill=(240, 50, 50, 255), outline=OUT, width=4)
    d.ellipse([S * .32, S * .08, S * .44, S * .14], fill=(255, 180, 180, 255))
    return _shrink(im, size)


def tack_box(size=64):
    """A little cardboard box of thumbtacks, flap open, TACKS printed on it (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (80, 50, 20, 255)
    d.rectangle([S * .16, S * .4, S * .84, S * .86], fill=(210, 165, 105, 255), outline=OUT, width=6)
    d.polygon([(S * .16, S * .4), (S * .84, S * .4), (S * .74, S * .24), (S * .26, S * .24)], fill=(190, 145, 90, 255), outline=OUT)
    for x in (.34, .48, .62):
        d.ellipse([S * (x - .05), S * .3, S * (x + .05), S * .38], fill=(220, 30, 30, 255), outline=(80, 0, 0, 255), width=3)
    im = _shrink(im, size)
    return _texted(im, [("TACKS", (32, 36))], (255, 255, 255, 255), (120, 70, 20, 255))


def photocopier(size=64):
    """An office photocopier: grey body, the lid, a control panel with a green start button, the output tray."""
    im, d, S = _big(size)
    OUT = (30, 30, 36, 255)
    d.rectangle([S * .12, S * .3, S * .88, S * .94], fill=(210, 212, 218, 255), outline=OUT, width=7)
    d.rectangle([S * .1, S * .2, S * .9, S * .32], fill=(180, 182, 190, 255), outline=OUT, width=6)
    d.rectangle([S * .56, S * .38, S * .84, S * .5], fill=(90, 92, 100, 255), outline=OUT, width=4)
    d.ellipse([S * .74, S * .4, S * .82, S * .48], fill=(60, 200, 90, 255))
    d.rectangle([S * .02, S * .58, S * .14, S * .64], fill=(170, 172, 180, 255), outline=OUT, width=4)          # out tray
    d.rectangle([S * .2, S * .6, S * .8, S * .86], fill=(195, 197, 205, 255), outline=(150, 150, 160, 255), width=4)
    return _shrink(im, size)


def copy_page(size=32, quality=0):
    """A sheet of paper out of the copier: 0 = blank, 1 = smudged grey mess, 2 = a crisp perfect star icon."""
    im, d, S = _big(size)
    OUT = (60, 60, 70, 255)
    d.rectangle([S * .18, S * .06, S * .82, S * .94], fill=(250, 250, 250, 255), outline=OUT, width=4)
    if quality == 1:
        for x, y in ((.3, .3), (.5, .5), (.42, .66), (.6, .3)):
            d.ellipse([S * x, S * y, S * (x + .2), S * (y + .14)], fill=(120, 120, 130, 160))
    elif quality == 2:
        import math
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            r = .26 if k % 2 == 0 else .11
            pts.append((S * (.5 + r * math.cos(a)), S * (.5 + r * math.sin(a))))
        d.polygon(pts, fill=(20, 20, 24, 255))
    return _shrink(im, size)


def receipt_printer(size=64):
    """A black point-of-sale receipt printer with paper feeding out the top."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rounded_rectangle([S * .14, S * .5, S * .86, S * .94], 10, fill=(40, 40, 46, 255), outline=OUT, width=7)
    d.rectangle([S * .3, S * .44, S * .7, S * .54], fill=(25, 25, 28, 255), outline=OUT, width=4)
    d.rectangle([S * .34, S * .1, S * .66, S * .5], fill=(250, 250, 245, 255), outline=(150, 150, 150, 255), width=3)
    for y in (.18, .26, .34, .42):
        d.line([(S * .38, S * y), (S * .62, S * y)], fill=(170, 170, 170, 255), width=3)
    d.ellipse([S * .74, S * .58, S * .8, S * .64], fill=(60, 200, 90, 255))
    return _shrink(im, size)


def long_receipt(size=64):
    """A ridiculously long receipt, curling at the bottom - CVS long."""
    im, d, S = _big(size)
    d.rectangle([S * .4, S * .0, S * .6, S * .86], fill=(250, 250, 245, 255), outline=(150, 150, 150, 255), width=3)
    d.arc([S * .36, S * .76, S * .7, S * 1.0], 0, 270, fill=(250, 250, 245, 255), width=int(S * .06))
    for k in range(18):
        y = .04 + k * .045
        d.line([(S * .43, S * y), (S * (.5 + (k % 3) * .03), S * y)], fill=(160, 160, 160, 255), width=3)
    return _shrink(im, size)


def dumbbell(size=32):
    """A chrome dumbbell."""
    im, d, S = _big(size)
    OUT = (30, 30, 36, 255)
    d.rectangle([S * .3, S * .44, S * .7, S * .56], fill=(200, 205, 215, 255), outline=OUT, width=4)
    for x in (.12, .7):
        d.rounded_rectangle([S * x, S * .28, S * (x + .18), S * .72], 4, fill=(60, 60, 66, 255), outline=OUT, width=5)
    return _shrink(im, size)


def oly_barbell(size=64):
    """A loaded Olympic barbell: a long bar with big red plates on each end."""
    im, d, S = _big(size)
    OUT = (20, 20, 24, 255)
    d.rectangle([S * .02, S * .47, S * .98, S * .53], fill=(200, 205, 215, 255), outline=OUT, width=3)
    for x in (.08, .8):
        d.rounded_rectangle([S * x, S * .22, S * (x + .1), S * .78], 6, fill=(200, 30, 30, 255), outline=OUT, width=5)
        d.rounded_rectangle([S * (x + (.1 if x < .5 else -.06)), S * .3, S * (x + (.16 if x < .5 else 0)), S * .7], 4, fill=(40, 40, 46, 255), outline=OUT, width=4)
    return _shrink(im, size)


def vending_machine(size=64):
    """A red soda vending machine: rows of cans behind glass, the coin slot and the dispenser."""
    im, d, S = _big(size)
    OUT = (40, 0, 0, 255)
    d.rectangle([S * .14, S * .04, S * .86, S * .96], fill=(210, 30, 30, 255), outline=OUT, width=7)
    d.rectangle([S * .2, S * .1, S * .62, S * .7], fill=(150, 200, 230, 255), outline=OUT, width=5)
    for r in range(4):
        for c in range(3):
            d.rectangle([S * (.24 + c * .13), S * (.14 + r * .14), S * (.32 + c * .13), S * (.24 + r * .14)],
                        fill=((240, 240, 240), (40, 90, 220), (250, 200, 40))[(r + c) % 3] + (255,), outline=OUT, width=2)
    d.rectangle([S * .68, S * .2, S * .8, S * .4], fill=(60, 60, 66, 255), outline=OUT, width=4)
    d.rectangle([S * .22, S * .76, S * .6, S * .88], fill=(30, 30, 34, 255), outline=OUT, width=4)
    return _shrink(im, size)


def moth_wallet(size=64):
    """A brown leather wallet flopped open - completely empty - with a little moth fluttering out."""
    im, d, S = _big(size)
    OUT = (50, 30, 10, 255)
    d.rounded_rectangle([S * .06, S * .44, S * .5, S * .9], 8, fill=(140, 90, 50, 255), outline=OUT, width=6)
    d.rounded_rectangle([S * .5, S * .44, S * .94, S * .9], 8, fill=(150, 100, 55, 255), outline=OUT, width=6)
    d.rectangle([S * .12, S * .52, S * .44, S * .62], fill=(100, 60, 30, 255))
    d.rectangle([S * .56, S * .52, S * .88, S * .62], fill=(100, 60, 30, 255))
    for pts in (((.62, .3), (.48, .12), (.56, .34)), ((.62, .3), (.76, .12), (.68, .34))):
        _outline_poly(d, [(S * x, S * y) for x, y in pts], (200, 180, 140, 255), (60, 50, 30, 255), 4)
    d.ellipse([S * .58, S * .24, S * .66, S * .38], fill=(120, 100, 70, 255))
    return _shrink(im, size)


# ---- set 26, batch 1 (INSANE): Live Wire, Fire Cart, Wrecker, Headbanger, Super Soaker -------------------------------

def utility_pole(size=64):
    """A wooden utility pole with a crossbar, a grey transformer can, and one power line snapped and hanging down."""
    im, d, S = _big(size)
    OUT = (30, 20, 10, 255)
    d.rectangle([S * .44, S * .04, S * .54, S * .98], fill=(130, 90, 50, 255), outline=OUT, width=5)
    d.rectangle([S * .14, S * .12, S * .86, S * .18], fill=(130, 90, 50, 255), outline=OUT, width=4)
    for x in (.18, .82):
        d.rectangle([S * (x - .02), S * .06, S * (x + .02), S * .12], fill=(200, 230, 240, 255), outline=OUT, width=2)
    d.rounded_rectangle([S * .56, S * .24, S * .76, S * .46], 6, fill=(150, 155, 165, 255), outline=OUT, width=5)
    d.line([(S * .82, S * .1), (S * .9, S * .4), (S * .84, S * .7), (S * .92, S * .92)], fill=(30, 30, 34, 255), width=6)   # the snapped line
    d.line([(S * .18, S * .1), (S * .02, S * .2)], fill=(30, 30, 34, 255), width=5)
    return _shrink(im, size)


def wire_end(size=32):
    """The sparking end of a snapped power line."""
    im, d, S = _big(size)
    d.line([(S * .1, S * .1), (S * .5, S * .5)], fill=(30, 30, 34, 255), width=int(S * .12))
    for a, b in (((.5, .5), (.86, .3)), ((.5, .5), (.9, .62)), ((.5, .5), (.66, .9)), ((.5, .5), (.3, .82))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(255, 250, 120, 255), width=5)
    d.ellipse([S * .4, S * .4, S * .6, S * .6], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def zig_bolt(n=16):
    """A short zig-zag lightning bolt (alpha only)."""
    def f(x, y):
        xx = 8 + (3 if (y // 4) % 2 else -3) * (1 - abs((y % 4) - 2) / 2)
        return 1 if abs(x - xx) < 1.6 and 1 < y < 15 else 0
    return _alpha(n, n, f)


def grocery_cart(size=64):
    """A chrome shopping cart facing right, the red handle at the back, four casters."""
    im, d, S = _big(size)
    OUT = (40, 40, 46, 255)
    C = (200, 205, 215, 255)
    d.polygon([(S * .12, S * .26), (S * .9, S * .3), (S * .8, S * .66), (S * .2, S * .66)], fill=(220, 225, 235, 120), outline=OUT)
    for k in range(6):
        x = .16 + k * .13
        d.line([(S * x, S * .28), (S * (x + .02), S * .66)], fill=C, width=4)
    for k in range(3):
        y = .34 + k * .1
        d.line([(S * .14, S * y), (S * .88, S * (y + .02))], fill=C, width=4)
    d.line([(S * .12, S * .26), (S * .9, S * .3), (S * .8, S * .66), (S * .2, S * .66), (S * .12, S * .26)], fill=OUT, width=6)
    d.line([(S * .12, S * .26), (S * .04, S * .14)], fill=OUT, width=7)
    d.line([(S * .0, S * .14), (S * .1, S * .14)], fill=(220, 30, 30, 255), width=9)                                # handle
    d.line([(S * .2, S * .66), (S * .26, S * .82), (S * .82, S * .82), (S * .8, S * .66)], fill=OUT, width=6)
    for x in (.28, .78):
        d.ellipse([S * (x - .06), S * .82, S * (x + .06), S * .94], fill=(30, 30, 34, 255), outline=OUT, width=3)
    return _shrink(im, size)


def demo_ball(size=64):
    """A huge black wrecking ball on its chain (the chain runs up off the top)."""
    im, d, S = _big(size)
    OUT = (5, 5, 8, 255)
    for k in range(5):
        y = k * .08
        d.ellipse([S * .46, S * y, S * .54, S * (y + .1)], outline=(110, 110, 120, 255), width=5)
    d.rectangle([S * .44, S * .38, S * .56, S * .46], fill=(70, 70, 76, 255), outline=OUT, width=4)
    d.ellipse([S * .14, S * .42, S * .86, S * .98], fill=(40, 40, 46, 255), outline=OUT, width=7)
    d.arc([S * .22, S * .5, S * .6, S * .8], 200, 290, fill=(140, 140, 150, 255), width=8)
    return _shrink(im, size)


def amp_stack(size=64):
    """A tall guitar amp stack: two black speaker cabinets, grille cloth, a gold logo plate, knobs on the head."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.rectangle([S * .18, S * .04, S * .82, S * .2], fill=(30, 30, 34, 255), outline=OUT, width=6)
    for k in range(5):
        d.ellipse([S * (.26 + k * .11), S * .1, S * (.32 + k * .11), S * .16], fill=(230, 190, 60, 255))
    for y0 in (.2, .58):
        d.rectangle([S * .14, S * y0, S * .86, S * (y0 + .38)], fill=(30, 30, 34, 255), outline=OUT, width=6)
        d.rectangle([S * .2, S * (y0 + .05), S * .8, S * (y0 + .33)], fill=(70, 70, 76, 255))
        for k in range(6):
            d.line([(S * .2, S * (y0 + .08 + k * .045)), (S * .8, S * (y0 + .08 + k * .045))], fill=(55, 55, 60, 255), width=2)
    d.rectangle([S * .4, S * .24, S * .6, S * .3], fill=(230, 190, 60, 255))
    return _shrink(im, size)


def mega_soaker(size=64, pumped=False):
    """A giant neon water gun: green body, big orange water tank on top, the pump handle under the barrel (slid back
    when pumped)."""
    im, d, S = _big(size)
    OUT = (20, 30, 10, 255)
    d.rounded_rectangle([S * .14, S * .4, S * .84, S * .58], 10, fill=(80, 210, 70, 255), outline=OUT, width=6)
    d.rectangle([S * .84, S * .44, S * .98, S * .54], fill=(250, 230, 40, 255), outline=OUT, width=4)             # nozzle
    d.rounded_rectangle([S * .24, S * .12, S * .66, S * .42], 14, fill=(250, 130, 30, 220), outline=OUT, width=6)  # tank
    d.line([(S * .3, S * .18), (S * .3, S * .36)], fill=(255, 220, 160, 255), width=5)
    d.polygon([(S * .2, S * .58), (S * .34, S * .58), (S * .28, S * .86), (S * .14, S * .86)], fill=(80, 210, 70, 255), outline=OUT)
    px = .5 if pumped else .64
    d.rounded_rectangle([S * px, S * .58, S * (px + .2), S * .7], 6, fill=(250, 230, 40, 255), outline=OUT, width=5)   # pump
    return _shrink(im, size)


# ---- set 26, batch 2: Night Night, Dome Piece, Drill, Cold Case, Bat Rush ---------------------------------------------

def music_box(size=64):
    """A little pink music box, lid open, a tiny ballerina on top, the wind-up key on the side."""
    im, d, S = _big(size)
    OUT = (80, 30, 60, 255)
    d.rectangle([S * .16, S * .56, S * .84, S * .92], fill=(250, 170, 210, 255), outline=OUT, width=6)
    d.polygon([(S * .16, S * .56), (S * .84, S * .56), (S * .9, S * .26), (S * .22, S * .26)], fill=(255, 200, 230, 255), outline=OUT)
    d.line([(S * .16, S * .56), (S * .84, S * .56), (S * .9, S * .26), (S * .22, S * .26), (S * .16, S * .56)], fill=OUT, width=5)
    d.line([(S * .5, S * .56), (S * .5, S * .38)], fill=(200, 180, 200, 255), width=4)
    d.ellipse([S * .44, S * .3, S * .56, S * .4], fill=(255, 240, 240, 255), outline=OUT, width=3)
    d.polygon([(S * .4, S * .5), (S * .6, S * .5), (S * .5, S * .4)], fill=(255, 150, 200, 255), outline=OUT)
    d.rectangle([S * .84, S * .68, S * .96, S * .74], fill=(230, 190, 60, 255), outline=OUT, width=3)
    d.ellipse([S * .9, S * .62, S * .98, S * .8], outline=(230, 190, 60, 255), width=4)
    return _shrink(im, size)


def big_pacifier(size=64):
    """A giant baby pacifier: blue shield, ring handle, the nipple pointing left."""
    im, d, S = _big(size)
    OUT = (20, 40, 90, 255)
    d.ellipse([S * .04, S * .38, S * .34, S * .62], fill=(255, 230, 190, 230), outline=OUT, width=5)
    d.rounded_rectangle([S * .3, S * .2, S * .52, S * .8], 18, fill=(90, 160, 240, 255), outline=OUT, width=6)
    d.ellipse([S * .5, S * .26, S * .96, S * .74], outline=OUT, width=int(S * .1))
    d.ellipse([S * .5, S * .26, S * .96, S * .74], outline=(250, 230, 80, 255), width=int(S * .06))
    return _shrink(im, size)


def football_helmet(size=64):
    """A red football helmet facing right, white stripe, grey face mask."""
    im, d, S = _big(size)
    OUT = (40, 0, 0, 255)
    d.chord([S * .06, S * .08, S * .86, S * .88], 150, 420, fill=(220, 30, 30, 255), outline=OUT, width=7)
    d.arc([S * .16, S * .1, S * .76, S * .5], 200, 340, fill=(255, 255, 255, 255), width=8)
    d.ellipse([S * .3, S * .44, S * .44, S * .58], fill=(30, 30, 34, 255))                                        # ear hole
    for y in (.52, .66, .8):
        d.line([(S * .6, S * y), (S * .96, S * y)], fill=(170, 175, 185, 255), width=6)
    d.line([(S * .72, S * .48), (S * .72, S * .84)], fill=(170, 175, 185, 255), width=6)
    return _shrink(im, size)


def power_drill(size=64, big=0):
    """A cordless power drill pointing right; big 1 = a heavier hammer drill, 2 = a giant industrial drill (yellow,
    long auger bit)."""
    im, d, S = _big(size)
    OUT = (20, 15, 5, 255)
    body = ((40, 120, 220), (230, 60, 30), (250, 200, 30))[big]
    bit = (.66, .78, .98)[big]
    d.rounded_rectangle([S * .1, S * .3, S * .56, S * .5], 10, fill=body + (255,), outline=OUT, width=6)
    d.polygon([(S * .22, S * .5), (S * .36, S * .5), (S * .32, S * .84), (S * .18, S * .84)], fill=(40, 40, 46, 255), outline=OUT)
    d.rectangle([S * .14, S * .84, S * .38, S * .94], fill=(40, 40, 46, 255), outline=OUT, width=4)                # battery
    d.rectangle([S * .56, S * .34, S * .64, S * .46], fill=(60, 60, 66, 255), outline=OUT, width=4)                # chuck
    d.line([(S * .64, S * .4), (S * bit, S * .4)], fill=(190, 195, 205, 255), width=int(S * (.04 + big * .02)))
    for k in range(int((bit - .64) / .06)):
        x = .66 + k * .06
        d.line([(S * x, S * .36), (S * (x + .03), S * .44)], fill=(110, 110, 120, 255), width=3)
    return _shrink(im, size)


def evidence_board(size=64):
    """A detective's corkboard: pinned photos and notes connected with red string."""
    im, d, S = _big(size)
    OUT = (60, 35, 15, 255)
    d.rectangle([S * .04, S * .1, S * .96, S * .9], fill=(200, 150, 90, 255), outline=OUT, width=7)
    pins = [(.2, .24), (.7, .22), (.45, .5), (.22, .7), (.76, .7)]
    for a, b in ((0, 2), (1, 2), (2, 3), (2, 4), (0, 1)):
        d.line([(S * pins[a][0], S * pins[a][1]), (S * pins[b][0], S * pins[b][1])], fill=(220, 30, 30, 255), width=3)
    for k, (x, y) in enumerate(pins):
        d.rectangle([S * (x - .09), S * (y - .07), S * (x + .09), S * (y + .07)], fill=(250, 250, 245, 255) if k % 2 else (240, 230, 160, 255), outline=OUT, width=3)
        d.ellipse([S * (x - .02), S * (y - .1), S * (x + .02), S * (y - .06)], fill=(220, 30, 30, 255))
    return _shrink(im, size)


def case_file(size=64):
    """A manila case file with a big red COLD CASE stamp across it (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (90, 60, 20, 255)
    d.rectangle([S * .1, S * .16, S * .9, S * .88], fill=(230, 200, 130, 255), outline=OUT, width=6)
    d.rectangle([S * .1, S * .08, S * .4, S * .18], fill=(230, 200, 130, 255), outline=OUT, width=5)
    d.rectangle([S * .14, S * .42, S * .86, S * .66], outline=(200, 30, 30, 255), width=6)
    im = _shrink(im, size)
    return _texted(im, [("COLD", (32, 28)), ("CASE", (32, 35))], (200, 30, 30, 255), (230, 200, 130, 255))


def case_ice(size=64):
    """A big clear ice block with frosted edges and shine (drawn over a frozen battler)."""
    im, d, S = _big(size)
    d.rounded_rectangle([S * .06, S * .06, S * .94, S * .94], 12, fill=(170, 220, 250, 120), outline=(230, 245, 255, 255), width=8)
    d.line([(S * .2, S * .16), (S * .2, S * .5)], fill=(255, 255, 255, 220), width=8)
    d.line([(S * .3, S * .16), (S * .3, S * .3)], fill=(255, 255, 255, 220), width=5)
    for x, y in ((.7, .8), (.82, .66), (.6, .9)):
        d.line([(S * (x - .04), S * y), (S * (x + .04), S * y)], fill=(255, 255, 255, 255), width=4)
        d.line([(S * x, S * (y - .04)), (S * x, S * (y + .04))], fill=(255, 255, 255, 255), width=4)
    return _shrink(im, size)


def alu_bat(size=64):
    """An aluminum softball bat, silver with a black grip, angled."""
    im, d, S = _big(size)
    OUT = (30, 30, 36, 255)
    d.line([(S * .16, S * .86), (S * .84, S * .18)], fill=OUT, width=int(S * .16))
    d.line([(S * .16, S * .86), (S * .84, S * .18)], fill=(200, 205, 215, 255), width=int(S * .11))
    d.line([(S * .1, S * .92), (S * .34, S * .68)], fill=(30, 30, 34, 255), width=int(S * .1))
    d.line([(S * .4, S * .56), (S * .8, S * .18)], fill=(250, 250, 255, 255), width=4)
    return _shrink(im, size)


def tiny_note(n=16):
    """A single eighth note (alpha only)."""
    def f(x, y):
        head = ((x - 5.5) / 3.2) ** 2 + ((y - 12) / 2.4) ** 2 < 1
        stem = 7.6 <= x <= 8.8 and 2 <= y <= 12
        flag = 8.8 <= x <= 12 and 2 <= y <= 4 + (x - 8.8) * .6
        return 1 if head or stem or flag else 0
    return _alpha(n, n, f)


# ---- set 26, batch 3: Speed Bag, Trash Can, Comeback, Wish List, Deep End ---------------------------------------------

def speed_bag(size=64, swing=0):
    """A boxing speed bag hanging under its round wooden platform; swing -1/0/1 tilts it mid-bounce."""
    im, d, S = _big(size)
    OUT = (40, 10, 10, 255)
    d.ellipse([S * .1, S * .04, S * .9, S * .2], fill=(150, 100, 50, 255), outline=OUT, width=6)
    bag = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    b = ImageDraw.Draw(bag)
    b.line([(S * .5, S * .18), (S * .5, S * .26)], fill=(60, 60, 66, 255), width=6)
    b.ellipse([S * .32, S * .24, S * .68, S * .8], fill=(200, 30, 30, 255), outline=OUT, width=6)
    b.arc([S * .36, S * .3, S * .56, S * .6], 200, 280, fill=(255, 140, 130, 255), width=6)
    if swing:
        bag = bag.rotate(-28 * swing, center=(S * .5, S * .2), resample=Image.BICUBIC)
    im.alpha_composite(bag)
    return _shrink(im, size)


def red_glove(size=64):
    """A red boxing glove punching right, white cuff."""
    im, d, S = _big(size)
    OUT = (60, 0, 0, 255)
    d.rounded_rectangle([S * .06, S * .36, S * .3, S * .7], 8, fill=(250, 250, 250, 255), outline=OUT, width=6)
    d.ellipse([S * .24, S * .2, S * .94, S * .84], fill=(220, 30, 30, 255), outline=OUT, width=7)
    d.ellipse([S * .3, S * .56, S * .56, S * .86], fill=(200, 25, 25, 255), outline=OUT, width=6)                  # thumb
    d.arc([S * .36, S * .26, S * .8, S * .56], 200, 300, fill=(255, 140, 130, 255), width=7)
    return _shrink(im, size)


def trash_bag(size=32):
    """A black trash bag, tied at the top, bulging."""
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    d.ellipse([S * .12, S * .3, S * .88, S * .96], fill=(40, 40, 46, 255), outline=OUT, width=5)
    d.polygon([(S * .4, S * .32), (S * .3, S * .06), (S * .5, S * .2), (S * .7, S * .06), (S * .6, S * .32)], fill=(40, 40, 46, 255), outline=OUT)
    d.arc([S * .22, S * .4, S * .5, S * .7], 200, 280, fill=(110, 110, 120, 255), width=5)
    return _shrink(im, size)


def garbage_truck(size=64):
    """A green garbage truck facing right, the big compactor body tipped up at the back, dripping."""
    im, d, S = _big(size)
    OUT = (10, 30, 10, 255)
    d.polygon([(S * .02, S * .24), (S * .62, S * .3), (S * .62, S * .72), (S * .06, S * .72)], fill=(60, 150, 70, 255), outline=OUT)
    d.line([(S * .02, S * .24), (S * .62, S * .3), (S * .62, S * .72), (S * .06, S * .72), (S * .02, S * .24)], fill=OUT, width=6)
    for k in range(3):
        d.line([(S * (.14 + k * .14), S * .3), (S * (.16 + k * .14), S * .7)], fill=(40, 110, 50, 255), width=4)
    d.rectangle([S * .62, S * .38, S * .94, S * .72], fill=(240, 240, 240, 255), outline=OUT, width=6)          # cab
    d.rectangle([S * .74, S * .42, S * .9, S * .54], fill=(120, 180, 230, 255), outline=OUT, width=4)
    for x in (.18, .44, .8):
        d.ellipse([S * (x - .08), S * .66, S * (x + .08), S * .82], fill=(25, 25, 28, 255), outline=OUT, width=4)
    d.ellipse([S * .02, S * .7, S * .08, S * .78], fill=(140, 160, 60, 255))                                       # drip
    return _shrink(im, size)


def trash_pile(size=64):
    """A heap of garbage: bags, a pizza box, a banana peel, a fish skeleton, flies."""
    im, d, S = _big(size)
    OUT = (20, 20, 22, 255)
    d.ellipse([S * .04, S * .5, S * .96, S * .98], fill=(70, 70, 76, 255), outline=OUT, width=5)
    for x, y in ((.2, .52), (.5, .42), (.72, .56)):
        d.ellipse([S * (x - .14), S * (y - .12), S * (x + .14), S * (y + .12)], fill=(40, 40, 46, 255), outline=OUT, width=5)
    d.polygon([(S * .32, S * .66), (S * .58, S * .6), (S * .62, S * .72), (S * .36, S * .78)], fill=(210, 170, 110, 255), outline=OUT)   # pizza box
    d.arc([S * .66, S * .66, S * .86, S * .86], 180, 330, fill=(250, 220, 60, 255), width=8)                      # banana peel
    d.line([(S * .1, S * .76), (S * .28, S * .76)], fill=(230, 230, 230, 255), width=4)                            # fish bones
    for x in (.14, .18, .22):
        d.line([(S * x, S * .72), (S * x, S * .8)], fill=(230, 230, 230, 255), width=3)
    return _shrink(im, size)


def scoreboard(size=64, home="0", away="99"):
    """A stadium scoreboard: HOME and AWAY with big amber digits (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (10, 10, 14, 255)
    d.rectangle([S * .02, S * .12, S * .98, S * .8], fill=(20, 20, 26, 255), outline=(120, 120, 130, 255), width=7)
    d.rectangle([S * .44, S * .8, S * .56, S * .96], fill=(90, 90, 96, 255), outline=OUT, width=4)
    d.line([(S * .5, S * .18), (S * .5, S * .74)], fill=(80, 80, 90, 255), width=4)
    im = _shrink(im, size)
    _texted(im, [("HOME", (16, 10)), ("AWAY", (48, 10))], (255, 255, 255, 255), (20, 20, 26, 255))
    _big_text(im, home, (16, 32), (255, 190, 40, 255), scale=2, font=SMALL)
    _big_text(im, away, (48, 32), (255, 190, 40, 255), scale=2, font=SMALL)
    return im


def bday_cake(size=64, lit=True):
    """A birthday cake: pink frosting, sprinkles, three candles - flames on (lit) or smoking out."""
    im, d, S = _big(size)
    OUT = (80, 40, 30, 255)
    d.rectangle([S * .12, S * .5, S * .88, S * .9], fill=(250, 240, 220, 255), outline=OUT, width=6)
    d.rectangle([S * .12, S * .5, S * .88, S * .62], fill=(255, 150, 200, 255), outline=OUT, width=5)
    for x in (.2, .34, .5, .66, .8):
        d.rectangle([S * x, S * .66, S * (x + .04), S * .7], fill=((80, 160, 250), (250, 200, 40), (120, 220, 90))[int(x * 10) % 3] + (255,))
    for x in (.3, .5, .7):
        d.rectangle([S * (x - .03), S * .3, S * (x + .03), S * .5], fill=(120, 190, 250, 255), outline=OUT, width=3)
        if lit:
            d.ellipse([S * (x - .04), S * .16, S * (x + .04), S * .3], fill=(255, 200, 40, 255))
            d.ellipse([S * (x - .02), S * .21, S * (x + .02), S * .29], fill=(255, 250, 200, 255))
        else:
            d.line([(S * x, S * .28), (S * (x + .03), S * .2), (S * (x - .02), S * .12)], fill=(180, 180, 185, 255), width=4)
    return _shrink(im, size)


def kiddie_pool(size=64):
    """An inflatable blue kiddie pool full of water, seen from the side-top."""
    im, d, S = _big(size)
    OUT = (20, 40, 90, 255)
    d.ellipse([S * .04, S * .44, S * .96, S * .9], fill=(60, 130, 230, 255), outline=OUT, width=7)
    d.ellipse([S * .14, S * .5, S * .86, S * .8], fill=(120, 200, 250, 255))
    d.arc([S * .04, S * .44, S * .96, S * .9], 200, 340, fill=(160, 210, 255, 255), width=6)
    d.arc([S * .3, S * .56, S * .6, S * .7], 200, 320, fill=(255, 255, 255, 255), width=4)
    return _shrink(im, size)


# ---- set 26, batch 4: Pillow Fight, Bad Sushi, Blindside, Uppercut, Sandbag ---------------------------------------------

def fluffy_pillow(size=64):
    """A big white bed pillow with puffy corners and a seam."""
    im, d, S = _big(size)
    OUT = (110, 110, 130, 255)
    d.rounded_rectangle([S * .06, S * .24, S * .94, S * .76], 30, fill=(250, 250, 255, 255), outline=OUT, width=6)
    for x, y in ((.06, .24), (.94, .24), (.06, .76), (.94, .76)):
        d.ellipse([S * (x - .06), S * (y - .06), S * (x + .06), S * (y + .06)], fill=(250, 250, 255, 255), outline=OUT, width=4)
    d.line([(S * .2, S * .5), (S * .8, S * .5)], fill=(210, 210, 225, 255), width=4)
    d.arc([S * .14, S * .3, S * .5, S * .48], 200, 300, fill=(255, 255, 255, 255), width=5)
    return _shrink(im, size)


def sushi_tray(size=64):
    """A gas-station sushi tray: clear plastic lid, six rolls, a fake grass divider, a little wasabi - kind of grey."""
    im, d, S = _big(size)
    OUT = (40, 40, 50, 255)
    d.rounded_rectangle([S * .04, S * .36, S * .96, S * .82], 8, fill=(30, 30, 34, 255), outline=OUT, width=5)
    for k in range(6):
        x = .12 + (k % 3) * .2
        y = .42 + (k // 3) * .18
        d.ellipse([S * x, S * y, S * (x + .16), S * (y + .14)], fill=(40, 50, 40, 255), outline=OUT, width=3)
        d.ellipse([S * (x + .03), S * (y + .03), S * (x + .13), S * (y + .11)], fill=(235, 230, 220, 255))
        d.ellipse([S * (x + .06), S * (y + .05), S * (x + .1), S * (y + .09)], fill=(230, 120, 100, 255))
    d.polygon([(S * .74, S * .48), (S * .9, S * .48), (S * .82, S * .76)], fill=(60, 180, 70, 255))               # plastic grass
    d.ellipse([S * .76, S * .7, S * .88, S * .78], fill=(140, 190, 60, 255))                                       # wasabi
    d.rounded_rectangle([S * .02, S * .26, S * .98, S * .4], 6, fill=(220, 235, 245, 150), outline=OUT, width=4)   # lid
    return _shrink(im, size)


def sushi_roll(size=32):
    """One maki roll, a little off-color."""
    im, d, S = _big(size)
    OUT = (30, 30, 30, 255)
    d.ellipse([S * .1, S * .1, S * .9, S * .9], fill=(40, 50, 40, 255), outline=OUT, width=6)
    d.ellipse([S * .22, S * .22, S * .78, S * .78], fill=(225, 225, 205, 255))
    d.ellipse([S * .38, S * .38, S * .62, S * .62], fill=(200, 140, 110, 255))
    return _shrink(im, size)


def sneak_box(size=64, alert=False):
    """A cardboard box sneaking along (someone's under it) - with a red ! over it when spotted."""
    im, d, S = _big(size)
    OUT = (90, 60, 20, 255)
    d.rectangle([S * .12, S * .4, S * .88, S * .9], fill=(205, 160, 100, 255), outline=OUT, width=6)
    d.polygon([(S * .12, S * .4), (S * .88, S * .4), (S * .8, S * .3), (S * .2, S * .3)], fill=(185, 140, 85, 255), outline=OUT)
    d.rectangle([S * .44, S * .4, S * .56, S * .9], fill=(230, 200, 150, 255))                                     # tape
    d.rectangle([S * .3, S * .56, S * .44, S * .62], fill=(40, 30, 20, 255))                                       # peep slit
    if alert:
        d.rectangle([S * .46, S * .0, S * .56, S * .18], fill=(230, 30, 30, 255))
        d.rectangle([S * .46, S * .21, S * .56, S * .27], fill=(230, 30, 30, 255))
    return _shrink(im, size)


def upper_glove(size=64):
    """A red boxing glove punching straight up, white cuff at the bottom."""
    im, d, S = _big(size)
    OUT = (60, 0, 0, 255)
    d.rounded_rectangle([S * .32, S * .7, S * .68, S * .94], 8, fill=(250, 250, 250, 255), outline=OUT, width=6)
    d.ellipse([S * .18, S * .06, S * .82, S * .76], fill=(220, 30, 30, 255), outline=OUT, width=7)
    d.ellipse([S * .08, S * .36, S * .38, S * .64], fill=(200, 25, 25, 255), outline=OUT, width=6)
    d.arc([S * .26, S * .12, S * .6, S * .5], 200, 300, fill=(255, 140, 130, 255), width=7)
    return _shrink(im, size)


def sandbag(size=32):
    """A tan burlap sandbag, tied."""
    im, d, S = _big(size)
    OUT = (90, 70, 30, 255)
    d.rounded_rectangle([S * .06, S * .3, S * .94, S * .78], 14, fill=(215, 190, 130, 255), outline=OUT, width=5)
    for x in (.26, .5, .74):
        d.line([(S * x, S * .34), (S * (x + .04), S * .74)], fill=(190, 160, 100, 255), width=3)
    d.ellipse([S * .82, S * .44, S * .96, S * .62], fill=(190, 160, 100, 255), outline=OUT, width=3)
    return _shrink(im, size)


# ---- set 26, batch 5: Weed Whacker, Sledgehammer, Seed Toss, Jet Ski, Back Alley ----------------------------------------

def string_trimmer(size=64):
    """A weed whacker: orange motor at the top, long shaft, the spinning head with the line at the bottom right."""
    im, d, S = _big(size)
    OUT = (20, 15, 5, 255)
    d.line([(S * .2, S * .2), (S * .8, S * .8)], fill=(20, 15, 5, 255), width=int(S * .11))
    d.line([(S * .2, S * .2), (S * .8, S * .8)], fill=(170, 175, 185, 255), width=int(S * .07))
    d.rounded_rectangle([S * .06, S * .06, S * .32, S * .3], 8, fill=(250, 130, 30, 255), outline=OUT, width=6)
    d.line([(S * .42, S * .36), (S * .5, S * .3)], fill=OUT, width=6)                                            # handle
    d.ellipse([S * .66, S * .66, S * .96, S * .96], fill=(60, 60, 66, 255), outline=OUT, width=6)
    for a, b in (((.82, .82), (.98, .7)), ((.82, .82), (.66, .98))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=(250, 220, 60, 255), width=7)
    return _shrink(im, size)


def grass_clip(n=16):
    """A grass clipping (alpha only): a short thin blade."""
    return _alpha(n, n, lambda x, y: 1 if abs((x - 3) - (y - 3) * .8) < 1.1 and 2 < y < 14 else 0)




def jet_ski(size=64):
    """A red and white jet ski facing right, handlebars up, spray kicking off the back."""
    im, d, S = _big(size)
    OUT = (30, 10, 10, 255)
    d.polygon([(S * .04, S * .56), (S * .8, S * .5), (S * .98, S * .62), (S * .86, S * .74), (S * .08, S * .74)], fill=(220, 30, 30, 255), outline=OUT)
    d.line([(S * .04, S * .56), (S * .8, S * .5), (S * .98, S * .62), (S * .86, S * .74), (S * .08, S * .74), (S * .04, S * .56)], fill=OUT, width=6)
    d.polygon([(S * .2, S * .5), (S * .56, S * .48), (S * .52, S * .56), (S * .2, S * .58)], fill=(240, 240, 245, 255), outline=OUT)  # seat
    d.line([(S * .62, S * .5), (S * .66, S * .3)], fill=(60, 60, 66, 255), width=6)
    d.line([(S * .58, S * .3), (S * .74, S * .28)], fill=(60, 60, 66, 255), width=7)                              # handlebars
    d.line([(S * .1, S * .68), (S * .8, S * .66)], fill=(250, 250, 250, 255), width=4)
    for x, y in ((.0, .7), (.06, .8), (.02, .62)):
        d.ellipse([S * x, S * y, S * (x + .08), S * (y + .08)], fill=(200, 230, 255, 255))
    return _shrink(im, size)


def shoe_print(n=16):
    """A sneaker footprint (alpha only): sole with a tread gap and the heel."""
    def f(x, y):
        sole = ((x - 7.5) / 3.6) ** 2 + ((y - 5.5) / 4.6) ** 2 < 1
        heel = ((x - 7.5) / 2.8) ** 2 + ((y - 12.5) / 2.4) ** 2 < 1
        return (.85 if y % 3 else .4) if sole else (1 if heel else 0)
    return _alpha(n, n, f)


def mole_hole(size=64):
    """A dirt mound with a dark hole in the top (the whack-a-mole hole)."""
    im, d, S = _big(size)
    OUT = (50, 30, 10, 255)
    d.chord([S * .06, S * .44, S * .94, S * 1.2], 180, 360, fill=(140, 95, 50, 255), outline=OUT, width=6)
    d.ellipse([S * .3, S * .5, S * .7, S * .64], fill=(30, 20, 10, 255))
    for x, y in ((.2, .7), (.76, .74), (.5, .78)):
        d.ellipse([S * x, S * y, S * (x + .06), S * (y + .04)], fill=(110, 75, 40, 255))
    return _shrink(im, size)


def arcade_mole(size=64):
    """A cartoon mole popping up: brown fur, pink nose, buck teeth, beady eyes."""
    im, d, S = _big(size)
    OUT = (40, 20, 10, 255)
    d.rounded_rectangle([S * .28, S * .2, S * .72, S * .9], 22, fill=(140, 90, 60, 255), outline=OUT, width=6)
    for x in (.38, .56):
        d.ellipse([S * x, S * .34, S * (x + .06), S * .42], fill=OUT)
    d.ellipse([S * .44, S * .44, S * .56, S * .54], fill=(255, 140, 170, 255), outline=OUT, width=3)
    d.rectangle([S * .46, S * .54, S * .54, S * .62], fill=(255, 255, 255, 255), outline=OUT, width=2)
    return _shrink(im, size)


def foam_mallet(size=64):
    """A whack-a-mole foam mallet: a big padded red head on a yellow handle."""
    im, d, S = _big(size)
    OUT = (60, 10, 10, 255)
    d.line([(S * .2, S * .9), (S * .56, S * .4)], fill=OUT, width=int(S * .1))
    d.line([(S * .2, S * .9), (S * .56, S * .4)], fill=(250, 210, 40, 255), width=int(S * .06))
    d.rounded_rectangle([S * .4, S * .1, S * .96, S * .44], 18, fill=(220, 40, 40, 255), outline=OUT, width=7)
    d.line([(S * .48, S * .18), (S * .86, S * .18)], fill=(255, 130, 120, 255), width=6)
    return _shrink(im, size)


def chia_fuzz(size=64, stage=0):
    """Chia sprouts growing on top of someone's head: 0 = a few green sprouts, 1 = a fuzzy layer, 2 = a full green afro."""
    import random
    im, d, S = _big(size)
    r = random.Random(4 + stage)
    if stage == 2:
        d.ellipse([S * .06, S * .1, S * .94, S * .84], fill=(70, 160, 60, 255), outline=(30, 90, 30, 255), width=6)
    n = (8, 30, 70)[stage]
    top, bot = ((.62, .9), (.4, .9), (.12, .8))[stage]
    for _ in range(n):
        x, y = r.uniform(.14, .86), r.uniform(top, bot)
        d.line([(S * x, S * (y + .08)), (S * (x + r.uniform(-.04, .04)), S * y)], fill=(60, 170, 60, 255), width=4)
        d.ellipse([S * (x - .03), S * (y - .03), S * (x + .03), S * (y + .03)], fill=(140, 220, 100, 255))
    return _shrink(im, size)


def spray_bottle(size=32):
    """A blue plant mister spray bottle, nozzle right."""
    im, d, S = _big(size)
    OUT = (20, 40, 80, 255)
    d.rounded_rectangle([S * .2, S * .4, S * .6, S * .96], 8, fill=(120, 190, 250, 220), outline=OUT, width=5)
    d.rectangle([S * .26, S * .26, S * .54, S * .4], fill=(250, 250, 250, 255), outline=OUT, width=4)
    d.polygon([(S * .54, S * .26), (S * .9, S * .26), (S * .9, S * .34), (S * .54, S * .34)], fill=(250, 250, 250, 255), outline=OUT)
    d.line([(S * .54, S * .36), (S * .68, S * .5)], fill=OUT, width=5)
    return _shrink(im, size)


# ---- set 26, batch 6: Finesse, Ext. Cord, Two-by-Four, Kick Back, Slow Jam ----------------------------------------------

def lemme_bubble(size=64):
    """A white speech bubble: LEMME / SEE THAT (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.rounded_rectangle([S * .02, S * .22, S * .98, S * .74], 26, fill=(255, 255, 255, 255), outline=OUT, width=8)
    d.polygon([(S * .22, S * .7), (S * .12, S * .94), (S * .4, S * .72)], fill=(255, 255, 255, 255))
    d.line([(S * .22, S * .74), (S * .12, S * .94), (S * .4, S * .74)], fill=OUT, width=7)
    im = _shrink(im, size)
    return _texted(im, [("LEMME", (32, 19)), ("SEE THAT", (32, 30))], (20, 20, 25, 255), (255, 255, 255, 255))


def fresh_snapback(size=64):
    """A brand-new snapback: black crown, flat red brim with the gold sticker still on it, the button on top."""
    im, d, S = _big(size)
    OUT = (15, 10, 10, 255)
    d.chord([S * .12, S * .14, S * .84, S * .9], 180, 360, fill=(30, 30, 40, 255), outline=OUT, width=7)
    d.rectangle([S * .12, S * .5, S * .84, S * .6], fill=(30, 30, 40, 255), outline=OUT, width=6)
    d.line([(S * .48, S * .16), (S * .48, S * .5)], fill=(70, 70, 85, 255), width=4)                             # panel seam
    d.ellipse([S * .44, S * .1, S * .52, S * .18], fill=(30, 30, 40, 255), outline=OUT, width=3)                 # button
    d.polygon([(S * .5, S * .56), (S * .98, S * .56), (S * .98, S * .68), (S * .5, S * .66)], fill=(220, 30, 40, 255), outline=OUT)
    d.line([(S * .5, S * .56), (S * .98, S * .56), (S * .98, S * .68), (S * .5, S * .66)], fill=OUT, width=6)    # flat brim
    d.ellipse([S * .7, S * .57, S * .82, S * .66], fill=(250, 210, 50, 255), outline=(150, 110, 0, 255), width=3)  # the sticker
    d.arc([S * .2, S * .22, S * .56, S * .56], 200, 260, fill=(110, 110, 130, 255), width=5)                      # shine
    return _shrink(im, size)


def ext_cord(size=64, swung=False):
    """The orange extension cord: coiled up with the plug hanging out - or swung out long, folded over double."""
    im, d, S = _big(size)
    OUT = (90, 30, 0, 255)
    OR = (250, 130, 20, 255)
    if not swung:
        for k in range(4):
            r = .3 - k * .03
            d.ellipse([S * (.5 - r), S * (.48 - r * .9), S * (.5 + r), S * (.48 + r * .9)], outline=OUT, width=13)
            d.ellipse([S * (.5 - r), S * (.48 - r * .9), S * (.5 + r), S * (.48 + r * .9)], outline=OR, width=8)
        d.line([(S * .74, S * .62), (S * .82, S * .84)], fill=OUT, width=12)
        d.line([(S * .74, S * .62), (S * .82, S * .84)], fill=OR, width=7)
        plug = (.82, .84)
    else:                                                                       # folded double: the loop is the business end
        for off in (-.035, .035):
            pts = [(S * (.08 + t * .84), S * (.5 + off + .22 * __import__("math").sin(t * 5.2))) for t in [i / 24 for i in range(25)]]
            d.line(pts, fill=OUT, width=12, joint="curve")
            d.line(pts, fill=OR, width=7, joint="curve")
        d.ellipse([S * .86, S * .2, S * .98, S * .64], outline=OUT, width=12)
        d.ellipse([S * .86, S * .2, S * .98, S * .64], outline=OR, width=7)
        plug = (.08, .5)
    px, py = plug
    d.rectangle([S * (px - .06), S * (py - .02), S * (px + .06), S * (py + .1)], fill=(240, 240, 235, 255), outline=OUT, width=4)
    for x in (-.03, .02):                                                       # the prongs
        d.rectangle([S * (px + x), S * (py + .1), S * (px + x + .015), S * (py + .16)], fill=(200, 200, 200, 255), outline=OUT, width=2)
    return _shrink(im, size)


def tape_measure(size=64):
    """A yellow tape measure, the tape pulled out long to the right with tick marks and the little hook."""
    im, d, S = _big(size)
    OUT = (40, 30, 0, 255)
    d.rectangle([S * .3, S * .56, S * .96, S * .66], fill=(255, 235, 90, 255), outline=OUT, width=4)
    for k in range(16):                                                         # ticks
        x = .33 + k * .04
        d.line([(S * x, S * .56), (S * x, S * (.6 if k % 4 else .63))], fill=OUT, width=3)
    d.rectangle([S * .94, S * .5, S * .98, S * .7], fill=(170, 170, 180, 255), outline=OUT, width=3)          # the hook
    d.rounded_rectangle([S * .02, S * .36, S * .38, S * .76], 12, fill=(250, 200, 30, 255), outline=OUT, width=7)
    d.ellipse([S * .1, S * .44, S * .3, S * .66], fill=(60, 60, 66, 255), outline=OUT, width=4)
    d.rectangle([S * .14, S * .28, S * .26, S * .38], fill=(60, 60, 66, 255), outline=OUT, width=4)            # the lock button
    return _shrink(im, size)


def two_by_four(size=64):
    """A 2x4: a long pale pine board on the diagonal, wood grain, a knot, and a bent nail sticking out the end."""
    im, d, S = _big(size)
    OUT = (90, 55, 20, 255)
    pts = [(S * .06, S * .82), (S * .82, S * .06), (S * .96, S * .2), (S * .2, S * .96)]
    _outline_poly(d, pts, (235, 195, 130, 255), OUT, 7)
    d.polygon([(S * .82, S * .06), (S * .96, S * .2), (S * .9, S * .2), (S * .78, S * .1)], fill=(210, 160, 95, 255))   # end grain
    for k in range(3):                                                          # the grain
        o = .05 + k * .04
        d.line([(S * (.14 + o), S * (.82 + o * .2)), (S * (.84 + o * .2), S * (.12 + o))], fill=(200, 150, 90, 255), width=3)
    d.ellipse([S * .42, S * .5, S * .52, S * .58], fill=(160, 100, 50, 255), outline=OUT, width=3)             # knot
    d.line([(S * .88, S * .12), (S * .98, S * .02), (S * .98, S * .1)], fill=(150, 150, 160, 255), width=5)      # bent nail
    return _shrink(im, size)


def wood_chip(n=16):
    """A splinter (alpha only): a thin jagged sliver."""
    return _alpha(n, n, lambda x, y: 1 if abs((x - 8) - (y - 8) * .35) < 1.3 - abs(y - 8) * .07 and 1 < y < 15 else 0)


def recliner(size=64, stage=0):
    """A brown leather recliner. 0 = upright, 1 = footrest popped out, 2 = laid all the way back."""
    im, d, S = _big(size)
    OUT = (40, 20, 10, 255)
    BR, HI = (130, 75, 40, 255), (170, 105, 60, 255)
    back = [((.1, .08), (.44, .08), (.44, .62), (.1, .62)), ((.02, .2), (.34, .1), (.44, .62), (.1, .66)),
            ((-.02, .5), (.06, .3), (.44, .56), (.4, .68))][stage]
    _outline_poly(d, [(S * x, S * y) for x, y in back], BR, OUT, 7)
    a, b_, c, e = back                                                          # tufted padding: two seams across the back
    lerp = lambda p, q, t: (S * (p[0] + (q[0] - p[0]) * t), S * (p[1] + (q[1] - p[1]) * t))
    for t in (.33, .66):
        d.line([lerp(a, e, t), lerp(b_, c, t)], fill=HI, width=5)
    d.rounded_rectangle([S * .3, S * .52, S * .72, S * .7], 10, fill=HI, outline=OUT, width=7)                  # the seat cushion
    d.rounded_rectangle([S * .26, S * .44, S * .7, S * .54], 8, fill=BR, outline=OUT, width=6)                  # armrest
    d.rectangle([S * .3, S * .7, S * .7, S * .86], fill=(100, 55, 30, 255), outline=OUT, width=6)               # base
    d.line([(S * .66, S * .56), (S * .76, S * .5)], fill=(60, 60, 66, 255), width=6)                             # the lever
    if stage:
        foot = ((.7, .66), (.96, .58), (.98, .7), (.72, .78)) if stage == 1 else ((.7, .6), (.98, .54), (.98, .66), (.72, .72))
        _outline_poly(d, [(S * x, S * y) for x, y in foot], HI, OUT, 6)
    return _shrink(im, size)


def jar_candle(size=32, lit=True):
    """A red jar candle - flame on top when lit."""
    im, d, S = _big(size)
    OUT = (60, 10, 20, 255)
    d.rounded_rectangle([S * .22, S * .44, S * .78, S * .96], 8, fill=(200, 40, 60, 255), outline=OUT, width=6)
    d.rectangle([S * .22, S * .56, S * .78, S * .66], fill=(255, 200, 210, 255))                                # the label band
    if lit:
        d.ellipse([S * .36, S * .06, S * .64, S * .46], fill=(255, 170, 40, 255))
        d.ellipse([S * .43, S * .2, S * .57, S * .44], fill=(255, 250, 200, 255))
    d.line([(S * .5, S * .38), (S * .5, S * .46)], fill=OUT, width=4)
    return _shrink(im, size)


def love_note(n=16):
    """A music note with a heart for a head (alpha only)."""
    def f(x, y):
        heart = ((x - 5) ** 2 + (y - 11) ** 2 < 6.5 or (x - 9) ** 2 + (y - 11) ** 2 < 6.5) and y < 13 or (y >= 12 and abs(x - 7) < 15 - y)
        stem = 10 <= x <= 11 and 1 <= y <= 11
        flag = 11 <= x <= 14 and 1 <= y <= 3 + (x - 11) * .4
        return 1 if heart or stem or flag else 0
    return _alpha(n, n, f)


# ---- set 27, batch 1: Send It, Allergy Szn, Blackout, Aura Farm, Rush Hour --------------------------------------------

def hero_cape(size=64, flap=0):
    """A red bedsheet cape tied at the neck, billowing out to the left (flap 1 = blown higher)."""
    im, d, S = _big(size)
    OUT = (70, 0, 10, 255)
    lift = .16 * flap
    pts = [(S * .62, S * .14), (S * .72, S * .2), (S * .66, S * .5), (S * .5, S * (.92 - lift)), (S * .3, S * (.8 - lift)),
           (S * .12, S * (.86 - lift * 1.6)), (S * .06, S * (.6 - lift * 1.4)), (S * .4, S * .3)]
    _outline_poly(d, pts, (220, 30, 40, 255), OUT, 7)
    d.line([(S * .56, S * .28), (S * .24, S * (.72 - lift))], fill=(250, 90, 100, 255), width=5)                 # fold
    d.line([(S * .5, S * .34), (S * .4, S * (.82 - lift))], fill=(170, 20, 30, 255), width=5)
    d.ellipse([S * .56, S * .08, S * .74, S * .22], fill=(250, 250, 250, 255), outline=OUT, width=4)             # the knot
    return _shrink(im, size)


def dive_goggles(size=32):
    """Big swim/aviator goggles: two round blue lenses with glare, black strap."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.line([(S * .0, S * .5), (S * 1.0, S * .5)], fill=OUT, width=10)
    for x in (.08, .52):
        d.ellipse([S * x, S * .26, S * (x + .4), S * .74], fill=(90, 190, 250, 255), outline=OUT, width=7)
        d.arc([S * (x + .08), S * .34, S * (x + .3), S * .58], 200, 280, fill=(240, 250, 255, 255), width=5)
    return _shrink(im, size)


def roof_ledge(size=64):
    """The edge of a projects rooftop: a brick parapet with a tar cap, a satellite dish on it."""
    im, d, S = _big(size)
    OUT = (40, 15, 10, 255)
    d.rectangle([S * .0, S * .5, S * 1.0, S * 1.0], fill=(160, 70, 50, 255), outline=OUT, width=6)
    for r in range(4):                                                          # bricks
        y = .58 + r * .11
        d.line([(0, S * y), (S, S * y)], fill=(110, 45, 30, 255), width=3)
        for c in range(6):
            x = (c + (r % 2) * .5) / 6
            d.line([(S * x, S * (y - .11)), (S * x, S * y)], fill=(110, 45, 30, 255), width=3)
    d.rectangle([S * .0, S * .44, S * 1.0, S * .52], fill=(70, 70, 75, 255), outline=OUT, width=5)            # cap
    d.chord([S * .66, S * .08, S * .96, S * .38], 120, 300, fill=(220, 220, 225, 255), outline=OUT, width=5)    # dish
    d.line([(S * .82, S * .24), (S * .84, S * .44)], fill=OUT, width=5)
    return _shrink(im, size)


def dive_crater(size=64):
    """A smoking impact crater: a cracked dark bowl with rubble chunks thrown up round the rim."""
    im, d, S = _big(size)
    OUT = (30, 20, 15, 255)
    d.ellipse([S * .04, S * .5, S * .96, S * .94], fill=(120, 95, 70, 255), outline=OUT, width=7)
    d.ellipse([S * .18, S * .58, S * .82, S * .86], fill=(50, 35, 25, 255))
    for a, b in (((.3, .7), (.18, .62)), ((.66, .74), (.82, .64)), ((.5, .62), (.52, .54))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=OUT, width=4)
    for x, y, r in ((.08, .44, .07), (.86, .42, .06), (.3, .42, .05), (.68, .4, .05)):
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], fill=(140, 115, 90, 255), outline=OUT, width=4)
    return _shrink(im, size)


def pollen_board(size=64, level="HIGH"):
    """The TV pollen count graphic: POLLEN COUNT over a level bar, green - orange - red by level (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    col = {"HIGH": (240, 200, 40, 255), "VERY HIGH": (250, 130, 30, 255), "EXTREME": (230, 30, 30, 255)}[level]
    n = {"HIGH": 2, "VERY HIGH": 3, "EXTREME": 4}[level]
    d.rounded_rectangle([S * .02, S * .14, S * .98, S * .86], 14, fill=(30, 40, 80, 255), outline=OUT, width=7)
    for k in range(4):                                                          # the level bar
        x = .12 + k * .2
        d.rectangle([S * x, S * .6, S * (x + .16), S * .76], fill=col if k < n else (70, 80, 110, 255), outline=OUT, width=4)
    im = _shrink(im, size)
    return _texted(im, [("POLLEN", (32, 12)), (level, (32, 23))], (255, 255, 255, 255), (20, 20, 25, 255))


def monster_flower(size=64, open_=1):
    """A giant yellow flower (open_ 0 = a fat bud, 1 = wide open with a pollen-dusted centre)."""
    im, d, S = _big(size)
    OUT = (60, 50, 0, 255)
    d.line([(S * .5, S * .56), (S * .5, S * 1.0)], fill=(40, 120, 40, 255), width=int(S * .08))
    d.ellipse([S * .52, S * .74, S * .8, S * .86], fill=(70, 170, 60, 255), outline=(30, 80, 30, 255), width=4)  # leaf
    if not open_:
        d.ellipse([S * .34, S * .24, S * .66, S * .62], fill=(110, 180, 70, 255), outline=(30, 80, 30, 255), width=6)
        d.polygon([(S * .4, S * .3), (S * .5, S * .14), (S * .6, S * .3)], fill=(250, 210, 60, 255), outline=OUT)
        return _shrink(im, size)
    import math
    for k in range(10):
        a = k * math.tau / 10
        cx, cy = .5 + .3 * math.cos(a), .4 + .3 * math.sin(a)
        d.ellipse([S * (cx - .14), S * (cy - .14), S * (cx + .14), S * (cy + .14)], fill=(250, 210, 40, 255), outline=OUT, width=4)
    d.ellipse([S * .3, S * .2, S * .7, S * .6], fill=(140, 80, 30, 255), outline=OUT, width=6)
    for k in range(14):
        x, y = .36 + (k * 37 % 28) / 100, .26 + (k * 23 % 28) / 100
        d.ellipse([S * x, S * y, S * (x + .04), S * (y + .04)], fill=(255, 240, 120, 255))
    return _shrink(im, size)


def pollen_dot(n=16):
    """A fuzzy pollen grain (alpha only): a soft dot with a spiky rim."""
    c = (n - 1) / 2

    def f(x, y):
        r = ((x - c) ** 2 + (y - c) ** 2) ** .5
        return 1 if r < 3.5 else (.6 if r < 5.5 and (x + y) % 2 == 0 else 0)
    return _alpha(n, n, f)


def city_skyline(size=64, lit=3):
    """A row of project towers at night; `lit` of the 3 blocks still have yellow windows on (0 = all dark)."""
    im, d, S = _big(size)
    OUT = (10, 10, 20, 255)
    towers = [(.0, .3, .3), (.28, .12, .26), (.52, .38, .22), (.72, .2, .28)]
    for i, (x, top, w) in enumerate(towers):
        d.rectangle([S * x, S * top, S * (x + w), S * 1.0], fill=(40, 40, 60, 255), outline=OUT, width=5)
        on = (i * 3) // 4 < lit
        for r in range(int((1 - top) / .1) - 1):
            for c in range(int(w / .08)):
                wx, wy = x + .04 + c * .08, top + .06 + r * .1
                if wx + .04 < x + w:
                    lamp = (250, 220, 90, 255) if on and (r * 7 + c * 3 + i) % 5 else (20, 20, 35, 255)
                    d.rectangle([S * wx, S * wy, S * (wx + .04), S * (wy + .05)], fill=lamp)
    return _shrink(im, size)


def dark_eyes(size=32):
    """Two glowing white eyes with tiny pupils, floating in the dark."""
    im, d, S = _big(size)
    for x in (.1, .56):
        d.ellipse([S * x, S * .3, S * (x + .34), S * .7], fill=(250, 250, 255, 255), outline=(120, 120, 180, 255), width=4)
        d.ellipse([S * (x + .12), S * .42, S * (x + .22), S * .58], fill=(10, 10, 20, 255))
    return _shrink(im, size)


def aura_tag(size=64, n="+100"):
    """A floating gamer-style score popup: "+100" over AURA in glowing purple (shown at 1:1)."""
    im, d, S = _big(size)
    d.rounded_rectangle([S * .04, S * .24, S * .96, S * .76], 16, fill=(60, 20, 100, 230), outline=(200, 140, 255, 255), width=6)
    im = _shrink(im, size)
    return _texted(im, [(n, (32, 18)), ("AURA", (32, 30))], (255, 230, 120, 255), (60, 0, 90, 255), font=SMALL)


def aura_orb(size=64):
    """A huge glowing aura ball: a white-hot core in layered blue-violet rings, crackling rim."""
    im, d, S = _big(size)
    for r, c in ((.48, (90, 60, 220, 140)), (.4, (120, 90, 250, 200)), (.3, (170, 150, 255, 255)), (.18, (235, 230, 255, 255)), (.08, (255, 255, 255, 255))):
        d.ellipse([S * (.5 - r), S * (.5 - r), S * (.5 + r), S * (.5 + r)], fill=c)
    import math
    for k in range(8):
        a = k * math.tau / 8 + .3
        d.line([(S * (.5 + .36 * math.cos(a)), S * (.5 + .36 * math.sin(a))), (S * (.5 + .48 * math.cos(a + .2)), S * (.5 + .48 * math.sin(a + .2)))],
               fill=(255, 255, 255, 255), width=4)
    return _shrink(im, size)


def subway_car(size=64, doors_open=False):
    """The front half of a silver subway car: windows, a lit route sign, sliding doors (open = dark gap)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.rounded_rectangle([S * .0, S * .14, S * 1.0, S * .9], 14, fill=(190, 195, 205, 255), outline=OUT, width=7)
    d.rectangle([S * .0, S * .66, S * 1.0, S * .72], fill=(40, 120, 220, 255))                                  # the stripe
    d.rectangle([S * .06, S * .2, S * .34, S * .3], fill=(20, 20, 20, 255), outline=OUT, width=3)                # route sign
    d.ellipse([S * .1, S * .21, S * .18, S * .29], fill=(250, 140, 30, 255))
    for x in (.42, .8):                                                          # windows
        d.rectangle([S * x, S * .24, S * (x + .14), S * .44], fill=(140, 190, 230, 255), outline=OUT, width=4)
    if doors_open:
        d.rectangle([S * .58, S * .24, S * .76, S * .86], fill=(30, 30, 40, 255), outline=OUT, width=5)
    else:
        d.rectangle([S * .58, S * .24, S * .76, S * .86], fill=(170, 175, 185, 255), outline=OUT, width=5)
        d.line([(S * .67, S * .24), (S * .67, S * .86)], fill=OUT, width=4)
        for x in (.6, .69):
            d.rectangle([S * x, S * .3, S * (x + .06), S * .46], fill=(140, 190, 230, 255), outline=OUT, width=3)
    d.ellipse([S * .1, S * .82, S * .26, S * .98], fill=(50, 50, 55, 255), outline=OUT, width=4)
    return _shrink(im, size)


def commuter(size=32, tint=0):
    """A rush-hour commuter mid-stride: suit (3 colors), briefcase swinging, coffee cup held up."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    suit = [(50, 60, 90, 255), (90, 60, 50, 255), (60, 60, 64, 255)][tint % 3]
    d.ellipse([S * .38, S * .04, S * .62, S * .26], fill=(220, 170, 130, 255) if tint != 1 else (140, 90, 60, 255), outline=OUT, width=4)
    d.rounded_rectangle([S * .34, S * .24, S * .66, S * .62], 6, fill=suit, outline=OUT, width=4)
    d.line([(S * .42, S * .62), (S * .3, S * .96)], fill=OUT, width=7)                                           # legs mid-stride
    d.line([(S * .58, S * .62), (S * .72, S * .96)], fill=OUT, width=7)
    d.rectangle([S * .06, S * .48, S * .32, S * .66], fill=(110, 70, 30, 255), outline=OUT, width=4)            # briefcase
    d.rectangle([S * .68, S * .14, S * .84, S * .34], fill=(250, 250, 245, 255), outline=OUT, width=3)          # coffee
    d.rectangle([S * .68, S * .14, S * .84, S * .18], fill=(40, 30, 20, 255))
    return _shrink(im, size)


# ---- set 27, batch 2: RIP Shirt, Fresh Fit, Hotfoot, Space Jam, Dirty Water -------------------------------------------

def rip_tee(size=64):
    """An airbrushed memorial tee: white shirt, a sky-blue cloud with a gold halo and wings, R.I.P. across the top
    (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 40, 50, 255)
    pts = [(S * .3, S * .06), (S * .42, S * .1), (S * .58, S * .1), (S * .7, S * .06), (S * .98, S * .24), (S * .88, S * .42),
           (S * .78, S * .36), (S * .78, S * .98), (S * .22, S * .98), (S * .22, S * .36), (S * .12, S * .42), (S * .02, S * .24)]
    _outline_poly(d, pts, (250, 250, 250, 255), OUT, 7)
    d.arc([S * .4, S * .02, S * .6, S * .18], 0, 180, fill=OUT, width=5)                                         # collar
    d.ellipse([S * .3, S * .46, S * .7, S * .9], fill=(150, 200, 250, 255))                                       # the airbrush cloud
    for x in (.24, .62):                                                                                          # wings
        d.ellipse([S * x, S * .56, S * (x + .14), S * .78], fill=(255, 255, 255, 255), outline=(180, 200, 230, 255), width=3)
    d.ellipse([S * .42, S * .58, S * .58, S * .8], fill=(60, 50, 70, 255))                                         # a silhouette
    d.ellipse([S * .4, S * .5, S * .6, S * .58], outline=(250, 200, 40, 255), width=5)                            # halo
    im = _shrink(im, size)
    return _texted(im, [("R.I.P.", (32, 17))], (60, 120, 220, 255), (255, 255, 255, 255))


def lint_roller(size=64):
    """A lint roller: the sticky white roll with lint stuck on, red handle."""
    im, d, S = _big(size)
    OUT = (40, 10, 10, 255)
    d.line([(S * .5, S * .52), (S * .7, S * .96)], fill=OUT, width=int(S * .12))
    d.line([(S * .5, S * .52), (S * .7, S * .96)], fill=(220, 40, 40, 255), width=int(S * .07))
    d.rounded_rectangle([S * .08, S * .14, S * .92, S * .5], 14, fill=(250, 250, 240, 255), outline=OUT, width=6)
    for x, y in ((.2, .26), (.36, .38), (.6, .22), (.78, .36), (.48, .3)):
        d.ellipse([S * x, S * y, S * (x + .06), S * (y + .05)], fill=(150, 140, 130, 255))
    d.line([(S * .1, S * .2), (S * .9, S * .2)], fill=(220, 220, 210, 255), width=3)
    return _shrink(im, size)


def lint_ball(n=16):
    """A lint fuzzball (alpha only): a scruffy clump."""
    c = (n - 1) / 2
    return _alpha(n, n, lambda x, y: 1 if ((x - c) ** 2 + (y - c) ** 2) ** .5 < 3 + ((x * 7 + y * 3) % 4) * .6 else 0)


def amber_cologne(size=32):
    """A fancy cologne bottle: faceted amber glass, gold cap, a black label."""
    im, d, S = _big(size)
    OUT = (40, 25, 0, 255)
    d.polygon([(S * .2, S * .4), (S * .8, S * .4), (S * .9, S * .7), (S * .7, S * .96), (S * .3, S * .96), (S * .1, S * .7)],
              fill=(230, 150, 40, 230), outline=OUT)
    d.line([(S * .2, S * .4), (S * .8, S * .4), (S * .9, S * .7), (S * .7, S * .96), (S * .3, S * .96), (S * .1, S * .7), (S * .2, S * .4)], fill=OUT, width=5)
    d.rectangle([S * .38, S * .14, S * .62, S * .4], fill=(250, 210, 60, 255), outline=OUT, width=5)
    d.rectangle([S * .32, S * .6, S * .68, S * .76], fill=(20, 20, 20, 255))
    d.line([(S * .26, S * .5), (S * .34, S * .84)], fill=(255, 230, 170, 255), width=4)
    return _shrink(im, size)


def hot_asphalt(size=64):
    """A patch of black summer asphalt baking: a yellow road line, wavy heat shimmer rising off it."""
    im, d, S = _big(size)
    d.polygon([(S * .0, S * .62), (S * 1.0, S * .62), (S * .9, S * .96), (S * .1, S * .96)], fill=(40, 40, 46, 255), outline=(15, 15, 20, 255))
    d.line([(S * .3, S * .8), (S * .7, S * .8)], fill=(250, 210, 40, 255), width=7)
    import math
    for k in range(4):                                                           # heat shimmer
        x0 = .16 + k * .22
        pts = [(S * (x0 + .04 * math.sin(t * 2.4)), S * (.56 - t * .1)) for t in range(5)]
        d.line(pts, fill=(255, 150, 80, 200), width=5, joint="curve")
    return _shrink(im, size)


def hood_slide(size=64, lit=False):
    """A black slide sandal with a white strap stripe, a white tube sock still in it - and on fire if lit."""
    im, d, S = _big(size)
    OUT = (10, 10, 15, 255)
    if lit:
        for x, h in ((.2, .1), (.42, .0), (.64, .06), (.84, .2)):
            d.polygon([(S * (x - .12), S * .6), (S * x, S * h), (S * (x + .12), S * .6)], fill=(250, 120, 20, 255))
            d.polygon([(S * (x - .06), S * .6), (S * x, S * (h + .2)), (S * (x + .06), S * .6)], fill=(255, 230, 90, 255))
    d.rounded_rectangle([S * .04, S * .72, S * .96, S * .88], 10, fill=(30, 30, 35, 255), outline=OUT, width=5)  # sole
    d.ellipse([S * .1, S * .3, S * .66, S * .78], fill=(250, 250, 250, 255), outline=(150, 150, 160, 255), width=5)  # the sock
    d.rectangle([S * .2, S * .1, S * .54, S * .44], fill=(250, 250, 250, 255), outline=(150, 150, 160, 255), width=5)
    for y in (.16, .24):
        d.line([(S * .22, S * y), (S * .52, S * y)], fill=(220, 40, 40, 255), width=4)                          # sock stripes
    d.chord([S * .42, S * .5, S * .94, S * .9], 180, 360, fill=(30, 30, 35, 255), outline=OUT, width=5)         # strap
    d.line([(S * .5, S * .64), (S * .86, S * .64)], fill=(250, 250, 250, 255), width=5)
    return _shrink(im, size)


def meteor_ball(size=64):
    """A basketball coming in from orbit: the ball bottom-right, a long flaming re-entry tail up-left."""
    im, d, S = _big(size)
    OUT = (40, 15, 0, 255)
    d.polygon([(S * .02, S * .1), (S * .2, S * .02), (S * .74, S * .5), (S * .5, S * .74)], fill=(250, 120, 20, 230))
    d.polygon([(S * .2, S * .24), (S * .3, S * .2), (S * .7, S * .56), (S * .56, S * .68)], fill=(255, 230, 100, 255))
    d.ellipse([S * .5, S * .5, S * .96, S * .96], fill=(235, 120, 30, 255), outline=OUT, width=6)
    d.line([(S * .73, S * .5), (S * .73, S * .96)], fill=OUT, width=4)
    d.line([(S * .5, S * .73), (S * .96, S * .73)], fill=OUT, width=4)
    d.arc([S * .58, S * .5, S * 1.0, S * .96], 120, 240, fill=OUT, width=4)
    d.arc([S * .46, S * .5, S * .88, S * .96], 300, 60, fill=OUT, width=4)
    return _shrink(im, size)


def street_hoop(size=64):
    """A street basketball hoop: white backboard with the red square, orange rim, a chain net."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.rectangle([S * .14, S * .04, S * .86, S * .46], fill=(245, 245, 250, 255), outline=OUT, width=6)
    d.rectangle([S * .38, S * .2, S * .62, S * .4], outline=(220, 30, 30, 255), width=5)
    d.ellipse([S * .28, S * .4, S * .72, S * .54], outline=(250, 110, 20, 255), width=7)
    for k in range(5):                                                           # chain net
        x = .3 + k * .1
        d.line([(S * x, S * .5), (S * (.42 + k * .04), S * .82)], fill=(170, 170, 180, 255), width=3)
    d.line([(S * .36, S * .66), (S * .64, S * .66)], fill=(170, 170, 180, 255), width=3)
    return _shrink(im, size)


def bus_stop(size=64):
    """A bus stop sign on a pole: the blue BUS STOP plate with a bus icon (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (15, 20, 40, 255)
    d.line([(S * .5, S * .4), (S * .5, S * 1.0)], fill=(140, 140, 150, 255), width=int(S * .06))
    d.rounded_rectangle([S * .2, S * .02, S * .8, S * .44], 8, fill=(30, 80, 200, 255), outline=OUT, width=6)
    d.rectangle([S * .36, S * .28, S * .64, S * .38], fill=(255, 255, 255, 255))
    im = _shrink(im, size)
    return _texted(im, [("BUS", (32, 3)), ("STOP", (32, 11))], (255, 255, 255, 255), OUT)


def curb_car(size=64):
    """A boxy old sedan doing 40 down the block: maroon body, chrome bumper, side view facing right."""
    im, d, S = _big(size)
    OUT = (20, 10, 10, 255)
    d.polygon([(S * .02, S * .5), (S * .24, S * .48), (S * .34, S * .3), (S * .7, S * .3), (S * .8, S * .48), (S * .98, S * .52),
               (S * .98, S * .74), (S * .02, S * .74)], fill=(130, 30, 40, 255), outline=OUT)
    d.line([(S * .02, S * .5), (S * .24, S * .48), (S * .34, S * .3), (S * .7, S * .3), (S * .8, S * .48), (S * .98, S * .52),
            (S * .98, S * .74), (S * .02, S * .74), (S * .02, S * .5)], fill=OUT, width=6)
    d.polygon([(S * .38, S * .35), (S * .52, S * .35), (S * .52, S * .48), (S * .3, S * .48)], fill=(160, 210, 240, 255))
    d.polygon([(S * .56, S * .35), (S * .68, S * .35), (S * .76, S * .48), (S * .56, S * .48)], fill=(160, 210, 240, 255))
    d.rectangle([S * .9, S * .6, S * .99, S * .7], fill=(220, 220, 225, 255), outline=OUT, width=3)             # bumper
    for x in (.2, .76):
        d.ellipse([S * (x - .1), S * .64, S * (x + .1), S * .86], fill=(25, 25, 25, 255), outline=OUT, width=4)
        d.ellipse([S * (x - .04), S * .7, S * (x + .04), S * .8], fill=(200, 200, 205, 255))
    return _shrink(im, size)


def city_bus(size=64):
    """A big city bus, side view facing right: white and blue, a row of windows, the route sign lit up."""
    im, d, S = _big(size)
    OUT = (15, 20, 40, 255)
    d.rounded_rectangle([S * .0, S * .16, S * 1.0, S * .82], 10, fill=(240, 240, 245, 255), outline=OUT, width=6)
    d.rectangle([S * .0, S * .6, S * 1.0, S * .7], fill=(30, 90, 210, 255))
    for k in range(5):
        x = .04 + k * .17
        d.rectangle([S * x, S * .26, S * (x + .13), S * .46], fill=(130, 180, 220, 255), outline=OUT, width=3)
    d.rectangle([S * .88, S * .2, S * .99, S * .56], fill=(110, 160, 210, 255), outline=OUT, width=3)          # windshield
    d.rectangle([S * .6, S * .18, S * .86, S * .24], fill=(250, 180, 30, 255))                                  # route sign
    for x in (.18, .8):
        d.ellipse([S * (x - .09), S * .72, S * (x + .09), S * .92], fill=(25, 25, 25, 255), outline=OUT, width=4)
    return _shrink(im, size)


def mud_splash(n=16):
    """A splatter of dirty water (alpha only): a blob with a couple of drops."""
    def f(x, y):
        return 1 if ((x - 7) / 5) ** 2 + ((y - 9) / 4) ** 2 < 1 or (x - 12) ** 2 + (y - 3) ** 2 < 3 or (x - 3) ** 2 + (y - 2) ** 2 < 2 else 0
    return _alpha(n, n, f)


# ---- set 27, batch 3: Cut Off, Time Out, Swap Bags, Yap Session, Moonwalk -----------------------------------------------

def liquor_glass(size=32):
    """A rocks glass of brown liquor with two ice cubes."""
    im, d, S = _big(size)
    OUT = (30, 20, 10, 255)
    d.polygon([(S * .14, S * .2), (S * .86, S * .2), (S * .78, S * .94), (S * .22, S * .94)], fill=(220, 235, 245, 150))
    d.polygon([(S * .18, S * .46), (S * .82, S * .46), (S * .78, S * .9), (S * .22, S * .9)], fill=(190, 110, 30, 255))
    for x, y in ((.3, .4), (.52, .48)):
        d.rectangle([S * x, S * y, S * (x + .18), S * (y + .16)], fill=(235, 245, 255, 255), outline=(150, 180, 200, 255), width=3)
    d.line([(S * .14, S * .2), (S * .86, S * .2), (S * .78, S * .94), (S * .22, S * .94), (S * .14, S * .2)], fill=OUT, width=5)
    d.line([(S * .24, S * .28), (S * .28, S * .84)], fill=(255, 255, 255, 255), width=4)
    return _shrink(im, size)


def bar_top(size=64):
    """A stretch of dark wood bar counter with a brass rail."""
    im, d, S = _big(size)
    OUT = (30, 15, 5, 255)
    d.rectangle([S * .0, S * .5, S * 1.0, S * .66], fill=(110, 60, 30, 255), outline=OUT, width=6)
    d.rectangle([S * .0, S * .66, S * 1.0, S * 1.0], fill=(70, 35, 15, 255), outline=OUT, width=6)
    d.line([(S * .0, S * .55), (S * 1.0, S * .55)], fill=(160, 100, 50, 255), width=4)
    d.line([(S * .0, S * .88), (S * 1.0, S * .88)], fill=(220, 180, 60, 255), width=7)                         # brass rail
    return _shrink(im, size)


def dunce_cap(size=64):
    """A tall white paper dunce cap with a big D on it (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (30, 30, 40, 255)
    d.polygon([(S * .5, S * .02), (S * .82, S * .92), (S * .18, S * .92)], fill=(250, 250, 245, 255), outline=OUT)
    d.line([(S * .5, S * .02), (S * .82, S * .92), (S * .18, S * .92), (S * .5, S * .02)], fill=OUT, width=7)
    d.line([(S * .2, S * .86), (S * .8, S * .86)], fill=(220, 40, 40, 255), width=6)
    im = _shrink(im, size)
    return _texted(im, [("D", (32, 34))], (220, 40, 40, 255), (255, 255, 255, 255), font=GLYPHS)


def egg_timer(size=32, ring=False):
    """A wind-up kitchen egg timer, white with red numbers - shaking when it rings."""
    im, d, S = _big(size)
    OUT = (40, 20, 20, 255)
    d.ellipse([S * .12, S * .2, S * .88, S * .9], fill=(250, 250, 245, 255), outline=OUT, width=6)
    d.rectangle([S * .4, S * .06, S * .6, S * .24], fill=(220, 40, 40, 255), outline=OUT, width=4)
    for k in range(6):
        import math
        a = k * math.tau / 6
        d.line([(S * (.5 + .26 * math.cos(a)), S * (.55 + .26 * math.sin(a))), (S * (.5 + .32 * math.cos(a)), S * (.55 + .32 * math.sin(a)))],
               fill=(220, 40, 40, 255), width=4)
    d.line([(S * .5, S * .55), (S * .62, S * .4)], fill=OUT, width=4)
    if ring:
        for x0 in (.0, .88):
            d.arc([S * (x0 - .1), S * .2, S * (x0 + .22), S * .7], 120 if x0 else 300, 240 if x0 else 60, fill=OUT, width=4)
    return _shrink(im, size)


def gym_duffel(size=64, open_=None):
    """A red gym duffel bag; open_ "cash" = stuffed with money, "laundry" = dirty socks and stink lines."""
    im, d, S = _big(size)
    OUT = (50, 5, 5, 255)
    if open_ == "cash":
        for k in range(5):
            x = .2 + k * .12
            d.rectangle([S * x, S * (.2 + (k % 2) * .06), S * (x + .14), S * .5], fill=(110, 180, 90, 255), outline=(30, 80, 30, 255), width=3)
    elif open_ == "laundry":
        d.ellipse([S * .26, S * .2, S * .48, S * .5], fill=(230, 225, 200, 255), outline=(120, 110, 80, 255), width=3)
        d.ellipse([S * .5, S * .26, S * .74, S * .5], fill=(200, 200, 190, 255), outline=(120, 110, 80, 255), width=3)
        for x in (.32, .5, .68):                                                     # stink lines
            d.arc([S * (x - .05), S * .0, S * (x + .05), S * .2], 90, 270, fill=(140, 180, 60, 255), width=4)
    d.rounded_rectangle([S * .06, S * .4, S * .94, S * .9], 24, fill=(200, 30, 40, 255), outline=OUT, width=7)
    d.arc([S * .3, S * .2, S * .7, S * .6], 180, 360, fill=OUT, width=8)                                          # handles
    d.line([(S * .1, S * .58), (S * .9, S * .58)], fill=(250, 250, 250, 255), width=5)                           # zipper line
    d.ellipse([S * .1, S * .54, S * .16, S * .62], fill=(200, 200, 200, 255))
    return _shrink(im, size)


def lightup_tile(size=32, lit=False):
    """A dance-floor tile: dark when off, lit glowing white-pink when stepped on."""
    im, d, S = _big(size)
    OUT = (20, 20, 30, 255)
    d.polygon([(S * .12, S * .3), (S * .88, S * .3), (S * .98, S * .78), (S * .02, S * .78)],
              fill=(255, 220, 250, 255) if lit else (130, 110, 170, 255), outline=OUT)
    d.line([(S * .12, S * .3), (S * .88, S * .3), (S * .98, S * .78), (S * .02, S * .78), (S * .12, S * .3)], fill=OUT, width=5)
    if lit:
        d.polygon([(S * .3, S * .4), (S * .7, S * .4), (S * .76, S * .66), (S * .24, S * .66)], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def black_fedora(size=32):
    """A black fedora with a white band."""
    im, d, S = _big(size)
    OUT = (5, 5, 10, 255)
    d.ellipse([S * .02, S * .56, S * .98, S * .82], fill=(25, 25, 30, 255), outline=OUT, width=5)
    d.rounded_rectangle([S * .22, S * .2, S * .78, S * .68], 12, fill=(30, 30, 36, 255), outline=OUT, width=5)
    d.rectangle([S * .22, S * .52, S * .78, S * .62], fill=(245, 245, 245, 255))
    d.line([(S * .5, S * .22), (S * .5, S * .34)], fill=OUT, width=5)                                             # the pinch
    return _shrink(im, size)


# ---- set 27, batch 4: Back Rub, Flu Shot, Bad Wind, Tat Gun, Cut Line ---------------------------------------------------

def back_scratcher(size=64):
    """A bamboo back scratcher: a long jointed cane, the curled little rake of a tip at the top right."""
    im, d, S = _big(size)
    OUT = (70, 45, 10, 255)
    d.line([(S * .08, S * .94), (S * .74, S * .26)], fill=OUT, width=int(S * .11))
    d.line([(S * .08, S * .94), (S * .74, S * .26)], fill=(220, 190, 110, 255), width=int(S * .07))
    for t in (.3, .6):                                                                                           # bamboo joints
        x, y = .08 + .66 * t, .94 - .68 * t
        d.line([(S * (x - .05), S * (y - .05)), (S * (x + .05), S * (y + .05))], fill=OUT, width=6)
    d.line([(S * .7, S * .3), (S * .86, S * .14)], fill=OUT, width=int(S * .11))
    d.line([(S * .7, S * .3), (S * .86, S * .14)], fill=(220, 190, 110, 255), width=int(S * .07))
    d.ellipse([S * .72, S * .0, S * .98, S * .26], fill=(220, 190, 110, 255), outline=OUT, width=6)          # the cupped tip
    for k in range(4):                                                                                           # rake fingers
        a, b = (.74 + k * .07, .04 + k * .07), (.78 + k * .07, -.02 + k * .07)
        d.line([(S * a[0], S * a[1]), (S * (a[0] + .1), S * (a[1] - .02))], fill=OUT, width=6)
    return _shrink(im, size)


def stat_slot(size=64, stat="???"):
    """A tiny slot machine window showing one stat (ATK / DEF / SPD / ???) with a lever (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 20, 0, 255)
    d.rounded_rectangle([S * .06, S * .22, S * .8, S * .78], 12, fill=(220, 40, 40, 255), outline=OUT, width=7)
    d.rectangle([S * .16, S * .34, S * .7, S * .66], fill=(255, 250, 235, 255), outline=OUT, width=5)
    d.line([(S * .88, S * .5), (S * .88, S * .18)], fill=(170, 170, 180, 255), width=6)                         # lever
    d.ellipse([S * .82, S * .08, S * .96, S * .22], fill=(250, 210, 40, 255), outline=OUT, width=4)
    im = _shrink(im, size)
    return _texted(im, [(stat, (28, 27))], (200, 20, 20, 255), (255, 250, 235, 255))


def alcohol_swab(size=32):
    """An alcohol prep pad: a small white square in a torn foil packet."""
    im, d, S = _big(size)
    OUT = (90, 90, 110, 255)
    d.polygon([(S * .1, S * .3), (S * .7, S * .2), (S * .9, S * .7), (S * .3, S * .82)], fill=(200, 210, 225, 255), outline=OUT)
    d.polygon([(S * .2, S * .36), (S * .64, S * .3), (S * .78, S * .64), (S * .34, S * .72)], fill=(255, 255, 255, 255))
    d.line([(S * .3, S * .45), (S * .6, S * .4)], fill=(120, 170, 230, 255), width=4)
    return _shrink(im, size)


def flu_syringe(size=64):
    """A big cartoon syringe pointing right: clear barrel with yellow vaccine, plunger, a long shiny needle."""
    im, d, S = _big(size)
    OUT = (30, 40, 60, 255)
    d.rectangle([S * .02, S * .4, S * .1, S * .6], fill=(220, 220, 230, 255), outline=OUT, width=4)             # plunger end
    d.rectangle([S * .1, S * .47, S * .22, S * .53], fill=(220, 220, 230, 255), outline=OUT, width=3)
    d.rectangle([S * .22, S * .36, S * .64, S * .64], fill=(220, 240, 250, 180), outline=OUT, width=5)          # barrel
    d.rectangle([S * .36, S * .4, S * .62, S * .6], fill=(250, 220, 80, 255))
    for x in (.3, .4, .5):
        d.line([(S * x, S * .36), (S * x, S * .44)], fill=OUT, width=3)
    d.polygon([(S * .64, S * .44), (S * .72, S * .46), (S * .72, S * .54), (S * .64, S * .56)], fill=(200, 200, 210, 255), outline=OUT)
    d.line([(S * .72, S * .5), (S * .98, S * .5)], fill=(210, 215, 230, 255), width=4)                          # the needle
    d.line([(S * .74, S * .48), (S * .92, S * .48)], fill=(255, 255, 255, 255), width=2)
    return _shrink(im, size)


def elevator_door(size=64):
    """One brushed-steel elevator door panel (the right edge is the seam), a little floor-number light up top."""
    im, d, S = _big(size)
    OUT = (40, 45, 55, 255)
    d.rectangle([S * .1, S * .02, S * .96, S * .98], fill=(180, 185, 195, 255), outline=OUT, width=7)
    for k in range(6):                                                                                            # brushed lines
        y = .14 + k * .14
        d.line([(S * .18, S * y), (S * .88, S * (y + .02))], fill=(205, 210, 220, 255), width=3)
    d.line([(S * .94, S * .04), (S * .94, S * .96)], fill=(110, 115, 125, 255), width=5)
    return _shrink(im, size)


def tattoo_gun(size=64):
    """A tattoo machine pointing down-right: coils, the frame, a grip, the needle tip, ink drop."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.line([(S * .5, S * .5), (S * .88, S * .9)], fill=OUT, width=int(S * .1))                                  # grip + tube
    d.line([(S * .5, S * .5), (S * .88, S * .9)], fill=(180, 180, 190, 255), width=int(S * .06))
    d.line([(S * .88, S * .9), (S * .96, S * .98)], fill=(60, 60, 66, 255), width=3)                            # needle
    d.ellipse([S * .92, S * .92, S * 1.0, S * 1.0], fill=(30, 30, 40, 255))
    for x, y in ((.14, .2), (.3, .12)):                                                                           # coils
        d.rounded_rectangle([S * x, S * y, S * (x + .14), S * (y + .3)], 6, fill=(200, 120, 40, 255), outline=OUT, width=5)
    d.polygon([(S * .1, S * .5), (S * .54, S * .3), (S * .6, S * .54), (S * .2, S * .62)], fill=(50, 50, 60, 255), outline=OUT)
    d.line([(S * .1, S * .5), (S * .54, S * .3), (S * .6, S * .54), (S * .2, S * .62), (S * .1, S * .5)], fill=OUT, width=5)
    d.line([(S * .1, S * .5), (S * .02, S * .7)], fill=(60, 60, 66, 255), width=5)                              # clip cord
    return _shrink(im, size)


def mom_tattoo(size=64):
    """A classic heart tattoo: red heart, a banner across it reading MOM (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (20, 20, 40, 255)
    d.ellipse([S * .14, S * .16, S * .52, S * .54], fill=(220, 30, 50, 255), outline=OUT, width=6)
    d.ellipse([S * .48, S * .16, S * .86, S * .54], fill=(220, 30, 50, 255), outline=OUT, width=6)
    d.polygon([(S * .16, S * .42), (S * .84, S * .42), (S * .5, S * .88)], fill=(220, 30, 50, 255))
    d.line([(S * .16, S * .44), (S * .5, S * .88), (S * .84, S * .44)], fill=OUT, width=6)
    d.ellipse([S * .24, S * .22, S * .36, S * .32], fill=(255, 150, 160, 255))
    d.polygon([(S * .02, S * .4), (S * .98, S * .4), (S * .92, S * .5), (S * .98, S * .6), (S * .02, S * .6), (S * .08, S * .5)],
              fill=(250, 240, 200, 255), outline=OUT)
    d.line([(S * .02, S * .4), (S * .98, S * .4), (S * .92, S * .5), (S * .98, S * .6), (S * .02, S * .6), (S * .08, S * .5), (S * .02, S * .4)], fill=OUT, width=5)
    im = _shrink(im, size)
    return _texted(im, [("MOM", (32, 28))], (30, 40, 120, 255), (250, 240, 200, 255))


def deli_sign(size=64, n="48"):
    """The deli counter's red NOW SERVING sign with the number in LED digits (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 0, 0, 255)
    d.rounded_rectangle([S * .04, S * .16, S * .96, S * .84], 10, fill=(200, 30, 30, 255), outline=OUT, width=7)
    d.rectangle([S * .26, S * .46, S * .74, S * .76], fill=(20, 10, 10, 255), outline=OUT, width=4)
    im = _shrink(im, size)
    return _texted(im, [("NOW", (32, 12)), ("SERVING", (32, 20)), (n, (32, 31))], (255, 250, 220, 255), (90, 0, 0, 255))


def deli_ticket(size=32):
    """A pulled deli number ticket: a red paper tab, a big 49 (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (90, 10, 10, 255)
    d.rectangle([S * .1, S * .2, S * .9, S * .8], fill=(250, 90, 90, 255), outline=OUT, width=6)
    for x in (.1, .9):
        d.ellipse([S * (x - .06), S * .44, S * (x + .06), S * .56], fill=(0, 0, 0, 0))
    im = _shrink(im, size)
    return _texted(im, [("49", (16, 12))], (255, 255, 255, 255), OUT)


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


# ---- set 28, batch 1: High Beams, Fog Machine, Order Up, Sag Check, Last Wish -------------------------------------------

def headlights(size=64, on=True):
    """A pair of round car headlights in the dark: chrome rings, glass lit blazing white-yellow (dim grey when off)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    for x in (.04, .56):
        if on:
            d.ellipse([S * (x - .04), S * .22, S * (x + .44), S * .78], fill=(255, 250, 200, 120))
        d.ellipse([S * x, S * .28, S * (x + .4), S * .72], fill=(200, 205, 215, 255), outline=OUT, width=6)        # chrome
        d.ellipse([S * (x + .06), S * .34, S * (x + .34), S * .66], fill=(255, 255, 235, 255) if on else (110, 115, 125, 255))
        if on:
            d.ellipse([S * (x + .12), S * .4, S * (x + .24), S * .52], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def brights_cone(n=16):
    """A soft beam of light (alpha only): bright on the left, fading and widening to the right."""
    return _alpha(n, n, lambda x, y: max(0, (1 - x / 16) * (1 - abs(y - 7.5) / (2 + x * .4))))


def club_fogger(size=64):
    """A club fog machine: black box, a chrome nozzle on the front, a red LED and a hose of fog coming off it."""
    im, d, S = _big(size)
    OUT = (10, 10, 15, 255)
    d.rounded_rectangle([S * .06, S * .44, S * .7, S * .86], 8, fill=(40, 40, 46, 255), outline=OUT, width=6)
    d.rectangle([S * .7, S * .56, S * .86, S * .7], fill=(200, 205, 215, 255), outline=OUT, width=5)            # nozzle
    d.ellipse([S * .14, S * .52, S * .22, S * .6], fill=(255, 40, 40, 255))
    d.line([(S * .3, S * .56), (S * .6, S * .56)], fill=(90, 90, 100, 255), width=4)                              # vents
    d.line([(S * .3, S * .64), (S * .6, S * .64)], fill=(90, 90, 100, 255), width=4)
    for x, y, r in ((.88, .5, .06), (.94, .4, .07), (.86, .3, .08)):                                              # fog curling out
        d.ellipse([S * (x - r), S * (y - r), S * (x + r), S * (y + r)], fill=(230, 230, 240, 230))
    return _shrink(im, size)


def laser_line(n=16):
    """A thin straight laser beam (alpha only): a hard bright line across the middle."""
    return _alpha(n, n, lambda x, y: 1 if abs(y - 7.5) < .8 else (.4 if abs(y - 7.5) < 1.6 else 0))


def order_phone(size=64, done=False):
    """A phone showing a delivery app: ORDER PLACED with a scooter icon (done: DELIVERED with a check) (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rounded_rectangle([S * .22, S * .04, S * .78, S * .96], 14, fill=(30, 30, 36, 255), outline=OUT, width=6)
    d.rectangle([S * .27, S * .12, S * .73, S * .86], fill=(250, 80, 60, 255) if not done else (60, 190, 90, 255))
    d.ellipse([S * .38, S * .54, S * .62, S * .78], fill=(255, 255, 255, 255))
    if done:
        d.line([(S * .43, S * .66), (S * .49, S * .72), (S * .58, S * .6)], fill=(60, 190, 90, 255), width=6)
    else:
        d.rectangle([S * .44, S * .6, S * .56, S * .7], fill=(250, 80, 60, 255))
    im = _shrink(im, size)
    words = [("DELIV-", (32, 12)), ("ERED", (32, 21))] if done else [("ORDER", (32, 12)), ("PLACED", (32, 21))]
    return _texted(im, words, (255, 255, 255, 255), (40, 20, 20, 255))


def delivery_rider(size=64, tint=0):
    """A delivery rider on a scooter, side view facing right: helmet, the big square insulated bag on the back."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    bag = [(250, 80, 60, 255), (250, 190, 40, 255), (60, 190, 90, 255)][tint % 3]
    d.rectangle([S * .04, S * .14, S * .36, S * .46], fill=bag, outline=OUT, width=6)                            # the bag
    d.line([(S * .1, S * .3), (S * .3, S * .3)], fill=(255, 255, 255, 255), width=4)
    d.rounded_rectangle([S * .3, S * .3, S * .56, S * .62], 8, fill=(60, 70, 90, 255), outline=OUT, width=5)    # rider body
    d.ellipse([S * .42, S * .08, S * .66, S * .32], fill=bag, outline=OUT, width=5)                             # helmet
    d.rectangle([S * .56, S * .16, S * .66, S * .24], fill=(140, 190, 230, 255))                                 # visor
    d.line([(S * .5, S * .44), (S * .74, S * .5)], fill=OUT, width=6)                                            # arm to bars
    d.polygon([(S * .2, S * .7), (S * .78, S * .66), (S * .86, S * .44), (S * .92, S * .44), (S * .84, S * .76), (S * .2, S * .78)],
              fill=(230, 230, 235, 255), outline=OUT)
    for x in (.24, .8):
        d.ellipse([S * (x - .1), S * .7, S * (x + .1), S * .92], fill=(30, 30, 30, 255), outline=OUT, width=4)
    return _shrink(im, size)


def sag_jeans(size=64, stage=0):
    """Baggy blue jeans: 0 = up at the waist with a belt loop line, 1 = sagging with plaid boxers out, 2 = round the knees."""
    im, d, S = _big(size)
    OUT = (15, 25, 60, 255)
    top = (.06, .3, .56)[stage]
    if stage:
        d.rectangle([S * .14, S * .04, S * .86, S * (top + .04)], fill=(220, 60, 60, 255), outline=(90, 10, 10, 255), width=5)   # boxers
        for k in range(4):
            x = .2 + k * .18
            d.line([(S * x, S * .04), (S * x, S * top)], fill=(250, 220, 220, 255), width=3)
        d.line([(S * .14, S * (top * .5)), (S * .86, S * (top * .5))], fill=(250, 220, 220, 255), width=3)
    d.polygon([(S * .1, S * top), (S * .9, S * top), (S * .96, S * .98), (S * .56, S * .98), (S * .5, S * (top + .3)),
               (S * .44, S * .98), (S * .04, S * .98)], fill=(60, 100, 180, 255), outline=OUT)
    d.line([(S * .1, S * top), (S * .9, S * top), (S * .96, S * .98), (S * .56, S * .98), (S * .5, S * (top + .3)), (S * .44, S * .98),
            (S * .04, S * .98), (S * .1, S * top)], fill=OUT, width=6)
    d.line([(S * .1, S * (top + .06)), (S * .9, S * (top + .06))], fill=(40, 70, 140, 255), width=4)            # waistband
    d.line([(S * .3, S * (top + .14)), (S * .26, S * .9)], fill=(110, 150, 220, 255), width=4)                  # fade
    return _shrink(im, size)


def dandelion(size=64, stage=0):
    """A dandelion clock on its stem: 0 = a full white puff, 1 = half blown, 2 = a bare stem."""
    im, d, S = _big(size)
    import math
    d.line([(S * .5, S * .5), (S * .54, S * .98)], fill=(70, 150, 60, 255), width=int(S * .05))
    d.ellipse([S * .44, S * .44, S * .56, S * .56], fill=(170, 160, 90, 255))
    n = (26, 12, 0)[stage]
    for k in range(n):
        a = k * math.tau / 26 + (.6 if stage else 0)
        x, y = .5 + .34 * math.cos(a), .5 + .34 * math.sin(a)
        d.line([(S * .5, S * .5), (S * x, S * y)], fill=(235, 235, 240, 255), width=3)
        d.ellipse([S * (x - .04), S * (y - .04), S * (x + .04), S * (y + .04)], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def dandelion_seed(n=16):
    """A dandelion seed parachute (alpha only): a fluffy fan on top, a thin stalk below."""
    def f(x, y):
        fan = y < 7 and abs(x - 7.5) < (7 - y) * .9 + 1 and (x + y) % 2 == 0
        stalk = abs(x - 7.5) < .7 and 6 <= y <= 14
        return 1 if fan or stalk else 0
    return _alpha(n, n, f)


# ---- set 28, batch 2: Mirror Tint, Jump Em, Quick Draw, Bad Vibes, Hood Power ---------------------------------------------

def tint_glass(size=64, tinted=False):
    """A car's side window glass in its rubber frame: clear see-through, or mirror-tinted black with a chrome sheen."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    pts = [(S * .06, S * .9), (S * .2, S * .14), (S * .9, S * .14), (S * .96, S * .9)]
    _outline_poly(d, pts, (20, 20, 30, 255) if tinted else (190, 225, 245, 120), OUT, 8)
    if tinted:
        d.polygon([(S * .3, S * .2), (S * .5, S * .2), (S * .26, S * .84), (S * .1, S * .84)], fill=(140, 150, 180, 255))
        d.polygon([(S * .56, S * .2), (S * .62, S * .2), (S * .4, S * .84), (S * .34, S * .84)], fill=(110, 120, 150, 255))
    else:
        d.line([(S * .34, S * .24), (S * .2, S * .7)], fill=(255, 255, 255, 200), width=5)
    return _shrink(im, size)


def tint_squeegee(size=32):
    """A rubber-bladed squeegee: black blade, orange handle."""
    im, d, S = _big(size)
    OUT = (20, 20, 20, 255)
    d.rectangle([S * .06, S * .14, S * .94, S * .3], fill=(30, 30, 30, 255), outline=OUT, width=4)
    d.rectangle([S * .14, S * .3, S * .86, S * .42], fill=(160, 160, 170, 255), outline=OUT, width=4)
    d.line([(S * .5, S * .42), (S * .5, S * .96)], fill=OUT, width=int(S * .16))
    d.line([(S * .5, S * .42), (S * .5, S * .96)], fill=(250, 140, 30, 255), width=int(S * .1))
    return _shrink(im, size)


def crew_member(size=64, tint=0):
    """One of the crew pulling up: a full figure in a hoodie (hood up, face in shadow), jeans, fresh kicks."""
    im, d, S = _big(size)
    OUT = (10, 10, 15, 255)
    col = [(60, 60, 70, 255), (150, 30, 40, 255), (40, 70, 140, 255)][tint % 3]
    d.polygon([(S * .3, S * .3), (S * .7, S * .3), (S * .76, S * .62), (S * .24, S * .62)], fill=col, outline=OUT)
    d.line([(S * .3, S * .3), (S * .7, S * .3), (S * .76, S * .62), (S * .24, S * .62), (S * .3, S * .3)], fill=OUT, width=5)
    d.ellipse([S * .34, S * .04, S * .66, S * .36], fill=col, outline=OUT, width=5)                               # the hood
    d.ellipse([S * .41, S * .12, S * .59, S * .32], fill=(25, 20, 20, 255))                                       # shadowed face
    d.rectangle([S * .38, S * .46, S * .62, S * .56], fill=tuple(max(0, c - 30) for c in col[:3]) + (255,), outline=OUT, width=3)   # pocket
    d.rectangle([S * .3, S * .62, S * .48, S * .9], fill=(50, 80, 140, 255), outline=OUT, width=4)
    d.rectangle([S * .52, S * .62, S * .7, S * .9], fill=(50, 80, 140, 255), outline=OUT, width=4)
    for x in (.26, .5):
        d.rounded_rectangle([S * x, S * .88, S * (x + .24), S * .98], 4, fill=(250, 250, 250, 255), outline=OUT, width=3)
    return _shrink(im, size)


def cowboy_hat(size=32):
    """A tan cowboy hat with a dark band."""
    im, d, S = _big(size)
    OUT = (60, 35, 10, 255)
    d.chord([S * .02, S * .44, S * .98, S * .86], 180, 360, fill=(200, 150, 90, 255), outline=OUT, width=5)
    d.ellipse([S * .02, S * .54, S * .98, S * .8], fill=(200, 150, 90, 255), outline=OUT, width=5)
    d.rounded_rectangle([S * .26, S * .18, S * .74, S * .64], 12, fill=(210, 160, 100, 255), outline=OUT, width=5)
    d.rectangle([S * .26, S * .5, S * .74, S * .6], fill=(70, 40, 20, 255))
    d.line([(S * .5, S * .2), (S * .5, S * .34)], fill=OUT, width=4)
    return _shrink(im, size)


def noon_clock(size=64, noon=False):
    """A big town clock face: hands at 11:59 - or straight up at 12:00 (noon) with the 12 lit red."""
    im, d, S = _big(size)
    OUT = (40, 25, 10, 255)
    import math
    d.ellipse([S * .06, S * .06, S * .94, S * .94], fill=(250, 240, 210, 255), outline=OUT, width=8)
    for k in range(12):
        a = k * math.tau / 12 - math.pi / 2
        d.line([(S * (.5 + .34 * math.cos(a)), S * (.5 + .34 * math.sin(a))), (S * (.5 + .4 * math.cos(a)), S * (.5 + .4 * math.sin(a)))],
               fill=(220, 30, 30, 255) if (k == 0 and noon) else OUT, width=7 if k % 3 == 0 else 4)
    m = -math.pi / 2 - (0 if noon else math.tau / 60)
    h = -math.pi / 2 - (0 if noon else math.tau / 720)
    d.line([(S * .5, S * .5), (S * (.5 + .22 * math.cos(h)), S * (.5 + .22 * math.sin(h)))], fill=OUT, width=9)
    d.line([(S * .5, S * .5), (S * (.5 + .34 * math.cos(m)), S * (.5 + .34 * math.sin(m)))], fill=OUT, width=6)
    d.ellipse([S * .45, S * .45, S * .55, S * .55], fill=(220, 30, 30, 255))
    return _shrink(im, size)


def air_ring(n=16):
    """A shockwave ring of air (alpha only): a thin bright circle."""
    c = (n - 1) / 2
    return _alpha(n, n, lambda x, y: max(0, 1 - abs(((x - c) ** 2 + (y - c) ** 2) ** .5 - 6) / 1.4))


def vibe_meter(size=64, level=0):
    """A VIBE CHECK gauge: green-yellow-red arc, the needle on GOOD (0), OK (1) or BAD (2) (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    import math
    d.rounded_rectangle([S * .04, S * .1, S * .96, S * .9], 10, fill=(40, 40, 50, 255), outline=OUT, width=6)
    for k, col in enumerate(((80, 200, 90, 255), (240, 210, 50, 255), (230, 50, 50, 255))):
        d.arc([S * .16, S * .3, S * .84, S * .98], 180 + k * 60, 240 + k * 60, fill=col, width=12)
    a = math.pi + (level * 60 + 30) * math.pi / 180
    d.line([(S * .5, S * .64), (S * (.5 + .3 * math.cos(a)), S * (.64 + .3 * math.sin(a)))], fill=(255, 255, 255, 255), width=6)
    d.ellipse([S * .45, S * .59, S * .55, S * .69], fill=(255, 255, 255, 255))
    im = _shrink(im, size)
    word = ("GOOD", "OK", "BAD")[level]
    return _texted(im, [("VIBE CHECK", (32, 9)), (word, (32, 45))], (255, 255, 255, 255) if level < 2 else (255, 90, 90, 255), (20, 20, 25, 255))


def bodega_cat(size=64, swat=False):
    """The bodega cat: a fat orange tabby sat on its haunches, unimpressed - or up on its back legs mid-swat."""
    im, d, S = _big(size)
    OUT = (70, 30, 0, 255)
    OR, LT = (240, 150, 50, 255), (255, 210, 150, 255)
    body = [S * .24, S * (.36 if swat else .46), S * .76, S * .96]
    d.ellipse(body, fill=OR, outline=OUT, width=6)
    d.ellipse([S * .34, S * (.56 if swat else .64), S * .66, S * .94], fill=LT)                                    # belly
    hy = .1 if swat else .2
    d.ellipse([S * .28, S * hy, S * .72, S * (hy + .38)], fill=OR, outline=OUT, width=6)                            # head
    for x in (.3, .62):                                                                                             # ears
        d.polygon([(S * x, S * (hy + .1)), (S * (x + .04), S * (hy - .06)), (S * (x + .1), S * (hy + .06))], fill=OR, outline=OUT)
    for x in (.38, .56):                                                                                            # eyes, half-shut
        d.line([(S * x, S * (hy + .18)), (S * (x + .08), S * (hy + .18))], fill=OUT, width=6)
    d.polygon([(S * .47, S * (hy + .25)), (S * .53, S * (hy + .25)), (S * .5, S * (hy + .29))], fill=(240, 120, 140, 255))
    for k in range(3):                                                                                              # stripes
        d.arc([S * .3, S * (hy + .02 + k * .04), S * .7, S * (hy + .2 + k * .04)], 220, 320, fill=(200, 100, 20, 255), width=4)
    if swat:
        d.line([(S * .72, S * .52), (S * .94, S * .3)], fill=OUT, width=int(S * .13))
        d.line([(S * .72, S * .52), (S * .94, S * .3)], fill=OR, width=int(S * .08))
        d.ellipse([S * .86, S * .2, S * 1.0, S * .34], fill=LT, outline=OUT, width=4)
    d.arc([S * .04, S * .5, S * .34, S * .96], 90, 250, fill=OR, width=int(S * .08))                                # tail
    return _shrink(im, size)


# ---- set 28, batch 3: Tag In, Bounce Back, Hold Grudge, Tickle Fight, Galaxy Rag ------------------------------------------

def ring_corner(size=64):
    """A wrestling ring corner: a padded red turnbuckle post with three ropes running off to the right."""
    im, d, S = _big(size)
    OUT = (20, 10, 10, 255)
    d.rectangle([S * .06, S * .06, S * .18, S * .98], fill=(170, 170, 180, 255), outline=OUT, width=5)
    for k, y in enumerate((.18, .4, .62)):
        d.line([(S * .18, S * (y + .04)), (S * 1.0, S * (y + .1))], fill=OUT, width=8)
        d.line([(S * .18, S * (y + .04)), (S * 1.0, S * (y + .1))], fill=(250, 250, 250, 255) if k != 1 else (220, 40, 40, 255), width=5)
        d.rounded_rectangle([S * .02, S * (y - .02), S * .24, S * (y + .1)], 6, fill=(220, 30, 40, 255), outline=OUT, width=4)
    return _shrink(im, size)


def luchador(size=64):
    """A tag-team partner in a luchador mask, mid flying-elbow: arms tucked, knee up, cape-less, all business."""
    im, d, S = _big(size)
    OUT = (10, 10, 15, 255)
    d.ellipse([S * .34, S * .04, S * .66, S * .36], fill=(40, 90, 200, 255), outline=OUT, width=5)            # the mask
    d.polygon([(S * .38, S * .14), (S * .48, S * .18), (S * .4, S * .24)], fill=(255, 255, 255, 255))         # eye holes
    d.polygon([(S * .62, S * .14), (S * .52, S * .18), (S * .6, S * .24)], fill=(255, 255, 255, 255))
    d.line([(S * .5, S * .04), (S * .5, S * .12)], fill=(250, 210, 40, 255), width=6)                          # mask stripe
    d.ellipse([S * .44, S * .27, S * .56, S * .33], fill=(220, 60, 60, 255))                                    # mouth hole
    d.rounded_rectangle([S * .3, S * .34, S * .7, S * .66], 10, fill=(200, 150, 110, 255), outline=OUT, width=5)
    d.rectangle([S * .3, S * .6, S * .7, S * .74], fill=(40, 90, 200, 255), outline=OUT, width=4)             # trunks
    d.line([(S * .38, S * .74), (S * .26, S * .96)], fill=OUT, width=int(S * .1))
    d.line([(S * .38, S * .74), (S * .26, S * .96)], fill=(200, 150, 110, 255), width=int(S * .06))
    d.line([(S * .62, S * .74), (S * .78, S * .62)], fill=OUT, width=int(S * .1))                              # knee up
    d.line([(S * .62, S * .74), (S * .78, S * .62)], fill=(200, 150, 110, 255), width=int(S * .06))
    d.line([(S * .7, S * .4), (S * .9, S * .28)], fill=OUT, width=int(S * .1))                                  # the elbow
    d.line([(S * .7, S * .4), (S * .9, S * .28)], fill=(200, 150, 110, 255), width=int(S * .06))
    return _shrink(im, size)


def bouncy_castle(size=64):
    """A kids' inflatable bouncy castle: red and yellow puffy turrets, a blue mesh doorway."""
    im, d, S = _big(size)
    OUT = (60, 10, 10, 255)
    d.rounded_rectangle([S * .06, S * .36, S * .94, S * .96], 16, fill=(230, 50, 50, 255), outline=OUT, width=6)
    for x in (.04, .74):                                                                                          # turrets
        d.rounded_rectangle([S * x, S * .1, S * (x + .22), S * .5], 12, fill=(250, 210, 40, 255), outline=OUT, width=6)
        d.ellipse([S * (x + .02), S * .02, S * (x + .2), S * .18], fill=(40, 120, 230, 255), outline=OUT, width=5)
    d.rounded_rectangle([S * .32, S * .5, S * .68, S * .9], 20, fill=(80, 150, 240, 255), outline=OUT, width=5)
    for k in range(4):
        x = .38 + k * .08
        d.line([(S * x, S * .52), (S * x, S * .88)], fill=(40, 90, 180, 255), width=3)
    for x in (.18, .82):
        d.line([(S * x, S * .5), (S * x, S * .92)], fill=(200, 30, 30, 255), width=4)                           # puffy seams
    return _shrink(im, size)


def grudge_dartboard(size=64):
    """A pub dartboard with a photo of the foe pinned dead center - a big X already drawn on it."""
    im, d, S = _big(size)
    OUT = (15, 15, 15, 255)
    import math
    d.ellipse([S * .04, S * .04, S * .96, S * .96], fill=(20, 20, 20, 255), outline=OUT, width=6)
    for k in range(20):
        a0, a1 = k * 18 - 9, k * 18 + 9
        d.pieslice([S * .1, S * .1, S * .9, S * .9], a0, a1, fill=(240, 220, 170, 255) if k % 2 else (30, 30, 30, 255))
    d.ellipse([S * .1, S * .1, S * .9, S * .9], outline=(200, 40, 40, 255), width=5)
    d.rectangle([S * .32, S * .3, S * .68, S * .72], fill=(250, 250, 245, 255), outline=OUT, width=4)        # the photo
    d.ellipse([S * .42, S * .36, S * .58, S * .5], fill=(120, 110, 100, 255))
    d.chord([S * .36, S * .48, S * .64, S * .76], 180, 360, fill=(120, 110, 100, 255))
    d.line([(S * .34, S * .32), (S * .66, S * .7)], fill=(220, 20, 20, 255), width=5)
    d.line([(S * .66, S * .32), (S * .34, S * .7)], fill=(220, 20, 20, 255), width=5)
    d.ellipse([S * .47, S * .02, S * .53, S * .08], fill=(170, 170, 180, 255))                                  # the tack
    return _shrink(im, size)


def throw_dart(size=32):
    """A dart pointing right: steel tip, knurled barrel, red flights."""
    im, d, S = _big(size)
    OUT = (20, 20, 20, 255)
    d.polygon([(S * .02, S * .3), (S * .26, S * .44), (S * .26, S * .56), (S * .02, S * .7)], fill=(220, 30, 40, 255), outline=OUT)
    d.rectangle([S * .24, S * .44, S * .66, S * .56], fill=(170, 170, 180, 255), outline=OUT, width=4)
    d.line([(S * .66, S * .5), (S * .98, S * .5)], fill=(210, 210, 220, 255), width=4)
    return _shrink(im, size)


def feather_duster(size=64):
    """A rainbow feather duster: a fat fluffy head of colored plumes on a wood handle."""
    im, d, S = _big(size)
    OUT = (40, 20, 10, 255)
    d.line([(S * .1, S * .92), (S * .5, S * .5)], fill=OUT, width=int(S * .09))
    d.line([(S * .1, S * .92), (S * .5, S * .5)], fill=(180, 120, 60, 255), width=int(S * .05))
    import math
    cols = [(250, 80, 120, 255), (250, 180, 40, 255), (80, 200, 230, 255), (150, 90, 230, 255), (90, 210, 110, 255)]
    for k in range(16):
        a = -math.pi * .9 + k * math.pi * 1.1 / 15
        x, y = .66 + .26 * math.cos(a), .34 + .26 * math.sin(a)
        d.ellipse([S * (x - .1), S * (y - .1), S * (x + .1), S * (y + .1)], fill=cols[k % 5])
    d.ellipse([S * .5, S * .2, S * .8, S * .5], fill=(250, 240, 250, 255))
    return _shrink(im, size)


def galaxy_durag(size=64):
    """A galaxy-print durag: deep purple-blue satin printed with stars and a nebula swirl, long tails flowing."""
    im, d, S = _big(size)
    OUT = (20, 10, 40, 255)
    d.chord([S * .12, S * .1, S * .88, S * .9], 180, 360, fill=(50, 30, 120, 255), outline=OUT, width=6)
    d.rectangle([S * .12, S * .46, S * .88, S * .56], fill=(40, 25, 100, 255), outline=OUT, width=5)
    for pts in (((.8, .5), (.98, .66), (.9, .96)), ((.76, .54), (.88, .8), (.74, .98))):                        # tails
        d.line([(S * x, S * y) for x, y in pts], fill=OUT, width=int(S * .1), joint="curve")
        d.line([(S * x, S * y) for x, y in pts], fill=(70, 40, 150, 255), width=int(S * .06), joint="curve")
    d.ellipse([S * .3, S * .18, S * .62, S * .4], fill=(200, 80, 200, 140))                                     # nebula
    for x, y in ((.24, .3), (.4, .16), (.56, .36), (.7, .24), (.46, .42), (.34, .4)):
        d.ellipse([S * (x - .02), S * (y - .02), S * (x + .02), S * (y + .02)], fill=(255, 255, 255, 255))
    d.line([(S * .66, S * .28), (S * .74, S * .28)], fill=(255, 255, 220, 255), width=3)
    d.line([(S * .7, S * .24), (S * .7, S * .32)], fill=(255, 255, 220, 255), width=3)
    return _shrink(im, size)


# ---- set 28, batch 4: Ice Pick, Blocked, Rat Tail, Kickback, Pass It On -----------------------------------------------------

def bar_ice_pick(size=64):
    """A bartender's ice pick pointing down-right: a long steel spike out of a red wood handle."""
    im, d, S = _big(size)
    OUT = (30, 10, 10, 255)
    d.line([(S * .12, S * .12), (S * .4, S * .4)], fill=OUT, width=int(S * .16))
    d.line([(S * .12, S * .12), (S * .4, S * .4)], fill=(200, 40, 40, 255), width=int(S * .1))
    d.rectangle([S * .38, S * .36, S * .46, S * .46], fill=(170, 170, 180, 255), outline=OUT, width=3)        # ferrule
    d.line([(S * .44, S * .44), (S * .94, S * .94)], fill=(210, 215, 225, 255), width=5)
    d.line([(S * .46, S * .44), (S * .9, S * .88)], fill=(255, 255, 255, 255), width=2)
    return _shrink(im, size)


def ice_shard(n=16):
    """A chipped-off ice shard (alpha only): a jagged triangle."""
    return _alpha(n, n, lambda x, y: 1 if y > 3 and abs(x - 7.5 - (y - 9) * .3) < (14 - y) * .55 else 0)


def dm_phone(size=64, stage=0):
    """A phone in a DM: 0 = the foe texts "hey", 1 = "hey??" "hello??", 2 = a red BLOCKED banner (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.rounded_rectangle([S * .22, S * .04, S * .78, S * .96], 14, fill=(30, 30, 36, 255), outline=OUT, width=6)
    d.rectangle([S * .27, S * .12, S * .73, S * .86], fill=(245, 245, 250, 255))
    for k in range(min(stage + 1, 2)):
        y = .2 + k * .2
        d.rounded_rectangle([S * .3, S * y, S * .62, S * (y + .14)], 8, fill=(220, 225, 235, 255))
    if stage == 2:
        d.rectangle([S * .22, S * .58, S * .78, S * .76], fill=(220, 30, 30, 255), outline=OUT, width=4)
    im = _shrink(im, size)
    words = [("hey", (29, 14))] + ([("hey??", (29, 27))] if stage >= 1 else [])
    im = _texted(im, words, (20, 20, 25, 255), (245, 245, 250, 255))
    if stage == 2:
        im = _texted(im, [("BLOCKED", (32, 40))], (255, 255, 255, 255), (120, 0, 0, 255))
    return im


def subway_rat(size=64, whip=False):
    """A fat grey subway rat scurrying right: pink ears and nose, beady eye, long pink tail (whipped up overhead when
    whip)."""
    im, d, S = _big(size)
    OUT = (30, 25, 25, 255)
    if whip:
        d.line([(S * .2, S * .62), (S * .1, S * .3), (S * .3, S * .06), (S * .6, S * .1)], fill=(230, 140, 150, 255), width=6, joint="curve")
    else:
        d.line([(S * .2, S * .66), (S * .06, S * .74), (S * .02, S * .6)], fill=(230, 140, 150, 255), width=6, joint="curve")
    d.ellipse([S * .16, S * .46, S * .72, S * .86], fill=(130, 125, 125, 255), outline=OUT, width=6)
    d.polygon([(S * .6, S * .5), (S * .96, S * .7), (S * .62, S * .82)], fill=(140, 135, 135, 255), outline=OUT)
    d.line([(S * .6, S * .5), (S * .96, S * .7), (S * .62, S * .82)], fill=OUT, width=5)
    d.ellipse([S * .56, S * .38, S * .7, S * .54], fill=(240, 160, 170, 255), outline=OUT, width=4)            # ear
    d.ellipse([S * .74, S * .56, S * .8, S * .62], fill=OUT)                                                      # eye
    d.ellipse([S * .92, S * .66, S * 1.0, S * .74], fill=(240, 120, 140, 255))                                    # nose
    for x in (.3, .56):
        d.line([(S * x, S * .84), (S * (x - .04), S * .94)], fill=(230, 140, 150, 255), width=4)                # feet
    return _shrink(im, size)


def interest_envelope(size=64):
    """A fat bank envelope stuffed with cash, bills poking out, WITH INTEREST scrawled on it (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (60, 50, 30, 255)
    for k in range(4):
        x = .2 + k * .14
        d.rectangle([S * x, S * .12, S * (x + .2), S * .4], fill=(120, 190, 100, 255), outline=(30, 80, 30, 255), width=3)
    d.rectangle([S * .06, S * .3, S * .94, S * .84], fill=(240, 225, 190, 255), outline=OUT, width=6)
    d.polygon([(S * .06, S * .3), (S * .5, S * .56), (S * .94, S * .3)], fill=(225, 205, 160, 255), outline=OUT)
    im = _shrink(im, size)
    return _texted(im, [("WITH", (32, 37)), ("INTEREST", (32, 45))], (200, 20, 20, 255), (255, 245, 220, 255))


def hot_potato(size=32):
    """A baked potato so hot it's glowing red at the edges, steam squiggles coming off it."""
    im, d, S = _big(size)
    OUT = (70, 30, 10, 255)
    d.ellipse([S * .08, S * .36, S * .92, S * .9], fill=(200, 120, 60, 255), outline=(230, 40, 20, 255), width=8)
    for x, y in ((.3, .54), (.6, .62), (.46, .72)):
        d.ellipse([S * x, S * y, S * (x + .06), S * (y + .05)], fill=OUT)
    for x in (.3, .5, .7):
        d.arc([S * (x - .08), S * .0, S * (x + .08), S * .34], 90, 270, fill=(255, 255, 255, 230), width=4)
    return _shrink(im, size)


# ---- set 28, batch 5: Flip Script, Cosplay, Guard Swarm, Honey Heal, Edge Up ---------------------------------------------

def script_page(size=64, flipped=False):
    """A movie script page: SCRIPT at the top, ATK over DEF in big type - swapped (DEF over ATK) when flipped
    (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (40, 40, 50, 255)
    d.rectangle([S * .14, S * .04, S * .86, S * .96], fill=(250, 250, 240, 255), outline=OUT, width=6)
    for y in (.62, .7, .78, .86):
        d.line([(S * .24, S * y), (S * .76, S * y)], fill=(180, 180, 190, 255), width=3)
    for y in (.1, .2):
        d.ellipse([S * .18, S * y, S * .24, S * (y + .06)], fill=(120, 120, 130, 255))                           # binder holes
    im = _shrink(im, size)
    a, b = ("DEF", "ATK") if flipped else ("ATK", "DEF")
    return _texted(im, [("SCRIPT", (34, 6)), (a, (34, 17)), (b, (34, 27))], (200, 30, 30, 255) if flipped else (30, 30, 40, 255), (250, 250, 240, 255))


def costume_bag(size=64):
    """A cheap Halloween costume in its plastic bag: a hanger hook up top, COSTUME across, a goofy mask pictured
    (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (30, 30, 40, 255)
    d.arc([S * .4, S * .0, S * .6, S * .16], 180, 360, fill=(160, 160, 170, 255), width=5)
    d.rectangle([S * .12, S * .1, S * .88, S * .96], fill=(240, 120, 30, 230), outline=OUT, width=6)
    d.ellipse([S * .3, S * .4, S * .7, S * .86], fill=(120, 200, 90, 255), outline=OUT, width=5)                  # the mask pic
    for x in (.38, .54):
        d.ellipse([S * x, S * .54, S * (x + .08), S * .62], fill=OUT)
    d.arc([S * .4, S * .62, S * .6, S * .76], 20, 160, fill=OUT, width=4)
    im = _shrink(im, size)
    return _texted(im, [("COSTUME", (32, 12))], (255, 255, 255, 255), (60, 20, 0, 255))


def cheap_mask(size=64):
    """A cheap rubber monster mask: lime green, googly eyes, a lopsided grin, the elastic string."""
    im, d, S = _big(size)
    OUT = (20, 40, 10, 255)
    d.line([(S * .06, S * .44), (S * .94, S * .44)], fill=(240, 240, 240, 255), width=3)
    d.ellipse([S * .16, S * .1, S * .84, S * .92], fill=(130, 210, 80, 255), outline=OUT, width=6)
    for x, r in ((.28, .12), (.56, .1)):
        d.ellipse([S * x, S * .28, S * (x + 2 * r), S * (.28 + 2 * r)], fill=(255, 255, 255, 255), outline=OUT, width=4)
        d.ellipse([S * (x + r * .7), S * (.28 + r * .9), S * (x + r * 1.3), S * (.28 + r * 1.5)], fill=OUT)
    d.chord([S * .3, S * .52, S * .74, S * .8], 0, 180, fill=(60, 20, 20, 255), outline=OUT, width=4)
    d.rectangle([S * .4, S * .66, S * .48, S * .72], fill=(255, 255, 255, 255))
    return _shrink(im, size)


def mall_cop(size=64):
    """A mall cop on a segway, side view facing right: white shirt, cap and badge, the two-wheeled stand-up scooter."""
    im, d, S = _big(size)
    OUT = (15, 15, 20, 255)
    d.line([(S * .56, S * .3), (S * .66, S * .84)], fill=(60, 60, 66, 255), width=6)                             # handle bar post
    d.line([(S * .5, S * .3), (S * .64, S * .28)], fill=(60, 60, 66, 255), width=6)
    d.rounded_rectangle([S * .3, S * .24, S * .54, S * .58], 8, fill=(240, 240, 245, 255), outline=OUT, width=5)  # shirt
    d.ellipse([S * .44, S * .32, S * .5, S * .38], fill=(250, 200, 50, 255))                                     # badge
    d.rectangle([S * .3, S * .58, S * .54, S * .84], fill=(40, 50, 80, 255), outline=OUT, width=4)               # pants
    d.ellipse([S * .32, S * .04, S * .52, S * .24], fill=(220, 170, 130, 255), outline=OUT, width=4)              # head
    d.rectangle([S * .3, S * .02, S * .54, S * .1], fill=(40, 50, 80, 255), outline=OUT, width=3)                # cap
    d.line([(S * .5, S * .08), (S * .6, S * .1)], fill=(40, 50, 80, 255), width=4)                                # brim
    d.rectangle([S * .24, S * .84, S * .76, S * .9], fill=(60, 60, 66, 255), outline=OUT, width=3)               # deck
    for x in (.28, .72):
        d.ellipse([S * (x - .08), S * .82, S * (x + .08), S * .98], fill=(30, 30, 30, 255), outline=OUT, width=3)
    return _shrink(im, size)


def honey_bear(size=32):
    """A plastic honey bear squeeze bottle: amber honey, a yellow cap on its head."""
    im, d, S = _big(size)
    OUT = (110, 60, 0, 255)
    d.ellipse([S * .2, S * .44, S * .8, S * .98], fill=(240, 160, 30, 230), outline=OUT, width=5)
    d.ellipse([S * .28, S * .2, S * .72, S * .56], fill=(240, 160, 30, 230), outline=OUT, width=5)
    for x in (.26, .6):
        d.ellipse([S * x, S * .16, S * (x + .14), S * .3], fill=(240, 160, 30, 230), outline=OUT, width=4)
    d.rectangle([S * .42, S * .02, S * .58, S * .2], fill=(250, 220, 50, 255), outline=OUT, width=4)
    d.ellipse([S * .38, S * .32, S * .44, S * .38], fill=OUT)
    d.ellipse([S * .56, S * .32, S * .62, S * .38], fill=OUT)
    return _shrink(im, size)


def tea_mug(size=32):
    """A big white mug of steaming tea with a tea bag tag hanging off it."""
    im, d, S = _big(size)
    OUT = (40, 30, 20, 255)
    d.rounded_rectangle([S * .14, S * .34, S * .74, S * .94], 8, fill=(250, 250, 250, 255), outline=OUT, width=5)
    d.ellipse([S * .14, S * .3, S * .74, S * .42], fill=(170, 100, 40, 255), outline=OUT, width=4)
    d.arc([S * .62, S * .46, S * .92, S * .8], 270, 90, fill=OUT, width=6)
    d.line([(S * .3, S * .36), (S * .26, S * .62)], fill=(200, 200, 200, 255), width=2)
    d.rectangle([S * .2, S * .6, S * .32, S * .72], fill=(250, 210, 60, 255), outline=OUT, width=2)
    for x in (.34, .5):
        d.arc([S * (x - .06), S * .0, S * (x + .06), S * .28], 90, 270, fill=(255, 255, 255, 220), width=4)
    return _shrink(im, size)


def chef_knife(size=64):
    """A big chef's knife pointing up-right: wide steel blade with a shine line, black riveted handle."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.polygon([(S * .38, S * .62), (S * .92, S * .08), (S * .96, S * .16), (S * .5, S * .72)], fill=(215, 220, 230, 255), outline=OUT)
    d.line([(S * .38, S * .62), (S * .92, S * .08), (S * .96, S * .16), (S * .5, S * .72), (S * .38, S * .62)], fill=OUT, width=5)
    d.line([(S * .46, S * .62), (S * .9, S * .18)], fill=(255, 255, 255, 255), width=3)
    d.line([(S * .1, S * .92), (S * .42, S * .66)], fill=OUT, width=int(S * .12))
    d.line([(S * .1, S * .92), (S * .42, S * .66)], fill=(40, 40, 46, 255), width=int(S * .08))
    for t in (.3, .6):
        x, y = .1 + .32 * t, .92 - .26 * t
        d.ellipse([S * (x - .02), S * (y - .02), S * (x + .02), S * (y + .02)], fill=(200, 200, 210, 255))
    return _shrink(im, size)


def honing_steel(size=64):
    """A honing steel: a long ridged steel rod, a guard and a wood handle, pointing up-left."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.line([(S * .1, S * .1), (S * .62, S * .62)], fill=(150, 155, 165, 255), width=int(S * .06))
    for k in range(6):
        t = .1 + k * .14
        x, y = .1 + .52 * t, .1 + .52 * t
        d.line([(S * (x - .02), S * (y + .02)), (S * (x + .02), S * (y - .02))], fill=(100, 105, 115, 255), width=2)
    d.line([(S * .56, S * .68), (S * .68, S * .56)], fill=OUT, width=8)                                          # guard
    d.line([(S * .64, S * .64), (S * .92, S * .92)], fill=OUT, width=int(S * .11))
    d.line([(S * .64, S * .64), (S * .92, S * .92)], fill=(150, 100, 50, 255), width=int(S * .07))
    return _shrink(im, size)


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


# ---- set 29, batch 1: Blow Dryer, Snow Globe, Spinners, Throw Shade, Burned CD --------------------------------------------

def blow_dryer(size=64):
    """A hot pink salon blow dryer pointing right: round motor body, the nozzle, a handle down, the cord."""
    im, d, S = _big(size)
    OUT = (60, 10, 40, 255)
    d.rectangle([S * .44, S * .3, S * .9, S * .5], fill=(240, 90, 170, 255), outline=OUT, width=6)              # nozzle
    d.rectangle([S * .86, S * .26, S * .96, S * .54], fill=(60, 60, 66, 255), outline=OUT, width=4)
    d.ellipse([S * .1, S * .16, S * .52, S * .62], fill=(240, 90, 170, 255), outline=OUT, width=6)              # motor
    d.ellipse([S * .2, S * .26, S * .42, S * .52], fill=(60, 60, 66, 255))
    for k in range(4):
        d.line([(S * .23, S * (.3 + k * .06)), (S * .39, S * (.3 + k * .06))], fill=(120, 120, 130, 255), width=3)  # vent grille
    d.line([(S * .32, S * .58), (S * .4, S * .92)], fill=OUT, width=int(S * .13))                               # handle
    d.line([(S * .32, S * .58), (S * .4, S * .92)], fill=(240, 90, 170, 255), width=int(S * .09))
    d.rectangle([S * .34, S * .66, S * .4, S * .72], fill=(255, 255, 255, 255))                                  # switch
    d.line([(S * .4, S * .92), (S * .2, S * .98), (S * .04, S * .9)], fill=(60, 60, 66, 255), width=4)          # cord
    return _shrink(im, size)


def gust_slash(n=16):
    """A razor gust (alpha only): a thin curved crescent."""
    def f(x, y):
        r1 = ((x - 4) ** 2 + (y - 8) ** 2) ** .5
        return 1 if 8.5 < r1 < 10.5 and x > 6 else 0
    return _alpha(n, n, f)


def hood_snow_globe(size=64, storm=False):
    """A snow globe of the block on a black base: a little row of buildings and a streetlight inside; storm = snow,
    lightning and a little tornado swirling inside the glass."""
    im, d, S = _big(size)
    OUT = (20, 20, 30, 255)
    d.ellipse([S * .1, S * .04, S * .9, S * .84], fill=(200, 230, 255, 140) if not storm else (110, 120, 160, 200), outline=OUT, width=6)
    for x, h in ((.26, .3), (.4, .22), (.54, .32), (.66, .26)):                                                   # the block
        d.rectangle([S * x, S * (.66 - h), S * (x + .12), S * .66], fill=(150, 80, 60, 255), outline=OUT, width=3)
        d.rectangle([S * (x + .03), S * (.66 - h + .05), S * (x + .06), S * (.66 - h + .09)], fill=(250, 220, 90, 255))
    d.line([(S * .22, S * .66), (S * .22, S * .4)], fill=OUT, width=4)
    d.ellipse([S * .19, S * .36, S * .27, S * .42], fill=(255, 240, 150, 255))
    d.rectangle([S * .14, S * .64, S * .86, S * .72], fill=(240, 245, 250, 255))                                  # snow on the ground
    d.polygon([(S * .14, S * .76), (S * .86, S * .76), (S * .94, S * .98), (S * .06, S * .98)], fill=(30, 30, 36, 255), outline=OUT)
    import random
    r = random.Random(7)
    for _ in range(26 if storm else 10):
        x, y = r.uniform(.2, .8), r.uniform(.12, .62)
        d.ellipse([S * x, S * y, S * (x + .03), S * (y + .03)], fill=(255, 255, 255, 255))
    if storm:
        d.line([(S * .6, S * .14), (S * .54, S * .3), (S * .62, S * .3), (S * .56, S * .46)], fill=(255, 240, 80, 255), width=5)
        for k in range(3):
            d.arc([S * (.3 + k * .03), S * (.16 + k * .08), S * (.48 - k * .02), S * (.24 + k * .08)], 0, 300, fill=(230, 230, 240, 255), width=3)
    d.arc([S * .2, S * .1, S * .5, S * .4], 200, 270, fill=(255, 255, 255, 255), width=5)
    return _shrink(im, size)


def spinner_rim(size=64, angle=0):
    """A chrome spinner rim on a tire: the outer spinner blades rotated by `angle` degrees, sun-glint on the chrome."""
    im, d, S = _big(size)
    import math
    OUT = (20, 20, 25, 255)
    d.ellipse([S * .02, S * .02, S * .98, S * .98], fill=(30, 30, 34, 255), outline=OUT, width=6)               # tire
    d.ellipse([S * .14, S * .14, S * .86, S * .86], fill=(200, 205, 215, 255), outline=OUT, width=5)
    for k in range(5):                                                                                           # spinner blades
        a = math.radians(angle + k * 72)
        b = a + .5
        d.polygon([(S * .5, S * .5), (S * (.5 + .34 * math.cos(a)), S * (.5 + .34 * math.sin(a))), (S * (.5 + .34 * math.cos(b)), S * (.5 + .34 * math.sin(b)))],
                  fill=(235, 240, 250, 255), outline=(120, 125, 140, 255))
    d.ellipse([S * .42, S * .42, S * .58, S * .58], fill=(250, 210, 50, 255), outline=OUT, width=4)
    d.polygon([(S * .3, S * .22), (S * .36, S * .3), (S * .3, S * .38), (S * .24, S * .3)], fill=(255, 255, 255, 255))   # glint
    return _shrink(im, size)


def lampshade(size=64):
    """A fringed living-room lampshade: cream drum shade with a gold trim and little tassels hanging off the rim."""
    im, d, S = _big(size)
    OUT = (90, 60, 20, 255)
    d.polygon([(S * .28, S * .16), (S * .72, S * .16), (S * .9, S * .7), (S * .1, S * .7)], fill=(245, 230, 190, 255), outline=OUT)
    d.line([(S * .28, S * .16), (S * .72, S * .16), (S * .9, S * .7), (S * .1, S * .7), (S * .28, S * .16)], fill=OUT, width=6)
    d.line([(S * .12, S * .64), (S * .88, S * .64)], fill=(220, 170, 50, 255), width=6)
    d.line([(S * .24, S * .24), (S * .76, S * .24)], fill=(220, 170, 50, 255), width=5)
    for k in range(8):                                                                                           # tassels
        x = .14 + k * .103
        d.line([(S * x, S * .7), (S * x, S * .84)], fill=(220, 170, 50, 255), width=3)
        d.ellipse([S * (x - .025), S * .82, S * (x + .025), S * .88], fill=(200, 140, 40, 255))
    d.line([(S * .36, S * .2), (S * .26, S * .6)], fill=(255, 250, 230, 255), width=4)
    return _shrink(im, size)


def burned_cd(size=64):
    """A burned CD-R: rainbow-sheen silver disc with the hole, MIX hand-written on it in sharpie (shown at 1:1)."""
    im, d, S = _big(size)
    OUT = (60, 60, 70, 255)
    d.ellipse([S * .04, S * .04, S * .96, S * .96], fill=(215, 220, 230, 255), outline=OUT, width=5)
    for a0, col in ((200, (180, 230, 255, 255)), (250, (255, 200, 240, 255)), (300, (220, 255, 200, 255))):
        d.arc([S * .12, S * .12, S * .88, S * .88], a0, a0 + 40, fill=col, width=10)
    d.ellipse([S * .36, S * .36, S * .64, S * .64], fill=(240, 240, 245, 255), outline=OUT, width=3)
    d.ellipse([S * .44, S * .44, S * .56, S * .56], fill=(0, 0, 0, 0), outline=OUT, width=3)
    im = _shrink(im, size)
    return _texted(im, [("MIX", (32, 10)), ("COPY", (32, 46))], (20, 20, 25, 255), (215, 220, 230, 255))


def cd_boombox(size=64):
    """A silver CD boombox: two big speakers, the CD lid on top popped open, a little LCD."""
    im, d, S = _big(size)
    OUT = (20, 20, 25, 255)
    d.line([(S * .2, S * .2), (S * .3, S * .06), (S * .7, S * .06), (S * .8, S * .2)], fill=(80, 80, 90, 255), width=6)   # handle
    d.rounded_rectangle([S * .04, S * .2, S * .96, S * .86], 10, fill=(190, 195, 205, 255), outline=OUT, width=6)
    for x in (.08, .64):
        d.ellipse([S * x, S * .4, S * (x + .28), S * .8], fill=(40, 40, 46, 255), outline=OUT, width=4)
        d.ellipse([S * (x + .09), S * .53, S * (x + .19), S * .67], fill=(90, 90, 100, 255))
    d.ellipse([S * .38, S * .26, S * .62, S * .5], fill=(220, 225, 235, 255), outline=OUT, width=4)             # CD lid
    d.rectangle([S * .4, S * .58, S * .6, S * .7], fill=(120, 200, 140, 255), outline=OUT, width=3)             # LCD
    return _shrink(im, size)


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


# ---- set 29, batch 3: Power Trade, Guard Trade, Shove Off, Dirty Cross, Open Window ----------------------------------------

def preworkout_tub(size=32):
    """A tub of pre-workout: black with a red lightning bolt and a scoop lid."""
    im, d, S = _big(size)
    OUT = (10, 10, 10, 255)
    d.rounded_rectangle([S * .16, S * .3, S * .84, S * .96], 8, fill=(30, 30, 34, 255), outline=OUT, width=5)
    d.rectangle([S * .12, S * .16, S * .88, S * .32], fill=(230, 40, 40, 255), outline=OUT, width=4)
    d.polygon([(S * .56, S * .38), (S * .36, S * .66), (S * .5, S * .66), (S * .42, S * .9), (S * .66, S * .58), (S * .52, S * .58)], fill=(250, 220, 40, 255))
    return _shrink(im, size)


def chamomile_box(size=32):
    """A soft yellow box of chamomile tea with a little daisy on it."""
    im, d, S = _big(size)
    OUT = (110, 90, 30, 255)
    d.rectangle([S * .12, S * .2, S * .88, S * .9], fill=(250, 235, 160, 255), outline=OUT, width=5)
    for k in range(6):
        import math
        a = k * math.tau / 6
        x, y = .5 + .14 * math.cos(a), .52 + .14 * math.sin(a)
        d.ellipse([S * (x - .08), S * (y - .08), S * (x + .08), S * (y + .08)], fill=(255, 255, 255, 255))
    d.ellipse([S * .43, S * .45, S * .57, S * .59], fill=(250, 190, 40, 255))
    d.line([(S * .5, S * .66), (S * .5, S * .84)], fill=(90, 160, 70, 255), width=4)
    return _shrink(im, size)


def big_umbrella(size=64, busted=False):
    """A big black golf umbrella, open - or a busted bodega umbrella: spokes snapped, canopy flipped inside out."""
    im, d, S = _big(size)
    OUT = (10, 10, 15, 255)
    if busted:
        d.polygon([(S * .5, S * .5), (S * .08, S * .1), (S * .3, S * .3), (S * .48, S * .04), (S * .62, S * .3), (S * .9, S * .14)],
                  fill=(60, 60, 70, 255), outline=OUT)
        for x, y in ((.08, .1), (.48, .04), (.9, .14), (.2, .4)):
            d.line([(S * .5, S * .5), (S * x, S * y)], fill=(160, 160, 170, 255), width=3)
    else:
        d.chord([S * .02, S * .1, S * .98, S * .8], 180, 360, fill=(30, 30, 40, 255), outline=OUT, width=6)
        for x in (.26, .5, .74):
            d.line([(S * .5, S * .14), (S * x, S * .45)], fill=(90, 90, 110, 255), width=3)
        d.arc([S * .1, S * .16, S * .5, S * .6], 200, 260, fill=(120, 120, 140, 255), width=5)
    d.line([(S * .5, S * .44), (S * .5, S * .9)], fill=(170, 170, 180, 255), width=5)
    d.arc([S * .5, S * .82, S * .66, S * .98], 0, 180, fill=(120, 70, 30, 255), width=7)                        # the hook handle
    return _shrink(im, size)


def push_broom(size=64):
    """A wide push broom pointing right: long wood handle, a fat black bristle head."""
    im, d, S = _big(size)
    OUT = (20, 15, 10, 255)
    d.line([(S * .02, S * .2), (S * .66, S * .5)], fill=OUT, width=int(S * .08))
    d.line([(S * .02, S * .2), (S * .66, S * .5)], fill=(200, 150, 90, 255), width=int(S * .05))
    d.rectangle([S * .62, S * .16, S * .78, S * .84], fill=(150, 100, 50, 255), outline=OUT, width=5)          # block
    for k in range(10):                                                                                           # bristles
        y = .2 + k * .065
        d.line([(S * .78, S * y), (S * .96, S * y)], fill=(30, 30, 30, 255), width=4)
    return _shrink(im, size)


def spray_can(size=64):
    """A spray paint can: toxic green, white cap and nozzle, a drip down the side."""
    im, d, S = _big(size)
    OUT = (10, 30, 10, 255)
    d.rounded_rectangle([S * .3, S * .3, S * .7, S * .96], 10, fill=(90, 210, 60, 255), outline=OUT, width=6)
    d.rectangle([S * .3, S * .52, S * .7, S * .68], fill=(30, 30, 30, 255))
    d.chord([S * .3, S * .14, S * .7, S * .46], 180, 360, fill=(240, 240, 240, 255), outline=OUT, width=5)
    d.rectangle([S * .44, S * .06, S * .56, S * .18], fill=(240, 240, 240, 255), outline=OUT, width=4)
    d.line([(S * .38, S * .3), (S * .38, S * .42)], fill=(90, 210, 60, 255), width=5)
    d.line([(S * .36, S * .36), (S * .36, S * .5)], fill=(160, 255, 120, 255), width=3)
    return _shrink(im, size)


def paint_x(size=64):
    """A dripping spray-painted X tag in toxic green."""
    im, d, S = _big(size)
    G, OUT = (110, 230, 60, 255), (30, 70, 10, 255)
    for a, b in (((.12, .12), (.88, .82)), ((.86, .1), (.14, .84))):
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=OUT, width=int(S * .18))
        d.line([(S * a[0], S * a[1]), (S * b[0], S * b[1])], fill=G, width=int(S * .12))
    for x, y in ((.2, .84), (.84, .86), (.5, .54)):                                                              # drips
        d.line([(S * x, S * y), (S * x, S * (y + .12))], fill=G, width=5)
        d.ellipse([S * (x - .03), S * (y + .1), S * (x + .03), S * (y + .16)], fill=G)
    return _shrink(im, size)


def sash_window(size=64, opened=False):
    """An apartment sash window in a brick wall: closed, or the bottom pane pushed up with the night air coming in."""
    im, d, S = _big(size)
    OUT = (30, 20, 15, 255)
    d.rectangle([S * .0, S * .0, S * 1.0, S * 1.0], fill=(160, 70, 50, 255))
    for r in range(8):
        y = r * .125
        d.line([(0, S * y), (S, S * y)], fill=(120, 50, 35, 255), width=3)
    d.rectangle([S * .14, S * .08, S * .86, S * .92], fill=(240, 240, 235, 255), outline=OUT, width=6)
    top = (.14, .08, .86, .5)
    d.rectangle([S * .2, S * .14, S * .8, S * .46], fill=(150, 190, 220, 255), outline=OUT, width=4)
    if opened:
        d.rectangle([S * .2, S * .52, S * .8, S * .86], fill=(20, 20, 40, 255))                                  # open air
        d.rectangle([S * .18, S * .4, S * .82, S * .5], fill=(240, 240, 235, 255), outline=OUT, width=4)        # the pane pushed up
    else:
        d.rectangle([S * .2, S * .54, S * .8, S * .86], fill=(150, 190, 220, 255), outline=OUT, width=4)
        d.line([(S * .14, S * .5), (S * .86, S * .5)], fill=OUT, width=6)
    return _shrink(im, size)


def pizza_box_fan(size=64):
    """A greasy flat pizza box being waved like a fan, a grease spot on the lid."""
    im, d, S = _big(size)
    OUT = (90, 60, 20, 255)
    d.polygon([(S * .06, S * .3), (S * .9, S * .14), (S * .96, S * .64), (S * .12, S * .82)], fill=(225, 195, 140, 255), outline=OUT)
    d.line([(S * .06, S * .3), (S * .9, S * .14), (S * .96, S * .64), (S * .12, S * .82), (S * .06, S * .3)], fill=OUT, width=6)
    d.ellipse([S * .5, S * .34, S * .72, S * .5], fill=(190, 140, 70, 255))                                     # grease spot
    d.line([(S * .12, S * .82), (S * .96, S * .64), (S * .96, S * .7), (S * .14, S * .88)], fill=OUT, width=4)
    return _shrink(im, size)


# ---- Pistol Whip redo: a pistol in three poses --------------------------------------------------------------------------

def whip_pistol(size=64, pose="aim"):
    """A black semi-auto pistol, side view. aim = pointing right; up = tipped barrel-up (they look at it); whip =
    flipped round, held by the barrel, the grip leading - mid-swing."""
    from PIL import Image as _Im
    im, d, S = _big(size)
    OUT = (10, 10, 12, 255)
    BK, HI = (45, 45, 52, 255), (120, 125, 140, 255)
    d.rectangle([S * .14, S * .3, S * .9, S * .44], fill=BK, outline=OUT, width=6)                               # the slide
    for k in range(4):                                                                                            # slide serrations
        x = .2 + k * .05
        d.line([(S * x, S * .32), (S * x, S * .42)], fill=(80, 80, 90, 255), width=3)
    d.line([(S * .2, S * .33), (S * .86, S * .33)], fill=HI, width=3)                                            # shine
    d.rectangle([S * .86, S * .34, S * .94, S * .4], fill=(30, 30, 34, 255), outline=OUT, width=3)              # muzzle
    d.polygon([(S * .16, S * .44), (S * .4, S * .44), (S * .36, S * .86), (S * .14, S * .86), (S * .1, S * .6)], fill=(60, 55, 50, 255), outline=OUT)
    d.line([(S * .16, S * .44), (S * .4, S * .44), (S * .36, S * .86), (S * .14, S * .86), (S * .1, S * .6), (S * .16, S * .44)], fill=OUT, width=6)   # grip
    for k in range(4):
        y = .52 + k * .08
        d.line([(S * .16, S * y), (S * .34, S * y)], fill=(85, 80, 72, 255), width=3)                           # grip texture
    d.arc([S * .36, S * .4, S * .58, S * .62], 0, 180, fill=OUT, width=6)                                        # trigger guard
    d.line([(S * .46, S * .44), (S * .44, S * .54)], fill=OUT, width=5)                                          # trigger
    if pose == "up":
        im = im.rotate(60, resample=_Im.BICUBIC)
    elif pose == "whip":
        im = im.transpose(_Im.FLIP_LEFT_RIGHT).rotate(-35, resample=_Im.BICUBIC)
    return _shrink(im, size)
