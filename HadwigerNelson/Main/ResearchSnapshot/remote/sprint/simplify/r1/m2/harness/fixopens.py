#!/usr/bin/env python3
"""Split mixed `open <plain> scoped <scoped>` commands into two valid commands.

  python3 fixopens.py --root TREE [--apply]

`open A B scoped C D` is not Lean: `scoped` is parsed as a namespace name.  Lean's
grammar has two commands, `open A B` and `open scoped C D`, and they are equivalent to
the intended mixed line, so splitting is semantics preserving.  Lines with an ` in`
(`open ... in term`) are left untouched.  Prints the number of lines rewritten.
"""
import argparse, pathlib, re, sys
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
    root = pathlib.Path(a.root)/"lean"/"OAI"; n_files = n_lines = 0
    for p in sorted(root.rglob("*.lean")):
        lines = p.read_text().splitlines(); out = []; changed = False
        for ln in lines:
            if not ln.startswith("open ") or " scoped " not in ln or re.search(r"\bin\b", ln):
                out.append(ln); continue
            toks = ln[5:].split(); plain, scoped, cur = [], [], None
            for t in toks:
                if t == "scoped": cur = scoped; continue
                (scoped if cur is scoped else plain).append(t)
            new = []
            if plain: new.append("open " + " ".join(dict.fromkeys(plain)))
            if scoped: new.append("open scoped " + " ".join(dict.fromkeys(scoped)))
            if not new: new = [ln]
            out.extend(new); changed = True; n_lines += 1
        if changed:
            n_files += 1
            if a.apply: p.write_text("\n".join(out) + "\n")
    print(f"{'rewrote' if a.apply else 'would rewrite'} {n_lines} lines in {n_files} modules")
main()
