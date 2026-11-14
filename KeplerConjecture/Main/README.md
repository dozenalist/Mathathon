# Main/ — index and current status

One page so that Astra, X and the next block can find things without reading the
whole ledger. Last updated at the end of block `K15-REVIEW-0308-M-CONTINUE`.
The block deliverable is `CONTINUATION_0308.md`; read that first.

| File | What it is | Status |
| --- | --- | --- |
| `ROADMAP.md` (project root, imported from setup) | the frozen research plan | carried |
| `CLAIMS.md` | the claim ledger: K15-C001…C067 plus K15-R001…R005 (recovered material) | current; three defects found and repaired this block (C029 withdrawn, C049 superseded, C058 repaired), plus C014 from the previous block |
| `REVIEW_0138.md` | **read this first**: the withdrawal of C029, its rejected text, the corrected estimate, and the second finding (sign predicates) | current |
| `RESULTS.md` | the short account: only `VERIFIED_CROSS`/`PROVED` statements count | current |
| `PROOF_GAPS.md` | G1–G10 with owners and closure conditions | current |
| `NEXT_PACKAGE.md` | the exact analytic inequality the geometric route now reduces to, with constants and a falsification test | current |
| `PARTITION_SPEC.md` | requirements R1–R5 for the cluster partition (G4) | current, R3 corrected |
| `INTERFACE.md` | the three conventions, their dictionaries, the certificate schema, the sign-verdict semantics, and what a transfer certificate would contain | current |
| `DECISIONS.md` | D1–D16: why each route was continued, revised or stopped | current |
| `INTEGRATION_0008.md` | what was integrated from which branch, with hashes (block 00:08) | current |
| `AUDIT_REQUEST_X.md` | exactly what X should audit now, and what is not at issue | current |
| `REVIEW_0223.md`, `REVIEW_0308.md` | the last two blocks' accounts (checker repairs; the `Φ` withdrawal) | current |
| `REMAINING_LEMMA.md` | the cut condition vs Hales' accounting and the literature | current |
| `PACKAGE_CUT.md`, `ROUTING_0308.md` | the next package (`sup_Λ t* ≤ Φ₀`) and the four-session routing | current |
| `TASKS.md` | task board and handoff questions Q1–Q12 | current |
| `LOCAL_COMPUTE_REQUESTS.md` | the local queue with per-role IDs (`M-LEAN-001/002`, `C-CERT-001`, `E-CERT-001`, `X-R01`, …) | current |
| `SOURCE_MANIFEST.md` | every branch revision and artifact hash read, plus the commands run | current |
| `Evidence/` | verbatim copies of the recovered swarm artifacts, with hashes | current |
| `CONTINUATION_0308.md` | **the block deliverable**: tasks 1–4, the corrections table, and the next package PN-1…PN-5 | current |
| `BARLOW_CELLS.md` | `K15-C094`: every Voronoi cell of every Barlow packing has volume `√32` — proof, the two-shape dichotomy, and the tightness corollary | current |
| `PROOF_STATUS.md` | **one page**: what is standing, what is conditional, what is not a bound, and the single most useful sentence | current |
| `REVIEW_0523.md` | **this block's deliverable**: D8 verified repaired on C's source, the six review items repaired, the certified all-twists theorem, and the proof-status account | current |
| `REVIEW_0438.md` | **this block's deliverable**: the `C094` repair, the reconciliation of C/E/X and the local evidence, the pair-route bridge, and the next package | current |
| `GEOMETRIC_LEMMA_0438.md` | `C106`–`C108`: the pair bound, the global bridge, the monotone `8π/(3K)` payoff, the `1.92%` gap, and Theorem D (`σ₀ > 2V_dod`) | current |
| `COMPLEXITY.md` | `K15-C100`: the cost/gap scorecard — why no route here is a shortcut, and the one well-posed improvement target (`K15-C096`'s `(S)`) | current |
| `GAP_FIXTURE.md` | `K15-C095`: the crack packing — infinite closed components, a second equality case of Kepler's bound, `b = −1.328495` at the crack faces | current |
| `PROGRESS.md` (project root, imported) | dated history; this block is K15-MAIN-008/009 | current |

## The state of the three routes, in one line each

1. **Analytic (certificate) route** — a working exact pipeline; the K33b
   certificate is verified by two independent implementations at
   `Δ ≤ 0.779966216777`, which is *not* an improvement. Nothing to promote.
   The periodic-to-general bridge is exact for its purpose (`BRIDGE_AUDIT.md` §6).
2. **Geometric (local) route** — reduces to the cut condition, which **implies Kepler**
   and is at least as strong as it (`C087`), so it is a reorganisation, not a shortcut.
   `b ≡ 0` on every Barlow packing (`C094`), so there is **no slack** at the extremal
   configurations. Step 0 is the bounded-closed-component question, now reduced for
   singleton components to `V(2.09) ≥ √32` (`C096`, `PN-1`).
3. **Shell/higher-point route** — no gain in the tested scope; not closed.

## What would make the next block successful

Either (a) a cluster-average improvement over Rogers with an explicit `V_0 > 5.55`,
or (b) a periodic witness violating the cut condition at bounded `Φ`, or (c) an
independent audit that finds another defect of the `C049` kind — the third is not
a failure, it is the cheapest way to protect the other two.
