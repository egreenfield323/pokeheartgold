# Plan: set 24 - thirty more (started 2026-11-02)

Read `.claude/plans/anim-set23-plan.md` first (same tools: `hood/test/reel/set23_lib.py`, `set23_fix.py`,
`reel.sh`), then the skill. Kits suffix `24`, variants 330-359, test-only turn-2 variants 360+.

## What the user asked for
"do 30 more" counting the moves that share animations, and "The big moves like hyper beam, giga impact, etc.
should have INSANE animations" (2026-11-02). INSANE = screen-filling, multi-phase, bg fades, screen shakes,
still a hood joke with the rule of three - the biggest thing in the game. Shared moves that get a new variant
are REMAPPED in battlefx.MOVES (Rock Throw keeps 13, Fury Attack keeps 3).

## Renames (applied 2026-11-02)
Giga Impact Car Crash -> 18 Wheeler; Crush Grip Death Grip -> Compactor; Magma Storm Lava Storm -> Flamin Hot;
Spike Cannon Nail Spray -> Staple Gun; Fissure Pothole -> Sinkhole; Trump Card Wild Card -> Reverse Card;
Teeter Dance Drunk Dance -> The Wobble. Descriptions written for all 30.

## The 30
### INSANE
- [x] 330 Hyper Beam = Full Auto: pistol - *click* jammed. An uzi - brrt, out of ammo. Then a MINIGUN on a tripod
      spins up... BRRRRRRT: the whole screen tracers + brass, flashes, shakes. Smoke clears. "RELOADING..."
- [x] 331 Giga Impact = 18 Wheeler: HONK. HONK. HOOOONK - an 18-wheeler barrels across the whole screen through the foe.
- [x] 332 Sacred Fire = Holy Fire: church organ. "CAN I GET AN AMEN?" ... "AMEN!" ... the clouds part, light shaft,
      a pillar of holy fire on the foe.
- [x] 333 Judgment = Sentencing: courtroom. BANG. BANG. "GUILTY" - a GIANT gavel from the sky flattens the foe.
- [x] 334 Roar of Time = Clock Out: the time clock 4:58... 4:59... 5:00 - CLOCK OUT - time freezes (sepia), clocks
      everywhere, a roar shockwave.
- [x] 335 Spacial Rend = Rip Space: a giant zipper unzips the screen: outer space behind it, the foe gets sucked in.
- [x] 336 Shadow Force = Ghost Ride (two turns): turn 1 they vanish under a bedsheet ghost; turn 2 a driverless
      minivan rolls in, ghost dancing on the roof, and rams the foe.
- [x] 337 Psycho Boost = Mind Blown: a chalkboard of math, ??? - more math, ??? - the third equation: galaxy explosion.
- [x] 338 Doom Desire = Bad Omen: a black cat crosses. A mirror cracks. Under a ladder. Then a shooting star crashes on them.
- [x] 339 Crush Grip = Compactor: the junkyard compactor squeezes the foe: crunch, crunch, CUBE.
- [x] 340 Magma Storm = Flamin Hot: one chip (sweat), two chips, the whole bag - volcano. (Replays as a trap: keep it tight.)
- [x] 341 Sky Attack = Air Strike (two turns): turn 1 pigeons line up on a wire; turn 2 pigeon squadron dive-bombs.
### Shared moves, their own now
- [x] 342 Rock Slide = Brick Wall: brick, brick, wall - then it falls on them.
- [x] 343 Triple Kick = Triple Tap: a tap shoe taps the foe (short, replays per hit).
- [x] 344 Pin Missile = Nail Gun: thunk thunk (short, per hit).
- [x] 345 Spike Cannon = Staple Gun: ka-chunk (short, per hit).
### New
- [x] 346 Spite = Petty   347 Nightmare = Bad Trip   348 Metronome = Wildin Out   349 Mimic = Bite Style
- [x] 350 Vital Throw = Bounced Out   351 SmellingSalt = Snap Out   352 Cotton Spore = Lint Trap   353 Trick = Bait Switch
- [x] 354 Teeter Dance = The Wobble   355 Crush Claw = Claw Machine   356 Tri Attack = Hat Trick   357 Trump Card = Reverse Card
- [x] 358 Morning Sun = Rise n Grind   359 Fissure = Sinkhole

## Log
- 2026-11-02: plan written, renames applied.
- 2026-11-02: batch 1 (330-334) built + reeled (s24b1, s24b1x). LESSONS: Holy Fire froze the game twice - suspects
  (both removed): 3 flame emitters started per tick (dozens alive) and a chained bg fade (0->10, 10->4, 4->0).
  Keep <= 1-2 new emitters per tick and only plain fade-in/fade-out pairs. tex slot 0 = 16x16 alpha, alpha1
  (tex 1) = 64x64. The pixel font has no '*'. set23_lib.apply(..., remap=[...]) moves shared moves.
  Pending re-check: Sentencing gavel head position, 18 Wheeler nose peek.
- 2026-11-02: batch 2 (335-339, test 360 = Ghost Ride turn 2) built + reeled (s24b2). Fixes after: ghost height on the
  van, galaxy height, mirror size. Compactor's ending not seen yet (reel ran out) - include 339 in the next reel.
- 2026-11-02: batch 3 (340-345, test 361 = Air Strike turn 2) built; 339-342 + 361 reeled clean (s24b3). 343-345 (per-hit
  ones) still to reel. Next: batch 4 = 346-350.
- 2026-11-02: ALL 30 built and reeled player-side (s24b4, s24b5, s24b6, s24fix, s24fix2). Late fixes: Sinkhole hole is
  screen-fixed (attacker-relative) because the foe drops through it; Ghost Ride van parks at x 128 so the ghost
  clears the foe box. Enemy side: hood/test/reel/enemy.sh (Cyndaquil uses Leer, Pidgey's FMJ plays the reel);
  en1 (330-335) clean. Running en2-en7 (rest of set 24 + set 23's 299-313).
- 2026-11-02: enemy side en2-en7 clean (set 24 + set 23's 299-313): every run ends back at "What will CYNDAQUIL
  do?". Full rebuild done (332 moves). hood-showcase.nds = all of set 24 (330-359 + test turn-2s 360/361),
  built with showcase(..., player_only=True) (45.5k words: the both-sides reel was 88k and won't load). Played
  start to finish from slot 6, no freeze. ALL DONE.
