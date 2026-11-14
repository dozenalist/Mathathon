import graph as g

M = g.M
rev = {m: [] for m in M}
for m, d in M.items():
    for i in d["imports"]:
        if i in rev:
            rev[i].append(m)

print("=== CompactFactors: size, importers-outside-group ===")
for m in sorted([m for m in M if "CompactFactors" in m], key=lambda x: M[x]["lines"]):
    ext = [r for r in rev[m] if "CompactFactors" not in r]
    print("%6d %-60s <- %s" % (M[m]["lines"], m, ", ".join(x.split(".")[-1] for x in ext) or "(none)"))

print()
print("=== PlaneSpectrum: size, importers-outside-group ===")
for m in sorted([m for m in M if "PlaneSpectrum" in m], key=lambda x: M[x]["lines"]):
    ext = [r for r in rev[m] if "PlaneSpectrum" not in r]
    print("%6d %-60s <- %s" % (M[m]["lines"], m, ", ".join(x.split(".")[-1] for x in ext) or "(none)"))

print()
print("=== modules importing CompactFactors at all ===")
for m in M:
    cf = [i for i in M[m]["imports"] if "CompactFactors" in i]
    if cf:
        print("%-50s -> %s" % (m.split(".")[-1], ", ".join(x.split(".")[-1] for x in cf)))
