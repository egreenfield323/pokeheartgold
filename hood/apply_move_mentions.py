#!/usr/bin/env python3
"""Move names mentioned in dialogue (TM gifts, field-move prompts, battle messages, item descriptions, tips...)
updated to the hood names, through the text-edit overlay (hood/data/text_edits.json) so the checks for line
width / box size / buffer length apply and the edits survive re-running the other apply scripts.

MENTIONS lists every row that talks about a move, and which names in it are moves - a lot of rows use the same
words for something else (Lake of Rage, Toxic Orb, the Copycat girl, Psychic-type, "Charge yourself with
friendship", gym Chains, debug menus...), so nothing is replaced unless it's listed here.
Run from the repo root:  python hood/apply_move_mentions.py [--dry]
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import text_edits as te  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
MOVES = json.loads((ROOT / "hood/data/moves.json").read_text(encoding="utf-8"))
ALL = "*"                                       # every move name in the row is a move

# bank -> {row: [original move names to replace] or ALL}
MENTIONS = {
    "msg_0026": {63: ["Strength"]},                                              # trainer card records
    "msg_0047_D01R0101": {16: ["Thunder Fang"], 17: ["Thunder Fang"]},           # Brock's RHYHORN
    "msg_0053_D11R0106": {3: ["Overheat"]},                                      # Blaine's TM
    "msg_0056_D15R0103": {4: ["Flash"], 5: ["Flash"]},
    "msg_0063_D22R0102": {6: ["Spore"]},
    "msg_0066_D23R0102": {61: ALL, 62: ALL, 63: ALL},                            # quiz answers
    "msg_0067_D23R0103": {7: ["Sunny Day"]},
    "msg_0070_D23R0106": {9: ["Fake Out"]},
    "msg_0111_D35R0101": {4: ["Hyper Beam"]},                                    # Lance
    "msg_0113_D35R0103": {17: ["Whirlpool"]},
    "msg_0115_D36R0101": {8: ["Cut"], 11: ALL, 16: ALL, 17: ALL, 19: ALL, 23: ALL, 25: ALL, 26: ALL},
    "msg_0122_D39R0101": {2: ["Waterfall"]},
    "msg_0129_D44R0102": {3: ["Dragon Pulse"], 5: ["Surf"]},
    "msg_0136_D48R0101": {8: ["Rock Climb", "Surf"]},
    "msg_0168": {42: ["Selfdestruct"], 43: ["Explosion"]},                       # trainer card records
    "msg_0191": {423: ["Light Screen", "Reflect"]},
    "msg_0197": {r: ALL for r in (200, 201, 202, 203, 204, 245, 246, 247, 273, 274, 275, 296, 297, 298, 427,
                                  428, 448, 494, 495, 496, 571, 572, 573, 574, 575, 576, 798, 997, 1004, 1085,
                                  1086, 1241, 1242)},                                # battle messages
    "msg_0211": {r: ALL for r in (1, 3, 5, 7, 8, 10, 11, 12, 15, 16, 17, 18, 20, 21, 23, 24, 25, 27, 28, 29, 30,
                                  32, 33)},                                          # field moves
    "msg_0221": {269: ["Light Screen", "Reflect"], 282: ["Hail"], 283: ["Sandstorm"], 284: ["Sunny Day"],
                 285: ["Rain Dance"], 286: ["Bind", "Wrap"], 358: ["Light Screen", "Reflect"]},   # item text
    "msg_0246": {51: ["Spore"]},
    "msg_0273": {5: ["Fly"], 7: ["Fly"]},                                        # the Fly map
    "msg_0345_R10R0202": {13: ["Charge Beam"], 17: ["Charge Beam"]},
    "msg_0370_R27R0101": {2: ["Sandstorm"]},
    "msg_0372_R28R0101": {2: ["Steel Wing"]},
    "msg_0378_R31": {8: ["Rest"]},
    "msg_0386_R34R0201": {2: ["Taunt"]},
    "msg_0390_R36": {5: ["Rock Smash"], 12: ["Dig"]},
    "msg_0393_R37": {1: ["Dig"]},
    "msg_0396_R39": {2: ["Headbutt"]},
    "msg_0397_R39R0101": {10: ["Natural Gift"]},
    "msg_0399_R42": {6: ["Strength"]},
    "msg_0403_R43R0201": {6: ["Sludge Bomb"]},
    "msg_0413": {21: ["Surf"]},                                                  # TV
    "msg_0419": {4: ["Flash"]},                                                  # radio
    "msg_0430": {48: ["Surf"]},
    "msg_0451_T01R0301": {56: ["Rock Climb"], 57: ["Rock Climb"]},               # Prof. Oak
    "msg_0452_T02": {6: ["Dream Eater"]},
    "msg_0454_T02GYM0101": {3: ["Rock Climb"], 4: ["Trick Room"]},               # Blue
    "msg_0462_T03GYM0101": {3: ["Rock Slide"], 4: ["Rock Slide"]},               # Brock
    "msg_0467_T04": {5: ["Psychic"]},                                            # SLOWBRO's Psychic
    "msg_0469_T04GYM0101": {12: ["Water Pulse"]},                                # Misty
    "msg_0485_T06GYM0101": {4: ["Shock Wave"]},                                  # Lt. Surge
    "msg_0492_T07GYM0101": {3: ["Giga Drain"]},                                  # Erika
    "msg_0509_T07R0501": {2: ["Hidden Power"], 3: ["Hidden Power"], 4: ["Hidden Power"], 5: ["Hidden Power"],
                          8: ["Hidden Power"]},
    "msg_0514_T08GYM0101": {3: ["Poison Jab"]},                                  # Janine
    "msg_0522_T10R0101": {1: ["Fly"]},
    "msg_0531_T11GYM0101": {4: ["Skill Swap"]},                                  # Sabrina
    "msg_0534_T11R0501": {1: ["Psychic"]},                                       # TM29
    "msg_0558_T22GYM0101": {3: ["Rock Smash"], 4: ["Roost"]},                    # Falkner
    "msg_0560_T22R0301": {16: ["Sleep Talk", "Snore"]},
    "msg_0567_T23GYM0102": {3: ["Cut"], 5: ["U-turn"]},                          # Bugsy
    "msg_0572_T24": {0: ["Fly"], 1: ["Fly"], 4: ["Fly"], 12: ["Fly"], 13: ["Rock Smash"]},
    "msg_0574_T24GYM0101": {5: ["Fly"], 6: ["Focus Punch"]},                     # Chuck
    "msg_0582_T25GYM0101": {5: ["Strength"], 7: ["Attract"]},                    # Whitney
    "msg_0606_T26GYM0101": {5: ["Iron Tail"]},                                   # Jasmine
    "msg_0611_T26R0701": {0: ["Strength"]},
    "msg_0612_T27": {10: ["Surf"]},
    "msg_0614_T27GYM0101": {3: ["Surf"], 5: ["Shadow Ball"]},                    # Morty
    "msg_0618_T27R0501": {28: ["Surf"]},
    "msg_0622_T28GYM0101": {3: ["Whirlpool"], 4: ["Hail"]},                      # Pryce
    "msg_0627_T29R0101": {2: ["Hidden Power"]},
    "msg_0631_T30GYM0101": {7: ["Dragon Pulse"]},                                # Clair
    "msg_0635_T30R0601": {42: ["Draco Meteor"], 52: ["Blast Burn"], 53: ["Hydro Cannon"], 54: ["Frenzy Plant"]},
    "msg_0666": {50: ["Headbutt"]},
    "msg_0691": {24: ["Fly"], 25: ["Fly"]},
    "msg_0704": {r: ALL for r in (10, 11, 13, 14, 15, 16, 17, 18)},              # "Did you know...?" tips
    "msg_0724": {102: ["Meteor Mash"], 103: ["Meteor Mash"]},
    "msg_0744_W40": {16: ["Surf"], 17: ["Surf"]},
}
# rows that need more than a name swap: (text after the swap, what it becomes). Raw strings: the game text's
# line codes are a literal backslash + n / r / f
REWRITES = {
    ("msg_0378_R31", 8): (r"“recover fast” became\nshortened to “Nap,”", r"“need a nap” became\nshortened to “Nap,”"),
    ("msg_0691", 24): ("What do you mean by Catch Flight?", "What’s that?"),       # (buffer length)
    ("msg_0691", 25): ("What do you mean by Catch Flight?", "What’s that?"),
    # (re-worded so the longer names don't split across lines or leave a word on its own)
    ("msg_0221", 269): (r"duration of barrier moves like Riot\nShield and Bulletproof used by the holder.",
                        r"duration of the holder’s barrier moves\nlike Riot Shield and Bulletproof."),
    ("msg_0390_R36", 5): ("It contains make-’em-faint Smash n Grab.", r"It contains make-’em-faint\nSmash n Grab."),
    ("msg_0704", 14): ("If your opponent is Flying, your Fan Blast", "If your foe is Flying, your Fan Blast"),
    ("msg_0744_W40", 16): (r"I see... You don’t have Hydrant Wave yet...\nThis is just between you and me...\r"
                           r"I got Hydrant Wave from a man at Ecruteak,\nand I think he’s still there.",
                           r"I see... No Hydrant Wave yet...\nThis is just between you and me...\r"
                           r"A man in Ecruteak gave me\nHydrant Wave. I bet he’s still there."),
    ("msg_0744_W40", 17): (r"you and me.\nI got Hydrant Wave from a man at Ecruteak.\fI think he’s still there.",
                           r"you and me.\fA man in Ecruteak gave me\nHydrant Wave. I bet he’s still there."),
}

START = r"(?:(?<![A-Za-z])|(?<=\\[nrf]))"       # a word start - also right after a \n / \r / \f code
GAP = r"(?: |\\n|\\r|\\f)+"                      # a two-word name may wrap onto the next line


def replace(text, olds):
    """Every listed name to its hood name in ONE pass (one after another, Magic Coat -> Bounce Back would then
    have its Bounce renamed too); longest names first, so Thunder Fang wins over Thunder."""
    # hood names already in the text match as themselves and stay (so a re-run doesn't turn Bounce Back into
    # Pogo Stick Back, or Loud Snore into Loud Loud Snore)
    hood = {v for k, v in MOVES.items() if not k.startswith("_")} - set(olds)
    names = sorted(set(olds) | hood, key=len, reverse=True)
    pat = re.compile(START + "(?:" + "|".join(GAP.join(re.escape(w) for w in n.split(" ")) for n in names)
                     + r")(?![a-z])")

    def sub(m):
        found = re.sub(GAP, " ", m.group(0))
        if found not in olds:
            return m.group(0)
        new = MOVES[found]
        gaps = re.findall(GAP, m.group(0))                       # keep a line break the name wrapped on
        if gaps and gaps[0] != " " and " " in new:
            a, b = new.split(" ", 1)
            return a + gaps[0] + b
        return new
    return pat.sub(sub, text)


def rewrap(text, lim):
    """Fix lines the longer name pushed too wide, keeping the original line breaks where it can: a too-wide
    line's last words go onto a new line after it if its box has room, else onto the start of the next line
    of the same text (a box that scrolls on with \\f continues it), else into a new box that scrolls on."""
    width = lambda line: te.line_px(te.parts(line))
    end = te.ending(text)
    paras = te.body(text).split("\\r")
    for p, para in enumerate(paras):
        boxes = [b.split("\\n") for b in para.split("\\f")]
        b = 0
        while b < len(boxes):
            box = boxes[b]
            i = 0
            while i < len(box):
                words = box[i].split(" ")
                spill = []
                while width(" ".join(words)) > lim["px"] and len(words) > 1:
                    spill.insert(0, words.pop())
                box[i] = " ".join(words)
                if spill:
                    if len(box) < lim["lines"]:
                        box.insert(i + 1, " ".join(spill))
                    elif i + 1 < len(box):
                        box[i + 1] = " ".join(spill + [box[i + 1]])
                    elif b + 1 < len(boxes):
                        boxes[b + 1][0] = " ".join(spill + [boxes[b + 1][0]])
                    else:
                        boxes.append([" ".join(spill)])
                i += 1
            b += 1
        paras[p] = "\\f".join("\\n".join(box) for box in boxes)
    return "\\r".join(paras) + end


def main():
    dry = "--dry" in sys.argv
    names = list(MENTIONS)
    base = te.base_banks(names)
    edits = te.load_edits()
    renamed = {k: v for k, v in MOVES.items() if not k.startswith("_") and k != v and k != "Block"}
    errors, changed = [], 0
    for name, rows in MENTIONS.items():
        cur = te.rows_of((te.MSG / f"{name}.gmm").read_text(encoding="utf-8"))
        limits = te.Limits(name, base[name])
        new_rows = {}
        for i, olds in rows.items():
            if i not in cur:
                errors.append(f"{name}:{i}: no such row")
                continue
            text = replace(cur[i], renamed if olds == ALL else olds)
            if (name, i) in REWRITES:
                a, b = REWRITES[(name, i)]
                if a not in text and b not in text:                  # (b: already done on an earlier run)
                    errors.append(f"{name}:{i}: rewrite doesn't match the text any more")
                text = text.replace(a, b)
            if text == cur[i]:
                continue
            text = rewrap(text, limits.for_row(name, base[name].get(i, cur[i]), cur[i]))
            text, errs = te.check(name, base[name].get(i, cur[i]), cur[i], text, limits)
            if errs:
                errors.append(f"{name}:{i}: {'; '.join(errs)}\n    {text}")
                continue
            new_rows[i] = text
            if dry:
                print(f"{name}:{i}: {text}")
        if new_rows and not dry:
            te.write_rows(name, new_rows)
            edits.setdefault(name, {}).update({str(i): t for i, t in new_rows.items()})
        changed += len(new_rows)
    if not dry:
        te.save_edits(edits)
    print(f"move mentions: {changed} rows {'would change' if dry else 'updated'}")
    if errors:
        print("\n".join(errors))
        sys.exit(1)


if __name__ == "__main__":
    main()
