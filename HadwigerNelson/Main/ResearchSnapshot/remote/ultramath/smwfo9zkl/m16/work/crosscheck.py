"""Cross-check the two independent encodings and verify every certificate by hand."""
import json, itertools, hashlib

A = json.load(open("states_k5_k6.json"))
B = json.load(open("states_k5_k6_b.json"))
assert sorted(A) == sorted(B), (sorted(A), sorted(B))
ok = True
lines = []
for key in sorted(A):
    a, b = A[key], B[key]
    # 1. same occurring value set
    sa = sorted(tuple(v) for v in a["occurring"])
    sb = sorted(tuple(v) for v in b["occurring"])
    if sa != sb:
        ok = False; lines.append(f"{key}: OCCURRING MISMATCH")
    # 2. same bipartite verdict
    if a["bipartite"] != b["bipartite"]:
        ok = False; lines.append(f"{key}: BIPARTITE MISMATCH")
    # 3. same orbit count
    if a["n_orbit_data"] != b["n_orbit_data"]:
        ok = False; lines.append(f"{key}: ORBIT COUNT MISMATCH {a['n_orbit_data']} vs {b['n_orbit_data']}")
    # 4. same 2-colouring groups when bipartite
    if a["bipartite"]:
        ga = sorted(tuple(v) for v in a["engines"]["groups"])
        gb = sorted(tuple(v) for v in b["groups"])
        if ga != gb:
            ok = False; lines.append(f"{key}: GROUP MISMATCH {ga} vs {gb}")
    else:
        # 5. verify program 1's odd cycle independently here, edge by edge
        cyc = [tuple(v) for v in a["odd_cycle_witness"]]
        occ = set(sa)
        assert all(v in occ for v in cyc), (key, cyc)
        assert cyc[0] == cyc[-1], (key, "not closed")
        L = len(cyc)-1
        assert L % 2 == 1, (key, f"even cycle length {L}")
        assert len(set(cyc[:-1])) == L, (key, "not simple")
        for t in range(L):
            u, v = set(cyc[t]), set(cyc[t+1])
            assert not (u & v), (key, f"edge {cyc[t]}-{cyc[t+1]} not a disjointness edge")
        lines.append(f"{key}: odd cycle of length {L} verified edge by edge: "
                     + " - ".join(str(list(v)) for v in cyc))
    lines.append(f"{key}: #occurring={len(sa)} bipartite={a['bipartite']} #orbit_data={a['n_orbit_data']}")
print("\n".join(lines))
print("\nALL AGREEMENT CHECKS PASSED" if ok else "\nMISMATCHES FOUND")
cert = "\n".join(lines) + "\n"
open("CERT-state-accounting.txt","w").write(cert)
print("sha256(certificate) =", hashlib.sha256(cert.encode()).hexdigest())
