"""Set 26 batch 5: Weed Whacker, Whack-a-Mole, Chia Pet, Jet Ski, Back Alley (variants 412-416).
Run once from the repo root: python -X utf8 hood/test/reel/set26_b5.py  (art: set26_b5_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "WEED26 MOLE26 MOLEB26 CHIA26 CHIAB26 SKI26 ALLEY26".split()

KITS = '''
    # ---- set 26, batch 5 ----------------------------------------------------------------------------------
    # Weed Whacker (Leaf Blade): revs - clippings - revs - clippings - then they edge the foe
    b, rs = pk(WEED26, {1: (fxart.string_trimmer(), 1.3, 4, {}), 2: (flipx(fxart.string_trimmer()), 1.3, 4, {})}, alpha=fxart.grass_clip())
    burst(b, rs, 0, rgb(90, 190, 70), rgb(180, 240, 140), .35, 12, .26, up=.14, gravity=.012, life=20, spin=0x0900)
    fin(WEED26, b, rs, (0, 1, 2))

    # Whack-a-Mole (Hammer Arm): a mole pops up - WHACK, missed. Another - missed. Then the FOE pops up. WHACK.
    b, rs = pk(MOLE26, {1: (fxart.mole_hole(), .8, 4, {}), 2: (fxart.arcade_mole(), .8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .5, 10, .26, life=10)
    fin(MOLE26, b, rs, (0, 1, 2))
    b, rs = pk(MOLEB26, {1: (fxart.foam_mallet(), .9, 4, {}), 2: (flipx(fxart.foam_mallet()), .9, 4, {})})
    fin(MOLEB26, b, rs, (1, 2))

    # Chia Pet (Seed Bomb): mist - sprouts on the foe's head - mist - fuzz - mist - a full chia afro - it bursts
    b, rs = pk(CHIA26, {1: (fxart.chia_fuzz(), .7, 4, {}), 2: (fxart.chia_fuzz(stage=1), .7, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(150, 210, 255), rgb(240, 250, 255), .3, 6, .06, gravity=.016, life=14)
    fin(CHIA26, b, rs, (0, 1, 2))
    b, rs = pk(CHIAB26, {1: (fxart.chia_fuzz(stage=2), .9, 4, {}), 2: (fxart.spray_bottle(), .5, 4, {})}, alpha=fxart.grass_clip())
    burst(b, rs, 0, rgb(90, 190, 70), rgb(180, 240, 140), .4, 22, .32, up=.18, gravity=.01, life=26, spin=0x0900)
    fin(CHIAB26, b, rs, (0, 1, 2))

    # Jet Ski (Aqua Jet): rev - rev - ZOOM across into the foe
    b, rs = pk(SKI26, {1: (fxart.jet_ski(), 1.2, 4, {}), 2: (flipx(fxart.jet_ski()), 1.2, 4, {})}, alpha=fxart.water_jet())
    burst(b, rs, 0, rgb(150, 210, 255), rgb(240, 250, 255), .35, 6, .14, up=.16, gravity=.02, life=16)
    burst(b, rs, 3, rgb(120, 190, 255), rgb(230, 245, 255), .5, 16, .26, up=.3, gravity=.02, life=22)
    fin(SKI26, b, rs, (0, 1, 2, 3))

    # Back Alley (Shadow Sneak): footsteps behind the foe - they turn - footsteps - they turn - hit from behind
    b, rs = pk(ALLEY26, {}, alpha=fxart.shoe_print())
    prop(b, rs, 0, tex=0, clr=rgb(40, 30, 50), clr_anm=(rgb(40, 30, 50), rgb(40, 30, 50)), scl=.75, life=40, alpha=(28, 28, 0))
    burst(b, rs, 1, rgb(60, 40, 80), rgb(120, 90, 150), .45, 12, .2, up=.06, life=20)
    fin(ALLEY26, b, rs, (0, 1))
'''

SCRIPTS = '''
def _weed_whacker(side, s):
    """Leaf Blade (Weed Whacker): rev - clippings fly. Rev - more clippings. Then they swing round and edge the foe."""
    sx = _sx(side)
    tr = _p(side, (sx * 28, 24), (-28, 14))
    res = _p(side, 1, 2)
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = se(s["pop"]) + _hold(WEED26, res, 0, tr, 2)
    for n in range(2):                                                         # rev... rev...
        w += se(s["rollout"])
        for k in range(4):
            w += emit_at(WEED26, res, 0, (tr[0] + (k % 2), tr[1])) + (emit_at(WEED26, 0, 0, (tr[0] + sx * 18, tr[1] - 16)) if k % 2 == 0 else []) + wait(1)
        w += wait(2)
    w += se(s["whoosh"]) + _lob(WEED26, res, side, tr, (dx - sx * 18, dy + 10), 4, 10)   # *EDGES*
    w += se(s["rollout"]) + se(s["slash"])
    for k in range(8):
        w += emit_at(WEED26, res, 1, (-sx * 18 + (k % 2) * 3, 10))
        if k % 2 == 0:
            w += emit_at(WEED26, 0, 1, (0, 14)) + shake_defender(1 + (k == 6) * 2, 1)
        w += wait(1)
    w += flash_screen(3) + func(48)
    return w + _lob(WEED26, res, side, (dx - sx * 18, dy + 10), tr, 4, 10)


def _whack_a_mole(side, s):
    """Hammer Arm (Whack-a-Mole): a mole pops out of a hole - WHACK - gone, missed. It pops out another hole - WHACK -
    missed. Then the foe pops up. WHACK."""
    sx = _sx(side)
    holes = [_s23(side, 0, (108, 84)), _s23(side, 0, (146, 64))]
    mres = _p(side, 1, 2)
    hs = lambda: [w_ for h in holes for w_ in emit_at(MOLE26, 1, 0, h)]
    w = se(s["pop"]) + _hold(MOLE26, 1, 0, holes[0], 3, lambda k: emit_at(MOLE26, 1, 0, holes[1]))
    for n, h in enumerate(holes):                                              # *pop* - WHACK - missed
        mole = (h[0], h[1] + 12)
        for k in range(3):
            w += emit_at(MOLE26, 2, 0, (mole[0], mole[1] - 10 + k * 5)) + hs() + wait(1)
        w += emit_at(MOLE26, 2, 0, mole) + hs() + wait(1)
        w += emit_at(MOLEB26, mres, 0, (mole[0] - sx * 6, mole[1] + 26)) + hs() + wait(1)
        w += se(s["bonk"]) + emit_at(MOLEB26, mres, 0, (mole[0] - sx * 6, mole[1] + 10)) + emit_at(MOLE26, 0, 0, (h[0], h[1] + 4)) + hs() + wait(1)
        w += _hold(MOLE26, 1, 0, holes[0], 3, lambda k: emit_at(MOLE26, 1, 0, holes[1]) + (se(s["disable"]) if k == 0 else []))
    w += bmove(side, 264, 2, 0, 10) + se(s["pop"]) + _hold(MOLE26, 1, 0, holes[0], 2, lambda k: emit_at(MOLE26, 1, 0, holes[1]))   # *the foe pops up*
    w += emit_at(MOLEB26, mres, 1, (-sx * 6, 54)) + hs() + wait(1)
    w += se(s["bslam"]) + se(s["bonk"]) + flash_screen(4) + emit_at(MOLEB26, mres, 1, (-sx * 6, 38)) + emit_at(MOLE26, 0, 1, (0, 30))   # WHACK
    w += bmove(side, 264, 2, 0, -10) + shake_defender(4, 3) + func(48) + hs() + wait(1)
    return w + _hold(MOLE26, 1, 0, holes[0], 4, lambda k: emit_at(MOLE26, 1, 0, holes[1]))


def _chia_pet(side, s):
    """Seed Bomb (Chia Pet): a spray bottle mists the foe's head - sprouts. Mist - fuzz. Mist - a full chia afro. Then
    it bursts."""
    sx = _sx(side)
    head = (0, 40)
    sp = (-sx * 18, 44)
    w = []
    for n, (kit, res) in enumerate(((CHIA26, 1), (CHIA26, 2), (CHIAB26, 1))):  # *spritz*... grow
        for k in range(3):
            w += emit_at(CHIAB26, 2, 1, (sp[0] + (k % 2) * 2, sp[1])) + (se(s["spray"]) if k == 0 else []) + (emit_at(CHIA26, 0, 1, (head[0], head[1] + 8)) if k == 1 else [])
            if n:                                                              # the last stage stays up while it's misted
                w += emit_at(CHIA26, n, 1, head)
            w += wait(1)
        w += se(s["lseed"]) + _hold(kit, res, 1, (head[0], head[1] - (8 if n == 2 else 0)), 5)
    w += se(s["kaboom"]) + flash_screen(4) + emit_at(CHIAB26, 0, 1, (0, 46)) + shake_defender(4, 3) + func(48)   # *POP*
    return w + func(34, 8, 0, 1, rgb(120, 220, 90), 11, 0) + wait(8)


def _jet_ski(side, s):
    """Aqua Jet (Jet Ski): on a jet ski - rev, spray - rev, spray - then it rips across and rams the foe."""
    sx = _sx(side)
    res = _p(side, 1, 2)
    ys = _p(side, (118, 78), (94, 116))
    xs = _p(side, (66, 172), (186, 70))
    at = lambda x: _s23(side, 0, (x, round(ys[0] + (ys[1] - ys[0]) * (x - xs[0]) / (xs[1] - xs[0]))))
    w = se(s["whoosh"]) + func(40, 2, 1) + _hold(SKI26, res, 0, at(xs[0]), 2)
    for n in range(2):                                                         # rev... rev...
        w += se(s["rollout"])
        for k in range(4):
            w += emit_at(SKI26, res, 0, (at(xs[0])[0], at(xs[0])[1] + (k % 2) * 2)) + (emit_at(SKI26, 0, 0, (at(xs[0])[0] - sx * 26, at(xs[0])[1] - 6)) if k % 2 == 0 else []) + wait(1)
    w += se(s["jet"]) + se(s["surf"])
    for k in range(5):                                                         # ZOOM
        x = round(xs[0] + (xs[1] - xs[0]) * ((k + 1) / 5) ** 1.3)
        w += emit_at(SKI26, res, 0, at(x)) + emit_at(SKI26, 0, 0, (at(x)[0] - sx * 30, at(x)[1] - 6)) + wait(1)
    w += se(s["splash"]) + se(s["bslam"]) + flash_screen(3) + emit_at(SKI26, 3, 1, (0, 14)) + shake_defender(4, 3) + func(48)
    w += _hold(SKI26, res, 0, at(xs[1]), 3) + func(40, 2, 0)
    return w + wait(3)


def _back_alley(side, s):
    """Shadow Sneak (Back Alley): footsteps behind the foe - step, step - they spin round: nothing. Step, step - they
    spin round: nothing. Then the hit comes from behind."""
    sx = _sx(side)
    w = func(40, 2, 1) + wait(2)
    for n in range(2):                                                         # step... step... *turns*
        for k in range(2):
            w += se(s["swipe"]) + emit_at(ALLEY26, 0, 1, (sx * (22 + k * 8 - n * 4), -16 + k * 4)) + wait(4)
        w += bmove(side, 264, 2, sx * 10, 0) + se(s["leer"]) + wait(5) + bmove(side, 264, 2, -sx * 10, 0) + wait(3)
    w += se(s["shadow"]) + wait(2)                                              # *from behind*
    w += se(s["kaboom"]) + flash_screen(4) + shake_defender(4, 3) + bmove(side, 264, 3, -sx * 16, 0)
    w += wait(4) + bmove(side, 264, 3, sx * 16, 0) + func(40, 2, 0)
    return w + wait(3)
'''

TABLE = {412: ("_weed_whacker", ("WEED26",), "Leaf Blade"),
         413: ("_whack_a_mole", ("MOLE26", "MOLEB26"), "Hammer Arm"),
         414: ("_chia_pet", ("CHIA26", "CHIAB26"), "Seed Bomb"),
         415: ("_jet_ski", ("SKI26",), "Aqua Jet"),
         416: ("_back_alley", ("ALLEY26",), "Shadow Sneak")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
