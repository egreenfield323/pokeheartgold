"""Set 24 batch 3: Flamin Hot, Air Strike, Brick Wall, Triple Tap, Nail Gun, Staple Gun (variants 340-345, test-only
361 = Air Strike's turn 2). Run once from the repo root: python -X utf8 hood/test/reel/set24_b3.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "HOT24 HOTB24 HOTC24 AIR24 AIRB24 WALL24 WALLB24 TAP24 NAIL24 NAILB24 STAPLE24 STAPLEB24".split()

KITS = '''
    # ---- set 24, batch 3 ----------------------------------------------------------------------------------
    # Flamin Hot (Magma Storm): one hot chip (sweat) - another (steam) - then the whole bag, and the foe ERUPTS in a
    # ring of fire
    b, rs = pk(HOT24, {1: (fxart.hot_chips(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.hot_chip(), .4, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(150, 210, 255), rgb(240, 250, 255), .3, 5, .1, up=.1, gravity=.016, life=16)
    fin(HOT24, b, rs, (0, 1, 2))
    b, rs = pk(HOTB24, {}, alpha=fxart.holy_flame())
    prop(b, rs, 0, tex=0, clr=rgb(255, 110, 20), clr_anm=(rgb(255, 240, 120), rgb(220, 30, 10)), scl=.42, life=18,
         gen=2, gen_intvl=1, emtr_life=28, init_pos=1, radius=1.5, axis=(0, 1, 0), vel=(0, .14), alpha=(31, 31, 0),
         scl_anm=(.4, 1.2, .5, 50, 160))
    burst(b, rs, 1, rgb(255, 120, 20), rgb(255, 250, 180), .45, 14, .2, up=.34, gravity=.02, life=24)
    fin(HOTB24, b, rs, (0, 1))
    b, rs = pk(HOTC24, {}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(240, 240, 245), n=6, life=22, scl=.32, up=.1)
    fin(HOTC24, b, rs, (0,))

    # Air Strike (Sky Attack): turn 1 - bread on the foe: a slice, a slice, the whole loaf. Turn 2 - one pigeon, two
    # pigeons, then the whole pigeon air force
    b, rs = pk(AIR24, {1: (fxart.bread_slice(), .45, 4, {}), 2: (fxart.bread_loaf(), .8, 4, {})}, alpha=fxart.feather())
    burst(b, rs, 0, rgb(200, 205, 215), rgb(255, 255, 255), .4, 8, .16, up=.08, gravity=.006, life=30, spin=0x0600)
    fin(AIR24, b, rs, (0, 1, 2))
    b, rs = pk(AIRB24, {2: (fxart.pigeon_dive(), .55, 4, {})}, alpha=fxart.feather())
    b, pg = added(b, fxart.pigeon_dive(), 24)
    spray2(b, rs, {"player": (-94, 150), "enemy": (-215, 91)}, (0, 24), 14, art_tex=pg, clr=rgb(255, 255, 255),
           clr_anm=(rgb(255, 255, 255), rgb(255, 255, 255)), scl=.5, gen=1, gen_intvl=2, emtr_life=40, radius=.5,
           spread=.03, alpha=(31, 31, 31))
    burst(b, rs, 3, rgb(200, 205, 215), rgb(255, 255, 255), .4, 12, .24, up=.1, gravity=.006, life=30, spin=0x0600)
    fin(AIRB24, b, rs, (0, 1, 2, 3))

    # Brick Wall (Rock Slide): bricks come down on the foe's head and stack up - one course, two, three - then the
    # whole wall topples
    b, rs = pk(WALL24, {1: (fxart.brick_wall(rows=1), 1.4, 4, {}), 2: (fxart.brick_wall(rows=2), 1.4, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(200, 180, 160), n=6, life=20, scl=.32, up=.03)
    fin(WALL24, b, rs, (0, 1, 2))
    b, rs = pk(WALLB24, {1: (fxart.brick_wall(), 1.4, 4, {}), 2: (fxart.brick_wall(tipped=35), 1.4, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(190, 70, 50), rgb(240, 140, 110), .5, 18, .3, up=.22, gravity=.022, life=26, spin=0x0800)
    fin(WALLB24, b, rs, (0, 1, 2))

    # Triple Tap (Triple Kick): a tap shoe on the foe's head - tap tap - STOMP (replays every hit: short)
    b, rs = pk(TAP24, {1: (fxart.tap_shoe(), .6, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(230, 235, 250), rgb(255, 255, 255), .4, 6, .16, life=10)
    fin(TAP24, b, rs, (0, 1))

    # Nail Gun (Pin Missile): thunk thunk thunk (replays every hit: short)
    b, rs = pk(NAIL24, {1: (fxart.nail_gun(), .7, 4, {}), 2: (flipx(fxart.nail_gun()), .7, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 120), rgb(255, 255, 255), .35, 5, .16, life=8)
    fin(NAIL24, b, rs, (0, 1, 2))
    b, rs = pk(NAILB24, {}, alpha=fxart.nail_streak())
    spray2(b, rs, {"player": (30, 26), "enemy": (-30, 16)}, (0, 24), 6, clr=rgb(210, 215, 225),
           clr_anm=(rgb(255, 255, 255), rgb(170, 175, 185)), scl=.32, gen=1, gen_intvl=3, emtr_life=18, radius=.05,
           spread=.02, alpha=(31, 31, 0))
    fin(NAILB24, b, rs, (0, 1))

    # Staple Gun (Spike Cannon): KA-CHUNK, KA-CHUNK - the foe stapled (replays every hit: short)
    b, rs = pk(STAPLE24, {1: (fxart.staple_gun(), .8, 4, {}), 2: (flipx(fxart.staple_gun()), .8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(230, 235, 250), rgb(255, 255, 255), .35, 5, .16, life=8)
    fin(STAPLE24, b, rs, (0, 1, 2))
    b, rs = pk(STAPLEB24, {2: (fxart.stuck_staple(), .35, 4, {})}, alpha=fxart.staple_bit())
    spray2(b, rs, {"player": (30, 26), "enemy": (-30, 16)}, (0, 24), 6, clr=rgb(220, 225, 235),
           clr_anm=(rgb(255, 255, 255), rgb(180, 185, 195)), scl=.36, gen=2, gen_intvl=4, emtr_life=14, radius=.08,
           spread=.03, alpha=(31, 31, 0))
    fin(STAPLEB24, b, rs, (0, 1, 2))
'''

SCRIPTS = '''
def _flamin_hot(side, s):
    """Magma Storm (Flamin Hot): a bag of flaming-hot chips. One chip in the foe's mouth - a bead of sweat. Another -
    steam out the ears. Then the WHOLE BAG - and the foe erupts in a ring of fire."""
    sx = _sx(side)
    bag = _s23(side, 0, _p(side, (100, 98), (150, 66)))
    mouth = _p(side, (0, 26), (0, 24))
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = se(s["pop"]) + _hold(HOT24, 1, 0, bag, 3)
    for n in range(2):                                                         # crunch... CRUNCH
        w += se(s["whoosh"]) + _lob(HOT24, 2, side, (bag[0], bag[1] + 20), (dx + mouth[0], dy + mouth[1]), 4, 14, lambda k: emit_at(HOT24, 1, 0, bag))
        w += se(s["crunch"]) + emit_at(HOT24, 1, 0, bag) + wait(1)
        w += func(34, 8, 0, 1, rgb(255, 70, 40), 6 + 5 * n, 0)
        w += emit_at(HOT24, 0, 1, (8, 40)) if n == 0 else emit_at(HOTC24, 0, 1, (0, 44)) + shake_defender(2, 2) + se(s["ember"])
        w += _hold(HOT24, 1, 0, bag, 5 + n)
    w += se(s["whoosh"]) + _lob(HOT24, 1, side, bag, (dx, dy + 34), 4, 18)    # THE WHOLE BAG
    w += se(s["crunch"]) + se(s["crunch"]) + _hold(HOT24, 1, 1, (0, 34), 3, lambda k: shake_defender(1, 1))
    w += func(33, 0, 1, 0, 10, rgb(120, 20, 0)) + se(s["kaboom"]) + se(s["flame"]) + flash_screen(5)   # *ERUPTS*
    w += emit_at(HOTB24, 0, 1, (0, 10)) + emit_at(HOTB24, 1, 1, (0, 30)) + func(68, 4, 4, 1, 8, 0)
    w += func(34, 8, 0, 1, rgb(255, 60, 20), 14, 0)
    for k in range(12):
        if k % 4 == 0:
            w += emit_at(HOTC24, 0, 1, (0, 46)) + shake_defender(2, 1)
        if k == 6:
            w += emit_at(HOTB24, 1, 1, (0, 30)) + se(s["ember"])
        w += wait(1)
    return w + func(33, 0, 1, 10, 0, rgb(120, 20, 0)) + wait(4)


def _air_strike(side, s):
    """Sky Attack (Air Strike), two turns. Turn 1: they bread the foe - a slice on their head, another slice, then the
    whole loaf. Coo. Turn 2: a pigeon dives in. Another. Then the entire pigeon air force."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    head = [(-6, 40), (8, 44)]
    on = []
    dress = lambda: [w_ for i in on for w_ in emit_at(AIR24, 1, 1, head[i])]
    one = []
    for n in range(2):                                                         # a slice... a slice...
        one += se(s["whoosh"]) + _lob(AIR24, 1, side, (sx * 22, 30), (dx + head[n][0], dy + head[n][1]), 5, 20, lambda k: dress())
        on.append(n)
        one += se(s["pop"]) + _hold(AIR24, 1, 1, head[n], 4, lambda k: dress())
    for k in range(4):                                                         # THE WHOLE LOAF
        one += emit_at(AIR24, 2, 1, (0, 50 + round(60 * (1 - (k + 1) / 4)))) + dress() + wait(1)
    one += se(s["bonk"]) + shake_defender(2, 2) + _hold(AIR24, 2, 1, (0, 50), 4, lambda k: dress())
    one += se(s["peck"]) + _hold(AIR24, 2, 1, (0, 50), 3, lambda k: dress() + (bmove(side, 264, 2, 0, 6) if k == 0 else []))
    one += se(s["peck"]) + _hold(AIR24, 2, 1, (0, 50), 4, lambda k: dress()) + bmove(side, 264, 2, 0, -6)   # *coo coo*
    two = []
    for n, frm in enumerate(((-150, 120), (150, 120))):                        # dive... dive...
        two += se(s["gust"])
        for k in range(5):
            t = ((k + 1) / 5) ** 1.4
            two += emit_at(AIRB24, 2, 1, (round(frm[0] * (1 - t)), round(40 + (frm[1] - 40) * (1 - t)))) + wait(1)
        two += se(s["peck"]) + emit_at(AIRB24, 3, 1, (0, 40)) + shake_defender(2, 2) + wait(3)
    two += func(33, 0, 1, 0, 8, rgb(60, 60, 80)) + se(s["gust"]) + se(s["peck"])   # THE AIR FORCE
    two += emit_at(AIRB24, _p(side, 0, 1), 0, _p(side, (-94, 150), (-215, 91)))
    for k in range(18):
        if k % 3 == 0:
            two += se(s["peck"]) + emit_at(AIRB24, 3, 1, (((k * 11) % 30) - 15, 30 + (k * 7) % 20)) + shake_defender(2, 1)
        if k == 9:
            two += flash_screen(3) + func(34, 8, 0, 1, rgb(170, 170, 180), 12, 0)
        two += wait(1)
    two += func(48) + func(33, 0, 1, 8, 0, rgb(60, 60, 80)) + wait(4)
    return one, two


def _air_strike_turn2_first(side, s):
    """Test only: Air Strike's second turn on its own."""
    return _air_strike(side, s)[1]


def _brick_wall(side, s):
    """Rock Slide (Brick Wall): bricks come down on the foe's head and stack up - one course, two courses, three - a
    whole wall on their head. It wobbles... and topples."""
    top = _p(side, (0, 60), (0, 60))
    w = []
    for n, (kit, res) in enumerate(((WALL24, 1), (WALL24, 2), (WALLB24, 1))):  # thud... thud... THUD
        for k in range(3):
            w += emit_at(kit, res, 1, (top[0], top[1] + round(60 * (1 - (k + 1) / 3)))) + wait(1)
        w += se(s["bslam"] if n == 2 else s["bonk"]) + emit_at(WALL24, 0, 1, (0, 34)) + shake_defender(1 + n, 1)
        w += _hold(kit, res, 1, top, 3 + n)
    for k in range(4):                                                         # *wobble*
        w += emit_at(WALLB24, 1, 1, (top[0] + (2 if k % 2 else -2), top[1])) + wait(1)
    w += emit_at(WALLB24, 2, 1, (top[0] + 6, top[1] - 4)) + wait(1) + emit_at(WALLB24, 2, 1, (top[0] + 10, top[1] - 10)) + wait(1)
    w += se(s["kaboom"]) + se(s["bslam"]) + flash_screen(3) + func(68, 4, 4, 1, 4, 0)   # CRASH
    w += emit_at(WALLB24, 0, 1, (0, 30)) + emit_at(WALL24, 0, 1, (0, 20)) + shake_defender(4, 3) + func(48)
    return w + wait(8)


def _triple_tap(side, s):
    """Triple Kick (Triple Tap): a tap shoe drops on the foe's head - tap, tap - STOMP. (Replays every hit.)"""
    head = (0, 44)
    w = se(s["whoosh"])
    for k in range(3):
        w += emit_at(TAP24, 1, 1, (head[0], head[1] + 30 - k * 10)) + wait(1)
    for k, dxx in enumerate((-6, 6)):                                          # tap tap
        w += se(s["dslap"]) + emit_at(TAP24, 1, 1, (head[0] + dxx, head[1])) + emit_at(TAP24, 0, 1, (head[0] + dxx, head[1] - 8)) + wait(1)
        w += emit_at(TAP24, 1, 1, (head[0] + dxx, head[1] + 4)) + wait(1)
    w += emit_at(TAP24, 1, 1, (head[0], head[1] + 10)) + wait(1)
    w += se(s["bonk"]) + se(s["dslap"]) + emit_at(TAP24, 1, 1, head) + emit_at(TAP24, 0, 1, (0, 36)) + flash_screen(1) + shake_defender(2, 2)
    return w + _hold(TAP24, 1, 1, head, 2) + emit_at(TAP24, 1, 1, (head[0], head[1] + 16)) + wait(2)


def _nail_gun(side, s):
    """Pin Missile (Nail Gun): a nail gun - thunk thunk thunk thunk. (Replays every hit.)"""
    sx = _sx(side)
    gun = _p(side, (sx * 30, 26), (-30, 16))
    res = _p(side, 1, 2)
    w = se(s["pop"]) + _hold(NAIL24, res, 0, gun, 2)
    w += emit_at(NAILB24, _p(side, 0, 1), 0, (gun[0] + sx * 16, gun[1] + 4))
    for k in range(10):
        w += emit_at(NAIL24, res, 0, (gun[0] - (sx * 2 if k % 3 == 0 else 0), gun[1]))
        if k % 3 == 0:
            w += se(s["peck"])
        if k % 3 == 2:
            w += emit_at(NAIL24, 0, 1, (((k * 9) % 20) - 10, 20 + (k * 5) % 16)) + shake_defender(1, 1)
        w += wait(1)
    return w + _hold(NAIL24, res, 0, gun, 2)


def _staple_gun(side, s):
    """Spike Cannon (Staple Gun): a heavy-duty staple gun - KA-CHUNK - KA-CHUNK - staples stuck all over the foe.
    (Replays every hit.)"""
    sx = _sx(side)
    gun = _p(side, (sx * 30, 26), (-30, 16))
    res = _p(side, 1, 2)
    spots = [(-10, 22), (10, 34), (0, 12)]
    on = []
    dress = lambda: [w_ for i in on for w_ in emit_at(STAPLEB24, 2, 1, spots[i])]
    w = se(s["pop"]) + _hold(STAPLE24, res, 0, gun, 2)
    w += emit_at(STAPLEB24, _p(side, 0, 1), 0, (gun[0] + sx * 16, gun[1] + 4))
    for n in range(3):                                                         # KA-CHUNK
        w += emit_at(STAPLE24, res, 0, (gun[0], gun[1] - 3)) + dress() + se(s["bslam"] if n == 2 else s["bonk"]) + wait(1)
        w += emit_at(STAPLE24, res, 0, gun) + dress() + wait(1)
        on.append(n)
        w += emit_at(STAPLE24, 0, 1, spots[n]) + shake_defender(1, 1) + emit_at(STAPLE24, res, 0, gun) + dress() + wait(1)
    return w + _hold(STAPLE24, res, 0, gun, 3, lambda k: dress())
'''

TABLE = {340: ("_flamin_hot", ("HOT24", "HOTB24", "HOTC24"), "Magma Storm"),
         341: ("_air_strike", ("AIR24", "AIRB24"), "Sky Attack"),
         342: ("_brick_wall", ("WALL24", "WALLB24"), "Rock Slide"),
         343: ("_triple_tap", ("TAP24",), "Triple Kick"),
         344: ("_nail_gun", ("NAIL24", "NAILB24"), "Pin Missile"),
         345: ("_staple_gun", ("STAPLE24", "STAPLEB24"), "Spike Cannon")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE, remap=tuple(m for _, _, m in TABLE.values()))
    p = set23_lib.ROOT / "hood/gunfx.py"
    s = p.read_text(encoding="utf-8")
    for a, b in (("            341: _air_strike,\n", "            341: _air_strike,\n            361: _air_strike_turn2_first,\n"),
                 ("        341: (AIR24, AIRB24,),\n", "        341: (AIR24, AIRB24,),\n        361: (AIR24, AIRB24,),\n")):
        assert s.count(a) == 1, a
        s = s.replace(a, b)
    p.write_text(s, encoding="utf-8", newline="")
