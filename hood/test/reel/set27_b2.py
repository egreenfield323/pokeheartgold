"""Set 27 batch 2: RIP Shirt, Fresh Fit, Hotfoot, Space Jam, Dirty Water (variants 429-433).
Run once from the repo root: python -X utf8 hood/test/reel/set27_b2.py  (art: set27_b2_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "RIP27 FRESH27 FRESHB27 FRESHC27 HOT27 SPACE27 SPACEB27 DIRT27 DIRTB27".split()

KITS = '''
    # ---- set 27, batch 2 ----------------------------------------------------------------------------------
    # RIP Shirt (Memento): they sway - sway - drop. The airbrushed R.I.P. tee lands on the foe. Tears.
    b, rs = pk(RIP27, {1: (fxart.rip_tee(), ONE_TO_ONE, 4, {"colors": 30})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(120, 190, 255), rgb(220, 240, 255), .22, 1, .02, gravity=.02, life=14, radius=.05)
    fin(RIP27, b, rs, (0, 1))

    # Fresh Fit (Refresh): covered in lint - roll - roll - a spritz of cologne. Fresh.
    b, rs = pk(FRESH27, {1: (fxart.lint_roller(), .8, 4, {}), 2: (fxart.amber_cologne(), .5, 4, {})}, alpha=fxart.lint_ball())
    prop(b, rs, 0, tex=0, clr=rgb(120, 110, 100), clr_anm=(rgb(120, 110, 100), rgb(120, 110, 100)), scl=.55, life=4)
    fin(FRESH27, b, rs, (0, 1, 2))
    b, rs = pk(FRESHB27, {}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 220), rgb(255, 255, 255), .5, 12, .22, up=.06, life=20, radius=.5)
    fin(FRESHB27, b, rs, (0,))
    b, rs = pk(FRESHC27, {}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(250, 230, 190), n=5, life=18, scl=.26, up=.05)
    fin(FRESHC27, b, rs, (0,))

    # Hotfoot (Blaze Kick): slides and socks on baking asphalt - hop, ow - hop, OW - the slide catches - kicked
    b, rs = pk(HOT27, {1: (fxart.hot_asphalt(), 1.3, 4, {}), 2: (fxart.hood_slide(lit=True), .7, 4, {})}, alpha=fxart.soft_puff())
    burst(b, rs, 0, rgb(255, 120, 20), rgb(255, 240, 120), .32, 12, .26, up=.14, life=18)
    fin(HOT27, b, rs, (0, 1, 2))

    # Space Jam (Meteor Mash): a hoop over the foe - a twinkle up in the sky - a bigger one - the ball from orbit. SWISH.
    b, rs = pk(SPACE27, {1: (fxart.meteor_ball(), 1.1, 4, {}), 2: (flipx(fxart.meteor_ball()), 1.1, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 220), rgb(255, 255, 255), .5, 6, .1, life=14, radius=.2)
    burst(b, rs, 3, rgb(255, 160, 40), rgb(255, 250, 200), .6, 24, .4, up=.16, life=22)
    fin(SPACE27, b, rs, (0, 1, 2, 3))
    b, rs = pk(SPACEB27, {1: (fxart.street_hoop(), 1.0, 4, {})})
    fin(SPACEB27, b, rs, (1,))

    # Dirty Water (Muddy Water): waiting at the bus stop - a car through the puddle - another - then the bus
    b, rs = pk(DIRT27, {1: (fxart.curb_car(), 1.4, 4, {}), 2: (fxart.city_bus(), 2.0, 4, {})}, alpha=fxart.mud_splash())
    burst(b, rs, 0, rgb(120, 95, 50), rgb(170, 140, 90), .4, 14, .3, up=.3, gravity=.03, life=20)
    burst(b, rs, 3, rgb(110, 85, 45), rgb(170, 140, 90), .6, 30, .42, up=.44, gravity=.03, life=26, radius=.6)
    fin(DIRT27, b, rs, (0, 1, 2, 3))
    b, rs = pk(DIRTB27, {1: (fxart.bus_stop(), ONE_TO_ONE, 4, {"colors": 30})}, alpha=fxart.mud_splash())
    prop(b, rs, 0, tex=0, clr=rgb(90, 75, 50), clr_anm=(rgb(90, 75, 50), rgb(90, 75, 50)), scl=.9, life=4)
    fin(DIRTB27, b, rs, (0, 1))
'''

SCRIPTS = '''
def _rip_shirt(side, s):
    """Memento (RIP Shirt): they sway... sway... and drop. The airbrushed R.I.P. tee drifts down onto the foe - who
    wears it, tearing up, and just deflates."""
    sx = _sx(side)
    w = []
    for n in range(2):                                                         # sway... sway...
        w += bmove(side, 258, 3, sx * 6 * (1 if n == 0 else -2), 0) + wait(3)
    w += bmove(side, 258, 3, sx * 6, 0) + se(s["faint"]) + bmove(side, 258, 4, 0, -14)   # *drops*
    w += func(34, 2, 0, 1, rgb(90, 90, 100), 13, 0) + wait(6)
    w += se(s["mlook"])
    for k in range(6):                                                         # the tee drifts down
        w += emit_at(RIP27, 1, 1, (sx * (k % 2) * 3, 74 - k * 10)) + wait(1)
    w += se(s["flop"]) + _hold(RIP27, 1, 1, (0, 14), 4)
    for k in range(14):                                                        # tears
        if k % 2 == 0:
            w += emit_at(RIP27, 0, 1, (-6 + (k % 4) * 3, 50))
        w += emit_at(RIP27, 1, 1, (0, 14))
        if k == 4:
            w += se(s["cry"] if "cry" in s else s["leer"]) + bmove(side, 264, 3, 0, -6) + func(34, 8, 0, 1, rgb(60, 70, 140), 12, 0)
        w += wait(1)
    w += bmove(side, 264, 3, 0, 6) + bmove(side, 258, 4, 0, 14)
    return w + wait(2)


def _fresh_fit(side, s):
    """Refresh (Fresh Fit): they're covered in lint. The lint roller - roll, half of it's gone. Roll - all gone. Then a
    spritz of cologne - spritz - SPRITZ - fresh."""
    sx = _sx(side)
    lint = [(-12, 18), (10, 30), (-4, 40), (14, 12), (-14, 34)]
    gone = []
    dots = lambda: [w_ for i, p in enumerate(lint) if i not in gone for w_ in emit_at(FRESH27, 0, 0, p)]
    w = se(s["pop"]) + _hold(FRESH27, 0, 0, lint[0], 4, lambda k: dots())
    for n in range(2):                                                         # roll... roll...
        w += se(s["rollout"])
        for k in range(5):
            w += emit_at(FRESH27, 1, 0, (sx * 2, 46 - k * 8)) + dots() + wait(1)
            if k == 2:
                gone += [n * 2, n * 2 + 1] + ([4] if n else [])
    w += _hold(FRESH27, 2, 0, (sx * 30, 40), 3)
    for n in range(3):                                                         # spritz, spritz, SPRITZ
        w += se(s["spray"]) + emit_at(FRESH27, 2, 0, (sx * 30, 40)) + emit_at(FRESHC27, 0, 0, (sx * 16, 40 - n * 4))
        w += _hold(FRESH27, 2, 0, (sx * 30, 40), 2 + n)
    w += se(s["bling"]) + emit_at(FRESHB27, 0, 0, (0, 30)) + func(34, 2, 0, 1, rgb(255, 250, 220), 12, 0)
    return w + wait(10)


def _hotfoot(side, s):
    """Blaze Kick (Hotfoot): slides and socks on summer asphalt - the heat shimmering. Hop - ow. Hop - OW. The slide
    catches fire - and they kick it off right into the foe."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    road = (0, 8)
    foot = (sx * 10, 16)
    w = se(s["pop"]) + _hold(HOT27, 1, 0, road, 5)
    for n in range(2):                                                         # hop - ow. hop - OW.
        w += se(s["ember"]) + bmove(side, 258, 2, 0, 8 + n * 4) + _hold(HOT27, 1, 0, road, 2)
        w += bmove(side, 258, 2, 0, -8 - n * 4) + func(34, 2, 0, 1, rgb(255, 90, 60), 9 + n * 2, 0) + _hold(HOT27, 1, 0, road, 3)
    w += se(s["flame"])
    for k in range(5):                                                         # it catches
        w += emit_at(HOT27, 1, 0, road) + emit_at(HOT27, 2, 0, foot) + (emit_at(HOT27, 0, 0, foot) if k == 2 else []) + wait(1)
    w += se(s["whoosh"]) + _lob(HOT27, 2, side, foot, (dx, dy + 20), 5, 18, lambda k: emit_at(HOT27, 1, 0, road))   # KICKED
    w += se(s["kaboom"]) + se(s["burn"]) + flash_screen(4) + emit_at(HOT27, 0, 1, (0, 20)) + emit_at(HOT27, 0, 1, (0, 34))
    w += shake_defender(4, 3) + func(34, 8, 0, 1, rgb(255, 130, 40), 13, 0) + func(48)
    for k in range(6):
        w += emit_at(HOT27, 1, 0, road) + wait(1)
    return w


def _space_jam(side, s):
    """Meteor Mash (Space Jam): a street hoop appears over the foe's head. A twinkle up in the sky. A bigger twinkle.
    Then a basketball on fire comes in from orbit - through the hoop - SWISH - right onto the foe."""
    sx = _sx(side)
    hoop = (0, 62)
    res = _p(side, 1, 2)
    top = (-sx * 70, 150)
    w = se(s["pop"]) + _hold(SPACEB27, 1, 1, hoop, 4)
    for n in range(2):                                                         # *twinkle* ... *TWINKLE*
        w += se(s["bling"]) + emit_at(SPACE27, 0, 1, (top[0] + sx * 20 * n, top[1] - 30 - n * 10))
        w += _hold(SPACEB27, 1, 1, hoop, 6)
    w += func(33, 0, 1, 0, 10, 0) + se(s["mbomb"])
    for k in range(6):                                                         # incoming
        t = (k + 1) / 6
        w += emit_at(SPACE27, res, 1, (round(top[0] * (1 - t)) - sx * 10, round(top[1] + (hoop[1] - 4 - top[1]) * t))) + emit_at(SPACEB27, 1, 1, hoop) + wait(1)
    w += se(s["swipe"]) + emit_at(SPACEB27, 1, 1, (hoop[0], hoop[1] - 3)) + emit_at(SPACE27, res, 1, (-sx * 10, 28)) + wait(1)   # SWISH
    w += se(s["kaboom"]) + se(s["explo"]) + flash_screen(5) + func(68, 5, 5, 1, 10, 0) + emit_at(SPACE27, 3, 1, (0, 22))
    w += shake_defender(5, 3) + func(48)
    for k in range(6):
        w += emit_at(SPACEB27, 1, 1, (hoop[0] + (k % 2) * 2, hoop[1])) + wait(1)
    return w + func(33, 0, 1, 10, 0, 0) + emit_at(SPACE27, 0, 0, (0, 30)) + wait(4)


def _dirty_water(side, s):
    """Muddy Water (Dirty Water): the foe's waiting at the bus stop, a puddle by the curb. A car flies through it -
    SPLASH. Another - SPLASH. Then the bus. Soaked."""
    sx = _sx(side)
    stop = (sx * 30, 16)
    pud = (0, -12)
    lane = -18
    scene = lambda: emit_at(DIRTB27, 1, 1, stop) + emit_at(DIRTB27, 0, 1, pud)
    w = se(s["pop"]) + _hold(DIRTB27, 1, 1, stop, 5, lambda k: emit_at(DIRTB27, 0, 1, pud))
    for n, (res, steps) in enumerate(((1, 5), (1, 5), (2, 7))):                # car... car... THE BUS
        w += se(s["rollout"] if n < 2 else s["whoosh"])
        for k in range(steps):
            x = round(-150 + 300 * (k + 1) / (steps + 1))
            w += emit_at(DIRT27, res, 1, (x, lane + (10 if n == 2 else 0))) + scene()
            if k == steps // 2:
                w += se(s["splash"] if n < 2 else s["surf"]) + emit_at(DIRT27, 3 if n == 2 else 0, 1, (0, 10))
                w += shake_defender(1 + n, 2) + func(34, 8, 0, 1, rgb(140, 110, 60), 10 + n * 2, 0)
            w += wait(1)
        w += _hold(DIRTB27, 1, 1, stop, 4 if n < 2 else 2, lambda k: emit_at(DIRTB27, 0, 1, pud))
    w += func(48) + flash_screen(2)
    return w + _hold(DIRTB27, 1, 1, stop, 6, lambda k: emit_at(DIRTB27, 0, 1, pud))
'''

TABLE = {429: ("_rip_shirt", ("RIP27",), "Memento"),
         430: ("_fresh_fit", ("FRESH27", "FRESHB27", "FRESHC27"), "Refresh"),
         431: ("_hotfoot", ("HOT27",), "Blaze Kick"),
         432: ("_space_jam", ("SPACE27", "SPACEB27"), "Meteor Mash"),
         433: ("_dirty_water", ("DIRT27", "DIRTB27"), "Muddy Water")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
