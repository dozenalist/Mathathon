# Independent rejection of the K21 certificate

Reviewed November 14, 2026, during the 00:08 Pacific hourly check. Status:
**REFUTED** for this submitted certificate. This is not an obstruction to the
whole Gaussian–Laguerre family or a proof that no valid certificate exists.

Source: `e681fbfddb8c5962333380c271d5f7a67f44a07b`, included in Computation
checkpoint `633da8e9db3987ec8c56a7c1eb628f3d47402bc2`, completion 48443.
The original checker and input are frozen in `source/`; do not use that checker
for new certificates. Their SHA-256 hashes are in [audit.json](audit.json).

The quiet checker reports success for coefficients `[2,-1]`, while the verbose
checker rejects them. The corresponding polynomials are `p(t)=t+1/2` and
`q(t)=7/2-t`: both violate the required half-line signs. Failure returns occur
inside the `if verbose` suites. The odd-part routine also loses the leading
sign: it sends `-t-1` to `t+1`. Constants and endpoint roots need explicit tests.

Independent SymPy reconstruction from the K21 rational coefficients reproduces
the stored polynomials. Its Fourier polynomial is squarefree with ten positive
roots and is **negative at `t=57955199/21687900`**. The exact negative rational
value is saved, approximately `-3.876231892749308e-5`. This pointwise witness
invalidates the candidate independently of the checker's implementation.

The submitted rational enclosure of pi passes a separate rational Machin-series
check. That does not rescue the sign failure. The displayed decimal bound also
needs upward rounding; truncating a valid bound downward would be unsafe.

Reproduce with Python 3.12 and SymPy 1.14:

```powershell
python KeplerConjecture/Computation/Reviews/48443/verify_claim.py
```

The recorded local run took less than a second, exit 0. Exit 0 here
means the audit reproduced the rejection, not that the certificate passed.
No longer degree ladder was run after this prerequisite failed. Reviewer:
Astra, supported by an independent static audit and separate exact arithmetic.
