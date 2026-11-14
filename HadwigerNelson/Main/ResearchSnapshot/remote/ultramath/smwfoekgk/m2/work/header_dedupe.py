#!/usr/bin/env python3
"""Scope-aware deletion of redundant `open` / `variable` / `include` header lines.

Usage: python3 header_dedupe.py <srcroot> <dstroot>

For each module, tracks lexical scope (namespace/section ... end).  A standalone
`open A B` line whose names are all already open in the current scope is deleted;
so is any `variable`/`include`/`omit`/`open scoped` line textually identical to one
already seen in the same scope.  `... in` modifier lines are never touched.
Prints per-module and total savings.
"""
import os, re, shutil, sys
from collections import defaultdict

src, dst = sys.argv[1], sys.argv[2]
DROP = re.compile(r"^(open|variable|include|omit)\b")
saved = defaultdict(int)
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst)
for dp, dn, fn in os.walk(os.path.join(dst, 'OAI')):
    for f in sorted(fn):
        if not f.endswith('.lean'):
            continue
        p = os.path.join(dp, f)
        L = open(p, encoding='utf-8').read().split('\n')
        out = []
        stack = [{'open': set(), 'decl': set()}]
        for l in L:
            s = l.strip()
            w = s.split()
            if w and w[0] in ('namespace', 'section') and not s.endswith(' in'):
                stack.append({'open': set(stack[-1]['open']), 'decl': set()})
                out.append(l); continue
            if w and w[0] == 'end':
                if len(stack) > 1:
                    stack.pop()
                out.append(l); continue
            cur = stack[-1]
            if s.endswith(' in'):
                out.append(l); continue
            if w and w[0] == 'open':
                names = [x for x in w[1:] if x not in ('scoped',)]
                if names and all(n in cur['open'] for n in names) and s in cur['decl']:
                    saved[f] += 1
                    continue
                cur['open'].update(names)
                cur['decl'].add(s)
                out.append(l); continue
            if w and w[0] in ('variable', 'include', 'omit'):
                if s in cur['decl']:
                    saved[f] += 1
                    continue
                cur['decl'].add(s)
                out.append(l); continue
            out.append(l)
        # second pass: drop bare `section`/`end` pairs that establish nothing
        res, i = [], 0
        while i < len(out):
            l = out[i]; t = l.strip()
            if t == 'section':
                depth, j, hasdecl = 1, i + 1, False
                while j < len(out) and depth > 0:
                    tt = out[j].strip()
                    ww = tt.split()
                    if ww and ww[0] in ('namespace', 'section') and not tt.endswith(' in'):
                        depth += 1
                    elif ww and ww[0] == 'end':
                        depth -= 1
                        if depth == 0:
                            break
                    elif ww and ww[0] in ('open', 'variable', 'include', 'omit', 'attribute', 'set_option', 'local'):
                        hasdecl = True
                    j += 1
                if depth == 0 and not hasdecl:
                    k = j + 1
                    while k < len(out) and out[k].strip() == '':
                        k += 1
                    saved[f] += 2
                    res.extend(out[k:])
                    i = len(out)
                    continue
            res.append(l); i += 1
        open(p, 'w', encoding='utf-8').write('\n'.join(res))
tot = sum(saved.values())
print('header lines removed: %d across %d modules' % (tot, len(saved)))
for k, v in sorted(saved.items(), key=lambda kv: -kv[1])[:15]:
    print('  %4d  %s' % (v, os.path.relpath(k, dst)))
