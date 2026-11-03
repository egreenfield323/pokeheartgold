"""Set 23 batch 3: Sawing Logs, Snuck Him, Fence Hop, Trap House, Muah (variants 309-313).
Run once from the repo root: python -X utf8 hood/test/reel/set23_b3.py  (art: set23_b3_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "LOG23 LOGB23 LOGC23 SNUCK23 SNUCKB23 FENCE23 TRAP23 KISS23 KISSB23".split()

KITS = '''
    # ---- set 23, batch 3 ----------------------------------------------------------------------------------
    # Sawing Logs (Snore): Z... a handsaw on a log - Z... - then a CHAINSAW, and the split log flies at the foe
    b, rs = pk(LOG23, {1: (fxart.log_side(), .9, 4, {}), 2: (fxart.handsaw(), .7, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(225, 190, 130), rgb(255, 240, 200), .3, 5, .12, up=.08, gravity=.014, life=14)
    fin(LOG23, b, rs, (0, 1, 2))
    b, rs = pk(LOGB23, {1: (fxart.chainsaw(), .8, 4, {}), 2: (fxart.log_half(), .6, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(225, 190, 130), rgb(255, 240, 200), .35, 12, .22, up=.12, gravity=.016, life=16)
    fin(LOGB23, b, rs, (0, 1, 2))
    b, rs = pk(LOGC23, {1: (fxart.big_z_snore(), .55, 4, {})})
    fin(LOGC23, b, rs, (1,))

    # Snuck Him (Mach Punch): "YO LOOK A BIRD" - nah - "IS THAT FREE WIFI?" - nah - "FREE MONEY!" - POW
    b, rs = pk(SNUCK23, {1: (fxart.line_bubble(["YO LOOK", "A BIRD!"]), ONE_TO_ONE, 4, {}),
                         2: (fxart.line_bubble(["IS THAT", "FREE WIFI?"]), ONE_TO_ONE, 4, {})})
    fin(SNUCK23, b, rs, (1, 2))
    b, rs = pk(SNUCKB23, {1: (fxart.line_bubble(["YO!", "FREE MONEY!"]), ONE_TO_ONE, 4, {}),
                          2: (fxart.impact_star(), 1.3, 8, {"scl_anm": (.3, 1.2, 1.0, 60, 255)})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .5, 10, .28, life=10)
    fin(SNUCKB23, b, rs, (0, 1, 2))

    # Fence Hop (Hi Jump Kick): run at the fence - rattle - again - then the dog behind it barks and they CLEAR it,
    # knee first into the foe
    b, rs = pk(FENCE23, {1: (fxart.chain_fence(), ONE_TO_ONE, 4, {}), 2: (fxart.guard_dog(), .8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 220), rgb(255, 255, 255), .55, 10, .26, life=10)
    burst(b, rs, 3, rgb(200, 205, 215), rgb(255, 255, 255), .35, 4, .1, up=.04, life=8)
    fin(FENCE23, b, rs, (0, 1, 2, 3))

    # Trap House (Spider Web): a glue trap with cheese on it - the foe sniffs - leans - steps on it. Stuck.
    b, rs = pk(TRAP23, {1: (fxart.glue_trap(), 1.05, 4, {}), 2: (fxart.cheese_wedge(), .3, 4, {})}, alpha=fxart.glue_strand())
    burst(b, rs, 0, rgb(250, 220, 60), rgb(255, 255, 180), .5, 10, .1, up=.1, gravity=.006, life=22)
    fin(TRAP23, b, rs, (0, 1, 2))

    # Muah (Sweet Kiss): a blown kiss lands - another - then the foe's phone: WHO IS SHE??
    b, rs = pk(KISS23, {1: (fxart.lipstick_kiss(), .58, 4, {})}, alpha=fxart.heart())
    burst(b, rs, 0, rgb(255, 90, 150), rgb(255, 220, 235), .4, 6, .12, up=.08, life=18)
    burst(b, rs, 2, rgb(255, 230, 60), rgb(255, 255, 220), .4, 6, .08, up=.02, life=24, radius=.5)
    fin(KISS23, b, rs, (0, 1, 2))
    b, rs = pk(KISSB23, {1: (fxart.phone_who(), ONE_TO_ONE, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 255), rgb(255, 255, 255), .35, 4, .14, life=8)
    fin(KISSB23, b, rs, (0, 1))
'''

SCRIPTS = '''
def _sawing_logs(side, s):
    """Snore (Sawing Logs): out cold - a Z - a handsaw saws a log in time with the snore. Z - saw saw. Then the
    snore goes CHAINSAW, the log splits and both halves fly into the foe."""
    head = _s23(side, 0, _p(side, (66, 112), (185, 52)))
    log = _s23(side, 0, (110, 84))
    saw = (log[0] + 2, log[1] + 14)
    dx, dy = TARGET_FROM_ATTACKER[side]
    zz = lambda k: emit_at(LOGC23, 1, 0, (head[0] + k * 3, head[1] + 8 + k * 5))
    w = se(s["pop"]) + _hold(LOG23, 1, 0, log, 3)
    for n in range(2):                                                         # zzz... saw saw
        w += se(s["sleep"])
        for k in range(7):
            w += emit_at(LOG23, 2, 0, (saw[0] + (6 if k % 2 else -6), saw[1])) + emit_at(LOG23, 1, 0, log) + zz(k)
            if k % 2 == 0:
                w += se(s["swipe"]) + emit_at(LOG23, 0, 0, (log[0], log[1] + 6))
            w += wait(1)
        if n == 1:
            w += shake_defender(1, 1)
        w += _hold(LOG23, 1, 0, log, 3)
    w += se(s["sleep"])
    for k in range(9):                                                         # zzzZZZ - VRRRRRRR
        w += emit_at(LOGB23, 1, 0, (saw[0] + (k % 2) * 3, saw[1] + 2 + (k % 3))) + emit_at(LOG23, 1, 0, log) + zz(k % 7)
        if k % 2 == 0:
            w += se(s["zap"]) + emit_at(LOGB23, 0, 0, (log[0], log[1] + 8))
        if k == 4:
            w += shake_defender(1, 2)
        w += wait(1)
    w += se(s["crack"])                                                        # *CRACK* - both halves at the foe
    a = _arc((log[0] - 8, log[1]), (dx - 10, dy + 30), 6, 22)
    b_ = _arc((log[0] + 8, log[1]), (dx + 10, dy + 18), 6, 30)
    for k in range(1, 6):
        w += emit_at(LOGB23, 2, 0, a[k]) + emit_at(LOGB23, 2, 0, b_[k]) + wait(1)
    w += se(s["bonk"]) + se(s["bslam"]) + flash_screen(3) + shake_defender(4, 3) + func(48)
    return w + wait(2) + se(s["sleep"]) + wait(1) + emit_at(LOGC23, 1, 0, (head[0], head[1] + 10)) + wait(1) + zz(1) + wait(1) + zz(2) + wait(2)


def _snuck_him(side, s):
    """Mach Punch (Snuck Him): "YO LOOK, A BIRD!" - the foe doesn't fall for it. "IS THAT FREE WIFI?" - nope.
    "YO! FREE MONEY!" - the foe whips round - POW."""
    sx = _sx(side)
    bub = _p(side, (sx * 50, 58), (-40, 30))
    w = []
    for n, (kit, res) in enumerate(((SNUCK23, 1), (SNUCK23, 2))):
        for k in range(9):
            w += emit_at(kit, res, 0, bub)
            if k == 5:
                w += bmove(side, 264, 1, 3, 0)                                 # *nah*
            if k == 6:
                w += bmove(side, 264, 1, -6, 0)
            if k == 7:
                w += bmove(side, 264, 1, 3, 0)
            w += wait(1)
        w += wait(2)
    for k in range(5):                                                         # "YO! FREE MONEY!"
        w += emit_at(SNUCKB23, 1, 0, bub)
        if k == 2:
            w += se(s["chaching"]) + bmove(side, 264, 2, sx * 20, 6)          # *whips round*
        w += wait(1)
    w += bmove(side, 258, 2, sx * 22, 8) + se(s["kaboom"]) + se(s["bslam"]) + flash_screen(4)   # POW
    w += emit_at(SNUCKB23, 2, 1, (-sx * 10, 24)) + emit_at(SNUCKB23, 0, 1, (0, 24)) + shake_defender(4, 3) + func(48)
    w += bmove(side, 258, 4, -sx * 22, -8) + wait(3) + bmove(side, 264, 3, -sx * 20, -6)
    return w + wait(3)


def _fence_hop(side, s):
    """Hi Jump Kick (Fence Hop): a chain-link fence, BEWARE OF DOG. They run at it - rattle - bounce off. Again.
    Then the dog pops up behind it barking, and they clear the fence in one jump - knee first into the foe."""
    fence = _s23(side, 1, (106, 86))
    dog = (fence[0] + 4, fence[1] + 12)
    run = _p(side, (24, 30), (-34, 4))
    leap = _p(side, (92, 54), (-96, -46))
    f = lambda dxy=(0, 0): emit_at(FENCE23, 1, 1, (fence[0] + dxy[0], fence[1] + dxy[1]))
    w = se(s["pop"]) + _hold(FENCE23, 1, 1, fence, 4)
    for n in range(2):                                                         # run - CLANG - bounce
        w += se(s["whoosh"]) + bmove(side, 258, 3, *run) + f() + wait(1) + f() + wait(1)
        w += se(s["bonk"]) + emit_at(FENCE23, 3, 1, fence) + shake_attacker(1, 2)
        for k in range(4):
            w += f(((2 if k % 2 else -2), 0)) + wait(1)
        w += bmove(side, 258, 3, -run[0], -run[1]) + _hold(FENCE23, 1, 1, fence, 4 + n)
    for k in range(6):                                                         # WOOF WOOF
        y = fence[1] + min(k, 3) * 4
        w += f() + emit_at(FENCE23, 2, 1, (dog[0], y))
        if k in (2, 4):
            w += se(s["rage"]) + shake_attacker(2, 1)
        w += wait(1)
    w += se(s["whoosh"]) + bmove(side, 258, 4, *leap)                          # *clears it*
    for k in range(3):
        w += f() + emit_at(FENCE23, 2, 1, dog) + wait(1)
    w += se(s["kaboom"]) + se(s["bslam"]) + flash_screen(4) + emit_at(FENCE23, 0, 1, (0, 24))   # KNEE
    w += shake_defender(4, 3) + func(48) + func(68, 4, 4, 1, 3, 0)
    w += _hold(FENCE23, 1, 1, fence, 3, lambda k: emit_at(FENCE23, 2, 1, dog) + (se(s["rage"]) if k == 1 else []))
    w += bmove(side, 258, 5, -leap[0], -leap[1])
    return w + _hold(FENCE23, 1, 1, fence, 4, lambda k: emit_at(FENCE23, 2, 1, dog) if k < 2 else [])


def _trap_house(side, s):
    """Spider Web (Trap House): a glue trap slides in with a wedge of cheese on it. The foe sniffs. Leans in. Then
    steps right on it - SQUELCH - and can't get off. Ain't leaving the trap house."""
    trap = _s23(side, 0, _p(side, (224, 74), (104, 122)))
    cheese = (trap[0], trap[1] - 2)
    onto = _p(side, (39, 18), (40, 31))
    sx_in = _p(side, 1, -1)
    t = lambda: emit_at(TRAP23, 1, 0, trap)
    w = se(s["whoosh"])
    for k in range(4):                                                         # slides in
        w += emit_at(TRAP23, 1, 0, (trap[0] + sx_in * round(70 * (1 - (k + 1) / 4)), trap[1])) + wait(1)
    for k in range(3):
        w += t() + emit_at(TRAP23, 2, 0, (cheese[0], cheese[1] + 24 - k * 8)) + wait(1)
    w += se(s["pop"]) + _hold(TRAP23, 1, 0, trap, 3, lambda k: emit_at(TRAP23, 2, 0, cheese))
    for n, lean in enumerate((8, 16)):                                         # *sniff*... *sniff sniff*
        w += se(s["sscent"]) + bmove(side, 264, 3, sx_in * lean, 0)
        w += _hold(TRAP23, 1, 0, trap, 4 + n, lambda k: emit_at(TRAP23, 2, 0, cheese))
        w += bmove(side, 264, 3, -sx_in * lean, 0) + _hold(TRAP23, 1, 0, trap, 3, lambda k: emit_at(TRAP23, 2, 0, cheese))
    w += bmove(side, 264, 4, onto[0], onto[1])                                 # *steps on it*
    w += _hold(TRAP23, 1, 0, trap, 2, lambda k: emit_at(TRAP23, 2, 0, cheese))
    w += se(s["splat"]) + emit_at(TRAP23, 0, 0, (trap[0], trap[1] + 10)) + func(34, 8, 0, 1, rgb(250, 220, 60), 9, 0)
    for k in range(3):                                                         # pull... pull... STUCK
        w += se(s["sludge"]) + bmove(side, 264, 2, 0, 6) + t() + wait(1) + t() + wait(1)
        w += bmove(side, 264, 2, 0, -6) + emit_at(TRAP23, 0, 0, (trap[0], trap[1] + 12)) + shake_defender(1, 1) + t() + wait(1)
    w += _hold(TRAP23, 1, 0, trap, 6)
    return w + bmove(side, 264, 4, -onto[0], -onto[1]) + _hold(TRAP23, 1, 0, trap, 2)


def _muah(side, s):
    """Sweet Kiss (Muah): blows a kiss - MUAH - a lipstick print lands on the foe. Another one. They're blushing.
    Then their phone buzzes: WHO IS SHE?? Now they're confused."""
    sx = _sx(side)
    mouth = _p(side, (sx * 10, 30), (-10, 24))
    marks = [_p(side, (-10, 20), (-10, 20)), _p(side, (12, 34), (12, 32))]
    phone = _p(side, (-79, -5), (46, 40))
    dx, dy = TARGET_FROM_ATTACKER[side]
    on = []
    dress = lambda: [w_ for i in on for w_ in emit_at(KISS23, 1, 1, marks[i])]
    w = []
    for n in range(2):                                                         # muah... muah
        w += se(s["attract"]) + bmove(side, 258, 2, sx * 6, 3) + wait(1) + bmove(side, 258, 2, -sx * 6, -3)
        w += _lob(KISS23, 1, side, mouth, (dx + marks[n][0], dy + marks[n][1]), 5, 14, lambda k: dress())
        on.append(n)
        w += se(s["dslap"]) + emit_at(KISS23, 0, 1, (0, 30)) + func(34, 8, 0, 1, rgb(255, 120, 170), 8 + 3 * n, 0)
        w += _hold(KISS23, 1, 1, marks[n], 4, lambda k: dress())
    w += _hold(KISS23, 1, 1, marks[0], 3, lambda k: dress())                   # *...*
    for k in range(14):                                                        # bzz bzz - WHO IS SHE??
        w += emit_at(KISSB23, 1, 1, (phone[0] + (1 if k % 2 else -1) * (2 if k < 6 else 0), phone[1])) + dress()
        if k in (0, 3):
            w += se(s["alarm"]) + emit_at(KISSB23, 0, 1, (phone[0], phone[1] + 30))
        if k == 6:
            w += bmove(side, 264, 3, -sx * 8, 0)                               # *reads it*
        w += wait(1)
    w += se(s["confuse"]) + emit_at(KISS23, 2, 1, (0, 40)) + bmove(side, 264, 3, sx * 8, 0)
    for k in range(8):                                                         # ...uhhh
        w += emit_at(KISSB23, 1, 1, phone) + dress()
        if k in (1, 4):
            w += bmove(side, 264, 2, (6 if k == 1 else -6), 0) + shake_defender(1, 1)
        w += wait(1)
    return w + wait(2)
'''

TABLE = {309: ("_sawing_logs", ("LOG23", "LOGB23", "LOGC23"), "Snore"),
         310: ("_snuck_him", ("SNUCK23", "SNUCKB23"), "Mach Punch"),
         311: ("_fence_hop", ("FENCE23",), "Hi Jump Kick"),
         312: ("_trap_house", ("TRAP23",), "Spider Web"),
         313: ("_muah", ("KISS23", "KISSB23"), "Sweet Kiss")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
