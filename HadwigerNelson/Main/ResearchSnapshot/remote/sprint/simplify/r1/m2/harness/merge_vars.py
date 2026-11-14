#!/usr/bin/env python3
"""Merge adjacent single-line `variable` commands: `variable A` + `variable B` -> `variable A B`.
  python3 merge_vars.py --root TREE [--apply]
Semantics preserving: Lean's `variable` accumulates binders in the enclosing block, in order, so
two consecutive commands declare exactly the binders of the merged one.  Only column-0 lines that
are a complete command are touched (`open ... in`-style forms, indented lines, and lines with a
trailing ` in` are left alone).
"""
import argparse, pathlib, re
VAR = re.compile(r"^variable\s+(?!\[)(.*\S)\s*$")
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
    root = pathlib.Path(a.root)/"lean"/"OAI"; tot = 0
    for p in sorted(root.rglob("*.lean")):
        lines = p.read_text().splitlines(); out = []; i = 0; d = 0
        while i < len(lines):
            cur = lines[i]
            if i + 1 < len(lines):
                m1, m2 = VAR.match(cur), VAR.match(lines[i+1])
                if m1 and m2 and " in " not in cur and " in " not in lines[i+1]:
                    out.append("variable " + m1.group(1) + " " + m2.group(1)); d += 1; i += 2; continue
            out.append(cur); i += 1
        if d:
            tot += d
            if a.apply: p.write_text("\n".join(out) + "\n")
    print(f"variable lines merged: {tot}")
main()
