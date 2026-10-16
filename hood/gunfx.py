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
BOTTLE, BRICK, EGG, FIRE = 7, 8, 9, 10
DONOR = {GUN: 73, KIT: 62, SMOKE: 84, CAR: 82, BLING: 168, CASH: 47, ROCKET: 349,
         BOTTLE: 349, BRICK: 349, EGG: 349, FIRE: 84}
LOAD = dict(DONOR)                                            # particle file each kit loads (battlefx repoints)   # small files: the battle heap can't fit big ones twice
SPARK, FLASH, TRACER = 0, 1, 2
CASING, CROSS = 0, 1
PUFF, DIRT = 1, 0
RIDE, WINDOW = 2, 0                                           # CAR: the lowrider + its gun flashes (riding along)
CAR_START, CAR_ROAD = -250, 2                                 # car spawn, pixels from the target (x, y up)
GUN_ON_CAR = (30, 23)                                         # the gun at the window, pixels from the car centre
CAR_LIFE = 90
PENDANT = 1                                                   # BLING: the chain + medallion (follows its emitter)
BILLS, STACK = 0, 1                                           # CASH: fluttering dollar bills, the bankroll
TO_ENEMY, TO_PLAYER = 0, 1                                    # ROCKET: an RPG round flying each way
# battler particle origins (sBattleAnimEmitterPositions, kind 0, perspective 0): player and enemy
ORIGIN = {"player": (-9616, -5464), "enemy": (11056, 4400)}
ROCKET_FRAMES = 18
THROWN = 0                                                    # BOTTLE/BRICK/EGG: the object, riding its emitter
EMBERS, BLAZE = 0, 1                                          # FIRE: the untouched fire-burst effect
THROW_FRAMES = 20
CAR_SPEED = 5                                                 # screen pixels per frame (at the enemy's depth)
TICK = 2                                                      # frames per script tick (scripts run at 30 Hz)
CAR_SCALE = 1.9                                               # 64px texture -> ~90px car on screen

# where the gun's muzzle sits relative to the battler's particle origin, in screen pixels (y up). Back
# sprites hold the gun on the right pointing right, front sprites mirror it (measured on Cyndaquil/Hoothoot).
MUZZLE = {"player": (31, 9), "enemy": (-30, 17)}
# particle units per screen pixel (x, y) at each battler's depth - measured in-game: the camera is a
# perspective one, so the far (enemy) side needs more units per pixel than the near (player) side
SCALE = {"near": (171, 167), "far": (355, 180)}
# ...but offsets inside the car's particle system come out 2.3x wider (measured; its velocity is unaffected)
PS_SCALE = {3: {"near": (74, 185), "far": (154, 200)}}

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
             vel=(0, CAR_SPEED * SCALE['far'][0] / 4096), air_resist=128)
    # window flashes: born with the car, same speed, hidden until the gun reaches the target, then strobing
    spa.set_texture(b, 0, tex_spark())
    life = int((-CAR_START - GUN_ON_CAR[0] + 60) / CAR_SPEED)  # gone once the gun is 60px past them
    gold = rgb(255, 230, 90)
    spa.edit(b, rs[WINDOW], clr=gold, clr_anm=(rgb(255, 255, 220), gold), scl=.9, gen=1, emtr_life=1, life=life,
             axis=(1, 0, 0), vel=(0, CAR_SPEED * SCALE['far'][0] / 4096), air_resist=128, init_pos=0,
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
    for ps, art, spin in ((BOTTLE, fxart.molotov(), 0x0A00), (BRICK, fxart.brick(), 0x0C00), (EGG, fxart.egg(), 0x0500)):
        b = bytearray(files[DONOR[ps]])
        rs = spa.resources(bytes(b))
        texels, pal = fxart.to_a3i5(art, 24)
        spa.set_texture(b, 1, texels, pal)
        spa.edit(b, rs[THROWN], gen=1, emtr_life=1, life=THROW_FRAMES * 2 + 10, scl=.9, init_pos=0, vel=(0, 0),
                 air_resist=128, alpha=(31, 31, 31), scl_anm=(1.0, 1.0, 1.0, 0, 255),
                 flags_on=(1 << 15) | (1 << 14) | (1 << 12), flags_off=1 << 13)
        struct.pack_into("<hhH", b, rs[THROWN]["off"] + 52, spin, spin, 0)   # tumbling
        out[ps] = bytes(b)
    out[FIRE] = bytes(files[DONOR[FIRE]])                     # the original fire burst, as is
    # (TRACER isn't listed: MoveEmitter deletes it when the flight ends)
    for ps, res in ((GUN, SPARK), (GUN, FLASH), (KIT, CASING), (KIT, CROSS), (SMOKE, PUFF),
                    (SMOKE, DIRT), (CAR, RIDE), (CAR, WINDOW), (BLING, PENDANT), (CASH, BILLS), (CASH, STACK),
                    (ROCKET, TO_ENEMY), (ROCKET, TO_PLAYER), (BOTTLE, THROWN), (BRICK, THROWN), (EGG, THROWN),
                    (FIRE, EMBERS), (FIRE, BLAZE)):
        flag = spa.resources(out[ps])[res]["flag"]
        assert flag >> 14 & 1, f"kit {ps} emitter {res} never finishes (no self_dest): WaitForParticles would hang"
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


def emit_at(ps, res, who, off=(0, 0)):
    """Emitter at the attacker (who=0) or defender (who=1) plus an offset in screen pixels (y up)."""
    if off == (0, 0):
        return [46, ps, res, 3 if who == 0 else 4]
    sx, sy = PS_SCALE.get(ps, SCALE)[_depth(who)]
    x, y = round(off[0] * sx), round(off[1] * sy)
    # ConfigureFromScript: zMode, battlerOrder 0, position mode 4/5 (battler A/B + offset), axis, flags,
    # camera; then the offset args {ignoreSide, x, y, z}
    return [46, ps, res, 17, 55, 6, 0, 0, 4 + who, 0, 0, 0, 55, 4, 1, _u(x), _u(y), 0]


def muzzle(ps, res, side, back=0):
    x, y = MUZZLE[side]
    return emit_at(ps, res, 0, (x - back if x > 0 else x + back, y))


def tracer(slot, frames, off=(0, 0), start=2, delay=0):
    """Bullet streak flown from the barrel to the target (+ off pixels), with MoveEmitter."""
    return [47, GUN, slot, TRACER, 3] + func(65, slot, off[0], off[1], delay, frames, 0, 0, start << 16, 0)


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
    """Test only: sin motion on a plain flash (slot 2), a spark, then on the chain (slot 1), a spark."""
    w = [47, GUN, 2, FLASH, 4] + func(72, 2, 0, 360, 270, 990, 24, 3, 30, 1, GUN) + wait(25)
    w += emit_at(GUN, SPARK, 1, (14, 6)) + wait(15)
    w += [47, BLING, 1, PENDANT, 4] + func(72, 1, 0, 360, 270, 990, 24, 3, 30, 1, BLING) + wait(25)
    return w + emit_at(GUN, SPARK, 1, (-14, 6)) + wait(10)


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


def _throw(kit):
    """Lob the kit's object from the attacker onto the target (MoveEmitterArc carries its emitter)."""
    return se_key("whoosh") + [47, kit, 1, THROWN, 3] + func(65, 1, 0, 0, 0, THROW_FRAMES, 0, 0, 0, 0)


def se_key(key):
    return ["SE", key]                                        # resolved to a sound id by variant()


def _molotov(side, s):
    """Flamethrower: a Molotov tumbles over, shatters, and they go up."""
    orange = rgb(255, 120, 20)
    w = func(19) + wait(4) + _throw(BOTTLE) + wait_frames(THROW_FRAMES)
    w += se(s["smash"]) + emit_at(GUN, SPARK, 1) + emit_at(FIRE, BLAZE, 1) + emit_at(FIRE, EMBERS, 1)
    w += func(34, 8, 0, 2, orange, 14, 0) + shake_defender(3, 6) + wait(8)
    w += emit_at(FIRE, BLAZE, 1, (-8, 4)) + emit_at(FIRE, BLAZE, 1, (8, 2)) + wait(8)
    w += emit_at(FIRE, EMBERS, 1, (0, 6)) + shake_defender(2, 4) + wait(16)
    return w


def _brick(side, s):
    """Rock Throw: a brick tumbles across, bonk, dust and a dizzy wobble."""
    w = func(19) + wait(4) + _throw(BRICK) + wait_frames(THROW_FRAMES)
    w += se(s["bonk"]) + emit_at(GUN, FLASH, 1, (0, 8)) + emit_at(GUN, SPARK, 1, (0, 12))
    w += emit_at(SMOKE, DIRT, 1, (-6, 6)) + emit_at(SMOKE, DIRT, 1, (6, 6)) + func(48) + wait(8)
    for k in range(3):                                         # seeing stars
        w += emit_at(GUN, SPARK, 1, ((-10, 0, 10)[k], 16)) + func(4, 0, 0x0A00, 5, 0 if k % 2 else 2) + wait(5)
    return w + wait(10)


def _egg(side, s):
    """Egg Bomb: egg ya house - lobbed onto them, splat, yolk everywhere."""
    yolk = rgb(255, 220, 60)
    w = func(19) + wait(4) + _throw(EGG) + wait_frames(THROW_FRAMES)
    w += se(s["splat"]) + emit_at(GUN, SPARK, 1, (0, 10)) + emit_at(SMOKE, DIRT, 1, (0, 10))
    w += func(34, 8, 0, 2, yolk, 14, 0) + shake_defender(2, 3) + wait(20)
    return w


def _chain_dangle(side, s):
    """Confusion: a quicker dangle, no lights-down."""
    return _chain_swing(side, s, swings=2, dark=False)


VARIANTS = {99: _calibrate, 7: _chain_swing, 8: _chain_dangle, 9: _payday, 10: _full_auto, 11: _rpg,
            12: _molotov, 13: _brick, 14: _egg, 1: _sniper, 2: _shotgun, 3: _spray, 4: _point_blank, 5: _gangsta, 6: _drive_by}


# particle kits each animation uses: the battle heap only fits a few particle systems at once
KITS = {99: (GUN, BLING), 1: (GUN, KIT, SMOKE), 2: (GUN, SMOKE), 3: (GUN, KIT, SMOKE), 4: (GUN, SMOKE),
        5: (GUN, KIT, SMOKE), 6: (GUN, SMOKE, CAR), 7: (GUN, BLING), 8: (GUN, BLING), 9: (GUN, CASH), 10: (GUN, KIT, SMOKE),
        11: (GUN, SMOKE, ROCKET), 12: (GUN, BOTTLE, FIRE), 13: (GUN, BRICK, SMOKE), 14: (GUN, EGG, SMOKE)}


def variant(k, sounds):
    """Animation script words for feel k; sounds = {"pop": seq, "boom": seq, ...}."""
    kits = KITS[k]
    frees = [w for ps in kits for w in (53, ps)]

    def body(side):
        _SIDE[0] = side
        w = VARIANTS[k](side, sounds) + [1, 50] + frees + [4]       # WaitForTasks, WaitForParticles, End
        while "SE" in w:                                            # sound markers from helpers
            i = w.index("SE")
            w[i:i + 2] = [5, sounds[w[i + 1]]]
        return w

    head = (PRELUDE + [51, kits[0], LOAD[kits[0]]] + PRELUDE_END +
            [w for ps in kits[1:] for w in (51, ps, LOAD[ps])])
    p, e = body("player"), body("enemy")
    # JumpBySide attacker: [64, 0, off->player, off->enemy]; offsets count from their own word
    j = len(head)
    words = head + [64, 0, 2, 1 + len(p)] + p + e
    assert words[j + 2] + j + 2 == j + 4 and words[j + 3] + j + 3 == j + 4 + len(p)
    return words
