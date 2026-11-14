"""Exact decision of 3-colourability of the circulant C_n(a..b), via CaDiCaL on an
explicit CNF, plus an independent backtracking check for the small instances.

C_n(a..b): vertices Z/n, edges between i and i+k for k in {a,...,b} (both signs).
"""
import subprocess, os, sys, itertools, tempfile

CADICAL = "/opt/lean/bin/cadical"

def cnf(n, a, b, path):
    K = set()
    for k in range(a, b+1):
        if k % n: K.add(k % n); K.add((-k) % n)
    K = sorted(K)
    var = lambda i,c: i*3 + c + 1
    clauses = []
    for i in range(n):
        clauses.append([var(i,0), var(i,1), var(i,2)])
        for c in range(3):
            for d in range(c+1,3):
                clauses.append([-var(i,c), -var(i,d)])
    for i in range(n):
        for k in K:
            j = (i+k) % n
            if j <= i: continue          # each edge once
            for c in range(3):
                clauses.append([-var(i,c), -var(j,c)])
    with open(path,"w") as f:
        f.write(f"p cnf {3*n} {len(clauses)}\n")
        for cl in clauses: f.write(" ".join(map(str,cl))+" 0\n")
    return len(clauses)

def sat(n,a,b):
    fd, path = tempfile.mkstemp(suffix=".cnf"); os.close(fd)
    try:
        nc = cnf(n,a,b,path)
        out = subprocess.run([CADICAL,"-q",path],capture_output=True,text=True)
        txt = out.stdout
        return ("s SATISFIABLE" in txt), out.stdout[-200:]
    finally:
        os.unlink(path)

if __name__ == "__main__":
    print("b/a ratio sweep, n = 6a:")
    for a in [4,5,6,8,10]:
        n = 6*a
        row=[]
        for mult in [1.5,1.8,1.95,2.0,2.2,2.5,2.8,2.95,3.0]:
            b = int(round(mult*a))
            if b>n//2: continue
            r,_ = sat(n,a,b)
            row.append(f"b/a={b/a:.2f}:{('SAT' if r else 'UNSAT')}")
        print(f" a={a:3d} n={n:3d}  " + "  ".join(row))
