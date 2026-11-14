import sys; sys.path.insert(0,'work')
from mpmath import mp, mpf, mpc, exp, sqrt, pi, acos, arg, fabs
from certify import decompose, in_arcs, margins
mp.dps=40
A=[(0,40),(120,160),(240,280)]; B=[(40,80),(160,200),(280,320)]
s3=sqrt(3)/2
for t in [mpf('-0.76'), mpf('-0.75'), mpf('0'), mpf('0.25')]:
    print("t=",t)
    for (a,b) in [(t,mpf(0)),(t+1,mpf(0)),(t+mpf(1)/2, s3)]:
        w=mpc(a,b)
        print("  vertex", (float(a),float(b)), "|w|=",float(fabs(w)))
        for (th,ph) in decompose(w):
            print("     th=%.6f ph=%.6f  mA(th in A)=%.4f mB(ph in B)=%.4f   mB?(th in B)=%.4f mA?(ph in A)=%.4f"%(
                float(th),float(ph),float(in_arcs(th,A)),float(in_arcs(ph,B)),float(in_arcs(th,B)),float(in_arcs(ph,A))))
