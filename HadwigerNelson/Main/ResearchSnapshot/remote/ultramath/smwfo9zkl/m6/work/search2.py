#!/usr/bin/env python3
"""
Procedure 2: independent decision of STRIP(k,ell) by propositional CNF + DPLL.

Encoding (structurally different from the combinatorial product search in
search1.py: it does NOT enumerate palettes, it decides label membership).

  Variables y[j][i] means "label i belongs to the palette at position j".
  Clauses for j = 0..5 (indices mod 6):
    (1) OR_i y[j][i]                                  palette nonempty
    (2) for each (k-2)-subset S: OR_{i in S} NOT y[j][i]      |P_j| <= k-3
    (3) OR_{i in O_j} y[j][i]                          strip outer (Lemma 8.1)
    (4) OR_{i in I_j} y[j][i]                          strip inner (Lemma 8.1)
    (5) (NOT y[j][i] OR NOT y[j+1][i])                 Cor 5.4
    (6) (NOT y[j][a] OR NOT y[j][b]) for cycle edges   Lemma 6.2 (optional)

Every CNF model is re-checked with model.check (a third, independent path).
UNSAT per delta is confirmed by running DPLL twice with opposite branching
orders, and the whole (k,ell) verdict is compared with search1.py.
"""
import itertools, json, sys
from model import allowed, check

def cnf(k, ell, delta, strong=False):
    idx = lambda j, i: j * k + i + 1   # DIMACS: literals are +-1..+-nk
    cl = []
    AI = allowed(k, ell, delta)
    for j, (O, I) in enumerate(AI):
        cl.append([idx(j, i) for i in range(k)])
        for S in itertools.combinations(range(k), k - 2):
            cl.append([-idx(j, i) for i in S])
        if not O or not I:
            cl.append([])                      # immediate contradiction (S0)
            continue
        cl.append([idx(j, i) for i in sorted(O)])
        cl.append([idx(j, i) for i in sorted(I)])
    for j in range(6):
        for i in range(k):
            cl.append([-idx(j, i), -idx((j + 1) % 6, i)])
    if strong:
        for j in range(6):
            for a in range(ell):
                cl.append([-idx(j, a), -idx(j, (a + 1) % ell)])
    return 6 * k, cl

def simplify(clauses, assign):
    out = []
    for c in clauses:
        sat = False
        rem = []
        for lit in c:
            v = abs(lit) - 1
            if v in assign:
                if assign[v] == (lit > 0):
                    sat = True
                    break
            else:
                rem.append(lit)
        if sat:
            continue
        if not rem:
            return None
        out.append(rem)
    return out

def dpll(nv, clauses, order):
    def rec(assign, cls):
        while True:
            units = [c[0] for c in cls if len(c) == 1]
            if not units:
                break
            for u in units:
                v, val = abs(u) - 1, u > 0
                if v in assign and assign[v] != val:
                    return None
                assign = assign | {v: val}
                cls = simplify(cls, {v: val})
                if cls is None:
                    return None
            if not cls:
                return assign
        if not cls:
            return assign
        shortest = min(cls, key=len)
        lit = min(shortest, key=lambda l: order[abs(l) - 1])
        v = abs(lit) - 1
        for val in (True, False):
            a2 = assign | {v: val}
            c2 = simplify(cls, {v: val})
            if c2 is None:
                continue
            r = rec(a2, c2)
            if r is not None:
                return r
        return None
    return rec({}, clauses)

def decide(k, ell, strong=False):
    for delta in itertools.product(range(6), repeat=ell):
        AI = allowed(k, ell, delta)
        if any(not O or not I for O, I in AI):
            continue
        nv, cl = cnf(k, ell, delta, strong)
        m1 = dpll(nv, cl, order=list(range(nv)))
        m2 = dpll(nv, cl, order=list(reversed(range(nv))))
        if (m1 is None) != (m2 is None):
            raise RuntimeError(f"order-dependent verdict at {(k, ell, delta)}")
        if m1 is not None:
            word = [sorted(i for i in range(k) if m1.get(j * k + i, False)) for j in range(6)]
            bad = check(k, ell, delta, word, strong=strong)
            if bad:
                raise RuntimeError(f"CNF model fails checker: {bad}")
            return ("SAT", {"delta": list(delta), "word": word})
    return ("UNSAT", None)

if __name__ == "__main__":
    out = {}
    for strong in (False, True):
        for k in range(4, 8):
            for ell in range(3, k + 1):
                v, cert = decide(k, ell, strong)
                key = f"k{k}_l{ell}_{'strong' if strong else 'weak'}"
                out[key] = {"verdict": v, "cert": cert}
                print(f"CNF/DPLL k={k} ell={ell} {'[+S4]' if strong else '     '}: {v}"
                      + ("" if cert is None else f" delta={cert['delta']} word={cert['word']}"))
    with open("strip_table_cnf.json", "w") as f:
        json.dump(out, f, indent=1)
    with open("strip_table.json") as f:
        p1 = json.load(f)
    bad = [key for key in out if key in p1 and p1[key]["verdict"] != out[key]["verdict"]]
    print("\nprocedure 1 vs procedure 2 disagreements:", bad if bad else "NONE")
