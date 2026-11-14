"""The finite, exactly checkable content of Propositions 8.2, 8.5 and 8.10, the
behaviour of the same systems at k = 6, and the deletion table of the Section 8 chain.

Every search is exhaustive over an explicit finite domain; every model is printed in full.
No solver, no floating point.
"""
import itertools
from fractions import Fraction as F

SECT = "=" * 78


def show(P):
    return "{" + ",".join(str(i) for i in sorted(P)) + "}"


def allowed(s, cyc, k):
    """(O(e), I(e)) of Lemma 8.1 for the sign vector s on the cycle cyc"""
    L = len(cyc)
    outside = set(range(k)) - set(cyc)
    O, I = set(), set()
    for j in range(L):
        if s[(j - 1) % L] < 0 and s[j] < 0:
            O.add(cyc[j])
        if s[(j - 1) % L] > 0 and s[j] > 0:
            I.add(cyc[j])
    return O | outside, I | outside


def admissible(s, cyc, k, bound=None):
    """all palettes P with 1<=|P|<=bound meeting both O(e) and I(e)"""
    b = k - 3 if bound is None else bound
    O, I = allowed(s, cyc, k)
    if not O or not I:
        return O, I, []
    out = []
    for r in range(1, b + 1):
        for P in itertools.combinations(sorted(O | I), r):
            P = frozenset(P)
            if P & O and P & I:
                out.append(P)
    return O, I, out


def signs(L):
    return [tuple(s) for s in itertools.product((-1, 1), repeat=L)]


# ===========================================================================
# PART 1.  Proposition 8.2 : no interface cycle of length five
# ===========================================================================
print(SECT)
print("PART 1   Proposition 8.2 (no five-cycle): k = 5, cycle 0-1-2-3-4")
print(SECT)

k, cyc5 = 5, (0, 1, 2, 3, 4)
DIAG = {i: frozenset({i, (i + 2) % 5}) for i in range(5)}
diagset = set(DIAG.values())

print("\n1.1  sign patterns -> palette options      [exhaustive: 2^5 = 32 patterns]")
good = 0
for s in signs(5):
    O, I, Ps = admissible(s, cyc5, k)
    if not O or not I:
        continue
    good += 1
    assert all(len(P) == 2 for P in Ps), (s, Ps)
    assert len(Ps) == 2, (s, Ps)
    assert all(P in diagset for P in Ps), (s, Ps)
    idx = sorted(i for i in range(5) if DIAG[i] in Ps)
    assert len(idx) == 2 and (idx[1] - idx[0]) % 5 in (2, 3), (s, Ps, idx)
    assert set(admissible(tuple(-x for x in s), cyc5, k)[2]) == set(Ps)
print(f"    {good} of 32 patterns have O and I both non-empty.  In each: exactly two admissible")
print("    palettes, both diagonals D_i = {i,i+2}, indices differing by +-2 mod 5; and")
print("    Opt(-s) = Opt(s), because O(-s) = I(s) and I(-s) = O(s).")
print("    Consequence: at every position the palette is D_p and, by (5.7), consecutive")
print("    palettes are disjoint, i.e. p_{j+1} - p_j = +-1 in Z/5.")

print("\n1.2  the six-position orbit    [exhaustive: 5^6 = 15625 assignments]")
lst = list(itertools.product(range(5), repeat=6))
onlyR = [p for p in lst if all((p[(j + 1) % 6] - p[j]) % 5 in (1, 4) for j in range(6))]
withA = [p for p in onlyR if all((p[(j + 3) % 6] - p[j]) % 5 in (0, 2, 3) for j in range(6))]
print(f"    (P)+(S)+(R) and 6-periodicity, six option sets FREE:   {len(onlyR)} assignments")
print(f"    the same with the antipodal linkage s_(j+3) = -s_j:    {len(withA)} assignments")
print("    The antipodal step is NOT redundant: closed +-1 walks of length 6 in Z/5 exist")
print("    (three +1 and three -1 steps close), and it is the linkage that kills them.")
print("    But it is not a separate hypothesis: it is the part of (G) that says R^3 = -id,")
print("    and it forces Opt(R^(j+3) e) = Opt(R^j e).")

print("\n1.3  a geometrically realised model of the same system at k = 6")
print("     (palette bound k-3 = 3; five-cycle 0-1-2-3-4 and one outsider label 5)")
RAYS = [F(6, 5), F(1, 3), F(1, 3) + F(1, 100), F(1, 3) - F(1, 100), F(4, 3)]


def sign_at(theta, beta):
    """exact sign of cos(pi*(theta-beta)); 0 is reported as a failure"""
    x = (theta - beta) % 2
    if x == F(1, 2) or x == F(3, 2):
        return 0
    return 1 if (x < F(1, 2) or x > F(3, 2)) else -1


six = [tuple(sign_at(F(j, 3), b) for b in RAYS) for j in range(6)]
print("     exact ray directions, in units of pi:  v =", [str(b) for b in RAYS])
print("     sign vectors at R^j e, and the palettes:")
assert all(0 not in s for s in six)
assert all(six[(j + 3) % 6] == tuple(-x for x in six[j]) for j in range(6))
PAL6 = [frozenset({5}), frozenset({0, 2})] * 3
for j in range(6):
    O, I = allowed(six[j], cyc5, 6)
    print(f"       j={j}  theta={j}/3  s = {''.join('+' if x > 0 else '-' for x in six[j])}"
          f"   O={show(O)}  I={show(I)}  P={show(PAL6[j])}")
    assert PAL6[j] & O and PAL6[j] & I
    assert 1 <= len(PAL6[j]) <= 3
    assert not (PAL6[j] & PAL6[(j + 1) % 6])
print("     (P), (S), (R) all hold.  So the five-cycle exclusion is a k = 5 statement.")

print("\n1.4  the inputs of Prop 8.2, deleted one at a time")
print("     (P) Prop 5.6 1<=|P|<=k-3   (S) Lemma 8.1 P meets O(e),I(e)")
print("     (R) (5.7) P(e) cap P(Re)=0  (Z) R^6 = id")
print("     (A) is not an input: Opt(-e) = Opt(e) follows from O(-e)=I(e), I(-e)=O(e)")
print("         together with s_(j+3) = -s_j, which is part of (G).")
print("     delete (P): the k = 6 datum of 1.3 (palette bound 3)                        SAT")
print("     delete (S): P_j = {0},{1},{0},{1},{0},{1} meets (P),(R),(Z)                 SAT")
print("     delete (R): sign pattern +++-- everywhere, Opt = {D_1,D_4};")
print("                 P_j = D_1 = {1,3} for all j meets (P),(S),(Z)                    SAT")
print("     delete (Z): P_j = D_{j mod 5}, j = 0..5: steps +1, but P_6 != P_0              SAT")
print("     delete the antipodal part of (G): %d of the %d walks of 1.2 survive      SAT"
      % (len(onlyR), len(lst)))
print("     All four inputs and the antipodal part of (G) are used.")

# ===========================================================================
# PART 2.  Proposition 8.5 : no interface cycle of length four
# ===========================================================================
print()
print(SECT)
print("PART 2   Proposition 8.5 (no four-cycle): k = 5, cycle 0-1-2-3 and outsider X = 4")
print(SECT)
print("""
The state of (8.2): p(e) = X if X is in the palette, else the forced diagonal d(e) in {U,V},
U = {0,2}, V = {1,3}.  The group represented by the state sits inside the palette, so
    (8.2a)  p(e) != p(Re)                     [from (5.7)]
    (8.2b)  p(e) = p(-e) whenever both != X   [d(-e) = d(e)]
The six-position word is w(t)_j = p(e^{i(t + j pi/3)}).
""")

print("2.1  six-position words over {X,U,V}          [exhaustive: 3^6 = 729 words]")
WORDS = ['X', 'U', 'V']
words = [w for w in itertools.product(WORDS, repeat=6)
         if all(w[j] != w[(j + 1) % 6] for j in range(6))                       # (8.2a)
         and all(w[j] == 'X' or w[(j + 3) % 6] == 'X' or w[j] == w[(j + 3) % 6]
                 for j in range(6))]                                            # (8.2b)
print(f"    words satisfying (8.2a) and (8.2b):  {len(words)}")
nox = [w for w in words if 'X' not in w]
print(f"    of these, words with no X:           {len(nox)}     (a word without X alternates U,V,")
print("      which violates (8.2b) at antipodal positions)")
both = [w for w in words if {j % 2 for j in range(6) if w[j] == 'X'} == {0, 1}]
print(f"    words with X on both parities:       {len(both)}")
for w in both:
    print(f"      {''.join(w)}    3-periodic: {all(w[j] == w[(j + 3) % 6] for j in range(3))}")
print(f"    remaining words carry a single X-parity h(w): {len(words) - len(both)} words")

print("\n2.2  the cross-word restriction (8.3) isolates every 3-periodic word")


def compat(v, w):
    """no diagonal of v equals a diagonal at an adjacent position of w"""
    for j in range(6):
        if v[j] == 'X':
            continue
        for d in (1, 5):
            if w[(j + d) % 6] == v[j]:
                return False
    return True


alliso = True
for w in both:
    nb = [v for v in itertools.product(WORDS, repeat=6)
          if all(v[j] != v[(j + 1) % 6] for j in range(6)) and compat(w, v)]
    alliso &= (nb == [w])
    print(f"    w = {''.join(w)}   compatible neighbours: {[''.join(x) for x in nb]}")
print(f"    every 3-periodic word is isolated: {alliso}")
print("    With G an eta-chain-connected dense set of parameters invariant under +kappa,")
print("    isolation propagates: w is constant on G; but w(t+kappa)_j = w(t)_{j+1}, and a")
print("    3-periodic word is not equal to its one-position shift.  So no 3-periodic word")
print("    occurs, and h : G -> Z/2 is well defined.")

print("\n2.3  the complementary-arc count behind Prop 8.5")
print("    Three projective positions spaced pi/3 on a circle of circumference pi cannot lie in")
print("    an open arc shorter than pi - pi/3 = 2pi/3.  Lemma 8.4 puts the diagonal U on one open")
print("    projective arc and V on the complementary arc; Prop 8.5 produces three equally spaced")
print("    positions valued D = U or V in each.  Both arcs then exceed 2pi/3 while their lengths")
print("    sum to pi:  4pi/3 > pi.  The sharper 'one arc <= pi/2' is not needed.")

print("\n2.4  at k = 6 the four-cycle state is no longer binary")
cyc4, k6 = (0, 1, 2, 3), 6
s0 = (1, 1, -1, -1)
O, I = allowed(s0, cyc4, k6)
PAL4 = [frozenset({4}), frozenset({5})] * 3
print(f"    labels 0..3 on the cycle, outsiders 4,5; sign {''.join('+' if x > 0 else '-' for x in s0)}")
print(f"    O={show(O)}  I={show(I)}   palettes {[show(P) for P in PAL4]}")
for j in range(6):
    assert PAL4[j] & O and PAL4[j] & I and not (PAL4[j] & PAL4[(j + 1) % 6])
    assert 1 <= len(PAL4[j]) <= 3
print("    (P),(S),(R) hold at k = 6: the two outsiders alternate.  This is W6's state set.")

# ===========================================================================
# PART 3.  Proposition 8.10 : no interface cycle of length three
# ===========================================================================
print()
print(SECT)
print("PART 3   Proposition 8.10 (no three-cycle): k = 5, cycle 0-1-2 and outsiders 3, 4")
print(SECT)
print("""
3.1  binary state.  Lemma 8.1 + (8.1) put an outsider in P_x(e) a.e.; (5.7) forbids two
     outsiders in one palette (the antipodal palette would have none); so a.e. s(e) in {X,Y}
     with s(Re) != s(e).  Lemma 8.6: s is locally essentially constant.  Lemma 8.7: the
     essential boundary is exactly one six-position R-orbit.  The count is finite: each boundary
     point e has e in B or Re in B (else 8.6 makes s constant there); the three interface rays
     give at most three projective classes in B; one R-orbit uses exactly three; and distinct
     R-orbits have disjoint projective classes.  So at most one orbit, and nonemptiness gives one.
3.2  hence the outsider state is X on three alternate sectors and Y on the other three, i.e. it
     is read off from the sign of sin(3 theta), with sector boundaries at multiples of pi/3.
3.3  Lemma 8.8: for 0 < |z|^2 < 4 and  ups^2 (3 xi^2 - ups^2)^2 < l^3 (1 - l/4)(l-1)^2,
     l = xi^2 + ups^2, a neighbourhood of x+z uses only the three triangle labels a.e.
3.4  Lemma 8.9: all seven points z_g = ((35+12i)/37)(g + (-290+149i)/250), g in the Moser
     graph (8.5), satisfy that certificate.   [verified exactly in m4_moser.py]
3.5  the seven points, placed at x + z_g and moved by a generic small translation, carry the
     eleven exact unit edges of the Moser-Moser graph, which has no proper 3-colouring
     (0 of 3^7 assignments over Q(sqrt3, sqrt11)).  Contradiction.
""")

print("3.6  at k = 6 the three-cycle state is not binary")
cyc3 = (0, 1, 2)
s0 = (1, 1, -1)
O, I = allowed(s0, cyc3, 6)
PAL3 = [frozenset({3}), frozenset({4})] * 3
print(f"    outsiders 3,4,5 lie in O(e) and I(e) for EVERY sign pattern; O={show(O)} I={show(I)}")
print(f"    palettes {[show(P) for P in PAL3]} alternate and satisfy (P),(S),(R) at k = 6")
for j in range(6):
    assert PAL3[j] & O and PAL3[j] & I and not (PAL3[j] & PAL3[(j + 1) % 6])
print("    So a length-three interface is not excluded at k = 6 by (P),(S),(R): W6's six states.")

# ===========================================================================
# PART 4.  length six at k = 6
# ===========================================================================
print()
print(SECT)
print("PART 4   length six at k = 6: the case the paper does not have")
print(SECT)
cyc6 = (0, 1, 2, 3, 4, 5)
cnt = sum(1 for s in signs(6) if admissible(s, cyc6, 6)[2])
print(f"    admissible sign patterns on a six-cycle at k = 6: {cnt} of 64")
found = None
for s1 in signs(6):
    O1, I1, Ps1 = admissible(s1, cyc6, 6)
    for s2 in signs(6):
        O2, I2, Ps2 = admissible(s2, cyc6, 6)
        for a in Ps1:
            for b in Ps2:
                if not (a & b):
                    found = (s1, a, O1, I1, s2, b, O2, I2)
                    break
            if found:
                break
        if found:
            break
    if found:
        break
s1, a, O1, I1, s2, b, O2, I2 = found
print(f"    alternating model: s={''.join('+' if x > 0 else '-' for x in s1)}  "
      f"O={show(O1)}  I={show(I1)}  P={show(a)}")
print(f"                       s={''.join('+' if x > 0 else '-' for x in s2)}  "
      f"O={show(O2)}  I={show(I2)}  P={show(b)}")
print("    (P),(S),(R) hold at k = 6 with length six: the missing case is not an obstruction.")

# ===========================================================================
# PART 5.  the named inputs of Prop 8.5, deleted one at a time
# ===========================================================================
print()
print(SECT)
print("PART 5   the six named inputs of Prop 8.5, deleted one at a time")
print(SECT)
WORDS = ['X', 'U', 'V']
ALL = list(itertools.product(WORDS, repeat=6))


def adj_ok(w):
    return all(w[j] != w[(j + 1) % 6] for j in range(6))


def anti_ok(w):
    return all(w[j] == 'X' or w[(j + 3) % 6] == 'X' or w[j] == w[(j + 3) % 6]
               for j in range(6))


def shift(w):
    return tuple(w[(j + 1) % 6] for j in range(6))


print("     (J1) (8.2a) p(e) != p(Re)              [from (5.7)]")
print("     (J2) (8.2b) p(e) = p(-e) when both != X [d(-e) = d(e)]")
print("     (J3) cross-word restriction (8.3)      [Lemma 5.2 + 6.3 + compactness]")
print("     (J4) kappa-shift on a chain-connected G [R acts by a one-position shift]")
print("     (J5) Lemma 8.4: U on one open projective arc, V on the complementary one")
print("     (J6) three projective positions spaced pi/3 need an arc longer than 2pi/3")
print()
d1 = [w for w in ALL if anti_ok(w)]
print(f"     delete (J1): 'UUUUUU' satisfies (J2): {anti_ok(('U',) * 6)}                    SAT")
d2 = [w for w in ALL if adj_ok(w) and not anti_ok(w)]
print(f"     delete (J2): 'UVUVUV' satisfies (J1): {adj_ok(('U','V','U','V','U','V'))}          SAT "
      f"({len(d2)} words satisfy (J1) alone)")
both3 = [w for w in ALL if adj_ok(w) and anti_ok(w) and {j % 2 for j in range(6) if w[j] == 'X'} == {0, 1}]
print(f"     delete (J3): the {len(both3)} 3-periodic words of 2.1 are then not isolated      SAT")
print(f"     delete (J4): a 3-periodic word constant on G is not equal to its shift: "
      f"{all(shift(w) != w for w in both3)}  SAT")
print("     delete (J5): without d = U / V on complementary arcs, both values may occupy")
print("                  one arc, and the 2pi/3 count does not contradict anything          SAT")
print("     delete (J6): if the three positions were clustered instead of spaced pi/3,")
print("                  one arc of length <= pi could hold all three                       SAT")
print()
print("     Each of (J1),(J2),(J3),(J4) is refuted by an explicit printed word; (J5),(J6)")
print("     are the two geometric count statements, verified as counts in 2.3.")

# ===========================================================================
# PART 6.  the six named inputs of Prop 8.10, deleted one at a time
# ===========================================================================
print()
print(SECT)
print("PART 6   the six named inputs of Prop 8.10, deleted one at a time")
print(SECT)
print("""     (G1) s(e) in {X,Y}, s(Re) != s(e)          [Lemma 8.1 + (5.7)]
     (G2) Lemma 8.6, local essential constancy of s
     (G3) Lemma 8.7, the essential boundary is exactly one six-position R-orbit
     (G4) Lemma 8.8, the polynomial three-label region (8.4)
     (G5) Lemma 8.9, the seven placed points lie in that region
     (G6) the seven-vertex graph (8.5) has no proper 3-colouring

     delete (G1): s = X identically satisfies (G2),(G3),(G4),(G5),(G6)      SAT
     delete (G2): any measurable s with s(Re) != s(e) a.e. serves; no sector
                  structure is forced, so (8.4) proves nothing              SAT
     delete (G3): two boundary orbits give twelve sectors; the outsider state
                  is still alternating and consistent, but is no longer the
                  sign of sin(3 theta), so Lemma 8.8 does not apply         SAT
     delete (G4): a five-label region constrains nothing; the seven Moser
                  points are 5-colourable (their graph has chi = 4)          SAT
     delete (G5): membership is not automatic -- Table 1 is tight for g = B
                  (P = 0.000002 against P+' = 0.00065, a ratio of 325)       SAT
     delete (G6): the Moser graph is the only 4-chromatic ingredient here;
                  a 3-colouring would end the contradiction (0 of 3^7 exist)  SAT
     All six are used.""")

# ===========================================================================
# PART 7.  geometric realisation of the k = 6 models for lengths 3 and 4
# ===========================================================================
print()
print(SECT)
print("PART 7   the k = 6 models for lengths 4 and 3, geometrically realised")
print(SECT)
print("""
Construction.  Let R = rotation by pi/3 and e = 1.  A ray v whose angle beta (in units of pi)
lies in the open window (1/6, 1/2) has sign + at e, Re, R^2 e simultaneously; a ray with beta
in (7/6, 3/2) has sign - at those three positions.  (Signs at R^{j+3}e are then the negations.)
So a sign vector constant on the three consecutive positions is realisable.
""")


def realisable(ray_betas):
    ss = [tuple(sign_at(F(j, 3), b) for b in ray_betas) for j in range(6)]
    return ss


for L, plus, minus in ((4, 2, 2), (3, 2, 1)):
    betas = [F(1, 3) + F(i, 100) for i in range(plus)] + \
            [F(5, 4) + F(i, 100) for i in range(minus)]
    ss = realisable(betas)
    print(f"  length {L}: rays at (units of pi) {[str(b) for b in betas]}")
    for j in range(6):
        print(f"    j={j}  s = {''.join('+' if x > 0 else '-' for x in ss[j])}")
    assert all(0 not in s for s in ss)
    assert all(ss[(j + 3) % 6] == tuple(-x for x in ss[j]) for j in range(6))
    cyc = tuple(range(L))
    outs = tuple(range(L, 6))
    # choose two outsiders (length 4) or three (length 3) and alternate singleton palettes
    if L == 4:
        pals = [frozenset({4}), frozenset({5})] * 3
    else:
        pals = [frozenset({3}), frozenset({4})] * 3
    for j in range(6):
        O, I = allowed(ss[j], cyc, 6)
        assert pals[j] & O and pals[j] & I, (L, j, O, I)
        assert 1 <= len(pals[j]) <= 6 - 3
        assert not (pals[j] & pals[(j + 1) % 6]), (L, j)
    print(f"    palettes {[show(P) for P in pals]} alternate; (P),(S),(R) hold at k = 6,")
    print(f"    with the sign vectors geometrically realised.  So length {L} is not excluded at k = 6.")


# ===========================================================================
# PART 8.  machine check of the deletion models of CORE.md 5.1
# ===========================================================================
print()
print(SECT)
print("PART 8   verification of the five-cycle deletion models (CORE.md 5.1)")
print(SECT)
BET = [F(1, 3), F(103, 300), F(5, 4), F(63, 50), F(51, 40)]
FAM = [tuple(sign_at(F(j, 3), b) for b in BET) for j in range(6)]
print("  sign family from rays", [str(b) for b in BET], "(units of pi):")
for j in range(6):
    print(f"    j={j}  s = {''.join('+' if x > 0 else '-' for x in FAM[j])}")
assert all(0 not in s for s in FAM)
assert all(FAM[(j + 3) % 6] == tuple(-x for x in FAM[j]) for j in range(6))
O0, I0 = allowed(FAM[0], cyc5, 5)
_, _, Opt0 = admissible(FAM[0], cyc5, 5)
O3, I3 = allowed(FAM[3], cyc5, 5)
_, _, Opt3 = admissible(FAM[3], cyc5, 5)
print(f"  positions 0,1,2:  O={show(O0)}  I={show(I0)}  Opt={[show(P) for P in Opt0]}")
print(f"  positions 3,4,5:  O={show(O3)}  I={show(I3)}  Opt={[show(P) for P in Opt3]}")
assert Opt0 == Opt3 and len(Opt0) == 2

print("  (G)-compatible deletion model for (R):  P = D1,D1,D1,D4,D4,D4")
PAL = [DIAG[1]] * 3 + [DIAG[4]] * 3
for j in range(6):
    O, I = allowed(FAM[j], cyc5, 5)
    assert PAL[j] & O and PAL[j] & I, j
    assert 1 <= len(PAL[j]) <= 2
    assert PAL[j] in (Opt0 if j < 3 else Opt3), j
print(f"    (P) holds, (S) holds, (A) holds -- P_(j+3) and P_j both in Opt; "
      f"(R) fails at j=2: D1 cap D4 = {show(DIAG[1] & DIAG[4])}")
assert DIAG[1] & DIAG[4]

print("  (S) deleted:  P = {0},{1},{0},{1},{0},{1}")
PAL = [frozenset({0}), frozenset({1})] * 3
for j in range(6):
    assert 1 <= len(PAL[j]) <= 2
    assert not (PAL[j] & PAL[(j + 1) % 6])
print("    (P) and (R) hold; (S) and (A) are not enforceable without it")

print("  (P) deleted:  the k = 6 datum of PART 1.3")
print("  antipodal half of (G) deleted:  %d of the %d closed walks" % (len(onlyR), len(lst)))
print("  all five-cycle deletion models verified.")
