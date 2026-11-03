"""Set 26 batch 4: Pillow Fight, Bad Sushi, Blindside, Uppercut, Sandbag (variants 407-411).
Run once from the repo root: python -X utf8 hood/test/reel/set26_b4.py  (art: set26_b4_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "PILLOW26 SUSHI26 SNEAK26 UPPER26 SAND26".split()

KITS = '''
    # ---- set 26, batch 4 ----------------------------------------------------------------------------------
    # Pillow Fight (FeatherDance): whack - whack - the pillow bursts, feathers everywhere
    b, rs = pk(PILLOW26, {1: (fxart.fluffy_pillow(), .8, 4, {})}, alpha=fxart.feather())
    burst(b, rs, 0, rgb(250, 250, 255), rgb(255, 255, 255), .35, 5, .12, up=.06, gravity=.004, life=26, spin=0x0600)
    burst(b, rs, 2, rgb(250, 250, 255), rgb(255, 255, 255), .45, 24, .3, up=.14, gravity=.004, life=44, radius=.6, spin=0x0700)
    fin(PILLOW26, b, rs, (0, 1, 2))

    # Bad Sushi (Poison Fang): gas station sushi - one piece - another - the whole tray. Badly poisoned.
    b, rs = pk(SUSHI26, {1: (fxart.sushi_tray(), 1.0, 4, {}), 2: (fxart.sushi_roll(), .45, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(170, 70, 200), n=6, life=24, scl=.32, up=.07)
    fin(SUSHI26, b, rs, (0, 1, 2))

    # Blindside (Shadow Punch): a cardboard box sneaks up - the foe turns, it freezes - again - "!" - POW
    b, rs = pk(SNEAK26, {1: (fxart.sneak_box(), .9, 4, {}), 2: (fxart.sneak_box(alert=True), .9, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .55, 12, .3, life=12)
    fin(SNEAK26, b, rs, (0, 1, 2))

    # Uppercut (Sky Uppercut): pop - POP - then all the way to the moon. *ding*
    b, rs = pk(UPPER26, {1: (fxart.upper_glove(), .8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .5, 10, .26, life=10)
    burst(b, rs, 2, rgb(255, 255, 220), rgb(255, 255, 255), .6, 4, .04, life=16, radius=.1)
    fin(UPPER26, b, rs, (0, 1, 2))

    # Sandbag (Sand Tomb): sandbags stacked round the foe (replays as a trap: short)
    b, rs = pk(SAND26, {1: (fxart.sandbag(), .5, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(210, 185, 130), n=5, life=18, scl=.3, up=.04)
    fin(SAND26, b, rs, (0, 1))
'''

SCRIPTS = '''
def _pillow_fight(side, s):
    """FeatherDance (Pillow Fight): a pillow upside the foe's head - whack - whack - then one whack too hard and it
    bursts. Feathers everywhere."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = []
    for n in range(3):                                                         # whack... whack... WHACK
        w += se(s["whoosh"]) + _lob(PILLOW26, 1, side, (sx * 20, 34), (dx - sx * 6, dy + 36), 4, 14)
        w += se(s["flop"] if n < 2 else s["bslam"]) + shake_defender(1 + n, 2)
        if n < 2:
            w += emit_at(PILLOW26, 0, 1, (0, 36)) + _lob(PILLOW26, 1, side, (dx - sx * 6, dy + 36), (sx * 20, 34), 4, 10)
    w += emit_at(PILLOW26, 2, 1, (0, 36)) + flash_screen(2) + func(34, 8, 0, 1, rgb(200, 200, 230), 11, 0)   # *POOF*
    return w + wait(14)


def _bad_sushi(side, s):
    """Poison Fang (Bad Sushi): a tray of gas station sushi. One piece into the foe - gulp. Another - they go green.
    Then the whole tray - badly poisoned."""
    sx = _sx(side)
    tray = _p(side, (-79, -5), (46, 40))
    dx, dy = TARGET_FROM_ATTACKER[side]
    mouth = (dx, dy + 26)
    tray_a = (dx + tray[0], dy + tray[1])
    t = lambda: emit_at(SUSHI26, 1, 1, tray)
    w = se(s["pop"]) + _hold(SUSHI26, 1, 1, tray, 4)
    for n in range(2):                                                         # gulp... gulp...
        w += se(s["whoosh"]) + _lob(SUSHI26, 2, side, (tray_a[0], tray_a[1] + 10), mouth, 4, 14, lambda k: t())
        w += se(s["crunch"]) + t() + shake_defender(1, 1) + wait(1)
        if n == 1:
            w += func(34, 8, 0, 1, rgb(150, 210, 80), 9, 0) + se(s["cough"])
        w += _hold(SUSHI26, 1, 1, tray, 4)
    w += se(s["whoosh"]) + _lob(SUSHI26, 1, side, tray_a, mouth, 4, 18)        # THE WHOLE TRAY
    w += se(s["crunch"]) + se(s["toxic"]) + func(34, 8, 0, 1, rgb(170, 70, 200), 14, 0) + shake_defender(3, 3)
    for k in range(12):
        if k % 3 == 0:
            w += emit_at(SUSHI26, 0, 1, (0, 30))
        if k == 6:
            w += se(s["toxic2"])
        w += wait(1)
    return w + wait(2)


def _blindside(side, s):
    """Shadow Punch (Blindside): they duck under a cardboard box and creep up on the foe. The foe turns - the box
    freezes. Creep. The foe turns - frozen. "!" - then POW out of nowhere."""
    sx = _sx(side)
    path = _p(side, ((92, 104), (118, 92), (144, 82)), ((160, 86), (132, 98), (104, 110)))
    pts = [_s23(side, 0, p) for p in path]
    box = lambda i, r=1: emit_at(SNEAK26, r, 0, pts[i])
    w = se(s["whoosh"]) + func(40, 2, 1) + _hold(SNEAK26, 1, 0, pts[0], 3)
    for n in range(2):                                                         # creep... freeze
        for k in range(3):
            w += emit_at(SNEAK26, 1, 0, _lerp(pts[n], pts[n + 1], (k + 1) / 3)) + (se(s["swipe"]) if k == 0 else []) + wait(1)
        w += bmove(side, 264, 2, -sx * 8, 0) + _hold(SNEAK26, 1, 0, pts[n + 1], 4) + bmove(side, 264, 2, sx * 8, 0)
        w += _hold(SNEAK26, 1, 0, pts[n + 1], 2)
    w += se(s["alarm"]) + _hold(SNEAK26, 2, 0, pts[2], 4)                    # "!"
    w += func(40, 2, 0) + bmove(side, 258, 2, sx * 30, 12) + se(s["kaboom"]) + se(s["bslam"]) + flash_screen(4)   # POW
    w += emit_at(SNEAK26, 0, 1, (0, 22)) + shake_defender(4, 3) + func(48)
    w += _lob(SNEAK26, 1, side, pts[2], (pts[2][0] + sx * 40, pts[2][1] + 60), 4, 20)
    return w + bmove(side, 258, 4, -sx * 30, -12) + wait(2)


def _uppercut(side, s):
    """Sky Uppercut (Uppercut): an uppercut - the foe pops up. Another - higher. Then the big one: they go all the way
    up and out of sight... *ding* ... and come crashing back down."""
    w = []
    for n, h in enumerate((10, 22)):                                           # pop... POP...
        for k in range(3):
            w += emit_at(UPPER26, 1, 1, (0, -20 + k * 14)) + wait(1)
        w += se(s["bonk"]) + emit_at(UPPER26, 0, 1, (0, 20)) + bmove(side, 264, 2, 0, h) + wait(2)
        w += bmove(side, 264, 3, 0, -h) + wait(2)
    for k in range(3):                                                         # TO THE MOON
        w += emit_at(UPPER26, 1, 1, (0, -20 + k * 16)) + wait(1)
    w += se(s["kaboom"]) + flash_screen(4) + emit_at(UPPER26, 0, 1, (0, 22)) + bmove(side, 264, 4, 0, 120)
    w += se(s["whoosh"]) + wait(6) + se(s["bling"]) + emit_at(UPPER26, 2, 1, (0, 150)) + wait(8)   # *ding*
    w += se(s["whoosh"]) + bmove(side, 264, 4, 0, -120) + wait(1)
    w += se(s["bslam"]) + shake_defender(4, 3) + func(68, 3, 3, 1, 3, 0) + func(48)
    return w + wait(3)


def _sandbag(side, s):
    """Sand Tomb (Sandbag): sandbags thud down round the foe - left - right - one more on top. Walled in. (Replays
    as a trap: short.)"""
    spots = [(-22, -8), (22, -8), (-12, 6), (12, 6), (0, 40)]
    on = []
    dress = lambda: [w_ for i in on for w_ in emit_at(SAND26, 1, 1, spots[i])]
    w = []
    for n, sp in enumerate(spots):
        for k in range(2):
            w += emit_at(SAND26, 1, 1, (sp[0], sp[1] + 30 - k * 15)) + dress() + wait(1)
        on.append(n)
        w += se(s["bslam"] if n == 4 else s["sand"]) + emit_at(SAND26, 0, 1, (sp[0], sp[1] + 4)) + dress() + wait(1)
    w += shake_defender(2, 2) + func(34, 8, 0, 1, rgb(210, 185, 130), 9, 0)
    for k in range(8):
        w += dress() + wait(1)
    return w
'''

TABLE = {407: ("_pillow_fight", ("PILLOW26",), "FeatherDance"),
         408: ("_bad_sushi", ("SUSHI26",), "Poison Fang"),
         409: ("_blindside", ("SNEAK26",), "Shadow Punch"),
         410: ("_uppercut", ("UPPER26",), "Sky Uppercut"),
         411: ("_sandbag", ("SAND26",), "Sand Tomb")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
