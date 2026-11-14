# Scheduled hourly assignment — Kepler problem 15

This is the authorized 00:08 Pacific hourly review, November 14, 2026. Work only
in KeplerConjecture, in your existing owned SAIR session and existing feature
branch. No new chats, historical swarms, delegation beyond the four owned chats,
Watch-Sair, or shared-default-branch pushes. Main is the integration owner;
Astra routes reports between existing workers because Main cannot message them.
Preserve source history and failed candidates. Use a normal feature-branch push.

Budget: at most 35 minutes, with a pushed checkpoint and final report by
01:00 Pacific (09:00 UTC), whichever comes first. If time is short, deliver the
smallest complete artifact with explicit gaps. Do not run Lean or heavy
numerics on the SAIR VM. Provide runnable code, immutable commit, exact command,
dependencies, estimated time/memory, and a bounded local request to Astra.
Small symbolic sanity checks are fine. Every purported bound requires global
sign/certificate evidence; finite grids are TESTED_FINITE. A CE-like reduction
is not progress without concrete dimension-three numerical evaluation.

All four latest branches are synchronized in supervisor branch
kepler15/setup-01a1d8c0, draft PR https://github.com/dozenalist/Mathathon/pull/1.
The new review and exact local evidence are being published there in this hourly
checkpoint, under Main/HOURLY_REVIEW_2026-11-14_0008.md and the review directories
named below. The complete actionable findings are included here so you can
start without waiting for the push. Fetch before integrating; preserve others'
changes. Report exact pushed hash, changed paths, statuses, reviewer, and any
remaining local execution request. Do not claim Ultramath activation from
maximum reasoning: actual runtime mode is still unconfirmed.

Reviewed completion 48443, tip 633da8e9db3987ec8c56a7c1eb628f3d47402bc2;
checker source e681fbfddb8c5962333380c271d5f7a67f44a07b.

Your K21 certificate is REFUTED. Local independent reconstruction using exact
SymPy Laguerre polynomials matches stored p,q and finds ten simple positive
roots of q. q(57955199/21687900) is negative, approximately
-3.876231892749308e-5. Full rational witness and frozen source are in
Computation/Reviews/48443. The JSON itself says ok=true with reason "A2: 10
simple root(s) of the odd part on the half-line".

Spend at most 20 minutes on the prerequisite repair:
- In certify_relaxed, "if verbose: print(...); return rec" makes failure returns
  conditional on verbosity. [2,-1] produces p=t+1/2, q=7/2-t and quiet ok=true,
  loud ok=false, even an impossible beats_kepler=true. Reject in both modes.
- yun_odd_part loses leading sign: -t-1 maps to t+1. Preserve scalar/sign and
  handle constants, zero polynomials, even multiplicities and endpoint roots
  explicitly. State exact algorithm/invariant; fail closed on unsupported cases.
- Add substantive adversarial tests, including verbosity invariance and the
  submitted K21 rational counterexample. Use an independent exact oracle.
- Bound displays must be rounded upward. Our separate rational Machin-series
  check validates your pi bracket, but 0.78010544 truncates your own float.
  Distinguish a valid rational objective from a certified volume-density bound.
- Withdraw PROVED claims from CERTIFIER.md and any ladder output. Retain failed
  JSON as evidence. Do not extend the ladder before independent checking.

Then supply a SMALL real 3D strengthened benchmark, not another abstract
proposal: unit-ball separation 2, conditional shell count <=12 out to rho=2.09,
eta>=0, fhat>=0, f<=eta on [2,rho], f<=0 beyond rho, objective
(4*pi/3)(f(0)+12 eta)/fhat(0). E is checking the shell lemma. Attribute the
DLOV count-strengthening framework. Include a same-degree eta=0 CE control,
degree/grid switches, conditioning/solver status, coefficients, held-out signs,
and gap report. Label the shell assumption conditional and all grid outputs
TESTED_FINITE. A global compact-interval exponential and tail certificate is
a separate obligation; do not pretend polynomial-only sign checking solves it.

Provide exact command and commit for Astra to run <=5 minutes, 1 CPU, <=2 GB,
with small defaults and JSON output. If the checker repair consumes the budget,
push that complete repair plus a precise handoff, not an unimplemented claimed
benchmark. Main integrates; X and Astra independently review. Final report must
identify what was actually run and what awaits local execution.

