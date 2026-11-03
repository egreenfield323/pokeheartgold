"""Set 23 batch 4: Cold Cocked, Last Call, Tanning Bed, Victory Lap, Gift Bomb (variants 314-318, plus test
variant 329 = Tanning Bed's turn 2 on its own). Run once from the repo root: python -X utf8 hood/test/reel/set23_b4.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "FREEZE23 FREEZEB23 BELL23 BELLB23 BELLC23 TAN23 TANB23 TROPHY23 GIFT23 GIFTB23 GIFTC23".split()

KITS = '''
    # ---- set 23, batch 4 ----------------------------------------------------------------------------------
    # Cold Cocked (Ice Punch): the chest freezer - a popsicle (nah) - a bag of peas (nah) - a FROZEN TURKEY. WHAM.
    b, rs = pk(FREEZE23, {1: (fxart.chest_freezer(), 1.0, 4, {}), 2: (fxart.popsicle(), .5, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(225, 240, 255), n=5, life=20, scl=.4, up=.06)
    fin(FREEZE23, b, rs, (0, 1, 2))
    b, rs = pk(FREEZEB23, {1: (fxart.peas_bag(), .55, 4, {}), 2: (fxart.frozen_turkey(), .95, 4, {})}, alpha=fxart.frost_crystal())
    burst(b, rs, 0, rgb(170, 220, 255), rgb(255, 255, 255), .45, 14, .24, up=.06, life=22, spin=0x0600)
    fin(FREEZEB23, b, rs, (0, 1, 2))

    # Last Call (Heal Bell): the club's dark, the mirror ball turning - ding... ding... DING-DING-DING - LAST CALL!
    # The lights slam on and everybody sobers up.
    b, rs = pk(BELL23, {1: (fxart.bar_bell(swing=-1), .9, 4, {}), 2: (fxart.bar_bell(swing=1), .9, 4, {})}, alpha=fxart.glow_dot())
    burst(b, rs, 0, rgb(160, 255, 170), rgb(240, 255, 240), .3, 10, .06, up=.12, life=24, radius=.6)
    fin(BELL23, b, rs, (0, 1, 2))
    b, rs = pk(BELLB23, {1: (fxart.mirror_ball(), .8, 4, {}), 2: (fxart.mirror_ball(phase=1), .8, 4, {})}, alpha=fxart.glow_dot())
    burst(b, rs, 0, rgb(255, 120, 220), rgb(160, 220, 255), .3, 6, .2, life=12, radius=.3)
    fin(BELLB23, b, rs, (0, 1, 2))
    b, rs = pk(BELLC23, {1: (fxart.burst_sign(["LAST CALL!"], fill=(40, 30, 70, 255), text=(255, 230, 80, 255)), SIGN_SCALE, 4, {"colors": 30})})
    fin(BELLC23, b, rs, (1,))

    # Tanning Bed (SolarBeam): turn 1 - the bed clamps shut, UV buzzing. Turn 2 - it pops open, they're ORANGE,
    # and the glare off that tan torches the foe.
    b, rs = pk(TAN23, {1: (fxart.tanning_bed(), 1.6, 4, {}), 2: (fxart.tanning_bed(shut=True), 1.6, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(170, 110, 255), n=6, life=18, scl=.28, up=.05)
    fin(TAN23, b, rs, (0, 1, 2))
    b, rs = pk(TANB23, {}, alpha=fxart.sun_ray())
    spray2(b, rs, {"player": (6, 36), "enemy": (-6, 30)}, (0, 24), 10, clr=rgb(255, 160, 40),
           clr_anm=(rgb(255, 250, 200), rgb(255, 110, 20)), scl=.9, gen=3, gen_intvl=1, emtr_life=22, radius=.15,
           spread=.02, alpha=(31, 28, 0))
    burst(b, rs, 2, rgb(255, 170, 40), rgb(255, 255, 220), .6, 10, .2, life=14)
    fin(TANB23, b, rs, (0, 1, 2))

    # Victory Lap (Petal Dance): trophy up, rose petals raining - strut - strut - then the trophy off the foe's head
    b, rs = pk(TROPHY23, {1: (fxart.victory_trophy(), .75, 4, {})}, alpha=fxart.rose_petal())
    burst(b, rs, 0, rgb(230, 30, 60), rgb(255, 150, 170), .35, 8, .06, up=-.02, gravity=.006, life=40, radius=1.2, spin=0x0500)
    burst(b, rs, 2, rgb(255, 230, 80), rgb(255, 255, 255), .45, 8, .2, life=12)
    fin(TROPHY23, b, rs, (0, 1, 2))

    # Gift Bomb (Present): a big present - it pops open: a smaller present - pops: a tiny one - pops: a bomb. BOOM.
    b, rs = pk(GIFT23, {1: (fxart.gift_box(), .9, 4, {}), 2: (fxart.gift_box(wrap=(40, 170, 80, 255), ribbon=(255, 255, 255, 255)), .65, 4, {})},
               alpha=fxart.confetti_bit())
    burst(b, rs, 0, rgb(255, 220, 60), rgb(120, 220, 255), .3, 12, .2, up=.16, gravity=.012, life=22, spin=0x0900)
    fin(GIFT23, b, rs, (0, 1, 2))
    b, rs = pk(GIFTB23, {1: (fxart.gift_box(wrap=(60, 110, 230, 255), ribbon=(255, 120, 200, 255)), .45, 4, {}),
                         2: (fxart.cartoon_bomb(), .7, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 180, 40), rgb(255, 255, 200), .3, 3, .08, up=.08, gravity=.008, life=10)
    fin(GIFTB23, b, rs, (0, 1, 2))
    b, rs = pk(GIFTC23, {1: (fxart.confetti_boom(), 1.7, 14, {"scl_anm": (.2, 1.2, 1.0, 50, 255)})}, alpha=fxart.confetti_bit())
    burst(b, rs, 0, rgb(255, 80, 200), rgb(80, 220, 255), .35, 18, .3, up=.2, gravity=.012, life=30, spin=0x0B00)
    fin(GIFTC23, b, rs, (0, 1))
'''

SCRIPTS = '''
def _cold_cocked(side, s):
    """Ice Punch (Cold Cocked): a chest freezer, lid up, cold mist rolling out. They dig in: a popsicle - nah,
    tossed. A bag of peas - nah, tossed. Then a whole FROZEN TURKEY comes out (slow, heavy) - and goes upside the
    foe's head. Frosted."""
    sx = _sx(side)
    fr = _s23(side, 0, (104, 82))
    top = (fr[0], fr[1] + 26)
    back = _s23(side, 0, _p(side, (-30, 40), (290, 20)))
    dx, dy = TARGET_FROM_ATTACKER[side]
    box = lambda: emit_at(FREEZE23, 1, 0, fr)
    w = se(s["pop"]) + box() + emit_at(FREEZE23, 0, 0, top) + wait(1) + _hold(FREEZE23, 1, 0, fr, 3)
    for kit, res in ((FREEZE23, 2), (FREEZEB23, 1)):                           # nah... nah...
        for k in range(3):
            w += box() + emit_at(kit, res, 0, (top[0], top[1] - 10 + k * 8)) + wait(1)
        w += _hold(kit, res, 0, (top[0], top[1] + 6), 3, lambda k: box())
        w += se(s["whoosh"]) + _lob(kit, res, side, (top[0], top[1] + 6), back, 5, 24, lambda k: box()) + _hold(FREEZE23, 1, 0, fr, 2)
    w += se(s["ishard"]) + emit_at(FREEZE23, 0, 0, top)                         # *...the turkey*
    for k in range(6):
        w += box() + emit_at(FREEZEB23, 2, 0, (top[0], top[1] - 14 + k * 5)) + wait(1)
    w += se(s["bling"]) + emit_at(FREEZEB23, 0, 0, (top[0], top[1] + 16))
    w += _hold(FREEZEB23, 2, 0, (top[0], top[1] + 16), 4, lambda k: box())
    w += se(s["whoosh"]) + _lob(FREEZEB23, 2, side, (top[0], top[1] + 16), (dx - sx * 6, dy + 26), 5, 20, lambda k: box())
    w += se(s["bslam"]) + se(s["ishard"]) + flash_screen(4) + emit_at(FREEZEB23, 0, 1, (0, 24))   # WHAM
    w += shake_defender(4, 3) + func(48) + func(34, 8, 0, 1, rgb(160, 220, 255), 14, 0)
    w += _lob(FREEZEB23, 2, side, (dx - sx * 6, dy + 26), (dx + sx * 40, dy - 10), 4, 16, lambda k: box())
    return w + _hold(FREEZE23, 1, 0, fr, 5)


def _last_call(side, s):
    """Heal Bell (Last Call): the club's dark, the mirror ball turning. The bartender's bell: ding... ding... then
    DING-DING-DING-DING - LAST CALL! - the lights slam on and the whole crew sobers right up."""
    bell = _s23(side, 0, (106, 80))
    ball = _s23(side, 0, (152, 24))
    mb = lambda k: emit_at(BELLB23, 1 + k % 2, 0, ball) + (emit_at(BELLB23, 0, 0, ball) if k % 4 == 0 else [])
    dark = rgb(40, 20, 70)
    w = func(33, 0, 1, 0, 12, dark) + wait(2)
    w += _hold(BELL23, 1, 0, bell, 4, mb)
    for n in range(2):                                                         # ding... ding...
        w += se(s["bling"]) + _hold(BELL23, 2, 0, bell, 2, lambda k: mb(k + 1)) + _hold(BELL23, 1, 0, bell, 5, mb)
    for k in range(8):                                                         # DING DING DING DING
        w += emit_at(BELL23, 1 + k % 2, 0, bell) + mb(k)
        if k % 2 == 0:
            w += se(s["bling"])
        w += wait(1)
    w += func(33, 0, 1, 12, 0, dark) + flash_screen(4) + se(s["safeguard"])    # LIGHTS ON
    sign = _p(side, (0, 58), (0, 50))
    for k in range(12):
        w += emit_at(BELLC23, 1, 0, sign) + emit_at(BELL23, 1, 0, bell) + emit_at(BELLB23, 1, 0, ball)
        if k in (2, 7):
            w += emit_at(BELL23, 0, 0, (0, 10)) + func(34, 2, 0, 1, rgb(160, 255, 170), 10, 0)
        if k == 4:
            w += shake_defender(1, 2)                                          # (the foe squints)
        w += wait(1)
    return w + wait(2)


def _tanning_bed(side, s):
    """SolarBeam (Tanning Bed), two turns. Turn 1: the tanning bed opens round them, they lie back, it clamps shut
    and buzzes purple. Turn 2: it pops open, they come out deep ORANGE, and the glare off the tan torches the foe."""
    sx = _sx(side)
    bed = (0, _p(side, 10, 6))
    one = se(s["pop"]) + _hold(TAN23, 1, 0, bed, 4)
    one += se(s["harden"]) + _hold(TAN23, 2, 0, bed, 2)                        # *clunk*
    for k in range(14):                                                        # bzzzzz
        one += emit_at(TAN23, 2, 0, (bed[0] + (k % 2), bed[1]))
        if k % 4 == 0:
            one += se(s["zap"]) + emit_at(TAN23, 0, 0, (bed[0], bed[1] + 4)) + func(34, 2, 0, 1, rgb(190, 120, 255), 6, 0)
        one += wait(1)
    one += wait(2)
    two = _hold(TAN23, 2, 0, bed, 3) + se(s["pop"]) + emit_at(TAN23, 0, 0, (bed[0], bed[1] + 6))   # *ding* - open
    two += func(34, 2, 0, 1, rgb(255, 120, 20), 15, 0)                         # ORANGE
    two += _hold(TAN23, 1, 0, bed, 5, lambda k: se(s["bling"]) + emit_at(TANB23, 2, 0, (0, 30)) if k == 1 else [])
    two += se(s["sbeam"]) + flash_screen(3) + emit_at(TANB23, _p(side, 0, 1), 0, (sx * 6, 30))   # the GLARE
    for k in range(14):
        if k % 3 == 0:
            two += emit_at(TANB23, 2, 1, (((k * 11) % 24) - 12, 20 + (k * 7) % 20)) + shake_defender(1, 1)
        if k == 6:
            two += se(s["ember"]) + func(34, 8, 0, 1, rgb(255, 140, 40), 13, 0)
        two += wait(1)
    two += func(48) + func(34, 2, 0, 1, rgb(255, 120, 20), 10, 0) + wait(4)
    return one, two


def _tanning_bed_turn2_first(side, s):
    """Test only: Tanning Bed's second turn on its own (the showcase only plays turn 1)."""
    return _tanning_bed(side, s)[1]


def _victory_lap(side, s):
    """Petal Dance (Victory Lap): trophy up, rose petals raining from the stands - strut left - strut right - then
    the trophy comes down on the foe's head. (Short: it replays every turn.)"""
    sx = _sx(side)
    up = _p(side, (sx * 4, 44), (0, 42))
    tro = lambda: emit_at(TROPHY23, 1, 0, up)
    rain = lambda k: emit_at(TROPHY23, 0, 0, (sx * 10, 92)) if k % 3 == 0 else []
    w = se(s["bling"]) + _hold(TROPHY23, 1, 0, up, 3, rain)
    for n, d_ in enumerate((-1, 1)):                                           # strut... strut...
        w += se(s["chaching"]) + bmove(side, 258, 4, d_ * 14, 0)
        w += _hold(TROPHY23, 1, 0, up, 4, lambda k: rain(k + n) + (bmove(side, 258, 1, 0, 4 if k % 2 == 0 else -4) if k < 4 else []))
        w += bmove(side, 258, 4, -d_ * 14, 0)
    w += _hold(TROPHY23, 1, 0, up, 2, rain)
    w += bmove(side, 258, 2, sx * 22, 8) + tro() + wait(1)                     # *BONK*
    w += se(s["bonk"]) + se(s["bslam"]) + flash_screen(3) + emit_at(TROPHY23, 2, 1, (0, 34)) + shake_defender(3, 3) + func(48)
    w += _hold(TROPHY23, 1, 0, up, 2) + bmove(side, 258, 4, -sx * 22, -8)
    return w + _hold(TROPHY23, 1, 0, up, 4, rain)


def _gift_bomb(side, s):
    """Present (Gift Bomb): a big wrapped present slides over to the foe. Pop - it's a smaller present. Pop - an
    even smaller one. Pop - a bomb, fuse lit. *...* BOOM, confetti everywhere."""
    sx = _sx(side)
    g = _p(side, (-62, 6), (40, 28))
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = se(s["whoosh"])
    for k in range(5):                                                         # *slides over*
        w += emit_at(GIFT23, 1, 1, (g[0] - sx * round(50 * (1 - (k + 1) / 5)), g[1])) + wait(1)
    w += _hold(GIFT23, 1, 1, g, 4, lambda k: bmove(side, 264, 2, -sx * 6, 0) if k == 1 else [])   # *ooh, for me?*
    for kit, res, nxt_kit, nxt_res in ((GIFT23, 1, GIFT23, 2), (GIFT23, 2, GIFTB23, 1), (GIFTB23, 1, GIFTB23, 2)):
        for k in range(3):                                                     # rattle rattle
            w += emit_at(kit, res, 1, (g[0] + (2 if k % 2 else -2), g[1])) + wait(1)
        w += se(s["pop"]) + emit_at(GIFT23, 0, 1, (g[0], g[1] + 10))           # pop
        for k in range(3):
            w += emit_at(nxt_kit, nxt_res, 1, (g[0], g[1] + 12 - k * 4)) + wait(1)
        w += _hold(nxt_kit, nxt_res, 1, g, 3 if nxt_res != 2 or nxt_kit != GIFTB23 else 2)
    fuse = (g[0] + 6, g[1] + 14)
    w += se(s["ember"]) + _hold(GIFTB23, 2, 1, g, 6, lambda k: emit_at(GIFTB23, 0, 1, fuse) if k % 2 == 0 else [])   # *tsss*
    w += bmove(side, 264, 2, sx * 6, 0) + _hold(GIFTB23, 2, 1, g, 2)
    w += se(s["kaboom"]) + se(s["explo"]) + flash_screen(5) + emit_at(GIFTC23, 1, 1, g) + emit_at(GIFTC23, 0, 1, g)   # BOOM
    w += func(68, 5, 5, 1, 3, 0) + shake_defender(4, 4) + func(48) + func(34, 8, 0, 1, rgb(60, 50, 50), 12, 0)
    return w + wait(10)
'''

TABLE = {314: ("_cold_cocked", ("FREEZE23", "FREEZEB23"), "Ice Punch"),
         315: ("_last_call", ("BELL23", "BELLB23", "BELLC23"), "Heal Bell"),
         316: ("_tanning_bed", ("TAN23", "TANB23"), "SolarBeam"),
         317: ("_victory_lap", ("TROPHY23",), "Petal Dance"),
         318: ("_gift_bomb", ("GIFT23", "GIFTB23", "GIFTC23"), "Present")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
    # the test-only variant (no move): Tanning Bed's turn 2 first
    p = set23_lib.ROOT / "hood/gunfx.py"
    s = p.read_text(encoding="utf-8")
    for a, b in (("            316: _tanning_bed,\
", "            316: _tanning_bed,\
            329: _tanning_bed_turn2_first,\
"),
                 ("        316: (TAN23, TANB23,),\
", "        316: (TAN23, TANB23,),\
        329: (TAN23, TANB23,),\
")):
        assert s.count(a) == 1, a
        s = s.replace(a, b)
    p.write_text(s, encoding="utf-8", newline="")
