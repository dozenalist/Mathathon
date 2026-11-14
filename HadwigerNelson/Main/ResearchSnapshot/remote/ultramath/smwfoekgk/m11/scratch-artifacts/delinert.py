import re, pathlib, sys
VAR=re.compile(r'^\s*(variable|open|omit|set_option|attribute|local instance|local notation|include|universe)\b')
SEC=re.compile(r'^section(\s+[A-Za-z_][\w\'.]*)?\s*$')
NS=re.compile(r'^namespace\b')
END=re.compile(r'^end\b')
total=0
for p in sorted(pathlib.Path(".").rglob("*.lean")):
    L=p.read_text().splitlines(); stack=[]; dels=set()
    for i,l in enumerate(L):
        s=l.strip()
        if SEC.match(s): stack.append(["sec", i, s])
        elif NS.match(s) or re.match(r'^(noncomputable |private |protected |scoped )*section\b', s): stack.append(["other", i, s])
        elif END.match(s):
            if not stack: continue
            kind, start, txt = stack.pop()
            if kind=="sec" and not any(VAR.match(x) for x in L[start+1:i]):
                dels.add(start); dels.add(i)
    if dels:
        out=[l for j,l in enumerate(L) if j not in dels]
        p.write_text("\n".join(out)+"\n"); total+=len(dels)
        print(f"{len(dels):4d} {p}")
print("removed lines:", total)
