# Kepler supervision and response records

Standing user instruction received November 13, 2026: after handling each user
message or monitored research response, report the progress made. Before every
return to idle, save the final response verbatim in `../ChatLogs/` and push the
owned changes to GitHub. Use a separate Windows-safe, date-stamped Markdown
filename including Pacific timezone and supervisor identifier. Preserve old
logs as written and record corrections in later logs. Never include credentials,
raw private inputs, internal reasoning, or unrelated project material.

Stage explicit Kepler paths, inspect the diff, commit, push the authorized
feature branch, and verify its remote commit before reporting success. If a
push is blocked, retain the local work and describe the actual blocker. A
response cannot name the hash of its own containing commit.

The current publication branch is `kepler15/setup-01a1d8c0`, exposed through
[draft PR #1](https://github.com/dozenalist/Mathathon/pull/1). Automatic approval
review rejected a direct update of the shared default branch. Continue with
reviewable feature branches; default-branch integration remains with the human
project lead unless separately authorized.

## Research ownership

All research belongs to SAIR project `KeplerConjecture`, canonical ID
`p-36b7a2950416475fab4b275b5afdfeb2`. Supervisor is
`01a1d8c0-f50f-7352-a61a-3927660a8eea`. At most four research chats may be active
at once, including the coordinator. Reuse the owned sessions:

| Role | Session |
| --- | --- |
| Main | `based-on-the-chats-e0wz` |
| Computation | `using-the-chats-in-mcl6` |
| Experimental | `i-ve-attached-thomas-4iws` |
| Counterexamples | `i-ve-attached-viazovska-f7hh` |

Main collects their results and maintains the claim ledger. Lean and heavy
numerical computations are handed off with exact source revisions and resource
budgets for local execution. No detached swarm or additional session is
authorized beyond this four-chat limit.

## Operational checkpoint, November 13, 2026

Initial bounded assignments were accepted in all four sessions through
`Watch-Sair.ps1`. The current model is `deepseek/deepseek-v4.1-flash` with maximum
reasoning. The documented API does not expose the browser's Ultramath mode
selector. Follow-up messages selected Ultramath through the UI, but the latest
observed running model calls still reported standard mode. Actual Ultramath
runtime activation remains unconfirmed and must not be inferred from a sent
message's settings.

Continuous watchers retain per-session reports, completion cursors and private
run state. Main completion 23906, Computation 44212 and Experimental 32222 were
saved and queued. Counterexamples completion 35865 was also saved and queued
after recovery of its watcher. All four owned watcher processes were confirmed
alive in their host context. The local Codex daemon was started and failed watchers were
recovered. Queueing succeeded with an active-writer resume warning during the
current supervisor turn; automatic resumption after idle remains unverified.
Deduplicate completion IDs against saved follow-up message IDs before sending
another assignment. The configured watcher deadline is November 15, 2026,
20:00 UTC.

The user stopped Computer Use with Escape. Browser actions ended immediately.
No further browser operation is part of this checkpoint.
