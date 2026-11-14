import os, re, json, sys
from collections import defaultdict

ROOT = "/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean/OAI"
files = []
for d, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith(".lean"):
            files.append(os.path.join(d, f))
files.sort()

DECL = re.compile(r'^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|nonrec\s+)*?(theorem|lemma)\s+([A-Za-z0-9_\.\'!?]+)')

def top_level_split_colon(stmt):
    """Split statement text into (binder-part, conclusion-part) using last top-level ':' (not ':=' , not '::')."""
    depth = 0
    idxs = []
    i = 0
    s = stmt
    while i < len(s):
        c = s[i]
        if c in '([{⟨':
            depth += 1
        elif c in ')]}⟩':
            depth -= 1
        elif c == '"':
            i += 1
            while i < len(s) and s[i] != '"':
                if s[i] == '\\': i += 1
                i += 1
        elif c == ':' and depth == 0:
            nxt = s[i+1:i+2]
            prv = s[i-1:i]
            if nxt == '=' or nxt == ':' or prv == ':':
                pass
            else:
                idxs.append(i)
        i += 1
    if not idxs:
        return stmt, ""
    k = idxs[-1]
    return s[:k], s[k+1:]

def norm(t):
    t = re.sub(r'--.*', '', t)
    t = t.replace('\n', ' ')
    t = re.sub(r'\s+', '', t)
    return t

decls = []
for path in files:
    rel = os.path.relpath(path, ROOT)
    lines = open(path, encoding='utf-8').read().split('\n')
    starts = []
    for i, ln in enumerate(lines):
        m = DECL.match(ln)
        if m:
            starts.append((i, m.group(1), m.group(2)))
    for j, (i, kind, name) in enumerate(starts):
        end = starts[j+1][0] if j+1 < len(starts) else len(lines)
        block = lines[i:end]
        # statement: from decl line up to the first line containing ':=' at top-level approx,
        # or ':= by'
        stmt_lines = []
        proof_lines = []
        found = False
        for b in block:
            if not found and (' := ' in b or b.rstrip().endswith(':=') or ':= by' in b):
                # statement part is before ':='
                head = b.split(':=', 1)[0]
                stmt_lines.append(head)
                rest = b.split(':=', 1)[1]
                proof_lines.append(rest)
                found = True
                continue
            if not found:
                stmt_lines.append(b)
            else:
                proof_lines.append(b)
        stmt = '\n'.join(stmt_lines)
        stmt = stmt[len(stmt_lines[0].split(kind,1)[0]):] if False else stmt
        hyp, con = top_level_split_colon(norm(stmt))
        # strip leading theorem/lemma name from hyp
        hyp = re.sub(r'^(theorem|lemma)[A-Za-z0-9_\.\'!?]*', '', hyp)
        decls.append(dict(file=rel, line=i+1, kind=kind, name=name,
                          hyp=hyp, con=con, nproof=len([p for p in proof_lines if p.strip()]),
                          proof='\n'.join(proof_lines)))

json.dump(decls, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'decls.json'), 'w'))
print("decls", len(decls))

# clusters of identical normalized conclusion, across different files
bycon = defaultdict(list)
for d in decls:
    bycon[d['con']].append(d)
rows = []
for con, ds in bycon.items():
    fl = {d['file'] for d in ds}
    if len(ds) >= 2 and len(con) > 8:
        rows.append((len(fl), len(ds), con, ds))
rows.sort(key=lambda r: (-r[0], -r[1]))
print("cross-file identical-conclusion clusters:", sum(1 for r in rows if r[0] >= 2))
with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'clusters.txt'), 'w') as fh:
    for nf, n, con, ds in rows:
        fh.write(f"### files={nf} decls={n} :: {con[:300]}\n")
        for d in ds:
            fh.write(f"    {d['file']}:{d['line']} {d['name']}  (hyp={d['hyp'][:160]}) (proof={d['nproof']})\n")
