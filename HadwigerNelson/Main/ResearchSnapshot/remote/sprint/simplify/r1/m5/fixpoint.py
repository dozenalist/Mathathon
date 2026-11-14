#!/usr/bin/env python3
"""Iterate the sound dead-declaration cut to a fixpoint.

A declaration is cut when (a) m10's regenerated declgraph never reaches it from the
7 headline declarations, (b) its short name is never mentioned anywhere in the
current tree, and (c) it is a proof (theorem/lemma/abbrev), never an instance,
structure, def or inductive.  Under those three conditions deleting it cannot
change what the tree proves, and cannot break compilation: proofs are only ever
invoked by name.

  python3 fixpoint.py --work PRISTINE --dst OUT --log DG.log [--max N]
"""
import json, re, os, argparse, pathlib, shutil, collections

DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+|partial\s+|unsafe\s+|scoped\s+)*"
                  r"(theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque)\s+([^\s:{(​\[]+)")
NS = re.compile(r"^namespace\s+([\w.]+)\s*$")
SEC = re.compile(r"^(?:noncomputable\s+|private\s+|protected\s+|public\s+)?section(?:\s+[\w.]+)?\s*$")
MUT = re.compile(r"^mutual\s*$")
END = re.compile(r"^end(?:\s+([\w.]+))?\s*$")
ENDL = re.compile(r"^\s*end(?:\s+[\w.]+)?\s*$")
STRUCT = re.compile(r"^\s*(variable|open|section|omit|attribute|set_option|universe|local\b|private\b|scoped\b|noncomputable\b|include\b)\b")
TOK = re.compile(r"[A-Za-z_\u00a1-\uffff][A-Za-z0-9_'!?\u00a1-\uffff]*")
SAFE_KINDS = {"theorem", "lemma", "abbrev"}

def deletable_region(lines, start, end):
    j = end
    while j > start and lines[j-1].strip() == '': j -= 1
    while j > start and (ENDL.match(lines[j-1]) or STRUCT.match(lines[j-1])
                         or lines[j-1].lstrip().startswith('--')): j -= 1
    if j > start and lines[j-1].strip().endswith('-/'):
        k = j - 1
        while k > start and not lines[k-1].strip().startswith('/--'): k -= 1
        j = k
    while j > start and lines[j-1].strip() == '': j -= 1
    return j

def scan(root):
    root = pathlib.Path(root)
    out = []
    tok = collections.Counter()
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
            out.append(dict(mod=mod, kind=kind, name=name, full=full, line=i, end=end,
                            lines=end - i + 1, path=str(f)))
    hdr = collections.Counter(d["name"] for d in out)
    return out, tok, hdr

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True)
    ap.add_argument("--dst", required=True)
    ap.add_argument("--log", required=True)
    ap.add_argument("--max", type=int, default=12)
    a = ap.parse_args()
    reached, reachedpairs = set(), set()
    for line in open(a.log, encoding="utf-8", errors="ignore"):
        p = line.split()
        if p and p[0] == "NODE":
            reached.add(p[2]); reachedpairs.add((p[1], p[2].split(".")[-1]))
    dst = pathlib.Path(a.dst)
    if dst.exists(): shutil.rmtree(dst)
    shutil.copytree(pathlib.Path(a.work) / "lean", dst / "lean")
    for it in range(1, a.max + 1):
        decls, tok, hdr = scan(dst)
        dead = [d for d in decls
                if d["full"] not in reached and (d["mod"], d["name"]) not in reachedpairs
                and d["kind"] in SAFE_KINDS and tok[d["name"]] - hdr[d["name"]] <= 0]
        if not dead:
            print(f"iter {it}: fixpoint, nothing left"); break
        per = collections.defaultdict(list)
        for d in dead: per[d["path"]].append(d)
        removed = 0
        for path, ds in per.items():
            p = pathlib.Path(path)
            lines = p.read_text(errors="ignore").splitlines()
            for d in sorted(ds, key=lambda d: -d["line"]):
                j = deletable_region(lines, d["line"], min(d["end"], len(lines)))
                del lines[d["line"]-1:j]
                removed += j - (d["line"] - 1)
            p.write_text("\n".join(lines) + "\n")
        print(f"iter {it}: {len(dead)} decls ({sum(d['lines'] for d in dead)} span-lines), "
              f"{removed} raw lines removed from {len(per)} files")
    tot = sum(1 for f in (dst / "lean" / "OAI").rglob("*.lean") for _ in open(f, errors="ignore"))
    print(f"final tree: {tot} raw lines over "
          f"{len(list((dst / 'lean' / 'OAI').rglob('*.lean')))} modules")

main()
