"""Set 28 batch 3: Tag In, Bounce Back, Hold Grudge, Tickle Fight, Galaxy Rag (variants 464-468).
Run once from the repo root: python -X utf8 hood/test/reel/set28_b3.py  (art: set28_b3_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "TAG28 TAGB28 BOUNCE28 GRUDGE28 GRUDGEB28 TICKLE28 TICKLEB28 GAL28".split()

KITS = '''
    # ---- set 28, batch 3 ----------------------------------------------------------------------------------
    # Tag In (Assist): the ring corner - TAG - the luchador partner off the top rope, flying elbow
    b, rs = pk(TAG28, {1: (fxart.ring_corner(), 1.1, 4, {}), 2: (flipx(fxart.ring_corner()), 1.1, 4, {})})
    fin(TAG28, b, rs, (1, 2))
    b, rs = pk(TAGB28, {1: (fxart.luchador(), .9, 4, {}), 2: (flipx(fxart.luchador()), .9, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .55, 14, .3, life=12)
    fin(TAGB28, b, rs, (0, 1, 2))

    # Bounce Back (Magic Coat): a bouncy castle - boing, boing - the foe's glob bounces right off it, back at them
    b, rs = pk(BOUNCE28, {1: (fxart.bouncy_castle(), 1.3, 4, {})}, alpha=fxart.soft_puff())
    prop(b, rs, 0, tex=0, clr=rgb(160, 80, 220), clr_anm=(rgb(160, 80, 220), rgb(160, 80, 220)), scl=.45, life=4)
    burst(b, rs, 2, rgb(200, 140, 255), rgb(255, 230, 255), .35, 10, .24, life=14)
    fin(BOUNCE28, b, rs, (0, 1, 2))

    # Hold Grudge (Grudge): the foe's photo on the dartboard - thunk - thunk - BULLSEYE
    b, rs = pk(GRUDGE28, {1: (fxart.grudge_dartboard(), 1.0, 4, {}), 2: (fxart.throw_dart(), .45, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 240, 160), rgb(255, 255, 255), .45, 10, .24, life=12)
    fin(GRUDGE28, b, rs, (0, 1, 2))
    b, rs = pk(GRUDGEB28, {1: (flipx(fxart.throw_dart()), .45, 4, {})})
    fin(GRUDGEB28, b, rs, (1,))

    # Tickle Fight (Tickle): the feather duster - tickle tickle - the foe cracks - HAHAHA
    b, rs = pk(TICKLE28, {1: (fxart.feather_duster(), .8, 4, {}), 2: (flipx(fxart.feather_duster()), .8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 180, 220), rgb(255, 255, 255), .4, 6, .16, up=.06, life=14)
    fin(TICKLE28, b, rs, (0, 1, 2))
    b, rs = pk(TICKLEB28, {1: (fxart.line_bubble(["HAHAHA"]), ONE_TO_ONE, 4, {"colors": 30})})
    fin(TICKLEB28, b, rs, (1,))

    # Galaxy Rag (Cosmic Power): the galaxy durag goes on - the stars come off it and swirl round them
    b, rs = pk(GAL28, {1: (fxart.galaxy_durag(), .6, 4, {}), 2: (flipx(fxart.galaxy_durag()), .6, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 230), rgb(255, 255, 255), .4, 3, .06, life=16, radius=.2)
    burst(b, rs, 3, rgb(200, 150, 255), rgb(255, 255, 255), .55, 20, .3, up=.06, life=22, radius=.6)
    fin(GAL28, b, rs, (0, 1, 2, 3))
'''

SCRIPTS = '''
def _tag_in(side, s):
    """Assist (Tag In): a ring corner appears behind them. *TAG* - the luchador partner climbs the turnbuckle... and
    comes off the top rope with a flying elbow on the foe."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    corner = (-sx * 34, 22)
    ck = _p(side, 1, 2)
    lres = _p(side, 1, 2)
    top = (corner[0], corner[1] + 40)
    scene = lambda: emit_at(TAG28, ck, 0, corner)
    w = se(s["pop"]) + _hold(TAG28, ck, 0, corner, 5)
    w += se(s["dslap"]) + emit_at(TAGB28, 0, 0, (corner[0] + sx * 10, 30)) + _hold(TAG28, ck, 0, corner, 3)   # *TAG*
    for k in range(4):                                                         # up the turnbuckle
        w += scene() + emit_at(TAGB28, lres, 0, (corner[0], corner[1] + 10 + k * 10)) + wait(1)
    w += se(s["whoosh"]) + _hold(TAG28, ck, 0, corner, 2, lambda k: emit_at(TAGB28, lres, 0, top))
    w += _lob(TAGB28, lres, side, top, (dx - sx * 8, dy + 30), 6, 30, lambda k: scene())   # FLYING ELBOW
    w += se(s["kaboom"]) + se(s["bslam"]) + flash_screen(4) + emit_at(TAGB28, 0, 1, (0, 24)) + shake_defender(4, 3)
    w += _hold(TAGB28, lres, 1, (-sx * 8, 26), 4) + func(48)
    return w + _hold(TAG28, ck, 0, corner, 3)


def _bounce_back(side, s):
    """Magic Coat (Bounce Back): a bouncy castle pops up round them - boing - boing. The foe lobs a nasty glob at
    it... it bounces right off, back into the foe."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    cas = (0, _p(side, 14, 4))
    hit = (sx * 24, 34)
    foe = (dx, dy + 24)
    w = se(s["pop"]) + _hold(BOUNCE28, 1, 0, cas, 4)
    for n in range(2):                                                         # boing... boing
        w += se(s["flop"]) + bmove(side, 258, 3, 0, 14) + _hold(BOUNCE28, 1, 0, cas, 3)
        w += bmove(side, 258, 3, 0, -14) + _hold(BOUNCE28, 1, 0, cas, 3)
    w += se(s["sludge"])
    for k in range(5):                                                         # the foe's glob...
        w += emit_at(BOUNCE28, 1, 0, cas) + emit_at(BOUNCE28, 0, 0, _lerp(foe, hit, (k + 1) / 5)) + wait(1)
    w += se(s["flop"]) + emit_at(BOUNCE28, 2, 0, hit)                         # *BOING*
    for k in range(5):                                                         # ...right back
        p = _lerp(hit, foe, (k + 1) / 5)
        w += emit_at(BOUNCE28, 1, 0, cas) + emit_at(BOUNCE28, 0, 0, (p[0], p[1] + round(20 * (1 - abs(k - 2) / 2.5)))) + wait(1)
    w += se(s["splat"]) + emit_at(BOUNCE28, 2, 1, (0, 24)) + func(48) + shake_defender(3, 2) + func(34, 8, 0, 1, rgb(160, 80, 220), 12, 0)
    return w + _hold(BOUNCE28, 1, 0, cas, 5) + wait(8)


def _hold_grudge(side, s):
    """Grudge (Hold Grudge): a dartboard with the foe's photo pinned on it, X'd out. Thunk - outer ring. Thunk -
    closer. Then BULLSEYE, right through the photo - and the foe feels it."""
    sx = _sx(side)
    board = _s23(side, 0, _p(side, (128, 66), (128, 70)))
    dkit = _p(side, GRUDGE28, GRUDGEB28)
    dres = _p(side, 2, 1)
    start = (sx * 20, 34)
    stuck = []
    scene = lambda: emit_at(GRUDGE28, 1, 0, board) + [w_ for p in stuck for w_ in emit_at(dkit, dres, 0, p)]
    w = se(s["pop"]) + _hold(GRUDGE28, 1, 0, board, 6)
    for n, off in enumerate(((sx * -6, 18), (sx * -6, -12), (sx * -12, 2))):  # thunk... thunk... BULLSEYE
        tgt = (board[0] + off[0], board[1] + off[1])
        w += se(s["whoosh"])
        for k in range(4):
            w += scene() + emit_at(dkit, dres, 0, _lerp(start, tgt, (k + 1) / 4)) + wait(1)
        stuck.append(tgt)
        w += se(s["peck"] if n < 2 else s["bslam"]) + emit_at(GRUDGE28, 0, 0, tgt)
        for k in range(5 if n < 2 else 2):
            w += scene() + wait(1)
    w += se(s["curse"]) + flash_screen(3) + func(48) + shake_defender(3, 3) + func(34, 8, 0, 1, rgb(90, 40, 110), 13, 0)
    for k in range(8):
        w += scene() + wait(1)
    return w + wait(8)


def _tickle_fight(side, s):
    """Tickle (Tickle Fight): a feather duster - tickle, the foe flinches. Tickle tickle - they're trying not to laugh.
    Then the full tickle attack - "HAHAHA" - totally defenseless."""
    sx = _sx(side)
    res = _p(side, 1, 2)
    bub = _s23(side, 1, _p(side, (204, 24), (104, 66)))
    w = []
    for n, reps in enumerate((3, 5, 8)):                                       # tickle... tickle tickle... TICKLE
        w += se(s["swipe"])
        for k in range(reps):
            w += emit_at(TICKLE28, res, 1, (-sx * (24 - (k % 2) * 6), 14 + (k % 3) * 6))
            if k % 2 == 0:
                w += emit_at(TICKLE28, 0, 1, (-sx * 10, 22)) + shake_defender(1 + n, 1)
            w += wait(1)
        w += wait(2)
    w += se(s["swagger"]) + func(34, 8, 0, 1, rgb(255, 170, 200), 12, 0)
    for k in range(12):                                                        # HAHAHA
        w += emit_at(TICKLEB28, 1, 1, bub) + (func(48) + shake_defender(2, 1) if k % 4 == 0 else []) + wait(1)
    return w + wait(4) + wait(8)


def _galaxy_rag(side, s):
    """Cosmic Power (Galaxy Rag): a galaxy-print durag drops on, tails flowing. The stars come off the print and orbit
    them - a whole galaxy. Unbothered."""
    sx = _sx(side)
    res = _p(side, 2, 1)
    head = (_p(side, 10, 0), _p(side, 32, 40))
    w = []
    for k in range(4):                                                         # drops on
        w += emit_at(GAL28, res, 0, (head[0], head[1] + 30 - k * 10)) + wait(1)
    w += se(s["bling"]) + _hold(GAL28, res, 0, head, 4) + func(33, 0, 1, 0, 10, 0)
    import math
    w += se(s["cosmic"] if "cosmic" in s else s["psych"])
    for k in range(16):                                                        # the stars orbit
        a = k * math.tau / 8
        w += emit_at(GAL28, res, 0, head) + emit_at(GAL28, 0, 0, (round(math.cos(a) * 30), round(26 + math.sin(a) * 14)))
        if k == 8:
            w += emit_at(GAL28, 3, 0, (0, 26)) + se(s["bling"]) + func(34, 2, 0, 1, rgb(180, 140, 255), 12, 0)
        w += wait(1)
    return w + _hold(GAL28, res, 0, head, 4) + func(33, 0, 1, 10, 0, 0)
'''

TABLE = {464: ("_tag_in", ("TAG28", "TAGB28"), "Assist"),
         465: ("_bounce_back", ("BOUNCE28",), "Magic Coat"),
         466: ("_hold_grudge", ("GRUDGE28", "GRUDGEB28"), "Grudge"),
         467: ("_tickle_fight", ("TICKLE28", "TICKLEB28"), "Tickle"),
         468: ("_galaxy_rag", ("GAL28",), "Cosmic Power")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
