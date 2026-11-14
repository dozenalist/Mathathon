import graph as g, re, collections

M = g.M
decl = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:noncomputable\s+|private\s+|protected\s+|partial\s+)?(theorem|lemma|def|abbrev|instance|structure|class|inductive)\s+([A-Za-z_][A-Za-z0-9_.'!?]*)")
tok = re.compile(r"[A-Za-z_][A-Za-z0-9_'!?]*")

names, uses, text = {}, {}, {}
for m, d in M.items():
    s = {}
    with open(d["path"], encoding="utf-8") as fh:
        txt = fh.read()
    text[m] = txt
    for line in txt.splitlines():
        mt = decl.match(line)
        if mt:
            nm = mt.group(2).split(".")[-1]
            if len(nm) > 4:
                s.setdefault(nm, 0)
    names[m] = s
    uses[m] = collections.Counter(tok.findall(txt))

def short(m):
    return m.split(".")[-1]

import sys
def report(target, consumers):
    print("#### decls of %s used by %s" % (short(target), ", ".join(short(c) for c in consumers)))
    for nm in sorted(names[target]):
        cs = [c for c in consumers if c in uses and uses[c][nm] >= 1]
        if cs:
            print("   %-42s <- %s" % (nm, ", ".join(short(c) for c in cs)))
    print()

if __name__ == "__main__":
    pairs = [
        ("OAI.MeasureTheory.CompactFactors.ConditionalSelection", "OAI.Analysis.PlaneSpectrum.ConditionalSpectrum"),
        ("OAI.Analysis.PlaneSpectrum.PhaseCollision", "OAI.MeasureTheory.CompactFactors.ConditionalSelection"),
        ("OAI.Analysis.PlaneSpectrum.PhaseEncoding", "OAI.Analysis.PlaneSpectrum.PhaseCollision"),
        ("OAI.Analysis.PlaneSpectrum.ConditionalSpectrum", "OAI.MeasureTheory.CompactFactors.Approximation"),
        ("OAI.MeasureTheory.CompactFactors.Approximation", "OAI.MeasureTheory.CompactFactors.ConditionalLimits"),
        ("OAI.MeasureTheory.CompactFactors.ConditionalLimits", "OAI.MeasureTheory.CompactFactors.Kernels"),
        ("OAI.MeasureTheory.CompactFactors.ConditionalLimits", "OAI.MeasureTheory.CompactFactors.Factors"),
        ("OAI.MeasureTheory.CompactFactors.RelativeCenters", "OAI.MeasureTheory.CompactFactors.Approximation"),
        ("OAI.MeasureTheory.CompactFactors.Kernels", "OAI.MeasureTheory.CompactFactors.Functions"),
        ("OAI.MeasureTheory.CompactFactors.Kernels", "OAI.MeasureTheory.CompactFactors.RelativeProducts"),
        ("OAI.MeasureTheory.CompactFactors.Kernels", "OAI.MeasureTheory.CompactFactors.Separability"),
        ("OAI.MeasureTheory.CompactFactors.Separability", "OAI.MeasureTheory.CompactFactors.AlgebraModels"),
        ("OAI.MeasureTheory.CompactFactors.AlgebraModels", "OAI.Analysis.PlaneSpectrum.Representations"),
        ("OAI.MeasureTheory.CompactFactors.AlgebraModels", "OAI.Analysis.PlaneSpectrum.Energy"),
        ("OAI.MeasureTheory.CompactFactors.Kernels", "OAI.Analysis.PlaneSpectrum.Energy"),
        ("OAI.MeasureTheory.CompactFactors.Kernels", "OAI.Analysis.PlaneSpectrum.Ergodicity"),
        ("OAI.MeasureTheory.CompactFactors.Centers", "OAI.MeasureTheory.CompactFactors.RelativeCenters"),
        ("OAI.MeasureTheory.CompactFactors.Stationary", "OAI.Analysis.PlaneSpectrum.Representations"),
    ]
    for tgt, con in pairs:
        report(tgt, [con])
