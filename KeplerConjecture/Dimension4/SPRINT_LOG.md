# Dimension-4 research sprint

Requested duration: one hour. Date: 14 November 2026.

The one-hour research and review block ran from **19:44:55 to 20:44:55 UTC**
(11:44:55 to 12:44:55 Pacific). Publication followed the final repository
checks after the block closed.

Three independent research subagents assessed the primary literature,
computational feasibility, and analytic obstructions. A fourth agent performed
a fresh adversarial review of the final mathematical claims. The coordinating agent developed the
cardinal counterexample, angular local profiles, the main exposition, and
the stronger real-Gaussian integral obstruction together with independent
checks from the theory and literature agents.

The initial local commit was
`5746863f92b9d7dade5854c311b237ed04020106`. The repository was subsequently
fast-forwarded to the existing GitHub main commit
`a33bb8323d5fb572b65b33d699989b038d8f0cc6`, preserving the newer project work.
At the publication review it was fast-forwarded again to
`4740a0d1ef23491599b8d26972c094766b5308f3` to retain concurrent zeta(5)
documentation updates.
The final publication base also includes
`6b96be24d6df7fc68b06203e162804629655401b`, preserving the concurrent
Hadwiger–Nelson exposition update.
Only the new `KeplerConjecture/Dimension4` folder is part of this sprint's
publication changes.

## Reproduction and review

The coordinating agent reran the artifact generators and independent checks
at approximately 20:27–20:28 UTC. All 388 Fourier-algebra checks and 24 saved
rank witnesses passed, as did the exact angular-profile checks and the
60/90-digit inspection of the published solver slice. The final plot was
visually inspected, and all 33 local Markdown links, display-math delimiters,
code fences, and JSON artifacts passed the publication checks.

The fresh adversarial reviewer independently checked the product theorem,
Li's dimension-4 obstruction, and the strongest derived Gaussian-integral
and angular-quadrature arguments. No mathematical gap was found. This review
does not replace formal proof checking or certify the stored numerical solver
output.

## Work completed during the research block

* Audited the lattice theorem, exact normalization, original two-point
  obstruction, modular ingredients, and recent claims about dimension 4.
* Proved and independently checked restrictions on radial, angular, Gaussian,
  positive-kernel, and real Gaussian-integral function classes.
* Built exact Fourier and shell-interpolation diagnostics and independently
  verified their saved finite-rank witnesses.
* Constructed an explicit Schwartz near-certificate with all arithmetic zeros
  and Fourier positivity but a rigorous sign violation.
* Developed and checked angular harmonic lifts and exact local primal/dual
  profiles, including their limits as evidence.
* Retrieved bounded byte ranges from the published numerical archive,
  reconstructed a first-shell slice, and compared 60- and 90-digit evaluations.
* Prepared the report, reproducible artifacts, figure, source provenance,
  and explicit claim ledger for publication.

No new sphere-packing density bound or exact auxiliary function was found.
No external Mathathon submission or recurring automation was created.
