#!/usr/bin/env python3
"""D1: dump the exact reference SETS A_n, D_n for n = 0..30 to JSON.

Reusable test data: a claimed bijection f: A_n -> D_n can be checked by
  sorted(map(tuple, f(listing_of_A[n]))) == sorted(listing_of_D[n]).
"""
import json, time
from d1_enum import gen_A_direct, gen_D_direct

t0 = time.perf_counter()
data = {"A": {}, "D": {}}
for n in range(0, 31):
    data["A"][str(n)] = [list(x) for x in gen_A_direct(n)]
    data["D"][str(n)] = [list(x) for x in gen_D_direct(n)]
    assert len(data["A"][str(n)]) == len(data["D"][str(n)])
with open("d1_sets_n0_30.json", "w") as f:
    json.dump(data, f)
el = time.perf_counter() - t0
print("wrote d1_sets_n0_30.json")
print("counts n=0..30:", [len(data["A"][str(n)]) for n in range(31)])
print("total tuples:", sum(len(data["A"][str(n)]) for n in range(31)), "per side")
print("wall time: %.4f s" % el)
