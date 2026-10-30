#!/usr/bin/env python3
"""Bag icons for every renamed item that still had its original picture (make_items.py does the drinks).

Each design is drawn in full colour (32x32, PIL) and quantized to the icon's 15 colours. Several items share one
picture (the game's item table, in code, points them at the same NCGR) and differ only by palette: those get one
design, and each item's palette is the design's palette with its accent colours turned to the item's hue.
Items that share a palette but not a picture are quantized together. Edits files/itemtool/itemdata/item_icon/*
in place (same sizes; originals read from the base commit).
Run from the repo root:  python hood/make_item_icons.py [--preview out.png]
"""
import colorsys
import json
import math
import re
import struct
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_items as mi  # noqa: E402
import text_edits as te  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
K = (20, 16, 20, 255)
W = (250, 250, 250, 255)
GOLD, GOLD_D, GOLD_L = (240, 190, 50, 255), (170, 115, 20, 255), (255, 240, 150, 255)
FONT = {"O": ["111", "101", "101", "101", "111"], "G": ["111", "100", "101", "101", "111"],
        "$": ["010", "111", "110", "011", "111"], "H": ["101", "101", "111", "101", "101"],
        "R": ["110", "101", "110", "101", "101"], "X": ["101", "101", "010", "101", "101"],
        "V": ["101", "101", "101", "101", "010"], "I": ["111", "010", "010", "010", "111"],
        "P": ["110", "101", "110", "100", "100"], "1": ["010", "110", "010", "010", "111"],
        "T": ["111", "010", "010", "010", "010"]}


def canvas():
    im = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def text(d, x, y, s, c):
    for k, ch in enumerate(s):
        for yy, row in enumerate(FONT[ch]):
            for xx, bit in enumerate(row):
                if bit == "1":
                    d.point((x + k * 4 + xx, y + yy), fill=c)


def outlined(im):
    """A 1px dark outline round everything (the bag icons all have one)."""
    px = im.load()
    out = im.copy()
    po = out.load()
    for y in range(32):
        for x in range(32):
            if px[x, y][3] == 0 and any(0 <= x + dx < 32 and 0 <= y + dy < 32 and px[x + dx, y + dy][3]
                                        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                po[x, y] = K
    return out


# ------------------------------------------------------------------ the designs

def ball(top, bottom=(245, 245, 245, 255), deco=None):
    def draw():
        im, d = canvas()
        d.pieslice([4, 4, 27, 27], 180, 360, fill=top)
        d.pieslice([4, 4, 27, 27], 0, 180, fill=bottom)
        d.rectangle([4, 15, 27, 16], fill=K)
        d.ellipse([12, 12, 19, 19], fill=K)
        d.ellipse([13, 13, 18, 18], fill=W)
        d.point((8, 8), fill=W)
        d.point((9, 7), fill=W)
        if deco:
            deco(im, d)
        return outlined(im)
    return draw


def mark(kind):
    """A tiny version of the emblem painted on that sack in battle (ballfx._emblem), where the patch would be."""
    def draw(im, d):
        x, y = 19, 21
        if kind == "clock":
            d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=W, outline=K)
            d.line([(x, y), (x, y - 3)], fill=K)
            d.line([(x, y), (x + 2, y)], fill=K)
        elif kind == "heart":
            d.polygon([(x - 4, y - 2), (x - 2, y - 4), (x, y - 2), (x + 2, y - 4), (x + 4, y - 2), (x, y + 3)],
                      fill=(240, 50, 90, 255))
        elif kind == "plus":
            d.rectangle([x - 1, y - 4, x + 1, y + 4], fill=W)
            d.rectangle([x - 4, y - 1, x + 4, y + 1], fill=W)
        elif kind == "moon":
            d.ellipse([x - 4, y - 4, x + 4, y + 4], fill=(250, 240, 170, 255))
            d.ellipse([x - 1, y - 6, x + 6, y + 2], fill=(40, 70, 60, 255))
        elif kind == "star":
            d.polygon([(x, y - 5), (x + 1, y - 1), (x + 5, y - 1), (x + 2, y + 1), (x + 3, y + 5), (x, y + 3),
                       (x - 3, y + 5), (x - 2, y + 1), (x - 5, y - 1), (x - 1, y - 1)], fill=GOLD)
        elif kind == "bolt":
            d.polygon([(x + 1, y - 5), (x - 3, y + 1), (x, y + 1), (x - 1, y + 5), (x + 3, y - 1), (x, y - 1)],
                      fill=GOLD)
        elif kind == "crown":
            d.polygon([(x - 4, y + 3), (x - 4, y - 3), (x - 2, y), (x, y - 4), (x + 2, y), (x + 4, y - 3),
                       (x + 4, y + 3)], fill=GOLD)
        elif kind == "speed":
            for k in range(3):
                d.line([(x - 4, y - 3 + k * 3), (x + 2 + k % 2 * 2, y - 3 + k * 3)], fill=W)
        elif kind == "chevrons":
            for k in range(2):
                d.line([(x - 4, y + 2 - k * 4), (x, y - 2 - k * 4), (x + 4, y + 2 - k * 4)], fill=GOLD)
        elif kind == "hook":
            d.line([(x + 2, y - 5), (x + 2, y + 1)], fill=W)
            d.arc([x - 3, y - 1, x + 3, y + 5], 0, 200, fill=W)
        elif kind == "weight":
            d.line([(x - 5, y), (x + 5, y)], fill=W)
            d.rectangle([x - 5, y - 3, x - 3, y + 3], fill=K)
            d.rectangle([x + 3, y - 3, x + 5, y + 3], fill=K)
        elif kind == "peace":
            d.ellipse([x - 4, y - 4, x + 4, y + 4], outline=W)
            d.line([(x, y - 4), (x, y + 4)], fill=W)
        elif kind == "rocket":
            d.polygon([(x, y - 5), (x + 2, y - 1), (x + 2, y + 3), (x - 2, y + 3), (x - 2, y - 1)], fill=W)
            d.point([(x - 3, y + 3), (x + 3, y + 3)], fill=(230, 50, 50, 255))
        elif kind == "tree":
            d.polygon([(x, y - 5), (x - 4, y + 2), (x + 4, y + 2)], fill=(60, 160, 60, 255))
            d.line([(x, y + 2), (x, y + 4)], fill=(120, 80, 40, 255))
        elif kind == "house":
            d.polygon([(x - 4, y), (x, y - 4), (x + 4, y)], fill=W)
            d.rectangle([x - 3, y, x + 3, y + 4], fill=W)
        elif kind == "net":
            for k in (-3, 0, 3):
                d.line([(x + k - 2, y - 4), (x + k + 2, y + 4)], fill=W)
                d.line([(x + k + 2, y - 4), (x + k - 2, y + 4)], fill=W)
        elif kind == "camo":
            for px, py in ((x - 3, y - 2), (x + 2, y), (x - 1, y + 3)):
                d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(60, 80, 40, 255))
        elif kind == "x2":
            text(d, x - 4, y - 2, "X", W)
        elif kind == "jersey":
            d.rectangle([x - 3, y - 3, x + 3, y + 4], fill=W)
            d.line([(x - 5, y - 2), (x + 5, y - 2)], fill=W)
    return draw


def sack(base=(176, 132, 78), emblem=None):
    """A kidnapping sack (Nap Sack, and the other ___ Sacks in their old ball colour): tied off with rope, denim
    patch."""
    r, g, b = base
    body, dark = (r, g, b, 255), (int(r * .72), int(g * .72), int(b * .72), 255)
    light = (min(255, int(r * 1.2) + 20), min(255, int(g * 1.2) + 20), min(255, int(b * 1.2) + 20), 255)

    def draw():
        im, d = canvas()
        d.ellipse([5, 10, 26, 29], fill=body)
        d.ellipse([8, 13, 16, 24], fill=light)
        d.ellipse([17, 18, 25, 28], fill=dark)
        d.ellipse([9, 14, 23, 26], fill=body)
        d.polygon([(12, 11), (19, 11), (22, 4), (9, 4)], fill=dark)
        for x in (9, 13, 17, 21):
            d.ellipse([x - 2, 2, x + 2, 6], fill=body)
        d.rectangle([11, 9, 20, 11], fill=(232, 208, 150, 255))
        d.line([(20, 10), (25, 14)], fill=(232, 208, 150, 255), width=1)
        if emblem:
            emblem(im, d)
        else:
            d.rectangle([16, 19, 22, 24], fill=(70, 90, 150, 255))
            d.point([(16, 19), (19, 19), (22, 19), (16, 24), (19, 24), (22, 24)], fill=W)
        return outlined(im)
    return draw


def pool_ring():
    """Pool Sack: a red-and-white pool ring with a rubber duck head."""
    def draw():
        im, d = canvas()
        for k in range(8):
            d.pieslice([3, 10, 28, 28], k * 45, k * 45 + 45, fill=(220, 40, 40, 255) if k % 2 else W)
        d.ellipse([11, 16, 20, 22], fill=(0, 0, 0, 0))
        d.ellipse([20, 4, 28, 12], fill=(250, 210, 40, 255))
        d.polygon([(27, 7), (31, 8), (27, 10)], fill=(240, 120, 30, 255))
        d.point([(25, 7)], fill=K)
        return outlined(im)
    return draw


def designer_bag():
    """Drip Sack: a brown monogram designer handbag with a gold clasp."""
    def draw():
        im, d = canvas()
        d.arc([10, 4, 22, 16], 180, 360, fill=(100, 64, 30, 255), width=2)
        d.polygon([(7, 11), (25, 11), (28, 27), (4, 27)], fill=(150, 100, 50, 255))
        for x, y in ((9, 16), (15, 20), (21, 16), (12, 24), (19, 24), (24, 22)):
            d.point([(x, y), (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)], fill=(220, 180, 110, 255))
        d.rectangle([7, 11, 25, 14], fill=(100, 64, 30, 255))
        d.rectangle([14, 13, 18, 17], fill=GOLD)
        return outlined(im)
    return draw


def clutch(base, material):
    """Kurt's custom bags (apricorn balls): a clutch with a fold-over flap and gold clasp, in its material."""
    r, g, b = base
    body, dark = (r, g, b, 255), (int(r * .7), int(g * .7), int(b * .7), 255)
    light = (min(255, int(r * 1.2) + 30), min(255, int(g * 1.2) + 30), min(255, int(b * 1.2) + 30), 255)

    def draw():
        im, d = canvas()
        d.rounded_rectangle([4, 10, 27, 26], 3, fill=body)
        if material == "nylon":
            d.line([(6, 10), (6, 26)], fill=W, width=2)
            d.line([(25, 10), (25, 26)], fill=W, width=2)
        elif material in ("gator", "croc"):
            for y in range(12, 26, 3):
                for x in range(5 + (y // 3) % 2, 27, 3):
                    d.point((x, y), fill=dark if material == "gator" else light)
        elif material == "denim":
            for x in range(5, 27, 2):
                d.point([(x, 24)], fill=(240, 150, 40, 255))
        elif material == "velvet":
            d.ellipse([6, 14, 14, 24], fill=light)
            d.ellipse([7, 15, 15, 25], fill=body)
        elif material == "suede":
            d.point([(8, 20), (9, 20), (20, 22), (21, 22), (17, 17)], fill=dark)
        elif material == "satin":
            d.polygon([(7, 26), (10, 26), (17, 10), (14, 10)], fill=W)
        d.polygon([(4, 10), (27, 10), (16, 19)], fill=dark)
        d.ellipse([14, 16, 18, 20], fill=GOLD, outline=K)
        return outlined(im)
    return draw


def duffel_bag():
    """Duffel Bag: black gym duffel, red stripe, handles, zipper."""
    def draw():
        im, d = canvas()
        d.arc([10, 5, 22, 17], 180, 360, fill=(90, 90, 105, 255), width=2)
        d.rounded_rectangle([3, 11, 28, 27], 6, fill=(40, 40, 48, 255))
        d.rectangle([3, 18, 28, 20], fill=(210, 40, 40, 255))
        d.line([(7, 13), (24, 13)], fill=(220, 220, 230, 255))
        d.rectangle([22, 12, 24, 15], fill=(220, 220, 230, 255))
        d.ellipse([3, 13, 7, 25], fill=(80, 80, 96, 255))
        return outlined(im)
    return draw


def rug_roll():
    """Rug Roll: a rolled-up red Persian rug, spiral end, gold bands, tassels."""
    def draw():
        im, d = canvas()
        d.rounded_rectangle([6, 11, 29, 23], 6, fill=(170, 30, 40, 255))
        for x in (13, 19, 25):
            d.line([(x, 12), (x, 22)], fill=(230, 180, 60, 255), width=2)
        d.ellipse([2, 11, 14, 23], fill=(240, 225, 190, 255))
        d.arc([4, 13, 12, 21], 0, 300, fill=(110, 20, 28, 255))
        d.arc([6, 15, 10, 19], 0, 300, fill=(110, 20, 28, 255))
        d.line([(28, 12), (31, 13)], fill=(240, 225, 190, 255))
        d.line([(28, 21), (31, 22)], fill=(240, 225, 190, 255))
        return outlined(im)
    return draw


def whole_gang():
    """Whole Gang: three hoods, glowing eyes, gold chains - the whole squad."""
    def draw():
        im, d = canvas()
        for k, (cx, cy) in enumerate(((7, 13), (25, 13), (16, 9))):
            hood = ((60, 50, 90, 255), (60, 50, 90, 255), (34, 28, 48, 255))[k]
            d.rounded_rectangle([cx - 6, cy + 7, cx + 6, cy + 19], 3, fill=hood, outline=K)
            d.ellipse([cx - 6, cy - 4, cx + 6, cy + 8], fill=hood, outline=K)
            d.arc([cx - 6, cy - 4, cx + 6, cy + 8], 190, 350, fill=(170, 130, 250, 255))
            d.rectangle([cx - 3, cy + 1, cx - 2, cy + 2], fill=W)
            d.rectangle([cx + 2, cy + 1, cx + 3, cy + 2], fill=W)
            d.arc([cx - 4, cy + 7, cx + 4, cy + 14], 20, 160, fill=GOLD, width=2)
        return outlined(im)
    return draw


def dots(c):
    return lambda im, d: [d.point(p, fill=c) for p in ((9, 10), (14, 7), (20, 9), (23, 12), (11, 13), (17, 11))]


def bottle(body, cap, label=None, h=20, w=10, neck=4):
    def draw():
        im, d = canvas()
        top = 30 - h
        d.rectangle([16 - neck // 2, top - 5, 15 + neck // 2, top], fill=body)
        d.rectangle([16 - neck // 2 - 1, top - 8, 16 + neck // 2, top - 5], fill=cap)
        d.rounded_rectangle([16 - w // 2, top, 15 + w // 2, 29], 3, fill=body)
        d.line([(17 - w // 2, top + 2), (17 - w // 2, 27)], fill=(255, 255, 255, 180))
        if label:
            d.rectangle([17 - w // 2, top + h // 3, 14 + w // 2, top + h // 3 + 6], fill=label)
        return outlined(im)
    return draw


def soup():
    im, d = canvas()
    for x, y in ((12, 4), (16, 2), (20, 4)):
        d.arc([x - 2, y, x + 2, y + 7], 270, 90, fill=(220, 220, 225, 255))                       # steam
    d.chord([4, 6, 27, 28], 0, 180, fill=(220, 90, 50, 255))
    d.ellipse([5, 13, 26, 19], fill=(240, 180, 70, 255))                                            # soup
    d.point((11, 15), fill=(250, 240, 200, 255)); d.point((19, 16), fill=(90, 160, 60, 255))         # noodles, herbs
    d.line([(9, 16), (14, 15)], fill=(250, 240, 200, 255)); d.line([(17, 15), (22, 17)], fill=(250, 240, 200, 255))
    d.rectangle([12, 27, 19, 28], fill=(180, 60, 30, 255))
    return outlined(im)


def vial():
    im, d = canvas()
    d.rectangle([12, 5, 19, 9], fill=(120, 80, 50, 255))                                             # cork
    d.rounded_rectangle([10, 9, 21, 28], 3, fill=(200, 235, 245, 255))
    for x, y in ((13, 22), (16, 24), (18, 21), (14, 26), (17, 18)):
        d.point((x, y), fill=(255, 255, 255, 255)); d.point((x + 1, y), fill=(170, 210, 230, 255))   # salts
    return outlined(im)


def nasal_spray():
    im, d = canvas()
    d.polygon([(14, 2), (17, 2), (18, 10), (13, 10)], fill=(240, 240, 245, 255))                   # nozzle
    d.rectangle([10, 10, 21, 13], fill=(240, 240, 245, 255))                                         # finger rest
    d.rounded_rectangle([11, 13, 20, 29], 2, fill=(230, 60, 60, 255))
    d.rectangle([12, 17, 19, 23], fill=(250, 250, 250, 255))
    d.line([(13, 20), (18, 20)], fill=(220, 40, 40, 255))
    return outlined(im)


def water_glass():
    im, d = canvas()
    d.polygon([(7, 6), (24, 6), (22, 29), (9, 29)], fill=(220, 235, 245, 255))
    d.polygon([(8, 13), (23, 13), (22, 28), (9, 28)], fill=(120, 180, 240, 255))
    d.line([(9, 8), (11, 26)], fill=(255, 255, 255, 255))
    d.point((15, 18), fill=(255, 255, 255, 255)); d.point((18, 22), fill=(255, 255, 255, 255))      # bubbles
    return outlined(im)


def tall_can(body, accent):
    def draw():
        im, d = canvas()
        d.rectangle([9, 3, 22, 29], fill=body)
        d.rectangle([9, 3, 22, 5], fill=(200, 200, 205, 255))
        d.ellipse([11, 11, 20, 20], fill=accent)                                                    # the flower
        for a in range(0, 360, 60):
            d.point((15.5 + 5 * math.cos(math.radians(a)), 15.5 + 5 * math.sin(math.radians(a))), fill=(250, 250, 250, 255))
        d.line([(10, 6), (10, 28)], fill=(255, 255, 255, 160))
        return outlined(im)
    return draw


def milk_carton():
    im, d = canvas()
    d.polygon([(9, 9), (15, 3), (22, 9)], fill=(240, 240, 240, 255))
    d.rectangle([9, 9, 22, 29], fill=(120, 70, 40, 255))
    d.rectangle([10, 13, 21, 21], fill=(245, 235, 220, 255))
    d.ellipse([13, 14, 18, 19], fill=(150, 90, 50, 255))
    d.line([(15, 3), (15, 8)], fill=(200, 200, 200, 255))
    return outlined(im)


def ammo_box():
    im, d = canvas()
    d.rectangle([4, 10, 27, 27], fill=(90, 110, 50, 255))
    d.rectangle([4, 10, 27, 13], fill=(70, 88, 38, 255))
    d.rectangle([12, 6, 19, 9], fill=(60, 60, 60, 255))                                              # handle
    d.rectangle([8, 17, 23, 22], fill=(230, 200, 80, 255))
    for x in (10, 14, 18):
        d.rectangle([x, 18, x + 2, 21], fill=(180, 120, 40, 255))                                    # rounds on the label
    return outlined(im)


def check_badge():
    im, d = canvas()
    pts = []
    for k in range(16):
        a = k * math.pi / 8
        r = 13 if k % 2 == 0 else 11
        pts.append((15.5 + r * math.cos(a), 15.5 + r * math.sin(a)))
    d.polygon(pts, fill=(40, 150, 240, 255))
    d.line([(10, 16), (14, 20), (22, 11)], fill=(250, 250, 250, 255), width=3)
    return outlined(im)


def protein_bar():
    im, d = canvas()
    d.polygon([(3, 18), (24, 7), (29, 14), (8, 25)], fill=(60, 60, 70, 255))
    d.polygon([(3, 18), (6, 16), (11, 23), (8, 25)], fill=(200, 200, 205, 255))                     # crimped ends
    d.polygon([(21, 8.5), (24, 7), (29, 14), (26, 15.5)], fill=(200, 200, 205, 255))
    d.polygon([(10, 16), (20, 11), (22, 14), (12, 19)], fill=(250, 200, 40, 255))
    return outlined(im)


def duffel():
    im, d = canvas()
    d.arc([9, 4, 22, 18], 180, 360, fill=(40, 40, 45, 255), width=2)                                 # straps
    d.rounded_rectangle([3, 11, 28, 27], 6, fill=(200, 40, 40, 255))
    d.line([(6, 13), (25, 13)], fill=(250, 250, 250, 255))                                           # zip
    d.rectangle([12, 18, 19, 22], fill=(250, 250, 250, 255))
    d.ellipse([5, 16, 8, 24], fill=(160, 25, 25, 255)); d.ellipse([23, 16, 26, 24], fill=(160, 25, 25, 255))
    return outlined(im)


def magazine(drum=False):
    def draw():
        im, d = canvas()
        if drum:
            d.rectangle([12, 3, 19, 12], fill=(60, 60, 68, 255))
            d.ellipse([5, 10, 26, 30], fill=(40, 40, 46, 255))
            d.ellipse([10, 15, 21, 25], fill=(90, 90, 100, 255))
            d.ellipse([14, 19, 17, 22], fill=(200, 200, 210, 255))
            d.rectangle([13, 1, 18, 3], fill=(200, 160, 60, 255))
        else:
            d.polygon([(11, 3), (18, 3), (22, 29), (15, 29)], fill=(45, 45, 52, 255))
            d.rectangle([12, 1, 17, 3], fill=(200, 160, 60, 255))                                    # top round
            d.line([(13, 6), (16, 26)], fill=(110, 110, 120, 255))
        return outlined(im)
    return draw


def x_shot():
    im, d = canvas()
    d.rectangle([11, 4, 20, 8], fill=(40, 40, 40, 255))
    d.rounded_rectangle([9, 8, 22, 29], 3, fill=(230, 60, 40, 255))
    d.rectangle([10, 13, 21, 24], fill=(250, 250, 250, 255))
    text(d, 14, 16, "X", (20, 20, 20, 255))
    return outlined(im)


def getaway_car():
    im, d = canvas()
    for y in (12, 16, 20):
        d.line([(1, y), (5, y)], fill=(200, 200, 210, 255))                                          # speed lines
    d.polygon([(7, 18), (11, 11), (22, 11), (26, 18)], fill=(30, 30, 35, 255))                        # cab
    d.polygon([(12, 12), (16, 12), (16, 17), (10, 17)], fill=(120, 170, 220, 255))
    d.polygon([(18, 12), (21, 12), (24, 17), (18, 17)], fill=(120, 170, 220, 255))
    d.rounded_rectangle([5, 17, 30, 24], 2, fill=(40, 40, 46, 255))
    d.rectangle([27, 18, 30, 19], fill=(255, 220, 80, 255))                                          # headlight
    for x in (11, 24):
        d.ellipse([x - 3, 21, x + 3, 27], fill=(20, 20, 20, 255)); d.ellipse([x - 1, 23, x + 1, 25], fill=(180, 180, 190, 255))
    return outlined(im)


def spray_can():
    im, d = canvas()
    d.rectangle([13, 2, 18, 5], fill=(30, 30, 30, 255))                                              # trigger
    d.rectangle([11, 5, 20, 8], fill=(60, 60, 60, 255))
    d.rounded_rectangle([10, 8, 21, 29], 2, fill=(230, 120, 30, 255))
    d.rectangle([11, 14, 20, 22], fill=(30, 30, 30, 255))
    d.line([(13, 18), (18, 18)], fill=(250, 220, 60, 255))
    for x, y in ((24, 4), (26, 6), (27, 3)):
        d.point((x, y), fill=(250, 140, 60, 255))                                                    # mist
    return outlined(im)


def grill():
    im, d = canvas()
    d.chord([2, 8, 29, 28], 180, 360, fill=(160, 50, 60, 255))                                       # gums
    for k in range(6):
        x = 4 + k * 4
        d.rectangle([x, 15, x + 3, 22], fill=GOLD)
        d.line([(x + 1, 16), (x + 1, 20)], fill=GOLD_L)
        d.line([(x + 3, 15), (x + 3, 22)], fill=GOLD_D)
    d.point((13, 17), fill=(150, 220, 255, 255)); d.point((21, 18), fill=(150, 220, 255, 255))       # diamonds
    return outlined(im)


def cash(big):
    def draw():
        im, d = canvas()
        n = 5 if big else 2
        for k in range(n):
            y = 24 - k * 3
            d.rectangle([5, y, 26, y + 4], fill=(110, 170, 90, 255))
            d.line([(6, y + 1), (25, y + 1)], fill=(170, 220, 150, 255))
        d.rectangle([13, 24 - (n - 1) * 3, 18, 28], fill=(240, 200, 60, 255))                         # the band
        text(d, 14, 24 - (n - 1) * 3, "$", (40, 90, 40, 255)) if big else None
        return outlined(im)
    return draw


def diamond(size):
    def draw():
        im, d = canvas()
        s = size
        d.polygon([(16 - s, 13), (16 - s // 2, 13 - s // 2), (16 + s // 2, 13 - s // 2), (16 + s, 13), (16, 13 + s + 2)],
                  fill=(150, 220, 250, 255))
        d.polygon([(16 - s // 2, 13 - s // 2), (16, 13), (16 + s // 2, 13 - s // 2)], fill=(230, 250, 255, 255))
        d.line([(16 - s, 13), (16 + s, 13)], fill=(90, 160, 210, 255))
        d.point((16 - s // 2 + 1, 12 - s // 2 + 2), fill=W)
        if s < 8:                                                                                     # the stud's post
            d.line([(16, 13 + s + 3), (16, 29)], fill=(200, 200, 210, 255))
        return outlined(im)
    return draw


def lint():
    im, d = canvas()
    for x, y, r in ((12, 18, 7), (19, 16, 6), (16, 22, 6), (21, 22, 4)):
        d.ellipse([x - r, y - r, x + r, y + r], fill=(170, 170, 180, 255))
    for x, y in ((9, 16), (15, 13), (22, 19), (13, 24), (18, 20)):
        d.point((x, y), fill=(120, 120, 135, 255))
    d.line([(24, 11), (28, 7)], fill=(170, 170, 180, 255))                                            # a stray thread
    return outlined(im)


def watch():
    im, d = canvas()
    d.rectangle([12, 2, 19, 30], fill=(210, 215, 225, 255))                                           # band
    for y in range(4, 30, 3):
        d.point((13, y), fill=(255, 255, 255, 255)); d.point((18, y + 1), fill=(150, 220, 250, 255))
    d.ellipse([7, 9, 24, 24], fill=(230, 235, 245, 255))
    d.ellipse([9, 11, 22, 22], fill=(30, 30, 40, 255))
    for a in range(0, 360, 45):
        d.point((15.5 + 5.5 * math.cos(math.radians(a)), 16.5 + 5.5 * math.sin(math.radians(a))), fill=(150, 220, 250, 255))
    d.line([(15, 16), (15, 13)], fill=W); d.line([(15, 16), (18, 17)], fill=W)
    return outlined(im)


def lighter():
    im, d = canvas()
    d.polygon([(15, 2), (18, 7), (16, 11), (13, 7)], fill=(255, 150, 30, 255))
    d.polygon([(15, 5), (16, 8), (15, 10), (14, 8)], fill=(255, 240, 120, 255))
    d.rectangle([11, 11, 20, 14], fill=(190, 190, 200, 255))
    d.ellipse([18, 10, 21, 13], fill=(120, 120, 130, 255))
    d.rounded_rectangle([10, 14, 21, 29], 2, fill=(230, 50, 50, 255))
    d.line([(11, 16), (11, 27)], fill=(255, 140, 140, 255))
    return outlined(im)


def water_balloon():
    im, d = canvas()
    d.ellipse([6, 4, 25, 25], fill=(70, 140, 240, 255))
    d.ellipse([9, 7, 14, 12], fill=(200, 230, 255, 255))
    d.polygon([(14, 25), (17, 25), (16, 28)], fill=(50, 110, 210, 255))
    d.line([(16, 28), (18, 30)], fill=(50, 110, 210, 255))
    return outlined(im)


def car_battery():
    im, d = canvas()
    d.rectangle([4, 10, 27, 27], fill=(40, 40, 46, 255))
    d.rectangle([4, 10, 27, 13], fill=(60, 60, 68, 255))
    d.rectangle([7, 6, 11, 10], fill=(220, 40, 40, 255)); d.rectangle([20, 6, 24, 10], fill=(200, 200, 210, 255))
    d.rectangle([7, 17, 24, 23], fill=(250, 200, 40, 255))
    d.polygon([(16, 17), (13, 21), (16, 21), (14, 24), (19, 19), (16, 19), (18, 17)], fill=(30, 30, 30, 255))
    return outlined(im)


def mower():
    im, d = canvas()
    d.line([(6, 2), (14, 17)], fill=(60, 60, 60, 255), width=2)                                       # handle
    d.rectangle([4, 1, 9, 3], fill=(60, 60, 60, 255))
    d.rounded_rectangle([10, 15, 28, 24], 3, fill=(60, 170, 60, 255))
    d.rectangle([17, 12, 23, 15], fill=(200, 200, 205, 255))                                          # engine
    for x in (13, 25):
        d.ellipse([x - 3, 22, x + 3, 28], fill=(20, 20, 20, 255))
    for x in (3, 6, 9):
        d.line([(x, 29), (x, 26)], fill=(80, 190, 60, 255))                                           # grass
    return outlined(im)


def moon_rock():
    im, d = canvas()
    d.polygon([(5, 18), (9, 9), (17, 6), (25, 10), (27, 19), (21, 27), (10, 26)], fill=(150, 160, 180, 255))
    for x, y, r in ((12, 14, 2), (20, 18, 3), (15, 21, 1)):
        d.ellipse([x - r, y - r, x + r, y + r], fill=(110, 115, 135, 255))
    d.line([(8, 11), (12, 8)], fill=(220, 225, 240, 255))
    for x, y in ((24, 6), (27, 9)):
        d.point((x, y), fill=(255, 255, 200, 255))
    return outlined(im)


def sunglasses():
    im, d = canvas()
    d.line([(2, 12), (29, 12)], fill=(20, 20, 20, 255), width=2)
    d.rounded_rectangle([3, 12, 14, 20], 3, fill=(20, 20, 25, 255))
    d.rounded_rectangle([17, 12, 28, 20], 3, fill=(20, 20, 25, 255))
    d.line([(5, 14), (8, 14)], fill=(140, 150, 200, 255)); d.line([(19, 14), (22, 14)], fill=(140, 150, 200, 255))
    return outlined(im)


def snack_bag(body, accent, curl=True):
    def draw():
        im, d = canvas()
        d.polygon([(7, 4), (24, 4), (26, 28), (5, 28)], fill=body)
        for x in range(7, 25, 3):
            d.polygon([(x, 4), (x + 1, 2), (x + 3, 4)], fill=body)                                    # crimps
        d.ellipse([9, 11, 22, 22], fill=accent)
        if curl:
            d.arc([11, 13, 20, 20], 0, 300, fill=(250, 250, 250, 255))
        d.line([(8, 6), (7, 26)], fill=(255, 255, 255, 140))
        return outlined(im)
    return draw


def pickle():
    im, d = canvas()
    d.ellipse([9, 3, 23, 29], fill=(100, 160, 50, 255))
    d.ellipse([10, 4, 17, 28], fill=(130, 190, 70, 255))
    for x, y in ((13, 8), (19, 12), (14, 16), (20, 20), (15, 24)):
        d.point((x, y), fill=(60, 110, 30, 255))                                                      # bumps
    return outlined(im)


def takeout():
    im, d = canvas()
    d.polygon([(6, 12), (25, 12), (22, 29), (9, 29)], fill=(245, 245, 240, 255))
    d.polygon([(6, 12), (11, 6), (20, 6), (25, 12)], fill=(230, 230, 225, 255))
    d.arc([10, 1, 21, 12], 200, 340, fill=(160, 160, 165, 255))                                       # wire handle
    d.rectangle([12, 17, 19, 23], fill=(220, 40, 40, 255))
    d.point((15, 20), fill=(250, 220, 80, 255)); d.point((16, 19), fill=(250, 220, 80, 255))
    return outlined(im)


def bike():
    im, d = canvas()
    for x in (8, 24):
        d.ellipse([x - 6, 15, x + 6, 27], outline=(30, 30, 30, 255), width=2)
    d.line([(8, 21), (14, 13), (22, 13), (24, 21)], fill=(220, 40, 40, 255), width=2)
    d.line([(14, 13), (16, 21), (8, 21)], fill=(220, 40, 40, 255), width=2)
    d.line([(12, 11), (16, 11)], fill=(30, 30, 30, 255), width=2)                                     # seat
    d.line([(22, 13), (21, 9), (24, 9)], fill=(30, 30, 30, 255), width=2)
    d.arc([12, 23, 20, 30], 180, 360, fill=(250, 200, 50, 255))                                       # cut lock
    return outlined(im)


# original item name -> (design, accent hue for a shared picture: None = the design's own colours)
DESIGNS = {
    "Master Ball": (whole_gang(), None),
    "Ultra Ball": (rug_roll(), None),
    "Great Ball": (duffel_bag(), None),
    "Poké Ball": (sack(), None),
    "Safari Ball": (sack((110, 150, 70), mark("camo")), None),
    "Net Ball": (sack((60, 170, 180), mark("net")), None),
    "Dive Ball": (pool_ring(), None),
    "Nest Ball": (sack((120, 180, 70), mark("house")), None),
    "Repeat Ball": (sack((240, 140, 40), mark("x2")), None),
    "Timer Ball": (sack((220, 70, 60), mark("clock")), None),
    "Luxury Ball": (designer_bag(), None),
    "Premier Ball": (sack((235, 235, 235), mark("star")), None),
    "Dusk Ball": (sack((40, 70, 60), mark("moon")), None),
    "Heal Ball": (sack((240, 130, 180), mark("plus")), None),
    "Quick Ball": (sack((60, 100, 210), mark("bolt")), None),
    "Fast Ball": (clutch((40, 70, 180), "nylon"), None),
    "Level Ball": (clutch((90, 110, 50), "gator"), None),
    "Lure Ball": (clutch((40, 80, 60), "croc"), None),
    "Heavy Ball": (clutch((60, 90, 150), "denim"), None),
    "Love Ball": (clutch((130, 20, 70), "velvet"), None),
    "Friend Ball": (clutch((170, 120, 70), "suede"), None),
    "Moon Ball": (clutch((190, 190, 220), "satin"), None),
    "Sport Ball": (sack((240, 140, 40), mark("jersey")), None),
    "Park Ball": (sack((240, 200, 60), mark("tree")), None),
    "Cherish Ball": (sack((200, 40, 50), mark("crown")), None),
    "Antidote": (bottle((240, 150, 190, 255), (240, 240, 240, 255), (250, 250, 250, 255)), None),
    "Full Heal": (soup, None),
    "Revive": (vial, None),
    "Max Revive": (nasal_spray, None),
    "Fresh Water": (water_glass, None),
    "Soda Pop": (bottle((220, 40, 40, 255), (240, 240, 240, 255), (250, 250, 250, 255), h=21, w=9), None),
    "Lemonade": (tall_can((120, 200, 190, 255), (240, 140, 160, 255)), None),
    "Moomoo Milk": (milk_carton, None),
    "Ether": (ammo_box, .22), "Max Ether": (ammo_box, .10), "Elixir": (ammo_box, .0), "Max Elixir": (ammo_box, .75),
    "Rare Candy": (check_badge, None),
    "HP Up": (protein_bar, None),
    "Protein": (duffel, .0), "Iron": (duffel, .62), "Carbos": (duffel, .08), "Calcium": (duffel, .33), "Zinc": (duffel, .55),
    "PP Up": (magazine(False), None),
    "PP Max": (magazine(True), None),
    "X Attack": (x_shot, .0), "X Defend": (x_shot, .6), "X Speed": (x_shot, .15), "X Accuracy": (x_shot, .8),
    "Escape Rope": (getaway_car, None),
    "Repel": (spray_can, .07), "Super Repel": (spray_can, .9), "Max Repel": (spray_can, .55),
    "Nugget": (grill, None),
    "Big Mushroom": (cash(True), None), "TinyMushroom": (cash(False), None),
    "Pearl": (diamond(5), None), "Big Pearl": (diamond(10), None),
    "Stardust": (lint, None), "Star Piece": (watch, None),
    "Fire Stone": (lighter, None), "Water Stone": (water_balloon, None), "Thunderstone": (car_battery, None),
    "Leaf Stone": (mower, None), "Moon Stone": (moon_rock, None), "Sun Stone": (sunglasses, None),
    "Oran Berry": (snack_bag((120, 40, 160, 255), (240, 120, 40, 255)), None),
    "Sitrus Berry": (snack_bag((220, 40, 30, 255), (255, 170, 40, 255)), None),
    "Lum Berry": (pickle, None),
    "Leftovers": (takeout, None),
    "Bicycle": (bike, None),
}

# ------------------------------------------------------------------ files


def icon_table():
    """{original item name: (NCGR, NCLR)} from the game's item table."""
    src = (ROOT / "src/item.c").read_text(encoding="utf-8")
    tab = {m.group(1): (int(m.group(2)), int(m.group(3))) for m in re.finditer(
        r"\[(ITEM_\w+)\]\s*=\s*\{\s*NARC_item_data_\d+_bin,\s*NARC_item_icon_item_icon_(\d+)_NCGR,"
        r"\s*NARC_item_icon_item_icon_(\d+)_NCLR", src)}
    vals = {}
    for line in (ROOT / "include/constants/items.h").read_text(encoding="utf-8").splitlines():
        m = re.match(r"#define (ITEM_\w+)\s+(\d+)", line.strip())
        if m and m.group(1) in tab:
            vals.setdefault(int(m.group(2)), m.group(1))
    names = te.base_banks(["msg_0222"])["msg_0222"]
    return {name: tab[vals[i]] for i, name in names.items() if i in vals}


def recolor(pal, hue):
    """The palette with its saturated (accent) colours turned to `hue`."""
    out = []
    for r, g, b in pal:
        h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
        if s > .3 and .12 < l < .9:
            r, g, b = (round(v * 255) for v in colorsys.hls_to_rgb(hue, l, s))
        out.append((r, g, b))
    return out


def build():
    """{relative path: bytes} for every icon file, and the preview images."""
    table = icon_table()
    # group the designs that share a picture or a palette: each group is quantized together
    groups, owner = [], {}
    for name in DESIGNS:
        g, p = table[name]
        hit = [k for k, grp in enumerate(groups) if any(table[n][0] == g or table[n][1] == p for n in grp)]
        if hit:
            groups[hit[0]].append(name)
        else:
            groups.append([name])
    files, previews = {}, []
    for grp in groups:
        pics = {}                                                     # NCGR -> image (the first design drawn)
        for name in grp:
            pics.setdefault(table[name][0], DESIGNS[name][0]())
        strip = Image.new("RGBA", (32 * len(pics), 32))
        for k, im in enumerate(pics.values()):
            strip.paste(im, (32 * k, 0))
        rgb = Image.new("RGB", strip.size, (0, 0, 0))
        rgb.paste(strip, mask=strip.split()[3])
        q = rgb.quantize(colors=15, method=Image.MEDIANCUT, dither=Image.NONE)
        flat = q.getpalette()[:45]
        flat += [0] * (45 - len(flat))                               # (fewer colours than 15: pad)
        base = [tuple(flat[i * 3:i * 3 + 3]) for i in range(15)]
        qa, sa = q.load(), strip.load()
        for k, (g, im) in enumerate(pics.items()):
            img = [[(qa[32 * k + x, y] + 1) if sa[32 * k + x, y][3] else 0 for x in range(32)] for y in range(32)]
            b = mi.head(mi.P % (g, "NCGR"))
            mi.write_ncgr(b, img)
            files[mi.P % (g, "NCGR")] = bytes(b)
            for name in grp:
                if table[name][0] == g:
                    hue = DESIGNS[name][1]
                    pal = recolor(base, hue) if hue is not None else base
                    c = table[name][1]
                    if mi.P % (c, "NCLR") not in files:
                        bb = mi.head(mi.P % (c, "NCLR"))
                        mi.write_nclr(bb, pal)
                        files[mi.P % (c, "NCLR")] = bytes(bb)
                    show = Image.new("RGBA", (32, 32))
                    show.putdata([(*pal[v - 1], 255) if v else (0, 0, 0, 0) for row in img for v in row])
                    previews.append((name, show))
    return files, previews


def main():
    files, previews = build()
    if "--preview" in sys.argv:
        items = {k: v for k, v in json.loads((ROOT / "hood/data/items.json").read_text(encoding="utf-8")).items()
                 if not k.startswith("_")}
        cols = 10
        sheet = Image.new("RGB", (cols * 40, ((len(previews) + cols - 1) // cols) * 48), (200, 205, 200))
        d = ImageDraw.Draw(sheet)
        for k, (name, im) in enumerate(previews):
            x, y = (k % cols) * 40, (k // cols) * 48
            sheet.paste(im, (x + 4, y + 2), im)
            d.text((x + 1, y + 35), items.get(name, [name])[0][:8], fill=(0, 0, 0))
        sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST).save(sys.argv[sys.argv.index("--preview") + 1])
        print("preview written:", len(previews), "icons")
        return
    for rel, b in files.items():
        (ROOT / rel).write_bytes(b)
    print(f"item icons: {len(files)} files")


if __name__ == "__main__":
    main()
