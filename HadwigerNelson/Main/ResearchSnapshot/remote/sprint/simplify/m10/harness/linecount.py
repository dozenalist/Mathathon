#!/usr/bin/env python3
"""Before/after line audit for a candidate tree.

  python3 linecount.py --base BASELINE.json --root DIR [--md] [--csv FILE]

Reports, per module: lines before, lines after, delta; plus totals and the
count of modules removed/added.  Non-.lean files added to lean/OAI are ignored.
Exit code 1 if the total saving is below --target (default 1500).
"""
import argparse, json, subprocess, sys, pathlib

def load(root):
    h = pathlib.Path(__file__).resolve().parent
    subprocess.run([sys.executable, str(h / "graph.py"), "count", "--root", str(root),
                    "--json", "/dev/stdout"], check=True, capture_output=True)
    return None

def counts(root):
    h = pathlib.Path(__file__).resolve().parent
    import tempfile, os
    with tempfile.NamedTemporaryFile("r", suffix=".json", delete=False) as f:
        tmp = f.name
    subprocess.run([sys.executable, str(h / "graph.py"), "count", "--root", str(root), "--json", tmp],
                   check=True, capture_output=True)
    d = json.loads(pathlib.Path(tmp).read_text()); os.unlink(tmp)
    tot = d.pop("__total__")
    return d, tot

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--root", default=".")
    ap.add_argument("--md", action="store_true")
    ap.add_argument("--csv")
    ap.add_argument("--target", type=int, default=1500)
    a = ap.parse_args()
    old = json.loads(pathlib.Path(a.base).read_text())
    otot = old.pop("__total__")
    new, ntot = counts(a.root)
    rows, dl = [], 0
    for m in sorted(set(old) | set(new)):
        b = old.get(m, {}).get("lines", 0); c = new.get(m, {}).get("lines", 0)
        if b != c or (m in old) != (m in new):
            tag = "removed" if m not in new else ("added" if m not in old else "")
            rows.append((b, c, c - b, m, tag))
            dl += c - b
    rows.sort(key=lambda r: r[2])
    if a.csv:
        with open(a.csv, "w") as f:
            f.write("before,after,delta,module,status\n")
            for b, c, d, m, t in rows: f.write(f"{b},{c},{d},{m},{t}\n")
            f.write(f"{otot['lines']},{ntot['lines']},{ntot['lines']-otot['lines']},TOTAL,\n")
    p = print
    if a.md: p("| module | before | after | delta |\n|---|---|---|---|")
    else: p(f"{'before':>7} {'after':>7} {'delta':>7}  module")
    for b, c, d, m, t in rows:
        if a.md: p(f"| `{m}`{(' ('+t+')') if t else ''} | {b} | {c} | {d:+d} |")
        else: p(f"{b:7d} {c:7d} {d:+7d}  {m}" + (f"  [{t}]" if t else ""))
    if a.md:
        p(f"| **TOTAL** | **{otot['lines']}** | **{ntot['lines']}** | **{ntot['lines']-otot['lines']:+d}** |")
        p(f"\nmodules: {len(old)} -> {len(new)}; code-lines {otot['code']} -> {ntot['code']}")
    else:
        p(f"{otot['lines']:7d} {ntot['lines']:7d} {ntot['lines']-otot['lines']:+7d}  TOTAL ({len(old)} -> {len(new)} modules)")
        p(f"code-lines {otot['code']} -> {ntot['code']} ({ntot['code']-otot['code']:+d})")
    saving = otot["lines"] - ntot["lines"]
    p(f"\nSAVING: {saving} raw lines, target {a.target}: {'MET' if saving >= a.target else 'NOT MET'}", file=sys.stderr)
    sys.exit(0 if saving >= a.target else 1)

main()
