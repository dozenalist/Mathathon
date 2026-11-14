#!/usr/bin/env python3
"""Cluster OAI declaration statements/proofs by normalised shape, to find
generalise-and-collapse candidates (direction d11).

  python3 cluster.py --root <TREE>/OAI [--mode stmt|proof|both] [--min N]
"""
import re, sys, os, json, argparse, collections

DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+|partial\s+|unsafe\s+|scoped\s+)*"
                  r"(theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque)\s+([^\s:{(​\[]+)")
NS = re.compile(r"^namespace\s+([\w.]+)\s*$")
SEC = re.compile(r"^(?:noncomputable\s+|private\s+|protected\s+|public\s+)?section(?:\s+[\w.]+)?\s*$")
MUT = re.compile(r"^mutual\s*$")
END = re.compile(r"^end(?:\s+([\w.]+))?\s*$")

KW = set("""theorem lemma def abbrev structure class instance inductive opaque by fun have show
from exact intro apply refine rw simp simpa unfold change congr ext constructor cases obtain rcases
let set calc at with if then else match forall exists not and or iff eq refl rfl trivial assumption
continuity measurability positivity ring norm_num linarith nlinarith omega decide infer_instance
subst induction using this exact_mod_cast push_cast field_simp positivity linear_combination
""".split())

def norm(text):
    # strip strings/comments, replace identifiers by _ , keep numerals & symbols
    t = re.sub(r"/-.*?-/", " ", text, flags=re.S)
    t = re.sub(r"--[^\n]*", " ", t)
    toks = re.findall(r"[A-Za-z_\u00a1-\uffff][A-Za-z0-9_'!?.\u00a1-\uffff]*|\d+|[^\sA-Za-z0-9_\u00a1-\uffff]", t)
    out = []
    for x in toks:
        if x in KW:
            out.append(x)
        elif re.fullmatch(r"\d+", x):
            out.append("0")
        elif re.fullmatch(r"[^\sA-Za-z0-9_\u00a1-\uffff]", x):
            out.append(x)
        else:
            out.append("_")
    return "".join(out)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--mode", default="stmt")
    ap.add_argument("--min", type=int, default=2)
    ap.add_argument("--top", type=int, default=40)
    a = ap.parse_args()
    decls = []
    for dp, dn, fn in os.walk(a.root):
        for f in sorted(fn):
            if not f.endswith(".lean"): continue
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, a.root)
            lines = open(p, encoding="utf-8", errors="ignore").read().splitlines()
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
                    found.append((kind, (pre + "." + name) if pre else name, i))
            for j, (kind, full, i) in enumerate(found):
                end = (found[j+1][2] - 1) if j + 1 < len(found) else len(lines)
                body = "\n".join(lines[i-1:end])
                # split header / proof at first ':= by' or ':=' at depth 0
                m = re.search(r"\n\s*(:=|where)\b", body)
                if m:
                    hdr, prf = body[:m.start()], body[m.start():]
                else:
                    hdr, prf = body, ""
                decls.append(dict(mod=rel, kind=kind, name=full, line=i, end=end,
                                  lines=end - i + 1, hdr=hdr, prf=prf))
    print(f"{len(decls)} declarations, {sum(d['lines'] for d in decls)} lines covered")
    for mode in (["stmt", "proof"] if a.mode == "both" else [a.mode]):
        cl = collections.defaultdict(list)
        for d in decls:
            k = norm(d["hdr"] if mode == "stmt" else d["prf"])
            if len(k) < 8: continue
            cl[k].append(d)
        groups = [v for v in cl.values() if len(v) >= a.min]
        groups.sort(key=lambda v: -sum(d["lines"] for d in v))
        print(f"\n=== {mode}: {len(groups)} clusters (>= {a.min}), "
              f"{sum(sum(d['lines'] for d in v) for v in groups)} lines in clusters ===")
        for v in groups[:a.top]:
            tot = sum(d["lines"] for d in v)
            if tot < 15: continue
            print(f"-- {len(v)} decls, {tot} lines | {v[0]['mod']}:{v[0]['line']} {v[0]['name']}")
            for d in v:
                print(f"     {d['lines']:4d} {d['mod']}:{d['line']} {d['name']}")
main()
