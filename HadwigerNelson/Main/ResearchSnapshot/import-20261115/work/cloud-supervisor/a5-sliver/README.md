# A5 sliver interval certificate — NOT RUN (definition incomplete)

Request (coordinator reply 20261114T211858): certify u1x*α3 + |u3x|*α1 ≤ 0 over
θ3 ∈ (155.704811°, 155.708600°) and θ3 ∈ (152.426823°, 152.430600°).

What the local files define (work/automation-supervisor/cycles/20261114T205121/history-response.json,
verifier coordinator chat for swarm smwguidy9, seq 54077, 2026-11-14T20:50:02Z):
  A = c1 + w,  v_j = c1 + (1 - s_j) u_j,  |A - v_j| = 1
  α_j = (σ² − 2 s_j + s_j²) / (2 (1 − s_j))
  w·u_1 = α_1, w·u_3 = α_3  ⇒  w_y = (u_1x α_3 + |u_3x| α_1)/det, det > 0
  apex below floor v = 1  ⇔  u_1x α_3 + |u_3x| α_1 ≤ 0

What is NOT defined anywhere locally: u_1, u_3 (unit directions?), s_1, s_3, σ as functions of θ3,
and the second free parameter (the rejected report's failing point was (28.72°, 155.70°), i.e. the
domain is 2-D; the sliver is only given as a θ3 range). m2's report/manifest that contains the
formulas was never downloaded into work/automation-supervisor/inbox/.

Decision: no script written. Guessing the parametrisation would produce a certificate of the wrong
statement. The coordinator has been asked (user-inbox message, 21:3xZ) to obtain from verifier m2 the
exact definitions and the range of the second parameter; once supplied, a rigorous check
(mpmath/fractions interval arithmetic with explicit error bounds) is a sub-second job to run here.
