#!/usr/bin/env python3
"""Kind-separated `open` compaction (repairs m7's compact_opens.py, see f33).

  python3 compact_opens2.py --root TREE [--apply]

Rewrites, all semantics preserving because `open` accumulates monotonically inside a block:
 1. drop a column-0 `open`/`open scoped` whose names are already open in the enclosing block
    (checked in the SAME kind only: plain vs scoped are different namespaces pools);
 2. merge two ADJACENT lines of the same kind into one (`open A` + `open B` -> `open A B`).
Never merges a plain open with an `open scoped` (that produced `open A scoped B`, which is not
Lean), never touches `open ... in`, never touches indented opens, tracks section/namespace/end.
"""
import argparse, pathlib, re
NS = re.compile(r"^(?:(?:noncomputable|private|protected|public)\s+)*(?:namespace|section|mutual)\b")
END = re.compile(r"^end(?:\s+([\w.]+))?\s*$")
OPENP = re.compile(r"^open\s+(?!scoped\b)([A-Za-z0-9_.'\u2080-\u209c\s]+?)\s*$")
OPENS = re.compile(r"^open\s+scoped\s+([A-Za-z0-9_.'\u2080-\u209c\s]+?)\s*$")
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true"); a = ap.parse_args()
    root = pathlib.Path(a.root)/"lean"/"OAI"; tot = 0
    for p in sorted(root.rglob("*.lean")):
        lines = p.read_text().splitlines()
        stack = [[set(), set()]]; out = []; dropped = 0; i = 0
        while i < len(lines):
            ln = lines[i]
            if END.match(ln):
                if len(stack) > 1: stack.pop()
                out.append(ln); i += 1; continue
            if NS.match(ln):
                stack.append([set(stack[-1][0]), set(stack[-1][1])])
                out.append(ln); i += 1; continue
            mp, msc = OPENP.match(ln), OPENS.match(ln)
            if not (mp or msc):
                out.append(ln); i += 1; continue
            kind = 0 if mp else 1
            names = (mp or msc).group(1).split()
            act = stack[-1][kind]
            if all(n in act for n in names):
                dropped += 1; i += 1; continue
            if i + 1 < len(lines):
                nxt = lines[i+1]
                m2 = OPENP.match(nxt) if kind == 0 else OPENS.match(nxt)
                if m2:
                    extra = m2.group(1).split()
                    names = list(dict.fromkeys(names + extra))
                    act.update(names); dropped += 1
                    out.append(("open " if kind == 0 else "open scoped ") + " ".join(names))
                    i += 2; continue
            act.update(names)
            out.append(ln); i += 1
        if dropped:
            tot += dropped
            if a.apply: p.write_text("\n".join(out) + "\n")
    print(f"total removable open lines: {tot}")
main()
