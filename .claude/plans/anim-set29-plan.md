# Plan: set 29 - the last 15 (started 2026-11-02)

Read `.claude/plans/anim-set28-plan.md` + 27 (tools, LESSONS). Kits suffix `29`, variants 484-498, test-only 499 =
Blow Dryer turn 2 first. Every batch: reel.sh + enemy.sh, then rebuild + showcase. Run testing straight through
(the user: "just do it") with a background ALLDONE watcher.

## Taken (on top of sets 27/28): ceiling fan (Air Cutter), shades (Leer, Stone Edge, Amnesia), DJ decks (Encore,
Horn Attack, Teeter Dance), riot shield (Light Screen), dumbbells (Superpower), phone battery % (Charge Beam),
Bootleg = Knock Off's name.

## Renames (applied, + all 15 descriptions)
Razor Wind Leaf Blower -> Blow Dryer; Weather Ball Weatherman -> Snow Globe; Mirror Shot Selfie Flash -> Spinners;
Psycho Cut Mind Cut -> Throw Shade; Copycat Biter -> Burned CD; Transform Body Double -> Face Swap; Sketch Copy
Style -> Caricature; Conversion 2 Remix -> B-Side; Swallow Chug It -> Take the L. Defog keeps Open Window (the
msg_0211 fog prompt reads fine).

## The 15
- [x] B1: 484 Razor Wind (Blow Dryer, 2 turns: plug in, low, HIGH / razor gusts), 485 Weather Ball (Snow Globe:
      shake, shake, the weather goes wild, thrown), 486 Mirror Shot (Spinners: spinner rims catch the sun, glare),
      487 Psycho Cut (Throw Shade: a lampshade thrown like a blade), 488 Copycat (Burned CD: sharpie-labeled CD in a
      boombox, skips, plays the copy)
- [x] B2: 489 Transform (Face Swap: phone filter scan), 490 Sketch (Caricature: easel, big-head drawing),
      491 Conversion (Rebrand: paint roller, new color), 492 Conversion 2 (B-Side: cassette flipped),
      493 Swallow (Take the L: a giant red L, gulp, heal)
- [x] B3: 494 Power Swap (Power Trade: pre-workout tub <-> chamomile tea; energy drink was Energy Ball's), 495 Guard Swap (Guard Trade: umbrellas swap),
      496 Arm Thrust (Shove Off: push broom, short - replays; foam finger was Psych Up's), 497 Cross Poison (Dirty Cross: spray-paint X tag),
      498 Defog (Open Window: window opens, pizza box fans the fog out)
- [x] Rebuild + showcase + tell the user. ALL MOVES DONE after this.

## Log
- 2026-11-02: plan written, renames + descriptions applied.
- 2026-11-02: all 3 batches reeled both sides + fixed. LESSON: func(48) must fire in the SAME tick as the shake (or
  before a bmove push) - started ticks later it catches the foe mid-shake and leaves it displaced till the next
  move. Applied to every set 28-29 script. Rebuilt; showcase 484-498 both sides. ALL 467 MOVES ANIMATED.
