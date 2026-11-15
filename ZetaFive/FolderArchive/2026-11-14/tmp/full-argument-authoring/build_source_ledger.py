"""Build the reproducible source ledger for the accompanying exposition."""
from pathlib import Path
import hashlib
import json

base = Path(__file__).resolve().parents[1]
workspace = base.parent
sha = "7fe736760f4b96bfdb4334b68e3b3124ecbe10b0"
repo = "https://github.com/mo271/Zeta5"
def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def paper(key, authors, title, url, role, locations, **extra):
    return dict(key=key, authors=authors, title=title, url=url, role=role,
                consulted_locations=locations, **extra)

sources = [
paper("persiflage", ["Frank Calegari (Persiflage)"], "zeta(5) is irrational",
 "https://galoisrepresentations.org/2026/09/24/zeta5-is-irrational/",
 "Explicitly requested guiding exposition and historical pointers; not the source of the quantitative estimates.",
 ["The formulas of Euler and Hermite", "Hankel Determinants", "The strategy",
  "Prevost's moments and the introduction of the zeta value"],
 date_displayed="2026-09-24",
 author_identity_source="https://math.uchicago.edu/~fcale/research.html",
 revision_caveat="The displayed publication date is recorded; the revision history of every paragraph is not established.",
 chronology="This post precedes Lai. No dependence on Lai is asserted."),
paper("fauzan", ["Aabir Fauzan"], "zeta(5) is irrational",
 "https://zenodo.org/records/22826419",
 "Concrete determinant construction, original local arithmetic strategy, real-energy argument, comparison measure and certificate data.",
 ["Sections 1.1, 2, 3, 4, 5, 6; Appendix A; Appendix B"],
 date_on_manuscript="2026-09-17",
 local_file="../sources/Fauzan_2026_zeta5.pdf",
 sha256=digest(workspace/"sources/Fauzan_2026_zeta5.pdf"),
 qualification="The original M=200 normalization estimate and smaller rank-loss claim are not assumed in this version."),
paper("firsching", ["Moritz Firsching", "Zeta5 contributors"], "Zeta5 Lean formalization",
 repo+"/tree/"+sha,
 "Primary source for the revised finite partial-fraction local estimates, M=400 normalizer, full rank loss, continuous growth profiles and corrected constant. Also cross-checks analytic derivations.",
 ["Apery/Arith", "Apery/Norm.lean", "Apery/Growth.lean", "Apery/Growth",
  "Apery/RealBound.lean", "Apery/MainEstimate.lean", "Apery/Measure.lean",
  "Apery/Potential.lean", "Apery/Energy*", "scripts/lemma61.py"],
 revision=sha, local_checkout="../sources/mo271-Zeta5",
 license="Apache-2.0",
 initial_substantive_commit="2c80b320d06b4395605edbd413649d19094507af",
 initial_commit_author="Moritz Firsching",
 additional_credit="Paul-Lez coauthored Comparator CI addition. Lean, Mathlib, PrimeNumberTheoremAnd contributors supply formal infrastructure/background.",
 verification_scope="Relevant source declarations/proofs inspected; complete Lean development not independently rebuilt for this draft."),
paper("lai", ["Chun Wing Lai"], "On Fauzan's Proof that zeta(5) is Irrational",
 "https://ai.vixra.org/pdf/2609.0080v1.pdf",
 "Later exposition used to cross-check and expand construction, positivity, exact degree and pullback; earlier chat drafts followed it.",
 ["Sections 3-7", "Theorem 9.3 and equations (106)-(107) checked for source discrepancy"],
 date_on_manuscript="2026-09-29", version="v1",
 local_file="../sources/Lai_2026_zeta5_rewrite.pdf",
 sha256=digest(workspace/"sources/Lai_2026_zeta5_rewrite.pdf"),
 qualification="Not a source on which Persiflage depends; literal corrected arithmetic conclusion is not used."),
paper("prevost", ["Marc Prevost"], "Remainder Pade approximants for the Hurwitz zeta function",
 "https://arxiv.org/pdf/1709.05389v1",
 "Exact antecedent for the positive measure, Stieltjes transform, Bernoulli moments and orthogonal-polynomial approximation viewpoint.",
 ["Section 2, equations (2.8)-(2.11)", "Theorems 1-2, equations (3.1)-(3.4)", "Section 4.1"],
 preprint_date="2017-09-15", journal="Results in Mathematics 74 (2019), article 51"),
paper("prevost1996", ["Marc Prevost"],
 "A new proof of the irrationality of zeta(2) and zeta(3) using Pade approximants",
 "https://doi.org/10.1016/0377-0427(95)00019-4",
 "Historical context, located through Prevost and Persiflage. No estimate imported.",
 ["Bibliographic identification and description in Prevost's later paper"],
 original_full_text_consulted=False),
paper("prevost-rivoal", ["Marc Prevost", "Tanguy Rivoal"],
 "Diagonal convergence of the remainder Pade approximants for the Hurwitz zeta function",
 "https://doi.org/10.1016/j.jnt.2020.10.019",
 "Background attribution for effective remainder Pade approximation; no theorem is used as an input.",
 ["Publisher abstract and bibliographic metadata"],
 publisher_url="https://www.sciencedirect.com/science/article/abs/pii/S0022314X20303620"),
paper("zudilin", ["Wadim Zudilin"], "A determinantal approach to irrationality",
 "https://arxiv.org/pdf/1507.05697v2",
 "Methodological antecedent: positive Hankel determinants, squared Vandermonde integrals, quadratic decay and coefficient normalization.",
 ["Proposition 2", "Section 2, equations (2)-(5)"],
 qualification="Its hypotheses differ; the criterion needed here is separately proved."),
paper("brown", ["Francis Brown"],
 "Mellin transforms, transfinite diameter and rational approximations of integrals",
 "https://arxiv.org/html/2604.20741v1",
 "Context for integral bilinear pairings, basis changes and denominator/common-factor savings.",
 ["Sections 3.1-3.2", "Sections 7.4-7.5"],
 qualification="No claim that the specific zeta(5) estimates occur in this paper."),
paper("krattenthaler", ["Christian Krattenthaler"],
 "A determinant identity for moments of orthogonal polynomials that implies Uvarov's formula for the orthogonal polynomials of rationally related densities",
 "https://arxiv.org/pdf/2103.03969v1",
 "General setting for rational modifications; primary confirmation of historical Uvarov connection.",
 ["Introduction", "Theorem 1", "Section 6", "References 8-9"],
 qualification="General determinant identity not invoked as an unproved step."),
paper("uvarov", ["V. B. Uvarov"],
 "The connection between systems of polynomials that are orthogonal with respect to different distribution functions",
 "https://doi.org/10.1016/0041-5553(69)90124-4",
 "Historical credit, consulted through Krattenthaler, not a proof input.",
 ["Krattenthaler Introduction, Section 6 and reference 9"],
 original_full_text_consulted=False),
paper("andreief", ["C. Andreief", "Peter J. Forrester (consulted account)"],
 "Andreief's integration identity",
 "https://arxiv.org/pdf/1806.10411v1",
 "Historical attribution and bibliographic confirmation of identity proved in the draft.",
 ["Introduction and identity", "Reference 5"],
 original_reference="C. Andreief, Mem. Soc. Sci. Phys. Nat. Bordeaux (3) 2 (1886), 1-14",
 original_full_text_consulted=False),
paper("dlmf", ["NIST DLMF editors and contributors"], "Digital Library of Mathematical Functions",
 "https://dlmf.nist.gov/",
 "Precise classical formula references.",
 ["4.36.3", "25.6.2", "25.11.29", "24.4", "24.10(i)"]),
]
reused=[]
for name in ["zeta5_detailed_argument.tex","appendix_classical.tex","appendix_algebra.tex"]:
    path=workspace/"detailed irrationality argument"/name
    reused.append({"file":"../detailed irrationality argument/"+name,"sha256":digest(path),
                  "role":"Earlier chat exposition expanded/reorganized and reattributed; not an independent mathematical source."})
notes={}
for name in ["analytic_sources.txt","local_sources.txt","global_sources.txt"]:
    path=base/"checks"/name
    if path.exists(): notes[name]=path.read_text(encoding="utf-8")
checks={}
for name in ["analytic_certificate.json","growth_exact_result.json","local_checks.json"]:
    path=base/"checks"/name
    if path.exists(): checks[name]={"sha256":digest(path),"results":json.loads(path.read_text(encoding="utf-8"))}
ledger={"created_local":"2026-11-14","timezone":"America/Los_Angeles",
 "purpose":"Audit trail for the full exposition requested using Persiflage as a guide.",
 "attribution_policy":"Credit mathematics, conceptual exposition, proof revisions, data and adapted code separately. Do not infer provenance from similarity alone. Distinguish consulted originals from historical references located indirectly.",
 "sources":sources,"earlier_chat_text_reused":reused,
 "detailed_source_maps":notes,"finite_checks":checks,
 "redistributed_source_excerpts":[{
     "file":"source-excerpts/InnerSum.lean",
     "source":repo+"/blob/"+sha+"/Apery/Growth/InnerSum.lean",
     "sha256":digest(base/"source-excerpts/InnerSum.lean"),
     "modification":"None; unmodified copy for exact table comparison.",
     "license":"Apache-2.0; see LICENSE.upstream.txt"}]}
(base/"source_ledger.json").write_text(json.dumps(ledger,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("Wrote source_ledger.json with",len(sources),"sources and",len(notes),"detailed source maps.")
