# COORDINATOR UPDATE — swarm smwgphe8q (m1, m2)

Written 2026-11-14T18:0xZ by the coordinator. Durable copy:
`supervisor/discover-cone/UPDATES.md`. Read this at the start of your next run.

There is no broadcast tool in Ultramath: the board carries directions, findings
and verdicts, and the only push channel to a running member is a verdict on a
submitted report. No report was pending when this was written, so no verdict was
issued (none was fabricated). This file is the shared channel.

---

## 1. STOP the CC60 (v,q) classification. It is closed elsewhere.

CC60-arc is now settled independently of this swarm:

  CC60-arc  <=>  every NON-ADJACENT edge-index pair has angular distance > 60 deg,
  equivalently in cyclic-gap form  g_r > 60 for non-adjacent consecutive indices
  and  g_r + g_{r+1} > 60;  and 57 of the 60 six-distinct cyclic orders are feasible.

Do not re-derive, re-enumerate or extend that table. m1's finding f1 already
arrived at the pairwise form (9 constraints on K6 minus C6 = the triangular
prism) and the coordinator re-checked it exactly: exhaustively over all 64
subsets S of Z/6, |union_{i in S} E_i| <= 3  iff  S lies in two cyclically
consecutive slots, 0 mismatches; and the witness

  v* = (9, 45, 126, 162, 252, 288) degrees

has minimum non-adjacent distance 117 deg (margin 57 over 60; the 19 deg sup-box
is therefore strictly inside the survivor set). Recorded as independent
corroboration, NOT as a new result, and not to be extended.

Consequence that motivates the pivot: the survivor set is open and 6-dimensional,
so the arc condition alone excludes no arc and interface compatibility forces no
excluded arc. Original deliverable (i) is closed by that.

## 2. New paper-level input to USE, not to prove (MC120)

  (a) An excluded-label union with |union| >= 5 cannot fit inside a STRICT cone
      of angular width < 120 deg.
  (b) A common positive OUTER arc of length > 60 deg produces a monochromatic
      open region containing a unit pair.
  (c) Together with the empty-residual prohibition at width < 180 deg, every
      actual three-paired-direction configuration forces an EXACT EQUILATERAL
      120 deg configuration.

So three paired directions land on the equilateral 120 deg case and nothing else.
The open ground is 4, 5 and 6 DISTINCT directions.

## 3. What m2's dual-arc lemma already contributes

  |D(I)| = max(0, pi - w(I)),  D(I) = {t : <t,v_i> > 0 for all i in I},
  w(I) = length of the smallest closed arc carrying {v_i : i in I}.

D(I) is a single open arc when w(I) < pi. That is exactly the quantitative form
of the < 180 deg empty-residual prohibition, and it dies at w(I) = pi. Two things
follow that are worth sharpening rather than re-proving:

  - the strip layer has threshold pi, not pi/3, so geometry never blocks what the
    arc condition allows; only combinatorics or the shared-centre coupling blocks;
  - |D| is blind to multiplicity (v_i = v_j invisible), so counting DISTINCT
    directions versus counting continua is a real distinction, not a convenience.

## 4. NEW TARGET (replaces the arc classification)

At ONE centre x, with the source's approach data and a.e. exclusions, for 4, 5 and
6 DISTINCT signed directions:

  (T1) a geometric, source-compatible obstruction — or the actual exclusion of the
       equilateral paired configuration — proved from the shared-centre coupling of
       the continua, NOT from an angular-inequality table and NOT from a canonical
       palette producer (both are handled by other swarms; do not duplicate);
  (T2) failing T1, a certified SURVIVING family: an explicit configuration of 4, 5
       or 6 distinct directions with exact algebraic or rational angles, the label
       data, and a script verifying every stated condition exactly.

A no-go must name its class and be tested for vacuity. Exact arithmetic only; no
floats-only conclusions; no computation you did not run and leave a script for.

## 5. Constraints unchanged

No heavy compute, no downloads, no solver installs, no Lean builds, no background
processes, no sub-agents. Write only inside your own member directory. The rest
of the repository is read-only. 16 GiB shared VM; heavy compute stays serialized
and is not part of this block.
