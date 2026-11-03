# Plan: set 27 - thirty more (started 2026-11-02)

Read `.claude/plans/anim-set26-plan.md` + `anim-set25-plan.md` + `anim-set24-plan.md` (tools, LESSONS). Kits suffix
`27`, variants 424-453 (422/423 are set 26's two-turn test variants). Every batch: reel.sh + enemy.sh.
Keep the user posted between steps. Remaining moves = moves.json keys not in battlefx.MOVES (75 before this set).

## Already taken (don't repeat)
pigeons (Sky Attack, Mud Bomb), leaf blower (Sandstorm), weather report (Leaf Storm), ring light / selfie (Flash,
Synthesis, Double Kick), barber + clippers (Mega Punch), incense + om (Zen Headbutt), chugging a jug (Milk Drink),
plant growing in stages (Frenzy Plant), bartender bell (Heal Bell).

## Renames
Brave Bird Bird Strike -> Send It; Seed Flare Bloom Bomb -> Allergy Szn; Needle Arm Needle Jab -> Flu Shot; Twineedle Double Shiv -> Tat Gun (toothbrush shivs are taken); Magnet Rise Hover Shoes -> Hoverboard.

## The 30
- [x] B1 INSANE: 424 Brave Bird (Send It: roof of the projects, cape + goggles - flap test, flap test - SEND IT:
      a flaming dive off the top of the screen, crater, they're dazed), 425 Seed Flare (Allergy Szn: pollen count
      HIGH - VERY HIGH - EXTREME - a giant flower erupts, the screen goes yellow, ACHOO blows the foe back),
      426 Dark Void (Blackout: the city skyline's windows go dark block by block, the screen goes black, just eyes,
      then Zs), 427 Aura Sphere (Aura Farm: pose +100 AURA, pose +500, then the giant aura orb: +10000),
      428 Dragon Rush (Rush Hour: subway platform - the train's late - it barrels in, doors open, a stampede)
- [x] B2: 429 Memento (RIP Shirt: they drop, the airbrushed RIP tee with their face, the foe tears up),
      430 Refresh (Fresh Fit: sneaker cleaning kit - scrub, scrub - crisp white glow), 431 Blaze Kick (Hotfoot: hot
      asphalt - tiptoe, tiptoe - a flaming kick), 432 Meteor Mash (Space Jam: a basketball from orbit, slam dunk on
      the foe), 433 Muddy Water (Dirty Water: the foe at the bus stop - a car through the puddle - splash, splash,
      then the bus)
- [x] B3: 434 Heal Block (Cut Off: the foe reaches for the drink - the bartender slides it away - YOU'RE CUT OFF),
      435 Punishment (Time Out: the corner, the kitchen timer, the stool), 436 Switcheroo (Swap Bags: shell game with
      two bags - swap, swap - wrong bag), 437 Chatter (Yap Session: speech bubbles piling up, the foe dizzy),
      438 Lunar Dance (Moonwalk: the glove, the hat, the moonwalk across, hee-hee)
- [x] B4: 439 Acupressure (Back Rub: the mall massage chair, coin in), 440 Needle Arm (Flu Shot: alcohol swab,
      the needle, the foe flinches - jab), 441 Ominous Wind (Bad Wind: the elevator - ding - someone let one go),
      442 Twineedle (Double Shiv: toothbrush shivs, short - replays), 443 Me First (Cut Line: the line at the club,
      they skip it)
- [x] B5: 444 Tail Glow (Glow Up: bonnet off, edge gel, swoop swoop, GLOW - Copycat dropped: Mimic + Mirror Move did copying), 445 Gastro Acid (Stomach Bug: gas station hot dog -
      rumble - rumble - an OUT OF ORDER sign on the foe; toilets were Whirlpool's), 446 Lucky Chant (Rabbit Foot: scratch-off - scratch - scratch - WINNER $2),
      447 Force Palm (Stiff Arm: stiff arm, stiff arm, Heisman pose), 448 Howl (Hype Howl: AWOO, the crowd howls back)
- [x] B6: 449 Meditate (Namaste: yoga mat - pose - pose - CRACK - glows anyway), 450 Imprison (Lock Up: the corner store's roll-down
      gate slams in front of the foe, padlock - the jail cell was Spit Up's), 451 Follow Me (Look at Me: spotlight, the foe can't look away), 452 Ice Ball (Snowball:
      packed and thrown, short - replays), 453 Magnet Rise (Hoverboard: wobble, wobble, it floats)
- [x] Rebuild + showcase (both sides if under ~75k words) + tell the user. 45 left after.

## Log
- 2026-11-02: plan written.
- 2026-11-02: renames + 30 descriptions applied. B1-B3 written + applied (variants 424-438).
- LESSON: func(48) (the hit blink) restores the battler to the spot it had when func(48) STARTED - calling it while the
  foe is knocked back undoes the return bmove (Allergy Szn / Rush Hour left Pidgey displaced). Call func(48) after the
  foe is back (bmove + wait), or before any displacement. Reels stop at 660 frames: put long moves in their own reel.
- 2026-11-02: B4-B6 written + applied (439-453). B1-B3 reeled both sides, fixed (roof/road/bar/bags/tiles positions
  off the message + HP boxes, pollen board + skyline moved, lint bigger, RIP tee lower). Swaps: Cut Line = deli
  counter (club rope taken), Glow Up = edges laid (cucumbers were Calm Mind's), Lock Up = store gate.
- 2026-11-02: all 6 batches reeled both sides + fixed. func(68) screen shake also restores positions (dropped the
  Rush Hour squash / Allergy knockback dy). Move descriptions can't use straight double quotes (msg encoder): curly.
  Rebuilt; showcase 424-453 both sides = 70k words. SET 27 DONE. 45 left.
