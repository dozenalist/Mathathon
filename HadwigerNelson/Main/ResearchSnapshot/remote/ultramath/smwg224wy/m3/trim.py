#!/usr/bin/env python3
"""Mechanical trim of a copy of the staged tree: delete the three closure-free
modules and every declaration that lies outside the proof-term closure of the seven
headline declarations.  No statement is touched, nothing is reproved.

  python3 trim.py --src <tree> --dst <tree> [--names SAFE.json REVIEW.json]
"""
import argparse
import json
import pathlib
import re
import shutil

REPO = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo")
SPANS = REPO / ".ultramath/smwg224wy/m3/SPANS_stage.json"

ENDISH = re.compile(r"^\s*end(\s+\S+)?\s*$")
ATTR = re.compile(r"^\s*@\[")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--dst", required=True)
    ap.add_argument("--drop", nargs="*", default=[])
    a = ap.parse_args()
    src, dst = pathlib.Path(a.src), pathlib.Path(a.dst)
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    sp = json.loads(SPANS.read_text())
    dead = set()
    for f in a.drop:
        dead |= set(json.loads((REPO / ".ultramath/smwg224wy/m3" / f).read_text()))

    # 1. whole modules with no declaration in the closure
    mods = sorted({v["mod"] for v in sp.values()})
    drop_mods = ["OAI.Geometry.PlaneColoring.ConnectedUnitFree",
                 "OAI.Geometry.PlaneColoring.MeasurableAssembly",
                 "OAI.Geometry.PlaneColoring.MeasurableProper"]
    for m in drop_mods:
        p = dst / "lean" / (m.replace(".", "/") + ".lean")
        if p.exists():
            p.unlink()
            print("removed module", m)

    # 2. delete declaration spans (before touching imports, so SPANS line numbers hold)
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
            # absorb an attribute line that sits alone above the declaration
            while a >= 2 and ATTR.match(lines[a - 2]):
                a -= 1
            # absorb a docstring block that ends on the line above
            if a >= 2 and lines[a - 2].rstrip().endswith("-/"):
                j = a - 2
                while j >= 1 and "/-" not in lines[j - 1]:
                    j -= 1
                if j >= 1:
                    a = j
            # never eat the namespace-closing `end`s that follow the last declaration
            while b > a and b - 1 < len(lines) and ENDISH.match(lines[b - 1]):
                b -= 1
            kill.update(range(a, b + 1))
        kept = [ln for i, ln in enumerate(lines, 1) if i not in kill]
        p.write_text("\n".join(kept) + "\n")
        total += len(kill)
        print(f"{len(kill):5d} lines from {mod}")
    print(f"total lines removed from declaration spans: {total}")

    # 3. strip the imports of the removed modules from every remaining file
    gone = set(drop_mods)
    for p in sorted((dst / "lean" / "OAI").rglob("*.lean")):
        lines = p.read_text().splitlines()
        keep = [ln for ln in lines
                if not (ln.startswith("import ") and ln[len("import "):].strip() in gone)]
        if len(keep) != len(lines):
            p.write_text("\n".join(keep) + "\n")
            print(f"dropped {len(lines)-len(keep)} import line(s) in {p.name}")


main()
