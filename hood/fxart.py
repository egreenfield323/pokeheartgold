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

def _outlined_text(d, xy, text, fill, outline=(15, 10, 10, 255), font=None):
    """Pixel text with a 1px outline all round (readable on anything)."""
    from PIL import ImageFont
    font = font or ImageFont.load_default()
    x, y = xy
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx or dy:
                d.text((x + dx, y + dy), text, font=font, fill=outline)
    d.text((x, y), text, font=font, fill=fill)


def _text_w(d, text):
    from PIL import ImageFont
    l, t, r, b = d.textbbox((0, 0), text, font=ImageFont.load_default())
    return r - l


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
    _outlined_text(d, (32 - _text_w(d, "POCKET") // 2, 18), "POCKET", red)
    _outlined_text(d, (32 - _text_w(d, "SAND!") // 2, 31), "SAND!", red)
    return im


# ------------------------------------------------------------------ set 4: fifteen more moves

def burst_sign(lines, fill=(255, 215, 40, 255), text=(225, 25, 25, 255), spikes=28, size=64):
    """A comic-book burst with shouted text (WHAM!, HONK!, STOMP!, HI-YAH!)."""
    import math
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (20, 10, 10, 255)
    pts = []
    for k in range(spikes):
        a = k * math.pi * 2 / spikes
        r = 31 if k % 2 == 0 else 21
        pts.append((31.5 + r * math.cos(a), 31.5 + r * .8 * math.sin(a)))
    d.polygon(pts, fill=fill, outline=OUT)
    light = tuple(min(255, c + 60) for c in fill[:3]) + (255,)
    d.polygon([(31.5 + (x - 31.5) * .75, 31.5 + (y - 31.5) * .75) for x, y in pts], fill=light)
    y0 = 32 - len(lines) * 6
    for k, line in enumerate(lines):
        _outlined_text(d, (32 - _text_w(d, line) // 2, y0 + k * 12), line, text)
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
    """A budget airliner, side view, nose right: HOOD AIR."""
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    OUT = (20, 25, 40, 255)
    d.polygon([(6, 27), (52, 25), (61, 30), (52, 36), (8, 36), (3, 31)], fill=(245, 245, 250, 255), outline=OUT)
    d.polygon([(8, 27), (2, 13), (10, 13), (20, 27)], fill=(230, 40, 40, 255), outline=OUT)        # tail fin
    d.polygon([(26, 34), (38, 34), (30, 50), (22, 50)], fill=(200, 205, 215, 255), outline=OUT)   # wing
    d.rectangle([24, 44, 34, 48], fill=(120, 125, 140, 255), outline=OUT)                          # engine
    d.line([(8, 33), (55, 33)], fill=(230, 40, 40, 255), width=2)                                  # stripe
    for x in range(16, 50, 4):
        d.rectangle([x, 28, x + 1, 29], fill=(60, 120, 200, 255))                                   # windows
    d.polygon([(52, 27), (57, 28), (58, 30), (53, 30)], fill=(40, 60, 90, 255))                    # cockpit
    _outlined_text(d, (12, 14), "HOOD AIR", (230, 40, 40, 255), outline=(255, 255, 255, 255))
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
