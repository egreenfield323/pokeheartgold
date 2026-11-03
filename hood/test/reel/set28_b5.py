"""Set 28 batch 5: Flip Script, Cosplay, Guard Swarm, Honey Heal, Edge Up (variants 474-478).
Run once from the repo root: python -X utf8 hood/test/reel/set28_b5.py  (art: set28_b5_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "FLIP28 COS28 COSB28 COP28 HONEY28 HONEYB28 EDGE28".split()

KITS = '''
    # ---- set 28, batch 5 ----------------------------------------------------------------------------------
    # Flip Script (Power Trick): the script reads ATK over DEF - flip - flip - FLIP: DEF over ATK
    b, rs = pk(FLIP28, {1: (fxart.script_page(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.script_page(flipped=True), ONE_TO_ONE, 4, {"colors": 30})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 240, 160), rgb(255, 255, 255), .45, 12, .24, life=14)
    fin(FLIP28, b, rs, (0, 1, 2))

    # Cosplay (Role Play): the costume bag - rip - a cheap rubber mask of the foe - pose - "...REALLY?"
    b, rs = pk(COS28, {1: (fxart.costume_bag(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.cheap_mask(), .6, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(250, 160, 60), n=5, life=16, scl=.3, up=.06)
    fin(COS28, b, rs, (0, 1, 2))
    b, rs = pk(COSB28, {1: (fxart.line_bubble(["...REALLY?"]), ONE_TO_ONE, 4, {"colors": 30})})
    fin(COSB28, b, rs, (1,))

    # Guard Swarm (Defend Order): mall cops on segways roll up - one - two - then a whole ring of them circling
    b, rs = pk(COP28, {1: (fxart.mall_cop(), .7, 4, {}), 2: (flipx(fxart.mall_cop()), .7, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(150, 200, 255), rgb(255, 255, 255), .45, 12, .2, up=.06, life=18, radius=.5)
    fin(COP28, b, rs, (0, 1, 2))

    # Honey Heal (Heal Order): tea - the honey bear - squeeze - squeeze - sip. Ahh.
    b, rs = pk(HONEY28, {1: (fxart.honey_bear(), .6, 4, {}), 2: (fxart.tea_mug(), .6, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(240, 170, 30), rgb(255, 220, 120), .22, 2, .02, gravity=.02, life=12, radius=.05)
    fin(HONEY28, b, rs, (0, 1, 2))
    b, rs = pk(HONEYB28, {}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(140, 255, 160), rgb(255, 255, 255), .45, 14, .18, up=.1, life=24, radius=.6)
    fin(HONEYB28, b, rs, (0,))

    # Edge Up (Sharpen): knife on the steel - shing - shing - SHIIING - glint
    b, rs = pk(EDGE28, {1: (fxart.chef_knife(), .8, 4, {}), 2: (fxart.honing_steel(), .8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 120), rgb(255, 255, 255), .35, 8, .22, up=.06, gravity=.01, life=12)
    fin(EDGE28, b, rs, (0, 1, 2))
'''

SCRIPTS = '''
def _flip_script(side, s):
    """Power Trick (Flip Script): a script page over them - ATK on top, DEF underneath. Flip. Flip back. FLIP - DEF on
    top now, in red. Script flipped."""
    pg = _s23(side, 0, _p(side, (104, 88), (160, 80)))
    w = se(s["pop"]) + _hold(FLIP28, 1, 0, pg, 8)
    for n, res in enumerate((2, 1, 2, 1, 2)):                                 # flip - flip - FLIP
        w += se(s["swipe"]) + _hold(FLIP28, res, 0, pg, 3 if n < 4 else 2)
    w += se(s["bling"]) + emit_at(FLIP28, 0, 0, pg) + func(34, 2, 0, 1, rgb(255, 120, 80), 12, 0)
    return w + _hold(FLIP28, 2, 0, pg, 10)


def _cosplay(side, s):
    """Role Play (Cosplay): a cheap costume bag pops up - rip - out comes a rubber mask of the foe. Mask on. Pose.
    The foe: "...REALLY?"."""
    sx = _sx(side)
    bag = (sx * 30, 30)
    head = (_p(side, 10, 0), _p(side, 30, 40))
    bub = _s23(side, 1, _p(side, (204, 24), (104, 66)))
    w = se(s["pop"]) + _hold(COS28, 1, 0, bag, 8)
    w += se(s["slash"]) + emit_at(COS28, 0, 0, bag) + wait(2)                 # *rip*
    w += se(s["whoosh"]) + _lob(COS28, 2, side, bag, head, 4, 18)
    w += se(s["bling"]) + bmove(side, 258, 2, 0, 8) + _hold(COS28, 2, 0, (head[0], head[1] + 8), 3)   # pose
    w += bmove(side, 258, 2, 0, -8) + _hold(COS28, 2, 0, head, 3)
    for k in range(12):                                                        # "...REALLY?"
        w += emit_at(COS28, 2, 0, head) + emit_at(COSB28, 1, 1, bub) + wait(1)
    return w


def _guard_swarm(side, s):
    """Defend Order (Guard Swarm): a mall cop on a segway rolls up. Another. Then a whole ring of them circling the
    attacker, whistles going. Nobody's getting through."""
    import math
    sx = _sx(side)
    w = se(s["whistle"] if "whistle" in s else s["alarm"])
    for k in range(5):                                                         # one...
        w += emit_at(COP28, 1, 0, (-120 + k * 18, 6)) + wait(1)
    w += _hold(COP28, 1, 0, (-30, 6), 2)
    for k in range(5):                                                         # two...
        w += emit_at(COP28, 1, 0, (-30, 6)) + emit_at(COP28, 2, 0, (120 - k * 18, 10)) + wait(1)
    w += se(s["alarm"]) + func(34, 2, 0, 1, rgb(150, 200, 255), 12, 0)
    for k in range(16):                                                        # the ring
        for j in range(4):
            a = (k / 16 + j / 4) * math.tau
            res = 1 if math.sin(a) < 0 else 2
            w += emit_at(COP28, res, 0, (round(math.cos(a) * 44), round(10 + math.sin(a) * 14)))
        if k % 5 == 0:
            w += emit_at(COP28, 0, 0, (0, 30))
        w += wait(1)
    return w


def _honey_heal(side, s):
    """Heal Order (Honey Heal): a big mug of tea. The honey bear - squeeze, a drizzle. Squeeze. Then a sip... ahhh."""
    sx = _sx(side)
    mug = (sx * 30, 14)
    bear = (sx * 30, 44)
    w = se(s["pop"]) + _hold(HONEY28, 2, 0, mug, 4)
    for n in range(2):                                                         # squeeze... squeeze
        w += se(s["absorb"])
        for k in range(5):
            w += emit_at(HONEY28, 2, 0, mug) + emit_at(HONEY28, 1, 0, (bear[0], bear[1] - (k % 2) * 2))
            w += (emit_at(HONEY28, 0, 0, (bear[0], bear[1] - 10)) if k % 2 == 0 else []) + wait(1)
    w += se(s["rest"]) + _lob(HONEY28, 2, side, mug, (sx * 8, 34), 3, 8)      # sip...
    w += emit_at(HONEYB28, 0, 0, (0, 26)) + func(34, 2, 0, 1, rgb(140, 255, 160), 12, 0)
    return w + _hold(HONEY28, 2, 0, (sx * 8, 34), 10)


def _edge_up(side, s):
    """Sharpen (Edge Up): the knife on the honing steel - shing. Shing. SHIIING - sparks - and a glint off the edge."""
    sx = _sx(side)
    st = (sx * 30, 36)
    w = se(s["pop"]) + _hold(EDGE28, 2, 0, st, 3)
    for n in range(3):                                                         # shing... shing... SHIIING
        w += se(s["slash"])
        for k in range(3):
            w += emit_at(EDGE28, 1, 0, (st[0] - 6 + k * 6, st[1] + 10 - k * 6)) + emit_at(EDGE28, 2, 0, st) + wait(1)
        w += emit_at(EDGE28, 0, 0, (st[0] + 4, st[1])) + emit_at(EDGE28, 2, 0, st) + emit_at(EDGE28, 1, 0, (st[0] + 6, st[1] - 8)) + wait(2 if n < 2 else 1)
    w += se(s["bling"]) + flash_screen(2) + func(34, 2, 0, 1, rgb(255, 120, 80), 12, 0)   # glint
    return w + _hold(EDGE28, 1, 0, (st[0], st[1] + 6), 8)
'''

TABLE = {474: ("_flip_script", ("FLIP28",), "Power Trick"),
         475: ("_cosplay", ("COS28", "COSB28"), "Role Play"),
         476: ("_guard_swarm", ("COP28",), "Defend Order"),
         477: ("_honey_heal", ("HONEY28", "HONEYB28"), "Heal Order"),
         478: ("_edge_up", ("EDGE28",), "Sharpen")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
