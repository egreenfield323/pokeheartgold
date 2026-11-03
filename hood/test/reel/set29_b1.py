"""Set 29 batch 1: Blow Dryer, Snow Globe, Spinners, Throw Shade, Burned CD (variants 484-488, test-only 499 =
Blow Dryer turn 2 first).
Run once from the repo root: python -X utf8 hood/test/reel/set29_b1.py  (art: set29_b1_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "DRY29 GLOBE29 RIM29 RIMB29 SHADE29 CD29".split()

KITS = '''
    # ---- set 29, batch 1 ----------------------------------------------------------------------------------
    # Blow Dryer (Razor Wind): plug in - low - HIGH (turn 1) / razor gusts across the field (turn 2)
    b, rs = pk(DRY29, {1: (fxart.blow_dryer(), .8, 4, {}), 2: (flipx(fxart.blow_dryer()), .8, 4, {})}, alpha=fxart.gust_slash())
    prop(b, rs, 0, tex=0, clr=rgb(220, 240, 255), clr_anm=(rgb(220, 240, 255), rgb(220, 240, 255)), scl=.7, life=4)
    burst(b, rs, 3, rgb(200, 230, 255), rgb(255, 255, 255), .5, 12, .3, life=14)
    fin(DRY29, b, rs, (0, 1, 2, 3))

    # Snow Globe (Weather Ball): shake - shake - the weather inside goes wild - thrown - SMASH
    b, rs = pk(GLOBE29, {1: (fxart.hood_snow_globe(), 1.0, 4, {}), 2: (fxart.hood_snow_globe(storm=True), 1.0, 4, {})}, alpha=fxart.soft_puff())
    burst(b, rs, 0, rgb(245, 250, 255), rgb(255, 255, 255), .3, 22, .34, up=.12, gravity=.008, life=26)
    fin(GLOBE29, b, rs, (0, 1, 2))

    # Spinners (Mirror Shot): the spinner rim keeps spinning - glint - glint - the sun hits it - GLARE
    b, rs = pk(RIM29, {1: (fxart.spinner_rim(), .8, 4, {}), 2: (fxart.spinner_rim(angle=36), .8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 230), rgb(255, 255, 255), .6, 6, .12, life=12, radius=.2)
    fin(RIM29, b, rs, (0, 1, 2))
    b, rs = pk(RIMB29, {}, alpha=fxart.soft_puff())
    prop(b, rs, 0, tex=0, clr=rgb(255, 250, 210), clr_anm=(rgb(255, 250, 210), rgb(255, 250, 210)), scl=.6, life=4, alpha=(26, 26, 0))
    fin(RIMB29, b, rs, (0,))

    # Throw Shade (Psycho Cut): a lampshade - on the head - then THROWN, spinning, and it slices the foe
    b, rs = pk(SHADE29, {1: (fxart.lampshade(), .7, 4, {}), 2: (flipx(fxart.lampshade()), .7, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 120, 220), rgb(255, 230, 250), .55, 14, .3, life=14)
    fin(SHADE29, b, rs, (0, 1, 2))

    # Burned CD (Copycat): MIX COPY - into the boombox - skip - skip - and it plays the copy
    b, rs = pk(CD29, {1: (fxart.burned_cd(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.cd_boombox(), .9, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(200, 230, 255), rgb(255, 240, 255), .5, 16, .28, life=16)
    fin(CD29, b, rs, (0, 1, 2))
'''

SCRIPTS = '''
def _blow_dryer(side, s):
    """Razor Wind (Blow Dryer), two turns. Turn 1: a salon blow dryer - plug in - click, low - click, HIGH, rattling
    in their hand. Turn 2: aimed at the foe - razor gusts rip across the field."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    res = _p(side, 1, 2)
    dr = (sx * 30, 30)
    one = se(s["pop"]) + _hold(DRY29, res, 0, dr, 5)
    for n in range(2):                                                         # click, low... click, HIGH
        one += se(s["clock"]) + se(s["gust"] if n else s["whoosh"])
        for k in range(6 + n * 4):
            one += emit_at(DRY29, res, 0, (dr[0] + (k % 2) * (1 + n), dr[1] + (k % 2) * n))
            if k % (3 - n) == 0:
                one += emit_at(DRY29, 0, 0, (dr[0] + sx * (18 + k * 2), dr[1] + 4))
            one += wait(1)
    one += _hold(DRY29, res, 0, dr, 3)
    two = se(s["gust"]) + se(s["razor"] if "razor" in s else s["slash"]) + _hold(DRY29, res, 0, dr, 2)
    for k in range(10):                                                        # razor gusts
        two += emit_at(DRY29, res, 0, dr)
        for j in range(2):
            t = ((k + j * 3) % 5 + 1) / 5
            p = _lerp(dr, (dx, dy + 24), t)
            two += emit_at(DRY29, 0, 0, (p[0], p[1] + (j * 12 - 6)))
        if k % 3 == 2:
            two += se(s["slash"]) + emit_at(DRY29, 3, 1, (0, 24)) + func(48) + shake_defender(2, 1)
        two += wait(1)
    two += wait(3) + wait(8)
    return one, two


def _blow_dryer_turn2_first(side, s):
    """Test only: Blow Dryer's second turn on its own."""
    return _blow_dryer(side, s)[1]


def _snow_globe(side, s):
    """Weather Ball (Snow Globe): a snow globe of the block. Shake - flurries. Shake - more. SHAKE - the weather inside
    goes wild, lightning and all. Thrown - SMASH - a blizzard bursts out over the foe."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    g = (sx * 30, 42)
    w = se(s["pop"]) + _hold(GLOBE29, 1, 0, g, 4)
    for n in range(2):                                                         # shake... shake...
        w += se(s["swipe"])
        for k in range(5):
            w += emit_at(GLOBE29, 1, 0, (g[0] + (3 if k % 2 else -3) * (n + 1), g[1])) + wait(1)
        w += _hold(GLOBE29, 1, 0, g, 3)
    w += se(s["thunder"])
    for k in range(6):                                                         # SHAKE - the storm
        w += emit_at(GLOBE29, 2, 0, (g[0] + (5 if k % 2 else -5), g[1] + (k % 2) * 2)) + wait(1)
    w += se(s["whoosh"]) + _lob(GLOBE29, 2, side, g, (dx, dy + 30), 5, 24)
    w += se(s["ishard"] if "ishard" in s else s["crack"]) + se(s["blizzard"]) + flash_screen(4)   # SMASH
    w += emit_at(GLOBE29, 0, 1, (0, 30)) + emit_at(GLOBE29, 0, 1, (0, 10)) + func(48) + shake_defender(4, 3)
    w += func(34, 8, 0, 1, rgb(210, 235, 255), 13, 0)
    for k in range(8):
        w += (emit_at(GLOBE29, 0, 1, (sx * (k - 4) * 6, 40)) if k % 3 == 0 else []) + wait(1)
    return w + wait(3) + wait(8)


def _spinners(side, s):
    """Mirror Shot (Spinners): a chrome spinner rim rolls in next to them, still spinning. Glint. Glint. Then the sun
    hits it just right - a blinding glare straight in the foe's eyes."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    rim = (sx * 34, 16)
    spin = lambda k: emit_at(RIM29, 1 + k % 2, 0, rim)
    w = se(s["rollout"])
    for k in range(5):                                                         # rolls in
        w += emit_at(RIM29, 1 + k % 2, 0, (rim[0] - sx * (40 - k * 8), rim[1])) + wait(1)
    for n in range(2):                                                         # glint... glint...
        for k in range(5):
            w += spin(k) + (se(s["bling"]) + emit_at(RIM29, 0, 0, (rim[0] - 6, rim[1] + 8)) if k == 2 else []) + wait(1)
    w += se(s["sbeam"]) + flash_screen(5)                                     # GLARE
    for k in range(12):
        w += spin(k)
        for t in (.3, .55, .8):
            p = _lerp(rim, (dx, dy + 26), t)
            w += emit_at(RIMB29, 0, 0, p)
        if k == 2:
            w += func(34, 8, 0, 1, rgb(255, 255, 230), 15, 0) + func(48) + shake_defender(3, 3)
        w += wait(1)
    return w + wait(3) + wait(8)


def _throw_shade(side, s):
    """Psycho Cut (Throw Shade): a lampshade lands on their head like they're the life of the party. Then they throw
    shade - literally - the lampshade flies spinning like a blade and slices clean through the foe."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    head = (_p(side, 10, 0), _p(side, 34, 44))
    w = []
    for k in range(4):                                                         # lands on their head
        w += emit_at(SHADE29, 1, 0, (head[0], head[1] + 30 - k * 10)) + wait(1)
    w += se(s["pop"]) + bmove(side, 258, 2, 0, 4) + _hold(SHADE29, 1, 0, (head[0], head[1] + 4), 4) + bmove(side, 258, 2, 0, -4)
    w += _hold(SHADE29, 1, 0, head, 4)
    w += se(s["psych"]) + se(s["whoosh"])
    for k in range(7):                                                         # THROWN - spinning
        p = _lerp(head, (dx + sx * 20, dy + 26), (k + 1) / 7)
        w += emit_at(SHADE29, 1 + k % 2, 0, p) + wait(1)
    w += se(s["slash"]) + se(s["bslam"]) + flash_screen(3) + emit_at(SHADE29, 0, 1, (0, 24)) + func(48) + shake_defender(4, 3)
    for k in range(4):                                                         # and gone
        w += emit_at(SHADE29, 1 + k % 2, 0, (dx + sx * (36 + k * 20), dy + 30 + k * 6)) + wait(1)
    return w + wait(3) + wait(8)


def _burned_cd(side, s):
    """Copycat (Burned CD): a burned CD - MIX COPY in sharpie - into the boombox. Skip. Skip. Then it plays: a
    bootleg copy of the last move, blasted at the foe."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    bb = (sx * 36, 28)
    cd = _p(side, (sx * 6, 66), (-30, 42))
    w = se(s["pop"]) + _hold(CD29, 1, 0, cd, 8, lambda k: emit_at(CD29, 2, 0, bb))
    w += se(s["whoosh"]) + _lob(CD29, 1, side, cd, (bb[0], bb[1] + 10), 4, 10, lambda k: emit_at(CD29, 2, 0, bb))
    for n in range(2):                                                         # skip... skip...
        w += se(s["peck"]) + _hold(CD29, 2, 0, (bb[0] + (2 if n else -2), bb[1]), 2) + _hold(CD29, 2, 0, bb, 4)
    w += se(s["bling"]) + se(s["bslam"])                                       # it plays
    for k in range(8):
        w += emit_at(CD29, 2, 0, (bb[0] + (k % 2), bb[1]))
        if k % 2 == 0:
            w += emit_at(CD29, 0, 0, _lerp(bb, (dx, dy + 24), (k + 2) / 8))
        w += wait(1)
    w += se(s["kaboom"]) + flash_screen(3) + emit_at(CD29, 0, 1, (0, 24)) + func(48) + shake_defender(3, 3)
    return w + _hold(CD29, 2, 0, bb, 4) + wait(8)
'''

TABLE = {484: ("_blow_dryer", ("DRY29",), "Razor Wind"),
         485: ("_snow_globe", ("GLOBE29",), "Weather Ball"),
         486: ("_spinners", ("RIM29", "RIMB29"), "Mirror Shot"),
         487: ("_throw_shade", ("SHADE29",), "Psycho Cut"),
         488: ("_burned_cd", ("CD29",), "Copycat")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
    p = set23_lib.ROOT / "hood/gunfx.py"
    s = p.read_text(encoding="utf-8")
    for a, b in (("            484: _blow_dryer,\n", "            484: _blow_dryer,\n            499: _blow_dryer_turn2_first,\n"),
                 ("        484: (DRY29,),\n", "        484: (DRY29,),\n        499: (DRY29,),\n")):
        assert s.count(a) == 1, a
        s = s.replace(a, b)
    p.write_text(s, encoding="utf-8", newline="")
