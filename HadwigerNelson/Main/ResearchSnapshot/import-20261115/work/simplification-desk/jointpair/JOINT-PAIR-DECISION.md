# Joint-pair support replacement (backlog item 3): superseded by R1, not integrated

Simplification desk, 2026-11-15 ~00:30Z.

## What was asked

Integrate `five_support_no_sixty_joint_pair` (`outputs/joint-support/JointPairSupport.lean`, LEAN_VERIFIED
standalone) as the replacement proof of `five_support_no_sixty`, delete the old proof, and keep Lemma 6.7.

## Why it no longer shortens anything

The joint-pair theorem was written against the encoding-r4 baseline. There, `five_support_no_sixty`
called `strict_state_no_unit_support` (States.lean:704). That made it the last FiveSupport consumer
of the strict-state branch.

R1 removed the strict-state branch. In the R1 tree, `FiveSupport.lean:116-123` proves
`five_support_no_sixty` in 8 lines as a direct call to
`fixed_state_no_unit_three_centres` (AvoidingTrace.lean:148).

| Route for `five_support_no_sixty` (same statement) | Lines |
|---|---|
| R1 (current): `five_support_next` + `five_adj_four` + `fixed_state_no_unit_three_centres` | 8 |
| Joint pair: `stateSupport_no_shift_of_contact_ban` (22) + `five_support_no_sixty_joint_pair` body (19) | 41 |

Swapping in the joint-pair route would add about 33 lines. It also enables no deletion:
`fixed_state_no_unit_three_centres` is still used by `Interfaces.lean:278`
(`interfaceStateSupport_no_unit`), and `triangle_no_unit_of_avoiding_traces` is still used by the
moving-centre theorem that `FourContinuity.lean:412` consumes. The three-centre machinery therefore
stays in the closure whichever route `five_support_no_sixty` takes.

## Decision

Do not integrate. No compile was spent on this; it is pure source and line arithmetic, verified by
reading the R1 sources at the cited lines. The joint-pair theorem stays a standalone LEAN_VERIFIED
alternative proof. It is useful as an independent route to the same statement (proof diversity for
the exposition), but it is not a simplification of the R1 tree.

The generic lemma `stateSupport_no_shift_of_contact_ban` would only pay off if a future change removed
the Interfaces consumer of `fixed_state_no_unit_three_centres`. No such change exists today.
