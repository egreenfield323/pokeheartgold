"""Set 28 batch 1 (INSANE): High Beams, Fog Machine, Order Up, Sag Check, Last Wish (variants 454-458).
Run once from the repo root: python -X utf8 hood/test/reel/set28_b1.py  (art: set28_b1_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "BEAM28 BEAMB28 FOG28 FOGB28 ORDER28 ORDERB28 ORDERC28 SAG28 SAGB28 WISH28 WISHB28".split()

KITS = '''
    # ---- set 28, batch 1 (INSANE) -------------------------------------------------------------------------
    # High Beams (Luster Purge): headlights in the dark - blink - blink - FULL BRIGHTS. "CUT YOUR BRIGHTS!"
    b, rs = pk(BEAM28, {1: (fxart.headlights(), 1.0, 4, {}), 2: (fxart.headlights(on=False), 1.0, 4, {})}, alpha=fxart.brights_cone())
    prop(b, rs, 0, tex=0, clr=rgb(255, 250, 210), clr_anm=(rgb(255, 250, 210), rgb(255, 250, 210)), scl=1.1, life=4, alpha=(24, 24, 0))
    fin(BEAM28, b, rs, (0, 1, 2))
    b, rs = pk(BEAMB28, {1: (fxart.line_bubble(["CUT YOUR", "BRIGHTS!"]), ONE_TO_ONE, 4, {"colors": 30})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 230), rgb(255, 255, 255), .6, 20, .36, life=18, radius=.6)
    fin(BEAMB28, b, rs, (0, 1))

    # Fog Machine (Mist Ball): the club fogger - pfft - pfft - then it floods the screen, lasers cutting through
    b, rs = pk(FOG28, {1: (fxart.club_fogger(), .9, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(220, 220, 235), n=4, life=26, scl=.4, up=.03)
    fin(FOG28, b, rs, (0, 1))
    b, rs = pk(FOGB28, {}, alpha=fxart.laser_line())
    prop(b, rs, 0, tex=0, clr=rgb(80, 255, 120), clr_anm=(rgb(80, 255, 120), rgb(80, 255, 120)), scl=1.6, life=4)
    prop(b, rs, 1, tex=0, clr=rgb(255, 60, 90), clr_anm=(rgb(255, 60, 90), rgb(255, 60, 90)), scl=1.6, life=4)
    fin(FOGB28, b, rs, (0, 1))

    # Order Up (Attack Order): ORDER PLACED - one rider - two - then every delivery driver in the city - DELIVERED
    b, rs = pk(ORDER28, {1: (fxart.order_phone(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.order_phone(done=True), ONE_TO_ONE, 4, {"colors": 30})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .55, 14, .3, life=12)
    fin(ORDER28, b, rs, (0, 1, 2))
    b, rs = pk(ORDERB28, {1: (fxart.delivery_rider(), .8, 4, {}), 2: (fxart.delivery_rider(tint=1), .8, 4, {})})
    fin(ORDERB28, b, rs, (1, 2))
    b, rs = pk(ORDERC28, {1: (flipx(fxart.delivery_rider(tint=2)), .8, 4, {}), 2: (flipx(fxart.delivery_rider()), .8, 4, {})})
    fin(ORDERC28, b, rs, (1, 2))

    # Sag Check (Gravity): jeans on both of them - sag - SAG - round the knees - then everything sinks
    b, rs = pk(SAG28, {1: (fxart.sag_jeans(), .8, 4, {}), 2: (fxart.sag_jeans(stage=1), .8, 4, {})})
    fin(SAG28, b, rs, (1, 2))
    b, rs = pk(SAGB28, {1: (fxart.sag_jeans(stage=2), .8, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(170, 160, 140), n=5, life=16, scl=.3, up=.03)
    fin(SAGB28, b, rs, (0, 1))

    # Last Wish (Healing Wish): night - a dandelion - make a wish - blow - BLOW - they float off with the seeds
    b, rs = pk(WISH28, {1: (fxart.dandelion(), 1.3, 4, {}), 2: (fxart.dandelion(stage=1), 1.3, 4, {})}, alpha=fxart.dandelion_seed())
    burst(b, rs, 0, rgb(250, 250, 255), rgb(255, 255, 255), .32, 10, .12, up=.08, gravity=-.004, life=40, radius=.4)
    fin(WISH28, b, rs, (0, 1, 2))
    b, rs = pk(WISHB28, {1: (fxart.dandelion(stage=2), 1.3, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(140, 255, 160), rgb(255, 255, 255), .45, 16, .2, up=.1, life=26, radius=.6)
    fin(WISHB28, b, rs, (0, 1))
'''

SCRIPTS = '''
def _high_beams(side, s):
    """Luster Purge (High Beams): pitch dark - a pair of headlights. Blink. Blink. Then FULL BRIGHTS straight in the
    foe's face - the screen whites out - "CUT YOUR BRIGHTS!"."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    hl = (sx * 36, 22)
    bub = _s23(side, 1, _p(side, (204, 24), (104, 66)))
    w = func(33, 0, 1, 0, 14, 0) + se(s["pop"]) + _hold(BEAM28, 2, 0, hl, 4)
    for n in range(2):                                                         # blink... blink...
        w += se(s["lockon"]) + _hold(BEAM28, 1, 0, hl, 2) + _hold(BEAM28, 2, 0, hl, 3)
    w += se(s["sbeam"]) + se(s["kaboom"]) + flash_screen(6) + func(68, 6, 6, 1, 12, 0)   # FULL BRIGHTS
    for k in range(12):
        w += emit_at(BEAM28, 1, 0, hl)
        for t in (.3, .55, .8):
            w += emit_at(BEAM28, 0, 0, (round(hl[0] + (dx - hl[0]) * t), round(hl[1] + (dy + 24 - hl[1]) * t)))
        if k % 4 == 0:
            w += func(34, 8, 0, 1, rgb(255, 255, 230), 15, 0) + emit_at(BEAMB28, 0, 1, (0, 24))
        if k == 6:
            w += se(s["thunder"]) + flash_screen(3)
        w += wait(1)
    w += se(s["leer"]) + func(33, 0, 1, 14, 4, 0)
    for k in range(12):                                                        # "CUT YOUR BRIGHTS!"
        w += emit_at(BEAMB28, 1, 1, bub) + (emit_at(BEAM28, 2, 0, hl) if k < 6 else []) + wait(1)
    return w + func(48) + func(33, 0, 1, 4, 0, 0) + wait(2)


def _fog_machine(side, s):
    """Mist Ball (Fog Machine): the club fogger - pfft. Pfft. Then it floods the whole screen, lasers cutting through
    the fog - the foe can't see a thing."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    fog = (sx * 36, 24)
    w = se(s["pop"]) + _hold(FOG28, 1, 0, fog, 4)
    for n in range(2):                                                         # pfft... pfft...
        w += se(s["smoke"]) + emit_at(FOG28, 0, 0, (fog[0] + sx * 20, fog[1] + 6)) + _hold(FOG28, 1, 0, fog, 6)
    w += func(33, 0, 1, 0, 14, 0) + se(s["haze"]) + se(s["mbomb"])             # FLOOD
    for k in range(18):
        w += emit_at(FOG28, 1, 0, fog)
        t = (k % 6 + 1) / 6
        w += emit_at(FOG28, 0, 0, (round(fog[0] + (dx - fog[0]) * t), round(fog[1] + (dy + 10 - fog[1]) * t + (k % 3) * 8)))
        if k % 3 == 0:                                                         # strobes
            w += func(34, 8, 0, 1, rgb(80, 255, 120) if k % 6 == 0 else rgb(255, 60, 90), 12, 0)
        if k % 6 == 3:
            w += flash_screen(2) + func(34, 8, 0, 1, rgb(160, 160, 180), 13, 0)
        if k == 9:
            w += se(s["kaboom"]) + shake_defender(4, 3)
        w += wait(1)
    return w + func(48) + func(33, 0, 1, 14, 0, 0) + wait(3)


def _order_up(side, s):
    """Attack Order (Order Up): a phone - ORDER PLACED. One delivery rider pulls up into the foe. Two more. Then every
    delivery driver in the city swarms them at once. DELIVERED."""
    sx = _sx(side)
    ph = _s23(side, 0, _p(side, (112, 76), (160, 84)))
    w = se(s["bling"]) + _hold(ORDER28, 1, 0, ph, 10)
    left = lambda r, x, y=6: emit_at(ORDERB28, r, 1, (x, y))
    right = lambda r, x, y=6: emit_at(ORDERC28, r, 1, (x, y))
    w += se(s["rollout"])
    for k in range(5):                                                         # one rider...
        w += left(1, -130 + k * 24) + wait(1)
    w += se(s["bonk"]) + emit_at(ORDER28, 0, 1, (0, 20)) + wait(3)
    w += se(s["rollout"])
    for k in range(5):                                                         # two more...
        w += left(2, -130 + k * 24, 0) + right(1, 130 - k * 24, 12) + wait(1)
    w += se(s["bonk"]) + emit_at(ORDER28, 0, 1, (0, 20)) + wait(3)
    w += func(33, 0, 1, 0, 12, 0) + se(s["alarm"]) + se(s["rollout2"])        # THE WHOLE CITY
    for k in range(16):
        p = (k % 4 + 1) / 4
        w += left(1 + k % 2, round(-130 + 110 * p), 2 + (k * 5) % 24) + right(1 + (k + 1) % 2, round(130 - 110 * p), (k * 7) % 28)
        if k % 2 == 0:
            w += left(2 - k % 2, round(-150 + 120 * p), 30 - (k * 3) % 16)
        if k % 4 == 3:
            w += se(s["bslam"]) + emit_at(ORDER28, 0, 1, (0, 20))
        if k == 8:
            w += func(68, 5, 5, 1, 10, 0) + flash_screen(3)
        w += wait(1)
    w += se(s["kaboom"]) + flash_screen(4) + shake_defender(4, 3) + func(48) + func(33, 0, 1, 12, 0, 0)
    return w + se(s["bling"]) + _hold(ORDER28, 2, 0, ph, 10)


def _sag_check(side, s):
    """Gravity (Sag Check): jeans on both of them. They sag - boxers out. They SAG - round the knees. Then gravity
    really kicks in: everybody sinks."""
    sx = _sx(side)
    a_j = (sx * 6, _p(side, 2, -14))
    d_j = (0, _p(side, -14, 2))
    both = lambda kit, r, sink=0: emit_at(kit, r, 0, (a_j[0], a_j[1] - sink)) + emit_at(kit, r, 1, (d_j[0], d_j[1] - sink))
    w = se(s["pop"])
    for k in range(5):
        w += both(SAG28, 1) + wait(1)
    for n, (kit, r) in enumerate(((SAG28, 2), (SAGB28, 1))):                   # sag... SAG
        w += se(s["swipe"] if n == 0 else s["flop"])
        for k in range(7):
            w += both(kit, r) + wait(1)
    w += func(33, 0, 1, 0, 12, 0) + se(s["epower"]) + se(s["kaboom"]) + flash_screen(4)   # GRAVITY
    w += bmove(side, 258, 6, 0, -12) + bmove(side, 264, 6, 0, -12)
    for k in range(10):
        sink = min(12, 2 * (k + 1))
        w += both(SAGB28, 1, sink) + (emit_at(SAGB28, 0, 1, (0, -6)) if k % 3 == 0 else []) + wait(1)
    w += bmove(side, 258, 4, 0, 12) + bmove(side, 264, 4, 0, 12)
    for k in range(4):
        w += both(SAGB28, 1, 12 - 3 * (k + 1)) + wait(1)
    w += wait(1) + func(68, 5, 5, 1, 10, 0) + func(48) + func(33, 0, 1, 12, 0, 0)   # the quake after everyone's back
    return w + wait(4)


def _last_wish(side, s):
    """Healing Wish (Last Wish): night falls. A dandelion. They make a wish - blow, half the seeds go - BLOW - and
    they float up and away with the seeds. Whoever's next gets the wish."""
    sx = _sx(side)
    dd = (sx * 36, 34)
    w = func(33, 0, 1, 0, 14, 0) + se(s["pop"]) + _hold(WISH28, 1, 0, dd, 6)
    w += se(s["bling"]) + emit_at(WISHB28, 0, 0, (dd[0], dd[1] + 22)) + _hold(WISH28, 1, 0, dd, 6)   # make a wish
    w += se(s["gust"]) + emit_at(WISH28, 0, 0, dd) + _hold(WISH28, 2, 0, dd, 8)                      # blow
    w += se(s["gust"]) + se(s["sscent"])                                                               # BLOW
    for k in range(6):
        w += emit_at(WISHB28, 1, 0, dd) + (emit_at(WISH28, 0, 0, (dd[0] - sx * k * 4, dd[1] + k * 3)) if k % 2 == 0 else []) + wait(1)
    w += se(s["whoosh"]) + bmove(side, 258, 10, 0, 40) + func(34, 2, 0, 1, rgb(255, 255, 255), 14, 0)   # floating away
    for k in range(12):
        w += emit_at(WISHB28, 1, 0, dd) + (emit_at(WISH28, 0, 0, (0, 20 + k * 3)) if k % 2 == 0 else []) + wait(1)
    w += func(40, 2, 1) + wait(6) + bmove(side, 258, 2, 0, -40) + wait(2) + func(40, 2, 0)
    w += se(s["rest"]) + emit_at(WISHB28, 0, 0, (0, 26))
    return w + func(33, 0, 1, 14, 0, 0) + wait(8)
'''

TABLE = {454: ("_high_beams", ("BEAM28", "BEAMB28"), "Luster Purge"),
         455: ("_fog_machine", ("FOG28", "FOGB28"), "Mist Ball"),
         456: ("_order_up", ("ORDER28", "ORDERB28", "ORDERC28"), "Attack Order"),
         457: ("_sag_check", ("SAG28", "SAGB28"), "Gravity"),
         458: ("_last_wish", ("WISH28", "WISHB28"), "Healing Wish")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
