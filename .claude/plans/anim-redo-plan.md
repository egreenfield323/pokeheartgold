# Plan: set-20 animation redo + Kimono Girls rewrite (started 2026-10-31)

**Read this whole file first, then `.claude/skills/hood-battle-animations/SKILL.md` (mandatory for any animation
work, especially "The gold standard" and "Where props can go").** The session that wrote this can end at any
moment. Tick boxes (`- [x]`) as soon as a step is done and verified, and add notes under "Log" at the bottom.
Never tick something that wasn't tested in DeSmuME.

## What the user asked for
1. Redo the 30 "set 20" animations (variants 264-293) to the new standard. The user called the first version
   "pretty poor and not funny at all", then called the prototypes Scam Likely / Rental Lambo / Crossover
   "literally so good. that should be the new standard".
   Standard: a recognizable hood situation, rule of three (expected, expected, then it breaks), a comic pause,
   the hit growing out of the joke, the foe reacting, and words only when they ARE the punchline.
2. Redo common moves that borrowed other moves' animations (done: variants 294-298).
3. Keep every prop clear of the HP boxes (the user caught clipping). Run `hood/test/clipcheck.py` on every reel.
4. **Kimono Girls ("Dancers") must become "super hardcore gangster"** (user's words). the user accepted
   "super hardcore gangster". Do this after the animations, or interleave if the animations stall.
5. Final deliverable: a full rebuild (`hood-soulsilver.nds`) plus `hood-showcase.nds` playing all the new-standard
   animations back to back (so the user can watch them with FMJ).

## Environment / how to test (zero-context version)
- Repo: `C:\Users\Evan\Documents\GitHub\hood-heartgold`. Source ROM:
  `C:/Users/Evan/Documents/dsume/Roms/4840 - Pokemon - SoulSilver Version (v10) (E).nds`.
- Pipeline: `hood/fxart.py` (art, PIL) -> `hood/gunfx.py` (kits + scripts + `VARIANTS` + `KITS`) -> `hood/battlefx.py`
  (`MOVES` = original move name -> variant number) -> `hood/patch_rom.py`.
- DeSmuME (`DeSmuME_0.9.13_x64.exe`) must be running for captures. The test battle is savestate **slot 6** of
  hood-showcase.nds (Cyndaquil vs Pidgey). Never make savestates yourself: if a save is broken, ask the user.
  Pidgey faints after about 6 moves, so keep a reel to 5 or 6 variants.
- **One command to test a set of variants:** `bash hood/test/reel/reel.sh NAME 277 278 279`. It fast-patches,
  builds the showcase, captures two segments and runs clipcheck. Output goes to `hood/test/reels_out/`:
  `NAME_a.png`/`NAME_b.png` (contact sheets, numbers = shot index), `NAME_a_frames/` (every shot),
  `NAME_a_clip.png` (flagged frames with box edges outlined in red). Look at the sheets, then zoom with
  `python -I hood/test/reel/zoomd.py hood/test/reels_out/NAME_a_frames out.png 30 45 60` (numbers from the sheet).
  Segment a covers about the first 3 animations, segment b the rest.
- Full rebuild (about 3 min):
  `python -I -X utf8 hood/patch_rom.py "C:/Users/Evan/Documents/dsume/Roms/4840 - Pokemon - SoulSilver Version (v10) (E).nds" hood-soulsilver.nds`
- Final showcase:
  `python -I -c "import sys; sys.path.insert(0,'hood'); import battlefx; battlefx.showcase('hood-soulsilver.nds','hood-showcase.nds', order=[...])"`
  The size must stay 135942344 bytes (slot-6 savestate compatibility).
- After writing art: `grep -o "^def [a-z_0-9]*" hood/fxart.py | sort | uniq -d` must print only `crackle` and
  `snore_z`. Grep script and kit names before adding them (a duplicate silently replaces the old one).
- Preview art before building: render it to a contact sheet with PIL (see `hood/test/reel/example_batch.py`'s
  neighbours in git history, or just `fxart.thing().resize((128,128), Image.NEAREST)` onto a green background).
- Long heredocs in this shell sometimes break (escapes get mangled): write scripts with the Write tool into
  `hood/test/reel/` or the session scratchpad, then run them.

## How a redo batch is applied (copy the pattern)
`hood/test/reel/example_batch.py` + `example_batch_scripts.py` is the batch-B script that redid 5 animations. It:
1. adds new kit constants after `LAST_KIT` (after batch D3 the last is `COMBOB22` = 566; the next new kits start at
   **567**; check `grep -n '^LAST_KIT' hood/gunfx.py` and the `range(...)` line above it), plus `DONOR.update({NAME: 82, ...})` and the names appended to the `SET10_82 += [...]` list that ends
   with `..., HIDEB22, MOOCHB22, ZAZAB22, ZAZAC22, DIPB22, SPITB22, POSTB22]`;
2. `swap_kit(s, OLDKIT, new_code)` replaces an old set-20 kit block in place (`b, rs = pk(NAME, {...})` up to the
   next `b, rs = pk(`), reusing the old constant name;
3. `swap_fn(s, old_fn_name, new_code)` replaces the script function, then renames it in `VARIANTS`
   (`            277: _smoke_screen,`) and extends `KITS` (`        277: (FOG20, FOGFX20,),`).
Kit rules: res 1/2 for props (`pk(NAME, {1: (art, scale, life, {}), 2: ...}, alpha=particle_shape)`), res 0 =
the alpha particle (bursts). **Never put text or 1:1 props on res 3** (it draws low and offset, and washes out
colours). Text props use `ONE_TO_ONE` (64px art) or `ONE_TO_ONE / 2` (32px); signs use
`fxart.burst_sign([...], fill=(220, 40, 40, 255), text=(255, 255, 255, 255))` at `SIGN_SCALE` with
`{"colors": 30}`; speech bubbles use `fxart.line_bubble(["LINE 1", "LINE 2"])` at `ONE_TO_ONE`.
**Draw order across kits = their order in `KITS[variant]`: later kits draw ON TOP** (Vape Cloud's shades only
showed over the fog after `KITS[277]` became `(FOGFX20, FOG20)`). Within one kit, a newer emitter draws under an
older one.
Script helpers: `emit_at(kit, res, who, (x, y))` (who 0 = attacker, 1 = foe; **relative to the battler's
CURRENT spot**), `_hold`, `_lob`, `stop_motion`, `bmove(side, 258|264, frames, dx, dy)`, `shake_defender`,
`func(48)` knockback, `flash_screen(n)`, `func(34, 8|2, 0, 1, rgb(..), strength, 0)` tint foe|attacker,
`se(s["name"])` (names: `battlefx.SOUNDS` + `battlefx.BUILTIN`).

Placement (player attacking; screen coordinates, y down): the foe's HP box is x 0-124, y 18-54; yours is
x 136-256, y 98-130; the message box starts at y 143. Clear zones: right of the foe's box (x >= 133, y < 90), the
lane (y 56-90), and the stage between your homie and your box (foe-relative about (-80, -5), attacker-relative
about (40, 40)). The foe is at screen (185, 81), the attacker at (64, 140). Proven spots: speech bubble from the
foe at foe-relative (-30, 36); from the attacker (sx * 50, 58); a 64px prop "next to the foe" goes on the stage
at foe-relative (-79, -5) or (-90, -5); a sign over the foe at (0, 58-62).

## Checklist

### Done and verified in DeSmuME (do not redo)
- [x] Move-name audit: 69 renames in `hood/data/moves.json` + descriptions + dialogue mentions (Lick -> Licked It too)
- [x] 265 Scam Likely, 273 Rental Lambo, 276 Crossover (prototypes = the standard)
- [x] 294 Pistol Whip (Scratch), 295 Double Tap (Double Kick), 296 Licked It (Lick), 297 Ricochet (Swift), 298 Smooth Talk (Hypnosis)
- [x] 264 Clown On, 266 Fair One, 267 Tax Punch, 268 Chicken Wing, 269 Ring Light, 270 Spike Strip, 271 Got Laced (sneakers redrawn), 272 Big Mad, 274 Inside Job, 275 Parkour
- [x] clipcheck pass over all of the above (reels r1-r5), fixes applied
- [x] `hood/test/clipcheck.py` + `hood/test/reel/` helpers committed to the repo; skill updated

### Batch C (DONE 2026-10-31: applied by `hood/test/reel/batch_c.py`, tested, clip-checked)
Old function / kits to replace are listed per move.
- [x] 277 Mist = **Vape Cloud** (`_smoke_screen`; kits FOG20, FOGFX20): a box-mod vape at the attacker. Puff,
      a smoke ring (alpha `fxart.ring()`). Puff, another ring. Third: a GIANT cloud swallows their side (FOGFX20's
      fog puffs + a grey bg fade), and only a pair of cool shades gleams in the fog (bling). Art: `vape_mod`, `cool_shades`.
- [x] 278 Charge = **Plug In** (`_plug_in`; AMP20, AMPFX20): a phone at "1%" (red battery), plugged into the
      attacker... "2%"... "3%" (painfully slow, foe taps foot or yawns). Then they pull out a giant FAST CHARGER
      brick: ZAP, "100%", lightning, the attacker glows yellow. Art: `phone_charge(level)` (text on screen, 1:1), `fast_charger`.
- [x] 279 Bug Bite = **Bed Bugs** (`_bed_bugs`; BUGS20, BUGFX20): a cheap motel bed slides under the foe, they
      lie down (bmove down). Itch (shake). Itch. Then bugs ERUPT and the foe launches up, and a "1 STAR." sign pops.
      Art: `motel_bed` (keep it on the stage or right of the foe; NOT at the foe's feet, which is your HP box).
- [x] 280 Wring Out = **Shakedown** (`_squeeze_out`; MOP20): the foe gets shaken (big shake_defender), and things
      fall out of them: coins (gold_coin burst), keys, then a squeaky RUBBER CHICKEN. The attacker pockets the coins.
      Art: `key_ring`, `rubber_chicken`.
- [x] 281 Magical Leaf = **Loud Pack** (`_loud_pack`; FANNY20, MONEY20): the neon fanny pack unzips with a
      boombox inside. Music notes home in on the foe, louder each time (3 waves). From off-screen top-left: a
      "TURN IT DOWN!" bubble, and a house slipper flies in and bonks the ATTACKER. Art: `boombox_pack`,
      music-note alpha (a `music_note` already exists in fxart: check what it is before reusing), `house_slipper`.
      (Mama's chancla was used before; a slipper from a neighbour's window is fine but make it a new drawing.)

### To do: batch D (designs to finish; same standard, rule of three)
- [x] 282 Endeavor = **Same Smoke** (`_grind`; TREAD20): fight prep. Earrings off (hoops fly), chain off,
      Vaseline on the face (jar + shine), then they swing. Endeavor cuts the foe's HP down to theirs.
- [x] 283 Odor Sleuth = **K9 Unit** (`_sniff_out`; SLEUTH20): a police K9 (vest says K9) trots in from the right
      and sniffs around the foe: sniff... sniff... then sits and BARKS. It "found" something: pulls a sandwich
      out and eats it, then trots off.
- [x] 284 Withdraw = **Hide Out** (`_hide_out`; FICUS20): they hide behind a tiny potted cactus WAY too small
      for them. The foe looks left, looks right (bmove), then the attacker sneezes ("ACHOO" bubble) and the cactus falls over.
- [x] 285 Power Gem = **Bling Beam** (`_rock_candy`; CANDY20, GEMBEAM20): a huge iced-out chain on the
      attacker. Tink (sparkle). Tink. Third: the medallion fires a gold beam (reuse GEMBEAM20's spray recoloured
      gold, or a new kit) and the foe gets crusted in diamonds.
- [x] 286 Leech Life = **Mooch** (`_mooch`; SHAKE20): the foe has a tray of fast food. The attacker takes a
      fry. Takes another fry. Then takes the whole burger and walks off chewing. The attacker heals (green glow).
- [x] 287 Detect = **Peep Game** (`_peep_game`; SCOPE20): the foe lunges (bmove), and the attacker is already
      a step to the side. Again. Third: the attacker holds up the foe's own playbook/clipboard reading "PLAN: HIT EM"
      with a "PEEPED." sign.
- [x] 288 Leaf Storm = **Zaza Storm** (`_zaza_storm`; LEAVES20): a TV weather map. "LIGHT" forecast, then
      "MODERATE", then "SEVERE ZAZA WARNING" in red, and the leaf storm (current LEAVES20 spray) buries the foe.
- [x] 289 Teleport = **Dip Out** (`_dip_out`; EXIT20): they sneak to the EXIT door. Rattle: locked. Rattle:
      locked. Then they jump straight out a window (glass shatters) and are gone (`func(40, 2, 1)` vanish, then unvanish at the end).
- [x] 290 Spit Up = **Spit Bars** (`_mouthwash_spit`; MOUTH20, SPITFX20): they "spit bars" literally. A metal
      bar flies at the foe. Another. Third: a whole jail cell slams down around the foe. "LOCKED UP." sign.
- [x] 291 Ingrain = **Post Up** (`_post_up`; CHAIR20): a lawn chair. Then a cooler. Then a whole grill fires
      up. They are NOT moving. Healing glow each beat.
- [x] 292 Fury Cutter = **Stab Combo** (`_stab_combo`; SLASH20, COMBO20): it already has fighting-game combo
      counters ("2 HIT!", "3 HIT!", "5 HIT COMBO!"). Add a twist: on the last hit an announcer bubble ("ULTRA
      COMBO!") and the attacker slips on the 6th swing, OR keep it and only fix placement. Re-check with clipcheck either way.
- [x] 293 Destiny Bond = **Ride or Die** (`_blood_pact`; BFF20, LINK20): handcuffs. Click on the attacker,
      click on the foe, a chain between them, then they throw the key away (key flies off-screen, distant splash).

### To do: wrap-up for the animations
- [x] Run every new-standard variant (264-298) through reel.sh + clipcheck one last time, 5-6 per reel.
- [x] Full rebuild, then the showcase with `order=[294, 295, 296, 297, 298] + list(range(264, 294))`.
- [x] Update the skill and the memory files if anything new was learned. Tell the user the enemy side is
      untested (Pidgey faints first).

### To do: Kimono Girls = super hardcore gangster
They're called "Dancers" in the hood text. Rewrite their own lines so they're a ruthless, hardcore gangster
crew: Zuki is the boss, and the dance theater is their front. Threats, loyalty, "nobody leaves the family",
counting money, cold menace. Keep it funny and over the top. No sexual content, ever. Keep each one's quirk,
gangsterized:
- Naoko: can't read a map, so she's the getaway driver who always gets lost.
- Miki: "the one who know the most talk the least", so she's the silent enforcer.
- Sayo: skates in sandals.
- Kuni: spins even underground, so she runs the underground.
The Bell Tower / Whirl Islands summoning lines can stay reverent but gangster ("the family been waitin' on HO-OH...").
- [x] Dump and read the current rows: `hood/data/dialogue/msg_0618_T27R0501.json` (Dance Theater: rows 9-20
      are the Dancers, 21-24 their calls, 40-45 after the event; rows 0-8 and 25-37 are the Fed heckler and
      bystanders, which can reference the new menace), `msg_0058_D17R0110.json` (Bell Tower, HO-OH),
      `msg_0125_D40R0107.json` (Whirl Islands, LUGIA). Also grep `hood/data/dialogue/*.json` and
      `files/msgdata/msg/*.gmm` for Zuki|Naoko|Miki|Sayo|Kuni|Dancer|Kimono to catch mentions elsewhere (msg_0122_D39R0101,
      msg_0310, msg_0440, msg_0542, msg_0543, msg_0377, msg_0413 mention them; adjust where it adds to the joke).
- [x] Rewrite the rows in those JSON files (same row numbers, same `{STRVAR...}`/`{YESNO}` tokens, same ending
      codes `\\r` `\\n` `\\f`). The apply script reflows long lines itself.
- [x] Apply: `python hood/apply_dialogue.py msg_0618_T27R0501 msg_0058_D17R0110 msg_0125_D40R0107 [others] --dry-run`,
      then without `--dry-run`. Nothing is written if any row fails a check, so read the errors.
- [x] Their pre-battle and defeat lines may live in the trainer text: check `hood/data/trainer_dialogue.json` and
      the trainer class "Kimono Girl" -> "Dancer" in `hood/data/trainer_classes.json`. Gangsterize those too
      (apply with `apply_hood.apply_trainers()`; read how other trainer edits were applied in that file first).
- [x] Full rebuild, then tell the user what changed (quote a few lines).

## Log (newest last)
- 2026-10-31: plan written. Variants 264-276 + 294-298 done and clip-checked. hood-showcase.nds currently plays
  [294-298, 264-276]. Next: batch C (277-281).
- 2026-10-31: batch C (277-281) done: `hood/test/reel/batch_c.py` (+ `batch_c_scripts.py`, art in
  `art_batch_c.py`, already appended to fxart). Reel output moved to `hood/test/reels_out/` (capture.py wipes
  hood/test/out). Next: batch D starting with 282.
- 2026-10-31: batch D1 (282-286) done: `hood/test/reel/batch_d1.py` (+ scripts, art in `art_batch_d1.py`,
  already appended). Next: 287 Peep Game (batch D2 = 287-291, then 292-293).
- 2026-11-02: batch D2 (287-291) done: `hood/test/reel/batch_d2.py` (+ scripts, art `art_batch_d2.py` appended).
  Spit Bars' function is `_spit_bars2` (an older `_spit_bars` exists). Next: 292 Stab Combo + 293 Ride or Die.
- 2026-11-02: batch D3 (292 Stab Combo + COMBO BREAKER twist, 293 Ride or Die = handcuffs + key thrown away) done (batch_d3.py). ALL 30 set-20 variants redone. If DeSmuME is closed, start it (only if it is NOT already open): PowerShell Start-Process with FilePath C:/Users/Evan/Documents/dsume/DeSmuME_0.9.13_x64.exe and the showcase ROM as argument. Wrap-up clip pass: 277-281 clean. Use hood/test/reel/plan_log.py to tick/log.
- 2026-11-02: Animations DONE: clip pass f1-f4 clean (264-276 + 294-298 checked earlier in r1-r5), full rebuild, hood-showcase.nds plays [294-298, 264-293] (35 anims, size 135942344). Next: Kimono Girls.
- 2026-11-02: Kimono Girls = hardcore gangster family DONE: hood/test/reel/kimono_gangster.py (dialogue JSON rows for 0618/0058/0125/0115 row 30/0377 row 7 + named lose-lines) applied with apply_dialogue.py (152 rows OK); hood/test/reel/kimono_trainers.py wrote the 5 TRMSG_LOSE lines into trainers.json + msg_0728.
- 2026-11-02: Final full rebuild done; showcase restored to all 35. ALL PLAN ITEMS DONE.
