import numpy as np, math
# ---- paper constants ----
kappa = math.pi/3
gamma = 2*math.asin(1/(2*math.sqrt(3)))
print("gamma            =", gamma)
print("cos(gamma)       =", math.cos(gamma), " (paper Lemma 6.4 claims 5/6 =", 5/6, ")")
print("gamma/pi         =", gamma/math.pi)
# irrationality argument in paper: 2cos(gamma)=5/3 rational algebraic integer -> integer. check
print("2cos(gamma)      =", 2*math.cos(gamma))
# distance claim: |1-e^{i gamma}| = 1/sqrt(3)
print("|1-e^{i g}|      =", abs(1-np.exp(1j*gamma)), " 1/sqrt3 =", 1/math.sqrt(3))
# triangle z_j = x + e^{i(t+2j kappa)}(1-e^{i gamma}), j=0,1,2 : equilateral side 1
t = 0.37
zs = [ (np.exp(1j*(t+2*j*kappa))*(1-np.exp(1j*gamma))) for j in range(3)]
print("dist to x        =", [abs(z) for z in zs])
d = [abs(zs[i]-zs[j]) for i in range(3) for j in range(i+1,3)]
print("pairwise dists   =", d)
# ---- diadic maps of Lemma 5.5: y+e^{it} = x + e^{i alpha+} + e^{i alpha-}, y-x = d real ----
def diadic(t, d):
    z = d + np.exp(1j*t)
    Theta = t + np.imag(np.log(1 + d*np.exp(-1j*t)))
    a = math.acos(abs(z)/2)
    return Theta + a, Theta - a
for d in [1e-3, 0.1, 0.4]:
    t = np.random.RandomState(0).uniform(0, 2*np.pi)
    a1,a2 = diadic(t,d)
    lhs = d + np.exp(1j*t); rhs = np.exp(1j*a1)+np.exp(1j*a2)
    print(f"d={d}: |lhs-rhs| = {abs(lhs-rhs):.3e}   (identity y+e^it = x+e^ia+ + e^ia-)")
    # expansion alpha_pm(t) = t +- kappa - d sin t -+ d/sqrt3 cos t + O(d^2)
    f1 = t + kappa - d*np.sin(t) - d/math.sqrt(3)*np.cos(t)
    f2 = t - kappa - d*np.sin(t) + d/math.sqrt(3)*np.cos(t)
    print("   first-order error a+:", abs(a1-f1), " a-:", abs(a2-f2), " (should be O(d^2))")
