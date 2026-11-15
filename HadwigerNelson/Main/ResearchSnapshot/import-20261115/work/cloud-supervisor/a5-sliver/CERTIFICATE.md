# A5 sliver: interval certificate (research desk, 2026-11-14 ~23:55Z)

**Verdict: PROOF-GRADE for the stated sliver claim, given the dependencies listed below.** The README in this
folder predates the domain file and says "NOT RUN". It is superseded by this file.

- Script: `certify_sliver.py` (sha256 `63e84a36…f351e341`). Output: `certificate_output.txt`
  (sha256 `68507c24…bb41`). Runtime 0.4 s. Exit 0, `ALL PIECES CERTIFIED: True`.
- Domain and target: `work/automation-supervisor/inbox/20261114T224105-download-4-A5-SLIVER-DEFS.md`
  (sha256 `714b2eb2…849f6d`), addendum block 42 (swarm smwgy3s8k m2), sections A1–A5.
- Arithmetic: exact `fractions.Fraction` intervals, rounded outward to multiples of 2^-120. Derivatives use
  forward mode, also as intervals. √3, √429 and √33 are enclosed by integer isqrt at 2^-200. No floating
  point enters any decision. Trigonometry is replaced by the rational parametrisation
  c = (1−u²)/(1+u²), s = 2u/(1+u²), negated for the shift-π arcs.

## What is certified

Notation: ci = (0,1), v1 = base1 + (c(u1), s(u1)), v3 = base3 − (c(u3), s(u3)), D = v3 − v1,
Δ = (v1_y + v3_y)/2 − 1, R = (1 − |D|²/4)·D_x² − |D|²·Δ².

| piece | rational box checked (over-covers the piece) | method | result |
|---|---|---|---|
| P1 (B1, θ3-sliver) | u1 ∈ [201/1000, u1*+1e-9], u3 ∈ [u3*−1e-9, −2152/10000] | monotonicity + exact corner | ∂R/∂u1 ≤ −0.0933 < 0, ∂R/∂u3 ≥ 2.4265 > 0 on the whole box (63 sub-boxes) |
| P2 (B2, θ3-sliver) | u1 ∈ [−36/1000, u1*+1e-9], u3 ∈ [u3*−1e-9, −245/1000] | monotonicity + exact corner | ∂R/∂u1 ≤ −0.5349 < 0, ∂R/∂u3 ≥ 0.00105 > 0 (15 sub-boxes) |
| P3 (B2, θ1-sliver) | u1 ∈ [−36/1000, −35/1000], u3 ∈ [u3*−1e-9, −148/1000] | direct bound | R ≥ 0.2937 > 0 (1 box) |

The following hold on every sub-box of every piece: D_x < 0, Δ > 0, |D|² < 4. Hence the lower apex
A1 = M + h·n, with n = (−D_y, D_x)/|D| and h = √(1−|D|²/4), satisfies

  **m_floor(A1) = A1_y − 1 ≤ 0 ⟺ R ≥ 0.**

The equivalence uses Δ ≥ 0 and D_x < 0. So A1 ∉ H, because H is open and requires m_floor > 0.

**Corner argument (P1, P2).** The corner coordinates u1* and u3* are the roots of g(u) = 1 − |v(u) − ci|²
in the file's ±1e-9 brackets. Each root is certified unique there: g has a strict sign change at the
bracket ends and g′ is one-signed on the bracket (output lines "root …"). At the exact corner,
|v1 − ci| = |v3 − ci| = 1, and (v1−ci)×(v3−ci) ∈ [0.97774, 0.97775] (B1) and [0.95215, 0.95216] (B2) is
positive. So ci is the apex M + h·n. With a = e^{iα}, b = e^{iβ} and 0 < β−α < π, we get h = cos((β−α)/2) and
n = −e^{i(α+β)/2}, so M + h·n − ci = 0. Hence R(u1*, u3*) = 0 exactly.

For a domain point with u1 ≤ u1* and u3 ≥ u3*, both segments below lie in the certified box:

  R(u1,u3) ≥ R(u1*,u3) ≥ R(u1*,u3*) = 0.

Equality holds only at the closed corner. There the apex is ci itself, on ∂H, so it is still outside the
open H.

**Far apex (supplementary).** |A2 − ci|² > 1 on all pieces, with infima 2.1907 (P1), 1.7085 (P2) and
1.3178 (P3).

## Discrepancy found

The domain file (§4, quoting the m2 report) says the far apex has |A_far − ci| > 1.5. **That is false on part
of P1.** On u1 ∈ [0.201000, 0.204437], u3 ∈ [−0.215250438, −0.2152], the rigorous enclosure is
|A2 − ci|² ∈ [2.2004, 2.2339] < 9/4.

The weaker |A2 − ci| > 1 is certified everywhere. If m_hi = 1 − |p − ci|² (the corner values in A2 are
consistent with this, but the file never states the definition), then m_hi(A2) < 0 still holds, and the
conclusion "the far apex is outside H" survives.

## Dependencies (what this certificate does NOT prove)

1. **The decomposition.** It is assumed that the complement of the F5 exclusion boxes inside arc1 × arc3 is
   exactly P1 ∪ P2 ∪ P3, and that the F5 boxes themselves are certified elsewhere (C2:
   1469 + 889 boxes). The desk re-derived the complement from the arc-end table (A1) and the box edges
   (§2). It is P1 ∪ P2 ∪ P3, with margins of at least 2.6e-4 at every non-corner end. The non-corner arc ends
   (B1 u1 low end, B1 u3 high end, B2 u1 low end, B2 u3 high end) are taken from the file and were not
   re-verified, because their defining margins (m_lo, m_lo2) are not defined in the file.
2. **The model.** H is the open region where all five margins are positive. The relevant apex is A1 = M + h·n.
   The target R ≥ 0 is equivalent to the needed statement (A5). Only the m_floor margin is used.
3. No global chromatic result follows from this.

---

# Update 2026-11-15 ~06:45Z: all three caveats CLOSED at the desk

**Verdict: the A5 apex exclusion is PROOF-GRADE over the FULL domain arc1 x arc3 of both blocks, by desk-derived
exact interval certificates.** It no longer depends on the lane's C2 boxes. Remaining assumption: the model,
i.e. the margin definitions quoted below and the reading of the claim.

Margin definitions, quoted by the verifier lane from `block4_check.py:65-75` (smwguidy9 m2):
c1=(sqrt3/2,1/2), c3=(-sqrt3/2,1/2), ci=(0,1); m_lo=|p-c1|^2-1, m_lo2=|p-c3|^2-1, m_hi=1-|p-ci|^2,
m_edge=3/4-p_x^2, m_floor=p_y-1; H = {all five > 0}, which is open.

1. **Arc ends, caveat (b)**: `certify_arc_ends.py` (sha 8ea21bf663493518696487cea22fa433521122e6840a7bf1b330706e0df8a6f5), output `arc_ends_output.txt` (sha 045489e1e380f1618c0a29884b25f0a5e7441c488776d34b0758cf04db04c903).
   All 8 arc ends (4 non-corner, where m_lo=0 or m_lo2=0, and 4 corner, where m_hi=0) are certified unique roots in their +/-1e-9
   brackets: strict sign change, a one-signed derivative, and the margin positive on the arc side.
2. **m_hi, caveat (c)**: m_hi = 1-|p-ci|^2, so m_hi < 0 <=> |p-ci| > 1. The far-apex bound '> 1.5' in the domain file
   is false (§ "Discrepancy" above); '> 1' is what is needed and what is certified.
3. **C2, caveat (a), re-derived**: `certify_full.py` (sha 25ab2cfa85d28bf232b6fc5c92e4242d1b74504af40e5ff09c9760c42b00a429), output `full_output.txt` (sha c076169b95b00432534c462f82ca9e69b07fa2c2157385ed31a905173de34839), 1.1 s.
   Claim (the desk's explicit reading of C2): for EVERY (u1,u3) in arc1 x arc3 (rational boxes reaching 1e-9 past every
   certified end), both unit apexes A1, A2 of (v1, v3) lie outside H.
   Method:
   - Corner boxes B1 [0.245044,0.255989] x [-0.215250,-0.165154] and B2 [0.165154,0.215250] x [-0.245375,-0.226058]
     are certified by monotonicity (dR/du1<0, dR/du3>0, D_x<0, Delta>0, |D|<2) plus the exact corner identity, so R>=0,
     i.e. m_floor(A1)<=0. On those boxes A2 is outside H by m_hi<0.
   - The rest of B1 is 460 boxes and the rest of B2 is 120. On every box some margin of A1 and some margin of A2 is strictly
     negative: A1 by m_floor, m_lo or m_lo2; A2 by m_hi throughout.
   This covers the F5 boxes AND the slivers, so it supersedes both C2 and the sliver-only certificate (which it re-proves).

Supporting script: `certify_sliver.py` (sha 63e84a36bfa95ea99103e314530dbaf38a9fa42667a8ac85b960882ff351e341) supplies the exact interval and derivative machinery.
No global chromatic result follows from A5 alone.
