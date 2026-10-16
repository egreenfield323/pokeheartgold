#!/usr/bin/env python3
"""Drip editor: a little local web app for hand-placing drip (hats, chains, kicks, grillz, guns, ...) on
Pokémon battle sprites, trainer battle sprites and overworld people (the player, Mom, the rival, every NPC).

    python hood/drip_editor.py            # then open http://localhost:8765 (opens by itself)

Pick something, drag its drip around, add or delete pieces, change styles/colours, move or resize the gun, and
Save. Rendering is the real generators (make_sprites.arm, make_trainers.dress_class, make_npcs.dress), so what
you see is what goes in the game. Save writes the hand-placed spec and regenerates the game files:
    Pokémon   hood/data/drip.json          -> its battle sprites + party icon
    trainers  hood/data/trainer_drip.json  -> the trainer sprite NARC (files/a/0/5/8)
    people    hood/data/npc_drip.json      -> its overworld model (files/data/mmodel/mmodel/*.NSBTX)

A view you've edited is stored in full ("auto_<view>": false plus every piece), so the automatic placement no
longer touches it. "Reset view" drops that and goes back to automatic.
"""
import base64
import functools
import json
import random
import re
import subprocess
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from PIL import Image

HOOD = Path(__file__).resolve().parent
sys.path.insert(0, str(HOOD))
import gunart  # noqa: E402
import make_sprites as ms  # noqa: E402
ms.git_blob = functools.lru_cache(maxsize=None)(ms.git_blob)   # originals never change: read each blob once
import make_npcs as mn  # noqa: E402
import make_trainers as mt  # noqa: E402

PORT = 8765
PAGE = HOOD / "drip_editor.html"
GUNS = list(gunart.GUNS)
BATTLE_COLORS = ["k", *ms.COLORS]


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def store(path, key, spec):
    data = read_json(path)
    if [k for k in spec if not k.startswith("_")]:
        data[key] = spec
    else:
        data.pop(key, None)
    write_json(path, data)


def png_url(im):
    buf = BytesIO()
    im.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def as_rgba(im, pal):
    im = im.copy()
    im.putpalette([v for c in pal for v in c])
    im.info["transparency"] = 0
    return im.convert("RGBA")


def strip(frames, pal):
    """Frames (lists of palette-index rows) side by side, as an RGBA image."""
    h, w = len(frames[0]), len(frames[0][0])
    im = Image.new("P", (w * len(frames), h))
    im.putdata([v for y in range(h) for f in frames for v in f[y]])
    return as_rgba(im, pal)


def view(info, png, orig, fw, fh, n, body):
    return dict(info, png=png_url(png), orig=png_url(orig), fw=fw, fh=fh, frames=n, body=body)


# ------------------------------------------------------------------ Pokémon battle sprites

class Pokemon:
    title, linked, views = "Pokémon", False, ("front", "back")

    def __init__(self):
        self.plan, self.names = ms.gun_plan()

    def name(self, n):
        return self.names[n].replace("SPECIES_", "").replace("_", " ").title()

    def specs(self):
        return read_json(ms.DRIP)

    def entries(self):
        return [(n, self.name(n)) for n in range(1, 494)]

    def load(self, n, spec):
        return {"name": self.name(n), "default_gun": self.plan[n], "guns": GUNS, "colors": BATTLE_COLORS}

    def render(self, n, spec):
        report = {}
        res = ms.arm(n, spec.get("gun") or self.plan[n], {str(n): spec}, report=report)
        if not res:
            return None
        out, pal = res
        views = {}
        for v in self.views:
            info = report.get(v)
            if not info:
                continue
            path = next(p for p in out if p.name == v + ".png" and p.parent.name == info["file"])
            src = ms.git_png(path)
            front = ms.git_png(path.parent / "front.png") or src
            opal = [tuple(front.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
            # backs too in the normal palette: that's how the battle shows them
            views[v] = view(info, as_rgba(out[path], pal), as_rgba(src, opal), 80, 80, 2, ms.bbox(src.load(), 0))
        return views

    def save(self, n, spec):
        store(ms.DRIP, str(n), spec)
        drip = {k: v for k, v in read_json(ms.DRIP).items() if not k.startswith("_")}
        out, _ = ms.arm(n, drip.get(str(n), {}).get("gun") or self.plan[n], drip)
        for p, im in out.items():
            im.save(p, transparency=0)
        icon = subprocess.run([sys.executable, "-I", str(HOOD / "make_icons.py"), "--only", str(n)],
                              capture_output=True, text=True).returncode == 0
        return f"{len(out)} battle sprite files" + (" + party icon" if icon else "")


# ------------------------------------------------------------------ trainer battle sprites

class Trainers:
    title, linked, views = "Trainers", False, ("front",)

    def __init__(self):
        self.data, self.files, self.names = mt.load()
        self.ids = [c for c in range(len(self.files) // 5)
                    if mt.dress_class(bytearray(self.data), self.files, self.names, c)]

    def specs(self):
        return read_json(mt.DRIP)

    def entries(self):
        return [(c, (self.names[c] if c < len(self.names) else f"class {c}").replace("₧₦", "PKMN"))
                for c in self.ids]

    def default_gun(self, c):
        return mt.gun_for(self.names[c] if c < len(self.names) else "", random.Random(c * 104729))

    def load(self, c, spec):
        return {"name": dict(self.entries())[c], "default_gun": self.default_gun(c), "guns": GUNS,
                "colors": BATTLE_COLORS}

    def render(self, c, spec):
        report = {}
        res = mt.dress_class(bytearray(self.data), self.files, self.names, c, spec, report)
        if not res:
            return None
        _, orig, im, pal, _ = res
        opal = [tuple(orig.getpalette()[i * 3:i * 3 + 3]) for i in range(16)]
        crop = (0, 0, 80, 80)
        return {"front": view(report["front"], as_rgba(im, pal).crop(crop), as_rgba(orig, opal).crop(crop),
                              80, 80, 1, ms.bbox(orig.load(), 0))}

    def save(self, c, spec):
        store(mt.DRIP, str(c), spec)
        r = subprocess.run([sys.executable, "-I", str(HOOD / "make_trainers.py")], capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(r.stderr.strip().splitlines()[-1])
        return "the trainer sprite archive (all classes)"


# ------------------------------------------------------------------ overworld people

NICE = {"HERO": "Player", "HEROINE": "Player (girl)", "GSMAMA": "Mom", "OOKIDO": "Prof. Oak", "DOCTOR": "Prof. Elm",
        "GSRIVEL": "Rival", "F_HERO": "Lyra / Ethan", "F_HERO_2": "Lyra / Ethan 2", "CYCLEHERO": "Player (bike)",
        "SWIMHERO": "Player (surf)"}


class People:
    title, linked, views = "People", True, mn.FACING

    def __init__(self):
        self.models = mn.models()
        self.ids = [n for n, nm in self.models.items() if mn.dress(n, nm, preview=True, spec={})]

    def specs(self):
        return {str(n): 1 for n, nm in self.models.items() if nm in read_json(mn.DRIP)}

    def label(self, n):
        nm = self.models[n]
        return f"{NICE[nm]} ({nm})" if nm in NICE else nm.replace("_", " ").title()

    def entries(self):
        return [(n, self.label(n)) for n in self.ids]

    def spec_of(self, n):
        return read_json(mn.DRIP).get(self.models[n], {})

    def load(self, n, spec):
        return {"name": self.label(n), "default_gun": None, "guns": None,
                "colors": ["k", "W", "g", "r", "u", "p", "o", "e"],
                "add": {"gun": {"kind": "pistol"}, "chain": {"heavy": False},
                        "hat": {"style": "beanie", "color": "k"}, "bonnet": {"color": "p"}, "powder": {}},
                "choices": {"style": {"hat": ["beanie", "snapback", "durag", "bandana"]},
                            "kind": ["pistol", "mid", "long", "heavy"]}}

    def render(self, n, spec):
        report = {}
        if not mn.dress(n, self.models[n], preview=True, spec=spec, report=report):
            return None
        pal, opal = report.pop("_pal"), report.pop("_orig_pal")
        views = {}
        for d in self.views:
            info = report.get(d)
            if not info:
                continue
            frames, orig = info.pop("frames"), info.pop("orig")
            fh, fw = len(frames[0]), len(frames[0][0])
            views[d] = view(info, strip(frames, pal), strip(orig, opal), fw, fh, len(frames), mo_bbox(orig[0]))
        return views

    def save(self, n, spec):
        store(mn.DRIP, self.models[n], spec)
        mn.dress(n, self.models[n], spec=spec)
        return f"overworld model {self.models[n]}"


def mo_bbox(rows):
    pts = [(x, y) for y, r in enumerate(rows) for x, v in enumerate(r) if v]
    if not pts:
        return None
    return [min(p[0] for p in pts), min(p[1] for p in pts), max(p[0] for p in pts), max(p[1] for p in pts)]


# ------------------------------------------------------------------ in-game text

KNOWN_BANKS = {"msg_0003_EVERYWHERE": "Shared script text (everywhere)", "msg_0237": "Pokémon names",
               "msg_0238": "Pokémon names (with article)", "msg_0222": "Item names", "msg_0223": "Item names (with article)",
               "msg_0224": "Item names (plural)", "msg_0749": "Move descriptions", "msg_0750": "Move names",
               "msg_0751": "Move names (caps)", "msg_0728": "Trainer battle lines", "msg_0730": "Trainer classes",
               "msg_0731": "Trainer classes (with article)"}


class Text:
    def __init__(self):
        import text_edits as te
        self.te = te
        self.names = [p.stem for p in te.bank_files()]
        self.base = te.base_banks(self.names)
        self.cur = {n: te.rows_of((te.MSG / f"{n}.gmm").read_text(encoding="utf-8")) for n in self.names}
        self.limits = {n: te.Limits(n, self.base[n]) for n in self.names}
        places = {}
        for line in (ms.ROOT / "include/constants/maps.h").read_text().splitlines():
            m = re.match(r"#define MAP_(\w+)\s+\d+\s*//\s*MAP_(\w+)", line)
            if m:
                places.setdefault(m.group(2), m.group(1).replace("_", " ").title())
        self.labels = {}
        for n in self.names:
            code = n.split("_", 2)[2] if n.count("_") >= 2 else None
            if n in KNOWN_BANKS:
                self.labels[n] = KNOWN_BANKS[n]
            elif code and code in places:
                self.labels[n] = places[code]
            else:
                first = next((t for t in self.cur[n].values() if self.plain(t).strip()), "")
                self.labels[n] = "“" + self.plain(first)[:38].strip() + "…”" if first else "(empty)"

    @staticmethod
    def plain(t):
        return re.sub(r"\{[^}]*\}", "…", t).replace("\\n", " ").replace("\\r", " ").replace("\\f", " ")

    def banks(self):
        edited = self.te.load_edits()
        return [{"id": n, "name": f"{n[4:8]} · {self.labels[n]}", "rows": len(self.cur[n]), "edited": n in edited}
                for n in self.names]

    def bank(self, n):
        lim = self.limits[n]
        edited = self.te.load_edits().get(n, {})
        return {"id": n, "label": self.labels[n], "readonly": self.te.READ_ONLY.get(n),
                "limits": {"px": lim.px, "lines": lim.lines, "units": lim.units, "script": self.te.is_script_bank(n)},
                "rows": [{"i": i, "base": self.base[n].get(i, ""), "text": t, "edited": str(i) in edited,
                          "ending": self.te.ending(t)} for i, t in sorted(self.cur[n].items())]}

    def check(self, n, rows):
        out = {}
        for i, text in rows.items():
            i = int(i)
            if i not in self.cur[n]:
                out[i] = {"text": text, "errors": ["no such row (rows can't be added)"]}
                continue
            base = self.base[n].get(i, "")
            new, errors = self.te.check(n, base, self.cur[n][i], text, self.limits[n])
            lim = self.limits[n].for_row(n, base, self.cur[n][i])
            out[i] = {"text": new, "errors": errors, "measure": self.te.measure(new), "limit": lim}
        return out

    def save(self, n, rows):
        res = self.check(n, rows)
        bad = {i: r["errors"] for i, r in res.items() if r["errors"]}
        if bad:
            return {"error": "fix these rows first", "rows": bad}
        new = {i: r["text"] for i, r in res.items()}
        self.te.write_rows(n, new)
        edits = self.te.load_edits()
        edits.setdefault(n, {}).update({str(i): t for i, t in new.items()})
        self.te.save_edits(edits)
        self.cur[n].update(new)
        return {"ok": True, "saved": len(new)}

    def search(self, q):
        q = q.lower().strip()
        hits = []
        for n in self.names:
            for i, t in self.cur[n].items():
                if q in self.plain(t).lower() or q in t.lower():
                    hits.append({"bank": n, "row": i, "label": self.labels[n], "text": self.plain(t)[:90]})
                    if len(hits) >= 400:
                        return hits
        return hits

    def font(self):
        return {"widths": self.te.WIDTHS, "chars": self.te.CHARS, "atlas": png_url(self.te.glyph_atlas()),
                "token_px": self.te.TOKEN_PX}


TEXT = []


def text():
    if not TEXT:
        TEXT.append(Text())
    return TEXT[0]


KINDS = {}


def kind(k):
    if k not in KINDS:
        KINDS[k] = {"pokemon": Pokemon, "trainer": Trainers, "npc": People}[k]()
    return KINDS[k]


def spec_for(K, i):
    return K.spec_of(i) if hasattr(K, "spec_of") else K.specs().get(str(i), {})


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def send(self, body, ctype="application/json", code=200):
        if not isinstance(body, bytes):
            body = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        q = {k: v[0] for k, v in parse_qs(url.query).items()}
        try:
            if url.path == "/":
                return self.send(PAGE.read_bytes(), "text/html; charset=utf-8")
            if url.path == "/api/text/banks":
                return self.send(text().banks())
            if url.path == "/api/text/bank":
                return self.send(text().bank(q["id"]))
            if url.path == "/api/text/search":
                return self.send(text().search(q.get("q", "")))
            if url.path == "/api/text/font":
                return self.send(text().font())
            if url.path == "/api/list":
                K = kind(q["kind"])
                edited = K.specs()
                return self.send([{"id": i, "name": nm, "edited": str(i) in edited} for i, nm in K.entries()])
            if url.path == "/api/load":
                K, i = kind(q["kind"]), int(q["id"])
                spec = spec_for(K, i)
                return self.send(dict(K.load(i, spec), id=i, spec=spec, linked=K.linked, views=list(K.views)))
        except Exception as e:
            return self.fail(e)
        self.send({"error": "not found"}, code=404)

    def do_POST(self):
        body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        try:
            if self.path == "/api/text/check":
                return self.send(text().check(body["id"], body["rows"]))
            if self.path == "/api/text/save":
                res = text().save(body["id"], body["rows"])
                return self.send(res, code=200 if res.get("ok") else 400)
            K, i, spec = kind(body["kind"]), int(body["id"]), body["spec"]
            if self.path == "/api/render":
                views = K.render(i, spec)
                return self.send({"views": views, "order": [v for v in K.views if views and v in views]})
            if self.path == "/api/save":
                return self.send({"ok": True, "wrote": K.save(i, spec)})
        except Exception as e:
            return self.fail(e)
        self.send({"error": "not found"}, code=404)

    def fail(self, e):                               # show it in the page instead of killing the server
        import traceback
        traceback.print_exc()
        self.send({"error": f"{type(e).__name__}: {e}"}, code=500)


def main():
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    url = f"http://localhost:{PORT}"
    print(f"drip editor: {url}  (Ctrl+C to stop)")
    if "--no-browser" not in sys.argv:
        webbrowser.open(url)
    server.serve_forever()


if __name__ == "__main__":
    main()
