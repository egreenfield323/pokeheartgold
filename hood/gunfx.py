"""Gunshot battle effects for Hood HeartGold: muzzle flashes at the gun, tracers, casings, smoke, crosshairs.

Three particle files are rebuilt from donors (a/0/2/9) with new textures and retuned emitters:
  GUN   (Pin Missile's):  SPARK spark burst, FLASH big muzzle flash, TRACER bullet streak (follows its emitter)
  KIT   (file 62):        CASING brass casings that fly out and fall, CROSS red crosshair that zooms in
  SMOKE (file 84):        PUFF gun smoke, DIRT dirt kicked up by bullets
build_files(narc_files) -> {donor id: new bytes}; variant(k, sounds) -> animation script words.
"""
import math
import struct

import fxart
import spa

GUN, KIT, SMOKE, CAR, BLING, CASH, ROCKET = 0, 1, 2, 3, 4, 5, 6  # particle system slots used by the scripts
BOTTLE, BRICK, EGG, FIRE, HOUSE, YOLK = 7, 8, 9, 10, 11, 12
HYDRANT, JET, SPLASH, SLUGGER, TASER, BOLTS, FOB, RINGS, SUB, CRACK = range(13, 23)
CHIPS, BURST, SHADES, BUBBLE, POCKET, SAND, FAN, WIND, GLINT = range(23, 32)
DONOR = {GUN: 73, KIT: 62, SMOKE: 84, CAR: 82, BLING: 168, CASH: 47, ROCKET: 349,
         BOTTLE: 349, BRICK: 349, EGG: 349, FIRE: 84, HOUSE: 168, YOLK: 84,
         HYDRANT: 349, JET: 84, SPLASH: 84, SLUGGER: 168, TASER: 349, BOLTS: 349, FOB: 349, RINGS: 62,
         SUB: 168, CRACK: 168,
         CHIPS: 82, BURST: 84, SHADES: 168, BUBBLE: 349, POCKET: 82, SAND: 84, FAN: 82, WIND: 84,
         GLINT: 349}
LOAD = dict(DONOR)                                            # particle file each kit loads (battlefx repoints)   # small files: the battle heap can't fit big ones twice
SPARK, FLASH, TRACER = 0, 1, 2
CASING, CROSS = 0, 1
PUFF, DIRT = 1, 0
RIDE, WINDOW = 2, 0                                           # CAR: the lowrider + its gun flashes (riding along)
PARKED, BOUNCE = 3, 1                                         # CAR: parked (stays), one hydraulics-bounce frame
STAND = 0                                                     # HYDRANT / TASER / FOB: the prop, standing there
JET_E, JET_P = 0, 1                                           # JET: water shot from the nozzle at the enemy / player
SWING_E, SWING_P = 0, 1                                       # SLUGGER: the bat swung by the player / the enemy
TASER_P = 1                                                   # TASER: the device pointing left (enemy holding it)
ZAP = 0                                                       # BOLTS: crackling lightning bolts
RING = 1                                                      # RINGS: a sound-wave ring blasting outward
BOX, PUMP = 0, 1                                              # SUB: the subwoofer, the cone pumping on a beat
SPLIT = 1                                                     # CRACK: the ground splitting open
BAG, CHIP_E, CHIP_P = 2, 0, 1                                 # CHIPS: the HOT chips bag, chips thrown each way
TONGUE, EMBER = 1, 0                                          # BURST: flames licking up, embers
SLIDE, LANDED = 0, 1                                          # SHADES: one pose of the slide down, the shades on
TING, SWEAT = 2, 1                                            # GLINT: a lens glint, sweat drops flying off
TALK, BANG = 0, 2                                             # BUBBLE: a cussing speech bubble (flown), a red "!"
SIGN, GRAIN_E, GRAIN_P = 2, 0, 1                              # POCKET: "POCKET SAND!", sand thrown each way
CLOUD = 1                                                     # SAND: the dust cloud
BODY, BLADES = 2, 0                                           # FAN: the box fan, its spinning blades
GUST_E, GUST_P = 0, 1                                         # WIND: gust lines blowing at the enemy / the player
FAN_AT = {"player": (-30, 22), "enemy": (30, 6)}            # the fan, behind the attacker (px from its origin)
TARGET_FROM_ATTACKER = {"player": (121, 59), "enemy": (-121, -59)}   # defender origin - attacker origin, px
GUST_AIM = (0, 10)                                            # where on the target the wind hits
GUST_FRAMES = 13


def aim_path(side, frm, aim):
    """(dx, dy) screen px from `frm` (px from the attacker) to `aim` (px from the target), y up."""
    (tx, ty) = TARGET_FROM_ATTACKER[side]
    return tx + aim[0] - frm[0], ty + aim[1] - frm[1]


def gust_path(side):
    """(dx, dy) screen px from the fan to the target (y up)."""
    return aim_path(side, FAN_AT[side], GUST_AIM)


BAG_AT = {"player": (26, 22), "enemy": (-26, 22)}           # the chip bag, in their hand
CHIP_AIM, CHIP_FRAMES = (0, 14), 12
HAND_AT = {"player": (16, 18), "enemy": (-16, 14)}          # where the sand comes out
SAND_AIM, SAND_FRAMES = (0, 24), 10                          # right in the face
SHADES_AT = {"player": (40, 50), "enemy": (-46, 20)}        # where the shades land (between them, up high)
SHADES_DROP = 32
FLY = 14                                                      # frames a flown set-3 piece takes to reach the target
BILLBOARD = 0x30                                              # flag bits 4-5: draw type (1 = stretched along its
#                                                               velocity - invisible on a piece riding its emitter)
JET_FRAMES, JET_G = 18, .012
HYDRANT_AT = {"player": (34, 6), "enemy": (-34, -4)}        # beside the attacker, towards the target
NOZZLE = {"player": (12, 1), "enemy": (-12, 1)}             # the open cap facing the target
JET_AIM = {"player": (74, 52), "enemy": (-68, -45)}         # nozzle -> target body, per attacker side
CAR_START, CAR_ROAD = -250, 2                                 # car spawn, pixels from the target (x, y up)
GUN_ON_CAR = (30, 23)                                         # the gun at the window, pixels from the car centre
CAR_LIFE = 90
PENDANT = 1                                                   # BLING: the chain + medallion (follows its emitter)
BILLS, STACK = 0, 1                                           # CASH: fluttering dollar bills, the bankroll
TO_ENEMY, TO_PLAYER = 0, 1                                    # ROCKET: an RPG round flying each way
# battler particle origins (sBattleAnimEmitterPositions, kind 0, perspective 0): player and enemy
ORIGIN = {"player": (-9616, -5464), "enemy": (11056, 4400)}
ROCKET_FRAMES = 18
THROWN = 1                                                    # BOTTLE/BRICK/EGG: the object, riding its emitter
THROW_PEAK = 30                                               # pixels the lob rises above the straight line
EMBERS, BLAZE = 0, 1                                          # FIRE: flames licking upward
HOME = 1                                                      # HOUSE: somebody's house
DRIP, SPLAT = 0, 1                                            # YOLK: egg splat + yolk dripping down
EMITTER_PIXEL = 172                                           # MoveEmitter's offset unit (BATTLE_ANIM_EMITTER_PIXEL)
THROW_FRAMES = 20
CAR_SPEED = 5                                                 # screen pixels per frame (at the enemy's depth)
TICK = 2                                                      # frames per script tick (scripts run at 30 Hz)
CAR_SCALE = 1.9                                               # 64px texture -> ~90px car on screen

# where the gun's muzzle sits relative to the battler's particle origin, in screen pixels (y up). Back
# sprites hold the gun on the right pointing right, front sprites mirror it (measured on Cyndaquil/Hoothoot).
MUZZLE = {"player": (31, 9), "enemy": (-30, 17)}
# particle units per screen pixel (x, y) at each battler's depth - measured in-game: the camera is a
# perspective one, so the far (enemy) side needs more units per pixel than the near (player) side
SCALE = {"near": (171, 167), "far": (169, 170)}             # (the particle camera is effectively flat)
VEL_UNITS = 355                                               # particle velocity units per screen pixel (measured)
PS_SCALE = {}

# the standard prelude every move script starts with (battler sprite copies, as in Spike Cannon)
PRELUDE = [56, 57, 0, 57, 1, 57, 2, 57, 3, 58, 4, 0, 0, 0, 58, 5, 0, 1, 1, 58, 6, 0, 2, 2, 58, 7, 0, 3, 3,
           45, 78, 1, 0]
PRELUDE_END = [1, 59, 60, 0, 60, 1, 60, 2, 60, 3]


def rgb(r, g, b):
    return (b >> 3) << 10 | (g >> 3) << 5 | r >> 3


BRASS, RED, SMOKE_GRAY, DIRT_BROWN = rgb(230, 180, 60), rgb(255, 0, 0), rgb(165, 165, 165), rgb(160, 110, 50)


# ------------------------------------------------------------------ textures

def _a5i3(w, h, alpha):
    """alpha(x, y) in 0..1 -> A5I3 texels using palette index 0 (white)."""
    return bytes((round(max(0.0, min(1.0, alpha(x, y))) * 31) << 3) for y in range(h) for x in range(w))


def _star_quarter(n, rays, width, core):
    """Quarter of a flash centred on the bottom-right corner (the hardware mirrors it into the full star).
    rays: (angle, length 0..1); width: half-width of a spike at its base, in radians."""
    c = n - 0.5

    def a(x, y):
        dx, dy = c - x, c - y
        r = math.hypot(dx, dy) / n
        ang = math.atan2(dy, dx)                               # 0..pi/2 inside the quarter
        v = 1.0 if r < core * .45 else max(0.0, 1 - (r - core * .45) / (core * .55)) ** .6   # solid hot core
        for t, L in rays:
            d = abs(ang - t)
            if r < L:                                          # spike tapers to a point at length L
                half = width * (1 - r / L)
                if d < half:
                    v = max(v, (1 - d / half) ** .35 * (1 - (r / L) ** 3))
        return v
    return a


def tex_spark(n=16):
    rays = [(0.0, 1.0), (math.pi / 2, 1.0), (math.pi / 4, .75)]
    return _a5i3(n, n, _star_quarter(n, rays, .42, .45))


def tex_flash(n=32):
    # long fat horizontal flame, shorter vertical + diagonal tongues, big hot core
    rays = [(0.0, 1.0), (math.pi / 2, .62), (math.pi / 4, .7), (math.pi / 7, .5), (5 * math.pi / 14, .45)]
    return _a5i3(n, n, _star_quarter(n, rays, .4, .5))


def tex_tracer(n=32):
    """A3I5 32x32: a hot streak along the attacker->target diagonal (symmetric, so it reads either way)."""
    d = (128, -64)                                             # screen direction player -> enemy
    L = math.hypot(*d)
    ux, uy = d[0] / L, d[1] / L
    out = bytearray()
    for y in range(n):
        for x in range(n):
            px, py = x - n / 2 + .5, y - n / 2 + .5
            along = px * ux + py * uy
            across = abs(-px * uy + py * ux)
            taper = max(0.0, 1 - abs(along) / 15)
            if across <= 1.1 * taper + .3 and taper > 0:
                idx, a = (1, 7) if across < .8 and taper > .3 else (2, 6)
            elif across <= 2.2 * taper + .3 and taper > 0:
                idx, a = 3, 4
            else:
                idx, a = 0, 0
            out.append(a << 5 | idx)
    return bytes(out)


TRACER_PAL = [0x0000, 0x7FFF, 0x5FFF, 0x03FF]                 # -, white, pale yellow, yellow (BGR555)


def tex_casing(n=16):
    """Quarter of a brass casing lying sideways (mirrored into a 2:1 capsule with a rim groove)."""
    c = n - 0.5

    def a(x, y):
        dx, dy = (c - x) / n, (c - y) / n
        if dx > .5 or dy > .24:
            return 0.0
        if dx > .38:                                           # rounded end
            return 1.0 if (dx - .38) ** 2 + (dy * 1.4) ** 2 < .12 ** 2 * 2.2 else 0.0
        return .65 if abs(dx - .3) < .04 else 1.0             # rim groove
    return _a5i3(n, n, a)


def tex_crosshair(n=32):
    """Quarter of a sniper reticle: ring, crosshair lines with a gap, centre dot, tick marks."""
    c = n - 0.5

    def a(x, y):
        dx, dy = c - x, c - y
        r = math.hypot(dx, dy)
        v = 0.0
        if abs(r - n * .72) < 1.1:
            v = 1.0                                            # ring
        if (dx < 1.0 or dy < 1.0) and n * .2 < r < n * .98:
            v = 1.0                                            # lines (gap at the centre)
        if r < 1.6:
            v = 1.0                                            # dot
        if abs(r - n * .45) < .7 and (dx < 3 or dy < 3):
            v = 1.0                                            # inner ticks
        return v
    return _a5i3(n, n, a)


def build_files(files):
    """{kit slot: rebuilt particle file} from the NARC member list (each keeps its donor's size)."""
    out = {}
    b = bytearray(files[DONOR[GUN]])
    spa.set_texture(b, 0, tex_spark())
    spa.set_texture(b, 1, tex_flash())
    spa.set_texture(b, 2, tex_tracer(), TRACER_PAL)
    out[GUN] = bytes(b)

    b = bytearray(files[DONOR[KIT]])
    rs = spa.resources(bytes(b))
    spa.set_texture(b, 0, tex_casing())
    spa.set_texture(b, 1, tex_crosshair())
    spa.edit(b, rs[CASING], clr=BRASS, clr_anm=(rgb(255, 230, 120), rgb(170, 120, 30)), gen=2, scl=.32,
             life=26, scl_anm=(1.0, 1.0, 1.0, 0, 255))
    spa.edit(b, rs[CROSS], clr=RED, clr_anm=(RED, rgb(255, 60, 60)), life=40, scl=1.25,
             scl_anm=(2.6, 1.0, 1.0, 110, 255))
    out[KIT] = bytes(b)

    b = bytearray(files[DONOR[SMOKE]])
    rs = spa.resources(bytes(b))
    # gun smoke: slow puffs that drift straight up, spread out, grow and fade (no trail)
    spa.edit(b, rs[PUFF], clr=SMOKE_GRAY, clr_anm=(rgb(225, 225, 225), rgb(120, 120, 128)), scl=.55,
             life=80, emtr_life=14, gen=1, gen_intvl=3, axis=(0, 1, 0), vel=(.006, .008), gravity=(0, .00006, 0),
             scl_anm=(.6, 1.6, 2.8, 50, 150), rndm=(90, 60, 160), air_resist=180, child_gen=0,
             child_clr=rgb(150, 150, 155))
    spa.edit(b, rs[DIRT], clr=DIRT_BROWN, clr_anm=(rgb(170, 120, 60), rgb(100, 70, 40)), scl=.45, emtr_life=3,
             child_clr=rgb(120, 85, 45))
    out[SMOKE] = bytes(b)

    b = bytearray(files[DONOR[CAR]])
    rs = spa.resources(bytes(b))
    texels, pal = fxart.to_a3i5(fxart.lowrider(), 32)
    spa.set_texture(b, 1, texels, pal)
    white = rgb(255, 255, 255)
    spa.edit(b, rs[RIDE], clr=white, clr_anm=(white, white), alpha=(31, 31, 31), scl=CAR_SCALE, flags_off=1 << 13,
             scl_anm=(1.0, 1.0, 1.0, 0, 255), gen=1, emtr_life=1, life=CAR_LIFE, axis=(1, 0, 0),
             vel=(0, CAR_SPEED * VEL_UNITS / 4096), air_resist=128)
    for res, life in ((PARKED, 80), (BOUNCE, 4)):              # the same lowrider, parked
        spa.edit(b, rs[res], clr=white, clr_anm=(white, white), alpha=(31, 31, 31), scl=CAR_SCALE, gen=1,
                 emtr_life=1, life=life, vel=(0, 0), init_pos=0, scl_anm=(1.0, 1.0, 1.0, 0, 255),
                 flags_on=1 << 14, flags_off=(1 << 13) | (1 << 15))
    # window flashes: born with the car, same speed, hidden until the gun reaches the target, then strobing
    spa.set_texture(b, 0, tex_spark())
    life = int((-CAR_START - GUN_ON_CAR[0] + 60) / CAR_SPEED)  # gone once the gun is 60px past them
    gold = rgb(255, 230, 90)
    spa.edit(b, rs[WINDOW], clr=gold, clr_anm=(rgb(255, 255, 220), gold), scl=.9, gen=1, emtr_life=1, life=life,
             axis=(1, 0, 0), vel=(0, CAR_SPEED * VEL_UNITS / 4096), air_resist=128, init_pos=0,
             gravity=(0, 0, 0), scl_anm=(1.0, 1.0, 1.0, 0, 255), alpha=(31, 31, 31), flick=140,
             flags_off=1 << 13)                                 # strobing the whole way in
    out[CAR] = bytes(b)

    b = bytearray(files[DONOR[BLING]])
    rs = spa.resources(bytes(b))
    texels, pal = fxart.to_a3i5(fxart.chain(), 30)
    spa.set_texture(b, 0, texels, pal)
    spa.edit(b, rs[PENDANT], clr=white, scl=1.5, gen=1, emtr_life=1, life=SWING_STEP, vel=(0, 0), init_pos=0,
             scl_anm=(1.0, 1.0, 1.0, 0, 255), alpha=(31, 31, 31), flags_off=1 << 13)
    struct.pack_into("<h", b, rs[PENDANT]["cngc"] + 12, 0)    # no pull towards a point
    out[BLING] = bytes(b)

    b = bytearray(files[DONOR[CASH]])
    rs = spa.resources(bytes(b))
    texels, pal = fxart.to_a3i5(fxart.bill(), 4)
    spa.set_texture(b, 0, texels, pal)
    texels, pal = fxart.to_a3i5(fxart.cash_stack(), 10)
    spa.set_texture(b, 1, texels, pal)
    spa.edit(b, rs[BILLS], clr=white, clr_anm=(white, white), scl=.42, gen=1, emtr_life=26, life=70,
             vel=(.025, -.02), gravity=(0, -.0032, 0), air_resist=124, alpha=(31, 31, 31), radius=2.8,
             scl_anm=(1.0, 1.0, 1.0, 0, 255), rndm=(60, 80, 120))
    spa.edit(b, rs[STACK], clr=white, clr_anm=(white, white), scl=1.3, gen=1, emtr_life=1, life=34,
             vel=(0, 0), init_pos=0, alpha=(31, 31, 20), scl_anm=(.6, 1.0, 1.0, 40, 255),
             flags_off=(1 << 12) | (1 << 13))                   # no rotation: held up straight
    struct.pack_into("<H", b, rs[STACK]["spin"], 0)            # held up, not spinning
    out[CASH] = bytes(b)

    b = bytearray(files[DONOR[ROCKET]])
    rs = spa.resources(bytes(b))
    texels, pal = fxart.to_a3i5(fxart.rocket(), 24)
    spa.set_texture(b, 1, texels, pal)
    (px, py), (ex, ey) = ORIGIN["player"], ORIGIN["enemy"]
    dist = math.hypot(ex - px, ey - py)
    ax, ay = (ex - px) / dist, (ey - py) / dist
    speed = dist / ROCKET_FRAMES / 4096
    for res, sign, rtt in ((TO_ENEMY, 1, 0), (TO_PLAYER, -1, 0x8000)):
        spa.edit(b, rs[res], gen=1, emtr_life=1, life=ROCKET_FRAMES, scl=1.1, init_pos=0, vel=(0, speed),
                 axis=(sign * ax, sign * ay, 0), air_resist=128, alpha=(31, 31, 31),
                 scl_anm=(1.0, 1.0, 1.0, 0, 255), flags_off=(1 << 15) | (1 << 13) | (1 << 12),
                 flags_on=1 << 14)                              # self-destruct, or the script waits forever
        struct.pack_into("<H", b, rs[res]["off"] + 56, rtt)     # fixed rotation: nose towards the target
        if "grvt" in rs[res]:
            spa.edit(b, rs[res], gravity=(0, 0, 0))
    out[ROCKET] = bytes(b)

    # thrown objects: one copy of the rocket file each, the object riding (and spinning on) its emitter
    for ps, art, spin, size in ((BOTTLE, fxart.molotov(), 0x0A00, .9), (BRICK, fxart.brick(), 0x0C00, .9),
                                (EGG, fxart.egg(), 0x0500, .55)):
        b = bytearray(files[DONOR[ps]])
        rs = spa.resources(bytes(b))
        texels, pal = fxart.to_a3i5(art, 24)
        spa.set_texture(b, 1, texels, pal)
        # the arc: MoveEmitter flies the emitter straight at the target while the object (following it) is
        # thrown upward under gravity, landing back on the line as the flight ends (MoveEmitterArc crashes)
        h = THROW_PEAK * VEL_UNITS / 4096                       # particle-local motion: velocity units
        g = 8 * h / THROW_FRAMES ** 2
        # NOT self-destructing: MoveEmitter owns the emitter and deletes it when the flight ends - if SPL freed it
        # first the task would write to freed memory (that froze the game)
        spa.edit(b, rs[THROWN], gen=1, emtr_life=1, life=THROW_FRAMES + 2, scl=size, init_pos=0, axis=(0, 1, 0),
                 clr=white,                                      # untinted: the art's own colours
                 vel=(0, g * THROW_FRAMES / 2), gravity=(0, -g, 0), air_resist=128, alpha=(31, 31, 31),
                 scl_anm=(1.0, 1.0, 1.0, 0, 255), tex=1,
                 flags_on=(1 << 15) | (1 << 12), flags_off=(1 << 13) | (1 << 14))
        struct.pack_into("<hhH", b, rs[THROWN]["off"] + 52, spin, spin, 0)   # tumbling
        out[ps] = bytes(b)
    # fire: short tongues of flame rising straight up (the donor's blast goes sideways), embers floating up
    b = bytearray(files[DONOR[FIRE]])
    rs = spa.resources(bytes(b))
    spa.edit(b, rs[BLAZE], axis=(0, 1, 0), vel=(.004, .018), gravity=(0, .0009, 0), life=18, emtr_life=8, gen=1,
             gen_intvl=2, scl=.55, scl_anm=(.6, 1.15, .25, 60, 150), child_gen=0, rndm=(70, 60, 120),
             air_resist=124, flags_off=1 << 13)
    spa.edit(b, rs[EMBERS], axis=(0, 1, 0), vel=(.012, .026), gravity=(0, .0005, 0), life=16, emtr_life=8,
             scl=.3, rndm=(60, 60, 160), air_resist=124)
    out[FIRE] = bytes(b)

    # the house that gets egged: pops up and stays for the whole bit
    b = bytearray(files[DONOR[HOUSE]])
    rs = spa.resources(bytes(b))
    texels, pal = fxart.to_a3i5(fxart.house(), 30)
    spa.set_texture(b, 0, texels, pal)
    spa.edit(b, rs[HOME], clr=white, scl=1.0, gen=1, emtr_life=1, life=170, vel=(0, 0), init_pos=0,
             scl_anm=(.3, 1.08, 1.0, 25, 255), alpha=(31, 31, 31), flags_off=(1 << 13) | (1 << 15))
    struct.pack_into("<h", b, rs[HOME]["cngc"] + 12, 0)
    out[HOUSE] = bytes(b)

    # yolk: a yellow splat that sags, drops running down
    b = bytearray(files[DONOR[YOLK]])
    rs = spa.resources(bytes(b))
    yellow, pale = rgb(255, 214, 40), rgb(255, 246, 190)
    spa.edit(b, rs[SPLAT], clr=yellow, clr_anm=(pale, yellow), scl=.45, life=40, emtr_life=2, gen=1,
             axis=(0, 1, 0), vel=(.004, 0), gravity=(0, -.00025, 0), scl_anm=(.4, 1.2, 1.0, 30, 200),
             child_gen=0, child_clr=yellow, air_resist=110)
    spa.edit(b, rs[DRIP], clr=yellow, clr_anm=(pale, yellow), scl=.22, life=36, emtr_life=6, gen=1,
             vel=(.004, -.004), gravity=(0, -.0007, 0), child_clr=yellow, air_resist=120)
    out[YOLK] = bytes(b)

    def single(ps, art, colors, res, **edit):
        """A copy of the donor with `art` as its colour texture and emitter `res` edited as a single prop."""
        bb = bytearray(files[DONOR[ps]])
        rr = spa.resources(bytes(bb))
        tex = rr[res]["tex"]
        colors = min(colors, spa.textures(bytes(bb))[tex][6] // 2)  # the slot's palette size (more = garbage)
        texels, pal = fxart.to_a3i5(art, colors)
        spa.set_texture(bb, tex, texels, pal)
        base = dict(gen=1, emtr_life=1, vel=(0, 0), init_pos=0, clr=white, air_resist=128, alpha=(31, 31, 31),
                    scl_anm=(1.0, 1.0, 1.0, 0, 255), flags_on=1 << 14, flags_off=(1 << 12) | (1 << 13) | (1 << 15))
        if "clr" in rr[res]:
            base["clr_anm"] = (white, white)                    # the art's own colours, no tint cycling
        base.update(edit)
        spa.edit(bb, rr[res], **base)
        if not base["flags_on"] & (1 << 12):                    # no rotation unless asked (the donor spins)
            struct.pack_into("<hhH", bb, rr[res]["off"] + 52, 0, 0, 0)
        if "cngc" in rr[res]:
            struct.pack_into("<h", bb, rr[res]["cngc"] + 12, 0)
        if "spin" in rr[res]:
            struct.pack_into("<H", bb, rr[res]["spin"], 0)
        return bb, rr

    # Hose Down: a big hydrant, and water shot out of its nozzle on a ballistic arc (velocity + gravity)
    b, rs = single(HYDRANT, fxart.hydrant(), 24, STAND, scl=1.25, life=75)
    out[HYDRANT] = bytes(b)
    b = bytearray(files[DONOR[JET]])
    rs = spa.resources(bytes(b))
    blue, foam = rgb(70, 140, 255), rgb(230, 245, 255)
    for res, (dx, dy) in ((JET_E, JET_AIM["player"]), (JET_P, JET_AIM["enemy"])):
        vx = dx * VEL_UNITS / 4096 / JET_FRAMES
        vy = dy * VEL_UNITS / 4096 / JET_FRAMES + JET_G * JET_FRAMES / 2
        sp = math.hypot(vx, vy)
        spa.edit(b, rs[res], clr=blue, clr_anm=(foam, blue), scl=.3, life=JET_FRAMES + 2, emtr_life=24, gen=2,
                 gen_intvl=1, init_pos=0, axis=(vx / sp, vy / sp, 0), vel=(.006, sp), gravity=(0, -JET_G, 0),
                 air_resist=128, rndm=(60, 20, 40), child_gen=0, flags_off=1 << 13)
    out[JET] = bytes(b)
    b = bytearray(files[DONOR[SPLASH]])
    rs = spa.resources(bytes(b))
    spa.edit(b, rs[1], clr=foam, clr_anm=(foam, blue), scl=.5, life=24, emtr_life=8, gen=1, child_gen=0,
             vel=(.02, .01), gravity=(0, -.0008, 0))
    spa.edit(b, rs[0], clr=blue, clr_anm=(foam, blue), scl=.25, life=22, emtr_life=8, gen=2,
             vel=(.03, .02), gravity=(0, -.0016, 0))
    out[SPLASH] = bytes(b)

    # Bat Swing: the bat's handle is the texture's centre, so the particle's rotation swings it from the hands
    b, rs = single(SLUGGER, fxart.bat_swing(), 30, SWING_E, scl=1.6, life=10, flags_on=(1 << 14) | (1 << 12))
    spa.edit(b, rs[SWING_P], gen=1, emtr_life=1, vel=(0, 0), init_pos=0, clr=white, air_resist=128,
             alpha=(31, 31, 31), scl_anm=(1.0, 1.0, 1.0, 0, 255), scl=1.6, life=10,
             flags_on=(1 << 14) | (1 << 12), flags_off=(1 << 13) | (1 << 15))
    struct.pack_into("<h", b, rs[SWING_P]["cngc"] + 12, 0)
    struct.pack_into("<hhH", b, rs[SWING_E]["off"] + 52, -0x0E00, -0x0E00, 0x5000)   # raised behind -> down-forward
    struct.pack_into("<hhH", b, rs[SWING_P]["off"] + 52, 0x0E00, 0x0E00, 0x3000)     # mirrored for the enemy
    out[SLUGGER] = bytes(b)

    # Taser: the device (pointing right; the enemy's copy turned round) and crackling bolts round the target
    b, rs = single(TASER, fxart.taser(), 24, STAND, scl=1.2, life=60)
    spa.edit(b, rs[TASER_P], gen=1, emtr_life=1, vel=(0, 0), init_pos=0, clr=white, air_resist=128,
             alpha=(31, 31, 31), scl_anm=(1.0, 1.0, 1.0, 0, 255), scl=1.2, life=60, gravity=(0, 0, 0),
             flags_on=1 << 14, flags_off=(1 << 13) | (1 << 15))
    struct.pack_into("<H", b, rs[TASER_P]["off"] + 56, 0x8000)
    out[TASER] = bytes(b)
    b, rs = single(BOLTS, fxart.bolt(), 24, ZAP, scl=1.1, life=3, emtr_life=26, gen=2, init_pos=1, radius=.9,
                   flags_on=(1 << 14) | (1 << 13))
    out[BOLTS] = bytes(b)

    # Panic button: a key fob, and sound-wave rings that blast out and fade
    b, rs = single(FOB, fxart.keyfob(), 24, STAND, scl=1.3, life=60)
    out[FOB] = bytes(b)
    b = bytearray(files[DONOR[RINGS]])
    rs = spa.resources(bytes(b))
    spa.set_texture(b, rs[RING]["tex"], fxart.ring_quarter())
    red = rgb(255, 50, 50)
    spa.edit(b, rs[RING], clr=red, clr_anm=(rgb(255, 255, 255), red), scl=1.0, life=18, emtr_life=1, gen=1,
             scl_anm=(.3, 1.6, 2.8, 120, 200), alpha=(31, 28, 0), vel=(0, 0), init_pos=0, flags_off=1 << 13)
    out[RINGS] = bytes(b)

    # Bass Drop: a subwoofer box (and its cone pumping on each hit), the ground cracking open
    b, rs = single(SUB, fxart.speaker(), 30, BOX, scl=1.25, life=110)
    spa.edit(b, rs[PUMP], gen=1, emtr_life=1, vel=(0, 0), init_pos=0, clr=white, air_resist=128,
             alpha=(31, 31, 31), scl_anm=(1.0, 1.22, 1.0, 60, 140), scl=1.25, life=6,
             flags_on=1 << 14, flags_off=(1 << 13) | (1 << 15))
    struct.pack_into("<h", b, rs[PUMP]["cngc"] + 12, 0)
    out[SUB] = bytes(b)
    b, rs = single(CRACK, fxart.ground_crack(), 12, SPLIT, scl=1.7, life=100, scl_anm=(.2, 1.0, 1.0, 70, 255))
    out[CRACK] = bytes(b)
    # ---- set 3 -------------------------------------------------------------------------------------------
    # Hot Shot: a big bag of HOT chips, ripped open; fistfuls of chips thrown in their face (static emitters on
    # the bag shooting tumbling chips at the target, one per direction)
    orange, yellow, red = rgb(255, 140, 30), rgb(255, 235, 120), rgb(220, 40, 20)

    def spray(b, rs, res, side, frm, aim, frames, **edit):
        """Emitter res shoots its particles from `frm` (px from the attacker) at `aim` (px from the target)."""
        dx, dy = aim_path(side, frm, aim)
        d = math.hypot(dx, dy)
        args = dict(axis=(dx / d, dy / d, 0), life=frames + 2, init_pos=1, air_resist=128,
                    flags_on=1 << 14, flags_off=(1 << 15) | BILLBOARD)
        if "chld" in rs[res]:
            args["child_gen"] = 0
        args.update(edit)
        if "grvt" not in rs[res]:
            args.pop("gravity", None)                        # (this emitter has no gravity block)
        args["vel"] = (args.pop("spread", 0), d * VEL_UNITS / 4096 / frames)
        spa.edit(b, rs[res], **args)
        if "grvt" in rs[res] and "gravity" not in edit:
            spa.edit(b, rs[res], gravity=(0, 0, 0))
        if "cngc" in rs[res]:
            struct.pack_into("<h", b, rs[res]["cngc"] + 12, 0)

    b, rs = single(CHIPS, fxart.chip_bag(), 32, BAG, scl=1.25, life=60, scl_anm=(.3, 1.12, 1.0, 30, 255))
    spa.set_texture(b, 0, fxart.chip())
    for res, sd in ((CHIP_E, "player"), (CHIP_P, "enemy")):
        spray(b, rs, res, sd, BAG_AT[sd], CHIP_AIM, CHIP_FRAMES, tex=0, clr=rgb(255, 100, 30),
              clr_anm=(rgb(255, 170, 60), rgb(230, 40, 20)), scl=.55, emtr_life=5, gen=2, gen_intvl=1, radius=.25,
              spread=.008, alpha=(31, 31, 31), scl_anm=(1.0, 1.0, 1.0, 0, 255), flick=0,
              flags_on=(1 << 14) | (1 << 12) | (1 << 13))
        struct.pack_into("<hhH", b, rs[res]["off"] + 52, -0x1400, 0x1400, 0)       # tumbling
    spa.edit(b, rs[3], flags_on=1 << 14)                     # the car's last emitter: unused
    out[CHIPS] = bytes(b)
    # the hit: tongues of flame shooting up (a new flame shape), embers popping out
    b = bytearray(files[DONOR[BURST]])
    rs = spa.resources(bytes(b))
    spa.set_texture(b, 1, fxart.flame_tongue())
    spa.set_texture(b, 0, fxart.speck())
    spa.edit(b, rs[TONGUE], clr=orange, clr_anm=(yellow, red), scl=.6, life=16, emtr_life=10, gen=1, gen_intvl=1,
             axis=(0, 1, 0), vel=(.008, .014), gravity=(0, .0006, 0), radius=.8, init_pos=1, air_resist=126,
             alpha=(31, 31, 0), scl_anm=(.4, 1.1, .6, 50, 160), rndm=(80, 40, 100), child_gen=0,
             flags_off=1 << 13)
    spa.edit(b, rs[EMBER], tex=0, clr=yellow, clr_anm=(rgb(255, 255, 200), orange), scl=.25, life=20,
             emtr_life=4, gen=3, axis=(0, 1, 0), vel=(.03, .02), gravity=(0, -.0015, 0), air_resist=122,
             alpha=(31, 31, 0), scl_anm=(1.0, 1.0, .5, 0, 160), child_gen=0, flags_off=BILLBOARD)
    out[BURST] = bytes(b)

    # Mean Mug (Leer): "deal with it" shades sliding down slow (velocity with air resistance: they ease to a
    # stop), a glint off the lens, sweat drops flying off the target
    # (stop-motion: air resistance doesn't brake a particle to a stop, so the slide is a pose per step)
    b, rs = single(SHADES, fxart.deal_shades(), 30, SLIDE, scl=2.0, life=SWING_STEP)
    spa.edit(b, rs[LANDED], gen=1, emtr_life=1, life=54, vel=(0, 0), init_pos=0, clr=white, air_resist=128,
             alpha=(31, 31, 31), scl=2.0, scl_anm=(1.0, 1.0, 1.0, 0, 255), flags_on=1 << 14,
             flags_off=(1 << 12) | (1 << 13) | (1 << 15))
    struct.pack_into("<hhH", b, rs[LANDED]["off"] + 52, 0, 0, 0)
    for k in ("cngc", "spin"):
        if k in rs[LANDED]:
            struct.pack_into("<h" if k == "cngc" else "<H", b, rs[LANDED][k] + (12 if k == "cngc" else 0), 0)
    out[SHADES] = bytes(b)
    b, rs = single(GLINT, fxart.sweat_drop(), 24, SWEAT, scl=.5, life=24, emtr_life=3, gen=2, init_pos=1, radius=.5,
                   axis=(0, 1, 0), vel=(.02, .02), air_resist=124, flags_off=(1 << 12) | (1 << 15) | BILLBOARD)
    spa.edit(b, rs[SWEAT], gravity=(0, -.0018, 0), alpha=(31, 31, 0))
    spa.set_texture(b, rs[TING]["tex"], fxart.glint())
    spa.edit(b, rs[TING], clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(255, 250, 200)), scl=.7, life=12,
             emtr_life=1, gen=1, vel=(0, 0), init_pos=0, air_resist=128, alpha=(31, 31, 0),
             scl_anm=(.2, 1.4, .3, 60, 160), child_gen=0, flags_on=(1 << 14) | (1 << 12),
             flags_off=(1 << 13) | (1 << 15) | BILLBOARD)
    struct.pack_into("<hhH", b, rs[TING]["off"] + 52, 0x0800, 0x0800, 0)            # a little twinkle spin
    out[GLINT] = bytes(b)

    # Talk Trash: cussing speech bubbles flown at the target, a red "!" popping over them
    b, rs = single(BUBBLE, fxart.speech_bubble(), 8, TALK, scl=.85, life=FLY + 2,
                   flags_on=1 << 15, flags_off=(1 << 12) | (1 << 13) | (1 << 14))
    spa.set_texture(b, rs[BANG]["tex"], fxart.bang())
    spa.edit(b, rs[BANG], clr=rgb(235, 30, 30), scl=.55, life=14, emtr_life=1, gen=1, vel=(0, 0), init_pos=0,
             air_resist=128, alpha=(31, 31, 0), scl_anm=(.3, 1.3, 1.0, 40, 255), child_gen=0,
             flags_on=1 << 14, flags_off=(1 << 12) | (1 << 13) | (1 << 15))
    struct.pack_into("<hhH", b, rs[BANG]["off"] + 52, 0, 0, 0)
    out[BUBBLE] = bytes(b)

    # Pocket Sand: "POCKET SAND!" bursts out over them, a cone of sand blasted into the target's face, a dust cloud
    b, rs = single(POCKET, fxart.pocket_sand_sign(), 32, SIGN, scl=1.35, life=44, scl_anm=(.2, 1.2, 1.0, 30, 255))
    tan, pale = rgb(225, 195, 130), rgb(250, 235, 195)
    spa.set_texture(b, 0, fxart.speck())
    for res, sd in ((GRAIN_E, "player"), (GRAIN_P, "enemy")):
        spray(b, rs, res, sd, HAND_AT[sd], SAND_AIM, SAND_FRAMES, tex=0, clr=rgb(205, 165, 95),
              clr_anm=(rgb(235, 205, 140), rgb(170, 125, 65)), scl=.55, emtr_life=6, gen=8, gen_intvl=1, radius=.2, spread=.022, alpha=(31, 31, 20),
              scl_anm=(.8, 1.0, 1.3, 0, 200), flick=0, gravity=(0, -.0006, 0))
    spa.edit(b, rs[3], flags_on=1 << 14)                     # the car's last emitter: unused
    out[POCKET] = bytes(b)
    b = bytearray(files[DONOR[SAND]])
    rs = spa.resources(bytes(b))
    spa.set_texture(b, 1, fxart.dust_cloud())
    spa.edit(b, rs[CLOUD], tex=1, clr=tan, clr_anm=(pale, tan), scl=.8, life=40, emtr_life=8, gen=1,
             gen_intvl=2, axis=(0, 1, 0), vel=(.012, .004), gravity=(0, .0002, 0), radius=.7, init_pos=1,
             air_resist=118, alpha=(31, 26, 0), scl_anm=(.5, 1.3, 1.8, 40, 150), rndm=(90, 60, 120),
             child_gen=0, flags_off=1 << 13)
    spa.edit(b, rs[0], flags_on=1 << 14)                     # unused
    out[SAND] = bytes(b)

    # Fan Blast: the box fan, its blades (a separate particle spinning on the grill), gust lines flown at them
    b, rs = single(FAN, fxart.box_fan(), 24, BODY, scl=1.15, life=96, scl_anm=(.3, 1.05, 1.0, 30, 255))
    spa.set_texture(b, rs[BLADES]["tex"], fxart.fan_blades())
    steel = rgb(175, 195, 220)
    spa.edit(b, rs[BLADES], clr=steel, clr_anm=(steel, steel), gravity=(0, 0, 0), scl=.78, flick=0, life=96, emtr_life=1, gen=1, vel=(0, 0), init_pos=0,
             air_resist=128, alpha=(31, 31, 31), scl_anm=(.3, 1.05, 1.0, 30, 255),
             flags_on=(1 << 14) | (1 << 12), flags_off=(1 << 13) | (1 << 15) | BILLBOARD)
    struct.pack_into("<hhH", b, rs[BLADES]["off"] + 52, 0x1C00, 0x1C00, 0)        # whirring
    for res in (1, 3):                                       # the car's other emitters: unused, kept harmless
        spa.edit(b, rs[res], flags_on=1 << 14)
    out[FAN] = bytes(b)
    # gusts: static emitters ON the fan, shooting wind lines at the target (MoveEmitter can only start a flight
    # at the attacker's centre, so flown lines came out of the attacker instead of the fan)
    b = bytearray(files[DONOR[WIND]])
    rs = spa.resources(bytes(b))
    paths = {sd: gust_path(sd) for sd in ("player", "enemy")}
    tilt = -sum(math.degrees(math.atan2(abs(dy), abs(dx))) for dx, dy in paths.values()) / 2
    spa.set_texture(b, 0, fxart.wind_streak(angle=tilt))   # one texture: the line is the same both ways
    for res, sd in ((GUST_E, "player"), (GUST_P, "enemy")):
        dx, dy = paths[sd]
        d = math.hypot(dx, dy)
        speed = d * VEL_UNITS / 4096 / GUST_FRAMES
        spa.edit(b, rs[res], tex=0, clr=rgb(235, 245, 255), clr_anm=(rgb(255, 255, 255), rgb(190, 215, 240)),
                 scl=.95, life=GUST_FRAMES + 1, emtr_life=7, gen=1, gen_intvl=2, axis=(dx / d, dy / d, 0),
                 vel=(0, speed), init_pos=1, radius=.45, air_resist=128, alpha=(31, 28, 0),
                 scl_anm=(1.0, 1.0, 1.0, 0, 255), rndm=(0, 0, 0), child_gen=0, gravity=(0, 0, 0),
                 flags_on=1 << 14, flags_off=(1 << 12) | (1 << 13) | (1 << 15) | BILLBOARD)
        struct.pack_into("<hhH", b, rs[res]["off"] + 52, 0, 0, 0)
        if "cngc" in rs[res]:
            struct.pack_into("<h", b, rs[res]["cngc"] + 12, 0)  # no pull towards a point
    out[WIND] = bytes(b)

    # (TRACER and the THROWN objects aren't listed: MoveEmitter deletes them when the flight ends, so they must
    #  NOT self-destruct - see below)
    for ps, res in ((GUN, SPARK), (GUN, FLASH), (KIT, CASING), (KIT, CROSS), (SMOKE, PUFF),
                    (SMOKE, DIRT), (CAR, RIDE), (CAR, WINDOW), (BLING, PENDANT), (CASH, BILLS), (CASH, STACK),
                    (ROCKET, TO_ENEMY), (ROCKET, TO_PLAYER), (FIRE, EMBERS), (FIRE, BLAZE), (HOUSE, HOME),
                    (YOLK, DRIP), (YOLK, SPLAT), (CAR, PARKED), (CAR, BOUNCE), (HYDRANT, STAND),
                    (JET, JET_E), (JET, JET_P), (SPLASH, 0), (SPLASH, 1), (SLUGGER, SWING_E), (SLUGGER, SWING_P),
                    (TASER, STAND), (TASER, TASER_P), (BOLTS, ZAP), (FOB, STAND), (RINGS, RING), (SUB, BOX),
                    (SUB, PUMP), (CRACK, SPLIT), (CHIPS, BAG), (CHIPS, CHIP_E), (CHIPS, CHIP_P), (BURST, TONGUE),
                    (BURST, EMBER), (SHADES, SLIDE), (GLINT, TING), (GLINT, SWEAT), (BUBBLE, BANG), (POCKET, SIGN),
                    (POCKET, GRAIN_E), (POCKET, GRAIN_P), (SAND, CLOUD), (FAN, BODY), (FAN, BLADES),
                    (WIND, GUST_E), (WIND, GUST_P)):
        flag = spa.resources(out[ps])[res]["flag"]
        assert flag >> 14 & 1, f"kit {ps} emitter {res} never finishes (no self_dest): WaitForParticles would hang"
    for ps, res in ((GUN, TRACER), (BOTTLE, THROWN), (BRICK, THROWN), (EGG, THROWN), (BUBBLE, TALK)):
        flag = spa.resources(out[ps])[res]["flag"]
        assert not flag >> 14 & 1, f"kit {ps} emitter {res} is flown by MoveEmitter: it must not self-destruct"
    return out


# ------------------------------------------------------------------ script pieces

def _u(v):
    return v & 0xFFFFFFFF


def func(fid, *args):
    return [45, fid, len(args), *(_u(a) for a in args)]


def wait(n):
    return [0, n]


def wait_frames(n):
    """A wait lasting about n frames (measured: wait(k) takes 2 * (k + 1))."""
    return wait(max(0, round(n / 2) - 1))


def se(seq):
    return [5, seq] if seq is not None else []


_SIDE = ["player"]                                            # whose turn the script being built is for


def _depth(who):
    """'near' or 'far' for the attacker (who=0) / defender (who=1) of the current script side."""
    attacker_near = _SIDE[0] == "player"
    return "near" if (who == 0) == attacker_near else "far"


_SLOT = {}                                                    # kit -> particle-system slot, for the variant being built


def _ps(kit):
    """The engine has only 16 particle-system slots (particleSystems[16], followed by emitters[16]): kit numbers
    go past that, so each animation puts its kits in slots 0, 1, 2."""
    return _SLOT[kit]


def emit_at(ps, res, who, off=(0, 0)):
    """Emitter at the attacker (who=0) or defender (who=1) plus an offset in screen pixels (y up)."""
    if off == (0, 0):
        return [46, _ps(ps), res, 3 if who == 0 else 4]
    sx, sy = PS_SCALE.get(ps, SCALE)[_depth(who)]
    x, y = round(off[0] * sx), round(off[1] * sy)
    # ConfigureFromScript: zMode, battlerOrder 0, position mode 4/5 (battler A/B + offset), axis, flags,
    # camera; then the offset args {ignoreSide, x, y, z}
    return [46, _ps(ps), res, 17, 55, 6, 0, 0, 4 + who, 0, 0, 0, 55, 4, 1, _u(x), _u(y), 0]


def muzzle(ps, res, side, back=0):
    x, y = MUZZLE[side]
    return emit_at(ps, res, 0, (x - back if x > 0 else x + back, y))


def tracer(slot, frames, off=(0, 0), start=2, delay=0):
    """Bullet streak flown from the barrel to the target (+ off pixels), with MoveEmitter."""
    return [47, _ps(GUN), slot, TRACER, 3] + func(65, slot, off[0], off[1], delay, frames, 0, 0, start << 16, 0)


def shake_defender(amp, count):
    return func(36, amp, 0, 1, count, 264)


def shake_attacker(amp, count):
    return func(36, amp, amp // 2, 1, count, 258)


def recoil(px, back_frames=4):
    return func(52, 1, -px, 258), func(52, back_frames, px, 258)


def flash_screen(steps=6):
    return [85, steps]


# ------------------------------------------------------------------ the five feels

def _sniper(side, s):
    w = func(33, 0, 1, 0, 12, 0)                              # the world goes dark...
    w += emit_at(KIT, CROSS, 1) + wait(34)                     # ...red crosshair locks on, beat of silence
    kick, back = recoil(10)
    w += se(s["boom"]) + flash_screen(8) + kick
    w += muzzle(GUN, FLASH, side) + muzzle(GUN, SPARK, side)
    w += tracer(1, 2, start=1) + wait(2)
    w += emit_at(GUN, FLASH, 1) + emit_at(GUN, SPARK, 1) + func(48) + func(68, 5, 0, 1, 3, 0)
    w += back + wait(6) + muzzle(SMOKE, PUFF, side) + wait(10)
    w += func(33, 0, 1, 12, 0, 0)
    return w


def _shotgun(side, s):
    kick, back = recoil(14, 6)
    w = se(s["boom2"]) + flash_screen(6) + kick + func(9)
    w += muzzle(GUN, FLASH, side) + muzzle(GUN, SPARK, side) + muzzle(GUN, SPARK, side, back=4)
    for slot, off in enumerate([(0, 0), (12, 7), (-12, -6), (7, -12), (-7, 12)], 1):
        w += tracer(slot, 4, off, start=1)
    w += wait(4) + emit_at(GUN, FLASH, 1) + emit_at(GUN, SPARK, 1)
    for off in ((10, 9), (-9, -7)):
        w += emit_at(GUN, SPARK, 1, off)
    w += func(48) + shake_defender(5, 4) + muzzle(SMOKE, PUFF, side) + back + wait(12)
    return w


def _spray(side, s):
    w = shake_attacker(2, 26)                                  # the shooter can't hold it steady
    jit = [(0, 0), (14, -9), (-10, 12), (18, 6), (-16, -4), (6, 16), (-4, -14)]
    dirt = [(14, -16), (-12, -18), (6, -20), (-17, -14), (11, -12), (-4, -19)]
    for i in range(7):
        w += se(s["pop"]) + muzzle(GUN, SPARK, side) + tracer(1 + i % 4, 3, jit[i], start=1)
        w += muzzle(KIT, CASING, side, back=18)
        if i < len(dirt):
            w += emit_at(SMOKE, DIRT, 1, dirt[i])
        w += wait(4)
    w += emit_at(GUN, SPARK, 1) + shake_defender(3, 4) + wait(8)
    return w


def _point_blank(side, s):
    w = func(57, 8, 70, -34, 258) + wait(9)                    # walk right up to them
    w += func(36, 1, 0, 1, 6, 258) + wait(8)                   # menacing pause
    w += se(s["boom"]) + flash_screen(12)
    w += emit_at(GUN, FLASH, 1, (-10, 4)) + emit_at(GUN, SPARK, 1)
    w += func(50, 4, 1) + func(48) + func(68, 6, 2, 1, 4, 0) + wait(10)
    w += muzzle(SMOKE, PUFF, side) + func(57, 10, -70, 34, 258) + wait(12)
    return w


def _gangsta(side, s):
    w = func(4, 0, 0x1C00, 14, 1, 0, 40) + wait(12)            # tilt it sideways
    for i in range(2):
        kick, back = recoil(4, 2)
        w += se(s["pop"]) + kick + muzzle(GUN, FLASH, side) + muzzle(GUN, SPARK, side)
        w += tracer(1 + i, 3, start=1) + muzzle(KIT, CASING, side, back=18) + back + wait(5)
    w += emit_at(GUN, SPARK, 1) + shake_defender(3, 3) + wait(4)
    w += muzzle(SMOKE, PUFF, side) + wait(14) + func(19) + wait(10)   # blow the smoke, little hop
    return w




def _drive_by(side, s):
    """Hop in the car off-screen, roll past the target blasting out the window, dip, come back."""
    w = func(19) + wait(8)                                     # hop up...
    w += func(57, 10, -130, 0, 258) + wait(12)                 # ...and run out of frame to get the car
    w += se(s["skrrt"]) + emit_at(CAR, RIDE, 1, (CAR_START, CAR_ROAD))
    w += emit_at(CAR, WINDOW, 1, (CAR_START + GUN_ON_CAR[0], CAR_ROAD + GUN_ON_CAR[1]))
    first = (-CAR_START - GUN_ON_CAR[0] - 25) / CAR_SPEED - 18  # frames until the gun lines up (-18 measured)
    for i in range(6):                                         # rounds land while it rolls past
        w += wait_frames(first if i == 0 else 6)
        w += se(s["pop"]) + emit_at(GUN, SPARK, 1, ((i * 37 % 9 - 4) * 3, (i * 23 % 7 - 3) * 3))
        if i % 2 == 0:
            w += emit_at(SMOKE, DIRT, 1, ((i - 3) * 9, -14))
        w += shake_defender(3, 2)
    w += wait(30)                                              # and they're gone
    w += func(57, 10, 130, 0, 258) + wait(12)                  # back like nothing happened
    return w


def _calibrate(side, s):
    """Test only: the same offset (40px left of the target) in three kits - where does each really land?"""
    w = emit_at(GUN, FLASH, 1, (-40, 0)) + wait(14)
    w += emit_at(YOLK, SPLAT, 1, (-40, 0)) + wait(14)
    w += emit_at(HOUSE, HOME, 1, (-40, 0)) + wait(30)
    return w


SWING_STEP = 4                                                # frames each pose of the swinging chain shows
# (= wait(1): one script tick takes ~2 frames, plus the tick the commands run in)


def _chain_swing(side, s, swings=3, dark=True):
    """Psychic: an iced-out chain swung in front of their face like a hypnotist's watch (stop-motion:
    one short-lived chain per pose along the pendulum arc)."""
    purple = rgb(70, 0, 110)
    w = func(33, 0, 1, 0, 9, purple) + wait(4) if dark else []
    poses = 10                                                 # per swing (there and back)
    for k in range(swings * poses):
        ph = 2 * math.pi * k / poses
        x = 15 * math.sin(ph) - 8                              # (the particle origin sits right of their face)
        y = 16 - 3 * math.cos(2 * ph)                          # rides up a little at the ends
        w += emit_at(BLING, PENDANT, 1, (round(x), round(y)))
        if k % (poses // 2) == poses // 4:                     # at each end of the swing
            end = 1 if math.sin(ph) > 0 else -1
            w += se(s["bling"]) + emit_at(GUN, SPARK, 1, (end * 15 - 8, 10))
            w += func(4, 0, 0x0C00, 6, 0 if end > 0 else 2)    # their head follows it
        w += wait(1)
    w += func(34, 8, 0, 2, purple, 14, 0) + shake_defender(3, 4) + emit_at(GUN, FLASH, 1) + wait(8)
    if dark:
        w += func(33, 0, 1, 9, 0, purple)
    return w


def _payday(side, s):
    """Make it rain: flash the bankroll, then a storm of bills flutters down on them."""
    w = se(s["chaching"]) + func(19) + emit_at(CASH, STACK, 0, (6, 52)) + wait(14)
    w += emit_at(CASH, BILLS, 1, (0, 62))                       # it's raining
    for k in range(4):
        w += wait(6) + emit_at(GUN, SPARK, 1, ((k * 29 % 21) - 10, (k * 17 % 13) - 4)) + shake_defender(2, 2)
        if k == 2:
            w += se(s["chaching"])
    return w + wait(30)


def _explosion(side, s, big=True):
    """A big hit on the target: fireball flash, sparks flying, dirt, smoke, the whole field shaking."""
    w = se(s["boom2"]) + flash_screen(12 if big else 6)
    w += emit_at(GUN, FLASH, 1) + emit_at(GUN, FLASH, 1, (8, 6)) + emit_at(GUN, SPARK, 1)
    for off in ((14, 10), (-12, 8), (10, -8), (-14, -6)):
        w += emit_at(GUN, SPARK, 1, off)
    w += emit_at(SMOKE, DIRT, 1, (-10, -14)) + emit_at(SMOKE, DIRT, 1, (12, -14))
    w += func(48) + func(68, 6, 3, 1, 5, 0) + shake_defender(5, 5)
    w += wait(6) + emit_at(SMOKE, PUFF, 1, (0, 4)) + emit_at(SMOKE, PUFF, 1, (-10, -2))
    return w


def _full_auto(side, s):
    """Hyper Beam: a minigun barrage - brass pouring out, the shooter shaking, then everything goes up."""
    w = shake_attacker(2, 60) + func(68, 2, 1, 1, 20, 0)       # the whole screen rattles
    jit = [(0, 0), (12, -8), (-9, 10), (16, 5), (-14, -4), (5, 14), (-4, -12), (10, 10)]
    for i in range(18):
        if i % 2 == 0:
            w += se(s["pop"])
        w += muzzle(GUN, SPARK, side) + tracer(1 + i % 6, 3, jit[i % len(jit)], start=1)
        if i % 2:
            w += muzzle(KIT, CASING, side, back=18)
        if i % 4 == 0:
            w += emit_at(GUN, SPARK, 1, (jit[(i + 3) % 8][0] // 2, jit[(i + 5) % 8][1] // 2))
        if i % 6 == 5:
            w += flash_screen(4)
        w += wait(1)
    w += muzzle(SMOKE, PUFF, side) + wait(4)
    return w + _explosion(side, s) + wait(14)


def _rpg(side, s):
    """Legendary finisher: shoulder an RPG, fwoosh, a smoking rocket crosses the field, KABOOM."""
    kick, back = recoil(12, 8)
    w = se(s["fwoosh"]) + kick + muzzle(GUN, FLASH, side) + muzzle(SMOKE, PUFF, side, back=20)
    w += emit_at(ROCKET, TO_ENEMY if side == "player" else TO_PLAYER, 0, MUZZLE[side])
    mx, my = MUZZLE[side]
    t = 0
    for k in (1, 2, 4):                                        # smoke trail left behind it
        w += wait_frames(ROCKET_FRAMES / 5 * (k - t))
        t = k
        f = k / 5
        dx, dy = (128 * f, 64 * f) if side == "player" else (-128 * f, -64 * f)
        w += emit_at(SMOKE, PUFF, 0, (round(mx * (1 - f) + dx), round(my * (1 - f) + dy)))
    w += wait_frames(ROCKET_FRAMES / 5) + back
    return w + _explosion(side, s) + wait(20)


def _throw(kit, slot=1, at=(0, 0)):
    """Lob the kit's object from the attacker at the target (+ `at` screen pixels from it): MoveEmitter flies
    the emitter in a line while the object, riding it, goes up and comes down (its own gravity)."""
    sx = SCALE[_depth(1)][0] / EMITTER_PIXEL               # MoveEmitter offsets are 172-unit pixels, x mirrored
    sy = SCALE[_depth(1)][1] / EMITTER_PIXEL               # by the attacker's side
    side = 1 if _SIDE[0] == "player" else -1
    ox, oy = round(at[0] * sx * side), round(at[1] * sy * side)
    return se_key("whoosh") + [47, _ps(kit), slot, THROWN, 3] + func(65, slot, ox, oy, 0, THROW_FRAMES, 0, 0, 0, 0)


def se_key(key):
    return ["SE", key]                                        # resolved to a sound id by variant()


def _molotov(side, s):
    """Flamethrower: a Molotov tumbles over and shatters; flames lick up and they dance around on fire."""
    orange = rgb(255, 120, 20)
    w = func(19) + wait(4) + _throw(BOTTLE) + wait_frames(THROW_FRAMES)
    w += se(s["smash"]) + emit_at(GUN, SPARK, 1, (0, -4)) + emit_at(FIRE, BLAZE, 1, (0, -8))
    w += emit_at(FIRE, EMBERS, 1, (0, -6)) + func(34, 8, 0, 2, orange, 14, 0)
    for k in range(4):                                         # hot hot hot: hopping side to side
        dx = (6, -12, 12, -6)[k]                                # nets to zero: they end up where they started
        w += func(57, 3, dx, 0, 264) + emit_at(FIRE, BLAZE, 1, ((-7, 7, -3, 5)[k], -8)) + wait(4)
    w += emit_at(FIRE, EMBERS, 1, (0, 0)) + shake_defender(2, 4) + wait(14)
    return w


def _brick(side, s):
    """Rock Throw: a brick tumbles across - BONK - they drop, lie there seeing stars, then slowly get up."""
    down = -10 if side == "player" else 10                    # MoveBattlerBy mirrors the enemy's y
    w = func(19) + wait(4) + _throw(BRICK) + wait_frames(THROW_FRAMES)
    w += se(s["bonk"]) + emit_at(GUN, FLASH, 1, (0, 12)) + emit_at(GUN, SPARK, 1, (0, 14))
    w += emit_at(SMOKE, DIRT, 1, (-8, -12)) + emit_at(SMOKE, DIRT, 1, (8, -12))
    w += func(57, 3, 0, down, 264) + func(36, 2, 0, 1, 3, 264) + wait(4)      # knocked down on the spot
    for k in range(16):                                        # out cold: stars round the head, slow wobble
        ang = k * math.pi / 4
        w += emit_at(GUN, SPARK, 1, (round(12 * math.cos(ang)), round(14 + 4 * math.sin(ang))))
        if k % 8 == 0:
            w += func(4, 0, 0x0500, 12, 0 if k % 16 == 0 else 2)
        w += wait(3)
    w += func(57, 16, 0, -down, 264) + wait(18)               # ...and slowly back up
    return w


def _egg(side, s):
    """Egg Bomb: egg ya house - their house pops up and gets egged, then they catch the last one."""
    yolk = rgb(255, 220, 60)
    hx, hy = (42, 20) if side == "player" else (-42, 20)      # their house: behind them, standing on their ground
    w = se(s["bling"]) + emit_at(HOUSE, HOME, 1, (hx, hy)) + wait(12)
    for k, (dx, dy) in enumerate(((-8, 6), (9, -4))):           # two on the house...
        w += func(19) + _throw(EGG, 1 + k, (hx + dx, hy + dy)) + wait_frames(THROW_FRAMES)
        w += se(s["splat"]) + emit_at(YOLK, SPLAT, 1, (hx + dx, hy + dy)) + emit_at(YOLK, DRIP, 1, (hx + dx, hy + dy - 2))
        w += wait(6)
    w += func(19) + _throw(EGG, 3) + wait_frames(THROW_FRAMES)  # ...and one for them
    w += se(s["splat"]) + emit_at(YOLK, SPLAT, 1, (0, 10)) + emit_at(YOLK, DRIP, 1, (0, 8))
    w += func(34, 8, 0, 2, yolk, 14, 0) + shake_defender(2, 3) + wait(30)
    return w


def _fly(ps, res, slot, frames, at=(0, 0)):
    """Create kit ps's emitter res at the attacker and fly it (MoveEmitter) to the target + at (screen px)."""
    sx = SCALE[_depth(1)][0] / EMITTER_PIXEL
    sy = SCALE[_depth(1)][1] / EMITTER_PIXEL
    side = 1 if _SIDE[0] == "player" else -1
    return [47, _ps(ps), slot, res, 3] + func(65, slot, round(at[0] * sx * side), round(at[1] * sy * side), 0, frames,
                                         0, 0, 0, 0)


def _hose(side, s):
    """Water Gun: a hydrant pops up beside them, cap off, and it HOSES the target - the water really comes out
    of the nozzle and arcs over."""
    blue = rgb(80, 150, 255)
    hx, hy = HYDRANT_AT[side]
    nx, ny = hx + NOZZLE[side][0], hy + NOZZLE[side][1]
    w = se(s["bonk"]) + emit_at(HYDRANT, STAND, 0, (hx, hy)) + wait(10)
    w += se(s["spray"]) + emit_at(JET, JET_E if side == "player" else JET_P, 0, (nx, ny))
    w += wait_frames(JET_FRAMES) + func(34, 8, 0, 2, blue, 14, 0)
    for k in range(3):                                          # getting drenched
        w += emit_at(SPLASH, 1, 1, ((-6, 6, 0)[k], (8, 2, 14)[k])) + emit_at(SPLASH, 0, 1, (0, 6))
        w += shake_defender(2, 3) + wait(5)
        if k == 1:
            w += se(s["spray"])
    return w + wait(16)


def _bat(side, s):
    """Bone Club: walk up, wind up, and swing the bat THROUGH them - CRACK - they reel."""
    px = -30 if side == "player" else 30                       # the hands, at the end of the walk-up
    w = func(57, 6, 60, -30, 258) + wait(8)                    # step in
    w += emit_at(SLUGGER, SWING_E if side == "player" else SWING_P, 1, (px, 6)) + se(s["whoosh"]) + wait(3)
    w += se(s["crack"]) + flash_screen(8) + emit_at(GUN, FLASH, 1, (0, 10)) + emit_at(GUN, SPARK, 1, (4, 14))
    w += func(48) + shake_defender(5, 4) + func(68, 4, 2, 1, 3, 0) + wait(8)
    w += func(57, 8, -60, 30, 258) + wait(10)
    return w + wait(6)


def _taser(side, s):
    """ThunderShock: pull the taser, prongs fly, and they light up - bolts crackling all over them."""
    tx, ty = MUZZLE[side]
    w = emit_at(TASER, STAND if side == "player" else TASER_P, 0, (tx - (6 if side == "player" else -6), ty)) + wait(8)
    w += se(s["pop"]) + tracer(1, 4, (-4, 3), start=1) + tracer(2, 4, (4, -3), start=1) + wait_frames(5)
    w += se(s["zap"]) + emit_at(BOLTS, ZAP, 1, (0, 8)) + flash_screen(4)
    for k in range(8):                                          # zzzzt: strobing, twitching
        if k == 4:
            w += se(s["zap"])
        w += func(34, 8, 0, 1, rgb(255, 255, 80) if k % 2 == 0 else rgb(20, 20, 40), 16, 0)
        w += func(36, 3, 1, 1, 2, 264) + wait(2)
    return w + wait(10)


def _car_alarm(side, s):
    """Screech: they mash the panic button on a key fob - the alarm screams and sound waves blast the target."""
    w = emit_at(FOB, STAND, 0, (8, 30)) + wait(8)
    for k in range(6):
        if k % 3 == 0:
            w += se(s["alarm"])
        w += emit_at(RINGS, RING, 1, (0, 8)) + emit_at(RINGS, RING, 0, (8, 30))
        w += func(34, 8, 1, 1, rgb(255, 40, 40) if k % 2 == 0 else rgb(255, 255, 255), 12, 0)
        w += func(36, 3, 0, 1, 3, 264) + wait(5)
    return w + wait(10)


def _bass_drop(side, s):
    """Earthquake: a subwoofer drops in and every bass hit pumps the cone, quakes the screen and cracks the
    ground open under the target."""
    bx, by = (-26, 50) if side == "player" else (26, 30)
    w = emit_at(SUB, BOX, 0, (bx, by)) + wait(8)
    for k in range(8):
        w += se(s["bass"]) + emit_at(SUB, PUMP, 0, (bx, by))
        w += func(68, 4 + k // 3, 2, 1, 2, 0) + func(36, 3, 2, 1, 2, 264) + func(36, 2, 1, 1, 2, 258)
        if k == 1:
            w += emit_at(CRACK, SPLIT, 1, (0, -20))
        w += emit_at(SMOKE, DIRT, 1, ((k % 3 - 1) * 14, -18))
        if k % 2 == 0:
            w += flash_screen(2)
        w += wait(5)
    w += func(48) + func(68, 6, 3, 1, 4, 0) + wait(16)
    return w


def cry(mode, param):
    """PlayCry: the attacker's own cry (modes 9/10 are Growl's distorted takes)."""
    return [65, mode, _u(-117), param]


def _hot_shot(side, s):
    """Ember: they rip open a big bag of HOT chips and fling fistfuls in the target's face - who catches fire."""
    at = BAG_AT[side]
    throw = CHIP_E if side == "player" else CHIP_P
    orange = rgb(255, 120, 20)
    w = emit_at(CHIPS, BAG, 0, at) + wait(10)                                   # the bag
    w += func(19) + se(s["crack"]) + emit_at(BURST, EMBER, 0, at) + wait(4)     # RRIP - it's that hot
    for k in range(3):                                                          # three handfuls
        if k != 1:
            w += se(s["ember"])
        w += emit_at(CHIPS, throw, 0, (at[0], at[1] + (4, -2, 8)[k])) + func(9) + wait(4)
    w += wait_frames(CHIP_FRAMES - 6)
    w += emit_at(BURST, TONGUE, 1, (0, -6)) + emit_at(BURST, EMBER, 1, (0, 6)) + se(s["fwoosh"])
    w += func(34, 8, 0, 2, orange, 14, 0) + shake_defender(3, 5) + func(48) + wait(18)
    return w


def _stare_down(side, s):
    """Leer (Mean Mug): lights down, red. "Deal with it" shades slide down into place - THUMP - the lens
    glints, and the target's sweating bullets and backing up."""
    at = SHADES_AT[side]
    dark = rgb(70, 0, 0)
    w = func(33, 0, 1, 0, 12, dark) + wait(4)
    steps = 9
    for k in range(steps):                                                      # ...sliiiide down (easing in)
        y = at[1] + round(SHADES_DROP * (1 - k / (steps - 1)) ** 1.6)
        w += emit_at(SHADES, SLIDE, 0, (at[0], y)) + wait(1)
    w += emit_at(SHADES, LANDED, 0, at)
    w += se(s["bass"]) + func(68, 3, 2, 1, 2, 0) + wait(4)                     # they're on. THUMP
    w += se(s["leer"]) + emit_at(GLINT, TING, 0, (at[0] - 12, at[1])) + wait(10)   # *ting*
    w += emit_at(GLINT, SWEAT, 1, (0, 28)) + func(34, 8, 0, 2, rgb(150, 175, 255), 12, 0)
    w += func(57, 10, 14, 0, 264) + func(36, 2, 0, 1, 8, 264) + wait(8)        # backing up, shaking
    w += emit_at(GLINT, SWEAT, 1, (6, 24)) + wait(12)
    w += func(57, 8, -14, 0, 264) + func(33, 0, 1, 12, 0, dark) + wait(10)
    return w


def _talk_trash(side, s):
    """Growl: they run their mouth - cussing speech bubbles fly across, and every one lands."""
    w = cry(9, 100) + shake_attacker(1, 14)
    for k in range(3):
        w += _fly(BUBBLE, TALK, 1 + k, FLY, ((-8, 8, 0)[k], (6, 14, 22)[k])) + wait(5)
    w += wait_frames(FLY - 10)
    for k in range(3):                                                          # each one hits
        w += emit_at(BUBBLE, BANG, 1, ((-10, 10, 0)[k], 30)) + func(36, 2, 0, 1, 2, 264)
        w += func(34, 3, 0, 1, rgb(255, 80, 80), 8, 0) + wait(4)
    w += cry(10, 127) + wait(14)
    return w


def _pocket_sand(side, s):
    """Sand-Attack: "POCKET SAND!" - and a fistful of sand right in the target's eyes."""
    hand = HAND_AT[side]
    throw = GRAIN_E if side == "player" else GRAIN_P
    w = emit_at(POCKET, SIGN, 0, (hand[0] // 3, 58)) + se(s["sand"]) + func(19) + wait(8)
    for k in range(2):                                                          # SHA-SHA!
        w += se(s["sand"]) + emit_at(POCKET, throw, 0, (hand[0], hand[1] + 3 * k)) + func(9) + wait(4)
    w += wait_frames(SAND_FRAMES - 4)
    w += emit_at(SAND, CLOUD, 1, (0, 20)) + emit_at(SAND, CLOUD, 1, (-8, 12))
    w += func(34, 8, 0, 2, rgb(215, 185, 120), 13, 0)
    w += func(4, 0, 0x0700, 10, 0) + func(36, 2, 0, 1, 6, 264) + wait(10)       # rubbing their eyes
    w += func(4, 0, 0x0700, 10, 2) + wait(16)
    return w


def _fan_blast(side, s):
    """Gust: a box fan drops in next to them, cranks to high, and blows the target clean back."""
    at = FAN_AT[side]                                       # right behind them, blowing past at the target
    gust = GUST_E if side == "player" else GUST_P
    w = emit_at(FAN, BLADES, 0, (at[0], at[1] + 1)) + emit_at(FAN, BODY, 0, at) + wait(8)
    w += se(s["gust"])
    push = 18
    for k in range(5):                                                          # waves of gusts off the grill
        w += emit_at(WIND, gust, 0, (at[0], at[1] + (0, 7, -6, 4, -3)[k]))
        if k == 2:                                                              # the first lines land:
            w += func(57, 10, push, 0, 264) + func(36, 2, 1, 1, 8, 264)          # blown back, flapping
        if k == 3:
            w += se(s["gust"])
        w += wait(3)
    w += wait_frames(GUST_FRAMES) + func(57, 8, -push, 0, 264) + wait(12)
    return w


def _chain_dangle(side, s):
    """Confusion: a quicker dangle, no lights-down."""
    return _chain_swing(side, s, swings=2, dark=False)


VARIANTS = {99: _calibrate, 7: _chain_swing, 8: _chain_dangle, 9: _payday, 10: _full_auto, 11: _rpg,
            12: _molotov, 13: _brick, 14: _egg, 15: _hose, 16: _bat, 17: _taser, 18: _car_alarm, 19: _bass_drop,
            20: _hot_shot, 21: _stare_down, 22: _talk_trash, 23: _pocket_sand, 24: _fan_blast, 1: _sniper, 2: _shotgun, 3: _spray, 4: _point_blank, 5: _gangsta, 6: _drive_by}


# particle kits each animation uses: the battle heap only fits a few particle systems at once
KITS = {99: (GUN, HOUSE, YOLK), 1: (GUN, KIT, SMOKE), 2: (GUN, SMOKE), 3: (GUN, KIT, SMOKE), 4: (GUN, SMOKE),
        5: (GUN, KIT, SMOKE), 6: (GUN, SMOKE, CAR), 7: (GUN, BLING), 8: (GUN, BLING), 9: (GUN, CASH), 10: (GUN, KIT, SMOKE),
        11: (GUN, SMOKE, ROCKET), 12: (GUN, BOTTLE, FIRE), 13: (GUN, BRICK, SMOKE), 14: (EGG, HOUSE, YOLK),
        15: (HYDRANT, JET, SPLASH), 16: (GUN, SLUGGER), 17: (GUN, TASER, BOLTS), 18: (FOB, RINGS),
        19: (SUB, CRACK, SMOKE), 20: (CHIPS, BURST), 21: (SHADES, GLINT), 22: (BUBBLE,), 23: (POCKET, SAND),
        24: (FAN, WIND)}


def variant(k, sounds):
    """Animation script words for feel k; sounds = {"pop": seq, "boom": seq, ...}."""
    kits = KITS[k]
    _SLOT.clear()
    _SLOT.update({ps: i for i, ps in enumerate(kits)})
    frees = [w for i in range(len(kits)) for w in (53, i)]

    def body(side):
        _SIDE[0] = side
        # WaitForTasks, then put both Pokémon back exactly where they belong (MoveBattlerBy moves dx // duration
        # per frame, so a move and its "undo" can disagree by a few pixels), WaitForParticles, free, End
        w = VARIANTS[k](side, sounds) + [1] + func(62, 2) + func(62, 8) + [50] + frees + [4]
        while "SE" in w:                                            # sound markers from helpers
            i = w.index("SE")
            w[i:i + 2] = [5, sounds[w[i + 1]]]
        return w

    head = (PRELUDE + [51, 0, LOAD[kits[0]]] + PRELUDE_END +
            [w for i, ps in enumerate(kits[1:], 1) for w in (51, i, LOAD[ps])])
    p, e = body("player"), body("enemy")
    # JumpBySide attacker: [64, 0, off->player, off->enemy]; offsets count from their own word
    j = len(head)
    words = head + [64, 0, 2, 1 + len(p)] + p + e
    assert words[j + 2] + j + 2 == j + 4 and words[j + 3] + j + 3 == j + 4 + len(p)
    return words
