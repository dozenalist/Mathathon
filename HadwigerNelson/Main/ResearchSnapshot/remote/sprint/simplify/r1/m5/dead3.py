#!/usr/bin/env python3
"""Final dead-declaration set: not reached by m10's declgraph AND never mentioned
by name in the tree's source (a `rfl` lemma used only inside a `simp [...]` list
can be absent from the proof term yet still be needed to compile).

  python3 dead3.py --tree DIR --log DG.log [--report OUT.json]
"""
import json, re, os, argparse, pathlib, collections

DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+|partial\s+|unsafe\s+|scoped\s+)*"
                  r"(theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque)\s+([^\s:{(​\[]+)")
NS = re.compile(r"^namespace\s+([\w.]+)\s*$")
SEC = re.compile(r"^(?:noncomputable\s+|private\s+|protected\s+|public\s+)?section(?:\s+[\w.]+)?\s*$")
MUT = re.compile(r"^mutual\s*$")
END = re.compile(r"^end(?:\s+([\w.]+))?\s*$")
TOK = re.compile(r"[A-Za-z_\u00a1-\uffff][A-Za-z0-9_'!?\u00a1-\uffff]*")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--report", default=None)
    a = ap.parse_args()
    root = pathlib.Path(a.tree)
    reached, reachedpairs = set(), set()
    for line in open(a.log, encoding="utf-8", errors="ignore"):
        p = line.split()
        if p and p[0] == "NODE":
            reached.add(p[2]); reachedpairs.add((p[1], p[2].split(".")[-1]))
    tok = collections.Counter(); hdr = collections.Counter(); decls = []
    for f in sorted((root / "lean" / "OAI").rglob("*.lean")):
        mod = ".".join(f.relative_to(root / "lean").with_suffix("").parts)
        text = f.read_text(errors="ignore")
        lines = text.splitlines()
        for t in TOK.findall(text): tok[t] += 1
        stack, found = [], []
        for i, ln in enumerate(lines, 1):
            m = NS.match(ln)
            if m: stack.append(m.group(1)); continue
            if SEC.match(ln) or MUT.match(ln): stack.append(""); continue
            eo = END.match(ln)
            if eo:
                nm = eo.group(1)
                if nm and nm in stack:
                    while stack and stack.pop() != nm: pass
                elif stack: stack.pop()
                continue
            d = DECL.match(ln)
            if d:
                kind, name = d.group(1), d.group(2)
                if name in ("where", "at", "at'"): continue
                pre = ".".join(x for x in stack if x)
                found.append((kind, name, (pre + "." + name) if pre else name, i))
        for j, (kind, name, full, i) in enumerate(found):
            end = (found[j+1][3] - 1) if j + 1 < len(found) else len(lines)
            decls.append(dict(mod=mod, name=name, full=full, line=i, end=end,
                              lines=end - i + 1))
            hdr[name] += 1
    dead = [d for d in decls
            if d["full"] not in reached and (d["mod"], d["name"]) not in reachedpairs
            and tok[d["name"]] - hdr[d["name"]] <= 0]
    tot = sum(d["lines"] for d in dead)
    print(f"{len(decls)} decls, {sum(d['lines'] for d in decls)} span-lines")
    print(f"DEAD (unreached AND unmentioned): {len(dead)} decls, {tot} span-lines")
    per = collections.Counter()
    for d in dead: per[d["mod"]] += d["lines"]
    for m, L in per.most_common(60): print(f"  {L:5d} {m}")
    dead.sort(key=lambda d: -d["lines"])
    print()
    for d in dead[:40]: print(f"  {d['lines']:4d} {d['mod']}:{d['line']} {d['full']}")
    if a.report: json.dump(dead, open(a.report, "w"), indent=0)

main()
