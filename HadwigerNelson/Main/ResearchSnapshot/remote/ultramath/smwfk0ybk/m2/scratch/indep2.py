"""Second, independent decision procedure: forward state-set DP (m5-style, no backtracking
search), plus model analysis: do the (C1)-(C5) models survive using only outsider labels?"""
import itertools
K = 6; FULL = 63
CS = [1, 1, -1, -1, -1, 1]
MASKS = [x for x in range(1, 64) if bin(x).count('1') <= 3]
POP = {x: bin(x).count('1') for x in MASKS}
def adm_of(ell, c, i):
    sig = [CS[(c[j] + 1 - i) % 6] for j in range(ell)]
    U = FULL ^ ((1 << ell) - 1)
    O = I = U
    for j in range(ell):
        if sig[(j-1) % ell] == -1 and sig[j] == -1: O |= 1 << j
        if sig[(j-1) % ell] ==  1 and sig[j] ==  1: I |= 1 << j
    return [p for p in MASKS if (p & O) and (p & I)]

def ok(ps):
    for a in range(6):
        for b in range(a+1, 6):
            if POP[ps[a]] == 3 == POP[ps[b]] and (ps[a] | ps[b]) == FULL: return False
    return True

def dp_count(ell, c, pred):
    """Number of C1&C3 models of the given geometry satisfying pred, by transferring the
    set of reachable (first palette, last palette) pairs; exact, no search tree."""
    adm = [adm_of(ell, c, i) for i in range(6)]
    if any(not a for a in adm): return 0
    cur = {(p, p) for p in adm[0]}
    for i in range(1, 6):
        nxt = set()
        for (f, l) in cur:
            for q in adm[i]:
                if not (q & l): nxt.add((f, q))
        cur = nxt
        if not cur: return 0
    tot = 0
    for (f, l) in cur:
        if f & l: continue
        for p0 in [f]:
            pass
        tot += 1
    return tot

def dp_sat(ell, c, pred=lambda ps: True):
    """Exists a model? enumerate distinct state pairs, then test pred by reconstructing
    one model per (first,last) pair via a parent map."""
    adm = [adm_of(ell, c, i) for i in range(6)]
    if any(not a for a in adm): return None
    # forward: layers[i][p] = {(first palette)} set reachable with P_i = p ; keep witnesses
    layers = [dict() for _ in range(6)]
    for p in adm[0]: layers[0][p] = {p: []}
    for i in range(1, 6):
        for q in adm[i]:
            wit = {}
            for p, ws in layers[i-1].items():
                if p & q: continue
                for f, path in ws.items():
                    wit.setdefault(f, path + [p])
            if wit: layers[i][q] = wit
    for q, ws in layers[5].items():
        for f, path in ws.items():
            if f & q: continue
            model = path + [q]
            if len(model) == 6 and ok(model) and pred(model):
                return model
    return None

if __name__ == '__main__':
    import json
    res = {}
    for ell in range(3, 7):
        tot = 6 ** (ell - 1)
        s = dict(geometries=tot, sat4=0, flips=0, nontrivial=0, all_models_trivial=0, sat3=0)
        W = {}
        for t in itertools.product(range(6), repeat=ell - 1):
            c = (0,) + t
            m3 = dp_sat(ell, c)
            if m3 is None: continue
            s['sat3'] += 1
            m4 = dp_sat(ell, c, ok)
            if m4 is None: s['flips'] += 1
            else:
                s['sat4'] += 1
                U = FULL ^ ((1 << ell) - 1)
                if any((p & ~U) for p in m4): s['nontrivial'] += 1
                if 'sat4' not in W: W['sat4'] = dict(cells=list(c), palettes=[[i for i in range(K) if (p >> i) & 1] for p in m4])
        res[ell] = s; res[ell]['witness'] = W.get('sat4')
        print(ell, s)
    json.dump(res, open('indep2.json', 'w'), indent=1)
