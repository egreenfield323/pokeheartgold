"""Set 26 batch 2: Night Night, Dome Piece, Drill, Cold Case, Bat Rush (variants 397-401, test-only 422 = Dome
Piece turn 2). Run once from the repo root: python -X utf8 hood/test/reel/set26_b2.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "NIGHT26 NIGHTB26 DOME26 DRILL26 DRILLB26 DRILLC26 COLD26 COLDB26 BAT26".split()

KITS = '''
    # ---- set 26, batch 2 ----------------------------------------------------------------------------------
    # Night Night (Spore): the music box plays - the foe yawns - plays - nods - then a giant pacifier. Out cold.
    b, rs = pk(NIGHT26, {1: (fxart.music_box(), 1.0, 4, {}), 2: (fxart.big_pacifier(), .6, 4, {})}, alpha=fxart.tiny_note())
    burst(b, rs, 0, rgb(255, 150, 210), rgb(255, 240, 250), .4, 4, .05, up=.1, life=26, radius=.3)
    fin(NIGHT26, b, rs, (0, 1, 2))
    b, rs = pk(NIGHTB26, {}, alpha=fxart.sleep_z16())
    burst(b, rs, 0, rgb(120, 170, 255), rgb(230, 240, 255), .45, 3, .04, up=.1, life=30, radius=.2)
    fin(NIGHTB26, b, rs, (0,))

    # Dome Piece (Skull Bash): turn 1 the helmet goes on, buckled - knock knock. Turn 2 they charge head first.
    b, rs = pk(DOME26, {1: (fxart.football_helmet(), .8, 4, {}), 2: (flipx(fxart.football_helmet()), .8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .55, 12, .3, life=12)
    fin(DOME26, b, rs, (0, 1, 2))

    # Drill (Horn Drill): a drill - a bigger drill - an industrial drill. Done.
    b, rs = pk(DRILL26, {1: (fxart.power_drill(), .8, 4, {}), 2: (fxart.power_drill(big=1), .9, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 220, 80), rgb(255, 255, 220), .35, 6, .2, life=8)
    fin(DRILL26, b, rs, (0, 1, 2))
    b, rs = pk(DRILLB26, {1: (fxart.power_drill(big=2), 1.4, 4, {}), 2: (flipx(fxart.power_drill()), .8, 4, {})})
    fin(DRILLB26, b, rs, (1, 2))
    b, rs = pk(DRILLC26, {1: (flipx(fxart.power_drill(big=1)), .9, 4, {}), 2: (flipx(fxart.power_drill(big=2)), 1.4, 4, {})})
    fin(DRILLC26, b, rs, (1, 2))

    # Cold Case (Sheer Cold): the evidence board, the case file - stamped COLD CASE - and the foe's on ice
    b, rs = pk(COLD26, {1: (fxart.evidence_board(), 1.1, 4, {}), 2: (fxart.case_file(), ONE_TO_ONE, 4, {})}, alpha=fxart.frost_crystal())
    burst(b, rs, 0, rgb(170, 220, 255), rgb(255, 255, 255), .45, 14, .24, up=.06, life=22, spin=0x0600)
    fin(COLD26, b, rs, (0, 1, 2))
    b, rs = pk(COLDB26, {1: (fxart.case_ice(), 1.4, 4, {})})
    fin(COLDB26, b, rs, (1,))

    # Bat Rush (Bone Rush): one bat swing, bonk (replays per hit: short)
    b, rs = pk(BAT26, {1: (fxart.alu_bat(), .8, 4, {}), 2: (flipx(fxart.alu_bat()), .8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .5, 10, .26, life=10)
    fin(BAT26, b, rs, (0, 1, 2))
'''

SCRIPTS = '''
def _night_night(side, s):
    """Spore (Night Night): a music box starts playing - the foe yawns. It keeps playing - they nod off. Then a giant
    pacifier pops right in their mouth. Night night."""
    mb = _s23(side, 0, (106, 86))
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = se(s["pop"]) + _hold(NIGHT26, 1, 0, mb, 3)
    for n in range(2):                                                         # *plinky lullaby*
        w += se(s["bling"])
        for k in range(8):
            w += emit_at(NIGHT26, 1, 0, (mb[0] + (k % 2), mb[1]))
            if k % 3 == 0:
                w += emit_at(NIGHT26, 0, 0, (mb[0], mb[1] + 26))
            if k == 4:
                w += bmove(side, 264, 3, 0, -4 - 2 * n) + (se(s["yawn"]) if n == 0 else [])
            w += wait(1)
        w += bmove(side, 264, 3, 0, 4 + 2 * n)
    w += se(s["whoosh"]) + _lob(NIGHT26, 2, side, (mb[0], mb[1] + 20), (dx - _sx(side) * 14, dy + 26), 5, 20, lambda k: emit_at(NIGHT26, 1, 0, mb))
    w += se(s["pop"]) + se(s["sleep"]) + func(34, 8, 0, 1, rgb(120, 150, 255), 10, 0)
    for k in range(12):                                                        # *out*
        w += emit_at(NIGHT26, 2, 1, (-_sx(side) * 14, 26)) + emit_at(NIGHT26, 1, 0, mb)
        if k in (1, 7):
            w += emit_at(NIGHTB26, 0, 1, (10, 44))
        w += wait(1)
    return w + wait(2)


def _dome_piece(side, s):
    """Skull Bash (Dome Piece), two turns. Turn 1: a football helmet comes down on their head - click - they knock on
    it twice, solid. Turn 2: helmet on, they charge head first into the foe."""
    sx = _sx(side)
    res = _p(side, 1, 2)
    head = _p(side, (sx * 2, 36), (0, 30))
    one = se(s["whoosh"])
    for k in range(4):
        one += emit_at(DOME26, res, 0, (head[0], head[1] + round(40 * (1 - (k + 1) / 4)))) + wait(1)
    one += se(s["harden"]) + _hold(DOME26, res, 0, head, 3)
    for n in range(2):                                                         # knock knock
        one += se(s["bonk"]) + emit_at(DOME26, 0, 0, (head[0], head[1] + 10)) + _hold(DOME26, res, 0, head, 4)
    one += func(34, 2, 0, 1, rgb(150, 190, 255), 10, 0) + _hold(DOME26, res, 0, head, 3)
    two = se(s["harden"]) + _hold(DOME26, res, 0, head, 3)
    two += bmove(side, 258, 2, -sx * 6, -2) + _hold(DOME26, res, 0, head, 2)  # *wind up*
    two += se(s["rage"]) + bmove(side, 258, 3, sx * 36, 14) + emit_at(DOME26, res, 0, head) + wait(1)   # CHARGE
    two += se(s["kaboom"]) + se(s["bslam"]) + flash_screen(5) + emit_at(DOME26, 0, 1, (0, 26)) + shake_defender(5, 3) + func(48) + func(68, 4, 4, 1, 4, 0)
    two += _hold(DOME26, res, 0, head, 2) + bmove(side, 258, 4, -sx * 30, -12) + bmove(side, 258, 2, -sx * 6, -2)
    return one, two + _hold(DOME26, res, 0, head, 3)


def _dome_piece_turn2_first(side, s):
    """Test only: Dome Piece's second turn on its own."""
    return _dome_piece(side, s)[1]


def _drill_ohko(side, s):
    """Horn Drill (Drill): a cordless drill on the foe - bzzzt, sparks. A hammer drill - BZZZT. Then an industrial
    drill with a bit the length of a car. That's it for them."""
    sx = _sx(side)
    at = _p(side, (-44, 24), (44, 24))
    drills = _p(side, ((DRILL26, 1), (DRILL26, 2), (DRILLB26, 1)), ((DRILLB26, 2), (DRILLC26, 1), (DRILLC26, 2)))
    w = []
    for n, (kit, res) in enumerate(drills):                                    # bzzzt... BZZZT... BRRRRRRR
        off = (at[0] - sx * 10 * n, at[1])
        w += se(s["pop"]) + _hold(kit, res, 1, off, 2)
        w += se(s["rollout"])
        for k in range(5 + 2 * n):
            w += emit_at(kit, res, 1, (off[0] + (k % 2) * sx * 2, off[1]))
            if k % 2 == 0:
                w += emit_at(DRILL26, 0, 1, (0, 22)) + shake_defender(1 + (n == 2), 1)
            w += wait(1)
        w += wait(2)
    w += se(s["kaboom"]) + flash_screen(6) + func(68, 5, 5, 1, 5, 0) + shake_defender(5, 4) + func(48)
    return w + func(34, 8, 0, 1, rgb(60, 60, 70), 14, 0) + wait(6)


def _cold_case(side, s):
    """Sheer Cold (Cold Case): the detective's evidence board, red string everywhere. The case file slides out. Stamped:
    COLD CASE. And the foe's on ice - frozen solid in a block."""
    bd = _s23(side, 0, (104, 80))
    file_ = (bd[0] + _sx(side) * 6, bd[1] - 14)
    w = func(33, 0, 1, 0, 8, rgb(30, 40, 70)) + se(s["pop"]) + _hold(COLD26, 1, 0, bd, 6)
    for k in range(4):                                                         # *the file*
        w += emit_at(COLD26, 2, 0, (file_[0], file_[1] - 30 + k * 8)) + emit_at(COLD26, 1, 0, bd) + wait(1)
    w += _hold(COLD26, 1, 0, bd, 4, lambda k: emit_at(COLD26, 2, 0, file_))
    w += se(s["bslam"]) + se(s["ishard"]) + flash_screen(4) + emit_at(COLD26, 0, 1, (0, 24))   # COLD. CASE.
    w += func(34, 8, 0, 1, rgb(160, 210, 255), 15, 0) + shake_defender(2, 2)
    for k in range(14):
        w += emit_at(COLDB26, 1, 1, (0, 14)) + emit_at(COLD26, 2, 0, file_)
        if k == 6:
            w += emit_at(COLD26, 0, 1, (0, 30)) + se(s["ishard"])
        w += wait(1)
    return w + func(48) + func(33, 0, 1, 8, 0, rgb(30, 40, 70)) + wait(2)


def _bat_rush(side, s):
    """Bone Rush (Bat Rush): one bat swing off the foe - bonk. (Replays per hit.)"""
    sx = _sx(side)
    res = _p(side, 1, 2)
    w = se(s["whoosh"])
    for k, (x, y) in enumerate(((-56, 52), (-40, 40), (-26, 30))):
        w += emit_at(BAT26, res, 1, (sx * x, y)) + wait(1)
    w += se(s["bonk"]) + emit_at(BAT26, 0, 1, (0, 30)) + shake_defender(2, 2) + emit_at(BAT26, res, 1, (-sx * 18, 26)) + wait(1)
    return w + emit_at(BAT26, res, 1, (-sx * 12, 20)) + wait(2)
'''

TABLE = {397: ("_night_night", ("NIGHT26", "NIGHTB26"), "Spore"),
         398: ("_dome_piece", ("DOME26",), "Skull Bash"),
         399: ("_drill_ohko", ("DRILL26", "DRILLB26", "DRILLC26"), "Horn Drill"),
         400: ("_cold_case", ("COLD26", "COLDB26"), "Sheer Cold"),
         401: ("_bat_rush", ("BAT26",), "Bone Rush")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
    p = set23_lib.ROOT / "hood/gunfx.py"
    s = p.read_text(encoding="utf-8")
    for a, b in (("            398: _dome_piece,\n", "            398: _dome_piece,\n            422: _dome_piece_turn2_first,\n"),
                 ("        398: (DOME26,),\n", "        398: (DOME26,),\n        422: (DOME26,),\n")):
        assert s.count(a) == 1, a
        s = s.replace(a, b)
    p.write_text(s, encoding="utf-8", newline="")
