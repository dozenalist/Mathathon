#!/usr/bin/env python3
"""Approximate declaration index + external-use counts for lean/OAI.

  python3 decls.py --root DIR [--uses NAME] [--unused] [--json OUT]

Splits each module into declared names (namespace-aware, approximate: tracks
`namespace`/`end` at line starts) and counts occurrences of each name in *other*
modules of the tree.  `--unused` lists declarations with zero external textual
occurrences and their line spans -- a candidate list for deletion, NOT a proof
of deadness (a name can be used only through `simp`/instance search or via an
anonymous instance).
"""
import re, sys, json, pathlib, argparse, collections

DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+|partial\s+|unsafe\s+)*"
                  r"(theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque)\s+([^\s:{(\[]+)")
NS = re.compile(r"^namespace\s+([\w.]+)\s*$")
END = re.compile(r"^end(?:\s+([\w.]+))?\s*$")

def index(root):
    root = pathlib.Path(root)
    mods = {}
    for p in sorted((root / "lean" / "OAI").rglob("*.lean")):
        mod = ".".join(p.relative_to(root / "lean").with_suffix("").parts)
        mods[mod] = p
    text = {m: p.read_text(errors="ignore") for m, p in mods.items()}
    decls = []          # (fullname, kind, mod, line)
    for m, t in text.items():
        stack = []
        for i, ln in enumerate(t.splitlines(), 1):
            s = ln.strip()
            # doc comment lines may contain 'namespace' text; only match raw starts
            mo = NS.match(ln)
            if mo:
                stack.append(mo.group(1)); continue
            eo = END.match(ln)
            if eo and stack:
                continue
            d = DECL.match(ln)
            if d:
                kind, name = d.group(1), d.group(2)
                if name in ("where", "at"): continue
                pre = ".".join(stack)
                full = f"{pre}.{name}" if pre else name
                decls.append((full, kind, m, i, len(ln) - len(ln.lstrip())))
    return mods, text, decls

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--unused", action="store_true")
    ap.add_argument("--uses", default=None)
    ap.add_argument("--json", default=None)
    ap.add_argument("--all", action="store_true")
    a = ap.parse_args()
    mods, text, decls = index(a.root)
    TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_']*")
    cnt = {m: collections.Counter(TOK.findall(t)) for m, t in text.items()}
    out = []
    for full, kind, mod, line, _ in decls:
        base = full.split(".")[-1]
        if len(base) <= 2: continue
        ext = sum(c[base] for m, c in cnt.items() if m != mod)
        where = [m for m, c in cnt.items() if m != mod and c[base]]
        out.append(dict(name=full, kind=kind, mod=mod, line=line, external=ext, users=where))
    if a.json: pathlib.Path(a.json).write_text(json.dumps(out, indent=0))
    if a.uses:
        sel = [d for d in out if a.uses in d["name"]]
        for d in sorted(sel, key=lambda d: d["external"]):
            print(f"{d['external']:4d} uses  {d['kind']:9s} {d['name']}  [{d['mod']}:{d['line']}]")
            for u in d["users"][:6]: print(f"          <- {u}")
        return
    if a.unused:
        for d in sorted(out, key=lambda d: d["mod"]):
            if d["external"] == 0: print(f"{d['kind']:9s} {d['name']}  [{d['mod']}:{d['line']}]")
        return
    tot = len(out)
    print(f"{tot} declarations indexed; "
          f"{sum(1 for d in out if d['external']==0)} with zero external textual use")

main()
