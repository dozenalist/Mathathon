#!/usr/bin/env python3
"""Compile-driven consistency fixed point for the diagnostic prune.

m10's `analyze.py free` walks the closure of the 7 headlines; a declaration whose
*definition* is not needed by them can still be *named* by a surviving declaration,
and then deleting it breaks the build.  This script iterates:

  rebuild tree  ->  compile the changed modules  ->  collect `Unknown identifier X`
  ->  add X (and any freed name with that short name) to the keep list

until a round compiles cleanly.  Prints, each round, the number of declarations
that had to be kept because a survivor still names them.
"""
import json, pathlib, re, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent
REPO = (ROOT / "../../..").resolve()
H = REPO / "sprint/simplify/m10/harness"
sys.path.insert(0, str(H))
_argv, sys.argv = sys.argv, ["analyze.py", "stats"]
from analyze import load, closure, ROOTS, spans          # noqa: E402
sys.argv = _argv

TARGET = "OAI.PlaneFiveColor.Spectral.ergodic_wild_fourier"
BASE_KEEP = ["OAI.PlaneFiveColor.Spectral.fourier_vanish_of_terminal",
             "OAI.Analysis.PlaneSpectrum.relative_difference_invariant",
             "OAI.PlaneFiveColor.Spectral.j_injective",
             "OAI.PlaneFiveColor.Spectral.scalarHom"]

nodes, et, ev = load()
sp = spans()
full_cl = closure(nodes, et, ev)
short2full = {}
for n in full_cl:
    short2full.setdefault(n.split(".")[-1], set()).add(n)

CHANGED = [l.strip().strip('"') for l in (ROOT / "build_changed.sh").read_text().splitlines()
           if l.strip('"').startswith("OAI/")]

def write_prune(keep):
    drop = {TARGET} - set(keep)
    red = closure(nodes, et, ev, drop_v=drop, roots=ROOTS + sorted(keep))
    freed = full_cl - red
    pr = {"drop_decls": {}, "drop_modules": [], "drop_imports": {}}
    for n in sorted(freed):
        if n in sp:
            pr["drop_decls"][n] = sp[n]
    (ROOT / "PRUNE8.json").write_text(json.dumps(pr, indent=1))
    return sum(v["lines"] for v in pr["drop_decls"].values()), len(pr["drop_decls"]), freed

def rebuild():
    subprocess.run(["rm", "-rf", "tree"], cwd=ROOT, check=True)
    subprocess.run(["cp", "-r", "tree-pristine", "tree"], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(H / "apply_prune.py"), "--tree", "tree",
                    "--prune", "PRUNE8.json"], cwd=ROOT, check=True, capture_output=True)
    M = REPO / ".ultramath/smwfoekgk/m5/work"
    T = ROOT / "tree/lean/OAI/Analysis/PlaneSpectrum"
    shutil.copy(M / "A.lean", T / "RSBase.lean")
    shutil.copy(M / "B.lean", T / "RSMeasure.lean")
    b = (T / "RSMeasure.lean").read_text().replace("import A\n", "import OAI.Analysis.PlaneSpectrum.RSBase\n", 1)
    (T / "RSMeasure.lean").write_text(b)
    hdr = ("import OAI.Analysis.PlaneSpectrum.RSBase\nimport OAI.Analysis.PlaneSpectrum.RSMeasure\n"
           "import OAI.Analysis.PlaneSpectrum.RadialEnergy\nimport OAI.Analysis.PlaneSpectrum.DifferenceLaw\n"
           "import OAI.MeasureTheory.CompactFactors.DifferenceInvariant\n"
           "import OAI.Analysis.PlaneSpectrum.SpectralMeasure\n")
    (T / "TheoremA.lean").write_text(hdr + "\n".join((M / "C.lean").read_text().splitlines()[2:]) + "\n")
    subprocess.run([sys.executable, "patch_ergodicity.py"], cwd=ROOT, check=True, capture_output=True)
    subprocess.run([sys.executable, "fix_omit.py"], cwd=ROOT, check=True, capture_output=True)
    # put the already-built staged oleans next to the sources: unchanged modules are
    # then found by the compiler, and only the changed ones are re-elaborated
    stage = REPO / "sprint/simplify/stage/lean/build/lib"
    for o in stage.rglob("*.olean"):
        dst = ROOT / "tree/lean" / o.relative_to(stage)
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(o, dst)
    for o in stage.rglob("*.ilean"):
        dst = ROOT / "tree/lean" / o.relative_to(stage)
        if dst.parent.exists(): shutil.copy(o, dst)

def compile_round():
    env = dict(__import__("os").environ)
    stage = REPO / "sprint/simplify/stage/lean/build/lib"
    env["LEAN_PATH"] = f"{ROOT}/tree/lean:{stage}:{env[chr(39)+chr(39)]}" if False else f"{ROOT}/tree/lean:{stage}:" + env["LEAN_PATH"]
    bad, failed = {}, []
    for m in CHANGED:
        src = f"{m}.lean"
        out = f"{m}.olean"
        p = subprocess.run(["lean", "-o", out, src], cwd=ROOT / "tree/lean", env=env,
                           capture_output=True, text=True, timeout=900)
        err = p.stdout + p.stderr
        if p.returncode != 0:
            for mm in re.finditer(r"Unknown identifier `([^`]+)`", err):
                bad.setdefault(mm.group(1), set()).add(m)
            for mm in re.finditer(r"unknown namespace `([^`]+)`", err):
                bad.setdefault(mm.group(1), set()).add(m)
            for mm in re.finditer(r"object file '.*?/(OAI/[^']+)\.olean' of module .* does not exist", err):
                bad.setdefault("MISSING:" + mm.group(1), set()).add(m)
            failed.append(m)
            (ROOT / f"err_{m.split('/')[-1]}.log").write_text(err)
        else:
            print(f"  ok   {m}")
    print("  compiled ok:", len(CHANGED) - len(failed), "/", len(CHANGED),
          "| failing:", ", ".join(x.split("/")[-1] for x in failed))
    return bad, failed

def keep_set(k):
    return set(k)

keep = list(BASE_KEEP)
for rnd in range(1, 13):
    lines, cnt, freed = write_prune(keep)
    rebuild()
    tot = sum(len(p.read_text().splitlines()) for p in (ROOT / "tree").rglob("*.lean"))
    print(f"round {rnd}: {cnt} decls / {lines} span-lines dropped; tree now {tot} lines")
    bad, failed = compile_round()
    bad = {k: v for k, v in bad.items() if not k.startswith("MISSING:")}
    if not failed:
        print(f"CLEAN after {rnd} round(s): {cnt} declarations, {lines} lines")
        break
    added = 0
    for sh, mods in bad.items():
        cands = short2full.get(sh, set())
        if not cands and "." not in sh:
            # an unknown *namespace*: keep everything freed underneath it
            cands = {n for n in full_cl - keep_set(keep) if f".{sh}." in n}
            print(f"  resolved namespace {sh} -> {len(cands)} decls")
        if not cands:
            print("  cannot resolve", sh)
            continue
        for n in cands:
            if n not in keep:
                keep.append(n); added += 1
    print(f"  unknown identifiers: {sorted(bad)}  -> kept {added} more decl(s)")
    if not added:
        print("no progress"); break
print("KEEP =", json.dumps(keep, indent=1))
