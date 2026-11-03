"""sheet.py out.png start end [every] [scale]: a contact sheet of hood/test/out/f_*.png frames [start, end)."""
import sys
from pathlib import Path
from PIL import Image
frames = sorted((Path(__file__).resolve().parents[1] / "out").glob("f_*.png"))
out, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
every = int(sys.argv[4]) if len(sys.argv) > 4 else 1
sc = float(sys.argv[5]) if len(sys.argv) > 5 else .5
pick = frames[a:b:every]
w, h = int(256 * sc), int(192 * sc)
cols = 10 if sc <= .5 else 5
rows = (len(pick) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (w + 2), rows * (h + 14)), (40, 40, 40))
from PIL import ImageDraw
d = ImageDraw.Draw(sheet)
for i, p in enumerate(pick):
    x, y = (i % cols) * (w + 2), (i // cols) * (h + 14)
    sheet.paste(Image.open(p).convert("RGB").crop((0, 0, 256, 192)).resize((w, h), Image.NEAREST), (x, y + 12))
    d.text((x + 2, y), str(a + i * every), fill=(255, 255, 0))
sheet.save(out)
print(len(frames), "frames;", len(pick), "on sheet")
