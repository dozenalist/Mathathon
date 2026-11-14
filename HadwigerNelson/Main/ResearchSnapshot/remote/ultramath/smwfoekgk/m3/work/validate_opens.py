#!/usr/bin/env python3
"""Static soundness check for the `open`-deduplication patch.

For every declaration that survives in the patched tree, the set of opened names
in force at its first token must equal the set that was in force at the same
declaration in the original tree.  Also checks that no scope line
(end / section / noncomputable section / namespace) disappeared or appeared, so
the enclosing namespace chain of every declaration is unchanged.

usage: validate_opens.py ORIG_OAI TREE_OAI
"""
import os, re, sys, collections

DECL = re.compile(r'^(?:@\[[^\n]*\]\s*)?((?:private |protected |noncomputable |partial |scoped )*)'
                  r'(theorem|lemma|def|abbrev|structure|class|instance|inductive)\s+([^\s({:]+)')
OPEN = re.compile(r'^open(\s+scoped)?\s+(.*)$')
SCOPE = re.compile(r'^(?:(?:noncomputable|private|protected|scoped)\s+)*section\b|^namespace\b')
END = re.compile(r'^end\b')


def walk(path):
    """-> list of (decl_name, open_set, namespace_stack) for each declaration."""
    out = []
    stack = [(set(), set())]        # (plain, scoped) per scope
    ns = []
    for line in open(path).read().split('\n'):
        s = line.strip()
        m = DECL.match(s)
        if m:
            out.append((m.group(3), frozenset(stack[-1][0]), frozenset(stack[-1][1]), tuple(ns)))
        if END.match(s):
            if len(stack) > 1:
                stack.pop()
            if ns:
                ns.pop()
            continue
        mo = OPEN.match(s)
        if mo and not s.endswith(' in'):
            names = mo.group(2).split()
            stack[-1][1 if mo.group(1) else 0].update(names)
            continue
        if SCOPE.match(s):
            parts = s.split()
            ns.append(parts[-1] if len(parts) > 1 else 'section')
            stack.append((set(stack[-1][0]), set(stack[-1][1])))
    return out


orig_root, tree_root = sys.argv[1], sys.argv[2]
bad = 0
scopebad = 0
for dp, dn, fn in os.walk(orig_root):
    for f in sorted(fn):
        if not f.endswith('.lean'):
            continue
        a = os.path.join(dp, f)
        rel = os.path.relpath(a, orig_root)
        b = os.path.join(tree_root, rel)
        if not os.path.exists(b):
            continue
        A = walk(a)
        B = walk(b)
        da = collections.defaultdict(list)
        for name, pl, sc, ns in A:
            da[name].append((pl, sc, ns))
        for name, pl, sc, ns in B:
            if name not in da:
                continue
            ok = (pl, sc, ns) in da[name]
            if not ok:
                bad += 1
                if bad <= 12:
                    print(f'OPEN-SET CHANGED {rel} :: {name}')
                    print(f'   patched plain-scoped={sorted(pl ^ sc)[:6]} ns={ns}')
                    print(f'   original {[ (sorted(p^s)[:6], n) for p,s,n in da[name] ]}')
        for pat, label in ((r'(?m)^end\b', 'end'), (r'(?m)^namespace\b', 'namespace'),
                           (r'(?m)^(?:(?:noncomputable|private|protected|scoped)\s+)*section\b', 'section')):
            if len(re.findall(pat, open(a).read())) != len(re.findall(pat, open(b).read())):
                scopebad += 1
                print(f'SCOPE LINE COUNT CHANGED {rel} ({label})')
print(f'declarations whose open set changed: {bad}')
print(f'scope-line mismatches (files): {scopebad}')
