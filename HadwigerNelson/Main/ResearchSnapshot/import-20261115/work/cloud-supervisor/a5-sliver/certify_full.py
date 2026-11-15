"""A5, desk re-derivation of the C2 F5-box exclusion over the FULL arc1 x arc3 domain of B1 and B2.

Claim certified (the desk's reading of C2, stated explicitly): for every (u1, u3) in arc1 x arc3 (true arcs,
over-covered by rational boxes reaching 1e-9 past every certified arc end), with
  v1 = base1 + (c(u1), s(u1)), v3 = base3 - (c(u3), s(u3)), D = v3 - v1, |D| < 2,
  A1 = M + h n, A2 = M - h n,  M = (v1+v3)/2, h = sqrt(1-|D|^2/4), n = (-D_y, D_x)/|D|,
BOTH apexes lie outside the open region H = {all five margins > 0}, where
  m_lo = |p-c1|^2-1, m_lo2 = |p-c3|^2-1, m_hi = 1-|p-ci|^2, m_edge = 3/4-p_x^2, m_floor = p_y-1
(c1 = (sqrt3/2,1/2), c3 = (-sqrt3/2,1/2), ci = (0,1); block4_check.py:65-75 as quoted by the verifier lane).

Per sub-box tests (exact Fraction intervals from certify_sliver.py):
  A2: some margin of A2 has interval hi < 0.
  A1: either some margin of A1 has hi < 0, or (D_x < 0, Delta > 0, |D|^2 < 4 and R.lo > 0), where
      R = (1-|D|^2/4) D_x^2 - |D|^2 Delta^2, Delta = M_y - 1; R > 0 <=> m_floor(A1) < 0 (certify_sliver.py).
  Corner box (the only place where A1 -> ci and every A1 margin -> 0): the monotonicity argument of
  certify_sliver.py on [a1, u1*+1e-9] x [u3*-1e-9, b3]: dR/du1 < 0 and dR/du3 > 0 there, together with
  R(corner) = 0 exactly (endpoint identity), give R >= 0, i.e. m_floor(A1) <= 0, on that box's part of the domain.
"""
import os, sys, time
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import certify_sliver as cs

I, Dl = cs.I, cs.Dl
S3 = cs.S3
C1 = (S3 / 2, I(Fr(1, 2)))
C3 = (-S3 / 2, I(Fr(1, 2)))
CI = (I(0), I(1))
E9 = Fr(1, 10 ** 9)


def margins(px, py):
    d2 = lambda q: (px - q[0]).sq() + (py - q[1]).sq()
    return {'m_lo': d2(C1) - 1, 'm_lo2': d2(C3) - 1, 'm_hi': 1 - d2(CI),
            'm_edge': I(Fr(3, 4)) - px.sq(), 'm_floor': py - 1}


def apexes(b1, b3, U1, U3):
    R, Dx, Dy, D2, Delta, v1, v3 = cs.quantities(b1, b3, U1, U3, grad=False)
    if not D2.hi < 4:
        return None
    h = (1 - D2 / 4).sqrt(); d = D2.sqrt()
    Mx, My = (v1[0] + v3[0]) / 2, (v1[1] + v3[1]) / 2
    nx, ny = (-Dy) / d, Dx / d
    A1 = (Mx + h * nx, My + h * ny)
    A2 = (Mx - h * nx, My - h * ny)
    return R, Dx, Delta, D2, A1, A2


def box_ok(b1, b3, B1, B3, stats):
    r = apexes(b1, b3, I(*B1), I(*B3))
    if r is None:
        return False
    R, Dx, Delta, D2, A1, A2 = r
    m2 = margins(*A2)
    a2 = [k for k, m in m2.items() if m.hi < 0]
    if not a2:
        return False
    m1 = margins(*A1)
    a1 = [k for k, m in m1.items() if m.hi < 0]
    if not a1:
        if Dx.hi < 0 and Delta.lo > 0 and D2.hi < 4 and R.lo > 0:
            a1 = ['R>0 (m_floor<0)']
        else:
            return False
    for k in a1:
        stats['A1'][k] = stats['A1'].get(k, 0) + 1
    for k in a2:
        stats['A2'][k] = stats['A2'].get(k, 0) + 1
    return True


def corner_ok(b1, b3, B1, B3):
    R, Dx, Dy, D2, Delta, _, _ = cs.quantities(b1, b3, I(*B1), I(*B3))
    r = apexes(b1, b3, I(*B1), I(*B3))
    if r is None:
        return False
    m2 = margins(*r[5])
    return (Dx.v.hi < 0 and Delta.v.lo > 0 and D2.v.hi < 4 and R.g1.hi < 0 and R.g3.lo > 0
            and any(m.hi < 0 for m in m2.values()))


def cover(b1, b3, U1, U3, corner, maxdepth=60):
    """bisect U1 x U3 minus the corner box; return (ok, nboxes, failures)."""
    stats = {'A1': {}, 'A2': {}, 'n': 0, 'fail': []}
    stack = [(U1, U3, 0)]
    W1, W3 = U1[1] - U1[0], U3[1] - U3[0]
    (c1lo, c1hi), (c3lo, c3hi) = corner
    while stack:
        B1, B3, dep = stack.pop()
        # skip boxes entirely inside the corner box (handled by monotonicity)
        if c1lo <= B1[0] and B1[1] <= c1hi and c3lo <= B3[0] and B3[1] <= c3hi:
            continue
        inside_corner_partly = not (B1[1] <= c1lo or B1[0] >= c1hi or B3[1] <= c3lo or B3[0] >= c3hi)
        stats['n'] += 1
        if not inside_corner_partly and box_ok(b1, b3, B1, B3, stats):
            continue
        if dep >= maxdepth:
            stats['fail'].append((B1, B3)); continue
        if (B1[1] - B1[0]) / W1 >= (B3[1] - B3[0]) / W3:
            # split at the corner boundary first if it cuts the box
            m = next((x for x in (c1lo, c1hi) if B1[0] < x < B1[1]), (B1[0] + B1[1]) / 2)
            stack += [((B1[0], m), B3, dep + 1), ((m, B1[1]), B3, dep + 1)]
        else:
            m = next((x for x in (c3lo, c3hi) if B3[0] < x < B3[1]), (B3[0] + B3[1]) / 2)
            stack += [(B1, (B3[0], m), dep + 1), (B1, (m, B3[1]), dep + 1)]
    return not stats['fail'], stats


BLOCKS = [
    # name, base1, base3, arc1 ends (low, high=corner), arc3 ends (low=corner, high)
    ('B1', cs.QM, cs.AP, ('0.201264277832277', '0.255989076986739'), ('-0.215250437021530', '0.035230739064970')),
    ('B2', cs.AM, cs.QP, ('-0.035230739064970', '0.215250437021530'), ('-0.245375379412415', '-0.148788059725258')),
]


def main():
    t0 = time.time()
    out = []
    log = lambda s: (out.append(s), print(s, flush=True))
    log('A5 FULL-DOMAIN apex exclusion (desk re-derivation of C2); exact Fraction intervals 2^-%d' % cs.PREC)
    allok = True
    for name, b1, b3, a1, a3 in BLOCKS:
        U1 = (Fr(a1[0]) - E9, Fr(a1[1]) + E9)
        U3 = (Fr(a3[0]) - E9, Fr(a3[1]) + E9)
        ok_c = False
        for frac in (Fr(1, 5), Fr(1, 10), Fr(1, 20), Fr(1, 50), Fr(1, 200)):
            corner = ((U1[1] - (U1[1] - U1[0]) * frac, U1[1]), (U3[0], U3[0] + (U3[1] - U3[0]) * frac))
            # certify the corner box by monotonicity, subdividing it (all sub-boxes need the sign conditions)
            okc, st = True, [corner]
            sub = [corner]; nsub = 0
            while sub:
                B1c, B3c = sub.pop(); nsub += 1
                if corner_ok(b1, b3, B1c, B3c):
                    continue
                if nsub > 4000:
                    okc = False; break
                if (B1c[1] - B1c[0]) >= (B3c[1] - B3c[0]) * (U1[1] - U1[0]) / (U3[1] - U3[0]):
                    m = (B1c[0] + B1c[1]) / 2; sub += [((B1c[0], m), B3c), ((m, B1c[1]), B3c)]
                else:
                    m = (B3c[0] + B3c[1]) / 2; sub += [(B1c, (B3c[0], m)), (B1c, (m, B3c[1]))]
            if okc:
                ok_c = True
                log(f'  {name}: corner box u1 in [{float(corner[0][0]):.9f},{float(corner[0][1]):.9f}], '
                    f'u3 in [{float(corner[1][0]):.9f},{float(corner[1][1]):.9f}] certified by monotonicity '
                    f'({nsub} sub-boxes; dR/du1<0, dR/du3>0, Dx<0, Delta>0, |D|<2, A2 outside H)')
                break
        if not ok_c:
            log(f'  {name}: corner box NOT certified'); allok = False; continue
        ok, st = cover(b1, b3, U1, U3, corner)
        allok &= ok
        log(f'  {name}: rest of domain certified={ok} boxes={st["n"]} failures={len(st["fail"])}')
        log(f'     A1 excluded by: {st["A1"]}')
        log(f'     A2 excluded by: {st["A2"]}')
    log(f'ALL BLOCKS CERTIFIED: {allok}   ({time.time() - t0:.1f} s)')
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'full_output.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    return 0 if allok else 1


if __name__ == '__main__':
    sys.exit(main())
