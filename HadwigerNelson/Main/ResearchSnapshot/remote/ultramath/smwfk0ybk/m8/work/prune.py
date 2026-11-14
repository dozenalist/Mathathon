import json, pathlib, re
MIN = pathlib.Path("min")
empty = set(json.load(open("empty.json")))
for e in empty:
    p = MIN/(e.replace(".","/")+".lean")
    if p.exists(): p.unlink()
n=0
for p in sorted(MIN.glob("OAI/**/*.lean")):
    txt = p.read_text(); new = txt
    for e in empty:
        new = re.sub(rf"^import {re.escape(e)}\n", "", new, flags=re.M)
    # drop now-unneeded import lines of other OAI modules not referenced? leave them
    if new != txt: p.write_text(new); n+=1
print("files rewritten:", n, "modules deleted:", len(empty))
tot=0; cnt=0
for p in sorted(MIN.glob("OAI/**/*.lean")):
    tot += len(p.read_text().splitlines()); cnt+=1
print(f"extracted+pruned tree: {cnt} modules, {tot} lines")
