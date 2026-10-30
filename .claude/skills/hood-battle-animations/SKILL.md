---
name: hood-battle-animations
description: Make (or fix) Hood HeartGold battle move animations - new particle art, kits, animation scripts, sounds, and testing them in DeSmuME. Use whenever the user asks for new/changed move animations, says an animation looks bad/clunky/unreadable, freezes, or asks about how move animations work in this repo.
---

# Hood HeartGold battle animations

Move animations are built in Python and patched into the ROM: `hood/fxart.py` (pixel art drawn in code) ->
`hood/gunfx.py` (particle kits + animation scripts) -> `hood/battlefx.py` (move mapping, sounds, patching) ->
`hood/patch_rom.py` (builds the ROM). Read this whole file before touching any of them.

## The bar (what the user wants)

- **Creative and hilarious, hood-themed, matching the move's hood name** (`hood/data/moves.json`) and its
  description (`hood/data/move_desc.json`). If the animation idea doesn't fit the name, propose a rename.
- **Field moves need names that work OUTSIDE battle too.** HMs and TMs used on the map (Surf, Waterfall,
  Whirlpool, Cut, Strength, Rock Smash, Rock Climb, Fly, Flash, Defog, Dig, Teleport, Headbutt, Sweet Scent...)
  get named in progression lines - "Would you like to use ___?" at a waterfall, "go back and ___ along Route
  27", "That's the HM ___. Teach it to clear lil trees." The name has to read as that action: Wet Ya Up /
  Hydrant Wave / Jacuzzi / Shank didn't, so they became Beam Me Up / Ride Da Wave / Flush It / Box Cutter. Before
  naming or animating one, read its lines (msg_0211 field prompts, apply_move_mentions MENTIONS, the
  dialogue files) and pick a name + gag that fits both the attack and the field use.
- **Every move needs a real hood joke with a story beat**, not a generic prop + one hit + a sign. A batch of
  household props (slingshot, sprinkler, power strip, pillow, skateboard, printer paper) got "boring, not funny,
  not hood like". What lands: a recognizable hood situation with a payoff - the pie hit gets filmed (POSTED.),
  six cords in one outlet -> blackout (PAY THE LIGHTS!), Mama's chancla thrown from off-screen, the parking
  boot, the raccoon out of the dumpster, the process server out of the bush (SERVED!), the itis after soul food.
  Pitch the gag list to the user first for big batches.
- **Don't fake body parts on top of a sprite** (arms in a headlock, a grabbing hand, a noogie fist): they float
  over the battler and read as junk ("a weird looking thing and a fist moving around"). Put an OBJECT on them
  instead (collar, boot, body bag, blankie).
- **The animation does the talking - most moves get NO sign.** A sign on every move is "pretty annoying". Only
  add one when the words ARE the joke and the picture can't say them (YOU UP?, PAY THE LIGHTS!, SERVED!,
  SALTY.). Text that's part of a prop (AUDIT, REC, PAST DUE, the WHO DID IT? bubble) is fine.
- **Sign words are the punchline in plain words** - no in-jokes that need explaining ("HEEL!" for a leash
  confused; "LEASHED!" says it).
- **All-new art for every move.** Don't reuse other moves' assets (a shared flame burst between two fire moves
  is the most reuse that's OK). Never re-skin an old prop (the user called out "the car again").
- **Readable at a glance.** Props big (64px textures), text in signs ("WHAM!", "POCKET SAND!" via
  `fxart.burst_sign`), outlined, high contrast. If you can't tell what it is in a 128px contact sheet, it's
  too small. Tiny/abstract = "can't tell what's going on" = redo.
- **Text must be pixel-crisp** - the user zooms in and calls lumpy/chewed letters "awful". See "Text and exact
  scales" below: pixel font only, shown at an exact whole-number px per texel, never rotated.
- **Signs: not too big.** ~80px wide is right (a 126px sign was "huge"; ~100px "a tad too big"). On common moves
  a big sign every turn gets "annoying" - keep at most one sign per move, and drop it if the gag reads without it
  (Catch Flight's BAGGAGE CLAIM! was cut; the suitcase bonk says it).
- **Common moves get the most care** (Fly, Tackle...): slow enough to read, the funniest gag.
- **Snappy.** ~1-2.5 s. Slow crawls feel "clunky". Build up -> beat -> big payoff (flash, shake, knockback).
- **Big moves are big**: Surf-type moves fill the screen like the original; legendaries/strong moves bigger.
- **Behave like the original move**: two-turn moves (Fly, Dig, SolarBeam...) need both turns (see below);
  targets/attackers always end back on their spot.
- Pokémon/props never stay displaced. The variant tail resets both battlers; don't fight it.

## Pipeline

1. **Art** - `hood/fxart.py`. Color art: RGBA PIL image (`to_a3i5` packs it). Particle shapes tinted by the
   emitter: alpha-only A5I3 bytes via `_alpha(w, h, f)` (see `soft_puff`, `flame_blob`, `heart`, `weed_leaf`).
   Signs: `burst_sign(["TEXT!"], fill=..., text=...)`. Preview every new piece quantized to its slot's palette
   (see "palette sizes") in a contact sheet before building.
2. **Kit** - in `gunfx.build_files`, set-4 section (`prop`, `mover`, `follower`, `spray`, `thrown`, `sign`,
   `poses`, `tex`, `rot`, `kit` helpers). A kit = a copy of a donor particle file (`DONOR`) with new textures and
   emitters (resources) reconfigured. Add the kit id to the big tuple, `DONOR`, and the self-destruct assertion
   lists at the end of `build_files`.
3. **Script** - a `_name(side, s)` function returning script words (or `(turn1, turn2)` for two-turn moves).
   Register in `VARIANTS` and `KITS` (<= 3 kits), map the move in `battlefx.MOVES`, add sounds to
   `battlefx.BUILTIN` (the move's original SE ids - find them in its original script, words 1500-2200).
4. **Build** - `python -I -X utf8 hood/patch_rom.py "<SoulSilver EU rom>" hood-soulsilver.nds`
   (rom: `C:/Users/Evan/Documents/dsume/Roms/4840 - Pokemon - SoulSilver Version (v10) (E).nds`).
   If it says "an original file didn't match ()", that's usually YOUR assertion: run `gunfx.build_files` on the
   NARC directly to get the traceback (snippet in "Testing").
5. **Test in DeSmuME** (below) and look at every animation before reporting it done.

## Hard engine rules (each of these froze or broke the game once)

- **Particle slots**: the engine has 16 particle-system slots. Kits are mapped to slots 0..2 per animation by
  `variant()` (`_ps()`), so always emit through the helpers (`emit_at`, `_fly`, `_throw`, `tracer`), never raw
  kit numbers. Max 3 kits per animation (battle heap).
- **self_dest (flag bit 14)**: every static emitter MUST self-destruct or `WaitForParticles` hangs forever.
  Emitters flown by MoveEmitter (`_fly`, `_throw`, `tracer`) must NOT (MoveEmitter frees them; SPL freeing them
  first = use-after-free freeze). `build_files` asserts both - add every new emitter to the right list.
- **MoveEmitter (func 65) always starts at the attacker's centre** (only the END point takes an offset). To make
  things come out of a prop that sits elsewhere, use a static emitter on the prop with velocity aimed at the
  target (`spray` / `aim_path`) instead.
- **Palette sizes per texture slot**: a donor's slot holds N colours (82 tex1: 32, 168 tex0: 30, 349 tex1: 24,
  47 tex1: 10, 47 tex0: 4, 57 tex1: 4). More colours = garbage pixels. `tex()`/`single()` cap it; check with
  `spa.textures(file)[i][6] // 2`.
- **Draw type (flag bits 4-5, `BILLBOARD`)**: some donor emitters (84 res0) are "directional billboards" that
  stretch along velocity - a piece riding its emitter with zero velocity is invisible. `prop`/`spray` clear it.
- **Leftover donor behaviour**: donors keep colour animation, gravity, flicker, convergence, spin. `prop()`
  neutralises them (clr_anm white, gravity 0, cngc/spin 0, rotation 0 unless flag bit 12). Raw `spa.edit` on a
  donor resource doesn't - that's how the fan blades cycled gold and fell off the fan.
- **Blocks**: `spa.edit` asserts if you pass a field whose block the resource lacks (`child_gen` without `chld`,
  `gravity` without `grvt`). `prop` drops them automatically; `spray` too.
- **Air resistance doesn't brake to a stop.** For "slides down and stops" use stop-motion poses
  (`stop_motion` + POSE/HOLD resources, SWING_STEP frames each).
- **MoveBattlerBy (func 57)** mirrors dx AND dy for battlers on the enemy side; player side as-is. Use
  `bmove(side, role, frames, right, up)` (screen px, up = positive) - measured in-game. role 258 attacker,
  264 defender. It moves dx//frames per frame: match a carried battler to a prop by using the prop's speed.
- **Two-turn moves**: return `(turn1, turn2)`; `variant()` emits `JumpByVariantBit0`
  (`[13, 2, 1+len(turn1)]`). Variant 0 = charge turn, 1 = the hit (set by ChargeMoveCleanup). The battle
  script hides the attacker after turn 1 (ToggleVanish); use `func(40, 2, 1)` / `func(40, 2, 0)`
  (SetBattlerVanished) like the original. The showcase only plays turn 1 - test turn 2 with a swapped test
  variant (see `_fly_turn2_first`, variant 97).
- **Sounds**: prefer built-in game SEs (`BUILTIN`) - new samples live in the battle wave archive and too many
  break the level-up fanfare (sound heap). Cries: `cry(mode, param)` (PlayCry, opcode 65).
- Script timing: `wait(n)` ~ 2(n+1) frames; `wait_frames(f)` converts. Scripts tick at 30 Hz.
- **Texture tiling (emitter header byte 75, bits 0-3)**: donors tile their small textures 2x2 / 2x1 mirrored
  (they hold a quarter of a shape). A whole shape (note, swirl, star) shows up 4x mirrored ("}{" notes) unless
  you clear it - set 5 does `b[off + TILE] &= 0xF0` for its kits. Cleared, the shape fills the quad: halve scales.
- **Particles can never go behind a Pokémon**: battler sprites sit at the back of the depth range and draw as
  opaque polygons first; no particle Z (clipped past ~14000) or alpha changes that. Place props so they don't
  overlap the battler instead (Duck n Cover's lid sits mid-screen on the player side).
- **HP boxes are a BG layer over the 3D**: props under the player's HP box (right of the player, x>140) vanish.
- **Shakes restore the battler's start position** when they end: a shake overlapping a MoveBattlerBy snaps it
  back (Smackdown's charge did that). Don't shake a battler that's about to move.
- Strobing tints (`func(34, ...)` alternating colours) leave the last colour fading out: end on the bright one.
- Don't tint a battler the colour of the effect it's inside: Beam Me Up's foe, tinted blue in the blue water
  column, just vanished. Tint after it comes out (soaked on landing).
- **Sounds - the sound heap is nearly full mid-battle.** Don't add instruments to the battle bank (751) or
  re-pitched/cloned sequences: a bigger bank made the enemy's Growl (Talk Trash) freeze loading its cry, and
  cloned game sequences played silent. Pick an existing game SE that already sounds right instead. Many of
  the game's own move SEs (wave archive 700, e.g. Supersonic's 1936) play silent mid-battle; check a new one
  is audible. Rapid-fire repeats of the hood "boom" (4 in ~1 s) also froze the next cry - after changing
  a move's sounds, run a full turn (enemy move included) and make sure the battle moves on.
- Scenes outside the move scripts (the evolution: overlay 95) play SEs hard-coded in the overlay's literal pools:
  swap the ids there (`evofx.SOUND_SWAP`). They use bank 751, the battle bank, so the hood samples play. The
  recompressed overlay must stay inside its 0x200 slot of the ROM or every later file moves (savestates break).
- Measuring audio: `hood/test/record_audio.py` records a move via File > Record WAV (DeSmuME saves it to its
  own AviFiles folder). Emulation is deterministic, so subtracting a run with the sound removed leaves just the SE.

## Coordinates and sizes

- `emit_at(kit, res, who, (x, y))`: who 0 attacker / 1 defender; offsets are SCREEN px (y up), NOT mirrored -
  mirror yourself with `sx = 1 if side == "player" else -1`.
- `TARGET_FROM_ATTACKER = {"player": (121, 59), "enemy": (-121, -59)}`; player origin ~(64,140) on screen,
  enemy ~(190,90). Screen is 256x192.
- Particle quad: 0.745 screen px per 64px-texture texel per 1.0 scale in battle (measured); a 32px texture is
  2 x that (the quad size doesn't depend on the texture). The evolution scene's camera: 0.673 (`evofx.EVO_PX`).
  Velocity: `VEL_UNITS = 355` per px/frame (`mover(vx, vy)` does it for you).
- `scl_anm = (start, mid, end, in, out)` with out=255 never runs the out phase: the particle HOLDS at `mid`, so
  its on-screen size is `scl * mid`, not `scl * end`.
- HP boxes: the foe's covers the top-left (y < ~52, x < ~120), yours the bottom-right. Player-side signs sit 50px
  above the homie (`_sign_at`) so they clear the foe's box.
- Measured: your HP box is x > ~135, y ~93-140; the message box (shown during the move) y > ~143 - both hide
  particles. The clear horizontal lane across the whole screen is y ~55-90 (Flop's tumbleweed rolls at y 70).
- Rotation: `rot(b, rs, res, spin=per_frame, init=angle)`, 0x10000 = full turn; spin needs flag bit 12.
  Directional art: pre-rotate the art (`bullet`, `glare_streak`) or use init rotation for SYMMETRIC shapes only.
  A held prop turned 0x8000 for the enemy hangs UPSIDE DOWN (the user caught the tasers) - give the enemy a
  left-right mirrored texture instead: `b, idx = mirrored(b, art)` (spa.add_texture) + `prop(..., tex=idx)`. Text
  in mirrored art reads backwards: draw the flipped art with the text redrawn (`fxart.big_taser(flip=True)`).

## Text and exact scales

- **Pixel font only**: `fxart._outlined_text` / `_text_w` / `burst_sign` use `SMALL` (hand-drawn 4x6 caps, a few
  lowercase), `_big_text(..., font=)` defaults to `GLYPHS` (5x7). Never PIL fonts: `ImageFont.load_default()` is a
  vector font now, and forced to hard pixels it comes out ragged ("chewed").
- **Exact scale or it's lumpy**: an uneven px/texel ratio doubles some pixel rows and not others. Signs show at
  2:1 (`SIGN_SCALE = 2 / .745`, `SIGN_POP` holds at 1.0 - `sign()` does it); props with text in the art at 1:1
  (`ONE_TO_ONE`, divided by the prop's held pop: `scl=ONE_TO_ONE / 1.15` with `scl_anm=(.2, 1.15, ...)`); a big
  prop at 3:1 / 4:1 (`ONE_TO_ONE * 3`). Check in game: crop a frame, count runs of text pixels - all even at 2:1.
- **Rotation smears** pixel art (thrown spinning bottles, tilted stamps): never rotate anything with text; draw
  it straight.
- `burst_sign` hugs its words (the burst is sized to the text), so signs stay ~80px at 2:1.
- **Sign text must be LIGHT** (white / yellow): every glyph gets a dark outline, so dark text melts into it and
  the word vanishes (STIFF. and TSSSS! were unreadable). Dark burst + light text, or bright burst + white text.
- Ball signs (`ballfx`) and GLOW UP! (`evofx`) follow the same rules with their own camera factors.

## Draw order

- Kits draw in the order of their slots: a later kit in the `KITS` tuple draws OVER earlier ones (signs over the
  jet). Inside one kit, a newer emitter draws UNDER older ones. Something that must show in front of a big prop
  (the suitcase falling out of the jet) goes in a later kit.

## Recipes that work

- Prop that pops in: `prop(..., scl_anm=(.2, 1.15, 1.0, 30, 255))`.
- Thrown arcing object: `thrown(b, rs, size, spin)` + `_throw(KIT, slot, at)` (lands after THROW_FRAMES).
- Stream/spray at the target from anywhere (breath, chips, leaves, sand, hearts, gusts): `spray(...)` with one
  resource per direction (E = player attacking, P = enemy attacking).
- Something gliding across the screen: `mover(vx, vy)`; a battler riding it: `bmove` at the same speed.
- Comet/trail: a flown emitter that drops particles every frame (`gen_intvl=1`, follow bit 15 OFF, no
  self_dest) flown with `_fly` alongside a `follower` head.
- Stop-motion: one resource with life SWING_STEP emitted at successive positions (`stop_motion`), then a HOLD
  resource with a longer life. Two halves of one art (rotate 180) = something that splits (Hi-Yah Chop).
- Impact kit of moves: `flash_screen(n)`, `shake_defender(amp, count)`, `func(48)` knockback,
  `func(68, ...)` screen shake, `func(34, 8, 0, 2, colour, strength, 0)` defender tint (34 with 2 = attacker),
  `func(33, 0, 1, from, to, colour)` background fade (lights down / flood blue / hot box).

## Testing (DeSmuME)

- **Ask before taking over DeSmuME if it's open** (Get-Process DeSmuME*). Never inject global keyboard input,
  never spam Lua windows, never blind-navigate the title screen.
- The current test battle: **hood-showcase slot 6** (Cyndaquil Lv13 vs a wild Pidgey Lv3, at the FIGHT menu).
  Pidgey's only move is FMJ (Tackle) too, so the showcase reel ALSO plays from the enemy side on its turn - make
  the capture long enough (~450 frames at step 4 for 3 animations) to check both sides. FIGHT = touch (128, 90),
  move 1 = touch (64, 51) (`--cmds` file).
- Keep showcase orders short (3-9 variants): a long reel takes minutes per turn. Fly's turn 1 leaves the
  attacker vanished - put 97 (turn 2 first) right after 25.
- `showcase()` locates the kits from the end of a/0/2/9 - it must skip `pad()`'s all-zero filler member (it once
  didn't: every animation loaded the wrong particle files and froze after the first one).
- Iterating: `python -I hood/test/fast_patch.py` re-patches just the kits + move scripts into the built
  hood-soulsilver.nds in about a second (no 2.5 min rebuild); then make the showcase. Full patch_rom.py once at the end.
- Showcase ROM (Tackle plays the variants in order, archives padded so savestates survive rebuilds):
  `python -I -c "import sys; sys.path.insert(0,'hood'); import battlefx; battlefx.showcase('hood-soulsilver.nds','hood-showcase.nds', order=[...])"`
- Capture: `python -I hood/test/capture.py --rom hood-showcase.nds --slot 3 --frames 300 --step 3 --lead 100`
  -> `hood/test/out/f_*.png`. Make 10-wide contact sheets (128x75 thumbnails) and READ them; zoom (crop + 2x)
  anything you can't judge. ~5 animations per 300-frame capture.
- Freeze = frames stop changing. Bisect by putting suspects first in the showcase order.
- Kit build traceback:
  ```python
  import sys; sys.path.insert(0, 'hood'); import ndspy.rom, ndspy.narc, gunfx
  rom = ndspy.rom.NintendoDSRom.fromFile(ROM)
  gunfx.build_files(ndspy.narc.NARC(rom.getFileByName("a/0/2/9")).files)
  ```
- When done, leave the showcase as `order=[5]` (FMJ's own animation) - the user plays that ROM; a full reel makes
  every Tackle take minutes.

## Checklist before saying "done"

- [ ] New art for every visible piece, readable in a contact sheet, quantized preview checked.
- [ ] Every text piece: pixel font, exact 1:1 / 2:1 scale, not rotated - zoomed in game, letters even.
- [ ] Every emitter in the right self_dest assertion list; build passes.
- [ ] Both sides make sense (offsets mirrored with `sx`, per-direction spray/mover resources).
- [ ] Recorded in DeSmuME, every animation viewed start to finish, no freeze, battlers back in place.
- [ ] Two-turn moves: both turns checked.
- [ ] Name/description still match (offer a rename if not; names <= 12 chars, apply with
      `hood/apply_move_names.py` / `hood/apply_move_desc.py`).
- [ ] Field move (HM / map-use TM)? Its name still makes sense in "use ___ to get across" lines. Renaming one:
      moves.json, then the old name in hood/data/dialogue + text_edits.json + msg_0211/0430, apply_move_names,
      apply_dialogue for those banks, apply_move_desc.
- [ ] Tell the user what each animation does, what you fixed, and what you couldn't test (enemy side).
