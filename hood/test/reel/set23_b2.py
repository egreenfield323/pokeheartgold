"""Set 23 batch 2: Mall Ninja, M-80, Zip Tie, Onion Breath, Rage Quit (variants 304-308).
Run once from the repo root: python -X utf8 hood/test/reel/set23_b2.py  (art: set23_b2_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "NINJA23 NINJAB23 M8023 M80B23 ZIP23 ZIPB23 ONION23 ONIONB23 RAGE23 RAGEB23".split()

KITS = '''
    # ---- set 23, batch 2 ----------------------------------------------------------------------------------
    # Mall Ninja (Karate Chop): headband on - chop the board: it does NOT break, ow - again, ow - then they chop the
    # FOE instead. (The board snaps on its own afterwards.)
    b, rs = pk(NINJA23, {1: (fxart.ninja_headband(), .8, 4, {}), 2: (fxart.board_chairs(), 1.0, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 240, 120), rgb(255, 255, 255), .45, 6, .16, life=12)
    fin(NINJA23, b, rs, (0, 1, 2))
    b, rs = pk(NINJAB23, {1: (fxart.board_chairs(broken=True), 1.0, 4, {}), 2: (fxart.chop_streak(), 1.1, 6, {"scl_anm": (.4, 1.2, 1.0, 80, 255)})},
               alpha=fxart.speck())
    burst(b, rs, 0, rgb(200, 150, 80), rgb(240, 210, 150), .4, 10, .2, up=.12, gravity=.016, life=18)
    fin(NINJAB23, b, rs, (0, 1, 2))

    # M-80 (DynamicPunch): light it - fizzle - light it - fizzle - the foe leans in to look - BOOM
    b, rs = pk(M8023, {1: (fxart.m80(), .6, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 180, 40), rgb(255, 255, 200), .3, 3, .08, up=.08, gravity=.008, life=10)
    burst(b, rs, 2, rgb(255, 230, 60), rgb(255, 255, 220), .4, 7, .1, up=.02, life=26, radius=.5)
    fin(M8023, b, rs, (0, 1, 2))
    b, rs = pk(M80B23, {1: (fxart.m80_blast(), 1.7, 14, {"scl_anm": (.2, 1.2, 1.0, 50, 255)})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(120, 115, 115), n=5, life=20, scl=.35, up=.05)
    puffs(b, rs, 2, rgb(70, 65, 65), n=12, life=30, scl=.45, up=.06)
    fin(M80B23, b, rs, (0, 1, 2))

    # Zip Tie (Bind): zzzip - the foe flexes, SNAP - a bigger one, SNAP - the yellow industrial one holds
    b, rs = pk(ZIP23, {1: (fxart.zip_tie(), 1.0, 4, {}), 2: (fxart.zip_tie(), 1.3, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(40, 40, 46), rgb(120, 120, 130), .4, 8, .22, up=.1, gravity=.014, life=16)
    fin(ZIP23, b, rs, (0, 1, 2))
    b, rs = pk(ZIPB23, {1: (fxart.zip_tie(color=(250, 200, 30, 255), hi=(255, 240, 150, 255)), 1.75, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 90), rgb(255, 255, 220), .4, 6, .14, life=10)
    fin(ZIPB23, b, rs, (0, 1))

    # Onion Breath (DragonBreath): a raw red onion - crunch - crunch (eyes watering) - then HAAAA in the foe's face
    b, rs = pk(ONION23, {1: (fxart.red_onion(), .75, 4, {}), 2: (fxart.red_onion(bites=1), .75, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(120, 190, 255), rgb(230, 245, 255), .3, 6, .1, up=.08, gravity=.016, life=18)
    fin(ONION23, b, rs, (0, 1, 2))
    b, rs = pk(ONIONB23, {2: (fxart.red_onion(bites=2), .75, 4, {})}, alpha=fxart.stink_wave())
    spray2(b, rs, {"player": (10, 34), "enemy": (-10, 26)}, (0, 22), 12, clr=rgb(170, 220, 60),
           clr_anm=(rgb(230, 255, 160), rgb(120, 190, 40)), scl=.7, gen=2, gen_intvl=1, emtr_life=22, radius=.2,
           spread=.03, alpha=(30, 26, 0))
    fin(ONIONB23, b, rs, (0, 1, 2))

    # Rage Quit (Outrage): GAME OVER - mash mash - GAME OVER - the controller goes through the screen and off
    # the foe's head, then they just swing
    b, rs = pk(RAGE23, {1: (fxart.gaming_monitor(), ONE_TO_ONE, 4, {}), 2: (fxart.gaming_monitor(cracked=True), ONE_TO_ONE, 4, {})},
               alpha=fxart.speck())
    burst(b, rs, 0, rgb(190, 230, 255), rgb(255, 255, 255), .35, 14, .24, up=.12, gravity=.016, life=20)
    fin(RAGE23, b, rs, (0, 1, 2))
    b, rs = pk(RAGEB23, {1: (fxart.gamepad(), .55, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 255), rgb(255, 255, 255), .3, 3, .08, life=8)
    burst(b, rs, 2, rgb(255, 50, 30), rgb(255, 200, 150), .45, 8, .16, up=.06, life=14)
    fin(RAGEB23, b, rs, (0, 1, 2))
'''

SCRIPTS = '''
def _mall_ninja(side, s):
    """Karate Chop (Mall Ninja): the headband goes on. They chop the board - it doesn't break, ow. Again - ow.
    So they chop the FOE instead. Then the board finally snaps by itself."""
    sx = _sx(side)
    hb = _s23(side, 0, _p(side, (68, 112), (185, 56)))
    board = _s23(side, 1, _p(side, (118, 72), (150, 64)))
    band = lambda: emit_at(NINJA23, 1, 0, hb)
    w = se(s["whoosh"])
    for k in range(4):                                                         # the headband flies on
        w += emit_at(NINJA23, 1, 0, (hb[0] - sx * 40 * (1 - (k + 1) / 4), hb[1] + 50 * (1 - (k + 1) / 4))) + wait(1)
    w += se(s["focus"]) + bmove(side, 258, 2, 0, 6) + emit_at(NINJA23, 0, 0, (hb[0], hb[1] + 6))
    w += _hold(NINJA23, 2, 1, board, 3, lambda k: band()) + bmove(side, 258, 2, 0, -6)
    w += _hold(NINJA23, 2, 1, board, 2, lambda k: band())
    for n in range(2):                                                         # HI-YAH... *bonk*
        w += bmove(side, 258, 2, sx * 26, 24) + se(s["chop"]) + emit_at(NINJAB23, 2, 1, (board[0], board[1] + 10))
        w += _hold(NINJA23, 2, 1, board, 1, lambda k: band())
        w += se(s["bonk"]) + emit_at(NINJA23, 0, 1, (board[0], board[1] + 6)) + shake_attacker(2, 2 + n)
        w += func(34, 2, 0, 1, rgb(255, 80, 80), 8 + 3 * n, 0)
        w += _hold(NINJA23, 2, 1, board, 3, lambda k: band()) + bmove(side, 258, 3, -sx * 26, -24)
        w += _hold(NINJA23, 2, 1, board, 4 + n, lambda k: band())
    w += _hold(NINJA23, 2, 1, board, 3, lambda k: band())                     # *...looks at the foe*
    w += bmove(side, 258, 2, sx * 22, 8) + se(s["chop"]) + se(s["bslam"]) + flash_screen(4)
    w += emit_at(NINJAB23, 2, 1, (0, 22)) + shake_defender(4, 3) + func(48) + func(68, 4, 4, 1, 3, 0)
    w += _hold(NINJA23, 2, 1, board, 2, lambda k: band()) + bmove(side, 258, 4, -sx * 22, -8)
    w += _hold(NINJA23, 2, 1, board, 4, lambda k: band())
    w += se(s["crack"]) + emit_at(NINJAB23, 0, 1, (board[0], board[1] + 6))   # ...*crack*
    return w + _hold(NINJAB23, 1, 1, board, 8, lambda k: band())


def _m80(side, s):
    """DynamicPunch (M-80): an M-80 by the foe. Light it... it fizzles. Light it... fizzles. The foe leans in for
    a closer look... BOOM."""
    sx = _sx(side)
    m = _p(side, (-55, 1), (40, 28))
    fuse = (m[0] + 2, m[1] + 11)
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = se(s["whoosh"]) + _lob(M8023, 1, side, (sx * 20, 24), (dx + m[0], dy + m[1]), 5, 16)
    w += se(s["bonk"]) + _hold(M8023, 1, 1, m, 3)
    for n, ticks in enumerate((6, 4)):                                         # tsss... *fizzle*
        w += se(s["ember"])
        w += _hold(M8023, 1, 1, m, ticks, lambda k: emit_at(M8023, 0, 1, fuse) if k % 2 == 0 else [])
        w += se(s["disable"]) + emit_at(M80B23, 0, 1, fuse) + _hold(M8023, 1, 1, m, 5)
        if n == 1:
            w += shake_defender(1, 1)
    w += bmove(side, 264, 5, -sx * 16, -sx * 6) + _hold(M8023, 1, 1, m, 3)   # *leans in*...
    w += se(s["ember"]) + _hold(M8023, 1, 1, m, 3, lambda k: emit_at(M8023, 0, 1, fuse))
    w += se(s["kaboom"]) + se(s["explo"]) + flash_screen(6) + emit_at(M80B23, 1, 1, m) + emit_at(M80B23, 2, 1, m)   # BOOM
    w += func(68, 6, 6, 1, 4, 0) + shake_defender(5, 4) + func(48) + func(34, 8, 0, 1, rgb(50, 40, 40), 14, 0)
    w += wait(6) + bmove(side, 264, 5, sx * 16, sx * 6) + wait(2)
    w += emit_at(M8023, 2, 1, (0, 34)) + se(s["confuse"]) + wait(8)
    return w


def _zip_tie(side, s):
    """Bind (Zip Tie): a zip tie cinches round the foe - they flex - SNAP. A bigger one - SNAP. Then the yellow
    industrial-size one. They ain't going nowhere. (Short: Bind replays it every turn.)"""
    mid = (0, 12)
    w = []
    for n, (kit, res) in enumerate(((ZIP23, 1), (ZIP23, 2), (ZIPB23, 1))):
        w += se(s["constrict"])
        for k in range(3):                                                     # zzzip
            w += emit_at(kit, res, 1, (mid[0], mid[1] + 36 - k * 12)) + wait(1)
        w += _hold(kit, res, 1, mid, 2, lambda k: shake_defender(1, 1) if k == 0 else [])
        if n < 2:                                                              # *flex* - SNAP
            w += bmove(side, 264, 2, 0, 4) + _hold(kit, res, 1, mid, 2)
            w += se(s["crack"]) + emit_at(ZIP23, 0, 1, mid) + bmove(side, 264, 2, 0, -4) + shake_defender(2, 2) + wait(2)
    w += se(s["bslam"]) + func(34, 8, 0, 1, rgb(150, 150, 160), 10, 0) + emit_at(ZIPB23, 0, 1, (0, 30))
    for k in range(10):                                                        # *stuck*
        w += emit_at(ZIPB23, 1, 1, mid)
        if k % 3 == 0:
            w += shake_defender(1, 1)
        w += wait(1)
    return w


def _onion_breath(side, s):
    """DragonBreath (Onion Breath): a raw red onion, eaten like an apple - crunch (eyes watering) - crunch - then
    a big HAAAA right in the foe's face. Their eyes water and they lock up."""
    sx = _sx(side)
    mouth = _s23(side, 0, _p(side, (76, 110), (176, 64)))
    o = lambda kit, res: emit_at(kit, res, 0, mouth)
    w = se(s["pop"]) + _hold(ONION23, 1, 0, mouth, 4)
    for n, (kit, res) in enumerate(((ONION23, 2), (ONIONB23, 2))):            # crunch... crunch...
        w += se(s["bite"]) + se(s["crunch"]) + o(kit, res) + shake_attacker(1, 2) + wait(1)
        w += emit_at(ONION23, 0, 0, (sx * 4, 34)) + _hold(kit, res, 0, mouth, 4 + n)
    w += func(34, 2, 0, 1, rgb(140, 200, 255), 8, 0) + _hold(ONIONB23, 2, 0, mouth, 4)   # *sniff*... *...*
    w += se(s["gust"]) + bmove(side, 258, 2, sx * 6, 4)                        # HAAAAA
    w += emit_at(ONIONB23, _p(side, 0, 1), 0, (mouth[0] + sx * 6, mouth[1] + 2))
    for k in range(14):
        if k == 7:
            w += se(s["cough"]) + emit_at(ONION23, 0, 1, (0, 32)) + shake_defender(2, 2)
            w += func(34, 8, 0, 1, rgb(255, 240, 60), 13, 0)
        if k == 10:
            w += se(s["twave"]) + bmove(side, 264, 3, sx * 10, 0)
        w += wait(1)
    return w + bmove(side, 258, 3, -sx * 6, -4) + bmove(side, 264, 3, -sx * 10, 0) + wait(3)


def _rage_quit(side, s):
    """Outrage (Rage Quit): GAME OVER. Button mash... GAME OVER. They go red - the controller goes through the
    screen and bounces off the foe's head - and they just swing on the foe."""
    sx = _sx(side)
    mon = _s23(side, 0, _p(side, (106, 74), (154, 66)))
    pad = _s23(side, 0, _p(side, (86, 120), (166, 92)))
    dx, dy = TARGET_FROM_ATTACKER[side]
    screen = lambda r=1: emit_at(RAGE23, r, 0, mon)
    w = se(s["pop"]) + _hold(RAGE23, 1, 0, mon, 3)
    for n in range(2):                                                         # mash mash mash... GAME OVER
        for k in range(5 + n):
            w += screen() + emit_at(RAGEB23, 1, 0, (pad[0] + (k % 2) * 2 * sx, pad[1] + (k % 2)))
            if k % 2 == 0:
                w += se(s["lockon"]) + emit_at(RAGEB23, 0, 0, (pad[0], pad[1] + 6))
            w += wait(1)
        w += se(s["faint"]) + func(34, 2, 0, 1, rgb(255, 60, 40), 7 + 4 * n, 0)
        w += _hold(RAGE23, 1, 0, mon, 5, lambda k: emit_at(RAGEB23, 1, 0, pad))
    w += se(s["rage"]) + shake_attacker(2, 3) + emit_at(RAGEB23, 2, 0, (0, 24))
    w += _hold(RAGE23, 1, 0, mon, 3, lambda k: emit_at(RAGEB23, 1, 0, pad))
    w += se(s["whoosh"]) + _lob(RAGEB23, 1, side, pad, mon, 4, 12, lambda k: screen())   # *YEET*
    w += se(s["crack"]) + se(s["smash"]) + emit_at(RAGE23, 0, 0, mon) + flash_screen(2) + screen(2) + wait(1)
    w += _lob(RAGEB23, 1, side, mon, (dx, dy + 30), 4, 14, lambda k: screen(2))
    w += se(s["bonk"]) + shake_defender(2, 2) + screen(2) + wait(1)
    w += bmove(side, 258, 2, sx * 22, 8) + se(s["bslam"]) + flash_screen(3) + shake_defender(4, 3) + func(48)   # and swing
    w += _hold(RAGE23, 2, 0, mon, 2) + bmove(side, 258, 3, -sx * 22, -8)
    return w + _hold(RAGE23, 2, 0, mon, 5)
'''

TABLE = {304: ("_mall_ninja", ("NINJA23", "NINJAB23"), "Karate Chop"),
         305: ("_m80", ("M8023", "M80B23"), "DynamicPunch"),
         306: ("_zip_tie", ("ZIP23", "ZIPB23"), "Bind"),
         307: ("_onion_breath", ("ONION23", "ONIONB23"), "DragonBreath"),
         308: ("_rage_quit", ("RAGE23", "RAGEB23"), "Outrage")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
