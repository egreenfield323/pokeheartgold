"""Set 26 batch 3: Speed Bag, Trash Can, Comeback, Wish List, Deep End (variants 402-406, test-only 423 = Deep End
turn 2). Run once from the repo root: python -X utf8 hood/test/reel/set26_b3.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "SPEED26 SPEEDB26 TRASH26 TRASHB26 SCORE26 SCOREB26 CAKE26 POOL26".split()

KITS = '''
    # ---- set 26, batch 3 ----------------------------------------------------------------------------------
    # Speed Bag (Bullet Punch): bap-bap-bap - faster - FASTER - and the glove goes into the foe
    b, rs = pk(SPEED26, {1: (fxart.speed_bag(swing=-1), .8, 4, {}), 2: (fxart.speed_bag(swing=1), .8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .5, 12, .3, life=10)
    fin(SPEED26, b, rs, (0, 1, 2))
    b, rs = pk(SPEEDB26, {1: (fxart.red_glove(), .7, 4, {}), 2: (flipx(fxart.red_glove()), .7, 4, {})})
    fin(SPEEDB26, b, rs, (1, 2))

    # Trash Can (Gunk Shot): a trash bag on the foe - another - then the garbage truck backs up and dumps the load
    b, rs = pk(TRASH26, {1: (fxart.trash_bag(), .55, 4, {}), 2: (fxart.garbage_truck(), 1.4, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(120, 110, 90), rgb(180, 170, 140), .4, 10, .2, up=.12, gravity=.016, life=18)
    fin(TRASH26, b, rs, (0, 1, 2))
    b, rs = pk(TRASHB26, {1: (fxart.trash_pile(), 1.2, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(140, 200, 60), n=8, life=26, scl=.35, up=.06)
    fin(TRASHB26, b, rs, (0, 1))

    # Comeback (Reversal): the scoreboard - 0 to 99 - 1 to 99 - buzzer beater: 100 to 99
    b, rs = pk(SCORE26, {1: (fxart.scoreboard(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.scoreboard(home="1"), ONE_TO_ONE, 4, {"colors": 30})},
               alpha=fxart.confetti_bit())
    burst(b, rs, 0, rgb(255, 80, 200), rgb(80, 220, 255), .4, 20, .3, up=.22, gravity=.012, life=30, spin=0x0B00)
    fin(SCORE26, b, rs, (0, 1, 2))
    b, rs = pk(SCOREB26, {1: (fxart.scoreboard(home="100"), ONE_TO_ONE, 4, {"colors": 30})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .55, 12, .3, life=12)
    fin(SCOREB26, b, rs, (0, 1))

    # Wish List (Wish): blow out the candles - they relight - blow - they relight - one huge blow and the cake's gone.
    # Wish granted.
    b, rs = pk(CAKE26, {1: (fxart.bday_cake(), 1.0, 4, {}), 2: (fxart.bday_cake(lit=False), 1.0, 4, {})}, alpha=fxart.glow_dot())
    burst(b, rs, 0, rgb(255, 240, 140), rgb(255, 255, 230), .32, 12, .08, up=.12, life=26, radius=.6)
    fin(CAKE26, b, rs, (0, 1, 2))

    # Deep End (Dive): turn 1 a cannonball into a kiddie pool. Turn 2 they burst up out of a pool under the foe.
    b, rs = pk(POOL26, {1: (fxart.kiddie_pool(), 1.4, 4, {})}, alpha=fxart.water_jet())
    burst(b, rs, 0, rgb(120, 190, 255), rgb(230, 245, 255), .5, 18, .26, up=.36, gravity=.02, life=26)
    burst(b, rs, 3, rgb(150, 210, 255), rgb(240, 250, 255), .3, 4, .04, up=.1, life=14)
    fin(POOL26, b, rs, (0, 1, 3))
'''

SCRIPTS = '''
def _speed_bag(side, s):
    """Bullet Punch (Speed Bag): the speed bag - bap bap bap - faster - BAPBAPBAP - then the glove goes straight into
    the foe before they can blink."""
    sx = _sx(side)
    bag = _p(side, (sx * 32, 48), (-34, 34))
    w = []
    for n, gap in enumerate((2, 1, 1)):                                        # bap bap... BAPBAPBAP
        for k in range(4 + 2 * n):
            w += emit_at(SPEED26, 1 + k % 2, 0, bag) + (se(s["dslap"]) if k % 2 == 0 else []) + wait(gap)
        w += wait(1)
    w += bmove(side, 258, 2, sx * 24, 8)                                       # POP
    dx, dy = TARGET_FROM_ATTACKER[side]
    for k in range(2):
        w += emit_at(SPEEDB26, _p(side, 1, 2), 1, (-sx * (20 - k * 8), 22)) + wait(1)
    w += se(s["kaboom"]) + flash_screen(3) + emit_at(SPEED26, 0, 1, (-sx * 6, 22)) + shake_defender(3, 2) + func(48)
    return w + bmove(side, 258, 3, -sx * 24, -8) + wait(2)


def _trash_can(side, s):
    """Gunk Shot (Trash Can): a trash bag off the foe's head. Another. Then the garbage truck backs up - beep beep -
    and dumps the whole load on them. Flies, stink, everything."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    truck = _s23(side, 0, _p(side, (218, 34), (108, 96)))
    start = (truck[0] + sx * 80, truck[1])
    w = []
    for n in range(2):                                                         # bag... bag...
        w += se(s["whoosh"]) + _lob(TRASH26, 1, side, (sx * 20, 30), (dx, dy + 34), 5, 22)
        w += se(s["bonk"]) + emit_at(TRASH26, 0, 1, (0, 34)) + shake_defender(1 + n, 2) + wait(3)
    w += se(s["lockon"])
    for k in range(6):                                                         # beep... beep... (backing up)
        w += emit_at(TRASH26, 2, 0, _lerp(start, truck, (k + 1) / 6)) + (se(s["lockon"]) if k % 2 == 1 else []) + wait(1)
    w += _hold(TRASH26, 2, 0, truck, 3)
    w += se(s["splat"]) + se(s["sludge"]) + shake_defender(2, 2)              # *DUMP*
    for k in range(4):
        w += emit_at(TRASH26, 2, 0, truck) + emit_at(TRASHB26, 1, 1, (0, 30 + (3 - k) * 14)) + wait(1)
    w += se(s["bslam"]) + func(34, 8, 0, 1, rgb(150, 200, 60), 13, 0) + func(48)
    for k in range(12):
        w += emit_at(TRASHB26, 1, 1, (0, 22)) + emit_at(TRASH26, 2, 0, truck)
        if k % 4 == 0:
            w += emit_at(TRASHB26, 0, 1, (0, 40)) + se(s["toxic"] if k == 0 else s["cough"])
        w += wait(1)
    return w + wait(2)


def _comeback(side, s):
    """Reversal (Comeback): the scoreboard - HOME 0, AWAY 99. Brutal. HOME 1, AWAY 99. Then the buzzer beater: HOME 100.
    The crowd loses it, and the comeback lands on the foe."""
    sx = _sx(side)
    sb = _s23(side, 0, (108, 80))
    w = se(s["pop"]) + _hold(SCORE26, 1, 0, sb, 8, lambda k: (se(s["faint"]) + func(34, 2, 0, 1, rgb(120, 120, 140), 9, 0)) if k == 2 else [])
    w += se(s["bling"]) + _hold(SCORE26, 2, 0, sb, 8)                         # 1 - 99
    w += se(s["alarm"]) + flash_screen(4) + emit_at(SCORE26, 0, 0, (sb[0], sb[1] + 20)) + se(s["chaching"])   # BUZZER BEATER
    w += _hold(SCOREB26, 1, 0, sb, 8, lambda k: func(34, 2, 0, 1, rgb(255, 220, 80), 12, 0) if k == 1 else [])
    w += bmove(side, 258, 2, sx * 24, 8) + se(s["kaboom"]) + flash_screen(3) + emit_at(SCOREB26, 0, 1, (0, 22))
    w += shake_defender(4, 3) + func(48) + bmove(side, 258, 4, -sx * 24, -8)
    return w + _hold(SCOREB26, 1, 0, sb, 4)


def _wish_list(side, s):
    """Wish (Wish List): a birthday cake. They blow out the candles - they relight. Blow - they relight (trick
    candles). One giant blow and the whole cake goes flying. Wish granted."""
    sx = _sx(side)
    ck = _s23(side, 0, (106, 88))
    w = se(s["pop"]) + _hold(CAKE26, 1, 0, ck, 4)
    for n in range(2):                                                         # blow... *relights*
        w += se(s["gust"]) + bmove(side, 258, 2, sx * 4, 2) + _hold(CAKE26, 2, 0, ck, 5) + bmove(side, 258, 2, -sx * 4, -2)
        w += se(s["ember"]) + _hold(CAKE26, 1, 0, ck, 4 + n, lambda k: shake_attacker(1, 1) if k == 1 and n == 1 else [])
    w += _hold(CAKE26, 1, 0, ck, 2) + se(s["gust"]) + se(s["whoosh"]) + bmove(side, 258, 2, sx * 8, 4)   # FWOOOO
    w += _lob(CAKE26, 2, side, ck, (ck[0] + sx * 140, ck[1] + 60), 6, 30) + bmove(side, 258, 2, -sx * 8, -4)
    w += se(s["bling"]) + se(s["absorb"]) + emit_at(CAKE26, 0, 0, (0, 20)) + func(34, 2, 0, 1, rgb(255, 240, 140), 11, 0)
    return w + wait(8)


def _deep_end(side, s):
    """Dive (Deep End), two turns. Turn 1: a kiddie pool - they hop up and CANNONBALL in - splash - gone. Turn 2: a
    pool under the foe, bubbles... then they burst up out of it and launch the foe."""
    py = _p(side, 18, -4)
    one = se(s["pop"]) + _hold(POOL26, 1, 0, (0, py), 3)
    one += bmove(side, 258, 3, 0, 24) + _hold(POOL26, 1, 0, (0, py - 24), 3)       # *hops up*
    one += se(s["whoosh"]) + bmove(side, 258, 2, 0, -24) + _hold(POOL26, 1, 0, (0, py), 1)
    one += se(s["splash"]) + se(s["surf"]) + emit_at(POOL26, 0, 0, (0, py + 12)) + func(40, 2, 1)   # CANNONBALL
    one += _hold(POOL26, 1, 0, (0, py), 8)
    fy = _p(side, 6, -16)
    two = se(s["pop"]) + _hold(POOL26, 1, 1, (0, fy), 3)
    for k in range(6):                                                         # *bubbles*
        two += emit_at(POOL26, 1, 1, (0, fy)) + (emit_at(POOL26, 3, 1, (((k * 7) % 20) - 10, fy + 6)) if k % 2 == 0 else []) + wait(1)
    two += se(s["splash"]) + se(s["wfall"]) + emit_at(POOL26, 0, 1, (0, fy + 10)) + func(40, 2, 0) + flash_screen(3)   # SPLOOSH
    two += bmove(side, 264, 3, 0, 22) + shake_defender(3, 2) + _hold(POOL26, 1, 1, (0, fy - 22), 3)
    two += bmove(side, 264, 4, 0, -22) + func(48)
    return one, two + _hold(POOL26, 1, 1, (0, fy), 3)


def _deep_end_turn2_first(side, s):
    """Test only: Deep End's second turn on its own (vanishes the attacker first, like the real turn 1)."""
    return func(40, 2, 1) + _deep_end(side, s)[1]
'''

TABLE = {402: ("_speed_bag", ("SPEED26", "SPEEDB26"), "Bullet Punch"),
         403: ("_trash_can", ("TRASH26", "TRASHB26"), "Gunk Shot"),
         404: ("_comeback", ("SCORE26", "SCOREB26"), "Reversal"),
         405: ("_wish_list", ("CAKE26",), "Wish"),
         406: ("_deep_end", ("POOL26",), "Dive")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
    p = set23_lib.ROOT / "hood/gunfx.py"
    s = p.read_text(encoding="utf-8")
    for a, b in (("            406: _deep_end,\n", "            406: _deep_end,\n            423: _deep_end_turn2_first,\n"),
                 ("        406: (POOL26,),\n", "        406: (POOL26,),\n        423: (POOL26,),\n")):
        assert s.count(a) == 1, a
        s = s.replace(a, b)
    p.write_text(s, encoding="utf-8", newline="")
