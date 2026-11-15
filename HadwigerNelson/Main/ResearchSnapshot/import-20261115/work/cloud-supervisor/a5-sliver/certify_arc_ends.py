"""A5 sliver caveat closure (research desk): certify the four NON-corner arc ends exactly.

Definitions (quoted by the verifier lane from block4_check.py:65-75, smwguidy9 m2):
  c1 = (sqrt3/2, 1/2), c3 = (-sqrt3/2, 1/2), ci = (0, 1);  d2 = squared distance;
  m_lo = d2(p,c1) - 1, m_lo2 = d2(p,c3) - 1, m_hi = 1 - d2(p,ci), m_edge = 3/4 - p_x^2, m_floor = p_y - 1;
  H = {p : all five margins > 0} (open).
Which margin defines each non-corner arc end (domain file A1, lane notes): entry arcs (qm, am) have their
LOW end at m_lo = 0; exit arcs (ap, qp) have their HIGH end at m_lo2 = 0.

For each end the decimal u from the domain file is bracketed by [u-1e-9, u+1e-9] and we certify, with the
exact Fraction interval arithmetic of certify_sliver.py:
  (i)  a strict sign change of the defining margin g across the bracket,
  (ii) g' one-signed on the bracket (so the root is unique there), and
  (iii) g > 0 on the ARC side of the root (u > root for a low end, u < root for a high end),
so the arc, being the connected set of u with v(u) in H, ends at that root inside the bracket.
Also re-certifies the corner ends (m_hi = 0) with the same orientation test, and records m_hi's definition,
which closes the far-apex caveat: |A2 - ci| > 1 (certified in certify_sliver.py) means m_hi(A2) < 0.
"""
import os, sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import certify_sliver as cs

I, Dl, cs_fn = cs.I, cs.Dl, cs.cs
S3 = cs.S3
C1 = (S3 / 2, I(Fr(1, 2)))
C3 = (-S3 / 2, I(Fr(1, 2)))
CI = (I(0), I(1))


def point(base, U, shift):
    u = Dl(U, I(1), I(0))
    c, s = cs_fn(u)
    if shift:
        c, s = -c, -s
    return base[0] + c, base[1] + s


def margin(name, p):
    d2 = lambda q: (p[0] - q[0]).sq() + (p[1] - q[1]).sq()
    if name == 'm_lo':
        return d2(C1) - 1
    if name == 'm_lo2':
        return d2(C3) - 1
    if name == 'm_hi':
        return 1 - d2(CI)
    raise ValueError(name)


ENDS = [
    # label, base, shift, margin, decimal u, side ('low' => arc is u > root; 'high' => arc is u < root)
    ('B1 entry qm  low  (theta1 22.759 deg)', cs.QM, 0, 'm_lo', '0.201264277832277', 'low'),
    ('B1 entry qm  high (corner)          ', cs.QM, 0, 'm_hi', '0.255989076986739', 'high'),
    ('B1 exit  ap  low  (corner)          ', cs.AP, 1, 'm_hi', '-0.215250437021530', 'low'),
    ('B1 exit  ap  high (theta3 184.035)  ', cs.AP, 1, 'm_lo2', '0.035230739064970', 'high'),
    ('B2 entry am  low  (theta1 -4.035)   ', cs.AM, 0, 'm_lo', '-0.035230739064970', 'low'),
    ('B2 entry am  high (corner)          ', cs.AM, 0, 'm_hi', '0.215250437021530', 'high'),
    ('B2 exit  qp  low  (corner)          ', cs.QP, 1, 'm_hi', '-0.245375379412415', 'low'),
    ('B2 exit  qp  high (theta3 163.074)  ', cs.QP, 1, 'm_lo2', '-0.148788059725258', 'high'),
]


def main():
    out = []
    log = lambda s: (out.append(s), print(s, flush=True))
    log('A5 arc-end certificate (exact Fraction intervals, outward rounding 2^-%d)' % cs.PREC)
    allok = True
    e = Fr(1, 10 ** 9)
    for label, base, shift, mname, ustr, side in ENDS:
        u = Fr(ustr)
        lo, hi = u - e, u + e
        glo = margin(mname, point(base, I(lo), shift)).v
        ghi = margin(mname, point(base, I(hi), shift)).v
        gd = margin(mname, point(base, I(lo, hi), shift)).g1
        change = (glo.hi < 0 < ghi.lo) or (ghi.hi < 0 < glo.lo)
        mono = gd.lo > 0 or gd.hi < 0
        arc_side_pos = (ghi.lo > 0) if side == 'low' else (glo.lo > 0)
        ok = change and mono and arc_side_pos
        allok &= ok
        log(f'  {label} {mname}=0 in [{float(lo):.12f},{float(hi):.12f}]: g(lo)={glo} g(hi)={ghi} '
            f"g'={gd} | sign change {change}, unique {mono}, positive on arc side {arc_side_pos} -> {ok}")
    log("m_hi = 1 - |p - ci|^2 (block4_check.py:71, ci=(0,1) at :65): m_hi(p) < 0 <=> |p - ci| > 1. "
        "certify_sliver.py certifies |A2 - ci|^2 > 1 on all pieces, so the far apex is outside H.")
    log(f'ALL ARC ENDS CERTIFIED: {allok}')
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'arc_ends_output.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    return 0 if allok else 1


if __name__ == '__main__':
    sys.exit(main())
