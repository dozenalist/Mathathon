# The two-point bound for arbitrary packings in R^3: a complete proof, the exact hypotheses, and the correct truncated/hybrid form

Member m2, swarm smwg019eu. Direction d5.

**What this document is.** The literature (Cohn–Elkies, Annals 157 (2003), Theorem 3.1) states the
two-point bound for all packings and proves it for *periodic* packings, with the step
"periodic packings come arbitrarily close to the greatest packing density" relegated to an appendix.
Every downstream use (three-point bounds, Viazovska's papers, the Cohn–de Laat–Salmon computations)
inherits that step. Here it is proved in full (Lemma 1.2), together with

* a correction of a claim in the problem statement: the "for k > 1 the phases do not cancel"
  obstruction is a non-issue (Remark 1.6) — the Poisson sum produces `|sum_j e^{2 pi i <v_j,t>}|^2 >= 0`,
  so periodic packings with any number of translates are covered;
* the truncated/hybrid theorem with an exact, *provable* price (Theorem 2.1), and the observation
  that the price is a **local count**, never an integral (Section 3);
* a proof that a relaxation of the sign condition on a set of measure zero buys exactly nothing
  (Corollary 2.3), so "allow f > 0 only on the contact sphere" is vacuous;
* an analysis of the truncation identity proposed in the problem statement: it is *equivalent* to a
  global equidistribution inequality for the tail (3.2), it is **not** a consequence of local
  regularity (the local route loses a factor 1/(c vol B_1) = 1.35..., Section 3.3), and any
  refutation of it must beat the two-point LP optimum by at least 5.30% (Proposition 3.3);
* the benchmark table with every constant re-derived from its defining local quantity and checked by
  interval arithmetic in `verify.py` (Section 4).

No new numerical bound is claimed. Everything below is either proved, or flagged in the gap list
(Section 5) as quoted from the literature.

---

## 0. Conventions, normalisation, and the exact hypothesis class

**0.1 (Packing).** `Lambda ⊂ R^3` with `|x-y| >= 2` for distinct `x,y`. Balls have radius 1, so the
balls `B(lambda,1)` are pairwise disjoint (Lebesgue-a.e.; they may touch).

**0.2 (Densities).** For `R > 0` put
`Phi(R) = vol( B(0,R) ∩ Union_{lambda in Lambda} B(lambda,1) ) / vol B(0,R)` and

    delta(Lambda) = limsup_{R -> infinity} Phi(R),          c(Lambda) = delta(Lambda) / vol(B_1),

with `vol(B_1) = 4 pi/3`. So `c = 3 delta/(4 pi)` and `delta = (4 pi/3) c`. Every inequality in this
document is stated for `c` unless it explicitly carries the factor `4 pi/3`; there is no other
convention anywhere below. (The literature sometimes calls `c` "the centre density" and `delta` "the
density"; Cohn–Elkies' `delta_CE` is our `c`. See 1.5.)

**0.3 (Fourier transform).** `fhat(t) = int_{R^3} f(x) e^{-2 pi i <t,x>} dx`. No `2 pi` is moved
anywhere else: the Gaussian `e^{-pi |x|^2}` is its own transform under this convention.

**0.4 (Admissibility; the exact hypothesis class of the cited theorem).** Following Cohn–Elkies
(Definition 2.2 there, with `n = 3`): `f : R^3 -> R` is *admissible* if there are `C > 0`, `eta > 0`
with

    |f(x)| <= C (1+|x|)^{-3-eta}   and   |fhat(x)| <= C (1+|x|)^{-3-eta}   for all x in R^3.

Admissibility implies `f` and `fhat` are continuous and that Poisson summation holds in the form

    sum_{x in L} f(x + v) = (1/|L|) sum_{t in L*} fhat(t) e^{-2 pi i <v,t>}                (PS)

for every lattice `L` with dual `L*` and every `v in R^3`, both sides converging absolutely
[CE, Section 2; classical: Stein–Weiss, Chapter VII, Cor. 2.6 for `Z^n`, general `L` by linear change
of variables]. Note `f(0) = int fhat` and `fhat(0) = int f` under admissibility (Fourier inversion at
a point of continuity).

**0.5 (The normalisation bridge to Cohn–Elkies).** CE Theorem 3.1 is stated for minimal distance 1
(balls of radius 1/2) and concludes `c <= f(0)/(2^n fhat(0))`. Substituting `F(x) = f(x/2)` gives
`Fhat(t) = 2^n fhat(2t)`, hence `F(0)/Fhat(0) = f(0)/(2^n fhat(0))`, and `F(x) <= 0` for `|x| >= 2`.
Therefore, in the normalisation 0.1–0.3,

> `c(Lambda) <= f(0)/fhat(0)`  and  `delta(Lambda) <= (4 pi/3) f(0)/fhat(0)`.       (CE-form)

All constants below are in the form (CE-form). Note `fhat(0) = int f > 0` and `f(0) > 0` are part of
the conclusion's meaningfulness; if `fhat(0) <= 0` the bound is void.

---

## 1. Theorem A: the two-point bound for every packing, proved

**Theorem A.** Let `f` be admissible (0.4), not identically zero, with

  (A1) `f(x) <= 0` for all `|x| >= 2`,   (A2) `fhat(t) >= 0` for all `t in R^3`.

Then every packing `Lambda ⊂ R^3` with minimal distance 2 satisfies `c(Lambda) <= f(0)/fhat(0)`, i.e.
`delta(Lambda) <= (4 pi/3) f(0)/fhat(0)`.

The proof is Lemmas 1.1–1.3 and the computation 1.4.

### 1.1 Radialisation is free

**Lemma 1.1.** If `f` satisfies the hypotheses of Theorem A then so does its rotation average
`fbar(x) = int_{SO(3)} f(Ux) dU` (Haar measure, total mass 1), and `fbar(0)/fhatbar(0) = f(0)/fhat(0)`.

*Proof.* `fbar(0) = f(0)`. For `|x| >= 2` and every `U`, `|Ux| = |x| >= 2`, so `f(Ux) <= 0` and hence
`fbar(x) <= 0`: (A1). `fhatbar(t) = int fbar(x) e^{-2 pi i<t,x>}dx = int_{SO(3)} fhat(U^{-1}t)dU >= 0` by
(A2): (A2). Admissibility: `|fbar(x)| <= int |f(Ux)| dU <= C(1+|x|)^{-3-eta}`, and the same for
`fhatbar`. Not identically zero: `fhat(0) = int f > 0` because `fhat >= 0` is continuous and `f` is
not identically 0 (else `fhat = 0`); so `fbar(0) = f(0) = int fhat > 0`. Finally `fhatbar(0) = int fbar
= int f = fhat(0)`. QED

Consequently one may assume `f` radial. (The conclusion of Theorem A and its hypotheses are
rotation-invariant; this is the standard reduction, included because every later statement is radial.)

### 1.2 Every packing is exhausted by periodic packings — proof, not assertion

**Lemma 1.2 (periodic approximation).** Let `Lambda` be a packing with minimal distance 2 and
`delta(Lambda)` as in 0.2. For every `eps > 0` there is a *periodic* packing `Pi` (the union of finitely
many translates of a lattice) with `delta(Pi) >= delta(Lambda) - eps`.

*Proof.* Let `c = c(Lambda) = delta/vol(B_1)`. Choose `S > 0` (a side length, to be optimised at the
end) and `Q = [2, S-2]^3`.

*Step 1 (counting cubes inside the ball).* Fix `S >= 10`. For `R >= 4S` tile R^3 by the cubes
`C_z = z + [0,S)^3`, `z in S Z^3`, and let `C_in(R)` be the set of tiles contained in
`B(0,R)`, `C_bd(R)` those meeting the boundary sphere `S(0,R)`. Since `vol(B(0,R)) =
sum_{C in C_in} vol C + vol(B(0,R) minus the inner tiles)` and the inner tiles fill all but a shell of
width `S sqrt 3`,

    sum_{C in C_in(R)} vol C  >= vol B(0,R) - vol(shell of width S sqrt 3)  >= (4 pi/3) R^3 (1 - O(S/R)).

Write `n(C) = #(Lambda ∩ C)`. All points of `Lambda ∩ B(0,R)` lie in the tiles of `C_in(R) ∪ C_bd(R)`,
and the tiles of `C_bd(R)` are contained in the shell of width `2 S sqrt 3` about `S(0,R)`, which has
volume `O(R^2 S)`; since `Lambda` is 2-separated, at most `O(R^2 S)` points of `Lambda` lie in it
(each of them owns a ball of radius 1, all disjoint, inside a shell of width `2 S sqrt 3 + 2`). Hence

    sum_{C in C_in(R)} n(C)  >=  N(0,R) - O(R^2 S),      N(0,R) := #(Lambda ∩ B(0,R)).

Let `C*` be a tile of `C_in(R)` maximising `n(C)`. Then

    n(C*) >= [N(0,R) - O(R^2 S)] / #C_in(R) >= [N(0,R) - O(R^2 S)] · S^3 / ((4 pi/3) R^3 (1 - O(S/R)))
          = c S^3 (1 + o(1))                                                        (1.2.1)

for fixed `S` and `R -> infinity` along a sequence with `N(0,R)/vol(B(0,R)) -> c`; the `o(1)` is
uniform in `S` (it is `O(S/R) + O(R^2 S/(c (4 pi/3) R^3))`).

*Step 2 (torus periodisation).* Let `C* = z + [0,S]^3` (a closed cube; boundary points are handled by
replacing `[2,S-2]` with `(2,S-2)` below, which changes nothing in measure). Put

    Lambda_S := Lambda ∩ (z + [2, S-2]^3)   ⊂ Λ ∩ C*,

i.e. the points of the tile at `l^infty`-distance `>= 2` from every face. Let `Pi = Lambda_S + S Z^3`.
Then `Pi` is periodic with period lattice `S Z^3`. It is a packing: if `x, y in Lambda_S` and
`0 != l in S Z^3`, then at least one coordinate of `l` is `!= 0`, say `l_1 = k S`, `k != 0`; as
`x_1, y_1 in (2, S-2)` we get `|x_1 - y_1 - kS| >= 4` (for `|k| >= 1`: `|x_1-y_1| <= S-4` gives
`x_1-y_1-kS <= -4` if `k >= 1`, symmetrically for `k <= -1`), so `|x-y-l| >= 4 >= 2`. And distinct
points of `Lambda_S` are already `>= 2` apart. Hence `Pi` is a packing with minimal distance 2.

Its density is exact and equals its centre density times `vol B_1`:

    delta(Pi) = #(Lambda_S) · vol(B_1) / S^3 ,     c(Pi) = #(Lambda_S)/S^3 .           (1.2.2)

*Step 3 (boundary loss).* Points of `Λ ∩ C*` that are *not* kept lie in the union of the six slabs
`{l^infty-dist to boundary < 2}` of `C*`; that union has volume `<= 6·2·S^2 = 12 S^2` and, being
2-separated, contains at most `O(S^2)` points. Therefore by (1.2.1)

    #(Lambda_S) >= c S^3 (1+o(1)) - O(S^2)   as S -> infinity, along the sequence R = R(S) -> infinity.

Then (1.2.2) gives `c(Pi) >= c (1 - O(1/S))`, i.e. `delta(Pi) = vol(B_1) c(Pi) >= delta(Lambda) -
eps` for `S` large. Finally, one period is enough: `Pi` is the union of `#(Lambda_S)` translates of
`S Z^3`, i.e. periodic in the sense of CE. QED

*Remark 1.2bis.* The two losses are `O(S/R)` (tile geometry) and `O(1/S)` (boundary slabs); both go to
zero. Nothing here needs `Lambda` to be saturated, periodic, or to have a limiting density: the
limsup is handled by choosing, for each `S`, a radius `R = R(S)` with
`N(0,R)/vol(B(0,R)) >= c - 1/S` and then `R` so large that the `o(1)` in (1.2.1) is `< 1/S`.

### 1.3 The Poisson computation for a periodic packing

Let `Pi = L + {v_1,...,v_k}` with `L` a lattice, `v_1,...,v_k` representatives that are pairwise
distinct modulo `L` (so `Pi` is a set, not a multiset), minimal distance `>= 2`, and
`c(Pi) = k/|L|` (centre density: `k` centres per fundamental volume `|L| = det L`).

**Lemma 1.3.** With `f` admissible and `S(f) := sum_{1 <= j,l <= k} sum_{x in L} f(x + v_j - v_l)`,

  (i) `S(f) = (1/|L|) sum_{t in L*} fhat(t) |sum_{j=1}^k e^{2 pi i <v_j,t>}|^2`,
  (ii) `S(f) >= (1/|L|) fhat(0) k^2`  if `fhat >= 0`,
  (iii) `S(f) <= k f(0)`              if `{x + v_j - v_l : (x,j,l) != (0,j,j)}` avoids `0` and
                                       `f <= 0` off `B_2` (i.e. on `|z| >= 2`).

*Proof.* (i) is (PS) summed over `j, l` and rearranged:
`sum_j sum_l sum_x f(x + v_j - v_l) = sum_{j,l} (1/|L|) sum_t fhat(t) e^{-2 pi i <(v_j - v_l), t>}`,
and `sum_{j,l} e^{-2 pi i <v_j-v_l,t>} = |sum_j e^{2 pi i <v_j,t>}|^2` (complex conjugate; the exponent
sign is irrelevant for the modulus). (ii): every term of the sum in (i) is `>= 0`, so the sum is at
least its `t = 0` term, which is `fhat(0) k^2/|L|`. (iii): the summand of `S(f)` indexed by
`(x,j,l)` is `f(0)` exactly for `(x,j,l) = (0,j,j)` — there are `k` such summands — and every other
index has `|x + v_j - v_l| >= 2`: if `x != 0` and `j = l` then `x` is a nonzero lattice vector, of
length `>= 2` (minimal distance of `Pi`); if `j != l` then `x + v_j` and `v_l` are two centres of `Pi`
which are distinct by the choice of representatives (were `x + v_j = v_l` then `v_j = v_l mod L`,
contradiction), so their distance is `>= 2`. Those summands are `<= 0`, so `S(f) <= k f(0)`. QED

### 1.4 Conclusion of Theorem A

Combining (ii) and (iii) of Lemma 1.3: `k f(0) >= fhat(0) k^2/|L|`, hence

    c(Pi) = k/|L| <= f(0)/fhat(0).                                                      (1.4.1)

By Lemma 1.2 the set of values `c(Pi)` over periodic packings has supremum `>= c(Lambda)` for every
packing `Lambda`, so (1.4.1) gives `c(Lambda) <= f(0)/fhat(0)`, and multiplying by `4 pi/3` gives
`delta(Lambda) <= (4 pi/3) f(0)/fhat(0)`. QED(Theorem A)

**Corollary 1.5.** In the notation of the problem statement, every admissible `f` with (A1), (A2)
yields `delta <= (4 pi/3) f(0)/fhat(0)` for every packing, and the corresponding two-point constant is
`C_2 := inf { f(0)/fhat(0) : f admissible, (A1), (A2) }` in centre-density units.

### 1.5 Remark: the "k > 1 phases do not cancel" objection is a non-issue

The problem statement warns: "For periodic packings with k > 1 the phases do not cancel". That is
correct for the naive object `sum_x f(x + v)` for a *single* translate `v` — the periodisation of `f`
along `L` is not `<= f(0)` pointwise, and the `t != 0` Fourier coefficients of `sum_x f(x+v)` are
complex and do not have a sign. But Lemma 1.3 shows that the object the argument actually needs is the
sum over *pairs of translates*, `S(f)`, and there the phase factor is
`|sum_j e^{2 pi i <v_j,t>}|^2 >= 0` — a modulus squared, so no cancellation is needed and *every*
`t in L*` term has the correct sign. Hence periodic packings with any `k` are covered, and with
Lemma 1.2 all packings are. (This is also visible in CE's own proof, where the same squared modulus
appears; the point of recording it is that the naive warning can be, and in one member's reading was,
mistaken for an obstruction to the general case.)

### 1.6 Remark: what Theorem A does *not* need

Neither saturation, nor a limiting pair correlation, nor compactness of the space of packings. The only
analytic input is Poisson summation for admissible functions (0.4), and the only geometric input is
that balls of radius 1 around the centres are disjoint. In particular no structure-factor/stacionarity
argument is needed — which is good, because for disordered packings the structure factor vanishes at
zero frequency and the "pair-correlation lower bound" route would fail (see 3.3).

---

## 2. Theorem B: the truncated / hybrid bound, with a proved price

The point of this section: the sign condition (A1) is used exactly once in the proof of Theorem A —
in Lemma 1.3(iii), to bound the off-diagonal summands by 0. If `f` is positive on a set `A`, the
off-diagonal summands that fall in `A` are the only obstruction, and there are at most `n` of them per
centre if `A` has a *local count bound*. The price is therefore a **count**, not an integral. That is
the only version of the truncated bound I can prove; Section 3 shows what is wrong with the integral
version proposed in the problem statement.

**Definition 2.0 (local count bound).** A set `A ⊂ R^3 \ {0}` has *contact number `n`* if for every
2-separated set `X ⊂ R^3` and every `x in X`,

    #{ x' in X : x' != x, x' - x in A }  <=  n.                                        (LC(A,n))

**Theorem B.** Let `f` be admissible with `fhat >= 0`, `f(0) > 0`, let `A ⊂ R^3 \ {0}` satisfy
`(LC(A,n))`, and let `M in R` be such that

   (B1) `f(x) <= M` for `x in A`,   (B2) `f(x) <= 0` for all `|x| >= 2` with `x not in A`.

Then every packing with minimal distance 2 satisfies

    c(Lambda) <= ( f(0) + n·max(M,0) ) / fhat(0),     delta(Lambda) <= (4 pi/3)·(f(0) + n max(M,0))/fhat(0).

*Proof.* By Lemma 1.2 it is enough to treat periodic packings `Pi = L + {v_1,...,v_k}` with minimal
distance `>= 2`. Keep the notation `S(f)` of Lemma 1.3. Part (i) there and `fhat >= 0` give
`S(f) >= k^2 fhat(0)/|L|`; this needs no sign condition. For the upper bound, split

    S(f) = k f(0) + sum_{bad} f(x + v_j - v_l) + sum_{rest} f(x + v_j - v_l),

where `bad` = the indices `(x,j,l) != (0,j,j)` with `x + v_j - v_l in A`, and `rest` = the remaining
off-diagonal indices. Every `rest` index has `|x + v_j - v_l| >= 2` (Lemma 1.3(iii)) and its difference
is not in `A`, so by (B2) its summand is `<= 0`. For the bad indices: fix `j`. The map
`(x,l) |-> (c,c') := (v_l, x+v_j)` is a bijection from pairs `(x in L, l in {1..k})` onto
`{v_1,...,v_k} × (L + v_j) ⊂ Pi × Pi`, and the condition `x+v_j-v_l in A` becomes `c' - c in A`. Hence,
by `(LC(A,n))` applied to the packing `Pi` (a 2-separated set) and summed over the `k` centres
`c in {v_1,...,v_k}` of one fundamental domain,

    #{bad indices with this j} <= n k ,   so   sum_{bad} f <= n k · max(M,0)

(each bad summand is `<= M`, and is `<= 0` when `M < 0`, whence `max(M,0)`). Combining:
`k(f(0) + n max(M,0)) >= S(f) >= k^2 fhat(0)/|L|`, i.e. `c(Pi) = k/|L| <= (f(0)+n max(M,0))/fhat(0)`.
Lemma 1.2 upgrades this to every packing. QED

**Corollary 2.1.** `A = empty`, `n = 0`, is Theorem A. So Theorem B is a strict generalisation.

**Corollary 2.2 (any relaxation on a set of measure zero is vacuous).** If `A` has empty interior
(in particular `A ⊂ {|x| = 2}`, the contact sphere), then (B1)+(B2) force `f <= 0` on all of
`{|x| >= 2}`: `f` is continuous, `{|x| > 2} \ A` is dense in `{|x| > 2}`, and `f <= 0` there. Then
Theorem A applies with the *better* constant `f(0)/fhat(0) <= (f(0) + n max(M,0))/fhat(0)`. So
"allow `f` to be positive on the contact sphere, priced by the kissing number 12" buys **nothing**;
the naive expectation that the contact sphere is a cheap place to relax is wrong. (This kills a route
I had considered before writing it up; it is recorded so that no other member spends time on it.)

**Corollary 2.3 (elementary local counts).** For `A_delta = {2 <= |x| <= 2+delta}`, `delta > 0`, one may
take `n = floor((3+delta)^3) - 1`. Proof: translating a centre to the origin, the `A_delta`-neighbours
are 2-separated points of the shell `{2 <= |y| <= 2+delta}`; their unit balls are pairwise disjoint, are
all disjoint from `B(0,1)` (`|y| >= 2`), and lie in `B(0,3+delta)`; comparing volumes,
`n (4 pi/3) <= (4 pi/3)((3+delta)^3 - 1)`. QED
At `delta -> 0+` this is `26` (for `delta > 0` the same volume bound gives at most 26 only when
`delta <= 3·(27/26... )`, in practice `n = 26` for `0 < delta < 28^{1/3}-3 = 0.0365890`, `27` for
`delta < 29^{1/3}-3 = 0.0723168`, `28` for `delta < 30^{1/3}-3 = 0.1072432`, `n = 31` at `delta = 0.2`;
`verify.py` prints the table). The true value is `12` at `delta = 0` (kissing number,
Schütte–van der Waerden), but Corollary 2.2 shows `delta = 0` is useless; for `delta > 0` no
kissing-type theorem with tolerance is used or claimed here.

**Corollary 2.4 (criterion).** Theorem B improves on a given two-point certificate `f_0` iff
`(f(0) + n max(M,0))/fhat(0) < f_0(0)/fhat_0(0)`. Because `n >= 26` for every shell of positive
thickness by Corollary 2.3, and `M` is bounded below only by `0` (a positive bump can be arbitrarily
small), the criterion is not vacuous, but the winning region is small: the relaxation must buy more
than `n M / fhat(0)` in the ratio. This is the precise sense in which "kissing-type local data" enters
the two-point bound, and it is the honest interface for anyone attempting architecture (B).

---

## 3. The truncation identity of the problem statement: exact form, and why it is not a lemma

The problem statement proposes: if `f` is Schwartz, `fhat >= 0`, `f <= 0` on `2 <= |x| <= R`, and
`I = int_{|x|>R} f`, then in the lattice case `V f(0) >= fhat(0) - I`. This is used to allow a positive
tail. It is a strong statement, and it should not be used, for the reasons below.

### 3.1 It is exactly equivalent to a global equidistribution inequality

Let `L` be a lattice with minimal distance `>= 2`, covolume `V = |L|`, and let `f` be admissible.
Poisson summation (PS) at `v = 0` gives

    sum_{lambda in L} f(lambda) = (1/V) sum_{t in L*} fhat(t)  >=  fhat(0)/V          (3.1.1)

(the first equality is (PS); the inequality drops the `t != 0` terms, which are `>= 0` by the
hypothesis `fhat >= 0`). Splitting off `lambda = 0`:

    V f(0)  >=  fhat(0) - V · sum_{0 != lambda in L} f(lambda).                        (3.1.2)

If `f <= 0` on `2 <= |x| <= R` then all lattice vectors with `0 < |lambda| <= R` contribute `<= 0`
to that sum (they have `|lambda| >= 2`), so

    V f(0)  >=  fhat(0) - V · T,      T := sum_{lambda in L, |lambda| > R} f(lambda).  (3.1.3)

Comparing (3.1.3) with the proposed identity `V f(0) >= fhat(0) - I`:

> **The proposed identity is exactly equivalent to**   `T <= I/V`,   i.e.
> `sum_{lambda in L, |lambda| > R} f(lambda)  <=  (1/V) · int_{|x| > R} f(x) dx.`     (3.2)

It is *sufficient* for (3.2) that `f <= 0` on `{|x| > R}` as well (then `T <= 0` and `I <= 0`, but the
inequality `T <= I/V` need not follow — see 3.3), or that `f` be "equidistributed relative to `L`" in
the mean-field sense. No proof of (3.2) from the stated hypotheses is known to me.

### 3.2 The constant in (3.2) is the *density* `1/V <= 1/(4 sqrt 2) = 0.17678`, not the local constant

Two elementary facts pin down what (3.2) is asking for.

(i) *Local regularity is not enough.* For any 2-separated set `X`, any nonneg `g` and any `R`,
`sum_{lambda in X, |lambda|>R} g(lambda) <= (1/vol B_1) int_{|x|>R} g(x) dx + O(Lip(g))` — put a ball
of radius 1 around each point, on which `g <= g(lambda) + Lip(g)`. The constant obtained is
`1/vol(B_1) = 3/(4 pi) = 0.238732`, which is *larger* than `1/V` (as `V >= 4 sqrt 2 = 5.656854`, Gauss,
FCC extremal) by the factor `V/vol(B_1) >= 1.350`. So no local/Lipschitz argument can give (3.2); it is
a genuine equidistribution statement about the lattice relative to `f`.

(ii) *Positive-definiteness is essential and is not enough to see it.* Dropping `fhat >= 0`, (3.2) is
plainly false: let `L = 2 Z^3` (`V = 8`, minimal distance 2) and let `g = h·1{2 sqrt 2 - w <= |x| <=
2 sqrt 2 + w}` be a spherical shell of height `h` around the shell `|x| = 2 sqrt 2`, on which `L` has 12
points. Then `sum_{|lambda|>R} g(lambda) = 12h` for `R < 2 sqrt 2 - w`, while `(1/V) int g = (1/8) h ·
4 pi (2 sqrt 2)^2 · 2w = 8 pi w h`; the ratio is `12/(8 pi w) -> infinity` as `w -> 0`. So (3.2) cannot
be rescued by any weak local argument: it is about `f`'s Fourier positivity against the lattice, not
about point counts.

### 3.3 What a refutation would have to achieve (quantitative obstruction)

**Proposition 3.3.** Suppose `f` is admissible, `fhat >= 0`, `f(0) > 0`, `f <= 0` on `2 <= |x| <= R`,
and suppose the proposed identity fails for some lattice `L` with `|L| = V`, i.e.
`V f(0) < fhat(0) - I`. Then, with `J := I = int_{|x|>R} f`,

    int_{|x| <= R} f  =  fhat(0) - J  >  V f(0)  >=  4 sqrt 2 · f(0),    hence
    fhat(0)/f(0)  >  4 sqrt 2 · ( 1 + J/(V f(0)) )  >=  4 sqrt 2 = 5.656854.

Since the two-point LP optimum in `R^3` is `f(0)/fhat(0) = 0.186150827...` (i.e.
`fhat(0)/f(0) = 5.3719879...` for the optimal *unrelaxed* certificate, where `f <= 0` on all of
`|x| >= 2`), any refutation must beat the unrelaxed two-point optimum by the factor

    (4 sqrt 2)/(5.3719879...)  =  1.0530281...   (at least 5.30%),

and strictly more if `J > 0`. *Proof.* `int_{|x|<=R} f = fhat(0) - J` (additivity of the integral), the
hypothesis gives `fhat(0) - J > V f(0)`, and `V >= 4 sqrt 2` is Gauss's theorem (FCC extremal among
lattices of minimal distance 2, covolume `4 sqrt 2`). The last display uses that the unrelaxed problem
— "minimise `f(0)/fhat(0)` over admissible `f` with `fhat >= 0` and `f <= 0` on `|x| >= 2`" — has value
`0.186150827...` by the literature (CE 2003, Table 3; quoted, see gap list). QED

So the proposed identity is not refutable by a small perturbation of the LP-optimal function: the
relaxation of the sign condition on `(R, infinity)` would have to buy at least 5.30% in the
`f(0)/fhat(0)` ratio. I do not know whether it is true; it is *open*, it is *not* a consequence of the
stated hypotheses by any argument I can find, and Theorem B is the version that is proved. Any member
who uses `delta <= (4 pi/3) f(0)/(fhat(0) - I)` should record that it is conditional on (3.2).

---

## 4. Benchmark table, with every constant re-derived from its defining local quantity

All rows are in the conventions of Section 0: minimal distance 2, unit balls, `c = delta/vol(B_1)`,
`delta = (4 pi/3) c`. `V_0` denotes a proved lower bound for the volume of a Voronoi cell; the local
rows use `c <= 1/V_0`, `delta <= (4 pi/3)/V_0` (the cell-volume bound is a centre-density bound, so
`c = 1/V_0` exactly, with no `4 pi/3` in it — this is the conversion most often got wrong).

| bound | input | `delta` | `c` |
|---|---|---|---|
| truth (Kepler, Hales 2005) | — | 0.740480489693 = `pi/sqrt 18` | 0.176776695 = `1/(4 sqrt 2)` |
| Hales–McLaughlin 2010 | `V_0 = 5.550291028515...` (regular dodecahedron, inradius 1) | 0.754697399337 = `4 pi/(3 V_0)` | 0.180170732 = `1/V_0` |
| Cohn–de Laat–Salmon 2022 | three-point SDP, truncation 1.886835, `d2=24, d3=9` | 0.770270440 | 0.183888522 |
| Muder 1998 | `V_0 = 5.41848` (cone decomposition) | 0.7730563 | 0.1845536 |
| Cohn–Elkies 2003 (two-point) | optimal admissible `f`, numerical | 0.779746762 | 0.186150827 |
| Rogers 1958 (simplex) | — | 0.779636 | 0.186124 |

The dodecahedral input is an algebraic number: for a regular dodecahedron with edge `a`,
`r_in = (a/2) sqrt((25+11 sqrt 5)/10)` and `V = ((15+7 sqrt 5)/4) a^3`, so with `r_in = 1`,

    V_0 = 2 (15 + 7 sqrt 5) ( 10/(25 + 11 sqrt 5) )^{3/2} = 5.5502910285...

`verify.py` recomputes every entry of the table from its defining quantity with rigorous interval
arithmetic (`mpmath.iv`), and prints PASS/FAIL. It also checks the two identities
`c = 3 delta/(4 pi)` and `delta = (4 pi/3) c` for each row.

---

## 5. What is proved, what is computed, what is quoted: numbered gap list

**Proved here (Sections 1–3).**
1. Lemma 1.1 (radialisation preserves the hypothesis class and the ratio).
2. Lemma 1.2 (every packing is exhausted, in density, by periodic packings of the same minimal
   distance; the torus construction with the explicit `O(S/R) + O(1/S)` losses).
3. Lemma 1.3 and Theorem A: `c <= f(0)/fhat(0)` for every packing, with the exact hypothesis class of
   admissibility (0.4) and no compactness or stationarity argument.
4. Remark 1.5: the `k > 1` "phases do not cancel" obstacle is a modulus squared
   `|sum_j e^{2 pi i <v_j,t>}|^2 >= 0`; there is no obstruction.
5. Theorem B (hybrid/truncated bound) with the price `n·max(M,0)` and its corollaries 2.1–2.4,
   including the vacuity of measure-zero relaxations (2.2) and the elementary counts (2.3).
6. The equivalence (3.2), the local-constant obstruction 3.2(i)(ii), and Proposition 3.3 (any refutation
   of the truncation identity must beat the two-point optimum by `>= 5.30%`).
7. All arithmetic of Section 4 (`verify.py`, and the Lean file `lean/bench.lean` for the conversion
   chain `V_0 -> c -> delta`).

**Quoted (not reproved here; standard or literature).**
8. Poisson summation for admissible functions in the form (PS) [Stein–Weiss Ch. VII Cor. 2.6; CE §2].
   This is the only analytic input of Theorem A. A Lean formalisation of (PS) is far out of reach
   here.
9. Gauss's theorem: a lattice in `R^3` with minimal distance 2 has covolume `>= 4 sqrt 2` (FCC
   extremal). Used only in 3.2(i) and Proposition 3.3.
10. The numerical values `0.186150827` (two-point optimum) and `0.770270440` (three-point), taken from
    the literature / the problem statement. They are *not* independently certified in this document;
    that is a different direction (d1). Proposition 3.3 inherits this dependence explicitly.
11. The kissing number `12` in `R^3` (Schütte–van der Waerden) is mentioned only in Corollary 2.3's
    remark and is not used in any bound.
12. The Hales–McLaughlin value `5.550291028515...` is used only as a benchmark row; the theorem
    "every Voronoi cell has volume `>= 5.550291028515`" is *not* reproved here.

**Open / not claimed.**
13. The truncation identity `V f(0) >= fhat(0) - I` (equivalently (3.2)) is neither proved nor refuted
    here; Proposition 3.3 shows a refutation must be substantial (>= 5.30% beyond the two-point
    optimum). Do not use it as a lemma.
14. No new numerical upper bound on `delta` is claimed in this document. In particular nothing here
    improves `0.754697399337`.

**What would falsify the results here.**
- A counterexample to Theorem A: an admissible `f` with (A1), (A2) and a packing with
  `c > f(0)/fhat(0)`. (Would contradict CE 2003 as well; I would look for an error in Lemma 1.2.)
- A 2-separated set with more than `floor((3+delta)^3) - 1` points in a shell
  `{2 <= |x| <= 2+delta}` around one of its points (would break Corollary 2.3).
- An admissible `f` with `fhat >= 0`, `f(0)/fhat(0) < 0.186150827` (Tier 1; would not contradict
  anything here, but would change the constant quoted in Proposition 3.3).
- An admissible `f` satisfying the truncation hypotheses with `fhat(0) - I > V f(0)` for some lattice
  (would refute 3.2 and require `fhat(0)/f(0) > 5.656854`, i.e. `>= 5.30%` better than the two-point
  optimum).
