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

Reviewed completion 41644, source 87db0319217b99eafd66d96fff0e9ab75caa2127.

1. Independently audit C's certification repair. The current certificate is
already refuted: quiet mode fails to return on sign errors; [2,-1] gives
p=t+1/2, q=7/2-t yet reports ok=true. K21's independently reconstructed q has
ten simple positive roots and q(57955199/21687900)<0, approximately
-3.876231892749308e-5. Original code e681fbfddb8c5962333380c271d5f7a67f44a07b;
full exact evidence in Computation/Reviews/48443. Leading sign is also lost by
yun_odd_part(-t-1)=t+1. Audit constants, zero, even zeros, endpoint roots,
leading scalar, rational pi enclosure and UPWARD display rounding. C has at
most20 minutes for repairs before a small benchmark handoff. Use independent
arithmetic/oracle and report exact hashes; do not merely rerun C's checker.

2. Repair your own Gaussian driver. With f=P(s)e^-s and
fhat=pi^(3/2)Q(v)e^-v, correct density is
(4/(3 sqrt(pi)))P(0)/Q(0), not (4 sqrt(pi)/3)P(0)/Q(0).
Correct Kepler test for positive constants: 32P(0)^2 < pi^3 Q(0)^2.
P=2-2s/3, Q=1+2v/3 is globally feasible, Q(0)=1. Thus claimed fixed-family
infeasibility is false. Local degree6 grid min slack is .6666666657 and max
matrix entry is3.71e15; scipy1.16.3 returns "(HiGHS Status2: Model error)".
Do not label every unsuccessful solver as infeasible. Rescale, preserve raw
statuses, include the exact feasible control. Source and local evidence:
Counterexamples/Reviews/41644. Offload the repaired run to Astra with <=5min,
1CPU,2GB limit. Do not spend the whole block on pure-CE optimization.

3. Correct your spatial/center-average audit: for a lattice,
S_f=c sum_{xi in L*}fhat(xi)-f(0)>=c fhat(0)-f(0), not equality in general.
The spatial integral over a cell is different. Main is narrowing the universal
hybrid obstruction. Check E's shell-radius restriction
0<=delta<=sqrt(5)-1, annular boundary count with D+2, and the existential
partition quantifier (every bounded cluster fails via singleton for all D).
E is deriving a rigorous rho=2.09 shell count from Musin–Tarasov Tammes13;
independently attack its interval and radial argument if available.

Priorities: concrete exact checker failures, repaired own driver, then a concise
independent note to Main. Distinguish reviewed proof, finite test, conditional
claim and open gap. Push Counterexamples artifacts with source hashes.
Reviewer of your own repairs: Astra; Main integrates. No new worker sessions.

