"""Set 29 batch 2: Face Swap, Caricature, Rebrand, B-Side, Take the L (variants 489-493).
Run once from the repo root: python -X utf8 hood/test/reel/set29_b2.py  (art: set29_b2_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "SWAP29 SWAPB29 EASEL29 EASELB29 ROLL29 TAPE29 L29".split()

KITS = '''
    # ---- set 29, batch 2 ----------------------------------------------------------------------------------
    # Face Swap (Transform): the filter - SCAN - SWAP - DONE
    b, rs = pk(SWAP29, {1: (fxart.faceswap_phone(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.faceswap_phone(stage=1), ONE_TO_ONE, 4, {"colors": 30})})
    fin(SWAP29, b, rs, (1, 2))
    b, rs = pk(SWAPB29, {1: (fxart.faceswap_phone(stage=2), ONE_TO_ONE, 4, {"colors": 30})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(160, 255, 220), rgb(255, 255, 255), .5, 16, .26, life=18, radius=.5)
    fin(SWAPB29, b, rs, (0, 1))

    # Caricature (Sketch): the easel - sketch sketch - a big-head caricature of the foe
    b, rs = pk(EASEL29, {1: (fxart.art_easel(), 1.0, 4, {}), 2: (fxart.art_easel(stage=1), 1.0, 4, {})})
    fin(EASEL29, b, rs, (1, 2))
    b, rs = pk(EASELB29, {1: (fxart.art_easel(stage=2), 1.0, 4, {}), 2: (fxart.artist_pencil(), .5, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 240, 160), rgb(255, 255, 255), .45, 12, .24, life=14)
    fin(EASELB29, b, rs, (0, 1, 2))

    # Rebrand (Conversion): the paint roller - roll - roll - a whole new color
    b, rs = pk(ROLL29, {1: (fxart.paint_roller(), .8, 4, {}), 2: (flipx(fxart.paint_roller()), .8, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(40, 190, 180), rgb(150, 240, 230), .25, 3, .04, gravity=.02, life=14, radius=.2)
    fin(ROLL29, b, rs, (0, 1, 2))

    # B-Side (Conversion 2): SIDE A - flip - SIDE B - play
    b, rs = pk(TAPE29, {1: (fxart.bside_tape(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.bside_tape(side_b=True), ONE_TO_ONE, 4, {"colors": 30})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 160, 180), rgb(255, 255, 255), .45, 12, .22, life=16)
    fin(TAPE29, b, rs, (0, 1, 2))

    # Take the L (Swallow): a giant red L drops in - they look at it - GULP - and somehow feel better
    b, rs = pk(L29, {1: (fxart.giant_l(), .8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(140, 255, 160), rgb(255, 255, 255), .45, 14, .18, up=.1, life=24, radius=.6)
    fin(L29, b, rs, (0, 1))
'''

SCRIPTS = '''
def _face_swap(side, s):
    """Transform (Face Swap): the phone comes out, face-swap filter on - SCAN, the line sweeps their face. SWAP - the two
    of them flicker back and forth. DONE."""
    ph = _s23(side, 0, _p(side, (110, 84), (156, 82)))
    w = se(s["pop"]) + _hold(SWAP29, 1, 0, ph, 10, lambda k: se(s["lockon"]) if k == 3 else [])
    w += se(s["psych"])
    for k in range(10):                                                        # SWAP - flicker
        w += emit_at(SWAP29, 2, 0, ph)
        if k % 2 == 0:
            col = (rgb(255, 120, 220), rgb(120, 255, 220))[(k // 2) % 2]
            w += func(34, 2, 0, 1, col, 11, 0) + func(34, 8, 0, 1, col, 11, 0)
        w += wait(1)
    w += se(s["bling"]) + emit_at(SWAPB29, 0, 0, (0, 30))
    return w + _hold(SWAPB29, 1, 0, ph, 10)


def _caricature(side, s):
    """Sketch (Caricature): a street caricature artist's easel next to the foe. Sketch sketch - rough lines. Sketch -
    then the reveal: a big-head caricature of the foe, huge grin. Keeping that one."""
    sx = _sx(side)
    ea = _s23(side, 0, _p(side, (128, 72), (118, 76)))
    pen = lambda k: emit_at(EASELB29, 2, 0, (ea[0] + (k % 3 - 1) * 6, ea[1] + 4 + (k % 2) * 6))
    w = se(s["pop"]) + _hold(EASEL29, 1, 0, ea, 5)
    w += se(s["swipe"])
    for k in range(8):                                                         # sketch... sketch...
        w += emit_at(EASEL29, 1 if k < 4 else 2, 0, ea) + pen(k) + (se(s["swipe"]) if k == 4 else []) + wait(1)
    w += bmove(side, 264, 2, 0, 4) + _hold(EASEL29, 2, 0, ea, 3) + bmove(side, 264, 2, 0, -4)   # the foe leans in
    w += se(s["bling"]) + emit_at(EASELB29, 0, 0, ea) + flash_screen(2)       # the reveal
    w += _hold(EASELB29, 1, 0, ea, 6) + shake_defender(2, 2)
    return w + _hold(EASELB29, 1, 0, ea, 8)


def _rebrand(side, s):
    """Conversion (Rebrand): the paint roller comes out - roll, a stripe of new color. Roll - another. Then the full
    coat: a whole new look. Rebranded."""
    sx = _sx(side)
    res = _p(side, 1, 2)
    w = []
    for n in range(3):                                                         # roll... roll... full coat
        w += se(s["swipe"])
        for k in range(5):
            w += emit_at(ROLL29, res, 0, (sx * (n * 10 - 10), 50 - k * 9)) + (emit_at(ROLL29, 0, 0, (sx * (n * 10 - 10), 34 - k * 6)) if k % 2 == 0 else []) + wait(1)
        w += func(34, 2, 0, 1, rgb(40, 190, 180), 7 + n * 3, 0) + wait(2)
    w += se(s["bling"]) + emit_at(ROLL29, 0, 0, (0, 30)) + flash_screen(2)
    return w + _hold(ROLL29, res, 0, (sx * 30, 30), 6)


def _b_side(side, s):
    """Conversion 2 (B-Side): a cassette - SIDE A. Pop it out, flip it - SIDE B. Click, play - a whole new sound."""
    tp = _s23(side, 0, _p(side, (110, 82), (156, 80)))
    w = se(s["pop"]) + _hold(TAPE29, 1, 0, tp, 8)
    w += se(s["clock"])
    for k in range(6):                                                         # flip...
        w += emit_at(TAPE29, 1 if k < 3 else 2, 0, (tp[0], tp[1] + (6 if k in (2, 3) else 0))) + wait(1)
    w += se(s["clock"]) + _hold(TAPE29, 2, 0, tp, 4)                          # click - play
    w += se(s["bling"]) + emit_at(TAPE29, 0, 0, tp) + func(34, 2, 0, 1, rgb(255, 120, 150), 12, 0)
    return w + _hold(TAPE29, 2, 0, tp, 8)


def _take_the_l(side, s):
    """Swallow (Take the L): a giant red L floats down in front of them. They look at it. Shrug. GULP - the whole
    thing. ...and they actually feel better."""
    sx = _sx(side)
    mouth = (_p(side, 12, 0), _p(side, 30, 34))
    w = se(s["whoosh"])
    for k in range(6):                                                         # it floats down
        w += emit_at(L29, 1, 0, (sx * 30, 90 - k * 10)) + wait(1)
    w += _hold(L29, 1, 0, (sx * 30, 34), 8)                                    # ...look at it
    w += bmove(side, 258, 2, 0, 4) + _hold(L29, 1, 0, (sx * 30, 34), 3) + bmove(side, 258, 2, 0, -4)   # shrug
    w += se(s["whoosh"]) + _lob(L29, 1, side, (sx * 30, 34), mouth, 4, 6)
    w += se(s["crunch"]) + shake_attacker(2, 3) + wait(6)                      # GULP
    w += se(s["rest"]) + emit_at(L29, 0, 0, (0, 28)) + func(34, 2, 0, 1, rgb(140, 255, 160), 12, 0)
    return w + wait(10)
'''

TABLE = {489: ("_face_swap", ("SWAP29", "SWAPB29"), "Transform"),
         490: ("_caricature", ("EASEL29", "EASELB29"), "Sketch"),
         491: ("_rebrand", ("ROLL29",), "Conversion"),
         492: ("_b_side", ("TAPE29",), "Conversion 2"),
         493: ("_take_the_l", ("L29",), "Swallow")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
