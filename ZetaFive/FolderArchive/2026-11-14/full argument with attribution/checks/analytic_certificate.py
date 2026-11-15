"""Exact interval verification of Fauzan's analytic certificate.

Mathematical data: Fauzan (2026), Appendix A, Tables 1--2.
The data file transcribes scripts/lemma61.py in Moritz Firsching's Zeta5
repository, revision 7fe736760f4b96bfdb4334b68e3b3124ecbe10b0 (Apache-2.0).
That script's numerical sampling is NOT used here. This implementation
uses only integer arithmetic, rational input and outward-rounded dyadic
intervals. All transcendental bounds come from explicitly bounded series.

Run: python analytic_certificate.py
Requires Python 3.10+ standard library only.
Outputs analytic_certificate.json and analytic_intervals.csv beside this file.
"""
from fractions import Fraction as F
from math import isqrt
from functools import lru_cache
from pathlib import Path
import csv
import hashlib
import json

BITS = 112
S = 1 << BITS
LOG_TERMS = 48
ATAN_TERMS = 64  # even; partial sum is a lower bound

def ceildiv(a, b):
    return -((-a) // b)

class I:
    """Closed interval [lo/S,hi/S]; each operation encloses exact arithmetic."""
    __slots__ = ("lo", "hi")
    def __init__(self, lo, hi=None):
        self.lo, self.hi = int(lo), int(lo if hi is None else hi)
        assert self.lo <= self.hi
    @staticmethod
    def q(x):
        x = F(x)
        return I(x.numerator*S//x.denominator,
                 ceildiv(x.numerator*S,x.denominator))
    def __add__(self, other):
        other = cv(other)
        return I(self.lo+other.lo,self.hi+other.hi)
    __radd__ = __add__
    def __neg__(self):
        return I(-self.hi,-self.lo)
    def __sub__(self, other):
        return self + (-cv(other))
    def __rsub__(self, other):
        return cv(other) + (-self)
    def __mul__(self, other):
        other=cv(other)
        vals=[a*b for a in (self.lo,self.hi) for b in (other.lo,other.hi)]
        return I(min(vals)//S,ceildiv(max(vals),S))
    __rmul__=__mul__
    def inv(self):
        assert not self.lo <= 0 <= self.hi
        return I(S*S//self.hi,ceildiv(S*S,self.lo))
    def __truediv__(self, other):
        return self*cv(other).inv()
    def __rtruediv__(self, other):
        return cv(other)*self.inv()
    def __pow__(self,n):
        assert n >= 0
        ans=I.q(1)
        for _ in range(n): ans=ans*self
        return ans
    def sqrt(self):
        assert self.lo >= 0
        l=isqrt(self.lo*S)
        u=isqrt(self.hi*S)
        if u*u < self.hi*S: u+=1
        return I(l,u)
    def bounds(self):
        return [str(F(self.lo,S)),str(F(self.hi,S))]
    def decimal_bounds(self,places=18):
        d=10**places
        l=self.lo*d//S; u=ceildiv(self.hi*d,S)
        def fmt(v):
            sign="-" if v<0 else ""
            v=abs(v)
            return f"{sign}{v//d}.{v%d:0{places}d}"
        return [fmt(l),fmt(u)]

def cv(x): return x if isinstance(x,I) else I.q(x)

def log_core(r):
    # 1 <= r <= 2; allow the tiny rounding enclosure at endpoints.
    z=(r-1)/(r+1); z2=z*z
    assert z.lo>=0 and z.hi<S
    p=z; ans=I.q(0)
    for j in range(LOG_TERMS):
        ans=ans+2*p/(2*j+1)
        p=p*z2
    tail=2*p/((2*LOG_TERMS+1)*(1-z2))
    return I(ans.lo,ans.hi+tail.hi)

LN2=log_core(I.q(2))

@lru_cache(maxsize=None)
def log_point(n):
    assert n>0
    x=F(n,S)
    e=x.numerator.bit_length()-x.denominator.bit_length()
    r=x/(F(2)**e)
    if r<1: e-=1; r*=2
    if r>=2: e+=1; r/=2
    assert 1<=r<2
    return log_core(I.q(r))+e*LN2

def log(x):
    x=cv(x); assert x.lo>0
    return I(log_point(x.lo).lo,log_point(x.hi).hi)

def atan_small(x):
    assert 0<=x.lo and x.hi<=S//2+1
    p=x; x2=x*x; ans=I.q(0)
    for j in range(ATAN_TERMS):
        term=p/(2*j+1)
        ans=ans+term if j%2==0 else ans-term
        p=p*x2
    remainder=p/(2*ATAN_TERMS+1)
    return I(ans.lo,ans.hi+remainder.hi)

PI=16*atan_small(I.q(F(1,5)))-4*atan_small(I.q(F(1,239)))

def atan(x):
    x=cv(x); assert x.lo>=0
    if x.hi<=S//2:
        return atan_small(x)
    if x.lo>S:
        return PI/2-atan(1/x)
    if x.hi<=S:
        return 2*atan(x/(1+(1+x*x).sqrt()))
    return I(atan(I(x.lo)).lo,atan(I(x.hi)).hi)

HERE=Path(__file__).resolve().parent
DATA=json.loads((HERE/"analytic_data.json").read_text(encoding="utf-8"))
T=[tuple(F(v,10**12) for v in row) for row in DATA["T"]]
AL=F(3,40); LAM=F(37,40); M0=F(-1329,200)
QM=F(59205077,10**10); QP=F(59205079,10**10)
U=F(-2733991,2000000)

@lru_cache(maxsize=None)
def potential(t):
    ans=I.q(0)
    for a,b,c in T:
        if a<=t<=b:
            z=I.q((b-a)/4)
        else:
            z=(I.q(abs(t-(a+b)/2))+I.q((t-a)*(t-b)).sqrt())/2
        ans=ans+c*log(z)
    return ans

@lru_cache(maxsize=None)
def field(t):
    if t==0: return -12*AL*log(AL)-2+12*AL
    y=I.q(t).sqrt()
    return log(1+t)-6*AL*log(t+AL*AL)-2+12*AL+2*y*(PI+atan(1/y)-6*atan(AL/y))

def phi_derivative(t):
    y=I.q(t).sqrt()
    return 2*(PI+atan(1/y)-6*atan(AL/y))

def parse_indices(s):
    for p in s.replace(";",",").split(","):
        if "-" in p:
            a,b=map(int,p.split("-"))
            yield from range(a,b+1)
        else:
            yield int(p)

def main():
    assert sum(c for a,b,c in T)==LAM
    assert all(b-a>F(1,225) for a,b,c in T)
    assert all(T[j+1][0]<T[j][0]<T[j][1]<T[j+1][1] for j in range(15))
    assert T[-1][0]>0 and T[-1][1]<2
    assert T[0][0]<QM<QP<T[0][1]
    dm,dp=phi_derivative(QM),phi_derivative(QP)
    assert dm.hi<0<dp.lo
    bracket=PI+atan(1/I.q(QP).sqrt())-6*atan(AL/I.q(QM).sqrt())
    assert bracket.hi<0
    vstar=log(1+QM)-6*AL*log(QP+AL*AL)-2+12*AL+2*I.q(QP).sqrt()*bracket
    pts=[F(0)]+[row[0] for row in reversed(T)]+[QM,QP]+[row[1] for row in T]+[F(2)]
    intervals=[]
    for row in DATA["rows"].splitlines():
        j,d,ktext=row.split(" ",2); j=int(j); d=int(d)
        for k in parse_indices(ktext):
            a,b=pts[j],pts[j+1]
            intervals.append((a+(b-a)*F(k,2**d),a+(b-a)*F(k+1,2**d),j,d,k))
    intervals.sort()
    assert len(intervals)==684
    assert all(l<r for l,r,j,d,k in intervals)
    assert intervals[0][0]==0 and intervals[-1][1]==2
    assert all(intervals[j][1]==intervals[j+1][0] for j in range(len(intervals)-1))
    rows=[]; worst=None
    for l,r,j,d,k in intervals:
        vl=field(r) if r<=QM else field(l) if l>=QP else vstar
        pl,pr=potential(l),potential(r)
        bound=I(2*max(pl.lo,pr.lo)-vl.hi,2*max(pl.hi,pr.hi)-vl.lo)
        assert F(bound.hi,S)<F(-6645002,10**6),(j,d,k,bound.decimal_bounds())
        if worst is None or bound.hi>worst[0].hi: worst=(bound,j,d,k)
        rows.append((j,d,k,str(l),str(r),*bound.bounds(),*bound.decimal_bounds()))
    accum=F(0); energy=I.q(0)
    for a,b,c in T:
        nxt=accum+c
        energy=energy+(nxt*nxt-accum*accum)*log((b-a)/4)
        accum=nxt
    cstar=-2*LAM+12*AL*LAM*(1-log(AL))+3*LAM*LAM-2*LAM*LAM*log(2*LAM)
    coefficient=LAM*M0-energy+cstar
    assert F(coefficient.hi,S)<U
    # Check the weakened field tail at t=2 (K>=2 gives 1/K<=1/2).
    tail=F(13,10)*log(2)+3*AL**3-(2*PI-F(1,2))*I.q(2).sqrt()
    assert F(tail.hi,S)<M0
    report={
        "status":"PASS: all comparisons performed with exact integer arithmetic",
        "bits":BITS,"log_terms":LOG_TERMS,"atan_terms":ATAN_TERMS,
        "data_source":DATA["source"],"source_revision":DATA["revision"],
        "data_sha256":hashlib.sha256((HERE/"analytic_data.json").read_bytes()).hexdigest(),
        "script_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "partition_intervals":len(intervals),
        "partition_exactly_covers":"[0,2]",
        "worst_interval_j_d_k":list(worst[1:]),
        "maximum_endpoint_bound_decimal_enclosure":worst[0].decimal_bounds(),
        "maximum_endpoint_bound_exact_enclosure":worst[0].bounds(),
        "target_potential_bound":"-6645002/1000000 < -1329/200",
        "phi_derivative_q_minus":dm.decimal_bounds(),
        "phi_derivative_q_plus":dp.decimal_bounds(),
        "V_star":vstar.decimal_bounds(),
        "energy":energy.decimal_bounds(),
        "C_star":cstar.decimal_bounds(),
        "quadratic_coefficient":coefficient.decimal_bounds(),
        "quadratic_coefficient_exact":coefficient.bounds(),
        "target_U":str(U),
        "tail_at_2_with_half_sqrt":tail.decimal_bounds(),
        "pi":PI.decimal_bounds(),
    }
    (HERE/"analytic_certificate.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    with (HERE/"analytic_intervals.csv").open("w",encoding="utf-8",newline="") as f:
        wr=csv.writer(f)
        wr.writerow(["j","d","k","left","right","bound_lower_exact","bound_upper_exact","bound_lower_decimal","bound_upper_decimal"])
        wr.writerows(rows)
    print(json.dumps(report,indent=2))

if __name__=="__main__":
    main()
