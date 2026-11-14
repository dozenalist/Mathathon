#!/usr/bin/env python3
"""Delete a `section`/`namespace X` that is immediately followed by its `end` (blank/comment lines
only in between).  `python3 drop_empty_blocks.py --root TREE [--apply]`.  An empty section has no
effect on elaboration, so removing both lines is semantics preserving.
"""
import argparse, pathlib, re
OP = re.compile(r"^\s*(namespace\s+[\w.]+|section(?:\s+\w+)?|noncomputable\s+section|mutual)\s*$")
EN = re.compile(r"^\s*end(?:\s+[\w.]+)?\s*$")
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
    root = pathlib.Path(a.root)/"lean"/"OAI"; tot = 0
    for p in sorted(root.rglob("*.lean")):
        lines = p.read_text().splitlines(); stack = []; kill = set()
        for i, ln in enumerate(lines):
            if OP.match(ln): stack.append(i)
            elif EN.match(ln) and stack:
                j = stack.pop()
                body = [x for x in lines[j+1:i] if x.strip() and not x.strip().startswith(("--", "/-", "-/", "*"))]
                if not body: kill.update({j, i})
        if kill:
            tot += len(kill)
            if a.apply: p.write_text("\n".join(l for i, l in enumerate(lines) if i not in kill) + "\n")
    print(f"empty-block lines removed: {tot}")
main()
