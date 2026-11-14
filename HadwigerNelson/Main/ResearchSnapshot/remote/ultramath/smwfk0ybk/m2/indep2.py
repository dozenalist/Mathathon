"""Second decision procedure for the tightened CSP at k=6, deliberately different in
algorithm from indep.py:

  * the pure (C1)&(C3) existence question is decided by a forward reachability DP over the
    state pair (first palette, current palette) -- no search tree at all;
  * the (C1)&(C3)&(C4) question is decided by an exhaustive DFS that fills the six positions
    RIGHT to LEFT (indep.py fills them left to right), with (C4) tested at completion;
  * model counting / structure by a third pass (models.py).

Constraints (k = 6, labels 0..5, bit i = label i):
  (C1) 1 <= |P_i| <= 3      (C2) P_i meets O_i and I_i      (C3) P_i & P_{i+1} = 0 (mod 6)
  (C4) no two of the six palettes are complementary (A | B == 63)
  sig_i[j] = sign(f_i . v_j) = CS[(c_j + 1 - i) % 6];  U = labels >= l;
  O_i = U | {j : sig_i[j-1] = sig_i[j] = -1};  I_i = U | {j : sig_i[j-1] = sig_i[j] = +1}.
"""
import itertools, json

K = 6; FULL = (1 << K) - 1
CS = [1, 1, -1, -1, -1, 1]
MASKS = [x for x in range(1, 1 << K) if bin(x).count('1') <= K - 3]
POP = {x: bin(x).count('1') for x in MASKS}

def adm_of(ell, c, i):
    sig = [CS[(c[j] + 1 - i) % 6] for j in range(ell)]
    U = FULL ^ ((1 << ell) - 1)
    O = I = U
    for j in range(ell):
        if sig[(j - 1) % ell] == -1 and sig[j] == -1: O |= 1 << j
        if sig[(j - 1) % ell] ==  1 and sig[j] ==  1: I |= 1 << j
    return [p for p in MASKS if (p & O) and (p & I)]

def ok4(ps):
    for a in range(6):
        for b in range(a + 1, 6):
            if POP[ps[a]] == 3 == POP[ps[b]] and (ps[a] | ps[b]) == FULL: return False
    return True

def exists_c3(adm):
    """Exact: reachable (first palette, current palette) pairs, forward, no backtracking."""
    cur = {(p, p) for p in adm[0]}
    for i in range(1, 6):
        cur = {(f, q) for (f, l) in cur for q in adm[i] if not (q & l)}
        if not cur: return None
    good = [(f, l) for (f, l) in cur if not (f & l)]
    if not good: return None
    f, l = good[0]
    return _greedy(adm, f, l)      # witness only; decidability is settled by `good`

def _greedy(adm, f, l):
    """One chain from first palette f to last palette l (feasibility guaranteed)."""
    mid = [f]
    for i in range(1, 5):
        for q in adm[i]:
            if not (q & mid[-1]):
                # check q can still be extended to l
                okk = True
                # forward reachability from q at layer i to l at layer 5
                R = {q}
                for j in range(i + 1, 5):
                    R = {r for r in adm[j] for p in R if not (p & r)}
                    if not R: break
                if R and any((not (r & l)) for r in R):
                    mid.append(q); break
        else:
            return None
    if mid[-1] & l: return None
    return mid + [l]

def exists_c4(ell, c):
    adm = [adm_of(ell, c, i) for i in range(6)]
    if any(not a for a in adm): return None
    ps = [None] * 6
    def bt(i):                     # fills positions 5,4,3,2,1,0  (right to left)
        if i < 0:
            return ok4(ps) and not (ps[5] & ps[0])
        for q in adm[i]:
            if i < 5 and (q & ps[i + 1]): continue
            ps[i] = q
            if bt(i - 1): return True
        return False
    if bt(5): return list(ps)
    return None

if __name__ == '__main__':
    res = {}
    for ell in range(3, 7):
        s = dict(l=ell, geometries=6 ** (ell - 1), sat3=0, sat4=0, flips=0)
        for t in itertools.product(range(6), repeat=ell - 1):
            c = (0,) + t
            adm = [adm_of(ell, c, i) for i in range(6)]
            if any(not a for a in adm): continue
            if exists_c3(adm) is None: continue
            s['sat3'] += 1
            m4 = exists_c4(ell, c)
            if m4 is None: s['flips'] += 1
            else:
                s['sat4'] += 1
                if 'witness' not in s:
                    s['witness'] = dict(cells=list(c),
                                        palettes=[[i for i in range(K) if (p >> i) & 1] for p in m4])
        res[ell] = s
        print(s)
    json.dump(res, open('indep2.json', 'w'), indent=1)
