"""Reuse and revise the opening exposition from this chat.

The underlying mathematics is Fauzan/Lai, with Prevost's earlier
representation and Persiflage's guiding perspective explicitly credited.
This script contains no externally copied prose.
"""
from pathlib import Path
root = Path(__file__).resolve().parents[2]
dest = root / "full argument with attribution" / "parts"
old = (root / "detailed irrationality argument" / "zeta5_detailed_argument.tex").read_text(encoding="utf-8")
start = old.index(r"\heading{2. Defining")
end = old.index(r"\newpage" + "\n" + r"\heading{7. Making")
body = old[start:end]
replacements = {
r"\heading{2. Defining the functional carefully}{Lai, section 4, Definition 4.2.}":
r"""\section{A rational functional and a positive measure}\label{sec:functional}
\source{Construction: Fauzan \cite[(2.2)--(2.3)]{fauzan} and Lai
\cite[Definition 4.2]{lai}. The presentation follows the functional
viewpoint in Persiflage \cite{persiflage}.}
\subsection{Defining the functional carefully}""",
r"\heading{3. Why the polynomial values are moments}{Lai, section 4, Lemma 4.5.}":
r"""\subsection{Why the polynomial values are moments}
\source{Pr\'evost \cite[Theorems 1--2]{prevost};
Fauzan \cite[Proposition 2.2]{fauzan}; Lai \cite[Lemma 4.5]{lai}.}""",
r"\heading{4. Why the pole values are the same integrals}{Lai, section 4, Lemma 4.6.}":
r"""\subsection{Why the pole values are the same integrals}
\source{The Stieltjes representation is Pr\'evost's \cite[Theorem 1]{prevost}.
The fifth-order calculation is also in Fauzan \cite[Proposition 2.2]{fauzan}
and Lai \cite[Lemma 4.6]{lai}.}""",
r"\heading{5. Building a polynomial from the functional}{Lai, section 5, Definitions 5.1--5.2 and Lemma 5.4.}":
r"""\section{Modifying the measure and taking its determinant}\label{sec:determinant}
\source{Fauzan \cite[Section 2.1]{fauzan}; Persiflage
\cite[Hankel Determinants]{persiflage}; Lai \cite[Section 5]{lai}.}
\subsection{The modifier and its affine moments}""",
r"\heading{6. Evaluating the matrix at $\xi$}{Lai, section 5, Proposition 5.6.}":
r"""\subsection{Evaluating the matrix at \(\xi\)}
\source{The positive Gram interpretation is explicit in Fauzan
\cite[Proposition 2.2]{fauzan}, Persiflage \cite{persiflage},
and Lai \cite[Proposition 5.6]{lai}.}""",
"The third equality is the theorem proved in sections 3--4 of this account.":
"The third equality is the representation proved in Section~\\ref{sec:functional}.",
"Appendix B proves exact degree $h$, but the upper bound suffices here.":
"Section~\\ref{sec:exact-degree} proves exact degree $h$, but the upper bound suffices.",
"for the determinant comes from a separate identity, stated in section 8 below.":
"for the determinant comes from Andr\\'eief's identity, proved in the analytic section.",
}
for a,b in replacements.items():
    if a not in body: raise ValueError(a)
    body = body.replace(a,b)
body = body.replace(r"\newpage"+"\n","")
body += r"""

\subsection{Putting both estimates on the same scale}
Fauzan uses the positive rational scalar
\begin{equation}\label{eq:normalization}
 S_K=\frac{(K!)^{2h}4^{h-1}}
 {(N!)^{12h}\prod_{i=1}^{h-1}((2i)!)^2},
 \qquad F_K(X)=S_K\Delta_K(X).
\end{equation}
This is his equation (2.5) \cite{fauzan}, also retained in
\texttt{Apery/Construction.lean} \cite{firsching}.
It follows at once that
\[
 F_K\in\Q[X],\qquad \deg F_K\leq h,\qquad F_K(\xi)>0.
\]
The rescaling is useful because factorial valuations admit exact formulas,
and factorial sizes admit Stirling estimates. It does not, on its own,
make every coefficient integral.

The need for a separate arithmetic estimate can be seen from a change of
basis. If \(E_i=\sum_j c_{ji}t^j\), then the pairing matrix in the \(E_i\)
basis is \(C^{\mathsf T}G_KC\), with determinant
\((\det C)^2\Delta_K\). This standard identity is used explicitly by Fauzan
\cite[Sections 3--4]{fauzan}; it also fits the determinant-normalization
framework in Brown \cite[Sections 3 and 7.5]{brown}.
Over \(\R\), basis changes help recognize positivity. At a prime \(p\),
a basis with \(p\)-adic-unit determinant preserves the determinant's
valuation while making coefficient divisibility easier to see.
"""
(dest/"construction.tex").write_text(body,encoding="utf-8")

algebra=(root/"detailed irrationality argument"/"appendix_algebra.tex").read_text(encoding="utf-8")
split=algebra.index(r"\newpage"+"\n"+r"\heading{Appendix C.")
degree=algebra[:split]
degree=degree.replace(r"\newpage"+"\n","")
degree=degree.replace(
r"\heading{Appendix B. Why the degree is exactly $h$}"+"\n"+
r"{Lai, section 6, Proposition 6.1. Optional for the irrationality argument.}",
r"""\section{Why the degree is exactly \(h\)}\label{sec:exact-degree}
\source{Fauzan \cite[(2.9)]{fauzan}; Lai \cite[Proposition 6.1]{lai};
the same formula is stated in Persiflage \cite{persiflage}.}""")
(dest/"exact_degree.tex").write_text(degree,encoding="utf-8")
pull=algebra[split:].replace(r"\newpage"+"\n","")
pull=pull.replace(
r"\heading{Appendix C. The same functional in different coordinates}"+"\n"+
r"{Lai, section 7, Lemma 7.3. Optional once the arithmetic estimate is assumed.}",
r"""\section{The pullback to integer poles}\label{app:pullback}
\source{Fauzan \cite[(3.1)]{fauzan}; Lai \cite[Lemma 7.3]{lai};
Firsching \cite[\texttt{Arith/Pullback.lean}]{firsching}.}""")
pull=pull.replace("The auxiliary functional in section 7 changes the pole locations from",
"The auxiliary arithmetic functional changes the pole locations from")
pull=pull.replace(
"\\[\n \\boxed{\\mu_X(R)=\\tau_X\\!\\left(x^5R(-x^2)\\right).}\n\\]",
"\\begin{equation}\\label{eq:pullback}\n \\boxed{\\mu_X(R)=\\tau_X\\!\\left(x^5R(-x^2)\\right).}\n\\end{equation}")
(dest/"pullback.tex").write_text(pull,encoding="utf-8")

classical=(root/"detailed irrationality argument"/"appendix_classical.tex").read_text(encoding="utf-8")
classical=classical.replace(r"\newpage"+"\n","")
classical=classical.replace(
r"\heading{Appendix A. A common source for the two integral formulas}"+"\n"+
r"{A Fourier-series calculation supplies the classical identities used in the proof.}",
r"""\section{Classical formulas used in the integral representation}\label{app:classical}
\source{Euler's formula, Hermite's formula, and the partial fractions of
\(\coth\) are classical; exact references are \cite{dlmf}.
This appendix expands the derivation in the earlier draft of this chat.}""")
classical=classical.replace(
r"\heading{Appendix A, continued. The Hurwitz integral}"+"\n"+
r"{Deriving the fifth-order formula, including the interchange of integrals.}",
r"\subsection{The Hurwitz integral}")
(dest/"classical.tex").write_text(classical,encoding="utf-8")
print("Wrote construction, exact degree, classical identities, and pullback.")
