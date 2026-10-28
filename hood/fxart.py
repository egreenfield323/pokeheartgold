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
    """A budget airliner, side view, nose right: HOOD AIR - with a rope ladder hanging off it."""
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
    rope = (200, 160, 90, 255)                                                                      # rope ladder
    for x in (38, 44):
        d.line([(x, 36), (x + 1, 62)], fill=rope, width=1)
    for y in range(40, 63, 4):
        d.line([(38 + (y - 36) // 26, y), (44 + (y - 36) // 26, y)], fill=rope)
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


def _big_text(im, text, centre, fill, scale=2):
    """Pixel text blown up `scale` times (nearest neighbour), with a 1px dark outline, centred at `centre`."""
    from PIL import ImageFont
    t = Image.new("RGBA", (6 * len(text) + 4, 14), (0, 0, 0, 0))
    ImageDraw.Draw(t).text((1, 1), text, font=ImageFont.load_default(), fill=fill)
    bb = t.getbbox()
    t = t.crop(bb)
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


def big_taser(size=64):
    """A comically huge yellow taser, XL on the side, the cartridge glowing blue, pointing right."""
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
    _big_text(im, "XL", (23, 26), (225, 30, 30, 255))
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
    """Red ink, stamped on crooked: TAXED in a double box."""
    import random
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    RED = (225, 25, 30, 255)
    d.rectangle([3, 17, 60, 46], outline=RED, width=3)
    d.rectangle([7, 21, 56, 42], outline=RED, width=1)
    _big_text(im, "TAXED", (32, 32), RED, scale=2)
    rnd = random.Random(5)
    px = im.load()
    for _ in range(70):                                                                              # worn ink
        x, y = rnd.randrange(size), rnd.randrange(16, 48)
        if px[x, y][0] > 150 and px[x, y][3]:
            px[x, y] = (0, 0, 0, 0)
    return im.rotate(16, resample=Image.NEAREST)


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
        d.text((32 - w // 2, y - 5), text, fill=(220, 20, 20, 255))
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
