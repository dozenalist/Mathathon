#!/usr/bin/env python3
"""Parallel, resumable builder for an OAI tree, parameterised by root.

`scripts/build_lean.py` is hard-wired to repo/lean and writes into repo/scripts/,
which this session must not touch.  Same idea, but the tree and the olean
directory are arguments, so a ported or trimmed copy can be built in place.

Usage: python3 build.py TREE [--jobs N] [--only PREFIX] [--log FILE]
Oleans go to TREE/build/lib and are prepended to LEAN_PATH.
"""
import json
import os
import pathlib
import re
import subprocess
import sys
import threading
import time

def main(argv):
    tree = pathlib.Path(argv[0]).resolve()
    jobs = int(argv[argv.index("--jobs") + 1]) if "--jobs" in argv else 2
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
    logp = pathlib.Path(argv[argv.index("--log") + 1]) if "--log" in argv else tree / "build_status.json"
    build = tree / "build" / "lib"

    mods = {}
    for p in sorted(tree.glob("OAI/**/*.lean")):
        name = ".".join(p.relative_to(tree).with_suffix("").parts)
        deps = []
        for line in p.read_text(errors="ignore").splitlines():
            m = re.match(r"^import\s+(OAI\.[\w.]+)\s*$", line)
            if m:
                deps.append(m.group(1))
        mods[name] = (p, deps)
    mods = {n: (p, [d for d in d if d in mods]) for n, (p, d) in mods.items()}

    # topological order
    order, state = [], {}
    def visit(n, stack=()):
        if state.get(n) == 2:
            return
        if state.get(n) == 1:
            sys.exit(f"cycle at {n}: {stack}")
        state[n] = 1
        for d in mods[n][1]:
            visit(d, stack + (n,))
        state[n] = 2
        order.append(n)
    for n in mods:
        visit(n)
    if only:
        order = [n for n in order if any(n == a or n.startswith(a + ".") or n.endswith("." + a) for a in only)]

    env = dict(os.environ)
    env["LEAN_PATH"] = f"{build}:" + env.get("LEAN_PATH", "")
    status = json.loads(logp.read_text()) if logp.exists() else {}
    status = {n: s for n, s in status.items() if n in mods}
    done, failed = set(), {}
    lock = threading.Lock()
    todo = list(order)

    def worker():
        while True:
            with lock:
                if not todo:
                    return
                n = next((m for m in todo if all(d in done or d not in mods for d in mods[m][1])), None)
                if n is None:
                    n = todo[0] if all(mods[m][1] and any(d in failed for d in mods[m][1]) for m in todo) else None
                    if n is None:
                        time.sleep(0.2)
                        continue
                todo.remove(n)
            p, deps = mods[n]
            if any(d in failed for d in deps):
                with lock:
                    failed[n] = "dep failed"
                    print(f"SKIP {n}", flush=True)
                continue
            out = build / (n.replace(".", "/") + ".olean")
            out.parent.mkdir(parents=True, exist_ok=True)
            if out.exists() and out.stat().st_mtime > p.stat().st_mtime and status.get(n, {}).get("ok"):
                with lock:
                    done.add(n)
                    print(f"OK   {n} (cached)", flush=True)
                continue
            t0 = time.time()
            r = subprocess.run(["lean", "-o", str(out), str(p)], cwd=tree, env=env,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            dt = time.time() - t0
            with lock:
                if r.returncode == 0:
                    done.add(n)
                    status[n] = {"ok": True, "secs": round(dt, 1)}
                    print(f"OK   {n} [{dt:.0f}s]", flush=True)
                else:
                    failed[n] = (r.stdout or "")[:3000]
                    status[n] = {"ok": False, "err": failed[n][:3000], "secs": round(dt, 1)}
                    print(f"FAIL {n} [{dt:.0f}s]\n{failed[n][:2000]}", flush=True)
                logp.write_text(json.dumps(status, indent=0))

    ts = [threading.Thread(target=worker) for _ in range(jobs)]
    [t.start() for t in ts]
    [t.join() for t in ts]
    print(f"done: {len(done)}/{len(order)} ok, {len(failed)} failed", flush=True)
    if failed:
        print("failed: " + ", ".join(sorted(failed)), flush=True)
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
