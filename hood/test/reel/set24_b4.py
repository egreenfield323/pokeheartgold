"""Set 24 batch 4: Petty, Bad Trip, Wildin Out, Bite Style, Bounced Out (variants 346-350).
Run once from the repo root: python -X utf8 hood/test/reel/set24_b4.py  (art: set24_b4_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "PETTY24 PETTYB24 TRIP24 TRIPB24 WILD24 WILDB24 BITE24 CLUB24 CLUBB24".split()

KITS = '''
    # ---- set 24, batch 4 ----------------------------------------------------------------------------------
    # Petty (Spite): takes back the hoodie it gave the foe - the chain - "AND MY LIGHTER."
    b, rs = pk(PETTY24, {1: (fxart.grey_hoodie(), .9, 4, {}), 2: (fxart.cuban_link(), .5, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 255, 220), rgb(255, 255, 255), .35, 5, .14, life=10)
    fin(PETTY24, b, rs, (0, 1, 2))
    b, rs = pk(PETTYB24, {1: (fxart.cheap_lighter(), .4, 4, {}), 2: (fxart.line_bubble(["AND MY", "LIGHTER."]), ONE_TO_ONE, 4, {})})
    fin(PETTYB24, b, rs, (1, 2))

    # Bad Trip (Nightmare): the sleeping foe dreams of cash - then bills - then RENT DUE
    b, rs = pk(TRIP24, {1: (fxart.dream_cloud(), ONE_TO_ONE, 4, {}), 2: (fxart.dream_cloud(what="bills"), ONE_TO_ONE, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 240, 140), rgb(255, 255, 255), .35, 5, .1, life=14)
    fin(TRIP24, b, rs, (0, 1, 2))
    b, rs = pk(TRIPB24, {1: (fxart.dream_cloud(what="rent"), ONE_TO_ONE, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(130, 60, 170), n=6, life=22, scl=.32, up=.04)
    fin(TRIPB24, b, rs, (0, 1))

    # Wildin Out (Metronome): spin the prize wheel - tick tick tick... tick... ...tick - lands on ?
    b, rs = pk(WILD24, {1: (fxart.prize_wheel(), 1.1, 4, {}), 2: (fxart.prize_wheel(turn=15), 1.1, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 120, 220), rgb(120, 230, 255), .45, 14, .26, up=.12, gravity=.01, life=24)
    fin(WILD24, b, rs, (0, 1, 2))
    b, rs = pk(WILDB24, {1: (fxart.prize_wheel(turn=30), 1.1, 4, {}), 2: (fxart.prize_wheel(turn=121), 1.1, 4, {})})
    fin(WILDB24, b, rs, (1, 2))

    # Bite Style (Mimic): the foe hops - they hop. The foe sways - they sway. "STOP COPYING ME" - "STOP COPYING ME"
    b, rs = pk(BITE24, {1: (fxart.line_bubble(["STOP", "COPYING ME"]), ONE_TO_ONE, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 80, 60), rgb(255, 220, 200), .4, 6, .14, life=12)
    fin(BITE24, b, rs, (0, 1))

    # Bounced Out (Vital Throw): the velvet rope, THE LIST - the foe steps up, blocked - again - "UR NOT ON THE LIST",
    # and they get thrown out
    b, rs = pk(CLUB24, {1: (fxart.club_rope(), 1.2, 4, {}), 2: (fxart.list_clipboard(), ONE_TO_ONE, 4, {})}, alpha=fxart.soft_puff())
    puffs(b, rs, 0, rgb(200, 190, 175), n=6, life=20, scl=.32, up=.04)
    fin(CLUB24, b, rs, (0, 1, 2))
    b, rs = pk(CLUBB24, {1: (fxart.line_bubble(["UR NOT ON", "THE LIST"]), ONE_TO_ONE, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .55, 10, .3, life=10)
    fin(CLUBB24, b, rs, (0, 1))
'''

SCRIPTS = '''
def _petty(side, s):
    """Spite (Petty): the foe's wearing the hoodie the attacker gave them - yoink, back it comes. The chain - yoink.
    Then: "AND MY LIGHTER." - even the lighter."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    spots = {"hoodie": (0, 14), "chain": (0, 24), "lighter": (16, 12)}
    on = ["hoodie", "chain", "lighter"]
    art = {"hoodie": (PETTY24, 1), "chain": (PETTY24, 2), "lighter": (PETTYB24, 1)}
    dress = lambda: [w_ for n in on for w_ in emit_at(art[n][0], art[n][1], 1, spots[n])]
    bub = _p(side, (sx * 50, 58), (-40, 30))
    back = (sx * 14, 24)
    w = []
    for k in range(5):
        w += dress() + wait(1)
    for name in ("hoodie", "chain"):                                           # yoink... yoink
        on.remove(name)
        kit, res = art[name]
        w += se(s["whoosh"]) + _lob(kit, res, side, (dx + spots[name][0], dy + spots[name][1]), back, 5, 22, lambda k: dress())
        w += se(s["pop"]) + emit_at(PETTY24, 0, 0, back) + _hold(kit, res, 0, back, 2, lambda k: dress())
        w += shake_defender(1, 1) + _hold(PETTY24, 0, 0, back, 0) + dress() + wait(3)
    w += _hold(PETTYB24, 2, 0, bub, 12, lambda k: dress())                     # "AND MY LIGHTER."
    on.remove("lighter")
    w += se(s["whoosh"]) + _lob(PETTYB24, 1, side, (dx + 16, dy + 12), back, 5, 18)
    w += se(s["disable"]) + func(34, 8, 0, 1, rgb(140, 140, 150), 13, 0) + shake_defender(2, 2)
    return w + _hold(PETTYB24, 1, 0, back, 5)


def _bad_trip(side, s):
    """Nightmare (Bad Trip): the foe's asleep, dreaming of cash. The dream turns into a pile of bills. Then the
    landlord's door: RENT DUE. They toss and turn."""
    cloud = _p(side, (-28, 47), (36, 44))
    w = []
    for n, (kit, res, ticks) in enumerate(((TRIP24, 1, 10), (TRIP24, 2, 10), (TRIPB24, 1, 13))):
        w += se(s["sleep"] if n == 0 else s["confuse"] if n == 1 else s["nshade"])
        for k in range(ticks):
            w += emit_at(kit, res, 1, (cloud[0], cloud[1] + (k % 2 if n == 2 else 0)))
            if n == 0 and k == 4:
                w += emit_at(TRIP24, 0, 1, (cloud[0] + 4, cloud[1] + 6))
            if n == 1 and k == 4:
                w += shake_defender(1, 2)
            if n == 2 and k % 3 == 0:
                w += shake_defender(3, 1) + emit_at(TRIPB24, 0, 1, (0, 20))
            if n == 2 and k == 2:
                w += func(34, 8, 0, 1, rgb(140, 60, 180), 14, 0)
            w += wait(1)
    return w + wait(2)


def _wildin_out(side, s):
    """Metronome (Wildin Out): the prize wheel. Spin it - tick tick tick tick... tick... tick... ...tick. It lands on ?.
    Who knows what's coming."""
    wh = _s23(side, 0, (106, 82))
    frames = ((WILD24, 1), (WILD24, 2), (WILDB24, 1))
    w = se(s["pop"]) + _hold(WILD24, 1, 0, wh, 3) + bmove(side, 258, 2, _sx(side) * 6, 4) + se(s["whoosh"])
    k = 0
    for hold in (1,) * 12 + (2,) * 4 + (3,) * 2:                                # tick tick tick... tick...
        kit, res = frames[k % 3]
        w += se(s["clock"]) + _hold(kit, res, 0, wh, hold)
        k += 1
        if k == 2:
            w += bmove(side, 258, 2, -_sx(side) * 6, -4)
    w += wait(1) + se(s["clock"]) + _hold(WILDB24, 2, 0, wh, 4)                 # ...tick. ?
    w += se(s["confuse"]) + se(s["chaching"]) + emit_at(WILD24, 0, 0, (wh[0], wh[1] + 20))
    return w + _hold(WILDB24, 2, 0, wh, 10)


def _bite_style(side, s):
    """Mimic (Bite Style): the foe hops - the attacker hops. The foe leans - the attacker leans. "STOP COPYING ME" -
    "STOP COPYING ME"."""
    sx = _sx(side)
    fbub = _p(side, (-30, 36), (50, 58))
    abub = _p(side, (sx * 50, 58), (-40, 30))
    w = []
    for who, dxy in ((264, (0, 10)), (258, (0, 10)), (264, (-8, 0)), (258, (-8, 0))):
        w += bmove(side, who, 2, *dxy) + wait(2) + bmove(side, who, 2, -dxy[0], -dxy[1]) + wait(3)
        if who == 258:
            w += se(s["bling"]) + wait(1)
    for who, bub in ((1, fbub), (0, abub)):                                    # STOP COPYING ME
        w += se(s["rage"] if who == 1 else s["leer"])
        for k in range(10):
            w += emit_at(BITE24, 1, who, bub)
            if k == 3 and who == 1:
                w += shake_defender(1, 2)
            w += wait(1)
    w += emit_at(BITE24, 0, 1, (0, 40)) + func(34, 8, 0, 1, rgb(255, 60, 40), 12, 0) + shake_defender(2, 3)
    return w + wait(4)


def _bounced_out(side, s):
    """Vital Throw (Bounced Out): a velvet rope, the attacker with THE LIST. The foe steps up - blocked. Steps up
    again - blocked. "UR NOT ON THE LIST." And they get thrown clean out the club."""
    sx = _sx(side)
    rope = _s23(side, 0, (114, 84))
    clip = _p(side, (sx * 30, 44), (-34, 26))
    bub = _p(side, (sx * 50, 58), (-40, 30))
    step = _p(side, (-14, -4), (14, 6))
    scene = lambda: emit_at(CLUB24, 1, 0, rope) + emit_at(CLUB24, 2, 0, clip)
    w = se(s["pop"]) + _hold(CLUB24, 1, 0, rope, 3, lambda k: emit_at(CLUB24, 2, 0, clip))
    for n in range(2):                                                         # *steps up* - nah
        w += bmove(side, 264, 3, *step) + scene() + wait(1) + scene() + wait(1)
        w += se(s["lockon"]) + emit_at(CLUB24, 2, 0, (clip[0], clip[1] + 2)) + emit_at(CLUB24, 1, 0, (rope[0] + 2, rope[1])) + wait(1)
        w += bmove(side, 258, 2, 0, 4) + scene() + wait(1) + bmove(side, 258, 2, 0, -4) + scene() + wait(1)   # *shakes head*
        w += bmove(side, 264, 3, -step[0], -step[1]) + scene() + wait(1) + scene() + wait(2)
    for k in range(12):                                                        # UR NOT ON THE LIST
        w += scene() + emit_at(CLUBB24, 1, 0, bub) + wait(1)
    w += bmove(side, 258, 2, sx * 22, 8) + se(s["bslam"]) + flash_screen(2) + emit_at(CLUBB24, 0, 1, (0, 20))   # *GRABS*
    w += bmove(side, 264, 4, sx * 40, 40) + bmove(side, 258, 4, -sx * 22, -8)
    for k in range(4):
        w += scene() + wait(1)
    w += bmove(side, 264, 4, -sx * 40, -40) + se(s["bslam"]) + se(s["kaboom"]) + emit_at(CLUB24, 0, 1, (0, 0))
    w += shake_defender(4, 3) + func(68, 4, 4, 1, 3, 0) + func(48)
    return w + _hold(CLUB24, 1, 0, rope, 4, lambda k: emit_at(CLUB24, 2, 0, clip))
'''

TABLE = {346: ("_petty", ("PETTY24", "PETTYB24"), "Spite"),
         347: ("_bad_trip", ("TRIP24", "TRIPB24"), "Nightmare"),
         348: ("_wildin_out", ("WILD24", "WILDB24"), "Metronome"),
         349: ("_bite_style", ("BITE24",), "Mimic"),
         350: ("_bounced_out", ("CLUB24", "CLUBB24"), "Vital Throw")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
