#!/usr/bin/env python3
"""Cross-module declaration reference graph for the OAI tree.

A token in module M is resolved to a declaration of module N when N is in M's
import closure, the name is declared in N, and the name is declared nowhere else
among M's visible modules (so the resolution is unambiguous).
Output: the declarations of a chosen cluster referenced from outside it -- i.e.
the exact public surface a replacement for that cluster must supply.

usage: iface2.py TREE_ROOT [cluster-module-short-name ...]
"""
import os, re, sys, collections, json

tree = sys.argv[1]
cluster_names = set(sys.argv[2:])
DECL = re.compile(r'^(?:@\[[^\n]*\]\s*)?((?:private |protected |noncomputable |partial |scoped )*)'
                  r'(theorem|lemma|def|abbrev|structure|class|instance|inductive)\s+([^\s({:]+)')
IMP = re.compile(r'^import\s+(OAI\.[\w.]+)', re.M)

mods, texts, lines = {}, {}, {}
for dp, dn, fn in os.walk(tree):
    for f in fn:
        if f.endswith('.lean'):
            p = os.path.join(dp, f)
            m = 'OAI.' + os.path.relpath(p, tree)[:-5].replace('/', '.')
            texts[m] = open(p).read()
            lines[m] = len(texts[m].splitlines())
            mods[m] = p

deps = {m: IMP.findall(t) for m, t in texts.items()}
closure = {}
def cl(m):
    if m in closure:
        return closure[m]
    seen, stack = {m}, list(deps[m])
    while stack:
        d = stack.pop()
        if d in seen or d not in mods:
            continue
        seen.add(d)
        stack.extend(deps[d])
    closure[m] = seen
    return seen

decls = collections.defaultdict(dict)
for m, t in texts.items():
    for i, l in enumerate(t.splitlines()):
        mm = DECL.match(l)
        if mm:
            decls[m][mm.group(3)] = (mm.group(2), i + 1)

refs = collections.defaultdict(lambda: collections.defaultdict(set))
for m in mods:
    vis = collections.defaultdict(list)
    for d in cl(m) - {m}:
        for name in decls[d]:
            vis[name].append(d)
    for name, owners in vis.items():
        if len(owners) != 1 or name in decls[m]:
            continue
        cnt = len(re.findall(r'(?<![A-Za-z0-9_.\'])' + re.escape(name) + r'(?![A-Za-z0-9_\'])', texts[m]))
        if cnt:
            refs[owners[0]][name].add(m)

cluster = {m for m in mods if m.split('.')[-1] in cluster_names}
print('cluster:', len(cluster), 'modules,', sum(lines[m] for m in cluster), 'lines')
tot = 0
for m in sorted(cluster, key=lambda m: -lines[m]):
    ext = {n: s - cluster for n, s in refs[m].items() if s - cluster}
    if not ext:
        continue
    tot += len(ext)
    print(f'--- {lines[m]:4d} {m[4:]}  exports {len(ext)} decls used outside:')
    for n in sorted(ext):
        print(f'      {n:45s} <- ' + ', '.join(sorted(x.split('.')[-1] for x in ext[n])))
print('total exported declarations:', tot)
json.dump({m: {n: sorted(s) for n, s in refs[m].items() if s - cluster} for m in cluster},
          open(os.path.join(os.path.dirname(__file__), 'iface.json'), 'w'), indent=1)
