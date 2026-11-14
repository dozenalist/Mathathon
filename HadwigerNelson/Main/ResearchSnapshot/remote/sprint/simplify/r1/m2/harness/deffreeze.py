#!/usr/bin/env python3
"""Definition freeze: pin the *meaning* of the constants that occur in the headline types.

  python3 deffreeze.py --root TREE --env ENV --out FILE [--ref FILE]

certify.py pins the 7 headline *types* (via `#check`) and re-elaborates them from
frozen.lean.  That is not enough: the headline types are built from a handful of
OAI definitions (`ProperColoring`, `WeakColoring`, `LabelModel.Proper`, `E`,
`planeChromaticNumber`), and none of them is pinned.  A tree that redefines
`planeChromaticNumber := 6` (or `LabelModel.Proper := ProperColoring`, or `E := C`)
prints exactly the same `#check` lines, keeps clean axioms, satisfies frozen.lean,
and is mathematically vacuous.

This tool prints the *type-closure* of the 7 headline types, selected down to the
definitional constants (def/abbrev/structure/class/inductive/instance), with `#print`,
and compares that text against a reference capture (default: the same tree, so pass
--ref for a real audit).  Any change in a definition that a headline statement
mentions changes this text.
"""
import argparse, json, pathlib, subprocess, sys, collections

HEAD = ["OAI.EuclideanFiveColor.no_proper_five_coloring",
        "OAI.EuclideanFiveColor.no_proper_five_coloring_algebraic",
        "OAI.Problem160.properColoring_seven",
        "OAI.EuclideanFiveColor.proper_iff_weak",
        "OAI.Problem160.chromaticNumber_bounds",
        "OAI.EuclideanFiveColor.not_proper_five_coloring_compl_null",
        "OAI.EuclideanFiveColor.algebraic_colorable_iff"]
DEFKINDS = {"def", "abbrev", "structure", "class", "inductive", "instance", "opaque"}
IMPORTS = ["OAI.Geometry.PlaneColoring.Five", "OAI.Geometry.PlaneColoring.Seven",
           "OAI.Geometry.PlaneColoring.Transfer", "OAI.Geometry.PlaneColoring.Chromatic",
           "OAI.Geometry.PlaneColoring.NullSetRobust"]

def frozen(h):
    et = collections.defaultdict(set)
    for ln in pathlib.Path(h / "DECLGRAPH.log").read_text().splitlines():
        if ln.startswith("EDGET "):
            _, a, b = ln.split(" ", 2); et[a].add(b)
    seen, stack = set(), list(HEAD)
    while stack:
        n = stack.pop()
        if n in seen: continue
        seen.add(n); stack.extend(et.get(n, ()))
    sp = json.loads(pathlib.Path(h / "SPANS.json").read_text())
    # constructors/fields of a structure are not in SPANS; freeze the structure itself.
    return sorted(n for n in seen if n in sp and sp[n]["kind"] in DEFKINDS)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="."); ap.add_argument("--env", default=None)
    ap.add_argument("--out", default=None); ap.add_argument("--ref", default=None)
    ap.add_argument("--harness", default=str(pathlib.Path(__file__).resolve().parent))
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve(); h = pathlib.Path(a.harness)
    build = root / "lean" / "build" / "lib"
    env = dict(**__import__("os").environ)
    if a.env:
        o = subprocess.run(["bash", "-c", f'source {a.env} >/dev/null 2>&1; printf "%s\\n%s" "$LEAN_PATH" "$PATH"'],
                           cwd=root, capture_output=True, text=True, check=True).stdout.split("\n")
        env["LEAN_PATH"], env["PATH"] = o[0], o[1]
    env["LEAN_PATH"] = f"{build}:{env.get('LEAN_PATH','')}"
    names = frozen(h)
    lines = [f"import {m}" for m in IMPORTS] + ["set_option pp.universes true", "set_option pp.proofs false", ""]
    for n in names:
        lines += [f"-- @@DEF {n}", f"#print {n}"]
    src = h / ".deffreeze_gen.lean"; src.write_text("\n".join(lines) + "\n")
    r = subprocess.run(["lean", str(src)], cwd=root / "lean", env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=1800)
    txt = r.stdout
    pathlib.Path(a.out).write_text(txt) if a.out else sys.stdout.write(txt)
    print(f"froze {len(names)} definitions; lean rc={r.returncode}", file=sys.stderr)
    if a.ref:
        ref = pathlib.Path(a.ref).read_text()
        if ref != txt:
            import difflib
            d = list(difflib.unified_diff(ref.splitlines(), txt.splitlines(), "reference", "candidate", n=1, lineterm=""))
            sys.stderr.write("\n".join(d[:120]) + "\n")
            print("DEF-FREEZE: FAIL (definitions behind the headline statements changed)", file=sys.stderr)
            sys.exit(1)
        print("DEF-FREEZE: PASS", file=sys.stderr)
    sys.exit(0 if r.returncode == 0 else 1)

main()
