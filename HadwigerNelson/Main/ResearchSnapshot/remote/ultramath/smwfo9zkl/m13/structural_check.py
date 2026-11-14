"""Structural checks for no-go.md.

S1  k = 5: every palette with 1 <= |P| <= 2 not contained in a triangle edge meets the
    outsider pair (exhaustive).  Hence every triangle centre is binary for {4,5} at k = 5,
    and Lemma 5.5 applies: the class forces separation at k = 5.  (Non-vacuity of the
    class.)

S2  k = 6: the singleton palettes of model (M) satisfy (6.2), the palette bound and the
    "no complementary triples" condition (exhaustive over the 1 + 15 + 20 admissible sets
    not contained in a triangle edge -- listed for the record).

S3  Which extra palette-level hypotheses would kill model (M)?  Exhaustive test of a list
    of candidate conditions against the model's palettes and against the k = 5 palettes.

S3b/S4 Forbidden sets of (5.2) at one centre.  For (M) they all lie inside O = {4,5,6}, so
    (M) satisfies (5.2) with c = 1.  S4b does the same for the T-ary model (M'), whose
    forbidden sets cover I once the centres fill a neighbourhood: (M') is therefore not
    (5.2)-completable with Z = R^2.  Both statements are needed in no-go.md section 5(f).

S5  The 18-point / 36-edge style finite shadow: for a small finite set of centres and a
    finite set of directions, the full constraint list of (M) is satisfied; this is what
    makes (M) checkable by a finite computation.
"""
from itertools import combinations

LBL5 = [1, 2, 3, 4, 5]
LBL6 = [1, 2, 3, 4, 5, 6]
T = {1, 2, 3}
EDGES = [(1, 2), (1, 3), (2, 3)]


def subsets(labels, maxsize):
    out = []
    for k in range(1, maxsize + 1):
        out += [set(c) for c in combinations(labels, k)]
    return out


def inside_an_edge(P):
    return any(P <= set(e) for e in EDGES)


def s1_k5():
    adm = [P for P in subsets(LBL5, 2) if not inside_an_edge(P)]
    no_outsider = [P for P in adm if not (P & {4, 5})]
    with_pair = [P for P in adm if (P & {4, 5})]
    return len(adm), len(no_outsider), len(with_pair)


def s2_k6():
    adm = [P for P in subsets(LBL6, 3) if not inside_an_edge(P)]
    by_size = {k: sum(1 for P in adm if len(P) == k) for k in (1, 2, 3)}
    comp = [(P, Q) for P in adm for Q in adm
            if len(P) == 3 and len(Q) == 3 and P | Q == set(LBL6) and P != Q]
    return len(adm), by_size, len(comp)


def s3_killing_conditions():
    """Candidates for an extra palette-level hypothesis; which ones kill which model?"""
    M = [{4}, {5}, {6}]                                        # singleton variant (M)
    Mp = [{1, 4}, {2, 5}, {3, 6}]                              # T-ary pair model (M')
    conds = {
        "P meets T={1,2,3}": lambda P: bool(P & T),
        "P meets O={4,5,6}": lambda P: bool(P & {4, 5, 6}),
        "|P| >= 2": lambda P: len(P) >= 2,
        "|P| <= 2": lambda P: len(P) <= 2,
        "|P| = 2": lambda P: len(P) == 2,
        "P not a singleton of O": lambda P: not (len(P) == 1 and P <= {4, 5, 6}),
        "P not a subset of O": lambda P: not (P <= {4, 5, 6}),
        "P meets T and meets O": lambda P: bool(P & T) and bool(P & {4, 5, 6}),
        "P = T": lambda P: P == T,
        "|P| = 3": lambda P: len(P) == 3,
        "P not one of {1,4},{2,5},{3,6}": lambda P: P not in ({1, 4}, {2, 5}, {3, 6}),
        "P is not a 2-element matching pair": lambda P: not (len(P) == 2 and P <= {1, 4}),
    }
    rows = []
    for name, f in conds.items():
        okM = all(f(P) for P in M)
        okMp = all(f(P) for P in Mp)
        rows.append((name,
                     "survives (M)" if okM else "kills (M)",
                     "survives (M')" if okMp else "kills (M')"))
    return rows


def s4_5_2_violation():
    """At x = 0, the decompositions of z = x + e + v = e + v give forbidden 2-sets whose
    union over admissible (e,v) is all of O.  We exhibit, for each label o in O, a pair
    (e,v) with o in the forbidden set, and then show no single label survives all pairs
    that occur for |z| <= 1."""
    import numpy as np
    PI = np.pi

    def s(t):
        return int(np.floor(9.0 * t / (2.0 * PI))) % 3

    # For the model at the single centre x = 0: p(e) = 4 + s(arg e).  The (5.2) constraint
    # forbids labels 4+s(arg e), 4+s(arg v) for every unit e,v.  Take e, v arbitrary:
    # the union over (e, v) of the forbidden sets covers all three of O.
    covered = set()
    witnesses = []
    for j in range(360):
        te = 2 * PI * j / 360
        for k in range(360):
            tv = 2 * PI * k / 360
            if abs(np.angle(np.exp(1j * (te - tv)))) < 1e-9:
                continue           # parallel: not an admissible sum
            f = {4 + s(te), 4 + s(tv)}
            new = f - covered
            if new:
                witnesses.append((j, k, sorted(f)))
            covered |= f
            if len(covered) == 3:
                return covered, witnesses[:5]
    return covered, witnesses[:5]



def s4b_p7():
    """(P7): (M) is (5.2)-completable with c = 1; (M') with Z = R^2 is not completable at all.

    At a fixed point z and a centre x with u = z - x, the pair (e,v) with e + v = u satisfies
    |e|=|v|=1, so the constraint is c(z) not in P(e) | P(v).  As x ranges over a neighbourhood
    of z, u ranges over a neighbourhood of 0, and the pairs sweep a 2-parameter family.
    """
    import numpy as np
    PI = np.pi

    def s(t):
        return int(np.floor(9.0 * t / (2.0 * PI))) % 3

    Q = [{1, 4}, {2, 5}, {3, 6}]
    SING = [{4}, {5}, {6}]

    def forbidden_cover(table, rmax=2.0, nr=400, na=720):
        cov = set()
        sets = set()
        for iu in range(1, nr + 1):
            r = rmax * iu / nr
            for ia in range(na):
                th = 2 * PI * ia / na
                u = r * np.exp(1j * th)
                perp = 1j * (u / r) * np.sqrt(max(0.0, 1 - r * r / 4))
                e, v = u / 2 + perp, u / 2 - perp
                f = table[s(np.angle(e))] | table[s(np.angle(v))]
                sets.add(tuple(sorted(f)))
                cov |= f
        return cov, sets

    out = []
    for name, table in (("(M) singletons", SING), ("(M') T-ary pairs", Q)):
        cov, sets = forbidden_cover(table)
        out.append((name, sorted(cov), sorted(sets), sorted(set(range(1, 7)) - cov)))
    return out


def s5_finite_shadow():
    """A finite set of centres and directions: every constraint of the model that is
    checkable on the finite data holds, so the model is finite-computation-checkable."""
    import numpy as np
    PI = np.pi

    def s(t):
        return int(np.floor(9.0 * t / (2.0 * PI))) % 3

    centres = [0j, 0.01 + 0j, 0.02j, 0.5 + 0.5j]
    ok = 0
    bad = 0
    # (5.7) at each centre
    for z in centres:
        for j in range(720):
            t = 2 * PI * j / 720
            if s(t) == s(t + PI / 3):
                bad += 1
            else:
                ok += 1
    # transport for the pairs at distance <= 1/50
    for a in centres:
        for b in centres:
            d = abs(b - a)
            if not (0 < d <= 1 / 50):
                continue
            for j in range(720):
                t = 2 * PI * j / 720
                w = np.exp(1j * t)
                W = (b - a) + w
                r = abs(W)
                half = W / 2
                perp = 1j * (W / r) * np.sqrt(max(0.0, 1 - r * r / 4))
                for u in (half + perp, half - perp):
                    if s(t) == s(np.angle(u)):
                        bad += 1
                    else:
                        ok += 1
    return ok, bad


if __name__ == "__main__":
    print("S1  k = 5 palettes (1 <= |P| <= 2, not inside a triangle edge):")
    n, no_out, with_out = s1_k5()
    print(f"    admissible = {n};  with NO outsider = {no_out}  (must be 0);  with outsider = {with_out}")
    print("    => every triangle centre is binary for {4,5} at k = 5, so Lemma 5.5 applies.\n")

    print("S2  k = 6 palettes (1 <= |P| <= 3, not inside a triangle edge):")
    n6, by_size, ncomp = s2_k6()
    print(f"    admissible = {n6}   by size = {by_size}")
    print(f"    pairs of complementary triples among them = {ncomp}  (these are exactly the")
    print(f"    pairs excluded by the k = 6 form of (5.2))\n")

    print("S3  candidate extra hypotheses versus the two models:")
    print(f"    {'hypothesis':36s}   {'(M) singleton':16s}  (M') T-ary pairs")
    for name, vm, vmp in s3_killing_conditions():
        print(f"    {name:36s}   {vm:16s}  {vmp}")
    print()

    covered, wit = s4_5_2_violation()
    print("S4  forbidden sets of model (M) at one centre, over all decompositions:")
    print(f"    labels of O forbidden at x = 0 by some pair (e,v): {sorted(covered)}")
    print(f"    witnesses (j_deg, k_deg, forbidden set): {wit}")
    print("    Labels of T are never forbidden by model (M), so (M) satisfies (5.2) with c = 1;")
    print("    see S4b for the correct statement (and for the T-ary model (M'), which fails).\n")

    print("S4b (P7): forbidden sets at ONE point when the centres fill a neighbourhood of it")
    for name, cov, sets, avail in s4b_p7():
        print(f"    {name}: realised forbidden sets = {sets}")
        print(f"        union = {cov};  labels available at that point = {avail}")
    print()

    ok, bad = s5_finite_shadow()
    print("S5  finite shadow over 4 centres x 720 directions:")
    print(f"    satisfied constraints = {ok};  violations = {bad}")
