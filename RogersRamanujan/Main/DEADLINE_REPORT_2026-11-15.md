# Rogers–Ramanujan deadline closeout — November 15, 2026

This is a post-deadline evidence review. The mathematical goal is **not verified
complete**. The supervision cycle has ended at its configured deadline.

## Watcher and completion evidence

- Assigned team: `o-67dc4eac-a86a-439c-9459-ef86c31aeaa7`.
- Assigned project: `p-9021becf3f0d47a89b3f3c794c1e872b` (RogersRamanujan).
- Coordinator: `chat-c03d79e54b`; supervisor:
  `01a1d855-a3bb-79d1-b1dd-3f665c6e2d48`.
- The saved state says `deadline_reached`. The configured deadline was
  November 15 at noon PST (`2026-11-15T20:00:00Z`). The final state update is
  `2026-11-15T22:00:39.8623598Z` (2:00:39 p.m. PST); these are distinct times.
- The interrupted read was `chat_changes`, with retry attempt 1 and no saved
  HTTP status. The recorded watcher process, PID 13636, is no longer running.
- The latest saved result is `sair-result-bbae30cad385478eb77aabb5fc422bdd.json`,
  completion **35622**. Its team, project, session and supervisor match the
  state, and its completion equals both saved completion counters.
- Completion 35622 is the already-reviewed GitHub synchronization confirmation,
  saved November 13 at 11:46 p.m. PST. It is not additional mathematical work.
- A bounded read of this exact SAIR session succeeded at
  `2026-11-15T22:06:30.7703318Z` (2:06:30 p.m. PST). With `after=35622`, the API
  returned zero records and no next-page cursor. Thus the API was reachable at
  review time, and it exposed no later chat records. This does not claim that
  all possible unreported or off-chat activity has been observed.
- A fresh GitHub fetch found no subsequent RogersRamanujan research changes on
  `main` or `rr127/main`. Relative to publication `5746863`, the research branch
  added only two dated ChatLogs responses. Before this closeout commit, its tip
  was `6c3c337279d0e2342ab499496defb7a60bcaeabb`.

The saved result is research/operational evidence, not authority to restart a
fleet or change projects. No new research prompt was sent and the watcher was
not restarted after the deadline. Its ended state is preserved.

## Verified progress retained

1. **Formalized standard bridges.** The integrated staircase equivalence and
   same-weight D/B shift were verified by `lake build RogersRamanujan` using
   Lean 4.35.0. The stated subtype inverse laws, weight identities, order and
   positivity obligations have permitted printed axioms and no `sorry`
   dependency. These are standard reductions, not a new A/D bijection.
2. **Executable classical baseline.** The Bressoud–Zeilberger implementation
   has successful saved endpoint-bijection checks for every weight 0–50,
   including 1,065 objects at weight 50. The separate signed-state census in
   that file ends at weight 25. Finite validation is not an all-input proof.
3. **Previously reproduced checks.** The latest reviewed regression passed
   13 checks, including both involutions on 3,198 tested states each and two
   negative controls detecting 224/224 corrupted cases each. The independent
   checker passed through weight 20. This closeout rechecked the saved evidence
   and unchanged sources; it did not rerun the full mathematical test suite.
4. **Written mathematical components.** Useful obstruction proofs rule out
   universal preservation of length and largest part. Local phi arguments
   establish admissibility, distinct Case-I deletion slots, nonnegative counts
   and split parts, and signed-weight identities. Partial family formulas and
   explicit counterexamples are retained with their corrected scope.
5. **Evidence corrections.** Unsupported all-input slot claims remain
   `TESTED_FINITE`; the B/D confusion and trace-count error are retracted.
   `(4^3,1^62)` has B endpoint `(25,17,8,8,8,8)`, D image `(30,20,9,7,5,3)`,
   and 1,910 edges / 1,911 states. No asymptotic complexity claim follows from
   the finite measurements.

## Remaining gaps

- A complete proof of phi branch stability and both compositions for the
  implementation, including repeated parts, virtual zeros and vanished ones.
- The full alternating-path endpoint/termination and inverse argument for that
  implementation, with all involution hypotheses discharged.
- A useful uniform family correspondence with an independently described
  inverse; the P2 pattern remains a conjecture.
- The actual Mathathon objective: a convincingly more natural A/D bijection,
  a complete proof and inverse, and an adequate comparison with prior work.
  Literature access/review gaps still limit novelty claims.

These are gaps in this project's reconstruction and intended improvement;
they do not question the established classical Rogers–Ramanujan identity.
There is no verified new full solution in the reviewed artifacts.

## Preserved provenance

The reviewed SAIR research tip is
`d8684a9384edc52e5960733a4f92bf8c207083db`. The consolidated research and summary
were published at `5746863f92b9d7dade5854c311b237ed04020106`; SAIR confirmed
that exact checkout, and its downloaded summary matched Git blob
`dbe2f4e8ececc2a936c55bd7cdda1d2696843973`.

See [the results summary](RESULTS.md), [claim ledger](CLAIMS.md),
[progress history](../PROGRESS.md), and
[Lean build evidence](verification/2026-11-13_2308_PST/lean435-build.txt).
This closeout is not a claim of an official competition submission.
