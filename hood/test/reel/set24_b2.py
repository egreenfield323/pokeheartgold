"""Set 24 batch 2 (INSANE): Rip Space, Ghost Ride, Mind Blown, Bad Omen, Compactor (variants 335-339, test-only
360 = Ghost Ride's turn 2). Run once from the repo root: python -X utf8 hood/test/reel/set24_b2.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "RIP24 RIPB24 GHOST24 GHOSTB24 MIND24 MINDB24 MINDC24 OMEN24 OMENB24 OMENC24 CRUSH24 CRUSHB24".split()

KITS = '''
    # ---- set 24, batch 2 (INSANE) -----------------------------------------------------------------------------
    # Rip Space (Spacial Rend): a giant zipper - unzip a little: stars - zip it back - then RIIIIP, the whole sky
    # unzips onto outer space and the foe gets yanked into it
    b, rs = pk(RIP24, {1: (fxart.space_zipper(), 2.4, 4, {}), 2: (fxart.space_zipper(opened=1), 2.4, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(220, 230, 255), rgb(255, 255, 255), .4, 8, .14, life=16, radius=.5)
    fin(RIP24, b, rs, (0, 1, 2))
    b, rs = pk(RIPB24, {1: (fxart.space_zipper(opened=2), 2.4, 4, {}), 2: (fxart.space_zipper(opened=2), 3.4, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(150, 70, 220), n=8, life=26, scl=.4, up=.02)
    fin(RIPB24, b, rs, (0, 1, 2))

    # Ghost Ride (Shadow Force): turn 1 a bedsheet ghost drops over them and floats off; turn 2 an empty minivan
    # rolls up, the ghost dancing on the roof - and it rams the foe
    b, rs = pk(GHOST24, {1: (fxart.sheet_ghost(), 1.0, 4, {}), 2: (fxart.minivan(), 2.4, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(235, 235, 250), n=5, life=20, scl=.35, up=.06)
    fin(GHOST24, b, rs, (0, 1, 2))
    b, rs = pk(GHOSTB24, {1: (flipx(fxart.minivan()), 2.4, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(220, 220, 230), rgb(255, 255, 255), .45, 16, .34, up=.16, gravity=.018, life=22, spin=0x0A00)
    fin(GHOSTB24, b, rs, (0, 1))

    # Mind Blown (Psycho Boost): 2+2=4 (the foe: ?) - E=MC2 (??) - 1+1=11 - MIND. BLOWN.
    b, rs = pk(MIND24, {1: (fxart.math_board(), ONE_TO_ONE, 4, {}), 2: (fxart.math_board(text="E=MC2"), ONE_TO_ONE, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(245, 245, 235), rgb(255, 255, 255), .3, 5, .1, up=.04, life=12)
    fin(MIND24, b, rs, (0, 1, 2))
    b, rs = pk(MINDB24, {1: (fxart.math_board(text="1+1=11"), ONE_TO_ONE, 4, {}), 2: (fxart.question_mark(), .45, 4, {})})
    fin(MINDB24, b, rs, (1, 2))
    b, rs = pk(MINDC24, {1: (fxart.galaxy_burst(), 3.0, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 120, 230), rgb(120, 230, 255), .55, 16, .32, up=.06, life=26, radius=.6)
    fin(MINDC24, b, rs, (0, 1))

    # Bad Omen (Doom Desire): a black cat crosses the foe's path - a mirror cracks - then a shooting star comes down
    b, rs = pk(OMEN24, {1: (fxart.black_cat(), .9, 4, {}), 2: (fxart.black_cat(step=1), .9, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(190, 225, 250), rgb(255, 255, 255), .3, 10, .2, up=.1, gravity=.016, life=18)
    fin(OMEN24, b, rs, (0, 1, 2))
    b, rs = pk(OMENB24, {1: (fxart.hand_mirror(), .9, 4, {}), 2: (fxart.hand_mirror(cracked=True), .9, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 240, 140), rgb(255, 255, 255), .35, 4, .03, life=20, radius=.2)
    fin(OMENB24, b, rs, (0, 1, 2))
    b, rs = pk(OMENC24, {1: (fxart.falling_star(), 1.8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 220, 60), rgb(255, 255, 230), .7, 20, .4, up=.1, life=24)
    fin(OMENC24, b, rs, (0, 1))

    # Compactor (Crush Grip): two steel walls close in on the foe - creak - crunch - CRUNCH - a cube of junk
    b, rs = pk(CRUSH24, {1: (fxart.compactor_plate(), 1.5, 4, {}), 2: (flipx(fxart.compactor_plate()), 1.5, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(255, 180, 60), rgb(255, 255, 200), .35, 10, .24, up=.1, gravity=.016, life=14)
    fin(CRUSH24, b, rs, (0, 1, 2))
    b, rs = pk(CRUSHB24, {1: (fxart.junk_cube(), 1.1, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(170, 165, 160), n=8, life=24, scl=.35, up=.05)
    fin(CRUSHB24, b, rs, (0, 1))
'''

SCRIPTS = '''
def _rip_space(side, s):
    """Spacial Rend (Rip Space): a giant zipper hangs in the sky. Zzzip - a peek of outer space. Zzzip - zipped back
    up. Then RIIIIIIP - all the way down onto the galaxy, and the foe gets yanked into it."""
    sx = _sx(side)
    z = _s23(side, 0, (140, 70))
    pull = _p(side, (-45, 11), (76, -70))
    zp = lambda res=1, kit=RIP24: emit_at(kit, res, 0, z)
    w = se(s["pop"]) + _hold(RIP24, 1, 0, z, 4)
    for n in range(2):                                                         # zzzip... (peek)... zzzip
        w += se(s["slash"]) + _hold(RIP24, 2, 0, z, 3, lambda k: emit_at(RIP24, 0, 0, (z[0], z[1] + 40)) if k == 0 else [])
        w += _hold(RIP24, 2, 0, z, 4 + 2 * n, lambda k: bmove(side, 264, 2, 0, 4) if k == 1 and n == 0 else
                   (bmove(side, 264, 2, 0, -4) if k == 3 and n == 0 else []))
        w += se(s["slash"]) + _hold(RIP24, 1, 0, z, 5)
    w += func(33, 0, 1, 0, 13, rgb(30, 10, 60)) + se(s["slash"]) + se(s["crack"])   # RIIIIIIIIP
    for k in range(3):
        w += zp(2) + wait(1) + zp(1, RIPB24) + wait(1)
    w += se(s["kaboom"]) + flash_screen(4) + func(68, 4, 4, 1, 10, 0)
    for k in range(14):
        w += emit_at(RIPB24, 2, 0, z)
        if k % 3 == 0:
            w += emit_at(RIPB24, 0, 0, (z[0] + (k % 2) * 20 - 10, z[1] + 10)) + emit_at(RIP24, 0, 0, (z[0], z[1] + 30))
        if k == 3:
            w += se(s["gust"]) + bmove(side, 264, 6, *pull) + shake_defender(2, 4)    # *yanked in*
        if k == 10:
            w += se(s["slash"]) + se(s["bslam"]) + flash_screen(5) + func(34, 8, 0, 1, rgb(180, 100, 255), 14, 0)
        w += wait(1)
    w += bmove(side, 264, 5, -pull[0], -pull[1]) + func(48)
    for k in range(4):                                                         # ...zipped back shut
        w += zp(2 if k < 2 else 1) + (se(s["slash"]) if k == 0 else []) + wait(1)
    return w + func(33, 0, 1, 13, 0, rgb(30, 10, 60)) + _hold(RIP24, 1, 0, z, 3)


def _ghost_ride(side, s):
    """Shadow Force (Ghost Ride), two turns. Turn 1: a bedsheet ghost costume drops over them - boo - and floats off
    (they're gone). Turn 2: an empty minivan rolls up, slide door open, the ghost dancing on the roof - ghost riding
    the whip - then it floors it into the foe."""
    sx = _sx(side)
    one = se(s["whoosh"])
    for k in range(4):                                                         # *drapes*
        one += emit_at(GHOST24, 1, 0, (0, 20 + round(50 * (1 - (k + 1) / 4)))) + wait(1)
    one += se(s["astonish"]) + _hold(GHOST24, 1, 0, (0, 20), 6, lambda k: emit_at(GHOST24, 0, 0, (0, 10)) if k == 2 else [])
    one += func(40, 2, 1)
    for k in range(6):                                                         # ...floats away
        one += emit_at(GHOST24, 1, 0, (sx * k * 6, 20 + k * 10 + (2 if k % 2 else 0))) + wait(1)
    one += wait(2)
    y = _p(side, 80, 92)
    van = _p(side, 2, 1)
    vkit = _p(side, GHOST24, GHOSTB24)
    start, stop, end = _p(side, (-70, 128, 400), (330, 196, -140))
    at = lambda x: _s23(side, 0, (x, y))
    ride = lambda x, hop=0: emit_at(vkit, van, 0, at(x)) + emit_at(GHOST24, 1, 0, _s23(side, 0, (x - sx * 4, y - 14 - hop)))
    two = se(s["bass"])
    for k in range(7):                                                         # *rolls up*, bass knocking
        x = round(start + (stop - start) * (k + 1) / 7)
        two += ride(x, 4 if k % 2 else 0) + (se(s["bass"]) if k % 2 == 0 else []) + wait(1)
    for k in range(8):                                                         # ghost riding the whip
        two += ride(stop, (8, 0, 8, 0, 12, 0, 12, 0)[k]) + (se(s["bass"]) if k % 2 == 0 else [])
        if k == 3:
            two += bmove(side, 264, 2, -sx * 6, 0)
        if k == 5:
            two += bmove(side, 264, 2, sx * 6, 0)
        two += wait(1)
    two += se(s["skrrt"])
    hit = False
    fx = _S23_AT["enemy" if side == "player" else "player"][0]
    for k in range(6):                                                         # FLOORS IT
        x = round(stop + (end - stop) * ((k + 1) / 6) ** 1.3)
        two += ride(x)
        if not hit and (x - fx) * sx > -40:
            hit = True
            two += se(s["kaboom"]) + se(s["bslam"]) + flash_screen(5) + func(68, 6, 4, 1, 5, 0)
            two += emit_at(GHOSTB24, 0, 1, (0, 20)) + shake_defender(4, 3) + func(48)
        two += wait(1)
    two += wait(2) + func(40, 2, 0) + se(s["pop"]) + emit_at(GHOST24, 0, 0, (0, 20)) + wait(4)
    return one, two


def _ghost_ride_turn2_first(side, s):
    """Test only: Ghost Ride's second turn on its own (vanishes the attacker first, like the real turn 1 would)."""
    return func(40, 2, 1) + _ghost_ride(side, s)[1]


def _mind_blown(side, s):
    """Psycho Boost (Mind Blown): a chalkboard: 2+2=4. The foe: ?. E=MC2. The foe: ??. Then 1+1=11. The foe
    stares... and their mind is BLOWN - a whole galaxy bursts out of their head."""
    board = _s23(side, 0, (106, 84))
    q = [(-12, 46), (12, 52)]
    w = se(s["pop"])
    for n, (kit, res) in enumerate(((MIND24, 1), (MIND24, 2), (MINDB24, 1))):
        w += se(s["lockon"]) + emit_at(MIND24, 0, 0, (board[0], board[1] - 4))
        ticks = (7, 8, 6)[n]
        for k in range(ticks):                                                 # ? ... ?? ...
            w += emit_at(kit, res, 0, board)
            if k >= 3 and n < 2:
                for j in range(n + 1):
                    w += emit_at(MINDB24, 2, 1, q[j])
            if k == 3 and n == 1:
                w += shake_defender(1, 2) + se(s["confuse"])
            w += wait(1)
    w += _hold(MINDB24, 1, 0, board, 4)                                       # *...*
    w += func(33, 0, 1, 0, 12, rgb(40, 10, 70)) + se(s["kaboom"]) + se(s["psych"]) + flash_screen(6)   # MIND. BLOWN.
    w += func(68, 4, 4, 1, 8, 0) + emit_at(MINDC24, 0, 1, (0, 40))
    for k in range(14):
        w += emit_at(MINDC24, 1, 1, (0, 28 + (k % 2) * 2)) + emit_at(MINDB24, 1, 0, board)
        if k % 4 == 0:
            w += shake_defender(2, 1) + emit_at(MINDC24, 0, 1, (0, 50))
        if k == 5:
            w += func(34, 8, 0, 1, rgb(220, 120, 255), 14, 0)
        w += wait(1)
    return w + func(48) + func(33, 0, 1, 12, 0, rgb(40, 10, 70)) + wait(4)


def _bad_omen(side, s):
    """Doom Desire (Bad Omen): a black cat strolls right across the foe's path. A hand mirror lands by them - and
    cracks. The sky goes dark. A star twinkles... and comes straight down on them."""
    y = _p(side, 88, 124)
    xs = _p(side, (126, 250), (14, 124))
    mirror = _p(side, (-79, -5), (46, 40))
    w = se(s["sscent"])
    for k in range(10):                                                        # *strolls by*
        x = round(xs[0] + (xs[1] - xs[0]) * (k + 1) / 10)
        w += emit_at(OMEN24, 1 + k % 2, 0, _s23(side, 0, (x, y)))
        if k == 4:
            w += bmove(side, 264, 2, 0, 4) + se(s["leer"])
        if k == 6:
            w += bmove(side, 264, 2, 0, -4)
        w += wait(1)
    w += wait(2) + se(s["whoosh"])
    for k in range(3):
        w += emit_at(OMENB24, 1, 1, (mirror[0], mirror[1] + 30 - k * 10)) + wait(1)
    w += _hold(OMENB24, 1, 1, mirror, 4)
    w += se(s["crack"]) + emit_at(OMEN24, 0, 1, mirror) + shake_defender(2, 2)    # *crack*
    w += _hold(OMENB24, 2, 1, mirror, 7)
    w += func(33, 0, 1, 0, 12, rgb(10, 10, 50)) + _hold(OMENB24, 2, 1, mirror, 3)   # *the sky goes dark*
    w += se(s["bling"]) + emit_at(OMENB24, 0, 1, (60, 110)) + _hold(OMENB24, 2, 1, mirror, 5)
    for k in range(6):                                                         # *here it comes*
        t = ((k + 1) / 6) ** 1.6
        w += emit_at(OMENC24, 1, 1, (round(60 - 54 * t), round(130 - 96 * t))) + emit_at(OMENB24, 2, 1, mirror) + wait(1)
    w += se(s["kaboom"]) + se(s["explo"]) + flash_screen(6) + func(68, 7, 7, 1, 6, 0)
    w += emit_at(OMENC24, 0, 1, (0, 24)) + emit_at(OMENC24, 0, 1, (0, 36)) + shake_defender(5, 4) + func(48)
    w += func(34, 8, 0, 1, rgb(255, 220, 60), 14, 0) + wait(8)
    return w + func(33, 0, 1, 12, 0, rgb(10, 10, 50)) + wait(4)


def _compactor(side, s):
    """Crush Grip (Compactor): the junkyard compactor: two steel walls slide in on either side of the foe - creak -
    crunch - CRUNCH - and there's just a cube of junk. Then the walls pull back and the foe pops out, flattened."""
    gaps = (60, 30, 18, 8, 0)
    walls = lambda g, dy=10: emit_at(CRUSH24, 1, 1, (-30 - g, dy)) + emit_at(CRUSH24, 2, 1, (30 + g, dy))
    w = se(s["harden"])
    for k in range(4):
        w += walls(60 + 60 * (3 - k) // 3) + wait(1)
    w += _hold(CRUSH24, 1, 1, (-90, 10), 3, lambda k: emit_at(CRUSH24, 2, 1, (90, 10)))
    for n, g in enumerate(gaps[1:4]):                                          # creak... crunch... CRUNCH
        w += se(s["harden"] if n == 0 else s["crunch"])
        for k in range(3):
            w += walls(round(gaps[n] + (g - gaps[n]) * (k + 1) / 3)) + wait(1)
        w += emit_at(CRUSH24, 0, 1, (-30 - g + 4, 20)) + shake_defender(1 + n, 2)
        w += walls(g) + wait(1) + walls(g) + wait(2 + n)
    w += se(s["bslam"]) + se(s["kaboom"]) + flash_screen(5) + func(68, 6, 6, 1, 5, 0)
    w += walls(0) + emit_at(CRUSHB24, 1, 1, (0, 14)) + emit_at(CRUSH24, 0, 1, (0, 40)) + wait(1)
    for k in range(10):                                                        # *a cube*
        w += walls(0) + emit_at(CRUSHB24, 1, 1, (0, 14)) + wait(1)
    w += se(s["harden"])
    for k in range(4):                                                         # *the walls pull back*
        w += walls(k * 20) + (emit_at(CRUSHB24, 1, 1, (0, 14)) if k < 2 else []) + wait(1)
    w += se(s["pop"]) + emit_at(CRUSHB24, 0, 1, (0, 14)) + func(34, 8, 0, 1, rgb(150, 150, 160), 13, 0) + shake_defender(3, 3) + func(48)
    return w + wait(6)
'''

TABLE = {335: ("_rip_space", ("RIP24", "RIPB24"), "Spacial Rend"),
         336: ("_ghost_ride", ("GHOST24", "GHOSTB24"), "Shadow Force"),
         337: ("_mind_blown", ("MIND24", "MINDB24", "MINDC24"), "Psycho Boost"),
         338: ("_bad_omen", ("OMEN24", "OMENB24", "OMENC24"), "Doom Desire"),
         339: ("_compactor", ("CRUSH24", "CRUSHB24"), "Crush Grip")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE, remap=("Spacial Rend", "Shadow Force", "Psycho Boost", "Doom Desire", "Crush Grip"))
    p = set23_lib.ROOT / "hood/gunfx.py"
    s = p.read_text(encoding="utf-8")
    for a, b in (("            336: _ghost_ride,\n", "            336: _ghost_ride,\n            360: _ghost_ride_turn2_first,\n"),
                 ("        336: (GHOST24, GHOSTB24,),\n", "        336: (GHOST24, GHOSTB24,),\n        360: (GHOST24, GHOSTB24,),\n")):
        assert s.count(a) == 1, a
        s = s.replace(a, b)
    p.write_text(s, encoding="utf-8", newline="")
