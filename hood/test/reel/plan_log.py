"""plan_log.py "message": append a dated line to .claude/plans/anim-redo-plan.md's Log, and/or tick boxes:
plan_log.py --tick "292 Fury Cutter" --tick "293 Destiny Bond" "message"  (ticks `- [ ] <text>` -> `- [x] <text>`)"""
import datetime
import sys
from pathlib import Path
p = Path(__file__).resolve().parents[3] / ".claude" / "plans" / "anim-redo-plan.md"
s = p.read_text(encoding="utf-8")
args = sys.argv[1:]
msg = []
while args:
    a = args.pop(0)
    if a == "--tick":
        t = args.pop(0)
        assert s.count(f"- [ ] {t}") == 1, t
        s = s.replace(f"- [ ] {t}", f"- [x] {t}")
    else:
        msg.append(a)
if msg:
    s = s.rstrip("\n") + f"\n- {datetime.date.today()}: " + " ".join(msg) + "\n"
p.write_text(s, encoding="utf-8")
print("plan updated")
