"""
Exact direction-local constraint system at a cyclic centre.

Geometry (paper §8): rays v_j at angles theta_j = (c_j+1)*60 degrees, j=0..l-1.
Directions sampled on the 12 cells of 30 degrees; cell i has midpoint 30i+15.
sigma_j(i) = sign(cos(midpoint_i - theta_j)) = sign(cos(15*k)) with k odd.
O_i = U cup {j : sigma_{j-1}(i)=sigma_j(i)=-1}
I_i = U cup {j : sigma_{j-1}(i)=sigma_j(i)=+1},  U = Fin k \ {0..l-1}   (paper (8.1))
All arithmetic is integer/bitmask: no floating point.
"""
import itertools

# sign of cos(15*k degrees) for odd k (never zero when k odd)
NEG_ODD = {7, 9, 11, 13, 15, 17}   # residues of odd k mod 24 giving cos(15k) < 0

def sgn_cos(km):
    r = km % 24
    if r % 2 == 0:
        raise ValueError("even multiple of 15 degrees: possible zero")
    return -1 if r in NEG_ODD else 1

def signs(k, l, c, cell):
    """sigma_j(cell) for j in Z/l, with the rays at (c_j+1)*60 deg."""
    mu = 30*cell + 15
    out = []
    for j in range(l):
        # mu - theta_j = (30*cell+15) - 60*(c[j]+1) = 15*(2*cell - 4*(c[j]+1) - 3)
        km = 2*cell + 1 - 4*(c[j]+1)
        out.append(sgn_cos(km))
    return out

def OI(k, l, c, cell):
    sig = signs(k, l, c, cell)
    U = frozenset(range(l, k))
    O = set(U); I = set(U)
    for j in range(l):
        if sig[(j-1) % l] == -1 and sig[j] == -1:
            O.add(j)
        if sig[(j-1) % l] == 1 and sig[j] == 1:
            I.add(j)
    return frozenset(O), frozenset(I)

def palettes(k):
    """all admissible palettes: bitmasks with 1 <= size <= k-3"""
    out = []
    for sz in range(1, k-2):
        for comb in itertools.combinations(range(k), sz):
            m = 0
            for x in comb: m |= 1 << x
            out.append(m)
    return out

def mask_of(S):
    m = 0
    for x in S: m |= 1 << x
    return m

def cycle_sat(k, l, c, parity, want_witness=False):
    """Is there a palette 6-tuple on the six cells of `parity` meeting
    (size bound, cyclic 60-degree disjointness, sliver hits)?"""
    cells = [(parity + 2*t) % 12 for t in range(6)]
    data = [OI(k, l, c, cell) for cell in cells]
    P = palettes(k)
    hits = []
    for (O, I) in data:
        om, im = mask_of(O), mask_of(I)
        hits.append([p for p in P if (p & om) and (p & im)])
    if any(len(h) == 0 for h in hits):
        return (False, None) if want_witness else False
    n = 6
    # DFS around the cycle; x_0 restricted to a canonical class to kill rotation only if asked
    sol = [0]*n
    def dfs(t, first, prev):
        if t == n:
            return (prev & first) == 0
        for p in hits[t]:
            if t > 0 and (p & prev):
                continue
            if t == n-1 and (p & first):
                continue
            sol[t] = p
            if dfs(t+1, first, p):
                return True
        return False
    for p0 in hits[0]:
        sol[0] = p0
        if dfs(1, p0, p0):
            w = [bitnames(k, q) for q in sol]
            return (True, w) if want_witness else True
    return (False, None) if want_witness else False

def bitnames(k, m):
    return tuple(i for i in range(k) if m >> i & 1)

def field_sat(k, l, c, want_witness=False):
    """A palette field on the whole direction circle exists iff both parities are satisfiable."""
    r0 = cycle_sat(k, l, c, 0, want_witness)
    r1 = cycle_sat(k, l, c, 1, want_witness)
    s0 = r0[0] if want_witness else r0
    s1 = r1[0] if want_witness else r1
    if want_witness:
        return (s0 and s1, (r0[1], r1[1]))
    return s0 and s1
