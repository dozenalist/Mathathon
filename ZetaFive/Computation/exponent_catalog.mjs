// Exact rational checks for ../EXPONENT_CATALOG.md. No external packages.
// Run from the repository root: node ZetaFive/Computation/exponent_catalog.mjs
// This verifies the limiting formulas and arithmetic, not the p-adic proof
// obligations that justify using those formulas as determinant bounds.
import assert from 'node:assert/strict';

const gcd = (a, b) => {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b) [a, b] = [b, a % b];
  return a;
};
class Q {
  constructor(n, d = 1n) {
    if (n instanceof Q) return n;
    n = BigInt(n); d = BigInt(d);
    assert.notEqual(d, 0n);
    if (d < 0n) { n = -n; d = -d; }
    const g = gcd(n, d);
    this.n = n / g; this.d = d / g;
  }
  add(b) { b = q(b); return q(this.n * b.d + b.n * this.d, this.d * b.d); }
  sub(b) { return this.add(q(b).neg()); }
  mul(b) { b = q(b); return q(this.n * b.n, this.d * b.d); }
  div(b) { b = q(b); return q(this.n * b.d, this.d * b.n); }
  neg() { return q(-this.n, this.d); }
  sq() { return this.mul(this); }
  cmp(b) { b = q(b); const n = this.n * b.d - b.n * this.d; return n < 0n ? -1 : n > 0n ? 1 : 0; }
  floor() { return this.n >= 0n ? this.n / this.d : -((-this.n + this.d - 1n) / this.d); }
  toString() { return this.d === 1n ? `${this.n}` : `${this.n}/${this.d}`; }
  decimal(digits = 9) {
    const scale = 10n ** BigInt(digits), n = this.n < 0n ? -this.n : this.n;
    const rounded = (2n * n * scale + this.d) / (2n * this.d);
    return `${this.n < 0n ? '-' : ''}${rounded / scale}.${String(rounded % scale).padStart(digits, '0')}`;
  }
}
const q = (n, d) => new Q(n, d);
const sum = xs => xs.reduce((a, b) => a.add(b), q(0));
const min = (a, b) => q(a).cmp(b) < 0 ? q(a) : q(b);
const pos = a => q(a).cmp(0) > 0 ? q(a) : q(0);
const eq = (actual, expected, label) => assert.equal(actual.toString(), expected.toString(), label);
const sorted = xs => [...new Map(xs.map(x => [x.toString(), x])).values()].sort((a, b) => a.cmp(b));
const alpha = q(3, 40), lambda = q(37, 40), H = q(23, 20), M = q(200);

function ell(x, z) { return q(x.sub(z).floor() + x.add(z).floor() + 1n); }
function R(k, x) {
  const T = q(H.mul(x).mul(2).floor()), s = H.mul(x).sub(T.div(2));
  const bq = q(x.mul(2).floor()), nplus = x.mul(2).sub(bq).div(2);
  const zbreaks = [q(0), q(1, 2)];
  for (const u of [x, alpha.mul(x)]) {
    const f = u.sub(u.floor());
    for (const z of [f, q(1).sub(f)]) if (z.cmp(0) > 0 && z.cmp(q(1, 2)) < 0) zbreaks.push(z);
  }
  const zs = sorted(zbreaks);
  let gamma = q(0);
  for (let i = 0; i + 1 < zs.length; i++) {
    const z = zs[i].add(zs[i + 1]).div(2), b = ell(alpha.mul(x), z).mul(3);
    gamma = gamma.add(zs[i + 1].sub(zs[i]).mul(T.sub(b)).mul(T.add(b).sub(ell(x, z)).sub(k)));
  }
  gamma = gamma.add(s.mul(T.mul(2).sub(bq).sub(k))).add(pos(s.sub(nplus)));
  const u = lambda.mul(x), m = q(u.mul(2).floor());
  const J = m.mul(u).sub(m.mul(m.add(1)).div(4));
  const normalization = lambda.mul(x).mul(2).mul(x.floor())
    .sub(lambda.mul(x).mul(12).mul(alpha.mul(x).floor())).sub(J.mul(2));
  return gamma.add(normalization).neg();
}

// Fauzan Appendix B.1: these breakpoints contain every change of affine formula.
const innerBreaks = [q(3), q(20)];
for (const c of [q(2), alpha.mul(2), lambda.mul(2), H.mul(2), alpha.mul(4), q(1).sub(alpha).mul(2), q(1).add(alpha).mul(2)]) {
  for (let j = 0n; j <= c.mul(20).floor(); j++) {
    const x = q(j).div(c);
    if (x.cmp(3) > 0 && x.cmp(20) < 0) innerBreaks.push(x);
  }
}
const ib = sorted(innerBreaks);
assert.equal(ib.length - 1, 143);
function innerIntegral(k) {
  let integral = q(0);
  for (let i = 0; i + 1 < ib.length; i++) {
    const l = ib[i], r = ib[i + 1], x = l.mul(2).add(r).div(3), y = l.add(r.mul(2)).div(3);
    const a = R(k, y).sub(R(k, x)).div(y.sub(x)), b = R(k, x).sub(a.mul(x));
    for (const t of [l.mul(3).add(r).div(4), l.add(r).div(2), l.add(r.mul(3)).div(4)]) {
      eq(R(k, t), a.mul(t).add(b), `affine inner formula k=${k}, interval=${i}`);
      eq(R(7, t).sub(R(5, t)), lambda.mul(t).mul(2), 'inner shift');
    }
    integral = integral.add(a.mul(q(1).div(l).sub(q(1).div(r))))
      .add(b.div(2).mul(q(1).div(l.sq()).sub(q(1).div(r.sq()))));
  }
  return integral;
}
const J5 = innerIntegral(5), J7 = innerIntegral(7);
eq(J5, q(322437603634266857629n, 7535670527041937280000n), 'published compact inner integral');
eq(J7.sub(J5), q(629, 1200), 'compact inner difference');

// Outer formulas are piecewise affine. All their breakpoints are included here.
const Hout = q(1).add(alpha.mul(4));
const ob = sorted([q(1, 3), q(1, 2), q(1), lambda.mul(2),
  q(1).sub(alpha).div(2), q(1).add(alpha).div(3), Hout.div(3),
  q(1).sub(alpha), q(1).add(alpha).div(2), Hout.div(2),
  ...[1, 2, 3, 4, 5].map(j => lambda.mul(2).div(j))]);
function integrateOuter(f, lower = q(1, 3), upper = lambda.mul(2)) {
  const breaks = sorted([lower, upper, ...ob.filter(x => x.cmp(lower) > 0 && x.cmp(upper) < 0)]);
  let value = q(0);
  for (let i = 0; i + 1 < breaks.length; i++) {
    const l = breaks[i], r = breaks[i + 1], mid = l.add(r).div(2);
    eq(f(l.mul(3).add(r).div(4)).add(f(l.add(r.mul(3)).div(4))).div(2), f(mid), 'affine outer formula');
    value = value.add(r.sub(l).mul(f(mid)));
  }
  return value;
}
const tlow = y => min(alpha, q(1).sub(y.mul(2))).add(pos(q(1).add(alpha).sub(y.mul(3))));
const thigh = y => min(alpha, q(1).sub(y)).add(pos(q(1).add(alpha).sub(y.mul(2))));
const bulk = k => integrateOuter(y => y.cmp(1) < 0 ? q(k + 2).mul(q(1).sub(y)) : q(0));
const zeros = k => integrateOuter(y => y.cmp(q(1, 2)) < 0
  ? alpha.mul(-12).sub(tlow(y).mul(k === 5 ? 5 : 6))
  : y.cmp(1) < 0 ? thigh(y).mul(-6) : q(0));
const rank = k => integrateOuter(y => pos(Hout.sub(y.mul((k - 1) / 2))));
const rankAt = (k, y) => pos(Hout.sub(y.mul((k - 1) / 2)));
const zeroCountAt = (k, y) => y.cmp(q(1, 2)) < 0
  ? y.sub(k === 7 ? alpha : 0).add(pos(q(1).add(alpha).sub(y.mul(3))))
  : y.sub(alpha).add(k === 5 ? pos(q(1).add(alpha).sub(y.mul(2))) : 0);
const zeroWeight = k => k === 7 ? q(0) : integrateOuter(y => y.cmp(q(1, 2)) < 0
  ? pos(Hout.sub(y.mul(3)).sub(pos(q(1).add(alpha).sub(y.mul(3))))).neg() : q(0));
for (const k of [5, 7]) {
  // The rank/zero-count crossings for k=5 are (1+alpha)/3 and Hout/3;
  // all are in ob. For k=7 the excess is identically zero on this range.
  eq(integrateOuter(y => pos(rankAt(k, y).sub(zeroCountAt(k, y))), q(1, 3), q(1)),
    zeroWeight(k).neg(), 'saving from min(rank, zero count)');
}
const scalarAt = y => lambda.mul(-2).mul(q(1).div(y).floor())
  .add(sum([1, 2, 3, 4, 5].map(j => pos(lambda.mul(2).sub(y.mul(j))))));
const scalarLow = integrateOuter(scalarAt, q(1, 3), q(1));
const scalarHigh = integrateOuter(scalarAt, q(1), lambda.mul(2));
eq(scalarLow, q(-3929, 16000), 'scalar through K');
eq(scalarHigh, q(289, 800), 'scalar above K');
const outer5 = sum([bulk(5), zeros(5), rank(5), zeroWeight(5), scalarLow, scalarHigh]);
const outer7 = sum([bulk(7), zeros(7), rank(7), zeroWeight(7), scalarLow, scalarHigh]);
eq(outer5, q(127751, 96000), 'published outer integral');
eq(outer7, q(27071, 16000), 'adapted outer integral');

// Sum the row weights directly for ordinary classes containing a numerator zero.
const expectedCosts = {5: [0, 1, 2, 4, 6], 7: [0, 3, 6, 9, 12]};
const expectedZeros = {5: [1, 1, 2, 2, 3], 7: [1, 1, 1, 1, 2]};
for (const k of [5, 7]) for (let ell = 2; ell <= 6; ell++) {
  const weights = Array.from({length: ell - 1}, (_, i) => i < ell - 2 ? min(0, q(i + 3).sub(q(ell + k - 1, 2))) : q(0));
  eq(sum(weights).mul(-2), q(expectedCosts[k][ell - 2]), 'removed-class weight cost');
  assert.equal(weights.filter(w => w.n === 0n).length, expectedZeros[k][ell - 2]);
}

const small5 = lambda.mul(6).div(M), small7 = lambda.mul(8).div(M);
// Bounds on the two infinite tails, not an exact integral over [20,M].
const tail5 = q(-2689, 48000).add(lambda.div(M)).sub(q(2863, 240).div(M.sq())).add(q(32).div(M.sq().mul(M)));
const tail7 = tail5.add(lambda.mul(2).mul(q(1, 20).sub(q(1).div(M))));
const A5 = sum([small5, J5, tail5, outer5]), A7 = sum([small7, J7, tail7, outer7]);
const U = q(-2733991, 2000000);
eq(A5, q(127125602969131786927559n, 94195881588024216000000n), 'published A200');
eq(A7.sub(A5), q(751, 768), 'total arithmetic change');
eq(A7.add(U), q(90471073220559134733281n, 94195881588024216000000n), 'final k=7 coefficient');

const rows = [
  ['Small primes', small5, small7], ['Inner 3 to 20', J5, J7],
  ['Inner tail bound 20 to 200', tail5, tail7], ['Outer range', outer5, outer7],
  ['Arithmetic subtotal', A5, A7], ['Real bound', U, U], ['Final coefficient', A5.add(U), A7.add(U)],
  ['Outer bulk poles', bulk(5), bulk(7)], ['Outer numerator zeros', zeros(5), zeros(7)],
  ['Outer polynomial rank', rank(5), rank(7)], ['Outer zero weights', zeroWeight(5), zeroWeight(7)],
  ['Outer scalar through K', scalarLow, scalarLow], ['Outer scalar above K', scalarHigh, scalarHigh],
];
console.log(JSON.stringify({
  status: 'All exact rational checks passed', innerIntervals: ib.length - 1,
  scope: 'Checks formulas, integrals, and totals; does not certify the adapted determinant valuation estimates.',
  rows: rows.map(([name, a, b]) => ({name,
    k5: {exact: a.toString(), decimal: a.decimal()},
    k7: {exact: b.toString(), decimal: b.decimal()},
    change: {exact: b.sub(a).toString(), decimal: b.sub(a).decimal()},
  })),
}, null, 2));
