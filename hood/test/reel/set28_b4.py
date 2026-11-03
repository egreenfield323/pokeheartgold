"""Set 28 batch 4: Ice Pick, Blocked, Rat Tail, Kickback, Pass It On (variants 469-473).
Run once from the repo root: python -X utf8 hood/test/reel/set28_b4.py  (art: set28_b4_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "PICK28 DM28 DMB28 RAT28 RATB28 KICK28 POT28".split()

KITS = '''
    # ---- set 28, batch 4 ----------------------------------------------------------------------------------
    # Ice Pick (Icicle Spear): chip - chip - ice flying (replays per hit: short)
    b, rs = pk(PICK28, {1: (fxart.bar_ice_pick(), .7, 4, {}), 2: (flipx(fxart.bar_ice_pick()), .7, 4, {})}, alpha=fxart.ice_shard())
    burst(b, rs, 0, rgb(200, 235, 255), rgb(255, 255, 255), .3, 10, .26, up=.1, gravity=.012, life=16, spin=0x0800)
    fin(PICK28, b, rs, (0, 1, 2))

    # Blocked (Block): the foe texts - "hey" - "hey??" - BLOCKED
    b, rs = pk(DM28, {1: (fxart.dm_phone(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.dm_phone(stage=1), ONE_TO_ONE, 4, {"colors": 30})})
    fin(DM28, b, rs, (1, 2))
    b, rs = pk(DMB28, {1: (fxart.dm_phone(stage=2), ONE_TO_ONE, 4, {"colors": 30})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 120, 120), rgb(255, 255, 255), .45, 10, .24, life=12)
    fin(DMB28, b, rs, (0, 1))

    # Rat Tail (Poison Tail): a subway rat scurries up - stops - sniffs - WHIP - and it's gone
    b, rs = pk(RAT28, {1: (fxart.subway_rat(), 1.0, 4, {}), 2: (fxart.subway_rat(whip=True), 1.0, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(170, 70, 200), n=5, life=20, scl=.28, up=.06)
    fin(RAT28, b, rs, (0, 1, 2))
    b, rs = pk(RATB28, {1: (flipx(fxart.subway_rat()), 1.0, 4, {}), 2: (flipx(fxart.subway_rat(whip=True)), 1.0, 4, {})})
    fin(RATB28, b, rs, (1, 2))

    # Kickback (Metal Burst): they take it - take it - then pay it all back WITH INTEREST
    b, rs = pk(KICK28, {1: (fxart.interest_envelope(), ONE_TO_ONE, 4, {"colors": 30})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(130, 220, 110), rgb(255, 255, 220), .5, 18, .32, up=.08, life=18)
    fin(KICK28, b, rs, (0, 1))

    # Pass It On (Psycho Shift): a hot potato - hot hot hot - tossed - tossed back - tossed - stuck with it
    b, rs = pk(POT28, {1: (fxart.hot_potato(), .6, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(250, 250, 255), n=3, life=16, scl=.22, up=.07)
    fin(POT28, b, rs, (0, 1))
'''

SCRIPTS = '''
def _ice_pick(side, s):
    """Icicle Spear (Ice Pick): the bartender's ice pick - chip - chip - ice flying off the foe. (Replays per hit.)"""
    sx = _sx(side)
    res = _p(side, 1, 2)
    w = []
    for n in range(2):                                                         # chip... chip
        for k in range(2):
            w += emit_at(PICK28, res, 1, (-sx * (30 - k * 8), 40 - k * 8)) + wait(1)
        w += se(s["ishard"] if "ishard" in s else s["crack"]) + emit_at(PICK28, 0, 1, (-sx * 6, 24)) + shake_defender(1 + n, 1)
        w += _hold(PICK28, res, 1, (-sx * 22, 32), 2)
    return w + func(34, 8, 0, 1, rgb(190, 225, 255), 9, 0) + wait(3)


def _blocked(side, s):
    """Block (Blocked): the foe's phone - they text "hey". Nothing. "hey??". Nothing. Then the red banner: BLOCKED.
    The foe's not going anywhere."""
    sx = _sx(side)
    ph = _s23(side, 1, _p(side, (164, 74), (108, 92)))
    w = se(s["pop"]) + _hold(DM28, 1, 1, ph, 10)
    w += se(s["peck"]) + _hold(DM28, 2, 1, ph, 10, lambda k: shake_defender(1, 1) if k == 3 else [])
    w += se(s["bslam"]) + se(s["disable"]) + flash_screen(2) + emit_at(DMB28, 0, 1, ph)   # BLOCKED
    w += func(34, 8, 0, 1, rgb(100, 100, 110), 12, 0)
    for k in range(12):
        w += emit_at(DMB28, 1, 1, ph) + (func(48) + shake_defender(2, 1) if k in (4, 8) else []) + wait(1)
    return w + wait(4) + wait(8)


def _rat_tail(side, s):
    """Poison Tail (Rat Tail): a fat subway rat scurries up to the foe. Stops. Sniffs. Tail up - WHIP. Poisoned. It
    scurries off like nothing happened."""
    sx = _sx(side)
    kit = _p(side, RAT28, RATB28)
    y = _p(side, -8, 6)
    w = se(s["swipe"])
    for k in range(6):                                                         # scurry
        w += emit_at(kit, 1, 1, (-sx * (120 - k * 18), y + (k % 2))) + wait(1)
    w += _hold(kit, 1, 1, (-sx * 22, y), 6)                                    # sniff...
    w += se(s["twhip"] if "twhip" in s else s["vwhip"]) + _hold(kit, 2, 1, (-sx * 22, y), 2)   # WHIP
    w += se(s["bslam"]) + emit_at(RAT28, 0, 1, (0, 20)) + func(48) + shake_defender(3, 2) + func(34, 8, 0, 1, rgb(170, 70, 200), 12, 0)
    w += _hold(kit, 2, 1, (-sx * 22, y), 3)
    for k in range(6):                                                         # gone
        w += emit_at(kit, 1, 1, (-sx * (22 - k * 22), y + (k % 2))) + wait(1)
    return w + wait(8)


def _kickback(side, s):
    """Metal Burst (Kickback): they take it - wince - take it - then pay the foe back, a fat envelope stuffed with
    cash, WITH INTEREST. SLAP."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = []
    for n in range(2):                                                         # take it... take it
        w += se(s["bonk"]) + flash_screen(1) + shake_attacker(1 + n, 2) + func(34, 2, 0, 1, rgb(255, 120, 120), 9, 0) + wait(5)
    w += se(s["bling"]) + _hold(KICK28, 1, 0, (sx * 24, 40), 6)
    w += se(s["whoosh"]) + _lob(KICK28, 1, side, (sx * 24, 40), (dx, dy + 30), 5, 18)
    w += se(s["dslap"]) + se(s["bslam"]) + flash_screen(4) + emit_at(KICK28, 0, 1, (0, 30)) + shake_defender(4, 3)
    w += _hold(KICK28, 1, 0, (dx, dy + 30), 8) + func(48)
    return w


def _pass_it_on(side, s):
    """Psycho Shift (Pass It On): a hot potato in their hands - hot hot hot. Tossed to the foe - tossed back - tossed
    again. The foe's stuck with it."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    me, foe = (sx * 14, 30), (dx, dy + 26)
    w = se(s["ember"]) + func(34, 2, 0, 1, rgb(255, 120, 60), 9, 0)
    for k in range(5):                                                         # hot hot hot
        w += emit_at(POT28, 1, 0, (me[0] + (k % 2) * 3, me[1] + (k % 2) * 3)) + (emit_at(POT28, 0, 0, me) if k % 2 == 0 else []) + wait(1)
    for n, (a, b) in enumerate(((me, foe), (foe, me), (me, foe))):            # toss... back... toss
        w += se(s["whoosh"]) + _lob(POT28, 1, side, a, b, 4, 24)
        w += se(s["ember"]) + (func(48) + shake_defender(1, 1) if b is foe else shake_attacker(1, 1))
    w += se(s["burn"]) + func(34, 8, 0, 1, rgb(255, 120, 60), 12, 0)        # stuck with it
    for k in range(8):
        w += emit_at(POT28, 1, 0, (foe[0] + (k % 2) * 3, foe[1])) + (emit_at(POT28, 0, 0, foe) if k % 2 == 0 else []) + wait(1)
    return w + wait(8)
'''

TABLE = {469: ("_ice_pick", ("PICK28",), "Icicle Spear"),
         470: ("_blocked", ("DM28", "DMB28"), "Block"),
         471: ("_rat_tail", ("RAT28", "RATB28"), "Poison Tail"),
         472: ("_kickback", ("KICK28",), "Metal Burst"),
         473: ("_pass_it_on", ("POT28",), "Psycho Shift")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
