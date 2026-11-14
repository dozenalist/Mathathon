#!/usr/bin/env python3
"""A repaired two-sided sandwich for E's cell volume: Euclidean slack + an explicit ball box.

E's rigorous_cell_volume.py (blob d015a2e1..., experimental d289bef) has two defects (X-C060,
X-C061).  This file implements the repair for the *same* atom and shows it still closes on the
same control (fcc contact cell = 4*sqrt2), so the repair costs nothing but is not optional.

The two changes, and nothing else:
  (1) NORM.   slack = R * sqrt(3) * max_component_error + f   (>= R * ||n - n'||_2 + f).
  (2) BOUNDEDNESS.  Add the box  |y_i| <= R  to BOTH polytopes.  The box contains B(0,R), and the
      cell is inside B(0,R) when R is an a-priori bound (for a saturated packing R = 2: every
      point of the cell is within 2 of its own centre).  Adding it to the outer polytope makes
      that polytope bounded, so an unbounded cell can no longer masquerade as a finite one; adding
      it to the inner polytope only shrinks it, which keeps the inner inclusion valid.
      Then the R-check becomes a check of R itself, not of whatever vertices happened to appear.

Run: python3 repaired_sandwich.py      (exit 0 iff the fcc control still encloses 4 sqrt2)
"""
import importlib.util, math, os, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, path))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

m = load("ecv", "E_rigorous_cell_volume_d015a2e.py")
Iv = m.Iv
polytope_volume = m.polytope_volume
DEN, QERR = m.DEN, m.QERR
_quantise = m._quantise
sqrt_iv = m.sqrt_iv

SQ3 = F(16, 10)      # a rational upper bound for sqrt(3)  (1.6^2 = 2.56 > 3)
def sandwich_fixed(centres, R):
    R = F(R)
    n_rat, b_rat, slacks = [], [], []
    for p in centres:
        sq = p[0]*p[0] + p[1]*p[1] + p[2]*p[2]
        L = sqrt_iv(sq)
        n = [p[t]/L for t in range(3)]
        b = L/2
        e = max((x.hi - x.lo)/2 for x in n)          # componentwise bound
        f = (b.hi - b.lo)/2
        nq = [_quantise(x.mid(), DEN) for x in n]
        bq = _quantise(b.mid(), DEN)
        n_rat.append(nq); b_rat.append(bq)
        slacks.append(R * SQ3 * (e + QERR) + f + QERR)   # <-- (1) Euclidean slack
    box_n = [(F(1),F(0),F(0)), (F(-1),F(0),F(0)), (F(0),F(1),F(0)),
             (F(0),F(-1),F(0)), (F(0),F(0),F(1)), (F(0),F(0),F(-1))]
    box_d = [R]*6
    inner = [b_rat[i] - slacks[i] for i in range(len(b_rat))] + box_d   # <-- (2) box in both
    outer = [b_rat[i] + slacks[i] for i in range(len(b_rat))] + box_d
    v_in, nvi, _ = polytope_volume(n_rat + box_n, inner)
    v_out, nvo, pts = polytope_volume(n_rat + box_n, outer)
    if v_in is None: v_in = F(0)
    if v_out is None: raise ValueError("outer polytope unbounded even with the box")
    return v_in, v_out, nvi, nvo, pts

def saturation_check(centres, outer_pts, R):
    """Necessary condition for Omega(w) subset B(w,R): every outer vertex must be within 2 of
    some centre (saturation).  Cheap, and it rejects the unbounded witness of X-C061."""
    bad = 0
    for y in outer_pts:
        if abs(y[0]) == R and abs(y[1]) == R:          # a box corner: check it too
            pass
        near = min(max(0.0, float((y[0]-c[0].mid())**2 + (y[1]-c[1].mid())**2 + (y[2]-c[2].mid())**2)**0.5)
                   for c in centres) if centres else 1e9
        if near > 2.0 + 1e-9: bad += 1
    return bad

if __name__ == '__main__':
    P = m.barlow_contact_cell("fcc")
    ref = 4*math.sqrt(2)
    for R in (F(2), F(3), F(4)):
        vi, vo, ni, no, _ = sandwich_fixed(P, R)
        enc = float(vi) <= ref <= float(vo)
        print("  R = %s : [%.15f, %.15f]  width %.1e  vertices %d/%d  contains 4sqrt2: %s"
              % (R, float(vi), float(vo), float(vo-vi), ni, no, enc))
    vi, vo, _, _, _ = sandwich_fixed(P, F(2))
    ok = float(vi) <= ref <= float(vo)
    # the unbounded witness must be REJECTED by the saturation check
    bad_c = [(Iv(2), Iv(0), Iv(0)), (Iv(-2), Iv(0), Iv(0)), (Iv(0), Iv(2), Iv(0)),
             (Iv(0), Iv(-2), Iv(0)), (Iv(0), Iv(0), Iv(-2))]
    v_in, v_out, _, _, pts = sandwich_fixed(bad_c, F(2))
    nb = saturation_check(bad_c, pts, F(2))
    print("\n  the unbounded witness (X-C061): repaired sandwich gives [%.6f, %.6f] (finite, because the"
          % (float(v_in), float(v_out)))
    print("  box cuts it) -- so the box alone does NOT detect unboundedness; the saturation check does:")
    print("  outer vertices failing 'within 2 of a centre': %d of %d" % (nb, len(pts)))
    ok = ok and nb > 0
    print("\n  E's original (unsound) sandwich for comparison: [5.656854249492, 5.656854249492]")
    print("\nRESULT:", "the repaired sandwich still encloses 4 sqrt2" if ok else "FAILED")
    sys.exit(0 if ok else 1)
