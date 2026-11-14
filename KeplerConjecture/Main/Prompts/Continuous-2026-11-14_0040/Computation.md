# Continuous Kepler assignment — November 14, 2026

The user restored Sair-Watch and wants SAIR to do the research. Work autonomously
for 45–60 minutes on concrete artifacts; when one step is blocked, advance the
independent fallback. Push a useful checkpoint before handing off. Main owns
mathematical choices and integration; Astra reviews, routes work and runs heavy
computation/Lean locally. Submit executable offloads with exact commit/command
and a small resource cap, then continue independent work. Do not end with only
a plan or ask for permission for routine research.

Use this existing Kepler session and feature branch only; four chats maximum,
no new swarms. Fetch supervisor commit ec2596dce67a4c6a93157d291c2f8e2e58f5cfc3.
All tracked work stays in KeplerConjecture. Distinguish proof, finite tests and
certificates. Use Ultramath if exposed; report actual mode, never infer it from
max reasoning. Stop by November 15, 20:00 UTC. Keep the last roughly nine hours
for checking and exposition. Report hash, evidence, gaps and next task.

Completion reviewed: 49543; source 8bb50f85.
Your regression suite passes locally; the old K21 certificate stays rejected.
Now implement the missing shell_bench.py from K15-C-REQ-003. Give a runnable
dimension-three comparison of eta>=0 shell allowance against the SAME-DEGREE
eta=0 CE control, using rho=2.09 conditionally. Include row/column scaling,
held-out sign tests, honest solver statuses, coefficients, objective and gap.
Small default run: <=5 minutes, one CPU, <=2 GB; offload execution to Astra.
An unwritten command or another specification does not satisfy this task.

After pushing the runnable benchmark, continue repairing/validating exactcert:
add positive valid examples, endpoint/even-multiplicity cases and an exact
independent oracle. Do not call the existing sampled oracle a proof. If a
verified baseline certificate is available, publish the rational data and
directed upper bound. Coordinate via branch artifacts; Main integrates,
X/Astra review. No expensive VM optimization or Lean.
