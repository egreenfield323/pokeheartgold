"""Insert a block of code into a file before/after an anchor line: insert.py file anchor before|after block_file"""
import sys
path, anchor, where, block = sys.argv[1], sys.argv[2], sys.argv[3], open(sys.argv[4], encoding="utf-8").read()
src = open(path, encoding="utf-8").read()
assert src.count(anchor) == 1, (anchor, src.count(anchor))
i = src.index(anchor)
if where == "after":
    i = src.index("\n", i) + 1
else:
    i = src.rindex("\n", 0, i) + 1
src = src[:i] + block + src[i:]
open(path, "w", encoding="utf-8", newline="").write(src)
print("inserted", len(block), "chars")
