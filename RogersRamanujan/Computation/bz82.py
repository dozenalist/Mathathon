r"""Bressoud--Zeilberger 1982 reference map, source-audited (cycle 2).

Source: D. M. Bressoud, D. Zeilberger, "A short Rogers--Ramanujan bijection",
Discrete Math. 38 (1982) 313--315.  Scan, retrieved and read in full:
https://sites.math.rutgers.edu/~zeilberg/mamarimY/rrDG.pdf
sha256 = 403543088ed9465bc8e3f9918defd22a57c86a21493226c9852729af614483c6

Notation bridge (BZ82 -> this project):
    their A(n) = our D_n   (gap partitions)
    their C(n) = our A_n   (parts = 1,4 mod 5)
    their B(n) = {length k, smallest part >= k};   B(n) = T(D_n)        [p.313]
    their shift lambda |-> (lambda_i - t + 2i - 1)  is our T            [p.313]

Signed state space                                                       [p.313]
    X(n) = {(j; lam) : j in Z, lam a partition, |lam| + j(5j-1)/2 = n},
with P(j) = j(5j-1)/2 the 5-pentagonal number (NOT j(3j-1)/2).

The two involutions, and which is which.  BZ82 p.313 says one of the two
involutions "is equivalent to the Jacobi Triple Product Identity", and that one
is **psi** (the residue involution), which yields
    sum_{j in Z} (-1)^j p(n - P(j)) = |A_n|.
**phi** is the other, "considerably simpler" involution.  An earlier version of
this docstring mislabelled phi as the Jacobi side; corrected in cycle 2.

Both involutions change the parity of j, so with X^e / X^o the even / odd parts:
    phi(X^o \ (0 x B(n))) = X^e \ (0 x B(n)),      [p.314, complement]
    psi(X^o \ (0 x A(n))) = X^e \ (0 x A(n)).      [p.314, complement]
The images are complements, not intersections: this was misstated in cycle 1.

Audit status of the phi Case II formula (cycle-2 correction of a cycle-1 error).
Cycle 1 claimed the printed rule was defective and "reconstructed" it.  That was
wrong: the printed set is `0 <= z <= a+2j-2`, and the cycle-1 analysis silently
imposed `z >= 1`.  With `z >= 0` the admissible set is never empty and the rule
is complete -- verified with 0 defects over all 66 658 in-domain states of
weight <= 30.  The cycle-1 code used `z >= 1` with a fallback of 0 when the set
came out empty, which is behaviourally identical (0 discrepancies over the same
range), so the *implementation* was always faithful; only the *diagnosis* was
wrong.  This file now states the printed rule directly and keeps the fallback
only as a guarded assertion.  See Main/DECISIONS.md D-3 and Counterexamples
REGISTRY RR-X005 (retracted claim, preserved on purpose).

Internal contract of this module: the functions `phi`, `psi`, `phi_domain` and
`psi_domain` take a state `(j, lam)` that is *assumed* to lie in some X(n); the
public functions `forward` and `inverse` validate their inputs.  `lam` is a
descending tuple of positive ints and `j` is an int.

No termination proof is claimed anywhere in this file.  `_iterate` carries a
repeated-state detector keyed on (parity, state) as a *failure safeguard*, so a
cycle is reported rather than looking like a timeout; that is not a proof of
termination.
"""

from rr_core import is_residue, is_gap, weight, T, Tinv



def f(j):
    """5-pentagonal number j(5j-1)/2 appearing in X(n).  P(j-1) = P(j)-(5j-3),
    P(j+1) = P(j)+(5j+2); those two identities drive every weight computation
    in the two involutions."""
    return j * (5 * j - 1) // 2


def is_signed_state(state):
    """True iff state is (j, lam) with j an int and lam a partition.

    The internal contract of phi/psi is exactly this; X(n) membership is a
    separate condition checked by `state_weight`.
    """
    if not isinstance(state, tuple) or len(state) != 2:
        return False
    j, lam = state
    if not isinstance(j, int) or isinstance(j, bool):
        return False
    if not isinstance(lam, tuple):
        return False
    for x in lam:
        if not isinstance(x, int) or isinstance(x, bool) or x <= 0:
            return False
    return all(lam[i] >= lam[i + 1] for i in range(len(lam) - 1))


def _require_state(state, who):
    if not is_signed_state(state):
        raise ValueError("%s: not a signed state (j, descending positive tuple): %r"
                         % (who, state))


def state_weight(state):
    j, lam = state
    return sum(lam) + f(j)


# --------------------------------------------------------------------------
# phi : the Jacobi-triple-product involution (BZ82 p.314)
# --------------------------------------------------------------------------
def phi(state):
    _require_state(state, "phi")
    if not phi_domain(state, state_weight(state)):
        raise ValueError("phi: state outside its domain (the excluded set is "
                         "0 x B(n), partitions whose smallest part is >= length): %r"
                         % (state,))
    j, lam = state
    t = len(lam)

    def lamx(x):
        return lam[x - 1] if 1 <= x <= t else 0

    a = 1
    while not (2 * j + a - lamx(a) > 0):
        a += 1
    mu = 2 * j + a - lamx(a)
    la, lmu = lamx(a), lamx(mu)
    tstar = t + (1 if a > t else 0) + (1 if mu > t else 0)

    if la + lmu >= 5 * j + tstar:                                    # Case I
        # Slots: the t real parts at positions 1..t, plus one phantom slot of
        # value 0 at each of a, mu that exceeds t.  The two slots at a and mu
        # are deleted, every remaining slot is incremented, and n_new ones are
        # inserted.  Weight change = -la-lmu+(t*-2)+(la+lmu-5j-t*) = -5j-2.
        slots = [(pos, lam[pos - 1]) for pos in range(1, t + 1)]
        phantom = [pos for pos in (a, mu) if pos > t]
        slots += [(pos, 0) for pos in phantom]
        drop = sorted([a, mu])
        keep = []
        for pos, val in slots:
            if pos in drop:
                drop.remove(pos)
                continue
            keep.append(val + 1)
        # a = mu cannot occur in Case I (Lemma MX.5): if a = mu then 2j = L, and
        # a <= t forces L >= 1 hence j >= 1 while Case I forces t* <= -j <= -1;
        # and a > t forces L = 0, j = 0, contradicting t* >= 1. So the two
        # deletion slots are always distinct and both are found above.
        # Cycle 3: the former 'if drop:' fallback for the a = mu collision was
        # dead code (0 hits in 1,746,369 states, worker m3; proved in MX.5) and is
        # replaced by an assertion.
        assert not drop, "phi Case I: a == mu is impossible here (Lemma MX.5)"
        n_new = la + lmu - 5 * j - tstar
        if n_new < 0:
            raise ValueError("phi Case I: negative number of inserted 1s")
        new = tuple(sorted(keep + [1] * n_new, reverse=True))
        out = (j + 1, new)
    else:                                                            # Case II
        # BZ82 p.314, verbatim:  m = Max{z <= a+2j-2 : z + lam(a+2j-1-z) <= t+5j-2}
        # where lam(x) = 0 outside 1..t and z ranges over INTEGERS with
        # 0 <= z <= a+2j-2.  The lower bound 0 is part of the printed rule: the
        # index a+2j-1-z then runs over 1..a+2j-1, so it never leaves the
        # padded range.  Imposing z >= 1 (as cycle 1 did) makes the set empty on
        # states such as (0;(2,1,1,1)) and is the sole cause of the cycle-1
        # "defect" claim; see the module docstring.
        hi = a + 2 * j - 2
        admissible = [z for z in range(0, hi + 1)
                      if z + lamx(a + 2 * j - 1 - z) <= t + 5 * j - 2]
        if not admissible:
            # Not reached on any state of weight <= 30 (0 of 10 285 Case-II
            # states); kept as an explicit obligation, not a silent default.
            raise ValueError("phi Case II: admissible set empty (unproved case)")
        m = max(admissible)
        p2 = t + 5 * j - 3 - m
        if m < 0 or p2 < 0:
            raise ValueError("phi Case II: negative created part (%d,%d)" % (m, p2))
        rest = [x - 1 for x in lam if x - 1 > 0]
        out = (j - 1, tuple(sorted(rest + [p for p in (m, p2) if p > 0], reverse=True)))

    if state_weight(out) != state_weight(state):
        raise AssertionError("phi: weight not preserved at %r" % (state,))
    return out


def phi_domain(state, n):
    """phi is defined on X(n) minus 0 x B(n)   (B = smallest part >= length)."""
    if not is_signed_state(state):
        return False
    j, lam = state
    if state_weight(state) != n:
        return False
    if j == 0:
        k = len(lam)
        if all(x >= k for x in lam):
            return False
    return True


# --------------------------------------------------------------------------
# psi : the residue involution  (BZ82 p.314)
# --------------------------------------------------------------------------
def _largest_mod(lam, r):
    best = 0
    for x in lam:
        if x % 5 == r and x > best:
            best = x
    return best


def psi(state):
    _require_state(state, "psi")
    if not psi_domain(state, state_weight(state)):
        raise ValueError("psi: state outside its domain (the excluded set is "
                         "0 x A(n)): %r" % (state,))
    j, lam = state
    t0 = sum(1 for x in lam if x % 5 == 0)
    m0, m2, m3 = _largest_mod(lam, 0), _largest_mod(lam, 2), _largest_mod(lam, 3)
    parts = list(lam)

    if t0 + j > 0 or m2 > 0:                                         # Case I
        thr = 5 * t0 + 5 * j - 3
        if thr >= m2:                                                # I(a)
            kept = []
            for x in parts:
                if x % 5 == 0:
                    if x - 5 > 0:
                        kept.append(x - 5)
                else:
                    kept.append(x)
            if thr <= 0:
                raise ValueError("psi I(a): nonpositive inserted part")
            kept.append(thr)
            out = (j - 1, tuple(sorted(kept, reverse=True)))
        else:                                                        # I(b)
            parts.remove(m2)
            kept = [x + 5 if x % 5 == 0 else x for x in parts]
            cnt = (m2 - 5 * j - 2 - 5 * t0)
            if cnt % 5 or cnt < 0:
                raise ValueError("psi I(b): bad multiplicity %d" % cnt)
            kept += [5] * (cnt // 5)
            out = (j + 1, tuple(sorted(kept, reverse=True)))
    else:                                                            # Case II
        thr = m3 + 5 * j - 3
        if thr >= m0:                                                # II(a)
            if m3 == 0:
                raise ValueError("psi II(a): no part = 3 (mod 5) to move")
            parts.remove(m3)
            if thr > 0:
                parts.append(thr)
            out = (j - 1, tuple(sorted(parts, reverse=True)))
        else:                                                        # II(b)
            new = m0 - 5 * j - 2
            if new <= 0:
                raise ValueError("psi II(b): nonpositive created part %d" % new)
            if m0 > 0:
                parts.remove(m0)
            parts.append(new)
            out = (j + 1, tuple(sorted(parts, reverse=True)))

    if state_weight(out) != state_weight(state):
        raise AssertionError("psi: weight not preserved at %r -> %r" % (state, out))
    return out


def psi_domain(state, n):
    """psi is defined on X(n) minus 0 x A(n)."""
    if not is_signed_state(state):
        return False
    j, lam = state
    if state_weight(state) != n:
        return False
    if j == 0 and is_residue(lam):
        return False
    return True


# --------------------------------------------------------------------------
# iteration to the endpoints
# --------------------------------------------------------------------------
def _iterate(start, first, second, target_pred, n, max_steps=10 ** 6):
    """Apply first, second, first, ... until target_pred(state); return (trace, state).

    Termination is checked against an explicit repeat detector, not a step cap:
    a repeated state proves the orbit cycles and the map is not total there.
    """
    trace = [start]
    state = start
    # The next involution is determined by the step parity, so the repeated-state
    # key must include the parity: seeing the same state at the other parity is
    # NOT yet a cycle.  (Cycle 1 keyed on the state alone and could have reported
    # a false cycle; no such case occurs in the tested range, but the detector is
    # now sound by construction.)
    seen = {(0, state)}
    if target_pred(state):
        return trace, state
    for step in range(max_steps):
        state = first(state) if step % 2 == 0 else second(state)
        trace.append(state)
        if target_pred(state):
            return trace, state
        key = ((step + 1) % 2, state)
        if key in seen:
            raise RuntimeError("orbit cycles at step %d from %r" % (step, start))
        seen.add(key)
    raise RuntimeError("iteration exceeded its safeguard of %d steps from %r"
                       % (max_steps, start))


def _in_B(lam):
    k = len(lam)
    return all(x >= k for x in lam)


def pi_forward(lam):
    """0 x A_n -> 0 x B_n by iterating (phi then psi).  Returns (b, trace)."""
    n = weight(lam)
    if not is_residue(lam):
        raise ValueError("pi_forward: input not in A_n: %r" % (lam,))
    trace, end = _iterate((0, lam), phi, psi, lambda st: st[0] == 0 and _in_B(st[1]), n)
    return end[1], trace


def pi_inverse(b):
    """0 x B_n -> 0 x A_n by iterating (psi then phi).  Returns (lam, trace)."""
    n = weight(b)
    if not _in_B(b):
        raise ValueError("pi_inverse: input not in B_n: %r" % (b,))
    trace, end = _iterate((0, b), psi, phi,
                          lambda st: st[0] == 0 and is_residue(st[1]), n)
    return end[1], trace


def forward(lam):
    """Our target map D_n <- A_n as stated in the project convention.

    BZ82 gives A_n -> D_n directly, so this is BZ82's map:
        A_n --(0 x id)--> 0 x A_n --iterate(phi,psi)--> 0 x B_n --T^{-1}--> D_n
    """
    b, _ = pi_forward(lam)
    return Tinv(b)


def inverse(lam):
    """D_n -> A_n:  D_n --T--> 0 x B_n --iterate(psi,phi)--> 0 x A_n."""
    if not is_gap(lam):
        raise ValueError("inverse: input not in D_n: %r" % (lam,))
    a, _ = pi_inverse(T(lam))
    return a
