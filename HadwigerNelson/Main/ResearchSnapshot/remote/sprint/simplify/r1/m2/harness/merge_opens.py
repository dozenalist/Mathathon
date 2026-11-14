#!/usr/bin/env python3
"""Merge ADJACENT same-kind `open` commands; never drops one.  Provably safe.

  python3 merge_opens.py --root TREE [--apply]

`open A` followed by `open B` (both column 0, neither an `open ... in` form) has exactly the
effect of `open A B`: `open` accumulates monotonically inside a block and the two commands are
adjacent, so nothing can shadow between them.  The same holds for two `open scoped`.  Plain and
scoped commands are NEVER merged (`open A scoped B` is not Lean, see f33), so there is no block
tracking and no dropping: the only possible failure mode of a drop (a name that a later block
needs) cannot arise.
"""
import argparse, pathlib, re
OPENP = re.compile(r"^open\s+(?!scoped\b)([A-Za-z0-9_.'\u2080-\u209c\s]+?)\s*$")
OPENS = re.compile(r"^open\s+scoped\s+([A-Za-z0-9_.'\u2080-\u209c\s]+?)\s*$")
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
    root = pathlib.Path(a.root)/"lean"/"OAI"; tot = 0
    for p in sorted(root.rglob("*.lean")):
        lines = p.read_text().splitlines(); out = []; i = 0; d = 0
        while i < len(lines):
            cur = lines[i]
            if i + 1 < len(lines):
                for kind, rx in (("open ", OPENP), ("open scoped ", OPENS)):
                    m1 = rx.match(cur)
                    m2 = rx.match(lines[i+1])
                    if m1 and m2:
                        names = list(dict.fromkeys(m1.group(1).split() + m2.group(1).split()))
                        out.append(kind + " ".join(names)); d += 1; i += 2; break
                else:
                    out.append(cur); i += 1
                continue
            out.append(cur); i += 1
        if d:
            tot += d
            if a.apply: p.write_text("\n".join(out) + "\n")
    print(f"adjacent same-kind open lines merged: {tot}")
main()
