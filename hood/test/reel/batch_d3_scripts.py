def _stab_combo(side, s):
    """Fury Cutter (Stab Combo): slash - "2 HIT!" - slash slash - "3 HIT!" - slash slash slash - "5 HIT COMBO!"
    - they go for a sixth - the foe ducks and clocks them. COMBO BREAKER!"""
    sx = _sx(side)
    sign = (6, 60) if side == "player" else (30, 50)
    w = []
    for n, (cnt, sres, sps) in enumerate(((2, 2, SLASH20), (1, 0, COMBO20), (2, 1, COMBO20))):
        for c in range(cnt):
            w += bmove(side, 258, 1, sx * 10, 3) + emit_at(SLASH20, 1, 1, (0, 20)) + emit_at(SLASH20, 0, 1, (0, 20))
            w += se(s["slash"]) + shake_defender(2, 1) + bmove(side, 258, 1, -sx * 10, -3) + wait(1)
        w += emit_at(sps, sres, 1, sign) + se(s["bling"] if n < 2 else s["chaching"]) + wait(3)
    w += flash_screen(3) + func(48) + wait(5)
    w += bmove(side, 258, 2, sx * 16, 4) + se(s["whoosh"]) + bmove(side, 264, 2, 0, -10) + wait(2)   # a sixth... *ducks*
    w += bmove(side, 264, 2, 0, 10) + se(s["bslam"]) + flash_screen(2) + shake_attacker(4, 3)        # *CLOCKED*
    w += bmove(side, 258, 3, -sx * 16, -4)
    for k in range(10):                                                        # COMBO BREAKER!
        w += emit_at(COMBOB22, 1, 1, sign)
        if k == 0:
            w += se(s["kaboom"]) + func(34, 2, 0, 1, rgb(255, 60, 60), 12, 0)
        w += wait(1)
    return w
# ====
def _ride_or_die(side, s):
    """Destiny Bond (Ride or Die): handcuffs - CLICK on the attacker - CLICK on the foe - a chain between them -
    then the attacker throws the key away. Way away. *distant splash*. Ride or die."""
    sx = _sx(side)
    cuff_a = (sx * 16, 24) if side == "player" else (-16, 18)
    cuff_f = (-sx * 12, 22) if side == "player" else (12, 18)
    both = lambda: emit_at(BFF20, 1, 0, cuff_a) + emit_at(BFF20, 1, 1, cuff_f)
    w = se(s["disable"]) + _hold(BFF20, 1, 0, cuff_a, 4)                      # CLICK
    w += se(s["disable"]) + shake_defender(1, 1)
    for k in range(4):                                                         # CLICK
        w += both() + wait(1)
    w += emit_at(LINK20, 0 if side == "player" else 1, 0, (cuff_a[0], cuff_a[1])) + se(s["dteam"])
    for k in range(8):                                                         # *chained*
        w += both() + wait(1)
    key = (sx * 22, 44) if side == "player" else (-22, 36)
    w += _hold(BFF20, 2, 0, key, 3, lambda k: both())                          # the key...
    w += se(s["whoosh"])
    for k in range(6):                                                         # ...YEET
        t = (k + 1) / 6
        w += both() + emit_at(BFF20, 2, 0, (round(key[0] - sx * 150 * t), round(key[1] + 80 * t - 30 * t * t))) + wait(1)
    for k in range(5):                                                         # *...*
        w += both() + wait(1)
    w += se(s["splash"])                                                       # *plip* - somewhere far away
    for k in range(8):
        w += both()
        if k == 2:
            w += shake_attacker(1, 2) + shake_defender(1, 2) + func(34, 8, 0, 1, rgb(160, 40, 220), 12, 0)
        w += wait(1)
    return w
