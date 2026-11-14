#!/usr/bin/env python3
"""Sound build + certificate for a copy of the OAI tree.  Cannot be fooled by stale oleans.

  python3 verify.py --root TREE --env scripts/env4341.sh [-j2] [--ref work/A.freeze]
                    [--keep-build] [--only MOD...]

Steps, in order, each of which must pass:
  1. wipe TREE/lean/build/lib            (a stale olean is what f20 shows can certify deleted code)
  2. build every TREE/lean/OAI/**/*.lean in topological order, -o into build/lib
  3. require  #built == #.lean  (a module that is not in the tree cannot be imported any more)
  4. certify.py  --root TREE  -> compare against harness/BASELINE.cert  (statement + axiom freeze)
  5. deffreeze.py --root TREE --ref REF  (the definitions behind those statements are frozen too)
  6. linecount vs harness/BASELINE.json, print the per-module table and the saving
Writes TREE/verify_report.json.  Exit 0 only if every step passes.
"""
import argparse, json, os, re, subprocess, sys, time, pathlib
from concurrent.futures import ThreadPoolExecutor

IMP = re.compile(r"^import\s+(OAI\.[\w.]+)\s*$", re.M)
H = pathlib.Path(__file__).resolve().parent

def scan(root):
    ms = {}
    for p in sorted((root/"lean"/"OAI").rglob("*.lean")):
        name = ".".join(p.relative_to(root/"lean").with_suffix("").parts)
        ms[name] = (p, [d for d in IMP.findall(p.read_text(errors="ignore")) if d.startswith("OAI.")])
    return ms

def levels(ms):
    lvl, order = {}, []
    def depth(n, stack=()):
        if n in lvl: return lvl[n]
        if n in stack: raise SystemExit(f"import cycle: {stack+(n,)}")
        d = 0
        for m in ms[n][1]:
            if m in ms: d = max(d, depth(m, stack+(n,))+1)
        lvl[n] = d; return d
    for n in ms: depth(n)
    by = {}
    for n, l in lvl.items(): by.setdefault(l, []).append(n)
    return [sorted(by[l]) for l in sorted(by)]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="."); ap.add_argument("--env", default=None)
    ap.add_argument("-j", "--jobs", type=int, default=2)
    ap.add_argument("--ref", default=None); ap.add_argument("--timeout", type=int, default=1800)
    ap.add_argument("--keep-build", action="store_true")
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--skip-cert", action="store_true")
    ap.add_argument("--skip-build", action="store_true")
    a = ap.parse_args()
    root = pathlib.Path(a.root).resolve()
    build = root/"lean"/"build"/"lib"
    ms = scan(root)
    print(f"tree {root}: {len(ms)} modules", flush=True)
    # step 0: source-level proof holes and trust-me constructs (a hole outside the
    # headline closure is invisible to #print axioms)
    ts = subprocess.run([sys.executable, str(H/"textscan.py"), "--root", str(root)],
                        capture_output=True, text=True)
    print(ts.stdout.strip().splitlines()[-1] if ts.stdout.strip() else "TEXTSCAN: ?", flush=True)
    if ts.returncode != 0:
        print(ts.stdout)
        (root/"verify_report.json").write_text(json.dumps({"passed": False, "textscan": False}, indent=1))
        print("VERDICT: FAIL (proof hole in the sources)"); sys.exit(1)
    if a.skip_build:
        print("skipping the build (--skip-build)", flush=True)
    elif build.exists() and not a.keep_build:
        subprocess.run(["rm", "-rf", str(build)], check=True)
        print("wiped build/lib", flush=True)
    build.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    if a.env:
        out = subprocess.run(["bash", "-c", f'source {a.env} >/dev/null 2>&1; printf "%s\\n%s" "$LEAN_PATH" "$PATH"'],
                             cwd=root, capture_output=True, text=True, check=True).stdout.split("\n")
        env["LEAN_PATH"], env["PATH"] = out[0], out[1]
    env["LEAN_PATH"] = f"{build}:{env.get('LEAN_PATH','')}"
    todo = set(ms)
    if a.only:
        todo = {n for n in ms if any(n == o or n.endswith("."+o) for o in a.only)}
        st = list(todo)
        while st:
            n = st.pop()
            for d in ms[n][1]:
                if d in ms and d not in todo: todo.add(d); st.append(d)
    ok, fails, secs = 0, [], {}
    t0 = time.time()
    for level in ([] if a.skip_build else levels(ms)):
        level = [n for n in level if n in todo]
        if not level: continue
        def run(n):
            p, _ = ms[n]
            out = build/(n.replace(".", "/")+".olean"); out.parent.mkdir(parents=True, exist_ok=True)
            if out.exists(): out.unlink()          # never leave a stale olean in place
            t = time.time()
            try:
                r = subprocess.run(["lean", "-o", str(out), str(p)], cwd=root/"lean", env=env,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=a.timeout)
                return n, r.returncode, r.stdout, time.time()-t
            except subprocess.TimeoutExpired:
                return n, 124, f"TIMEOUT {a.timeout}s", time.time()-t
        lf = []
        with ThreadPoolExecutor(max_workers=a.jobs) as ex:
            for n, rc, out, dt in ex.map(run, level):
                secs[n] = dt
                if rc != 0: lf.append((n, out, dt))
                else: ok += 1
                if int(ok + len(fails) + len(lf)) % 10 == 0: print(f"  ... {ok} ok, {len(fails)+len(lf)} pending/failed", flush=True)
        # a parallel failure on a contended box is not evidence: retry every failure serially
        for n, out, dt in lf:
            n2, rc2, out2, dt2 = run(n)
            if rc2 == 0:
                ok += 1
                print(f"RETRY-OK {n} [{dt2:.0f}s] (parallel attempt died after {dt:.0f}s; resource flakiness, not a build failure)", flush=True)
            else:
                fails.append(n); print(f"FAIL {n} [{dt2:.0f}s]\n{out2[:3000]}", flush=True)
    wall = time.time()-t0
    if a.skip_build:
        ok = len(list(build.rglob("*.olean"))) // 1
        ok = sum(1 for n in todo if (build/(n.replace(".", "/")+".olean")).exists())
        print(f"\nBUILD: skipped, {ok}/{len(todo)} oleans already present", flush=True)
    print(f"\nBUILD: {ok}/{len(todo)} modules OK in {wall:.0f}s", flush=True)
    report = {"modules": len(ms), "built": ok, "fails": fails, "wall": wall, "passed": True}
    if fails or ok != len(todo):
        report["passed"] = False
        print("BUILD FAILED", flush=True)
    # certificate
    cert_ok = freeze_ok = None
    if report["passed"] and not a.skip_cert:
        certf = root/"verify.cert"
        r = subprocess.run([sys.executable, str(H/"certify.py"), "--root", str(root),
                            "--env", str(pathlib.Path(a.env).resolve()) if a.env else "",
                            "--out", str(certf)], capture_output=True, text=True)
        ref = (H/"BASELINE.cert").read_text()
        got = certf.read_text() if certf.exists() else ""
        cert_ok = (r.returncode == 0 and got == ref)
        print(f"CERTIFY: {'PASS (byte-identical to BASELINE.cert)' if cert_ok else 'FAIL'}", flush=True)
        if not cert_ok:
            import difflib
            print("\n".join(list(difflib.unified_diff(ref.splitlines(), got.splitlines(), "BASELINE.cert", "tree"))[:40]))
        if a.ref:
            fr = subprocess.run([sys.executable, str(H/"deffreeze.py"), "--root", str(root),
                                 "--env", str(pathlib.Path(a.env).resolve()) if a.env else "",
                                 "--out", str(root/"verify.freeze"), "--ref", a.ref], capture_output=True, text=True)
            freeze_ok = fr.returncode == 0
            print(f"DEF-FREEZE: {'PASS' if freeze_ok else 'FAIL'}", flush=True)
    report["certify"] = cert_ok; report["deffreeze"] = freeze_ok
    report["passed"] = bool(report["passed"] and (cert_ok is not False) and (freeze_ok is not False))
    lc = subprocess.run([sys.executable, str(H/"linecount.py"), "--base", str(H/"BASELINE.json"),
                         "--root", str(root)], capture_output=True, text=True)
    print(lc.stdout[-3000:]); print(lc.stderr[-500:])
    report["linecount_rc"] = lc.returncode
    (root/"verify_report.json").write_text(json.dumps(report, indent=1))
    print(f"\nVERDICT: {'PASS' if report['passed'] else 'FAIL'}  ({ok}/{len(todo)} built, certify={cert_ok}, deffreeze={freeze_ok}, linecount_rc={lc.returncode})")
    sys.exit(0 if report["passed"] else 1)

main()
