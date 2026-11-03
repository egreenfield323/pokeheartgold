"""set23_fix.py FIXFILE: apply (old, new) string swaps (python list FIXES in FIXFILE) to hood/gunfx.py and to the
set-23 batch files that hold the same code (so they stay a faithful record). Each old string must occur exactly
once in gunfx."""
import sys
from pathlib import Path
R = Path(__file__).resolve().parents[3]
fixes = {}
exec(Path(sys.argv[1]).read_text(encoding="utf-8"), fixes)
g = R / "hood/gunfx.py"
s = g.read_text(encoding="utf-8")
for old, new in fixes["FIXES"]:
    assert s.count(old) == 1, (s.count(old), old)
    s = s.replace(old, new)
g.write_text(s, encoding="utf-8", newline="")
for f in sorted((R / "hood/test/reel").glob("set2[0-9]_b*.py")):
    t = f.read_text(encoding="utf-8")
    t2 = t
    for old, new in fixes["FIXES"]:
        if t2.count(old) == 1:
            t2 = t2.replace(old, new)
    if t2 != t:
        f.write_text(t2, encoding="utf-8", newline="")
print("fixed", len(fixes["FIXES"]))
