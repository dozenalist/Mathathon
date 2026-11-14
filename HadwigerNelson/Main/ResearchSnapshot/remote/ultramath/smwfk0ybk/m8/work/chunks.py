import re, pathlib, collections
ROOT = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/lean")
DECL = re.compile(r"^(?:@\[[^\n]*\n)*\s*(?:(?:noncomputable|private|protected|local|scoped|partial|unsafe)\s+)*(theorem|lemma|def|abbrev|structure|class|inductive|instance|example)\b")
CTRL = re.compile(r"^\s*(?:noncomputable\s+)?(namespace|end|section|open|variable|universe|set_option|attribute|notation|macro|scoped|local|instance)")
def chunks(path):
    lines = path.read_text(errors="ignore").splitlines(keepends=True)
    starts = []
    pending_attr = False
    for i,l in enumerate(lines):
        if l.startswith("@["):
            if not pending_attr:
                starts.append(i); pending_attr = True
            continue
        if not l or l[0] in " \t":
            continue
        pending_attr = False
        starts.append(i)
    out = []
    for k,s in enumerate(starts):
        e = starts[k+1] if k+1 < len(starts) else len(lines)
        out.append((s,e,"".join(lines[s:e])))
    return lines, out
c = collections.Counter(); lines_by_kind = collections.Counter()
for p in sorted(ROOT.glob("OAI/**/*.lean")):
    lines, ch = chunks(p)
    for s,e,txt in ch:
        head = next((l for l in txt.splitlines() if not l.startswith("@[")), "")
        m = DECL.match(head)
        k = m.group(1) if m else ("ctrl:" + (head.split()[0] if head.split() else "?"))
        c[k] += 1; lines_by_kind[k] += e-s
for k,v in c.most_common():
    print(f"{k:20s} {v:5d} chunks  {lines_by_kind[k]:6d} lines")
