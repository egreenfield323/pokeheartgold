"""Set 27 batch 6: Namaste, Lock Up, Look at Me, Snowball, Hoverboard (variants 449-453).
Run once from the repo root: python -X utf8 hood/test/reel/set27_b6.py  (art: set27_b6_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "YOGA27 GATE27 LOOK27 SNOW27 HOVER27".split()

KITS = '''
    # ---- set 27, batch 6 ----------------------------------------------------------------------------------
    # Namaste (Meditate): the yoga mat - stretch - deeper - deeper - CRACK! - ...they feel great actually
    b, rs = pk(YOGA27, {1: (fxart.yoga_mat(), 1.2, 4, {}),
                        2: (fxart.burst_sign(["CRACK!"], fill=(255, 250, 230, 255), text=(40, 40, 40, 255)), SIGN_SCALE, 4, {"colors": 30})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 140, 90), rgb(255, 255, 220), .45, 14, .24, up=.08, life=20, radius=.5)
    fin(YOGA27, b, rs, (0, 1, 2))

    # Lock Up (Imprison): the corner store gate comes down - rattle - rattle - SLAM - padlock click
    b, rs = pk(GATE27, {1: (fxart.roll_gate(), 1.4, 4, {}), 2: (fxart.big_padlock(), .5, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(180, 170, 150), n=5, life=16, scl=.3, up=.04)
    fin(GATE27, b, rs, (0, 1, 2))

    # Look at Me (Follow Me): the marquee sign blinking LOOK over them - the foe glances - glances - can't look away
    b, rs = pk(LOOK27, {1: (fxart.marquee_down(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.marquee_down(phase=1), ONE_TO_ONE, 4, {"colors": 30})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 240, 120), rgb(255, 255, 255), .4, 5, .12, life=16, radius=.4)
    fin(LOOK27, b, rs, (0, 1, 2))

    # Snowball (Ice Ball): packed - thrown - SPLAT (replays every turn: short)
    b, rs = pk(SNOW27, {1: (fxart.snowball(), .6, 4, {})}, alpha=fxart.soft_puff())
    burst(b, rs, 0, rgb(240, 248, 255), rgb(255, 255, 255), .32, 14, .26, up=.12, gravity=.012, life=18)
    fin(SNOW27, b, rs, (0, 1))

    # Hoverboard (Magnet Rise): on the hoverboard - wobble - wobble - then it actually lifts off
    b, rs = pk(HOVER27, {1: (fxart.hoverboard(), .9, 4, {}), 2: (fxart.hoverboard(glow=True), .9, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(120, 220, 255), rgb(255, 255, 255), .4, 8, .14, up=-.04, life=16, radius=.4)
    fin(HOVER27, b, rs, (0, 1, 2))
'''

SCRIPTS = '''
def _namaste(side, s):
    """Meditate (Namaste): a yoga mat rolls out. Stretch - up. Lean - deeper. Deeper... CRACK! A long pause. Then...
    they actually feel amazing. Power up."""
    sx = _sx(side)
    mat = (0, 8)
    m = lambda: emit_at(YOGA27, 1, 0, mat)
    w = se(s["pop"]) + _hold(YOGA27, 1, 0, mat, 4)
    w += se(s["swipe"]) + bmove(side, 258, 3, 0, 8) + _hold(YOGA27, 1, 0, mat, 6)   # stretch
    w += se(s["swipe"]) + bmove(side, 258, 3, sx * 6, -4) + _hold(YOGA27, 1, 0, mat, 6)   # deeper
    w += bmove(side, 258, 3, sx * 4, -2) + _hold(YOGA27, 1, 0, mat, 3)        # deeper...
    w += se(s["crack"]) + se(s["bonk"]) + shake_attacker(2, 2)               # CRACK!
    for k in range(10):
        w += m() + emit_at(YOGA27, 2, 0, (sx * 24, 56)) + wait(1)
    w += bmove(side, 258, 3, -sx * 10, -2) + _hold(YOGA27, 1, 0, mat, 6)      # ...
    w += se(s["bling"]) + emit_at(YOGA27, 0, 0, (0, 30)) + func(34, 2, 0, 1, rgb(255, 140, 90), 12, 0)   # feels great
    return w + _hold(YOGA27, 1, 0, mat, 8)


def _lock_up(side, s):
    """Imprison (Lock Up): the corner store's roll-down gate drops in front of the foe - rattle, sticks. Rattle, sticks.
    SLAM. Padlock - click. Closed."""
    gate = lambda y: emit_at(GATE27, 1, 1, (0, y))
    w = se(s["pop"])
    for n, (y0, y1) in enumerate(((110, 64), (64, 42))):                       # rattle... sticks
        for k in range(4):
            w += gate(round(y0 + (y1 - y0) * (k + 1) / 4)) + wait(1)
        w += se(s["clock"]) + _hold(GATE27, 1, 1, (0, y1), 5)
    for k in range(3):                                                         # SLAM
        w += gate(round(42 - 26 * (k + 1) / 3)) + wait(1)
    w += se(s["bslam"]) + se(s["crunch"]) + flash_screen(2) + emit_at(GATE27, 0, 1, (0, -6)) + shake_defender(3, 2)
    w += _hold(GATE27, 1, 1, (0, 16), 4)
    w += se(s["lockon"]) + _hold(GATE27, 2, 1, (0, 0), 1, lambda k: gate(16))   # *click*
    w += func(34, 8, 0, 1, rgb(100, 100, 110), 12, 0)
    for k in range(10):
        w += emit_at(GATE27, 2, 1, (0, 0)) + gate(16) + wait(1)
    return w


def _look_at_me(side, s):
    """Follow Me (Look at Me): a Vegas marquee pops up over them blinking LOOK. The foe glances over - looks away.
    Glances - looks away. Then it just can't stop looking."""
    sx = _sx(side)
    sign = _s23(side, 0, _p(side, (100, 72), (176, 34)))
    blink = lambda k: emit_at(LOOK27, 1 + (k // 2) % 2, 0, sign)
    w = se(s["pop"])
    k = 0
    for n in range(2):                                                         # glance... away
        for j in range(6):
            w += blink(k) + (bmove(side, 264, 2, -sx * 6, 0) if j == 1 else []) + (bmove(side, 264, 2, sx * 6, 0) if j == 4 else []) + wait(1)
            k += 1
        w += se(s["bling"])
    w += se(s["mlook"]) + bmove(side, 264, 3, -sx * 10, 0) + func(34, 8, 0, 1, rgb(255, 230, 120), 12, 0)   # locked on
    for j in range(12):
        w += blink(k) + (emit_at(LOOK27, 0, 0, (sign[0], sign[1] - 20)) if j % 4 == 0 else []) + wait(1)
        k += 1
    return w + bmove(side, 264, 3, sx * 10, 0) + wait(2)


def _snowball(side, s):
    """Ice Ball (Snowball): packed - pat pat - thrown - SPLAT. (Replays every turn: short.)"""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    hand = (sx * 22, 30)
    w = se(s["pop"])
    for k in range(4):                                                         # pat pat
        w += emit_at(SNOW27, 1, 0, (hand[0], hand[1] + (k % 2))) + (se(s["flop"]) if k % 2 == 0 else []) + wait(1)
    w += se(s["whoosh"]) + _lob(SNOW27, 1, side, hand, (dx, dy + 26), 5, 16)
    w += se(s["splat"]) + emit_at(SNOW27, 0, 1, (0, 26)) + shake_defender(2, 2) + func(34, 8, 0, 1, rgb(200, 230, 255), 10, 0)
    return w + wait(6)


def _hoverboard(side, s):
    """Magnet Rise (Hoverboard): they hop on a hoverboard - wobble - WOBBLE, almost eats it - then the thing lights up
    and actually lifts off the ground. Floating."""
    sx = _sx(side)
    foot = _p(side, 8, -6)
    board = lambda r, x=0, y=0: emit_at(HOVER27, r, 0, (x, foot + y))
    w = se(s["pop"]) + _hold(HOVER27, 1, 0, (0, foot), 4)
    for n, amp in enumerate((4, 8)):                                           # wobble... WOBBLE
        for j, dx in enumerate((amp, -2 * amp, amp)):
            w += bmove(side, 258, 2, dx, 0) + se(s["whoosh"] if j == 1 else s["swipe"])
            off = (amp, -amp, 0)[j]
            for k in range(2):
                w += board(1, off) + wait(1)
        w += _hold(HOVER27, 1, 0, (0, foot), 2)
    w += se(s["mbomb"]) + se(s["bling"]) + flash_screen(2)                    # it LIFTS OFF
    w += bmove(side, 258, 6, 0, 14)
    for k in range(6):
        w += board(2, 0, round(14 * (k + 1) / 6)) + wait(1)
    for k in range(12):                                                        # floating
        y = 14 + (2 if (k // 3) % 2 else 0)
        w += board(2, 0, y) + (emit_at(HOVER27, 0, 0, (0, foot + y - 4)) if k % 4 == 0 else []) + wait(1)
    w += bmove(side, 258, 4, 0, -14)
    for k in range(4):
        w += board(2, 0, round(14 * (1 - (k + 1) / 4))) + wait(1)
    return w + _hold(HOVER27, 2, 0, (0, foot), 3)
'''

TABLE = {449: ("_namaste", ("YOGA27",), "Meditate"),
         450: ("_lock_up", ("GATE27",), "Imprison"),
         451: ("_look_at_me", ("LOOK27",), "Follow Me"),
         452: ("_snowball", ("SNOW27",), "Ice Ball"),
         453: ("_hoverboard", ("HOVER27",), "Magnet Rise")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
