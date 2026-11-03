"""Set 25 batch 3: 360 Deal, Eat Good, Waterworks, Bone Toss, Shmoney (variants 372-376).
Run once from the repo root: python -X utf8 hood/test/reel/set25_b3.py  (art: set25_b3_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "DEAL25 DEALB25 DEALC25 PLATE25 PLATEB25 TEAR25 BONE25 SHM25".split()

KITS = '''
    # ---- set 25, batch 3 ----------------------------------------------------------------------------------
    # 360 Deal (Submission): the contract - "SIGN HERE." - "AND HERE." - stamped: 360 DEAL. They take everything.
    b, rs = pk(DEAL25, {1: (fxart.record_contract(), ONE_TO_ONE, 4, {}), 2: (fxart.record_contract(signed=1), ONE_TO_ONE, 4, {})},
               alpha=fxart.confetti_bit())
    burst(b, rs, 0, rgb(100, 200, 90), rgb(200, 255, 190), .4, 14, .28, up=.16, gravity=.01, life=26, spin=0x0900)
    fin(DEAL25, b, rs, (0, 1, 2))
    b, rs = pk(DEALB25, {1: (fxart.record_contract(signed=2), ONE_TO_ONE, 4, {}),
                         2: (fxart.burst_sign(["360 DEAL."], fill=(200, 20, 30, 255), text=(255, 255, 255, 255)), SIGN_SCALE, 4, {"colors": 30})})
    fin(DEALB25, b, rs, (1, 2))
    b, rs = pk(DEALC25, {1: (fxart.line_bubble(["SIGN HERE."]), ONE_TO_ONE, 4, {}), 2: (fxart.line_bubble(["AND HERE."]), ONE_TO_ONE, 4, {}),
                         3: (fxart.fancy_pen(), .45, 4, {})})
    fin(DEALC25, b, rs, (1, 2, 3))

    # Eat Good (Softboiled): grandma's plate - a scoop - another scoop - then she dumps the whole pot. Healed.
    b, rs = pk(PLATE25, {1: (fxart.grandma_plate(), 1.0, 4, {}), 2: (fxart.grandma_plate(full=True), 1.0, 4, {})}, alpha=fxart.glow_dot())
    burst(b, rs, 0, rgb(120, 255, 140), rgb(230, 255, 230), .3, 10, .06, up=.12, life=24, radius=.6)
    fin(PLATE25, b, rs, (0, 1, 2))
    b, rs = pk(PLATEB25, {1: (fxart.cook_pot(), .9, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(240, 240, 245), n=5, life=20, scl=.3, up=.08)
    fin(PLATEB25, b, rs, (0, 1))

    # Waterworks (Fake Tears): sniff - sob - a full fountain of tears - the foe softens - "JK."
    b, rs = pk(TEAR25, {1: (fxart.line_bubble(["JK."]), ONE_TO_ONE, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(120, 190, 255), rgb(230, 245, 255), .3, 2, .05, up=.02, gravity=.016, life=16)
    burst(b, rs, 2, rgb(110, 180, 255), rgb(230, 245, 255), .4, 16, .2, up=.32, gravity=.02, life=26)
    burst(b, rs, 3, rgb(120, 190, 255), rgb(230, 245, 255), .32, 6, .1, up=.1, gravity=.018, life=18)
    fin(TEAR25, b, rs, (0, 1, 2, 3))

    # Bone Toss (Bonemerang): a bone out - bonk - and back (replays per hit: short)
    b, rs = pk(BONE25, {1: (fxart.dog_bone(), .7, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .45, 8, .2, life=10)
    fin(BONE25, b, rs, (0, 1))

    # Shmoney (Dragon Dance): the shmoney dance - cash up - step, step - money everywhere, powered up
    b, rs = pk(SHM25, {1: (fxart.band_stack(), .8, 4, {})}, alpha=fxart.confetti_bit())
    burst(b, rs, 0, rgb(100, 200, 90), rgb(200, 255, 190), .4, 8, .18, up=.16, gravity=.01, life=24, spin=0x0900)
    burst(b, rs, 2, rgb(100, 200, 90), rgb(200, 255, 190), .45, 20, .3, up=.24, gravity=.01, life=30, spin=0x0B00)
    burst(b, rs, 3, rgb(255, 80, 60), rgb(255, 220, 140), .35, 10, .04, up=.12, life=22, radius=.6)
    fin(SHM25, b, rs, (0, 1, 2, 3))
'''

SCRIPTS = '''
def _three_sixty_deal(side, s):
    """Submission (360 Deal): a record contract lands in front of the foe with a pen. "SIGN HERE." - they sign.
    "AND HERE." - they initial. Stamped: 360 DEAL. Their money goes straight to the attacker."""
    sx = _sx(side)
    c = _s23(side, 0, (112, 72))
    bub = _p(side, (sx * 50, 58), (-40, 30))
    pen = (c[0] + sx * 8, c[1] - 4 + _l3(.45))
    sign = _p(side, (0, 58), (0, 50))
    w = se(s["whoosh"])
    for k in range(3):
        w += emit_at(DEAL25, 1, 0, (c[0], c[1] + 30 - k * 10)) + wait(1)
    w += emit_at(DEAL25, 1, 0, c) + emit_at(DEALC25, 3, 0, pen) + se(s["pop"]) + wait(1)
    for n, (bkit, bres, after) in enumerate(((DEALC25, 1, (DEAL25, 2)), (DEALC25, 2, (DEALB25, 1)))):   # SIGN HERE... AND HERE...
        cur = (DEAL25, 1) if n == 0 else (DEAL25, 2)
        w += _hold(bkit, bres, 0, bub, 8, lambda k: emit_at(cur[0], cur[1], 0, c) + emit_at(DEALC25, 3, 0, pen))
        w += bmove(side, 264, 2, -sx * 8, -4)
        for k in range(5):                                                     # *scribble*
            w += emit_at(cur[0], cur[1], 0, c) + emit_at(DEALC25, 3, 0, (pen[0] + (3 if k % 2 else -3), pen[1] - k)) + (se(s["swipe"]) if k % 2 == 0 else []) + wait(1)
        w += bmove(side, 264, 2, sx * 8, 4) + _hold(after[0], after[1], 0, c, 3)
    w += se(s["bslam"]) + se(s["chaching"]) + flash_screen(3)               # STAMPED
    for k in range(12):
        w += emit_at(DEALB25, 2, 0, sign) + emit_at(DEALB25, 1, 0, c)
        if k == 3:
            w += emit_at(DEAL25, 0, 1, (0, 24)) + se(s["chaching"]) + func(34, 8, 0, 1, rgb(140, 140, 150), 13, 0) + shake_defender(2, 2)
        if k == 6:
            w += func(48) + shake_attacker(1, 2)
        w += wait(1)
    return w + wait(2)


def _eat_good(side, s):
    """Softboiled (Eat Good): grandma fixes a plate. Scoop. Scoop. Then she just dumps the whole pot on it - a mountain
    of food - and they eat good. Healed up."""
    sx = _sx(side)
    pl = _s23(side, 0, _p(side, (102, 96), (150, 64)))
    pot = (pl[0] + sx * 26, pl[1] + 26)
    w = se(s["pop"]) + _hold(PLATE25, 1, 0, pl, 3) + se(s["pop"]) + _hold(PLATEB25, 1, 0, pot, 3, lambda k: emit_at(PLATE25, 1, 0, pl))
    for n in range(2):                                                         # scoop... scoop...
        w += emit_at(PLATEB25, 1, 0, (pot[0] - sx * 6, pot[1] - 4)) + emit_at(PLATE25, 1, 0, pl) + wait(1)
        w += se(s["splat"]) + emit_at(PLATEB25, 0, 0, pot) + _hold(PLATEB25, 1, 0, pot, 4, lambda k: emit_at(PLATE25, 1, 0, pl))
    for k in range(4):                                                         # *dumps the whole pot*
        w += emit_at(PLATEB25, 1, 0, (pot[0] - sx * 4 * k, pot[1] + 2 * k)) + emit_at(PLATE25, 1 if k < 2 else 2, 0, pl) + wait(1)
    w += se(s["splat"]) + se(s["bslam"]) + shake_attacker(1, 2)
    for k in range(14):                                                        # *eats good*
        w += emit_at(PLATE25, 2, 0, pl)
        if k % 3 == 0:
            w += se(s["crunch"]) + bmove(side, 258, 1, 0, 4) + wait(1) + bmove(side, 258, 1, 0, -4)
        if k in (4, 10):
            w += se(s["absorb"]) + emit_at(PLATE25, 0, 0, (0, 20)) + func(34, 2, 0, 1, rgb(120, 255, 140), 11, 0)
        w += wait(1)
    return w + wait(2)


def _waterworks(side, s):
    """Fake Tears (Waterworks): sniff... a tear. Sob - more tears. Then the full fountain, tears spraying everywhere.
    The foe goes soft and leans in - then: JK."""
    sx = _sx(side)
    eyes = _p(side, (sx * 4, 34), (0, 26))
    bub = _p(side, (sx * 50, 58), (-40, 30))
    w = se(s["sscent"]) + emit_at(TEAR25, 0, 0, eyes) + wait(6)                # sniff
    w += se(s["sscent"]) + emit_at(TEAR25, 3, 0, eyes) + shake_attacker(1, 2) + wait(6)   # sob
    w += se(s["splash"]) + se(s["sscent"])                                    # WAAAAHHH
    for k in range(10):
        if k % 2 == 0:
            w += emit_at(TEAR25, 2, 0, eyes) + shake_attacker(1, 1)
        if k == 5:
            w += bmove(side, 264, 4, -sx * 10, -4) + func(34, 8, 0, 1, rgb(150, 200, 255), 8, 0)   # *aww...*
        w += wait(1)
    w += wait(2) + se(s["leer"])
    for k in range(12):                                                        # "JK."
        w += emit_at(TEAR25, 1, 0, bub)
        if k == 3:
            w += func(34, 8, 0, 1, rgb(255, 60, 40), 12, 0) + shake_defender(2, 2) + bmove(side, 264, 3, sx * 10, 4)
        w += wait(1)
    return w + wait(2)


def _bone_toss(side, s):
    """Bonemerang (Bone Toss): a bone flung at the foe - bonk - and it curves right back. (Replays per hit.)"""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    hand = (sx * 20, 30)
    w = se(s["whoosh"]) + _lob(BONE25, 1, side, hand, (dx, dy + 30), 5, 26)
    w += se(s["bonk"]) + emit_at(BONE25, 0, 1, (0, 30)) + shake_defender(2, 2)
    return w + se(s["whoosh"]) + _lob(BONE25, 1, side, (dx, dy + 30), hand, 5, -18) + wait(1)


def _shmoney(side, s):
    """Dragon Dance (Shmoney): the shmoney dance - cash held up, step left, step right, money flying - then the whole
    stack goes up in the air and they're powered all the way up."""
    sx = _sx(side)
    cash = (sx * 10, 52)
    w = []
    for n, d_ in enumerate((-10, 10, -10)):                                    # step... step... step
        w += se(s["bass"]) + bmove(side, 258, 3, d_, 4)
        for k in range(3):
            w += emit_at(SHM25, 1, 0, (cash[0] + d_ // 2, cash[1] + (k % 2) * 2)) + wait(1)
        w += emit_at(SHM25, 0, 0, cash) + se(s["chaching"] if n < 2 else s["bling"])
        w += bmove(side, 258, 3, -d_, -4) + _hold(SHM25, 1, 0, cash, 2)
    w += se(s["dcharge"]) + emit_at(SHM25, 2, 0, (0, 60)) + flash_screen(2)    # MAKE IT RAIN
    for k in range(12):
        if k % 3 == 0:
            w += emit_at(SHM25, 3, 0, (0, 10)) + func(34, 2, 0, 1, rgb(255, 90, 60) if k % 2 == 0 else rgb(90, 160, 255), 10, 0)
        w += wait(1)
    return w + func(34, 2, 0, 1, rgb(255, 90, 60), 11, 0) + wait(3)
'''

TABLE = {372: ("_three_sixty_deal", ("DEAL25", "DEALB25", "DEALC25"), "Submission"),
         373: ("_eat_good", ("PLATE25", "PLATEB25"), "Softboiled"),
         374: ("_waterworks", ("TEAR25",), "Fake Tears"),
         375: ("_bone_toss", ("BONE25",), "Bonemerang"),
         376: ("_shmoney", ("SHM25",), "Dragon Dance")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
