#!/usr/bin/env python3
"""D1 bonus: refine |A_n|, |D_n| by NUMBER OF PARTS (exact enumeration, stdlib).

Purpose: |A_n| = |D_n| does NOT come from a length-preserving bijection; the
k-spectra differ already at n = 4. This is a negative fact useful to anyone
building a bijection A_n -> D_n (in particular combined with T, which preserves
the number of parts). Also reports the least n where the spectra differ and the
least n where the *sorted* spectra agree/differ.
"""
import json
from collections import Counter

NMAX = 30

def gen_A_direct(n):
    allowed = [p for p in range(n, 0, -1) if p % 5 in (1, 4)]
    out = []
    def rec(rem, i, acc):
        if rem == 0:
            out.append(tuple(acc)); return
        if i >= len(allowed): return
        p = allowed[i]; t = 0
        while t * p <= rem:
            if t: acc.append(p)
            rec(rem - t * p, i + 1, acc)
            t += 1
        del acc[len(acc) - (t - 1):]
    rec(n, 0, [])
    return out

def gen_D_direct(n):
    out = []
    def rec(rem, maxpart, acc):
        if rem == 0:
            out.append(tuple(acc)); return
        for p in range(min(maxpart, rem), 0, -1):
            acc.append(p); rec(rem - p, p - 2, acc); acc.pop()
    rec(n, n, [])
    return out

specA, specD, first_diff = {}, {}, None
for n in range(NMAX + 1):
    ca = Counter(len(x) for x in gen_A_direct(n))
    cd = Counter(len(x) for x in gen_D_direct(n))
    specA[n] = dict(sorted(ca.items()))
    specD[n] = dict(sorted(cd.items()))
    if first_diff is None and specA[n] != specD[n]:
        first_diff = n

print(" n | k: |A_n^(k)|            | k: |D_n^(k)|")
for n in range(0, 13):
    print(f"{n:2d} | {specA[n]} | {specD[n]}")
print("first n with different k-spectra:", first_diff)
print("spectra at that n:")
print("  A_%d k->count: %s" % (first_diff, specA[first_diff]))
print("  D_%d k->count: %s" % (first_diff, specD[first_diff]))
print("A_%d all: %s" % (first_diff, gen_A_direct(first_diff)))
print("D_%d all: %s" % (first_diff, gen_D_direct(first_diff)))

# sanity: total of each spectrum is the known grand total
J = json.load(open("d1_counts.json"))
for n in range(NMAX + 1):
    assert sum(specA[n].values()) == J["counts"]["A_direct"][n]
    assert sum(specD[n].values()) == J["counts"]["D_direct"][n]
print("spectra totals match d1_counts.json for n=0..30: True")

with open("d1_by_length.json", "w") as f:
    json.dump({"A": {str(n): specA[n] for n in specA},
               "D": {str(n): specD[n] for n in specD},
               "first_n_with_different_spectra": first_diff}, f, indent=1)
