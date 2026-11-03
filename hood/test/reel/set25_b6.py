"""Set 25 batch 6: Thumbtacks, Copy Paste, Receipts, Max Out, Hustle (variants 387-391).
Run once from the repo root: python -X utf8 hood/test/reel/set25_b6.py  (art: set25_b6_art.py, already in fxart)"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import set23_lib  # noqa: E402

NAMES = "TACK25 COPY25 COPYB25 REC25 RECB25 GYM25 GYMB25 HUST25".split()

KITS = '''
    # ---- set 25, batch 6 ----------------------------------------------------------------------------------
    # Thumbtacks (Spikes): a tack on the foe's side - another - then the whole box spills
    b, rs = pk(TACK25, {1: (fxart.tack_box(), ONE_TO_ONE, 4, {}), 2: (fxart.thumbtack(), .4, 4, {})})
    b, tk = added(b, fxart.thumbtack(), 24)
    burst(b, rs, 0, rgb(255, 255, 255), rgb(255, 255, 255), .35, 16, .3, up=.16, gravity=.02, life=40, tex=tk,
          clr_anm=(rgb(255, 255, 255), rgb(255, 255, 255)), alpha=(31, 31, 31))
    fin(TACK25, b, rs, (0, 1, 2))

    # Copy Paste (Mirror Move): the copier - a blank page - a smudged page - a perfect copy
    b, rs = pk(COPY25, {1: (fxart.photocopier(), 1.0, 4, {}), 2: (fxart.copy_page(), .5, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(150, 255, 170), rgb(255, 255, 255), .45, 6, .14, life=10)
    fin(COPY25, b, rs, (0, 1, 2))
    b, rs = pk(COPYB25, {1: (fxart.copy_page(quality=1), .5, 4, {}), 2: (fxart.copy_page(quality=2), .5, 4, {})})
    fin(COPYB25, b, rs, (1, 2))

    # Receipts (Bide): the receipt printer - it keeps printing - and printing - then they whip the foe with it
    b, rs = pk(REC25, {1: (fxart.receipt_printer(), .9, 4, {}), 2: (fxart.long_receipt(), .6, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .55, 12, .3, life=12)
    fin(REC25, b, rs, (0, 1, 2))
    b, rs = pk(RECB25, {1: (fxart.long_receipt(), 1.3, 4, {})})
    fin(RECB25, b, rs, (1,))

    # Max Out (Superpower): curl the dumbbell - press the barbell - then lift the whole vending machine and throw it
    b, rs = pk(GYM25, {1: (fxart.dumbbell(), .6, 4, {}), 2: (fxart.oly_barbell(), 1.2, 4, {})}, alpha=fxart.fizz_drop())
    burst(b, rs, 0, rgb(150, 210, 255), rgb(240, 250, 255), .3, 4, .1, up=.1, gravity=.016, life=14)
    fin(GYM25, b, rs, (0, 1, 2))
    b, rs = pk(GYMB25, {1: (fxart.vending_machine(), 1.1, 4, {})}, alpha=fxart.speck())
    burst(b, rs, 0, rgb(220, 60, 60), rgb(250, 230, 120), .45, 18, .32, up=.2, gravity=.02, life=24, spin=0x0A00)
    fin(GYMB25, b, rs, (0, 1))

    # Hustle (Struggle): open the wallet - a moth - shake it - nothing - so they just swing
    b, rs = pk(HUST25, {1: (fxart.moth_wallet(), .8, 4, {})}, alpha=fxart.tiny_spark())
    burst(b, rs, 0, rgb(255, 250, 200), rgb(255, 255, 255), .45, 8, .22, life=10)
    fin(HUST25, b, rs, (0, 1))
'''

SCRIPTS = '''
def _thumbtacks(side, s):
    """Spikes (Thumbtacks): a box of thumbtacks. One flicked onto the foe's side - plink. Another - plink. Then they
    dump the whole box and tacks bounce everywhere."""
    sx = _sx(side)
    box = _p(side, (sx * 30, 40), (-34, 26))
    dx, dy = TARGET_FROM_ATTACKER[side]
    spots = [(-24, -2), (22, 2)]
    on = []
    dress = lambda: [w_ for i in on for w_ in emit_at(TACK25, 2, 1, spots[i])]
    w = se(s["pop"]) + _hold(TACK25, 1, 0, box, 3)
    for n in range(2):                                                         # plink... plink...
        w += se(s["whoosh"]) + _lob(TACK25, 2, side, box, (dx + spots[n][0], dy + spots[n][1]), 5, 20, lambda k: emit_at(TACK25, 1, 0, box) + dress())
        on.append(n)
        w += se(s["tspikes"]) + _hold(TACK25, 1, 0, box, 4, lambda k: dress())
    w += se(s["whoosh"]) + _lob(TACK25, 1, side, box, (dx - sx * 20, dy + 20), 4, 16, lambda k: dress())   # THE WHOLE BOX
    w += se(s["tspikes"]) + se(s["bonk"]) + emit_at(TACK25, 0, 1, (0, 10)) + shake_defender(2, 2)
    for k in range(12):
        w += dress() + (se(s["tspikes"]) if k % 4 == 0 else []) + wait(1)
    return w + func(34, 8, 0, 1, rgb(255, 80, 80), 9, 0) + wait(2)


def _copy_paste(side, s):
    """Mirror Move (Copy Paste): the office copier. Press start - out comes a blank page. Again - a smudged mess.
    Again - a perfect copy. *bling*"""
    sx = _sx(side)
    cp = _s23(side, 0, (106, 84))
    tray = (cp[0] - sx * 26, cp[1] + 2)
    w = se(s["pop"]) + _hold(COPY25, 1, 0, cp, 3)
    for n, (kit, res) in enumerate(((COPY25, 2), (COPYB25, 1), (COPYB25, 2))):
        w += se(s["lockon"]) + emit_at(COPY25, 0, 0, (cp[0], cp[1] + 10))
        for k in range(4):                                                     # *whirr*
            w += emit_at(COPY25, 1, 0, (cp[0] + (k % 2), cp[1])) + (se(s["rollout"]) if k == 0 else []) + wait(1)
        for k in range(3):                                                     # *the page slides out*
            w += emit_at(COPY25, 1, 0, cp) + emit_at(kit, res, 0, (tray[0] - sx * k * 6, tray[1] + k * 4)) + wait(1)
        out = (tray[0] - sx * 12, tray[1] + 8)
        if n == 0:
            w += _hold(kit, res, 0, out, 4, lambda k: emit_at(COPY25, 1, 0, cp)) + shake_attacker(1, 1)
        elif n == 1:
            w += se(s["disable"]) + _hold(kit, res, 0, out, 4, lambda k: emit_at(COPY25, 1, 0, cp)) + shake_attacker(2, 2)
        else:
            w += se(s["bling"]) + flash_screen(2) + _hold(kit, res, 0, out, 8, lambda k: emit_at(COPY25, 1, 0, cp) + (emit_at(COPY25, 0, 0, out) if k == 1 else []))
    return w + wait(2)


def _receipts(side, s):
    """Bide (Receipts): the receipt printer starts printing. And printing. And PRINTING - CVS long. Then they snatch
    the whole thing and whip the foe with it - every receipt paid back double."""
    sx = _sx(side)
    pr = _s23(side, 0, (106, 86))
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = se(s["pop"]) + _hold(REC25, 1, 0, pr, 3)
    for n, (kit, res, h) in enumerate(((REC25, 2, 22), (RECB25, 1, 40))):    # print... print... PRINT
        w += se(s["rollout"])
        for k in range(6 + 2 * n):
            w += emit_at(REC25, 1, 0, pr) + emit_at(kit, res, 0, (pr[0], pr[1] + 8 + round(h * (k + 1) / (6 + 2 * n)))) + wait(1)
        w += _hold(REC25, 1, 0, pr, 3, lambda k: emit_at(kit, res, 0, (pr[0], pr[1] + 8 + h)))
    w += se(s["swipe"]) + _lob(RECB25, 1, side, (pr[0], pr[1] + 48), (dx, dy + 30), 4, 16, lambda k: emit_at(REC25, 1, 0, pr))   # *WHIP*
    w += se(s["dslap"]) + se(s["bslam"]) + flash_screen(3) + emit_at(REC25, 0, 1, (0, 26)) + shake_defender(3, 2)
    w += se(s["dslap"]) + flash_screen(3) + shake_defender(3, 2) + func(48)    # (double)
    return w + _hold(REC25, 1, 0, pr, 4)


def _max_out(side, s):
    """Superpower (Max Out): curl the dumbbell - up, down. Press the barbell - up, down, shaking. Then they lift the
    whole vending machine over their head... and throw it at the foe."""
    sx = _sx(side)
    db = (sx * 26, 30)
    over = (0, 66)
    dx, dy = TARGET_FROM_ATTACKER[side]
    w = []
    for k in range(6):                                                         # curl, curl
        w += emit_at(GYM25, 1, 0, (db[0], db[1] + (10 if k % 3 == 1 else 0))) + (se(s["harden"]) if k % 3 == 1 else []) + wait(1)
    for k in range(8):                                                         # press, press (shaking)
        w += emit_at(GYM25, 2, 0, (over[0] + (k % 2), over[1] + (8 if k % 4 in (1, 2) else 0)))
        if k % 4 == 1:
            w += se(s["harden"]) + shake_attacker(1, 1)
        if k == 6:
            w += emit_at(GYM25, 0, 0, (0, 40))
        w += wait(1)
    w += se(s["focus"])
    for k in range(8):                                                         # *the vending machine*
        w += emit_at(GYMB25, 1, 0, (over[0] + (k % 2) * 2, over[1] + min(k, 4) * 3))
        if k % 3 == 0:
            w += shake_attacker(2, 1)
        w += wait(1)
    w += se(s["whoosh"]) + _lob(GYMB25, 1, side, (over[0], over[1] + 12), (dx, dy + 24), 5, 24)   # *THROWS IT*
    w += se(s["kaboom"]) + se(s["bslam"]) + flash_screen(5) + func(68, 5, 5, 1, 5, 0) + emit_at(GYMB25, 0, 1, (0, 24))
    w += shake_defender(4, 3) + func(48) + func(34, 2, 0, 1, rgb(120, 140, 200), 10, 0)
    return w + wait(4)


def _hustle(side, s):
    """Struggle (Hustle): no moves left. They open the wallet - a moth flies out. Shake it - nothing. So they just
    start swinging, wild. (Hurts them too.)"""
    sx = _sx(side)
    wl = (sx * 26, 32)
    w = se(s["pop"]) + _hold(HUST25, 1, 0, wl, 5, lambda k: se(s["astonish"]) if k == 1 else [])
    for k in range(6):                                                         # *shake shake* - nothing
        w += emit_at(HUST25, 1, 0, (wl[0] + (4 if k % 2 else -4), wl[1])) + (se(s["disable"]) if k == 4 else []) + wait(1)
    w += _hold(HUST25, 1, 0, wl, 3)
    for n in range(3):                                                         # swing, swing, SWING
        w += bmove(side, 258, 2, sx * 18, 6) + se(s["bonk"] if n < 2 else s["bslam"]) + emit_at(HUST25, 0, 1, (((n * 13) % 20) - 10, 24))
        w += shake_defender(1 + n, 1) + bmove(side, 258, 2, -sx * 18, -6) + wait(1)
    w += func(48) + shake_attacker(2, 2) + func(34, 2, 0, 1, rgb(255, 80, 80), 9, 0)   # (recoil)
    return w + wait(3)
'''

TABLE = {387: ("_thumbtacks", ("TACK25",), "Spikes"),
         388: ("_copy_paste", ("COPY25", "COPYB25"), "Mirror Move"),
         389: ("_receipts", ("REC25", "RECB25"), "Bide"),
         390: ("_max_out", ("GYM25", "GYMB25"), "Superpower"),
         391: ("_hustle", ("HUST25",), "Struggle")}

if __name__ == "__main__":
    set23_lib.apply(NAMES, KITS, SCRIPTS, TABLE)
