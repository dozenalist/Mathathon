"""Step 1 vacuity check: is the TIGHTENED interface CSP (C1)-(C5) at k=6 SAT by inspection?

Independent re-implementation (written from the paper's displays and from
.ultramath/smwfhd5sl/m5/INTERFACE-NOGO.md section 1; shares no code with it or with d1).

Encoding.  Labels are 0..k-1 as bitmasks.  For an interface of length l:
  T = {0,...,l-1}   the cycle labels,
  U = {l,...,k-1}   the outsiders, m = k-l.
For a ray geometry c in {0,...,5}^l (cell index of each ray v_j) and a direction
index i in 0..5, the sign of e_i . v_j is +1 iff c_j + 1 - i = 0,1,5 (mod 6).
  O_i = U | {j : sign_{j-1} = sign_j = -1}     (Lemma 8.1, allowed set after 'O')
  I_i = U | {j : sign_{j-1} = sign_j = +1}
Constraints:
  (C1) 1 <= |P_i| <= k-3
  (C2) P_i & O_i != 0 and P_i & I_i != 0
  (C3) P_i & P_{i+1} == 0 (indices mod 6)
  (C4) k=6: no two of the six palettes are complementary 3-sets
  (C5) k=6: at most three of the six palettes are ternary (|P_i| = 3)
The check below does not search: it exhibits one assignment and verifies it, for every
one of the 6^l sign words, for l = 3 and l = 4 at k = 6 (m = 3, 2).
"""
from itertools import product

COS = {0: 1, 1: 1, 2: -1, 3: -1, 4: -1, 5: 1}


def allowed(l, k, c):
    """(O_i, I_i) as bitmasks for i = 0..5."""
    O, I = [], []
    for i in range(6):
        sig = [COS[(c[j] + 1 - i) % 6] for j in range(l)]
        o = sum(1 << t for t in range(l, k))          # outsiders are allowed everywhere
        ii = sum(1 << t for t in range(l, k))
        for j in range(l):
            if sig[(j - 1) % l] == -1 and sig[j] == -1:
                o |= 1 << j
            if sig[(j - 1) % l] == 1 and sig[j] == 1:
                ii |= 1 << j
        O.append(o)
        I.append(ii)
    return O, I


def check(k, l, c, palettes):
    """Verify (C1)-(C5) for the given explicit palette list (bitmasks).  Returns reason or None."""
    O, I = allowed(l, k, c)
    for i in range(6):
        p = palettes[i]
        n = bin(p).count('1')
        if not (1 <= n <= k - 3):
            return f"(C1) at i={i}: |P|={n}"
        if not (p & O[i]) or not (p & I[i]):
            return f"(C2) at i={i}"
        if p & palettes[(i + 1) % 6]:
            return f"(C3) at i={i}"
    if k == 6:
        full = (1 << k) - 1
        for i in range(6):
            for j in range(i + 1, 6):
                if palettes[i] | palettes[j] == full and bin(palettes[i]).count('1') == 3 \
                        and bin(palettes[j]).count('1') == 3:
                    return f"(C4) palettes {i},{j} complementary"
        if sum(1 for p in palettes if bin(p).count('1') == 3) > 3:
            return "(C5) more than three ternary"
    return None


def main():
    k = 6
    for l in (3, 4):
        a, b = 1 << l, 1 << (l + 1)          # two distinct outsiders, l and l+1
        pals = [a if i % 2 == 0 else b for i in range(6)]
        bad = 0
        total = 0
        first = None
        for c in product(range(6), repeat=l):
            total += 1
            why = check(k, l, c, pals)
            if why is not None:
                bad += 1
                first = first or (c, why)
        print(f"k=6 l={l}: {total} sign words, {total - bad} satisfy (C1)-(C5) "
              f"with palettes {[bin(p) for p in pals]}"
              + (f"; FIRST FAILURE {first}" if bad else ""))
    # the witness displayed as label lists
    l = 3
    a, b = 1 << l, 1 << (l + 1)
    print("witness (k=6,l=3): P_0=P_2=P_4={%d}, P_1=P_3=P_5={%d}" % (l, l + 1))
    assert check(6, 3, (0, 0, 0), [a, b, a, b, a, b]) is None


if __name__ == "__main__":
    main()
