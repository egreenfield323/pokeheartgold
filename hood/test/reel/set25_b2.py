"""Set 25 batch 2: Spoon Bend, Pinched, Lights Out, Palm Reader, Jackhammer (variants 367-371).
Run once from the repo root: python -X utf8 hood/test/reel/set25_b2.py  (art: set25_b2_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "SPOON25 SPOONB25 SPOONC25 PIN25 PINB25 LAMP25 LAMPB25 LAMPC25 PALM25 PALMB25 JACK25 JACKB25".split()

KITS = '''
    # ---- set 25, batch 2 ----------------------------------------------------------------------------------
    # Spoon Bend (Kinesis): a spoon - bends. A fork - bends. A whole STOP sign - bends. The foe's seeing things.
    b, rs = pk(SPOON25, {1: (fxart.bent_spoon(), .8, 4, {}), 2: (fxart.bent_spoon(bent=True), .8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(200, 120, 255), rgb(255, 230, 255), .4, 8, .12, life=16)
    fin(SPOON25, b, rs, (0, 1, 2))
    b, rs = pk(SPOONB25, {1: (fxart.bent_fork(), .8, 4, {}), 2: (fxart.bent_fork(bent=True), .8, 4, {})})
    fin(SPOONB25, b, rs, (1, 2))
    b, rs = pk(SPOONC25, {1: (fxart.stop_post(), ONE_TO_ONE, 4, {}), 2: (fxart.stop_post(bent=True), ONE_TO_ONE, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 60), rgb(255, 255, 220), .4, 7, .08, up=.02, life=26, radius=.5)
    fin(SPOONC25, b, rs, (0, 1, 2))

    # Pinched (ViceGrip): a clothespin on the foe - a bigger one - a GIANT one
    b, rs = pk(PIN25, {1: (fxart.clothespin(), .5, 4, {}), 2: (fxart.clothespin(), .9, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .4, 6, .16, life=10)
    fin(PIN25, b, rs, (0, 1, 2))
    b, rs = pk(PINB25, {1: (fxart.clothespin(), 2.0, 4, {})})
    fin(PINB25, b, rs, (1,))

    # Lights Out (Guillotine): the lamp clicks off - back on - then the breaker box: total blackout. LIGHTS OUT.
    b, rs = pk(LAMP25, {1: (fxart.floor_lamp(), 1.0, 4, {}), 2: (fxart.floor_lamp(on=False), 1.0, 4, {})})
    fin(LAMP25, b, rs, (1, 2))
    b, rs = pk(LAMPB25, {1: (fxart.breaker_box(), .9, 4, {}), 2: (fxart.breaker_box(off=True), .9, 4, {})})
    fin(LAMPB25, b, rs, (1, 2))
    b, rs = pk(LAMPC25, {1: (fxart.burst_sign(["LIGHTS OUT."], fill=(30, 30, 40, 255), text=(255, 230, 80, 255)), SIGN_SCALE, 4, {"colors": 30})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .6, 14, .32, life=12)
    fin(LAMPC25, b, rs, (0, 1))

    # Palm Reader (Mind Reader): the PSYCHIC neon, the crystal ball: mist... more mist... a target - locked on
    b, rs = pk(PALM25, {1: (fxart.psychic_sign(), ONE_TO_ONE, 4, {}), 2: (fxart.seer_ball(), .9, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(220, 140, 255), rgb(255, 240, 255), .4, 8, .1, up=.04, life=18)
    fin(PALM25, b, rs, (0, 1, 2))
    b, rs = pk(PALMB25, {1: (fxart.seer_ball(vision=1), .9, 4, {}), 2: (fxart.seer_ball(vision=2), .9, 4, {})}, alpha=fxart.ring())
    prop(b, rs, 0, tex=0, clr=rgb(255, 50, 50), clr_anm=(rgb(255, 200, 200), rgb(230, 20, 20)), scl=1.2, life=16,
         alpha=(31, 31, 0), scl_anm=(2.4, .6, .5, 160, 255))
    fin(PALMB25, b, rs, (0, 1, 2))

    # Jackhammer (Drill Peck): 6 AM - BRRRT, the foe's window lights up - BRRRRRT, "ITS 6 AM!!" - so they jackhammer
    # the foe
    b, rs = pk(JACK25, {1: (fxart.jackhammer(), .9, 4, {}), 2: (fxart.apt_window(), 1.0, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(190, 175, 155), n=5, life=18, scl=.3, up=.06)
    fin(JACK25, b, rs, (0, 1, 2))
    b, rs = pk(JACKB25, {1: (fxart.apt_window(lit=True), 1.0, 4, {}), 2: (fxart.line_bubble(["ITS 6 AM!!"]), ONE_TO_ONE, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 120), rgb(255, 255, 255), .4, 8, .22, life=8)
    fin(JACKB25, b, rs, (0, 1, 2))
'''

SCRIPTS = '''
def _spoon_bend(side, s):
    """Kinesis (Spoon Bend): they stare down a spoon - it bends. A fork - it bends. Then a whole STOP sign out of the
    sidewalk - it bends right over. The foe can't believe their eyes."""
    spot = _s23(side, 0, (106, 86))
    w = []
    for n, (kit, k1, k2) in enumerate(((SPOON25, 1, 2), (SPOONB25, 1, 2), (SPOONC25, 1, 2))):
        w += se(s["pop"]) + _hold(kit, k1, 0, spot, 3 + n)
        w += se(s["psych"]) + func(34, 2, 0, 1, rgb(200, 120, 255), 8 + 3 * n, 0) + emit_at(SPOON25, 0, 0, (spot[0], spot[1] + 10))
        for k in range(4 + n):                                                 # *concentrates*
            w += emit_at(kit, k1, 0, (spot[0] + (1 if k % 2 else -1) * (1 + n), spot[1])) + wait(1)
        w += se(s["harden"] if n < 2 else s["bslam"]) + _hold(kit, k2, 0, spot, 5 + n)
        if n == 1:
            w += shake_defender(1, 1)
    w += se(s["confuse"]) + emit_at(SPOONC25, 0, 1, (0, 40))
    for k in range(8):                                                         # *the foe's seeing things*
        w += emit_at(SPOONC25, 2, 0, spot)
        if k % 3 == 0:
            w += bmove(side, 264, 2, 6 if k % 2 == 0 else -6, 0)
        if k % 3 == 1:
            w += bmove(side, 264, 2, -6 if k % 2 == 0 else 6, 0)
        w += wait(1)
    return w + wait(2)


def _pinched(side, s):
    """ViceGrip (Pinched): a clothespin snaps onto the foe - yow. A bigger one - YOW. Then a giant clothespin
    clamps the whole foe."""
    w = []
    pins = [(PIN25, 1, (-14, 30)), (PIN25, 2, (16, 18))]
    on = []
    dress = lambda: [w_ for i in on for w_ in emit_at(pins[i][0], pins[i][1], 1, pins[i][2])]
    for n, (kit, res, at) in enumerate(pins):                                  # snap... SNAP
        for k in range(3):
            w += emit_at(kit, res, 1, (at[0] - 30 + k * 10, at[1] + 20 - k * 6)) + dress() + wait(1)
        on.append(n)
        w += se(s["bite"]) + emit_at(PIN25, 0, 1, at) + shake_defender(1 + n, 2) + func(34, 8, 0, 1, rgb(255, 80, 80), 7 + 3 * n, 0)
        w += _hold(kit, res, 1, at, 4, lambda k: dress())
    for k in range(4):                                                         # the GIANT one
        w += emit_at(PINB25, 1, 1, (0, 24 + (3 - k) * 14)) + dress() + wait(1)
    w += se(s["bite"]) + se(s["bslam"]) + flash_screen(3) + shake_defender(4, 3) + func(48) + func(34, 8, 0, 1, rgb(255, 60, 60), 13, 0)
    return w + _hold(PINB25, 1, 1, (0, 24), 8, lambda k: dress())


def _lights_out(side, s):
    """Guillotine (Lights Out): click - the lamp goes off. Click - back on, the foe breathes. Then the attacker pulls
    the main breaker: total blackout... a single hit in the dark. LIGHTS OUT."""
    lamp = _s23(side, 0, _p(side, (226, 70), (24, 92)))
    box = _s23(side, 0, (106, 84))
    w = se(s["pop"]) + _hold(LAMP25, 1, 0, lamp, 4)
    w += se(s["lockon"]) + func(33, 0, 1, 0, 6, 0) + _hold(LAMP25, 2, 0, lamp, 6, lambda k: shake_defender(1, 1) if k == 2 else [])   # click (off)
    w += se(s["lockon"]) + func(33, 0, 1, 6, 0, 0) + _hold(LAMP25, 1, 0, lamp, 5)   # click (on) - phew
    w += se(s["pop"]) + _hold(LAMPB25, 1, 0, box, 4, lambda k: emit_at(LAMP25, 1, 0, lamp))
    w += se(s["bslam"]) + func(33, 0, 1, 0, 16, 0) + _hold(LAMPB25, 2, 0, box, 5)   # *KA-CHUNK* - blackout
    w += wait(4) + se(s["kaboom"]) + flash_screen(2) + emit_at(LAMPC25, 0, 1, (0, 24)) + shake_defender(5, 4) + func(48)   # *...WHAM*
    sign = _p(side, (0, 58), (0, 50))
    w += _hold(LAMPC25, 1, 0, sign, 10, lambda k: func(34, 8, 0, 1, rgb(30, 30, 40), 14, 0) if k == 2 else [])
    return w + func(33, 0, 1, 16, 0, 0) + wait(4)


def _palm_reader(side, s):
    """Mind Reader (Palm Reader): a neon PSYCHIC sign flickers on. The crystal ball: mist. More mist. Then the vision -
    a target - and the foe's locked in."""
    sign = _s23(side, 0, (214, 24))
    ball = _s23(side, 0, (106, 86))
    neon = lambda k: emit_at(PALM25, 1, 0, sign) if k % 6 != 5 else []
    w = func(33, 0, 1, 0, 8, rgb(40, 20, 60)) + se(s["zap"]) + _hold(PALM25, 1, 0, sign, 3)
    for n, (kit, res) in enumerate(((PALM25, 2), (PALMB25, 1))):             # mist... more mist...
        w += se(s["psych"]) + emit_at(PALM25, 0, 0, (ball[0], ball[1] + 4))
        w += _hold(kit, res, 0, ball, 8, neon)
    w += se(s["lockon"]) + flash_screen(2) + _hold(PALMB25, 2, 0, ball, 4, neon)   # *the vision*
    w += se(s["lockon2"]) + emit_at(PALMB25, 0, 1, (0, 24))
    w += _hold(PALMB25, 2, 0, ball, 8, lambda k: neon(k) + (shake_defender(1, 2) + func(34, 8, 0, 1, rgb(255, 60, 60), 10, 0) if k == 3 else []))
    return w + func(33, 0, 1, 8, 0, rgb(40, 20, 60)) + wait(2)


def _jackhammer(side, s):
    """Drill Peck (Jackhammer): 6 AM. BRRRRT - the foe's window lights up. BRRRRRRT - "ITS 6 AM!!" - so the attacker
    swings the jackhammer round and goes to work on the foe."""
    sx = _sx(side)
    jh = _s23(side, 0, (110, 92))
    win = _s23(side, 0, _p(side, (232, 38), (20, 84)))
    bub = _p(side, (-30, 36), (50, 58))
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = func(33, 0, 1, 0, 8, rgb(30, 30, 70)) + _hold(JACK25, 2, 0, win, 3, lambda k: emit_at(JACK25, 1, 0, jh))
    for n in range(2):                                                         # BRRRT... BRRRRRT
        w += se(s["rollout"])
        for k in range(6 + 3 * n):
            w += emit_at(JACK25, 1, 0, (jh[0] + (k % 2), jh[1] + (2 if k % 2 else 0))) + emit_at(JACK25 if n == 0 and k < 3 else JACKB25, 2 if n == 0 and k < 3 else 1, 0, win)
            if k % 3 == 0:
                w += se(s["rollout"]) + emit_at(JACK25, 0, 0, (jh[0], jh[1] - 18))
            w += wait(1)
        if n == 1:
            w += _hold(JACKB25, 2, 1, bub, 10, lambda k: emit_at(JACKB25, 1, 0, win) + emit_at(JACK25, 1, 0, jh) + (shake_defender(1, 1) if k == 2 else []))
        else:
            w += _hold(JACKB25, 1, 0, win, 3, lambda k: emit_at(JACK25, 1, 0, jh))
    w += se(s["whoosh"]) + _lob(JACK25, 1, side, jh, (dx, dy + 40), 4, 16, lambda k: emit_at(JACKB25, 1, 0, win))   # *turns it on the foe*
    w += se(s["rollout"])
    for k in range(14):                                                        # BRRRRRRRRRT
        w += emit_at(JACK25, 1, 1, ((k % 2) * 3 - 1, 40 + (k % 3))) + emit_at(JACKB25, 1, 0, win)
        if k % 2 == 0:
            w += emit_at(JACKB25, 0, 1, (0, 30)) + shake_defender(2, 1) + (se(s["rollout"]) if k % 4 == 0 else [])
        w += wait(1)
    w += se(s["bslam"]) + flash_screen(3) + func(48) + func(33, 0, 1, 8, 0, rgb(30, 30, 70))
    return w + wait(3)
'''

TABLE = {367: ("_spoon_bend", ("SPOON25", "SPOONB25", "SPOONC25"), "Kinesis"),
         368: ("_pinched", ("PIN25", "PINB25"), "ViceGrip"),
         369: ("_lights_out", ("LAMP25", "LAMPB25", "LAMPC25"), "Guillotine"),
         370: ("_palm_reader", ("PALM25", "PALMB25"), "Mind Reader"),
         371: ("_jackhammer", ("JACK25", "JACKB25"), "Drill Peck")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
