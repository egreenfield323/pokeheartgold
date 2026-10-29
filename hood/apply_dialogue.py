#!/usr/bin/env python3
"""Write the hand-written hood dialogue (hood/data/dialogue/<bank>.json) into the message banks, without
re-running the whole reskin (apply_hood.py only works on clean files).

Every row goes through the same checks apply_hood.py makes (the original's command tokens, the original's ending
code, lines of at most 38 characters) and through text_edits.check (characters the font has, pixel width, lines
per text box, buffer size). Rows the hand-edit overlay (hood/data/text_edits.json) owns are rewritten there too,
or the overlay would put the old text back; a house-break-in threat (apply_house_threats.py) that opens the old
row is kept in front of the new text.
Run from the repo root:  python hood/apply_dialogue.py [bank ...] [--dry-run]
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_house_threats as aht  # noqa: E402
import text_edits as te  # noqa: E402

DIALOGUE = Path(__file__).resolve().parent / "data" / "dialogue"
BS = "\\"


def tokens(t):
    return sorted(x for x in re.findall(r"\{[^}]*\}", t) if not x.startswith(("{COLOR", "{SIZE")))


def plain_lines(t):
    t = re.sub(r"\{[^}]*\}", "", t)
    return re.split(r"\\[nrf]", t)


def load(bank):
    raw = json.loads((DIALOGUE / f"{bank}.json").read_text(encoding="utf-8"))
    rows = {}
    for k, v in raw.items():
        if k.startswith("_"):
            continue
        rows[int(k)] = v.replace("\n", BS + "n").replace("\r", BS + "r").replace("\f", BS + "f")
    return rows


def gmm_name(name):
    """The bank's .gmm stem: the json may leave off the map suffix (msg_0542 for msg_0542_T20)."""
    hits = list(te.MSG.glob(name + ".gmm")) or list(te.MSG.glob(name + "_*.gmm"))
    if len(hits) != 1:
        sys.exit(f"{name}: no single message bank matches ({[h.stem for h in hits]})")
    return hits[0].stem


A = "['’]"
# Plain-English phrasing -> hood. Lowercase words only (a capital first letter is kept), so names, move names, types
# and places ("Fighting Dojo", "Catching Show") are never touched.
NOT_TO = "(?!the|a|an|my|your|his|her|their|our|this|that|these|those)"
SLANG = [  # (must-not-follow guard before the phrase, phrase, replacement)
    ("", "trying to", "tryna"),
    (r"(?<!get )(?<!got )", rf"going to(?= {NOT_TO}[a-z])", "gon'"),
    ("", "gonna", "gon'"),
    ("", "want to", "wanna"),
    (r"(?<!will )(?<!to )(?<!['’]d )(?<!['’]ll )", "have to", "gotta"),
    ("", "has to", "gotta"),
    ("", "kind of", "kinda"),
    ("", "sort of", "sorta"),
    ("", "out of", "outta"),
    ("", "a lot of", "a lotta"),
    ("", "let me", "lemme"),
    ("", "give me", "gimme"),
    ("", "about to", "'bout to"),
    ("", "because", "'cause"),
    ("", "probably", "prob'ly"),
    ("", "excuse me", "'scuse me"),
    ("", rf"isn{A}t", "ain't"),
    ("", rf"aren{A}t", "ain't"),
    ("", "am not", "ain't"),
    ("", rf"haven{A}t", "ain't"),
    ("", rf"hasn{A}t", "ain't"),
    ("", rf"doesn{A}t", "don't"),
    ("", rf"you{A}re", "you"),
    ("", rf"they{A}re", "they"),
    ("", rf"we{A}re", "we"),
    ("", "children", "kids"),
    ("", "friends", "homies"),
    ("", "friend", "homie"),
    ("", "money", "bread"),
    ("", "very", "hella"),
    ("", "hello", "wassup"),
    ("", "hey", "ayo"),
    ("", "thank you", "good looks"),
    ("", "thanks for", "good looks for"),
    ("", "wow", "sheesh"),
    ("", "what's up", "wassup"),
    ("", "what’s up", "wassup"),
    ("", "come on", "c'mon"),
    ("", "i am", "I'm"),
    ("", "you are", "you"),
    ("", "they are", "they"),
    ("", "we are", "we"),
    ("", "everyone", "everybody"),
    ("", "someone", "somebody"),
    ("", "anyone", "anybody"),
    ("", "no one", "nobody"),
    ("", "does not", "don't"),
    ("", "do not", "don't"),
    ("", "cannot", "can't"),
    ("", "will not", "won't"),
    ("", rf"should(?: have|{A}ve)", "shoulda"),
    ("", rf"would(?: have|{A}ve)", "woulda"),
    ("", rf"could(?: have|{A}ve)", "coulda"),
    ("", "isn't it", "ain't it"),
    ("", "really", "deadass"),
]
SLANG_RE = [(re.compile(rf"(?<![\w’']){g}([{p[0].upper()}{p[0]}]){p[1:]}(?![\w’'])"), r) for g, p, r in SLANG]
KEEP_ING = {"string", "spring", "sling", "swing", "sting", "cling", "fling", "wring", "ceiling", "during", "awning",
            "pudding", "sibling", "darling", "ping", "king", "thing", "things", "bring", "sing", "ring", "wing"}
ING = re.compile(r"(?<![\w’'{])([a-z]{3,}?)ing(?![\w’'])")
ESC = {"\\n": "\x01", "\\r": "\x02", "\\f": "\x03"}
# Rows that must keep their wording (Buena's password answers have to match the radio show).
FROZEN = {"msg_0066_D23R0101": range(40, 70)}


def slang(text):
    """Push a row's plain English toward hood talk; {tokens} are left alone."""
    for k, v in ESC.items():
        text = text.replace(k, v)
    parts = re.split(r"(\{[^}]*\})", text)
    for n, part in enumerate(parts):
        if part.startswith("{"):
            continue
        for rx, rep in SLANG_RE:
            part = rx.sub(lambda m, rep=rep: rep[0].upper() + rep[1:] if m.group(1).isupper() else rep, part)
        part = ING.sub(lambda m: m.group(0) if m.group(0) in KEEP_ING else m.group(1) + "in'", part)
        parts[n] = part
    text = "".join(parts)
    for k, v in ESC.items():
        text = text.replace(v, k)
    return text


def reflow(text, px, lines, maxlen):
    """Re-wrap each box of `text` to fit `px` / `maxlen` per line and `lines` per box; a box that grows past
    `lines` spills into new \f boxes. Line breaks the writer put inside a box are treated as spaces."""
    end = te.ending(text)
    toks = {}

    def hide(m):
        key = f"{len(toks)}"
        toks[key] = m.group(0)
        return key
    body = re.sub(r"\{[^}]*\}", hide, text[:len(text) - len(end)])
    pieces = re.split(r"(\\[rf])", body)
    space = te.char_px(" ")

    def width(w):
        for k, v in toks.items():
            w = w.replace(k, v)
        return te.line_px(te.parts(w)), len(re.sub(r"\{[^}]*\}", "", w))
    out = []
    for n, piece in enumerate(pieces):
        if n % 2:
            out.append(piece)
            continue
        words = piece.replace(BS + "n", " ").split()
        rows, cur, cw, cl = [], [], 0, 0
        for w in words:
            ww, wl = width(w)
            if cur and (cw + space + ww > px or cl + 1 + wl > maxlen):
                rows.append(" ".join(cur))
                cur, cw, cl = [], 0, 0
            cw, cl = (cw + space + ww, cl + 1 + wl) if cur else (ww, wl)
            cur.append(w)
        if cur:
            rows.append(" ".join(cur))
        chunks = [rows[i:i + lines] for i in range(0, len(rows), lines)] or [[]]
        out.append((BS + "f").join((BS + "n").join(c) for c in chunks))
    res = "".join(out) + end
    for k, v in toks.items():
        res = res.replace(k, v)
    return res


def threat_of(text):
    for t in aht.THREATS:
        tt = t.replace("'", "’")
        if text.startswith(tt + BS + "r"):
            return tt
    return None


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    names = args or sorted(p.stem for p in DIALOGUE.glob("*.json"))
    gmm = {n: gmm_name(n) for n in names}                  # msg_0542.json -> msg_0542_T20.gmm
    banks = [gmm[n] for n in names]
    base = te.base_banks(banks)
    edits = te.load_edits()
    errors, written, staged = [], 0, {}
    for name, bank in gmm.items():
        rows = load(name)
        current = te.rows_of((te.MSG / f"{bank}.gmm").read_text(encoding="utf-8"))
        limits = te.Limits(bank, base[bank])
        # Lines may run as long as the bank's longest original line (38 at least); pixel width is checked too.
        maxlen = max([38] + [len(ln) for t in base[bank].values() for ln in plain_lines(t)])
        out = {}
        frozen = FROZEN.get(bank, ())
        # Rows the json leaves alone still get the slang pass; one that then fails a check just stays as it was.
        for i, cur in current.items():
            if i in rows or i in frozen or i not in base[bank] or not cur:
                continue
            text = slang(cur)
            if text == cur or tokens(text) != tokens(base[bank][i]):
                continue
            final, errs = te.check(bank, base[bank][i], cur, text, limits)
            if errs:
                continue
            out[i] = final
            if edits.get(bank, {}).get(str(i)) is not None:
                edits[bank][str(i)] = final
        for i, text in rows.items():
            if i not in base[bank]:
                errors.append(f"{bank}[{i}]: no such row")
                continue
            if i not in frozen:
                text = slang(text)
            orig, cur = base[bank][i], current.get(i, "")
            over = edits.get(bank, {}).get(str(i))
            threat = threat_of(over) if over else None
            if threat and not text.startswith(threat):
                text = threat + BS + "r" + text
            if tokens(text) != tokens(orig):
                errors.append(f"{bank}[{i}]: codes differ from the original: {tokens(orig)} vs {tokens(text)}")
            lim = limits.for_row(bank, orig, cur)
            if any(len(ln) > maxlen for ln in plain_lines(text)) or te.check(bank, orig, cur, text, limits)[1]:
                fixed = reflow(text, lim["px"], lim["lines"], maxlen)
                if not te.check(bank, orig, cur, fixed, limits)[1]:
                    text = fixed
            for ln in plain_lines(text):
                if len(ln) > maxlen:
                    errors.append(f"{bank}[{i}]: line over {maxlen} chars ({len(ln)}): {ln!r}")
            final, errs = te.check(bank, orig, cur, text, limits)
            errors += [f"{bank}[{i}]: {e}" for e in errs]
            out[i] = final
            if over is not None:
                edits[bank][str(i)] = final
        staged[bank] = out
        written += len(out)
    if errors:
        print("\n".join(errors))
        sys.exit(f"{len(errors)} problem(s). Nothing was written.")
    if not dry:
        for bank, out in staged.items():
            te.write_rows(bank, out)
        te.save_edits(edits)
    print(f"dialogue: {written} rows in {len(banks)} banks {'checked' if dry else 'written'}")


if __name__ == "__main__":
    main()
