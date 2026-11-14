# Kepler supervision and response records

## Current cadence: checks every 45 minutes

The latest user instruction, November 14 at approximately 00:53 Pacific,
cancels Sair-Watch after a brief restoration attempt. All four restored monitor
processes were stopped and their exits verified. Do not restart any watcher.
Preserve their stopped state and reports as historical evidence. Queued watcher
notifications are stale triggers, not authority for extra research cycles.

Automation `kepler-hourly-review-and-github-sync` retains its historical ID but
is now named **Kepler review every 45 minutes**, with
`FREQ=MINUTELY;INTERVAL=45;UNTIL=20261115T200000Z`. It reads the four existing
SAIR chats through the API, reviews completed work, runs actionable local jobs,
and gives concise follow-ups to idle chats. Do not interrupt a busy session or
duplicate an assignment. Check `ownership.json`, `supervision-state.json`, and
the saved assignment and timing-update IDs before every send. Historical
`hourly-state.json` is superseded by `supervision-state.json`.

SAIR does the bulk of mathematical research, implementation and independent
auditing. Main owns choices and integration; Astra supervises, reviews evidence,
routes messages, executes Lean/heavy work locally and publishes results. Give
**a full 60 minutes of substantive work per assignment**, as explicitly
requested in the latest user message. Record receipt time and earliest finish,
check actual elapsed work at the scheduled review, and refill any early-ending
idle chat with remaining work and its independent fallback. An
interim push or one quick fix should lead into the next useful subtask, not end
the block. Supply independent fallbacks when a worker is waiting on a dependency.
Allow an early handoff for a genuine blocker, verified completion, user stop or
the deadline. Keep long local checks explicit rather than blocking other review.

### Ultramath verified on November 14

The four new full-hour assignments were sent through the official website with
Ultramath selected. Subsequent actual `model_call` records report
`reasoning_mode=ultramath` for all four owned sessions. This resolves the earlier
runtime-mode uncertainty; see `ASSIGNMENTS_2026-11-14_0112.json` for delivery IDs,
model-call sequences, timestamps and the exact saved prompts.

The documented `chat_say` API has no mode selector, and prior API sends ran in
standard mode despite maximum effort. For future prompts use the website's
Ultramath selector unless the official API subsequently documents an equivalent
field. Verify actual model calls after delivery. Do not infer activation from
maximum effort or a message setting alone. Keep using the official API for
read-only history, ownership and deduplication checks. This change does not
authorize extra chats, swarms or a watcher restart.

The full hour is an assignment requirement, not yet an observed completion.
The 01:38 Pacific review observed early endings in all four earlier assignments;
follow-ups and runtime evidence are in `ASSIGNMENTS_2026-11-14_0138.json`.
The 02:23 review found Main's next completion after 45.573 minutes and delivered
a fresh hour at 10:35:02.848 UTC, earliest finish 11:35:02.848 UTC. The other
three chats continued their current blocks. Both new prompt deliveries and
subsequent actual Ultramath calls are recorded in `ASSIGNMENTS_2026-11-14_0223.json`.
Worker elapsed-time claims must be checked against actual API timestamps and
turn completions. Finishing an initial checklist is not verified completion
of the Kepler project; proceed to substantive fallbacks. Evidence-only messages
do not restart a busy assignment's hour.
Interim pushes must lead to further useful work; do not fill time with sleeping
or artificial loops. The 45-minute cadence remains in force.

Every scheduled checkpoint synchronizes the latest pushed Kepler artifacts into
the review branch, preserves authorship/source hashes, and keeps unreviewed
claims pending. Ask agents to push substantive work still only on SAIR. No force
pushes, unrelated edits or shared-default-branch integration.

Each push includes a short plain-language update in `HourlyUpdates/` (directory
name retained), a refreshed cumulative `PROGRESS_SUMMARY.md`, technical progress
and evidence, and the exact final response in a dated `ChatLogs/` file. Verify
the remote before idle. A no-change check still receives an honest update.
Stop on user request, verified completion or November 15 at noon Pacific
(20:00 UTC); reserve the final quarter for checking, integration and exposition.

The actual assignments and subsequent longer-work instructions are recorded in
`ASSIGNMENTS_2026-11-14_0040.json`. Their historical `Continuous-*` filenames
record what was sent; they do not override this 45-minute policy. The brief
watcher restoration and its retirement are operational history, not a new
mathematical result. Other projects' shared supervision code was not changed.

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

## Historical operational checkpoint, November 13, 2026

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
