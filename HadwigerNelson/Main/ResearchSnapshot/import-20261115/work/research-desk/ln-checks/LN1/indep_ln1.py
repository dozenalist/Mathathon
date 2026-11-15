"""indep_ln1.py -- research-desk independent checker for the L-N1 claims (a), (b), (c).

Written from the DEFINITIONS in RELAXATION-DECISION.md / ln1_referee.py (read as text only;
no lane code is executed or imported).  Stdlib only; run with `python -I indep_ln1.py`.
Optional cross-check against the desk's own independent_census.py (numpy):
    python -P -E indep_ln1.py --xcheck

Model (fixed-phase census), as defined in the lane text:
  * class tau in (Z/6)^6 modulo adding (1,..,1); canonical rep has tau_0 = 0  -> 7776 classes.
  * column j in Z/6, index i in Fin6: sign s_ij = + iff (j - tau_i) mod 6 in {0,1,5}, else -.
    (this is PAT = [1,1,-1,-1,-1,1] indexed by (j - tau_i) mod 6.)
  * P+_j = {i : s_ij = +}, P-_j = {i : s_ij = -};  E_i = {i, i+1};  J(F) = Fin6 \\ U_{i in F} E_i,
    so v in J(F)  <=>  v not in F and v-1 not in F.
  * SAT  <=>  exist Q_0..Q_5 subsets of Fin6 with Q_j meets J(P+_j), Q_j meets J(P-_j), and
    Q_j cap Q_{j+1} = {} cyclically (j+1 mod 6).
Two SAT implementations, different algorithms:
  A: full subset palettes (all 63 nonempty Q), transfer of "set of start palettes" as int bitsets,
     predecessor sets enumerated as submasks of the complement.
  B: two-element palettes Q = {a,b}, a in J(P+), b in J(P-), cyclic DFS with pruning.
"""
import hashlib, itertools, os, sys, time
from collections import Counter

T0 = time.time()
FIN6 = range(6)
PLUS = (0, 1, 5)                      # (j - tau_i) mod 6 in PLUS  <=>  sign +


def canon(t):
    b = t[0]
    return tuple((x - b) % 6 for x in t)


def cls_str(t):
    return "".join(str(x) for x in t)


def parse(s):
    return tuple(int(c) for c in s)


def columns(t):
    """For each column j: (mask of J(P+), mask of J(P-))."""
    out = []
    for j in FIN6:
        plus = [((j - t[i]) % 6) in PLUS for i in FIN6]
        jp = jn = 0
        for v in FIN6:
            if (not plus[v]) and (not plus[(v - 1) % 6]):   # v uncovered by E_i, i in P+
                jp |= 1 << v
            if plus[v] and plus[(v - 1) % 6]:               # v uncovered by E_i, i in P-
                jn |= 1 << v
        out.append((jp, jn))
    return out


# ---------- SAT method A: all nonempty subset palettes ----------
DISJ_BITS = [0] * 64          # DISJ_BITS[Q] = bitset over masks R (1..63) with Q & R == 0
for Q in range(1, 64):
    for R in range(1, 64):
        if Q & R == 0:
            DISJ_BITS[Q] |= 1 << R


def submasks(m):
    s = m
    while s:
        yield s
        s = (s - 1) & m


def sat_A(t):
    cols = columns(t)
    allowed = []
    for jp, jn in cols:
        allowed.append([Q for Q in range(1, 64) if (Q & jp) and (Q & jn)])
        if not allowed[-1]:
            return False
    # S[Q] = bitset of start palettes Q0 from which Q (at the current column) is reachable
    S = {Q: 1 << Q for Q in allowed[0]}
    for j in range(1, 6):
        ok = set(allowed[j])
        nS = {}
        for R, starts in S.items():
            for Q in submasks(63 & ~R):              # Q disjoint from R
                if Q in ok:
                    nS[Q] = nS.get(Q, 0) | starts
        S = nS
        if not S:
            return False
    return any(starts & DISJ_BITS[Q5] for Q5, starts in S.items())


# ---------- SAT method B: two-element palettes, DFS ----------
def sat_B(t):
    cols = columns(t)
    opts = []
    for jp, jn in cols:
        o = [(1 << a) | (1 << b) for a in FIN6 if jp >> a & 1 for b in FIN6 if jn >> b & 1]
        if not o:
            return False
        opts.append(o)

    def dfs(j, prev, first):
        if j == 6:
            return prev & first == 0
        for q in opts[j]:
            if q & prev == 0 and dfs(j + 1, q, first):
                return True
        return False

    return any(dfs(1, q0, q0) for q0 in opts[0])


# ---------- group actions on tuples (then canon) ----------
def act_shift(t):            # constant shift tau -> tau + 1 (the quotient defining classes)
    return tuple((x + 1) % 6 for x in t)


def act_rot(t):              # index rotation: (rot t)_i = t_{i-1}   [RELAXATION-DECISION.md table]
    return canon(tuple(t[(i - 1) % 6] for i in FIN6))


def act_rho(t):              # reflection: (rho t)_i = t_{5-i}         [ln1_referee.py rho()]
    return canon(tuple(t[(5 - i) % 6] for i in FIN6))


def act_neg(t):              # value negation tau -> -tau  (NOT claimed; tested as an extra)
    return canon(tuple((-x) % 6 for x in t))


def orbits(points, gens):
    pts = set(points)
    seen, orbs = set(), []
    for p in sorted(pts):
        if p in seen:
            continue
        orb, stack = {p}, [p]
        while stack:
            x = stack.pop()
            for g in gens:
                y = g(x)
                assert y in pts, ("generator leaves the set", x, y)
                if y not in orb:
                    orb.add(y)
                    stack.append(y)
        seen |= orb
        orbs.append(sorted(orb))
    return orbs                     # ordered by minimal element


def main():
    xcheck = "--xcheck" in sys.argv
    out = []

    def say(*a):
        s = " ".join(str(x) for x in a)
        print(s, flush=True)
        out.append(s)

    verdicts = {}

    def chk(name, cond, extra=""):
        say(("PASS " if cond else "FAIL ") + name + ((" :: " + str(extra)) if extra != "" else ""))
        return cond

    me = os.path.abspath(__file__)
    say("checker:", me)
    say("sha256 :", hashlib.sha256(open(me, "rb").read()).hexdigest())
    say("python :", sys.version.split()[0], " flags isolated=%d" % sys.flags.isolated)

    # ================= census =================
    CL = sorted({canon(t) for t in itertools.product(FIN6, repeat=6)})
    chk("7776 canonical classes", len(CL) == 7776, len(CL))
    SA = {t: sat_A(t) for t in CL}
    t1 = time.time()
    SB_raw = {t: sat_B(t) for t in itertools.product(FIN6, repeat=6)}   # all 46656 raw tuples
    say("[time] sat_A on 7776 classes + sat_B on 46656 raw tuples: %.1fs" % (time.time() - T0))
    chk("method A == method B on all 7776 classes", all(SA[t] == SB_raw[t] for t in CL))
    SAT = sorted(t for t in CL if SA[t])
    SATS = set(SAT)
    chk("177 census-SAT classes", len(SAT) == 177, len(SAT))

    # ================= (a) invariance of SAT under each generator =================
    say("\n=== (a) group actions: invariance of SAT, brute force ===")
    inv_shift = all(SB_raw[t] == SB_raw[act_shift(t)] for t in SB_raw)
    chk("constant shift tau->tau+1: SAT(raw) invariant on all 46656 raw tuples (classes well-defined)", inv_shift)
    gens = {"rot (tau_i -> tau_{i-1})": act_rot, "rho (tau_i -> tau_{5-i})": act_rho,
            "neg (tau -> -tau) [extra, not claimed]": act_neg}
    inv = {}
    for nm, g in gens.items():
        bad = [t for t in CL if SA[t] != SA[g(t)]]
        inv[nm] = not bad
        chk("SAT invariant under %s on all 7776 classes" % nm, not bad, "counterexamples=%d" % len(bad))
    # orders of generators on classes
    def order(g):
        for k in range(1, 13):
            ok = True
            for t in CL:
                x = t
                for _ in range(k):
                    x = g(x)
                if x != t:
                    ok = False
                    break
            if ok:
                return k
    say("orders on the 7776 classes: rot=%d rho=%d neg=%d" % (order(act_rot), order(act_rho), order(act_neg)))
    # dihedral relation rho rot rho = rot^{-1}
    rel = all(act_rho(act_rot(act_rho(t))) == act_rot(act_rot(act_rot(act_rot(act_rot(t))))) for t in CL)
    chk("relation rho.rot.rho = rot^-1 on classes (so <rot,rho> is dihedral of order 12 on indices)", rel)

    O_rho = orbits(SAT, [act_rho])
    O_rot = orbits(SAT, [act_rot])
    O_dih = orbits(SAT, [act_rot, act_rho])
    O_dihn = orbits(SAT, [act_rot, act_rho, act_neg])
    O_neg = orbits(SAT, [act_neg])
    O_rhon = orbits(SAT, [act_rho, act_neg])
    def sz(O):
        return dict(sorted(Counter(len(o) for o in O).items()))
    say("orbits on the 177 SAT classes  (size: count)")
    say("  <rho>            :", len(O_rho), sz(O_rho))
    say("  <rot>            :", len(O_rot), sz(O_rot))
    say("  <rot,rho>  (D6)  :", len(O_dih), sz(O_dih))
    say("  extra <neg>      :", len(O_neg), sz(O_neg))
    say("  extra <rho,neg>  :", len(O_rhon), sz(O_rhon))
    say("  extra <rot,rho,neg>:", len(O_dihn), sz(O_dihn))
    a_ok = (chk("89 rho-orbits, sizes {1,2}", len(O_rho) == 89 and set(sz(O_rho)) == {1, 2}, len(O_rho))
            & chk("35 rot-orbits", len(O_rot) == 35, len(O_rot))
            & chk("18 dihedral orbits, sizes {2,3,4,6,12}",
                  len(O_dih) == 18 and set(sz(O_dih)) == {2, 3, 4, 6, 12}, (len(O_dih), sorted(set(sz(O_dih))))))
    verdicts["a"] = a_ok

    # full scan: which (index permutation pi) x (value map x->a x, a in {1,5}) preserve the SAT set
    say("scan: maps tau -> canon(a * tau o pi^-1), pi in S6, a in {1,-1}, preserving the 177-set")
    stab = []
    for pi in itertools.permutations(FIN6):
        for a in (1, 5):
            def g(t, pi=pi, a=a):
                u = [0] * 6
                for i in FIN6:
                    u[pi[i]] = (a * t[i]) % 6
                return canon(tuple(u))
            if all(g(t) in SATS for t in SAT):      # bijection on classes, so into == onto
                stab.append((pi, a))
    dih_perms = {tuple((s * i + c) % 6 for i in FIN6) for s in (1, -1) for c in FIN6}
    say("  stabiliser size:", len(stab), "; index perms occurring:", len({p for p, _ in stab}),
        "; all of them dihedral (i -> +-i + c):", all(p in dih_perms for p, _ in stab),
        "; value maps occurring:", sorted({a for _, a in stab}))

    # ================= (b) m1 shard =================
    say("\n=== (b) m1 shard ===")
    M1s = ("001234 054322 001344 005322 002335 044311 004332 011244 005332 011344 011334 055332 "
           "012335 044321 013340 043310 013542 023154 022445 055331 023450 054320").split()
    M1 = [parse(w) for w in M1s]
    chk("22 listed, all distinct, all canonical (tau_0=0)", len(set(M1)) == 22 and all(t[0] == 0 for t in M1))
    chk("all 22 census-SAT", all(t in SATS for t in M1), [w for w, t in zip(M1s, M1) if t not in SATS])
    pairs_ok = all(act_rho(M1[2 * k]) == M1[2 * k + 1] for k in range(11))
    chk("listed as 11 rho-pairs (each |-group in the .md is {tau, rho tau})", pairs_ok)
    shard0 = sorted(x for k, o in enumerate(O_rho) if k % 8 == 1 for x in o)
    shard1 = sorted(x for k, o in enumerate(O_rho) if (k + 1) % 8 == 1 for x in o)   # 1-based alt
    b1 = chk("= union of rho-orbits with 0-based index k = 1 mod 8 (orbits ordered by min element)",
             shard0 == sorted(M1), "%d orbits, %d classes" % (sum(1 for k in range(len(O_rho)) if k % 8 == 1), len(shard0)))
    say("  alt reading (1-based index = 1 mod 8): %d classes, equal to m1 list: %s" % (len(shard1), shard1 == sorted(M1)))
    k65 = [k for k, o in enumerate(O_rho) if parse("013542") in o]
    chk("{013542,023154} is rho-orbit #65 (0-based)", k65 == [65] and O_rho[65] == [parse("013542"), parse("023154")], k65)
    dih_id = {x: k for k, o in enumerate(O_dih) for x in o}
    hit = Counter(dih_id[t] for t in M1)
    say("  distribution of the 22 over dihedral orbits (D-orbit#[size]: #shard classes):")
    for k in sorted(hit):
        mem = [cls_str(t) for t in M1 if dih_id[t] == k]
        say("    D%-2d[%2d]: %d  %s" % (k, len(O_dih[k]), hit[k], " ".join(mem)))
    b2 = chk("the 22 classes lie in exactly 8 dihedral orbits", len(hit) == 8, len(hit))
    rot_hit = len({k for k, o in enumerate(O_rot) for t in M1 if t in o})
    say("  (for reference: they meet %d rot-orbits)" % rot_hit)
    verdicts["b"] = b1 and b2 and pairs_ok

    # ================= (c) orbit-65 two-level obstruction =================
    say("\n=== (c) orbit-65 obstruction ===")

    def minus(t, S, d=1):
        u = list(t)
        for i in S:
            u[i] -= d
        return canon(tuple(u))

    c_ok = True
    for w, jstar_claim in (("013542", 3), ("023154", 2)):
        t = parse(w)
        c_ok &= chk(w + " census-SAT", t in SATS)
        l1 = {j: minus(t, [j]) in SATS for j in FIN6}
        sj = [j for j in FIN6 if l1[j]]
        c_ok &= chk(w + " level 1 (tau - e_j): exactly one SAT coordinate, j*=%d" % jstar_claim,
                    sj == [jstar_claim], "SAT j's = %s; classes %s" % (sj, {j: cls_str(minus(t, [j])) for j in FIN6}))
        if len(sj) == 1:
            js = sj[0]
            l2 = {j: minus(t, [js, j]) in SATS for j in FIN6 if j != js}
            c_ok &= chk(w + " level 2 (tau - e_j* - e_j, j != j*): all five UNSAT", not any(l2.values()),
                        {j: (cls_str(minus(t, [js, j])), l2[j]) for j in l2})
        # exhaustive: all 720 generic staircases (decrement order = permutation)
        depth = Counter()
        for p in itertools.permutations(FIN6):
            d, S = 0, []
            for i in p:
                S.append(i)
                if minus(t, S) not in SATS:
                    break
                d += 1
            depth[d] += 1
        c_ok &= chk(w + " exhaustive: none of 720 decrement staircases is all-SAT",
                    depth[6] == 0, "max SAT steps survived: %d; histogram %s" % (max(depth), dict(sorted(depth.items()))))
        # alternative direction (+1 increments): numbers only, information
        l1p = [j for j in FIN6 if minus(t, [j], -1) in SATS]
        surv_p = sum(1 for p in itertools.permutations(FIN6)
                     if all(minus(t, p[:k + 1], -1) in SATS for k in range(6)))
        say("  info, increment direction (tau + e_j): level-1 SAT j's = %s; all-SAT +staircases = %d" % (l1p, surv_p))
        # non-generic staircases (ordered set partitions, ties allowed): survivors by number of blocks
        surv = Counter()
        def ordered_partitions(items):
            if not items:
                yield []
                return
            for r in range(1, len(items) + 1):
                for first in itertools.combinations(items, r):
                    rest = [x for x in items if x not in first]
                    for tail in ordered_partitions(rest):
                        yield [first] + tail
        for P in ordered_partitions(list(FIN6)):
            S, okP = [], True
            for blk in P:
                S += list(blk)
                if minus(t, S) not in SATS:
                    okP = False
                    break
            if okP:
                surv[len(P)] += 1
        say("  info, surviving ordered-partition staircases by #blocks k:", dict(sorted(surv.items())))
    verdicts["c"] = c_ok

    # info: how many SAT classes have at least one all-SAT generic (6-singleton) staircase
    gen_ok = sum(1 for t in SAT if any(all(minus(t, p[:k + 1]) in SATS for k in range(6))
                                       for p in itertools.permutations(FIN6)))
    say("\ninfo (outside scope): SAT classes with >=1 all-SAT generic staircase: %d ; without: %d"
        % (gen_ok, 177 - gen_ok))

    # ================= optional cross-check vs desk census =================
    if xcheck:
        say("\n=== xcheck vs research-desk independent_census.py (numpy, transfer matrices) ===")
        import importlib.util, io, contextlib
        p = r"C:/Users/jarom/Documents/Codex/2026-11-13/i/work/research-desk/census/independent_census.py"
        spec = importlib.util.spec_from_file_location("desk_census", p)
        mod = importlib.util.module_from_spec(spec)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            spec.loader.exec_module(mod)
        their = {mod.decode(c) for c in range(mod.N) if mod.SAT[c]}
        chk("desk census SAT set == this SAT set", their == SATS, (len(their), len(SATS & their)))

    say("\nVERDICTS: " + "  ".join("(%s) %s" % (k, "CONFIRMED" if v else "DISAGREES") for k, v in verdicts.items())
        + "   (d) UNDETERMINED: certificate JSONs not available")
    say("[time] total %.1fs" % (time.time() - T0))


if __name__ == "__main__":
    main()
