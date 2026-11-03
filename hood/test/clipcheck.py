#!/usr/bin/env python3
"""Flag frames where a move animation probably runs under an HP box or the message box.

The boxes draw over particles, so a prop that's half under a box shows its other half pressed right up against
the box edge. This compares every captured frame with the first one (before the move) in thin strips just
outside each box edge and reports the frames where animation pixels show up there.
Usage:  python -I hood/test/clipcheck.py FRAME_DIR [--min N] [--sheet OUT.png]
--sheet saves the flagged frames (2x, the strips outlined in red, the worst frame of each run) to look at.
FRAME_DIR holds capture.py's f_NNN.png (256x384, top screen first).
"""
import sys
from pathlib import Path
from PIL import Image, ImageChops, ImageDraw

STRIPS = {                                  # x0, y0, x1, y1 on the top screen (measured)
    "foe box (right edge)": (125, 18, 132, 55),
    "foe box (bottom edge)": (0, 55, 124, 61),
    "your box (left edge)": (128, 98, 135, 131),
    "your box (top edge)": (136, 91, 256, 97),
    "message box (top edge)": (90, 136, 256, 142),
}


def changed(a, b, box, tol=48):
    d = ImageChops.difference(a.crop(box), b.crop(box)).convert("L")
    return sum(1 for v in d.get_flattened_data() if v > tol)


def _runs(frames):
    runs, cur = [], [frames[0]]
    for fr in frames[1:]:
        if fr[0] - cur[-1][0] <= 2:
            cur.append(fr)
        else:
            runs.append(cur); cur = [fr]
    return runs + [cur]


def main():
    folder = Path(sys.argv[1])
    least = int(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 8
    files = sorted(folder.glob("f_*.png"))
    base = Image.open(files[0]).convert("RGB").crop((0, 0, 256, 192))
    hits = {}
    for f in files[1:]:
        im = Image.open(f).convert("RGB").crop((0, 0, 256, 192))
        if changed(im, base, (0, 0, 256, 192)) > 256 * 192 * .4:          # a full-screen flash / fade: skip
            continue
        for name, box in STRIPS.items():
            n = changed(im, base, box)
            if n >= least:
                hits.setdefault(name, []).append((int(f.stem[2:]), n))
    for name, frames in hits.items():
        runs = _runs(frames)
        print(f"{name}: " + ", ".join(f"{r[0][0]}-{r[-1][0]} (max {max(n for _, n in r)}px)" for r in runs))
    if not hits:
        print("nothing touching the boxes")
    elif "--sheet" in sys.argv:
        worst = sorted({max(r, key=lambda t: t[1])[0] for frames in hits.values() for r in _runs(frames)})[:24]
        cols = 4
        sheet = Image.new("RGB", (cols * 514, ((len(worst) + cols - 1) // cols) * 400), (30, 30, 30))
        for i, k in enumerate(worst):
            im = Image.open(folder / f"f_{k:03d}.png").convert("RGB").crop((0, 0, 256, 192))
            d = ImageDraw.Draw(im)
            for box in STRIPS.values():
                d.rectangle([box[0], box[1], box[2] - 1, box[3] - 1], outline=(255, 0, 0))
            d.text((2, 180), str(k), fill=(255, 255, 0))
            sheet.paste(im.resize((512, 384), Image.NEAREST), ((i % cols) * 514, (i // cols) * 400))
        sheet.save(sys.argv[sys.argv.index("--sheet") + 1])


if __name__ == "__main__":
    main()
