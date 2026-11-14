"""Certificates for the composed decision.

For each (ell, k) the certificate records

  * the exact word witness (a six-tuple of palette bitmasks) plus its hexagon (TE)
    witness for every satisfiable (label, cell-triple) pair, together with the
    word-level extras (L5), (C1), (MON);
  * the exact set of satisfiable (label, starting cell) pairs;
  * the exact list of surviving configurations (label, starting cell, weak order);
  * a SHA-256 of the canonical serialisation of the survivor list.

`verify` recomputes everything from scratch and compares.
"""
import hashlib
import json
from itertools import product

import implA
import combo
import rim as RIM

T = implA.intervals()
EXTRAS = ('L5', 'C1', 'MON')


def triple_of(ch, ell, k):
    S = tuple(frozenset(j for j in range(ell) if p in T[ch[j]]) for p in range(6))
    return tuple(implA.allowed_sets(S[p], ell, k) for p in range(3)), S


def key_of(trip):
    return json.dumps([[sorted(a), sorted(b)] for (a, b) in trip])


def canonical_survivors(good):
    rows = []
    for (i, c0, order) in good:
        rows.append((i, tuple(c0), tuple(tuple(b) for b in order)))
    rows.sort()
    h = hashlib.sha256()
    for r in rows:
        h.update(repr(r).encode())
    return rows, h.hexdigest()


def build(ell, k):
    orders = implA.weak_orders(ell)
    oidx = {o: n for n, o in enumerate(orders)}
    wordbook = {}
    sat = {}
    good = []
    for i in range(k):
        ok = []
        for idx in range(6 ** ell):
            ch = []
            t = idx
            for _ in range(ell):
                ch.append(t % 6)
                t //= 6
            ch = tuple(ch)
            trip, S = triple_of(ch, ell, k)
            if any(not oc[0] or not oc[1] for oc in trip):
                continue
            ocs = trip + tuple((b, a) for (a, b) in trip)
            doms = [implA.domain(a, b, ell, k, i) for (a, b) in ocs]
            ws = combo.words_for(doms, i, k, ell, EXTRAS, True)
            if not ws:
                continue
            w = ws[0]
            c, sol = RIM.rim_ok(w, i, k, ell, want_witness=True)
            wordbook.setdefault(i, {})[key_of(trip)] = {
                'word': list(w),
                'rim_c': list(c),
                'rim_Q': [[sol[(j, m)] for m in range(6)] for j in range(6)],
            }
            ok.append(ch)
        ok = set(ok)
        sat[i] = sorted(ok)
        for c0 in ok:
            for order in orders:
                cur = list(c0)
                fine = True
                for _ in range(6):
                    for blk in order:
                        for j in blk:
                            cur[j] = (cur[j] - 1) % 6
                        trip, S = triple_of(tuple(cur), ell, k)
                        if key_of(trip) not in wordbook.get(i, {}):
                            fine = False
                            break
                    if not fine:
                        break
                if fine and tuple(cur) == c0:
                    good.append((i, c0, order))
    rows, digest = canonical_survivors(good)
    return {
        'ell': ell, 'k': k, 'extras': list(EXTRAS),
        'sat_pairs': {str(i): [list(c) for c in sat[i]] for i in sat},
        'survivors': [[i, list(c0), [list(b) for b in order]] for (i, c0, order) in rows],
        'survivor_sha256': digest,
        'order_index': {str(kk): oidx[o] for o in orders for kk in [repr(o)]},
        'wordbook': {str(i): wordbook.get(i, {}) for i in range(k)},
    }


def verify(cert, quiet=False):
    ell, k = cert['ell'], cert['k']
    errs = []
    wb = cert['wordbook']
    # 1. every stored word and its rim witness satisfy the full system
    for i in range(k):
        for key, dat in wb.get(str(i), {}).items():
            trip = tuple((frozenset(a), frozenset(b)) for a, b in json.loads(key))
            ocs = trip + tuple((b, a) for (a, b) in trip)
            w = tuple(dat['word'])
            for pos, (O, I) in enumerate(ocs):
                P = set(implA.bits(w[pos], k))
                if not P:
                    errs.append(('empty palette', i, key, pos))
                if len(P) > k - 3:
                    errs.append(('(PB)', i, key, pos))
                if not (P & O) or not (P & I):
                    errs.append(('(S14)', i, key, pos))
                if i in P:
                    errs.append(('(SA)', i, key, pos))
                if any(P <= {j, (j + 1) % ell} for j in range(ell)):
                    errs.append(('(E)', i, key, pos))
            if not implA.word_ok(w, i, k, ell, EXTRAS):
                errs.append(('word system', i, key))
            c = tuple(dat['rim_c'])
            sol = {(j, m): dat['rim_Q'][j][m] for j in range(6) for m in range(6)}
            e = RIM.verify_rim(w, i, k, c, sol)
            if e:
                errs.append(('rim', i, key, e[:2]))
    # 2. the SAT (label, cell) set and the survivor list agree with a fresh run
    fresh = build(ell, k)
    if fresh['survivor_sha256'] != cert['survivor_sha256']:
        errs.append(('survivor hash', fresh['survivor_sha256'], cert['survivor_sha256']))
    if fresh['sat_pairs'] != cert['sat_pairs']:
        errs.append(('sat pairs differ',))
    if len(fresh['survivors']) != len(cert['survivors']):
        errs.append(('survivor count', len(fresh['survivors']), len(cert['survivors'])))
    if not quiet:
        print(f"verify ell={ell} k={k}: wordbook entries "
              f"{sum(len(v) for v in wb.values())}, survivors {len(cert['survivors'])}, "
              f"sha256 {cert['survivor_sha256'][:16]}..., errors {len(errs)}")
    return errs


if __name__ == '__main__':
    import sys
    mode = sys.argv[1]
    ell = int(sys.argv[2])
    k = int(sys.argv[3])
    if mode == 'build':
        c = build(ell, k)
        print(json.dumps({kk: c[kk] for kk in c if kk != 'wordbook' and kk != 'order_index'}))
        with open(f'cert_{ell}_{k}.json', 'w') as f:
            json.dump(c, f)
        print("wordbook size", sum(len(v) for v in c['wordbook'].values()))
    else:
        with open(f'cert_{ell}_{k}.json') as f:
            c = json.load(f)
        e = verify(c)
        print("ERRORS", e[:3], "count", len(e))
