"""Set 24 batch 6: Hat Trick, Reverse Card, Rise n Grind, Sinkhole (variants 356-359).
Run once from the repo root: python -X utf8 hood/test/reel/set24_b6.py  (art: set24_b6_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "HATS24 HATSB24 CARD24 CARDB24 RISE24 RISEB24 RISEC24 SINK24 SINKB24".split()

KITS = '''
    # ---- set 24, batch 6 ----------------------------------------------------------------------------------
    # Hat Trick (Tri Attack): fitted caps flicked onto the foe's head and stacking: the fire one, the ice one, the zap
    # one - then the whole stack topples
    b, rs = pk(HATS24, {1: (fxart.fitted_cap(), .5, 4, {}), 2: (fxart.fitted_cap(color=(40, 110, 230, 255), emblem="ice"), .5, 4, {})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 130, 30), rgb(255, 240, 160), .4, 8, .16, up=.1, life=14)
    burst(b, rs, 3, rgb(150, 210, 255), rgb(255, 255, 255), .4, 8, .16, up=.06, life=14)
    fin(HATS24, b, rs, (0, 1, 2, 3))
    b, rs = pk(HATSB24, {1: (fxart.fitted_cap(color=(250, 200, 30, 255), emblem="zap"), .5, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 80), rgb(255, 255, 255), .45, 10, .22, life=12)
    fin(HATSB24, b, rs, (0, 1))

    # Reverse Card (Trump Card): +2 - +4 - the foe slaps a +4 back - REVERSE. Cards everywhere.
    b, rs = pk(CARD24, {1: (fxart.game_card(), ONE_TO_ONE, 4, {}), 2: (fxart.game_card(label="+4", color=(40, 110, 230, 255)), ONE_TO_ONE, 4, {})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 220), rgb(255, 255, 255), .4, 6, .16, life=10)
    fin(CARD24, b, rs, (0, 1, 2))
    b, rs = pk(CARDB24, {1: (fxart.game_card(label="rev", color=(60, 180, 80, 255)), ONE_TO_ONE, 4, {})}, alpha=fxart.confetti_bit())
    burst(b, rs, 0, rgb(230, 50, 50), rgb(60, 120, 230), .5, 20, .32, up=.18, gravity=.012, life=30, spin=0x0B00)
    burst(b, rs, 2, rgb(60, 190, 80), rgb(250, 210, 40), .5, 16, .28, up=.14, gravity=.012, life=28, spin=0x0900)
    fin(CARDB24, b, rs, (0, 1, 2))

    # Rise n Grind (Morning Sun): 6:00 BEEP - snooze. 6:09 BEEP - snooze. 6:18 - fine. Sun up, coffee, healed.
    b, rs = pk(RISE24, {1: (fxart.bedside_clock(ringing=True), ONE_TO_ONE, 4, {}), 2: (fxart.bedside_clock(t="6:09", ringing=True), ONE_TO_ONE, 4, {})},
               alpha=fxart.glow_dot())
    burst(b, rs, 0, rgb(255, 230, 120), rgb(255, 255, 230), .3, 10, .06, up=.12, life=24, radius=.6)
    fin(RISE24, b, rs, (0, 1, 2))
    b, rs = pk(RISEB24, {1: (fxart.bedside_clock(t="6:18", ringing=True), ONE_TO_ONE, 4, {}), 2: (fxart.coffee_mug(), .5, 4, {})})
    fin(RISEB24, b, rs, (1, 2))
    b, rs = pk(RISEC24, {1: (fxart.sunrise(), 2.0, 4, {})})
    fin(RISEC24, b, rs, (1,))

    # Sinkhole (Fissure): a crack under the foe - it splits wider - the street opens up and swallows them
    b, rs = pk(SINK24, {1: (fxart.road_crack(), 1.2, 4, {}), 2: (fxart.road_crack(big=True), 1.2, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(170, 160, 150), n=8, life=24, scl=.35, up=.05)
    fin(SINK24, b, rs, (0, 1, 2))
    b, rs = pk(SINKB24, {1: (fxart.sinkhole(), 1.4, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(110, 110, 118), rgb(170, 170, 178), .45, 16, .26, up=.2, gravity=.02, life=22, spin=0x0800)
    fin(SINKB24, b, rs, (0, 1))
'''

SCRIPTS = '''
def _hat_trick(side, s):
    """Tri Attack (Hat Trick): a fitted cap flicked onto the foe's head - the fire one (sizzle). The ice one stacks on
    top (frost). The zap one on top of that (ZZT). A tower of three hats wobbles... and it all comes down."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    hats = [(HATS24, 1, (0, 40)), (HATS24, 2, (0, 50)), (HATSB24, 1, (0, 60))]
    fx = [(HATS24, 0, "ember", rgb(255, 120, 40)), (HATS24, 3, "ishard", rgb(150, 210, 255)), (HATSB24, 0, "spark", rgb(255, 250, 80))]
    on = []
    dress = lambda dxx=0: [w_ for i in on for w_ in emit_at(hats[i][0], hats[i][1], 1, (hats[i][2][0] + dxx * (i + 1), hats[i][2][1]))]
    w = []
    for n in range(3):                                                         # flick... flick... flick
        kit, res, at = hats[n]
        w += se(s["whoosh"]) + _lob(kit, res, side, (sx * 22, 30), (dx + at[0], dy + at[1]), 5, 20, lambda k: dress())
        on.append(n)
        fk, fr, snd, col = fx[n]
        w += se(s[snd]) + emit_at(fk, fr, 1, at) + func(34, 8, 0, 1, col, 9, 0) + shake_defender(1, 1)
        w += _hold(kit, res, 1, at, 4 + n, lambda k: dress())
    for k in range(6):                                                         # *wobble*
        w += dress((-1, 1, -2, 2, -3, 3)[k]) + wait(1)
    w += se(s["bslam"]) + flash_screen(3) + shake_defender(3, 3) + func(48)    # TIMBER
    paths = [_arc((dx, dy + 40 + 10 * i), (dx + (-50, 10, 60)[i], dy - 30 + 10 * i), 5, 20 + 6 * i) for i in range(3)]
    on.clear()
    for k in range(1, 5):
        for i in range(3):
            w += emit_at(hats[i][0], hats[i][1], 0, paths[i][k])
        w += wait(1)
    return w + wait(3)


def _reverse_card(side, s):
    """Trump Card (Reverse Card): a card game between them. SLAP: +2. SLAP: +4. The foe smirks and slaps a +4 right
    back... and the attacker drops the REVERSE card. Cards everywhere."""
    sx = _sx(side)
    pile = _s23(side, 0, (124, 72))
    me = _p(side, (sx * 24, 30), (-24, 20))
    dx, dy = TARGET_FROM_ATTACKER[side]
    them = (dx - sx * 10, dy + 24)
    top = []
    show = lambda: emit_at(top[-1][0], top[-1][1], 0, pile) if top else []
    w = []
    for n, (kit, res, frm) in enumerate(((CARD24, 1, me), (CARD24, 2, me), (CARD24, 2, them))):   # SLAP. SLAP. *slap*
        w += se(s["whoosh"]) + _lob(kit, res, side, frm, pile, 4, 12, lambda k: show())
        top.append((kit, res))
        w += se(s["dslap"]) + emit_at(CARD24, 0, 0, pile) + show() + wait(1)
        if n == 0:
            w += shake_defender(1, 1)
        if n == 1:
            w += func(34, 8, 0, 1, rgb(255, 60, 40), 9, 0) + shake_defender(2, 2)
        if n == 2:
            w += bmove(side, 264, 2, 0, 6) + se(s["swagger"])                  # *smirks*
        w += _hold(top[-1][0], top[-1][1], 0, pile, 4 + n, lambda k: [])
        if n == 2:
            w += bmove(side, 264, 2, 0, -6)
    w += _hold(top[-1][0], top[-1][1], 0, pile, 2) + se(s["whoosh"])          # ...REVERSE
    w += _lob(CARDB24, 1, side, me, pile, 4, 16, lambda k: show())
    w += se(s["bslam"]) + se(s["chaching"]) + flash_screen(4) + emit_at(CARDB24, 1, 0, pile) + wait(1)
    w += emit_at(CARDB24, 0, 1, (0, 30)) + emit_at(CARDB24, 2, 0, pile) + func(68, 3, 3, 1, 4, 0)
    for k in range(10):
        w += emit_at(CARDB24, 1, 0, pile)
        if k == 2:
            w += shake_defender(4, 3) + func(48) + se(s["kaboom"])
        w += wait(1)
    return w + wait(2)


def _rise_n_grind(side, s):
    """Morning Sun (Rise n Grind): pitch dark. 6:00 BEEP BEEP - snooze. 6:09 BEEP BEEP - snooze. 6:18 BEEP BEEP -
    fine. The sun comes up, a hot coffee, and they're healed up and on the grind."""
    sx = _sx(side)
    c = _s23(side, 0, (104, 86))
    sun = _s23(side, 0, _p(side, (40, 70), (220, 56)))
    mug = _p(side, (sx * 26, 30), (-26, 18))
    w = func(33, 0, 1, 0, 12, rgb(10, 15, 50)) + wait(2)
    for n, (kit, res) in enumerate(((RISE24, 1), (RISE24, 2), (RISEB24, 1))):   # BEEP BEEP... *snooze*
        w += se(s["alarm"])
        for k in range(6):
            w += emit_at(kit, res, 0, (c[0] + (1 if k % 2 else -1), c[1])) + (se(s["alarm"]) if k == 3 else []) + wait(1)
        if n < 2:
            w += bmove(side, 258, 2, sx * 6, 4) + se(s["disable"]) + emit_at(kit, res, 0, c) + wait(1)
            w += bmove(side, 258, 2, -sx * 6, -4) + _hold(kit, res, 0, c, 4)
    w += bmove(side, 258, 3, 0, 8) + func(33, 0, 1, 12, 0, rgb(10, 15, 50))   # *...fine.*
    for k in range(6):                                                         # the sun comes up
        w += emit_at(RISEC24, 1, 0, (sun[0], sun[1] - 30 + k * 6)) + emit_at(RISEB24, 1, 0, c) + wait(1)
    w += se(s["sunny"]) + bmove(side, 258, 3, 0, -8) + flash_screen(2)
    for k in range(12):                                                        # coffee. healed.
        w += emit_at(RISEC24, 1, 0, sun) + emit_at(RISEB24, 2, 0, mug)
        if k in (1, 6):
            w += se(s["absorb"]) + emit_at(RISE24, 0, 0, (0, 20)) + func(34, 2, 0, 1, rgb(255, 220, 100), 11, 0)
        w += wait(1)
    return w + wait(2)


def _sinkhole(side, s):
    """Fissure (Sinkhole): the street cracks under the foe - they step back - it splits wider - then the ground just
    opens and swallows them. A beat. They climb back out wrecked."""
    back = _p(side, 16, 30)
    feet = (0, -22)
    w = se(s["crack"]) + bmove(side, 264, 3, 0, back)
    w += _hold(SINK24, 1, 1, feet, 5, lambda k: shake_defender(1, 1) if k == 1 else [])
    w += se(s["crack"]) + se(s["sand"]) + emit_at(SINK24, 0, 1, (feet[0], feet[1] + 4))
    w += _hold(SINK24, 2, 1, feet, 7, lambda k: (bmove(side, 264, 1, 3 if k % 2 else -3, 0) if k < 4 else []))
    w += se(s["kaboom"]) + se(s["bslam"]) + flash_screen(4) + func(68, 5, 5, 1, 6, 0) + emit_at(SINKB24, 0, 1, feet)   # *CRASH*
    hole = _s23(side, 0, _p(side, (185, 81), (64, 104)))                       # (fixed on screen: the foe drops through it)
    w += _hold(SINKB24, 1, 0, hole, 2)
    w += bmove(side, 264, 4, 0, -60)
    for k in range(10):                                                        # *gone*
        w += emit_at(SINKB24, 1, 0, hole)
        if k % 4 == 0:
            w += emit_at(SINK24, 0, 0, (hole[0], hole[1] + 4))
        w += wait(1)
    w += se(s["bslam"]) + bmove(side, 264, 5, 0, 60) + func(34, 8, 0, 1, rgb(110, 90, 80), 13, 0)
    w += _hold(SINKB24, 1, 0, hole, 3) + shake_defender(3, 2) + func(48)
    return w + bmove(side, 264, 3, 0, -back) + wait(3)
'''

TABLE = {356: ("_hat_trick", ("HATS24", "HATSB24"), "Tri Attack"),
         357: ("_reverse_card", ("CARD24", "CARDB24"), "Trump Card"),
         358: ("_rise_n_grind", ("RISE24", "RISEB24", "RISEC24"), "Morning Sun"),
         359: ("_sinkhole", ("SINK24", "SINKB24"), "Fissure")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
