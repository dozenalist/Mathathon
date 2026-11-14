"""Numerical re-verification of the two constructions against the paper's Lemma 5.2(3) in its
own form:   z + f = x + s + t,  |s|=|t|=1,  s a local angular diffeomorphism  =>  P_z(f) cap P_x(s) = empty.
For a frozen field P this reads  P(f) cap P(s) = empty.  We sample (d, alpha, f, branch) directly,
compute s with complex arithmetic, and compare labels.  (Numerical check only; the decision is made
in THRESHOLD.md by the exact arguments of Lemma 1.1/2.2 and the certificate exact3.py.)"""
import math, random

# ---------- construction 1: m = 1, 18 sectors, word (0..5)^3, works for D <= D* -------------
def P18(theta):
    return math.floor(9*theta/math.pi) % 6

# ---------- construction 2: m = 2, double cover, works for D <= 2 sin(2 pi/9) - 1 -------------
def P2(theta):
    # three period-arcs of width 2pi/9 in [0,2pi/3), each carried by two labels
    x = theta % (2*math.pi/3)
    j = min(int(x // (2*math.pi/9)), 2)
    return frozenset({j, j+3})

def branches(d, alpha, f):
    a = complex(d*math.cos(alpha), d*math.sin(alpha))
    ff = complex(math.cos(f), math.sin(f))
    w = a + ff; r = abs(w)
    if r < 1e-12 or r > 2-1e-12: return []
    c = min(r/2.0, 1.0); q = math.sqrt(max(0.0, 1-c*c)); what = w/r
    return [w/2 + sg*1j*what*q for sg in (1, -1)]

def run(P, D, N=400000, seed=7):
    random.seed(seed)
    tot = viol = 0
    worst = None
    for _ in range(N):
        d = D*random.random(); alpha = random.uniform(-math.pi, math.pi); f = random.uniform(-math.pi, math.pi)
        for s in branches(d, alpha, f):
            tot += 1
            ang = math.atan2(s.imag, s.real)
            A = P(f); B = P(ang)
            if isinstance(A, int): A = frozenset({A})
            if isinstance(B, int): B = frozenset({B})
            if A & B:
                viol += 1
                if worst is None:
                    worst = (d, alpha, f, math.remainder(ang-f, 2*math.pi))
    return tot, viol, worst

DSTAR = 2*math.cos(2*math.pi/9)-1
print("D* = 2cos(2pi/9)-1 = %.12f" % DSTAR)
for D in [0.3, 0.5, DSTAR]:
    tot, viol, w = run(P18, D)
    print("  construction 1 (18 sectors, singletons) at D=%.7f : %d checks, %d violations" % (D, tot, viol))
for D in [0.2, 2*math.sin(2*math.pi/9)-1]:
    tot, viol, w = run(P2, D)
    print("  construction 2 (double cover, |P|=2)     at D=%.7f : %d checks, %d violations" % (D, tot, viol))
for D in [0.55, 0.6, 0.7]:
    tot, viol, w = run(P18, D)
    print("  construction 1 ABOVE the threshold      at D=%.7f : %d checks, %d violations   first at delta=%.6f" % (D, tot, viol, (w[3] if w else float('nan'))))
print()
print("shifts where it breaks above D*: band = [a(D),b(D)] , same-label distances start at 5*pi/9 = %.9f" % (5*math.pi/9))
for D in [DSTAR, 0.55]:
    a = 2*math.asin((1-D)/2); b = 2*math.asin((1+D)/2)
    print("   D=%.7f : a=%.9f b=%.9f" % (D,a,b))
