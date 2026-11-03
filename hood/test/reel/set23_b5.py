"""Set 23 batch 5: Clothesline, Bullhorn, Hype Man, Ring Ya Bell, Heat Check (variants 319-323).
Run once from the repo root: python -X utf8 hood/test/reel/set23_b5.py  (art: set23_b5_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "LINE23 LINEB23 HORN23 HORNB23 HYPE23 HYPEB23 DING23 DINGB23 THERMO23 THERMOB23".split()

KITS = '''
    # ---- set 23, batch 5 ----------------------------------------------------------------------------------
    # Clothesline (Cross Chop): the line goes up - a tee gets hung - the drawers get hung - the foe gets fed up,
    # charges - and gets CLOTHESLINED.
    b, rs = pk(LINE23, {1: (fxart.clothesline_rig(), 1.6, 4, {}), 2: (fxart.white_tee(), .5, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .5, 10, .26, life=12)
    fin(LINE23, b, rs, (0, 1, 2))
    b, rs = pk(LINEB23, {1: (fxart.line_boxers(), .5, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 60), rgb(255, 255, 220), .4, 7, .08, up=.02, life=24, radius=.5)
    fin(LINEB23, b, rs, (0, 1))

    # Bullhorn (Megahorn): "IS THIS ON?" - tap tap - SKREEEE - tap tap - SKREEEE - forget it, they ram the foe with it
    b, rs = pk(HORN23, {1: (fxart.bullhorn(), .7, 4, {}), 2: (flipx(fxart.bullhorn()), .7, 4, {})}, alpha=fxart.feedback_squiggle())
    burst(b, rs, 0, rgb(255, 240, 120), rgb(255, 255, 255), .45, 6, .16, life=12)
    fin(HORN23, b, rs, (0, 1, 2))
    b, rs = pk(HORNB23, {1: (fxart.line_bubble(["IS THIS ON?"]), ONE_TO_ONE, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .55, 12, .3, life=10)
    fin(HORNB23, b, rs, (0, 1))

    # Hype Man (Hyper Voice): YEAH! - WHAT! - OKAAAY!! and the foe gets blown back
    b, rs = pk(HYPE23, {1: (fxart.hype_bubble("YEAH!"), ONE_TO_ONE, 4, {}), 2: (fxart.hype_bubble("WHAT!", scale=2), ONE_TO_ONE, 4, {})},
               alpha=fxart.shout_arc())
    burst(b, rs, 0, rgb(255, 255, 255), rgb(255, 255, 255), .45, 5, .14, life=12)
    fin(HYPE23, b, rs, (0, 1, 2))
    b, rs = pk(HYPEB23, {2: (fxart.burst_sign(["OKAAAY!!"], fill=(220, 40, 40, 255), text=(255, 255, 255, 255)), SIGN_SCALE, 4, {"colors": 30})},
               alpha=fxart.shout_arc())
    spray2(b, rs, {"player": (10, 40), "enemy": (-10, 30)}, (0, 24), 10, clr=rgb(255, 255, 255),
           clr_anm=(rgb(255, 255, 255), rgb(255, 220, 120)), scl=.9, gen=2, gen_intvl=2, emtr_life=16, radius=.1,
           spread=.01, alpha=(31, 28, 0))
    fin(HYPEB23, b, rs, (0, 1, 2))

    # Ring Ya Bell (Dizzy Punch): ding-dong ditch - ring and run - ring and run - third time the foe's waiting, so
    # they ring the FOE's bell. Birds.
    b, rs = pk(DING23, {1: (fxart.doorbell_plate(), .7, 4, {}), 2: (fxart.line_bubble(["DING", "DONG!"]), ONE_TO_ONE, 4, {})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 180), rgb(255, 255, 255), .35, 6, .12, life=10)
    fin(DING23, b, rs, (0, 1, 2))
    b, rs = pk(DINGB23, {1: (fxart.dizzy_bird(), .38, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .6, 12, .3, life=10)
    fin(DINGB23, b, rs, (0, 1))

    # Heat Check (Heat Wave): the thermostat - 72 - click, 85 - click, 99 - the heat rolls over the foe - and from
    # off-screen: WHO TOUCHED MY THERMOSTAT
    b, rs = pk(THERMO23, {1: (fxart.thermostat(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.thermostat(temp="85"), ONE_TO_ONE, 4, {"colors": 30})},
               alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(150, 210, 255), rgb(240, 250, 255), .3, 5, .12, up=.1, gravity=.014, life=16)
    burst(b, rs, 3, rgb(150, 210, 255), rgb(240, 250, 255), .35, 14, .2, up=.12, gravity=.014, life=18)
    fin(THERMO23, b, rs, (0, 1, 2, 3))
    b, rs = pk(THERMOB23, {2: (fxart.thermostat(temp="99"), ONE_TO_ONE, 4, {"colors": 30}),
                           3: (fxart.line_bubble(["WHO TOUCHED", "MY", "THERMOSTAT"]), ONE_TO_ONE, 4, {})}, alpha=fxart.heat_shimmer())
    spray2(b, rs, {"player": (40, 50), "enemy": (-40, 20)}, (0, 20), 14, clr=rgb(255, 120, 30),
           clr_anm=(rgb(255, 230, 120), rgb(240, 60, 20)), scl=.7, gen=3, gen_intvl=1, emtr_life=24, radius=.4,
           spread=.02, alpha=(30, 26, 0))
    fin(THERMOB23, b, rs, (0, 1, 2, 3))
'''

SCRIPTS = '''
def _clothesline(side, s):
    """Cross Chop (Clothesline): a clothesline goes up between them. A white tee gets hung. A pair of heart
    drawers gets hung. The foe's had enough, charges - and runs neck-first into the line. Flipped."""
    sx = _sx(side)
    rig = _s23(side, 0, (124, 58))
    tee = _s23(side, 0, (106, 70))
    box = _s23(side, 0, (140, 70))
    charge = _p(side, (-42, -14), (40, 66))
    hung = []
    dress = lambda: emit_at(LINE23, 1, 0, rig) + ([w_ for w_ in emit_at(LINE23, 2, 0, tee)] if "tee" in hung else []) + \\
        ([w_ for w_ in emit_at(LINEB23, 1, 0, box)] if "box" in hung else [])
    w = se(s["pop"]) + _hold(LINE23, 1, 0, rig, 4)
    for name, kit, at in (("tee", LINE23, tee), ("box", LINEB23, box)):        # hang it... hang it...
        w += se(s["whoosh"]) + _lob(kit, 2 if kit == LINE23 else 1, side, (sx * 16, 30), at, 5, 20, lambda k: dress())
        hung.append(name)
        w += se(s["pop"]) + dress() + wait(1)
        w += _hold(LINE23, 1, 0, rig, 4, lambda k: dress())
    w += bmove(side, 264, 2, 0, 4) + shake_defender(1, 2) + _hold(LINE23, 1, 0, rig, 3, lambda k: dress())   # *...bro*
    w += bmove(side, 264, 2, 0, -4) + se(s["rage"]) + func(34, 8, 0, 1, rgb(255, 80, 60), 9, 0)
    w += _hold(LINE23, 1, 0, rig, 2, lambda k: dress())
    w += se(s["whoosh"]) + bmove(side, 264, 3, *charge) + dress() + wait(1) + dress() + wait(1)   # *charges*
    w += se(s["bslam"]) + se(s["chop"]) + flash_screen(4) + emit_at(LINE23, 0, 1, (0, 30))        # CLOTHESLINED
    w += bmove(side, 264, 3, -charge[0], -charge[1] + 26) + shake_defender(3, 3)
    hung.clear()
    a = _arc(tee, (tee[0] - 60, tee[1] + 50), 6, 20)
    b_ = _arc(box, (box[0] + 50, box[1] + 60), 6, 24)
    for k in range(1, 6):
        w += emit_at(LINE23, 1, 0, rig) + emit_at(LINE23, 2, 0, a[k]) + emit_at(LINEB23, 1, 0, b_[k]) + wait(1)
    w += bmove(side, 264, 4, 0, -26) + func(48) + emit_at(LINEB23, 0, 1, (0, 36))
    return w + _hold(LINE23, 1, 0, rig, 6, lambda k: se(s["confuse"]) if k == 0 else [])


def _bullhorn(side, s):
    """Megahorn (Bullhorn): a police bullhorn. "IS THIS ON?" - tap tap - SKREEEE feedback. Tap tap - SKREEEEE.
    Forget it: they ram the foe WITH the bullhorn."""
    sx = _sx(side)
    horn = _p(side, (sx * 26, 26), (-30, 14))
    res = _p(side, 1, 2)
    bub = _p(side, (sx * 50, 58), (-40, 30))
    mouth = (horn[0] + sx * 18, horn[1] + 4)
    h = lambda d=0: emit_at(HORN23, res, 0, (horn[0] + d, horn[1]))
    w = se(s["pop"]) + _hold(HORN23, res, 0, horn, 3)
    for n in range(2):                                                         # tap tap... SKREEEE
        for k in range(2):
            w += se(s["lockon"]) + h(sx * 2) + wait(1) + h() + wait(1)
        w += _hold(HORNB23, 1, 0, bub, 6, lambda k: h()) if n == 0 else _hold(HORN23, res, 0, horn, 2)
        w += se(s["alarm"]) + (se(s["alarm"]) if n else [])
        for k in range(5 + 2 * n):
            w += h((k % 2) * 2) + (emit_at(HORN23, 0, 0, mouth) if k % 2 == 0 else []) + wait(1)
        w += shake_defender(1 + n, 2) + (shake_attacker(2, 2) if n else []) + _hold(HORN23, res, 0, horn, 4)
    w += _hold(HORN23, res, 0, horn, 3)                                        # *looks at it*... forget it
    w += bmove(side, 258, 3, sx * 30, 14) + h() + wait(1)                       # RAM
    w += se(s["bslam"]) + se(s["horn"]) + flash_screen(4) + emit_at(HORNB23, 0, 1, (-sx * 8, 22))
    w += shake_defender(4, 3) + func(48) + func(68, 4, 4, 1, 3, 0) + _hold(HORN23, res, 0, horn, 2)
    w += bmove(side, 258, 4, -sx * 30, -14)
    return w + _hold(HORN23, res, 0, horn, 4)


def _hype_man(side, s):
    """Hyper Voice (Hype Man): "YEAH!" - "WHAT!" (louder) - "OKAAAY!!" - and the sound blows the foe back."""
    sx = _sx(side)
    bub = _p(side, (sx * 50, 58), (-40, 30))
    mouth = _p(side, (sx * 12, 34), (-12, 26))
    w = []
    for n, (res, ticks) in enumerate(((1, 7), (2, 8))):                       # YEAH!... WHAT!
        w += se(s["rage"]) + bmove(side, 258, 2, 0, 6 + 2 * n)
        for k in range(ticks):
            w += emit_at(HYPE23, res, 0, bub)
            if k == 1:
                w += bmove(side, 258, 2, 0, -6 - 2 * n) + emit_at(HYPE23, 0, 0, mouth)
            if k == 3 and n == 1:
                w += shake_defender(1, 2)
            w += wait(1)
        w += wait(2)
    sign = _p(side, (0, 58), (0, 50))
    w += se(s["rage"]) + se(s["bdrum"]) + bmove(side, 258, 2, 0, 10) + flash_screen(2)   # OKAAAY!!
    w += emit_at(HYPEB23, _p(side, 0, 1), 0, mouth)
    for k in range(13):
        w += emit_at(HYPEB23, 2, 0, sign)
        if k == 1:
            w += bmove(side, 258, 2, 0, -10)
        if k == 4:
            w += se(s["bslam"]) + shake_defender(4, 3) + func(48) + bmove(side, 264, 3, sx * 12, 4)
        if k == 10:
            w += bmove(side, 264, 3, -sx * 12, -4)
        w += wait(1)
    return w + wait(2)


def _ring_ya_bell(side, s):
    """Dizzy Punch (Ring Ya Bell): ding-dong ditch. A doorbell by the foe: DING DONG - the attacker bolts. The foe
    looks around. DING DONG - bolts again. Third time the foe's waiting right there - so they ring the FOE's
    bell instead. Little birds circle their head."""
    sx = _sx(side)
    plate = _p(side, (-79, -5), (46, 40))
    bub = _p(side, (-28, 36), (plate[0] + 4, plate[1] + 40))
    run = _p(side, (-40, -10), (40, 10))
    p = lambda: emit_at(DING23, 1, 1, plate)
    w = se(s["pop"]) + _hold(DING23, 1, 1, plate, 3)
    for n in range(2):                                                         # DING DONG - *runs*
        w += se(s["lockon"]) + emit_at(DING23, 0, 1, plate) + se(s["bling"])
        w += _hold(DING23, 2, 1, bub, 3, lambda k: p() + (se(s["bling"]) if k == 1 else []))
        w += se(s["whoosh"]) + bmove(side, 258, 3, *run) + _hold(DING23, 2, 1, bub, 3, lambda k: p())
        w += bmove(side, 264, 2, -6, 0) + _hold(DING23, 1, 1, plate, 2)       # *looks round*
        w += bmove(side, 264, 3, 12, 0) + _hold(DING23, 1, 1, plate, 2)
        w += bmove(side, 264, 2, -6, 0) + (shake_defender(1, 2) if n else [])
        w += bmove(side, 258, 3, -run[0], -run[1]) + _hold(DING23, 1, 1, plate, 3)
    w += bmove(side, 264, 2, -sx * 10, -4) + _hold(DING23, 1, 1, plate, 4)     # *the foe's waiting*
    w += bmove(side, 258, 2, sx * 22, 8) + se(s["bling"]) + se(s["kaboom"]) + flash_screen(4)   # DING DONG
    w += emit_at(DINGB23, 0, 1, (0, 30)) + shake_defender(4, 3) + func(48)
    w += bmove(side, 258, 4, -sx * 22, -8) + bmove(side, 264, 3, sx * 10, 4) + se(s["confuse"])
    import math as _m
    for k in range(14):                                                        # tweet tweet
        for j in range(3):
            a = k * .55 + j * 2.1
            w += emit_at(DINGB23, 1, 1, (round(22 * _m.cos(a)), 40 + round(6 * _m.sin(a))))
        w += p() + wait(1)
    return w


def _heat_check(side, s):
    """Heat Wave (Heat Check): the thermostat says 72. Click - 85, the foe starts sweating. Click - 99, red - a
    wall of heat rolls over the foe. Then Dad, from off-screen: WHO TOUCHED MY THERMOSTAT."""
    sx = _sx(side)
    th = _s23(side, 0, (106, 80))
    dad = _s23(side, 0, (40, 76))
    w = se(s["pop"]) + _hold(THERMO23, 1, 0, th, 5)
    w += bmove(side, 258, 2, sx * 8, 6) + se(s["lockon"]) + wait(1) + bmove(side, 258, 2, -sx * 8, -6)   # click - 85
    w += _hold(THERMO23, 2, 0, th, 4) + emit_at(THERMO23, 0, 1, (0, 30)) + shake_defender(1, 1)
    w += _hold(THERMO23, 2, 0, th, 5)
    w += bmove(side, 258, 2, sx * 8, 6) + se(s["lockon"]) + wait(1) + bmove(side, 258, 2, -sx * 8, -6)   # click - 99
    w += se(s["flame"]) + func(33, 0, 1, 0, 8, rgb(255, 120, 40))
    w += emit_at(THERMOB23, _p(side, 0, 1), 0, (th[0], th[1]))
    for k in range(16):                                                        # *the heat*
        w += emit_at(THERMOB23, 2, 0, th)
        if k == 4:
            w += emit_at(THERMO23, 3, 1, (0, 30)) + func(34, 8, 0, 1, rgb(255, 70, 40), 13, 0) + shake_defender(2, 3)
        if k == 10:
            w += se(s["ember"]) + emit_at(THERMO23, 0, 1, (0, 34))
        w += wait(1)
    w += func(33, 0, 1, 8, 0, rgb(255, 120, 40)) + func(48)
    for k in range(13):                                                        # WHO TOUCHED MY THERMOSTAT
        w += emit_at(THERMOB23, 2, 0, th) + emit_at(THERMOB23, 3, 0, dad)
        if k == 2:
            w += se(s["leer"]) + shake_attacker(2, 2)
        w += wait(1)
    return w + wait(2)
'''

TABLE = {319: ("_clothesline", ("LINE23", "LINEB23"), "Cross Chop"),
         320: ("_bullhorn", ("HORN23", "HORNB23"), "Megahorn"),
         321: ("_hype_man", ("HYPE23", "HYPEB23"), "Hyper Voice"),
         322: ("_ring_ya_bell", ("DING23", "DINGB23"), "Dizzy Punch"),
         323: ("_heat_check", ("THERMO23", "THERMOB23"), "Heat Wave")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
