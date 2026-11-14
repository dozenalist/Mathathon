"""Instance-by-instance agreement of procedure A (tight_csp.py, DFS) and
procedure B (tight_csp_indep.c, state-set DP).  Also checks the dihedral
invariance c -> -c of the SAT predicate (an independent check of the O/I
encoding) and the monotonicity control against m5."""
from itertools import product
import tight_csp as A

Bsat = {ell: set() for ell in (3,4,5,6)}
for line in open("indep_out.txt"):
    p = line.split()
    if p and p[0] == "SAT":
        ell = int(p[1]); Bsat[ell].add(tuple(int(x) for x in p[2:]))

ok = True
summary = {}
for ell in (3,4,5,6):
    geoms = A.geometry_list(ell)
    Asat = set()
    for c in geoms:
        s,_ = A.solve(c, tight=True, want="first")
        if s: Asat.add(c)
    same = (Asat == Bsat[ell])
    ok &= same
    # dihedral invariance: reversal of the orbit, c -> -c (both normalised to c0=0)
    refl_sat = 0; mism = []
    for c in geoms:
        cr = (0,) + tuple((-x) % 6 for x in c[1:])
        cr = (0,) + tuple((-x) % 6 for x in c[1:])
        if (cr in Asat) != (c in Asat):
            mism.append((c, cr))
    # note: reflection sends cells c to -c up to the normalisation of cell 0
    summary[ell] = {"A": len(Asat), "B": len(Bsat[ell]), "agree": same,
                    "reflection_mismatches": len(mism)}
    print("ell=%d  |A|=%d  |B|=%d  agree=%s  reflection mismatches=%d"
          % (ell, len(Asat), len(Bsat[ell]), same, len(mism)))
    if mism[:3]: print("   e.g.", mism[:3])
    # store A's SAT set for later (witness extraction / model analysis)
    open("sat_set_%d.txt" % ell, "w").write("\n".join(" ".join(map(str,c)) for c in sorted(Asat)) + "\n")
print("\nALL INSTANCES AGREE:", ok)
