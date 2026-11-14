"""Exact review of frozen checker repairs and X's rational SOS certificate."""
import importlib.util
import json
from pathlib import Path
import sys
import sympy as sp

root=Path(sys.argv[1])
spec=importlib.util.spec_from_file_location('main_checker',root/'Computation/shell_check.py')
M=importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
u=sp.Symbol('u')
def cs(p): return list(reversed(sp.Poly(p,u).all_coeffs()))
cases=[
 ('old interval',lambda:M.le_on_interval([0,1,-1],0,0,1)),
 ('old nonnegative ray',lambda:M.nonneg_on_half_line([0,-1,1])),
 ('old nonpositive ray',lambda:M._ray([0,1,-1],0)),
 ('square interval',lambda:M.le_on_interval(cs((u*(u-sp.Rational(1,2))*(u-1))**2),0,0,1)),
 ('negative square ray',lambda:M.nonneg_on_half_line(cs(-(u*(u-1)*(u-sp.Rational(1,2))*(u-2))**2))),
 ('positive square ray',lambda:M._ray(cs((u*(u-1)*(u-2))**2),0)),
]
for name, fn in cases:
    ans=fn(); print(name,'accepted=',ans); assert ans==False

# A negative interval between two extremely close irrational roots. Their
# rational isolating intervals may share a boundary, leaving no tested gap.
centre=sp.Rational(7,5)
q=(u-centre)**2-sp.Rational(2,10**40)
print('NARROW POCKET polynomial:',q)
print('exact negative witness q(7/5)=',q.subs(u,centre))
print('isolating intervals:',sp.Poly(q,u).intervals(eps=sp.Rational(1,10**8)))
print('checker test points:',M._roots_and_gaps(q,0,sp.oo))
print('narrow pocket nonnegative accepted=',M.nonneg_on_half_line(cs(q)))
print('narrow pocket nonpositive negation accepted=',M._ray(cs(-q),0))
print('narrow pocket bounded negation accepted=',M.le_on_interval(cs(-q),0,0,3))

# Independently reconstruct the width-one Gaussian transform. If
# F(s)=s^k exp(-s), its Fourier polynomial satisfies Q_{k+1}=T(Q_k),
# T(Q)=-v Q''+(2v-3/2)Q'+(3/2-v)Q. No worker transform/checker is imported.
data=json.loads((root/'Counterexamples/X_C013_certificate.json').read_text())
s,v=sp.symbols('s v')
factors=[sum(sp.Rational(c)*s**(len(row)-1-i) for i,c in enumerate(row)) for row in data['q']]
H=sp.expand(sum(f*f for f in factors))
P=sp.Poly(sp.expand(-(s-4)*H),s)
Q=sp.Integer(0); basis=sp.Integer(1)
for k in range(P.degree()+1):
    Q+=P.nth(k)*basis
    basis=sp.expand(-v*sp.diff(basis,v,2)+(2*v-sp.Rational(3,2))*sp.diff(basis,v)+(sp.Rational(3,2)-v)*basis)
Q=sp.Poly(sp.expand(Q),v)
assert P.eval(0)==sp.Rational(data['P0'])
assert Q.eval(0)==sp.Rational(data['Q0'])
assert P.eval(0)>0 and Q.eval(0)>0
roots=Q.count_roots(0,sp.oo)
assert roots==0
ratio=P.eval(0)/Q.eval(0)

def atan_bounds(inv,n):
    x=sp.Rational(1,inv)
    partial=sum((-1)**k*x**(2*k+1)/(2*k+1) for k in range(n))
    following=partial+(-1)**n*x**(2*n+1)/(2*n+1)
    return min(partial,following),max(partial,following)
a,b=atan_bounds(5,50),atan_bounds(239,15)
pi_lo=16*a[0]-4*b[1]
upper=sp.Rational(794809295672,10**12)
assert 16*ratio**2 < 9*pi_lo*upper**2
print('X-C013: exact SOS factors, independent Fourier recurrence and Q root count PASS')
print('Q roots on [0,infinity):',roots,'Q(0):',Q.eval(0))
print('P(0)/Q(0):',ratio)
print('Machin rational enclosure verifies density < 0.794809295672')
print('This is a weaker ordinary CE control, not a new best packing bound.')
