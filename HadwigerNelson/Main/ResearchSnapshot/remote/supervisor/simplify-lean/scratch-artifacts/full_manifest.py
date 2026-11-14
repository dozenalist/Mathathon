#!/usr/bin/env python3
"""FULL downstream manifest for lean/OAI + forward-reference audit of the integrated source.
One process, stdlib only. Usage: cd <repo> && python3 supervisor/simplify-lean/.scratch/full_manifest.py
Writes supervisor/simplify-lean/MANIFEST-full.json (or stdout with --dry)."""
import os, re, sys, json, hashlib
ROOT = 'lean/OAI'
INT = 'supervisor/simplify-lean/snapshots/integ-d123de9bc689a01c/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean'
imp = re.compile(r'^import\s+(OAI\.[A-Za-z0-9_.]+)', re.M)
decl = re.compile(r'^(?:@\[[^\n]*\]\s*)?(?:private |protected |noncomputable |partial |local |scoped )*'
                  r'(?:theorem|lemma|def|abbrev|structure|inductive|class|instance)\s+([A-Za-z0-9_\'!?]+)', re.M)

mods = {}
for dp, _, fs in os.walk(ROOT):
    for f in fs:
        if f.endswith('.lean'):
            fp = os.path.join(dp, f)
            m = 'OAI.' + os.path.relpath(fp, ROOT)[:-5].replace('/', '.')
            src = open(fp).read()
            mods[m] = dict(path=fp, imports=imp.findall(src),
                           sha256=hashlib.sha256(open(fp, 'rb').read()).hexdigest(),
                           lines=src.count('\n') + 1)
N = len(mods)
# topological order over all modules; dangling/out-of-tree imports recorded, not fatal
order, state = [], {}
def visit(m, stack):
    st = state.get(m)
    if st == 'done': return True
    if st == 'open': return False          # cycle
    state[m] = 'open'
    for d in mods[m]['imports']:
        if d in mods and not visit(d, stack + [m]): return False
    state[m] = 'done'; order.append(m); return True
for m in sorted(mods): visit(m, [])
missing = sorted({d for m in mods for d in mods[m]['imports'] if d not in mods})
for i, m in enumerate(order, 1): mods[m]['order'] = i

SMOKE = ['OAI.Analysis.PlaneSpectrum.ConditionalSpectrum',
         'OAI.MeasureTheory.CompactFactors.ConditionalLimits']
def clos(roots):
    seen, st = set(), list(roots)
    while st:
        x = st.pop()
        for d in mods.get(x, {}).get('imports', []):
            if d in mods and d not in seen: seen.add(d); st.append(d)
    return seen
smoke = clos(SMOKE) | set(SMOKE)
# modules that ADDITIONALLY become required because the two edited files gained items
thm = {m: re.findall(r'^(?:theorem|lemma|def|abbrev)\s+([A-Za-z0-9_\']+)', open(mods[m]['path']).read(), re.M)
       for m in mods}

# --- forward-reference audit of the integrated ConditionalSpectrum -------------------
isrc = open(INT).read().split('\n')
def decl_line(name):
    for i, l in enumerate(isrc, 1):
        if re.match(r'^(?:@\[[^\n]*\]\s*)?(?:private |protected |noncomputable |local )*'
                    r'(?:theorem|lemma|def|abbrev|structure|inductive|class|instance)\s+' + re.escape(name) + r'\b', l):
            return i
    return None
own = {}
for i, l in enumerate(isrc, 1):
    mm = decl.match(l)
    if mm: own.setdefault(mm.group(1), i)
core = decl_line('uniform_precision_contradiction')
i0 = next(i for i, l in enumerate(isrc) if l.startswith('theorem uniform_precision_contradiction'))
i1 = next(i for i in range(i0, len(isrc)) if isrc[i].startswith(('omit ', 'theorem ', 'lemma ', 'def ', 'abbrev ')) and i > i0 + 5)
body = '\n'.join(isrc[i0:i1])
used = sorted({t for t in re.findall(r'[A-Za-z_][A-Za-z0-9_\']*', body) if t in own and t != 'uniform_precision_contradiction'})
fwd = [(t, own[t]) for t in used if own[t] > core]
back = [(t, own[t]) for t in used if own[t] < core]

out = {
 "generated_for": "full downstream manifest, lean/OAI source closure",
 "counts": {"modules_found": N, "topological_order_len": len(order), "claimed_83": N == 83,
            "total_lines": sum(v['lines'] for v in mods.values()),
            "smoke_closure_modules": len(smoke),
            "full_tree_modules": N,
            "extra_modules_beyond_smoke": N - len(smoke)},
 "imports_outside_lean_OAI": missing,
 "smoke_closure": sorted(smoke),
 "modules": [{"order": mods[m]['order'], "module": m, "path": mods[m]['path'],
              "sha256": mods[m]['sha256'], "lines": mods[m]['lines'],
              "imports": mods[m]['imports'],
              "in_smoke_closure": m in smoke} for m in order],
 "forward_reference_audit": {
   "file": INT,
   "core_theorem": "uniform_precision_contradiction",
   "core_decl_line": core,
   "same_file_deps_used": len(used),
   "forward_references": [{"ident": t, "decl_line": l} for t, l in fwd],
   "satisfied_dependencies": [{"ident": t, "decl_line": l} for t, l in back]},
}
open('supervisor/simplify-lean/MANIFEST-full.json', 'w').write(json.dumps(out, indent=1))
print(json.dumps({k: out[k] for k in ("counts", "imports_outside_lean_OAI")}, indent=1))
print("forward refs:", out["forward_reference_audit"]["forward_references"])
print("deps satisfied before core:", len(back), "of", len(used))
