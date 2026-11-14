#!/usr/bin/env python3
"""Apply a dead-declaration set (column-0 structural lines only are preserved) and
repair against the compiler, re-adding exactly the declarations it complains about.

  python3 cutfix.py --pristine DIR --dst DIR --dead JSON --staged DIR --env ENV.sh
"""
import json, re, sys, os, argparse, pathlib, shutil, collections, subprocess

END0 = re.compile(r"^end(\s|$)")
STRUCT0 = re.compile(r"^(variable|open|section|omit|attribute|set_option|universe|local\b|private\b|scoped\b|noncomputable\b|include\b|namespace\b)\b")
DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+|partial\s+|unsafe\s+|scoped\s+)*(theorem|lemma|def|abbrev|structure|class|instance|inductive|opaque)\s+([^\s:{(​\[]+)")
NS = re.compile(r"^namespace\s+([\w.]+)\s*$")
SEC = re.compile(r"^(?:noncomputable\s+|private\s+|protected\s+|public\s+)?section(?:\s+[\w.]+)?\s*$")
MUT = re.compile(r"^mutual\s*$")
END = re.compile(r"^end(?:\s+([\w.]+))?\s*$")
UNK = re.compile(r"Unknown identifier `([^`]+)`")

def spans(lines):
    stack, found = [], []
    for i, ln in enumerate(lines, 1):
        m = NS.match(ln)
        if m: stack.append(m.group(1)); continue
        if SEC.match(ln) or MUT.match(ln): stack.append(""); continue
        eo = END.match(ln)
        if eo:
            nm = eo.group(1)
            if nm and nm in stack:
                while stack and stack.pop() != nm: pass
            elif stack: stack.pop()
            continue
        d = DECL.match(ln)
        if d and d.group(2) not in ("where", "at", "at'"):
            out_name = d.group(2)
            found.append((out_name, i))
    return [(n, i, (found[j+1][1]-1) if j+1 < len(found) else len(lines))
            for j, (n, i) in enumerate(found)]

STOP0 = re.compile(r"^(end(\s|$)|variable\b|open\b|section\b|omit\b|attribute\b|set_option\b|universe\b|local\b|private\b|protected\b|scoped\b|noncomputable\b|include\b|namespace\b|/--|--|@\[|mutual\b)")
def region(lines, start, end):
    """Delete from `start` up to the first later column-0 line that starts a new
    declaration or a structural command; never touch such a line."""
    k = start + 1
    while k <= len(lines):
        ln = lines[k-1]
        if k > start and ln[:1] not in (' ', '\t') and (STOP0.match(ln) or DECL.match(ln)):
            break
        k += 1
    j = k - 1
    while j > start and lines[j-1].strip() == '': j -= 1
    return max(j, start)

def materialise(pris, drop):
    lines = pris.splitlines()
    for n, s, e in sorted(spans(lines), key=lambda t: -t[1]):
        if n in drop:
            lines[s-1:region(lines, s, min(e, len(lines)))] = []
    return "\n".join(lines) + "\n"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pristine", required=True); ap.add_argument("--dst", required=True)
    ap.add_argument("--dead", required=True); ap.add_argument("--staged", required=True)
    ap.add_argument("--env", required=True); ap.add_argument("--rounds", type=int, default=8)
    a = ap.parse_args()
    pri = pathlib.Path(a.pristine).resolve() / "lean"
    dst = pathlib.Path(a.dst).resolve() / "lean"
    if (pathlib.Path(a.dst)).exists(): shutil.rmtree(a.dst)
    shutil.copytree(pri, dst)
    for f in ("CheckBoth.lean", "CheckStage.lean"):
        s = pathlib.Path(a.staged).resolve() / "lean" / f
        if s.exists(): shutil.copy(s, dst / f)
    seed = pathlib.Path(a.staged).resolve() / "lean" / "build"
    if seed.exists():
        shutil.copytree(seed, dst / "build")
    dead = json.load(open(a.dead))
    bymod = collections.defaultdict(set)
    for d in dead: bymod[d["mod"]].add(d["name"])
    build = dst / "build" / "lib"
    build.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    o = subprocess.run(["bash", "-c",
        f"source {a.env} >/dev/null 2>&1; printf '%s\\n' \"$LEAN_PATH\"; printf '%s\\n' \"$PATH\""],
        capture_output=True, text=True, check=True).stdout.splitlines()
    env["LEAN_PATH"] = f"{build}:{o[0]}"; env["PATH"] = o[1]
    reverted = []
    for mod, drop in sorted(bymod.items()):
        p = dst / "OAI" / (mod.replace(".", "/") + ".lean")
        pris = p.read_text(errors="ignore")
        olean = build / (mod.replace(".", "/") + ".olean")
        olean.parent.mkdir(parents=True, exist_ok=True)
        for rnd in range(a.rounds + 1):
            p.write_text(materialise(pris, drop))
            r = subprocess.run(["lean", "-o", str(olean), str(p)], cwd=dst, env=env,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            if r.returncode == 0:
                print(f"OK   {mod} (dropped {len(drop)})", flush=True); break
            missing = {m.group(1).split(".")[-1] for m in UNK.finditer(r.stdout)}
            add = missing & drop
            if not add:
                print(f"REVERT {mod}: {[l for l in r.stdout.splitlines() if 'error' in l][:2]}", flush=True)
                p.write_text(pris); reverted.append(mod)
                subprocess.run(["lean", "-o", str(olean), str(p)], cwd=dst, env=env,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                break
            drop -= add
            print(f"  readd {sorted(add)} in {mod}", flush=True)
        else:
            p.write_text(pris); reverted.append(mod)
            print(f"REVERT {mod}: rounds exhausted", flush=True)
    n = sum(1 for f in (dst / "OAI").rglob("*.lean") for _ in open(f, errors="ignore"))
    print(f"\ntree now {n} raw lines; reverted {len(reverted)}: {reverted}")

main()
