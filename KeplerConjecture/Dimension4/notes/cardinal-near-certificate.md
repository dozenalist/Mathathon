# A Schwartz near-certificate that fails the packing sign

This construction satisfies the normalization, Fourier positivity, and both
lattice zero conditions required of an exact $D_4$ certificate. It nevertheless
fails the sign condition at an explicit point. It isolates why reproducing the
arithmetic zeros is insufficient. It is an elementary construction for this
exposition, with no claim of novelty.

Use the Fourier convention

$$
\widehat g(\xi)=\int_{\mathbb R^n}g(x)e^{-2\pi i x\cdot\xi}\,dx.
$$

Choose a real, even, nonnegative $C_c^\infty$ function $\kappa$ supported in
$[-1/20,1/20]$, with integral $1$. For example, normalize the bump

$$
\kappa(s)=C\begin{cases}
\exp\!\left(-\frac1{1-400s^2}\right),& |s|<1/20,\\
0,& |s|\ge1/20.
\end{cases}
$$

Set

$$
\rho=\kappa*\kappa,\qquad
h=\mathbf1_{[-1/2,1/2]}*\rho,\qquad
\phi=\mathcal F^{-1}h.
$$

The function $h$ is smooth, nonnegative, and supported in $[-3/5,3/5]$.
Because $\rho$ has integral $1$ and support in $[-1/10,1/10]$,

$$
h(0)=1,\qquad \int_{\mathbb R}h=1,\qquad h(m)=0
\quad(m\in\mathbb Z\setminus\{0\}).
$$

Fourier inversion and evenness give

$$
\phi(t)=\operatorname{sinc}(t)\,\widehat\kappa(t)^2,
\qquad
\operatorname{sinc}(t)=\frac{\sin(\pi t)}{\pi t},
\quad \operatorname{sinc}(0)=1.
$$

Since $h\in C_c^\infty$, $\phi$ is a real Schwartz function. In particular,
$\phi(0)=1$ and $\phi(m)=0$ for every nonzero integer $m$.

## Transport to the product lattice

Let $B$ be any real basis matrix for $D_4$, with its basis vectors as columns.
Its determinant has absolute value $2$. Write

$$
\mathcal B=\begin{pmatrix}B&0\\0&B\end{pmatrix},\qquad
\Lambda=D_4\times D_4=\mathcal B\mathbb Z^8,
\qquad |\det\mathcal B|=4.
$$

For $z=(x,y)\in\mathbb R^8$, define

$$
F(z)=\prod_{j=1}^{8}\phi\bigl((\mathcal B^{-1}z)_j\bigr).
$$

This is Schwartz, and change of variables gives the exact Fourier transform

$$
\widehat F(\xi)=4\prod_{j=1}^{8}
h\bigl((\mathcal B^T\xi)_j\bigr).
$$

It follows that

$$
F(0)=1,\qquad \widehat F(0)=4,\qquad \widehat F\ge0,
$$

and

$$
F|_{\Lambda\setminus\{0\}}=0,\qquad
\widehat F|_{\Lambda^*\setminus\{0\}}=0.
$$

Indeed, the coordinate vector is a nonzero integer vector at each relevant
lattice point, so at least one factor vanishes. No numerical approximation is
used in these assertions.

## An explicit sign violation

Let $b_1$ be the first column of $B$ and take

$$
z_0=((5/2)b_1,0).
$$

Every nonzero vector in $D_4$ has length at least $\sqrt2$. Thus $z_0$ belongs
to the required lattice sign set: its four relevant lengths are
$(5/2)|b_1|,0,(5/2)|b_1|,(5/2)|b_1|$.

On the support of $\kappa$,

$$
\cos(2\pi(5/2)s)\ge\cos(\pi/4)=\frac1{\sqrt2}.
$$

Hence $\widehat\kappa(5/2)\ge1/\sqrt2$, and therefore

$$
F(z_0)=\phi(5/2)
=\frac{2}{5\pi}\widehat\kappa(5/2)^2
\ge\frac1{5\pi}>0.
$$

This contradicts the required inequality $F(z_0)\le0$.

## Consequence for the research program

Even a smooth, rapidly decreasing, Fourier-positive function with the exact
normalization and every required lattice zero can be decisively unsuitable.
These conditions are necessary but do not replace a proof of the continuum
sign inequality.

This example depends on the chosen lattice basis and is not simultaneously
$O(4)$-invariant. Averaging it over arbitrary simultaneous rotations does not
preserve its prescribed zeros on the fixed lattice. Symmetry averaging preserves
all requirements for a genuinely feasible packing certificate because its
continuum sign conditions are rotation invariant; this example lacks that
crucial hypothesis.
