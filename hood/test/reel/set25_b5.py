"""Set 25 batch 5: Two-Piece, Jump Out, Roll Up, Waffle Iron, Bazooka (variants 382-386).
Run once from the repo root: python -X utf8 hood/test/reel/set25_b5.py  (art: set25_b5_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "CHICK25 BUSH25 SKATE25 WAFF25 GUM25 GUMB25".split()

KITS = '''
    # ---- set 25, batch 5 ----------------------------------------------------------------------------------
    # Two-Piece (Comet Punch): a fried drumstick off the foe's head (replays per hit: short)
    b, rs = pk(CHICK25, {1: (fxart.drumstick(), .5, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(220, 160, 80), rgb(250, 220, 160), .3, 10, .2, up=.14, gravity=.018, life=16)
    fin(CHICK25, b, rs, (0, 1))

    # Jump Out (Jump Kick): a bush - rustle - rustle - and they JUMP OUT of it knee first
    b, rs = pk(BUSH25, {1: (fxart.shrub(), 1.4, 4, {}), 2: (fxart.shrub(rustle=1), 1.4, 4, {})}, alpha=fxart.feather())
    burst(b, rs, 0, rgb(80, 180, 70), rgb(160, 230, 140), .4, 14, .26, up=.16, gravity=.01, life=26, spin=0x0800)
    burst(b, rs, 3, rgb(255, 250, 200), rgb(255, 255, 255), .5, 10, .3, life=10)
    fin(BUSH25, b, rs, (0, 1, 2, 3))

    # Roll Up (Rolling Kick): skates on - wobble - wobble - then a spin and a kick
    b, rs = pk(SKATE25, {1: (fxart.roller_skate(), .6, 4, {}), 2: (flipx(fxart.roller_skate()), .6, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .5, 12, .3, life=12)
    fin(SKATE25, b, rs, (0, 1, 2))

    # Waffle Iron (Clamp): the foe on the bottom plate - SLAM - sizzle - waffled (replays as a trap: short)
    b, rs = pk(WAFF25, {1: (fxart.waffle_iron(), 1.5, 4, {}), 2: (fxart.waffle_iron(shut=True), 1.5, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(240, 240, 245), n=5, life=20, scl=.3, up=.1)
    fin(WAFF25, b, rs, (0, 1, 2))

    # Bazooka (Octazooka): bubblegum - a bubble, bigger, HUGE - POP, all over the foe's face
    b, rs = pk(GUM25, {1: (fxart.gum_bubble(), .35, 4, {}), 2: (fxart.gum_bubble(), .8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 160, 220), rgb(255, 255, 255), .5, 14, .3, life=12)
    fin(GUM25, b, rs, (0, 1, 2))
    b, rs = pk(GUMB25, {1: (fxart.gum_bubble(), 1.6, 4, {}), 2: (fxart.gum_splat(), .9, 4, {})})
    fin(GUMB25, b, rs, (1, 2))
'''

SCRIPTS = '''
def _two_piece(side, s):
    """Comet Punch (Two-Piece): a fried drumstick off the foe's head - bonk, crumbs. (Replays per hit.)"""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = se(s["whoosh"]) + _lob(CHICK25, 1, side, (sx * 20, 30), (dx, dy + 38), 5, 22)
    w += se(s["bonk"]) + emit_at(CHICK25, 0, 1, (0, 38)) + shake_defender(2, 2)
    return w + _lob(CHICK25, 1, side, (dx, dy + 38), (dx + sx * 30, dy + 60), 3, 8) + wait(1)


def _jump_out(side, s):
    """Jump Kick (Jump Out): a bush where the attacker was. Rustle. The foe looks. Rustle. Then they JUMP OUT the bush
    knee first into the foe."""
    sx = _sx(side)
    bush = _s23(side, 1, _p(side, (64, 124), (185, 70)))
    leap = _p(side, (88, 50), (-92, -46))
    b = lambda r=1: emit_at(BUSH25, r, 1, bush)
    w = se(s["whoosh"]) + func(40, 2, 1) + _hold(BUSH25, 1, 1, bush, 4)        # *ducks in*
    for n in range(2):                                                         # rustle... rustle...
        w += se(s["swipe"])
        for k in range(4):
            w += b(1 + k % 2) + wait(1)
        w += _hold(BUSH25, 1, 1, bush, 3, lambda k: bmove(side, 264, 2, -sx * 6, 0) if k == 0 and n == 0 else (bmove(side, 264, 2, sx * 6, 0) if k == 2 and n == 0 else []))
    w += _hold(BUSH25, 1, 1, bush, 3)                                          # *...*
    w += func(40, 2, 0) + se(s["whoosh"]) + emit_at(BUSH25, 0, 1, (bush[0], bush[1] + 10)) + bmove(side, 258, 3, *leap) + b() + wait(1)   # JUMP OUT
    w += b() + wait(1) + se(s["kaboom"]) + se(s["bslam"]) + flash_screen(4) + emit_at(BUSH25, 3, 1, (0, 24))
    w += shake_defender(4, 3) + func(48) + func(68, 3, 3, 1, 3, 0)
    w += _hold(BUSH25, 1, 1, bush, 2) + bmove(side, 258, 5, -leap[0], -leap[1])
    return w + _hold(BUSH25, 1, 1, bush, 4)


def _roll_up(side, s):
    """Rolling Kick (Roll Up): roller skates. Wobble - wobble - then they get it going, spin, and roll a kick right into
    the foe."""
    sx = _sx(side)
    sk = _p(side, (sx * 22, 8), (-22, -6))
    res = _p(side, 1, 2)
    skate = lambda dxx=0: emit_at(SKATE25, res, 0, (sk[0] + dxx, sk[1]))
    w = se(s["pop"]) + _hold(SKATE25, res, 0, sk, 3)
    for n, d_ in enumerate((-8, 8)):                                           # wobble... wobble...
        w += se(s["rollout"]) + bmove(side, 258, 3, d_, 0) + skate() + wait(1)
        w += shake_attacker(1, 2) + skate(2) + wait(1) + skate(-2) + wait(1)
        w += bmove(side, 258, 3, -d_, 0) + skate() + wait(2)
    w += se(s["rollout"])
    for k in range(6):                                                         # *spinnn*
        w += bmove(side, 258, 1, 8 if k % 2 == 0 else -8, 0) + skate() + wait(1)
    w += bmove(side, 258, 3, sx * 26, 10) + skate() + wait(1)                 # KICK
    w += se(s["kaboom"]) + se(s["bslam"]) + flash_screen(3) + emit_at(SKATE25, 0, 1, (0, 24)) + shake_defender(4, 3) + func(48)
    return w + bmove(side, 258, 4, -sx * 26, -10) + _hold(SKATE25, res, 0, sk, 3)


def _waffle_iron(side, s):
    """Clamp (Waffle Iron): the foe's sat on the bottom plate of a waffle iron - SLAM - sizzle sizzle - pop it open:
    golden brown. (Replays as a trap: short.)"""
    at = (0, 10)
    w = se(s["pop"]) + _hold(WAFF25, 1, 1, (0, 70), 4)                         # *it hovers over them*
    for k in range(3):
        w += emit_at(WAFF25, 1, 1, (0, 70 - (k + 1) * 18)) + wait(1)
    w += se(s["bslam"]) + shake_defender(2, 2) + _hold(WAFF25, 2, 1, at, 1)     # SLAM
    for k in range(10):                                                        # *sizzle*
        w += emit_at(WAFF25, 2, 1, at)
        if k % 3 == 0:
            w += emit_at(WAFF25, 0, 1, (0, 30)) + se(s["ember"])
        w += wait(1)
    w += se(s["bling"]) + func(34, 8, 0, 1, rgb(230, 170, 60), 12, 0)        # *ding* - golden brown
    return w + _hold(WAFF25, 1, 1, at, 5)


def _bazooka(side, s):
    """Octazooka (Bazooka): bubblegum. A little bubble - pop. A bigger bubble. Then a HUGE one... it floats over to
    the foe - POP - gum all over their face."""
    sx = _sx(side)
    mouth = _p(side, (sx * 12, 32), (-12, 24))
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = []
    for kit, res, ticks in ((GUM25, 1, 4), (GUM25, 2, 5)):                    # blow... blow...
        for k in range(ticks):
            w += emit_at(kit, res, 0, (mouth[0] + sx * k, mouth[1])) + wait(1)
        w += se(s["pop"]) + emit_at(GUM25, 0, 0, mouth) + wait(3)
    for k in range(6):                                                         # HUGE
        w += emit_at(GUMB25, 1, 0, (mouth[0] + sx * (4 + k * 2), mouth[1] + k)) + wait(1)
    for k, p in enumerate(_arc((mouth[0] + sx * 16, mouth[1] + 6), (dx, dy + 28), 6, 20)[1:]):   # *floats over*
        w += emit_at(GUMB25, 1, 0, p) + wait(1)
    w += se(s["pop"]) + se(s["splat"]) + flash_screen(2) + emit_at(GUM25, 0, 1, (0, 28))   # POP
    w += func(34, 8, 0, 1, rgb(255, 140, 200), 12, 0) + shake_defender(2, 2)
    for k in range(10):
        w += emit_at(GUMB25, 2, 1, (0, 28))
        if k in (3, 6):
            w += bmove(side, 264, 2, 6 if k == 3 else -6, 0)
        w += wait(1)
    return w + wait(2)
'''

TABLE = {382: ("_two_piece", ("CHICK25",), "Comet Punch"),
         383: ("_jump_out", ("BUSH25",), "Jump Kick"),
         384: ("_roll_up", ("SKATE25",), "Rolling Kick"),
         385: ("_waffle_iron", ("WAFF25",), "Clamp"),
         386: ("_bazooka", ("GUM25", "GUMB25"), "Octazooka")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
