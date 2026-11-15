# Monte Carlo check of how many mod-180 sign cells the relaxation field set meets (no cell enumeration).
# Random integer angles in units of 1/U degree (alpha_0 = 0); exact sign decisions; field = SAT on every arc.
import random, collections, sys
random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
U = 1000
D = lambda d: d * U
E = [(1 << i) | (1 << ((i + 1) % 6)) for i in range(6)]
PAL2 = [m for m in range(1, 64) if bin(m).count('1') <= 2]
def cos_sign(x):
    x %= D(360)
    if x == D(90) or x == D(270): return 0
    return 1 if (x < D(90) or x > D(270)) else -1
cache = {}
def sat(rows):
    if rows in cache: return cache[rows]
    if any(rp == 0 or rn == 0 for rp, rn in rows): cache[rows] = False; return False
    dom = [[m for m in PAL2 if (m & rp) and (m & rn)] for rp, rn in rows]
    ok = False
    for s in dom[0]:
        reach = {s}
        for j in range(1, 6):
            reach = {m for m in dom[j] if any(not (m & p) for p in reach)}
            if not reach: break
        if any(not (m & s) for m in reach): ok = True; break
    cache[rows] = ok; return ok
def rows_at(alpha, t):
    out = []
    for j in range(6):
        x = t + D(60) * j; pos = neg = 0
        for i in range(6):
            s = cos_sign(x - alpha[i])
            if s > 0: pos |= E[i]
            elif s < 0: neg |= E[i]
        out.append((63 & ~pos, 63 & ~neg))
    return tuple(out)
def field(alpha):
    crit = sorted(set((a + D(30)) % D(60) for a in alpha))
    if len(crit) < 6: return None
    mids = [(crit[k] + crit[(k + 1) % 6] + (D(60) if k == 5 else 0)) // 2 for k in range(6)]
    return all(sat(rows_at(alpha, t)) for t in mids)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 200000
hits = 0; signc = collections.Counter(); res = collections.Counter()
for _ in range(N):
    alpha = [0] + [random.randrange(D(360)) for _ in range(5)]
    f = field(alpha)
    if f:
        hits += 1
        a = tuple(x // D(180) for x in alpha[1:]); g = [x % D(180) for x in alpha[1:]]
        signc[(a, tuple(sorted(range(5), key=lambda i: g[i])))] += 1
        n = tuple(x // D(60) for x in alpha[1:]); fr = [x % D(60) for x in alpha[1:]]
        res[(n, tuple(sorted(range(5), key=lambda i: fr[i])))] += 1
print('samples', N, 'field hits', hits, 'rate', hits / N, '(1/648 =', 1 / 648, ')')
print('distinct sign cells hit', len(signc), 'distinct resonance cells hit', len(res))
print('top sign cells', signc.most_common(5))
