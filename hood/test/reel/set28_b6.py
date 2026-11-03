"""Set 28 batch 6: Blend In, Night Vision, Paranoia, Fresh Scent, Mood Swap (variants 479-483).
Run once from the repo root: python -X utf8 hood/test/reel/set28_b6.py  (art: set28_b6_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "VIS28 VISB28 NV28 THINK28 THINKB28 TREE28 TREEB28 MOOD28".split()

KITS = '''
    # ---- set 28, batch 6 ----------------------------------------------------------------------------------
    # Blend In (Camouflage): hi-vis vest on, a clipboard - they walk right up past the foe - "YOU GOOD."
    b, rs = pk(VIS28, {1: (fxart.hivis_vest(), .7, 4, {}), 2: (fxart.work_clipboard(), .5, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(220, 255, 80), rgb(255, 255, 255), .4, 10, .18, life=14)
    fin(VIS28, b, rs, (0, 1, 2))
    b, rs = pk(VISB28, {1: (fxart.line_bubble(["YOU GOOD."]), ONE_TO_ONE, 4, {"colors": 30})})
    fin(VISB28, b, rs, (1,))

    # Night Vision (Miracle Eye): the goggles flip down - click - everything goes green - nowhere to hide
    b, rs = pk(NV28, {1: (fxart.nv_goggles(), .6, 4, {})}, alpha=fxart.air_ring())
    burst(b, rs, 0, rgb(80, 255, 110), rgb(220, 255, 220), .7, 4, .14, life=16, radius=.2)
    fin(NV28, b, rs, (0, 1))

    # Paranoia (Worry Seed): 3 a.m. thoughts piling up over the foe - DID I LOCK IT? - DID THEY SEE THAT? - 3:00 AM
    b, rs = pk(THINK28, {1: (fxart.thought_cloud(lines=("DID I", "LOCK IT?")), ONE_TO_ONE, 4, {"colors": 30}),
                         2: (fxart.thought_cloud(lines=("DID THEY", "SEE THAT?")), ONE_TO_ONE, 4, {"colors": 30})})
    fin(THINK28, b, rs, (1, 2))
    b, rs = pk(THINKB28, {1: (fxart.thought_cloud(lines=("3:00 AM",)), ONE_TO_ONE, 4, {"colors": 30})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(200, 210, 255), rgb(255, 255, 255), .4, 6, .14, life=14)
    fin(THINKB28, b, rs, (0, 1))

    # Fresh Scent (Aromatherapy): stink lines - a pine tree freshener - another - a whole forest of them. Fresh.
    b, rs = pk(TREE28, {1: (fxart.freshener_tree(), .5, 4, {}), 2: (fxart.freshener_tree(col=1), .5, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(150, 190, 60), n=3, life=16, scl=.24, up=.06)
    fin(TREE28, b, rs, (0, 1, 2))
    b, rs = pk(TREEB28, {1: (fxart.freshener_tree(col=2), .5, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(140, 255, 160), rgb(255, 255, 255), .45, 14, .18, up=.08, life=22, radius=.6)
    fin(TREEB28, b, rs, (0, 1))

    # Mood Swap (Heart Swap): a red mood ring over them, a blue one over the foe - they swap
    b, rs = pk(MOOD28, {1: (fxart.mood_ring(), .6, 4, {}), 2: (fxart.mood_ring(col=1), .6, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(220, 160, 255), rgb(255, 255, 255), .4, 10, .2, life=14)
    fin(MOOD28, b, rs, (0, 1, 2))
'''

SCRIPTS = '''
def _blend_in(side, s):
    """Camouflage (Blend In): a hi-vis vest drops on, a clipboard in hand - they walk right up past the foe like they
    belong there. The foe just nods: "YOU GOOD." Walk back. Never questioned."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    vest = (0, _p(side, 16, 22))
    clip = (sx * 22, 24)
    walk = (round(dx * .45), round(dy * .45))
    gear = lambda o=(0, 0): emit_at(VIS28, 1, 0, (vest[0] + o[0], vest[1] + o[1])) + emit_at(VIS28, 2, 0, (clip[0] + o[0], clip[1] + o[1]))
    w = []
    for k in range(4):                                                         # vest drops on
        w += emit_at(VIS28, 1, 0, (vest[0], vest[1] + 30 - k * 10)) + wait(1)
    w += se(s["pop"]) + emit_at(VIS28, 0, 0, vest)
    for k in range(5):
        w += gear() + wait(1)
    w += se(s["swipe"]) + bmove(side, 258, 8, walk[0], walk[1])               # walks right up
    for k in range(5):
        w += gear(_lerp((0, 0), walk, (k + 1) / 5)) + wait(1)
    bub = _s23(side, 1, _p(side, (204, 24), (104, 66)))
    for k in range(12):                                                        # "YOU GOOD."
        w += gear(walk) + emit_at(VISB28, 1, 1, bub) + (bmove(side, 264, 2, 0, -3) if k == 3 else []) + (bmove(side, 264, 2, 0, 3) if k == 6 else []) + wait(1)
    w += bmove(side, 258, 6, -walk[0], -walk[1])
    for k in range(4):
        w += gear(_lerp(walk, (0, 0), (k + 1) / 4)) + wait(1)
    return w + func(34, 2, 0, 1, rgb(220, 255, 80), 11, 0) + _hold(VIS28, 1, 0, vest, 4)


def _night_vision(side, s):
    """Miracle Eye (Night Vision): the goggles flip down over their eyes - click - the whole screen goes dark and green.
    Beep... beep... the foe lights up bright. Nowhere to hide."""
    head = (_p(side, 10, 0), _p(side, 28, 36))
    w = []
    for k in range(3):                                                         # flip down
        w += emit_at(NV28, 1, 0, (head[0], head[1] + 16 - k * 8)) + wait(1)
    w += se(s["lockon"]) + func(33, 0, 1, 0, 15, 0)
    w += func(34, 2, 0, 1, rgb(80, 255, 110), 14, 0)
    for k in range(18):                                                        # beep... beep...
        w += emit_at(NV28, 1, 0, head)
        if k % 6 == 0:
            w += se(s["lockon2"] if "lockon2" in s else s["lockon"]) + emit_at(NV28, 0, 1, (0, 24))
        if k == 12:
            w += se(s["bling"]) + func(34, 8, 0, 1, rgb(220, 255, 220), 15, 0) + flash_screen(2)
        w += wait(1)
    return w + func(33, 0, 1, 15, 0, 0) + _hold(NV28, 1, 0, head, 3)


def _paranoia(side, s):
    """Worry Seed (Paranoia): 3 a.m. Thought clouds start popping up over the foe: DID I LOCK IT? ... DID THEY SEE
    THAT? ... 3:00 AM. The foe's wide awake and twitching. No sleep tonight."""
    spots = [_s23(side, 1, p) for p in _p(side, ((182, 32), (124, 66)), ((104, 70), (152, 58)))]
    w = func(33, 0, 1, 0, 10, 0)
    shown = []
    for n, (kit, res) in enumerate(((THINK28, 1), (THINK28, 2), (THINKB28, 1))):
        w += se(s["pop"] if n < 2 else s["alarm"])
        sp = spots[n % 2]
        for k in range(10 if n < 2 else 12):
            w += emit_at(kit, res, 1, sp) + (shake_defender(1 + n, 1) if k == 3 else []) + wait(1)
    w += se(s["leer"]) + func(34, 8, 0, 1, rgb(220, 220, 255), 12, 0) + emit_at(THINKB28, 0, 1, (0, 30))
    return w + func(33, 0, 1, 10, 0, 0) + wait(4)


def _fresh_scent(side, s):
    """Aromatherapy (Fresh Scent): stink lines coming off them. A pine-tree air freshener pops up - sniff. Another. Then
    a whole forest of them dangling all round. Fresh."""
    sx = _sx(side)
    trees = [((sx * 30, 52), TREE28, 1), ((-sx * 26, 46), TREE28, 2), ((sx * 12, 66), TREEB28, 1), ((-sx * 8, 60), TREE28, 1),
             ((sx * 40, 34), TREE28, 2), ((-sx * 36, 30), TREEB28, 1)]
    up = []
    hang = lambda: [w_ for i in up for w_ in emit_at(trees[i][1], trees[i][2], 0, trees[i][0])]
    w = []
    for k in range(6):                                                         # stinky
        w += (emit_at(TREE28, 0, 0, (0, 24)) if k % 2 == 0 else []) + wait(1)
    for n, group in enumerate(([0], [1], [2, 3, 4, 5])):                       # one... two... a forest
        up += group
        w += se(s["pop"] if n < 2 else s["bling"])
        for k in range(6):
            w += hang() + (emit_at(TREE28, 0, 0, (0, 24)) if n < 2 and k == 2 else []) + wait(1)
    w += se(s["sscent"]) + emit_at(TREEB28, 0, 0, (0, 26)) + func(34, 2, 0, 1, rgb(140, 255, 160), 12, 0)
    for k in range(8):
        w += hang() + wait(1)
    return w


def _mood_swap(side, s):
    """Heart Swap (Mood Swap): a mood ring floats over each of them - red over the attacker, blue over the foe. They
    swap places. Now the attacker's chill and the foe's heated."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    a, b = (0, _p(side, 64, 54)), (dx, dy + 46)
    both = lambda pa, pb: emit_at(MOOD28, 1, 0, pa) + emit_at(MOOD28, 2, 0, pb)
    w = se(s["pop"]) + func(34, 2, 0, 1, rgb(255, 90, 90), 10, 0) + func(34, 8, 0, 1, rgb(90, 140, 255), 10, 0)
    for k in range(8):
        w += both(a, b) + wait(1)
    w += se(s["psych"]) + se(s["whoosh"])
    for k in range(6):                                                         # they swap
        t = (k + 1) / 6
        h = round(24 * 4 * t * (1 - t))
        pa, pb = _lerp(a, b, t), _lerp(b, a, t)
        w += both((pa[0], pa[1] + h), (pb[0], pb[1] - h)) + wait(1)
    w += se(s["bling"]) + emit_at(MOOD28, 0, 0, a) + emit_at(MOOD28, 0, 1, (0, 46))
    w += func(34, 2, 0, 1, rgb(90, 140, 255), 12, 0) + func(34, 8, 0, 1, rgb(255, 90, 90), 12, 0)
    for k in range(10):
        w += both(b, a) + wait(1)
    return w
'''

TABLE = {479: ("_blend_in", ("VIS28", "VISB28"), "Camouflage"),
         480: ("_night_vision", ("NV28",), "Miracle Eye"),
         481: ("_paranoia", ("THINK28", "THINKB28"), "Worry Seed"),
         482: ("_fresh_scent", ("TREE28", "TREEB28"), "Aromatherapy"),
         483: ("_mood_swap", ("MOOD28",), "Heart Swap")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
