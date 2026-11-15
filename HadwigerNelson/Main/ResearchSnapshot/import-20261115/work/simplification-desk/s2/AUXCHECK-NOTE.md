# S2 signature gate: the 4 "changed" defs are aux-name renames only (research desk, 2026-11-15)

The signature dump reported 4 changed declarations, all in RelativeProducts:
Family.avg, Family.l2Linear, Family.toL2 and pairSequence (all under OAI.EuclideanFiveColor.BoundedMeasurable).
Only their def-VALUE hash differs; the type hash, binder flags and universes are identical, and the source text is byte-identical to R1.

Check: `AuxCheck.lean` (sha 7c6a12ad...), compiled with tools/desk_lean.py against s2/build and against the R1 build, exit 0 both times.
Logs: `auxcheck-s2.log`, `auxcheck-r1.log`. For each def it prints the type hash, the raw value hash, the value hash with every
`_proof_N`/`_auxLemma` constant replaced by one placeholder (normalised), and the sorted multiset of the normalised types of those aux constants.

| def | type | raw value | normalised value | aux-type multiset | #aux |
|---|---|---|---|---|---|
| Family.avg | equal | DIFFERS | equal | equal | 10 |
| Family.l2Linear | equal | DIFFERS | equal | equal | 12 |
| Family.toL2 | equal | DIFFERS | equal | equal | 9 |
| pairSequence | equal | DIFFERS | equal | equal | 9 |

Cause, confirmed from the printed aux names. In R1 these defs reference shared auxiliary proofs named `BoundedMeasurable.projectCLM._proof_N`, generated at the now-deleted `projectCLM` and shared by proof deduplication. In S2 the same proofs are generated at `Family.toL2._proof_N`. The definitions are therefore identical up to renaming of auxiliary proof constants, whose statements agree as a multiset. This is not a change of definition, so the S2 signature gate PASSES with 0 substantive changes.
