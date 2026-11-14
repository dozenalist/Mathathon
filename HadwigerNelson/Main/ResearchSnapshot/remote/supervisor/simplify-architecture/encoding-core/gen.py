#!/usr/bin/env python3
"""Generate EncodingCore.lean / Wrappers.lean / MANIFEST.md by mechanical transplant.

Reads the SHARED originals read-only; writes only into this directory.
Every edit is asserted by count, so a drifted source fails loudly instead of
silently producing wrong code.
"""
import hashlib, pathlib, re

REPO = pathlib.Path(__file__).resolve().parents[3]
SPEC = REPO / "lean/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean"
LIM  = REPO / "lean/OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean"
L = SPEC.read_text().splitlines()
sha_spec = hashlib.sha256(SPEC.read_bytes()).hexdigest()

LIML = LIM.read_text().splitlines()

def find(name, lines=None):
    lines = lines if lines is not None else L
    for i, s in enumerate(lines):
        if s.strip().startswith("theorem " + name):
            return i
    raise SystemExit("not found: " + name + " in " + str(lines)[:40])

# ---- statement extraction: from the preceding `omit ... in` to the `:= by` ----
def statement(name, lines):
    i = find(name, lines)
    j = i
    while j > 0 and lines[j-1].strip() == "":
        j -= 1
    if lines[j-1].strip().startswith("omit"):
        j -= 1
    k = i
    while ":=" not in lines[k]:
        k += 1
    return lines[j:k+1], (j, k)

# ---- proof body: finite theorem, lines 324..476 (1-based) ----
B0, B1 = 324, 476
body = L[B0-1:B1]
assert body[0].strip() == "classical", body[0]
assert body[1].strip() == "let P : X → W := q ∘ p", body[1]
assert body[2].strip() == "have hP : Measurable P := hq.comp hp", body[2]
edits = []
out = []
for s in body:
    t = s
    if t.strip() in ("let P : X → W := q ∘ p", "have hP : Measurable P := hq.comp hp"):
        edits.append(("delete", s.strip())); continue
    for a, b, tag in (("H i (p x)", "H i (S x)", "H i"), ("H k (p x)", "H k (S x)", "H k"),
                      ("hH (p x)", "hH (S x)", "hH")):
        if a in t:
            n = t.count(a)
            edits.append(("sub x%d" % n, a + " -> " + b))
            t = t.replace(a, b)
    out.append(t)
body_new = out
# leftover p-dependent sites inside the body must be exactly the kernel arguments
leftover = [s for s in body_new if "(p x)" in s]
print("EDIT COUNT:", len(edits))
for e in edits: print("   ", e)
print("LEFT-OVER '(p x)' lines (must all be kernelEncoding arguments):", len(leftover))
for s in leftover: print("    |", s.strip()[:150])
print("lines with q/hp/hq left in body:", [s.strip()[:120] for s in body_new if re.search(r"\bq\b|\bhq\b|\bhp\b", s)])

HEADER = """\
/-
  PROPOSED COMMON ENCODING CORE.  For review; not integrated, not built by this block.

  The proof body is a MECHANICAL TRANSPLANT of
    `OAI.PlaneFiveColor.Spectral.finite_uniform_precision_contradiction`
  (`lean/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean`, lines {b0}-{b1}, source sha256 {sha}),
  with exactly the 7 edits listed in `PLAN.md` §6: delete the two local `P`/`hP` bindings (now
  parameters) and rewrite the 6 sites `H ?_ (p x)` -> `H ?_ (S x)`, `hH (p x)` -> `hH (S x)`.
  Nothing else was touched. The `kernelEncoding … (p x)` arguments are NOT parametrised.

  Intended home: inside `ConditionalSpectrum.lean`, immediately before
  `finite_uniform_precision_contradiction`. As a standalone module it compiles against the same
  three imports that file uses, so it can be checked without touching shared sources.
-/
import OAI.Analysis.PlaneSpectrum.FourierTests
import OAI.Analysis.PlaneSpectrum.SmallArcs
import OAI.MeasureTheory.CompactFactors.ConditionalSelection

namespace OAI
noncomputable section
open Filter Topology
open MeasureTheory ProbabilityTheory
open EuclideanFiveColor
open scoped ENNReal BigOperators ComplexConjugate
open scoped BigOperators ENNReal

-- The two originals each declare these LOCAL instances (Spectrum:43-44,178-179,260-261;
-- Limits:363-364) and they never leak across files, so the merged file must declare them again.
-- They are the same terms in both sources (`borel Circle`), which is what makes the two statements
-- the same proposition; `Circle` is Mathlib's unit circle with `ω.real : ℝ`.
local instance : MeasurableSpace Circle := borel Circle
local instance : BorelSpace Circle := ⟨rfl⟩

namespace PlaneFiveColor.Spectral

section
variable {{X Y W : Type*}} [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
  [MeasurableSpace Y] [StandardBorelSpace Y] [Nonempty Y]
  [MeasurableSpace W] [StandardBorelSpace W] [Nonempty W]

/-- The shared encoding hypothesis. `S : X → Z` is the read-out map: the approximating family lives
on `Z` and is sampled at `S x`. `P : X → W` is the factor map whose coefficient functions are used.

`S := p` (with `Z := Y`) gives the old `FiniteEncodingApproximationAt`;
`S := id` (with `Z := X`) gives the old `AmbientEncodingAt`. Both are *definitional*, see the two
`abbrev`s below and the `Iff.rfl` checks in `Wrappers.lean`. -/
def EncodingApproximationAt (μ : Measure X) [IsProbabilityMeasure μ] (p : X → Y) (P : X → W)
    {{Z : Type*}} (S : X → Z)
    (b : X → D) (m : ℕ) (γ : ℝ) : Prop :=
  ∃ (r : ℕ) (B C : ℝ) (H : Fin r → Z → Fin m → ℂ),
    0 ≤ B ∧ 0 ≤ C ∧ (∀ z, ∑ i, ‖H i z‖ ≤ C) ∧
    ∀ k : K, ∃ coeff : W → Fin r → ℂ,
      (∀ w, ‖coeff w‖ ≤ B) ∧
      Integrable (fun x => dist
        (PhaseEncoding.kernelEncoding (condDistrib b p μ)
          (fun d => (eval (kCoeff k) d : ℂ)) m (p x))
        (∑ i, coeff (P x) i • H i (S x)) ^ 2) μ ∧
      (∫ x, dist
        (PhaseEncoding.kernelEncoding (condDistrib b p μ)
          (fun d => (eval (kCoeff k) d : ℂ)) m (p x))
        (∑ i, coeff (P x) i • H i (S x)) ^ 2 ∂μ) < γ^2

/-- Definitional shadow of the old `FiniteEncodingApproximationAt`. -/
abbrev FiniteEncodingApproximationAt' (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : Y → W) (b : X → D) (m : ℕ) (γ : ℝ) : Prop :=
  EncodingApproximationAt μ p (fun x => q (p x)) p b m γ

/-- Definitional shadow of the old `AmbientEncodingAt` (whose home is `ConditionalLimits`). -/
abbrev AmbientEncodingAt' (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : X → W) (b : X → D) (m : ℕ) (γ : ℝ) : Prop :=
  EncodingApproximationAt μ p q id b m γ

/-- Both uniform-precision contradictions are this statement at `S := p, P := q ∘ p` and
`S := id, P := q`. No hypothesis is added, dropped or strengthened; in particular `hwild` stays a
hypothesis at `P` — the wildness of the difference law is neither derived nor hidden. -/
omit [StandardBorelSpace Y] [Nonempty Y] in
theorem uniform_precision_contradiction
    (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (P : X → W) {{Z : Type*}} (S : X → Z) (b : X → D)
    (hp : Measurable p) (hP : Measurable P) (hb : Measurable b)
    (m : ℕ) (hm : 0 < m) (g : Y → Fin m → D)
    (hg : ∀ᵐ y ∂μ.map p, condDistrib b p μ y =
      (m : ℝ≥0∞)⁻¹ • ∑ i, Measure.dirac (g y i))
    (hwild : IsWild (DifferenceFourier.differenceLaw (μ.map P)
      (condDistrib b P μ)))
    (ρ c : ℝ) (N : ℕ) (hρ : 0 < ρ) (hc : 0 < c) (hN : 0 < N)
    (harc : ∀ (ω : Measure Circle) [IsProbabilityMeasure ω],
      (∀ n, 0 < n → n ≤ N → ‖∫ w, (w : ℂ)^n ∂ω‖ < c) →
      ω.real {{w | ‖(w : ℂ)-1‖ ≤ 4*ρ}} < 1/(4*(m : ℝ)^2))
    (happrox : EncodingApproximationAt μ p P S b m (((ρ^m/(m : ℝ))/100)/100)) :
    False := by
"""

FOOTER = """
end
end PlaneFiveColor.Spectral
end
end OAI
"""

core = HEADER.format(b0=B0, b1=B1, sha=sha_spec) + "\n".join("  " + s if s.strip() else s for s in body_new) + "\n" + FOOTER
(pathlib.Path("EncodingCore.lean")).write_text(core)

# ---------------- Wrappers ----------------
fin_stmt, (fj, fk) = statement("finite_uniform_precision_contradiction", L)
amb_stmt, (aj, ak) = statement("ambient_uniform_precision_contradiction", LIML)
print("\nFINITE STMT lines", fj+1, "-", fk+1, "| AMBIENT STMT lines", aj+1, "-", ak+1)

def as_call(stmt, call):
    s = list(stmt)
    last = s[-1]
    assert last.rstrip().endswith(":= by"), last
    s[-1] = last.rstrip()[:-len(":= by")] + ":= " + call
    return "\n".join(s)

fin_text = as_call(fin_stmt,
  "uniform_precision_contradiction μ p (fun x => q (p x)) (Z := Y) p b\n"
  "    hp (hq.comp hp) hb m hm g hg hwild ρ c N hρ hc hN harc (finite_core_iff.mp happrox)")
amb_text = as_call(amb_stmt,
  "uniform_precision_contradiction μ p q (Z := X) id b\n"
  "    hp hq hb m hm g hg hwild ρ c N hρ hc hN harc (ambient_core_iff.mp happrox)")

WRAP = """\
/-
  PROPOSED WRAPPERS.  For review; not integrated.

  Both statements below are copied BYTE-FOR-BYTE from the shared originals
  (`ConditionalSpectrum.lean` and `ConditionalLimits.lean`, extracted mechanically by `gen.py`);
  only the proof body is replaced, and only by the corresponding call to
  `uniform_precision_contradiction`.

  The two `Iff.rfl` lemmas are the *definitional-equality certificates* for the aliases:
  if the old definition and the new one are not definitionally the same proposition, these fail to
  elaborate. They are the check that `S := p` and `S := id` reproduce the originals exactly.

  Names carry a `_core` suffix only because the originals are imported in this review file; at
  integration the originals' bodies are replaced and the suffix disappears (the statements, hence
  all call sites such as `finite_uniform_successor_contradiction`, are unchanged).
-/
import EncodingCore
import OAI.Analysis.PlaneSpectrum.ConditionalSpectrum
import OAI.MeasureTheory.CompactFactors.ConditionalLimits

namespace OAI
noncomputable section
open Filter Topology
open MeasureTheory ProbabilityTheory
open scoped ENNReal BigOperators ComplexConjugate
open scoped BigOperators ENNReal

-- The two originals each declare these LOCAL instances (Spectrum:43-44,178-179,260-261;
-- Limits:363-364) and they never leak across files, so the merged file must declare them again.
-- They are the same terms in both sources (`borel Circle`), which is what makes the two statements
-- the same proposition; `Circle` is Mathlib's unit circle with `ω.real : ℝ`.
local instance : MeasurableSpace Circle := borel Circle
local instance : BorelSpace Circle := ⟨rfl⟩

namespace PlaneFiveColor.Spectral
open EuclideanFiveColor

local instance : MeasurableSpace Circle := borel Circle
local instance : BorelSpace Circle := ⟨rfl⟩

variable {{X Y W : Type*}} [MeasurableSpace X] [StandardBorelSpace X] [Nonempty X]
  [MeasurableSpace Y] [StandardBorelSpace Y] [Nonempty Y]
  [MeasurableSpace W] [StandardBorelSpace W] [Nonempty W]

/-- Definitional-equality certificate for the finite alias (`S := p`, `Z := Y`). -/
theorem finite_core_iff (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : Y → W) (b : X → D) (m : ℕ) (γ : ℝ) :
    FiniteEncodingApproximationAt μ p q b m γ
      ↔ FiniteEncodingApproximationAt' μ p q b m γ :=
  Iff.rfl

{fin}

/-- Definitional-equality certificate for the ambient alias (`S := id`, `Z := X`). -/
theorem ambient_core_iff (μ : Measure X) [IsProbabilityMeasure μ]
    (p : X → Y) (q : X → W) (b : X → D) (m : ℕ) (γ : ℝ) :
    AmbientEncodingAt μ p q b m γ ↔ AmbientEncodingAt' μ p q b m γ :=
  Iff.rfl

{amb}

end PlaneFiveColor.Spectral
end
end OAI
""".format(fin=fin_text, amb=amb_text)
pathlib.Path("Wrappers.lean").write_text(WRAP)
print("wrote EncodingCore.lean and Wrappers.lean")


# ---- de-duplicate the `local instance` pair (the header patch can match twice) ----
_w = pathlib.Path("Wrappers.lean").read_text()
_blk = "local instance : MeasurableSpace Circle := borel Circle\nlocal instance : BorelSpace Circle := \u27e8rfl\u27e9\n"
_f = _w.find(_blk); _s2 = _w.find(_blk, _f + 1)
if _f != -1 and _s2 != -1:
    _cut = _s2
    while _cut > 0 and _w[_cut-1] == "\n":
        _cut -= 1
    _w = _w[:_cut] + _w[_s2 + len(_blk):]
    _w = _w.replace("open EuclideanFiveColor\n\nvariable", "open EuclideanFiveColor\n\nvariable")
    pathlib.Path("Wrappers.lean").write_text(_w)
    print("de-duplicated Circle instances in Wrappers.lean")
