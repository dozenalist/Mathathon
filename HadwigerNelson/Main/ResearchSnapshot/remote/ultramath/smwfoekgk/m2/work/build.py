#!/usr/bin/env python3
"""Topological builder: lean -o into <builddir>/lib.

Usage: python3 build.py <srcroot> <builddir> [--jobs N] [--only M1,M2] [--keep-going]

LEAN_PATH from the environment, with <builddir>/lib prepended.  Modules in --only are
built in dependency order; their other dependencies resolve from the rest of LEAN_PATH
(usually the baseline olean tree).  Writes <builddir>/status.json.
"""
import json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

src = os.path.abspath(sys.argv[1]); build = os.path.abspath(sys.argv[2])
jobs, keep_going, only = 2, False, None
args = sys.argv[3:]; i = 0
while i < len(args):
    if args[i] == '--jobs': jobs = int(args[i+1]); i += 2
    elif args[i] == '--only': only = set(args[i+1].split(',')); i += 2
    elif args[i] == '--keep-going': keep_going = True; i += 1
    else: raise SystemExit('bad arg ' + args[i])

lib = os.path.join(build, 'lib'); os.makedirs(lib, exist_ok=True)
mods, deps = {}, {}
for dp, dn, fn in os.walk(src):
    for f in sorted(fn):
        if not f.endswith('.lean'): continue
        p = os.path.join(dp, f); rel = os.path.relpath(p, src)
        if not rel.startswith('OAI/'): continue
        m = rel[:-5].replace('/', '.'); mods[m] = p; d = []
        for line in open(p, errors='ignore'):
            mm = re.match(r'^import\s+(OAI\.[\w.]+)', line.strip())
            if mm: d.append(mm.group(1))
        deps[m] = d

order, state = [], {}
def visit(n):
    if state.get(n) == 2: return
    if state.get(n) == 1: raise SystemExit('cycle at ' + n)
    state[n] = 1
    for x in deps[n]:
        if x in mods: visit(x)
    state[n] = 2; order.append(n)
for n in sorted(mods): visit(n)

if only:
    missing = only - set(mods)
    if missing: raise SystemExit('unknown modules: %s' % sorted(missing))
target = [m for m in order if only is None or m in only]
tset = set(target)
env = dict(os.environ, LEAN_PATH=lib + ':' + os.environ.get('LEAN_PATH',''))
status, fail = {}, []

def work(m):
    out = os.path.join(lib, m.replace('.', '/') + '.olean')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    if os.path.exists(out):
        t_out = os.path.getmtime(out)
        if t_out > os.path.getmtime(mods[m]):
            fresh = True
            for x in deps[m]:
                xo = os.path.join(lib, x.replace('.', '/') + '.olean')
                if os.path.exists(xo) and os.path.getmtime(xo) > t_out:
                    fresh = False
                    break
            if fresh:
                return True, 0.0, ''
    t = time.time()
    r = subprocess.run(['lean', '-o', out, mods[m]], capture_output=True, text=True, env=env, cwd=src)
    dt = time.time() - t; ok = r.returncode == 0
    return ok, dt, ('' if ok else (r.stdout + r.stderr)[:6000])

done, pending, fut = set(), list(target), {}
with ThreadPoolExecutor(max_workers=jobs) as ex:
    while pending or fut:
        while pending:
            m = pending[0]
            if all((x not in tset) or (x in done) for x in deps[m]):
                pending.pop(0); fut[ex.submit(work, m)] = m
            else: break
        if not fut:
            for m in pending:
                status[m] = {'ok': False, 'secs': 0, 'err': 'skipped: dependency failed'}; fail.append(m)
            pending = []; break
        f = next(iter(fut)); m = fut.pop(f)
        ok, dt, err = f.result(); done.add(m)
        status[m] = {'ok': ok, 'secs': round(dt,1), 'err': err}
        print(('OK   ' if ok else 'FAIL ') + "%s (%.1fs)" % (m, dt), flush=True)
        if not ok:
            print(err, flush=True); fail.append(m)
            if not keep_going:
                for x in list(fut): x.cancel()
                json.dump({'built': len(status), 'fail': fail, 'status': status}, open(os.path.join(build,'status.json'),'w'), indent=1)
                sys.exit(1)
json.dump({'built': len(status), 'fail': fail, 'status': status}, open(os.path.join(build,'status.json'),'w'), indent=1)
print("done: %d/%d ok, %d failed" % (len(status)-len(fail), len(target), len(fail)))
sys.exit(0 if not fail else 1)
