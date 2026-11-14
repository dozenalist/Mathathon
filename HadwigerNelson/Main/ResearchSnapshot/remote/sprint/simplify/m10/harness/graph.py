#!/usr/bin/env python3
"""Module graph + line counting for the OAI Lean development.

Usage:
  graph.py count  [--root DIR] [--json OUT]      per-module lines
  graph.py reach  MOD ... [--root DIR] [--json]  import-reachable set from MODs
  graph.py tree   MOD ... [--root DIR]           print reachable set with lines
"""
import re, sys, json, pathlib

IMP = re.compile(r"^import\s+([\w.]+)\s*$", re.M)

def modules(root):
    root = pathlib.Path(root)
    ms = {}
    for p in sorted((root / "lean" / "OAI").rglob("*.lean")):
        name = ".".join(p.relative_to(root / "lean").with_suffix("").parts)
        txt = p.read_text(errors="ignore")
        deps = [d for d in IMP.findall(txt) if d.startswith("OAI.")]
        lines = txt.count("\n") + (0 if txt.endswith("\n") or not txt else 1)
        # code lines: drop blank and full-line comments / docstring-only lines
        code = 0
        for ln in txt.splitlines():
            s = ln.strip()
            if not s or s.startswith("--") or s.startswith("/-") or s.startswith("-/"):
                continue
            code += 1
        ms[name] = dict(path=str(p.relative_to(root)), deps=deps, lines=lines,
                        code=code, bytes=len(txt))
    return ms

def reach(ms, roots):
    seen, stack = set(), list(roots)
    while stack:
        n = stack.pop()
        if n in seen: continue
        if n not in ms:
            print(f"WARN unknown module {n}", file=sys.stderr); continue
        seen.add(n); stack.extend(ms[n]["deps"])
    return seen

def main():
    a = sys.argv[1:]
    root = "."
    if "--root" in a:
        i = a.index("--root"); root = a[i+1]

    ms = modules(root)
    if a and a[0] == "count":
        tot = sum(v["lines"] for v in ms.values())
        totc = sum(v["code"] for v in ms.values())
        if "--json" in a:
            pathlib.Path(a[a.index("--json")+1]).write_text(json.dumps(
                {k: {kk: vv for kk, vv in v.items()} for k, v in ms.items()} | {"__total__": {"lines": tot, "code": totc}}, indent=0))
        else:
            for k in sorted(ms, key=lambda k: -ms[k]["lines"]):
                print(f"{ms[k]['lines']:6d} {ms[k]['code']:6d} {k}")
            print(f"{tot:6d} {totc:6d} TOTAL ({len(ms)} modules)")
        return
    if a and a[0] in ("reach", "tree"):
        roots = [x for x in a[1:] if not x.startswith("--")]
        sel = reach(ms, roots)
        tot = sum(ms[n]["lines"] for n in sel)
        if a[0] == "tree":
            for k in sorted(sel, key=lambda k: -ms[k]["lines"]):
                print(f"{ms[k]['lines']:6d} {k}")
        print(f"{tot} lines in {len(sel)}/{len(ms)} modules", file=sys.stderr if a[0]!="tree" else sys.stdout)
        if "--json" in a:
            pathlib.Path(a[a.index("--json")+1]).write_text(json.dumps(sorted(sel)))
        return
    print(__doc__)

main()
