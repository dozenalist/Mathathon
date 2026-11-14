"""word.py -- the free-label sector word for the six-cycle, decided exactly.

Object.  Fix m >= 1, n = 6m sectors of angle Delta = 2*pi/n, and let a *word* be
W : Z_n -> palettes (subsets of the six labels).  By the dictionary of
dictionary.py, the sector-constant palette field P_z(e) = W(sector(arg e)) satisfies
the paper's (5.3) and (5.7) for all centre pairs at distance <= d0 = pi/(9m) iff

  (A) every W(i) is an admissible C_6 palette: 1 <= |W(i)| <= 3 and W(i) is not
      contained in a cycle edge {j,j+1} mod 6                          [(6.2)]
  (B) W(i) does not contain the free label (taken to be 0; relabelling is a
      symmetry of C_6, so this loses nothing)
  (C) W(i) cap W(i+delta) = empty for every i and every
      delta in {+-(m-1), +-m, +-(m+1)} mod 6m.

RESULTS (this file).
  R1  Uniform construction: for every m >= 5 the 2m-periodic word
          A^(m-3) B^2 C^(m-3) D^2 E^2,  A={1,3} B={1,4} C={2,4} D={2,5} E={3,5},
      repeated three times on Z_{6m}, satisfies (A),(B),(C).
      * exact integer verification for every m in 5..1500;
      * a machine-checked symbolic proof (sympy, every comparison is a linear
        inequality in m decided over m >= 6) that it holds for ALL m >= 6;
      * m = 5 is checked directly (the symbolic proof needs m >= 6 only at the
        two block boundaries where a length m-3 block could shrink to nothing).
  R2  Classification: (A),(B),(C) is satisfiable iff m >= 5, for the pairs-only
      domain and for the pairs+triples domain alike.  m = 1,2,3,4 are UNSAT,
      certified three ways: complete forward DFS, complete reverse DFS, Cadical
      CNF (plus a hand proof for m = 1,2,3: a triangle in the constraint graph).
  R3  Paper-level side conditions on the word of R1: palettes have size 2 (so
      m2's bound 2+2 <= 5 = k-1 holds at k=6), no ternary palette (m11 is
      vacuous), the trace condition (P5) holds for every cycle edge (a point mass
      at any label of W(i) outside that edge), and no label other than 0 is
      absent from the palette field.

Run:  python3 word.py            (all checks, ~2 min)
      python3 word.py --cert     (also rebuild and check certificates/cert.json)
"""
import json
import os
import subprocess
import sys
import tempfile
from itertools import combinations

CADICAL = '/opt/lean/bin/cadical'
HERE = os.path.dirname(os.path.abspath(__file__))
CERT = os.path.join(HERE, 'certificates', 'cert_m_le_4.json')

# ---------------------------------------------------------------- palettes
EDGES = [(1 << j) | (1 << ((j + 1) % 6)) for j in range(6)]


def admissible(S):
    return 1 <= bin(S).count('1') <= 3 and not any(S & e == S for e in EDGES)


def domain(pairs_only=True, avoid0=True):
    out = []
    for r in (2, 3):
        for c in combinations(range(6), r):
            S = sum(1 << i for i in c)
            if avoid0 and S & 1:
                continue
            if admissible(S):
                out.append(S)
    return [v for v in out if bin(v).count('1') == 2] if pairs_only else out


def offsets(m):
    n = 6 * m
    return sorted({(m + k) % n for k in (-1, 0, 1)} | {(-m + k) % n for k in (-1, 0, 1)})


def lab(S):
    return '{' + ','.join(str(i) for i in range(6) if S >> i & 1) + '}'


# ------------------------------------------------------------ R1 the word
Av, Bv, Cv, Dv, Ev = ((1 << 1) | (1 << 3), (1 << 1) | (1 << 4), (1 << 2) | (1 << 4),
                      (1 << 2) | (1 << 5), (1 << 3) | (1 << 5))


def word2m(m):
    return [Av] * max(0, m - 3) + [Bv] * 2 + [Cv] * max(0, m - 3) + [Dv] * 2 + [Ev] * 2


def word6m(m):
    W = word2m(m)
    return [W[i % (2 * m)] for i in range(6 * m)] if m >= 1 else []


def check_word(m, W):
    """exact check of (A),(B),(C); returns list of violations."""
    n = 6 * m
    bad = []
    if len(W) != n:
        return [('length', len(W), n)]
    for i, v in enumerate(W):
        if not admissible(v):
            bad.append(('A', i, lab(v)))
        if v & 1:
            bad.append(('B', i, lab(v)))
    S = set(offsets(m))
    for i in range(n):
        for d in S:
            j = (i + d) % n
            if i != j and W[i] & W[j]:
                bad.append(('C', i, d, lab(W[i]), lab(W[j])))
    return bad


def verify_range(lo, hi):
    bad = []
    for m in range(lo, hi + 1):
        v = check_word(m, word6m(m))
        if v:
            bad.append((m, v[:3]))
    return bad


# --------------------------------------------------- R2 decision procedures
def dfs_decide(m, vals, order, want_count=False, cap=5 * 10**7):
    """complete backtracking; returns (sat, nodes, count).  Sound and complete:
    a value is skipped only when it contradicts an already assigned neighbour."""
    n = 6 * m
    S = set(offsets(m))
    nbr = {i: sorted({(i + d) % n for d in S}) for i in range(n)}
    ok = [[not (a & b) for b in vals] for a in vals]
    assign = {}
    nodes = [0]
    cnt = [0]

    def rec(k):
        nodes[0] += 1
        if nodes[0] > cap:
            raise MemoryError
        if k == n:
            cnt[0] += 1
            return True
        i = order[k]
        for v in range(len(vals)):
            if all(ok[v][assign[j]] for j in nbr[i] if j in assign):
                assign[i] = v
                if rec(k + 1):
                    if not want_count:
                        return True
                del assign[i]
        return False

    try:
        sat = rec(0)
    except MemoryError:
        return ('CAP', nodes[0], None)
    return (sat, nodes[0], cnt[0])


def cadical_decide(m, vals, timeout=600):
    n = 6 * m
    S = offsets(m)
    V = len(vals)

    def var(i, v):
        return i * V + v + 1

    cl = []
    for i in range(n):
        cl.append([var(i, v) for v in range(V)])
        for a, b in combinations(range(V), 2):
            cl.append([-var(i, a), -var(i, b)])
    for i in range(n):
        for d in S:
            j = (i + d) % n
            if i == j:
                continue
            for a in range(V):
                for b in range(V):
                    if vals[a] & vals[b]:
                        cl.append([-var(i, a), -var(j, b)])
    with tempfile.NamedTemporaryFile('w', suffix='.cnf', delete=False) as f:
        f.write(f"p cnf {n * V} {len(cl)}\n")
        for c in cl:
            f.write(" ".join(map(str, c)) + " 0\n")
        path = f.name
    try:
        r = subprocess.run([CADICAL, '-q', path], capture_output=True, text=True, timeout=timeout)
        out = r.stdout.strip().splitlines()
        first = out[0].strip() if out else ''
        if first.startswith('s UNSATISFIABLE'):
            return 'UNSAT'
        if first.startswith('s SATISFIABLE'):
            return 'SAT'
        return 'UNKNOWN(' + (first or 'no output') + ')'
    finally:
        os.unlink(path)


def search_tree(m, vals):
    """complete search tree as nested [value, [subtree,...]] for the certificate."""
    n = 6 * m
    S = set(offsets(m))
    nbr = {i: sorted({(i + d) % n for d in S}) for i in range(n)}
    ok = [[not (a & b) for b in vals] for a in vals]
    assign = {}

    def rec(k):
        if k == n:
            return None            # a full solution would appear here
        i = k
        children = []
        for v in range(len(vals)):
            if all(ok[v][assign[j]] for j in nbr[i] if j in assign):
                assign[i] = v
                children.append([v, rec(k + 1)])
                del assign[i]
        return children
    return rec(0)


def verify_tree(m, vals, tree):
    """independent replay of the certificate: at every node the listed children are
    exactly the locally consistent values, and a leaf has none."""
    n = 6 * m
    S = set(offsets(m))
    nbr = {i: sorted({(i + d) % n for d in S}) for i in range(n)}
    ok = [[not (a & b) for b in vals] for a in vals]
    assign = {}
    bad = []

    def rec(k, children):
        if k == n:
            bad.append(('tree continues past the last sector', k))
            return
        i = k
        good = [v for v in range(len(vals))
                if all(ok[v][assign[j]] for j in nbr[i] if j in assign)]
        listed = [c[0] for c in children]
        if good != listed:
            bad.append(('children mismatch', k, good, listed))
            return
        for v, sub in children:
            assign[i] = v
            if sub is None:
                bad.append(('tree has a complete assignment (SAT, not UNSAT)', k, v))
            elif sub == []:
                continue          # leaf: no value at k+1 is consistent -> verified below
            else:
                rec(k + 1, sub)
            del assign[i]
        # each leaf must be a genuine dead end
        for v, sub in children:
            if sub == []:
                assign[i] = v
                nxt = k + 1
                if nxt < n and any(all(ok[w][assign[j]] for j in nbr[nxt] if j in assign)
                                   for w in range(len(vals))):
                    bad.append(('spurious leaf', k, v))
                del assign[i]

    rec(0, tree)
    return bad


# ---------------------------------------------- R3 paper-level side conditions
def side_conditions(m):
    W = word6m(m)
    vals = sorted(set(W))
    res = {}
    res['sizes'] = sorted({bin(v).count('1') for v in vals})
    res['admissible'] = all(admissible(v) for v in vals)
    res['free label 0 absent'] = all(not (v & 1) for v in W)
    res['m2 (2|P| <= 5)'] = 2 * max(bin(v).count('1') for v in W) <= 5
    res['m11 ternary present'] = any(bin(v).count('1') == 3 for v in W)
    p5 = True
    for e in range(6):
        edge = {e, (e + 1) % 6}
        for v in vals:
            S = {i for i in range(6) if v >> i & 1}
            p5 &= bool(S - edge)      # a point mass at such a label kills both
    res['(P5) every edge killable in every palette'] = p5
    u = 0
    for v in vals:
        u |= v
    res['labels never in a palette'] = [i for i in range(6) if not (u >> i & 1)]
    return res


# ---------------------------------------------- R4 free-label budget at k = 6
def free_budget(mmax=600):
    """LEMMA.  At k = 6, a word satisfying (A) admissibility and (C) the six-offset
    transport has palette union of size >= 5 (m >= 3): at most ONE label can be free.
    Proof: if the union lies in a 4-set A, two disjoint palettes in A are complementary
    pairs, so every neighbour of i is A \\ W(i); applying that at i+(m-1) with offset
    -(m+1) gives W(i-2) = W(i), i.e. W is 2-periodic; but one of m-1, m, m+1 is even,
    and an even shift must then land on W(i) itself, which is not disjoint from W(i).
    Checked here: (1) the combinatorial part for all 15 four-subsets, (2) the parity
    fact for all m >= 3, (3) that no 2-periodic word on a 4-set satisfies (C)."""
    from itertools import combinations as C4
    out = []
    # (1)
    ok1 = True
    for A in C4(range(6), 4):
        Aset = sum(1 << i for i in A)
        vals = [sum(1 << i for i in c) for r in (2, 3) for c in C4(A, r)]
        vals = [v for v in vals if admissible(v)]
        for a in vals:
            mates = [b for b in vals if not (a & b)]
            ok1 &= (mates in ([Aset ^ a], [])) if bin(a).count('1') == 2 else (mates == [])
    out.append(('4-set: disjoint partner is the complement, triples have none', ok1))
    # (2)
    ok2 = all(any(d % 2 == 0 for d in offsets(m)) for m in range(3, 2001))
    out.append(('one of the six offsets is even, every m >= 3', ok2))
    # (3)
    bad = 0
    for m in range(3, mmax + 1):
        n, S = 6 * m, set(offsets(m))
        for A in C4(range(6), 4):
            vals = [sum(1 << i for i in c) for r in (2, 3) for c in C4(A, r)]
            vals = [v for v in vals if admissible(v)]
            for P in vals:
                for Q in vals:
                    W = [P if i % 2 == 0 else Q for i in range(n)]
                    if all(not (W[i] & W[(i + d) % n]) for i in range(n) for d in S):
                        bad += 1
    out.append((f'no 2-periodic 4-set word satisfies (C), m = 3..{mmax}', bad == 0))
    return out


# ----------------------------------------------------------------- main
def main():
    ok = []

    def say(name, cond, extra=""):
        print(('  PASS  ' if cond else '  FAIL  ') + name + ("   " + extra if extra else ""))
        ok.append(cond)

    print("R1  uniform word  A^(m-3) B^2 C^(m-3) D^2 E^2  on Z_{2m}, repeated 3x on Z_{6m}")
    print("    m=6 :", " ".join(lab(v) for v in word2m(6)))
    print("    m=5 :", " ".join(lab(v) for v in word2m(5)))
    bad = verify_range(5, 1500)
    say("exact integer check of (A),(B),(C) for every m in 5..1500", not bad, str(bad[:2]))
    print("    symbolic proof for all m >= 6: run symbolic_proof.py (sympy, linear"
          " inequalities)")
    sym = subprocess.run([sys.executable, os.path.join(HERE, 'symbolic_proof.py')],
                         capture_output=True, text=True)
    say("symbolic proof: word satisfies (C) for every m >= 6",
        'SYMBOLIC RESULT for every m >= 6: True' in sym.stdout)
    say("m=5 checked directly (the end of the proof's range)", not check_word(5, word6m(5)))

    print()
    print("R2  classification: satisfiable iff m >= 5")
    P, Wd = domain(True), domain(False)
    print("    pairs-only domain:", [lab(v) for v in P])
    cert = {}
    for m in (1, 2, 3, 4):
        for label, vals in (('pairs', P), ('pairs+triples', Wd)):
            n = 6 * m
            f = dfs_decide(m, vals, list(range(n)))
            r = dfs_decide(m, vals, list(range(n - 1, -1, -1)))
            c = cadical_decide(m, vals)
            tree = search_tree(m, vals)
            badt = verify_tree(m, vals, tree)
            cert[f'm={m}|{label}'] = tree
            say(f"m={m} {label}: UNSAT by forward DFS, reverse DFS, Cadical, certificate",
                (not f[0]) and (not r[0]) and c == 'UNSAT' and not badt,
                f"nodes fwd={f[1]} rev={r[1]} cadical={c} cert-nodes-ok={not badt}")
    for m in (5, 6, 9, 12):
        for label, vals in (('pairs', P), ('pairs+triples', Wd)):
            s = dfs_decide(m, vals, list(range(6 * m)))
            say(f"m={m} {label}: SAT", bool(s[0]))
    if '--cert' in sys.argv:
        os.makedirs(os.path.dirname(CERT), exist_ok=True)
        with open(CERT, 'w') as f:
            json.dump(cert, f)
        print("    certificate written to", os.path.relpath(CERT, HERE))
        back = json.load(open(CERT))
        badt = []
        for key, tree in back.items():
            mm = int(key.split('|')[0][2:])
            vals = P if key.endswith('pairs') else Wd
            badt += verify_tree(mm, vals, tree)
        say("certificate file re-verified", not badt, str(badt[:2]))

    print()
    print("R3  paper-level side conditions on the word (m = 6)")
    sc = side_conditions(6)
    for k, v in sc.items():
        print(f"    {k}: {v}")
    say("(P1) |P| in {2} (no singletons)", sc['sizes'] == [2])
    say("(6.2) admissibility", sc['admissible'])
    say("non-proper self-avoidance (label 0 absent)", sc['free label 0 absent'])
    say("m2's bound 2+2 <= 5 at k=6", sc['m2 (2|P| <= 5)'])
    say("m11: no ternary palette", not sc['m11 ternary present'])
    say("(P5) for every cycle edge", sc['(P5) every edge killable in every palette'])
    say("only label 0 is absent from the field (so self-avoidance forces c = 0)",
        sc['labels never in a palette'] == [0])

    print()
    print("R4  free-label budget at k=6 (a word satisfying (A),(C) has union size >= 5)")
    for name, cond in free_budget():
        say(name, cond)

    print()
    print("SUMMARY:", "ALL CHECKS PASS" if all(ok) else f"{ok.count(False)} FAILED")


if __name__ == "__main__":
    main()
