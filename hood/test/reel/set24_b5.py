"""Set 24 batch 5: Snap Out, Lint Trap, Bait Switch, The Wobble, Claw Machine (variants 351-355).
Run once from the repo root: python -X utf8 hood/test/reel/set24_b5.py  (art: set24_b5_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "SNAP24 SNAPB24 LINT24 LINTB24 LINTC24 SHELL24 SHELLB24 WOB24 CLAW24".split()

KITS = '''
    # ---- set 24, batch 5 ----------------------------------------------------------------------------------
    # Snap Out (SmellingSalt): "YO. WAKE UP." - nothing. A splash of water - nothing. A gym sock under the nose - UP.
    b, rs = pk(SNAP24, {1: (fxart.gym_sock(), .7, 4, {}), 2: (fxart.line_bubble(["YO.", "WAKE UP."]), ONE_TO_ONE, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(120, 190, 255), rgb(230, 245, 255), .4, 14, .22, up=.16, gravity=.018, life=20)
    fin(SNAP24, b, rs, (0, 1, 2))
    b, rs = pk(SNAPB24, {}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 60), rgb(255, 255, 220), .4, 6, .06, up=.02, life=30, radius=.5)
    burst(b, rs, 1, rgb(255, 250, 200), rgb(255, 255, 255), .6, 12, .3, life=10)
    fin(SNAPB24, b, rs, (0, 1))

    # Lint Trap (Cotton Spore): the dryer buzzes, the door pops - a puff of lint, another - then the WHOLE lint trap
    # on the foe
    b, rs = pk(LINT24, {1: (fxart.clothes_dryer(), 1.0, 4, {}), 2: (fxart.clothes_dryer(open_door=True), 1.0, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(185, 180, 185), n=6, life=24, scl=.3, up=.02)
    fin(LINT24, b, rs, (0, 1, 2))
    b, rs = pk(LINTB24, {1: (fxart.lint_screen(), .7, 4, {}), 2: (fxart.lint_blanket(), 1.4, 4, {})})
    fin(LINTB24, b, rs, (1, 2))
    b, rs = pk(LINTC24, {1: (fxart.lint_blanket(), .5, 4, {})})
    fin(LINTC24, b, rs, (1,))

    # Bait Switch (Trick): the shell game - the foe's watch under the middle cup - shuffle, shuffle, SHUFFLE - pick:
    # empty. The attacker's wearing it.
    b, rs = pk(SHELL24, {1: (fxart.cardboard_table(), 1.0, 4, {}), 2: (fxart.solo_cup(), .5, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 240, 140), rgb(255, 255, 255), .4, 6, .12, life=14)
    fin(SHELL24, b, rs, (0, 1, 2))
    b, rs = pk(SHELLB24, {1: (fxart.gold_watch(), .4, 4, {})})
    fin(SHELLB24, b, rs, (1,))

    # The Wobble (Teeter Dance): "WOBBLE BABY" - wobble, wobble (in sync) - third time the foe goes the wrong way
    b, rs = pk(WOB24, {1: (fxart.line_bubble(["WOBBLE", "BABY"]), ONE_TO_ONE, 4, {}), 2: (fxart.dance_note(), .4, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 60), rgb(255, 255, 220), .4, 7, .08, up=.02, life=26, radius=.5)
    fin(WOB24, b, rs, (0, 1, 2))

    # Claw Machine (Crush Claw): the claw comes down - misses - comes down - slips - comes down, grabs the foe, lifts
    # them all the way up... and drops them
    b, rs = pk(CLAW24, {1: (fxart.claw_grabber(), .9, 4, {}), 2: (fxart.claw_grabber(shut=True), .9, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .5, 10, .26, life=10)
    fin(CLAW24, b, rs, (0, 1, 2))
'''

SCRIPTS = '''
def _snap_out(side, s):
    """SmellingSalt (Snap Out): the foe's out of it, stars circling. "YO. WAKE UP." - nothing. A splash of water -
    nothing. Then a crusty gym sock under their nose - and they shoot straight up."""
    sx = _sx(side)
    bub = _p(side, (sx * 50, 58), (-40, 30))
    nose = _p(side, (-16, 30), (16, 30))
    dx, dy = TARGET_FROM_ATTACKER[side]
    stars = lambda k: emit_at(SNAPB24, 0, 1, (0, 42)) if k % 5 == 0 else []
    w = se(s["confuse"]) + _hold(SNAP24, 2, 0, bub, 0)
    for k in range(4):
        w += stars(k) + wait(1)
    w += _hold(SNAP24, 2, 0, bub, 10, stars) + wait(2)                         # "YO. WAKE UP." ... nothing
    w += se(s["whoosh"]) + se(s["splash"]) + emit_at(SNAP24, 0, 1, (0, 40)) + func(34, 8, 0, 1, rgb(120, 180, 255), 8, 0)
    for k in range(8):                                                         # splash... nothing
        w += stars(k + 1) + (shake_defender(1, 1) if k == 2 else []) + wait(1)
    w += se(s["whoosh"]) + _lob(SNAP24, 1, side, (sx * 20, 30), (dx + nose[0], dy + nose[1]), 4, 10)
    w += _hold(SNAP24, 1, 1, nose, 6, lambda k: (se(s["sscent"]) if k == 1 else []) + stars(k))   # *sniff*...
    w += se(s["astonish"]) + se(s["bslam"]) + flash_screen(4) + emit_at(SNAPB24, 1, 1, (0, 20))   # WIDE AWAKE
    w += bmove(side, 264, 2, 0, 30) + func(34, 8, 0, 1, rgb(140, 220, 80), 12, 0)
    w += _hold(SNAP24, 1, 1, nose, 3) + bmove(side, 264, 3, 0, -30) + shake_defender(4, 3) + func(48)
    return w + wait(3)


def _lint_trap(side, s):
    """Cotton Spore (Lint Trap): the dryer tumbles - BZZZT - the door pops open. A puff of lint at the foe. Another.
    Then the attacker yanks the lint trap and the whole fuzzy slab of lint lands on the foe."""
    sx = _sx(side)
    dr = _s23(side, 0, (104, 86))
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = se(s["rollout"])
    for k in range(6):                                                         # *tumble tumble*
        w += emit_at(LINT24, 1, 0, (dr[0] + (k % 2), dr[1])) + wait(1)
    w += se(s["alarm"]) + _hold(LINT24, 1, 0, dr, 3) + se(s["pop"]) + emit_at(LINT24, 0, 0, (dr[0] + sx * 10, dr[1]))
    w += _hold(LINT24, 2, 0, dr, 3)
    for n in range(2):                                                         # pfff... pfff...
        w += se(s["gust"]) + _lob(LINTC24, 1, side, (dr[0] + sx * 10, dr[1]), (dx, dy + 30), 5, 16, lambda k: emit_at(LINT24, 2, 0, dr))
        w += emit_at(LINT24, 0, 1, (0, 30)) + se(s["cough"]) + shake_defender(1 + n, 2) + _hold(LINT24, 2, 0, dr, 4)
    for k in range(4):                                                         # *the lint trap comes out*
        w += emit_at(LINT24, 2, 0, dr) + emit_at(LINTB24, 1, 0, (dr[0], dr[1] + 10 + k * 8)) + wait(1)
    w += _hold(LINTB24, 1, 0, (dr[0], dr[1] + 34), 3, lambda k: emit_at(LINT24, 2, 0, dr))
    w += se(s["whoosh"]) + _lob(LINTB24, 2, side, (dr[0], dr[1] + 34), (dx, dy + 18), 5, 24, lambda k: emit_at(LINT24, 2, 0, dr))
    w += se(s["flop"]) + emit_at(LINT24, 0, 1, (0, 14)) + func(34, 8, 0, 1, rgb(170, 170, 175), 13, 0)
    for k in range(10):                                                        # *smothered*
        w += emit_at(LINTB24, 2, 1, (0, 18)) + emit_at(LINT24, 2, 0, dr)
        if k % 3 == 0:
            w += bmove(side, 264, 3, 2 if k % 2 else -2, 0)
        w += wait(1)
    return w + wait(2)


def _bait_switch(side, s):
    """Trick (Bait Switch): a cardboard box table, three cups - the foe's gold watch goes under the middle one.
    Shuffle. Shuffle. SHUFFLE. The foe picks the middle cup: empty. The attacker's already wearing the watch."""
    sx = _sx(side)
    t = _s23(side, 0, (110, 96))
    cups = [(t[0] - 18, t[1] + 14), (t[0], t[1] + 14), (t[0] + 18, t[1] + 14)]
    dx, dy = TARGET_FROM_ATTACKER[side]
    table = lambda: emit_at(SHELL24, 1, 0, t)
    cupw = lambda pos: [w_ for p in pos for w_ in emit_at(SHELL24, 2, 0, p)]
    w = se(s["pop"]) + _hold(SHELL24, 1, 0, t, 2, lambda k: cupw(cups))
    w += se(s["whoosh"]) + _lob(SHELLB24, 1, side, (dx, dy + 20), (cups[1][0], cups[1][1] - 6), 5, 20, lambda k: table() + cupw(cups))
    w += _hold(SHELL24, 1, 0, t, 2, lambda k: cupw(cups))
    pos = list(cups)
    for n, (steps, pairs) in enumerate(((3, ((0, 1),)), (2, ((1, 2), (0, 1))), (1, ((0, 2), (1, 2), (0, 1), (0, 2))))):
        for a, b in pairs:                                                     # shuffle shuffle SHUFFLE
            pa, pb = pos[a], pos[b]
            w += se(s["swipe"])
            for k in range(steps):
                f = (k + 1) / steps
                lift = round(6 * (1 - abs(2 * f - 1)))
                qa = (round(pa[0] + (pb[0] - pa[0]) * f), pa[1] + lift)
                qb = (round(pb[0] + (pa[0] - pb[0]) * f), pb[1] - lift)
                w += table() + cupw([qa, qb] + [pos[i] for i in range(3) if i not in (a, b)]) + wait(1)
            pos[a], pos[b] = pb, pa
        w += _hold(SHELL24, 1, 0, t, 2 if n < 2 else 3, lambda k: cupw(pos))
    w += bmove(side, 264, 3, -sx * 10, -4) + _hold(SHELL24, 1, 0, t, 3, lambda k: cupw(pos))    # *...that one*
    lifted = [pos[0], (cups[1][0], cups[1][1] + 16), pos[2]]
    w += se(s["pop"]) + _hold(SHELL24, 1, 0, t, 7, lambda k: cupw(lifted))   # *lifts it*: EMPTY
    w += se(s["bling"]) + se(s["chaching"]) + emit_at(SHELL24, 0, 0, (sx * 10, 24)) + bmove(side, 264, 3, sx * 10, 4)
    w += _hold(SHELLB24, 1, 0, (sx * 10, 24), 10, lambda k: table() + cupw(lifted) + (func(34, 8, 0, 1, rgb(255, 60, 40), 11, 0) + shake_defender(2, 2) if k == 3 else []))
    return w


def _the_wobble(side, s):
    """Teeter Dance (The Wobble): the DJ: "WOBBLE BABY". Wobble left - both of them. Wobble right - both. Third time
    the foe wobbles the wrong way, bumps, and goes down dizzy."""
    sx = _sx(side)
    dj = _s23(side, 0, (40, 76))
    notes = lambda k: emit_at(WOB24, 2, 0, (dj[0] + 24 + (k % 3) * 8, dj[1] + 10 + (k % 4) * 6)) if k % 2 == 0 else []
    w = se(s["bass"])
    for k in range(10):                                                        # WOBBLE BABY
        w += emit_at(WOB24, 1, 0, dj) + notes(k) + (se(s["bass"]) if k % 4 == 0 else []) + wait(1)
    for n, d_ in enumerate((-10, 10)):                                         # wobble... wobble...
        w += bmove(side, 258, 3, d_, 0) + bmove(side, 264, 3, d_, 0) + se(s["bass"])
        for k in range(4):
            w += notes(k + n) + wait(1)
        w += bmove(side, 258, 3, -d_, 0) + bmove(side, 264, 3, -d_, 0) + wait(2)
    w += bmove(side, 258, 3, -10, 0) + bmove(side, 264, 3, 12, 0) + se(s["bass"]) + wait(2)   # ...wrong way
    w += se(s["bonk"]) + shake_defender(2, 2) + bmove(side, 264, 3, 0, -8) + emit_at(WOB24, 0, 1, (0, 36)) + se(s["confuse"])
    w += bmove(side, 258, 3, 10, 0)
    for k in range(8):
        w += notes(k) + wait(1)
    return w + bmove(side, 264, 3, -12, 8) + wait(2)


def _claw_machine(side, s):
    """Crush Claw (Claw Machine): *coin* - the claw comes down on the foe - closes on nothing. Again - grabs, the foe
    slips out. Third try: it grabs them, lifts them ALL the way up... and drops them."""
    top, low = 110, 34
    dx, dy = TARGET_FROM_ATTACKER[side]
    claw = lambda res, y: emit_at(CLAW24, res, 0, (dx, dy + y))
    w = se(s["chaching"])
    for n in range(3):
        for k in range(5):                                                     # *whirr* down
            w += claw(1, round(top - (top - low) * (k + 1) / 5)) + (se(s["rollout"]) if k == 0 else []) + wait(1)
        w += claw(2, low) + se(s["harden"]) + wait(1) + claw(2, low) + wait(1)
        if n == 0:                                                             # nothing
            for k in range(5):
                w += claw(2, round(low + (top - low) * (k + 1) / 5)) + wait(1)
            w += se(s["disable"]) + wait(2)
        elif n == 1:                                                           # *slips out*
            w += bmove(side, 264, 3, 0, 10) + claw(2, low + 10) + wait(1) + claw(2, low + 12) + wait(1)
            w += bmove(side, 264, 2, 0, -10) + se(s["bonk"]) + shake_defender(1, 1)
            for k in range(4):
                w += claw(2, round(low + 12 + (top - low) * (k + 1) / 4)) + wait(1)
            w += se(s["disable"]) + wait(2)
        else:                                                                  # GOT EM - all the way up...
            w += se(s["bling"]) + emit_at(CLAW24, 0, 1, (0, low - 10))
            for k in range(6):
                w += bmove(side, 264, 2, 0, 9) + claw(2, low + 9 * (k + 1)) + wait(1)
            w += claw(2, low + 54) + wait(1) + claw(2, low + 54) + wait(2)      # *...*
            w += se(s["disable"]) + claw(1, low + 54) + bmove(side, 264, 3, 0, -54) + wait(2)   # ...drop
            w += se(s["bslam"]) + se(s["kaboom"]) + flash_screen(4) + emit_at(CLAW24, 0, 1, (0, 10)) + shake_defender(4, 3)
            w += func(68, 4, 4, 1, 3, 0) + func(48)
            for k in range(4):
                w += claw(1, round(low + 54 + 20 * (k + 1))) + wait(1)
    return w + wait(3)
'''

TABLE = {351: ("_snap_out", ("SNAP24", "SNAPB24"), "SmellingSalt"),
         352: ("_lint_trap", ("LINT24", "LINTB24", "LINTC24"), "Cotton Spore"),
         353: ("_bait_switch", ("SHELL24", "SHELLB24"), "Trick"),
         354: ("_the_wobble", ("WOB24",), "Teeter Dance"),
         355: ("_claw_machine", ("CLAW24",), "Crush Claw")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
