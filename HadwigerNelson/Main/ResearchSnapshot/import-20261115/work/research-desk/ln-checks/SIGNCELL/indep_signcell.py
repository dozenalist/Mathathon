"""indep_signcell.py -- independent exact recount of the SIGNCEL-COUNT.md section-1 claims.

Written from scratch for the research desk.  Pure stdlib, exact integer arithmetic only
(angles are integers in a fixed unit; no floats in any decision).  Executes no lane script.
Optional input: desk_sat177.txt (dumped from the trusted desk model by desk_sat_dump.py).

Run:  python -I indep_signcell.py > indep_signcell.out

MODEL (from the desk census + ALL-PHASE-REFEREE s.2, re-derived here):
  * interface i positive at phase s  iff  (s - alpha_i) mod 360 in [0,90) u (270,360)  (cos > 0).
  * orbit of base phase t: phases t + 60 j, j = 0..5;  column j = (sign_i(t+60j))_i.
    Equivalently tau_i = round((alpha_i - t)/60) mod 6 and column(tau,j)_i = PAT[(j - tau_i) mod 6].
  * fixed-phase CSP on the 6 columns: palettes P_j (nonempty subsets of {0..5}) hitting R+(col_j)
    and R-(col_j), P_j & P_{j+1} = 0 cyclically (R+/R- exactly as in the desk's sides()).
  * cut points of t (where some tau_i changes) are t = alpha_i + 30 (mod 60).  On a resonance cell
    (all alpha_i distinct mod 60) these are 6 distinct points, cutting R/60 into 6 arcs; the cell
    is SAT ("admits a relaxation field") iff the class on EVERY arc is SAT, i.e. its k=6 staircase
    survives.  A resonance cell does not have a single class tau; it has a cyclic staircase of 6.

Method A (combinatorial, no coordinates): resonance cell = (pi, a): gauge alpha_0 = 0,
  alpha_j = 60 a_j + e_j, e_j in (0,60) distinct, pi = order of e_1..e_5.  Staircase classes
  a - 1_{A_k}, A_k = first k of (0, pi_1..pi_5); SAT looked up in the 177-table (solver S1).
  Sign cell / base chamber / gauge-free labels derived combinatorially from (pi, a).
Method B (geometric, sign-cell-first): enumerate sign cells (b, f-order) and subdivide each into
  its resonance cells (g, e-interleaving); build one explicit random integer interior point per
  cell with a random global rotation; compute every label directly from the coordinates
  (pairwise floors, triple orientations) and SAT from actual cosine signs at arc midpoints,
  decided by a different solver (S2, relation-composition trace).
"""
import sys, os, time, itertools, random, hashlib
from collections import Counter

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
def log(*a):
    print(*a, flush=True)
def stamp(msg):
    log(f'[{time.time() - T0:7.1f}s] {msg}')

with open(os.path.abspath(__file__), 'rb') as _f:
    SELF_SHA = hashlib.sha256(_f.read()).hexdigest()
log('indep_signcell.py sha256 =', SELF_SHA)
log('python', sys.version.split()[0], ' flags isolated =', sys.flags.isolated)

PAT = (1, 1, -1, -1, -1, 1)
PAIRS = [(i, j) for i in range(6) for j in range(i + 1, 6)]                         # 15
TRIPLES = [(i, j, k) for i in range(6) for j in range(i + 1, 6) for k in range(j + 1, 6)]  # 20
CHECKS = []
def check(name, ok, detail=''):
    CHECKS.append((name, bool(ok)))
    log(f'  [{"PASS" if ok else "FAIL"}] {name} {detail}')

# =====================================================================================
# Part 0. Fixed-phase table: two own solvers over UNRESTRICTED palettes 1..63
# =====================================================================================
stamp('Part 0: fixed-phase SAT table')

def side_masks(col):
    rp = rn = 0
    for v in range(6):
        a, b = col[(v - 1) % 6], col[v]
        if a <= 0 and b <= 0:
            rp |= 1 << v
        if a >= 0 and b >= 0:
            rn |= 1 << v
    return rp, rn

DISJ = [0] * 64                       # DISJ[p] = bitset over palettes q (1..63) with p & q == 0
for p in range(1, 64):
    for q in range(1, 64):
        if not (p & q):
            DISJ[p] |= 1 << q
ALLOWED = {}
for rp in range(64):
    for rn in range(64):
        m = 0
        for p in range(1, 64):
            if (p & rp) and (p & rn):
                m |= 1 << p
        ALLOWED[(rp, rn)] = m

def bits(x):
    while x:
        lb = x & -x
        yield lb.bit_length() - 1
        x ^= lb

def sat_S1(cols):
    """forward reachable-set per start palette, early exit"""
    A = [ALLOWED[side_masks(c)] for c in cols]
    if not all(A):
        return False
    for p0 in bits(A[0]):
        S = 1 << p0
        for j in range(1, 6):
            nx = 0
            for p in bits(S):
                nx |= DISJ[p]
            S = nx & A[j]
            if not S:
                break
        else:
            if S & DISJ[p0]:
                return True
    return False

def sat_S2(cols):
    """relation composition R_0;R_1;...;R_5 over all 63 palettes as bitset rows, then trace"""
    A = [ALLOWED[side_masks(c)] for c in cols]
    if 0 in A:
        return False
    rel = []
    for j in range(6):
        nxt = A[(j + 1) % 6]
        rel.append({p: DISJ[p] & nxt for p in bits(A[j])})
    comp = dict(rel[0])
    for j in range(1, 6):
        Rj = rel[j]
        new = {}
        for p0, row in comp.items():
            acc = 0
            for q in bits(row):
                acc |= Rj.get(q, 0)
            new[p0] = acc
        comp = new
    return any((row >> p0) & 1 for p0, row in comp.items())

def column(tau, j):
    return tuple(PAT[(j - tau[i]) % 6] for i in range(6))

def enc(t):                           # canonical code of class t (tau_0 normalised to 0)
    b = t[0]
    v = 0
    for x in t[1:]:
        v = v * 6 + (x - b) % 6
    return v

DEC = [None] * 7776
for tail in itertools.product(range(6), repeat=5):
    t = (0,) + tail
    DEC[enc(t)] = t
assert all(DEC[enc(DEC[c])] == DEC[c] for c in range(7776))

SATC = bytearray(7776)
mism = 0
for c in range(7776):
    cols = [column(DEC[c], j) for j in range(6)]
    s1 = sat_S1(cols)
    s2 = sat_S2(cols)
    mism += (s1 != s2)
    SATC[c] = 1 if s1 else 0
NSAT = sum(SATC)
log(f'  S1 SAT = {NSAT}, UNSAT = {7776 - NSAT}; S1 vs S2 mismatches = {mism}')
check('fixed-phase SAT count 177 (own solvers)', NSAT == 177 and mism == 0)
# shift invariance of the CSP (justifies tau_0 = 0 normalisation)
bad = 0
for c in range(0, 7776, 7):
    t = DEC[c]
    for sh in range(1, 6):
        cols = [column(tuple((x + sh) % 6 for x in t), j) for j in range(6)]
        bad += (sat_S1(cols) != bool(SATC[c]))
check('SAT invariant under common shift of tau (sampled 1111 classes x 5 shifts)', bad == 0)
deskf = os.path.join(HERE, 'desk_sat177.txt')
if os.path.exists(deskf):
    with open(deskf) as f:
        desk = {enc(tuple(int(x) for x in line.split())) for line in f if line.strip()}
    mine = {c for c in range(7776) if SATC[c]}
    check('own 177-set == desk independent_census.py SAT set (class by class)', desk == mine,
          f'(desk {len(desk)}, mine {len(mine)}, sym diff {len(desk ^ mine)})')
else:
    log('  desk_sat177.txt not found; desk comparison skipped')

# =====================================================================================
# Part A. Combinatorial enumeration of resonance cells (pi, a)
# =====================================================================================
stamp('Part A: combinatorial enumeration')

MASK = [0] * 64            # MASK[A]: bit c set iff class (DEC[c] - 1_A) is SAT
for A in range(64):
    m = 0
    for c in range(7776):
        t = DEC[c]
        if SATC[enc(tuple((t[i] - ((A >> i) & 1)) % 6 for i in range(6)))]:
            m |= 1 << c
    MASK[A] = m

# k=6 staircases (tau, linear order of all six indices) -- link to the desk census 8640
per_order = Counter()
tot6 = 0
for order in itertools.permutations(range(6)):
    acc = MASK[0]
    U = 0
    for x in order[:-1]:
        U |= 1 << x
        acc &= MASK[U]
    n = bin(acc).count('1')
    per_order[n] += 1
    tot6 += n
log(f'  k=6 staircases surviving: {tot6} over 720 linear orders; per-order histogram {dict(per_order)}')
check('k=6 survivors = 8640 (desk census by_k[6]) and 8640 = 6*1440', tot6 == 8640)

def pos_orient(pos):          # bits over TRIPLES: 1 iff (pos_i, pos_j, pos_k) positively cyclic
    o = 0
    for (i, j, k) in TRIPLES:
        o = (o << 1) | (((pos[j] - pos[i]) % 6) < ((pos[k] - pos[i]) % 6))
    return o

def pack(P, Q, O180, O60, sat):
    return ((((P << 15) | Q) << 20 | O180) << 20 | O60) << 1 | sat

recA = []
A_sign_key = {}       # Q -> (b, f-order) combinatorial key
A_old_key = Counter() # (pi, a mod 2) blocks met by SAT
A_old_to_Q = {}       # (pi, a mod 2) -> set of Q
A_sat_cells = 0
for pi in itertools.permutations((1, 2, 3, 4, 5)):
    order = (0,) + pi
    acc = MASK[0]
    U = 0
    for x in order[:-1]:
        U |= 1 << x
        acc &= MASK[U]
    satbits = acc
    re = [0] * 6                      # rank of e_j (e_0 = 0 is below all)
    for r, j in enumerate(pi):
        re[j] = r
    pos60 = [0] + [1 + re[j] for j in range(1, 6)]
    O60 = pos_orient(pos60)
    gtE = {(j, k): re[k] > re[j] for (j, k) in PAIRS if j >= 1}
    memo3 = {}
    for c in range(7776):
        a = DEC[c]
        sat = (satbits >> c) & 1
        A_sat_cells += sat
        # gauge-free resonance label P
        P = 0
        for (j, k) in PAIRS:
            if j == 0:
                d = a[k]
            else:
                d = (a[k] - a[j] - (0 if gtE[(j, k)] else 1)) % 6
            P = P * 6 + d
        # sign cell: f_j = 60 (a_j mod 3) + e_j, b_j = floor(d_j / 180)
        m3 = tuple(x % 3 for x in a)
        got = memo3.get(m3)
        if got is None:
            fk = {j: m3[j] * 5 + re[j] for j in range(1, 6)}
            ford = tuple(sorted(range(1, 6), key=lambda j: fk[j]))
            rf = [0] * 6
            for r, j in enumerate(ford):
                rf[j] = r
            pos180 = [0] + [1 + rf[j] for j in range(1, 6)]
            got = (ford, rf, pos_orient(pos180))
            memo3[m3] = got
        ford, rf, O180 = got
        b = [x // 3 for x in a]
        Q = 0
        for (j, k) in PAIRS:
            if j == 0:
                d = b[k]
            else:
                d = (b[k] - b[j] - (0 if rf[k] > rf[j] else 1)) % 2
            Q = Q * 2 + d
        key = (tuple(b[1:]), ford)
        prev = A_sign_key.setdefault(Q, key)
        if prev != key:
            raise SystemExit('A: Q label not injective on (b, f-order)')
        ok = (pi, tuple(x % 2 for x in a))
        A_old_to_Q.setdefault(ok, set()).add(Q)
        if sat:
            A_old_key[ok] += 1
        recA.append(pack(P, Q, O180, O60, sat))
stamp(f'Part A done: {len(recA)} cells enumerated')

def summarise(rec, tag):
    """all counts recomputed from a record list"""
    Pm = (1 << 1) * (1 << 20) * (1 << 20) * (1 << 15)
    Ps = set(); Qc = Counter(); B180 = Counter(); B60 = Counter()
    Q_by_B = {}
    satQ = Counter(); satB = Counter(); satB60 = Counter(); nsat = 0
    for r in rec:
        sat = r & 1
        O60 = (r >> 1) & 0xFFFFF
        O180 = (r >> 21) & 0xFFFFF
        Q = (r >> 41) & 0x7FFF
        P = r >> 56
        Ps.add(P); Qc[Q] += 1; B180[O180] += 1; B60[O60] += 1
        Q_by_B.setdefault(O180, set()).add(Q)
        if sat:
            nsat += 1; satQ[Q] += 1; satB[O180] += 1; satB60[O60] += 1
    out = dict(cells=len(rec), distinct_P=len(Ps), sign_cells=len(Qc),
               cells_per_sign=Counter(Qc.values()), base_chambers=len(B180),
               cells_per_base=Counter(B180.values()),
               signs_per_base=Counter(len(v) for v in Q_by_B.values()),
               mod60_orders=len(B60), nsat=nsat,
               base_met=len(satB), sat_per_base=Counter(satB.values()),
               sign_met=len(satQ), fills=sorted(satQ.values()),
               mod60_met=len(satB60), sat_per_mod60=Counter(satB60.values()),
               satQ=satQ, satB=satB)
    log(f'  [{tag}] resonance cells {out["cells"]}, distinct gauge-free P labels {out["distinct_P"]}')
    log(f'  [{tag}] sign cells (distinct Q) {out["sign_cells"]}, resonance cells per sign cell {dict(out["cells_per_sign"])}')
    log(f'  [{tag}] base chambers (distinct mod-180 cyclic orders) {out["base_chambers"]}, '
        f'resonance cells per chamber {dict(out["cells_per_base"])}, sign cells per chamber {dict(out["signs_per_base"])}')
    log(f'  [{tag}] mod-60 cyclic orders {out["mod60_orders"]}')
    log(f'  [{tag}] SAT resonance cells {nsat}')
    log(f'  [{tag}] SAT meets {out["base_met"]} base chambers; SAT per met chamber {dict(out["sat_per_base"])}')
    log(f'  [{tag}] SAT meets {out["sign_met"]} sign cells; fills {out["fills"]} (sum {sum(out["fills"])})')
    log(f'  [{tag}] SAT meets {out["mod60_met"]} mod-60 cyclic orders; SAT per order {dict(out["sat_per_mod60"])}')
    return out

SA = summarise(recA, 'A')
nold = len(A_old_key)
log(f'  [A] old mod-60 key (order of frac(alpha/60), floor(alpha/60) mod 2), gauge alpha_0=0: '
    f'{len(A_old_to_Q)} blocks, met by SAT {nold}, fills {dict(Counter(A_old_key.values()))}')
split = sum(1 for v in A_old_to_Q.values() if len(v) > 1)
log(f'  [A] old-key blocks spread over >1 true sign cell: {split} of {len(A_old_to_Q)}; '
    f'max sign cells per old block {max(len(v) for v in A_old_to_Q.values())}')

# =====================================================================================
# Part B. Geometric, sign-cell-first enumeration with explicit integer points
# =====================================================================================
stamp('Part B: geometric enumeration (sign cell -> resonance subcells -> explicit points)')

def make_geom(U):
    """label + SAT functions for integer angles in units of 1/U degree (U even)"""
    P30, P60, P90, P180, P270, P360 = 30 * U, 60 * U, 90 * U, 180 * U, 270 * U, 360 * U

    def direct_sign(y):            # sgn cos(y), y integer angle; never called at +-90
        y %= P360
        assert y != P90 and y != P270
        return 1 if (y < P90 or y > P270) else -1

    ROW = [tuple(direct_sign(P60 + P60 * w + P60 * j) for j in range(6)) for w in range(6)]

    def labels(al):
        P = 0
        Q = 0
        for (i, j) in PAIRS:
            d = (al[j] - al[i]) % P360
            P = P * 6 + d // P60
            Q = Q * 2 + d // P180
        O180 = 0
        O60 = 0
        for (i, j, k) in TRIPLES:
            ai = al[i]
            O180 = (O180 << 1) | (((al[j] - ai) % P180) < ((al[k] - ai) % P180))
            O60 = (O60 << 1) | (((al[j] - ai) % P60) < ((al[k] - ai) % P60))
        return P, Q, O180, O60

    def generic(al):
        rs = {x % P60 for x in al}
        return len(rs) == 6

    def arcs(al):
        cuts = sorted((x + P30) % P60 for x in al)
        for k in range(6):
            lo = cuts[k]
            hi = cuts[k + 1] if k < 5 else cuts[0] + P60
            yield (lo + hi) // 2

    def windows(al, t):
        return tuple(((t - x - P30) % P360) // P60 for x in al)

    def direct_matrix(al, t):     # cols[j][i] = sgn cos(t + 60 j - alpha_i), computed directly
        return [tuple(direct_sign(t + P60 * j - al[i]) for i in range(6)) for j in range(6)]

    return dict(ROW=ROW, labels=labels, generic=generic, arcs=arcs, windows=windows,
                direct_matrix=direct_matrix, P60=P60, P180=P180, P360=P360)

ARC_MEMO = {}
ROT_MEMO = {}
def arc_sat(w, ROW):
    s = ARC_MEMO.get(w)
    if s is None:
        cols = [tuple(ROW[w[i]][j] for i in range(6)) for j in range(6)]
        key = min(tuple(cols[(j + r) % 6] for j in range(6)) for r in range(6))
        s = ROT_MEMO.get(key)
        if s is None:
            s = sat_S2(list(key))
            ROT_MEMO[key] = s
        ARC_MEMO[w] = s
    return s

def cell_sat(G, al):
    ROW = G['ROW']; win = G['windows']
    for t in G['arcs'](al):
        if not arc_sat(win(al, t), ROW):
            return 0
    return 1

U = 1000
G = make_geom(U)
P60, P180, P360 = G['P60'], G['P180'], G['P360']
labels = G['labels']
rng = random.Random(20261114)
EVALS = range(2, P60, 2)
GSEQS = list(itertools.combinations_with_replacement(range(3), 5))       # 21
ARR = {}
def arrangements(sizes):
    res = []
    def rec(rem, seq):
        if not any(rem):
            res.append(tuple(seq)); return
        for v in range(3):
            if rem[v]:
                rem[v] -= 1; seq.append(v); rec(rem, seq); seq.pop(); rem[v] += 1
    rec(list(sizes), [])
    return res

recB = []
B_sign_Q = {}
B_dirchk = 0
B_dirbad = 0
Bpts = {}         # P -> one explicit point (kept for SAT cells only + a few)
nsc = 0
for b in itertools.product((0, 1), repeat=5):
    for pf in itertools.permutations((1, 2, 3, 4, 5)):
        nsc += 1
        cnt = 0
        Qseen = set()
        for gs in GSEQS:
            g = [0] * 6
            for r in range(5):
                g[pf[r]] = gs[r]
            blocks = [[pf[r] for r in range(5) if gs[r] == v] for v in range(3)]
            sizes = tuple(len(x) for x in blocks)
            if sizes not in ARR:
                ARR[sizes] = arrangements(sizes)
            for arr in ARR[sizes]:
                ptr = [0, 0, 0]
                eorder = []
                for v in arr:
                    eorder.append(blocks[v][ptr[v]]); ptr[v] += 1
                ev = sorted(rng.sample(EVALS, 5))
                e = [0] * 6
                for r, idx in enumerate(eorder):
                    e[idx] = ev[r]
                rho = rng.randrange(0, P360, 2)
                al = [rho] + [(rho + P180 * b[j - 1] + P60 * g[j] + e[j]) % P360 for j in range(1, 6)]
                assert G['generic'](al)
                P, Q, O180, O60 = labels(al)
                s = cell_sat(G, al)
                Qseen.add(Q)
                cnt += 1
                if s:
                    Bpts[P] = al
                if (len(recB) % 47) == 0:          # validate the window shortcut against direct cosines
                    for t in G['arcs'](al):
                        w = G['windows'](al, t)
                        cols = [tuple(G['ROW'][w[i]][j] for i in range(6)) for j in range(6)]
                        B_dirchk += 1
                        B_dirbad += (cols != G['direct_matrix'](al, t))
                recB.append(pack(P, Q, O180, O60, s))
        if cnt != 243 or len(Qseen) != 1:
            raise SystemExit(f'B: sign cell {(b, pf)} gave {cnt} subcells / {len(Qseen)} Q labels')
        B_sign_Q[(b, pf)] = Qseen.pop()
stamp(f'Part B done: {nsc} enumerated sign cells, {len(recB)} explicit points; '
      f'arc memo {len(ARC_MEMO)}, rotation-canonical CSPs solved {len(ROT_MEMO)}')
check('B: window shortcut == direct cosine signs at actual points',
      B_dirbad == 0, f'({B_dirchk} arc matrices compared, {B_dirbad} mismatches)')
check('B: 3840 enumerated sign cells carry 3840 distinct gauge-free Q labels',
      len(set(B_sign_Q.values())) == 3840 == len(B_sign_Q))
SB = summarise(recB, 'B')

# =====================================================================================
# Part C. Cross-method comparison, completeness / constancy by random points, spot points
# =====================================================================================
stamp('Part C: A vs B cell-by-cell, random completeness sample, spot points')
recA.sort(); recB.sort()
check('A and B records identical cell-by-cell (P,Q,O180,O60,SAT) over all cells', recA == recB,
      f'({len(recA)} vs {len(recB)})')
mapAB = all(A_sign_key[q] == (b, pf) for (b, pf), q in B_sign_Q.items())
check('A combinatorial sign key (b, f-order) == B enumeration key for every Q', mapAB)
del recA

LOOK = {}
for r in recB:
    LOOK[r >> 56] = r & ((1 << 56) - 1)
NR = 150000
rng2 = random.Random(77)
miss = qbad = obad = sbad = 0
nonG = 0
for _ in range(NR):
    al = [rng2.randrange(0, P360, 2) for _ in range(6)]
    if not G['generic'](al):
        nonG += 1
        continue
    P, Q, O180, O60 = labels(al)
    rest = LOOK.get(P)
    if rest is None:
        miss += 1
        continue
    s = cell_sat(G, al)
    if (rest >> 41) != Q:
        qbad += 1
    if ((rest >> 1) & ((1 << 40) - 1)) != ((O180 << 20) | O60):
        obad += 1
    if (rest & 1) != s:
        sbad += 1
check('random points: every P label among the 933120 found (no further resonance cell)',
      miss == 0, f'({NR - nonG} generic points, {miss} new)')
check('random points: sign cell (Q) of point == sign cell of its resonance cell (W_180 subset W_60)',
      qbad == 0, f'({qbad} bad)')
check('random points: cyclic orders mod 60/180 constant on resonance cells', obad == 0, f'({obad} bad)')
check('random points: SAT (all-arc field) constant on resonance cells', sbad == 0, f'({sbad} bad)')

def spot(name, al_frac_num, den):
    Ul = 2 * den * 30              # integer, even, keeps 30-degree cut offsets integral
    Gl = make_geom(Ul)
    al = [x * Ul // den for x in al_frac_num]
    gen = Gl['generic'](al)
    if not gen:
        log(f'  spot {name}: NOT in an open resonance cell (some alpha_i = alpha_j mod 60): wall point')
        return
    P, Q, O180, O60 = Gl['labels'](al)
    s = cell_sat(Gl, al)
    met = SB['satQ'].get(Q, 0)
    log(f'  spot {name}: SAT={s}; its sign cell has {met} SAT resonance cells; '
        f'its base chamber has {SB["satB"].get(O180, 0)}')
    return P, Q, s

spot('(0,30,90,150,240,300)', [0, 30, 90, 150, 240, 300], 1)
r1 = spot('(0,108.75,123.75,142.5,292.5,315)', [0, 435, 495, 570, 1170, 1260], 4)
r2 = spot('(0,60/7,540/7,1020/7,1500/7,1980/7)', [0, 60, 540, 1020, 1500, 1980], 7)
r3 = spot('(0,30.5,90.25,150.75,240.125,300.375) [near hexagon]', [0, 244, 722, 1206, 1921, 2403], 8)

# chart statistic: (mod-180 cyclic order, floor(alpha_i/180) mod 2 modulo diagonal) WITHOUT gauge
def chart_count(rot):
    keys = set()
    for P, al in Bpts.items():
        a0 = al[0]
        al2 = [(x - a0 + rot) % P360 for x in al]
        eps = [x // P180 for x in al2]
        eps = tuple(x ^ eps[0] for x in eps)
        keys.add((labels(al2)[2], eps))
    return len(keys)
ch = {deg: chart_count(deg * U) for deg in (0, 15, 30, 45, 60, 90, 120, 150, 179)}
log(f'  ungauged chart key (cyclic order mod 180, eps mod diag) for the {len(Bpts)} SAT cells, '
    f'distinct keys by global rotation alpha_0 = deg: {ch}')
log(f'  (rotation 0 is the gauge alpha_0 = 0 and must equal the true sign-cell count {SB["sign_met"]})')

# =====================================================================================
# Part E. Desk follow-up: label invariance, wall-free path certificates, naive label
# =====================================================================================
stamp('Part E: path certificates and the ungauged (naive) label')
# (a) Q is a function of the differences (alpha_j - alpha_i) mod 360 only (global-rotation
#     invariant) and changes only when a difference crosses 180Z, i.e. on W_180: constant on
#     components.  Complete: Q determines b_j = floor(beta_j/180) and the order of beta_j mod 180,
#     and that fibre is S^1 x (open convex simplex in the lifted cube (0,360)^5): connected.
def wallfree_path(al, bl, P180=P180, P360=P360):
    """exact certificate of a path al -> bl avoiding W_180: (1) global rotation alpha_0 -> beta_0
    (all differences fixed, so no wall is met); (2) straight segment in beta = alpha - alpha_0
    inside the open cube (0,360)^5; every wall there is an affine hyperplane beta_j = 180 or
    beta_j - beta_k = c, c in {-180,0,180}; nonzero with equal signs at both ends => never hit."""
    b1 = [(al[j] - al[0]) % P360 for j in range(1, 6)]
    b2 = [(bl[j] - bl[0]) % P360 for j in range(1, 6)]
    for j in range(5):
        if b1[j] == 0 or b2[j] == 0 or (b1[j] - P180) * (b2[j] - P180) <= 0:
            return False
    for j in range(5):
        for k in range(j + 1, 5):
            for c in (-P180, 0, P180):
                if (b1[j] - b1[k] - c) * (b2[j] - b2[k] - c) <= 0:
                    return False
    return True

def naive_key(al, Gx, P180x, P360x):
    O180 = Gx['labels'](al)[2]
    eps = [(x % P360x) // P180x for x in al]
    return (O180, tuple(x ^ eps[0] for x in eps))

satpts = list(Bpts.values())
byQ = {}
for al in satpts:
    byQ.setdefault(labels(al)[1], []).append(al)
ncert = sum(1 for q, L in byQ.items() for al in L[1:] if wallfree_path(L[0], al))
nneed = sum(len(L) - 1 for L in byQ.values())
check('every SAT rep is joined to its Q-class first rep by a certified W_180-free path',
      ncert == nneed, f'({ncert}/{nneed} certificates, {len(byQ)} Q classes)')
# (c) all pairs of SAT reps inside one base chamber, naive label of the B points as generated
byB = {}
for al in satpts:
    byB.setdefault(labels(al)[2], []).append(al)
pairs = diffnaive = cert = qdiff = uncovered = 0
for O, L in byB.items():
    nk = [naive_key(al, G, P180, P360) for al in L]
    qs = [labels(al)[1] for al in L]
    for x in range(len(L)):
        for y in range(x + 1, len(L)):
            pairs += 1
            if nk[x] != nk[y]:
                diffnaive += 1
                if qs[x] != qs[y]:
                    qdiff += 1
                elif wallfree_path(L[x], L[y]):
                    cert += 1
                else:
                    uncovered += 1
log(f'  same-base-chamber SAT pairs {pairs}; naive label differs on {diffnaive}; of these '
    f'{cert} joined by certified wall-free path, {qdiff} with different normalised Q, {uncovered} unresolved')
check('decisive check: every naive-label split inside a base chamber is resolved', uncovered == 0)
log(f'  naive label on the B points as generated (random global rotation per cell): '
    f'{len({naive_key(al, G, P180, P360) for al in satpts})} distinct values for the 1440 SAT cells')
# union of all naive labels a SAT cell can show as its global rotation sweeps the circle
allnaive = set()
for al in satpts:
    ev = sorted({(-x) % P180 for x in al} | {(-x) % P180 + P180 for x in al})
    for k in range(len(ev)):
        lo = ev[k]; hi = ev[k + 1] if k + 1 < len(ev) else ev[0] + P360
        rot = (lo + hi) // 2
        allnaive.add(naive_key([(x + rot) % P360 for x in al], G, P180, P360))
log(f'  all naive labels reachable by global rotation of the SAT cells: {len(allnaive)}')
# staircase chart: base phase t = 0, class tau (tau_0 = 0), cut points c_i = 60(rank+1)/7 along the
# crossing order; alpha_i = 60 tau_i + c_i - 30  (one point per (tau, linear order) survivor)
U7 = 1400
G7 = make_geom(U7)
st_pts = []
for order in itertools.permutations(range(6)):
    acc = MASK[0]; Uu = 0
    for x in order[:-1]:
        Uu |= 1 << x; acc &= MASK[Uu]
    for c in bits(acc):
        tau = DEC[c]
        cut = [0] * 6
        for r, i in enumerate(order):
            cut[i] = 60 * U7 * (r + 1) // 7
        al = [(60 * U7 * tau[i] + cut[i] - 30 * U7) % (360 * U7) for i in range(6)]
        st_pts.append((order[0] == 0, al))
st_sat = sum(cell_sat(G7, al) for _, al in st_pts)
st_Q = {G7['labels'](al)[1] for _, al in st_pts}
metQ_scaled = set(SB['satQ'])      # Q is unit-independent (same packing), so directly comparable
check('staircase chart: all 8640 survivor points are geometrically SAT and lie in the met sign cells',
      st_sat == len(st_pts) == 8640 and st_Q <= metQ_scaled, f'({st_sat} SAT, {len(st_Q)} sign cells)')
n_all = len({naive_key(al, G7, 180 * U7, 360 * U7) for _, al in st_pts})
n_0 = len({naive_key(al, G7, 180 * U7, 360 * U7) for f0, al in st_pts if f0})
log(f'  naive label in the staircase chart (t = 0): {n_all} values over all 8640 survivor points, '
    f'{n_0} over the 1440 with crossing order starting at interface 0')

# =====================================================================================
# Part D. Independent topology check in low dimension: grid union-find on T^n
# =====================================================================================
stamp('Part D: grid union-find component counts in T^n, n = 3, 4')
from math import factorial
def uf_count(n, s, m):
    N = 360 // s
    S = s * n; M = m * n
    total = N ** n
    parent = list(range(total))
    def find(x):
        r = x
        while parent[r] != r:
            r = parent[r]
        while parent[x] != r:
            parent[x], x = r, parent[x]
        return r
    strides = [N ** (n - 1 - i) for i in range(n)]
    for idx in range(total):
        rem = idx
        al = []
        for i in range(n):
            k, rem = divmod(rem, strides[i])
            al.append(i + S * k)
        for i in range(n):
            x = al[i]
            ok = True
            for j in range(n):
                if j != i:
                    y0 = x + ((al[j] - x) % S)
                    if (y0 - al[j]) % M == 0:
                        ok = False; break
            if ok:
                k = (x - i) // S
                nb = idx + (((k + 1) % N) - k) * strides[i]
                ra, rb = find(idx), find(nb)
                if ra != rb:
                    parent[ra] = rb
    return len({find(x) for x in range(total)})
for n, steps in ((3, (20, 10, 5)), (4, (20, 15, 12))):
    for m in (60, 180):
        exp = factorial(n - 1) * (360 // m) ** (n - 1)
        got = [uf_count(n, s, m) for s in steps]
        log(f'  n={n} mod {m}: grid steps {steps} deg -> components {got}; (n-1)!*(360/m)^(n-1) = {exp}')
        check(f'grid union-find n={n} mod {m} finest grid == formula', got[-1] == exp)

# =====================================================================================
# Verdicts
# =====================================================================================
stamp('Verdicts')
same = all(SA[k] == SB[k] for k in ('cells', 'distinct_P', 'sign_cells', 'base_chambers', 'nsat',
                                     'base_met', 'sign_met', 'fills', 'mod60_met'))
check('A and B summary counts identical', same)
v = []
v.append(('1 resonance cells = 933120', SB['cells'] == 933120 == SB['distinct_P'] == SA['distinct_P']))
v.append(('2 sign cells = 3840', SB['sign_cells'] == 3840 == SA['sign_cells']))
v.append(('3 base chambers = 120', SB['base_chambers'] == 120 == SA['base_chambers']))
v.append(('4 SAT meets 16 base chambers x 90', SB['nsat'] == 1440 and SB['base_met'] == 16 and
          dict(SB['sat_per_base']) == {90: 16}))
v.append(('5 SAT meets 62 sign cells, fills sum 1440', SB['sign_met'] == 62 and sum(SB['fills']) == 1440))
v.append(('6 720 is not the sign-cell (W_180) or resonance (W_60) met count',
          SB['sign_met'] != 720 and SB['nsat'] != 720 and SB['sign_cells'] != 720))
for name, ok in v:
    log(f'  claim {name}: {"HOLDS" if ok else "DOES NOT HOLD"}')
log(f'  measured: resonance {SB["cells"]}, sign {SB["sign_cells"]}, base {SB["base_chambers"]}, '
    f'SAT {SB["nsat"]}, base met {SB["base_met"]} {dict(SB["sat_per_base"])}, '
    f'sign met {SB["sign_met"]} fills {SB["fills"]}, mod-60 orders met {SB["mod60_met"]} '
    f'{dict(SB["sat_per_mod60"])}, old mod-60 key blocks met {nold}')
nf = sum(1 for _, ok in CHECKS if not ok)
log(f'internal checks: {len(CHECKS) - nf} pass, {nf} fail')
stamp('done')
