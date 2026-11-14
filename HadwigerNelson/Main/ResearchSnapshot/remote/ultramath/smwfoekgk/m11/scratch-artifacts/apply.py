import sys, json, pathlib
sys.path.insert(0,'.scratch'); import narrow4
ROOT = pathlib.Path("work/lean/OAI")
EXTRA={
 "Analysis/PlaneSpectrum/Basic.lean":["Mathlib.Analysis.Complex.Polynomial.Basic","Mathlib.Algebra.AlgebraicCard","Mathlib.Analysis.SpecialFunctions.Complex.Circle","Mathlib.FieldTheory.IsAlgClosed.Basic","Mathlib.Topology.Homotopy.Lifting","Mathlib.Analysis.Convex.Contractible","Mathlib.AlgebraicTopology.FundamentalGroupoid.SimplyConnected"],
 "MeasureTheory/CompactFactors/Centers.lean":["Mathlib.Analysis.Convex.StrictConvexSpace","Mathlib.Analysis.InnerProductSpace.Basic","Mathlib.Analysis.InnerProductSpace.Convex","Mathlib.Analysis.CStarAlgebra.Classes"],
 "Geometry/PlaneColoring/Expansion.lean":["Mathlib.MeasureTheory.Function.ContinuousMapDense","Mathlib.Analysis.Convex.StrictConvexSpace","Mathlib.Analysis.Calculus.Deriv.Abs"],
}
mods=[l.strip() for l in open(".scratch/all17.txt") if l.strip()]
summary={}
for mod in mods:
    imps=sorted(set(narrow4.base_for(mod))|set(EXTRA.get(mod,[])))
    p=ROOT/mod; lines=p.read_text().splitlines(); i=lines.index("import Mathlib")
    body=lines[i+1:]
    if mod.endswith("Geometry/PlaneColoring/Expansion.lean"):
        for j,l in enumerate(body):
            if l.strip()=="nlinarith":
                body[j]=l.replace("nlinarith","nlinarith [show (0:ℝ) ≤ (K:ℝ) from K.2]"); break
    p.write_text("\n".join(lines[:i]+["import "+m for m in imps]+body)+"\n")
    summary[mod]=imps
    print(f"{mod:50s} {len(imps):4d} imports")
json.dump(summary, open(".scratch/narrow_final.json","w"), indent=0)
print("total unique:", len({m for v in summary.values() for m in v}))
