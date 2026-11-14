"""Extract an explicit frozen free-label word witnessing SAT at d = 0.175, n = 60,
then re-verify it independently of CaDiCaL:  (i) every palette nonempty, size 2..3,
C6-admissible, avoids label 0;  (ii) the word is disjoint on every shift in +-K(d);
(iii) a direct re-evaluation of Lemma 5.2(3) on a dense grid of (psi, theta) for all
distances d' <= 0.175 shows no violation of P(f) cap P(f+shift) = empty.
"""
import math, subprocess, os, tempfile, itertools, json
from frozen import shift, deriv
from wordsearch import palettes_valid_for_C6, Kset_from, sh_interval
CADICAL = "/opt/lean/bin/cadical"

def solve_word(n, d, alph, iv):
    K = Kset_from(d, n, iv)
    var = {}; cnt = 0
    for i in range(n):
        for P in alph:
            cnt += 1; var[(i,P)] = cnt
    cl = []
    for i in range(n):
        cl.append([var[(i,P)] for P in alph])
        for P,Q in itertools.combinations(alph,2):
            cl.append([-var[(i,P)], -var[(i,Q)]])
    for k in sorted(K):
        for i in range(n):
            j = (i+k) % n
            for P in alph:
                for Q in alph:
                    if not P.isdisjoint(Q):
                        cl.append([-var[(i,P)], -var[(j,Q)]])
    fd,path = tempfile.mkstemp(suffix=".cnf"); os.close(fd)
    try:
        with open(path,"w") as f:
            f.write(f"p cnf {cnt} {len(cl)}\n")
            for c in cl: f.write(" ".join(map(str,c))+" 0\n")
        r = subprocess.run([CADICAL,path],capture_output=True,text=True)
        txt = r.stdout
        if "s SATISFIABLE" not in txt: return None, K
        val = {}
        for line in txt.splitlines():
            if line.startswith("v"):
                for t in line[1:].split():
                    lit = int(t)
                    if lit == 0: continue
                    val[abs(lit)] = lit > 0
        word = []
        for i in range(n):
            chosen = [P for P in alph if val.get(var[(i,P)],False)]
            word.append(sorted(chosen[0]) if chosen else None)
        return word, K
    finally: os.unlink(path)

if __name__ == "__main__":
    alph = palettes_valid_for_C6()
    n, d = 60, 0.175
    iv = sh_interval(d, 8000)
    word, K = solve_word(n, d, alph, iv)
    print("witness for n=%d d=%.3f" % (n,d))
    print("shift interval [delta_min, M] =", iv)
    print("K (sector shifts) =", sorted(K))
    print("word =", word)
    # independent verification 1: structural
    ok = True
    for i,w in enumerate(word):
        assert w is not None
        assert 2 <= len(w) <= 3 and 0 not in w
        assert any((b-a) % 6 not in (1,5) for a in w for b in w if a < b), (i,w)
        for k in K:
            if not set(w).isdisjoint(word[(i+k) % n]):
                ok = False; print("FAIL disjointness", i, k, w, word[(i+k)%n])
    print("structural verification:", "OK" if ok else "FAILED")
    # independent verification 2: direct evaluation of the geometric constraint
    bad = 0; tested = 0
    for i in range(400):
        psi = -math.pi + 2*math.pi*i/400
        for j in range(720):
            theta = -math.pi + 2*math.pi*j/720
            for sgn in (+1,-1):
                d2 = shift(d, psi, sgn)
                if d2 is None: continue
                fi = int(math.floor((theta % (2*math.pi))/(2*math.pi/n))) % n
                fj = int(math.floor(((theta+d2) % (2*math.pi))/(2*math.pi/n))) % n
                tested += 1
                if not set(word[fi]).isdisjoint(word[fj]): bad += 1
    print(f"geometric re-evaluation: {tested} (psi,theta,branch) samples, violations = {bad}")
    json.dump({"n":n,"d":d,"word":word,"K":sorted(K),"iv":iv}, open("witness_0175.json","w"), indent=1)
