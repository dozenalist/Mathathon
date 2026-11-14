import cmath, math
from shiftset import branches, admissible

# structure of the shift functions:  shift_+(psi) = phi + arccos(r/2) - psi,
# where d + e^{i psi} = r e^{i phi}.  Locate extrema.
for d in [0.1, 0.3, 0.5, 0.7, 0.9]:
    xs=[]; ps=[]
    for i in range(3601):
        psi = -math.pi + 2*math.pi*i/3600
        bb = admissible(d, psi)
        for b in bb:
            if b['sgn']>0:
                xs.append(b['shift']); ps.append(psi)
    imin = min(range(len(xs)), key=lambda i: xs[i]); imax = max(range(len(xs)), key=lambda i: xs[i])
    print(f"d={d}:  min shift+ = {xs[imin]:.6f} at psi={ps[imin]:.4f} ({math.degrees(ps[imin]):.2f} deg)"
          f"   max shift+ = {xs[imax]:.6f} at psi={ps[imax]:.4f} ({math.degrees(ps[imax]):.2f} deg)")
    # also report arccos((1-d)/2) and arccos((1+d)/2)
    print(f"     arccos((1-d)/2)={math.acos((1-d)/2):.6f}   arccos((1+d)/2)={math.acos((1+d)/2):.6f}"
          f"   pi-arccos((1-d)/2)={math.pi-math.acos((1-d)/2):.6f}")
