#!/usr/bin/env python3
"""Parallel topological builder for a copy of the OAI Lean development.

  python3 hbuild.py --root DIR --env scripts/env4341.sh [-j2] [--fresh] [--only MOD ...]

Builds DIR/lean/OAI/**/*.lean into DIR/lean/build/lib.  LEAN_PATH is
DIR/lean/build/lib : <LEAN_PATH obtained by sourcing --env>.  With --fresh the
build dir is wiped first.  Prints one line per module and a timing summary.
Exit code 1 iff some module failed.
"""
import argparse, os, re, subprocess, sys, time, json, pathlib
from concurrent.futures import ThreadPoolExecutor

IMP = re.compile(r"^import\s+([\w.]+)\s*$", re.M)

def scan(root):
    root = pathlib.Path(root)
    ms = {}
    for p in sorted((root / "lean" / "OAI").rglob("*.lean")):
        name = ".".join(p.relative_to(root / "lean").with_suffix("").parts)
        deps = [d for d in IMP.findall(p.read_text(errors="ignore")) if d.startswith("OAI.")]
        ms[name] = (p, deps)
    return ms

def topo_levels(ms):
    lvl, order = {}, []
    def depth(n, stack=()):
        if n in lvl: return lvl[n]
        if n in stack: raise SystemExit(f"import cycle: {stack + (n,)}")
        d = 0
        for m in ms[n][1]:
            if m in ms: d = max(d, depth(m, stack + (n,)) + 1)
        lvl[n] = d; return d
    for n in ms: depth(n)
    by = {}
    for n, l in lvl.items(): by.setdefault(l, []).append(n)
    return [sorted(by[l]) for l in sorted(by)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--env", default=None, help="bash script to source for LEAN_PATH")
    ap.add_argument("-j", "--jobs", type=int, default=2)
    ap.add_argument("--fresh", action="store_true")
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--seed", default=None,
                    help="donor build/lib: copy its oleans in first so only the changed cone rebuilds")
    ap.add_argument("--no-resume", action="store_true",
                    help="rebuild modules whose olean is already newer than source+deps")
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    build = root / "lean" / "build" / "lib"
    if a.fresh and build.exists():
        subprocess.run(["rm", "-rf", str(build)], check=True)
    build.mkdir(parents=True, exist_ok=True)

    env = dict(os.environ)
    if a.env:
        out = subprocess.run(["bash", "-c",
                              f"source {a.env} >/dev/null 2>&1; "
                              f"printf 'LEAN_PATH=%s\\nPATH=%s\\n' \"$LEAN_PATH\" \"$PATH\""],
                             cwd=root, capture_output=True, text=True, check=True).stdout
        kv = dict(ln.split("=", 1) for ln in out.strip().splitlines() if "=" in ln)
        env["LEAN_PATH"] = kv.get("LEAN_PATH", "")
        env["PATH"] = kv.get("PATH", env.get("PATH", ""))
    env["LEAN_PATH"] = f"{build}:{env.get('LEAN_PATH','')}"

    if a.seed:
        donor = pathlib.Path(a.seed).resolve()
        n = 0
        for o in donor.rglob("*.olean"):
            dst = build / o.relative_to(donor)
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                subprocess.run(["cp", "-a", str(o), str(dst)], check=True); n += 1
        print(f"seeded {n} oleans from {donor}", flush=True)

    ms = scan(root)
    levels = topo_levels(ms)
    todo = set(ms)
    if a.only:
        todo = {n for n in ms if any(n == o or n.startswith(o + ".") or n.endswith("." + o) for o in a.only)}
        # close under deps
        st = list(todo)
        while st:
            n = st.pop()
            for d in ms[n][1]:
                if d in ms and d not in todo: todo.add(d); st.append(d)

    fails, secs, t0 = [], {}, time.time()
    for li, level in enumerate(levels):
        level = [n for n in level if n in todo]
        if not level: continue
        def olean(n):
            return build / (n.replace(".", "/") + ".olean")
        def uptodate(n):
            o = olean(n)
            if not o.exists(): return False
            t = o.stat().st_mtime
            if t < ms[n][0].stat().st_mtime: return False
            return all(not olean(d).exists() or olean(d).stat().st_mtime <= t for d in ms[n][1] if d in ms)
        def run(n):
            p, _ = ms[n]
            if not a.no_resume and uptodate(n):
                return n, 0, "", 0.0
            out = olean(n)
            out.parent.mkdir(parents=True, exist_ok=True)
            t = time.time()
            try:
                r = subprocess.run(["lean", "-o", str(out), str(p)], cwd=root / "lean", env=env,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                                   timeout=a.timeout)
                return n, r.returncode, r.stdout, time.time() - t
            except subprocess.TimeoutExpired:
                return n, 124, f"TIMEOUT after {a.timeout}s (machine contention)", time.time() - t
        with ThreadPoolExecutor(max_workers=a.jobs) as ex:
            for n, rc, out, dt in ex.map(run, level):
                secs[n] = dt
                if rc != 0:
                    fails.append(n); print(f"FAIL {n} [{dt:.1f}s]", flush=True)
                    print(out[:4000], flush=True)
                else:
                    print(f"OK   {n} [{dt:.1f}s]", flush=True)
    tt = time.time() - t0
    print(f"\n{len(todo)-len(fails)}/{len(todo)} modules OK in {tt:.0f}s (j={a.jobs}); "
          f"sum of module times {sum(secs.values()):.0f}s")
    if fails:
        print("FAILED: " + ", ".join(fails))
        json.dump({"fails": fails, "secs": secs, "wall": tt}, open(root / "build_report.json", "w"), indent=1)
        sys.exit(1)
    json.dump({"fails": [], "secs": secs, "wall": tt}, open(root / "build_report.json", "w"), indent=1)

main()
