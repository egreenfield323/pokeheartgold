"""The catching items are kidnapping gear (items.json: Nap Sack, Duffel Bag, Rug Roll, Whole Gang, ___ Sack):
thrown over the homie, it wobbles while they fight it, and they jump back out when sent out.

The throw itself is engine code (battle_anim_ball.c, overlay 7); what it draws comes from data, per ball
(ball id - 1 = the row of the overlay-7 tables in asm/battle_anim_data.s):
- a/0/0/8: the OAM sprite (sBallSpriteResources: char 0x105 + 3 row, palette 0x53 + row, cell 0x104 + 3 row).
  10 cells: 0 closed, 1-7 spinning in flight, 8 squashed (wobbling), 9 open.
- a/0/9/5: particles. Send-out: gBallAnimSealParticles (file, emitter count). Capture: gBallAnimBurstParticles
  (file, skipped emitter, emitter count) - the sack opening plays every emitter but the skipped one, the click
  plays only the skipped one. Break-out (every ball): member 52, 2 emitters.

    patch(rom)   (called from battlefx.patch)
"""
import math
import struct

import ndspy.lz10
import ndspy.narc
from PIL import Image, ImageDraw

BALLS = 25                                                    # Master .. Park (rows 0-24)
LOOK = {}                                                     # testing: {row: row whose look it borrows}
SIZE = 32                                                     # every cell becomes one 32x32 OAM (was 16x16)
LIFT = -26                                                    # its top edge: the art is bottom-heavy, so the gear
#                                                               lands where the 16px ball did, not 10px lower

OUTLINE = (40, 26, 16, 255)
ROPE = (232, 208, 150, 255)
ROPE_D = (170, 140, 80, 255)
HOLE = (24, 16, 10, 255)
PATCH = (70, 90, 150, 255)
STITCH = (240, 240, 240, 255)
BURLAP = (176, 132, 78)

# sack colours for the other balls (row -> base colour): their old ball colour, so you can still tell them apart
TINT = {4: (110, 150, 70), 5: (60, 170, 180), 6: (70, 130, 230), 7: (120, 180, 70), 8: (240, 140, 40),
        9: (220, 70, 60), 10: (50, 50, 56), 11: (235, 235, 235), 12: (40, 70, 60), 13: (240, 130, 180),
        14: (60, 100, 210), 15: (200, 40, 50), 16: (240, 200, 50), 17: (220, 70, 50), 18: (50, 90, 200),
        19: (100, 100, 110), 20: (240, 130, 180), 21: (70, 170, 70), 22: (50, 60, 130), 23: (240, 140, 40),
        24: (240, 200, 60)}

# what's painted on each sack
EMBLEM = {4: "camo", 5: "net", 7: "house", 8: "x2", 9: "clock", 11: "star", 12: "moon", 13: "plus", 14: "bolt",
          15: "crown", 23: "jersey", 24: "tree"}


def _shades(base):
    r, g, b = base
    return ((r, g, b, 255), (int(r * .72), int(g * .72), int(b * .72), 255),
            (min(255, int(r * 1.2) + 20), min(255, int(g * 1.2) + 20), min(255, int(b * 1.2) + 20), 255))


EMBLEM_INK = (250, 250, 250, 255)
GOLDEN = (250, 200, 40, 255)


def _emblem(d, kind, x, y, body):
    """A big chunky symbol centred at (x, y) on the 64px canvas (white or gold, dark outline: it survives the
    halving)."""
    d.fontmode = "1"
    W, O = EMBLEM_INK, OUTLINE
    if kind == "camo":
        for dx, dy, r in ((-8, -6, 5), (6, -2, 6), (-2, 8, 5), (10, 10, 4)):
            d.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r], fill=(60, 80, 40, 255))
    elif kind == "net":
        for k in range(-12, 13, 6):
            d.line([x + k - 6, y - 10, x + k + 6, y + 10], fill=W, width=2)
            d.line([x + k + 6, y - 10, x + k - 6, y + 10], fill=W, width=2)
    elif kind == "house":
        d.polygon([(x - 11, y), (x, y - 11), (x + 11, y)], fill=W, outline=O)
        d.rectangle([x - 8, y, x + 8, y + 10], fill=W, outline=O)
        d.rectangle([x - 3, y + 3, x + 3, y + 10], fill=O)
    elif kind == "x2":
        d.line([x - 12, y - 6, x - 2, y + 6], fill=W, width=4)
        d.line([x - 2, y - 6, x - 12, y + 6], fill=W, width=4)
        d.arc([x, y - 8, x + 12, y + 2], 180, 30, fill=W, width=4)
        d.line([x + 11, y, x + 1, y + 7], fill=W, width=4)
        d.line([x + 1, y + 7, x + 13, y + 7], fill=W, width=4)
    elif kind == "clock":
        d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=W, outline=O, width=2)
        d.line([x, y, x, y - 8], fill=O, width=3)
        d.line([x, y, x + 6, y + 3], fill=O, width=3)
    elif kind == "star":
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            r = 13 if k % 2 == 0 else 6
            pts.append((x + r * math.cos(a), y + r * math.sin(a)))
        d.polygon(pts, fill=GOLDEN, outline=O)
    elif kind == "moon":
        d.ellipse([x - 12, y - 12, x + 12, y + 12], fill=(250, 240, 170, 255), outline=O)
        d.ellipse([x - 4, y - 14, x + 16, y + 6], fill=body)             # bite out of it: a crescent
    elif kind == "plus":
        d.rectangle([x - 4, y - 12, x + 4, y + 12], fill=W, outline=O)
        d.rectangle([x - 12, y - 4, x + 12, y + 4], fill=W, outline=O)
        d.rectangle([x - 3, y - 11, x + 3, y + 11], fill=W)
    elif kind == "bolt":
        d.polygon([(x + 2, y - 14), (x - 8, y + 2), (x - 1, y + 2), (x - 4, y + 14), (x + 8, y - 3), (x + 1, y - 3)],
                  fill=GOLDEN, outline=O)
    elif kind == "heart":
        d.ellipse([x - 12, y - 10, x, y + 2], fill=(240, 50, 90, 255))
        d.ellipse([x, y - 10, x + 12, y + 2], fill=(240, 50, 90, 255))
        d.polygon([(x - 12, y - 3), (x + 12, y - 3), (x, y + 12)], fill=(240, 50, 90, 255))
    elif kind == "speed":
        for k, ln in enumerate((18, 24, 14)):
            d.line([x - 12, y - 8 + k * 8, x - 12 + ln, y - 8 + k * 8], fill=W, width=3)
    elif kind == "chevrons":
        for k in range(3):
            d.line([x - 10, y + 6 - k * 7, x, y - 2 - k * 7, x + 10, y + 6 - k * 7], fill=GOLDEN, width=3)
    elif kind == "hook":
        d.line([x + 4, y - 14, x + 4, y + 4], fill=W, width=3)
        d.arc([x - 8, y - 4, x + 6, y + 12], 0, 200, fill=W, width=3)
        d.line([x - 8, y + 2, x - 4, y - 2], fill=W, width=3)
    elif kind == "weight":
        d.rectangle([x - 14, y - 2, x + 14, y + 2], fill=(200, 200, 210, 255), outline=O)
        for s in (-1, 1):
            d.rectangle([x + s * 12 - 4, y - 10, x + s * 12 + 4, y + 10], fill=(60, 60, 66, 255), outline=O)
    elif kind == "peace":
        d.ellipse([x - 12, y - 12, x + 12, y + 12], outline=W, width=3)
        d.line([x, y - 12, x, y + 12], fill=W, width=3)
        d.line([x, y, x - 8, y + 9], fill=W, width=3)
        d.line([x, y, x + 8, y + 9], fill=W, width=3)
    elif kind == "jersey":
        d.polygon([(x - 12, y - 10), (x - 5, y - 13), (x, y - 9), (x + 5, y - 13), (x + 12, y - 10),
                   (x + 9, y - 3), (x + 7, y - 4), (x + 7, y + 12), (x - 7, y + 12), (x - 7, y - 4), (x - 9, y - 3)],
                  fill=W, outline=O)
        _pixel_text(d, (x, y + 1), "23", O)
    elif kind == "tree":
        d.polygon([(x, y - 14), (x - 11, y + 4), (x + 11, y + 4)], fill=(60, 160, 60, 255), outline=O)
        d.rectangle([x - 2, y + 4, x + 2, y + 12], fill=(120, 80, 40, 255))
    elif kind == "crown":
        d.polygon([(x - 12, y + 8), (x - 12, y - 6), (x - 6, y + 1), (x, y - 10), (x + 6, y + 1), (x + 12, y - 6),
                   (x + 12, y + 8)], fill=GOLDEN, outline=O)
    elif kind == "rocket":
        d.polygon([(x, y - 15), (x + 6, y - 4), (x + 6, y + 8), (x - 6, y + 8), (x - 6, y - 4)], fill=W, outline=O)
        d.ellipse([x - 3, y - 6, x + 3, y], fill=(80, 160, 240, 255))
        d.polygon([(x - 6, y + 2), (x - 11, y + 11), (x - 6, y + 8)], fill=(230, 50, 50, 255))
        d.polygon([(x + 6, y + 2), (x + 11, y + 11), (x + 6, y + 8)], fill=(230, 50, 50, 255))
        d.polygon([(x - 4, y + 8), (x, y + 15), (x + 4, y + 8)], fill=GOLDEN)
    elif kind == "lvl":
        d.rectangle([x - 17, y - 9, x + 17, y + 9], fill=W, outline=O)
        _pixel_text(d, (x, y), "LVL", O)


def _pixel_text(d, centre, text, fill):
    """The sign pixel font at 2x on even pixels: the 2x halving brings it back to crisp 1:1 on the sprite."""
    import fxart
    m = fxart._text_mask(text)
    m = m.resize((m.width * 2, m.height * 2), Image.NEAREST)
    x, y = (round(centre[0] - m.width / 2) & ~1), (round(centre[1] - m.height / 2) & ~1)
    d._image.paste(fill, (x, y), m)


def _sack(bulge=0.0, open_=False, squash=1.0, base=BURLAP, emblem=None):
    """The sack on a 64x64 canvas (halved later): a lumpy bag, rope round the neck, a denim patch with white
    stitches. bulge pushes a homie-shaped lump out of one side."""
    body, dark, light = _shades(base)
    im = Image.new("RGBA", (64, 64))
    d = ImageDraw.Draw(im)
    cx, bot = 32, 60
    w, h = 23, int(34 * squash)
    top = bot - h
    d.ellipse([cx - w, top, cx + w, bot], fill=OUTLINE)
    d.ellipse([cx - w + 3, top + 3, cx + w - 3, bot - 3], fill=body)
    if bulge:                                                 # somebody's elbow in there
        bx = cx + int(18 * bulge)
        d.ellipse([bx - 11, top + 2, bx + 11, top + 24], fill=OUTLINE)
        d.ellipse([bx - 8, top + 5, bx + 8, top + 21], fill=body)
    d.ellipse([cx - w + 6, top + 8, cx - 4, bot - 10], fill=light)            # light from the upper left
    d.ellipse([cx + 2, top + 16, cx + w - 4, bot - 4], fill=dark)
    d.ellipse([cx - w + 8, top + 10, cx + w - 8, bot - 8], fill=body)
    for y in range(top + 8, bot - 4, 6):                      # weave
        d.line([cx - w + 8, y, cx + w - 8, y + 1], fill=dark, width=1)
    if emblem:                                                # what kind of sack it is, painted on the front
        _emblem(d, emblem, cx + 2, bot - 18, body)
    else:
        px, py = cx + 4, bot - 22                             # denim patch, stitched on
        d.rectangle([px - 1, py - 1, px + 13, py + 11], fill=OUTLINE)
        d.rectangle([px, py, px + 12, py + 10], fill=PATCH)
        for k in range(0, 13, 4):
            d.point([(px + k, py + 1), (px + k, py + 9)], fill=STITCH)
    if open_:                                                 # the mouth, wide open and dark
        d.ellipse([cx - 20, top - 12, cx + 20, top + 12], fill=OUTLINE)
        d.ellipse([cx - 17, top - 9, cx + 17, top + 9], fill=HOLE)
        d.arc([cx - 20, top - 12, cx + 20, top + 12], 20, 160, fill=ROPE, width=3)
    else:                                                     # neck gathered up and tied off with rope
        d.polygon([(cx - 9, top + 4), (cx + 9, top + 4), (cx + 13, top - 10), (cx - 13, top - 10)], fill=OUTLINE)
        d.polygon([(cx - 6, top + 3), (cx + 6, top + 3), (cx + 10, top - 8), (cx - 10, top - 8)], fill=dark)
        d.rectangle([cx - 10, top - 1, cx + 10, top + 4], fill=OUTLINE)
        d.rectangle([cx - 9, top, cx + 9, top + 3], fill=ROPE)
        d.line([cx - 9, top + 3, cx + 9, top + 3], fill=ROPE_D)
        d.line([cx + 9, top + 2, cx + 18, top + 10], fill=OUTLINE, width=4)        # loose rope end
        d.line([cx + 9, top + 2, cx + 18, top + 10], fill=ROPE, width=2)
        for k in range(-10, 11, 5):                           # the frilly top
            d.ellipse([cx + k - 3, top - 14, cx + k + 3, top - 7], fill=OUTLINE)
            d.ellipse([cx + k - 2, top - 13, cx + k + 2, top - 8], fill=body)
    return im


def _tube(bulge=0.0, open_=False, squash=1.0):
    """Pool Sack: a red-and-white pool ring with a rubber duck head, thrown like a lasso."""
    RED, WHITE, DUCK, BEAK = (220, 40, 40, 255), (245, 245, 245, 255), (250, 210, 40, 255), (240, 120, 30, 255)
    im = Image.new("RGBA", (64, 64))
    d = ImageDraw.Draw(im)
    h = int(30 * squash)
    top, bot = 56 - h, 56
    d.ellipse([4, top, 60, bot], fill=OUTLINE)
    for k in range(8):                                        # stripes
        d.pieslice([6, top + 2, 58, bot - 2], k * 45, k * 45 + 45, fill=RED if k % 2 else WHITE)
    hole = (18, top + h * .3, 46, bot - h * .3)
    d.ellipse(hole, fill=OUTLINE)
    d.ellipse([hole[0] + 2, hole[1] + 2, hole[2] - 2, hole[3] - 2], fill=HOLE if open_ else (0, 0, 0, 0))
    if bulge:                                                 # somebody stuck in the middle, kicking
        d.ellipse([22, top - 6, 42, top + 12], fill=OUTLINE)
        d.ellipse([25, top - 3, 39, top + 9], fill=(150, 100, 60, 255))
    d.ellipse([44, top - 14, 60, top + 2], fill=OUTLINE)      # the duck
    d.ellipse([46, top - 12, 58, top], fill=DUCK)
    d.polygon([(57, top - 7), (63, top - 5), (57, top - 3)], fill=BEAK)
    d.point([(53, top - 8)], fill=OUTLINE)
    d.rectangle([48, top, 54, top + 6], fill=DUCK)
    return im


def _handbag(bulge=0.0, open_=False, squash=1.0):
    """Drip Sack: a designer handbag - brown monogram canvas, gold clasp, leather handle."""
    TAN, TAN_D, GOLD_, MONO = (150, 100, 50, 255), (100, 64, 30, 255), (250, 200, 40, 255), (220, 180, 110, 255)
    im = Image.new("RGBA", (64, 64))
    d = ImageDraw.Draw(im)
    h = int(30 * squash)
    top, bot = 58 - h, 58
    d.arc([20, top - 18, 44, top + 8], 180, 360, fill=OUTLINE, width=6)                  # handle
    d.arc([20, top - 18, 44, top + 8], 180, 360, fill=TAN_D, width=3)
    d.polygon([(10, top), (54, top), (60, bot), (4, bot)], fill=OUTLINE)
    d.polygon([(12, top + 3), (52, top + 3), (57, bot - 3), (7, bot - 3)], fill=TAN)
    if bulge:
        d.ellipse([34, top - 8, 54, top + 12], fill=OUTLINE)
        d.ellipse([37, top - 5, 51, top + 9], fill=TAN)
    for yy in range(top + 8, bot - 4, 8):                     # monogram flowers
        for xx in range(12 + (yy // 8) % 2 * 5, 54, 10):
            _pixel_text(d, (xx, yy), "+", MONO)
    if open_:
        d.rectangle([12, top - 2, 52, top + 6], fill=OUTLINE)
        d.rectangle([14, top, 50, top + 4], fill=HOLE)
    else:
        d.rectangle([12, top + 3, 52, top + 9], fill=TAN_D)                                  # flap
        d.rectangle([28, top + 6, 36, top + 14], fill=GOLD_, outline=OUTLINE)                # clasp
    return im


# Kurt's apricorn balls are custom bags: row -> (material, base colour)
MATERIAL = {16: ("nylon", (40, 70, 180)), 17: ("gator", (90, 110, 50)), 18: ("croc", (40, 80, 60)),
            19: ("denim", (60, 90, 150)), 20: ("velvet", (130, 20, 70)), 21: ("suede", (170, 120, 70)),
            22: ("satin", (190, 190, 220))}


def _material(d, kind, box, base):
    """Fill box (x0, y0, x1, y1) with the material's texture."""
    x0, y0, x1, y1 = box
    body, dark, light = _shades(base)
    if kind == "nylon":                                       # tracksuit: white side stripes, a shine
        d.line([x0 + 4, y0, x0 + 4, y1], fill=(250, 250, 250, 255), width=3)
        d.line([x1 - 4, y0, x1 - 4, y1], fill=(250, 250, 250, 255), width=3)
        d.line([x0 + 12, y0 + 3, x1 - 14, y0 + 3], fill=light, width=2)
    elif kind in ("gator", "croc"):                           # scales / bumps
        step = 6 if kind == "gator" else 5
        for yy in range(y0 + 2, y1, step):
            for xx in range(x0 + 2 + (yy // step) % 2 * (step // 2), x1 - 1, step):
                if kind == "gator":
                    d.rectangle([xx, yy, xx + step - 2, yy + step - 2], outline=dark)
                else:
                    d.ellipse([xx, yy, xx + 2, yy + 2], fill=light)
    elif kind == "denim":                                     # orange stitching
        for yy in (y0 + 3, y1 - 3):
            for xx in range(x0 + 3, x1 - 3, 4):
                d.line([xx, yy, xx + 2, yy], fill=(240, 150, 40, 255))
        d.line([x0 + (x1 - x0) // 2, y0 + 3, x0 + (x1 - x0) // 2, y1 - 3], fill=dark)
    elif kind == "velvet":                                    # deep, soft sheen
        d.ellipse([x0 + 4, y0 + 2, x0 + (x1 - x0) // 2, y1 - 4], fill=light)
        d.ellipse([x0 + 7, y0 + 4, x0 + (x1 - x0) // 2 + 4, y1 - 2], fill=body)
    elif kind == "suede":                                     # matte, a few scuffs
        for xx, yy in ((x0 + 8, y0 + 6), (x0 + 20, y0 + 12), (x1 - 10, y0 + 5), (x1 - 16, y1 - 6)):
            d.line([xx, yy, xx + 3, yy + 1], fill=dark)
    elif kind == "satin":                                     # glossy diagonal highlight
        d.polygon([(x0 + 6, y1), (x0 + 16, y1), (x0 + 30, y0), (x0 + 20, y0)], fill=(250, 250, 255, 255))


def _clutch(bulge=0.0, open_=False, squash=1.0, material="suede", base=(170, 120, 70)):
    """A custom bag (Kurt's apricorn balls): a structured clutch with a fold-over flap and gold clasp, in its
    material."""
    body, dark, light = _shades(base)
    GOLD_ = (250, 200, 40, 255)
    im = Image.new("RGBA", (64, 64))
    d = ImageDraw.Draw(im)
    h = int(32 * squash)
    top, bot = 58 - h, 58
    d.rounded_rectangle([6, top, 58, bot], 6, fill=OUTLINE)
    d.rounded_rectangle([9, top + 3, 55, bot - 3], 4, fill=body)
    if bulge:                                                 # somebody's fist in there
        d.ellipse([34, top - 8, 54, top + 12], fill=OUTLINE)
        d.ellipse([37, top - 5, 51, top + 9], fill=body)
    _material(d, material, (9, top + 3, 55, bot - 3), base)
    if open_:                                                 # flap thrown back, wide open
        d.polygon([(6, top), (58, top), (50, top - 14), (14, top - 14)], fill=OUTLINE)
        d.polygon([(9, top), (55, top), (48, top - 11), (16, top - 11)], fill=dark)
        d.rectangle([10, top + 2, 54, top + 8], fill=HOLE)
    else:                                                     # the flap, the clasp
        d.polygon([(6, top), (58, top), (32, top + h // 2 + 2)], fill=OUTLINE)
        d.polygon([(9, top + 2), (55, top + 2), (32, top + h // 2 - 1)], fill=dark)
        d.ellipse([28, top + h // 2 - 5, 36, top + h // 2 + 3], fill=GOLD_, outline=OUTLINE)
    return im


def _duffel(bulge=0.0, open_=False, squash=1.0):
    """Duffel Bag: a black gym duffel with a red stripe, handles, and a zipper along the top."""
    BLACK, BLACK_L, RED, ZIP = (40, 40, 48, 255), (80, 80, 96, 255), (210, 40, 40, 255), (220, 220, 230, 255)
    im = Image.new("RGBA", (64, 64))
    d = ImageDraw.Draw(im)
    h = int(30 * squash)
    top, bot = 58 - h, 58
    d.arc([18, top - 16, 46, top + 10], 180, 360, fill=OUTLINE, width=6)                     # handles
    d.arc([18, top - 16, 46, top + 10], 180, 360, fill=BLACK_L, width=3)
    d.rounded_rectangle([4, top, 60, bot], 14, fill=OUTLINE)
    d.rounded_rectangle([7, top + 3, 57, bot - 3], 12, fill=BLACK)
    if bulge:                                                 # somebody's knee in there
        d.ellipse([34, top - 8, 56, top + 14], fill=OUTLINE)
        d.ellipse([37, top - 5, 53, top + 11], fill=BLACK)
    d.rectangle([7, top + h // 2 - 3, 57, top + h // 2 + 3], fill=RED)                     # stripe
    d.ellipse([4, top + 4, 14, bot - 4], fill=BLACK_L)                                    # end caps
    d.ellipse([50, top + 4, 60, bot - 4], fill=BLACK_L)
    if open_:
        d.ellipse([12, top - 4, 52, top + 10], fill=OUTLINE)
        d.ellipse([15, top - 1, 49, top + 7], fill=HOLE)
    else:
        d.line([12, top + 4, 52, top + 4], fill=ZIP, width=2)                             # zipper
        d.rectangle([48, top + 2, 52, top + 9], fill=ZIP)
    return im


def _rug(bulge=0.0, open_=False, squash=1.0):
    """Rug Roll: a rolled-up Persian rug, spiral end showing, gold pattern bands."""
    RED, RED_D, GOLD, CREAM = (170, 30, 40, 255), (110, 20, 28, 255), (230, 180, 60, 255), (240, 225, 190, 255)
    im = Image.new("RGBA", (64, 64))
    d = ImageDraw.Draw(im)
    if open_:                                                 # unrolled flat, waiting for somebody to step on it
        d.polygon([(4, 50), (60, 50), (52, 34), (12, 34)], fill=OUTLINE)
        d.polygon([(8, 48), (56, 48), (50, 36), (14, 36)], fill=RED)
        d.polygon([(16, 46), (48, 46), (44, 38), (20, 38)], outline=GOLD)
        for x in range(10, 56, 4):
            d.line([x, 50, x, 54], fill=CREAM)                # tassels
        d.ellipse([50, 22, 64, 36], fill=OUTLINE)             # the last of the roll
        d.ellipse([52, 24, 62, 34], fill=RED_D)
        return im
    h = int(24 * squash)
    top, bot = 46 - h // 2, 46 + h // 2
    d.rounded_rectangle([8, top, 58, bot], h // 2, fill=OUTLINE)
    d.rounded_rectangle([11, top + 3, 55, bot - 3], h // 2 - 3, fill=RED)
    if bulge:
        d.ellipse([26, top - 10, 46, top + 8], fill=OUTLINE)
        d.ellipse([29, top - 7, 43, top + 6], fill=RED)
    for x in (22, 34, 46):                                    # pattern bands
        d.line([x, top + 3, x, bot - 3], fill=GOLD, width=3)
    d.line([12, top + 5, 54, top + 5], fill=(210, 80, 80, 255), width=2)                 # shine
    d.ellipse([2, top, 2 + h, bot], fill=OUTLINE)             # the spiral end
    d.ellipse([5, top + 3, h - 1, bot - 3], fill=CREAM)
    c = (2 + h / 2, (top + bot) / 2)
    for r in range(3, h // 2 - 2, 3):
        d.arc([c[0] - r, c[1] - r, c[0] + r, c[1] + r], 0, 300, fill=RED_D)
    for y in (top + 2, bot - 4):                              # tassels poking out the far end
        d.line([56, y, 62, y + 2], fill=CREAM, width=2)
    return im


def _homie(bulge=0.0, open_=False, squash=1.0):
    """Whole Gang: a homie in a hoodie diving in flat out, arms first (open = arms flung wide, about to land)."""
    INK, RIM, SKIN, EYE = (34, 28, 48, 255), (150, 110, 230, 255), (150, 100, 60, 255), (255, 255, 255, 255)
    CHAIN, JEANS = (250, 200, 40, 255), (60, 70, 120, 255)
    im = Image.new("RGBA", (64, 64))
    d = ImageDraw.Draw(im)
    cy = 36 + int((1 - squash) * 20)
    d.rounded_rectangle([14, cy - 9, 50, cy + 9], 9, fill=OUTLINE)                     # body, horizontal
    d.rounded_rectangle([17, cy - 6, 47, cy + 6], 7, fill=INK)
    d.line([18, cy - 6, 46, cy - 6], fill=RIM, width=2)
    d.line([4, cy + 2, 16, cy + 6], fill=OUTLINE, width=8)                             # legs kicking back
    d.line([4, cy + 2, 16, cy + 6], fill=JEANS, width=5)
    d.ellipse([44, cy - 12, 62, cy + 6], fill=OUTLINE)                                 # hooded head
    d.ellipse([46, cy - 10, 60, cy + 4], fill=INK)
    d.ellipse([50, cy - 6, 59, cy + 2], fill=SKIN)
    d.point([(54, cy - 3), (57, cy - 3)], fill=EYE)
    d.line([40, cy + 4, 46, cy + 6], fill=CHAIN, width=2)
    if open_:                                                 # arms flung wide
        for s in (-1, 1):
            d.line([38, cy, 50, cy + s * 22], fill=OUTLINE, width=8)
            d.line([38, cy, 50, cy + s * 22], fill=INK, width=5)
            d.ellipse([47, cy + s * 22 - 4, 55, cy + s * 22 + 4], fill=SKIN, outline=OUTLINE)
    else:                                                     # arms out in front, superman
        d.line([40, cy - 4, 62, cy - 8], fill=OUTLINE, width=7)
        d.line([40, cy - 4, 61, cy - 8], fill=INK, width=4)
        d.ellipse([57, cy - 12, 64, cy - 5], fill=SKIN, outline=OUTLINE)
    if bulge:                                                 # somebody squirming under him
        d.ellipse([20, cy + 6, 40, cy + 18], fill=OUTLINE)
        d.ellipse([23, cy + 8, 37, cy + 16], fill=JEANS)
    return im


def frames(row=3):
    """The 10 cells for ball row `row`, 32x32 RGBA each."""
    draw = {0: _homie, 1: _rug, 2: _duffel, 6: _tube, 10: _handbag}.get(row)
    if row in MATERIAL:
        material, mbase = MATERIAL[row]

        def draw(**k):
            return _clutch(material=material, base=mbase, **k)
    if draw is None:
        base, emblem = TINT.get(row, BURLAP), EMBLEM.get(row)

        def draw(**k):
            return _sack(base=base, emblem=emblem, **k)

    def small(im, angle=0):
        if angle:
            im = im.rotate(angle, resample=Image.NEAREST, center=(32, 40))
        return im.resize((SIZE, SIZE), Image.NEAREST)
    closed = draw()
    out = [small(closed)] + [small(closed, -k * 45) for k in range(1, 8)]     # tumbling through the air
    out.append(small(draw(bulge=1.0, squash=.85)))                            # somebody in there fighting it
    out.append(small(draw(open_=True)))                                       # open: get in
    return _quantize(out)


def _quantize(imgs, n=15):
    """All frames down to one shared palette of n colours (+ transparent): the sprite has 16."""
    strip = Image.new("RGBA", (SIZE * len(imgs), SIZE))
    for k, im in enumerate(imgs):
        strip.paste(im, (SIZE * k, 0))
    rgb = Image.new("RGB", strip.size)
    rgb.paste(strip, mask=strip.split()[3])
    q = rgb.quantize(colors=n, method=Image.MEDIANCUT, dither=Image.NONE).convert("RGB")
    q.putalpha(strip.split()[3].point(lambda a: 255 if a >= 128 else 0))
    return [q.crop((SIZE * k, 0, SIZE * (k + 1), SIZE)) for k in range(len(imgs))]


def palette(imgs):
    cols = []
    for im in imgs:
        for c in im.getdata():
            if c[3] >= 128 and c[:3] not in cols:
                cols.append(c[:3])
    assert len(cols) <= 15, f"{len(cols)} colours: the ball sprite has a 16-colour palette"
    return cols


def _bgr555(c):
    r, g, b = c[:3]
    return (b >> 3) << 10 | (g >> 3) << 5 | r >> 3


def build(files, row=3):
    """{member: new data} for a/0/0/8: ball row `row`'s sprite."""
    CHAR, PLTT, CELL = 0x105 + 3 * row, 0x53 + row, 0x104 + 3 * row
    imgs = frames(LOOK.get(row, row))
    cols = palette(imgs)
    index = {c: i + 1 for i, c in enumerate(cols)}

    def tiles(im):                                            # 1D mapping: 16 tiles row by row
        out = bytearray()
        px = im.load()
        for ty in range(SIZE // 8):
            for tx in range(SIZE // 8):
                for y in range(8):
                    for x in range(0, 8, 2):
                        a, b = (px[tx * 8 + x + i, ty * 8 + y] for i in (0, 1))
                        lo = index[a[:3]] if a[3] >= 128 else 0
                        hi = index[b[:3]] if b[3] >= 128 else 0
                        out.append(lo | hi << 4)
        return out

    def unpack(i):
        f = files[i]
        return bytearray(ndspy.lz10.decompress(f) if f[0] == 0x10 else f)

    # character data (RGCN/RAHC): header sizes grow with the texels
    g = unpack(CHAR)
    texels = b"".join(tiles(im) for im in imgs)
    head = g[:0x30]
    struct.pack_into("<I", head, 0x10 + 0x18, len(texels))            # RAHC data size
    struct.pack_into("<I", head, 0x10 + 4, 0x20 + len(texels))        # RAHC block size
    g = head + texels
    struct.pack_into("<I", g, 8, len(g))                              # file size

    # palette (RLCN/TTLP): 16 colours, 0 transparent
    p = unpack(PLTT)
    pal = [_bgr555((56, 104, 152))] + [_bgr555(c) for c in cols]
    pal += [0] * (16 - len(pal))
    struct.pack_into("<16H", p, 0x10 + 0x18, *pal)

    # cells (RECN/KBEC): every cell one 32x32 OAM at (-16, -16); tile numbers in 64-byte units (1D 64K)
    c = unpack(CELL)
    ncell, attrtype, celloff = struct.unpack_from("<HHI", c, 0x18)
    rec = 16 if attrtype == 1 else 8
    base = 0x18 + celloff
    oams = base + ncell * rec
    assert ncell == len(imgs)
    for k in range(ncell):
        noam, attr, ooff = struct.unpack_from("<HHI", c, base + k * rec)
        assert noam == 1
        if attrtype == 1:                                     # bounding box: xmax ymax xmin ymin
            struct.pack_into("<hhhh", c, base + k * rec + 8, 15, 31 + LIFT, -16, LIFT)
        a0 = LIFT & 0xFF                                      # square, drawn LIFT px up (the art sits low)
        a1 = (2 << 14) | ((-16) & 0x1FF)                      # 32x32, x = -16
        a2 = (k * 16 * 32 // 64) & 0x3FF                      # palette 0
        struct.pack_into("<HHH", c, oams + ooff, a0, a1, a2)
    return {CHAR: ndspy.lz10.compress(bytes(g)), PLTT: bytes(p), CELL: ndspy.lz10.compress(bytes(c))}


# ------------------------------------------------------------------ particles (a/0/9/5)

GENERIC = 52                                                  # break-out, every ball: 2 emitters
TILE = 75
WHITE = 0x7FFF

# row -> (opening sign, click sign, send-out sign)
SIGNS = {0: (["GANG", "GANG!"], ["CLAIMED!"], ["WE", "OUTSIDE!"]),
         1: (["ROLL 'EM", "UP!"], ["WRAPPED!"], ["UNROLLED!"]),
         2: (["ZZZIP!"], ["PACKED!"], ["I'M", "OUT!"]),
         4: (["WELCOME", "TO THE", "ZOO!"], ["CAGED!"], ["ZOO'S", "OPEN!"]),
         5: (["IT'S A", "TRAP!"], ["TRAPPED!"], ["SPRUNG!"]),
         6: (["CANNON", "BALL!"], ["SPLASHED!"], ["MARCO!"]),
         7: (["COME", "CHILL"], ["MOVED IN!"], ["HOME", "SWEET", "HOME"]),
         8: (["RUN IT", "BACK!"], ["RE-UPPED!"], ["BACK", "AGAIN!"]),
         9: (["TAKE YOUR", "TIME"], ["FINALLY!"], ["SORRY", "I'M LATE"]),
         10: (["DRIPPED", "OUT!"], ["SO", "FRESH!"], ["STAY", "DRIPPY"]),
         11: (["VIP", "ONLY!"], ["ON THE", "LIST!"], ["I HAVE", "ARRIVED"]),
         12: (["LIGHTS", "OUT!"], ["GONE", "DARK!"], ["NIGHT", "SHIFT!"]),
         13: (["SIP", "SIP!"], ["PATCHED", "UP!"], ["FEELIN'", "GOOD!"]),
         14: (["TOO", "QUICK!"], ["GOT 'EM!"], ["ZOOM!"]),
         15: (["MY", "DAY 1!"], ["FOR", "LIFE!"], ["DAY", "ONE!"]),
         16: (["CAUGHT", "LACKIN'!"], ["SWISH!"], ["SKRRT!"]),
         17: (["BOSS", "MOVES!"], ["OUT-", "RANKED!"], ["LEVEL", "UP!"]),
         18: (["SNAP!"], ["CROC'D!"], ["SEE YA", "LATER!"]),
         19: (["HEAVY", "DUTY!"], ["OOF!"], ["LIGHT", "WORK!"]),
         20: (["COME", "HERE", "BAE"], ["WIFED", "UP!"], ["MISSED", "ME?"]),
         21: (["WE", "COOL?"], ["HOMIES", "4 LIFE"], ["WASSUP", "BRO!"]),
         22: (["SILKY", "SMOOTH"], ["MOON-", "LIT!"], ["SHINE", "ON!"]),
         23: (["GAME", "TIME!"], ["BENCHED!"], ["PUT ME", "IN!"]),
         24: (["PARK", "IT!"], ["PARKED!"], ["BACK", "OUTSIDE"])}
SACK_SIGNS = (["GET IN", "THE BAG!"], ["SNATCHED!"], ["I'M", "OUT!"])


def tables(rom):
    """Per ball row: (send-out file, its emitter count), (capture file, skipped emitter, emitter count), from the
    overlay-7 tables (found by their first rows)."""
    ov = rom.loadArm9Overlays([7])[7].data
    burst = ov.find(struct.pack("<9I", 0x1B, 0, 5, 0x1C, 2, 5, 0x1D, 1, 5))
    seal = ov.find(struct.pack("<6I", 1, 5, 2, 4, 3, 3))
    assert burst > 0 and seal > 0, "ball particle tables not found in overlay 7"
    return ([struct.unpack_from("<2I", ov, seal + 8 * i) for i in range(BALLS)],
            [struct.unpack_from("<3I", ov, burst + 12 * i) for i in range(BALLS)])


def _rgb(r, g, b):
    return (b >> 3) << 10 | (g >> 3) << 5 | r >> 3


def _prop(b, res, tex, scl=1.0, life=40, rise=.6, pop=1.2):
    """Emitter res as one particle (a sign, the dogpile): pops up big, settles, floats up a little; untinted;
    self-destructs."""
    import spa
    r = spa.resources(bytes(b))[res]
    edit = dict(gen=1, emtr_life=1, life=life, scl=scl, init_pos=0, clr=WHITE, axis=(0, 1, 0),
                vel=(0, rise * 355 / 4096), air_resist=118, tex=tex,
                flags_on=1 << 14, flags_off=(1 << 12) | (1 << 13) | (1 << 15) | 0x30)
    if "scl" in r:
        edit["scl_anm"] = (.2, pop, 1.0, 35, 255)
    if "clr" in r:
        edit["clr_anm"] = (WHITE, WHITE)
    if "alp" in r:
        edit["alpha"] = (31, 31, 31)
    if "grvt" in r:
        edit["gravity"] = (0, 0, 0)
    if "chld" in r:
        edit["child_gen"] = 0
    spa.edit(b, r, **edit)
    struct.pack_into("<hhH", b, r["off"] + 52, 0, 0, 0)       # upright, no spin
    if "spin" in r:
        struct.pack_into("<H", b, r["spin"], 0)
    if "cngc" in r:
        struct.pack_into("<h", b, r["cngc"] + 12, 0)
    b[r["off"] + TILE] &= 0xF0                                # the whole picture, not 4 mirrored quarters


def _dust(b, res):
    """The donor's sparkles, recoloured as dust and fibres."""
    import spa
    r = spa.resources(bytes(b))[res]
    edit = dict(clr=_rgb(190, 150, 95))
    if "clr" in r:
        edit["clr_anm"] = (_rgb(225, 195, 140), _rgb(120, 90, 55))
    if "chld" in r:
        edit["child_clr"] = _rgb(160, 120, 70)
    spa.edit(b, r, **edit)


def particles(files, seal_rows, burst_rows):
    """{member: new data} for a/0/9/5."""
    import fxart
    import spa

    def picture(data, im):
        texels, pal = fxart.to_a3i5(im, 32)
        return spa.add_texture(data, 1, 64, 64, texels, pal)

    def sign(data, lines):
        return picture(data, fxart.burst_sign(lines))

    def low_sign(data, lines):
        """A sign drawn in the bottom of its texture: it stays where the homie was while the gear (an OAM sprite,
        drawn over every particle) rises out of the way."""
        return picture(data, fxart.burst_sign(lines, cy=45.5 if len(lines) < 3 else 41.5, flat=.58))

    out = {}
    for row in range(BALLS):
        look = LOOK.get(row, row)
        opening, click, sendout = SIGNS.get(look, SACK_SIGNS)
        # send-out: the homie jumps out
        res, count = seal_rows[row]
        data, t = sign(files[res], sendout)
        b = bytearray(data)
        _prop(b, 0, t, scl=fxart.SIGN_SCALE, life=44, pop=1.0)
        for e in range(1, count):
            _dust(b, e)
        out[res] = bytes(b)
        # capture: it opens over them, then the click
        res, skip, count = burst_rows[row]
        used = [e for e in range(count) if e != skip]
        data, t_open = low_sign(files[res], opening)
        data, t_click = sign(data, click)
        extra = None
        if look == 0:                                         # the Whole Gang piles on
            data, extra = picture(data, fxart.dogpile())
        b = bytearray(data)
        _prop(b, used[0], t_open, scl=fxart.SIGN_SCALE, life=44, rise=-.5, pop=1.0)
        if skip < count:
            _prop(b, skip, t_click, scl=fxart.SIGN_SCALE, life=50, pop=1.0)
        rest = used[1:]
        if extra is not None:
            _prop(b, rest.pop(0), extra, scl=1.5, life=50, rise=0)
        for e in rest:
            _dust(b, e)
        out[res] = bytes(b)
    # break-out (every ball): they fight their way out
    data, t = picture(files[GENERIC], fxart.burst_sign(["NOT", "TODAY!"], fill=(255, 255, 255, 255),
                                                       text=(220, 30, 30, 255)))
    b = bytearray(data)
    _prop(b, 1, t, scl=fxart.SIGN_SCALE, life=44, pop=1.0)
    _dust(b, 0)
    out[GENERIC] = bytes(b)
    for k, v in out.items():
        assert all(r["flag"] >> 14 & 1 for r in spa.resources(v)), f"a/0/9/5 {k}: an emitter never finishes"
    return out


def patch(rom):
    seal_rows, burst_rows = tables(rom)
    narc = ndspy.narc.NARC(rom.getFileByName("a/0/0/8"))
    for row in range(BALLS):
        for i, data in build(narc.files, row).items():
            narc.files[i] = data
    rom.setFileByName("a/0/0/8", narc.save())
    narc = ndspy.narc.NARC(rom.getFileByName("a/0/9/5"))
    for i, data in particles(narc.files, seal_rows, burst_rows).items():
        narc.files[i] = data
    rom.setFileByName("a/0/9/5", narc.save())
    print(f"snatch gear: {BALLS} ball sprites + capture signs")


def preview(path):
    sheet = Image.new("RGBA", (10 * 36, BALLS * 36), (60, 90, 60, 255))
    for row in range(BALLS):
        for k, im in enumerate(frames(row)):
            sheet.alpha_composite(im, (k * 36 + 2, row * 36 + 2))
    sheet.resize((sheet.width * 2, sheet.height * 2), Image.NEAREST).save(path)


if __name__ == "__main__":
    import sys
    preview(sys.argv[1])
