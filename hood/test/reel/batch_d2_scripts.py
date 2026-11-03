def _peep_game(side, s):
    """Detect (Peep Game): the foe lunges - the attacker is already a step to the side - again - then the
    attacker holds up the foe's own playbook: PLAN: HIT EM. PEEPED."""
    sx = _sx(side)
    board = (sx * 42, 44) if side == "player" else (-40, 30)
    w = []
    for n in range(2):                                                         # lunge... *already gone*
        w += bmove(side, 258, 2, -sx * 16, 0) + wait(1)
        w += se(s["whoosh"]) + bmove(side, 264, 3, -sx * 26, -8) + wait(3)
        w += se(s["leer"]) + bmove(side, 264, 3, sx * 26, 8) + bmove(side, 258, 2, sx * 16, 0) + wait(3)
    w += se(s["disable"]) + _hold(SCOPE20, 1, 0, board, 4)                     # *the playbook*
    w += func(34, 8, 0, 1, rgb(255, 255, 160), 13, 0) + shake_defender(2, 2)
    for k in range(12):                                                        # PEEPED.
        w += emit_at(SCOPE20, 1, 0, board)
        if k >= 2:
            w += emit_at(SCOPE20, 2, 0, (0, 60) if side == "player" else (0, 50))
        if k == 2:
            w += se(s["bonk"]) + emit_at(SCOPE20, 0, 0, (0, 30))
        w += wait(1)
    return w + func(34, 2, 0, 1, rgb(255, 255, 200), 12, 0) + wait(2)
# ====
def _zaza_storm(side, s):
    """Leaf Storm (Zaza Storm): the TV weather report - LIGHT... MODERATE... SEVERE ZAZA WARNING - and the
    storm hits: waves of leaves bury the foe."""
    sx = _sx(side)
    tv = (sx * 40, 44) if side == "player" else (-40, 30)
    r = 0 if side == "player" else 1
    w = []
    for kit, res, ticks, snd in ((ZAZAB22, 1, 6, "clock"), (ZAZAB22, 2, 6, "clock"), (ZAZAC22, 1, 10, "alarm")):
        w += se(s[snd]) + _hold(kit, res, 0, tv, ticks, lambda k: (flash_screen(2) + shake_attacker(1, 1)) if (k == 2 and res == 1 and kit == ZAZAC22) else [])
    w += se(s["twister"]) + func(33, 0, 1, 0, 6, rgb(90, 180, 60))
    for k in range(3):                                                         # wave, wave, wave
        w += emit_at(LEAVES20, r, 0, (0, 10 + k * 8)) + se(s["leaf"]) + bmove(side, 258, 2, 0, 3) + wait(2)
        w += bmove(side, 258, 2, 0, -3) + se(s["gust"]) + wait(2)
    for k in range(12):
        if k % 3 == 0:
            w += shake_defender(2, 1) + se(s["leaf"])
        w += wait(1)
    return w + func(34, 8, 0, 1, rgb(90, 200, 70), 13, 0) + func(48) + func(33, 0, 1, 6, 0, rgb(90, 180, 60)) + wait(4)
# ====
def _dip_out(side, s):
    """Teleport (Dip Out): they sneak to the EXIT - rattle - locked - rattle - LOCKED - so they dive straight
    out the window instead. Glass everywhere. Gone."""
    sx = _sx(side)
    door = (sx * 40, 40) if side == "player" else (-40, 26)
    win = (-sx * 34, 60) if side == "player" else (34, 30)
    room = lambda broken=False: emit_at(EXIT20, 1, 0, door) + emit_at(DIPB22 if broken else EXIT20, 1 if broken else 2, 0, win)
    w = []
    for k in range(3):
        w += room() + wait(1)
    w += bmove(side, 258, 3, sx * 12, 0) + room() + wait(1)                    # *sneaks over*
    for n in range(2):                                                         # rattle... LOCKED
        for k in range(4):
            w += emit_at(EXIT20, 1, 0, (door[0] + (2 if k % 2 else -2), door[1])) + emit_at(EXIT20, 2, 0, win)
            if k % 2 == 0:
                w += se(s["bonk"])
            w += wait(1)
        w += shake_attacker(1, 1)
        for k in range(4):
            w += room() + wait(1)
    w += se(s["whoosh"]) + bmove(side, 258, 3, (win[0] - sx * 12) // 2, 26) + room() + wait(1)   # *dive*
    w += se(s["smash"]) + se(s["crack"]) + emit_at(EXIT20, 0, 0, (win[0] - sx * 12, win[1] - 26)) + func(40, 2, 1)
    for k in range(10):                                                        # gone.
        w += room(True) + wait(1)
    w += bmove(side, 258, 1, -(win[0] - sx * 12) // 2 - sx * 12, -26) + room(True) + wait(1)
    for k in range(4):
        w += room(True) + wait(1)
    return w + func(40, 2, 0) + wait(2)
# ====
def _spit_bars(side, s):
    """Spit Up (Spit Bars): they spit BARS - literally. A steel bar flies at the foe - CLANG - another - CLANG -
    then a whole jail cell slams down over them. LOCKED UP."""
    sx = _sx(side)
    dx, dy = TARGET_FROM_ATTACKER[side]
    mouth = (sx * 14, 34) if side == "player" else (-14, 28)
    w = []
    for n in range(2):                                                         # ptoo... CLANG
        w += se(s["spray"]) + shake_attacker(1, 1) + emit_at(MOUTH20, 0, 0, mouth)
        w += stop_motion(MOUTH20, 1, 0, mouth, (dx - sx * 6, dy + 22), 4, ease=1.2)
        w += se(s["ishard"]) + se(s["bonk"]) + shake_defender(2, 2) + wait(3)
    w += se(s["spray"]) + shake_attacker(2, 1) + wait(2)
    for k in range(4):                                                         # *the cell drops*
        w += emit_at(SPITB22, 1, 1, (0, 22 + round(70 * (1 - (k + 1) / 4) ** 1.5))) + wait(1)
    w += se(s["bslam"]) + se(s["kaboom"]) + flash_screen(3) + shake_defender(4, 3) + func(48) + func(68, 4, 4, 1, 2, 0)
    for k in range(12):                                                        # LOCKED UP.
        w += emit_at(SPITB22, 2, 1, (0, 64)) + emit_at(SPITB22, 1, 1, (0, 22))
        if k == 2:
            w += se(s["disable"])
        w += wait(1)
    return w
# ====
def _post_up(side, s):
    """Ingrain (Post Up): a lawn chair - they sit - a cooler - then a whole grill, fired up. They are NOT
    moving. Healing every beat."""
    sx = _sx(side)
    ch = (sx * 12, 14) if side == "player" else (-12, 4)
    cool = (sx * 46, 26) if side == "player" else (-40, 10)
    grill = (-sx * 34, 34) if side == "player" else (34, 20)
    have = []
    def camp():
        w = emit_at(CHAIR20, 1, 0, ch)
        if "cooler" in have:
            w += emit_at(CHAIR20, 2, 0, cool)
        if "grill" in have:
            w += emit_at(POSTB22, 1, 0, grill)
        return w
    w = se(s["bonk"]) + camp() + wait(2) + bmove(side, 258, 3, 0, -6) + se(s["flop"]) + camp() + wait(2)
    for what in ("cooler", "grill"):                                           # ...and a cooler... and a GRILL
        w += func(34, 2, 0, 1, rgb(120, 255, 140), 12, 0) + se(s["absorb"])
        for k in range(4):
            w += camp() + wait(1)
        have.append(what)
        w += se(s["bonk"] if what == "cooler" else s["flame"]) + camp() + wait(1)
        if what == "grill":
            w += emit_at(POSTB22, 0, 0, (grill[0], grill[1] + 20))
    for k in range(12):                                                        # *not moving*
        w += camp()
        if k % 4 == 0:
            w += emit_at(CHAIR20, 0, 0, (0, 30)) + func(34, 2, 0, 1, rgb(120, 255, 140), 12, 0)
        if k == 6:
            w += emit_at(POSTB22, 0, 0, (grill[0], grill[1] + 20))
        w += wait(1)
    return w + bmove(side, 258, 3, 0, 6) + camp() + wait(1)
