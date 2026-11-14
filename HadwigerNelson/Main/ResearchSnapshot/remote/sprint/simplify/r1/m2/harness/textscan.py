#!/usr/bin/env python3
"""Source-level scan for proof holes and trust-me constructs, comment-aware.

  python3 textscan.py --root TREE      exit 1 if anything is found

Looks for `sorry`, `admit`, `native_decide`, `implemented_by`, `@[extern`, `opaque`,
`axiom`, `unsafe`, `set_option autoImplicit`, `set_option maxHeartbeats 0` in *code*
lines only (a `--` or `/- -/` comment is ignored, so prose about `sorry` does not trip it).
The axiom certificate of the 7 headlines cannot see a hole in a declaration the headlines
do not use; this can.
"""
import argparse, pathlib, re, sys
PAT = [("sorry", re.compile(r"\bsorry\b")), ("admit", re.compile(r"\badmit\b")),
       ("native_decide", re.compile(r"\bnative_decide\b")),
       ("implemented_by", re.compile(r"\bimplemented_by\b")),
       ("extern", re.compile(r"@\[\s*extern")), ("opaque", re.compile(r"^\s*(?:@\[[^]]*\]\s*)?opaque\b")),
       ("axiom", re.compile(r"^\s*(?:@\[[^]]*\]\s*)?axiom\b")),
       ("unsafe", re.compile(r"^\s*unsafe\b")),
       ("maxHeartbeats0", re.compile(r"set_option\s+maxHeartbeats\s+0")),
       ("autoImplicit", re.compile(r"set_option\s+autoImplicit\s+true"))]
def code_lines(text):
    out, depth = [], 0
    for i, ln in enumerate(text.splitlines(), 1):
        s, keep, j = ln, [], 0
        while j < len(s):
            if depth == 0 and s.startswith("/-", j): depth = 1; j += 2; continue
            if depth > 0:
                if s.startswith("-/", j): depth = 0; j += 2
                else: j += 1
                continue
            if s.startswith("--", j): break
            keep.append(s[j]); j += 1
        out.append((i, "".join(keep)))
    return out
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--root", default="."); a = ap.parse_args()
    hits = []
    for p in sorted((pathlib.Path(a.root)/"lean"/"OAI").rglob("*.lean")):
        for i, ln in code_lines(p.read_text(errors="ignore")):
            for name, rx in PAT:
                if rx.search(ln): hits.append((str(p), i, name, ln.strip()[:100]))
    for h in hits[:40]: print(f"{h[0]}:{h[1]}: {h[2]}: {h[3]}")
    print(f"TEXTSCAN: {len(hits)} hits" + ("" if hits else " (clean)"))
    sys.exit(1 if hits else 0)
main()
