# Primary sources and research implications

Access date for this collection is November 13, 2026, America/Los_Angeles. `FULL_TEXT_CHECKED` means the cited statement or passage was inspected. It does not mean the complete proof or ancillary computation was independently reproduced.

## H05U — Hales's original local criterion

Thomas C. Hales, *A Proof of the Kepler Conjecture (unabridged)*, November 14, 2005. `FULL_TEXT_CHECKED`. The exact requested locator is Section 3.1, Definition 3.2 and Lemma 3.3, printed page 34, PDF page 46, with the proof beginning on printed page 34 and continuing on page 35. The abridged Annals article renumbers the corresponding statement as Lemma 1.3. [Official unabridged supplement](https://annals.math.princeton.edu/supplemental/2005/162-3/p01/proof_kepler.pdf), [Annals article](https://annals.math.princeton.edu/2005/162-3/p01)

For a saturated packing of unit balls with centers \(\Lambda\), let \(\Omega(v)\) be its Voronoi cells. A correction \(A:\Lambda\to\mathbb R\) is negligible when some \(C_1\) satisfies

\[
\sum_{v\in\Lambda\cap B(x,r)}A(v)\le C_1r^2
\quad(x\in\mathbb R^3,\ r\ge1).
\]

It is fcc-compatible when \(\operatorname{vol}\Omega(v)+A(v)\ge\sqrt{32}\) for every center. These conditions imply \(\delta(x,r,\Lambda)\le\pi/\sqrt{18}+C/r\), with \(C\) depending on \(\Lambda\) through \(C_1\). The signed sum and its uniformity in the observation center matter. The paragraph after the proof gives the generalized upper density bound \(4\pi/(3L)\) from corrected volumes bounded below by \(L>0\). [Definition 3.2, Lemma 3.3, and following paragraph](https://annals.math.princeton.edu/supplemental/2005/162-3/p01/proof_kepler.pdf#page=46)

## CE03 — Cohn–Elkies two-point linear programming

Henry Cohn and Noam Elkies, *New upper bounds on sphere packings I*, Annals of Mathematics 157 (2003), 689–714. `FULL_TEXT_CHECKED`. Read Section 2 for admissibility and Fourier conventions, Theorems 3.1–3.2 on pages 694–696, Section 5 for equality constraints, and Section 7 for numerical construction. [Paper](https://annals.math.princeton.edu/wp-content/uploads/annals-v157-n2-p09.pdf), [arXiv record](https://arxiv.org/abs/math/0110009)

Use \(\widehat f(y)=\int f(x)e^{-2\pi i\langle x,y\rangle}\,dx\). For real radial Schwartz \(f\), \(\widehat f(0)>0\), \(\widehat f\ge0\), and \(f(x)\le0\) when \(\lVert x\rVert\ge2\), the unit-sphere volume density satisfies

\[
\Delta_3\le\frac{4\pi}{3}\frac{f(0)}{\widehat f(0)}.
\]

The minimum-separation-one convention instead uses balls of radius \(1/2\) and a \(\pi/6\) factor. Radialization preserves feasibility and objective. Polynomial–Gaussian or Fourier-eigenfunction searches provide numerical baselines. Sharpness requires compatible zeros at nonzero lattice and dual-lattice lengths. Consult LI24 before proposing a sharp 3D function within these hypotheses. [Theorems 3.1–3.2 and Sections 5, 7](https://annals.math.princeton.edu/wp-content/uploads/annals-v157-n2-p09.pdf)

## LI24 — a rigorous obstruction to ordinary two-point LP in 3D

Rupert Li, *Dual linear programming bounds for sphere packing via discrete reductions*, Advances in Mathematics 460 (2024), 110043. Inspected arXiv v3, November 6, 2022. `FULL_TEXT_CHECKED`. Theorem 6.1 proves that the optimal 3D Cohn–Elkies **center-density** bound is greater than \(0.18398089\), exceeding \(2^{-5/2}\). Its certificate uses \(m=53\), \(r=\sqrt{89}\). Convert center density to volume density by multiplying by \(4\pi/3\). [Section 6 and Theorem 6.1](https://arxiv.org/html/2206.09876v3#S6), [published article](https://doi.org/10.1016/j.aim.2024.110043)

This rules out an exact Kepler proof using the ordinary Cohn–Elkies program, including any choice of modular or other symmetric functions within it. A stronger bound needs genuinely additional constraints. It remains useful to improve simple explicit bounds or understand the obstruction. Sections 3–5 describe discrete reduction and exact certification. The arXiv record provides `Mu_3_53_sqrt89.txt` and `verify_dual.sage`. Those ancillary computations have not been rerun locally. [Versioned record and ancillary files](https://arxiv.org/abs/2206.09876v3)

## V17 — Viazovska in dimension 8

Maryna S. Viazovska, *The sphere packing problem in dimension 8*, Annals of Mathematics 185 (2017), 991–1015. arXiv v2, April 4, 2017. `FULL_TEXT_CHECKED`. Theorem 2 states the LP bound. Theorem 3 constructs a radial Schwartz function with \(g(0)=\widehat g(0)=1\), \(\widehat g\ge0\), and \(g(x)\le0\) outside radius \(\sqrt2\). This certifies E8's density \(\pi^4/384\). The modular construction and global sign arguments are the mechanisms to study. A change of dimension requires a new valid construction and a strong enough bound. [Journal article](https://annals.math.princeton.edu/2017/185-3/p07), [versioned preprint](https://arxiv.org/abs/1603.04246v2)

## CKMRV17 — dimension 24 and version-sensitive certificates

Henry Cohn, Abhinav Kumar, Stephen D. Miller, Danylo Radchenko, and Maryna Viazovska, *The sphere packing problem in dimension 24*, Annals of Mathematics 185 (2017), 1017–1033. `FULL_TEXT_CHECKED` for the journal theorem and `METADATA_CHECKED` for the latest ancillary revision. Theorem 1.1 establishes Leech-lattice optimality and uniqueness among periodic optimal packings. The auxiliary function and its verification provide a second model of a short analytic certificate. [Journal PDF](https://annals.math.princeton.edu/wp-content/uploads/annals-v185-n3-p08-nodoi.pdf)

The current arXiv version is **v4, September 6, 2026**. Its record says `appendix.txt` corrects details of the published ancillary computation and preserves `appendix-original.txt`. Use the corrected version for reproduction and record its hash. Neither ancillary version has been run in this preparation. [Versioned record](https://arxiv.org/abs/1603.06518v4)

## CDS22 — concrete three-point hybrids and 3D benchmarks

Henry Cohn, David de Laat, and Andrew Salmon, *Three-point bounds for sphere packing*, arXiv:2206.15373v1, June 30, 2022. `FULL_TEXT_CHECKED`. Theorem 1.1, page 3, combines a Fourier-positive pair function and a positive-definite three-point kernel with finite-radius sign constraints. Theorem 1.4, page 5, treats lattice packings. Sections 5–6 explain parametrization and certification. [Paper](https://arxiv.org/pdf/2206.15373)

Table 1.1 on page 5 reports these 3D **volume-density** upper bounds.

| Method | Reported bound |
| --- | --- |
| Ordinary two-point LP | 0.779747 |
| Strengthened two-point bound | 0.773080 |
| General truncated three-point bound | 0.770271 |
| Lattice three-point bound | 0.741506 |

The first three apply to unrestricted packings. The last has a lattice hypothesis. Compare all with \(\pi/\sqrt{18}\approx0.740480489693\). These are published benchmarks, with local reproduction pending. Theorem 1.1 specializes to CE when the three-point term vanishes. Section 2.2 discusses a symmetrized strengthening and its practical parametrization limits. [Table 1.1 and Section 2.2](https://arxiv.org/pdf/2206.15373), [authors' numerical dataset](https://dspace.mit.edu/entities/product/d32e22af-d2e4-4084-abd9-998c9604e0b1)

## DLOV14 — additional constraints from local packing information

David de Laat, Fernando Mário de Oliveira Filho, and Frank Vallentin, *Upper bounds for packings of spheres of several radii*, Forum of Mathematics, Sigma 2 (2014), e23. `FULL_TEXT_CHECKED` for the abstract and Section 5 scope. Section 5 strengthens bounds for identical spheres using additional information. Read this alongside the strengthened two-point column in CDS22 before claiming that a local constraint is new. Its several-radius setting also helps identify which positivity conditions survive a proposed generalization. [Paper](https://arxiv.org/pdf/1206.2608), [published article](https://doi.org/10.1017/fms.2014.24)

## DV15 — convergent hierarchies

David de Laat and Frank Vallentin, *A semidefinite programming hierarchy for packing problems in discrete geometry*, Mathematical Programming 151 (2015), 529–553. Inspected arXiv v3, August 24, 2021. `ABSTRACT_CHECKED`, full theorem hypotheses require worker audit. The paper develops a hierarchy for topological packing graphs and proves convergence to their independence number. This supplies a conceptual route for local constraints. A specific finite level still needs a useful 3D bound and an explicit complexity comparison. [Versioned paper](https://arxiv.org/abs/1311.3789v3)

## DLM20 — recovering exact SDP certificates

Maria Dostert, David de Laat, and Philippe Moustrou, *Exact semidefinite programming bounds for packing problems*, arXiv:2001.00256v3, July 9, 2020, published in SIAM Journal on Optimization. `ABSTRACT_CHECKED`, algorithm details require worker audit. The authors round floating-point solutions to rational or quadratic-field certificates and apply them to geometric packing problems. This is relevant to turning a successful numerical search into inspectable evidence and to diagnosing nearly singular PSD matrices. [Versioned paper](https://arxiv.org/abs/2001.00256v3), [journal record](https://doi.org/10.1137/20M1351692)

## CZ14 — sphere packing through spherical codes

Henry Cohn and Yufei Zhao, *Sphere packing bounds via spherical codes*, arXiv:1212.5966, published in Duke Mathematical Journal 163 (2014), 1965–2002. `ABSTRACT_CHECKED`, theorem locators require worker audit. The paper improves the geometric passage from spherical-code bounds to packing bounds and compares it with CE. It supports a bounded alternate route through local angular constraints and a secondary higher-dimensional experiment. A new 3D consequence must be computed and its additional geometric assumptions proved. [Primary preprint](https://arxiv.org/abs/1212.5966)

## HM10 — dodecahedral local-volume benchmark

Thomas C. Hales and Sean McLaughlin, *The dodecahedral conjecture*, Journal of the American Mathematical Society 23 (2010), 299–344. `FULL_TEXT_CHECKED` for the main statement and computational outline. The author manuscript states the Voronoi-cell volume bound in Section 1, pages 1–2, and the stronger truncated-cell version as Theorem 2.1, page 6. Section 1.1 gives the density conversion \(4\pi/(3V)\). Section 3 identifies graph enumeration, LP, and interval arithmetic in the proof. [Author manuscript](https://www.cs.cmu.edu/~seanmcl/papers/McLaughlin-Dodec.pdf), [published record](https://doi.org/10.1090/S0894-0347-09-00647-X)

For a regular dodecahedron of inradius one, its edge is \(a=20/\sqrt{250+110\sqrt5}\), and \(V=(15+7\sqrt5)a^3/4\). Evaluating these geometric expressions in local double arithmetic gives \(V\approx5.5502910285155105\), hence \(4\pi/(3V)\approx0.7546973993374058\). This evaluation supplies the displayed digits, with the theorem providing the bound. Compare a proposed simple 3D bound with this benchmark and account for any imported proof machinery. [Main statement and density conversion](https://www.cs.cmu.edu/~seanmcl/papers/McLaughlin-Dodec.pdf#page=2)

## H12 — revised proof architecture

Thomas C. Hales, *Dense Sphere Packings: A Blueprint for Formal Proofs*, Cambridge University Press, London Mathematical Society Lecture Note Series 400 (2012). `AUTHOR_METADATA_CHECKED`, book not read in this preparation. Hales identifies it as the second-generation proof used for Flyspeck. Compare any proposed simplification with this revised architecture as well as H05U. Resolve exact chapter locators before relying on a particular lemma. [Author's book list](https://publicationsthomashales.wordpress.com/books/)

## FLY17 — formal verification and actual computational obligations

Thomas Hales and 21 coauthors, *A formal proof of the Kepler conjecture*, Forum of Mathematics, Pi 5 (2017), e2. arXiv:1501.02155v1, January 9, 2015. `FULL_TEXT_CHECKED` for introduction and verification architecture. The formal proof combines HOL Light and Isabelle and checks both textual mathematics and computational components. Read the main formal theorem, Section 7 on tame graphs, and the computational verification sections before estimating what a replacement certificate removes. A newly formalized reduction must disclose all outstanding local inequalities. [Published paper](https://doi.org/10.1017/fmp.2017.1), [preprint](https://arxiv.org/abs/1501.02155v1)

## FORM26 — recent Lean infrastructure

Sidharth Hariharan, Christopher Birkbeck, Seewoo Lee, Ho Kiu Gareth Ma, Bhavik Mehta, Auguste Poiroux, and Maryna Viazovska, *Progress in Formalizing Sphere Packing in Dimension 8*, arXiv:2604.23468v3, May 29, 2026. `ABSTRACT_CHECKED`. The current title supersedes the earlier *A Milestone in Formalization* title. The authors report a February 2026 formalization milestone with Gauss-assisted final stages. Inspect actual repository declarations, dependencies, and axioms before reusing any infrastructure. Compatibility with Mathathon's pinned Lean/mathlib remains unverified. [Current version](https://arxiv.org/abs/2604.23468v3)
