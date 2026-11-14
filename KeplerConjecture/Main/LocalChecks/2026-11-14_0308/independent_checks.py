"""Independent exact checks of the frozen 03:08 sources; no solver required."""
import importlib.util, json, sys
from pathlib import Path
import sympy as sp

root=Path(sys.argv[1]); s,v,u=sp.symbols('s v u'); R=sp.Rational
def transform(P,src,dst):
    poly=sp.Poly(P,src); result=sp.Integer(0); basis=sp.Integer(1)
    for k in range(poly.degree()+1):
        result+=poly.nth(k)*basis
        basis=sp.expand(-dst*sp.diff(basis,dst,2)+(2*dst-R(3,2))*sp.diff(basis,dst)+(R(3,2)-dst)*basis)
    return sp.Poly(sp.expand(result),dst)
def atan_bounds(inv,n):
    x=R(1,inv); a=sum((-1)**k*x**(2*k+1)/(2*k+1) for k in range(n))
    b=a+(-1)**n*x**(2*n+1)/(2*n+1)
    return min(a,b),max(a,b)
al,ah=atan_bounds(5,50); bl,bh=atan_bounds(239,15)
pi_lo,pi_hi=16*al-4*bh,16*ah-4*bl

d=json.loads((root/'Counterexamples/X_C014_certificate.json').read_text())
# Stored factors are already expanded in s, descending coefficient order.
# S=8 records the optimizer's basis scaling; applying it again would be wrong.
qs=[sum(R(c)*s**(len(row)-1-i) for i,c in enumerate(row)) for row in d['q']]
P=sp.Poly(sp.expand(-(s-4)*sum(q*q for q in qs)),s)
Q=transform(P.as_expr(),s,v)
assert P.eval(0)>0 and Q.eval(0)>0
roots=Q.count_roots(0,sp.oo); assert roots==0
ratio=P.eval(0)/Q.eval(0); bound=R(780718153344,10**12)
assert 16*ratio**2 < 9*pi_lo*bound**2
print('X-C014: SOS spatial sign; independent Fourier recurrence; zero nonnegative Q roots: PASS')
print('P0 =',P.eval(0)); print('Q0 =',Q.eval(0)); print('exact ratio =',ratio)
print('Machin rational comparison proves density < 0.780718153344')

# Reconstruct C's displayed identities without importing its verifier/transform.
ps=[R(4,3),-R(37,3),R(101,12)*u+R(1,4),-R(13,6)]
p=sp.expand(-(u-12)*sum(z*z for z in ps))
positive=R(73964663853612149,39608831771148288)
q=sp.expand((22*u-R(7250725477,114904064))**2+positive+u*(R(101,12)*u-R(36667,1616))**2)
assert positive>0 and pi_lo>3
q_fourier=transform(p,u,u).as_expr()
assert sp.expand(q_fourier-q)==0
r=sp.cancel(p.subs(u,0)/q.subs(u,0)); assert r==R(731040,1529773)
assert 4*pi_hi*r/3 < R(20017173734,10**10)
print('C both-sides identities and independently reconstructed Fourier pair: PASS')
print('ratio =',r,'; density < 2.0017173734 (weaker than density <= 1)')

spec=importlib.util.spec_from_file_location('main_checker',root/'Computation/shell_check.py')
M=importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
def cs(expr): return list(reversed(sp.Poly(expr,u).all_coeffs()))
narrow=(u-R(7,5))**2-R(2,10**40)
checks=[('narrow nonnegative',lambda:M.nonneg_on_half_line(cs(narrow)),False),
        ('narrow negation ray',lambda:M._ray(cs(-narrow),0),False),
        ('narrow negation bounded',lambda:M.le_on_interval(cs(-narrow),0,0,3),False),
        ('old endpoint interval',lambda:M.le_on_interval([0,1,-1],0,0,1),False),
        ('square zero probes',lambda:M.le_on_interval(cs((u*(u-R(1,2))*(u-1))**2),0,0,1),False),
        ('zero half-line',lambda:M.nonneg_on_half_line([0]),True),
        ('nonnegative square',lambda:M.nonneg_on_half_line(cs((u-R(1,3))**2)),True),
        ('positive constant',lambda:M.nonneg_on_half_line([1]),True),
        ('negative constant',lambda:M.nonneg_on_half_line([-1]),False)]
for name,fn,want in checks:
    got=fn(); print('Main control:',name,got,'expected',want); assert got==want
print('Named Main controls pass; generic soundness remains a separate proof obligation.')
