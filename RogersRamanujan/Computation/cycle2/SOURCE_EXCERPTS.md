# Source excerpts used by `bz82_audit.py`

For source auditing: the operative lines of the paper, extracted with
`pdftotext -layout` from the scan

    https://sites.math.rutgers.edu/~zeilberg/mamarimY/rrDG.pdf
    sha256 403543088ed9465bc8e3f9918defd22a57c86a21493226c9852729af614483c6

which is byte-identical (same sha256) to the copy recorded in
`Literature/READING_NOTES.md`. OCR noise is preserved below exactly as
extracted; the bracketed `[OCR: ...]` notes are mine and are the only
editorial additions. `Computations/cycle2/bz82_audit.py` is transcribed from
these lines, not from any secondary summary.

## p. 313 -- the two families, the shift, the state space

```
A(n) ={()t(1), . . . , A(t)); t20, A(1)+ - -- +).(t) = n, A(i)-)t(i+ 1)>2 for
i= 1, . . . , t-1 and A(t)>0}, C(n)={(A(1), . . . , A(t)); tzo, A(1)+ ---+/
\(t)= n, A(i)-)t(i+1)>0 and M051, 4(mod 5) for i=1,...,t}
```
[OCR: `t20` = `t >= 0`; `A(i)-)t(i+1)>2` = `lam(i) - lam(i+1) >= 2`;
`M051, 4(mod 5)` = `lam(i) = 1, 4 (mod 5)`. So their `A(n)` is our `D_n` and
their `C(n)` is our `A_n`.]

```
B(n)={()t(1), . . .,)t(t)); t>0, A(1)+ - - - +A(t) =n and A(1)2---2A(t)2t}
by (Ml),..,).(t))<->()t(1)-t+1,...,)t(i)+2i-1-t,...,A(t)+t-1).
```
[OCR: `A(1)2---2A(t)2t` = `lam(1) >= ... >= lam(t) >= t`.]

```
X(n)={(j;A(1),...,A(t));-oo<j<oo, t20,/(1)>~->)(t)>0
                                 and %(5j2-j)+)(1)+ - - . +)t(t)=n}
```
[OCR: `%(5j2-j)` = `j(5j-1)/2`. Note the pentagonal number is `j(5j-1)/2`,
not `j(3j-1)/2`.]

## p. 314 -- phi

```
Definition of (p. Consider (1'; M1), . . . , )l(t))eX(n)-OXB(n). Let a=
Min{x; 2i+x-/(x)>0}, u =2i+a-A(a), t*= t+x(A(a)=0)+x(A(u)=0).
  Case I: A(a)+)t(p.)~5j2 t*. Delete the parts )l(a) and Ma); add 1 to each of
the remaining parts and insert A(a)+)t(p.)-5j-t* new parts of 1; j<-j+1.
  Case 11: A(a)+)t(p.)-5j<t*. Let
         m =Max{zSa+2j-2; z+)t(a+2j-1-z)$t+5j-2}.
Subtract 1 from each of the 1? parts and create new parts m and t+5j-3-m;
j<-j-1.
```
[OCR: `~5j2 t*` is `>= 5j + t*`; `$t+5j-2` is `<= t+5j-2`; `1?` is `t`.]

The paper's own argument that phi is an involution, verbatim:

```
Indeed if a, i, etc. are the new values of a, j etc. after an application of
Case I, then f=j+1, d=a-1, )t(d)=)t(a+1)+1, [L=2f+a-)t(d)=2j+a-}l(a+1)>p.,
T=)t(a)+)t(p.)-(5j+2), so W+X(_)-51-< f and we arrive at Case II. Furthermore,
applying Case II now yields m =A(a), f+5i-3-m=}t(p.) and we are back where we
started.
```

## p. 314 -- psi

```
Definition of :11. Consider (j;)l(1),. . . , )t(t))e X(n)- O X C(n). Let to be
the number of parts which are = 0 (mod 5) and for i = 0, 2, 3 let mi be the
largest part which is = i (mod 5) (if there are no such parts m,- = 0).
  Case I: t0+j>0 or m2>0.
  Case I(a): 5t0+5j-3>m2. Subtract 5 from each of the t0 parts which are
=0(mod 5) and insert a new part of 5t0+5j-3, j<-j-1.
  Case I(b): 5to+5j-3<m2. Delete the part m2, add 5 to each of the to parts
which are =0 (mod 5) and create (m2- 51' - 2- Sto) new parts of 5 each,
j<-j + 1.
  Case II: to+js0 and m2=0.
  Case II(a): m3+5j-3>m0. Add 5j-3 to m3 (and sort); je-j-1.
  Case II(b): m3+5j-3<mo. Subtract 5j+2 from m0 (and sort); j<-j+1.
```
[OCR: the four `>`/`<` comparison signs come out as `>` and `<` but with the
overbar lost; the printed comparisons are `>=` in I(a) and II(a) and `<` in
I(b) and II(b) -- otherwise the case split would not be exhaustive. The two
equality placements are the "tie-breaks"; see `negative_control.py` PSI-1,
PSI-2 for the measured cost of getting them wrong.]

## p. 315 -- the three examples

```
Examples
  (1) <p(2; 11, 9, 8, 7, 6, 1, 1, 1): (3'; 10, 9, 7, 2, 2, 2). Here a =4, 41.
      = 1, Case I applies.
  (2) ¢(-2; 15, 14, 9, 9, 8, 8, 8, 5, 5,4, 3, 2, 1) = (-3; 14, 10, 9, 9, 8,
      8, 8,4, 3, 2, 2,1). Here to = 3, m2=2, Case 1(a) applies.
  (3) 7T ((4, 1)) = (3, 2) since
           (0;4,1)1>(1;1,1,1)1>(0;2,1,1,1)1>(-1;1,1)i>
           (m3,1,1)£>(1;2,1)i>(0;2,2,1)1>(1;3)i>(0;3,2).
```
[OCR: `(3';...)` = `(3; ...)`; `41.` = `mu`; `(m3,1,1)` = `(0;3,1,1)` -- the
initial character is a garbled `0`, and `3` is the first part. The `1>`/`i>`/
`£>` glyphs are the arrow between successive states.]
