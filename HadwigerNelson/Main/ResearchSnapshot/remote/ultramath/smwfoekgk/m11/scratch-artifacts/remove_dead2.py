#!/usr/bin/env python3
"""Delete declarations that nothing in the tree refers to.

A declaration is deleted only when
  * its name occurs nowhere in the tree except at its own definition (so it is
    not mentioned by any proof, type, attribute list, `variable` line, ...),
  * it is not an instance/structure/class/inductive (those can be used
    implicitly, by typeclass search or by `deriving`),
  * it carries no attribute at all (so no `@[simp]`, `@[to_additive]`, ...),
  * it is not one of the headline theorems,
  * it is not cited in the repository's results/ documents.
The scan is iterated to a fixpoint, since removing a dead lemma can make a
second one dead.

usage: remove_dead.py TREE_ROOT RESULTS_ROOT
"""
import os, re, sys, json, collections

tree, results = sys.argv[1], sys.argv[2]
SECONDARY = {'Chromatic', 'Covering', 'Converse', 'ConnectedUnitFree', 'Metric', 'Seven',
             'MeasurableProper', 'NullSetRobust', 'Lattice', 'MeasurableAssembly', 'Basic',
             'Assembly', 'Transfer'}
def protected_modules(root):
    return set()
    for dp, dn, fn in os.walk(root):
        for f in fn:
            if f.endswith('.lean') and f[:-5] in SECONDARY:
                out.add(os.path.join(dp, f))
    return out
KEEP = {'no_proper_five_coloring', 'no_proper_five_coloring_algebraic',
        'no_proper_five_coloring_compl_null', 'properColoring_seven',
        'proper_iff_weak', 'chromaticNumber_bounds', 'algebraic_colorable_iff',
        'not_proper_five_coloring_compl_null', 'exists_measurable_proper_seven',
        'weakMeasurableColoring_seven',
        'diam_le_one_connectedComponentIn_of_properColoring'}
DECL = re.compile(r'^(@\[[^\n]*\]\s*)?((?:private |protected |noncomputable |partial |scoped )*)'
                  r'(theorem|lemma|def|abbrev|structure|class|instance|inductive)\s+([^\s({:]+)')
TOK = re.compile(r"[A-Za-z_][A-Za-z0-9_'!?]*")

doc = ''
if os.path.exists('../../../README.md'):
    doc += open('../../../README.md', errors='ignore').read()
for dp, dn, fn in os.walk(results):
    for f in fn:
        if f.endswith('.md'):
            doc += open(os.path.join(dp, f), errors='ignore').read()

deleted = []
for it in range(12):
    files = {}
    for dp, dn, fn in os.walk(tree):
        for f in fn:
            if f.endswith('.lean'):
                p = os.path.join(dp, f)
                files[p] = open(p).read()
    toks = collections.Counter(TOK.findall('\n'.join(files.values())))
    cand = []
    for p, t in files.items():
        L = t.splitlines()
        idx = [(i, m.group(1) or '', m.group(2).strip(), m.group(3), m.group(4))
               for i, l in enumerate(L) for m in [DECL.match(l)] if m]
        STRUCT = re.compile(r'^(end\b|namespace\b|section\b|open\b|variable\b|omit\b|include\b'
                            r'|attribute\b|noncomputable\b|local\b|scoped\b|#|/-!|@\[)')
        for k, (i, attrs, kinds, kind, name) in enumerate(idx):
            end = idx[k + 1][0] if k + 1 < len(idx) else len(L)
            j0 = i + 1
            while j0 < end:
                if STRUCT.match(L[j0].strip()):
                    break
                j0 += 1
            end = j0
            while end > i and L[end - 1].strip() == '':
                end -= 1
            cand.append((p, i, end, attrs, kinds, kind, name, L[i - 1] if i else ''))
    prot = protected_modules(tree)
    lastcomp = collections.Counter(c[6].split(".")[-1] for c in cand)
    drop = collections.defaultdict(list)
    for p, i, end, attrs, kinds, kind, name, prev in cand:
        last = name.split('.')[-1]
        if kind not in ('lemma', 'def', 'abbrev', 'theorem'):
            continue
        if p in prot and kind == 'theorem':
            continue
        if not TOK.fullmatch(last):
            continue
        if toks[last] > lastcomp[last]:
            continue
        if '.' in name and toks[name] > 1:
            continue
        if attrs:
            continue
        if kinds not in ('', 'noncomputable', 'private', 'noncomputable private', 'private noncomputable'):
            continue
        if name in KEEP or re.search(r'\b' + re.escape(last) + r'\b', doc):
            continue
        if prev.strip().startswith(('variable', 'omit', 'include', '@[')):
            continue
        LL = files[p].splitlines()
        j = i
        while True:
            while j > 0 and (LL[j - 1].strip().startswith('--') or LL[j - 1].strip().endswith('-/')):
                if LL[j - 1].strip().endswith('-/'):
                    k = j - 1
                    while k > 0 and '/-' not in LL[k]:
                        k -= 1
                    j = k
                else:
                    j -= 1
            if j > 0 and (LL[j - 1].strip().startswith('omit') or
                          LL[j - 1].strip().startswith('include')) and LL[j - 1].strip().endswith('in'):
                j -= 1
                continue
            break
        drop[p].append((j, end, name, kind))
    if not drop:
        break
    for p, rs in drop.items():
        L = open(p).read().split('\n')
        for i, end, name, kind in sorted(rs, reverse=True):
            del L[i:end]
            deleted.append((p, name, kind, end - i))
        open(p, 'w').write('\n'.join(L))
    print(f'round {it}: removed {sum(len(v) for v in drop.values())} declarations')

print('total declarations removed:', len(deleted), 'lines:', sum(d[3] for d in deleted))
json.dump(deleted, open(os.path.join(os.path.dirname(__file__), 'removed_decls.json'), 'w'), indent=0)
per = collections.Counter()
for p, name, kind, n in deleted:
    per[p] += n
for p, n in per.most_common(15):
    print(f'  {n:4d} {p}')
