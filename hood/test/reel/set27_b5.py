"""Set 27 batch 5: Glow Up, Stomach Bug, Rabbit Foot, Stiff Arm, Hype Howl (variants 444-448).
Run once from the repo root: python -X utf8 hood/test/reel/set27_b5.py  (art: set27_b5_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "GLOW27 GLOWB27 DOG27 DOGB27 LUCK27 LUCKB27 LUCKC27 STIFF27 HOWL27 HOWLB27".split()

KITS = '''
    # ---- set 27, batch 5 ----------------------------------------------------------------------------------
    # Glow Up (Tail Glow): the bonnet comes off - edge gel - swoop, swoop, SWOOP - they GLOW
    b, rs = pk(GLOW27, {1: (fxart.satin_bonnet(), .7, 4, {}), 2: (fxart.edge_gel(), .45, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 240, 160), rgb(255, 255, 255), .35, 4, .1, life=12, radius=.2)
    fin(GLOW27, b, rs, (0, 1, 2))
    b, rs = pk(GLOWB27, {1: (fxart.edge_brush(), .45, 4, {}), 2: (flipx(fxart.edge_brush()), .45, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 220, 90), rgb(255, 255, 255), .6, 24, .34, up=.06, life=24, radius=.6)
    fin(GLOWB27, b, rs, (0, 1, 2))

    # Stomach Bug (Gastro Acid): a gas station hot dog - gulp - rumble - RUMBLE - OUT OF ORDER
    b, rs = pk(DOG27, {1: (fxart.gas_hot_dog(), .6, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(150, 200, 60), n=4, life=18, scl=.26, up=.05)
    fin(DOG27, b, rs, (0, 1))
    b, rs = pk(DOGB27, {1: (fxart.out_of_order(), ONE_TO_ONE, 4, {"colors": 30})})
    fin(DOGB27, b, rs, (1,))

    # Rabbit Foot (Lucky Chant): rub the rabbit foot - scratch - scratch - scratch: WIN $2
    b, rs = pk(LUCK27, {1: (fxart.rabbit_foot(), .5, 4, {}), 2: (fxart.scratch_ticket(), ONE_TO_ONE, 4, {"colors": 30})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(120, 240, 120), rgb(255, 255, 255), .35, 5, .12, life=14, radius=.3)
    fin(LUCK27, b, rs, (0, 1, 2))
    b, rs = pk(LUCKB27, {1: (fxart.scratch_ticket(stage=1), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.scratch_ticket(stage=2), ONE_TO_ONE, 4, {"colors": 30})})
    fin(LUCKB27, b, rs, (1, 2))
    b, rs = pk(LUCKC27, {1: (fxart.scratch_ticket(stage=3), ONE_TO_ONE, 4, {"colors": 30})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 80), rgb(255, 255, 255), .45, 14, .24, up=.08, life=20, radius=.5)
    fin(LUCKC27, b, rs, (0, 1))

    # Stiff Arm (Force Palm): the foe charges - stiff-armed - charges - stiff-armed - the Heisman. Zapped stiff.
    b, rs = pk(STIFF27, {1: (fxart.heisman_statue(), 1.0, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 240, 80), rgb(255, 255, 255), .5, 12, .28, life=12)
    fin(STIFF27, b, rs, (0, 1))

    # Hype Howl (Howl): "AWOOO!" - the stands, quiet... - then the whole crowd howls back
    b, rs = pk(HOWL27, {1: (fxart.howl_crowd(), 1.3, 4, {}), 2: (fxart.howl_crowd(howl=True), 1.3, 4, {})})
    fin(HOWL27, b, rs, (1, 2))
    b, rs = pk(HOWLB27, {1: (fxart.line_bubble(["AWOOO!"]), ONE_TO_ONE, 4, {"colors": 30})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 120, 80), rgb(255, 255, 220), .5, 16, .26, up=.1, life=20, radius=.5)
    fin(HOWLB27, b, rs, (0, 1))
'''

SCRIPTS = '''
def _glow_up(side, s):
    """Tail Glow (Glow Up): the satin bonnet comes off - pop. Edge control. The brush: swoop. Swoop. SWOOP. Edges
    laid - and they GLOW."""
    sx = _sx(side)
    head = (0, 40)
    jar = (sx * 30, 16)
    bres = _p(side, 1, 2)
    w = se(s["pop"]) + _hold(GLOW27, 1, 0, head, 5)
    w += se(s["whoosh"]) + _lob(GLOW27, 1, side, head, (-sx * 50, 60), 4, 16)  # bonnet off
    w += se(s["pop"]) + _hold(GLOW27, 2, 0, jar, 3)
    for n in range(3):                                                         # swoop... swoop... SWOOP
        w += se(s["swipe"])
        for k in range(4):
            w += emit_at(GLOW27, 2, 0, jar) + emit_at(GLOWB27, bres, 0, (sx * (-10 + k * 7), 46 - abs(k - 1.5) * 3)) + wait(1)
        w += emit_at(GLOW27, 0, 0, (sx * 6, 44)) + _hold(GLOW27, 2, 0, jar, 2 + n)
    w += func(33, 0, 1, 0, 10, 0) + se(s["bling"]) + flash_screen(3)          # GLOW UP
    for k in range(12):
        if k % 4 == 0:
            w += emit_at(GLOWB27, 0, 0, (0, 30)) + func(34, 2, 0, 1, rgb(255, 230, 120) if k % 8 == 0 else rgb(255, 255, 255), 13, 0)
        w += wait(1)
    return w + func(33, 0, 1, 10, 0, 0) + wait(2)


def _stomach_bug(side, s):
    """Gastro Acid (Stomach Bug): a gas station roller-grill hot dog, tossed to the foe - gulp. Rumble. RUMBLE. An OUT
    OF ORDER sign gets hung on them."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = se(s["whoosh"]) + _lob(DOG27, 1, side, (sx * 20, 30), (dx, dy + 30), 6, 22)
    w += se(s["crunch"]) + shake_defender(1, 1) + wait(6)                    # gulp
    for n in range(2):                                                         # rumble... RUMBLE
        w += se(s["rollout"]) + shake_defender(1 + n * 2, 3) + emit_at(DOG27, 0, 1, (0, 20))
        w += func(34, 8, 0, 1, rgb(150, 200, 60), 9 + n * 3, 0) + wait(6)
    for k in range(4):                                                         # OUT OF ORDER
        w += emit_at(DOGB27, 1, 1, (0, 54 - k * 10)) + wait(1)
    w += se(s["bonk"]) + se(s["disable"]) + _hold(DOGB27, 1, 1, (0, 14), 12)
    return w + wait(2)


def _rabbit_foot(side, s):
    """Lucky Chant (Rabbit Foot): rub the lucky rabbit foot - then the scratch-off: scratch - a 7. Scratch - 7. Scratch -
    7 - WIN... $2. Hey, a win's a win."""
    sx = _sx(side)
    foot = (sx * 26, 36)
    tkt = _s23(side, 0, _p(side, (112, 70), (130, 64)))
    w = se(s["pop"])
    for k in range(6):                                                         # rub rub
        w += emit_at(LUCK27, 1, 0, (foot[0] + (k % 2) * 2, foot[1] + (k % 2))) + (emit_at(LUCK27, 0, 0, foot) if k % 3 == 0 else []) + wait(1)
    w += se(s["pop"]) + _hold(LUCK27, 2, 0, tkt, 4)
    for kit, res in ((LUCKB27, 1), (LUCKB27, 2)):                             # scratch... scratch...
        w += se(s["swipe"]) + _hold(kit, res, 0, tkt, 6)
    w += se(s["swipe"]) + _hold(LUCKC27, 1, 0, tkt, 3) + se(s["bling"]) + emit_at(LUCKC27, 0, 0, tkt)   # WIN $2
    return w + _hold(LUCKC27, 1, 0, tkt, 10)


def _stiff_arm(side, s):
    """Force Palm (Stiff Arm): the foe charges in - STIFF ARM, sent back. Charges again - STIFF ARM. The gold Heisman
    pose. The foe's left twitching."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    run = (round(-dx * .45), round(-dy * .45))
    w = []
    for n in range(2):                                                         # charge... STIFF ARM
        w += se(s["whoosh"]) + bmove(side, 264, 4, run[0], run[1]) + wait(3)
        w += se(s["bslam"]) + emit_at(STIFF27, 0, 0, (sx * 30, 26)) + flash_screen(2)
        w += bmove(side, 264, 3, -run[0], -run[1]) + wait(4)
    w += se(s["bling"]) + func(33, 0, 1, 0, 8, 0) + _hold(STIFF27, 1, 0, (sx * 30, 24), 8)   # the Heisman
    w += se(s["spark"]) + shake_defender(3, 3) + func(34, 8, 0, 1, rgb(255, 240, 80), 13, 0)
    for k in range(8):
        w += emit_at(STIFF27, 1, 0, (sx * 30, 24)) + (emit_at(STIFF27, 0, 1, (0, 24)) if k % 3 == 0 else []) + wait(1)
    return w + func(48) + func(33, 0, 1, 8, 0, 0) + wait(2)


def _hype_howl(side, s):
    """Howl (Hype Howl): "AWOOO!" - the stands... nothing. AWOOO! - one fan. Then the WHOLE crowd throws their heads
    back and howls. Hyped up."""
    crowd = _s23(side, 0, _p(side, (150, 54), (100, 62)))
    bub = _s23(side, 0, _p(side, (78, 72), (170, 30)))
    w = se(s["pop"]) + _hold(HOWLB27, 1, 0, bub, 8, lambda k: emit_at(HOWL27, 1, 0, crowd))   # AWOOO!
    w += _hold(HOWL27, 1, 0, crowd, 8)                                        # ...crickets
    w += se(s["rage"]) + _hold(HOWLB27, 1, 0, bub, 6, lambda k: emit_at(HOWL27, 1, 0, crowd))
    w += se(s["rage"]) + se(s["bslam"]) + flash_screen(2)                     # the WHOLE crowd
    for k in range(14):
        w += emit_at(HOWL27, 2, 0, (crowd[0], crowd[1] + (k % 2)))
        if k % 4 == 0:
            w += emit_at(HOWLB27, 0, 0, (0, 30)) + func(34, 2, 0, 1, rgb(255, 120, 80), 12, 0)
        w += wait(1)
    return w + _hold(HOWL27, 1, 0, crowd, 3)
'''

TABLE = {444: ("_glow_up", ("GLOW27", "GLOWB27"), "Tail Glow"),
         445: ("_stomach_bug", ("DOG27", "DOGB27"), "Gastro Acid"),
         446: ("_rabbit_foot", ("LUCK27", "LUCKB27", "LUCKC27"), "Lucky Chant"),
         447: ("_stiff_arm", ("STIFF27",), "Force Palm"),
         448: ("_hype_howl", ("HOWL27", "HOWLB27"), "Howl")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
