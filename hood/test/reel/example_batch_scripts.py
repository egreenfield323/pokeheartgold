def _clown_on(side, s):
    """Torment (Clown On): a clown nose lobbed on - BOINK - a rainbow wig drops on - FLOP - giant clown shoes
    land on their feet - and the honk: CLOWNED."""
    sx = _sx(side)
    nose, wig, shoes = (-sx * 4, 14), (0, 32), (0, -10)
    have = []
    def dress(extra=0):
        w = []
        if "shoes" in have:
            w += emit_at(CLOWNB22, 2, 1, shoes)
        if "wig" in have:
            w += emit_at(CLOWN20, 2, 1, wig)
        if "nose" in have:
            w += emit_at(CLOWN20, 1, 1, nose)
        return w
    w = se(s["whoosh"]) + _lob(CLOWN20, 1, side, (sx * 22, 30), _foe_at(side, nose), 5, 22)
    have.append("nose")
    w += se(s["bonk"]) + shake_defender(1, 2)
    for k in range(3):
        w += dress() + wait(1)
    for k in range(4):                                                         # the wig drops
        y = round(wig[1] + 60 * (1 - (k + 1) / 4) ** 1.5)
        w += emit_at(CLOWN20, 1, 1, nose) + emit_at(CLOWN20, 2, 1, (wig[0], y)) + wait(1)
    have.append("wig")
    w += se(s["flop"]) + shake_defender(1, 1)
    for k in range(3):
        w += dress() + wait(1)
    for k in range(3):                                                         # the shoes
        w += dress() + emit_at(CLOWNB22, 2, 1, (shoes[0], shoes[1] + 30 - k * 10)) + wait(1)
    have.append("shoes")
    w += se(s["bonk"]) + shake_defender(1, 1)
    for k in range(4):                                                         # *...*
        w += dress() + wait(1)
    w += se(s["alarm"]) + emit_at(CLOWN20, 0, 1, (0, 40)) + func(34, 8, 0, 1, rgb(255, 80, 160), 12, 0)
    for k in range(12):                                                        # CLOWNED.
        w += emit_at(CLOWNB22, 1, 1, (0, 62)) + dress()
        if k == 5:
            w += se(s["alarm"]) + shake_defender(1, 1)
        w += wait(1)
    return w
# ====
def _spike_strip(side, s):
    """Stealth Rock (Spike Strip): a police spike strip unrolls across the foe's side - and a pizza moped,
    nobody on it, comes flying in - POP - POP - it sags flat - and the pizza flips onto the foe's head."""
    sx = _sx(side)
    strip = (-22, -6)
    sc_end = (strip[0] - 18, 4)
    w = se(s["sand"])
    for k in range(4):                                                         # *unrolls*
        w += emit_at(LEGO20, 1, 1, (strip[0] - (3 - k) * 14, strip[1])) + wait(1)
    w += se(s["bonk"])
    for k in range(5):                                                         # here comes the pizza
        t = k / 4
        w += emit_at(LEGO20, 1, 1, strip) + emit_at(LEGO20, 2, 1, (round(sc_end[0] - 110 * (1 - t)), sc_end[1]))
        if k == 0:
            w += se(s["skrrt"])
        w += wait(1)
    for k in range(2):                                                         # POP - POP
        w += se(s["pop"]) + emit_at(LEGO20, 0, 1, (sc_end[0] + (-14 if k == 0 else 14), sc_end[1] - 12))
        w += emit_at(LEGO20, 1, 1, strip) + emit_at(SPIKEB22 if k else LEGO20, 1 if k else 2, 1, sc_end) + shake_defender(1, 1) + wait(1)
        w += emit_at(LEGO20, 1, 1, strip) + emit_at(SPIKEB22 if k else LEGO20, 1 if k else 2, 1, sc_end) + wait(1)
    w += emit_at(SPIKEB22, 0, 1, sc_end) + se(s["whoosh"])
    for k in range(6):                                                         # the pizza flips up... and over
        t = (k + 1) / 6
        p = (round(sc_end[0] + (0 - sc_end[0]) * t), round(sc_end[1] + (30 - sc_end[1]) * t + 40 * (1 - (2 * t - 1) ** 2)))
        w += emit_at(LEGO20, 1, 1, strip) + emit_at(SPIKEB22, 1, 1, sc_end) + emit_at(SPIKEB22, 2, 1, p) + wait(1)
    w += se(s["splat"]) + se(s["bonk"]) + shake_defender(3, 2) + func(48)
    for k in range(10):
        w += emit_at(SPIKEB22, 2, 1, (0, 30)) + emit_at(LEGO20, 1, 1, strip) + emit_at(SPIKEB22, 1, 1, sc_end)
        if k == 2:
            w += func(34, 8, 0, 1, rgb(250, 200, 90), 12, 0)
        w += wait(1)
    return w
# ====
def _got_laced(side, s):
    """Grass Knot (Got Laced): the foe's laces tie themselves together - step... wobble - step... wobble -
    STEP - faceplant, a shoe flies off. "WHO TIED THESE?!\""""
    sx = _sx(side)
    lc = (0, -4)
    w = se(s["vwhip"]) + _hold(LACES20, 1, 1, lc, 3) + se(s["vwhip2"]) + _hold(LACES20, 1, 1, lc, 3)
    for k in range(2):                                                         # step... wobble
        w += bmove(side, 264, 2, -sx * 4, 3) + emit_at(LACES20, 1, 1, lc) + wait(1)
        w += shake_defender(2, 2) + _hold(LACES20, 1, 1, lc, 2) + bmove(side, 264, 2, sx * 4, -3) + _hold(LACES20, 1, 1, lc, 2)
    w += bmove(side, 264, 2, -sx * 14, -18) + se(s["bslam"]) + flash_screen(2) + emit_at(LACES20, 0, 1, (-sx * 20, -14))
    w += shake_defender(3, 2) + func(68, 3, 3, 1, 2, 0)
    for k in range(6):                                                         # the shoe flies off
        t = (k + 1) / 6
        w += emit_at(LACES20, 1, 1, (-sx * 14, -10)) + emit_at(LACES20, 2, 1, (round(sx * 40 * t), round(-6 + 70 * t - 40 * t * t))) + wait(1)
    bub = (-30, 36) if side == "player" else (40, 40)
    for k in range(12):                                                        # "WHO TIED THESE?!"
        w += emit_at(LACEB22, 1, 1, bub) + emit_at(LACES20, 1, 1, (-sx * 14, -10)) + wait(1)
    return w + bmove(side, 264, 5, sx * 14, 18) + wait(2)
# ====
def _inside_job(side, s):
    """Secret Power (Inside Job): a safe by the foe - dial... BZZT - dial... BZZT - then the door opens from the
    INSIDE: a guy in a ski mask. "IT WAS OPEN THE WHOLE TIME." Then a spring glove punches the foe."""
    sx = _sx(side)
    sf = (-sx * 36, 30) if side == "player" else (36, 34)
    w = se(s["bonk"]) + _hold(SAFE20, 1, 1, sf, 3)
    for n in range(2):                                                         # dial... BZZT
        for k in range(3):
            w += se(s["clock"]) + emit_at(SAFE20, 1, 1, sf) + wait(1)
        w += se(s["disable"]) + func(34, 2, 0, 1, rgb(255, 40, 40), 10, 0)
        for k in range(3):
            w += emit_at(SAFE20, 1, 1, (sf[0] + (2 if k % 2 else -2), sf[1])) + wait(1)
        w += _hold(SAFE20, 1, 1, sf, 2)
    w += _hold(SAFE20, 1, 1, sf, 3)                                           # *...*
    w += se(s["disable"]) + emit_at(SAFE20, 0, 1, (sf[0], sf[1] + 10))         # *creak*
    bub = (12, 42) if side == "player" else (-30, 60)
    for k in range(14):                                                        # "IT WAS OPEN THE WHOLE TIME"
        w += emit_at(SAFE20, 2, 1, sf)
        if k >= 2:
            w += emit_at(SAFEB22, 1, 1, bub)
        w += wait(1)
    dx = -sf[0] // 3
    w += se(s["whoosh"]) + emit_at(SAFE20, 2, 1, sf) + emit_at(SAFEB22, 2, 1, (sf[0] + dx, sf[1] - 6)) + wait(1)
    w += se(s["bslam"]) + flash_screen(3) + emit_at(SAFE20, 0, 1, (-sx * 8, 24)) + shake_defender(4, 2) + func(48)   # BOING
    for k in range(4):
        w += emit_at(SAFE20, 2, 1, sf) + emit_at(SAFEB22, 2, 1, (sf[0] + dx, sf[1] - 6)) + wait(1)
    return w + _hold(SAFE20, 2, 1, sf, 3)
# ====
def _parkour(side, s):
    """Rock Climb (Parkour): "PARKOUR!" - off the mailbox - off the fire hydrant - and a flip right down onto
    the foe."""
    dx, dy = TARGET_FROM_ATTACKER[side]
    p1 = (round(dx * .33), round(dy * .33) + 30)
    p2 = (round(dx * .66), round(dy * .66) + 40)
    box, hyd = (p1[0], p1[1] - 24), (p2[0], p2[1] - 22)
    street = lambda: emit_at(CLIMB20, 1, 0, box) + emit_at(CLIMB20, 2, 0, hyd)
    w = []
    for k in range(3):
        w += street() + wait(1)
    w += se(s["rage"])
    for k in range(8):                                                         # PARKOUR!
        w += street() + emit_at(PARKB22, 1, 0, (0, 58)) + wait(1)
    cur = (0, 0)
    for tgt, bonk in ((p1, True), (p2, True)):                                 # hop... hop
        w += se(s["whoosh"]) + bmove(side, 258, 3, tgt[0] - cur[0], tgt[1] - cur[1] + 10) + street() + wait(1)
        w += bmove(side, 258, 1, 0, -10) + se(s["bonk"]) + street() + wait(1) + street() + wait(1)
        cur = tgt
    w += se(s["whoosh"]) + bmove(side, 258, 3, (dx - cur[0]) // 2, 36) + street() + wait(1)   # flip...
    w += bmove(side, 258, 2, dx - cur[0] - (dx - cur[0]) // 2, dy + 14 - cur[1] - 36) + street() + wait(1)
    w += se(s["kaboom"]) + flash_screen(3) + emit_at(CLIMB20, 0, 1, (0, 20)) + shake_defender(4, 3)   # ...DOWN
    w += func(68, 4, 4, 1, 2, 0) + func(48)
    for k in range(3):
        w += street() + wait(1)
    w += bmove(side, 258, 6, -dx, -(dy + 14)) + street() + wait(1)
    for k in range(4):
        w += street() + wait(1)
    return w
