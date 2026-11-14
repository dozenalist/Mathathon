#!/usr/bin/env python3
"""Build a copy of the OAI tree, reusing oleans from a read-only cache build.

usage: build.py TREE_ROOT OUT_LIB [CacheLib] [module-prefix ...]

Compiles modules in topological order; a module is skipped when an olean with a
newer mtime than its source (and all its OAI deps' sources) exists in OUT_LIB or
in CacheLib.  Prints one line per compiled module and a summary.
"""
import os, re, sys, subprocess, time, pathlib
from concurrent.futures import ThreadPoolExecutor

tree = pathlib.Path(sys.argv[1]).resolve()
out = pathlib.Path(sys.argv[2]).resolve()
cache = pathlib.Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else None
only = sys.argv[4:]
orig = None
if os.environ.get('ORIG'):
    orig = pathlib.Path(os.environ['ORIG']).resolve()

mods = {}
for p in sorted(tree.glob('OAI/**/*.lean')):
    name = '.'.join(p.relative_to(tree).with_suffix('').parts)
    deps = [m.group(1) for m in
            (re.match(r'^import\s+(OAI\.[\w.]+)\s*$', l) for l in p.read_text(errors='ignore').splitlines())
            if m]
    mods[name] = (p, deps)

order, state = [], {}

def visit(n, stack=()):
    if state.get(n) == 2:
        return
    if state.get(n) == 1:
        raise SystemExit('cycle ' + n)
    state[n] = 1
    for d in mods[n][1]:
        if d in mods:
            visit(d, stack + (n,))
    state[n] = 2
    order.append(n)

for n in list(mods):
    visit(n)

def olean(base, n):
    return base / (n.replace('.', '/') + '.olean') if base else None

def fresh(n):
    p, deps = mods[n]
    if orig is not None:
        o0 = orig / 'OAI' / (n[4:].replace('.', '/') + '.lean')
        if o0.exists() and o0.read_bytes() == p.read_bytes():
            return True
    t = p.stat().st_mtime
    for d in deps:
        t = max(t, mods[d][0].stat().st_mtime)
    for base in (out, cache):
        o = olean(base, n)
        if o and o.exists() and o.stat().st_mtime > t:
            return True
    return False

todo = [n for n in order if not fresh(n)]
if only:
    keep = set()
    changed = set(n for n in todo)
    for n in order:
        if any(n == a or n.startswith(a + '.') or n.endswith('.' + a) for a in only):
            keep.add(n)
    # also everything transitively depending on kept modules
    rev = {}
    for n, (p, deps) in mods.items():
        for d in deps:
            rev.setdefault(d, []).append(n)
    stack = list(keep)
    while stack:
        n = stack.pop()
        for u in rev.get(n, []):
            if u not in keep:
                keep.add(u)
                stack.append(u)
    todo = [n for n in todo if n in keep]

print(f'{len(todo)} modules to build (of {len(order)})', flush=True)
lp = [str(out)]
if cache:
    lp.append(str(cache))
env = dict(os.environ)
env['LEAN_PATH'] = ':'.join(lp) + (':' + env['LEAN_PATH'] if env.get('LEAN_PATH') else '')
env['TMPDIR'] = str(tree.parent / '.scratch')
os.makedirs(env['TMPDIR'], exist_ok=True)

t0 = time.time()
fails = []

def build(n):
    p, _ = mods[n]
    o = olean(out, n)
    o.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(['lean', '-o', str(o), str(p)], env=env,
                       capture_output=True, text=True)
    if r.returncode != 0:
        return n, r.stdout + r.stderr
    return n, None

with ThreadPoolExecutor(max_workers=2) as ex:
    for n, err in ex.map(build, todo):
        if err:
            fails.append((n, err))
            print('FAIL', n, flush=True)
        else:
            print('ok  ', n, flush=True)

print(f'done in {time.time()-t0:.0f}s, {len(fails)} failures', flush=True)
for n, err in fails[:3]:
    print('=' * 20, n)
    print(err[:4000])
