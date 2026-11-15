"""Finite exact consistency checks for the local-arithmetic exposition.

These supplement the proofs; they are not certificates for every n.
Uses the Python standard library only. All arithmetic is rational.
"""
from fractions import Fraction as F
from math import comb, factorial, prod
import json
from pathlib import Path

def vp(x, p):
    x = F(x)
    if not x:
        return 10**9
    a, b = abs(x.numerator), x.denominator
    v = 0
    while a % p == 0:
        a //= p
        v += 1
    while b % p == 0:
        b //= p
        v -= 1
    return v

def bernoulli(n):
    b = [F(1)]
    for m in range(1, n+1):
        b.append(-sum(F(comb(m+1,k))*b[k] for k in range(m))/F(m+1))
    return b

B = bernoulli(100)

def harmonic(j):
    return sum((F(1, k**5) for k in range(1,j+1)), F(0))

def phi(j):
    return (F(j**4), -F(j**4)*harmonic(j)-F(1,4)+F(1,2*j))

def mu(e):
    return (-1)**e * B[2*e+2] * F((2*e+3)*(2*e+4)*(2*e+5),24)

def binomial(x, k):
    return F(prod(x-i for i in range(k)), factorial(k))

def mul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j]+=x*y
    return out

def roots(zz):
    out=[F(1)]
    for z in zz:
        out=mul(out,[-F(z),F(1)])
    return out

def evaluate(a,x):
    out=F(0)
    for c in reversed(a):
        out=out*x+c
    return out

def divmonic(a,b):
    a=a[:]
    if len(a)<len(b):
        return [F(0)], a
    q=[F(0)]*(len(a)-len(b)+1)
    for i in range(len(q)-1,-1,-1):
        c=a[i+len(b)-1]
        q[i]=c
        for j,d in enumerate(b):
            a[i+j]-=c*d
    return q,a[:len(b)-1]

def tau(poly):
    return sum((F(j*(j-1)*(j-2),24)*poly[j]*B[j-3]
                for j in range(3,len(poly))),F(0))

counts={}
for i in range(1,9):
    for z in range(-10,11):
        q = F((-1)**i*2*(-z*z)*prod(j*j-z*z for j in range(1,i)),factorial(2*i))
        assert q==binomial(z+i,2*i)+binomial(z+i-1,2*i)
counts["integer_basis_cases"]=8*21

pc=mc=0
for p in [5,7,11,13,17,19,23]:
    for a in range(1,p):
        f,g=phi(a),phi(p-a)
        assert all(vp(g[i]-f[i],p)>=1 for i in range(2))
        pc+=1
    for e in range(2*p-3):
        assert vp(mu(e),p)>=0
        mc+=1
counts["pole_congruences"]=pc
counts["low_moments"]=mc

dc=0
for p,pp in [(5,[-7,-2,1,6]),(7,[-8,-1,3,10]),(11,[-12,-1,3,14])]:
    for mult in [2,3,4]:
        zz=list(range(p))*mult
        aa=roots(zz)
        den=roots(pp)
        pol,_=divmonic(aa,den)
        if len(pol)>=p*p:
            continue
        beta=min(sum(z%p==c for z in zz)-sum(r%p==c for r in pp) for c in range(p))
        lin=F(0)
        con=tau(pol)
        for r in pp:
            residue=evaluate(aa,F(r))/prod(F(r-s) for s in pp if s!=r)
            d=r if r>=0 else -r-1
            con+=residue*harmonic(d)
            lin-=residue
        assert min(vp(lin,p),vp(con,p))>=beta-4
        dc+=1
counts["direct_class_bound_cases"]=dc

def sx(H,c,p):
    return sum(j%p==c for j in range(1,H+1))+sum(j%p==(-c)%p for j in range(1,H+1))

ic=0
for n in [1,2,3,5,10]:
    K,N,h=40*n,3*n,37*n
    for p in [5,7,11,13,17,19,23,29,31,37,41,43]:
        if not p<=K/3:
            continue
        m=(p-1)//2
        q=K//p
        reserve=3*q+6
        if reserve>h:
            continue
        beta=[6*sx(N,c,p)-sx(K,c,p)-4 for c in range(m+1)]
        lo,hi=-2*q-6,8*q+20
        lrow=lambda k,b:max(0,(k-b+1)//2)
        kstar=max(k for k in range(lo,hi+1) if sum(lrow(k,b) for b in beta[1:])<=h-reserve)
        L=[0]+[lrow(kstar,b) for b in beta[1:]]
        L[0]=h-sum(L)
        T=min(F(L[c])+F(beta[c],2) for c in range(1,m+1))
        assert T<=2*L[0]+F(beta[0]+5,2)
        ww=[(c,i,min(F(i)+F(beta[c],2),T) if c else min(2*i+F(beta[0]+5,2),T))
            for c in range(m+1) for i in range(L[c])]
        assert len(ww)==h
        for c,i,w in ww:
            for a in range(m+1):
                nu=i if c==a else L[a]
                rhs=nu+F(beta[a],2) if a else 2*nu+F(beta[0]+5,2)
                assert w<=rhs
        ic+=1
counts["inner_allocations_and_all_row_class_inequalities"]=ic
counts["status"]="PASS; finite consistency checks only"
destination=Path(__file__).with_name("local_checks.json")
destination.write_text(json.dumps(counts,indent=2)+"\n",encoding="utf-8")
print(json.dumps(counts,indent=2))
