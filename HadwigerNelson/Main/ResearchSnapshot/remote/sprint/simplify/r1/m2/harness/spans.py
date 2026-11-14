#!/usr/bin/env python3
"""Declaration line spans, namespace-aware, for lean/OAI.

  python3 spans.py --root DIR --json OUT      -> {fullname: {mod, line, end, lines, kind}}
The span of a declaration runs from its start line to the line before the next
declaration in the same module (so it includes the doc comment, the proof and the
blank line that follows); this makes "lines freed by deleting decls" additive.
"""
import re, sys, json, pathlib, argparse

DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+|partial\s+|unsafe\s+|scoped\s+)*"
                  r"(theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque)\s+([^\s:{(\[]+)")
NS = re.compile(r"^namespace\s+([\w.]+)\s*$")
SEC = re.compile(r"^(?:noncomputable\s+|private\s+|protected\s+|public\s+)?section(?:\s+[\w.]+)?\s*$")
MUT = re.compile(r"^mutual\s*$")
END = re.compile(r"^end(?:\s+([\w.]+))?\s*$")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    root = pathlib.Path(a.root)
    out = {}
    for p in sorted((root / "lean" / "OAI").rglob("*.lean")):
        mod = ".".join(p.relative_to(root / "lean").with_suffix("").parts)
        lines = p.read_text(errors="ignore").splitlines()
        stack, found = [], []
        for i, ln in enumerate(lines, 1):
            if NS.match(ln):
                stack.append(NS.match(ln).group(1)); continue
            if SEC.match(ln) or MUT.match(ln):
                stack.append(""); continue
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
                full = f"{pre}.{name}" if pre else name
                found.append((full, kind, i))
        for j, (full, kind, i) in enumerate(found):
            end = (found[j+1][2] - 1) if j + 1 < len(found) else len(lines)
            out[full] = dict(mod=mod, line=i, end=end, lines=end - i + 1, kind=kind)
    if a.json: pathlib.Path(a.json).write_text(json.dumps(out, indent=0))
    print(f"{len(out)} declarations over {len(set(v['mod'] for v in out.values()))} modules")
    if not a.json:
        for k in sorted(out, key=lambda k: -out[k]["lines"])[:20]:
            print(f"{out[k]['lines']:5d} {out[k]['mod']}:{out[k]['line']} {k}")

main()
