"""The exact decision of the tightened interface CSP at k = 6, in the mission's
own format, with every satisfiable case's witness.

Normalisation: a global rotation by pi/3 shifts every ray cell by 1 and leaves the
six-palette system unchanged, so the 6^(l-1) cell vectors with c_0 = 0 are one
representative per class (m5/interface_csp.scan).  Both the normalised and the raw
6^l counts are printed; the normalised ones are directly comparable with m5's
Theorem 1 table.

For each satisfiable pair (l, geometry) a witness is printed and re-verified from
the paper's own definition of O(e), I(e) (Lemma 8.1, display (8.1)) rather than
from the bitmask code path.
"""
from itertools import product
import chain_csp as C

K = 6
LBL = "012345"

def show(mod):
    return " ".join("{" + ",".join(LBL[i] for i in range(K) if (p >> i) & 1) + "}" for p in mod)

def verify_from_paper(cell, ell, mod):
    """Re-derive O_i, I_i from the paper's words and check (C1),(C2),(C3)."""
    assert all(1 <= C.pc(p) <= K - 3 for p in mod), "C1"
    for i in range(6):
        jj = (i + 1) % 6
        assert not (mod[i] & mod[jj]), "C3"
    SIG = C.sign_matrix(cell, ell)
    U = set(range(ell, K))
    for i in range(6):
        s = SIG[i]
        O = set(U) | {j for j in range(ell) if not s[(j - 1) % ell] and not s[j]}
        I = set(U) | {j for j in range(ell) if s[(j - 1) % ell] and s[j]}
        P = {j for j in range(K) if (mod[i] >> j) & 1}
        assert P & O, f"C2 outer at {i}"
        assert P & I, f"C2 inner at {i}"
    return True

def dump_all(path="all_witnesses.json"):
    """Every satisfiable (l, cell vector) at k = 6 with an explicit model, plus the
    smallest all-size<=2 model when one exists."""
    import json
    out = []
    for ell in range(3, K + 1):
        for c in product(range(6), repeat=ell):
            m = C.first_model(c, ell, K)
            if m is None:
                continue
            verify_from_paper(c, ell, m)
            sm = C.first_model(c, ell, K, maxsize=2)
            out.append({"l": ell, "cells": list(c),
                        "model": [sorted(i for i in range(K) if (p >> i) & 1) for p in m],
                        "pair_model": (None if sm is None else
                                       [sorted(i for i in range(K) if (p >> i) & 1) for p in sm]),
                        "tight": C.tight_ok(m, K)})
    with open(path, "w") as f:
        json.dump(out, f)
    print(f"wrote {path}: {len(out)} satisfiable instances, "
          f"{sum(1 for e in out if e['pair_model'])} of them with an all-size<=2 model, "
          f"{sum(1 for e in out if e['tight'])} with a (C4)+(C5)-clean model")


if __name__ == "__main__":
    import sys
    if "--all" in sys.argv:
        dump_all()
        sys.exit(0)
    print("k = 6.  'geoms' counts cell vectors; 'norm' uses c_0 = 0 (m5's normalisation).")
    print(" l | geoms   SAT(C1-3)  SAT(C1-5)  norm SAT | first witness (c_0 = 0): cells, palettes")
    for ell in range(3, K + 1):
        raw = list(product(range(6), repeat=ell))
        nrm = [c for c in raw if c[0] == 0]
        s13 = [c for c in raw if C.has_model(c, ell, K)]
        s15 = [c for c in raw if C.has_model(c, ell, K, tight=True)]
        n13 = [c for c in nrm if C.has_model(c, ell, K)]
        n15 = [c for c in nrm if C.has_model(c, ell, K, tight=True)]
        w = None
        for c in n15:
            w = (c, C.first_model(c, ell, K, tight=True))
            break
        verify_from_paper(w[0], ell, w[1])
        # cross-check that the model is also (C4)/(C5)-clean and all-size<=2 where possible
        print(f"{ell:>2} | {len(raw):>6} {len(s13):>10} {len(s15):>10} {len(n15):>9} | "
              f"{w[0]}  {show(w[1])}")
        print(f"   | norm (C1-3) {len(n13)}/{len(nrm)}   norm (C1-5) {len(n15)}/{len(nrm)}"
              f"   raw (C1-5)/(C1-3) equality: {len(s13) == len(s15)}")
