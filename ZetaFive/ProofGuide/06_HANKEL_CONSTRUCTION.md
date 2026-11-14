# 6. How the matrix produces a polynomial of controlled degree

[Overview](../PROOF_OVERVIEW.md) · [Previous: positivity](05_POSITIVITY.md) · [Next: moments](07_MOMENT_REPRESENTATION.md)

**Corollary 5.5 gives the degree bound needed for irrationality. Proposition 6.1 shows that the degree is exactly $h=37n$.** Both facts come from the simple poles of the rational functions used in the matrix.

Recall $D_r(t)=\prod_{j=1}^r(t+j^2)$, $W(t)=D_N(t)^6/D_K(t)$, and $h=K-N$. The rational-function variable $t$ and the polynomial variable $X$ are independent. The rule $\mu_X$ is rational-linear and takes rational functions in $t$ to affine polynomials in $X$; its full definition appears in [companion 7](07_MOMENT_REPRESENTATION.md).

Definitions 5.1–5.2 set

$$
G_K(X)_{ij}=\mu_X\bigl(W(t)t^{i+j}\bigr)
\quad(0\le i,j<h),\qquad
\Delta_K(X)=\det G_K(X).
$$

The indices start at zero. Entries depend only on $i+j$, so they are constant along anti-diagonals; this is the meaning of **Hankel matrix**.

## To bound the degree, it suffices to have affine entries

Suppose each entry is $a_{ij}X+b_{ij}$ with rational coefficients. Every term in the determinant expansion is a product of $h$ such entries, so has degree at most $h$. The sum also has degree at most $h$:

$$
\deg\Delta_K\le h.
$$

The nonzero rational factors $S_K$ and $m_{K,M}$ do not change degree. This proves the upper bound for $Q_{K,M}$ used in Lemma 3.1. The arithmetic branch is still needed to make its coefficients integers.

## To prove exact degree, show that the leading coefficient survives

Write

$$
G_K(X)=G_0+XG_1,
$$

where $G_0$ and $G_1$ are rational matrices, depending on $K$. The coefficient of $X^h$ in $\det(G_0+XG_1)$ is $\det G_1$. Thus exact degree follows from $\det G_1\ne0$.

Let

$$
T(t)=\frac{D_K(t)}{D_N(t)}
=\prod_{k=N+1}^K(t+k^2),\qquad x_k=-k^2.
$$

The $x_k$ are the $h$ distinct poles remaining in $W=D_N^5/T$. Define nonzero rational numbers

$$
d_k=\frac{k^4D_N(x_k)^5}{T'(x_k)}
\quad(N<k\le K),
$$

where the prime denotes polynomial differentiation. The residue calculation below gives

$$
(G_1)_{ij}=\sum_{k=N+1}^K d_k x_k^{i+j}.
$$

Let $\mathcal V$ be the square matrix with entries $\mathcal V_{ik}=x_k^i$, with rows $0\le i<h$ and columns $N<k\le K$. This matrix is distinct from the external field $V(t)$ in companion 4. Then

$$
G_1=\mathcal V\,\operatorname{diag}(d_{N+1},\ldots,d_K)\,\mathcal V^{\mathsf T}.
$$

Here $\operatorname{diag}$ means the diagonal matrix with the displayed entries. The Vandermonde formula gives

$$
\det\mathcal V=\prod_{N<k<\ell\le K}(x_\ell-x_k)\ne0.
$$

Each $d_k$ is nonzero as well: none of the remaining poles is a zero of $D_N$, and all roots of $T$ are simple. Consequently

$$
[X^h]\Delta_K=(\det\mathcal V)^2\prod_{k=N+1}^Kd_k\ne0.
$$

The notation $[X^h]$ means “coefficient of $X^h$.” This is the mechanism behind Proposition 6.1.

In fact, using $\prod_kT'(x_k)=(-1)^{h(h-1)/2}(\det\mathcal V)^2$ simplifies the coefficient to

$$
[X^h]\Delta_K
=(-1)^{h(h-1)/2}\prod_{k=N+1}^K k^4D_N(-k^2)^5.
$$

This particular coefficient is an integer. That does not establish integrality of the other coefficients.

## Where the affine entries and the weights come from

Lemma 5.4 supplies the partial fractions of

$$
R_{ij}(t)=W(t)t^{i+j}
=\frac{D_N(t)^5t^{i+j}}{T(t)}.
$$

Because the poles are simple, there is a polynomial $P_{ij}(t)$ with rational coefficients such that

$$
R_{ij}(t)=P_{ij}(t)+
\sum_{k=N+1}^K\frac{c_k^{ij}}{t+k^2},
\qquad
c_k^{ij}=\frac{D_N(x_k)^5x_k^{i+j}}{T'(x_k)}.
$$

The superscript $ij$ labels the entry; it is not an exponent. The residue formula follows by multiplying by $t+k^2$ and evaluating at $t=x_k$. Polynomial division gives the polynomial part; it is zero when $6N+i+j<K$.

The two features of $\mu_X$ needed here are:

- It sends a polynomial in $t$ with rational coefficients to a rational constant, independent of $X$.
- It sends $1/(t+k^2)$ to an affine polynomial whose coefficient of $X$ is $k^4$.

Applying $\mu_X$ to the partial fraction expansion therefore gives an affine matrix entry. Its coefficient of $X$ is $\sum_k k^4c_k^{ij}=\sum_k d_kx_k^{i+j}$, exactly the expression used above.

Thus Lemma 5.4 leads to Corollary 5.5, and the same residues supply the additional Vandermonde argument in Proposition 6.1.

## Why the numerator was built into the matrix

The factor $D_N^6$ cancels the first $N$ factors of $D_K$, leaving $h=K-N$ simple poles. It also leaves fifth-order zeros at the canceled locations through $W=D_N^5/T$. Those zeros create arithmetic cancellations in the local estimates.

On the positive integration axis, every factor remains positive. This preserves the Gram-matrix argument from [companion 5](05_POSITIVITY.md). The same choice therefore serves positivity and divisibility, while its effect on real size is measured by the external field in companion 4.

## A small example of the construction

For illustration only, use $N=0$, $K=2$, and hence $h=2$. These are not the parameters of the asymptotic proof. Then $D_0=1$ and $W=1/((t+1)(t+4))$. The functional in companion 7 gives

$$
G(X)=
\begin{pmatrix}
-5X+21/4&21X-87/4\\
21X-87/4&-85X+529/6
\end{pmatrix},
$$

so

$$
48\det G(X)=-768X^2+1268X-489.
$$

This exhibits affine entries, degree equal to matrix size, and a rational determinant that becomes integral after scaling. A single example says nothing about asymptotic decay; that requires the two estimates in companions 3 and 4.
