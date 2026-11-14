#!/usr/bin/env python3
"""Compile the named OAI modules of a tree and print the full error of each failure.

usage: check1.py TREE OUT CACHE mod1 mod2 ...
The tree is searched for sources; deps resolve from OUT then CACHE.
"""
import os, sys, subprocess
from concurrent.futures import ThreadPoolExecutor

tree, out, cache = sys.argv[1], sys.argv[2], sys.argv[3]
names = sys.argv[4:]
env = dict(os.environ)
env['LEAN_PATH'] = ':'.join([out, cache] + ([env['LEAN_PATH']] if env.get('LEAN_PATH') else []))
env['TMPDIR'] = os.path.abspath('.scratch')
os.makedirs(env['TMPDIR'], exist_ok=True)

def run(n):
    src = os.path.join(tree, n.replace('.', '/') + '.lean')
    dst = os.path.join(out, n.replace('.', '/') + '.olean')
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    r = subprocess.run(['lean', '-o', dst, src], env=env, capture_output=True, text=True)
    return n, r.returncode, r.stdout + r.stderr

with ThreadPoolExecutor(max_workers=int(os.environ.get('W', '4'))) as ex:
    for n, rc, msg in ex.map(run, names):
        print(f'==== {n} rc={rc}', flush=True)
        if rc != 0:
            print(msg[:3000], flush=True)
