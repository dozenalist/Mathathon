"""Rational interval witness against the original measure for D_N^8.

No floating-point arithmetic enters the certificate. Logs use the atanh
series after range reduction; atan uses a half-angle reduction and an
alternating series; pi uses Machin's formula; sqrt uses integer isqrt.
The result is a lower bound on a single-point value, hence on the
best possible potential upper constant for this particular measure.
It is NOT an upper bound on a supremum or an exclusion of other measures.
"""
from fractions import Fraction as F
from math import isqrt
import json
from pathlib import Path

# Appendix A, Table 1 of Fauzan's source; entries are scaled by 10^12.
ROWS = [
 (3906748086,8992695531,10515596180),
 (2312248264,15340997855,29471737793),
 (1402286665,25730180724,42934365099),
 (881725356,41909578246,58204231966),
 (578197906,65851089563,69037621310),
 (396324613,99481037884,78873099189),
 (283911191,144325727458,84856120711),
 (212206188,201105762729,88396082127),
 (165097686,269345996903,88303382125),
 (133347132,347089554156,85472321255),
 (111522114,430806704415,78899184238),
 (96349355,515561896511,70353471918),
 (85815639,595448778546,58838976615),
 (78667711,664241383483,44421321106),
 (74129565,716160577112,30462865791),
 (71741310,746637295669,5959622577),
]
assert sum(c for a,b,c in ROWS)==925000000000
assert all(0<a<b and c>0 for a,b,c in ROWS)
assert all(a_next<a and b<b_next for (a,b,c),(a_next,b_next,c_next) in zip(ROWS,ROWS[1:]))

SCALE=10**18

def down(x):return F((x.numerator*SCALE)//x.denominator,SCALE)
def up(x):return -down(-x)

class I:
    def __init__(self,lo,hi=None):
        self.lo=down(F(lo));self.hi=up(F(lo if hi is None else hi))
        assert self.lo<=self.hi
    def __add__(self,o):
        o=asI(o);return I(self.lo+o.lo,self.hi+o.hi)
    __radd__=__add__
    def __neg__(self):return I(-self.hi,-self.lo)
    def __sub__(self,o):return self+-asI(o)
    def __rsub__(self,o):return asI(o)+-self
    def __mul__(self,o):
        o=asI(o);v=[self.lo*o.lo,self.lo*o.hi,self.hi*o.lo,self.hi*o.hi];return I(min(v),max(v))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=asI(o);assert not o.lo<=0<=o.hi
        return self*I(1/o.hi,1/o.lo)
    def __rtruediv__(self,o):return asI(o)/self
    def sqrt(self):
        assert self.lo>=0
        a=isqrt((self.lo.numerator*SCALE*SCALE)//self.lo.denominator)
        b=isqrt((self.hi.numerator*SCALE*SCALE)//self.hi.denominator)
        return I(F(a,SCALE),F(b+1,SCALE))
    def log(self):
        assert self.lo>0
        return I(logq(self.lo).lo,logq(self.hi).hi)
    def atan(self):
        assert self.lo>=0
        # atan(x)=2 atan(x/(1+sqrt(1+x^2))). On our inputs reduced x<1/2.
        z=self/(1+(1+self*self).sqrt())
        assert z.hi<F(1,2)
        return 2*I(atanq(z.lo).lo,atanq(z.hi).hi)
    def encode(self):
        return {'lower_exact':str(self.lo),'upper_exact':str(self.hi),
                'lower_decimal':float(self.lo),'upper_decimal':float(self.hi)}

def asI(x):return x if isinstance(x,I) else I(x)

def log_series(x):
    assert 1<=x<=2
    z=(x-1)/(x+1)
    z2=z*z
    power=z
    out=F(0)
    N=30
    for k in range(N):
        out+=power/F(2*k+1)
        power*=z2
    remainder=2*power/F(2*N+1)/(1-z2)
    return I(2*out,2*out+remainder)

LOG2=log_series(F(2))

def logq(x):
    k=0
    while x<1:x*=2;k-=1
    while x>=2:x/=2;k+=1
    return k*LOG2+log_series(x)

def atanq(x):
    assert 0<=x<=F(1,2)
    out=F(0);power=x;x2=x*x;N=40
    for k in range(N):
        out+=(-1 if k%2 else 1)*power/F(2*k+1)
        power*=x2
    nextterm=power/F(2*N+1)
    return I(out,out+nextterm)  # N even: final included term is negative.

PI=16*atanq(F(1,5))-4*atanq(F(1,239))

def J(t,b):
    y=t.sqrt()
    return b*(t+b*b).log()-2*b+2*y*(b/y).atan()

def main():
    t=I(F(3,4));a=I(F(3,40));lam=I(F(37,40))
    pot=I(0);energy=I(0);cumulative=I(0)
    for ai,bi,ci in ROWS:
        aa,bb,c=I(F(ai,10**12)),I(F(bi,10**12)),I(F(ci,10**12))
        # t=3/4 lies strictly to the right of every interval in Table 1.
        assert t.lo>bb.hi
        pot+=c*((t-(aa+bb)/2+((t-aa)*(t-bb)).sqrt())/2).log()
        energy+=((cumulative+c)*(cumulative+c)-cumulative*cumulative)*((bb-aa)/4).log()
        cumulative+=c
    field=2*PI*t.sqrt()+J(t,I(1))-8*J(t,a)
    phi=2*pot-field
    C=-2*lam+16*a*lam*(1-a.log())+3*lam*lam-2*lam*lam*(2*lam).log()
    real_floor=lam*phi-energy+C
    raw=json.loads((Path(__file__).parents[1]/'arithmetic_variant_results.json').read_text())
    arithmetic=I(F(raw[0]['normalization_coefficient_exact']))
    budget_floor=arithmetic+real_floor
    assert budget_floor.lo>F(13,10)
    result={'t':'3/4','pi_interval':PI.encode(),'potential_value_phi8':phi.encode(),
            'real_certificate_coefficient_lower_witness':real_floor.encode(),
            'arithmetic_coefficient':arithmetic.encode(),
            'combined_certificate_lower_witness':budget_floor.encode(),
            'proved':'For the original measure and the D_N^8 arithmetic certificate at M=200, any valid potential upper constant yields total coefficient >13/10. Other measures and arithmetic estimates are not excluded.',
            'method':'Rational interval arithmetic; every endpoint rounded outward to 10^-18; rigorous series remainders.'}
    Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
