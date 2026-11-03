"""Set 26 batch 1 (INSANE): Live Wire, Fire Cart, Wrecker, Headbanger, Super Soaker (variants 392-396).
Run once from the repo root: python -X utf8 hood/test/reel/set26_b1.py  (art: set26_b1_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "WIRE26 CART26 CARTB26 WRECK26 WRECKB26 HEAD26 SOAK26 SOAKB26 SOAKC26".split()

KITS = '''
    # ---- set 26: thirty more (batch 1, INSANE) ----------------------------------------------------------------
    # Live Wire (Volt Tackle): a snapped power line sparking - ZZT - ZZT - they grab it and charge, the transformer blows
    b, rs = pk(WIRE26, {1: (fxart.utility_pole(), 1.2, 4, {}), 2: (fxart.wire_end(), .5, 4, {})}, alpha=fxart.zig_bolt())
    burst(b, rs, 0, rgb(255, 250, 120), rgb(255, 255, 255), .4, 6, .2, life=10)
    burst(b, rs, 3, rgb(255, 240, 80), rgb(255, 255, 255), .6, 16, .34, life=14)
    fin(WIRE26, b, rs, (0, 1, 2, 3))

    # Fire Cart (Flare Blitz): a shopping cart rolls - sparks - flames - FULL FIRE - straight into the foe
    b, rs = pk(CART26, {1: (fxart.grocery_cart(), 1.3, 4, {}), 2: (flipx(fxart.grocery_cart()), 1.3, 4, {})}, alpha=fxart.holy_flame())
    burst(b, rs, 0, rgb(255, 130, 30), rgb(255, 240, 140), .45, 8, .1, up=.24, life=16)
    burst(b, rs, 3, rgb(255, 100, 20), rgb(255, 250, 160), .55, 18, .3, up=.3, life=24)
    fin(CART26, b, rs, (0, 1, 2, 3))
    b, rs = pk(CARTB26, {}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(200, 205, 215), rgb(255, 255, 255), .45, 14, .34, up=.2, gravity=.02, life=24, spin=0x0A00)
    fin(CARTB26, b, rs, (0,))

    # Wrecker (Rock Wrecker): the wrecking ball swings - over their head - swings - they duck - SMASH
    b, rs = pk(WRECK26, {1: (fxart.demo_ball(), 2.0, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(170, 165, 160), rgb(230, 225, 220), .5, 20, .36, up=.22, gravity=.022, life=26, spin=0x0900)
    fin(WRECK26, b, rs, (0, 1))
    b, rs = pk(WRECKB26, {}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(190, 180, 170), n=12, life=30, scl=.45, up=.04)
    fin(WRECKB26, b, rs, (0,))

    # Headbanger (Head Smash): amp stacks, the riff - headbang - HEADBANG (pyro) - full send into the foe
    b, rs = pk(HEAD26, {1: (fxart.amp_stack(), 1.0, 4, {})}, alpha=fxart.holy_flame())
    burst(b, rs, 0, rgb(255, 130, 30), rgb(255, 240, 140), .45, 8, .06, up=.5, life=18)
    burst(b, rs, 3, rgb(255, 100, 20), rgb(255, 250, 160), .55, 14, .1, up=.6, life=22)
    fin(HEAD26, b, rs, (0, 1, 3))

    # Super Soaker (Water Spout): pump - pump - PUMPPUMPPUMP - a flood
    b, rs = pk(SOAK26, {1: (fxart.mega_soaker(), .9, 4, {}), 2: (fxart.mega_soaker(pumped=True), .9, 4, {})}, alpha=fxart.water_jet())
    burst(b, rs, 0, rgb(120, 190, 255), rgb(230, 245, 255), .5, 16, .24, up=.3, gravity=.02, life=24)
    fin(SOAK26, b, rs, (0, 1, 2))
    b, rs = pk(SOAKB26, {1: (flipx(fxart.mega_soaker()), .9, 4, {}), 2: (flipx(fxart.mega_soaker(pumped=True)), .9, 4, {})})
    fin(SOAKB26, b, rs, (1, 2))
    b, rs = pk(SOAKC26, {}, alpha=fxart.water_jet())
    spray2(b, rs, {"player": (48, 28), "enemy": (-48, 18)}, (0, 22), 10, clr=rgb(110, 180, 255),
           clr_anm=(rgb(230, 245, 255), rgb(60, 130, 240)), scl=.9, gen=3, gen_intvl=1, emtr_life=40, radius=.2,
           spread=.03, alpha=(31, 28, 0))
    fin(SOAKC26, b, rs, (0, 1))
'''

SCRIPTS = '''
def _live_wire(side, s):
    """Volt Tackle (Live Wire): a snapped power line hanging off the pole, the end sparking. ZZT. ZZT. They grab it -
    lit up - and charge the foe with it. The transformer blows and the whole block flickers."""
    sx = _sx(side)
    pole = _s23(side, 0, (112, 70))
    end = (pole[0] + 14, pole[1] - 22)
    held = (sx * 16, 28)
    scene = lambda: emit_at(WIRE26, 1, 0, pole)
    w = se(s["pop"]) + _hold(WIRE26, 1, 0, pole, 3, lambda k: emit_at(WIRE26, 2, 0, end))
    for n in range(2):                                                         # ZZT... ZZT...
        w += se(s["spark"]) + emit_at(WIRE26, 0, 0, end) + shake_defender(n, 1) + _hold(WIRE26, 1, 0, pole, 4 + n, lambda k: emit_at(WIRE26, 2, 0, end))
    w += se(s["whoosh"]) + _lob(WIRE26, 2, side, end, held, 4, 8, lambda k: scene())   # *grabs it*
    for k in range(6):                                                         # *lit up*
        w += scene() + emit_at(WIRE26, 2, 0, held)
        if k % 2 == 0:
            w += se(s["zap"]) + emit_at(WIRE26, 0, 0, (0, 30)) + func(34, 2, 0, 1, rgb(255, 250, 80) if k % 4 == 0 else rgb(40, 40, 40), 13, 0)
        w += wait(1)
    w += func(33, 0, 1, 0, 14, 0) + bmove(side, 258, 3, sx * 30, 12) + se(s["tbolt"]) + se(s["kaboom"])   # CHARGE
    w += flash_screen(6) + emit_at(WIRE26, 3, 1, (0, 24)) + emit_at(WIRE26, 3, 0, (pole[0] + 10, pole[1] + 18)) + func(68, 6, 6, 1, 10, 0)
    for k in range(10):
        if k % 2 == 0:
            w += shake_defender(2, 1) + func(34, 8, 0, 1, rgb(255, 250, 80) if k % 4 == 0 else rgb(30, 30, 30), 14, 0)
        if k == 4:
            w += se(s["thunder"]) + flash_screen(3)
        w += wait(1)
    w += func(48) + bmove(side, 258, 4, -sx * 30, -12) + shake_attacker(2, 3) + func(33, 0, 1, 14, 0, 0)
    return w + func(34, 8, 0, 1, rgb(255, 250, 80), 12, 0) + wait(3)


def _fire_cart(side, s):
    """Flare Blitz (Fire Cart): they hop in a shopping cart. It rolls - squeak - sparks off the wheels. Faster - it
    catches. FASTER - fully on fire - and it plows into the foe. They climb out singed."""
    sx = _sx(side)
    res = _p(side, 1, 2)
    y = _p(side, 82, 104)
    xs = _p(side, (-40, 160), (300, 70))
    at = lambda x: _s23(side, 0, (x, y))
    w = se(s["whoosh"]) + func(40, 2, 1) + wait(2)                            # *hops in*
    steps = [(.0, 0), (.12, 0), (.24, 0), (.34, 1), (.46, 1), (.58, 1), (.7, 2), (.84, 2), (1.0, 2)]
    for k, (t, fire) in enumerate(steps):
        x = round(xs[0] + (xs[1] - xs[0]) * t)
        w += emit_at(CART26, res, 0, at(x))
        if k % 2 == 0:
            w += se(s["rollout"] if fire < 2 else s["flame"])
        if fire == 1 and k % 2 == 1:
            w += emit_at(CART26, 0, 0, at(x))
        if fire == 2:
            w += emit_at(CART26, 0, 0, at(x)) + (emit_at(CART26, 3, 0, at(x)) if k == 6 else [])
        w += wait(1 if fire else 2)
    w += se(s["kaboom"]) + se(s["explo"]) + flash_screen(6) + func(33, 0, 1, 0, 10, rgb(160, 50, 0))   # CRASH
    w += emit_at(CART26, 3, 1, (0, 20)) + emit_at(CARTB26, 0, 1, (0, 20)) + func(68, 6, 6, 1, 8, 0) + shake_defender(5, 4) + func(48)
    w += func(34, 8, 0, 1, rgb(255, 100, 30), 14, 0) + wait(8)
    w += func(33, 0, 1, 10, 0, rgb(160, 50, 0)) + func(40, 2, 0) + func(34, 2, 0, 1, rgb(50, 40, 40), 12, 0) + shake_attacker(2, 2)
    return w + wait(4)


def _wrecker(side, s):
    """Rock Wrecker (Wrecker): a wrecking ball swings across - right over the foe's head. Back again, lower - the foe
    ducks. Third swing comes in low and SMASHES them."""
    import math as _m
    fx, fy = _S23_AT["enemy" if side == "player" else "player"]
    piv = (fx, fy - 150)
    pos = lambda ang, r: _s23(side, 0, (round(piv[0] + r * _m.cos(ang)), round(piv[1] + r * _m.sin(ang))))
    w = []
    for n, (r, a0, a1) in enumerate(((112, 2.4, .74), (130, .74, 2.4), (150, 2.5, 1.57))):
        w += se(s["whoosh"])
        steps = 8 if n < 2 else 6
        for k in range(steps):
            t = (k + 1) / steps
            a = a0 + (a1 - a0) * (t if n < 2 else t ** 1.6)
            w += emit_at(WRECK26, 1, 0, pos(a, r))
            if n == 1 and k == 2:
                w += bmove(side, 264, 2, 0, -10)                               # *ducks*
            if n == 1 and k == 6:
                w += bmove(side, 264, 2, 0, 10)
            w += wait(1)
        if n < 2:
            w += wait(3)
    w += se(s["kaboom"]) + se(s["bslam"]) + se(s["explo"]) + flash_screen(7) + func(68, 8, 8, 1, 8, 0)   # SMASH
    w += emit_at(WRECK26, 0, 1, (0, 20)) + emit_at(WRECKB26, 0, 1, (0, 10)) + bmove(side, 264, 3, -_sx(side) * -30, 20)
    w += _hold(WRECK26, 1, 0, pos(1.57, 150), 4)
    w += bmove(side, 264, 4, _sx(side) * -30, -20) + shake_defender(4, 3) + func(48)
    for k in range(5):
        w += emit_at(WRECK26, 1, 0, pos(1.57 - (k + 1) * .18, 150)) + wait(1)
    return w + wait(4)


def _headbanger(side, s):
    """Head Smash (Headbanger): two amp stacks. The riff hits - headbang. Again - HEADBANG, pyro going off. Then they
    full-send headbang straight into the foe."""
    sx = _sx(side)
    amps = [_s23(side, 0, (100, 84)), _s23(side, 0, _p(side, (34, 70), (218, 40)))]
    rack = lambda: [w_ for a in amps for w_ in emit_at(HEAD26, 1, 0, a)]
    w = se(s["bass"]) + _hold(HEAD26, 1, 0, amps[0], 3, lambda k: emit_at(HEAD26, 1, 0, amps[1]))
    for n in range(2):                                                         # headbang... HEADBANG
        w += se(s["bdrum"]) + se(s["bass"]) + flash_screen(2)
        for k in range(4):
            w += rack() + bmove(side, 258, 1, sx * 4, -8 if k % 2 == 0 else 8)
            w += bmove(side, 258, 1, -sx * 4, 0) + func(34, 2, 0, 1, (rgb(255, 60, 60), rgb(60, 120, 255))[k % 2], 7 + 3 * n, 0) + wait(1)
        w += emit_at(HEAD26, 0, 0, (amps[n][0], amps[n][1] + 30)) + _hold(HEAD26, 1, 0, amps[0], 3, lambda k: emit_at(HEAD26, 1, 0, amps[1]))
    w += se(s["rage"]) + bmove(side, 258, 2, sx * 30, 12) + rack() + wait(1)  # FULL SEND
    w += se(s["kaboom"]) + se(s["bslam"]) + flash_screen(6) + func(68, 6, 6, 1, 6, 0)
    for a in amps:
        w += emit_at(HEAD26, 3, 0, (a[0], a[1] + 30))
    w += shake_defender(5, 3) + func(48) + rack() + wait(2) + bmove(side, 258, 4, -sx * 30, -12)
    return w + shake_attacker(3, 2) + func(34, 2, 0, 1, rgb(255, 60, 60), 12, 0) + _hold(HEAD26, 1, 0, amps[0], 4, lambda k: emit_at(HEAD26, 1, 0, amps[1]))


def _soaker_flood(side, s):
    """Water Spout (Super Soaker): a giant water gun. Pump. Pump. PUMPPUMPPUMP. Then the whole tank in one blast - a
    flood straight into the foe."""
    sx = _sx(side)
    gun = _p(side, (sx * 26, 26), (-26, 16))
    kit = _p(side, SOAK26, SOAKB26)
    tip = _p(side, (48, 28), (-48, 18))
    w = se(s["pop"]) + _hold(kit, 1, 0, gun, 3)
    for n, (reps, gap) in enumerate(((1, 3), (1, 3), (3, 1))):               # pump... pump... PUMPPUMPPUMP
        for r in range(reps):
            w += se(s["harden"]) + _hold(kit, 2, 0, gun, gap) + _hold(kit, 1, 0, gun, gap)
        if n == 2:
            w += shake_attacker(1, 2)
    w += func(33, 0, 1, 0, 10, rgb(40, 90, 200)) + se(s["hpump"]) + se(s["surf"]) + flash_screen(2)   # FWOOOSH
    w += emit_at(SOAKC26, _p(side, 0, 1), 0, tip) + func(68, 4, 4, 1, 14, 0)
    for k in range(18):
        w += emit_at(kit, 1, 0, (gun[0] - sx * (k % 2), gun[1]))
        if k % 4 == 0:
            w += emit_at(SOAK26, 0, 1, (0, 24)) + shake_defender(2, 1) + se(s["splash"])
        if k == 6:
            w += bmove(side, 264, 4, sx * 14, 4) + func(34, 8, 0, 1, rgb(80, 150, 255), 14, 0)
        w += wait(1)
    w += bmove(side, 264, 4, -sx * 14, -4) + func(48) + func(33, 0, 1, 10, 0, rgb(40, 90, 200))
    return w + _hold(kit, 1, 0, gun, 3)
'''

TABLE = {392: ("_live_wire", ("WIRE26",), "Volt Tackle"),
         393: ("_fire_cart", ("CART26", "CARTB26"), "Flare Blitz"),
         394: ("_wrecker", ("WRECK26", "WRECKB26"), "Rock Wrecker"),
         395: ("_headbanger", ("HEAD26",), "Head Smash"),
         396: ("_soaker_flood", ("SOAK26", "SOAKB26", "SOAKC26"), "Water Spout")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
