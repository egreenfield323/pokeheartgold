# Hood HeartGold

A parody reskin of the HeartGold decomp. Your Pokémon are your gang, the starters are straps, and every trainer is somebody from the block.

## What changes

| Area | Data file | Game files touched |
|---|---|---|
| Move names (12 max) + "X hit 'em with Y!" | `data/moves.json` | `msg_0750`, `0751`, `0003` |
| Items: Poké Ball → Burner, Potion → Band-Aid… | `data/items.json` | `msg_0222`, `0223`, `0224` |
| Trainer classes: Youngster → Corner Boy… | `data/trainer_classes.json` | `msg_0730`, `0731` |
| Trainer trash talk (all 738 trainers) | `data/trainer_dialogue.json` | `poketool/trainer/trainers.json` |
| Oak intro, Elm's lab, starter pick, battle text | `data/story_text.json` | `msg_0219`, `0543`, `0190`, `0197` |
| Starter lines get +20% stats; AR15 line is Steel/Dark | `apply_hood.py` | `personal.json` |
| AR15 line learns FMJ / Reload / Hollow Point / Steel Core | `apply_hood.py` | `wotbl.narc` |
| Team Rocket → The Feds (all game text; Grunts → Agents) | `data/story_text.json` `global_replace` | every `msg_*.gmm` that mentions them |
| Battle sprites: original Pokémon, now strapped (gun by strength + drip) | `make_sprites.py`, `data/drip.json` | `poketool/pokegra/pokegra/*/*.png` |

### Starters
Every Pokémon keeps its real name. They just come strapped:
- **Chikorita**: .22 → Bayleef: revolver → Meganium: .357 Magnum
- **Cyndaquil**: Beretta → Quilava: Extendo → Typhlosion: Draco
- **Totodile**: Glock → Croconaw: Glock with a light → Feraligatr: drum-mag AK
- **Larvitar**: AR-15 → Pupitar: AR-15 with a bump stock → Tyranitar: M4. It learns **FMJ**, **Hollow Point**, **Steel Core** and **Reload** (renamed Tackle, Crunch, Iron Head and Recover).

## Sprites

`python hood/make_sprites.py` takes the **original** sprites (read from git, so re-running is safe) and draws an evolving gun on every Pokémon. The guns are drawn by `gunart.py`.

- **Gun families.** Every evolution line gets a family, and the gun upgrades with each stage:

  | Family | Stage 1 → 2 → 3 |
  |---|---|
  | Revolver | .22 → .38 → gold .357 Magnum |
  | Pistol | Beretta → Extendo → Draco |
  | Glock | Glock → Glock with light → drum-mag AK |
  | Rifle | AR-15 → bump-stock AR → M4 |
  | Shotgun | sawed-off → pump → drum auto-shotgun |
  | SMG | Uzi → MAC-10 → LMG |

  Single-stage Pokémon pick a rung by base stat total. Legendaries carry a sniper, grenade launcher, minigun or RPG, depending on strength.
- **Accent colors.** Grips, mags and stocks take the Pokémon's own signature color. In the shiny palette the gun is gold-plated, and on the front sprite's second frame it fires.
- **Auto-drip on every Pokémon**, front and back. Each item is new pixel art overlaid on the sprite (no recolored pixels), placed around the head. The script finds the head by detecting pupils, or by a silhouette guess that leans toward the opponent. 94 front/back views have hand-set `head_front` / `head_back` points in `data/drip.json`. In the second animation frame, every item is motion-tracked so it moves with the body:
  - **Headwear** drawn on top of the head: durag with tails, ribbed beanie with pom, backwards snapback with brim and button, or bandana with knot (`hats.py`).
  - **A chain** on the chest.
  - **Kicks** on any feet it detects. Evolved Pokémon get Jordans, in red if the sprite already has a red and black/white otherwise.
  - **Iced-out sparkles** for strong final evolutions and legendaries.
  - Colors come from the sprite's own palette, so nothing gets washed out.
- **Back-sprite guns** are held at the side and aimed off-screen toward the opponent.
- **Hand-placed drip** in `data/drip.json` replaces the auto item of the same kind (head, chain or shoes). Set `"auto": false` to turn auto-drip off for a Pokémon. Available items: chains, grillz, shades, white kicks or Jordans, saggy jeans, durags, beanies, cigarettes, a glass pipe, a brick, weed leaves, sparkles, and full recolors. Each entry can also override the grip position (`hand_front`), the gun size (`gun_scale`) or the gun itself (`gun`). The coordinates are pixels in the sprite's first 80×80 frame.
- **Palette slots.** Each sprite has only 16 colors. The script requests only the colors that sprite's gun and drip use, reuses the sprite's own colors where they're close, and merges near-identical shades only as a last resort.
- `--preview out.png --only 25,155 [--cols 3 --zoom 3]` renders a contact sheet without touching the game files.

## Overworld sprites

`python hood/make_overworld.py` dresses every overworld Pokémon texture (`files/data/mmodel/mmodel/*.NSBTX`, 568 files):

- **Which sprites:** the walking follower, the overworld legendaries you walk up to (Lugia, Ho-Oh, the beasts, etc. all use these same sprites), the red Gyarados, and the sleeping Snorlax.
- **Frames:** each file has 8 frames (away, toward, left, right; two walk frames each). Every frame gets the same hat the Pokémon wears in battle and a mini gun from its battle gun's class: pistol, SMG, rifle, or RPG for legendaries. Frames facing the camera also get a chain. Shiny palettes get gold guns.
- **Format:** `nsbtx.py` reads and writes the textures in place. Only pixel and palette bytes change, never the file layout.
- `--preview out.png --only 6,249` renders a contact sheet.

`python hood/make_title.py` gives the 3D Ho-Oh on the title screen sunglasses and a gold grill by painting its eye and mouth textures. The title-screen Lugia has no face texture (its look comes from vertex colors), so it can't get drip without editing the mesh. The legendary encounter cutscenes show the overworld sprite, which is already dressed, and the Celebi cutscene's own copy is dressed too.

## Dialogue

- **Hand-written lines:** each `data/dialogue/<bank>.json` replaces whole lines. This covers the full opening of the game: Oak's intro, your house (Mom), New Bark Town, Elm's lab, Lyra's house, Routes 29 and 30, Cherrygrove (the Guide Gent), Mr. Pokémon's house with Oak, and the bag descriptions. The apply script requires the same control codes and the same box ending as the original line, so scripts keep working.
- **Everything else:** gets the slang swaps in `story_text.json` `global_replace` (Block/Block Boss/Chains/Hood Ball/homie/bread/...).
  - Each swap is kept only if the line still fits the text box, re-wrapping the box's words when needed.
  - `bank_replace` holds the battle-only swaps (status effects).
- **Trainer lines:** all 1,717 are written into bank 0728, the in-game copy, through the `trtbl` (trainer, type) → row table.

## Everything else

| Script | What it dresses |
|---|---|
| `make_forms.py` | 78 alternate-form battle sprites: Unown letters, Deoxys, Rotom, Arceus, Burmy and the rest |
| `make_icons.py` | 541 party / PC box icons. They use 3 shared palettes, so drip uses colors those palettes already have. Hats go above detected pupils. |
| `make_trainers.py` | 129 trainer battle sprites (`files/a/0/5/8`): a gun by rank (minigun for the Champion and Rocket Boss, M4 for Gym Leaders and Elite Four, AR/MAC/pistols below) plus a chain. The bitmap is decrypted DP-style and re-encrypted with its own key, and the cell-drawn copy is rebuilt for the 95 classes whose layout round-trips exactly. |
| `make_npcs.py` | 215 overworld people: hats and chains for everyone, guns for gang types. The player wears a durag, chain and pistol in every state. Lyra/Ethan wear a red bandana. Oak is in a wife beater with bare legs, Elm in a stained coat, both with powder under the nose. |
| `make_intro.py` | Oak's intro portrait: wife beater, drawers, powder under the nose |
| `make_items.py` | Bag icons: Hennessy / Henny XO / Patrón bottles, Ace o Spades / Grey Goose, Red Bull / Icy Hot cans |
| `make_anims.py` | Gun-named moves borrow existing projectile animations: FMJ, Hollow Point, Double/Triple Tap use Bullet Seed; Steel Core and Spray n Pray use Pin Missile |
| `make_walker.py` | Pokéwalker 4-shade pictures and route icons (`files/a/2/5/6`, `files/a/2/4/8`), with LZ10 recompression and a NARC rebuild |

The Pokédex reuses the battle sprites and icons, so it's covered by the scripts above.


## Playing it (no compiler needed)

```sh
pip install ndspy pillow
python hood/patch_rom.py path/to/your-dump.nds hood-heartgold.nds
```

Then open the output in melonDS (`winget install melonDS.melonDS`).

- **Supported ROMs:** US HeartGold (`IPKE`) or US SoulSilver (`IPGE`). The two share every file this mod changes. On SoulSilver the title screen shows Lugia, which can't take drip.
- **How it works:** every changed asset is rebuilt with the game's own encoders in `hood/bin/` (`hood/build_tools.sh` rebuilds them) and swapped into the ROM's archives. The game code isn't touched.
- **Safety check:** before replacing any file, the patcher checks that your ROM's original copy matches the decomp. If anything differs, it writes nothing.

## Re-applying after edits

The script maps *original* names to new ones, so run it on clean files:

```sh
git checkout -- files/
python hood/apply_hood.py
python hood/make_sprites.py
python hood/make_overworld.py
python hood/make_title.py
python hood/make_forms.py
python hood/make_icons.py
python hood/make_trainers.py
python hood/make_walker.py
python hood/make_npcs.py
python hood/make_intro.py
python hood/make_items.py
python hood/make_anims.py
```

It checks every string against `charmap.txt`, the name length limits and the line widths before it writes anything. If any check fails, it aborts.

## Building

Build it the normal way (see `../INSTALL.md`). You need MWCC and the Nitro SDK. The ROM won't match the original sha1 any more, so don't use `make compare`.
