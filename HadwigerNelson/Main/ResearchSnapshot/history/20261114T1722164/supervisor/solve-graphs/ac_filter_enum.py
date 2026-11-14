"""AC-conditional finite filter for six-cycle common-interface configurations.

DECLARED FINITE SPACE (everything claimed below is about this space only):
  q in {0,...,5}^6 with q0 = 0 ;  v_i = e^{i q_i pi/3} ;  labels C = {0,...,5} ;
  six-cycle interfaces E_i = {i, (i+1) mod 6}.

CONDITIONS APPLIED
  (AC)  for every direction d: |union{E_i : q_i = d}| <= 3
        [Theorem AC: if the union of excluded label sets leaves <= 2 labels, False.
         A same-direction group of cycle edges excludes exactly that union.]
  (SIX) six-orbit two-side constraints at every angle j = 0..5, for one cell; the six cells
        are equivalent because (c+j) mod 6 rotates the cyclic list, so one check suffices.
        C1 P_j != empty ; C2 |P_j| <= 2 ; C3 P_j cap P_{j+1} = empty (cyclic) ;
        C4 P_j not subset of any E_i ;
        C5 P_j meets C minus union{E_i : s[i][j] = sigma} for BOTH sigma.
        s[i][j] = sign cos((c+j-q_i) pi/3), gated exactly by the residue table below.

All integer/bitmask arithmetic. No floating point. One process.
"""
import sys, time, itertools

T0 = time.time()
C = (1 << 6) - 1
E = [(1 << i) | (1 << ((i + 1) % 6)) for i in range(6)]
SIGN = {0: 1, 1: 1, 2: -1, 3: -1, 4: -1, 5: 1}      # sign cos(n*pi/3), n mod 6

def popcount(x): return bin(x).count("1")

# palette candidates: nonempty, size <= 2, not contained in any E_i   (C1, C2, C4)
PAL = []
for a in range(6):
    P = 1 << a
    if not any(P & ~e == 0 for e in E): PAL.append(P)
for a, b in itertools.combinations(range(6), 2):
    P = (1 << a) | (1 << b)
    if not any(P & ~e == 0 for e in E): PAL.append(P)
print(f"[0] palette candidates after C1,C2,C4: {len(PAL)}  "
      f"{[ [i for i in range(6) if P>>i&1] for P in PAL ]}")

def allowed_lists(q):
    """A[u] = set of palettes allowed at a position with (c+j) mod 6 = u."""
    out = []
    for u in range(6):
        up = dn = 0
        for i in range(6):
            if SIGN[(u - q[i]) % 6] == 1: up |= E[i]
            else:                         dn |= E[i]
        cup, cdn = C & ~up, C & ~dn
        A = frozenset(P for P in PAL if (P & cup) and (P & cdn))
        out.append(A)
    return out

def cycle_feasible(A):
    if any(len(a) == 0 for a in A): return None
    for p0 in A[0]:
        reach = {p0}
        for j in range(1, 6):
            reach = {p for p in A[j] if any((p & r) == 0 for r in reach)}
            if not reach: break
        if not reach: continue
        for p5 in reach:
            if (p5 & p0) == 0:
                seq = [p0]
                # rebuild a witness greedily
                cur = p0
                ok = True
                for j in range(1, 6):
                    nxt = next((p for p in A[j] if (p & cur) == 0 and
                                (j < 5 or (p & p0) == 0)), None)
                    if nxt is None: ok = False; break
                    seq.append(nxt); cur = nxt
                if ok and (seq[5] & p0) == 0: return seq
    return None

def ac_exclusion(q):
    """Return list of (direction, union_size) violating AC, empty if AC passes."""
    bad = []
    for d in range(6):
        idx = [i for i in range(6) if q[i] == d]
        U = 0
        for i in idx: U |= E[i]
        if popcount(U) >= 4: bad.append((d, idx, popcount(U)))
    return bad

print("\n[1] spot check of the fixed q named in the consumer note")
for q in [(0,3,3,3,0,0)]:
    bad = ac_exclusion(q)
    print(f"      q={q}")
    for d, idx, sz in bad:
        U = 0
        for i in idx: U |= E[i]
        print(f"        direction d={d} (v_i = e^(i*{d}pi/3)): group {idx}, "
              f"union labels {[i for i in range(6) if U>>i&1]} size {sz} >= 4  -> AC forbids")
    print(f"        AC-excluded: {bool(bad)}; complement of the d=3 group = "
          f"{[i for i in range(6) if not (E[1]|E[2]|E[3])>>i&1]}")

print("\n[2] enumeration over q in {0..5}^6 with q0 = 0")
n_total = n_ac = n_feas = 0
survivors = []; ac_fail = 0
first_witness = None
for tail in itertools.product(range(6), repeat=5):
    q = (0,) + tail
    n_total += 1
    if ac_exclusion(q): ac_fail += 1; continue
    n_ac += 1
    A = allowed_lists(q)
    w = cycle_feasible(A)
    if w is None: continue
    n_feas += 1
    survivors.append(q)
    if first_witness is None: first_witness = (q, w, A)

print(f"      candidates in declared space      : {n_total}")
print(f"      pass AC filter                    : {n_ac}")
print(f"      fail AC filter                    : {ac_fail}")
print(f"      pass AC AND six-orbit feasible    : {n_feas}")
print(f"      elapsed {time.time()-T0:.2f}s")

if first_witness:
    q, w, A = first_witness
    print(f"\n[3] CERTIFICATE: one survivor q = {q}")
    for j, P in enumerate(w):
        print(f"        angle j={j}: palette {[i for i in range(6) if P>>i&1]}")
    print("      (feasible in every cell: the six cells are cyclic rotations of one another)")
print(f"\n[4] survivor count: {len(survivors)}")
if len(survivors) <= 24:
    print("      survivors:", survivors)
else:
    print("      first 24 :", survivors[:24])

print("\n" + "=" * 70)
print("SCOPE: finite statement about q in {0..5}^6 with q0 = 0, six-cycle interfaces,")
print("conditional on Theorem AC (paper-level, initial Astra acceptance, NOT Lean-checked).")
print("Not an all-angle statement, not a plane statement, not WeakColoring6.")
print("=" * 70)
