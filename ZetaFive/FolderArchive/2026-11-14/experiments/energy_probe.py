"""Exploratory floating-point comparison; this is NOT an interval certificate.

Uses the 16 arcsine components in Fauzan (2026), Appendix A, Table 1.
The q=6 case checks the original field; q=8 tests an additional numerator
factor D_N^2 while retaining alpha and the old comparison measure.
"""
import json
import math
from pathlib import Path
import numpy as np

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
alpha=3/40
lam=37/40
assert sum(c for a,b,c in ROWS)==925000000000

def J(t,b):
    if t==0:
        return 2*b*(math.log(b)-1)
    y=math.sqrt(t)
    return b*math.log(t+b*b)-2*b+2*y*math.atan(b/y)

def potential(t):
    result=0
    for ai,bi,ci in ROWS:
        a,b,c=ai/1e12,bi/1e12,ci/1e12
        if a<=t<=b:
            v=math.log((b-a)/4)
        else:
            v=math.log((abs(t-(a+b)/2)+math.sqrt((t-a)*(t-b)))/2)
        result+=c*v
    return result

def field(t,q):
    return 2*math.pi*math.sqrt(t)+J(t,1)-q*J(t,alpha)

def phi(t,q):
    return 2*potential(t)-field(t,q)

def golden_max(f,a,b):
    # Used only after a mesh has located a putative local maximum.
    r=(math.sqrt(5)-1)/2
    x=b-r*(b-a);y=a+r*(b-a)
    for _ in range(100):
        if f(x)>f(y):
            b=y;y=x;x=b-r*(b-a)
        else:
            a=x;x=y;y=a+r*(b-a)
    t=(a+b)/2
    return f(t),t

def main():
    energy=0; cumulative=0
    for ai,bi,ci in ROWS:
        c=ci/1e12
        energy+=((cumulative+c)**2-cumulative**2)*math.log((bi-ai)/4e12)
        cumulative+=c
    mesh=sorted(set([0.0,*np.geomspace(1e-12,100,30000),
                     *[a/1e12 for a,b,c in ROWS],
                     *[b/1e12 for a,b,c in ROWS]]))
    results={}
    for q in [6,8]:
        values=[phi(t,q) for t in mesh]
        candidates=[(v,t) for t,v in zip(mesh,values)]
        for i in range(1,len(mesh)-1):
            if values[i]>=values[i-1] and values[i]>=values[i+1]:
                candidates.append(golden_max(lambda t:phi(t,q),mesh[i-1],mesh[i+1]))
        max_value,t=max(candidates)
        C=-2*lam+2*q*alpha*lam*(1-math.log(alpha))+3*lam**2-2*lam**2*math.log(2*lam)
        results[str(q)]={"sampled_supremum":max_value,"location":t,
                         "C":C,"energy":energy,
                         "candidate_real_exponent":lam*max_value-energy+C}
    results['status']='Exploratory double precision; no interval proof and no global optimization claim.'
    Path(__file__).with_suffix('.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()
