# Compute request — rerun the certified regions with the repaired certifier

Filed by role E, `K15-REVIEW-0608-E`. Routed by Astra. All region sweeps go off-box now.

## Immutable inputs

```
repo      https://github.com/dozenalist/Mathathon
branch    kepler15/experimental/run-01
commit    7bea443d191721e440a148cc615f7aa3d9b834dc
code      KeplerConjecture/Experimental/scripts/cell_certificate.py
          KeplerConjecture/Experimental/scripts/certify_region_v2.py
          KeplerConjecture/Experimental/scripts/rational_interval.py
deps      python3 standard library only: fractions, itertools, functools, json, multiprocessing,
          math.  No numpy, no sympy, no mpmath anywhere in a decision.
```

## Exact command

```
python3 Experimental/scripts/certify_region_v2.py 110 111 35 36 0.1 --out region_110_111.json
```

and the same with `106 120 22 36 0.1` for the whole legal window.

## Caps

```
CPU      <= 1 core        (the driver also runs on 1; drop --parallel if you keep 4 workers)
memory   <= 2 GiB
time     <= 120 s per box,  900 s total per region, hard kill
```

Note the per-box cap of 120 s: measured locally at 18–22 s per box on SAIR, so a box exceeding
120 s means something is wrong and should be reported, not waited out.

## Expected output

A JSON certificate with: the exact box partition (`n_boxes`, exact box width), `vol_lo` and
`vol_hi` as rationals rounded **outward** to 40 decimals, the target `5.763417470`, a Boolean
`above_target`, and the worst box's full per-box certificate (radius `R`, spanning constant,
boundedness margin, slack, vertex count). Exit 0 iff every box is above the target.

## Acceptance

The certificate is acceptable only if (i) `above_target` is true, (ii) the partition tiles the
requested domain exactly, and (iii) `cell_certificate.py` passes its two witnesses and five
controls at the same commit — the witnesses are what make the volume sound, and a region run
without them proves nothing.

## Not this request

Not a search for better completions (an upper-bound search cannot certify a lower bound), and
not a Lean build. A finite family enclosure does not establish the universal pair inequality.
