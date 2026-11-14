"""Bressoud--Zeilberger 1982 reference map, reconstructed from the scan.

Source: D. M. Bressoud, D. Zeilberger, "A short Rogers--Ramanujan bijection",
Discrete Math. 38 (1982) 313--315.  Scan:
https://sites.math.rutgers.edu/~zeilberg/mamarimY/rrDG.pdf
sha256(pdf) = 403543088ed9465bc8e3f9918defd22a57c86a21493226c9852729af614483c6

Notation bridge (BZ82 -> this project):
    their A(n) = our D_n   (gap partitions)
    their C(n) = our A_n   (parts = 1,4 mod 5)
    their B(n) = {length k, smallest part >= k};  B(n) = T(D_n)   [p.313]
    their shift  lambda |-> (lambda_i - t + 2i - 1)  is our T          [p.313]

Signed state space                                                        [p.313]
    X(n) = {(j; lam) : j in Z, lam a partition, |lam| + j(5j-1)/2 = n}.
    X^e / X^o = even / odd j.  Both involutions below change parity of j, so
    phi(X^o) = X^e cap (0 x B(n)) and psi(X^o) = X^e cap (0 x A(n)) [p.314].

Reconstruction decisions where the scan/OCR is ambiguous (recorded, and tested):
  R-1  Case I / Case II of phi split on  lam(a)+lam(mu) >= 5j + t*  (tie -> I).
  R-2  "add 1 to each of the remaining parts" is implemented on the padded slot
       list of length t*, so a phantom slot 0 becomes the part 1.
  R-3  Case II of phi: the range of the maximum m is 1 <= z <= a+2j-1, i.e.
       the index a+2j-1-z must be >= 0.  The scan prints a bound that excludes
       the value needed by BZ82's own example (3) on p.315, so the index bound
       is read as the intended constraint.  Verified against that example.
  R-4  psi Case I(a) is taken for 5t0+5j-3 >= m2  (tie -> I(a)), because BZ82's
       example (2) on p.315 is exactly a tie and is labelled I(a).
  R-5  psi Case II(a) is taken for m3+5j-3 >= m0 (tie -> II(a)).
  R-6  "m_i = largest part = i (mod 5), or 0" is read with m_i = 0 meaning the
       virtual part 0, so psi Case II(b) with m0 = 0 creates the part -5j-2.
"""

from rr_core import is_residue, is_gap, weight, T, Tinv



def f(j):
    """Shifted pentagonal number j(5j-1)/2 appearing in X(n)."""
    return j * (5 * j - 1) // 2


def state_weight(state):
    j, lam = state
    return sum(lam) + f(j)


# --------------------------------------------------------------------------
# phi : the Jacobi-triple-product involution (BZ82 p.314)
# --------------------------------------------------------------------------
def phi(state):
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
        if drop:
            # a == mu with only one slot of that value: remove a second copy of
            # the same value if one exists, otherwise the state is degenerate.
            v = lam[a - 1] if a <= t else 0
            idx = next((i for i, x in enumerate(keep) if x - 1 == v), None)
            if idx is None:
                raise ValueError("phi Case I: slot %r not removable" % (drop,))
            del keep[idx]
        n_new = la + lmu - 5 * j - tstar
        if n_new < 0:
            raise ValueError("phi Case I: negative number of inserted 1s")
        new = tuple(sorted(keep + [1] * n_new, reverse=True))
        out = (j + 1, new)
    else:                                                            # Case II
        hi = t + 5 * j - 3
        # Derived selection rule (DECISIONS D-3).  BZ82 prints
        #     m = Max{z <= a+2j-2 : z + lam(a+2j-1-z) <= t+5j-2}
        # and then creates parts m and hi-m.  The two created parts enter only
        # as an unordered pair, and the printed set is empty in a few states
        # (e.g. (0;(2,1,1,1)), forced by BZ82's own example (3) on p.315), so
        # the rule is completed by defaulting to m = 0 in that case: the pair
        # then degenerates to the single part hi.  Exhaustively verified
        # against phi-phi = id on every Case-II state of weight <= 30.
        m = 0
        for z in range(a + 2 * j - 2, 0, -1):
            if z + lamx(a + 2 * j - 1 - z) <= t + 5 * j - 2:
                m = z
                break
        if hi < 0 or m > hi:
            raise ValueError("phi Case II: no admissible m (hi=%d, m=%d)" % (hi, m))
        p2 = hi - m
        rest = [x - 1 for x in lam if x - 1 > 0]
        out = (j - 1, tuple(sorted(rest + [p for p in (m, p2) if p > 0], reverse=True)))

    if state_weight(out) != state_weight(state):
        raise AssertionError("phi: weight not preserved at %r" % (state,))
    return out


def phi_domain(state, n):
    """phi is defined on X(n) minus 0 x B(n)   (B = smallest part >= length)."""
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
    seen = {start}
    if target_pred(state):
        return trace, state
    for step in range(max_steps):
        state = first(state) if step % 2 == 0 else second(state)
        trace.append(state)
        if target_pred(state):
            return trace, state
        if state in seen:
            raise RuntimeError("orbit cycles at step %d from %r" % (step, start))
        seen.add(state)
    raise RuntimeError("iteration did not terminate from %r" % (start,))


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
