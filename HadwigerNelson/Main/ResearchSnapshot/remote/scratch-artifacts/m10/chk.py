import pathlib, re, difflib, sys
old = pathlib.Path(sys.argv[1]); new = pathlib.Path(sys.argv[2])
STRUCT = re.compile(r"^(namespace|section|noncomputable|variable|open|end|instance|local|universe|include|omit|attribute|example|#|mutual|scoped)")
tot = 0
for p in sorted(old.rglob("*.lean")):
    q = new / p.relative_to(old)
    if not q.exists():
        print("WHOLE-FILE-DELETED", p.name); continue
    a = p.read_text().splitlines(); b = q.read_text().splitlines()
    for ln in difflib.unified_diff(a, b, lineterm="", n=0):
        if ln.startswith("-") and not ln.startswith("---") and STRUCT.match(ln[1:]):
            tot += 1
            print(f"{str(p).split('OAI/')[-1]}: {ln[1:]}")
print("TOTAL structural removed:", tot)
