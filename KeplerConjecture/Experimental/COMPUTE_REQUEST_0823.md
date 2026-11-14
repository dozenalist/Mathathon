# Compute request `K15-COMPUTE-0823` — the thirteen-facet minimum, on Astra

**Status: REQUESTED.** Owner: role E (Experimental). Reviewer: X. Integrator: Main.

## Why

`REVIEW_2026-11-14_0823` §5.2–5.3 leaves exactly one quantitative question open in the
thirteen-face case: the minimum of `vol Ω(w1)` over legal completions whose cell has **thirteen
facets**. This block's local search reaches `6.358455110` (`24` starts, `80 s`, deterministic) and
`6.452822187`, `6.719022368` on two other completions, against a threshold of `5.763417470`. Those
are *upper* bounds on the minimum. The question is whether a longer run finds anything lower, and
whether the configurations found survive exact certification.

## The job

```text
request_id      = K15-COMPUTE-0823
owner           = role E (Experimental), branch kepler15/experimental/run-01
reviewer        = X
claim_id        = K15-E106 (provisional): min vol over 13-facet completions >= 6.0
source_commit   = 74282517011a30821e4712a687b58023fc0b592c
working_dir     = KeplerConjecture/Experimental/scripts
command         = python3 face_count_obstruction.py --push-multi
dependencies    = python3.12, numpy, scipy (ConvexHull); no Lean, no network
resources       = 1 CPU, 1 GiB, 900 s wall cap, no disk beyond the output JSON
expected_output = Experimental/evidence/push_multi_0823.json: every start's seed, kick, final
                  volume, facet count, and the seven free-centre coordinates of the best
success         = the best volume is reproduced to 6 decimal places, all 13 planes support
                  facets in the exact certificate, and the value is > 5.763417470
```

**Second stage (only if the first succeeds).** Rerun the winning configurations through
`cell_certificate.polytope_volume` with the ring faces at `b = 1051462224238/10^12` (rounded down,
so the value is a lower bound) and record the exact rational. This is the only step that produces a
certificate rather than a float.

## What this cannot settle, stated in advance

A multi-start local search produces **upper** bounds on a minimum. A miss is not evidence of a
lower bound, and no result of this job may be quoted as one. What it *can* do is tell the next
block whether the value `6.36` is near a plateau (many starts agree) or whether the search is still
descending (each longer run finds less) — and those two outcomes call for different next steps.

## Constraints honoured

One CPU, one GiB, a hard `900 s` cap, no network, no Lean, and the command is the one in the
repository at the named commit — nothing is generated at run time. If the runner cannot reproduce
`6.358455110` from that commit, the request is **FAILED** and nothing downstream is used.
