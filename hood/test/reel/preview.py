"""preview.py OUT.png EXPR [EXPR ...]: render fxart pieces (Python expressions using fxart, e.g.
"fxart.vape_mod()" or 'fxart.line_bubble(["HI"])') onto a green contact sheet at 2x, 7 per row."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import fxart  # noqa: E402
from PIL import Image  # noqa: E402
ims = [eval(e, {"fxart": fxart}) for e in sys.argv[2:]]
cols = 7
sheet = Image.new("RGBA", (cols * 136, ((len(ims) + cols - 1) // cols) * 136), (90, 160, 90, 255))
for i, im in enumerate(ims):
    sheet.alpha_composite(im.resize((128, 128), Image.NEAREST), ((i % cols) * 136 + 4, (i // cols) * 136 + 4))
sheet.save(sys.argv[1])
