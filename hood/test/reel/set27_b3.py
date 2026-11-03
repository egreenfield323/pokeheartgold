"""Set 27 batch 3: Cut Off, Time Out, Swap Bags, Yap Session, Moonwalk (variants 434-438).
Run once from the repo root: python -X utf8 hood/test/reel/set27_b3.py  (art: set27_b3_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "CUT27 CUTB27 TIME27 TIMEB27 SWAP27 SWAPB27 YAP27 YAPB27 YAPC27 MOON27 MOONB27".split()

KITS = '''
    # ---- set 27, batch 3 ----------------------------------------------------------------------------------
    # Cut Off (Heal Block): the foe leans for the drink - it slides away - again - "CUT OFF."
    b, rs = pk(CUT27, {1: (fxart.bar_top(), 1.6, 4, {}), 2: (fxart.liquor_glass(), .5, 4, {})})
    fin(CUT27, b, rs, (1, 2))
    b, rs = pk(CUTB27, {1: (fxart.line_bubble(["CUT OFF."]), ONE_TO_ONE, 4, {"colors": 30})})
    fin(CUTB27, b, rs, (1,))

    # Time Out (Punishment): the dunce cap - the egg timer ticks - BRRRING
    b, rs = pk(TIME27, {1: (fxart.dunce_cap(), .7, 4, {"colors": 30}), 2: (fxart.egg_timer(), .45, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .5, 10, .26, life=10)
    fin(TIME27, b, rs, (0, 1, 2))
    b, rs = pk(TIMEB27, {1: (fxart.egg_timer(ring=True), .45, 4, {})})
    fin(TIMEB27, b, rs, (1,))

    # Swap Bags (Switcheroo): two red duffels - swap - swap - open: they've got the cash, the foe's got the laundry
    b, rs = pk(SWAP27, {1: (fxart.gym_duffel(), .8, 4, {}), 2: (fxart.gym_duffel(open_="cash"), .8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 160), rgb(255, 255, 255), .45, 10, .2, up=.06, life=16)
    fin(SWAP27, b, rs, (0, 1, 2))
    b, rs = pk(SWAPB27, {1: (fxart.gym_duffel(open_="laundry"), .8, 4, {})})
    fin(SWAPB27, b, rs, (1,))

    # Yap Session (Chatter): AND THEN - GIRL... - ANYWAY SO LIKE - bubbles piling up till the foe's head spins
    b, rs = pk(YAP27, {1: (fxart.line_bubble(["AND THEN"]), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.line_bubble(["GIRL..."]), ONE_TO_ONE, 4, {"colors": 30})})
    fin(YAP27, b, rs, (1, 2))
    b, rs = pk(YAPB27, {1: (fxart.line_bubble(["ANYWAY", "SO LIKE"]), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.line_bubble(["LISTEN."]), ONE_TO_ONE, 4, {"colors": 30})})
    fin(YAPB27, b, rs, (1, 2))
    b, rs = pk(YAPC27, {1: (fxart.line_bubble(["WAIT WAIT"]), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.line_bubble(["NO BUT"]), ONE_TO_ONE, 4, {"colors": 30})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 240, 120), rgb(255, 255, 255), .4, 5, .12, life=16, radius=.4)
    fin(YAPC27, b, rs, (0, 1, 2))

    # Moonwalk (Lunar Dance): fedora on - the dance floor lights up under every step - backwards - and gone
    b, rs = pk(MOON27, {1: (fxart.lightup_tile(), .8, 4, {}), 2: (fxart.lightup_tile(lit=True), .8, 4, {})})
    fin(MOON27, b, rs, (1, 2))
    b, rs = pk(MOONB27, {1: (fxart.black_fedora(), .5, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 220), rgb(255, 255, 255), .45, 10, .2, up=.06, life=18)
    fin(MOONB27, b, rs, (0, 1))
'''

SCRIPTS = '''
def _cut_off(side, s):
    """Heal Block (Cut Off): the foe at the bar, a drink right there. They lean for it - it slides away. Lean - slides
    away. Then the bartender: "CUT OFF." Sad foe."""
    sx = _sx(side)
    bar = (0, 2)
    glass = [(-sx * 18, 16), (-sx * 40, 16), (-sx * 64, 16)]
    w = se(s["pop"]) + _hold(CUT27, 1, 1, bar, 4, lambda k: emit_at(CUT27, 2, 1, glass[0]))
    for n in range(2):                                                         # lean... *sliiide*
        w += bmove(side, 264, 3, -sx * 8, 0) + _hold(CUT27, 1, 1, bar, 2, lambda k: emit_at(CUT27, 2, 1, glass[n]))
        w += se(s["swipe"])
        for k in range(3):
            w += emit_at(CUT27, 1, 1, bar) + emit_at(CUT27, 2, 1, _lerp(glass[n], glass[n + 1], (k + 1) / 3)) + wait(1)
        w += bmove(side, 264, 3, sx * 8, 0) + _hold(CUT27, 1, 1, bar, 3, lambda k: emit_at(CUT27, 2, 1, glass[n + 1]))
    w += se(s["bonk"])
    for k in range(12):                                                        # "CUT OFF."
        w += emit_at(CUTB27, 1, 1, (-sx * 6, 58)) + emit_at(CUT27, 1, 1, bar) + emit_at(CUT27, 2, 1, glass[2])
        if k == 4:
            w += se(s["disable"]) + func(34, 8, 0, 1, rgb(90, 90, 120), 12, 0) + bmove(side, 264, 3, 0, -6)
        w += wait(1)
    return w + bmove(side, 264, 3, 0, 6) + wait(2)


def _time_out(side, s):
    """Punishment (Time Out): a dunce cap drops on the foe's head - bonk. The egg timer goes down - tick... tock... the
    foe fidgets... BRRRING - time's up, and it hits."""
    sx = _sx(side)
    cap = (0, 46)
    tmr = (sx * 30, 10)
    scene = lambda: emit_at(TIME27, 1, 1, cap)
    w = []
    for k in range(4):                                                         # the cap drops
        w += emit_at(TIME27, 1, 1, (0, 100 - k * 18)) + wait(1)
    w += se(s["bonk"]) + shake_defender(1, 2) + _hold(TIME27, 1, 1, cap, 3, lambda k: emit_at(TIME27, 2, 1, tmr))
    for k in range(16):                                                        # tick... tock...
        w += scene() + emit_at(TIME27, 2, 1, tmr)
        if k % 4 == 0:
            w += se(s["clock"])
        if k == 8:
            w += bmove(side, 264, 2, sx * 5, 0)
        if k == 10:
            w += bmove(side, 264, 2, -sx * 5, 0)
        w += wait(1)
    w += se(s["alarm"])
    for k in range(6):                                                         # BRRRING
        w += scene() + emit_at(TIMEB27, 1, 1, (tmr[0] + (k % 2) * 2, tmr[1])) + wait(1)
    w += se(s["bslam"]) + flash_screen(4) + emit_at(TIME27, 0, 1, (0, 24)) + shake_defender(4, 3) + func(48)
    return w + _hold(TIME27, 1, 1, cap, 6, lambda k: emit_at(TIMEB27, 1, 1, tmr))


def _swap_bags(side, s):
    """Switcheroo (Swap Bags): a red duffel by each of them. Swap - swap - SWAP, too fast to follow. They unzip theirs:
    stacked with cash. The foe unzips theirs: dirty laundry. Stink lines."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    a, b = (sx * 34, 20), (dx - sx * 30, dy + 4)
    both = lambda pa, pb: emit_at(SWAP27, 1, 0, pa) + emit_at(SWAP27, 1, 0, pb)
    w = se(s["pop"]) + _hold(SWAP27, 1, 0, a, 5, lambda k: emit_at(SWAP27, 1, 0, b))
    for n, steps in enumerate((5, 4, 3)):                                      # swap... swap... SWAP
        w += se(s["whoosh"])
        for k in range(steps):
            t = (k + 1) / steps
            h = round(30 * 4 * t * (1 - t))
            pa, pb = _lerp(a, b, t), _lerp(b, a, t)
            w += both((pa[0], pa[1] + h), (pb[0], pb[1] - h)) + wait(1)
        a, b = b, a
        w += both(a, b) + wait(1)
    w += se(s["bling"]) + emit_at(SWAP27, 0, 0, (sx * 30, 20))                 # cash...
    w += _hold(SWAP27, 2, 0, (sx * 34, 20), 5, lambda k: emit_at(SWAP27, 1, 0, (dx - sx * 30, dy + 4)))
    w += se(s["smog"]) + shake_defender(2, 2) + func(34, 8, 0, 1, rgb(150, 190, 70), 12, 0)   # ...laundry
    return w + _hold(SWAP27, 2, 0, (sx * 34, 20), 12, lambda k: emit_at(SWAPB27, 1, 0, (dx - sx * 30, dy + 4)))


def _yap_session(side, s):
    """Chatter (Yap Session): "AND THEN" - "GIRL..." - "ANYWAY SO LIKE" - then it just doesn't stop: bubbles on top of
    bubbles till the foe's head is spinning."""
    spots = [_s23(side, 0, p) for p in ((80, 64), (150, 60), (112, 86))]
    lines = [(YAP27, 1), (YAP27, 2), (YAPB27, 1), (YAPC27, 1), (YAPB27, 2), (YAPC27, 2)]
    w = []
    up = []
    for n in range(3):                                                         # AND THEN... GIRL... ANYWAY SO LIKE
        up.append(n)
        w += se(s["sface"] if n % 2 else s["pop"])
        for k in range(6):
            for i in up:
                w += emit_at(lines[i][0], lines[i][1], 0, spots[i])
            w += wait(1)
    w += se(s["chatter"] if "chatter" in s else s["swagger"])
    for k in range(16):                                                        # it doesn't stop
        for j in range(3):
            kit, res = lines[(k // 2 + j * 2) % 6]
            w += emit_at(kit, res, 0, spots[j])
        if k % 4 == 0:
            w += se(s["pop"]) + emit_at(YAPC27, 0, 1, (0, 40))
        if k in (4, 10):
            w += bmove(side, 264, 2, 6, 0)
        if k in (7, 13):
            w += bmove(side, 264, 2, -6, 0)
        w += wait(1)
    w += se(s["confuse"]) + func(34, 8, 0, 1, rgb(250, 200, 80), 11, 0)
    for k in range(8):
        w += (emit_at(YAPC27, 0, 1, (0, 40)) if k % 3 == 0 else []) + wait(1)
    return w


def _moonwalk(side, s):
    """Lunar Dance (Moonwalk): spotlight - fedora on. They moonwalk backwards and the dance floor lights up under every
    step. Hat tip - *hee-hee* - and they moonwalk right off the screen."""
    sx = _sx(side)
    hy = _p(side, 30, 40)
    hat = lambda x: emit_at(MOONB27, 1, 0, (x + _p(side, 10, 0), hy))
    ty = _p(side, 4, -12)
    tiles = [-sx * 12 * k for k in range(5)]
    floor = lambda lit: [w_ for i, x in enumerate(tiles) for w_ in emit_at(MOON27, 2 if i in lit else 1, 0, (x, ty))]
    w = func(33, 0, 1, 0, 12, 0) + se(s["pop"]) + _hold(MOONB27, 1, 0, (_p(side, 10, 0), hy), 4, lambda k: floor(()))
    for n in range(1, 5):                                                      # step back - tile lights - step back
        w += bmove(side, 258, 2, -sx * 12, 0) + se(s["swipe"] if n % 2 else s["peck"])
        for k in range(3):
            w += hat(tiles[n]) + floor((n,) if k < 2 else (n - 1, n)) + wait(1)
    w += se(s["bling"]) + emit_at(MOONB27, 0, 0, (tiles[4], hy + 4))               # hat tip - hee-hee
    for k in range(6):
        w += hat(tiles[4]) if k not in (2, 3) else emit_at(MOONB27, 1, 0, (tiles[4] + _p(side, 10, 0), hy + 8))
        w += floor((4,)) + wait(1)
    w += se(s["whoosh"]) + bmove(side, 258, 6, -sx * 90, 0)                    # ...and gone
    for k in range(5):
        w += hat(tiles[4] - sx * 18 * (k + 1)) + floor(()) + wait(1)
    w += func(33, 0, 1, 12, 0, 0) + wait(4) + bmove(side, 258, 4, sx * 138, 0)
    return w + wait(2)
'''

TABLE = {434: ("_cut_off", ("CUT27", "CUTB27"), "Heal Block"),
         435: ("_time_out", ("TIME27", "TIMEB27"), "Punishment"),
         436: ("_swap_bags", ("SWAP27", "SWAPB27"), "Switcheroo"),
         437: ("_yap_session", ("YAP27", "YAPB27", "YAPC27"), "Chatter"),
         438: ("_moonwalk", ("MOON27", "MOONB27"), "Lunar Dance")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
