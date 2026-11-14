import re, pathlib, json, collections

ROOT = pathlib.Path("tree")
NS = re.compile(r"^namespace\s+([A-Za-z_][\w'.]*)\s*$")
SEC = re.compile(r"^(?:noncomputable\s+|private\s+|protected\s+)?section\b")
END = re.compile(r"^end\b\s*([A-Za-z_][\w'.]*)?\s*$")
HEAD = r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|unsafe\s+|scoped\s+|local\s+)*"
DECL = re.compile(HEAD + r"(theorem|lemma|def|abbrev|structure|class|inductive|instance|example)\s+([A-Za-z_][\w'.]*)")
ANON = re.compile(r"^(?:private\s+|protected\s+|noncomputable\s+|scoped\s+|local\s+)*(instance|example)\b")

out = []
per_mod = collections.defaultdict(list)
for p in sorted(ROOT.glob("OAI/**/*.lean")):
    mod = ".".join(p.relative_to(ROOT).with_suffix("").parts)
    L = p.read_text(errors="ignore").splitlines()
    stack = []
    incom = False
    for i, line in enumerate(L):
        s = line.strip()
        if incom:
            if s.endswith("-/"):
                incom = False
            continue
        if s.startswith("/-"):
            if not s.endswith("-/"):
                incom = True
            continue
        m = NS.match(line)
        if m:
            stack.append(("ns", m.group(1)))
            continue
        if SEC.match(line):
            stack.append(("sec", None))
            continue
        e = END.match(line)
        if e:
            nm = e.group(1)
            if nm is None:
                if stack:
                    stack.pop()
            else:
                for k in range(len(stack) - 1, -1, -1):
                    if stack[k][0] == "ns" and stack[k][1] == nm:
                        del stack[k:]
                        break
                else:
                    if stack:
                        stack.pop()
            continue
        m = DECL.match(line)
        kind = name = None
        if m:
            kind, name = m.group(1), m.group(2)
        elif ANON.match(line):
            kind = "instance"
        if kind:
            priv = line.lstrip().startswith("private") or "private " in line.split(kind)[0]
            ns = [x[1] for x in stack if x[0] == "ns"]
            full = ".".join(ns + ([name] if name else [])) if name else None
            attr = "@[" in line
            # attribute on the previous line
            j = i - 1
            while j >= 0 and L[j].strip() == "":
                j -= 1
            if j >= 0 and L[j].strip().startswith("@"):
                attr = True
            rec = dict(mod=mod, file=str(p.relative_to(ROOT)), line=i + 1, kind=kind,
                       name=name, full=full, attr=attr, private=priv)
            out.append(rec)
            per_mod[mod].append(rec)
json.dump(out, open("ana/decls_ns.json", "w"))
print("decls", len(out), "with full name", sum(1 for d in out if d["full"]))
print("private", sum(1 for d in out if d["private"]))
