"""Chromatic number of the forced 9-point configuration, as a function of the shift gamma.

z(m,j)(gamma) = e^{i 2j(pi/3)} (1 + zeta_m e^{i gamma}),   zeta_m = e^{i(2m+1)pi/3},
m,j in {0,1,2}: the points that the sum construction forces into the 3-label complement C
at a complement-3 state alternation (engine.md, section 5).

Edges are decided by the 36 equations |z_a - z_b| = 1 (real analytic in gamma).  We locate
every solution (sign changes + tangential minima), then evaluate the graph and its chromatic
number on every stratum.
"""
import numpy as np, itertools, json, hashlib, mpmath as mp
mp.mp.dps = 40
kappa = np.pi/3
g0 = 2*np.arcsin(1/(2*np.sqrt(3)))

def zpts(g):
    k = np.pi/3
    zeta = [np.exp(1j*((2*m+1)*k)) for m in range(3)]
    return np.array([np.exp(1j*2*j*k)*(1 + zeta[m]*np.exp(1j*g)) for m in range(3) for j in range(3)])

def d2(g, a, b):
    P = zpts(g); return abs(P[a]-P[b])**2

N = 400000
gs = np.linspace(0, 2*np.pi, N, endpoint=False)
D = np.zeros((N, 9, 9))
for idx, g in enumerate(gs):
    P = zpts(g); D[idx] = np.abs(P[:,None]-P[None,:])
crit = []
for (a,b) in itertools.combinations(range(9),2):
    f = D[:,a,b]**2 - 1.0
    # sign changes
    s = np.sign(f)
    idx = np.where(s[:-1]*s[1:] < 0)[0]
    for i in idx:
        lo, hi = gs[i], gs[i+1]; flo = f[i]
        for _ in range(80):
            mid = 0.5*(lo+hi); fm = d2(mid,a,b)-1
            if flo*fm <= 0: hi = mid
            else: lo, flo = mid, fm
        crit.append(0.5*(lo+hi))
    # possible tangential zeros: local minima of |f| below a threshold (vectorised)
    absf = np.abs(f)
    loc = np.where((absf[1:-1] < absf[:-2]) & (absf[1:-1] < absf[2:]) & (absf[1:-1] < 1e-2))[0] + 1
    for i in loc:
        lo, hi = gs[i-1], gs[i+1]
        # golden-section on |f|
        gr = (np.sqrt(5)-1)/2; c = hi - gr*(hi-lo); d = lo + gr*(hi-lo)
        fc, fd = abs(d2(c,a,b)-1), abs(d2(d,a,b)-1)
        for _ in range(120):
            if fc < fd: hi, d, fd = d, c, fc; c = hi - gr*(hi-lo); fc = abs(d2(c,a,b)-1)
            else: lo, c, fc = c, d, fd; d = lo + gr*(hi-lo); fd = abs(d2(d,a,b)-1)
        gg = 0.5*(lo+hi)
        if abs(d2(gg,a,b)-1) < 1e-20:
            crit.append(gg)
crit = sorted(crit)
# dedupe
ded = []
for c in crit:
    if not ded or abs(c-ded[-1]) > 1e-9: ded.append(c)
crit = ded
print("distinct critical gamma values:", len(crit))

def graph(g, tol=1e-12):
    P = zpts(g); return [(a,b) for a in range(9) for b in range(a+1,9)
                         if abs(abs(P[a]-P[b])-1) < tol]

def chromatic(E):
    for c in range(1,7):
        for col in itertools.product(range(c), repeat=9):
            if all(col[a]!=col[b] for (a,b) in E): return c
    return None

report = []
def analyse(g, label, gex=None):
    E = graph(g)
    chi = chromatic(E)
    gG = g if gex is None else gex
    radii = [abs(1+np.exp(1j*((2*m+1)*kappa+gG))) for m in range(3)]
    report.append({"gamma": float(g if gex is None else gex), "label": label, "n_edges": len(E),
                   "chromatic": chi, "radii": [float(r) for r in radii],
                   "unit_chord_circles": [m for m in range(3) if abs(radii[m]*np.sqrt(3)-1) < 1e-10]})

for i,g in enumerate(crit): analyse(g, f"critical#{i}")
inter = sorted(set([0.0] + crit + [2*np.pi]))
for i in range(len(inter)-1):
    if inter[i+1]-inter[i] > 1e-9:
        analyse(0.5*(inter[i]+inter[i+1]), "open stratum")
analyse(float(g0), "paper constant gamma0")
analyse(float(2*np.pi-g0), "2pi-gamma0")
print("chromatic numbers attained:", sorted(set(r["chromatic"] for r in report)))
print("max chromatic number:", max(r["chromatic"] for r in report))
print("\nall strata with chi >= 2:")
for r in report:
    if r["chromatic"] >= 2:
        print(f"  gamma={r['gamma']:.12f}  chi={r['chromatic']}  #edges={r['n_edges']}  radii={[round(x,6) for x in r['radii']]}  unit-chord circles={r['unit_chord_circles']}  [{r['label']}]")
print("\nnumber of strata with chi>=2:", sum(1 for r in report if r["chromatic"]>=2), "of", len(report))
txt = json.dumps(report, indent=1, sort_keys=True)
open("CERT-circles-ceiling.json","w").write(txt)
print("sha256:", hashlib.sha256(txt.encode()).hexdigest())
