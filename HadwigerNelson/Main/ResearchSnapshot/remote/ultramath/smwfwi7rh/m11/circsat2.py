import sys
from circsat import sat
print("does a larger n help when b > 2a ?")
for (a,b) in [(4,9),(5,11),(6,13),(8,17),(10,21),(10,22)]:
    for n in [3*a, 4*a, 6*a, 8*a, 10*a, 14*a, 20*a]:
        if n < 2*b+2: continue
        try:
            r,_ = sat(n,a,b)
        except Exception as e:
            r = f"err {e}"
        print(f"  a={a} b={b} (b/a={b/a:.2f})  n={n:4d}  {r}")
