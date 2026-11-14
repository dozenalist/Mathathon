"""s7_triangle.py -- is the (3,2) residue possible at the vertices of a unit triangle?

Instance: three nodes p0, p1, p2 with |p1-p0| = |p2-p1| = |p0-p2| = 1 (a unit equilateral
triangle), palettes indexed by the six absolute lattice directions (multiples of 60 deg;
all side directions are lattice directions for this triangle).
At every node the palette map must be the (3,2) residue: exactly two values, a 3-set T and a
2-set B, disjoint, alternating along the R-orbit (which (5.7) forces: two equal consecutive
values would not be disjoint).
Other constraints: 1 <= |P| <= 3, (5.7), MON, C1, and (UNIT) at the three pairs.

Procedure 1 (default): explicit enumeration of all residue fields, exact python checks.
Procedure 2 (--cnf): print a CNF for CaDiCaL.

usage: python3 s7_triangle.py [--cnf] [--colour] [--pairs | --singles]
   --pairs    only the two-node instances (x, x+u), for the non-vacuity check
   --singles  only one node (calibration: must be SAT)
"""
import sys
from itertools import combinations, product

K = 6
DIRS = [(1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1)]   # direction index -> lattice vector
# triangle vertices in lattice coordinates (0,0), (1,0), (0,1): |e1|=|e2|=1, |e2-e1|=1
def triangle():
    return [(0, 0), (1, 0), (0, 1)]

def side_dir(a, b):
    d = (b[0] - a[0], b[1] - a[1])
    for i in [-1, 1]:
        for j in [-1, 1]:
            if (i * d[0], j * d[1]) in DIRS and abs(d[0]) <= 1 and abs(d[1]) <= 1 \
               and (d[0] == 0 or d[1] == 0 or d[0] + d[1] == 0):
                pass
    idx = {v: i for i, v in enumerate(DIRS)}
    return idx[d]

def residues():
    """all (T,B) with |T|=3, |B|=2, disjoint  (the 3-set is the one that occurs at even positions)"""
    out = []
    for T in combinations(range(K), 3):
        for B in combinations([l for l in range(K) if l not in T], 2):
            out.append((frozenset(T), frozenset(B)))
    return out

RES = residues()

def word(T, B, phase):
    """6 palettes along the R-orbit; phase 0: T at even positions"""
    return tuple(T if (k % 2 == phase) else B for k in range(6))

def ok_node(w):
    for k in range(6):
        P = w[k]
        if not (1 <= len(P) <= 3): return False
        if P & w[(k + 1) % 6]: return False                    # (5.7)
        Q = w[(k + 2) % 6]
        if len(P) + len(Q) == 5 and not (P & Q): return False  # MON
        for j in range(k + 1, 6):
            Q2 = w[j]
            if len(P) == 3 and len(Q2) == 3 and not (P & Q2): return False   # C1
    return True

def ok_pair(wa, wb, d):
    """(UNIT) at a unit pair whose difference has direction d"""
    for k in range(6):
        if k in (d, (d + 3) % 6): continue
        if wa[k] & wb[k]: return False
    return True

def enumerate_triangle(with_colour=False, verbose=True):
    pts = triangle()
    dd = {(i, j): side_dir(pts[i], pts[j]) for i in range(3) for j in range(3) if i != j}
    sols = []
    for c0 in product(RES, (0, 1)):
        w0 = word(c0[0][0], c0[0][1], c0[1])
        if not ok_node(w0): continue
        for c1 in product(RES, (0, 1)):
            w1 = word(c1[0][0], c1[0][1], c1[1])
            if not ok_node(w1): continue
            if not ok_pair(w0, w1, dd[(0, 1)]): continue
            for c2 in product(RES, (0, 1)):
                w2 = word(c2[0][0], c2[0][1], c2[1])
                if not ok_node(w2): continue
                if not ok_pair(w0, w2, dd[(0, 2)]): continue
                if not ok_pair(w1, w2, dd[(1, 2)]): continue
                if with_colour:
                    # colours must exist: c_i not in the node's palettes, distinct on unit pairs
                    cs = []
                    for w in (w0, w1, w2):
                        free = [l for l in range(K) if all(l not in P for P in w)]
                        if not free: break
                        cs.append(free)
                    if len(cs) < 3: continue
                    if not any(x != y and x != z and y != z for x in cs[0] for y in cs[1] for z in cs[2]):
                        continue
                sols.append((w0, w1, w2))
    if verbose:
        print(f"unit triangle, residue at all three vertices: {len(sols)} solution(s)"
              + ("  [with colour condition]" if with_colour else ""))
        if sols:
            w0, w1, w2 = sols[0]
            for nm, w in zip("pqr", sols[0]):
                print("  ", nm, [''.join(map(str, sorted(P))) for P in w])
    return sols

def enumerate_pair(with_colour=False, verbose=True):
    pts = [(0, 0), (1, 0)]
    d = side_dir(pts[0], pts[1])
    sols = []
    for c0 in product(RES, (0, 1)):
        w0 = word(c0[0][0], c0[0][1], c0[1])
        if not ok_node(w0): continue
        for c1 in product(RES, (0, 1)):
            w1 = word(c1[0][0], c1[0][1], c1[1])
            if not ok_node(w1): continue
            if not ok_pair(w0, w1, d): continue
            sols.append((w0, w1))
    if verbose:
        print(f"unit pair, residue at both: {len(sols)} solution(s)")
        if sols:
            print("   e.g.", [''.join(map(str, sorted(P))) for P in sols[0][0]], "|",
                  [''.join(map(str, sorted(P))) for P in sols[0][1]])
    return sols

def enumerate_single(verbose=True):
    n = 0
    for c0 in product(RES, (0, 1)):
        w0 = word(c0[0][0], c0[0][1], c0[1])
        if ok_node(w0): n += 1
    if verbose: print(f"single node, residue: {n} field(s)")
    return n

if __name__ == "__main__":
    print("residue alphabet size:", len(RES), "x 2 phases =", 2 * len(RES), "per node")
    enumerate_single()
    enumerate_pair()
    enumerate_pair(with_colour=True)
    enumerate_triangle()
    enumerate_triangle(with_colour=True)
