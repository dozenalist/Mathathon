# Lean 4.35.0 feasibility for the optional submission (backlog item 6)

Simplification desk, 2026-11-15 ~01:05Z. Local inspection only: nothing was downloaded, built or installed.

## What exists locally

| Component | Location | Status |
|---|---|---|
| Lean 4.35.0 toolchain | `C:/Users/jarom/.elan/toolchains/leanprover--lean4---v4.35.0` (3.3 GB) | PRESENT. `lean --version`: `Lean (version 4.35.0, x86_64-w64-windows-gnu, commit eb6cafb7290e8bd5f2937522d8d804f58f02bafc, Release)` |
| Repo root pin | `Mathathon/lean-toolchain` = `leanprover/lean4:v4.35.0`; `lake-manifest.json` mathlib `inputRev v4.35.0`, rev `56a005855ea17e0b0958f73ec801ae140b0a1679` | present |
| Mathlib v4.35.0 SOURCE | `Mathathon/.lake/packages/mathlib` (git HEAD `56a00585…`, 8,624 `Mathlib/**/*.lean`) | PRESENT (source only) |
| Dependency sources | `Mathathon/.lake/packages/{batteries 66e46918, aesop 4a174c49, Qq dce0ad79, proofwidgets df72b022, plausible dfa4f381, LeanSearchClient d6b4c7be, importGraph a41f0e9a, Cli c24fe607}` | PRESENT (source only) |
| Mathlib v4.35.0 BUILD (oleans) | `Mathathon/.lake/packages/mathlib/.lake` | ABSENT (empty directory). No dependency `.lake/build` dirs either |
| Mathlib cache archives (`.ltar`) | `~/.cache/mathlib`, `%LOCALAPPDATA%/mathlib` | ABSENT |
| Workspace toolchains | `work/lean-env/elan/toolchains/` | 4.34.1 only (the pinned proof environment) |

## What a 4.35.0 check would need

Compiling the 83-module OAI closure against Mathlib v4.35.0 needs the Mathlib v4.35.0 oleans. There are two routes:

1. **Cache download (needs Jarom's OK; NOT done).** From `Mathathon/`, run `lake exe cache get`. The source is the Mathlib Azure cache, `https://lakecache.blob.core.windows.net`, per `Cache/Infra.lean:63` in the local checkout (`azureAccountURL`; `MATHLIB_CACHE_GET_URL` overrides it). The exact download size cannot be measured offline. For scale, the local pinned 4.34.1 Mathlib build is 6.5 GB unpacked for 8,529 modules, and v4.35.0 has 8,624. Expect a download of several GB compressed and about 6.5–7 GB unpacked in `.lake/packages/mathlib/.lake/build`. Free disk is about 25 GB, and the supervisor's disk rule applies. Running `lake exe cache get` also first compiles Mathlib's small `cache` executable with the 4.35.0 toolchain, which uses one Lean process.
2. **Local from-source build.** That means all of Mathlib, about 8.6k modules, under the one-Lean-process / 8 GB rule. It takes many hours, so it is infeasible before the 20:00Z submission.

Even with the oleans in place, the 83 OAI modules (about 31k lines) would then each have to be ported and compiled on 4.35.0. That is about 83 sequential compiles at roughly 70–90 s, so 1.5–2 h of exclusive Lean time, plus fixes for any API drift. Deprecated names have already broken jobs on 4.34.1: `le_or_lt`, `if_pos`, `Nat.even_zero`.

## Recommendation

Not feasible without a download. If Jarom wants the optional 4.35.0 submission, the minimal step is route 1, his explicit OK for one `lake exe cache get` in `Mathathon/` (source above, several GB). After that, a smoke test: compile one OAI leaf module, such as `Basic.lean`, on 4.35.0 before committing to the full port. The desk will not start any of this without that OK.
