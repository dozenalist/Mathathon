"""How much does (C4)+(C5) prune?  Count models per instance (k=6)."""
from itertools import product
from profile2 import sign_word, slivers, admissible
import json

def count_models(ell, k, c):
    sl = slivers(ell, k, sign_word(ell, c))
    adm = [admissible(k, O, I) for (O, I) in sl]
    if any(not a for a in adm):
        return 0, 0, None
    full = frozenset(range(k))
    n_all = n_tight = 0
    example_tight = None
    cur = []
    def rec(i):
        nonlocal n_all, n_tight, example_tight
        if i == 6:
            if cur[5] & cur[0]:
                return
            n_all += 1
            t = [p for p in cur if len(p) == 3]
            ok = len(t) <= 3
            if ok:
                for a in range(len(t)):
                    for b in range(a + 1, len(t)):
                        if (t[a] | t[b]) == full:
                            ok = False
            if ok:
                n_tight += 1
                if example_tight is None:
                    example_tight = [sorted(p) for p in cur]
            return
        for q in adm[i]:
            if i and (q & cur[i-1]):
                continue
            cur.append(q); rec(i+1); cur.pop()
    rec(0)
    return n_all, n_tight, example_tight

if __name__ == "__main__":
    for ell in (3,4,5,6):
        tot_all = tot_tight = 0
        sat_tight_only = 0
        n_inst = 0
        first_kill = None
        for c in product(range(6), repeat=ell):
            a,b,ex = count_models(ell,6,c)
            n_inst += 1
            tot_all += a; tot_tight += b
            if a and not b:
                sat_tight_only += 1
            if a and b and first_kill is None:
                first_kill = {"cells": list(c), "models_C13": a, "models_C15": b,
                              "witness_C15": ex}
        print(f"ell={ell}: instances={n_inst}  models C1-C3={tot_all}  models C1-C5={tot_tight} "
              f" pruned={100*(tot_all-tot_tight)/max(tot_all,1):.1f}%  instances killed entirely={sat_tight_only}")
        print("   sample:", first_kill)
