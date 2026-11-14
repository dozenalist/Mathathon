import re, pathlib, sys
for rej in pathlib.Path(".").rglob("*.rej"):
    src = rej.with_suffix("")
    lines = src.read_text().splitlines()
    txt = rej.read_text().splitlines()
    hunks=[]; cur=None
    for l in txt:
        if l.startswith("@@"):
            if cur: hunks.append(cur)
            cur=[]
        elif cur is not None and l[:1] in "-+ " and not l.startswith("---") and not l.startswith("+++"):
            cur.append(l)
    if cur: hunks.append(cur)
    total_removed=0
    for h in hunks:
        minus=[l[1:] for l in h if l.startswith("-")]
        plus=[l[1:] for l in h if l.startswith("+")]
        if plus:
            print("  !! hunk has additions, skipping", src); continue
        strip=[x.strip() for x in minus]
        # find first and last anchoring non-empty lines
        idxs=[i for i,x in enumerate(strip) if x]
        if not idxs: continue
        first, last = strip[idxs[0]], strip[idxs[-1]]
        try:
            a = next(i for i,l in enumerate(lines) if l.strip()==first)
            b = next(i for i in range(a, len(lines)) if lines[i].strip()==last)
        except StopIteration:
            print("  !! anchors not found in", src, ":", first[:50], "/", last[:50]); continue
        # sanity: number of lines to delete should be b-a+1 close to len(minus)
        del lines[a:b+1]
        total_removed += b-a+1
    src.write_text("\n".join(lines)+"\n")
    rej.unlink()
    print(f"repaired {src}: removed {total_removed} lines")
