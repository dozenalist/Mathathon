"""Independence of the tightening constraints (C4),(C5) at k=6 over m5's interface CSP.

Fresh implementation from the specification in m5/INTERFACE-NOGO.md section 1:
  sig_i[j] = sign(f_i . v_j) = COS_SIGN[(c_j + 1 - i) % 6]  (no zero: the cells avoid it)
  O_i = U | {j : sig_i[j-1] = -1 and sig_i[j] = -1}
  I_i = U | {j : sig_i[j-1] = +1 and sig_i[j] = +1}
(C1) 1 <= |P_i| <= k-3    (C2) P_i meets O_i and I_i    (C3) P_i & P_{i+1} = 0 (mod 6)
(C4) no two of the six palettes are complementary (A u B = Fin k); at k=6 with (C1)
     this is: not both are 3-sets with union Fin 6.
(C5) at most three of the six palettes are ternary.
"""
import itertools, json, sys
K = 6
COS_SIGN = [1, 1, -1, -1, -1, 1]        # sign cos(m*pi/3), m = 0..5
FULL = (1 << K) - 1
MASKS = [x for x in range(1, 1 << K) if bin(x).count('1') <= K - 3]   # 41 masks
POP = {x: bin(x).count('1') for x in MASKS}

def geometry(ell, c):
    sig = [[COS_SIGN[(c[j] + 1 - i) % 6] for j in range(ell)] for i in range(6)]
    U = FULL ^ ((1 << ell) - 1)
    OI = []
    for i in range(6):
        O = I = U
        for j in range(ell):
            if sig[i][(j - 1) % ell] == -1 and sig[i][j] == -1: O |= 1 << j
            if sig[i][(j - 1) % ell] ==  1 and sig[i][j] ==  1: I |= 1 << j
        OI.append((O, I))
    return OI

def admissible(OI):
    return [[p for p in MASKS if (p & O) and (p & I)] for (O, I) in OI]

def compl_pair(ps):
    """True iff some two palettes are complementary 3-sets."""
    tri = [p for p in ps if POP[p] == 3]
    for a, b in itertools.combinations(tri, 2):
        if (a | b) == FULL: return True
    return False

def search(adm, want):
    """First six-palette C1&C3 model satisfying predicate want(ps) -> bool, else None."""
    ps = []
    def bt(i):
        if i == 6:
            return (ps[5] & ps[0]) == 0 and want(ps)
        for q in adm[i]:
            if ps and (q & ps[-1]): continue
            ps.append(q)
            if bt(i + 1): return True
            ps.pop()
        return False
    for q in adm[0]:
        ps = [q]
        if bt(1): return list(ps)
    return None

def bits(p): return [i for i in range(K) if (p >> i) & 1]

def run(ell, verbose=False):
    tot = 6 ** (ell - 1)
    stat = dict(l=ell, geometries=tot, sat3=0, flips=0, sat4=0,
                any_viol4=0, any_viol5=0, any_far_viol_with_C5=0)
    ex_viol4 = ex_viol5 = ex_far = None
    true_w = (lambda ps: True)
    c4_w   = (lambda ps: not compl_pair(ps))
    nc4_w  = (lambda ps: compl_pair(ps))
    nc5_w  = (lambda ps: sum(1 for p in ps if POP[p] == 3) >= 4)
    # (C5) true and (C4) false, complementary pair not adjacent -> the genuinely new content
    def far_w(ps):
        if sum(1 for p in ps if POP[p] == 3) >= 4: return False
        for a in range(6):
            for b in range(a + 1, 6):
                if POP[ps[a]] == 3 and POP[ps[b]] == 3 and (ps[a] | ps[b]) == FULL:
                    return (b - a) in (2, 3, 4)
        return False
    for t in itertools.product(range(6), repeat=ell - 1):
        c = (0,) + t
        adm = admissible(geometry(ell, c))
        if any(not a for a in adm):  continue
        m3 = search(adm, true_w)
        if m3 is None:  continue
        stat['sat3'] += 1
        m4 = search(adm, c4_w)
        if m4 is not None: stat['sat4'] += 1
        else: stat['flips'] += 1
        v4 = search(adm, nc4_w)
        if v4 is not None:
            stat['any_viol4'] += 1
            if ex_viol4 is None: ex_viol4 = dict(ell=ell, cells=list(c), palettes=[bits(p) for p in v4])
        v5 = search(adm, nc5_w)
        if v5 is not None:
            stat['any_viol5'] += 1
            if ex_viol5 is None: ex_viol5 = dict(ell=ell, cells=list(c), palettes=[bits(p) for p in v5])
        vf = search(adm, far_w)
        if vf is not None:
            stat['any_far_viol_with_C5'] += 1
            if ex_far is None: ex_far = dict(ell=ell, cells=list(c), palettes=[bits(p) for p in vf])
    stat['ex_viol4'] = ex_viol4; stat['ex_viol5'] = ex_viol5; stat['ex_far'] = ex_far
    return stat

if __name__ == '__main__':
    out = [run(ell) for ell in range(3, 7)]
    for s in out:
        print({k: v for k, v in s.items() if not k.startswith('ex_')})
    print('--- witnesses for non-implication of (C4) ---')
    for s in out:
        if s['ex_viol4']: print('C1&C2&C3 model with a complementary pair:', s['ex_viol4'])
        if s['ex_viol5']: print('C1&C2&C3 model with >=4 ternary:', s['ex_viol5'])
        if s['ex_far']: print('C1&C2&C3&C5 model w/ far complementary pair:', s['ex_far'])
    json.dump(out, open('indep.json', 'w'), indent=1)
