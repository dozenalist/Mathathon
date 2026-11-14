#!/usr/bin/env python3
"""Axiom + statement certificate for the headline theorems.

  python3 certify.py --root DIR --env scripts/env4341.sh [--out FILE]

Writes a Lean file that (a) prints each headline type with `#check`,
(b) prints its axioms with `#print axioms`, (c) re-elaborates the frozen
statements from frozen.lean against the tree, and runs it with the tree's
oleans on LEAN_PATH.  Output is deterministic text suitable for diffing.
Exit 1 if the check file fails.
"""
import argparse, subprocess, sys, pathlib, os

HEAD = [
    "OAI.EuclideanFiveColor.no_proper_five_coloring",
    "OAI.EuclideanFiveColor.no_proper_five_coloring_algebraic",
    "OAI.Problem160.properColoring_seven",
    "OAI.EuclideanFiveColor.proper_iff_weak",
    "OAI.Problem160.chromaticNumber_bounds",
    "OAI.EuclideanFiveColor.not_proper_five_coloring_compl_null",
    "OAI.EuclideanFiveColor.algebraic_colorable_iff",
]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--env", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    h = pathlib.Path(__file__).resolve().parent
    build = root / "lean" / "build" / "lib"
    env = dict(os.environ)
    if a.env:
        out = subprocess.run(["bash", "-c",
                              f"source {a.env} >/dev/null 2>&1; printf 'LEAN_PATH=%s\\nPATH=%s\\n' \"$LEAN_PATH\" \"$PATH\""],
                             cwd=root, capture_output=True, text=True, check=True).stdout
        kv = dict(l.split("=", 1) for l in out.strip().splitlines() if "=" in l)
        env["LEAN_PATH"], env["PATH"] = kv.get("LEAN_PATH", ""), kv.get("PATH", env.get("PATH", ""))
    env["LEAN_PATH"] = f"{build}:{env.get('LEAN_PATH','')}"

    lines = ["import OAI.Geometry.PlaneColoring.Five", "import OAI.Geometry.PlaneColoring.Seven",
             "import OAI.Geometry.PlaneColoring.Transfer", "import OAI.Geometry.PlaneColoring.Chromatic",
             "import OAI.Geometry.PlaneColoring.NullSetRobust", "",
             "-- @@STATEMENTS"]
    for n in HEAD:
        lines += [f"set_option pp.universes true in #check @{n}",
                  f"#print axioms {n}", f"-- @@END {n}"]
    cert = h / ".certify_gen.lean"
    cert.write_text("\n".join(lines) + "\n")
    r = subprocess.run(["lean", str(cert)], cwd=root / "lean", env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=900)
    body = r.stdout
    # frozen-statement check
    r2 = subprocess.run(["lean", str(h / "frozen.lean")], cwd=root / "lean", env=env,
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=1800)
    report = ["== toolchain ==",
              subprocess.run(["lean", "--version"], cwd=root / "lean", env=env, capture_output=True, text=True).stdout.strip(),
              "", "== statements and axioms ==", body.strip(), "",
              "== frozen statement check ==", ("PASS" if r2.returncode == 0 else "FAIL"),
              ("" if r2.returncode == 0 else r2.stdout.strip()[:6000])]
    txt = "\n".join(report) + "\n"
    if a.out:
        pathlib.Path(a.out).write_text(txt)
    sys.stdout.write(txt)
    sys.exit(0 if (r.returncode == 0 and r2.returncode == 0) else 1)

main()
