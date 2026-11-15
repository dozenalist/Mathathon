# Referee report — swarm `smwh11dth`, member m5

I produced no Lean artifact. Everything below is a claim I re-derived from the read-only
sources with my own scripts, or a quotation with `file:line`. Nothing was compiled: no `lean`,
no `lake`, no build, no background process; the only executions are `python3` / `rg` / `diff` /
`patch` text processing, each well under a second (`elapsed_ms` 4–220 in the tool report).

## 0. Artifacts refereed (pinned by hash, as delivered at the end of my pass)

| file | sha256 | size |
|---|---|---|
| `.ultramath/smwh11dth/m1/FiveSupport-swap.lean` | `cf08473dba9a2c077cca444d02377221db6c59cb952dffd4b995c80615b36ce1` | 455 lines |
| `.ultramath/smwh11dth/m1/FiveSupport-swap.diff` | `0ef8f217080f2dc34db128d164bce8a37bc16fe07258b533a69374603f30c3e1` | 3 hunks |
| `lean/OAI/Geometry/PlaneColoring/FiveSupport.lean` (base, untouched) | `6d54703f840a1b4d20b81f5f206b18d79a1fbacde9a481990049b3c41b9c4813` | 376 lines |
| `supervisor/…/step-ban/StepBanShort-r2.lean` (settled producer) | `19bffbcd71bed9b8e92daddf705df89963319604e1e20b4332d6b2f0cf717655` | 105 lines |
| `.ultramath/smwgzbcnp/m1/ConsumerFromV2.lean` (previous swarm) | `4e700e4a1954a9e9a9ed4cc775effa0d881975aecb45898386f762001b6c0d15` | 166 lines |

m1 revised `FiveSupport-swap.lean` at 00:00, after my first pass (which had audited the 23:42
version `2503db18…`, 434+21 lines). **Every verdict below is on the `cf0847…` version**, re-run
end to end after the revision. The 23:42 version passed the same checks.

My tooling (all in this directory): `referee.py` (tokenizer / binder extractor), `audit_swap.py`
(structural audit + verdict), `strip.py` (comment stripper), `selftest.py` (7 negative controls),
`make_fixture.py` (referee reconstruction, **not** a deliverable), `finite_m4.py` (independent
`Fin 5` brute force).

## 1. Verdict table

`PASS` = I reproduced the claim myself. `FAIL` = the claim is false as stated. `NOTE` = true but
carries a defect or an unverified residue. `OPEN` = not decidable without the parent's compile.

### 1.1 m1 — the swap artifact

| # | claim | verdict | my evidence |
|---|---|---|---|
| A1 | the only call site in the build tree is `CyclicCore.lean:119` | **PASS** | `rg -n '\bfive_opposite_contacts_false\b' lean/` → 2 hits: `FiveSupport.lean:199` (decl), `CyclicCore.lean:119` (call). Nothing else in `lean/`. |
| A2 | that call passes 9 explicit positional args in telescope order | **PASS** | I re-derived the 14-slot telescope from `FiveSupport.lean:169` (`variable (c) (hc)` → slots 1–2) + `:199-202`; the 9 explicit slots are `c hc hw hx hab hi hi' hj hj'`, which is exactly the call text. No `@`, no `_`, no named args. |
| A3 | `hn`/`hp` cannot be passed positionally by any consumer | **PASS** | they are `have`s at `:203`/`:204`, absent from the 14-slot telescope; `verify` by inspection of the telescope above. |
| A4 | `hn`/`hp` are nevertheless **live** (`tauto` consumes them) | **PASS** | `Mathlib/Tactic/Tauto.lean` at the pin, sha256 `dd80c05f5ef9a7b73918bbbe9d736f1c4eaaea4b047a2f9ace1cf87d42359a5f`: `:157-163` `casesMatcher` matches `_ ∧ _`; `:185` `casesMatching … (recursive := true)`; `:191` `assumption`. `hn : i-1∈… ∧ i+2∈…` (`:177`), and after `rcases hk with rfl\|rfl` (`:211`) the goals are literally `hn.1`/`hn.2`. Same for `hp` at `:215`. |
| A5 | consumer keeps its name and its statement is token-identical | **PASS** | my tokenizer: 99 tokens both sides, 0 differences; 10 binders `(hw {x (hx {a (hab {i (hi (hi' (hj (hj'` identical in flag, name and order; conclusion `False`. |
| A6 | `five_support_step_ban` (v1, manuscript Lemma 6.7) retained verbatim | **PASS** | `:90-114` = 25 non-blank lines, found contiguously and byte-identically in the swap. |
| A7 | the three r2 declarations are inserted token-identically | **PASS** | inserted block `W[219:276]` (57 lines) token-equals r2:38-96 minus r2:70 (`variable …`); each of `five_outsider_unique`, `five_pair_meet`, `five_support_step_ban_v2` has a statement token-equal to r2's. |
| A8 | nothing else in the base file changes | **PASS** | comment-stripped code: 363 non-blank lines + 34 (the block's code lines) = 397 = the swap's count exactly; the only line-level edits are the two rerouted calls plus one comment-only header (20 lines) and blank-line residue. Declaration inventory: 35 base / 38 swap, added = exactly the three v2 names, removed = none, base order preserved. |
| A9 | `FiveSupport-swap.diff` is `patch -p1`-applicable and its result **is** the delivered file | **PASS** | I copied the base to a scratch tree, `patch -p1 < FiveSupport-swap.diff` (clean), then `diff -q` → identical and `sha256sum` → `cf0847…` on both sides. |
| A10 | exactly one `variable (c : ℂ → Fin 5) (hc : Measurable c)` is in force where `_v2` sits | **PASS** | enclosing section `186-314` of the swap contains it once. This is the load-bearing detail: r2's own copy of that line (r2:70) had to be dropped, since a second `variable (c …)` in the same section is `variable 'c' has already been declared`. |
| A11 | `CyclicCore.lean:119` needs no edit | **PASS (argument, not a run)** | name preserved + statement token-identical (A5) ⇒ same telescope ⇒ the unchanged call elaborates. Only the parent's compile converts this to a fact. |
| A12 | no `sorry` / `admit` / `axiom`; scopes balanced | **PASS** | all three counts 0 → 0; 10 `noncomputable section` vs 10 bare `end`; `namespace OAI` :3 / `end OAI` :last. |

### 1.2 m1 — prose defects (artifact unaffected)

| # | claim | verdict | evidence |
|---|---|---|---|
| B1 | "the other 40 declarations of the base file" (`STATEMENT-IDENTITY.md`) | **NOTE — miscount** | the base has **35** declarations (`^(?:@\[…\]\s*)*(lemma\|theorem\|def\|…)`, and m1's own `work/decls-base.txt` has 35 lines, `decls-swap.txt` 38). The load-bearing part — 3 added, 0 removed, order preserved — reproduces. |
| B2 | header line "one 57-line insertion" | **PASS** | the insertion is exactly 57 lines (`W[219:276]`). |
| B3 | "`lean` writes no olean unless `-o` is given" (`work/SwapContract.lean`) | **OPEN** | plausible and consistent with `scripts/build_lean.py:59` always passing `-o`, but I did not run `lean` and will not claim it. Irrelevant to the deliverable. |

### 1.3 m2 — substitution adequacy

| # | claim | verdict | evidence |
|---|---|---|---|
| C1 | v2's conclusion entails the old lemma's conclusion | **PASS, trivially** | both statements are the same 122-token formula (my check: identical modulo the name, 8 binders with identical flags/order). m2's framing ("two different theorems, needs a bridge") is answered by identity: the bridge is `id`. Their normalisation reaches the same verdict. |
| C2 | N1/N2/N6/N7 (`_v2` statement, binder table, actuals at `:220`/`:221`, `CyclicCore:119` slot split) | **PASS** | I reproduce all four independently: the instantiation map `:220 → _v2 c hc hw hx (i:=i) (j:=i+1) hi hi' (Or.inl rfl)` and `:221 → … (i:=j) (j:=j+1) hj hj' …` is forced by `hi' : a∈fiveSupport c hc x (i+1)`, i.e. the callee's `j := i+1`. |
| C3 | N4 — every identifier of the `_v2` block is in scope before base `:199` or in the import closure | **PASS** | I located all 14: `five_support_trace` :86, `palette_neighbor_disjoint` :23 (both before :199); `fiveState_diag` Accumulation:378, `avoiding_trace_palette` BoundaryTrace:53, `palette_sixty_disjoint` PaletteTransport:450, `sixty` PaletteTransport:390, `palette` Palettes:35, `fiveDiag`/`fiveAdj` Exclusion:8/9, `angularMeasure`/`direction` Coloring:17/18, `fiveState` Accumulation:364, `TraceVector` Compactness:251 — all in the 23-module import closure of `FiveSupport.lean` (computed transitively). |
| C4 | N5 — the two label lemmas do not mention `c`/`hc`/`k`, so the section variable adds no binder | **PASS** | comment-stripped identifier scan of both declarations: no bare `c`, `hc` or `k`. |
| C5 | D1 — `hn`/`hp` are not binders | **PASS** | agrees with A3. |
| C6 | D2/D3 — "`hn`/`hp` … later uses: 0 \| DEAD \| the ONLY dead locals" | **FAIL** | refuted by A4. This is a textual-absence fallacy: `tauto` closes the goals at `:211`/`:215` with `hn.1/hn.2`, `hp.1/hp.2` without naming them. `_hst` (`:218`) is the only genuinely dead local. Still asserted in their 00:06 revision (sha256 `2078d6da147269a3ca633c3f3802f1cac5dea9ee25fe511ae6ed58b07a15f0dc`), posted before my f4. |
| C7 | token count 125 for the v1/v2 statements | **NOTE** | a tokenizer-convention difference only (mine 122, m1's 122, m2's 125); all three find the same identical sequence, so the verdict is unaffected. |

### 1.4 m3 — the two `UNRESOLVED` names of the previous audit's check D

| # | claim | verdict | evidence |
|---|---|---|---|
| D1 | `hd` has no occurrence in the consumer, so nothing to bind and no capture | **PASS** | `awk 'NR>=199&&NR<=233' FiveSupport.lean \| grep -c '\bhd\b'` → 0. m3's resolver prints the same (`0 occurrence(s) in 199-233, 0 binder(s)`). |
| D2 | `he` is bound at `:223` and used at `:224, :227, :228, :230, :231`; binding precedes first use | **PASS** | quoted occurrences, and m3's tool prints `223:77 BINDS <- filter_upwards-with` then five `use -> :223` rows. On the swap file the same rows appear at `:302`+, i.e. exactly the `+79` offset (21 header + 58 insertion) — a good consistency check on both sides. |
| D3 | the previous check D's two `UNRESOLVED` rows were artefacts, not defects | **PASS** | its regex `(?:[(\({⟨,])\s*he\s*(?=[\s:,:⟩)])` cannot match `with … ha he` (space, not an opener), then matched the use `⟨he,` at `:227`; and `hd` has no occurrence to match. |

### 1.5 m4 — the "next consumer" and the finite witnesses

| # | claim | verdict | evidence |
|---|---|---|---|
| E1 | the finite facts the machinery rests on | **PASS** | my own `Fin 5` brute force, coded from the Lean statements (not from m4's script): `five_outsider_unique` 625/625; `five_pair_meet` 25×32×32; `FiveComb.opposite_contacts` 25; `FiveComb.two_bans` 25 (with the existential); `five_adj_four` 25; `five_forced_label` 40 hypothesis-satisfying `p`; `five_diag_disjoint ↔ fiveAdj` 25; `five_no_common_adj` 32. |
| E2 | V6 witness `(i,j,s,t)=(0,1,1,0)` | **PASS** | `adj(0,1)`, `s=1∈{0,1}∩{1,2}`, `adj(1,0)`, `four(0,1,1,0)=True` — so `five_two_ban_false` of that shape is refutable, as claimed. |
| E3 | V7 witness `(0,1,0,1)`, V8 witness `(0,0,0,1)` | **PASS** | `adj(0,1) ∧ adj(0,1) ∧ four(0,1,0,1)`; and `four(0,0,0,1)=True` kills the `fiveAdj i j`-dropped form. Both encode fine. |
| E4 | V10 witnesses `(0,0)`, `(0,2)` for dropping `Disjoint` from `opposite_contacts` | **PASS** | `diag 0 = {0,2}`; `(0,0)`: union `{0,2}`, not disjoint, not adjacent; `(0,2)`: `{0,2}∩{1,4} = {4}`, not adjacent. |
| E5 | V12 — no two diagonals cover `Fin 5` | **PASS** | enumerated all 25 pairs: none covers; `fiveDiag` is injective on the 5 labels. |
| E6 | a "next genuinely used consumer of `five_support_step_ban`" exists | **FAIL (premise empty)** | `rg -n '\bfive_support_step_ban\b' lean/` → decl `:90` + the two calls `:220`/`:221`, both inside the lemma being swapped. There is no other consumer to reduce. Posted as finding f3. |

### 1.5b m4's delivered reduction (`FINDING.md` `a2cd6c3d…`, `HdisBranchFree.lean` `c8a2b922…`)

m4 answered the empty-premise problem correctly: it reframes onto the **`hdis` block of the unique
consumer** (`FiveSupport.lean:205-216`) and proposes a branch-free replacement plus one new lemma
`five_lists_disjoint_sixty`. I referee that on its own terms.

| # | claim | verdict | my evidence |
|---|---|---|---|
| E7 | the copy keeps the consumer's statement | **PASS** | `five_opposite_contacts_false_hdis` at `m4:66` vs `FiveSupport:199`: 99 = 99 tokens, identical; 10 binders identical in flag/name/order; conclusion `False`. |
| E8 | the new lemma and the replacement block are as documented, and nothing else in the lemma moves | **PASS** | `five_lists_disjoint_sixty` at `m4:56`; `hdis`'s declared type is token-identical to the base's (`have hdis : Disjoint ( { i - 1 , i + 2 } : Finset ( Fin 5 ) ) { j - 1 , j + 2 }`); everything from `have hji :=` to the end of the lemma is token-identical to the base's; `intro k hk hl` is absent as claimed; raw length 35 lines = base 35. |
| E9 | both `rcases … <;> tauto` sites are gone from the **code** | **PASS** | comment-stripped, `tauto` appears 0 times in `HdisBranchFree.lean` (the two raw hits are the header doc quoting the old block); code `rcases` sites are 4 (`:87`, `:93`, `:94`, `:97`), matching "6 → 4". |
| E10 | the proof's logic is sound | **PASS (source reading)** | `hp2` is `hp : j-1∈L(b−sixty) ∧ j+2∈L(b−sixty)` transported along `a+2*sixty = b−sixty` (from `hab`, by `ring`); `hAi`/`hBj` are the two **subsets** `{i−1,i+2} ⊆ L(a+sixty)`, `{j−1,j+2} ⊆ L(a+2*sixty)` from the conjunctions; `five_lists_disjoint_sixty` gives `Disjoint L(a+sixty) L(a+2*sixty)` from `five_support_no_sixty` at the two angular steps (its `disjoint_iff_ne` + `rintro … rfl` reduces to `(a+sixty)+sixty ∈ …` vs `∉`), and `Disjoint` monotonicity finishes. No element is ever introduced, which is exactly why the two inversions disappear. |
| E11 | the five `Finset` names it needs are present at the **pinned** Mathlib with the binder orders used (m4 §8.1 left this to m6; I checked it) | **PASS** | pin `Mathlib/Data/Finset/Disjoint.lean:59` `disjoint_iff_ne : Disjoint s t ↔ ∀ a ∈ s, ∀ b ∈ t, a ≠ b`; `Insert.lean:441` `insert_subset (ha : a ∈ t) (hs : s ⊆ t) : insert a s ⊆ t`; `Insert.lean:145` `singleton_subset_iff : {a} ⊆ s ↔ a ∈ s`; `Disjoint.lean:73` `disjoint_of_subset_left (h : s ⊆ u) (d : Disjoint u t) : Disjoint s t`; `Disjoint.lean:76` `disjoint_of_subset_right (h : t ⊆ u) (d : Disjoint s u) : Disjoint s t`. Nested exactly as m4 writes them, the two monotonicity steps type-check: inner = `{j−1,j+2}` right-into `L(a+2*sixty)`, outer = `{i−1,i+2}` left-into `L(a+sixty)`. |
| E12 | the 4-way split at `:225-231` is *not* removable, and the tempting finite closer is refuted | **PASS** | their `five_two_ban_false` shape has the satisfying witness `(i,j,s,t)=(0,1,1,0)` (my E2), so no `decide` lemma of that shape yields `False`; the actual contradiction consumes `hbI.1 hbI.2 hbJ.1 hbJ.2`, the negations of `hban`'s own disjuncts. Their recommendation to leave it alone is right. |
| E13 | m1's swap and m4's reduction **compose** | **PASS (static)** | the edits touch disjoint source lines (m1: the header, `:220`/`:221`; m4: `:205-216` plus one lemma inserted before `:199`), and m4's block consumes `hn`, `hp`, `hab` by name — the three names m1's swap preserves. Neither edit changes the other's premises. A composite file is the sum of the two, and `hn`/`hp` become *explicitly* used, which retires the `tauto`-based argument of A4 in favour of a visible one. |

### 1.6 m6 — API risk register (the parts I could check exactly)

| # | claim | verdict | evidence |
|---|---|---|---|
| F1 | `le_or_lt` is gone as a generic name; `Fin.le_or_lt` survives with the `Fin.le_or_gt` alias | **PASS** | word-boundary count in the pin `Mathlib/`: 2 hits, both `Mathlib/Data/Fin/Basic.lean:163` (docstring) and `:165` (`protected alias le_or_gt := Fin.le_or_lt`). |
| F2 | `if_pos` present, stated with `{h : Decidable c}` implicit before `(hc : c)` | **PASS** | pin `.scratch/toolchain/src/lean/Init/Core.lean:1185` `theorem if_pos {c : Prop} {h : Decidable c} (hc : c) {α : Sort u} {t : α} {e : α} : (if c then t else e) = t`; `/opt` (4.33.1) has the same statement at `:1178` — same statement, different line, so a citation pinned to `/opt` line numbers is not transferable. |
| F3 | `Nat.even_zero` gone; `Even.zero` is the `to_additive` image of `IsSquare.one` | **PASS** | `even_zero` count in pin `Mathlib/`: 0. `Mathlib/Algebra/Group/Even.lean:105-106` `@[to_additive (attr := simp)] lemma IsSquare.one …`, corroborated by `:109` `grind_pattern Even.zero => Even (0 : α)`. |
| F4 | none of the three named breakers is touched by the swap | **PASS** | `grep -c` in `FiveSupport-swap.lean` (and in r2): `le_or_lt` 0, `if_pos` 0, `even_zero` 0. |
| F5 | the two Finset lemmas the inserted block actually uses, and their pin locations | **PASS** | pin `Mathlib/Data/Finset/Defs.lean:243` `theorem not_subset : ¬s ⊆ t ↔ ∃ x ∈ s, x ∉ t`; pin `Mathlib/Data/Finset/Disjoint.lean:47` `theorem disjoint_left : Disjoint s t ↔ ∀ ⦃a⦄, a ∈ s → a ∉ t`. Both match r2's citations. |
| F6 | `measurePreserving_add_right` binder order | **PASS, with the caveat that it is a `to_additive` image** | it has **no source declaration** in the pin: the only textual occurrence is a docstring at `Mathlib/MeasureTheory/Group/Prod.lean:467`. Its multiplicative source is `Mathlib/MeasureTheory/Group/Measure.lean:97` `theorem measurePreserving_mul_right (μ : Measure G) [IsMulRightInvariant μ] (g : G)`, so the additive form takes `(μ) (g)` — which matches r2's application `measurePreserving_add_right angularMeasure (sixty : Angles)`. A name-grep cannot confirm such a name; the parent's already-passed r2 run is the empirical confirmation. |

## 2. Statement-identity manifest (independent)

Tokenizer: maximal `[A-Za-z_][A-Za-z0-9_']*`, maximal digits, or one other non-space character.
Whitespace is never a token. For the consumer the sequence is taken from `lemma` to `:= by`.

| pair | tokens | binders (flag, name, in order) | conclusion | classification |
|---|---|---|---|---|
| `FiveSupport.lean:199` → `FiveSupport-swap.lean:278` | 99 = 99, 0 differences | `(hw {x (hx {a (hab {i (hi (hi' (hj (hj'` (10) | `False` | **IDENTICAL** |
| `FiveSupport.lean:90` (v1) → `r2:76` (v2) | 122 = 122, 1 difference (index 1: the name) | `(hw {x (hx {a {i (hi (hj (hij` (8) | same `∀ᵐ` conjunction | **NAME-ONLY** |
| `FiveSupport.lean:199` → `smwgzbcnp/m1/ConsumerFromV2.lean:122` | 99 = 99, 1 difference (the name) | as row 1 | `False` | **NAME-ONLY** |

Row 2 is what makes the swap sound: the `_v2` route's conclusion is not merely implied by v1's,
it **is** the same formula, so no transport lemma is needed anywhere.

## 3. Call-site table of `five_opposite_contacts_false` (complete census)

| # | `file:line` | kind | arguments, in order |
|---|---|---|---|
| 1 | `lean/OAI/Geometry/PlaneColoring/FiveSupport.lean:199` | declaration | 14-slot telescope: `c hc` (section vars, `:169`) `hw {x} hx {a b} hab {i j} hi hi' hj hj'` |
| 2 | `lean/OAI/Geometry/PlaneColoring/CyclicCore.lean:119` | **the only call** | `c hc hw hx (by dsimp [sixty]; ring) hi hi' hj hj'` — 9 explicit actuals filling `c hc hw hx hab hi hi' hj hj'`; `x a b i j` implicit, inferred from `hx` and the four memberships |

No consumer passes `hn`/`hp` — they are `have`s inside the proof. Every other occurrence of the
name in the repository is under `sprint/` (historical trees, line numbers 194–199) or a staged
copy at `supervisor/simplify-lean/integration/FiveSupport.lean:177`; none is in the build glob
`lean/OAI/**/*.lean` (`scripts/build_lean.py:15`). Only `CyclicCore` imports `FiveSupport`
(`rg` + a transitive-import computation: 23 modules in the closure, and `CyclicCore` the only
reverse edge).

## 4. Adjudications (where two members disagree)

1. **`hn`/`hp` dead or live.** m1 says LIVE (`tauto`), m2 says DEAD (0 textual uses). m1 wins;
   see A4/C6. Consequence: the delivered file keeps `:203`/`:204`, which is the correct call.
   The brief's premise ("the dead binders `hn` and `hp`") is false; the brief's *condition* for
   deleting them is satisfied vacuously, but deleting them requires the extra edit
   `rcases … with rfl|rfl <;> tauto` → `rcases …; · exact hn.1; · exact hn.2` at `:211` and
   `:215`, i.e. 4 changed lines that cannot be validated without a compile. Not worth it.
2. **`hd`/`he`.** Both are false alarms of the earlier audit's regex; m3's file-level resolver
   and my region-level census agree to the line (D1–D3).
3. **`assert` of adequacy (m2) vs identity (m1/m5).** m2's decision procedure is sound but its
   question is moot: the two statements are one formula, so the bridge term is `id`.
4. **m4's assignment.** There is no next consumer of `five_support_step_ban` in the live tree
   (E6). Any m4 deliverable must say so explicitly and identify the *reframing* it actually
   answered (`five_two_ban_false` of the tempting shape is refuted, E2 — that is a legitimate
   "missing lemma + counterexample", but it is not a consumer).

## 5. Defects I am reporting

1. **Substantive (m2):** `adequacy.txt` D2/D3 declare `hn`/`hp` dead. False (A4, C6). Their own
   row `M3 (hn used later in the body) rejected as it must be` shows the self-test cannot catch
   this class of error, because the checker's notion of "use" is textual. Their 00:06 revision
   (sha256 `2078d6da…`) still says `<- DEAD` and does not mention `tauto`.
2. **Cosmetic (m1):** "the other 40 declarations" — 35 (their own `decls-base.txt` agrees).
3. **Integration risk (both, and the parent):** `FiveSupport-swap.lean` cannot be `import`ed and
   its derived module name is not a valid Lean identifier (`scripts/build_lean.py:16` builds the
   name by joining path parts: `OAI.Geometry.PlaneColoring.FiveSupport-swap`). The glob at
   `build_lean.py:15` would also try to compile it *beside* the original, giving two modules that
   both declare `OAI.EuclideanFiveColor.five_opposite_contacts_false`. **The right action is the
   one the diff is shaped for:** apply it in place at
   `lean/OAI/Geometry/PlaneColoring/FiveSupport.lean` (`patch -p1` from the repo root) and never
   place the hyphenated copy in `lean/`. Whether `lean -o` rejects the hyphenated module name is
   **OPEN** — assert nothing; the in-place application avoids the question.
4. **Overclaiming risk:** `work/SwapContract.lean`'s claim that `lean` writes no olean without
   `-o` is unverified here (B3); it does not affect the swap.
5. **Packaging note (m4):** `hdis.diff` is a diff between m4's own local files — its header is
   `--- orig-199-233.lean` / `+++ new-body.lean`, so it is **not** `patch -p1`-applicable to the
   repository. The artifact is `HdisBranchFree.lean`; the diff is documentation. Do not point
   `patch` at it.

## 6. The exact remaining obligation

One local run on the parent's machine, and nothing else:

```
cd <repo>
patch -p1 < .ultramath/smwh11dth/m1/FiveSupport-swap.diff      # in place, sha256 of the result: cf0847…
cat >> lean/OAI/Geometry/PlaneColoring/FiveSupport.lean <<'EOF'
namespace OAI
namespace EuclideanFiveColor
#check @five_opposite_contacts_false
#check @five_support_step_ban
#check @five_support_step_ban_v2
#print axioms five_opposite_contacts_false
end EuclideanFiveColor
end OAI
EOF
source scripts/env4341.sh
( cd lean && lean OAI/Geometry/PlaneColoring/FiveSupport.lean )
```

Accept iff: exit 0; the `#check @five_opposite_contacts_false` telescope equals the one in job
220720-0's transcript up to the name (expected 14 slots, the explicit ones `c hc hw hx hab hi
hi' hj hj'`); `#print axioms five_opposite_contacts_false` lists only the standard axioms; and a
subsequent `python3 scripts/build_lean.py` shows `CyclicCore` still `OK` **with no edit to
`CyclicCore.lean`**. Everything I could check without that run is checked above; the compile is
the only thing that converts A11 (and F6, and the `decide` cost of `five_outsider_unique`) from
argument to fact. I did not run it, and no other claim in this report depends on it.

**Optional second run, if the parent also wants m4's branch-free `hdis` (E13).** The two edits
compose, but they are not one file yet: apply m1's diff in place first, then splice m4's
`five_lists_disjoint_sixty` (`m4/HdisBranchFree.lean:56-64`) in before the consumer and replace
the `hdis` block (`:205-216` in base numbering) by m4's `hp2/hAi/hBj/hdis`. Keep `hn`/`hp` (m4's
block uses them by name) and keep the `_v2` reroute. That composite is **uncompiled and
unassembled by me** — the two-part version above is the one I have evidence for. If the parent
prefers to start from m4's file instead, note that it imports `OAI.Geometry.PlaneColoring.FiveSupport`
(`m4/HdisBranchFree.lean:40`) and declares no `five_support_step_ban_v2`, so the rename at
`:88`/`:89` alone would leave `_v2` undefined: that route additionally needs the whole v2 block
inserted, i.e. it is strictly more work than splicing into m1's file.

## 7. Reproduce (≈1 s total, no Lean)

```
cd .ultramath/smwh11dth/m5
python3 audit_swap.py ../m1/FiveSupport-swap.lean     # ~10 structural checks + verdict, exit 0 iff PASS
python3 selftest.py                                   # the same audit on 7 mutants; every line must read 'detected'
python3 referee.py                                    # token/binder identity over the three statement pairs
python3 finite_m4.py                                  # independent Fin 5 brute force
python3 make_fixture.py && python3 audit_swap.py fixture/FiveSupport-expected.lean   # referee's own shape must PASS
```

If m1 revises the artifact after my pass, `python3 audit_swap.py <new file>` re-decides every
structural claim in this report against the new bytes; the hashes in §0 identify what I actually
audited. The only claim that method cannot reach is the compile (§6); nothing else in this report
depends on m1's file staying still.
