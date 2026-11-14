#!/usr/bin/env python3
"""Delete whole-line comments and docstrings; keep every line that carries code or is blank.

  python3 strip_comments.py --root TREE [--apply]

Character-accurate: a line is removed iff it lies wholly inside a comment (`--` to end of line, or a
`/- ... -/` block) and contains no code character.  Lines where a comment shares the line with code
are kept, so token separation can never be lost.  Blank lines are kept.
Lean treats comments as whitespace, so a whole-line comment has no effect on elaboration.
"""
import argparse, pathlib
def scan_line(s, depth):
    """return (has_code, saw_comment, new_depth)"""
    j = 0; code = False; com = depth > 0
    while j < len(s):
        if depth:
            if s.startswith("-/", j): depth = 0; j += 2
            else: j += 1
            continue
        if s.startswith("--", j): com = True; break
        if s.startswith("/-", j): depth = 1; com = True; j += 2; continue
        if s[j] not in " \t": code = True
        j += 1
    return code, com, depth
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
    root = pathlib.Path(a.root)/"lean"/"OAI"; tot = 0
    for p in sorted(root.rglob("*.lean")):
        lines = p.read_text().splitlines(); depth = 0; kill = set()
        for i, ln in enumerate(lines):
            code, com, depth = scan_line(ln, depth)
            if com and not code and ln.strip(): kill.add(i)
        if kill:
            tot += len(kill)
            if a.apply: p.write_text("\n".join(l for k, l in enumerate(lines) if k not in kill) + "\n")
    print(f"comment lines removed: {tot}")
main()
