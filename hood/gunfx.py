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
(PLANE, WHAM, WAVE, DUCK, CABLE, XRAY, HONK, CONE, BOOZE, BREATH, LEAF, HAZE, BOOT, STOMP, TOPJAW, BOTJAW, GLITZ,
 SLUG, SHATTER, SLASH, TIRE, SMOG, COUGH, WHEEL, TRAIL, BLOCKS, CHOP, HIYAH, EIGHT, ANSWER, HEART) = range(32, 63)
(TORCH, BEAM, HUH, STUN, STATIC, ZZZT, BOOMBOX, SOUNDWAVE, BWOMP, SQUAD, SQUAD2, SQUADUP, BALLOON, DRENCH, SPLOOSH,
 DISS, SLAP, OOOH, CUP, GOOP, DIRTY, LID, NOPE, CHAIR, CLANG, SMACKDN, BIGTASER, MEGABOLT, BZZT,
 EYES, CIRCLE, CLOCKED) = range(63, 95)
DONOR = {GUN: 73, KIT: 62, SMOKE: 84, CAR: 82, BLING: 168, CASH: 47, ROCKET: 349,
         BOTTLE: 349, BRICK: 349, EGG: 349, FIRE: 84, HOUSE: 168, YOLK: 84,
         HYDRANT: 349, JET: 84, SPLASH: 84, SLUGGER: 168, TASER: 349, BOLTS: 349, FOB: 349, RINGS: 62,
         SUB: 168, CRACK: 168,
         CHIPS: 82, BURST: 84, SHADES: 168, BUBBLE: 349, POCKET: 82, SAND: 84, FAN: 82, WIND: 84,
         GLINT: 349,
         PLANE: 82, WHAM: 168, WAVE: 82, DUCK: 349, CABLE: 168, XRAY: 82, HONK: 82, CONE: 349, BOOZE: 349,
         BREATH: 84, LEAF: 82, HAZE: 84, BOOT: 168, STOMP: 82, TOPJAW: 168, BOTJAW: 168, GLITZ: 349, SLUG: 82,
         SLASH: 82, TIRE: 349, SMOG: 84, COUGH: 349, WHEEL: 82, TRAIL: 84, BLOCKS: 82, CHOP: 168,
         HIYAH: 168, EIGHT: 82, ANSWER: 168, HEART: 82,
         TORCH: 82, BEAM: 168, HUH: 168, STUN: 82, STATIC: 168, ZZZT: 168, BOOMBOX: 82, SOUNDWAVE: 84, BWOMP: 168,
         SQUAD: 82, SQUAD2: 168, SQUADUP: 168, BALLOON: 349, DRENCH: 82, SPLOOSH: 168, DISS: 168, SLAP: 82,
         OOOH: 168, CUP: 349, GOOP: 84, DIRTY: 168, LID: 82, NOPE: 168, CHAIR: 82, CLANG: 168, SMACKDN: 168,
         BIGTASER: 82, MEGABOLT: 168, BZZT: 168, EYES: 82, CIRCLE: 168, CLOCKED: 168}
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

# ---- set 4 emitters (per kit)
POSE, HOLD = 0, 1                                             # the 64px stop-motion kits: one pose, the held one
POP = 0                                                       # the 64px sign kits: the burst popping up
PASS, DIVE_E, DIVE_P, JETSMOKE = 2, 1, 3, 0                   # JET: across the sky, dive-bombing each way, smoke
WAVE_E, WAVE_P, FOAM = 2, 3, 0                                # WAVE: a crest rolling each way, foam splashing up
DUCK_E, DUCK_P = 0, 1                                         # DUCK: the rubber duck riding along each way
BONES, SPARKS = 2, 0                                          # XRAY: the flickering skeleton, sparks
HONK_A, HONK_B, STEAM = 2, 3, 0                               # HONK: two HONK!s, steam off their head
SWIG, LIGHTER = 0, 2                                          # BOOZE: the bottle at their mouth, the lighter flame
FIRE_E, FIRE_P = 0, 1                                         # BREATH: fire breathed each way
LEAF_E, LEAF_P, BIGLEAF = 0, 1, 2                             # LEAF: leaves thrown each way, the big leaf
HAZE1 = 1                                                     # HAZE: the haze rolling over the target
DUST = 0                                                      # STOMP: dust thrown up
SPARKLE = 2                                                   # GLITZ: bling sparkles
DOT, HOLE, IMPACT = 2, 3, 0                                   # SLUG: the laser-sight dot, the bullet hole, sparks
SLASH_A, SLASH_B, SLASH_C, GLEAM = 1, 2, 3, 0                 # SLASH: three slash angles, the blade's gleam
TIRE_UP, TIRE_FLAT, HISS = 0, 1, 2                            # TIRE: the tire, the flat, air hissing out
SMOG1, SMOG2 = 1, 0                                           # SMOG: big smoke everywhere, wisps at the target
PUFFUP = 0                                                    # COUGH: a *cough* cloud rising
SPIN, ROLL, SMOKE1 = 2, 3, 0                                  # WHEEL: spinning in place, rolling (flown), tire smoke
FIRETRAIL = 1                                                 # TRAIL: flames left behind the wheel (flown)
HALF_L, HALF_R, CHUNKS = 2, 3, 0                              # BLOCKS: the stack's two halves (poses), chunks
CHARGE, ROLL8, WISPS = 3, 2, 0                                # EIGHT: the 8-ball growing, rolling (flown), dark wisps
LOCKET, SLAM, HEARTS_E, HEARTS_P = 2, 3, 0, 1                 # HEART: the pendant, it flying in, hearts each way
# ---- set 5 emitters (per kit)
TORCH_E, TORCH_P, SWIRL = 1, 2, 0                             # TORCH: the flashlight aimed each way, dizzy swirls
BEAM_E, BEAM_P = 0, 1                                         # BEAM: the cone of light each way
STUN_E, STUN_P, ARC_E, ARC_P = 1, 2, 0, 3                     # STUN: the stun gun each way, crackles shot each way
RING_X, RING_HOLD = 0, 1                                      # STATIC: a ring blasting out, the ring holding them
BOX5, THUMP, NOTES_E, NOTES_P = 1, 2, 0, 3                    # BOOMBOX: the boombox, it pumping, notes each way
SWAVE_E, SWAVE_P = 0, 1                                       # SOUNDWAVE: ")" arcs each way
FIG, FIG_S, POOF = 1, 2, 0                                    # SQUAD: a homie (big / small), the poof he appears in
FIG2, FIG2_S = 0, 1                                           # SQUAD2: the other homie (big / small)
DROPS = 2                                                     # BALLOON: water dripping off them
CROWN, SPLASHDROPS = 1, 0                                     # DRENCH: the splash, drops flying
SLAP_POSE, SLAP_HOLD, POWS = 1, 2, 0                          # SLAP: the palm coming down, landed, impact lines
HELD, BUBBLES = 0, 2                                          # CUP: the cup in hand, bubbles rising off them
GOOP_SPLAT, GOOP_DRIPS = 1, 0                                 # GOOP: the purple splat, drips
LIDUP, LIDFLASH, PINGS = 1, 2, 0                              # LID: the shield, its flash, deflection pings
CHAIR_POSE, CHAIR_HOLD, STARS = 1, 2, 0                       # CHAIR: the chair coming down, landed, dizzy stars
BIG_E, BIG_P, ZIGS = 1, 2, 0                                  # BIGTASER: the XL taser each way, crackling
STRIKE, STRIKE2 = 0, 1                                        # MEGABOLT: the bolt, a second smaller one
EYES_R, EYES_L = 1, 2                                         # EYES: the eyes emoji looking right / left
TORCH_AT = {"player": (28, 30), "enemy": (-28, 30)}          # the flashlight (px from the attacker)
TORCH_SCALE, BEAM_AIM = 1.25, (0, 22)                         # ...shining in their eyes
TILE = 75                                                     # emitter header byte: texture tile counts (bits 0-3)
TEXEL = .74                                                   # screen px per texel of a 64px texture at scale 1.0
STUN_AT = {"player": (25, 9), "enemy": (-24, 17)}            # the stun gun, in their hand
STUN_TIP = {"player": (39, 10), "enemy": (-38, 16)}          #   its prongs
STUN_FRAMES = 10
BOX_AT = {"player": (-26, 48), "enemy": (26, 38)}            # the boombox, up on their shoulder
LID_AT = {"player": (52, 62), "enemy": (-28, 16)}            # the trash-can lid: mid-screen / in front of them
NOTE_FRAMES = 14
BEAT_AIM = (0, 24)


def _angle(dx, dy):
    """Particle rotation (0x10000 a turn, counter-clockwise on screen) for art pointing right to point at (dx, dy)."""
    return round(math.degrees(math.atan2(dy, dx)) / 360 * 0x10000) & 0xFFFF


def torch_geometry(side):
    """(rotation, lens, beam centre, beam scale): the flashlight aimed at their eyes, the beam from lens to face."""
    cx, cy = TORCH_AT[side]
    dx, dy = aim_path(side, TORCH_AT[side], BEAM_AIM)
    d = math.hypot(dx, dy)
    ux, uy = dx / d, dy / d
    nose = (.92 - .5) * 64 * TEXEL * TORCH_SCALE                 # texture centre -> lens, px
    lens = (cx + ux * nose, cy + uy * nose)
    length = d - nose
    centre = (round(lens[0] + ux * length / 2), round(lens[1] + uy * length / 2))
    return _angle(dx, dy), lens, centre, length / (64 * TEXEL)


DIVE_FRAMES, DIVE_FROM = 12, (110, 80)                       # the jet's dive: from up there (px from the target)
JET_SPEED = 6                                                 # px per frame: the jet, and whoever it's carrying
PICKUP_FROM = (-160, 52)                                      # jet centre vs the attacker: the ladder's bottom rung
LADDER_X = 11                                                 #   hangs 35px below it, 11px right of the centre
CARRY_FRAMES = 36
WAVE_FROM = {"player": (-330, -12), "enemy": (336, 36)}    # the tidal wave's centre: off-screen, mid-height
WAVE_SPEED, WAVE_SCALE = 8, 5.0                              # a wall of water the height of the screen
LEAF_FRAMES, HEART_FRAMES, BREATH_FRAMES = 12, 12, 14
ROLL_FRAMES, EIGHT_FRAMES = 12, 16
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

    # ---- set 4 ---------------------------------------------------------------------------------------------
    NEEDS = {"clr_anm": "clr", "scl_anm": "scl", "alpha": "alp", "flick": "alp", "gravity": "grvt",
             "child_gen": "chld", "child_clr": "chld"}

    def prop(b, rs, res, **edit):
        """Emitter res as one particle (a prop): no tint, no drift, no spin unless asked; self-destructs."""
        r = rs[res]
        base = dict(gen=1, emtr_life=1, vel=(0, 0), init_pos=0, clr=white, air_resist=128, alpha=(31, 31, 31),
                    scl_anm=(1.0, 1.0, 1.0, 0, 255), clr_anm=(white, white), child_gen=0, gravity=(0, 0, 0),
                    flags_on=1 << 14, flags_off=(1 << 12) | (1 << 13) | (1 << 15) | BILLBOARD)
        base.update(edit)
        for k, block in NEEDS.items():
            if k in base and block not in r:
                del base[k]
        spa.edit(b, r, **base)
        if not base["flags_on"] & (1 << 12):
            struct.pack_into("<hhH", b, r["off"] + 52, 0, 0, 0)
        if "cngc" in r:
            struct.pack_into("<h", b, r["cngc"] + 12, 0)
        if "spin" in r:
            struct.pack_into("<H", b, r["spin"], 0)

    def rot(b, rs, res, spin=0, init=0):
        """Rotation: spin per frame (needs flag bit 12) and the starting angle (0x10000 = a full turn)."""
        struct.pack_into("<hhH", b, rs[res]["off"] + 52, spin, spin, init & 0xFFFF)

    def mover(b, rs, res, vx, vy, **edit):
        """A prop gliding at (vx, vy) screen px per frame (y up)."""
        v = math.hypot(vx, vy)
        prop(b, rs, res, axis=(vx / v, vy / v, 0), vel=(0, v * VEL_UNITS / 4096), **edit)

    def follower(b, rs, res, **edit):
        """One particle riding an emitter that MoveEmitter flies (so: no self-destruct)."""
        args = dict(flags_on=1 << 15, flags_off=(1 << 12) | (1 << 13) | (1 << 14) | BILLBOARD)
        args.update(edit)
        prop(b, rs, res, **args)

    def tex(b, idx, art, colors=32):
        if isinstance(art, bytes):
            spa.set_texture(b, idx, art)
            return
        colors = min(colors, spa.textures(bytes(b))[idx][6] // 2)
        texels, pal = fxart.to_a3i5(art, colors)
        spa.set_texture(b, idx, texels, pal)

    def kit(ps):
        bb = bytearray(files[DONOR[ps]])
        return bb, spa.resources(bytes(bb))

    def thrown(b, rs, size, spin):
        """Res THROWN as a lobbed object riding its emitter (see the Molotov / brick / egg)."""
        h = THROW_PEAK * VEL_UNITS / 4096
        g = 8 * h / THROW_FRAMES ** 2
        prop(b, rs, THROWN, life=THROW_FRAMES + 2, scl=size, axis=(0, 1, 0), vel=(0, g * THROW_FRAMES / 2),
             gravity=(0, -g, 0), tex=1, flags_on=(1 << 15) | (1 << 12), flags_off=(1 << 13) | (1 << 14) | BILLBOARD)
        rot(b, rs, THROWN, spin)

    def sign(ps, lines, **colors):
        b, rs = kit(ps)
        tex(b, 0, fxart.burst_sign(lines, **colors), 30)
        prop(b, rs, POP, scl=1.25, life=28, scl_anm=(.2, 1.25, 1.0, 35, 255))
        out[ps] = bytes(b)

    def poses(ps, art, scl, hold_life):
        b, rs = kit(ps)
        tex(b, 0, art, 30)
        prop(b, rs, POSE, scl=scl, life=SWING_STEP)
        prop(b, rs, HOLD, scl=scl, life=hold_life)
        out[ps] = bytes(b)

    # Catch Flight (Fly): HOOD AIR crossing the sky, then dive-bombing the target; smoke where it hits
    b, rs = kit(PLANE)
    tex(b, 1, fxart.jet())
    tex(b, 0, fxart.soft_puff())
    mover(b, rs, PASS, JET_SPEED, 0, scl=1.6, life=72)
    dx, dy = DIVE_FROM
    mover(b, rs, DIVE_E, dx / DIVE_FRAMES, -dy / DIVE_FRAMES, scl=1.5, life=DIVE_FRAMES)
    rot(b, rs, DIVE_E, init=-round(math.degrees(math.atan2(dy, dx)) / 360 * 0x10000))
    mover(b, rs, DIVE_P, -dx / DIVE_FRAMES, -dy / DIVE_FRAMES, scl=1.5, life=DIVE_FRAMES)
    rot(b, rs, DIVE_P, init=round((180 + math.degrees(math.atan2(dy, dx))) / 360 * 0x10000))
    prop(b, rs, JETSMOKE, tex=0, clr=rgb(150, 150, 155), clr_anm=(rgb(230, 230, 230), rgb(110, 110, 115)), scl=.8,
         life=30, emtr_life=3, gen=4, init_pos=1, radius=.6, vel=(.03, 0), alpha=(31, 26, 0),
         scl_anm=(.6, 1.4, 2.0, 40, 150), air_resist=118)
    out[PLANE] = bytes(b)
    sign(WHAM, ["WHAM!"])

    # Hydrant Wave (Surf): a wave rolling across the block, a rubber duck riding it, foam on impact
    b, rs = kit(WAVE)
    tex(b, 1, fxart.wave_crest())
    tex(b, 0, fxart.soft_puff())
    mover(b, rs, WAVE_E, WAVE_SPEED, 0, scl=WAVE_SCALE, life=84)
    mover(b, rs, WAVE_P, -WAVE_SPEED, 0, scl=WAVE_SCALE, life=84)
    foam = rgb(225, 240, 255)
    prop(b, rs, FOAM, tex=0, clr=foam, clr_anm=(rgb(255, 255, 255), rgb(120, 180, 255)), scl=.55, life=26,
         emtr_life=4, gen=4, axis=(0, 1, 0), vel=(.03, .035), gravity=(0, -.0016, 0), init_pos=1, radius=.5,
         alpha=(31, 31, 0), air_resist=124)
    out[WAVE] = bytes(b)
    b, rs = kit(DUCK)
    tex(b, 1, fxart.rubber_duck(), 24)
    mover(b, rs, DUCK_E, WAVE_SPEED, 0, scl=1.2, life=84)
    mover(b, rs, DUCK_P, -WAVE_SPEED, 0, scl=1.2, life=84)
    out[DUCK] = bytes(b)

    # Power Line (Thunder): the snapped cable swinging down (poses), the x-ray skeleton, sparks
    poses(CABLE, fxart.power_cable(), 1.6, 56)
    b, rs = kit(XRAY)
    tex(b, 1, fxart.skeleton())
    tex(b, 0, fxart.glint())
    prop(b, rs, BONES, scl=1.25, life=40, flick=230)
    prop(b, rs, SPARKS, tex=0, clr=rgb(255, 250, 140), clr_anm=(rgb(255, 255, 255), rgb(255, 220, 40)), scl=.45,
         life=8, emtr_life=22, gen=3, init_pos=1, radius=.7, vel=(.05, 0), alpha=(31, 31, 0),
         flags_on=(1 << 14) | (1 << 13))
    out[XRAY] = bytes(b)

    # Road Rage (Dragon Rage): HONK!s, steam blasting off their head; traffic cones lobbed
    b, rs = kit(HONK)
    tex(b, 1, fxart.burst_sign(["HONK!"], fill=(250, 60, 40, 255), text=(255, 255, 255, 255)))
    tex(b, 0, fxart.soft_puff())
    prop(b, rs, HONK_A, scl=1.15, life=22, scl_anm=(.2, 1.3, 1.0, 35, 255))
    prop(b, rs, HONK_B, scl=.85, life=22, scl_anm=(.2, 1.3, 1.0, 35, 255))
    prop(b, rs, STEAM, tex=0, clr=rgb(245, 245, 250), clr_anm=(rgb(255, 255, 255), rgb(200, 200, 210)), scl=.5,
         life=22, emtr_life=26, gen=2, gen_intvl=1, axis=(0, 1, 0), vel=(.012, .03), init_pos=1, radius=.3,
         alpha=(31, 28, 0), scl_anm=(.6, 1.2, 1.8, 30, 150), air_resist=122)
    out[HONK] = bytes(b)
    b, rs = kit(CONE)
    tex(b, 1, fxart.traffic_cone(), 24)
    thrown(b, rs, .8, 0x0B00)
    out[CONE] = bytes(b)

    # Molotov (Flamethrower): a swig from the bottle, spat through a lighter (fire breath), the bottle lobbed
    b, rs = kit(BOOZE)
    tex(b, 1, fxart.liquor_bottle(), 24)
    tex(b, 0, fxart.soft_puff(hard=1.6))
    prop(b, rs, SWIG, scl=.9, life=26)
    rot(b, rs, SWIG, init=0x2400)                                # tipped back
    thrown(b, rs, .8, 0x0A00)
    prop(b, rs, LIGHTER, tex=0, clr=rgb(255, 170, 40), clr_anm=(rgb(255, 240, 120), rgb(255, 90, 20)), scl=.35,
         life=40, flick=90)
    out[BOOZE] = bytes(b)
    b, rs = kit(BREATH)
    tex(b, 1, fxart.flame_blob())
    for res, sd in ((FIRE_E, "player"), (FIRE_P, "enemy")):
        spray(b, rs, res, sd, (12 if sd == "player" else -12, 30), (0, 16), BREATH_FRAMES, tex=1,
              clr=rgb(255, 130, 30), clr_anm=(rgb(255, 235, 110), rgb(220, 40, 20)), scl=.7, emtr_life=22, gen=2,
              gen_intvl=1, radius=.15, spread=.008, alpha=(31, 31, 0), scl_anm=(.4, 1.0, 1.6, 30, 200))
    out[BREATH] = bytes(b)

    # Zaza Leaf (Razor Leaf): a big leaf behind them, leaves flung like shuriken, the haze rolling in
    b, rs = kit(LEAF)
    tex(b, 1, fxart.big_weed_leaf())
    tex(b, 0, fxart.weed_leaf())
    green = rgb(80, 200, 60)
    for res, sd in ((LEAF_E, "player"), (LEAF_P, "enemy")):
        spray(b, rs, res, sd, (10 if sd == "player" else -10, 26), (0, 18), LEAF_FRAMES, tex=0, clr=green,
              clr_anm=(rgb(140, 240, 110), rgb(40, 150, 40)), scl=1.05, emtr_life=6, gen=2, gen_intvl=1, radius=.2,
              spread=.006, alpha=(31, 31, 31), flick=0, flags_on=(1 << 14) | (1 << 12) | (1 << 13))
        rot(b, rs, res, spin=0x1C00)
    prop(b, rs, BIGLEAF, scl=1.4, life=50, scl_anm=(.2, 1.15, 1.0, 30, 255), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, BIGLEAF, spin=0x0180)
    out[LEAF] = bytes(b)
    b, rs = kit(HAZE)
    tex(b, 1, fxart.tall_puff())
    prop(b, rs, HAZE1, tex=1, clr=rgb(150, 190, 130), clr_anm=(rgb(190, 225, 170), rgb(110, 140, 100)), scl=.9,
         life=44, emtr_life=22, gen=1, gen_intvl=2, init_pos=1, radius=1.0, vel=(.006, 0), alpha=(26, 22, 0),
         scl_anm=(.5, 1.3, 2.0, 40, 150), air_resist=120, flags_on=(1 << 14) | (1 << 13))
    prop(b, rs, 0, life=1)
    out[HAZE] = bytes(b)

    # Stomp Out (Pound): the boot coming down (poses), STOMP!, dust
    poses(BOOT, fxart.work_boot(), 1.5, 14)
    b, rs = kit(STOMP)
    tex(b, 1, fxart.burst_sign(["STOMP!"]))
    tex(b, 0, fxart.soft_puff())
    prop(b, rs, 2, scl=1.2, life=28, scl_anm=(.2, 1.25, 1.0, 35, 255))
    prop(b, rs, DUST, tex=0, clr=rgb(190, 165, 120), clr_anm=(rgb(230, 210, 170), rgb(150, 125, 90)), scl=.6,
         life=24, emtr_life=2, gen=6, init_pos=1, radius=.7, vel=(.05, 0), alpha=(31, 26, 0),
         scl_anm=(.6, 1.3, 1.8, 40, 150), air_resist=116)
    out[STOMP] = bytes(b)

    # Grill Chomp (Bite): the two jaws closing (poses), sparkles off the gold
    poses(TOPJAW, fxart.jaw(True), 1.3, 8)
    poses(BOTJAW, fxart.jaw(False), 1.3, 8)
    b, rs = kit(GLITZ)
    tex(b, 0, fxart.glint())
    gold = rgb(255, 220, 80)
    prop(b, rs, SPARKLE, tex=0, clr=gold, clr_anm=(rgb(255, 255, 220), gold), scl=.5, life=14, emtr_life=2, gen=3,
         init_pos=1, radius=.8, alpha=(31, 31, 0), scl_anm=(.2, 1.4, .6, 50, 160), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, SPARKLE, spin=0x0900)
    out[GLITZ] = bytes(b)

    # Hollow Point (Crunch): a laser-sight dot settling on them, then BANG - a bullet hole punched in, sparks
    b, rs = kit(SLUG)
    tex(b, 1, fxart.bullet_hole())
    tex(b, 0, fxart.laser_dot())
    red = rgb(255, 30, 30)
    prop(b, rs, DOT, tex=0, clr=red, clr_anm=(rgb(255, 120, 120), red), scl=.55, life=SWING_STEP, flick=40)
    prop(b, rs, HOLE, scl=1.15, life=38, scl_anm=(.3, 1.15, 1.0, 20, 255))
    prop(b, rs, IMPACT, tex=0, clr=rgb(255, 230, 120), clr_anm=(rgb(255, 255, 230), rgb(255, 140, 30)), scl=.3,
         life=12, emtr_life=2, gen=8, init_pos=1, radius=.3, vel=(.09, 0), alpha=(31, 31, 0), air_resist=118,
         flags_on=(1 << 14) | (1 << 13))
    prop(b, rs, 1, life=1)
    out[SLUG] = bytes(b)

    # Switchblade (Slash): three slashes at different angles, the blade's gleam; the tire, slashed flat, hissing
    b, rs = kit(SLASH)
    tex(b, 1, fxart.slash_arc())
    tex(b, 0, fxart.glint())
    for res, ang in ((SLASH_A, 0), (SLASH_B, 0x2800), (SLASH_C, 0xD400)):
        prop(b, rs, res, scl=1.3, life=9, alpha=(31, 31, 0), scl_anm=(.6, 1.25, 1.0, 40, 255))
        rot(b, rs, res, init=ang)
    prop(b, rs, GLEAM, tex=0, clr=rgb(255, 255, 255), scl=.6, life=10, scl_anm=(.2, 1.4, .3, 50, 160),
         alpha=(31, 31, 0))
    out[SLASH] = bytes(b)
    b, rs = kit(TIRE)
    tex(b, 1, fxart.tire(), 24)
    tex(b, 0, fxart.soft_puff())
    prop(b, rs, TIRE_UP, scl=1.0, life=56)
    prop(b, rs, TIRE_FLAT, scl=1.0, life=44, scl_anm=(1.0, 1.0, .85, 0, 120))
    prop(b, rs, HISS, tex=0, clr=rgb(240, 240, 245), scl=.35, life=14, emtr_life=16, gen=2, gen_intvl=1,
         init_pos=1, radius=.3, vel=(.045, 0), alpha=(30, 24, 0), scl_anm=(.6, 1.2, 1.8, 30, 150))
    out[TIRE] = bytes(b)

    # Hot Box (SmokeScreen): smoke everywhere, wisps over the target; *cough* clouds
    b, rs = kit(SMOG)
    tex(b, 1, fxart.tall_puff())
    tex(b, 0, fxart.soft_puff())
    smoke = rgb(170, 175, 160)
    prop(b, rs, SMOG1, tex=1, clr=smoke, clr_anm=(rgb(215, 220, 205), rgb(130, 135, 125)), scl=1.3, life=64,
         emtr_life=36, gen=1, gen_intvl=2, init_pos=1, radius=2.6, vel=(.005, 0), gravity=(0, .0002, 0),
         alpha=(24, 20, 0), scl_anm=(.5, 1.4, 2.2, 40, 160), air_resist=124, flags_on=(1 << 14) | (1 << 13))
    prop(b, rs, SMOG2, tex=0, clr=smoke, clr_anm=(rgb(235, 235, 225), rgb(150, 150, 140)), scl=.6, life=30,
         emtr_life=24, gen=2, gen_intvl=2, axis=(0, 1, 0), vel=(.006, .012), init_pos=1, radius=.7,
         alpha=(28, 22, 0), scl_anm=(.5, 1.2, 1.8, 40, 150), air_resist=122)
    out[SMOG] = bytes(b)
    b, rs = kit(COUGH)
    tex(b, 1, fxart.cough_bubble(), 24)
    prop(b, rs, PUFFUP, scl=.9, life=26, axis=(0, 1, 0), vel=(0, .9 * VEL_UNITS / 4096),
         scl_anm=(.3, 1.15, 1.0, 40, 255))
    out[COUGH] = bytes(b)

    # Burnout (Flame Wheel): the flaming tire spinning in place in its own smoke, then rolling in (flown) with
    # flames trailing it (a second flown emitter dropping flames)
    b, rs = kit(WHEEL)
    tex(b, 1, fxart.flame_wheel())
    tex(b, 0, fxart.soft_puff())
    prop(b, rs, SPIN, scl=1.0, life=30, scl_anm=(.4, 1.05, 1.0, 30, 255), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, SPIN, spin=-0x2600)
    follower(b, rs, ROLL, scl=1.0, life=ROLL_FRAMES + 2, flags_on=(1 << 15) | (1 << 12))
    rot(b, rs, ROLL, spin=-0x2600)
    prop(b, rs, SMOKE1, tex=0, clr=rgb(160, 160, 165), clr_anm=(rgb(230, 230, 235), rgb(110, 110, 115)), scl=.6,
         life=26, emtr_life=28, gen=2, gen_intvl=1, axis=(0, 1, 0), vel=(.02, .02), init_pos=1, radius=.4,
         alpha=(30, 24, 0), scl_anm=(.5, 1.3, 2.0, 40, 150), air_resist=120)
    out[WHEEL] = bytes(b)
    b, rs = kit(TRAIL)
    tex(b, 1, fxart.flame_blob())
    prop(b, rs, FIRETRAIL, tex=1, clr=rgb(255, 130, 30), clr_anm=(rgb(255, 235, 110), rgb(220, 40, 20)), scl=.55,
         life=14, emtr_life=ROLL_FRAMES + 2, gen=2, gen_intvl=1, axis=(0, 1, 0), vel=(.004, .008), alpha=(31, 31, 0),
         scl_anm=(1.0, 1.0, .3, 0, 120), flags_on=0,
         flags_off=(1 << 12) | (1 << 13) | (1 << 14) | (1 << 15) | BILLBOARD)
    prop(b, rs, 0, life=1)
    out[TRAIL] = bytes(b)

    # Hi-Yah Chop (Brick Break): a stack of bricks on their head - the two halves (one art, the right half turned
    # round) as stop-motion poses so they can split apart - and a giant karate hand chopping down (poses)
    b, rs = kit(BLOCKS)
    tex(b, 1, fxart.half_stack())
    tex(b, 0, fxart.chunk())
    prop(b, rs, HALF_L, scl=1.75, life=SWING_STEP)
    prop(b, rs, HALF_R, scl=1.75, life=SWING_STEP)
    rot(b, rs, HALF_R, init=0x8000)
    brick = rgb(190, 70, 50)
    prop(b, rs, CHUNKS, tex=0, clr=brick, clr_anm=(rgb(220, 110, 85), rgb(140, 45, 30)), scl=.5, life=30,
         emtr_life=2, gen=7, init_pos=1, radius=.5, axis=(0, 1, 0), vel=(.07, .05), gravity=(0, -.003, 0),
         air_resist=126, flags_on=(1 << 14) | (1 << 12) | (1 << 13))
    rot(b, rs, CHUNKS, spin=0x1400)
    prop(b, rs, 1, life=1)
    out[BLOCKS] = bytes(b)
    poses(CHOP, fxart.big_hand(), 1.5, 16)
    sign(HIYAH, ["HI-YAH!"], fill=(255, 140, 30, 255))

    # Magic 8-Ball (Shadow Ball): the ball growing in their hands in dark wisps, rolling over (flown), the answer
    b, rs = kit(EIGHT)
    tex(b, 1, fxart.eight_ball())
    tex(b, 0, fxart.soft_puff())
    prop(b, rs, CHARGE, scl=1.0, life=20, scl_anm=(.2, 1.0, 1.0, 120, 255))
    follower(b, rs, ROLL8, scl=1.0, life=EIGHT_FRAMES + 2, flags_on=(1 << 15) | (1 << 12))
    rot(b, rs, ROLL8, spin=-0x0C00)
    prop(b, rs, WISPS, tex=0, clr=rgb(90, 40, 140), clr_anm=(rgb(150, 90, 210), rgb(40, 10, 70)), scl=.55, life=22,
         emtr_life=20, gen=2, gen_intvl=1, axis=(0, 1, 0), vel=(.012, .02), init_pos=1, radius=.6,
         alpha=(28, 22, 0), scl_anm=(.5, 1.2, 1.6, 40, 150), air_resist=122)
    out[EIGHT] = bytes(b)
    b, rs = kit(ANSWER)
    tex(b, 0, fxart.eight_answer(), 30)
    prop(b, rs, POP, scl=1.3, life=44, scl_anm=(.2, 1.15, 1.0, 30, 255))
    out[ANSWER] = bytes(b)

    # Loyalty (Return): the RIDE OR DIE pendant glowing, hearts flying, the pendant slamming in (flown)
    b, rs = kit(HEART)
    tex(b, 1, fxart.heart_pendant())
    tex(b, 0, fxart.heart())
    prop(b, rs, LOCKET, scl=1.1, life=30, scl_anm=(.3, 1.2, 1.0, 30, 255))
    follower(b, rs, SLAM, scl=1.2, life=HEART_FRAMES + 2)
    pink = rgb(255, 90, 150)
    for res, sd in ((HEARTS_E, "player"), (HEARTS_P, "enemy")):
        spray(b, rs, res, sd, (10 if sd == "player" else -10, 30), (0, 18), HEART_FRAMES, tex=0, clr=pink,
              clr_anm=(rgb(255, 170, 200), rgb(230, 40, 110)), scl=.5, emtr_life=8, gen=2, gen_intvl=1,
              radius=.2, spread=.01, alpha=(31, 31, 31), flick=0)
    out[HEART] = bytes(b)

    # ---- set 5 ---------------------------------------------------------------------------------------------
    FIXED_ROT = (1 << 12) | (1 << 13)                         # flags_off for sprays whose rotation is set by hand

    # Flashlight (Confuse Ray): a big flashlight aimed at their eyes, the beam, dizzy swirls, HUH?!
    b, rs = kit(TORCH)
    tex(b, 1, fxart.flashlight())
    tex(b, 0, fxart.dizzy_swirl())
    for res, sd in ((TORCH_E, "player"), (TORCH_P, "enemy")):
        prop(b, rs, res, scl=TORCH_SCALE, life=62, scl_anm=(.4, 1.1, 1.0, 30, 255))
        rot(b, rs, res, init=torch_geometry(sd)[0])
    violet = rgb(200, 90, 255)
    prop(b, rs, SWIRL, tex=0, clr=violet, clr_anm=(rgb(255, 170, 255), rgb(140, 40, 220)), scl=.42, life=40,
         scl_anm=(.3, 1.2, 1.0, 40, 255), flags_on=(1 << 14) | (1 << 12))
    rot(b, rs, SWIRL, spin=-0x1400)
    prop(b, rs, 3, life=1)
    out[TORCH] = bytes(b)
    b, rs = kit(BEAM)
    tex(b, 0, fxart.light_cone(), 30)
    for res, sd in ((BEAM_E, "player"), (BEAM_P, "enemy")):
        ang, _, _, scale = torch_geometry(sd)
        prop(b, rs, res, scl=scale, life=48, flick=50)
        rot(b, rs, res, init=ang)
    out[BEAM] = bytes(b)
    sign(HUH, ["HUH?!"], fill=(170, 90, 255, 255), text=(255, 235, 60, 255))

    # Stun Taser (Thunder Wave): the stun gun snapping, crackles shot at them, rings of static locking them up
    b, rs = kit(STUN)
    tex(b, 1, fxart.stun_gun())
    tex(b, 0, fxart.crackle())
    prop(b, rs, STUN_E, scl=1.1, life=50, scl_anm=(.4, 1.1, 1.0, 30, 255))
    prop(b, rs, STUN_P, scl=1.1, life=50, scl_anm=(.4, 1.1, 1.0, 30, 255))
    rot(b, rs, STUN_P, init=0x8000)
    cyan = rgb(120, 220, 255)
    for res, sd in ((ARC_E, "player"), (ARC_P, "enemy")):
        spray(b, rs, res, sd, STUN_TIP[sd], (0, 22), STUN_FRAMES, tex=0, clr=cyan,
              clr_anm=(rgb(200, 240, 255), rgb(40, 110, 255)), scl=.3, emtr_life=8, gen=1, gen_intvl=1, radius=.2,
              spread=.02, alpha=(31, 31, 31), scl_anm=(1.0, 1.0, 1.0, 0, 255), flick=60,
              flags_on=(1 << 14) | (1 << 13))
    out[STUN] = bytes(b)
    b, rs = kit(STATIC)
    tex(b, 0, fxart.static_ring(), 30)
    prop(b, rs, RING_X, scl=1.5, life=14, scl_anm=(.3, 1.2, 1.6, 90, 200), alpha=(31, 31, 0))
    prop(b, rs, RING_HOLD, scl=1.3, life=44, flick=110)
    out[STATIC] = bytes(b)
    sign(ZZZT, ["ZZZT!"], fill=(80, 200, 255, 255), text=(255, 240, 40, 255))

    # Bass Boost (Supersonic): a boombox on their shoulder, pumping - sound waves and notes rattle their skull
    b, rs = kit(BOOMBOX)
    tex(b, 1, fxart.boombox())
    tex(b, 0, fxart.music_note())
    prop(b, rs, BOX5, scl=1.2, life=64, scl_anm=(.3, 1.1, 1.0, 30, 255))
    prop(b, rs, THUMP, scl=1.2, life=6, scl_anm=(1.0, 1.2, 1.0, 90, 170))
    pink = rgb(255, 110, 210)
    for res, sd in ((NOTES_E, "player"), (NOTES_P, "enemy")):
        spray(b, rs, res, sd, BOX_AT[sd], BEAT_AIM, NOTE_FRAMES, tex=0, clr=pink,
              clr_anm=(rgb(255, 230, 120), rgb(255, 80, 200)), scl=.5, emtr_life=4, gen=1, gen_intvl=2, radius=.3,
              spread=.012, alpha=(31, 31, 31), scl_anm=(.6, 1.1, 1.0, 40, 255), flick=0,
              flags_off=(1 << 15) | BILLBOARD | FIXED_ROT)
    out[BOOMBOX] = bytes(b)
    b, rs = kit(SOUNDWAVE)
    tex(b, 1, fxart.sound_arc())
    for res, sd in ((SWAVE_E, "player"), (SWAVE_P, "enemy")):
        spray(b, rs, res, sd, BOX_AT[sd], BEAT_AIM, NOTE_FRAMES - 2, tex=1, clr=rgb(255, 120, 220),
              clr_anm=(rgb(255, 255, 255), rgb(240, 60, 200)), scl=1.0, emtr_life=5, gen=1, gen_intvl=2, radius=0,
              alpha=(31, 31, 18), scl_anm=(.5, 1.3, 1.6, 60, 200), flick=0, flags_off=(1 << 15) | BILLBOARD | FIXED_ROT)
        rot(b, rs, res, init=_angle(*aim_path(sd, BOX_AT[sd], BEAT_AIM)))
    out[SOUNDWAVE] = bytes(b)
    sign(BWOMP, ["BWOMP!"], fill=(255, 80, 200, 255), text=(255, 255, 255, 255))

    # Squad Up (Double Team): the homies pop out of nowhere, one after another
    b, rs = kit(SQUAD)
    tex(b, 1, fxart.squad_hoodie())
    tex(b, 0, fxart.soft_puff())
    prop(b, rs, FIG, scl=1.45, life=56, scl_anm=(.3, 1.1, 1.0, 30, 255))
    prop(b, rs, FIG_S, scl=1.0, life=56, scl_anm=(.3, 1.1, 1.0, 30, 255))
    prop(b, rs, POOF, tex=0, clr=rgb(170, 150, 210), clr_anm=(rgb(240, 230, 255), rgb(110, 90, 150)), scl=.5, life=20,
         emtr_life=2, gen=5, init_pos=1, radius=.6, vel=(.04, 0), alpha=(30, 24, 0), scl_anm=(.6, 1.3, 1.8, 40, 150),
         air_resist=116)
    prop(b, rs, 3, life=1)
    out[SQUAD] = bytes(b)
    b, rs = kit(SQUAD2)
    tex(b, 0, fxart.squad_cap(), 30)
    prop(b, rs, FIG2, scl=1.45, life=56, scl_anm=(.3, 1.1, 1.0, 30, 255))
    prop(b, rs, FIG2_S, scl=1.0, life=56, scl_anm=(.3, 1.1, 1.0, 30, 255))
    out[SQUAD2] = bytes(b)
    sign(SQUADUP, ["SQUAD", "UP!"], fill=(150, 90, 240, 255), text=(255, 220, 40, 255))

    # Water Bomb (Water Pulse): a water balloon lobbed - SPLOOSH - and they're dripping
    b, rs = kit(BALLOON)
    tex(b, 1, fxart.water_balloon(), 24)
    tex(b, 0, fxart.droplet())
    thrown(b, rs, .85, 0x0700)
    water = rgb(80, 160, 255)
    prop(b, rs, DROPS, tex=0, clr=water, clr_anm=(rgb(200, 235, 255), water), scl=.25, life=20, emtr_life=30, gen=1,
         gen_intvl=3, init_pos=1, radius=.7, axis=(0, -1, 0), vel=(0, .025), alpha=(31, 31, 0))
    prop(b, rs, 0, life=1)
    out[BALLOON] = bytes(b)
    b, rs = kit(DRENCH)
    tex(b, 1, fxart.splash_crown())
    tex(b, 0, fxart.droplet())
    prop(b, rs, CROWN, scl=1.7, life=26, scl_anm=(.3, 1.15, 1.0, 25, 255), alpha=(31, 31, 0))
    prop(b, rs, SPLASHDROPS, tex=0, clr=water, clr_anm=(rgb(220, 240, 255), water), scl=.3, life=26, emtr_life=2,
         gen=8, init_pos=1, radius=.4, axis=(0, 1, 0), vel=(.06, .05), gravity=(0, -.004, 0), air_resist=126)
    for res in (2, 3):
        prop(b, rs, res, life=1)
    out[DRENCH] = bytes(b)
    sign(SPLOOSH, ["SPLOOSH!"], fill=(60, 150, 255, 255), text=(255, 255, 255, 255))

    # Sneak Diss (Faint Attack): they vanish, "UR MID" pops up behind the target, and a palm comes down. OOOOH!
    b, rs = kit(DISS)
    tex(b, 0, fxart.diss_bubble(), 30)
    prop(b, rs, POP, scl=1.3, life=40, scl_anm=(.2, 1.15, 1.0, 30, 255))
    out[DISS] = bytes(b)
    b, rs = kit(SLAP)
    tex(b, 1, fxart.slap_hand())
    tex(b, 0, fxart.pow_lines())
    prop(b, rs, SLAP_POSE, scl=1.35, life=SWING_STEP)
    prop(b, rs, SLAP_HOLD, scl=1.35, life=12)
    prop(b, rs, POWS, tex=0, clr=rgb(255, 255, 255), clr_anm=(rgb(255, 255, 255), rgb(255, 220, 80)), scl=.9,
         life=10, scl_anm=(.5, 1.3, 1.5, 60, 200), alpha=(31, 31, 0))
    prop(b, rs, 3, life=1)
    out[SLAP] = bytes(b)
    sign(OOOH, ["OOOOH!"], fill=(255, 140, 30, 255), text=(255, 255, 255, 255))

    # Dirty Sprite (Toxic): a double cup of purple drank, thrown - it splashes all over them and they're bubbling
    b, rs = kit(CUP)
    tex(b, 1, fxart.double_cup(), 24)
    tex(b, 0, fxart.bubble())
    prop(b, rs, HELD, scl=1.0, life=16, scl_anm=(.4, 1.1, 1.0, 30, 255))
    thrown(b, rs, .9, 0x0900)
    drank = rgb(170, 70, 235)
    prop(b, rs, BUBBLES, tex=0, clr=drank, clr_anm=(rgb(230, 170, 255), rgb(120, 30, 190)), scl=.35, life=24,
         emtr_life=34, gen=1, gen_intvl=2, init_pos=1, radius=.8, axis=(0, 1, 0), vel=(.008, .03),
         scl_anm=(.4, 1.1, 1.3, 50, 200), alpha=(31, 31, 0), air_resist=126)
    out[CUP] = bytes(b)
    b, rs = kit(GOOP)
    tex(b, 1, fxart.goop())
    prop(b, rs, GOOP_SPLAT, tex=1, clr=drank, clr_anm=(rgb(220, 150, 255), drank), scl=.55, life=40, emtr_life=2,
         gen=2, init_pos=1, radius=.4, axis=(0, 1, 0), vel=(.006, 0), gravity=(0, -.0003, 0),
         scl_anm=(.4, 1.2, 1.0, 30, 200), air_resist=110)
    prop(b, rs, GOOP_DRIPS, tex=1, clr=drank, clr_anm=(rgb(220, 150, 255), rgb(110, 30, 170)), scl=.4, life=30,
         emtr_life=10, gen=1, gen_intvl=2, init_pos=1, radius=.8, axis=(0, -1, 0), vel=(.004, .008),
         gravity=(0, -.0008, 0), air_resist=120)
    out[GOOP] = bytes(b)
    sign(DIRTY, ["DIRTY!"], fill=(150, 60, 220, 255), text=(120, 255, 90, 255))

    # Duck n Cover (Protect): they duck behind a trash-can lid - everything pings off it. NOPE.
    b, rs = kit(LID)
    tex(b, 1, fxart.trash_lid())
    tex(b, 0, fxart.ping())
    prop(b, rs, LIDUP, scl=1.35, life=56, scl_anm=(.3, 1.15, 1.0, 25, 255))
    prop(b, rs, LIDFLASH, scl=1.35, life=10, scl_anm=(1.0, 1.3, 1.5, 0, 120), alpha=(26, 16, 0))
    prop(b, rs, PINGS, tex=0, clr=rgb(255, 255, 200), clr_anm=(rgb(255, 255, 255), rgb(255, 210, 60)), scl=.45,
         life=10, emtr_life=1, gen=1, scl_anm=(.3, 1.4, .6, 50, 160), alpha=(31, 31, 0))
    prop(b, rs, 3, life=1)
    out[LID] = bytes(b)
    sign(NOPE, ["NOPE."], fill=(110, 200, 255, 255), text=(225, 25, 25, 255))

    # Smackdown (Take Down): they charge in with a folding chair - CLANG - and see stars from the recoil
    b, rs = kit(CHAIR)
    tex(b, 1, fxart.folding_chair())
    tex(b, 0, fxart.star5())
    prop(b, rs, CHAIR_POSE, scl=1.5, life=SWING_STEP)
    prop(b, rs, CHAIR_HOLD, scl=1.5, life=12)
    prop(b, rs, STARS, tex=0, clr=rgb(255, 230, 60), clr_anm=(rgb(255, 255, 200), rgb(255, 200, 30)), scl=.35,
         life=7, alpha=(31, 31, 31))
    prop(b, rs, 3, life=1)
    out[CHAIR] = bytes(b)
    b, rs = kit(CLANG)
    tex(b, 0, fxart.impact_burst(), 30)
    prop(b, rs, POP, scl=1.6, life=12, scl_anm=(.3, 1.2, 1.0, 40, 255), alpha=(31, 31, 0))
    out[CLANG] = bytes(b)
    sign(SMACKDN, ["SMACK", "DOWN!"], fill=(230, 30, 30, 255), text=(255, 230, 40, 255))

    # Big Taser (Thunderbolt): an XL taser held high, crackling - then a giant bolt drops out of the sky on them
    b, rs = kit(BIGTASER)
    tex(b, 1, fxart.big_taser())
    tex(b, 0, fxart.zigzag())
    prop(b, rs, BIG_E, scl=1.4, life=52, scl_anm=(.3, 1.1, 1.0, 30, 255))
    prop(b, rs, BIG_P, scl=1.4, life=52, scl_anm=(.3, 1.1, 1.0, 30, 255))
    rot(b, rs, BIG_P, init=0x8000)
    prop(b, rs, ZIGS, tex=0, clr=rgb(255, 240, 80), clr_anm=(rgb(255, 255, 255), rgb(120, 200, 255)), scl=.45,
         life=4, emtr_life=24, gen=2, init_pos=1, radius=.9, alpha=(31, 31, 31), flags_on=(1 << 14) | (1 << 13))
    prop(b, rs, 3, life=1)
    out[BIGTASER] = bytes(b)
    b, rs = kit(MEGABOLT)
    tex(b, 0, fxart.mega_bolt(), 30)
    prop(b, rs, STRIKE, scl=2.2, life=24, flick=90)
    prop(b, rs, STRIKE2, scl=1.5, life=10, flick=140)
    rot(b, rs, STRIKE2, init=0x0E00)
    out[MEGABOLT] = bytes(b)
    sign(BZZT, ["BZZZT!!"], fill=(255, 225, 30, 255), text=(40, 60, 230, 255))

    # Clock It (Foresight): side-eye... then the thumbnail red circle and arrow on them. U GOT CLOCKED
    b, rs = kit(EYES)
    tex(b, 1, fxart.side_eye())
    prop(b, rs, EYES_R, scl=1.2, life=6)
    prop(b, rs, EYES_L, scl=1.2, life=6)
    rot(b, rs, EYES_L, init=0x8000)
    for res in (0, 3):
        prop(b, rs, res, life=1)
    out[EYES] = bytes(b)
    b, rs = kit(CIRCLE)
    tex(b, 0, fxart.clocked_circle(), 30)
    prop(b, rs, POP, scl=2.0, life=46, scl_anm=(1.6, .95, 1.0, 20, 255))
    out[CIRCLE] = bytes(b)
    sign(CLOCKED, ["U GOT", "CLOCKED"], fill=(255, 255, 255, 255), text=(230, 20, 20, 255))
    # the donors tile their small textures 2x2 (or 2x1) mirrored - quarters of a shape; set 5's are whole shapes
    for ps in range(TORCH, CLOCKED + 1):
        b = bytearray(out[ps])
        for r in spa.resources(bytes(b)):
            b[r["off"] + TILE] &= 0xF0
        out[ps] = bytes(b)

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
                    (WIND, GUST_E), (WIND, GUST_P),
                    (PLANE, PASS), (PLANE, DIVE_E), (PLANE, DIVE_P), (PLANE, JETSMOKE), (WHAM, POP), (WAVE, WAVE_E),
                    (WAVE, WAVE_P), (WAVE, FOAM), (DUCK, DUCK_E), (DUCK, DUCK_P), (CABLE, POSE), (CABLE, HOLD),
                    (XRAY, BONES), (XRAY, SPARKS), (HONK, HONK_A), (HONK, HONK_B), (HONK, STEAM), (BOOZE, SWIG),
                    (BOOZE, LIGHTER), (BREATH, FIRE_E), (BREATH, FIRE_P), (LEAF, LEAF_E), (LEAF, LEAF_P),
                    (LEAF, BIGLEAF), (HAZE, HAZE1), (BOOT, POSE), (BOOT, HOLD), (STOMP, 2), (STOMP, DUST),
                    (TOPJAW, POSE), (TOPJAW, HOLD), (BOTJAW, POSE), (BOTJAW, HOLD), (GLITZ, SPARKLE),
                    (SLUG, DOT), (SLUG, HOLE), (SLUG, IMPACT), (SLASH, SLASH_A), (SLASH, SLASH_B), (SLASH, SLASH_C), (SLASH, GLEAM),
                    (TIRE, TIRE_UP), (TIRE, TIRE_FLAT), (TIRE, HISS), (SMOG, SMOG1), (SMOG, SMOG2), (COUGH, PUFFUP),
                    (WHEEL, SPIN), (WHEEL, SMOKE1), (BLOCKS, HALF_L), (BLOCKS, HALF_R), (BLOCKS, CHUNKS), (CHOP, POSE), (CHOP, HOLD), (HIYAH, POP),
                    (EIGHT, CHARGE), (EIGHT, WISPS), (ANSWER, POP), (HEART, LOCKET), (HEART, HEARTS_E),
                    (HEART, HEARTS_P),
                    (TORCH, TORCH_E), (TORCH, TORCH_P), (TORCH, SWIRL), (BEAM, BEAM_E), (BEAM, BEAM_P), (HUH, POP),
                    (STUN, STUN_E), (STUN, STUN_P), (STUN, ARC_E), (STUN, ARC_P), (STATIC, RING_X),
                    (STATIC, RING_HOLD), (ZZZT, POP), (BOOMBOX, BOX5), (BOOMBOX, THUMP), (BOOMBOX, NOTES_E),
                    (BOOMBOX, NOTES_P), (SOUNDWAVE, SWAVE_E), (SOUNDWAVE, SWAVE_P), (BWOMP, POP), (SQUAD, FIG),
                    (SQUAD, FIG_S), (SQUAD, POOF), (SQUAD2, FIG2), (SQUAD2, FIG2_S), (SQUADUP, POP),
                    (BALLOON, DROPS), (DRENCH, CROWN), (DRENCH, SPLASHDROPS), (SPLOOSH, POP), (DISS, POP),
                    (SLAP, SLAP_POSE), (SLAP, SLAP_HOLD), (SLAP, POWS), (OOOH, POP), (CUP, HELD), (CUP, BUBBLES),
                    (GOOP, GOOP_SPLAT), (GOOP, GOOP_DRIPS), (DIRTY, POP), (LID, LIDUP), (LID, LIDFLASH),
                    (LID, PINGS), (NOPE, POP), (CHAIR, CHAIR_POSE), (CHAIR, CHAIR_HOLD), (CHAIR, STARS),
                    (CLANG, POP), (SMACKDN, POP), (BIGTASER, BIG_E), (BIGTASER, BIG_P), (BIGTASER, ZIGS),
                    (MEGABOLT, STRIKE), (MEGABOLT, STRIKE2), (BZZT, POP), (EYES, EYES_R), (EYES, EYES_L),
                    (CIRCLE, POP), (CLOCKED, POP)):
        flag = spa.resources(out[ps])[res]["flag"]
        assert flag >> 14 & 1, f"kit {ps} emitter {res} never finishes (no self_dest): WaitForParticles would hang"
    for ps, res in ((GUN, TRACER), (BOTTLE, THROWN), (BRICK, THROWN), (EGG, THROWN), (BUBBLE, TALK),
                    (CONE, THROWN), (BOOZE, THROWN),
                    (WHEEL, ROLL), (TRAIL, FIRETRAIL), (EIGHT, ROLL8), (HEART, SLAM),
                    (BALLOON, THROWN), (CUP, THROWN)):
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
    """Emitter at the attacker (who=0) or defender (who=1) plus an offset in screen pixels (y up).
    (Particles always draw over the Pokémon: their sprites sit at the back of the depth range and draw first, as
    opaque polygons - no depth or alpha puts a particle behind one.)"""
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


def _fly_turn2_first(side, s):
    """Test only (the showcase always plays variant 0): Catch Flight with the turns swapped, to see turn 2."""
    one, two = _catch_flight(side, s)
    return two, one


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


def bmove(side, role, frames, right, up):
    """MoveBattlerBy in screen px (right, up). The game mirrors moves for battlers on the enemy side."""
    on_player_side = (side == "player") == (role == 258)
    dx, dy = (right, -up) if on_player_side else (-right, up)
    return func(57, frames, dx, dy, role)


def stop_motion(ps, pose, who, start, end, steps, ease=1.6):
    """One short-lived pose per step from start to end (screen px), easing in."""
    w = []
    for k in range(steps):
        t = (k / (steps - 1)) ** ease
        w += emit_at(ps, pose, who, (round(start[0] + (end[0] - start[0]) * t),
                                     round(start[1] + (end[1] - start[1]) * t))) + wait(1)
    return w


def _catch_flight(side, s):
    """Fly (two turns). Turn 1: HOOD AIR swoops in low, they grab the rope ladder and get carried off. Turn 2: the jet
    dive-bombs the target - WHAM! - and they drop back in from the sky."""
    sx = 1 if side == "player" else -1
    # the jet swoops in low; when the ladder reaches them they grab on and get carried off at its speed
    one = se(s["jet"]) + emit_at(PLANE, PASS, 0, PICKUP_FROM)
    one += wait_frames((-PICKUP_FROM[0] - LADDER_X) / JET_SPEED - 2)
    one += se(s["whoosh"]) + bmove(side, 258, CARRY_FRAMES, JET_SPEED * CARRY_FRAMES, 6) + wait(22)
    one += func(40, 2, 1)                                                    # ...gone (SetBattlerVanished)
    dive = DIVE_E if side == "player" else DIVE_P
    two = se(s["whoosh"]) + emit_at(PLANE, dive, 1, (-sx * DIVE_FROM[0], DIVE_FROM[1])) + wait_frames(DIVE_FRAMES)
    two += emit_at(WHAM, POP, 1, (sx * -18, 46)) + emit_at(PLANE, JETSMOKE, 1, (0, 10)) + flash_screen(8)
    two += se(s["bonk"]) + shake_defender(5, 4) + func(48) + func(68, 5, 2, 1, 4, 0) + wait(12)
    two += bmove(side, 258, 1, 0, 150) + wait(1) + func(40, 2, 0)            # back in, from the sky
    two += bmove(side, 258, 10, 0, -150) + wait(12)
    return one, two


def _hydrant_wave(side, s):
    """Surf: the whole block floods - a wall of water the height of the screen sweeps across both of them,
    a rubber duck riding the crest."""
    blue = rgb(40, 90, 220)
    fx, fy = WAVE_FROM[side]
    sx = 1 if side == "player" else -1
    wave = WAVE_E if side == "player" else WAVE_P
    duck = DUCK_E if side == "player" else DUCK_P
    w = func(33, 0, 1, 0, 10, blue) + se(s["surf"]) + wait(2)
    w += emit_at(WAVE, wave, 1, (fx, fy)) + emit_at(DUCK, duck, 1, (fx - sx * 20, fy + 56)) + wait(5)
    w += emit_at(WAVE, wave, 1, (fx, fy - 26)) + se(s["surf"])
    w += wait_frames(abs(fx) / WAVE_SPEED - 30)
    w += se(s["splash"]) + emit_at(WAVE, FOAM, 1, (0, 10)) + emit_at(WAVE, FOAM, 0, (0, 10))
    w += func(34, 8, 0, 2, blue, 14, 0) + shake_defender(3, 6) + func(68, 3, 2, 1, 4, 0) + wait(8)
    w += emit_at(WAVE, FOAM, 1, (-10, 4)) + se(s["splash"]) + wait(20)
    w += func(33, 0, 1, 10, 0, blue) + wait(6)
    return w


def _power_line(side, s):
    """Thunder: a live power line snaps, swings down on the target and lights them up - you can see the skeleton."""
    night = rgb(10, 10, 40)
    w = func(33, 0, 1, 0, 12, night) + wait(4)
    w += stop_motion(CABLE, POSE, 1, (10, 110), (10, 34), 7)
    w += emit_at(CABLE, HOLD, 1, (10, 34))
    w += se(s["thunder"]) + flash_screen(6) + emit_at(XRAY, SPARKS, 1, (0, 22)) + emit_at(XRAY, BONES, 1, (0, 18))
    for k in range(8):                                                       # BZZZZT
        w += func(34, 3, 0, 1, rgb(0, 0, 0) if k % 2 == 0 else rgb(255, 250, 120), 16, 0)
        w += func(36, 2, 1, 1, 2, 264) + wait(2)
        if k % 3 == 0:
            w += flash_screen(2)
        if k == 4:
            w += se(s["thunder"])
    w += wait(8) + func(33, 0, 1, 12, 0, night) + wait(6)
    return w


def _road_rage(side, s):
    """Dragon Rage: they go red, steam blasting out, HONK! HONK! - and start launching traffic cones."""
    sx = 1 if side == "player" else -1
    w = func(34, 2, 0, 1, rgb(255, 30, 30), 15, 0) + shake_attacker(2, 18)
    w += emit_at(HONK, STEAM, 0, (sx * 6, 36)) + se(s["rage"]) + wait(6)
    w += se(s["alarm"]) + emit_at(HONK, HONK_A, 0, (sx * 34, 54)) + wait(8)
    w += se(s["alarm"]) + emit_at(HONK, HONK_B, 0, (sx * -8, 62)) + wait(6)
    for k in range(3):                                                       # cones, cones, cones
        w += func(9) + _throw(CONE, 1 + k, ((-10, 10, 0)[k], (6, 2, 14)[k])) + wait(4)
    w += wait_frames(THROW_FRAMES - 16)
    for k in range(3):
        w += se(s["bonk"]) + shake_defender(3, 2) + func(34, 4, 0, 1, rgb(255, 140, 40), 10, 0) + wait(4)
    return w + wait(10)


def _molotov2(side, s):
    """Flamethrower (Molotov): a swig of the good stuff, sprayed through a lighter - then the bottle's lobbed."""
    sx = 1 if side == "player" else -1
    orange = rgb(255, 120, 20)
    fire = FIRE_E if side == "player" else FIRE_P
    w = emit_at(BOOZE, SWIG, 0, (sx * 12, 34)) + func(19) + wait(12)          # glug glug
    w += emit_at(BOOZE, LIGHTER, 0, (sx * 22, 26)) + se(s["fwoosh"]) + wait(5)  # *flick*
    w += se(s["flame"]) + emit_at(BREATH, fire, 0, (0, 0)) + func(9) + wait(10)
    w += emit_at(BREATH, fire, 0, (0, 0)) + func(34, 8, 0, 2, orange, 14, 0) + shake_defender(2, 8) + wait(12)
    w += _throw(BOOZE, 1, (0, 4)) + wait_frames(THROW_FRAMES)                 # and the bottle
    w += se(s["smash"]) + emit_at(BURST, TONGUE, 1, (0, -6)) + emit_at(BURST, EMBER, 1, (0, 4)) + flash_screen(6)
    w += shake_defender(4, 4) + func(48) + wait(16)
    return w


def _zaza_leaf(side, s):
    """Razor Leaf (Zaza Leaf): the big leaf rises behind them, the leaves fly like shuriken - and the target's zooted."""
    sx = 1 if side == "player" else -1
    leaf = LEAF_E if side == "player" else LEAF_P
    w = emit_at(LEAF, BIGLEAF, 0, (sx * -16, 42)) + se(s["leaf"]) + wait(10)
    for k in range(3):
        w += se(s["razor"]) + emit_at(LEAF, leaf, 0, (0, 4 * k - 4)) + wait(4)
    w += wait_frames(LEAF_FRAMES - 8)
    w += func(34, 8, 0, 2, rgb(80, 200, 60), 12, 0) + shake_defender(2, 4) + emit_at(HAZE, HAZE1, 1, (0, 16))
    w += wait(6) + func(4, 0, 0x0600, 16, 0) + wait(16)                      # ...whoa
    w += func(4, 0, 0x0600, 16, 2) + wait(18)
    return w


def _stomp_out(side, s):
    """Pound (Stomp Out): a giant boot comes down out of the sky. STOMP!"""
    sx = 1 if side == "player" else -1
    w = stop_motion(BOOT, POSE, 1, (0, 120), (0, 30), 6)
    w += emit_at(BOOT, HOLD, 1, (0, 30))
    w += se(s["bonk"]) + emit_at(STOMP, 2, 1, (sx * -30, 56)) + emit_at(STOMP, DUST, 1, (0, -8))
    w += func(68, 4, 2, 1, 3, 0) + shake_defender(4, 3) + bmove(side, 264, 3, 0, -8) + wait(10)
    w += bmove(side, 264, 8, 0, 8) + wait(10)
    return w


def _grill_chomp(side, s):
    """Bite (Grill Chomp): a mouth full of gold grillz chomps down on them. Twice."""
    w = []
    for chomp in range(2):
        for k in range(4):                                                   # jaws closing
            w += emit_at(TOPJAW, POSE, 1, (0, 50 - 5 * k)) + emit_at(BOTJAW, POSE, 1, (0, -14 + 5 * k)) + wait(1)
        w += emit_at(TOPJAW, HOLD, 1, (0, 32)) + emit_at(BOTJAW, HOLD, 1, (0, 4))
        w += se(s["bite"]) + flash_screen(3) + shake_defender(3, 3) + emit_at(GLITZ, SPARKLE, 1, (0, 18))
        w += func(34, 4, 0, 1, rgb(255, 60, 60), 12, 0) + wait(6)
    return w + wait(8)


def _hollow_point(side, s):
    """Crunch (Hollow Point): a red laser-sight dot dances over them... settles dead centre... BANG."""
    import random
    rnd = random.Random(7)
    w = se(s["leer"])
    for k in range(12):                                                      # the dot hunting, then settling
        a = 20 * (1 - k / 11) ** 1.5
        w += emit_at(SLUG, DOT, 1, (round(rnd.uniform(-a, a)), 22 + round(rnd.uniform(-a, a)))) + wait(1)
    for k in range(4):                                                       # locked on. hold it...
        w += emit_at(SLUG, DOT, 1, (0, 22)) + wait(1)
    w += se(s["boom"]) + muzzle(GUN, FLASH, side) + flash_screen(10)         # BANG
    w += emit_at(SLUG, HOLE, 1, (0, 22)) + emit_at(SLUG, IMPACT, 1, (0, 22)) + emit_at(GUN, SPARK, 1, (0, 22))
    w += se(s["crunch"]) + func(48) + shake_defender(6, 4) + func(68, 5, 3, 1, 4, 0)
    w += func(34, 8, 0, 2, rgb(255, 50, 50), 13, 0) + wait(18)
    return w


def _switchblade(side, s):
    """Slash (Switchblade): the blade flicks open, they dash in - slash, slash, slash - and slash the tire too."""
    sx = 1 if side == "player" else -1
    tire = (sx * 34, -4)
    w = emit_at(TIRE, TIRE_UP, 1, tire) + emit_at(SLASH, GLEAM, 0, (sx * 16, 26)) + se(s["bling"]) + wait(8)
    w += bmove(side, 258, 6, 60, 30) + wait(7)                               # dash in
    for k, res in enumerate((SLASH_A, SLASH_B, SLASH_C)):
        w += se(s["slash"]) + emit_at(SLASH, res, 1, ((-4, 4, 0)[k], (20, 14, 18)[k])) + shake_defender(2, 2)
        w += func(34, 3, 0, 1, rgb(255, 60, 60), 10, 0) + wait(3)
    w += se(s["slash"]) + emit_at(SLASH, SLASH_B, 1, tire) + wait(2)          # ...and the tire
    w += emit_at(TIRE, TIRE_FLAT, 1, (tire[0], tire[1] - 3)) + emit_at(TIRE, HISS, 1, tire) + se(s["spray"])
    w += bmove(side, 258, 8, -60, -30) + wait(14)
    return w


def _hot_box(side, s):
    """SmokeScreen (Hot Box): they hotbox the whole battlefield. Can't see a thing. *cough* *cough*"""
    sx = 1 if side == "player" else -1
    haze = rgb(110, 120, 100)
    w = func(33, 0, 1, 0, 11, haze) + se(s["smoke"]) + emit_at(SMOG, SMOG1, 0, (sx * 24, 24)) + wait(8)
    w += emit_at(SMOG, SMOG1, 1, (0, 20)) + emit_at(SMOG, SMOG2, 1, (0, 10)) + wait(10)
    for k in range(3):
        w += emit_at(COUGH, PUFFUP, 1, ((k - 1) * 14, 42 + (k % 2) * 6)) + se(s["cough"])
        w += shake_defender(2, 3) + func(34, 4, 0, 1, rgb(170, 175, 160), 12, 0) + wait(8)
    w += wait(12) + func(33, 0, 1, 11, 0, haze) + wait(6)
    return w


def _burnout(side, s):
    """Flame Wheel (Burnout): the tire spins in place in a cloud of smoke and catches fire - then it's launched."""
    sx = 1 if side == "player" else -1
    at = (sx * 22, 10)
    w = emit_at(WHEEL, SPIN, 0, at) + emit_at(WHEEL, SMOKE1, 0, at) + se(s["burn"]) + shake_attacker(1, 14)
    w += wait(14)
    w += se(s["burn2"]) + _fly(WHEEL, ROLL, 1, ROLL_FRAMES) + _fly(TRAIL, FIRETRAIL, 2, ROLL_FRAMES)
    w += wait_frames(ROLL_FRAMES)
    w += emit_at(BURST, TONGUE, 1, (0, -6)) + emit_at(BURST, EMBER, 1, (0, 4)) + se(s["fwoosh"])
    w += func(34, 8, 0, 2, rgb(255, 120, 20), 14, 0) + shake_defender(4, 4) + func(48) + wait(16)
    return w


def _hi_yah(side, s):
    """Brick Break (Hi-Yah Chop): a stack of bricks balanced on their head; a giant karate hand comes down -
    HI-YAH! - the stack splits clean in two and the chop lands on their head."""
    sx = 1 if side == "player" else -1
    top = 48                                                                 # the stack, on their head
    w = []
    for k in range(9):                                                       # the hand comes down on it
        t = (k / 8) ** 1.6
        w += emit_at(BLOCKS, HALF_L, 1, (0, top)) + emit_at(BLOCKS, HALF_R, 1, (0, top))
        w += emit_at(CHOP, POSE, 1, (0, round(128 - (128 - (top + 30)) * t))) + wait(1)
    w += se(s["chop"]) + emit_at(HIYAH, POP, 1, (sx * -34, 70)) + flash_screen(5)
    w += emit_at(BLOCKS, CHUNKS, 1, (0, top))
    for k in range(1, 7):                                                    # CRACK - in two, flying apart
        dx, dy = 6 * k, top - (k * k) // 2
        w += emit_at(BLOCKS, HALF_L, 1, (-dx, dy)) + emit_at(BLOCKS, HALF_R, 1, (dx, dy))
        if k < 4:
            w += emit_at(CHOP, POSE, 1, (0, top + 30 - 6 * k))
        w += wait(1)
    w += emit_at(CHOP, HOLD, 1, (0, top + 8)) + se(s["bonk"])                # ...right on the head
    w += shake_defender(4, 4) + bmove(side, 264, 3, 0, -8) + func(68, 3, 2, 1, 3, 0) + wait(8)
    w += bmove(side, 264, 8, 0, 8) + wait(10)
    return w


def _magic_8ball(side, s):
    """Shadow Ball (Magic 8-Ball): a Magic 8-Ball grows in their hands in dark wisps, rolls over and gives
    the answer: OUTLOOK NOT GOOD."""
    sx = 1 if side == "player" else -1
    dark = rgb(40, 10, 60)
    w = func(33, 0, 1, 0, 11, dark) + emit_at(EIGHT, CHARGE, 0, (sx * 4, 26))
    w += emit_at(EIGHT, WISPS, 0, (sx * 4, 24)) + se(s["shadow"]) + wait(10)
    w += _fly(EIGHT, ROLL8, 1, EIGHT_FRAMES) + wait_frames(EIGHT_FRAMES)
    w += se(s["shadow2"]) + emit_at(ANSWER, POP, 1, (sx * -34, 50)) + flash_screen(4)
    w += func(34, 8, 0, 2, rgb(120, 40, 200), 14, 0) + shake_defender(3, 4) + func(48) + wait(18)
    w += func(33, 0, 1, 11, 0, dark) + wait(6)
    return w


def _loyalty(side, s):
    """Return (Loyalty): RIDE OR DIE. The pendant glows, the love flies - and then it hits them for real."""
    sx = 1 if side == "player" else -1
    pink = rgb(255, 120, 180)
    hearts = HEARTS_E if side == "player" else HEARTS_P
    w = emit_at(HEART, LOCKET, 0, (sx * 10, 46)) + se(s["loyal"]) + func(34, 2, 0, 1, pink, 10, 0) + wait(10)
    for k in range(3):
        w += emit_at(HEART, hearts, 0, (0, 2 * k)) + se(s["loyal2"]) + wait(4)
    w += _fly(HEART, SLAM, 1, HEART_FRAMES) + wait_frames(HEART_FRAMES)
    w += flash_screen(6) + func(34, 8, 0, 2, pink, 14, 0) + shake_defender(4, 4) + func(48) + se(s["bonk"])
    return w + wait(14)


def _chain_dangle(side, s):
    """Confusion: a quicker dangle, no lights-down."""
    return _chain_swing(side, s, swings=2, dark=False)


# ------------------------------------------------------------------ set 5: the everyday moves

def _flashlight(side, s):
    """Confuse Ray (Flashlight): lights out - *click* - a flashlight right in their eyes. Swirly-eyed. HUH?!"""
    sx = 1 if side == "player" else -1
    _, _, beam, _ = torch_geometry(side)
    night = rgb(5, 5, 25)
    w = func(33, 0, 1, 0, 12, night) + wait(4)
    w += emit_at(TORCH, TORCH_E if side == "player" else TORCH_P, 0, TORCH_AT[side]) + se(s["confuse"]) + wait(8)
    w += emit_at(BEAM, BEAM_E if side == "player" else BEAM_P, 0, beam) + flash_screen(3)       # *click*
    w += func(34, 8, 0, 2, rgb(255, 255, 220), 15, 0) + func(36, 2, 0, 1, 4, 264) + wait(10)   # blinded
    w += se(s["confuse2"]) + emit_at(TORCH, SWIRL, 1, (-7, 24)) + emit_at(TORCH, SWIRL, 1, (7, 24))
    w += func(4, 0, 0x0900, 10, 0) + wait(8)
    w += emit_at(HUH, POP, 1, (sx * -30, 58)) + wait(8)
    w += func(4, 0, 0x0900, 10, 2) + se(s["confuse2"]) + wait(14)
    w += func(33, 0, 1, 12, 0, night) + wait(6)
    return w


def _stun_taser(side, s):
    """Thunder Wave (Stun Taser): the stun gun snaps, crackles shoot over, rings of static lock them up stiff."""
    sx = 1 if side == "player" else -1
    w = emit_at(STUN, STUN_E if side == "player" else STUN_P, 0, STUN_AT[side]) + se(s["twave"]) + wait(6)
    w += emit_at(STUN, ARC_E if side == "player" else ARC_P, 0, STUN_TIP[side]) + func(9)
    w += wait_frames(STUN_FRAMES + 4)
    w += se(s["twave2"]) + emit_at(STATIC, RING_X, 1, (0, 20)) + emit_at(STATIC, RING_HOLD, 1, (0, 20))
    w += flash_screen(3)
    for k in range(9):                                                       # locked up, twitching (ends lit)
        if k in (2, 5):
            w += emit_at(STATIC, RING_X, 1, (0, 20))
        if k == 3:
            w += se(s["twave2"]) + emit_at(ZZZT, POP, 1, (sx * -30, 58))
        w += func(34, 8, 0, 1, rgb(255, 255, 80) if k % 2 == 0 else rgb(30, 30, 70), 14, 0)
        w += func(36, 2, 0, 1, 2, 264) + wait(2)
    w += func(36, 1, 0, 1, 8, 264) + wait(14)
    return w


def _bass_boost(side, s):
    """Supersonic (Bass Boost): a boombox up on their shoulder, bass so heavy the target's head rattles."""
    sx = 1 if side == "player" else -1
    at = BOX_AT[side]
    notes, wave = (NOTES_E, SWAVE_E) if side == "player" else (NOTES_P, SWAVE_P)
    w = emit_at(BOOMBOX, BOX5, 0, at) + wait(8)
    for k in range(4):                                                       # BWOMP. BWOMP. BWOMP. BWOMP.
        w += se(s["bass"]) + emit_at(BOOMBOX, THUMP, 0, at) + emit_at(SOUNDWAVE, wave, 0, at)
        if k % 2 == 0:
            w += emit_at(BOOMBOX, notes, 0, at)
        w += func(68, 2, 1, 1, 2, 0) + func(36, 1, 1, 1, 2, 258)
        if k:
            w += func(4, 0, 0x0A00, 4, 0 if k % 2 else 2)                    # head bobbing (it can't help it)
        w += wait(5)
    w += emit_at(BWOMP, POP, 1, (sx * -30, 58)) + func(68, 4, 2, 1, 3, 0) + shake_defender(3, 5)
    w += func(34, 8, 0, 2, rgb(255, 120, 220), 12, 0) + wait(16)
    return w


SQUAD_SPOTS = {"player": [(-44, 6), (46, 6), (98, 58)], "enemy": [(42, 4), (-42, 4), (-78, 12)]}
#                 (the player's third homie: back row, smaller, standing up above the HP box - it draws over him)


def _squad_up(side, s):
    """Double Team (Squad Up): poof, poof, poof - the whole squad's standing behind them. SQUAD UP!"""
    big = side == "player"                                                   # near side: the homies are bigger
    figs = [(SQUAD, FIG if big else FIG_S), (SQUAD2, FIG2 if big else FIG2_S), (SQUAD, FIG_S)]
    dim = rgb(40, 20, 70)
    w = func(33, 0, 1, 0, 8, dim) + se(s["dteam"]) + func(19)
    for k, (x, y) in enumerate(SQUAD_SPOTS[side]):
        w += emit_at(SQUAD, POOF, 0, (x, y)) + emit_at(*figs[k], 0, (x, y))
        if k == 2:
            w += se(s["dteam"])
        w += wait(3)
    w += shake_attacker(2, 8) + emit_at(SQUADUP, POP, 0, (0, 62 if big else 50)) + wait(14)
    for x, y in SQUAD_SPOTS[side]:                                           # ...and they're gone
        w += emit_at(SQUAD, POOF, 0, (x, y)) + wait(3)
    w += wait(6) + func(33, 0, 1, 8, 0, dim) + wait(4)
    return w


def _water_bomb(side, s):
    """Water Pulse (Water Bomb): a water balloon lobbed right on them. SPLOOSH. Dripping and dazed."""
    sx = 1 if side == "player" else -1
    blue = rgb(60, 140, 255)
    w = func(19) + se(s["wpulse"]) + wait(4) + _throw(BALLOON, 1, (0, 16)) + wait_frames(THROW_FRAMES)
    w += se(s["wpulse2"]) + emit_at(DRENCH, CROWN, 1, (0, 14)) + emit_at(DRENCH, SPLASHDROPS, 1, (0, 22))
    w += flash_screen(3) + func(34, 8, 0, 2, blue, 14, 0) + shake_defender(3, 4) + wait(4)
    w += emit_at(SPLOOSH, POP, 1, (sx * -30, 58)) + emit_at(BALLOON, DROPS, 1, (0, 14)) + wait(8)
    w += func(4, 0, 0x0700, 10, 0) + wait(10) + func(4, 0, 0x0700, 10, 2) + wait(14)
    return w


def _sneak_diss(side, s):
    """Faint Attack (Sneak Diss): they vanish - "UR MID" pops up behind the target - and a palm comes down on the
    back of their head. OOOOH!"""
    sx = 1 if side == "player" else -1
    w = se(s["faint"]) + func(36, 2, 0, 1, 3, 258) + wait(4) + func(40, 2, 1) + wait(8)      # gone
    w += emit_at(DISS, POP, 1, (sx * 26, 42)) + se(s["leer"]) + wait(6)                    # from behind them
    w += func(4, 0, 0x0800, 8, 0) + wait(12)                                                # ...huh?
    w += stop_motion(SLAP, SLAP_POSE, 1, (sx * 14, 96), (sx * 4, 40), 4)
    w += emit_at(SLAP, SLAP_HOLD, 1, (sx * 4, 38)) + se(s["bonk"]) + emit_at(SLAP, POWS, 1, (0, 34))
    w += flash_screen(4) + func(48) + shake_defender(4, 3) + bmove(side, 264, 3, 0, -6) + wait(4)
    w += emit_at(OOOH, POP, 1, (sx * -32, 56)) + func(4, 0, 0x0800, 8, 2) + bmove(side, 264, 6, 0, 6) + wait(14)
    w += func(40, 2, 0) + func(36, 2, 0, 1, 3, 258) + wait(8)                               # back, innocent
    return w


def _dirty_sprite(side, s):
    """Toxic (Dirty Sprite): a double cup of the purple stuff - thrown. It's all over them and they're bubbling."""
    sx = 1 if side == "player" else -1
    purple = rgb(160, 60, 230)
    w = emit_at(CUP, HELD, 0, (sx * 22, 30)) + se(s["toxic"]) + func(19) + wait(8)
    w += _throw(CUP, 1, (0, 18)) + wait_frames(THROW_FRAMES)
    w += se(s["splat"]) + emit_at(GOOP, GOOP_SPLAT, 1, (0, 22)) + emit_at(GOOP, GOOP_DRIPS, 1, (0, 18))
    w += func(34, 8, 0, 2, purple, 14, 0) + shake_defender(3, 3) + wait(4)
    w += emit_at(CUP, BUBBLES, 1, (0, 10)) + se(s["toxic2"]) + emit_at(DIRTY, POP, 1, (sx * -30, 58))
    for k in range(3):                                                       # badly poisoned: pulsing purple
        w += func(34, 8, 0, 1, purple, 12, 0) + func(36, 2, 0, 1, 2, 264) + wait(6)
        if k == 1:
            w += se(s["toxic2"])
    return w + wait(12)


def _duck_n_cover(side, s):
    """Protect (Duck n Cover): they duck behind a trash-can lid and everything pings right off it. NOPE."""
    sx = 1 if side == "player" else -1
    # the enemy holds it up in front of itself; the player's Pokémon (seen from behind) holds it out towards
    # the foe, up in the middle of the screen - drawn over their back it'd look like it was behind them
    at = LID_AT[side]
    w = bmove(side, 258, 3, 0, -10) + emit_at(LID, LIDUP, 0, at) + se(s["protect"]) + wait(6)   # duck!
    w += emit_at(LID, LIDFLASH, 0, at) + flash_screen(3) + func(34, 2, 0, 1, rgb(200, 230, 255), 12, 0) + wait(5)
    for dx, dy in ((10, 14), (-8, 4), (6, -10)):                             # ping. ping. ping.
        w += emit_at(LID, PINGS, 0, (at[0] + sx * dx, at[1] + dy)) + se(s["bling"])
        w += func(36, 1, 0, 1, 2, 258) + wait(4)
    w += emit_at(NOPE, POP, 0, (at[0] + sx * 4, 58)) + wait(14)
    w += bmove(side, 258, 6, 0, 10) + wait(8)
    return w


def _smackdown(side, s):
    """Take Down (Smackdown): they charge in with a steel folding chair - CLANG - and stagger back seeing stars."""
    sx = 1 if side == "player" else -1
    w = bmove(side, 258, 4, -8, -4) + se(s["tdown"]) + wait(6)               # winding up
    w += bmove(side, 258, 6, 72, 36) + wait(6)                               # CHARGE
    w += stop_motion(CHAIR, CHAIR_POSE, 1, (sx * -20, 100), (0, 40), 4)
    w += emit_at(CHAIR, CHAIR_HOLD, 1, (0, 36)) + se(s["tdown2"]) + emit_at(CLANG, POP, 1, (0, 24))
    w += emit_at(SMACKDN, POP, 1, (sx * -36, 62)) + flash_screen(8) + func(48) + shake_defender(6, 4)
    w += func(68, 5, 3, 1, 4, 0) + bmove(side, 264, 3, 0, -8) + wait(8)
    w += bmove(side, 264, 8, 0, 8) + bmove(side, 258, 8, -64, -32) + wait(10)               # back off
    w += se(s["bonk"]) + shake_attacker(2, 4)                                                # the recoil
    for k in range(10):                                                      # seeing stars
        a = k * math.pi / 4
        for ph in (0, math.pi):
            w += emit_at(CHAIR, STARS, 0, (round(14 * math.cos(a + ph)), round(44 + 4 * math.sin(a + ph))))
        w += wait(2)
    return w + wait(4)


def _big_taser(side, s):
    """Thunderbolt (Big Taser): an XL taser held up high, crackling - and a giant bolt drops out of the sky."""
    sx = 1 if side == "player" else -1
    night = rgb(10, 10, 40)
    at = (sx * 18, 58)
    w = func(33, 0, 1, 0, 12, night) + emit_at(BIGTASER, BIG_E if side == "player" else BIG_P, 0, at) + wait(6)
    w += emit_at(BIGTASER, ZIGS, 0, at) + se(s["tbolt"]) + shake_attacker(1, 14) + wait(14)   # charging up
    w += emit_at(MEGABOLT, STRIKE, 1, (0, 54)) + se(s["tbolt2"]) + flash_screen(8)            # KRAKOOM
    w += emit_at(MEGABOLT, STRIKE2, 1, (sx * 10, 70)) + emit_at(BIGTASER, ZIGS, 1, (0, 16))
    for k in range(9):                                                       # (ends on the lit step)
        if k == 2:
            w += emit_at(BZZT, POP, 1, (sx * -34, 60))
        if k == 4:
            w += emit_at(MEGABOLT, STRIKE2, 1, (sx * -12, 66)) + flash_screen(3) + se(s["tbolt2"])
        w += func(34, 8, 0, 1, rgb(255, 250, 90) if k % 2 == 0 else rgb(0, 0, 0), 16, 0)
        w += func(36, 2, 1, 1, 2, 264) + wait(2)
    w += func(48) + wait(10) + func(33, 0, 1, 12, 0, night) + wait(6)
    return w


def _clock_it(side, s):
    """Foresight (Clock It): the eyes emoji over their head, looking away... looking away... SNAP - right at the
    target. BWOMM: red circle, red arrow, U GOT CLOCKED."""
    sx = 1 if side == "player" else -1
    at = (sx * 4, 62)
    look_at, look_away = (EYES_R, EYES_L) if side == "player" else (EYES_L, EYES_R)
    w = se(s["clock"])
    for k in range(5):                                                       # whistling, minding their business
        w += emit_at(EYES, look_away, 0, (at[0] - sx * (k % 2), at[1])) + wait(2)
    w += se(s["leer"])
    for k in range(5):                                                       # ...wait.
        w += emit_at(EYES, look_at, 0, (at[0] + sx * (2 if k == 0 else 0), at[1])) + wait(2)
    w += se(s["vineboom"]) + emit_at(CIRCLE, POP, 1, (sx * -2, 16)) + flash_screen(4)       # BWOMM
    w += func(68, 6, 3, 1, 3, 0) + func(33, 0, 1, 0, 6, rgb(60, 0, 0))
    for k in range(8):                                                       # staring them down the whole time
        w += emit_at(EYES, look_at, 0, at) + wait(2)
        if k == 2:
            w += emit_at(CLOCKED, POP, 1, (sx * -34, 62)) + shake_defender(2, 4)
    for k in range(6):
        w += emit_at(EYES, look_at, 0, at) + wait(2)
    w += func(33, 0, 1, 6, 0, rgb(60, 0, 0)) + wait(6)
    return w


VARIANTS = {97: _fly_turn2_first, 99: _calibrate, 7: _chain_swing, 8: _chain_dangle, 9: _payday, 10: _full_auto, 11: _rpg,
            12: _molotov, 13: _brick, 14: _egg, 15: _hose, 16: _bat, 17: _taser, 18: _car_alarm, 19: _bass_drop,
            20: _hot_shot, 21: _stare_down, 22: _talk_trash, 23: _pocket_sand, 24: _fan_blast,
            25: _catch_flight, 26: _hydrant_wave, 27: _power_line, 28: _road_rage, 29: _molotov2, 30: _zaza_leaf,
            31: _stomp_out, 32: _grill_chomp, 33: _hollow_point, 34: _switchblade, 35: _hot_box, 36: _burnout,
            37: _hi_yah, 38: _magic_8ball, 39: _loyalty,
            40: _flashlight, 41: _stun_taser, 42: _bass_boost, 43: _squad_up, 44: _water_bomb, 45: _sneak_diss,
            46: _dirty_sprite, 47: _duck_n_cover, 48: _smackdown, 49: _big_taser, 50: _clock_it, 1: _sniper, 2: _shotgun, 3: _spray, 4: _point_blank, 5: _gangsta, 6: _drive_by}


# particle kits each animation uses: the battle heap only fits a few particle systems at once
KITS = {97: (PLANE, WHAM), 99: (GUN, HOUSE, YOLK), 1: (GUN, KIT, SMOKE), 2: (GUN, SMOKE), 3: (GUN, KIT, SMOKE), 4: (GUN, SMOKE),
        5: (GUN, KIT, SMOKE), 6: (GUN, SMOKE, CAR), 7: (GUN, BLING), 8: (GUN, BLING), 9: (GUN, CASH), 10: (GUN, KIT, SMOKE),
        11: (GUN, SMOKE, ROCKET), 12: (GUN, BOTTLE, FIRE), 13: (GUN, BRICK, SMOKE), 14: (EGG, HOUSE, YOLK),
        15: (HYDRANT, JET, SPLASH), 16: (GUN, SLUGGER), 17: (GUN, TASER, BOLTS), 18: (FOB, RINGS),
        19: (SUB, CRACK, SMOKE), 20: (CHIPS, BURST), 21: (SHADES, GLINT), 22: (BUBBLE,), 23: (POCKET, SAND),
        24: (FAN, WIND), 25: (PLANE, WHAM), 26: (WAVE, DUCK), 27: (CABLE, XRAY), 28: (HONK, CONE),
        29: (BOOZE, BREATH, BURST), 30: (LEAF, HAZE), 31: (BOOT, STOMP), 32: (TOPJAW, BOTJAW, GLITZ),
        33: (SLUG, GUN), 34: (SLASH, TIRE), 35: (SMOG, COUGH), 36: (WHEEL, TRAIL, BURST),
        37: (BLOCKS, CHOP, HIYAH), 38: (EIGHT, ANSWER), 39: (HEART,),
        40: (TORCH, BEAM, HUH), 41: (STUN, STATIC, ZZZT), 42: (BOOMBOX, SOUNDWAVE, BWOMP),
        43: (SQUAD, SQUAD2, SQUADUP), 44: (BALLOON, DRENCH, SPLOOSH), 45: (DISS, SLAP, OOOH), 46: (CUP, GOOP, DIRTY),
        47: (LID, NOPE), 48: (CHAIR, CLANG, SMACKDN), 49: (BIGTASER, MEGABOLT, BZZT), 50: (EYES, CIRCLE, CLOCKED)}


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
        got = VARIANTS[k](side, sounds)
        tail = [1] + func(62, 2) + func(62, 8) + [50] + frees + [4]
        if isinstance(got, tuple):                                 # a two-turn move (Fly): turn 1, turn 2
            one, two = got[0] + tail, got[1] + tail
            w = [13, 2, 1 + len(one)] + one + two                  # JumpByVariantBit0: bit 0 set = the hit
        else:
            w = got + tail
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
