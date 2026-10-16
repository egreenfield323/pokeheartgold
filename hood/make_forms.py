#!/usr/bin/env python3
"""Strap the alternate-form battle sprites (Unown letters, Deoxys, Rotom, Burmy, Arceus, ...).

Same pipeline as make_sprites.py: evolving gun, hat, chain, kicks, ice. Forms share their base
species' gun and hat style; head placement is auto-detected per form (forms change shape).
Run from the repo root:  python hood/make_forms.py [--preview out.png]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_sprites as ms  # noqa: E402

OTHER = ms.ROOT / "files/poketool/pokegra/otherpoke"
FORM_SPECIES = {"arceus": 493, "burmy": 412, "castform": 351, "cherrim": 421, "deoxys": 386,
                "gastrodon": 423, "giratina": 487, "pichu": 172, "rotom": 479, "shaymin": 492,
                "shellos": 422, "unown": 201, "wormadam": 413}


def main():
    plan, names = ms.gun_plan()
    drip = {k: v for k, v in json.loads(ms.DRIP.read_text(encoding="utf-8")).items() if not k.startswith("_")}
    preview = sys.argv[sys.argv.index("--preview") + 1] if "--preview" in sys.argv else None
    sheet, count = [], 0
    for dirname, n in FORM_SPECIES.items():
        gun = drip.get(str(n), {}).get("gun", plan[n])
        spec = {k: v for k, v in drip.get(str(n), {}).items() if k in ("gun", "auto")}
        for form in sorted(p for p in (OTHER / dirname).iterdir() if p.is_dir()):
            paths = [form / "front.png", form / "back.png"]
            res = ms.arm(n, gun, {str(n): spec}, paths=paths)
            if not res:
                continue
            out, pal = res
            count += 1
            if preview:
                f = out[paths[0]]
                b = out[paths[1]].copy()
                b.putpalette([v for c in pal for v in c])
                b.info["transparency"] = 0
                sheet.append((n, f"{dirname}/{form.name}", gun, f, b))
            else:
                for p, im in out.items():
                    im.save(p, transparency=0)
    if preview:
        from PIL import Image, ImageDraw
        cols, cw, ch = 4, 330, 96
        img = Image.new("RGB", (cols * cw, ((len(sheet) + cols - 1) // cols) * ch), (205, 225, 205))
        d = ImageDraw.Draw(img)
        for k, (n, name, gun, f, b) in enumerate(sheet):
            x, y = (k % cols) * cw, (k // cols) * ch
            fr, br = f.convert("RGBA"), b.convert("RGBA").crop((0, 0, 80, 80))
            img.paste(fr, (x, y + 12), fr)
            img.paste(br, (x + 165, y + 12), br)
            d.text((x + 2, y), f"{name} - {gun}", fill=(0, 0, 0))
        img.resize((img.width * 2, img.height * 2), Image.NEAREST).save(preview)
        print("preview:", preview)
    else:
        print(f"strapped {count} alternate forms")


if __name__ == "__main__":
    main()
