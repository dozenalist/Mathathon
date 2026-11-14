#!/usr/bin/env python3
"""Scope-exact deletion of redundant `open`/`variable`/`include`/`omit` header lines.

Usage: python3 header_dedupe2.py <srcroot> <dstroot>

Removes a standalone `open ...` line when every name it opens is already open in the
enclosing scope, and any variable/include/omit line textually identical to one
already present in the same scope.  `... in` modifier lines are never touched.

Self-check: recomputes the effective open-set at every declaration start in both the
original and the transformed module and refuses (exit 1) if they differ anywhere.
"""
import os, re, shutil, sys
from collections import defaultdict

src, dst = sys.argv[1], sys.argv[2]
saved = defaultdict(int)
if os.path.exists(dst):
    shutil.rmtree(dst)
shutil.copytree(src, dst)

def strip_comments(lines):
    out, depth = [], 0
    for l in lines:
        res, i = [], 0
        while i < len(l):
            if depth == 0 and l.startswith('--', i): break
            if l.startswith('/-', i): depth += 1; i += 2; continue
            if depth > 0 and l.startswith('-/', i): depth -= 1; i += 2; continue
            if depth == 0: res.append(l[i])
            i += 1
        out.append(''.join(res))
    return out

DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)*(theorem|lemma|def|abbrev|instance|structure|class|inductive|opaque)\b")
def is_open_cmd(s):
    w = s.split()
    return bool(w) and w[0] == 'open' and not s.endswith(' in')

def opens(s):
    w = s.split()
    return tuple(x for x in w[1:] if x not in ('scoped',))

def effective_opens_at_decls(lines):
    """map declaration-start line index -> frozenset of open names in force"""
    code = strip_comments(lines)
    stack = [frozenset()]
    res = {}
    for i, l in enumerate(code):
        s = l.strip()
        if not s: continue
        w = s.split()
        if s.endswith(' in'):
            continue
        if w[0] == 'namespace' or s == 'section' or s.startswith('section ') or w[-1] == 'section':
            stack.append(stack[-1]); continue
        if w[0] == 'end':
            if len(stack) > 1: stack.pop()
            continue
        if w[0] == 'open':
            stack[-1] = stack[-1] | frozenset(opens(s)); continue
        if not l[0].isspace() and DECL.match(s):
            res[i] = stack[-1]
    return res

for dp, dn, fn in os.walk(os.path.join(dst, 'OAI')):
    for f in sorted(fn):
        if not f.endswith('.lean'): continue
        p = os.path.join(dp, f)
        orig = open(p, encoding='utf-8').read().split('\n')
        code = strip_comments(orig)
        out, stack = [], [{'open': frozenset(), 'seen': set()}]
        for i, l in enumerate(orig):
            s = code[i].strip()
            w = s.split()
            if s and not s.endswith(' in'):
                if w[0] == 'namespace' or s == 'section' or s.startswith('section ') or w[-1] == 'section':
                    stack.append({'open': stack[-1]['open'], 'seen': set()}); out.append(l); continue
                if w[0] == 'end':
                    if len(stack) > 1: stack.pop()
                    out.append(l); continue
                if w[0] == 'open':
                    nm = opens(s)
                    if all(n in stack[-1]['open'] for n in nm) and s in stack[-1]['seen']:
                        saved[f] += 1; continue
                    stack[-1]['open'] = stack[-1]['open'] | frozenset(nm)
                    stack[-1]['seen'].add(s); out.append(l); continue
                if w[0] in ('variable', 'include', 'omit'):
                    if s in stack[-1]['seen']:
                        saved[f] += 1; continue
                    stack[-1]['seen'].add(s); out.append(l); continue
            out.append(l)
        before = effective_opens_at_decls(orig)
        after = effective_opens_at_decls(out)
        # every declaration start of the transformed file must have the same open set
        # as the corresponding declaration start of the original, matched by order
        ob = [before[k] for k in sorted(before)]
        oa = [after[k] for k in sorted(after)]
        if len(ob) != len(oa) or any(x != y for x, y in zip(ob, oa)):
            print('SELF-CHECK FAILED:', p)
            for j, (x, y) in enumerate(zip(ob, oa)):
                if x != y:
                    print('  first mismatch at decl', j, 'missing', sorted(x - y), 'extra', sorted(y - x)); break
            sys.exit(1)
        open(p, 'w', encoding='utf-8').write('\n'.join(out))
tot = sum(saved.values())
print('header lines removed: %d across %d modules (scope self-check passed for all)' % (tot, len(saved)))
for k, v in sorted(saved.items(), key=lambda kv: -kv[1])[:10]:
    print('  %4d  %s' % (v, os.path.basename(k)))
