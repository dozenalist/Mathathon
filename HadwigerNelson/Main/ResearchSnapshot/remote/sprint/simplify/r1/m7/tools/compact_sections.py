#!/usr/bin/env python3
"""Remove `noncomputable section ... end` pairs that are provably no-ops.

A pair is removed only when
  * the enclosing frame is already `noncomputable` (so the flag is inherited), and
  * its body contains no `variable`, `open`, `set_option`, `attribute`, `instance`,
    `local`, `include`, `omit`, nested `section`/`namespace`/`mutual` or attribute line,
so deleting the pair changes nothing at all.

  python3 compact_sections.py --root DIR [--apply]
"""
import argparse, pathlib, re

NC = re.compile(r"^(?:private\s+|protected\s+)?noncomputable\s+section(?:\s+[\w.]+)?\s*$")
SEC = re.compile(r"^(?:private\s+|protected\s+|public\s+)?section(?:\s+([\w.]+))?\s*$")
NS = re.compile(r"^namespace\s+([\w.]+)\s*$")
MUT = re.compile(r"^mutual\s*$")
END = re.compile(r"^end(?:\s+([\w.]+))?\s*$")
BAD = re.compile(r"^\s*(variable|open|set_option|attribute|instance|local|include|omit|universe|"
                 r"section|namespace|mutual|noncomputable|@\[|#)")


def compact(lines):
    stack = [dict(kind="root", name=None, nc=True)]   # module level counts as noncomputable? no:
    stack[0]["nc"] = False
    start = {}                    # stack depth -> line index of the opener
    killed = set()
    for i, ln in enumerate(lines):
        m = END.match(ln)
        if m and not ln.startswith(" "):
            nm = m.group(1)
            if len(stack) > 1:
                top = stack[-1]
                if (nm is None and top["kind"] in ("sec", "mut", "nc")) or (nm is not None and nm == top["name"]):
                    opener = start.pop(len(stack), None)
                    if opener is not None and top["kind"] == "nc" and stack[-2]["nc"]:
                        body = lines[opener + 1:i]
                        if not any(BAD.match(b) for b in body) and not any("/-" in b for b in body):
                            killed.add(opener); killed.add(i)
                    stack.pop()
            continue
        mn = NC.match(ln)
        ms, mns, mm = SEC.match(ln), NS.match(ln), MUT.match(ln)
        if mn:
            stack.append(dict(kind="nc", name=None, nc=True))
            start[len(stack)] = i
        elif ms:
            stack.append(dict(kind="sec", name=ms.group(1), nc=stack[-1]["nc"]))
            start[len(stack)] = i
        elif mns:
            stack.append(dict(kind="ns", name=mns.group(1), nc=stack[-1]["nc"]))
            start[len(stack)] = i
        elif mm:
            stack.append(dict(kind="mut", name=None, nc=stack[-1]["nc"]))
            start[len(stack)] = i
    return [ln for j, ln in enumerate(lines) if j not in killed], len(killed) // 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    base = pathlib.Path(a.root) / "lean" / "OAI"
    tot = 0
    for p in sorted(base.rglob("*.lean")):
        lines = p.read_text(errors="ignore").splitlines()
        out, n = compact(lines)
        if n:
            tot += n
            print(f"{2*n:5d}  {p.relative_to(base.parent)}")
            if a.apply:
                p.write_text("\n".join(out) + "\n")
    print(f"redundant noncomputable-section pairs removable: {tot} (= {2*tot} lines)")


main()
