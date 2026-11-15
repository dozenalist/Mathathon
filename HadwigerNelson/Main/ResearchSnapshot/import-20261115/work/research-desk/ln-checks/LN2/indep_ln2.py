#!/usr/bin/env python3
"""indep_ln2.py -- independent exact checker for the L-N2 claims:
  (I)  m7's three-centre palette/trace field at k = 6 on the unit triangle A=0, B=1, C=1/2+(sqrt3/2)i
       (claims 1-7 of the research-desk brief, incl. the 19 constraints of the lane's model_check.py);
  (II) the stated finite facts of the Step-1 ladder LADDER-k6.md.

Written from scratch.  The lane files (model_check.py, ladder_k6.py, LADDER-k6.md) and the Lean
sources are READ AS TEXT ONLY (to extract the model data, the 19 check ids and the exact constraint
statements); nothing of theirs is imported or executed.  stdlib only; exact arithmetic only
(Fractions, and a+b*sqrt3 with Fraction a,b).  Floats are never used for a decision; an 80-digit
Decimal evaluation is used only to cross-validate the exact sign routine.

Deliberate differences from the lane's checker:
  * Q(sqrt3) is a class with an independently written sign test, cross-validated on random and
    Pell-type near-zero elements against 80-digit Decimal evaluation.
  * Sector boundaries and centre directions are GENERATED as powers of the exact rotation
    R = [[1/2,-sqrt3/2],[sqrt3/2,1/2]] (not tabulated); R is verified to be the rotation by pi/3
    (cos 1/2, sin > 0, det 1, order exactly 6) and each sector is verified to be an open arc of
    length exactly pi/3 (consecutive boundaries have dot 1/2 and positive cross).
  * Sector membership of a direction is decided by an exact classifier.  "f in sector j  =>
    f+pi/3 in sector j+1 (mod 6)" is PROVED exactly (R maps boundary j to boundary j+1, det R = 1,
    so cross signs are preserved) and is also exercised on exact sample directions (rational
    Pythagorean points and their R-images, which have sqrt3 coordinates).
  * The unit-distance centre pairs used by (TE) are DISCOVERED by searching x + dir(j) over the
    centres, not listed by hand.
  * BinaryCenter is evaluated with the Lean definition (a.e. t: i in P(t) or j in P(t)) as well as
    with the lane's reading (P(t) subset {i,j} a.e.).
"""
import sys, time, hashlib, os, re, random
from fractions import Fraction as F
from itertools import combinations
from decimal import Decimal, getcontext

T0 = time.perf_counter()
try:
    sys.stdout.reconfigure(encoding="utf-8")      # Lean text contains non-ASCII symbols
except Exception:
    pass
SELF_SHA = hashlib.sha256(open(os.path.abspath(__file__), "rb").read()).hexdigest()

WORK = "C:/Users/jarom/Documents/Codex/2026-11-13/i/work"
INBOX = WORK + "/automation-supervisor/inbox"
LANE_MODEL = INBOX + "/20261115T025639-download-3-model_check.py"
LANE_LADDER_PY = INBOX + "/20261115T025639-download-2-ladder_k6.py"
LANE_LADDER_MD = INBOX + "/20261115T025639-download-5-LADDER-k6.md"
LEAN_TREES = [
    WORK + "/encoding-integration/full-original/OAI/Geometry/PlaneColoring",
    WORK + "/lean-queue/encoding-r4/src/OAI/Geometry/PlaneColoring",
    WORK + "/lean-queue/threecentre-r1/src/OAI/Geometry/PlaneColoring",
    WORK + "/lean-queue/threecentre-integration/src/OAI/Geometry/PlaneColoring",
    WORK + "/simplification-desk/s1/OAI/Geometry/PlaneColoring",
    WORK + "/simplification-desk/s2/OAI/Geometry/PlaneColoring",
]

RESULTS = []          # (tag, status, detail)


def out(*a):
    print(*a, flush=True)


def verdict(tag, status, detail):
    RESULTS.append((tag, status, detail))
    out(f"  => {tag}: {status}  [{detail}]")


def S(it):
    """canonical printable set"""
    return "{" + ",".join(str(v) for v in sorted(it)) + "}"


def read_text(path):
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
        return raw, raw.decode("utf-8", errors="replace")
    except OSError:
        return None, None


# =============================================================================== Q(sqrt3)
class Q3:
    """a + b*sqrt(3), a, b Fractions."""
    __slots__ = ("a", "b")

    def __init__(self, a=0, b=0):
        self.a = F(a)
        self.b = F(b)

    def __add__(self, o):
        o = q(o); return Q3(self.a + o.a, self.b + o.b)
    __radd__ = __add__

    def __sub__(self, o):
        o = q(o); return Q3(self.a - o.a, self.b - o.b)

    def __rsub__(self, o):
        return q(o) - self

    def __mul__(self, o):
        o = q(o); return Q3(self.a * o.a + 3 * self.b * o.b, self.a * o.b + self.b * o.a)
    __rmul__ = __mul__

    def __neg__(self):
        return Q3(-self.a, -self.b)

    def __eq__(self, o):
        o = q(o); return self.a == o.a and self.b == o.b

    def __hash__(self):
        return hash((self.a, self.b))

    def sign(self):
        a, b = self.a, self.b
        sa = (a > 0) - (a < 0)
        sb = (b > 0) - (b < 0)
        if sb == 0:
            return sa
        if sa == 0:
            return sb
        if sa == sb:
            return sa
        d = a * a - 3 * b * b           # != 0 since sqrt3 is irrational and a, b != 0
        assert d != 0
        return sa if d > 0 else sb      # |a| > |b|sqrt3  <=>  a^2 > 3 b^2

    def __repr__(self):
        if self.b == 0:
            return str(self.a)
        return f"({self.a}{'+' if self.b >= 0 else '-'}{abs(self.b)}*r3)"


def q(v):
    return v if isinstance(v, Q3) else Q3(v)


R3H = Q3(0, F(1, 2))                    # sqrt3/2


def V(x, y):
    return (q(x), q(y))


def vadd(u, v): return (u[0] + v[0], u[1] + v[1])
def vsub(u, v): return (u[0] - v[0], u[1] - v[1])
def cross(u, v): return u[0] * v[1] - u[1] * v[0]
def dot(u, v): return u[0] * v[0] + u[1] * v[1]
def veq(u, v): return u[0] == v[0] and u[1] == v[1]


COS60, SIN60 = Q3(F(1, 2)), R3H


def rot(v):
    return (COS60 * v[0] - SIN60 * v[1], SIN60 * v[0] + COS60 * v[1])


def rotn(v, n):
    for _ in range(n % 6):
        v = rot(v)
    return v


out("=" * 96)
out("indep_ln2.py  --  independent exact checker, L-N2 (m7 palette/trace field at k=6 + Step-1 ladder)")
out("self sha256:", SELF_SHA)
out("=" * 96)

# ----------------------------------------------------------------------- [0] exact sign validation
out("\n[0] Validating the exact sign routine of Q(sqrt3) against 80-digit Decimal evaluation")
getcontext().prec = 80
SQRT3_D = Decimal(3).sqrt()


def dec(x):
    return (Decimal(x.a.numerator) / Decimal(x.a.denominator)
            + Decimal(x.b.numerator) / Decimal(x.b.denominator) * SQRT3_D)


rng = random.Random(20261115)
tests = []
for _ in range(6000):
    tests.append(Q3(F(rng.randint(-90, 90), rng.randint(1, 40)), F(rng.randint(-90, 90), rng.randint(1, 40))))
a_, b_ = 2, 1                           # Pell solutions a^2 - 3 b^2 = 1: hardest near-zero cases
for _ in range(12):
    for sa in (1, -1):
        for sb in (1, -1):
            tests.append(Q3(sa * a_, sb * b_))
            tests.append(Q3(sa * a_ * F(1, 7), sb * b_ * F(1, 7)))
    a_, b_ = 2 * a_ + 3 * b_, a_ + 2 * b_
nbad = sum(1 for x in tests if x.sign() != ((dec(x) > 0) - (dec(x) < 0)))
out(f"  {len(tests)} elements (incl. 96 Pell-type a^2-3b^2=1 near-zero cases up to a~1e7): mismatches = {nbad}")
assert nbad == 0

# ----------------------------------------------------------------------- [1] rotation and sectors
out("\n[1] Rotation by pi/3 and the six sectors, generated exactly")
I2 = (V(1, 0), V(0, 1))
assert COS60 * COS60 + SIN60 * SIN60 == 1                      # unit: det R = cos^2 + sin^2 = 1
assert COS60 == F(1, 2) and SIN60.sign() > 0                   # cos = 1/2, sin > 0  => angle pi/3
orders = [k for k in range(1, 7) if veq(rotn(V(1, 0), k), V(1, 0)) and veq(rotn(V(0, 1), k), V(0, 1))]
out(f"  R: cos = 1/2, sin = sqrt3/2 > 0, det = 1; R^k = I for k in 1..6 only at k = {orders}")
assert orders == [6]
BETA0 = V(R3H, F(-1, 2))                                        # candidate boundary at angle -pi/6
assert dot(BETA0, BETA0) == 1
mid = vadd(BETA0, rot(BETA0))                                   # bisector of arc [beta0, R beta0]
assert mid[1] == 0 and mid[0].sign() > 0                        # bisector is the +x axis
LO = [rotn(BETA0, j) for j in range(7)]                         # boundary j at angle j*pi/3 - pi/6
assert veq(LO[6], LO[0])
DIR = [rotn(V(1, 0), j) for j in range(6)]                      # sector-centre direction j*pi/3
for j in range(6):
    assert dot(LO[j], LO[j + 1]) == F(1, 2) and cross(LO[j], LO[j + 1]).sign() > 0   # arc = pi/3 exactly
    assert dot(DIR[j], DIR[j]) == 1
    assert cross(LO[j], DIR[j]).sign() > 0 and cross(DIR[j], LO[j + 1]).sign() > 0
    assert veq(rot(LO[j]), LO[j + 1])
out("  boundaries LO[j] = R^j(sqrt3/2,-1/2) (angle j*pi/3 - pi/6); arc LO[j]->LO[j+1] has cos 1/2, sin>0,")
out("  i.e. length exactly pi/3; bisector of sector 0 is (1,0); dir(j) = R^j(1,0) lies strictly inside sector j.")
SECTOR_LEN = [F(1, 3)] * 6                                      # in units of pi
assert sum(SECTOR_LEN) == 2
out("  angular measure: each open sector = pi/3, total 2*pi; the 6 boundary directions are null.")


def classify(e):
    hits = [j for j in range(6) if cross(LO[j], e).sign() > 0 and cross(e, LO[j + 1]).sign() > 0]
    bnd = [j for j in range(6) if cross(LO[j], e).sign() == 0 and dot(LO[j], e).sign() > 0]
    return hits, bnd


# exact sample directions: rational Pythagorean points, (-1,0), and their R-images (sqrt3 coordinates)
samples = {}
for qq in range(1, 16):
    for pp in range(-45, 46):
        n2 = qq * qq + pp * pp
        e = V(F(qq * qq - pp * pp, n2), F(2 * pp * qq, n2))
        samples[(e[0].a, e[0].b, e[1].a, e[1].b)] = e
samples[(F(-1), 0, 0, 0)] = V(-1, 0)
base = list(samples.values())
for e in base:
    for k in (1, 2, 3):
        r = rotn(e, k)
        samples[(r[0].a, r[0].b, r[1].a, r[1].b)] = r
for j in range(6):
    samples[("dir", j)] = DIR[j]
    samples[("lo", j)] = LO[j]
SAMPLES = list(samples.values())
n_inside = n_bnd = 0
SAMPLE_SECTOR = []
for e in SAMPLES:
    assert dot(e, e) == 1
    hits, bnd = classify(e)
    assert (len(hits) == 1 and not bnd) or (not hits and len(bnd) == 1)
    if hits:
        n_inside += 1
        SAMPLE_SECTOR.append((e, hits[0]))
    else:
        n_bnd += 1
out(f"  exact sample directions: {len(SAMPLES)} unit vectors in Q(sqrt3)^2; {n_inside} strictly inside a sector,")
out(f"  {n_bnd} on a boundary (skipped: null set).  Every sample classified into exactly one sector or boundary.")
ROT_SECTOR = [classify(rot(e))[0] for e, _ in SAMPLE_SECTOR]          # sector of e+pi/3, classified afresh
rot_ok = all(rs == [(j + 1) % 6] for (e, j), rs in zip(SAMPLE_SECTOR, ROT_SECTOR))
out(f"  'e in sector j => e+pi/3 in sector j+1 (mod 6)' on all {len(SAMPLE_SECTOR)} interior samples: {rot_ok}")
assert rot_ok
out("  (exact proof for ALL e: R maps LO[j] -> LO[j+1] incl. LO[5] -> LO[6] = LO[0], and det R = 1 preserves")
out("   the sign of cross(LO[j], e) and cross(e, LO[j+1]); so R(sector j) = sector j+1 exactly.)")

# ----------------------------------------------------------------------- [2] lane text -> model data
out("\n[2] Model data, transcribed from the TEXT of model_check.py (lines 66-102), cross-checked by regex")
LAB = tuple(range(6))
CEN = {"A": V(0, 0), "B": V(1, 0), "C": V(F(1, 2), R3H)}
NAMES = ("A", "B", "C")
# (value on even sectors, value on odd sectors)
PAL_DATA = {"A": ({0, 1, 2}, {3}), "B": ({3}, {4}), "C": ({4, 5}, {0})}
TR_DATA = {
    "A": ((F(1, 3), F(1, 3), F(1, 3), F(0), F(0), F(0)), (F(0), F(0), F(0), F(1), F(0), F(0))),
    "B": ((F(0), F(0), F(0), F(1), F(0), F(0)), (F(0), F(0), F(0), F(0), F(1), F(0))),
    "C": ((F(0), F(0), F(0), F(0), F(1, 2), F(1, 2)), (F(1), F(0), F(0), F(0), F(0), F(0))),
}


def P(x, j):
    return frozenset(PAL_DATA[x][j % 2])


def TR(x, j):
    return TR_DATA[x][j % 2]


def P_at(x, e):
    hits, _ = classify(e)
    return P(x, hits[0])


raw, txt = read_text(LANE_MODEL)
LANE_IDS = []
if txt is None:
    out("  lane model_check.py NOT READABLE -- transcription not cross-checked")
else:
    out("  lane model_check.py sha256:", hashlib.sha256(raw).hexdigest())
    norm = re.sub(r"\s+", " ", txt)
    expect = [
        'SQ3H = q3(0, F(1, 2))',
        'A = (ZERO, ZERO)', 'B = (ONE, ZERO)', 'C = (q3(F(1,2)), SQ3H)',
        'sector j = open arc of directions of angle (j*pi/3 - pi/6, j*pi/3 + pi/6)',
        '"A": {j: frozenset({0, 1, 2}) if j % 2 == 0 else frozenset({3}) for j in SECTORS}',
        '"B": {j: frozenset({3}) if j % 2 == 0 else frozenset({4}) for j in SECTORS}',
        '"C": {j: frozenset({4, 5}) if j % 2 == 0 else frozenset({0}) for j in SECTORS}',
        '"A": {j: ((F(1,3), F(1,3), F(1,3), F(0), F(0), F(0)) if j % 2 == 0 else (F(0), F(0), F(0), F(1), F(0), F(0))) for j in SECTORS}',
        '"B": {j: ((F(0), F(0), F(0), F(1), F(0), F(0)) if j % 2 == 0 else (F(0), F(0), F(0), F(0), F(1), F(0))) for j in SECTORS}',
        '"C": {j: ((F(0), F(0), F(0), F(0), F(1,2), F(1,2)) if j % 2 == 0 else (F(1), F(0), F(0), F(0), F(0), F(0))) for j in SECTORS}',
    ]
    miss = [s for s in expect if s not in norm]
    out(f"  {len(expect) - len(miss)}/{len(expect)} transcribed data strings found verbatim (whitespace-normalised)")
    for s in miss:
        out("   MISSING:", s)
    assert not miss
    LANE_IDS = re.findall(r'check\("([A-Z][0-9]+[a-z]?)\s', txt)
    out(f"  check ids declared in the lane text ({len(LANE_IDS)}): {' '.join(LANE_IDS)}")
for x in NAMES:
    out(f"  {x} = {CEN[x]}:  P even = {S(P(x, 0))}, odd = {S(P(x, 1))};"
        f"  trace even = {[str(v) for v in TR(x, 0)]}, odd = {[str(v) for v in TR(x, 1)]}")

# ----------------------------------------------------------------------- [3] source readings (Lean text)
out("\n[3] Source statements (Lean TEXT, read as data) that fix the readings used below")


def lean_find(tree, fname, name):
    raw_, t = read_text(tree + "/" + fname)
    if t is None:
        return None, None
    pat = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:lemma|theorem|def|abbrev)\s+" + re.escape(name) + r"(?:\s|$)")
    lines = t.splitlines()
    for i, ln in enumerate(lines, 1):
        if pat.match(ln):
            return i, lines
    return None, lines


FO = LEAN_TREES[0]
for fname, name, nl in [("FiveSupport.lean", "palette_neighbor_disjoint", 2),
                        ("PaletteTransport.lean", "palette_sixty_disjoint", 2),
                        ("Compactness.lean", "trace_bounds", 4),
                        ("BoundaryTrace.lean", "avoiding_trace_palette", 3),
                        ("BinaryPalettes.lean", "BinaryCenter", 2),
                        ("BinaryPalettes.lean", "binary_alternation", 4),
                        ("BinaryPalettes.lean", "binary_centers_separated", 3)]:
    ln, lines = lean_find(FO, fname, name)
    if ln is None:
        out(f"  {fname}: {name} NOT FOUND in full-original tree")
        continue
    out(f"  full-original {fname}:{ln}")
    for k in range(nl):
        out("     | " + lines[ln - 1 + k].rstrip())
out("  Readings used:")
out("   TE  : for each fixed unit displacement a with x and x+dir(a) both centres, Disjoint(P_{x+dir a}(t), P_x(t))")
out("         for a.e. palette direction t -- i.e. for ALL directions t, not only t = a.  (palette_neighbor_disjoint)")
out("   5.7 : for a.e. f, Disjoint(P_x(f), P_x(f+pi/3)).  (palette_sixty_disjoint)")
out("   trace: 0 <= b_i <= 1 a.e., sum_i b_i = 1; palette = (essential) union over traces of {t : b_i(t) > 0};")
out("          the model declares exactly ONE trace per centre (a function of t, constant on sectors).")
out("   BinaryCenter x i j (Lean): a.e. t, i in P_x(t) OR j in P_x(t).  The lane's C12 instead uses P_x(t) subset {i,j}.")

# ----------------------------------------------------------------------- [4] the 19 constraints
out("\n[4] Independent evaluation of the model (exhaustive over the 6 sectors; spot-checked on exact samples)")

# ---- geometry and unit pairs (discovered)
D2 = {}
for x, y in combinations(NAMES, 2):
    d = vsub(CEN[x], CEN[y]); D2[(x, y)] = dot(d, d)
TE_INST = []                                     # (x, j, y) with x + dir(j) == centre y
for x in NAMES:
    for j in range(6):
        for y in NAMES:
            if y != x and veq(vadd(CEN[x], DIR[j]), CEN[y]):
                TE_INST.append((x, j, y))
out("  |XY|^2 exact: " + ", ".join(f"{x}{y}={D2[(x, y)]}" for x, y in D2))
out("  unit-displacement instances x + dir(j*pi/3) = y found by search: "
    + ", ".join(f"{x}+dir({j})={y}" for x, j, y in TE_INST))

CHK = {}


def record(cid, ok, detail, note=""):
    CHK[cid] = (ok, detail, note)
    out(f"  {cid:4s} {'PASS' if ok else 'FAIL'}  {detail}" + (f"   ({note})" if note else ""))


# H1
record("H1", all(v == 1 for v in D2.values()) and len(TE_INST) == 6,
       "all three squared side lengths == 1 exactly in Q(sqrt3); 6 ordered unit instances")
# H2
pv = {x: {P(x, j) for j in range(6)} for x in NAMES}
tv = {x: {TR(x, j) for j in range(6)} for x in NAMES}
record("H2", all(len(pv[x]) <= 2 and len(tv[x]) <= 2 for x in NAMES),
       "distinct palette values per centre " + str({x: len(pv[x]) for x in NAMES})
       + ", trace values " + str({x: len(tv[x]) for x in NAMES}),
       "structural: sector-constant on open arcs => Borel; true by construction of the data")
# C1
# sample checks reuse the exact classification of each sample e (sector j) and of e+pi/3 (ROT_SECTOR)
c1 = all(P(x, j) for x in NAMES for j in range(6)) and all(P(x, j) for x in NAMES for _, j in SAMPLE_SECTOR)
record("C1", c1, "every P_x(sector) nonempty; min size = %d" % min(len(P(x, j)) for x in NAMES for j in range(6)))
# C2
mx = max(len(P(x, j)) for x in NAMES for j in range(6))
record("C2", mx <= 3 and mx == 3, f"max |P_x(e)| over centres/sectors = {mx} (<= k-3 = 3, attained)",
       "the source of the k-3 ceiling is not cited; only the numeric fact is checked")
# C3  (TE) -- all directions t, every discovered instance
te_tab = []
te_ok = True
for x, j0, y in TE_INST:
    for t in range(6):
        inter = P(y, t) & P(x, t)
        te_tab.append((x, j0, y, t, inter))
        te_ok &= not inter
te_samples = all(not (P(x, j) & P(y, j)) for x, _, y in TE_INST for _, j in SAMPLE_SECTOR)
record("C3", te_ok and te_samples,
       f"Disjoint(P_y(t),P_x(t)) for all 6 instances x+dir(a)=y and ALL 6 sectors t (36 cases)"
       f" + {len(SAMPLE_SECTOR)} exact sample directions per instance")
for x, y in combinations(NAMES, 2):
    ev, od = (P(x, 0), P(y, 0)), (P(x, 1), P(y, 1))
    out(f"        ({x},{y}): even {S(ev[0])} vs {S(ev[1])} -> {S(ev[0] & ev[1])};"
        f"  odd {S(od[0])} vs {S(od[1])} -> {S(od[0] & od[1])}")
# C4  (5.7) incl. wrap, via the rotation map (not via index arithmetic alone)
c4 = all(not (P(x, j) & P(x, classify(rot(DIR[j]))[0][0])) for x in NAMES for j in range(6))
c4s = all(not (P(x, j) & P(x, rs[0])) for x in NAMES for (_, j), rs in zip(SAMPLE_SECTOR, ROT_SECTOR))
wrap = classify(rot(DIR[5]))[0] == [0]
record("C4", c4 and c4s and wrap,
       f"Disjoint(P_x(f),P_x(f+pi/3)) for 3 centres x 6 sectors (wrap 5->0 verified: R dir(5) in sector 0 = {wrap})"
       f" + {len(SAMPLE_SECTOR)} exact samples per centre")
# C5
c5 = all(all(v >= 0 for v in TR(x, j)) and all(v <= 1 for v in TR(x, j)) and sum(TR(x, j)) == 1
         for x in NAMES for j in range(6))
record("C5", c5, "every trace entry in [0,1] and each trace sums to exactly 1 (Fractions)")
# C6
c6 = all(frozenset(i for i in LAB if TR(x, j)[i] > 0) == P(x, j) for x in NAMES for j in range(6))
record("C6", c6, "{i : b_x(e)_i > 0} == P_x(e) for all centres and sectors")
# C7
c7 = True
Zs = {}
for x in NAMES:
    Z = frozenset(i for i in LAB if all(TR(x, j)[i] == 0 for j in range(6)))   # a.e.-zero labels
    Zs[x] = Z
    for r in range(len(Z) + 1):
        for J in combinations(sorted(Z), r):
            if any(P(x, j) <= frozenset(J) for j in range(6)):
                c7 = False
record("C7", c7 and all(Zs.values()),
       "for every J within the a.e.-zero labels " + str({x: S(Zs[x]) for x in NAMES})
       + ": P_x(e) not subset of J, every sector",
       "hypothesis non-vacuous (Z nonempty), but the conclusion is implied by C1+C6 (P nonempty, P cap Z = empty)")
# C8a/b/c
h0, b0 = classify(V(1, 0))
record("C8a", h0 == [0] and not b0, "(1,0) strictly inside sector 0 by exact cross-product signs")
record("C8b", P_at("A", V(1, 0)) == frozenset({0, 1, 2}), f"P_A((1,0)) = {S(P_at('A', V(1, 0)))}, size 3 > 2")
Sset = frozenset({0, 1, 2})
meas = sum(SECTOR_LEN[j] for j in range(6) if Sset <= P("A", j))
record("C8c", meas == 1, f"angular measure of {{t : {{0,1,2}} subset P_A(t)}} = {meas}*pi > 0")
# C9a/b
zeta = vadd(CEN["A"], DIR[0])
record("C9a", veq(zeta, CEN["B"]), "A + dir(0) == B exactly")
T = frozenset(LAB) - Sset
record("C9b", all(P("B", j) & T for j in range(6)),
       f"P_B(t) meets T = {S(T)} in every sector (hits: {[S(P('B', j) & T) for j in range(6)]})",
       "this is a single direction t=0 from A (a null set); it does not refute an a.e.-in-t statement")
# C10
sums = {(x, y, j): len(P(x, j)) + len(P(y, j)) for x, y in combinations(NAMES, 2) for j in range(6)}
smax = max(sums.values())
arg = sorted({(x, y, j % 2) for (x, y, j), v in sums.items() if v == smax})
record("C10", smax == 5 and all(v <= 5 for v in sums.values()),
       f"max over unit pairs/sectors of |P_x|+|P_y| = {smax}, attained at (pair, parity) {arg}")
# C11
free = {x: frozenset(LAB) - frozenset().union(*(P(x, j) for j in range(6))) for x in NAMES}
c11_zero = all(all(TR(x, j)[i] == 0 for j in range(6) for i in free[x]) for x in NAMES)
record("C11", all(free.values()) and c11_zero,
       "labels absent from every palette (and identically 0 in the trace): " + str({x: S(free[x]) for x in NAMES}))
# C12 -- two readings
lane_bin = {x: [p for p in combinations(LAB, 2) if all(P(x, j) <= frozenset(p) for j in range(6))] for x in NAMES}
lean_bin = {x: [(i, j2) for i in LAB for j2 in LAB if all((i in P(x, t)) or (j2 in P(x, t)) for t in range(6))]
            for x in NAMES}


def alternation_ok(x, i, j2):
    # binary_alternation: a.e. t, (t+60 in PS_i <-> t notin PS_i) and (t in PS_j <-> t notin PS_i)
    for t in range(6):
        t1 = classify(rot(DIR[t]))[0][0]
        if ((i in P(x, t1)) != (i not in P(x, t))) or ((j2 in P(x, t)) != (i not in P(x, t))):
            return False
    return True


alt_all = all(alternation_ok(x, i, j2) for x in NAMES for (i, j2) in lean_bin[x])
ne_all = all(i != j2 for x in NAMES for (i, j2) in lean_bin[x])
shared = [(x, y, p) for x, y in combinations(NAMES, 2) for p in lean_bin[x] if p in lean_bin[y]]
lane_reading_ok = (lane_bin["A"] == [] and lane_bin["B"] == [(3, 4)] and lane_bin["C"] == []
                   and alternation_ok("B", 3, 4))
lean_sub_claim = (lean_bin["A"] == [] and lean_bin["C"] == [])
record("C12", lane_reading_ok,
       "lane reading (P subset {i,j}): " + str({x: lane_bin[x] for x in NAMES}),
       "PASS only under the lane's reading; see C12-Lean below")
out("  C12-Lean  BinaryCenter per Lean def (ordered pairs): "
    + str({x: lean_bin[x] for x in NAMES}))
out(f"            sub-claim 'A is not binary for any pair, C similarly' under the Lean def: {lean_sub_claim}")
out(f"            binary_alternation holds for every Lean binary pair: {alt_all};  binary_ne (i != j): {ne_all};"
    f"  same pair at two distinct centres (binary_centers_separated): {shared if shared else 'none'}")
# X1
X1_taut = all(frozenset(p) & frozenset(p) for r in range(1, 7) for p in combinations(LAB, r))
record("X1", X1_taut, "every nonempty P has P cap P != empty (all 63 nonempty subsets of Fin 6)",
       "TAUTOLOGY: carries no information about the model")
# G1
Cg = frozenset({0, 1, 3, 4})
splits = []
for r in range(1, len(Cg)):
    for Vv in combinations(sorted(Cg), r):
        Vs = frozenset(Vv); W = Cg - Vs
        splits.append((Vs, W))
nonbin = [(a, b) for a, b in splits if len(a) >= 3 or len(b) >= 3]
ex = (frozenset({0, 1, 3}), frozenset({4}))
record("G1", len(nonbin) > 0 and all(max(len(a), len(b)) <= 3 for a, b in splits) and ex in splits,
       f"C={S(Cg)}: {len(splits)} ordered splits into disjoint nonempty V,W with V u W = C;"
       f" {len(nonbin)} non-binary; all max side <= 3; {S(ex[0])}/{S(ex[1])} present",
       "pure finite combinatorics, independent of the model")

ids_mine = list(CHK.keys())
out(f"\n  my evaluation covers {len(ids_mine)} ids: {' '.join(ids_mine)}")
if LANE_IDS:
    out(f"  lane ids == my ids: {LANE_IDS == ids_mine}")
    assert LANE_IDS == ids_mine and len(ids_mine) == 19

# ----------------------------------------------------------------------- [5] the numbered claims
out("\n[5] Verdicts on the numbered claims of the brief")
verdict("Claim 1 (sides exactly 1)", "CONFIRMED" if CHK["H1"][0] else "DISAGREES",
        "|AB|^2=|AC|^2=|BC|^2=1 in Q(sqrt3); A+dir(0)=B, A+dir(pi/3)=C, B+dir(2pi/3)=C exactly")
cl2 = (CHK["C3"][0] and P("A", 0) == {0, 1, 2} and P("B", 0) == {3} and P("A", 1) == {3} and P("B", 1) == {4})
verdict("Claim 2 (TE disjointness)", "CONFIRMED" if cl2 else "DISAGREES",
        "required (Lean palette_neighbor_disjoint) for ALL a.e. directions t at each unit pair, not only t = the"
        " displacement; holds for all 3 pairs x all 6 sectors (A,B even {0,1,2}/{3}, odd {3}/{4}; A,C {0,1,2}/{4,5},"
        " {3}/{0}; B,C {3}/{4,5}, {4}/{0})")
verdict("Claim 3 (pi/3 disjointness incl. wrap)", "CONFIRMED" if CHK["C4"][0] else "DISAGREES",
        "sector j -> j+1 under +pi/3 proved exactly via R; all 18 (centre,sector) cases incl. 5->0 disjoint")
verdict("Claim 4 (traces)", "CONFIRMED" if (CHK["C5"][0] and CHK["C6"][0]) else "DISAGREES",
        "18 declared traces: entries in [0,1], sum exactly 1, positivity set == palette")
cl5 = (len(P("A", 0)) + len(P("C", 0)) == 5 and CHK["C10"][0])
verdict("Claim 5 (|P_A|+|P_C| = 3+2 = 5, saturating)", "CONFIRMED" if cl5 else "DISAGREES",
        f"even sectors: |{S(P('A', 0))}|+|{S(P('C', 0))}| = 5; max over all unit pairs/sectors = {smax} (<= 5)")
claimed_free = {"A": frozenset({4, 5}), "B": frozenset({0, 1, 2, 5}), "C": frozenset({1, 2, 3})}
supp = {x: frozenset(LAB) - free[x] for x in NAMES}
maxP = {x: max(len(P(x, j)) for j in range(6)) for x in NAMES}
cap_eq = all(maxP[x] == len(supp[x]) - 1 for x in NAMES)
# general implication C1 + C4 => |P_x(f)| <= |supp_x| - 1 (exhaustive over disjoint nonempty P,Q inside U)
impl = True
for mU in range(1, 64):
    U = [i for i in LAB if mU >> i & 1]
    for mP in range(1, 64):
        if mP & ~mU:
            continue
        for mQ in range(1, 64):
            if (mQ & ~mU) or (mQ & mP):
                continue
            if bin(mP).count("1") > len(U) - 1:
                impl = False
out(f"  support_x = labels used at x: {{{', '.join(x + ': ' + S(supp[x]) for x in NAMES)}}};"
    f" max|P_x| = {maxP}; |supp_x|-1 = { {x: len(supp[x]) - 1 for x in NAMES} }")
out(f"  general bound from C1+C4 (P(f), P(f+pi/3) disjoint nonempty within supp): |P| <= |supp|-1  (exhaustive: {impl})")
cl6 = (free == claimed_free and CHK["C11"][0] and cap_eq and maxP["A"] == 3 and impl)
verdict("Claim 6 (C11 absent sets; caps at support-1 = 3, not 2)", "CONFIRMED" if cl6 else "DISAGREES",
        f"absent sets {[S(free[x]) for x in NAMES]} == claimed; at A |supp|=4, max|P_A|=3=|supp|-1 > 2;"
        " max|P_x| = |supp_x|-1 at every centre (B: 1, C: 2), the C1+C4 ceiling, attained")
fails = [c for c, (ok, _, _) in CHK.items() if not ok]
verdict("Claim 7 (19/19 lane predicates as coded)", "CONFIRMED" if not fails else "DISAGREES",
        f"all 19 predicates evaluate True independently (fails: {fails or 'none'}). Trivial/structural, carry no"
        f" model information: X1 (tautology), G1 (model-free combinatorics), H2 (by construction), C7 (implied by C1+C6)")
verdict("Claim 7 / C12 sub-claim 'A not (i,j)-binary for any pair, C similarly' (Lean BinaryCenter def)",
        "DISAGREES" if not lean_sub_claim else "CONFIRMED",
        f"Lean def (a.e. i in P or j in P): A binary for {[p for p in lean_bin['A'] if p[0] < p[1]]},"
        f" B for {[p for p in lean_bin['B'] if p[0] < p[1]]}, C for {[p for p in lean_bin['C'] if p[0] < p[1]]};"
        f" the lane tested P subset {{i,j}} instead. Headline survives: binary_alternation holds for all {alt_all},"
        f" i != j {ne_all}, no pair shared by two centres")

# ----------------------------------------------------------------------- [6] Step-1 ladder
out("\n[6] Step-1 ladder (LADDER-k6.md): stated finite facts, recomputed with bitmasks")


def subs(n, r):
    return [m for m in range(1 << n) if bin(m).count("1") == r]


def pc(m):
    return bin(m).count("1")


full5, full6 = (1 << 5) - 1, (1 << 6) - 1
s5, s6 = subs(5, 3), subs(6, 3)
L6a = len(s5) == 10 and all(pc(full5 & ~m) == 2 for m in s5)
L6b = len(s6) == 20 and all(pc(full6 & ~m) == 3 for m in s6)
out(f"  L6: Fin5: {len(s5)} 3-sets, all complements of card 2: {L6a};  Fin6: {len(s6)} 3-sets, all complements card 3: {L6b}")
# L5/L7: two_complement_pred content; hcomp satisfiable for card-3 S at k=5, unsatisfiable at k=6
def tcp_ok(n):
    fulln = (1 << n) - 1
    for m in range(1 << n):
        for i in range(n):
            for j in range(n):
                if (fulln & ~m) == ((1 << i) | (1 << j)):
                    for a in range(n):
                        if not (m >> a & 1) and a not in (i, j):
                            return False
    return True


def hcomp_sat(n, m):
    fulln = (1 << n) - 1
    return any((fulln & ~m) == ((1 << i) | (1 << j)) for i in range(n) for j in range(n))


L5 = tcp_ok(5) and tcp_ok(6)
L7a = all(hcomp_sat(5, m) for m in s5)
L7b = not any(hcomp_sat(6, m) for m in s6)
out(f"  L5: two_complement_pred (univ\\S={{i,j}}, a notin S => a in {{i,j}}) holds exhaustively for Fin5, Fin6: {L5}")
out(f"  L7: hcomp univ\\S={{i,j}} satisfiable for every 3-set at k=5: {L7a}; for NO 3-set at k=6: {L7b}")
# section 2
alt_trip = sorted({frozenset({i % 6, (i + 2) % 6, (i + 4) % 6}) for i in range(6)}, key=sorted)
out(f"  alternating triples {{i,i+2,i+4}} of Z/6: {[S(t) for t in alt_trip]}")
assert [sorted(t) for t in alt_trip] == [[0, 2, 4], [1, 3, 5]]


def has_alt(Sset_):
    return any(t <= Sset_ for t in alt_trip)


Cc, P2 = frozenset({0, 1, 3, 4}), frozenset({2, 5})
sec2 = (Cc | P2 == frozenset(LAB)) and not has_alt(Cc) and not has_alt(P2)
out(f"  [2] P1={S(Cc)}, P2={S(P2)}: union = Fin6: {Cc | P2 == frozenset(LAB)}; P1 alt? {has_alt(Cc)}; P2 alt? {has_alt(P2)}")
cnt = {r: sum(1 for c in combinations(LAB, r) if not has_alt(frozenset(c))) for r in range(7)}
tot = {r: sum(1 for _ in combinations(LAB, r)) for r in range(7)}
ge3 = sum(cnt[r] for r in range(3, 7))
out(f"  [3] avoiding both alternating triples by card: {cnt} (totals {tot}); card>=3 total = {ge3}")
sec3 = (cnt[3] == 18 and tot[3] == 20 and cnt[4] == 9 and tot[4] == 15 and ge3 == 27 and tot[3] - cnt[3] == 2)
rep = (354 + 150 + 6 == 510)
out(f"  sec.4 cited REPORT.md arithmetic 354+150+6 = 510: {rep}  (the counts themselves: source not available locally)")
# hashes stated in LADDER-k6.md
rawpy, _ = read_text(LANE_LADDER_PY)
rawmd, mdtxt = read_text(LANE_LADDER_MD)
stated = "627ff696648a30397768f96eac47a6fefcdb98a3e73a8544a38f5b00dd079876"
if rawpy is not None:
    h_inbox = hashlib.sha256(rawpy).hexdigest()
    h_lf = hashlib.sha256(rawpy.replace(b"\r\n", b"\n")).hexdigest()
    out(f"  ladder_k6.py (inbox copy) sha256 = {h_inbox}; LF-normalised = {h_lf}; stated {stated[:8]}...: "
        f"{'MATCH' if stated in (h_inbox, h_lf) else 'NO MATCH'}")
if rawmd is not None:
    out(f"  LADDER-k6.md (inbox copy) sha256 = {hashlib.sha256(rawmd).hexdigest()}")
# Lean line citations in the ladder (file:line), scanned as text across local trees
cites = [("Palettes.lean", "palette_nonempty", 47), ("BinaryPalettes.lean", "ae_circle_palette_exclusion", 218),
         ("BinaryPalettes.lean", "ae_circle_typicalSampling", 229), ("BinaryPalettes.lean", "typical_sample_palette", 213),
         ("BinaryPalettes.lean", "ae_not_binary_circle", 182), ("BinaryPalettes.lean", "two_complement_pred", 236),
         ("BinaryPalettes.lean", "circle_complement_binary", 242), ("BinaryPalettes.lean", "palette_triple_null", 253),
         ("BinaryPalettes.lean", "palette_cardinality", 260), ("Palettes.lean", "edge_palette_not_pair", 124)]
cite_rows = []
for fname, name, cl in cites:
    found = []
    for tr in LEAN_TREES:
        ln, _ = lean_find(tr, fname, name)
        if ln is not None:
            found.append(ln)
    ok = cl in found
    cite_rows.append((name, cl, sorted(set(found)), ok))
    out(f"  cite {fname}:{cl:<4d} {name:30s} found at lines {sorted(set(found))} -> {'match' if ok else 'MISMATCH'}")
mism = [r for r in cite_rows if not r[3]]
# hSc at 255-256
_, blines = lean_find(FO, "BinaryPalettes.lean", "palette_triple_null")
hsc = [i for i, l in enumerate(blines or [], 1) if "have hSc" in l]
out(f"  'hSc' (L6 cite 255-256) found at full-original BinaryPalettes.lean lines {hsc}")
lad_ok = L6a and L6b and L5 and L7a and L7b and sec2 and sec3 and rep
verdict("Ladder finite facts (L5-L7, sec.2, sec.3)", "CONFIRMED" if lad_ok else "DISAGREES",
        "10/10 Fin5 3-sets have complement 2, 20/20 Fin6 have 3; hcomp unsatisfiable at k=6; C={0,1,3,4}+{2,5}"
        " covers Fin6 w/o alternating triple; 18/20, 9/15, 27 avoiders; 2 of 20 contain one")
verdict("Ladder file:line citations", "PARTIAL" if mism else "CONFIRMED",
        f"{len(cites) - len(mism)}/{len(cites)} match a local Lean tree; mismatches: "
        + "; ".join(f"{n} cited {c}, found {f}" for n, c, f, _ in mism))
verdict("Ladder TRUE/UNPROVED verdicts on Lean steps (L0-L4, L8-L10)", "UNDETERMINED",
        "these are proof-status claims about Lean declarations, not finite facts; no Lean run (out of scope)")

# ----------------------------------------------------------------------- summary
out("\n" + "=" * 96)
out("SUMMARY")
for tag, st, det in RESULTS:
    out(f"  {st:12s} {tag}")
out(f"runtime {time.perf_counter() - T0:.3f} s;  self sha256 {SELF_SHA}")
out("=" * 96)
