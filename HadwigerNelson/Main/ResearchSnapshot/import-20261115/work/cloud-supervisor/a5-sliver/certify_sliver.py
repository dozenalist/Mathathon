"""A5 sliver certificate (research desk, 2026-11-14).

Rigorous: exact rational interval arithmetic (fractions.Fraction endpoints, outward rounding to
multiples of 2^-120), forward-mode derivatives carried as intervals, sqrt constants enclosed via
integer isqrt. No floating point enters any decision.

Statement certified (domain and target from inbox 20261114T224105-download-4-A5-SLIVER-DEFS.md, addendum
block 42, swarm smwgy3s8k m2):
  For every (u1, u3) in each of the three uncovered pieces P1, P2, P3, with
    v1 = base1 + (c(u1), s(u1)),  v3 = base3 - (c(u3), s(u3))     [shift 0 / shift pi]
    c(u) = (1-u^2)/(1+u^2), s(u) = 2u/(1+u^2),  ci = (0,1),
    D = v3 - v1, Delta = (v1_y+v3_y)/2 - 1, R = (1 - |D|^2/4) D_x^2 - |D|^2 Delta^2,
  we have D_x < 0, Delta > 0, |D|^2 < 4 and R >= 0; hence the lower apex A1 = M + h n,
  n = (-D_y, D_x)/|D|, h = sqrt(1-|D|^2/4), satisfies A1_y <= 1 (m_floor(A1) <= 0), i.e. A1 is not in
  the open region H. Equality R = 0 occurs only at the exact closed corner of P1 and P2, where A1 = ci.
  Supplementary: the far apex A2 = M - h n satisfies |A2 - ci| > 1 (the domain file's '> 1.5' is FALSE on part
  of P1; see the separate disproof line in the output).

Proof structure:
  P3: direct interval lower bound R > 0 on a subdivision of an over-covering rational box.
  P1, P2: on an over-covering rational box B = [a1, b1] x [a3, b3] that contains the exact corner
  (u1*, u3*) at its (b1-side, a3-side) we certify dR/du1 < 0 and dR/du3 > 0 on all of B. Then for any
  (u1, u3) in B with u1 <= u1*, u3 >= u3*:  R(u1,u3) >= R(u1*,u3) >= R(u1*,u3*) = 0 (mean value
  theorem on segments inside B). R(u1*,u3*) = 0 is the endpoint identity: |v1-ci| = |v3-ci| = 1 at
  the corner and (v1-ci) x (v3-ci) > 0 force A1 = ci (checked algebraically in the report), so
  A1_y - 1 = 0 and R = 0. The corner coordinates u1*, u3* are the unique roots of
  g(u) = 1 - |v(u) - ci|^2 in the rational brackets [u -/+ 1e-9]; uniqueness is certified by a strict
  sign change of g at the bracket ends and a one-signed derivative g' on the bracket.
"""
from fractions import Fraction as Fr
from math import isqrt
import sys, time

PREC = 120
SCALE = 1 << PREC


def rdown(x):
    return Fr((x.numerator * SCALE) // x.denominator, SCALE)


def rup(x):
    return Fr(-((-x.numerator * SCALE) // x.denominator), SCALE)


class I:
    __slots__ = ('lo', 'hi')

    def __init__(self, lo, hi=None):
        hi = lo if hi is None else hi
        lo, hi = Fr(lo), Fr(hi)
        assert lo <= hi, (lo, hi)
        self.lo, self.hi = rdown(lo), rup(hi)

    def __add__(a, b):
        if isinstance(b, Dl): return NotImplemented
        b = b if isinstance(b, I) else I(b); return I(a.lo + b.lo, a.hi + b.hi)
    __radd__ = __add__

    def __neg__(a):
        return I(-a.hi, -a.lo)

    def __sub__(a, b):
        if isinstance(b, Dl): return NotImplemented
        b = b if isinstance(b, I) else I(b); return I(a.lo - b.hi, a.hi - b.lo)

    def __rsub__(a, b):
        return I(b) - a

    def __mul__(a, b):
        if isinstance(b, Dl): return NotImplemented
        b = b if isinstance(b, I) else I(b)
        p = (a.lo * b.lo, a.lo * b.hi, a.hi * b.lo, a.hi * b.hi)
        return I(min(p), max(p))
    __rmul__ = __mul__

    def inv(a):
        assert a.lo > 0 or a.hi < 0, 'division by interval containing 0'
        return I(1 / a.hi, 1 / a.lo)

    def __truediv__(a, b):
        b = b if isinstance(b, I) else I(b); return a * b.inv()

    def __rtruediv__(a, b):
        return I(b) * a.inv()

    def sq(a):
        if a.lo >= 0: return I(a.lo * a.lo, a.hi * a.hi)
        if a.hi <= 0: return I(a.hi * a.hi, a.lo * a.lo)
        return I(0, max(a.lo * a.lo, a.hi * a.hi))

    def sqrt(a):
        assert a.lo >= 0
        lo = Fr(isqrt((a.lo.numerator * SCALE * SCALE) // a.lo.denominator), SCALE)
        n = -((-a.hi.numerator * SCALE * SCALE) // a.hi.denominator)
        r = isqrt(n); r = r if r * r == n else r + 1
        return I(lo, Fr(r, SCALE))

    def __repr__(self):
        return f'[{float(self.lo):.12g}, {float(self.hi):.12g}]'


def sqrt_const(n):
    k = 200
    r = isqrt(n * 4 ** k)
    return I(Fr(r, 2 ** k), Fr(r + 1, 2 ** k))


class Dl:
    """value interval + gradient intervals w.r.t. (u1, u3)"""
    __slots__ = ('v', 'g1', 'g3')

    def __init__(self, v, g1=None, g3=None):
        self.v = v if isinstance(v, I) else I(v)
        self.g1 = g1 if g1 is not None else I(0)
        self.g3 = g3 if g3 is not None else I(0)

    def _c(b):
        return b if isinstance(b, Dl) else Dl(b)

    def __add__(a, b):
        b = Dl._c(b); return Dl(a.v + b.v, a.g1 + b.g1, a.g3 + b.g3)
    __radd__ = __add__

    def __neg__(a):
        return Dl(-a.v, -a.g1, -a.g3)

    def __sub__(a, b):
        b = Dl._c(b); return Dl(a.v - b.v, a.g1 - b.g1, a.g3 - b.g3)

    def __rsub__(a, b):
        return Dl._c(b) - a

    def __mul__(a, b):
        b = Dl._c(b); return Dl(a.v * b.v, a.g1 * b.v + a.v * b.g1, a.g3 * b.v + a.v * b.g3)
    __rmul__ = __mul__

    def __truediv__(a, b):
        b = Dl._c(b); iv = b.v.inv()
        q = a.v * iv
        return Dl(q, (a.g1 - q * b.g1) * iv, (a.g3 - q * b.g3) * iv)

    def sq(a):
        return Dl(a.v.sq(), 2 * a.v * a.g1, 2 * a.v * a.g3)


S3, S429, S33 = sqrt_const(3), sqrt_const(429), sqrt_const(33)
QM = (-S3 / 24, (6 + S429) / 24)
QP = (S3 / 12, (3 + 2 * S33) / 12)
AP = (I(Fr(1, 2)), I(Fr(3, 2)))
AM = (I(Fr(-1, 2)), I(Fr(3, 2)))


def cs(u):
    d = 1 + u.sq()
    return (1 - u.sq()) / d, (2 * u) / d


def pts(b1, b3, U1, U3, grad=True):
    u1 = Dl(U1, I(1), I(0)) if grad else U1
    u3 = Dl(U3, I(0), I(1)) if grad else U3
    c1, s1 = cs(u1); c3, s3 = cs(u3)
    v1 = (b1[0] + c1, b1[1] + s1)
    v3 = (b3[0] - c3, b3[1] - s3)
    return v1, v3


def quantities(b1, b3, U1, U3, grad=True):
    v1, v3 = pts(b1, b3, U1, U3, grad)
    Dx, Dy = v3[0] - v1[0], v3[1] - v1[1]
    D2 = Dx.sq() + Dy.sq()
    Delta = (v1[1] + v3[1]) / 2 - 1
    R = (1 - D2 / 4) * Dx.sq() - D2 * Delta.sq()
    return R, Dx, Dy, D2, Delta, v1, v3


def g_of(base, U, shift):
    u = Dl(U, I(1), I(0))
    c, s = cs(u)
    if shift: c, s = -c, -s
    vx, vy = base[0] + c, base[1] + s
    return 1 - (vx.sq() + (vy - 1).sq())


def certify_root(base, shift, ustr, label, log):
    u = Fr(ustr); e = Fr(1, 10 ** 9)
    lo, hi = u - e, u + e
    glo = g_of(base, I(lo), shift).v; ghi = g_of(base, I(hi), shift).v
    gd = g_of(base, I(lo, hi), shift).g1
    sign_change = (glo.lo > 0 and ghi.hi < 0) or (glo.hi < 0 and ghi.lo > 0)
    mono = gd.lo > 0 or gd.hi < 0
    log(f'  root {label}: bracket [{float(lo):.12f}, {float(hi):.12f}] g(lo)={glo} g(hi)={ghi} g\'={gd} '
        f'-> strict sign change {sign_change}, one-signed derivative {mono}')
    assert sign_change and mono
    return lo, hi


def far_apex_check(b1, b3, U1, U3):
    R, Dx, Dy, D2, Delta, v1, v3 = quantities(b1, b3, U1, U3, grad=False)
    h = (1 - D2 / 4).sqrt(); d = D2.sqrt()
    Mx, My = (v1[0] + v3[0]) / 2, (v1[1] + v3[1]) / 2
    A2x = Mx - h * (-Dy) / d; A2y = My - h * Dx / d
    return A2x.sq() + (A2y - 1).sq()          # |A2 - ci|^2


def bisect_check(box, test, maxdepth, stats, depth=0):
    ok = test(*box)
    stats['boxes'] += 1
    if ok:
        return True
    if depth >= maxdepth:
        stats['fail'].append(box); return False
    (a1, b1), (a3, b3) = box
    w1 = (b1 - a1) / (stats['w1'] or 1); w3 = (b3 - a3) / (stats['w3'] or 1)
    if w1 >= w3:
        m = (a1 + b1) / 2; kids = [((a1, m), (a3, b3)), ((m, b1), (a3, b3))]
    else:
        m = (a3 + b3) / 2; kids = [((a1, b1), (a3, m)), ((a1, b1), (m, b3))]
    return all([bisect_check(k, test, maxdepth, stats, depth + 1) for k in kids])


def main():
    out = []
    log = lambda s: (out.append(s), print(s, flush=True))
    t0 = time.time()
    log('A5 sliver certificate: exact rational interval arithmetic, outward rounding 2^-%d' % PREC)
    log('Corner roots (g = 1 - |v - ci|^2), brackets from the domain file (A1):')
    r_B1_u1 = certify_root(QM, 0, '0.255989076986739', 'B1 u1* (qm, theta1=28.7175 deg)', log)
    r_B1_u3 = certify_root(AP, 1, '-0.215250437021530', 'B1 u3* (ap, theta3=155.7048 deg)', log)
    r_B2_u1 = certify_root(AM, 0, '0.215250437021530', 'B2 u1* (am, theta1=24.2952 deg)', log)
    r_B2_u3 = certify_root(QP, 1, '-0.245375379412415', 'B2 u3* (qp, theta3=152.4268 deg)', log)

    # Orientation at the corners: (v1 - ci) x (v3 - ci) > 0 on the bracket boxes
    for name, b1, b3, ru1, ru3 in (('B1', QM, AP, r_B1_u1, r_B1_u3), ('B2', AM, QP, r_B2_u1, r_B2_u3)):
        v1, v3 = pts(b1, b3, I(*ru1), I(*ru3), grad=False)
        cross = v1[0] * (v3[1] - 1) - (v1[1] - 1) * v3[0]
        log(f'  {name} corner orientation (v1-ci)x(v3-ci) = {cross} > 0: {cross.lo > 0}')
        assert cross.lo > 0

    pieces = [
        # name, bases, u1 box, u3 box, mode
        ('P1  B1 theta3-sliver: u1 in arc1(qm) (over-covered by [201/1000, u1*+1e-9]), u3 in [u3*-1e-9, -2152/10000]',
         QM, AP, (Fr(201, 1000), r_B1_u1[1]), (r_B1_u3[0], Fr(-2152, 10000)), 'mono'),
        ('P2  B2 theta3-sliver: u1 in arc1(am) (over-covered by [-36/1000, u1*+1e-9]), u3 in [u3*-1e-9, -245/1000]',
         AM, QP, (Fr(-36, 1000), r_B2_u1[1]), (r_B2_u3[0], Fr(-245, 1000)), 'mono'),
        ('P3  B2 theta1-sliver: u1 in [-36/1000, -35/1000], u3 in arc3(qp) (over-covered by [u3*-1e-9, -148/1000])',
         AM, QP, (Fr(-36, 1000), Fr(-35, 1000)), (r_B2_u3[0], Fr(-148, 1000)), 'direct'),
    ]
    allok = True
    for name, b1, b3, U1, U3, mode in pieces:
        log('== ' + name)
        stats = {'boxes': 0, 'fail': [], 'w1': U1[1] - U1[0], 'w3': U3[1] - U3[0]}
        worst = {'dR1': None, 'dR3': None, 'R': None, 'far': None}

        def test(B1, B3):
            R, Dx, Dy, D2, Delta, _, _ = quantities(b1, b3, I(*B1), I(*B3))
            far = far_apex_check(b1, b3, I(*B1), I(*B3))
            ok = Dx.v.hi < 0 and Delta.v.lo > 0 and D2.v.hi < 4 and far.lo > 1
            if mode == 'mono':
                ok = ok and R.g1.hi < 0 and R.g3.lo > 0
            else:
                ok = ok and R.v.lo > 0
            if ok:
                for k, val, pick in (('dR1', R.g1.hi, max), ('dR3', R.g3.lo, min), ('R', R.v.lo, min), ('far', far.lo, min)):
                    worst[k] = val if worst[k] is None else pick(worst[k], val)
            return ok

        ok = bisect_check((U1, U3), test, 40, stats)
        allok &= ok
        log(f'   certified={ok}  boxes={stats["boxes"]}  failures={len(stats["fail"])}')
        if mode == 'mono':
            log(f'   sup dR/du1 <= {float(worst["dR1"]):.6g} < 0 ; inf dR/du3 >= {float(worst["dR3"]):.6g} > 0 on the whole box')
        else:
            log(f'   inf R >= {float(worst["R"]):.6g} > 0 on the whole box')
        log(f'   far apex: inf |A2-ci|^2 >= {float(worst["far"]):.6g} > 1, so |A2-ci| > 1')
        log('   also certified on every sub-box: D_x < 0, Delta > 0, |D|^2 < 4')
    B1 = (Fr(201, 1000), Fr(201, 1000) + (r_B1_u1[1] - Fr(201, 1000)) / 16)
    B3 = (r_B1_u3[0], Fr(-2152, 10000))
    far = far_apex_check(QM, AP, I(*B1), I(*B3))
    log(f'NOTE (disproof of the domain file claim |A_far - ci| > 1.5): on the P1 sub-box u1 in [{float(B1[0]):.6f}, {float(B1[1]):.6f}], '
        f'u3 in [{float(B3[0]):.9f}, {float(B3[1]):.6f}] the enclosure |A2-ci|^2 in {far} has upper end < 9/4: {far.hi < Fr(9, 4)}')
    log(f'ALL PIECES CERTIFIED: {allok}   ({time.time() - t0:.1f} s)')
    open('certificate_output.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    return 0 if allok else 1


if __name__ == '__main__':
    sys.exit(main())
