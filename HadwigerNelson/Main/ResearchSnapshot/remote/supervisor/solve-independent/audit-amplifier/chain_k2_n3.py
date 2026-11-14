"""Exact audit of the amplifier at k = 2 with the chaining actually exercised (n = 3).
Field Q(sqrt5, sqrt7), basis (1, s5, s7, s35), Fraction coefficients.  Arithmetic verification of
distance claims only: no search, no solver.
Gadget: G = path p - r - q with p=(0,0), q=(1/4,0), r=(1/8, h), h = 3*sqrt7/8 = sqrt63/8.
  |p-q| = 1/4 (not 1), |p-r| = |q-r| = 1, so G is a unit-distance graph, bipartite, and p,q lie in the
  same part, so EVERY proper 2-colouring has c(p) = c(q)  -- (H2) at k = 2.
d = 1/4, so n* = min{n : n d > 1/2} = 3 and D = 3/4."""
from fractions import Fraction as F

class F45:                     # a + b*sqrt5 + c*sqrt7 + e*sqrt35
    __slots__=('a','b','c','e')
    def __init__(s,a=0,b=0,c=0,e=0): s.a,s.b,s.c,s.e=F(a),F(b),F(c),F(e)
    def __add__(s,o): return F45(s.a+o.a,s.b+o.b,s.c+o.c,s.e+o.e)
    def __neg__(s): return F45(-s.a,-s.b,-s.c,-s.e)
    def __sub__(s,o): return s+(-o)
    def __mul__(s,o):
        # (a+b s5+c s7+e s35)(a'+b' s5+c' s7+e' s35);  s5^2=5, s7^2=7, s5 s7 = s35
        A=s.a*o.a + 5*s.b*o.b + 7*s.c*o.c + 35*s.e*o.e
        B=s.a*o.b + s.b*o.a + 7*s.c*o.e + 7*s.e*o.c
        C=s.a*o.c + 5*s.b*o.e + s.c*o.a + 5*s.e*o.b
        E=s.a*o.e + s.b*o.c + s.c*o.b + s.e*o.a
        return F45(A,B,C,E)
    def __eq__(s,o): return (s.a,s.b,s.c,s.e)==(o.a,o.b,o.c,o.e)
    def __repr__(s): return f"[{s.a} {s.b}s5 {s.c}s7 {s.e}s35]"
def n(x): return F45(x)
def s5(): return F45(0,1)
def s7(): return F45(0,0,1)
Z=(n(0),n(0))
def pt(a,b,c=0,e=0): return (F45(a,b,c,e), F45(0))
def V(x,y): return (x,y)

h = F45(0,0,F(3,8))                    # 3*sqrt7/8
p = [ (F45(F(i,4)), F45(0)) for i in range(4) ]          # p_0..p_3 along x-axis
r = [ (F45(F(i,4)+F(1,8)), h) for i in range(3) ]        # r_0..r_2
print("chain C_3 points:", 4+3, "= nV-(n-1) with V=3, n=3:", 3*3-2)
def d2(u,v):
    dx=u[0]-v[0]; dy=u[1]-v[1]
    return dx*dx + dy*dy
C = p + r
print("\n--- unit distances inside the chain (exact) ---")
E=[]
for i in range(len(C)):
    for j in range(i+1,len(C)):
        if d2(C[i],C[j])==n(1): E.append((i,j))
names = [f"p{k}" for k in range(4)] + [f"r{k}" for k in range(3)]
print("edges:", [(names[a],names[b]) for a,b in E], " count:", len(E), " ( nE = 3*2 = 6 )")
acc = [ (a,b) for (a,b) in E if not ((names[a][0]==names[b][0])) ]
print("accidental cross-copy unit edges (MISSING accident class in AMPLIFIER.md 5):",
      [(names[a],names[b]) for a,b in acc])
# bipartition: p's in A, r's in B
A={i for i in range(4)}; B={4,5,6}
ok = all((a in A) != (b in A) for a,b in E)
print("bipartition p's / r's proper?", ok)
print("ends p_0 and q_2 = p_3 at distance", d2(p[0],p[3]), "= (3/4)^2 :", d2(p[0],p[3])==n(F(9,16)))
print("=> in every proper 2-colouring c(p_0)=c(p_3); but r_0 has the OTHER colour, so")
print("   AMPLIFIER.md Lemma 1 'all points of the chain have the same colour' is FALSE here.")

# --- rotation: cos = 1 - 1/(2D^2) = 1 - 1/(2*9/16) = 1/9 ; sin = 4 sqrt5 / 9
D=F(3,4); cs = 1 - F(1,2)/ (D*D)
sn = F45(0, F(4,9))                     # 4 sqrt5 / 9
print(f"\ncos theta = {cs} (= 1/9 : {cs==F(1,9)}), sin theta = 4 sqrt5/9")
print("check cos^2+sin^2 = 1:", n(cs)*n(cs) + sn*sn == n(1))
def rot(v):
    x,y=v
    return ( n(cs)*x - sn*y, sn*x + n(cs)*y )
X = C + [rot(v) for v in C[1:]]          # share the point p_0 = 0
print("\n|X| =", len(X), " (points, all distinct check next)")
distinct = all(not (X[i][0]==X[j][0] and X[i][1]==X[j][1]) for i in range(len(X)) for j in range(i+1,len(X)))
print("all points distinct:", distinct)
far1 = p[3]; far2 = rot(p[3])
print("far ends:", far1, far2)
print("|far1 - far2|^2 =", d2(far1,far2), " equals 1?", d2(far1,far2)==n(1))
EX=[]
for i in range(len(X)):
    for j in range(i+1,len(X)):
        if d2(X[i],X[j])==n(1): EX.append((i,j))
print("\n|E(X)| =", len(EX), " (bound 2nE+1 = 13)")
print("=> X is not 2-colourable: c(p_0)=c(far1)=c(far2) by the chain argument, but |far1-far2| = 1.")
