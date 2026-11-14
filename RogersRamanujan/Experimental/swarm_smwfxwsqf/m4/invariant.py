"""Provable residue invariant on the A side, and its D-side counterpart.
Claim: for alpha in A_n,  #{p == 1 mod 5} - #{p == 4 mod 5}  ==  n (mod 5).
Proof: n = sum p == sum(p mod 5) = s*1 + t*4 = s - t (mod 5)."""
from explore import enum_A, enum_D
bad = []
for n in range(26):
    for a in enum_A(n):
        s = sum(1 for p in a if p % 5 == 1); t = sum(1 for p in a if p % 5 == 4)
        if (s - t - n) % 5 != 0: bad.append((n, a, s - t))
print("A-side invariant s-t == n mod 5, n<=25:", "PASS" if not bad else ("FAIL", bad[:5]))
# D-side: level k obeys n - k^2 = |nu| >= 0, so k <= floor(sqrt n); k mod 5 is NOT forced
print("check: is k mod 5 forced by n mod 5 on the D side?")
for n in range(0, 26):
    ks = sorted({len(l) for l in enum_D(n)})
    print(f"  n={n:2d} n mod5={n%5}  levels k present={ks}  (k mod 5 = {sorted({k%5 for k in ks})})")
