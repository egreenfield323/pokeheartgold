#!/usr/bin/env python3
"""One-off rename (2026-10-29): the catching items are kidnapping gear now, not balls. Rewrites the old hood names
in every text source (message banks, dialogue JSON, the hand-edit overlay, trainer/story text). items.json holds the
names themselves; apply_item_names.py writes the name banks. Idempotent."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TIERS = {"OG": "Whole Gang", "Plug": "Rug Roll", "Bando": "Duffel Bag", "Hood": "Nap Sack"}
SACKS = ["Zoo", "Trap", "Pool", "Crib", "Re-Up", "Late", "Drip", "VIP", "Night", "Henny", "Dash", "Day1", "Sport",
         "Park"]
# Kurt's apricorn balls are custom bags in different materials
MATERIALS = {"Fast": "Nylon", "Level": "Gator", "Lure": "Croc", "Heavy": "Denim", "Love": "Velvet",
             "Friend": "Suede", "Moon": "Satin"}

# a name can start right after a text code (\r, \n, \f: no word boundary) and wrap onto the next line (Hood\nBalls)
B = r"(?:(?<=\\[nrf])|\b)"
SEP = r"( |\\+n)"
RULES = [(rf"{B}([Aa])n OG Ball\b", r"\1 Whole Gang"), (rf"{B}HOOD BALLS\b", "SNATCH GEAR"),
         (rf"{B}Hood Ball Pocket\b", "Snatch Gear Pocket"), (r"types of Hood Balls\b", "types of snatch gear")]
NEW = {**TIERS, **{k: f"{k} Sack" for k in SACKS}, **{k: f"{v} Bag" for k, v in MATERIALS.items()}}


def _swap(new):
    a, b = new.split(" ")
    return lambda m: f"{a}{m.group(1)}{b}{m.group(2)}"


RULES += [(rf"{B}{re.escape(k)}{SEP}(?:Ball|Sack)(s?)\b", _swap(v)) for k, v in NEW.items()]


def rename(text):
    for pat, rep in RULES:
        text = re.sub(pat, rep, text)
    return text


def main():
    paths = list((ROOT / "files/msgdata/msg").glob("*.gmm")) + list((ROOT / "hood/data/dialogue").glob("*.json"))
    paths += [ROOT / "hood/data" / n for n in ("text_edits.json", "trainer_dialogue.json", "story_text.json")]
    n = 0
    for p in paths:
        s = p.read_text(encoding="utf-8")
        t = rename(s)
        if t != s:
            p.write_text(t, encoding="utf-8", newline="\n")
            n += 1
    print(f"sack names: {n} files")


if __name__ == "__main__":
    main()
