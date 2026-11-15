# Results-desk independent count of the all-phase relaxation field set (written from the model definitions only).
# Model: labels 0..5, E_i={i,i+1}; alpha in (R/360)^6, alpha_0 = 0. At phase x: Ppos={i: cos(x-alpha_i)>0},
# Pneg={i: cos<0}; Rp = C minus U E_i (i in Ppos), Rn likewise. R(t,alpha): P_j meets Rp(t+60j) and Rn(t+60j),
# P_j disjoint from P_{j+1} cyclically. Field exists iff R(t,alpha) SAT for every t (one t per arc of R/60 cut by alpha_i+30).
# Resonance cell (alpha_0 = 0): integer parts n_i = floor(alpha_i/60) in 0..5 (i=1..5) and the strict order of the
# fractional parts f_i = alpha_i mod 60 in (0,60). All cells are congruent simplices, so measure = fraction of cells.
# Exact arithmetic: all angles are integers in units of 1/14 degree (f values k*60/7, t midpoints are half-steps).
import itertools, sys, time
from fractions import Fraction as F
t0 = time.time()
U = 14                       # units per degree: f_i = rank * 60/7 degrees -> rank*120 units; arcs midpoints integer
DEG = lambda d: d * U
def cos_sign(x):             # x integer angle in units; sign of cos
    x %= DEG(360)
    if x == DEG(90) or x == DEG(270): return 0
    return 1 if (x < DEG(90) or x > DEG(270)) else -1
E = [(1 << i) | (1 << ((i + 1) % 6)) for i in range(6)]
PAL2 = [m for m in range(1, 64) if bin(m).count('1') <= 2]
cache = {}
def fixed_sat(rows):          # rows: tuple of (Rp,Rn) masks for j=0..5 ; returns (sat, empty_side)
    if rows in cache: return cache[rows]
    if any(rp == 0 or rn == 0 for rp, rn in rows):
        cache[rows] = (False, True); return cache[rows]
    dom = [[m for m in PAL2 if (m & rp) and (m & rn)] for rp, rn in rows]
    ok = False
    for s in dom[0]:
        reach = {s}
        for j in range(1, 6):
            reach = {m for m in dom[j] if any(not (m & p) for p in reach)}
            if not reach: break
        if any(not (m & s) for m in reach): ok = True; break
    cache[rows] = (ok, False); return cache[rows]
rcache = {}
def rows_at(alpha, t):
    key = tuple(((t - a) % DEG(360)) // DEG(30) for a in alpha)   # half-sector of t - alpha_i; t is never critical
    r = rcache.get(key)
    if r is not None: return r
    out = []
    for j in range(6):
        x = t + DEG(60) * j
        pos = neg = 0
        for i in range(6):
            s = cos_sign(x - alpha[i])
            if s > 0: pos |= E[i]
            elif s < 0: neg |= E[i]
        out.append((63 & ~pos, 63 & ~neg))
    rcache[key] = tuple(out)
    return rcache[key]
FIELD = []
counts = dict(cells=0, field=0, empty_side=0, c2_only=0)
sign_cells, base60, base180 = set(), set(), set()
for perm in itertools.permutations(range(5)):          # perm[r] = which coordinate (1..5) has rank r
    frac = [0] * 6
    for r, i in enumerate(perm): frac[i + 1] = (r + 1) * 120     # (r+1)*60/7 degrees in units of 1/14 deg
    crit = sorted(((frac[i] + DEG(30)) % DEG(60)) for i in range(6))
    mids = [(crit[k] + crit[(k + 1) % 6] + (DEG(60) if k == 5 else 0)) // 2 for k in range(6)]
    for n in itertools.product(range(6), repeat=5):
        alpha = [0] + [DEG(60) * n[i] + frac[i + 1] for i in range(5)]
        counts['cells'] += 1
        sat_all, empty = True, False
        for t in mids:
            s, e = fixed_sat(rows_at(alpha, t))
            if not s:
                sat_all = False; empty = empty or e
        if sat_all:
            counts['field'] += 1
            a = tuple(n[i] // 3 for i in range(5)); g = [60 * (n[i] % 3) * U + frac[i + 1] for i in range(5)]
            sign_cells.add((a, tuple(sorted(range(5), key=lambda i: g[i]))))
            base60.add(perm); base180.add(tuple(sorted(range(5), key=lambda i: g[i])))
            FIELD.append(tuple(alpha))
        elif empty: counts['empty_side'] += 1
        else: counts['c2_only'] += 1
print(counts, 'measure =', F(counts['field'], counts['cells']))
print('sign cells (mod 180: 2^5 x 5! = 3840) meeting field set:', len(sign_cells))
print('base chambers, mod-60 fractional orders (5! = 120) meeting field set:', len(base60))
print('base chambers, mod-180 orders (5! = 120) meeting field set:', len(base180))
print('distinct fixed-phase row patterns cached:', len(cache), ' time %.1fs' % (time.time() - t0))

import random, collections
H=DEG(180); FULL=DEG(360)
def comp_label(al):           # correct component label: normalise alpha_0 = 0, then (floor(a_i/180), order of a_i mod 180)
    b=[(x-al[0])%FULL for x in al]
    return (tuple(x//H for x in b[1:]), tuple(sorted(range(1,6),key=lambda i:b[i]%H)))
def naive_label(al):          # (Z/2)^6 / <1,...,1> lift read off WITHOUT normalising alpha_0, plus the cyclic order mod 180
    e=[(x%FULL)//H for x in al]; e=tuple(v^e[0] for v in e)
    r=[x%H for x in al]; o=sorted(range(6),key=lambda i:r[i]); k=o.index(0); cyc=tuple(o[k:]+o[:k])
    return (e,cyc)
print('field reps',len(FIELD))
print('correct component labels (alpha_0 = 0):',len({comp_label(a) for a in FIELD}))
random.seed(5)
for trial in range(3):
    rot=[]
    for a in FIELD:
        s=random.randrange(FULL); rot.append(tuple(x+s for x in a))   # one global angle per rep (stays in its component)
    print('trial',trial,'correct labels after rotation:',len({comp_label(a) for a in rot}),' naive (Z/2)^6/<1> labels:',len({naive_label(a) for a in rot}))
