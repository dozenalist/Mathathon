#!/usr/bin/env python3
"""Mechanical trim of a copy of the staged tree: delete the three closure-free
modules and a set of declarations that lie outside the proof-term closure of the
seven headline declarations.

spans.py runs a declaration from its start line to the line before the next one,
so a span also covers every command in between (`variable`, `open scoped`,
`attribute`, `local instance`, `section`/`end`, a leading `/-!`).  Those are
clipped off the span before deleting, otherwise later proofs in the same file
break in ways that look unrelated.

  python3 trim2.py --src <tree> --dst <tree> --drop SET.json [SET.json ...]
"""
import argparse
import json
import pathlib
import re
import shutil

REPO = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo")
SPANS = REPO / ".ultramath/smwg224wy/m3/SPANS_stage.json"

# a line at this indentation starts a new command: never delete it from a span tail
CMD = re.compile(r"^(\s*)(variable|variables|attribute|local|open|section|end|"
                 r"namespace|set_option|noncomputable|@\[|/-!|#)")
ATTR = re.compile(r"^\s*@\[")
CLOSE = re.compile(r"^\s*-/\s*$")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst", required=True)
    ap.add_argument("--drop", nargs="+", required=True)
    a = ap.parse_args()
    src, dst = pathlib.Path(a.src), pathlib.Path(a.dst)
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    sp = json.loads(SPANS.read_text())
    dead = set()
    for f in a.drop:
        dead |= set(json.loads((REPO / ".ultramath/smwg224wy/m3" / f).read_text()))

    drop_mods = ["OAI.Geometry.PlaneColoring.ConnectedUnitFree",
                 "OAI.Geometry.PlaneColoring.MeasurableAssembly",
                 "OAI.Geometry.PlaneColoring.MeasurableProper"]
    for m in drop_mods:
        p = dst / "lean" / (m.replace(".", "/") + ".lean")
        if p.exists():
            p.unlink()

    bymod = {}
    for k, v in sp.items():
        if k in dead:
            bymod.setdefault(v["mod"], []).append((v["line"], v["end"], k))
    total = 0
    for mod, rows in sorted(bymod.items()):
        p = dst / "lean" / (mod.replace(".", "/") + ".lean")
        lines = p.read_text().splitlines()
        kill = set()
        for a0, b0, name in rows:
            a, b = a0, min(b0, len(lines))
            # absorb a lone attribute line above the declaration
            while a >= 2 and ATTR.match(lines[a - 2]) and lines[a - 2].lstrip().startswith("@["):
                a -= 1
            # absorb a docstring block that closes on the line above
            if a >= 2 and lines[a - 2].rstrip().endswith("-/"):
                j = a - 2
                while j >= 1 and "/-" not in lines[j - 1] and not CMD.match(lines[j - 1]):
                    j -= 1
                if j >= 1 and "/-" in lines[j - 1]:
                    a = j
            # clip the tail: keep every trailing command/blank line that follows the
            # declaration (spans swallow inter-declaration commands)
            t = b + 1
            i = b
            while i > a:
                ln = lines[i - 1]
                if ln.strip() == "" or CMD.match(ln):
                    t = i
                    i -= 1
                else:
                    break
            b = t - 1
            kill.update(range(a, b + 1))
        kept = [ln for i, ln in enumerate(lines, 1) if i not in kill]
        p.write_text("\n".join(kept) + "\n")
        total += len(kill)
    print(f"declaration lines removed: {total}")

    gone = set(drop_mods)
    for p in sorted((dst / "lean" / "OAI").rglob("*.lean")):
        lines = p.read_text().splitlines()
        keep = [ln for ln in lines
                if not (ln.startswith("import ") and ln[len("import "):].strip() in gone)]
        if len(keep) != len(lines):
            p.write_text("\n".join(keep) + "\n")

    n = m = 0
    for p in (dst / "lean" / "OAI").rglob("*.lean"):
        m += 1
        n += len(p.read_text().splitlines())
    print(f"tree: {m} modules, {n} raw lines")


main()
