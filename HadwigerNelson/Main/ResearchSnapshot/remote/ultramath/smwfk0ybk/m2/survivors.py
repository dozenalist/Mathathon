"""Dump one (C1)-(C5) model for EVERY satisfiable geometry at k=6, l=3..6.

These are the objects the next tightening (C6) must kill: each satisfies (C1) |P|<=3,
(C2) Lemma 8.1, (C3) (5.7), (C4) m6 Thm 1, (C5) m6 Thm 2 at the six directions of one
pi/3-orbit, with an exact ray geometry (cell vector).  Labels are 0..5, bit i <-> label i.
"""
import itertools, json, sys
sys.path.insert(0, '.')
from indep import geometry, admissible, search, POP, bits, FULL

def c4(ps):
    return not any(POP[ps[a]] == 3 == POP[ps[b]] and (ps[a] | ps[b]) == FULL
                   for a in range(6) for b in range(a + 1, 6))

out = []
for ell in range(3, 7):
    n = 0
    for t in itertools.product(range(6), repeat=ell - 1):
        c = (0,) + t
        adm = admissible(geometry(ell, c))
        if any(not a for a in adm): continue
        m = search(adm, c4)
        if m is None: continue
        n += 1
        out.append(dict(l=ell, cells=list(c), P=[bits(p) for p in m],
                        ternary=sum(1 for p in m if POP[p] == 3),
                        labels_used=len(set().union(*[set(bits(p)) for p in m]))))
    print(f'l={ell}: {n} satisfiable geometries dumped', flush=True)
json.dump(dict(k=6, note="one (C1)-(C5) model per satisfiable geometry; first cell normalised to 0 "
                         "by the pi/3 rotation symmetry", total=len(out), models=out),
          open('survivors.json', 'w'), indent=0)
print('total', len(out))
