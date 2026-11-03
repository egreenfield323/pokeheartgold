# Plan: set 23 - thirty new move animations (started 2026-11-02)

**Read this whole file first, then `.claude/skills/hood-battle-animations/SKILL.md`, then the "Environment" and
"How a redo batch is applied" sections of `.claude/plans/anim-redo-plan.md` (same tools, same rules).**
Tick boxes as soon as a move is built AND watched in DeSmuME. Log at the bottom (`plan_log.py` writes to the
OTHER plan file; edit this one by hand).

## What the user asked for
"pick 30 new moves and create animations for them. also if move names aren't hood/funny enough, change them"
(2026-11-02). The bar is the gold standard (Scam Likely / Rental Lambo / Crossover): a recognizable hood
situation, rule of three, a comic pause, the hit growing out of the joke, the foe reacting, words only when
they ARE the punchline. All-new art. Clear of the HP boxes (clipcheck every reel).

## How new moves differ from the redo batches
These moves had NO hood animation: each gets a NEW variant number (299-328), a `MOVES` entry in
`hood/battlefx.py`, new `VARIANTS`/`KITS` entries, and kits starting at **567** (`LAST_KIT` after set 22 is
`COMBOB22` = 566). Constants are suffixed `23` (MILK23, ...). Kit code goes before the
`    # ---- set 21: common-move redo` comment in `build_files`; scripts go after `_crossover` area (anywhere
before `VARIANTS = {`). Batch scripts: `hood/test/reel/set23_bN.py` (+ `set23_bN_art.py` appended to fxart,
`set23_bN_scripts.py`).
Multi-hit moves replay the animation per hit and Bind/Outrage/Petal Dance replay it every turn: keep those short.

## Renames (moves.json -> apply_move_names.py; descriptions -> move_desc.json -> apply_move_desc.py)
- [x] Karate Chop: Chop Block -> **Mall Ninja**; DynamicPunch: Dynamite -> **M-80**; Outrage: Spazz Out -> **Rage Quit**;
      Sweet Kiss: Sweet Talk -> **Muah**; Cross Chop: Cross Up -> **Clothesline**; Megahorn: Air Horn -> **Bullhorn**
      (+ new descriptions for those and for every picked move whose description was empty)

## The 30 (variant: move = hood name - the gag)
### Batch 1
- [x] 299 Milk Drink = Got Milk: a gallon jug. Sip (heal glow). Sip. Third: CHUGS the whole gallon, tosses the
      empty jug over their shoulder - "GOT MILK?" sign.
- [x] 300 Super Fang = Half Off: a store price gun. Beep - a "$20" sticker on the foe. Beep - "SALE". Third: a giant
      red "50% OFF" tag slaps on, and the attacker bites (chomp) - the foe's worth half now.
- [x] 301 Poison Gas = Crop Duster: the attacker strolls past the foe - a little green puff. Strolls back - puff.
      Third: an actual crop-duster biplane flies over the lane dumping a green cloud. The foe turns green; flies buzz.
- [x] 302 Glare = Death Stare: lights go down, two glowing angry eyes in the dark. The foe sweats a bead. Another.
      Third: the foe goes stiff (yellow), a cricket chirps.
- [x] 303 Mega Punch = Catch a Fade: a barber pole spins up on the stage. Clippers buzz over the foe's head - hair
      falls. Buzz again. Third: "U WANT A FADE?" - POW.
### Batch 2
- [x] 304 Karate Chop = Mall Ninja: a strip-mall dojo kid: a headband/belt flies on, they chop a board - it does NOT
      break (bonk, they shake out their hand), chop again - nope. Third: they chop the FOE instead (crit flash).
- [x] 305 DynamicPunch = M-80: an M-80 by the foe. Light the fuse - fizzles. Relight - fizzles. The FOE leans in to
      look... BOOM. Sooty foe, confused.
- [x] 306 Bind = Zip Tie: zip tie on - the foe flexes, SNAP. Bigger zip tie - SNAP. Third: an industrial-size zip
      tie cinches them (squeeze shakes). Short (replays each turn).
- [x] 307 DragonBreath = Onion Breath: a raw red onion. Crunch. Crunch (the attacker tears up). Then HAAAA - a green
      onion breath wave, the foe's eyes water, they go stiff (yellow).
- [x] 308 Outrage = Rage Quit: a gaming monitor: GAME OVER. Mash - GAME OVER. Third: the controller gets thrown,
      cracks the screen and bonks the foe; the attacker goes red and flails into them.
### Batch 3
- [x] 309 Snore = Sawing Logs: asleep, Z. A log on the stage, a handsaw saws it (snore). Third: a CHAINSAW roars,
      the log splits, the halves fly at the foe.
- [x] 310 Mach Punch = Snuck Him: "YO LOOK, A BIRD" - the foe doesn't look. "IS THAT FREE WIFI?" - nope. "FREE
      MONEY!" - the foe whips round - POW.
- [x] 311 Hi Jump Kick = Fence Hop: a chain-link fence (BEWARE OF DOG) on the stage. Run up, rattle, nope. Again.
      Then a dog barks behind them and they CLEAR it in fear, flying knee into the foe.
- [x] 312 Spider Web = Trap House: a glue trap with a cheese wedge by the foe. The foe eyes it, inches over, steps
      on it - STUCK. Struggles, sticky strings, can't leave.
- [x] 313 Sweet Kiss = Muah: blows a kiss - a lipstick mark lands on the foe. Another. Then the foe's phone buzzes:
      "WHO IS SHE??" - confused.
### Batch 4
- [x] 314 Ice Punch = Cold Cocked: a chest freezer on the stage. Pulls out a popsicle - tosses it. A bag of peas -
      tosses it. Third: a FROZEN TURKEY - WHAM. The foe frosts over.
- [x] 315 Heal Bell = Last Call: a bar bell on a rope: ding, ding, DING-DING-DING - the club lights slam on, the
      party's over, everybody sobers up (status cured, sparkle).
- [x] 316 SolarBeam = Tanning Bed (two turns): turn 1 the tanning bed clamps shut on them, buzzes purple. Turn 2 it
      opens, they're ORANGE, and the tan glare beams the foe.
- [x] 317 Petal Dance = Victory Lap: struts left, struts right with a trophy, petals raining - third: bonks the
      foe with the trophy. Short (replays).
- [x] 318 Present = Gift Bomb: a wrapped box slides to the foe. Rattle. Tick... tick. The lid pops - a cartoon bomb -
      beat - BOOM.
### Batch 5
- [x] 319 Cross Chop = Clothesline: a laundry line strung across the stage. A shirt gets hung. Drawers get hung.
      Third: the foe runs straight into the line and flips over.
- [x] 320 Megahorn = Bullhorn: a police bullhorn. "IS THIS ON?" feedback squeal. Tap tap, squeal. Third: forget it,
      they ram the foe WITH the bullhorn.
- [x] 321 Hyper Voice = Hype Man: "YEAH!" bubble, "WHAT!" bigger, "OKAAAAY!!" huge - sound rings blow the foe back.
- [x] 322 Dizzy Punch = Ring Ya Bell: ding-dong ditch: a doorbell by the foe, ring - the attacker runs off. Ring - runs.
      Third ring: the foe's waiting - the attacker rings THEIR bell (POW), birds circle the foe.
- [x] 323 Heat Wave = Heat Check: a thermostat on the stage: 72. Click - 85. Click - 99 - heat waves engulf the foe,
      they sweat red. "WHO TOUCHED THE THERMOSTAT?!"
### Batch 6
- [x] 324 Flatter = Gas Up: a gas pump nozzle in the foe. $5... $20... $99.99 - the foe puffs up big and wobbly (confused).
- [x] 325 Mega Kick = Door Kick: a front door on the stage. Knock knock. Knock knock. Third: the door gets kicked off
      its hinges and flies into the foe.
- [x] 326 ExtremeSpeed = Getaway: a money bag, a rental e-scooter. It beeps... "3 MPH". Beep... Then TURBO - ZOOM
      straight through the foe.
- [x] 327 Zap Cannon = Bug Zapper: a porch bug zapper glowing purple. A moth - ZZT. Another - ZZT. Then the foe drifts
      toward the light, hypnotized - BZZZZT, paralyzed.
- [x] 328 Pain Split = Split Bill: the check folder lands between them: the attacker slides it to the foe, the foe
      slides it back, then they tear the receipt in half. HP shared.

### Wrap-up
- [x] Every new variant through reel.sh + clipcheck (5-6 per reel).
- [x] SolarBeam turn 2 tested with a swapped test variant.
- [x] Full rebuild; leave hood-showcase.nds playing all 30 (or `order=[5]` if the user wants to play it).
- [x] Tell the user: names changed, what each gag is, enemy side untested.

## Log (newest last)
- 2026-11-02: plan written.
- 2026-11-02: renames + descriptions applied. Batches 1-2 (299-308) built and reeled (s23b1, s23b2); fixes after the
  reels went in via hood/test/reel/set23_fix.py (Crop Duster puffs, Mall Ninja board spot, Rage Quit monitor spot)
  and still need one confirming reel. Tools: set23_lib.py (apply), set23_fix.py (string swaps). Next: batch 3 (309-313).
- 2026-11-02: batches 3-4 (309-318) built + reeled (s23b3, s23b4). Test variant 329 = Tanning Bed turn 2 (reel it
  right after 316). Fixes after reels (fence dog height, glue trap size/spot, lips size, UV puffs, bomb size) still
  need a confirming reel. Next: batch 5 (319-323).
- 2026-11-02: batch 5 (319-323) built + reeled (s23b5); Ring Ya Bell bubble moved after the reel. Next: batch 6 (324-328).
- 2026-11-02: batch 6 (324-328) built + reeled (s23b6). ALL 30 BUILT. Remaining: one confirming reel for every
  post-reel fix (301 302 304 308 311 312 313 316 329 318 322 326 327), full rebuild, showcase.
- 2026-11-02: fix reels s23fixA/B/C clean. Full rebuild done. ONE showcase with all 31 (89k script words) HANGS the
  game at FMJ (script too big; ~45k is fine), so: hood-showcase.nds = 299-313, hood-showcase-2.nds = 314-316, 329,
  317-328 (same size, slot 6 works for both; DeSmuME only reopens Recent ROMs, so open -2 by hand). Enemy side
  untested (Pidgey faints first). ALL PLAN ITEMS DONE.
- 2026-11-02: CORRECTION: the 31-anim hang was NOT a script-size limit - slot 6 was saved with a shorter FMJ
  script, so the game reads the new one truncated. Back to ONE hood-showcase.nds with all 31 (299-316, 329,
  317-328); hood-showcase-2.nds deleted. Waiting on the user for a fresh slot 6 save made on this ROM.
