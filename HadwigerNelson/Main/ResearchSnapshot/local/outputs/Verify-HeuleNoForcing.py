import hashlib, json, pathlib, sys
p = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).with_name("HEULE553-NO-FORCING-CERTIFICATE.json")
a = json.loads(p.read_text(encoding="utf-8"))
assert hashlib.sha256(a["edge_text"].encode()).hexdigest() == a["edge_sha256"]
edges = [tuple(int(x)-1 for x in line.split()[1:]) for line in a["edge_text"].splitlines() if line.startswith("e ")]
assert a["vertices"] == 553 and len(edges) == 2722 and len(set(edges)) == 2722
assert all(0 <= i < j < 553 for i,j in edges)
w = a["witnesses"]
assert len(w) == 34
for c in w:
    assert len(c) == 553 and all(type(x) is int and 0 <= x < 5 for x in c)
    assert all(c[i] != c[j] for i,j in edges)
assert len({tuple(c[i] for c in w) for i in range(553)}) == 553
print("PASS: 34 proper five-colourings separate every distinct vertex pair. Fixed graph only.")
