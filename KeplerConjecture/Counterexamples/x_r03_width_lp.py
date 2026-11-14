#!/usr/bin/env python3
"""X-R03: LP + exact certification over the FREE-WIDTH Gaussian family.

minimise P(0) subject to  P(s) <= 0 on [4,inf),  Q(w) >= 0 on [0,inf),  Q(0) = 1,
for f = P(s)e^{-as}, with the exact Fourier map of ce_width_family.
Search: LP on a grid with column equilibration + cutting planes.
Certificate: exact Sturm/multiplicity sign test; rounding renormalised so Q(0)=1 exactly.
Reports a bound ONLY when the exact certificate passes AND the Kepler test is decidable.
"""
import sys, numpy as np, sympy as sp
from fractions import Fraction as Fr
from scipy.optimize import linprog
import ce_width_family as W, ce_exact_gauss as G

s_ = W.s_; w_ = W.w_

def data(N, a, ng=120, smax=30.0, vmax=30.0):
    As = W.A_polys(N)
    def qrow(wv):
        return np.array([float(sp.N((a**(-n))*As[n].subs(w_, wv), 30)) for n in range(N+1)])
    S = np.linspace(4.0, smax, ng); V = np.linspace(0.0, vmax, ng)
    AP = np.array([[s**n for n in range(N+1)] for s in S])
    AQ = np.array([qrow(v) for v in V])
    p0 = np.zeros(N+1); p0[0] = 1.0                      # P(0) = c_0
    q0 = qrow(0.0)                                        # Q(0) = sum c_n a^-n A_n(0)
    sc = np.maximum(np.abs(AP).max(axis=0), np.abs(AQ).max(axis=0)); sc[sc==0]=1.0
    return dict(N=N, a=a, As=As, AP=AP/sc, AQ=AQ/sc, sc=sc, p0=p0, q0=q0/sc,
                qrow=lambda wv: qrow(wv)/sc, S=S, V=V)

def exact_Q(c, d):
    a=d['a']; As=d['As']
    return sp.expand(sum(sp.Rational(Fr(float(ci)).limit_denominator(10**9))*(a**(-n))*As[n]
                         for n, ci in enumerate(c)))

def certify_vec(c, d, eps_num=10**9):
    a=d['a']
    cf=[sp.Rational(Fr(float(ci)).limit_denominator(eps_num)) for ci in c]
    P=sp.expand(sum(ci*s_**n for n,ci in enumerate(cf)))
    Q=exact_Q(cf,d)
    Q0=sp.nsimplify(Q.subs(w_,0))
    if Q0 == 0: return None, "Q(0)=0 after rounding"
    # renormalise exactly so that Q(0)=1: scale c by 1/Q0 (ratio P0/Q0 is scale invariant)
    cf=[x/Q0 for x in cf]; P=sp.expand(P/Q0); Q=sp.expand(Q/Q0)
    P0=sp.nsimplify(P.subs(s_,0))
    if P0<=0: return None, "P(0)<=0 after normalisation"
    okP,rP=G.sign_on_half_line(P,4,-1); okQ,rQ=G.sign_on_half_line(Q,0,+1)
    if not (okP and okQ): return None, "signs: P[%s] Q[%s]" % ("ok" if okP else rP[:40], "ok" if okQ else rQ[:40])
    return (P,Q,sp.nsimplify(P0),sp.nsimplify(Q.subs(w_,0))), "ok"

def run(N, a, iters=25, eps=1e-10):
    d=data(N,a); extra_P=[]; extra_Q=[]
    for it in range(iters):
        rows=[d['AP']]+([np.array(extra_P)] if extra_P else [])+[-d['AQ']]+([-np.array(extra_Q)] if extra_Q else [])
        Aub=np.vstack(rows)
        bub=np.concatenate([np.full(len(d['AP']),-eps)]+([np.full(len(extra_P),-eps)] if extra_P else [])
                           +[np.zeros(len(d['AQ']))]+([np.zeros(len(extra_Q))] if extra_Q else []))
        res=linprog(d['p0'],A_ub=Aub,b_ub=bub,A_eq=d['q0'].reshape(1,-1),b_eq=[1.0],
                    bounds=[(None,None)]*(N+1),method='highs')
        if not res.success:
            return None, "SOLVER status %s %r (max|A|=%.2e) — not a proof of infeasibility" % (res.status,(res.message or '')[:60],np.abs(Aub).max())
        c=np.asarray(res.x)*d['sc']
        got,msg=certify_vec(c,d)
        if got:
            P,Q,P0,Q0=got
            kk=W.kepler_ok(P0,Q0,a)
            return (P0,Q0,W.density(P0,Q0,a),kk,P), "certified"
        # cutting plane
        cf=[sp.Rational(Fr(float(ci)).limit_denominator(10**9)) for ci in c]
        P=sp.expand(sum(ci*s_**n for n,ci in enumerate(cf))); Q=exact_Q(cf,d)
        bad=None
        for sv in np.linspace(4.0, 400.0, 3000):
            if float(sp.N(sp.Poly(P,s_).eval(sv))) > 0: bad=('P',sv); break
        if bad is None:
            for wv in np.linspace(0.0, 400.0, 3000):
                if float(sp.N(sp.Poly(Q,w_).eval(wv))) < 0: bad=('Q',wv); break
        if bad is None: return None, "certifier failed with no sampled violation: "+msg
        k,vv=bad
        if k=='P': extra_P.append(list(np.array([vv**n for n in range(N+1)])/d['sc']))
        else:      extra_Q.append(list(d['qrow'](vv)))
    return None, "no certificate in %d iterations" % iters

if __name__=="__main__":
    As_=sp.Rational(sys.argv[1]) if len(sys.argv)>1 else None
    print("%-3s %-5s %-11s %-13s %-9s %s" % ("N","a","P0/Q0","density","<Kepler","status"))
    best=None
    for N in ([int(sys.argv[2])] if len(sys.argv)>2 else [4,6]):
        for a in ([As_] if As_ else [sp.Rational(1,2),sp.Rational(3,4),1,sp.Rational(3,2),2,3]):
            out,msg=run(N,a)
            if out:
                P0,Q0,dens,kk,P=out
                print("%-3d %-5s %-11s %-13.6f %-9s %s" % (N,a,str(sp.nsimplify(P0/Q0))[:11],float(dens),kk,msg))
                if best is None or float(dens)<best[2]: best=(N,a,float(dens),sp.nsimplify(P0/Q0),kk,P)
            else:
                print("%-3d %-5s %-11s %-13s %-9s %s" % (N,a,"-","-","-",msg[:64]))
    print("-"*78)
    if best:
        N,a,dens,ratio,kk,P=best
        print("BEST CERTIFIED: N=%d a=%s  P0/Q0=%s  density=%.9f  beats Kepler: %s" % (N,a,ratio,dens,kk))
        print("  P(s) =", sp.factor(P))
        print("  STATUS: PROVED upper bound %0.9f for all unit-ball packings (exact signs)." % dens
              if kk else "  STATUS: PROVED upper bound %.9f (above Kepler, so no theorem about sharpness)." % dens)
    else:
        print("NO CERTIFIED CANDIDATE — no bound claimed.")
