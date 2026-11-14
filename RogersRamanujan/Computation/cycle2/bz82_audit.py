#!/usr/bin/env python3
"""
bz82_audit.py -- a fresh, source-audited transcription of the two involutions of
Bressoud & Zeilberger, "A short Rogers-Ramanujan bijection",
Discrete Mathematics 38 (1982) 313--315.

Written in RR127 cycle 2 for direction A (computation), directly from the
printed text of pp. 314 and the worked examples of p. 315, which were re-read
from the original scan
  https://sites.math.rutgers.edu/~zeilberg/mamarimY/rrDG.pdf
  sha256 403543088ed9465bc8e3f9918defd22a57c86a21493226c9852729af614483c6
The scan's sha256 matches the digest recorded in
`Literature/READING_NOTES.md`, so this is the same artefact the project
already cites.

This module does NOT import, call or copy `Computation/bz82.py`.  It was
written and exhaustively tested first; the comparison against `bz82.py` is a
separate program (`compare_bz82.py`) run afterwards.

--------------------------------------------------------------------------------
SOURCE LINES (quoted verbatim from `pdftotext -layout` of the scan, OCR noise
corrected only where the paper's own worked examples force the reading)
--------------------------------------------------------------------------------
p. 314:
  "Consider (j; lam(1), ..., lam(t)) in X(n) - 0 x B(n).  Let
   a = Min{x; 2j+x-lam(x) > 0},  mu = 2j+a-lam(a),
   t* = t + chi(lam(a)=0) + chi(lam(mu)=0).
   Case I: lam(a)+lam(mu) >= 5j + t*.  Delete the parts lam(a) and lam(mu);
     add 1 to each of the remaining parts and insert lam(a)+lam(mu)-5j-t*
     new parts of 1; j <- j+1.
   Case II: lam(a)+lam(mu)-5j < t*.  Let
     m = Max{z <= a+2j-2; z + lam(a+2j-1-z) <= t+5j-2}.
     Subtract 1 from each of the t parts and create new parts m and
     t+5j-3-m; j <- j-1."
p. 314, psi:
  "Let t0 be the number of parts which are = 0 (mod 5) and for i = 0,2,3 let
   mi be the largest part which is = i (mod 5) (if there are no such parts
   mi = 0).
   Case I: t0+j > 0 or m2 > 0.
     Case I(a): 5t0+5j-3 >= m2.  Subtract 5 from each of the t0 parts which
       are = 0 (mod 5) and insert a new part of 5t0+5j-3, j <- j-1.
     Case I(b): 5t0+5j-3 < m2.  Delete the part m2, add 5 to each of the t0
       parts which are = 0 (mod 5) and create (m2-5j-2-5t0)/5 new parts of 5
       each, j <- j+1.
   Case II: t0+j <= 0 and m2 = 0.
     Case II(a): m3+5j-3 >= m0.  Add 5j-3 to m3 (and sort); j <- j-1.
     Case II(b): m3+5j-3 < m0.  Subtract 5j+2 from m0 (and sort); j <- j+1."
p. 313: X(n) = {(j; lam) : -oo<j<oo, t>=0, lam(1)>=...>=lam(t)>0,
                j(5j-2)/2 + |lam| = n}
        (the OCR "j(5j^2-j)" is the printed pentagonal number j(5j-1)/2, which
         the same page's own shift and the paper's worked examples confirm)
p. 313: B(n) = {(lam(1),...,lam(t)) : t >= 0, |lam| = n, lam(1)>=...>=lam(t)>=t}

--------------------------------------------------------------------------------
READINGS THAT THE PRINTED TEXT LEAVES OPEN (declared, then tested)
--------------------------------------------------------------------------------
R1. THE INTEGER DOMAIN OF z IN phi CASE II.  The printed line gives only the
    upper bound  z <= a+2j-2.  We take the domain to be the integers z with
        0 <= z <= a+2j-2.
    Reasons, both internal to the rule: (i) z is one of the two parts that the
    same sentence creates, and `m` is printed as a part, so m >= 0; (ii) the
    index of lam that is read is a+2j-1-z, which must be a legal index >= 1,
    which is *exactly* the printed bound z <= a+2j-2.  The two halves of the
    printed bound are therefore (index legality) and (part non-negativity).
    If z were allowed to run over all integers z <= a+2j-2 the maximum could
    change; this is measured, not assumed -- see `case_ii_z_domain_survey`,
    which reports the number of Case-II states on which the two domains select
    different m.  [Supervisor correction C1.]
R2. THE a = mu TIE IN phi CASE I.  The rule says "delete the parts lam(a) and
    lam(mu)", which is ambiguous when a = mu.  It is vacuous: `a = mu` forces
    Case II.  Proof: a = mu means lam(a) = 2j, so j >= 1 (a <= t forces
    lam(a) > 0; a > t forces lam(a) = 0 = 2j, i.e. j = 0, and then
    Case I would read 0 = lam(a)+lam(mu) >= 0 + t* >= 0, forcing t* = 0 and
    therefore t = 0, j = 0, i.e. the state (0;()) which lies in 0 x B(0) and
    is not in phi's domain).  With j >= 1 and lam(a) = 2j, Case I would need
    4j = lam(a)+lam(mu) >= 5j + t* > 4j because t* > t - 2 + ... ; precisely
    t* >= 0 and 4j >= 5j + t* gives t* <= -j < 0, impossible.  Hence in Case I
    a != mu and the deletion of two distinct slots is unambiguous.  Verified
    exhaustively as well, see `tie_diagnostics`.
R3. ZERO PARTS.  "Subtract 1 from each of the t parts", resp. "subtract 5 from
    each of the t0 parts which are = 0 (mod 5)", can produce a 0; a created
    part can be 0.  Zero is not a part (p. 313: lam(t) > 0), so every 0 is
    dropped.  Dropping a 0 never changes |lam|, so this reading is the only one
    consistent with the invariant |lam| + P(j) = n.  We test that no created
    part is *negative*.
R4. SORTING.  Never stated except "(and sort)" in psi II; every result is
    returned as a descending tuple, which is the contract's representation.

--------------------------------------------------------------------------------
FROZEN INTERFACE
--------------------------------------------------------------------------------
  pent(j)                     P(j) = j(5j-1)/2
  lam_at(lam, x)              lam(x), 0 for x > t   (x >= 1)
  weight(j, lam)              |lam| + P(j)
  in_B(lam)                   lam in B(n): len k, smallest part >= k
  in_A(lam)                   lam in A(n)/C(n): every part = 1 or 4 (mod 5)
  phi(j, lam) -> (state, diag)      state = (j', lam');  diag = diagnostics
  psi(j, lam) -> (state, diag)
  phi_domain(j, lam)          (j,lam) in X(n) - 0 x B(n)
  psi_domain(j, lam)          (j,lam) in X(n) - 0 x A(n)
  states_of_weight(n)         all of X(n)
  partitions(n)               all partitions of n as descending tuples
  pi_iterate(lam) -> (out, steps, trace)   the BZ82 endpoint map on 0 x A(n)
  T(lam), Tinv(lam)           p.313 shift D_n <-> B(n)
Errors are raised, never silently repaired.  Deterministic; no randomness.
"""

from fractions import Fraction

__all__ = [
    "pent", "lam_at", "weight", "in_B", "in_A", "partitions", "states_of_weight",
    "phi", "psi", "phi_domain", "psi_domain", "pi_iterate", "T", "Tinv",
    "residues", "m_of", "case_ii_admissible_set",
]

# ----------------------------------------------------------------------------
# basics
# ----------------------------------------------------------------------------


def pent(j):
    """P(j) = j(5j-1)/2, the 5-pentagonal numbers 0,2,9,21,38,... and
    0,3,11,24,42,... on the negative side.  Integral for every integer j."""
    if not isinstance(j, int):
        raise TypeError("j must be an int")
    return j * (5 * j - 1) // 2


def lam_at(lam, x):
    """lam(x) for x >= 1, with the convention lam(x) = 0 for x > t.

    x <= 0 is a programming error here: the rules never read lam(0), and the
    printed bound z <= a+2j-2 is exactly what guarantees the index
    a+2j-1-z >= 1."""
    if x < 1:
        raise ValueError("lam is only indexed from 1; got x=%r" % (x,))
    return lam[x - 1] if x <= len(lam) else 0


def weight(j, lam):
    return sum(lam) + pent(j)


def in_B(lam):
    """B(n) as on p.313: length k, smallest part >= k.  () is in B(0)."""
    k = len(lam)
    return k == 0 or lam[-1] >= k


def in_A(lam):
    """The paper's C(n): every part = 1 or 4 (mod 5).  () is in C(0)."""
    return all(p % 5 in (1, 4) for p in lam)


def residues(lam):
    """t0, m0, m2, m3 as on p.314.  mi = 0 when there is no part = i (mod 5)."""
    t0 = sum(1 for p in lam if p % 5 == 0)
    m = {}
    for r in (0, 2, 3):
        c = [p for p in lam if p % 5 == r]
        m[r] = max(c) if c else 0
    return t0, m[0], m[2], m[3]


def partitions(n, maxpart=None):
    """All partitions of n as descending tuples of positive ints, in
    lexicographic (descending-first) order.  Generator."""
    if n < 0:
        return
    if maxpart is None:
        maxpart = n
    if n == 0:
        yield ()
        return
    for first in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - first, first):
            yield (first,) + rest


def _is_partition(lam):
    return all(isinstance(p, int) and p > 0 for p in lam) and all(
        lam[i] >= lam[i + 1] for i in range(len(lam) - 1)
    )


def states_of_weight(n):
    """All of X(n) = {(j;lam) : |lam| + P(j) = n}, as a list of (j, lam)."""
    out = []
    j = 0
    while pent(j) <= n:
        out.extend((j, lam) for lam in partitions(n - pent(j)))
        j += 1
    j = -1
    while pent(j) <= n:
        out.extend((j, lam) for lam in partitions(n - pent(j)))
        j -= 1
    return out


# ----------------------------------------------------------------------------
# phi  (p.314)
# ----------------------------------------------------------------------------


def case_ii_admissible_set(j, lam, zmin=0):
    """The admissible set {z : zmin <= z <= a+2j-2, z + lam(a+2j-1-z) <= t+5j-2}.

    Returned as an explicit sorted list of ints, together with the endpoints
    (a, mu, t, tstar, hi = a+2j-2, rhs = t+5j-2).  `zmin=0` is reading R1; the
    survey also evaluates zmin=None, meaning "all integers <= a+2j-2", which is
    enumerated down to a safe explicit floor."""
    t = len(lam)
    a = _phi_a(j, lam)
    mu = 2 * j + a - lam_at(lam, a)
    hi = a + 2 * j - 2
    rhs = t + 5 * j - 2
    if zmin is None:
        # "all integers z <= hi": an explicit finite floor is needed.  The only
        # reason the constraint can hold far below 0 is lam(a+2j-1-z) being 0,
        # i.e. the index exceeding t; take the floor well past that point.
        lo = min(0, hi) - (t + 4 * abs(j) + 4)
    else:
        lo = zmin
    S = [z for z in range(lo, hi + 1) if z + lam_at(lam, a + 2 * j - 1 - z) <= rhs]
    return S, dict(a=a, mu=mu, t=t, hi=hi, rhs=rhs, lo=lo)


def _phi_a(j, lam):
    """a = Min{x >= 1 : 2j + x - lam(x) > 0}.  Exists: for x > 2j + lam(1)
    (and x > t) the quantity is 2j + x, which is positive."""
    x = 1
    while 2 * j + x - lam_at(lam, x) <= 0:
        x += 1
        if x > 10 ** 7:
            raise RuntimeError("no such a: j=%r lam=%r" % (j, lam))
    return x


def phi(j, lam, zmin=0):
    """Bressoud--Zeilberger's phi, transcribed from p.314.

    Returns ((j', lam'), diag).  diag['case'] is 'I' or 'II' and the remaining
    keys record the quantities the printed rule names, so that a trace can be
    printed with the paper's own letters."""
    if not _is_partition(lam):
        raise ValueError("not a partition: %r" % (lam,))
    t = len(lam)
    a = _phi_a(j, lam)
    la = lam_at(lam, a)
    mu = 2 * j + a - la
    lmu = lam_at(lam, mu)
    tstar = t + (1 if la == 0 else 0) + (1 if lmu == 0 else 0)
    diag = dict(case=None, a=a, mu=mu, t=t, tstar=tstar, lam_a=la, lam_mu=lmu)
    if la + lmu >= 5 * j + tstar:
        # ---- Case I -------------------------------------------------------
        diag["case"] = "I"
        ones = la + lmu - 5 * j - tstar
        if a == mu:
            raise RuntimeError(
                "phi Case I with a = mu: reading R2 says this cannot happen; "
                "j=%r lam=%r" % (j, lam))
        if tstar < max(a, mu):
            # Would break the weight identity; recorded, not silently fixed.
            diag["tstar_too_small"] = (tstar, a, mu)
        vals = [lam_at(lam, y) + 1 for y in range(1, tstar + 1) if y not in (a, mu)]
        new = tuple(sorted(vals + [1] * ones, reverse=True))
        diag["ones_inserted"] = ones
        diag["slots_kept"] = len(vals)
        return (j + 1, new), diag
    # ---- Case II ----------------------------------------------------------
    diag["case"] = "II"
    S, endpoints = case_ii_admissible_set(j, lam, zmin=zmin)
    diag.update(endpoints)
    diag["admissible_size"] = len(S)
    if not S:
        diag["m"] = None
        raise RuntimeError("phi Case II: admissible set empty; j=%r lam=%r" % (j, lam))
    m = S[-1]
    diag["m"] = m
    diag["admissible_min"] = S[0]
    hi_part = t + 5 * j - 3 - m
    diag["created"] = (m, hi_part)
    if m < 0 or hi_part < 0:
        diag["negative_created_part"] = True
    parts = [p - 1 for p in lam if p - 1 > 0]
    if m > 0:
        parts.append(m)
    if hi_part > 0:
        parts.append(hi_part)
    new = tuple(sorted(parts, reverse=True))
    return (j - 1, new), diag


def m_of(j, lam, zmin=0):
    """Just the Case-II maximum, for the z-domain survey."""
    S, endpoints = case_ii_admissible_set(j, lam, zmin=zmin)
    return (S[-1] if S else None), endpoints, S


# ----------------------------------------------------------------------------
# psi  (p.314)
# ----------------------------------------------------------------------------


def psi(j, lam):
    """Bressoud--Zeilberger's psi, transcribed from p.314."""
    if not _is_partition(lam):
        raise ValueError("not a partition: %r" % (lam,))
    t = len(lam)
    t0, m0, m2, m3 = residues(lam)
    diag = dict(t=t, t0=t0, m0=m0, m2=m2, m3=m3, case=None, sub=None)
    if t0 + j > 0 or m2 > 0:
        if 5 * t0 + 5 * j - 3 >= m2:
            # ---- Case I(a) ------------------------------------------------
            diag["case"], diag["sub"] = "I", "a"
            nu = 5 * t0 + 5 * j - 3
            diag["nu"] = nu
            parts = [p - 5 for p in lam if p % 5 == 0 and p - 5 > 0]
            parts += [p for p in lam if p % 5 != 0]
            if nu > 0:
                parts.append(nu)
            new = tuple(sorted(parts, reverse=True))
            return (j - 1, new), diag
        # ---- Case I(b) ----------------------------------------------------
        diag["case"], diag["sub"] = "I", "b"
        num = m2 - 5 * j - 2 - 5 * t0
        if num % 5 != 0:
            raise RuntimeError("psi I(b): (m2-5j-2-5t0)/5 = %r/5 not integral" % (num,))
        k = num // 5
        if k < 0:
            diag["negative_copy_count"] = k
        diag["copies_of_5"] = k
        dropped = False
        parts = []
        for p in lam:
            if not dropped and p == m2:
                dropped = True          # delete *the* part m2 (one copy)
                continue
            parts.append(p + 5 if p % 5 == 0 else p)
        if not dropped:
            raise RuntimeError("psi I(b): m2=%r not found in %r" % (m2, lam))
        parts += [5] * max(k, 0)
        new = tuple(sorted(parts, reverse=True))
        return (j + 1, new), diag
    # ---- Case II ----------------------------------------------------------
    diag["case"] = "II"
    if not (t0 + j <= 0 and m2 == 0):
        raise AssertionError("psi case split is not exhaustive")
    if m3 + 5 * j - 3 >= m0:
        # ---- Case II(a) ---------------------------------------------------
        diag["case"], diag["sub"] = "II", "a"
        nu = m3 + 5 * j - 3
        diag["nu"] = nu
        replaced = False
        parts = []
        for p in lam:
            if not replaced and p == m3:
                replaced = True
                if nu > 0:
                    parts.append(nu)     # "replace m3 by nu (delete when 0)"
                continue
            parts.append(p)
        if not replaced:
            raise RuntimeError("psi II(a): m3=%r not found in %r" % (m3, lam))
        new = tuple(sorted(parts, reverse=True))
        return (j - 1, new), diag
    # ---- Case II(b) -------------------------------------------------------
    diag["case"], diag["sub"] = "II", "b"
    nu = m0 - 5 * j - 2
    diag["nu"] = nu
    if m0 == 0:
        # no part = 0 (mod 5): the replacement is *created*
        diag["created"] = True
        if nu <= 0:
            diag["nonpositive_created_part"] = nu
        parts = list(lam) + ([nu] if nu > 0 else [])
    else:
        diag["created"] = False
        replaced = False
        parts = []
        for p in lam:
            if not replaced and p == m0:
                replaced = True
                if nu > 0:
                    parts.append(nu)
                continue
            parts.append(p)
        if not replaced:
            raise RuntimeError("psi II(b): m0=%r not found in %r" % (m0, lam))
    new = tuple(sorted(parts, reverse=True))
    return (j + 1, new), diag


# ----------------------------------------------------------------------------
# domains
# ----------------------------------------------------------------------------


def phi_domain(j, lam):
    """phi acts on X(n) - 0 x B(n)."""
    return not (j == 0 and in_B(lam))


def psi_domain(j, lam):
    """psi acts on X(n) - 0 x C(n)  (C(n) = our A_n)."""
    return not (j == 0 and in_A(lam))


# ----------------------------------------------------------------------------
# the endpoint map pi and the p.313 shift
# ----------------------------------------------------------------------------


def pi_iterate(lam, max_steps=200000):
    """pi(lam) for lam in C(n) = A_n: iterate phi, psi, phi, psi, ... until a
    state (0; mu) with mu in B(n) is reached (p.314: 'an iteration of the
    simple mapping psi phi which is repeated until arrival at 0 x B(n)').

    Returns (mu, steps, trace).  trace is a list of dicts, one per visit,
    labelled with the map applied and the printed branch.  A repeated state is
    a hard error (it would mean the iteration cycles)."""
    n = sum(lam)
    state = (0, tuple(lam))
    trace = [dict(step=0, j=0, lam=tuple(lam), via="-", case="-", note="0 x C(n), start")]
    seen = {state}
    steps = 0
    use_phi = True
    while not (state[0] == 0 and in_B(state[1])):
        if use_phi:
            if not phi_domain(*state):
                raise RuntimeError("pi: phi applied outside its domain at %r" % (state,))
            new, diag = phi(*state)
            label = "phi"
        else:
            if not psi_domain(*state):
                raise RuntimeError("pi: psi applied outside its domain at %r" % (state,))
            new, diag = psi(*state)
            label = "psi"
        if weight(*new) != n:
            raise RuntimeError("pi: weight changed %r -> %r" % (state, new))
        steps += 1
        note = "case %s" % diag["case"]
        if diag.get("sub"):
            note += diag["sub"]
        if diag["case"] == "II" and "m" in diag:
            note += " (m=%d)" % diag["m"]
        if "nu" in diag:
            note += " (nu=%d)" % diag["nu"]
        trace.append(dict(step=steps, j=new[0], lam=new[1], via=label,
                          case=note.strip(), diag=diag))
        state = new
        if state in seen:
            raise RuntimeError("pi: repeated state %r at step %d" % (state, steps))
        seen.add(state)
        use_phi = not use_phi
        if steps > max_steps:
            raise RuntimeError("pi: step cap")
    return state[1], steps, trace


def T(lam):
    """p.313 shift: lam in D(n) -> (lam_i - t + 2i - 1) in B(n), i = 1..t."""
    t = len(lam)
    out = [lam[i] - t + 2 * (i + 1) - 1 for i in range(t)]
    return tuple(out)


def Tinv(b):
    """Inverse of T: b in B(n) -> (b_i + t - 2i + 1) in D(n)."""
    t = len(b)
    return tuple(b[i] + t - 2 * (i + 1) + 1 for i in range(t))
