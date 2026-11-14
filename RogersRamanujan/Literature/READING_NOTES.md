# Reading notes and research handoffs

Prepared 2026-11-13. These are original summaries, not full-paper transcriptions.
Source status refers to what was inspected during preparation; mathematical
claims have not thereby been independently proved or formalized. Bibliographic
details and machine-readable fields are in [sources.json](sources.json).

## GM81a

**A. M. Garsia and S. C. Milne, “Method for constructing bijections for classical
partition identities.”** PNAS 78(4), 2026--2028 (1981).
[Publisher](https://doi.org/10.1073/pnas.78.4.2026);
[PMC record](https://pmc.ncbi.nlm.nih.gov/articles/PMC319275/).

**Read:** abstract and bibliographic record. The scanned full text was not
successfully retrieved; do not label this as a full-text review.

**Takeaway:** The announcement describes a constructive route joining Schur's
map to two further bijections by a principle involving pairs of involutions.
This is one of SAIR's explicit references and establishes the historical
benchmark: an actual correspondence already exists.

**Handoff:** Main should describe exactly which aspect a new construction
improves. Lean may eventually extract a generic finite-involution principle,
but that alone does not resolve naturalness. Use PAK06 §8.4 for an accessible
exposition; use GM81b for the original full construction when available.

## GM81b

**A. M. Garsia and S. C. Milne, “A Rogers--Ramanujan bijection.”** Journal of
Combinatorial Theory, Series A 31(3), 289--339 (1981).
[Publisher/DOI](https://doi.org/10.1016/0097-3165(81)90062-5).

**Read:** publisher abstract, metadata, and reference list; the complete
51-page argument was not retrieved. This is the second official reference.

**Takeaway:** The paper supplies the endpoint bijection through combined
partition transformations and the involution principle. Its abstract also
discusses extensions to related identities. Reimplementing it is established
work, even when the implementation is new.

**Handoff:** Main should obtain and inspect the relevant original sections
before claiming equivalence to, or a correction of, this map. Computation
should start with BZ82's shorter reference algorithm so this access gap does
not stall infrastructure. Do not conflate the two algorithms without proof.

## BZ82

**D. M. Bressoud and D. Zeilberger, “A short Rogers--Ramanujan bijection.”**
Discrete Mathematics 38, 313--315 (1982).
[Author-hosted scan](https://sites.math.rutgers.edu/~zeilberg/mamarimY/rrDG.pdf);
[DOI](https://doi.org/10.1016/0012-365X(82)90298-9).

**Read:** three-page text; first-page scan visually checked. Locators:
p. 313, intermediate family and signed state space; p. 314, two involutions
and stopping argument; p. 315, examples. OCR corrupts several inequalities.

**Takeaway:** This is still an iterated-involution construction. Its notation
`A(n)` means our `D_n`; `C(n)` means our `A_n`; `B(n)` consists of partitions
whose smallest part is at least their length. The first-page shift is the
map `T` in ROADMAP. Intermediate states have signed integer `j` with
`|lambda| + j(5j-1)/2 = n`.

**Handoff:** C implements the involutions and reverse path; X checks each
case against the scan and validates endpoints after the notation bridge.
Finite-state invertibility must justify termination; “iterate until success”
is not a proof. E can seek provable simplifications of repeated path segments.

## BP06

**Cilanne Boulet and Igor Pak, “A combinatorial proof of the Rogers--Ramanujan
and Schur identities.”** JCTA 113, 1019--1030 (2006).
[Author PDF](https://pi.math.cornell.edu/~cilanne/Publications/RogersRamanujan.pdf);
[arXiv](https://arxiv.org/abs/math/0411072);
[DOI](https://doi.org/10.1016/j.jcta.2005.09.007).

**Read:** introduction, §1, and selected constructions/proofs in §2, especially
Lemmas 2.2 and 2.4 and the inverse description; §3 remarks. Author PDF is dated
September 12, 2005.

**Takeaway:** Two symmetries of a generalized Dyson rank are established by
explicit maps on partitions cut by two Durfee rectangles. The global identity
also uses the Jacobi triple product. Their “Rogers--Ramanujan partitions” have
smallest part at least length, so apply `T` before comparing to gap partitions.

**Handoff:** E studies the uniquely determined insertion indices and branch
inversion. L can formalize an individual symmetry after its hypotheses are
fixed. These local bijections are ingredients; the paper does not directly
hand us the requested simple residue-to-gap map. Track the missing endpoint
conversion explicitly.

## PAK06

**Igor Pak, “Partition bijections, a survey.”** Ramanujan Journal 12, 5--75
(2006). [Author PDF](https://www.math.ucla.edu/~pak/papers/psurvey.pdf).

**Read:** selected passages in §§7.1--7.2 and 8.4, and corresponding historical
remarks. The available 69-page preprint is dated September 18, 2002; use its
section numbers rather than journal page numbers.

**Takeaway:** The survey organizes the partition transformations and gives
the general involution principle in §8.4. Exercises 8.4.4--8.4.5 connect it to
Rogers--Ramanujan and ask about worst-case iteration growth. That requested
lower bound must not be treated as a proved complexity theorem.

**Handoff:** Main uses this to build the dependency map; L can extract a
generic endpoint-path lemma. C should distinguish a correspondence from the
particular algorithm computing it. Consult the survey before presenting a
standard staircase, conjugation, or Durfee reduction as new.

## PAK04

**Igor Pak, “The nature of partition bijections II. Asymptotic stability.”**
32-page preprint, listed as 2004 on the author's research page.
[PDF](https://www.math.ucla.edu/~pak/papers/stab5.pdf);
[author listing](https://www.math.ucla.edu/~pak/papers/research.htm).

**Read:** introduction, Theorem 4.1, and references/final discussion. Detailed
geometric definitions and their application to a proposed map remain an audit
task. The PDF date text is ambiguous; use the author's listed year.

**Takeaway:** This develops geometric/AG-bijections and asymptotic stability
under hypotheses. The introduction refers the Rogers--Ramanujan nonexistence
argument to a separate forthcoming paper; reference [18] is marked “in
preparation.” Thus this manuscript is not, by itself, a retrieved complete
proof of that obstruction.

**Handoff:** X should inspect §§2--4 and test the exact hypotheses against
each proposed geometric algorithm. M must distinguish this framework from
the informal word “natural.” Arithmetic, adaptive, or other constructions
cannot be ruled out merely by repeating the title of an obstruction result.

## PAK18

**Igor Pak, “Complexity problems in enumerative combinatorics.”** 2018 survey,
author version dated April 21, 2018.
[PDF](https://www.math.ucla.edu/~pak/papers/ICM-paper9.pdf).

**Read:** §§3.2, 3.4--3.5 (printed pp. 16--18), Theorem 3.1 and references
[137]--[138].

**Takeaway:** The survey separates efficient computation from explanatory
bijections. It discusses ranking-based constructions and states Theorem 3.1,
a no-geometric-bijection result for a particular piecewise-linear framework.
It cites the stability manuscript PAK04, whose own introduction refers to a
separate argument. The precise source chain deserves care.

**Handoff:** X should produce a hypothesis-by-hypothesis obstruction note
before eliminating a route. M must not claim that all natural maps are
impossible. C should report measured runtime separately from proved bounds,
and distinguish bounds in `n` from those in encoded input length. An efficient
rank matching is a control, not an automatic solution to SAIR's objective.

## SOODAK18

**Ellis Soodak, “New perspectives on the first Rogers--Ramanujan identity:
potential steps towards a simple bijective proof.”** University of Chicago
REU paper, July 20, 2018.
[PDF](https://math.uchicago.edu/~may/REU2018/REUPapers/Soodak.pdf).

**Read:** introductory motivation, §3 reformulations, §4 Definitions 4.1,
4.2, 4.4 and Conjecture 4.6 (pp. 5--7). Exploratory student paper.

**Takeaway:** The conjecture compares neighborhoods of the intersection of
the two families. On the gap side, proximity permits transferring up to two
units between parts; on the residue side it permits consolidating ones into
one recipient. The author reports checks through weight 20, not a proof.

**Handoff:** X first transcribes all conventions and reproduces the reported
weight-20 count, then extends independently. Preserve the distinctions between
deleting a depleted part, creating a new part, and retaining unused ones.
Save full witnesses for any discrepancy. A counterexample would reject this
specific refinement, not the possibility of a natural bijection.

## MSZ09

**James McLaughlin, Andrew V. Sills, and Peter Zimmer, “Rogers--Ramanujan
computer searches.”** Journal of Symbolic Computation 44(8), 1068--1078 (2009).
[Author PDF](https://sites.math.rutgers.edu/~asills/compsearch/CompSearchJSCrev.pdf);
[institutional record](https://digitalcommons.wcupa.edu/math_facpub/30/);
[DOI](https://doi.org/10.1016/j.jsc.2009.02.003).

**Read:** introduction and search-method passages in §§3--4. The later arXiv
deposit [1812.08222](https://arxiv.org/abs/1812.08222) does not make this a
2018 journal result.

**Takeaway:** Numerical and symbolic searches find candidate q-series/product
identities; the numerical relation-finding stage needs subsequent proof.
The project is about identities of Rogers--Ramanujan type, not a natural
bijection for SAIR127.

**Handoff:** C/E can borrow the discipline of a bounded, recorded search space
and a separate certification phase. Use exact coefficients when testing our
combinatorial proposals. A newly guessed generating function only helps this
project if it exposes a realizable, invertible transformation or useful lemma.

## HEX26

**Ilmar Gahramanov, “Riordan lattice paths counted by area.”** Hexagon
`2610.00705v1` (2026), CC BY 4.0.
[Versioned record](https://hexagonmath.org/2610.00705v1);
[local TeX](sources/hexagon_2610_00705v1.tex).

**Read:** relevant source passages in §§1--4, especially the first-step
decomposition and equation (4.7). The claims about asymptotics and limit laws
were not independently audited. Full source is retained with attribution.

**Takeaway:** The area generating function satisfies a q-shift functional
equation; the no-horizontal-step specialization yields a Rogers--Ramanujan-type
quotient. This supplies an adjacent path model rather than the target
partition bijection.

**Handoff:** E may investigate a reversible bridge after naming its objects
and weight statistic. C should check that bridge before investing in path
asymptotics. Review and search details are in [HEXAGON_REVIEW](HEXAGON_REVIEW.md).

## Shared cautions and source gaps

- The two official 1981 references have verified metadata and abstract-level
  review here. Access to the complete texts is an explicit follow-up, not an
  implied completed task.
- Source cards summarize selected relevant sections, not full independent
  referee reports. No paper's presence establishes the correctness of all its
  claims.
- The team needs an exact comparison of maps, not just titles containing
  “bijective” or “simple.” Preserve the source's own domain and codomain.
- A preprint's version and retrieval date matter. Do not silently replace
  a cited version after a new result has depended on it.

## Event-cycle update: BZ82 full text retrieved (2026-11-14)

The scan `https://sites.math.rutgers.edu/~zeilberg/mamarimY/rrDG.pdf`
(sha256 `403543088ed9465bc8e3f9918defd22a57c86a21493226c9852729af614483c6`,
3 pages) was downloaded and read **in full**, closing the earlier "first page
only" access gap for this source. Extractable text covers all of pp.313-315;
several inequality signs are corrupted by OCR and were reconstructed from the
paper's own worked examples rather than guessed.

What the full text adds to the preparation cards:

* p.313 fixes the notation bridge exactly: their `A(n)` is our `D_n`, their
  `C(n)` is our `A_n`, their `B(n)` = {smallest part >= length} = `T(D_n)`, and
  the displayed shift `(lambda_i - t + 2i - 1)` is our `T`.
* p.313 defines `X(n) = {(j; lam) : |lam| + j(5j-1)/2 = n}`; the shift is the
  *5-pentagonal* number, not `j(3j-1)/2`.
* p.314 gives `phi` (the Jacobi-triple-product involution, cases I/II with a
  parameter `m`) and `psi` (the residue involution, cases I(a)/I(b)/II(a)/II(b)).
  Both are asserted to be involutions changing the parity of `j`.
* p.315 gives three examples. All three are reproduced exactly by our
  implementation, including the nine-state chain of example (3).

**Source defect found (RR-L004).** The printed `phi` Case II rule
`m = Max{z <= a+2j-2 : z + lam(a+2j-1-z) <= t+5j-2}` is inconsistent with the
paper's own example (3): its admissible set is empty at the state
`(0;2,1,1,1)`, which the printed chain sends to `(-1;1,1)`. Taken literally, the
rule gives 2 692 defects among the 3 198 in-domain states of weight <= 18 and
the endpoint iteration cycles at `n = 2`. The reconstruction used, and why it is
the unique consistent completion, is `../Main/DECISIONS.md` D-3. Consequence for
citation: our `forward`/`inverse` are a **faithful reimplementation with one
reconstructed rule**, not a verbatim transcription.

**Still open.** GM81a and GM81b remain abstract/metadata only; no claim in this
cycle compares our work to Garsia--Milne's map, and none should be made until
`GM81b` pp.289-339 is read.
