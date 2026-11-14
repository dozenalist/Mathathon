#!/usr/bin/env python3
"""Remove redundant column-0 `open` / `open scoped` commands.

Two rewrites, both semantics preserving:
 1. drop an `open` line all of whose names are already open in the enclosing block;
 2. merge two adjacent plain `open` lines into one.

Section/namespace structure is tracked with a stack of markers; `end` pops only a
matching marker, and on any ambiguity it pops nothing (which can only make the
script *keep* an `open`, never drop a needed one).  Lines containing `--`, `(`
or a trailing `in` are never touched; `open ... in` is left alone.

  python3 compact_opens.py --root DIR [--apply] [--only MOD ...]
"""
import argparse, pathlib, re

SEC = re.compile(r"^(?:noncomputable\s+|private\s+|protected\s+|public\s+)*section(?:\s+([\w.]+))?\s*$")
NS = re.compile(r"^namespace\s+([\w.]+)\s*$")
MUT = re.compile(r"^mutual\s*$")
END = re.compile(r"^end(?:\s+([\w.]+))?\s*$")
NAMES = r"[A-Za-z0-9_.'\u2080-\u209c]+(?:\s+[A-Za-z0-9_.'\u2080-\u209c]+)*"
OPENP = re.compile(r"^open\s+(" + NAMES + r")\s*$")
OPENS = re.compile(r"^open\s+scoped\s+(" + NAMES + r")\s*$")


def compact(lines):
    stack = [("root", None, set(), set())]          # (kind, name, plain, scoped)
    out, dropped = [], 0
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = END.match(ln)
        if m and not ln.startswith(" "):
            nm = m.group(1)
            k, top, _, _ = stack[-1]
            if len(stack) > 1 and ((nm is None and top is None) or (nm is not None and nm == top)):
                stack.pop()
            out.append(ln); i += 1; continue
        ms = SEC.match(ln)
        mn = NS.match(ln)
        if ms or mn or MUT.match(ln):
            name = (ms.group(1) if ms else (mn.group(1) if mn else None))
            stack.append(("b", name, set(stack[-1][2]), set(stack[-1][3])))
            out.append(ln); i += 1; continue
        if "--" not in ln and "(" not in ln:
            mp, msc = OPENP.match(ln), OPENS.match(ln)
            if mp or msc:
                names = (mp or msc).group(1).split()
                act = stack[-1][3] if msc else stack[-1][2]
                if names and names[0] != "scoped" and names[-1] != "in" and all(n in act for n in names):
                    dropped += 1; i += 1; continue
                if mp and names[0] != "scoped" and i + 1 < len(lines) and "--" not in lines[i + 1] and "(" not in lines[i + 1]:
                    mp2 = None if OPENS.match(lines[i + 1]) else OPENP.match(lines[i + 1])
                    if mp2 and mp2.group(1).split()[0] != "scoped" and mp2.group(1).split()[-1] != "in":
                        names = names + mp2.group(1).split()
                        stack[-1][2].update(names)
                        dropped += 1
                        out.append("open " + " ".join(names))
                        i += 2; continue
                act.update(names)
                out.append(ln); i += 1; continue
        out.append(ln); i += 1
    return out, dropped


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    base = pathlib.Path(a.root) / "lean" / "OAI"
    tot = 0
    for p in sorted(base.rglob("*.lean")):
        lines = p.read_text(errors="ignore").splitlines()
        out, dropped = compact(lines)
        if dropped:
            tot += dropped
            print(f"{dropped:4d}  {p.relative_to(base.parent)}")
            if a.apply:
                p.write_text("\n".join(out) + "\n")
    print(f"total removable open lines: {tot}")


main()
