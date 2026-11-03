"""Set 26 batch 6: Finesse, Ext. Cord, Two-by-Four, Kick Back, Slow Jam (variants 417-421).
Run once from the repo root: python -X utf8 hood/test/reel/set26_b6.py  (art: set26_b6_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "FIN26 FINB26 CORD26 CORDB26 PLANK26 PLANKB26 RECL26 RECLB26 RECLC26 JAM26 JAMB26".split()

KITS = '''
    # ---- set 26, batch 6 ----------------------------------------------------------------------------------
    # Finesse (Covet): "LEMME SEE THAT" - they snatch the foe's fresh snapback, try it on, and walk off
    b, rs = pk(FIN26, {1: (fxart.lemme_bubble(), ONE_TO_ONE, 4, {}), 2: (fxart.fresh_snapback(), .55, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 220, 60), rgb(255, 255, 220), .4, 8, .2, life=12)
    fin(FIN26, b, rs, (0, 1, 2))
    b, rs = pk(FINB26, {1: (flipx(fxart.fresh_snapback()), .55, 4, {})})
    fin(FINB26, b, rs, (1,))

    # Ext. Cord (Power Whip): the orange extension cord - folded in half - swing, swing, WHAP WHAP WHAP
    b, rs = pk(CORD26, {1: (fxart.ext_cord(swung=True), 1.0, 4, {}), 2: (flipx(fxart.ext_cord(swung=True)), 1.0, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .5, 10, .28, life=10)
    fin(CORD26, b, rs, (0, 1, 2))
    b, rs = pk(CORDB26, {1: (fxart.ext_cord(), .7, 4, {})})
    fin(CORDB26, b, rs, (1,))

    # Two-by-Four (Wood Hammer): measure twice... swing once. Splinters. They feel it too.
    b, rs = pk(PLANK26, {1: (fxart.tape_measure(), .8, 4, {}), 2: (flipx(fxart.tape_measure()), .8, 4, {})}, alpha=fxart.wood_chip())
    burst(b, rs, 0, rgb(220, 170, 100), rgb(250, 220, 160), .4, 16, .3, up=.14, gravity=.014, life=22, spin=0x0800)
    fin(PLANK26, b, rs, (0, 1, 2))
    b, rs = pk(PLANKB26, {1: (fxart.two_by_four(), 1.0, 4, {}), 2: (flipx(fxart.two_by_four()), 1.0, 4, {})})
    fin(PLANKB26, b, rs, (1, 2))

    # Kick Back (Slack Off): the recliner - lever - footrest pops - laid all the way back. Ahhh.
    b, rs = pk(RECL26, {1: (fxart.recliner(), 1.5, 4, {}), 2: (fxart.recliner(stage=1), 1.5, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(120, 240, 140), rgb(230, 255, 230), .35, 10, .08, up=.12, life=24, radius=.6)
    fin(RECL26, b, rs, (0, 1, 2))
    b, rs = pk(RECLB26, {1: (fxart.recliner(stage=2), 1.5, 4, {}), 2: (flipx(fxart.recliner()), 1.5, 4, {})})
    fin(RECLB26, b, rs, (1, 2))
    b, rs = pk(RECLC26, {1: (flipx(fxart.recliner(stage=1)), 1.5, 4, {}), 2: (flipx(fxart.recliner(stage=2)), 1.5, 4, {})})
    fin(RECLC26, b, rs, (1, 2))

    # Slow Jam (GrassWhistle): candle - candle - candle - the slow jam comes on - the foe sways - out cold
    b, rs = pk(JAM26, {1: (fxart.jar_candle(), .45, 4, {}), 2: (fxart.jar_candle(lit=False), .45, 4, {})}, alpha=fxart.love_note())
    burst(b, rs, 0, rgb(255, 120, 190), rgb(255, 220, 240), .3, 2, .05, up=.06, life=30, radius=.2)
    fin(JAM26, b, rs, (0, 1, 2))
    b, rs = pk(JAMB26, {}, alpha=fxart.snore_z())
    burst(b, rs, 0, rgb(200, 210, 255), rgb(255, 255, 255), .3, 1, .03, up=.07, life=30, radius=.1)
    fin(JAMB26, b, rs, (0,))
'''

SCRIPTS = '''
def _finesse(side, s):
    """Covet (Finesse): "LEMME SEE THAT" - the foe's fresh snapback (sticker still on). They snatch it, try it on, check
    the fit... and just walk off with it."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    bub = _s23(side, 0, _p(side, (100, 80), (126, 34)))
    foe_hat, my_hat = _p(side, ((FINB26, 1), (FIN26, 2)), ((FIN26, 2), (FINB26, 1)))
    on_foe = lambda: emit_at(foe_hat[0], foe_hat[1], 1, (0, 32))
    w = se(s["pop"]) + _hold(FIN26, 1, 0, bub, 12, lambda k: on_foe() + (se(s["leer"]) if k == 6 else []))   # LEMME SEE THAT
    w += _hold(foe_hat[0], foe_hat[1], 1, (0, 32), 3)
    w += se(s["swipe"]) + shake_defender(1, 2) + _lob(my_hat[0], my_hat[1], side, (dx, dy + 32), (0, 44), 6, 18)   # *snatch*
    for n in range(2):                                                         # fit check
        w += bmove(side, 258, 2, 0, 4) + _hold(my_hat[0], my_hat[1], 0, (0, 44), 2) + bmove(side, 258, 2, 0, -4)
        w += _hold(my_hat[0], my_hat[1], 0, (0, 44), 2)
    w += se(s["bling"]) + emit_at(FIN26, 0, 0, (0, 48)) + _hold(my_hat[0], my_hat[1], 0, (0, 44), 4)
    w += se(s["whoosh"]) + bmove(side, 258, 8, -sx * 72, 0)                    # ...and walks off (emits stay base-relative)
    for k in range(4):
        w += emit_at(my_hat[0], my_hat[1], 0, (-sx * 18 * (k + 1), 44)) + wait(1)
    w += shake_defender(2, 3) + wait(6) + bmove(side, 258, 6, sx * 72, 0)
    for k in range(3):
        w += emit_at(my_hat[0], my_hat[1], 0, (-sx * 24 * (2 - k), 44)) + wait(1)
    return w + _hold(my_hat[0], my_hat[1], 0, (0, 44), 3)


def _ext_cord(side, s):
    """Power Whip (Ext. Cord): somebody went and got the extension cord. It sits there coiled - the foe sees it and
    shakes. Folded in half. Swing - the foe flinches. Swing - flinch. Then WHAP WHAP WHAP."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    coil = (sx * 30, 18)
    res = _p(side, 1, 2)
    at = (dx - sx * 34, dy + 18)
    w = se(s["pop"]) + _hold(CORDB26, 1, 0, coil, 6, lambda k: shake_defender(1, 2) if k == 3 else [])
    for n in range(2):                                                         # swing... swing...
        w += se(s["whoosh"]) + emit_at(CORD26, res, 0, (at[0] - sx * 20, at[1] + 14)) + wait(1)
        w += emit_at(CORD26, res, 0, at) + bmove(side, 264, 2, sx * 10, 0) + wait(1)
        w += emit_at(CORD26, res, 0, (at[0] - sx * 20, at[1] + 14)) + wait(2) + bmove(side, 264, 2, -sx * 10, 0) + wait(2)
    for k in range(3):                                                         # WHAP WHAP WHAP
        w += emit_at(CORD26, res, 0, (at[0] - sx * 20, at[1] + 14)) + wait(1)
        w += se(s["vwhip"]) + se(s["dslap"] if k < 2 else s["bslam"]) + emit_at(CORD26, res, 0, (at[0] + sx * 6, at[1] - 6))
        w += emit_at(CORD26, 0, 1, (0, 20)) + shake_defender(1 + k, 2) + wait(1)
    w += flash_screen(3) + func(34, 8, 0, 1, rgb(255, 90, 90), 9, 0) + func(48)
    return w + wait(6)


def _two_by_four(side, s):
    """Wood Hammer (Two-by-Four): measure twice... (the tape measure goes across the foe, then again) ...cut once: a 2x4
    upside their head. Splinters everywhere - and the attacker's hands sting too."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    tres, bres = _p(side, 1, 2), _p(side, 1, 2)
    w = []
    for n, h in enumerate((14, 30)):                                           # measure... measure again
        for k in range(3):
            w += emit_at(PLANK26, tres, 1, (-sx * (30 - k * 6), h)) + wait(1)
        w += se(s["clock"]) + _hold(PLANK26, tres, 1, (-sx * 12, h), 5)
    w += wait(3) + se(s["whoosh"])
    for k, (x, y) in enumerate(((sx * 14, 50), (dx * .4, dy + 70), (dx - sx * 26, dy + 52))):   # ...swing once
        w += emit_at(PLANKB26, bres, 0, (round(x), round(y))) + wait(1)
    w += se(s["wslap"]) + se(s["crack"]) + flash_screen(4) + emit_at(PLANKB26, bres, 0, (dx - sx * 18, dy + 30))
    w += emit_at(PLANK26, 0, 1, (0, 26)) + shake_defender(4, 3) + func(48) + wait(2)
    w += _hold(PLANKB26, bres, 0, (dx - sx * 18, dy + 30), 4)
    w += bmove(side, 258, 2, -sx * 10, 0) + func(34, 2, 0, 1, rgb(255, 120, 120), 9, 0) + wait(3)   # recoil: that stung
    return w + bmove(side, 258, 3, sx * 10, 0) + wait(2)


def _kick_back(side, s):
    """Slack Off (Kick Back): a recliner under them. Pull the lever - *clunk* - footrest pops out. Lay all the way back.
    Ahhhh - HP comes back."""
    sx = _sx(side)
    seat = _p(side, (0, -4), (0, -2))
    st = _p(side, ((RECL26, 1), (RECL26, 2), (RECLB26, 1)), ((RECLB26, 2), (RECLC26, 1), (RECLC26, 2)))
    w = se(s["pop"]) + _hold(st[0][0], st[0][1], 0, seat, 6)
    w += se(s["clock"]) + bmove(side, 258, 2, 0, -4) + _hold(st[1][0], st[1][1], 0, seat, 6)   # *clunk* - footrest
    w += se(s["flop"]) + bmove(side, 258, 2, -sx * 4, -4) + _hold(st[2][0], st[2][1], 0, seat, 4)   # all the way back
    w += se(s["rest"]) + func(34, 2, 0, 1, rgb(140, 255, 160), 12, 0)
    for k in range(10):                                                        # ahhhh
        w += emit_at(st[2][0], st[2][1], 0, seat) + (emit_at(RECL26, 0, 0, (0, 30)) if k % 3 == 0 else []) + wait(1)
    w += bmove(side, 258, 3, sx * 4, 8) + _hold(st[0][0], st[0][1], 0, seat, 3)
    return w


def _slow_jam(side, s):
    """GrassWhistle (Slow Jam): setting the mood around the foe - a candle lit - another - another. The slow jam comes
    on, love notes drift over, the foe sways... and dozes right off."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    spots = [(-30, 2), (30, 2), (sx * 44, 18)]
    lit = []
    cs = lambda: [w_ for i, p in enumerate(spots) for w_ in emit_at(JAM26, 1 if i in lit else 2, 1, p)]
    w = se(s["pop"]) + _hold(JAM26, 2, 1, spots[0], 3, lambda k: emit_at(JAM26, 2, 1, spots[1]) + emit_at(JAM26, 2, 1, spots[2]))
    for i in range(3):                                                         # *flick* - lit, lit, lit
        lit.append(i)
        w += se(s["ember"])
        for k in range(3):
            w += cs() + wait(1)
    w += se(s["sscent"])
    for k in range(16):                                                        # the slow jam: notes drift over, the foe sways
        if k % 2 == 0:
            t = (k % 8) / 8
            w += emit_at(JAM26, 0, 0, (round(dx * t), round(dy * t + 30)))
        if k in (2, 8):
            w += bmove(side, 264, 3, sx * 6, 0)
        if k in (5, 11):
            w += bmove(side, 264, 3, -sx * 6, 0)
        w += cs() + wait(1)
    w += se(s["yawn"]) + bmove(side, 264, 3, 0, -6) + func(34, 8, 0, 1, rgb(80, 80, 160), 10, 0)   # ...out
    for k in range(10):
        w += (emit_at(JAMB26, 0, 1, (sx * 14, 36)) if k % 3 == 0 else []) + cs() + wait(1)
    return w + bmove(side, 264, 3, 0, 6) + wait(2)
'''

TABLE = {417: ("_finesse", ("FIN26", "FINB26"), "Covet"),
         418: ("_ext_cord", ("CORD26", "CORDB26"), "Power Whip"),
         419: ("_two_by_four", ("PLANK26", "PLANKB26"), "Wood Hammer"),
         420: ("_kick_back", ("RECL26", "RECLB26", "RECLC26"), "Slack Off"),
         421: ("_slow_jam", ("JAM26", "JAMB26"), "GrassWhistle")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
