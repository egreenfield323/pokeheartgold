"""Set 27 batch 4: Back Rub, Flu Shot, Bad Wind, Tat Gun, Cut Line (variants 439-443).
Run once from the repo root: python -X utf8 hood/test/reel/set27_b4.py  (art: set27_b4_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "RUB27 RUBB27 RUBC27 FLU27 FLUB27 WIND27 WINDB27 TAT27 TATB27 DELI27 DELIB27".split()

KITS = '''
    # ---- set 27, batch 4 ----------------------------------------------------------------------------------
    # Back Rub (Acupressure): the back scratcher - scratch scratch - ahh - then the stat slot machine spins: ATK!
    b, rs = pk(RUB27, {1: (fxart.back_scratcher(), .8, 4, {}), 2: (flipx(fxart.back_scratcher()), .8, 4, {})})
    fin(RUB27, b, rs, (1, 2))
    b, rs = pk(RUBB27, {1: (fxart.stat_slot(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.stat_slot(stat="ATK"), ONE_TO_ONE, 4, {"colors": 30})})
    fin(RUBB27, b, rs, (1, 2))
    b, rs = pk(RUBC27, {1: (fxart.stat_slot(stat="DEF"), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.stat_slot(stat="SPD"), ONE_TO_ONE, 4, {"colors": 30})},
               alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 230, 80), rgb(255, 255, 255), .5, 14, .26, up=.06, life=18)
    fin(RUBC27, b, rs, (0, 1, 2))

    # Flu Shot (Needle Arm): swab - the needle comes in - flinch - again - flinch - JAB
    b, rs = pk(FLU27, {1: (fxart.flu_syringe(), .9, 4, {}), 2: (flipx(fxart.flu_syringe()), .9, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .45, 10, .24, life=10)
    fin(FLU27, b, rs, (0, 1, 2))
    b, rs = pk(FLUB27, {1: (fxart.alcohol_swab(), .45, 4, {})})
    fin(FLUB27, b, rs, (1,))

    # Bad Wind (Ominous Wind): the elevator doors close on the foe - ding - green seeping out the seam - doors open
    b, rs = pk(WIND27, {1: (fxart.elevator_door(), 1.0, 4, {}), 2: (flipx(fxart.elevator_door()), 1.0, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(150, 200, 60), n=4, life=24, scl=.3, up=.05)
    fin(WIND27, b, rs, (0, 1, 2))
    b, rs = pk(WINDB27, {}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(200, 180, 255), rgb(255, 255, 255), .4, 10, .16, up=.08, life=20, radius=.5)
    fin(WINDB27, b, rs, (0,))

    # Tat Gun (Twineedle): bzzzzt - a MOM heart tattoo on the foe (replays per hit: short)
    b, rs = pk(TAT27, {1: (fxart.tattoo_gun(), .7, 4, {}), 2: (flipx(fxart.tattoo_gun()), .7, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(30, 40, 90), rgb(60, 70, 140), .2, 4, .1, gravity=.01, life=12)
    fin(TAT27, b, rs, (0, 1, 2))
    b, rs = pk(TATB27, {1: (fxart.mom_tattoo(), ONE_TO_ONE, 4, {"colors": 30})})
    fin(TATB27, b, rs, (1,))

    # Cut Line (Me First): NOW SERVING 48 - the foe's got 49 - ding, 49 - and they cut right in front
    b, rs = pk(DELI27, {1: (fxart.deli_sign(), ONE_TO_ONE, 4, {"colors": 30}), 2: (fxart.deli_sign(n="49"), ONE_TO_ONE, 4, {"colors": 30})})
    fin(DELI27, b, rs, (1, 2))
    b, rs = pk(DELIB27, {1: (fxart.deli_ticket(), ONE_TO_ONE / 2, 4, {"colors": 30})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .5, 12, .28, life=10)
    fin(DELIB27, b, rs, (0, 1))
'''

SCRIPTS = '''
def _back_rub(side, s):
    """Acupressure (Back Rub): the back scratcher - scratch, scratch - ohhh right there. Then the little stat slot
    machine over their head spins - ??? DEF SPD ATK DEF SPD... ATK."""
    sx = _sx(side)
    res = _p(side, 1, 2)
    slot = _p(side, (sx * 6, 66), (-30, 40))
    w = []
    for n in range(2):                                                         # scratch scratch
        w += se(s["swipe"])
        for k in range(5):
            w += emit_at(RUB27, res, 0, (-sx * 16, 24 + (k % 2) * 8 + n * 4)) + wait(1)
        w += func(34, 2, 0, 1, rgb(255, 210, 200), 8, 0) + wait(1)
    w += se(s["clock"])
    reel = [(RUBB27, 1), (RUBC27, 1), (RUBC27, 2), (RUBB27, 2)]
    for k in range(12):                                                        # it spins...
        kit, r = reel[k % 4]
        w += emit_at(kit, r, 0, slot) + (se(s["peck"]) if k % 2 == 0 else []) + wait(1 if k < 8 else 2)
    w += se(s["bling"]) + emit_at(RUBC27, 0, 0, slot) + func(34, 2, 0, 1, rgb(255, 120, 80), 12, 0)   # ATK!
    return w + _hold(RUBB27, 2, 0, slot, 10)


def _flu_shot(side, s):
    """Needle Arm (Flu Shot): an alcohol swab on the foe - the foe shivers. The needle comes in - they flinch away.
    It comes in again - flinch. Then: JAB."""
    sx = _sx(side)
    res = _p(side, 1, 2)
    arm = (-sx * 12, 20)
    w = []
    for k in range(5):                                                         # swab swab
        w += emit_at(FLUB27, 1, 1, (arm[0] + (k % 2) * 4, arm[1] + (k % 2) * 2)) + wait(1)
    w += shake_defender(1, 2) + wait(2)
    for n in range(2):                                                         # it comes in - flinch
        for k in range(3):
            w += emit_at(FLU27, res, 1, (-sx * (60 - k * 10), 22)) + wait(1)
        w += bmove(side, 264, 2, sx * 10, 0) + se(s["leer"])
        for k in range(3):
            w += emit_at(FLU27, res, 1, (-sx * (40 + k * 6), 22)) + wait(1)
        w += bmove(side, 264, 2, -sx * 10, 0) + wait(2)
    for k in range(3):                                                         # JAB
        w += emit_at(FLU27, res, 1, (-sx * (54 - k * 12), 22)) + wait(1)
    w += se(s["psting"]) + se(s["bslam"]) + flash_screen(3) + emit_at(FLU27, 0, 1, (-sx * 8, 22)) + shake_defender(4, 3)
    w += _hold(FLU27, res, 1, (-sx * 30, 22), 6) + func(48)
    return w + wait(2)


def _bad_wind(side, s):
    """Ominous Wind (Bad Wind): elevator doors slide shut on the foe - ding. Green starts seeping out the seam. More.
    The doors open: the foe's green and coughing - and the attacker's just whistling."""
    sx = _sx(side)
    door = lambda gap: emit_at(WIND27, 1, 1, (-16 - gap, 18)) + emit_at(WIND27, 2, 1, (16 + gap, 18))
    w = se(s["pop"])
    for k in range(5):                                                         # *shhhk* - closed
        w += door(30 - k * 7) + wait(1)
    w += se(s["bling"]) + _hold(WIND27, 1, 1, (-16, 18), 6, lambda k: emit_at(WIND27, 2, 1, (16, 18)))   # ding
    for k in range(14):                                                        # ...green
        w += door(0)
        if k % 3 == 0:
            w += emit_at(WIND27, 0, 1, (0, 8 + k))
        if k == 6:
            w += se(s["smog"])
        w += wait(1)
    w += se(s["pop"])
    for k in range(5):                                                         # doors open
        w += door(k * 7) + (emit_at(WIND27, 0, 1, (0, 20)) if k % 2 == 0 else []) + wait(1)
    w += se(s["cough"]) + func(34, 8, 0, 1, rgb(150, 200, 60), 13, 0) + shake_defender(2, 3)
    w += se(s["swagger"]) + emit_at(WINDB27, 0, 0, (0, 30)) + func(34, 2, 0, 1, rgb(220, 200, 255), 10, 0)   # *whistles*
    for k in range(8):
        w += (emit_at(WIND27, 0, 1, (0, 24)) if k % 3 == 0 else []) + wait(1)
    return w


def _tat_gun(side, s):
    """Twineedle (Tat Gun): the tattoo gun - bzzzzzt on the foe - and a MOM heart tattoo. (Replays per hit: short.)"""
    sx = _sx(side)
    res = _p(side, 1, 2)
    w = se(s["zap"])
    for k in range(7):                                                         # bzzzzt
        w += emit_at(TAT27, res, 1, (-sx * (14 + (k % 2) * 2), 30 + (k % 2))) + (emit_at(TAT27, 0, 1, (-sx * 2, 18)) if k % 3 == 0 else [])
        w += (se(s["zap"]) if k == 4 else []) + (shake_defender(1, 1) if k == 3 else []) + wait(1)
    w += se(s["bling"]) + _hold(TATB27, 1, 1, (0, 16), 8)
    return w


def _cut_line(side, s):
    """Me First (Cut Line): the deli counter - NOW SERVING 48. The foe's holding ticket 49. *ding* - 49! The foe steps
    up... and the attacker cuts right in front, no ticket, and gets served first."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    sign = _s23(side, 0, _p(side, (110, 62), (118, 70)))
    tkt = (sx * 18, 26)
    w = se(s["pop"]) + _hold(DELI27, 1, 0, sign, 8, lambda k: emit_at(DELIB27, 1, 1, tkt))
    w += se(s["bling"]) + _hold(DELI27, 2, 0, sign, 4, lambda k: emit_at(DELIB27, 1, 1, tkt))   # *ding* 49
    w += bmove(side, 264, 3, -sx * 10, 0) + _hold(DELI27, 2, 0, sign, 3, lambda k: emit_at(DELIB27, 1, 1, tkt))
    w += se(s["whoosh"]) + bmove(side, 258, 3, dx - sx * 36, dy)               # CUTS IN
    w += _hold(DELI27, 2, 0, sign, 2, lambda k: emit_at(DELIB27, 1, 1, tkt))
    w += se(s["bslam"]) + flash_screen(3) + emit_at(DELIB27, 0, 1, (0, 20)) + bmove(side, 264, 2, sx * 14, 0)
    w += _hold(DELI27, 2, 0, sign, 6, lambda k: emit_at(DELIB27, 1, 1, tkt))
    w += bmove(side, 258, 4, -(dx - sx * 36), -dy) + bmove(side, 264, 3, -sx * 4, 0) + wait(3) + func(48)
    return w + wait(2)
'''

TABLE = {439: ("_back_rub", ("RUB27", "RUBB27", "RUBC27"), "Acupressure"),
         440: ("_flu_shot", ("FLU27", "FLUB27"), "Needle Arm"),
         441: ("_bad_wind", ("WIND27", "WINDB27"), "Ominous Wind"),
         442: ("_tat_gun", ("TAT27", "TATB27"), "Twineedle"),
         443: ("_cut_line", ("DELI27", "DELIB27"), "Me First")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
