"""Set 28 batch 2: Mirror Tint, Jump Em, Quick Draw, Bad Vibes, Hood Power (variants 459-463).
Run once from the repo root: python -X utf8 hood/test/reel/set28_b2.py  (art: set28_b2_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "TINT28 TINTB28 CREW28 DRAW28 DRAWB28 VIBE28 VIBEB28 CAT28 CATB28".split()

KITS = '''
    # ---- set 28, batch 2 ----------------------------------------------------------------------------------
    # Mirror Tint (Mirror Coat): squeegee - squeegee - mirror tint. The foe's blast bounces right back.
    b, rs = pk(TINT28, {1: (fxart.tint_glass(), 1.1, 4, {}), 2: (fxart.tint_glass(tinted=True), 1.1, 4, {})}, alpha=fxart.soft_puff())
    prop(b, rs, 0, tex=0, clr=rgb(200, 90, 255), clr_anm=(rgb(200, 90, 255), rgb(200, 90, 255)), scl=.5, life=4)
    fin(TINT28, b, rs, (0, 1, 2))
    b, rs = pk(TINTB28, {1: (fxart.tint_squeegee(), .5, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(230, 200, 255), rgb(255, 255, 255), .5, 16, .3, life=14)
    fin(TINTB28, b, rs, (0, 1))

    # Jump Em (Beat Up): one of the crew pulls up and swings (replays per teammate: short)
    b, rs = pk(CREW28, {1: (fxart.crew_member(), .9, 4, {}), 2: (fxart.crew_member(tint=1), .9, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .5, 10, .26, life=10)
    fin(CREW28, b, rs, (0, 1, 2))

    # Quick Draw (Vacuum Wave): cowboy hat - the town clock at 11:59 - tick - tick - 12:00 - BANG, first
    b, rs = pk(DRAW28, {1: (fxart.noon_clock(), 1.0, 4, {}), 2: (fxart.noon_clock(noon=True), 1.0, 4, {})})
    fin(DRAW28, b, rs, (1, 2))
    b, rs = pk(DRAWB28, {1: (fxart.cowboy_hat(), .55, 4, {})}, alpha=fxart.air_ring())
    prop(b, rs, 0, tex=0, clr=rgb(230, 245, 255), clr_anm=(rgb(230, 245, 255), rgb(230, 245, 255)), scl=.9, life=4)
    burst(b, rs, 3, rgb(230, 245, 255), rgb(255, 255, 255), .7, 6, .2, life=12, radius=.2)
    fin(DRAWB28, b, rs, (0, 1, 3))

    # Bad Vibes (Psywave): VIBE CHECK - GOOD - OK - BAD - bad vibes radiate off the foe
    b, rs = pk(VIBE28, {1: (fxart.vibe_meter(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.vibe_meter(level=1), ONE_TO_ONE, 4, {"colors": 30})})
    fin(VIBE28, b, rs, (1, 2))
    b, rs = pk(VIBEB28, {1: (fxart.vibe_meter(level=2), ONE_TO_ONE, 4, {"colors": 30})}, alpha=fxart.air_ring())
    burst(b, rs, 0, rgb(190, 80, 230), rgb(255, 200, 255), .6, 6, .18, life=18, radius=.3)
    fin(VIBEB28, b, rs, (0, 1))

    # Hood Power (Nature Power): the bodega cat - unimpressed - swat - swat - SWAT
    b, rs = pk(CAT28, {1: (fxart.bodega_cat(), .8, 4, {}), 2: (fxart.bodega_cat(swat=True), .8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .5, 10, .26, life=10)
    fin(CAT28, b, rs, (0, 1, 2))
    b, rs = pk(CATB28, {1: (flipx(fxart.bodega_cat()), .8, 4, {}), 2: (flipx(fxart.bodega_cat(swat=True)), .8, 4, {})})
    fin(CATB28, b, rs, (1, 2))
'''

SCRIPTS = '''
def _mirror_tint(side, s):
    """Mirror Coat (Mirror Tint): a clear car window in front of them - squeegee, squeegee - the tint goes on, mirror
    black. The foe fires a blast at it... and it bounces straight back into them."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    win = (sx * 32, 24)
    w = se(s["pop"]) + _hold(TINT28, 1, 0, win, 4)
    for n in range(2):                                                         # squeegee... squeegee
        w += se(s["swipe"])
        for k in range(4):
            w += emit_at(TINTB28, 1, 0, (win[0] - 14 + k * 9, win[1] + 18 - n * 14)) + emit_at(TINT28, 1 + n, 0, win) + wait(1)
    w += se(s["bling"]) + emit_at(TINTB28, 0, 0, win) + _hold(TINT28, 2, 0, win, 6)
    foe = (dx, dy + 24)
    w += se(s["psych"])
    for k in range(5):                                                         # the foe's blast...
        w += emit_at(TINT28, 0, 0, _lerp(foe, win, (k + 1) / 5)) + emit_at(TINT28, 2, 0, win) + wait(1)
    w += se(s["reflect"]) + flash_screen(3) + emit_at(TINTB28, 0, 0, win)     # *PING*
    for k in range(4):                                                         # ...right back
        w += emit_at(TINT28, 0, 0, _lerp(win, foe, (k + 1) / 4)) + emit_at(TINT28, 2, 0, win) + wait(1)
    w += se(s["kaboom"]) + flash_screen(4) + emit_at(TINTB28, 0, 1, (0, 24)) + shake_defender(4, 3) + func(48)
    return w + _hold(TINT28, 2, 0, win, 5)


def _jump_em(side, s):
    """Beat Up (Jump Em): one of the crew pulls up next to the foe and swings. (Replays per teammate: short.)"""
    sx = _sx(side)
    res = 1 + (side == "enemy")
    w = se(s["whoosh"])
    for k in range(3):                                                         # pulls up
        w += emit_at(CREW28, res, 1, (-sx * (70 - k * 14), 10)) + wait(1)
    w += _hold(CREW28, res, 1, (-sx * 28, 10), 2)
    w += se(s["bonk"]) + se(s["bslam"]) + emit_at(CREW28, 0, 1, (0, 22)) + func(48) + shake_defender(3, 2)
    w += _hold(CREW28, res, 1, (-sx * 26, 10), 4)
    for k in range(3):
        w += emit_at(CREW28, res, 1, (-sx * (40 + k * 18), 10)) + wait(1)
    return w + wait(8)


def _quick_draw(side, s):
    """Vacuum Wave (Quick Draw): a cowboy hat drops on. The town clock: 11:59. Tick... tick... 12:00 - DING - and
    they're already drawn: a blast of air across the field before the foe even moves."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    clk = _s23(side, 0, (124, 70))
    hat = (_p(side, 10, 0), _p(side, 32, 40))
    scene = lambda r=1: emit_at(DRAW28, r, 0, clk) + emit_at(DRAWB28, 1, 0, hat)
    w = []
    for k in range(4):                                                         # the hat drops on
        w += emit_at(DRAWB28, 1, 0, (hat[0], hat[1] + 30 - k * 10)) + wait(1)
    w += se(s["pop"])
    for k in range(14):                                                        # tick... tick...
        w += scene() + (se(s["clock"]) if k % 5 == 0 else []) + wait(1)
    w += se(s["bling"]) + scene(2) + wait(1)                                   # 12:00
    w += se(s["kaboom"]) + flash_screen(3)
    for k in range(4):                                                         # BANG - the air shot
        p = _lerp((sx * 20, 30), (dx, dy + 24), (k + 1) / 4)
        w += scene(2) + emit_at(DRAWB28, 0, 0, p) + emit_at(DRAWB28, 0, 0, _lerp((sx * 20, 30), (dx, dy + 24), k / 4)) + wait(1)
    w += se(s["bslam"]) + emit_at(DRAWB28, 3, 1, (0, 24)) + shake_defender(4, 3) + func(48)
    for k in range(6):
        w += scene(2) + wait(1)
    return w


def _bad_vibes(side, s):
    """Psywave (Bad Vibes): a VIBE CHECK meter next to the foe. GOOD... the needle slips to OK... then hard into BAD -
    and bad vibes pour off the foe in waves."""
    sx = _sx(side)
    mtr = _s23(side, 0, _p(side, (128, 80), (114, 72)))
    w = se(s["pop"]) + _hold(VIBE28, 1, 0, mtr, 8)
    w += se(s["leer"]) + _hold(VIBE28, 2, 0, mtr, 8, lambda k: shake_defender(1, 1) if k == 2 else [])
    w += se(s["alarm"]) + _hold(VIBEB28, 1, 0, mtr, 4)
    w += se(s["psych"]) + func(34, 8, 0, 1, rgb(190, 80, 230), 13, 0)
    for k in range(12):                                                        # the waves
        w += emit_at(VIBEB28, 1, 0, mtr) + (emit_at(VIBEB28, 0, 1, (0, 22)) if k % 3 == 0 else [])
        w += (se(s["psych"]) + shake_defender(2, 2) if k == 6 else []) + wait(1)
    return w + func(48) + wait(2)


def _hood_power(side, s):
    """Nature Power (Hood Power): the bodega cat sits down next to the foe. Stares. Slow blink. Swat. Swat. Then it
    stands up and SWATS. Sits back down like nothing happened."""
    sx = _sx(side)
    kit = _p(side, CAT28, CATB28)
    cat = (-sx * 34, 2)
    w = se(s["pop"]) + _hold(kit, 1, 1, cat, 10)
    for n in range(2):                                                         # swat... swat...
        w += se(s["swipe"]) + _hold(kit, 2, 1, cat, 2) + emit_at(CAT28, 0, 1, (-sx * 8, 26)) + shake_defender(1, 1)
        w += _hold(kit, 1, 1, cat, 5)
    w += _hold(kit, 2, 1, (cat[0], cat[1] + 4), 3)                            # stands up...
    w += se(s["slash"]) + se(s["bslam"]) + flash_screen(3) + emit_at(CAT28, 0, 1, (0, 26)) + shake_defender(4, 3)   # SWAT
    w += _hold(kit, 2, 1, (cat[0], cat[1] + 4), 3) + func(48)
    return w + _hold(kit, 1, 1, cat, 8)
'''

TABLE = {459: ("_mirror_tint", ("TINT28", "TINTB28"), "Mirror Coat"),
         460: ("_jump_em", ("CREW28",), "Beat Up"),
         461: ("_quick_draw", ("DRAW28", "DRAWB28"), "Vacuum Wave"),
         462: ("_bad_vibes", ("VIBE28", "VIBEB28"), "Psywave"),
         463: ("_hood_power", ("CAT28", "CATB28"), "Nature Power")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
