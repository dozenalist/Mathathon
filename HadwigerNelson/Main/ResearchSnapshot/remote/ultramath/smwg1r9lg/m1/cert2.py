"""Certificate build/verify on top of the composed decision (combo.decide).

The certificate is exact: it stores one word (with its hexagon (TE) witness) for
every satisfiable (label, cell) pair, the exact set of satisfiable (label, cell)
pairs, the exact survivor list (stored in full for ell = 6; for the larger cases
only its SHA-256, plus the counts), and the SHA-256 of the canonical survivor
list.  `verify` re-runs the decision from scratch.
"""
import hashlib
import json

import implA
import combo
import rim as RIM

EXTRAS = ('L5', 'C1', 'MON')


def key_of(trip):
    return '|'.join(f"{sorted(a)};{sorted(b)}" for (a, b) in trip)


def parse_key(key):
    out = []
    for part in key.split('|'):
        a, b = part.split(';')
        out.append((frozenset(json.loads(a.replace("'", '"'))),
                    frozenset(json.loads(b.replace("'", '"')))))
    return tuple(out)


def canonical(good):
    rows = sorted((i, tuple(c0), tuple(tuple(b) for b in order)) for (i, c0, order) in good)
    h = hashlib.sha256()
    for r in rows:
        h.update(repr(r).encode())
    return rows, h.hexdigest()


def build(ell, k, store_survivors=True):
    good, info, per_label = combo.decide(ell, k, EXTRAS, need_rim=True)
    wordbook = {}
    for (trip, i), (ok, w, _n) in info.items():
        if not ok:
            continue
        c, sol = RIM.rim_ok(w, i, k, ell, want_witness=True)
        wordbook.setdefault(str(i), {})[key_of(trip)] = {
            'word': list(w),
            'rim_c': list(c),
            'rim_Q': [[sol[(j, m)] for m in range(6)] for j in range(6)],
        }
    rows, digest = canonical(good)
    out = {
        'ell': ell, 'k': k, 'extras': list(EXTRAS),
        'sat_pairs': {str(i): sorted(list(c) for c in per_label[i]) for i in range(k)},
        'n_survivors': len(rows),
        'survivor_sha256': digest,
        'wordbook': wordbook,
    }
    if store_survivors:
        out['survivors'] = [[i, list(c0), [list(b) for b in order]]
                            for (i, c0, order) in rows]
    return out


def verify(cert):
    ell, k = cert['ell'], cert['k']
    errs = []
    for i in range(k):
        for key, dat in cert['wordbook'].get(str(i), {}).items():
            trip = parse_key(key)
            ocs = trip + tuple((b, a) for (a, b) in trip)
            w = tuple(dat['word'])
            for pos, (O, I) in enumerate(ocs):
                P = set(implA.bits(w[pos], k))
                if not P:
                    errs.append(('empty', i, key, pos))
                if len(P) > k - 3:
                    errs.append(('PB', i, key, pos))
                if not (P & set(O)) or not (P & set(I)):
                    errs.append(('S14', i, key, pos))
                if i in P:
                    errs.append(('SA', i, key, pos))
                if any(P <= {j, (j + 1) % ell} for j in range(ell)):
                    errs.append(('E', i, key, pos))
            if not implA.word_ok(w, i, k, ell, EXTRAS):
                errs.append(('word', i, key))
            c = tuple(dat['rim_c'])
            sol = {(j, m): dat['rim_Q'][j][m] for j in range(6) for m in range(6)}
            e = RIM.verify_rim(w, i, k, c, sol)
            if e:
                errs.append(('rim', i, key, e[:1]))
    fresh = build(ell, k)
    if fresh['survivor_sha256'] != cert['survivor_sha256']:
        errs.append(('sha', fresh['survivor_sha256'], cert['survivor_sha256']))
    if fresh['sat_pairs'] != {kk: [list(c) for c in v] for kk, v in cert['sat_pairs'].items()}:
        errs.append(('sat',))
    if fresh['n_survivors'] != cert['n_survivors']:
        errs.append(('count', fresh['n_survivors'], cert['n_survivors']))
    print(f"verify ell={ell} k={k}: words {sum(len(v) for v in cert['wordbook'].values())}, "
          f"sat pairs {sum(len(v) for v in cert['sat_pairs'].values())}, "
          f"survivors {cert['n_survivors']}, sha {cert['survivor_sha256'][:16]}, "
          f"errors {len(errs)}")
    return errs


if __name__ == '__main__':
    import sys, time
    if sys.argv[1] == 'build':
        ell, k = int(sys.argv[2]), int(sys.argv[3])
        t = time.time()
        c = build(ell, k, store_survivors=(ell == 6))
        with open(f'cert_{ell}_{k}.json', 'w') as f:
            json.dump(c, f)
        print(f"built ell={ell} k={k}: words {sum(len(v) for v in c['wordbook'].values())}, "
              f"sat pairs {sum(len(v) for v in c['sat_pairs'].values())}, "
              f"survivors {c['n_survivors']}, sha {c['survivor_sha256'][:16]} "
              f"[{time.time()-t:.1f}s]")
    else:
        ell, k = int(sys.argv[2]), int(sys.argv[3])
        c = json.load(open(f'cert_{ell}_{k}.json'))
        e = verify(c)
        print("ERRORS", len(e), e[:3])
