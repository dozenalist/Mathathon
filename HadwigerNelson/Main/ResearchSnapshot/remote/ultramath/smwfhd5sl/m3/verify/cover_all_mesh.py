"""Strengthening of W4: a multiplicity-3, 6-label, arbitrarily fine cover of [-5,5]^2.

For every d > 0 we build a relatively open cover U of Q = [-5,5]^2 with
  (C1) every member has Euclidean diameter <= d           (mesh <= d)
  (C2) every point of Q lies in at most 3 members        (multiplicity <= 3)
  (C3) the members carry labels in {1,2,3} c {1..6} and equal-labelled members
       are DISJOINT, and at every point the members containing it have pairwise
       distinct labels.
(C3) is exactly the shape of the cover produced in paper Lemma 7.6 (the U_{n,i}
are indexed by a label and two components of one U_{n,i} are disjoint).  So the
cover is of the paper's own kind, three-valued where the paper needs two, and it
exists at EVERY mesh.  Paper Lemma 7.5 therefore cannot be repaired by any choice
of its mesh constant: multiplicity three is attainable arbitrarily finely.

Construction: triangular lattice Lam = s*{m(1,0)+n(1/2,sqrt3/2)} with s/r = 6/5,
members U_a = open disc(a, r) cap Q, r = d/2, label (m+2n) mod 3.
  covering radius   s/sqrt3     = 0.69282.. r   <  r
  third nearest  >= sqrt3 s /2  = 1.03923.. r   >  r      => multiplicity <= 3
  equal label    >= sqrt3 s     = 2.07846.. r   >  2r     => disjoint discs
All exact (see check_exact); sampling confirms.
"""
from fractions import Fraction as F
import math

SR = F(6, 5)          # s / r
SQ3 = math.sqrt(3)

def check_exact():
    """The three algebraic inequalities, in exact rational arithmetic."""
    return dict(
        covering_radius_le_r = (SR*SR <= 3),          # s^2/3 <= r^2
        third_nearest_gt_r   = (F(3,4)*SR*SR > 1),    # 3s^2/4 > r^2
        equal_label_gt_2r    = (3*SR*SR > 4),         # 3s^2 > 4r^2
        third_nearest_exact  = f"({F(3,4)*SR*SR} r^2) > r^2",
        equal_label_exact    = f"({3*SR*SR} r^2) > (2r)^2 = 4 r^2",
        s_over_r = str(SR),
    )

def build(d):
    r = d/2.0
    s = float(SR)*r
    # x = s(m+n/2), y = s n sqrt3/2 ; for |x|,|y| <= 6 one needs
    # |n| <= 7/s and |m| <= (6+3.5)/s.  Use independent ranges.
    Mx = int(9.7/s) + 2
    My = int(7.1/s) + 2
    pts = []
    for m in range(-Mx, Mx+1):
        for n in range(-My, My+1):
            x = s*(m + n/2.0); y = s*(n*SQ3/2)
            if -6.0-2*r <= x <= 6.0+2*r and -6.0-2*r <= y <= 6.0+2*r:
                pts.append((x, y, (m+2*n) % 3))
    return r, s, pts

def cell(p, r):
    return (int(math.floor(p[0]/(2*r))), int(math.floor(p[1]/(2*r))))

def sample_check(d, N=100):
    r, s, pts = build(d)
    grid = {}
    for a in pts:
        grid.setdefault(cell(a, r), []).append(a)
    def near(p):
        c = cell(p, r); out=[]
        for i in (-1,0,1):
            for j in (-1,0,1):
                out.extend(grid.get((c[0]+i, c[1]+j), []))
        return out
    hist = {}; uncovered = 0; clash = 0; worst = 0
    for i in range(N+1):
        for j in range(N+1):
            p = (-5 + 10.0*i/N, -5 + 10.0*j/N)
            cov = [a for a in near(p) if (p[0]-a[0])**2 + (p[1]-a[1])**2 < r*r]
            k = len(cov); hist[k] = hist.get(k, 0)+1
            worst = max(worst, k)
            if k == 0: uncovered += 1
            labs = [a[2] for a in cov]
            if len(set(labs)) != len(labs): clash += 1
    # exact pairwise-distance audit of the lattice: min same-label distance
    return dict(d=d, r=r, s=s, mesh=2*r, max_mult=worst, hist=hist,
                uncovered=uncovered, label_clash=clash, ndiscs=len(pts))

def audit_lattice():
    """min |a-a'| for same-label a!=a' is sqrt3*s (vector (1,1)); min for
    a!=a' is s; the third nearest distance is sqrt3*s/2.  Enumerate the
    difference vectors with |v|^2 <= 4 r^2 in units of s."""
    same = None; small = []
    for m in range(-3,4):
        for n in range(-3,4):
            if (m,n)==(0,0): continue
            q2 = F(m*m+m*n+n*n)           # |v|^2 / s^2, exact
            lab = (m+2*n) % 3
            if q2*SR*SR <= 4:             # |v| <= 2r  => discs may meet
                small.append((m,n,str(q2),lab))
            if lab == 0:
                same = q2 if same is None else min(same, q2)
    return dict(same_label_min_v2_over_s2=str(same), same_label_min_v2_over_r2=str(same*SR*SR),
                close_vectors_found=small)

if __name__ == "__main__":
    print("exact inequalities:", check_exact())
    print("lattice audit:", audit_lattice())
    ok = True
    for d in [2.0, 1.0, 0.5, 0.1, 0.01, 1e-3]:
        res = sample_check(d, N=60)
        print("d=%-8g maxmult=%d uncovered=%d labelclash=%d mesh=%g ndiscs=%d"
              % (d, res['max_mult'], res['uncovered'], res['label_clash'], res['mesh'], res['ndiscs']))
        ok &= (res['max_mult'] <= 3 and res['uncovered'] == 0 and res['label_clash'] == 0)
    print("ALL OK" if ok else "FAILURE")
