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

Reviewed completion 35401, source b84f9a05eebf810a5522bd9c275df0a1e77d3fce.

Repair the exact statements, then deliver two concrete routes within this block.

1. E011 varying radii: for R=2+delta and r,s in [2,R],
max (r^2+s^2-4)/(2rs)=max(1-2/R^2,R/4). The equal-radius formula suffices only
for 0<=delta<=sqrt(5)-1. At delta=2, centers at radii 2 and 4 on one ray have
separation 2 and angle zero. State the allowed range.
E001 boundary counting cannot subtract upper bounds: use disjoint unit balls
to obtain |T| <= (r+D+2)^3-r^3 <=3(D+2)(r+D+2)^2.
E004's universal "every cluster of diameter<=D" fails for ALL D because of the
singleton dodecahedral cell; formulate EXISTENCE of a suitable partition with
bounded diameter and controlled boundary loss. E003's finite-certification
impossibility is too broad: a bounded cell plus a known complete neighborhood
can certify that further bisectors are irrelevant.
E020 averaged pair mass is necessary, not equivalent to the pointwise count.
Your reviewed source contains no implemented three-point SDP; avoid asserting
that a new evaluator already reproduces CDS bounds.

2. Concrete thin-shell lemma: try rho=209/100. Primary source
Musin–Tarasov, The strong thirteen spheres problem, arXiv:1002.1439v3,
Theorem 1 §2 printed p3, preceding Remark defining the constant. Paper:
https://arxiv.org/pdf/1002.1439v3. New source card Literature/TAMMES13.md and
hashed PDF are in supervisor checkpoint. Rounded 57.1367 degrees is NOT an
upper enclosure. Prove a sufficient directed enclosure from the defining
equations, or supply exact bounded interval code for local execution. Combine
with the restricted varying-radius lemma to get <=12 neighbors in [2,2.09].
Disclose the external theorem's computer-assisted enumeration dependency.
Avoid unsupported novelty or simplification claims.

State/prove with Main the shell-allowance analytic theorem: eta>=0,
fhat>=0, f<=eta on [2,rho], f<=0 beyond rho gives
density <= (4*pi/3)(f(0)+12 eta)/fhat(0), with all decay/positivity hypotheses,
normalizations and periodic-to-general bridge. Attribute DLOV14. C is assigned
the actual bounded numerical prototype, comparing eta=0 at the same degree.
Do not treat the reduction alone as evidence of strength.

3. Preserve the distinct GEOMETRIC route: specify one explicit candidate rule
constructing bounded blocks/transfer neighborhoods that handles the isolated
dodecahedral defect. State one checkable target inequality and exhibit a small
obstruction or a successful worked configuration. If you cannot construct such
a rule, report that precisely instead of repeating the accounting lemma.

Artifacts: corrected Experimental claims/LOCAL_CRITERION, a concise shell lemma
with dependencies and interval handoff, one explicit partition candidate file
or counterexample. Heavy/Lean jobs offloaded. Reviewer: X and Astra; Main
integrates. Push a coherent checkpoint and report exact source hash.

