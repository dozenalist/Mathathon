#!/usr/bin/env python3
"""Sequential topological build with automatic revert to the pristine module.

For each module, in dependency order: compile it; if it fails, restore the pristine
(uncut) source from --pristine and compile again.  Cascades cannot happen because
we never leave a module unbuilt.  Reports the modules that had to be reverted.

  python3 buildseq.py --cut DIR --pristine DIR --env ENV.sh [--jobs 2]
"""
import argparse, os, re, subprocess, sys, pathlib, time, json
from concurrent.futures import ThreadPoolExecutor

IMP = re.compile(r"^import\s+([\w.]+)\s*$", re.M)

def scan(root):
    root = pathlib.Path(root) / "lean"
    ms = {}
    for p in sorted((root / "OAI").rglob("*.lean")):
        name = ".".join(p.relative_to(root).with_suffix("").parts)
        ms[name] = (p, [d for d in IMP.findall(p.read_text(errors="ignore")) if d.startswith("OAI.")])
    # a module that was deleted is simply absent
    for name, (p, ds) in list(ms.items()):
        ms[name] = (p, [d for d in ds if d in ms])
    return ms

def levels(ms):
    lvl = {}
    def depth(n, stack=()):
        if n in lvl: return lvl[n]
        d = 0
        for m in ms[n][1]:
            if m in ms: d = max(d, depth(m, stack + (n,)) + 1)
        lvl[n] = d; return d
    for n in ms: depth(n)
    out = {}
    for n, l in lvl.items(): out.setdefault(l, []).append(n)
    return [sorted(out[l]) for l in sorted(out)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cut", required=True)
    ap.add_argument("--pristine", required=True)
    ap.add_argument("--env", required=True)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--report", default=None)
    a = ap.parse_args()
    cut, pri = pathlib.Path(a.cut).resolve(), pathlib.Path(a.pristine).resolve()
    build = cut / "lean" / "build" / "lib"
    build.mkdir(parents=True, exist_ok=True)
    out = subprocess.run(["bash", "-c",
        f"source {a.env} >/dev/null 2>&1; printf '%s\\n' \"$LEAN_PATH\"; printf '%s\\n' \"$PATH\""],
        capture_output=True, text=True, check=True).stdout.splitlines()
    env = dict(os.environ)
    env["LEAN_PATH"] = f"{build}:{out[0]}"
    env["PATH"] = out[1]
    ms = scan(cut)
    lv = levels(ms)
    reverted, fails = [], []
    for level in lv:
        work = [n for n in level if n in ms]
        # modules whose deps are all present must build; retry after correcting deps
        pending = list(work)
        while pending:
            def run(n):
                p, _ = ms[n]
                o = build / (n.replace(".", "/") + ".olean")
                o.parent.mkdir(parents=True, exist_ok=True)
                r = subprocess.run(["lean", "-o", str(o), str(p)], cwd=cut / "lean",
                                   env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
                return n, r.returncode, r.stdout
            with ThreadPoolExecutor(max_workers=1) as ex:
                n, rc, log = ex.submit(run, pending[0]).result()
            if rc == 0:
                pending.pop(0); print(f"OK   {n}", flush=True); continue
            q = pri / "lean" / (n.replace(".", "/") + ".lean")
            if not q.exists():
                print(f"HARD FAIL (no pristine) {n}\n{log[:1500]}", flush=True); fails.append(n); pending.pop(0); continue
            tgt = cut / "lean" / (n.replace(".", "/") + ".lean")
            print(f"REVERT {n} (cut version fails)", flush=True)
            reverted.append(n)
            tgt.write_text(q.read_text())
            # loop retries the same module with the pristine source
    n = sum(1 for f in (cut / "lean" / "OAI").rglob("*.lean") for _ in open(f, errors="ignore"))
    print(f"\nreverted {len(reverted)} modules; final tree {n} raw lines over "
          f"{len(list((cut / 'lean' / 'OAI').rglob('*.lean')))} modules")
    if a.report: json.dump({"reverted": reverted, "fails": fails, "lines": n}, open(a.report, "w"), indent=1)

main()
