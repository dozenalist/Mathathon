# Local computation requests — role X (Counterexamples)

For Main to collect into `Main/LOCAL_COMPUTE_REQUESTS.md`. Both requests are independent;
`X-R01` is the valuable one and `X-R02` is a hardening check. Neither is on the critical path
for X's audit conclusions, which are complete and depend only on exact arithmetic already run
in-VM (`Counterexamples/evidence/normalization_check.out`).

---

## X-R01 — exact semialgebraic optimisation of the 3D Laguerre–Gaussian CE family

```text
request_id            X-R01
claim_id              K15-X-C008
owner                 X (i-ve-attached-viazovska-f7hh, role Counterexamples)
independent_reviewer  C (using-the-chats-in-mcl6)
purpose               Obtain a fully certified 3D CE value inside the exactly-decidable family
                      f = sum_{k<=K} c_k L_k^{1/2}(2*pi|x|^2) e^{-pi|x|^2}, i.e. the exact optimum
                      of  minimise p(0)/q(0)  s.t.  p(s) <= 0 on [4,inf), q(s) >= 0 on [0,inf),
                      where p and q are the polynomials of f and fhat in s=|x|^2. This is the
                      reproducible control the roadmap asks for, with no grids and no tails.
repository branch     kepler15/counterexamples/run-01
source commit         5c6eac3 (research commit; later commits touching only this manifest do not affect the run)
tracked paths         KeplerConjecture/Counterexamples/ce_laguerre_exact.py
                      KeplerConjecture/Counterexamples/ce_lp_search.py
exact command         cd KeplerConjecture/Counterexamples
                      python3 - <<'PY'   # driver provided in the request body below
deps                  python 3.12, sympy 1.14.0, numpy 2.5.3, scipy 1.18.1 (all already present)
estimated resources   < 4 GB RAM, single thread, < 20 min for K <= 12
precision             exact rational arithmetic throughout (sympy Rational); no floating point in
                      the certificate. Search step may use floats; only exact output is reported.
seed                  none (deterministic)
parameter bounds      K in 1..12; grid for the search step: 2000 points on [4,400] and
                      2000 on [0,400], refined by adding any point where the exact certificate
                      fails (cutting planes), at most 200 refinement rounds
expected outputs      KeplerConjecture/Counterexamples/evidence/ce_opt_K{K}.json with
                      {K, coefficients as exact rationals, p, q, p(0), q(0), bound_occupied,
                       sturm_roots_p_on_[4,inf), sturm_roots_q_on_[0,inf)}
success criterion     for each K: Sturm counts are 0 and 0, signs are correct at the domain
                      endpoints, and bound_occupied = (4pi/3) p(0)/q(0) is reported as an exact
                      rational times pi. Sanity assertion (Li, Thm 6.1): the limit over K must
                      stay strictly above 0.740480489; a value below it means an implementation
                      error, not a theorem.
certificate format    exact rational coefficient vector + Sturm root counts; independently
                      re-checkable by re-running ce_laguerre_exact.certify(c, K)
status                exploratory-to-rigorous: whatever passes the exact certificate IS a theorem
                      about all packings of unit balls; whatever fails is discarded
current state         certifier written and validated (eigenbasis verified to 4.6e-15); the naive
                      grid LP produced only spurious points (X-C007), so a cutting-plane loop is
                      required. Not run locally yet.
next X task while pending: X-C002's open question O2 (soft non-sharpness in 3D from Barlow
                      difference sets), and the distributional form of X-C001 (O1).
```

Driver sketch (self-contained, to be committed alongside):

```python
# minimise p(0) subject to p<=0 on [4,inf), q>=0 on [0,inf), q(0)=1, p(0)>0;
# iterate: solve LP on the current point set -> round to rationals with denominator 10**9
#          -> certify exactly (Sturm) -> if it fails, extract the violating s from the exact
#          polynomial, add it to the point set, repeat.
```

## X-R02 — hardening: independent re-verification of the icosahedral and dodecahedral constants

```text
request_id            X-R02
claim_id              K15-X-C003
owner                 X
independent_reviewer  M
purpose               Recompute, with a second independent method, the two polytope volumes that
                      fix the dodecahedral ceiling: V(regular dodecahedron, inradius 1) = 5.5502910
                      and V(rhombic dodecahedron, inradius 1) = 4*sqrt(2) = 5.6568542, and the
                      forced correction A >= 4*sqrt2 - V_dod = 0.1065632.
repository branch     kepler15/counterexamples/run-01
source commit         5c6eac3 (research commit; later commits touching only this manifest do not affect the run)
tracked paths         KeplerConjecture/Counterexamples/normalization_check.py  (section 4)
exact command         cd KeplerConjecture/Counterexamples && python3 normalization_check.py
deps                  sympy 1.14.0, numpy 2.5.3, scipy 1.18.1
estimated resources   < 1 GB RAM, < 1 min
precision             1e-9 absolute on the hull volumes; the closed forms
                      (15+7*sqrt5)/4 * (1/1.113516...)  and  4*sqrt2  should be checked symbolically
success criterion     both closed forms reproduce the hull volumes to 1e-12, and the derived
                      density ceiling (4pi/3)/V_dod = 0.7546974 matches Hales-McLaughlin's
                      published 0.7546974 to 1e-6
status                rigorous once the closed forms are symbolic
current state         hull computation passes; the symbolic closed form is not yet checked
```
