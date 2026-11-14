#!/usr/bin/env python3
"""Generate the integration patch for the common encoding core.  UNCOMPILED generator.

Reads the shared originals READ-ONLY. Writes only under encoding-core/integration/.
Freezes every input hash, refuses to run if one moves, and audits DECLARATION ORDER inside
the patched files: any identifier used by an inserted block that is declared later in the
same file is a build error, so it is reported as a hard failure.
"""
import hashlib, json, pathlib, re, subprocess

EC   = pathlib.Path(__file__).resolve().parent
REPO = EC.parents[2]
SPEC = REPO / "lean/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean"
LIM  = REPO / "lean/OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean"
CORE = EC / "EncodingCore.lean"
OUT  = EC / "integration"
OUT.mkdir(exist_ok=True)

FROZEN = {
  "lean/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean":
     (SPEC, "6602b9d8f20bbdfd447f2f3fcfa523f2c33d09c247e3d2983be7503df9f2dc9b"),
  "lean/OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean":
     (LIM,  "ca74ba1033fead55133670218739a36b4c75173d9b04d765affd19da9d215cc0"),
}
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
moved = [k for k, (p, h) in FROZEN.items() if sha(p) != h]
if moved:
    raise SystemExit("SHARED ORIGINAL MOVED, refusing: " + ", ".join(moved))

L = SPEC.read_text().splitlines(); M = LIM.read_text().splitlines(); C = CORE.read_text().splitlines()
def idx(lines, pred, start=0):
    for i in range(start, len(lines)):
        if pred(lines[i]): return i
    raise SystemExit("marker not found")

# ---- blocks lifted verbatim from EncodingCore.lean ----
i = idx(C, lambda s: s.startswith("/-- The shared encoding hypothesis"))
j = idx(C, lambda s: s.startswith("/-- Definitional shadow of the old `FiniteEncodingApproximationAt`"))
GEN_DEF = [s for s in C[i:j] if True]
while GEN_DEF and GEN_DEF[-1].strip() == "": GEN_DEF.pop()
assert GEN_DEF[0].startswith("/--") and any("def EncodingApproximationAt" in s for s in GEN_DEF)
i = idx(C, lambda s: s.startswith("/-- Both uniform-precision contradictions are this statement"))
if C[i-1].strip().startswith("omit"): i -= 1          # `omit ... in` now precedes the doc comment
j = idx(C, lambda s: s.startswith("end"), i)
GEN_THM = C[i:j]
while GEN_THM and GEN_THM[-1].strip() == "": GEN_THM.pop()
assert any("uniform_precision_contradiction" in s for s in GEN_THM)
assert any("bounded_coefficient_bins" in s for s in GEN_THM), "proof body missing"
assert not any("sorry" in s for s in GEN_THM + GEN_DEF)

# ---------------- ConditionalSpectrum ----------------
i_def = idx(L, lambda s: s.startswith("def FiniteEncodingApproximationAt"))
j_def = idx(L, lambda s: s.startswith("def ") and "FiniteEncodingApproximationAt" not in s, i_def)
SPEC_ALIAS = [
 "/-- The encoding hypothesis read through `p`: definitionally `EncodingApproximationAt` at",
 "`S := p` (and `Z := Y`). Same binders, same order, same proposition. -/",
 "abbrev FiniteEncodingApproximationAt (μ : Measure X) [IsProbabilityMeasure μ] (p : X → Y)",
 "    (q : Y → W) (b : X → D) (m : ℕ) (γ : ℝ) : Prop :=",
 "  EncodingApproximationAt μ p (fun x => q (p x)) p b m γ",
 "",
]
i_thm = idx(L, lambda s: s.startswith("theorem finite_uniform_precision_contradiction"))
i_by  = idx(L, lambda s: s.rstrip().endswith(":= by"), i_thm)
i_end = idx(L, lambda s: s.startswith("omit ") or s.startswith("theorem "), i_by + 1) - 1
while L[i_end].strip() == "": i_end -= 1
# anchor a = the wrapper's own `omit ... in` line
a = i_thm
while not L[a].strip().startswith("omit"): a -= 1
SPEC_BODY = ["  exact uniform_precision_contradiction μ p (fun x => q (p x)) (Z := Y) p b",
             "    hp (hq.comp hp) hb m hm g hg hwild ρ c N hρ hc hN harc happrox"]
# ORDER: generic def + alias early (nothing in them needs the helpers), common proof AFTER
# both helpers and immediately BEFORE the finite wrapper.
new = (L[:i_def] + GEN_DEF + [""] + SPEC_ALIAS            # def EncodingApproximationAt, abbrev
       + L[j_def:a]                                       # FiniteEncodingApproximation, helpers
       + GEN_THM + [""]                                   # the common theorem (uses the helpers)
       + L[a:i_thm] + L[i_thm:i_by+1] + SPEC_BODY         # the finite wrapper, body replaced
       + L[i_end+1:])
P_SPEC = OUT / "OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean"
P_SPEC.parent.mkdir(parents=True, exist_ok=True); P_SPEC.write_text("\n".join(new) + "\n")

# ---------------- ConditionalLimits ----------------
k_def = idx(M, lambda s: s.startswith("def AmbientEncodingAt"))
k_end = idx(M, lambda s: s.startswith("omit "), k_def)
LIM_ALIAS = [
 "/-- The encoding hypothesis read through `id`: definitionally `EncodingApproximationAt` at",
 "`S := id` (and `Z := X`). Same binders, same order, same proposition. -/",
 "abbrev AmbientEncodingAt (μ : Measure X) [IsProbabilityMeasure μ] (p : X → Y) (q : X → W)",
 "    (b : X → D) (m : ℕ) (γ : ℝ) : Prop :=",
 "  EncodingApproximationAt μ p q id b m γ",
 "",
]
k_thm = idx(M, lambda s: s.startswith("theorem ambient_uniform_precision_contradiction"))
k_by  = idx(M, lambda s: s.rstrip().endswith(":= by"), k_thm)
k_endthm = idx(M, lambda s: s.startswith("end PlaneFiveColor.Spectral"), k_by) - 1
while M[k_endthm].strip() == "": k_endthm -= 1
LIM_BODY = ["  exact uniform_precision_contradiction μ p q (Z := X) id b",
            "    hp hq hb m hm g g hg hwild ρ c N hρ hc hN harc happrox"]
LIM_BODY[1] = "    hp hq hb m hm g hg hwild ρ c N hρ hc hN harc happrox"
newM = M[:k_def] + LIM_ALIAS + M[k_end:k_thm] + M[k_thm:k_by+1] + LIM_BODY + M[k_endthm+1:]
# --- R4 downstream adaptation (adopted verbatim; one line, no hypothesis changed) ------------
# The alias phrases the conversion lemma's goal as `… • Hf i (id x) …`, so the old closing term
# `by rw [← integral_congr_ae he]; exact hae` no longer matches. Replace that term only.
OLD_TERM = "by rw [← integral_congr_ae he]; exact hae"
NEW_TERM = "by simpa only [id_eq] using ((integral_congr_ae he) ▸ hae)"
joined = "\n".join(newM)
assert joined.count(OLD_TERM) == 1, joined.count(OLD_TERM)
newM = joined.replace(OLD_TERM, NEW_TERM).split("\n")
assert any(NEW_TERM in l for l in newM)
P_LIM = OUT / "OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean"
P_LIM.parent.mkdir(parents=True, exist_ok=True); P_LIM.write_text("\n".join(newM) + "\n")

# ---------------- DECLARATION-ORDER AUDIT (the bug found by the local source audit) ----------
DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:private |protected |noncomputable |partial |unsafe )*"
                  r"(?:def|lemma|theorem|abbrev|instance|structure|class|inductive)\s+"
                  r"([A-Za-z_][\w'.]*)")
def decls(lines):
    d = {}
    for n, s in enumerate(lines, 1):
        m = DECL.match(s)
        if m: d.setdefault(m.group(1), n)
    return d
def code_only(ls):
    """Strip Lean comments/docstrings (line and block) so the audit sees code, not prose."""
    out, depth = [], 0
    for l in ls:
        buf, i = "", 0
        while i < len(l):
            if depth == 0 and l.startswith("/-", i):
                depth += 1; i += 2; continue
            if depth == 0 and l.startswith("--", i):
                break
            if depth > 0 and l.startswith("-/", i):
                depth -= 1; i += 2; continue
            if depth > 0:
                i += 1; continue
            buf += l[i]; i += 1
        out.append(buf)
    return out
def audit(lines, blocks, label):
    d = decls(lines)
    bad = []
    anchors = {}
    for name, blk in blocks.items():
        tgt = [i for i, s in enumerate(lines, 1) if len(blk) and blk[0][:40].strip() and blk[0].strip() in s]
        at = tgt[0] if tgt else None
        anchors[name] = at
        if at is None: bad.append((name, "ANCHOR NOT FOUND", None, None)); continue
        text = "\n".join(lines[at-1:])
        used = set()
        for nm, ln in d.items():
            if nm in name: continue
            if re.search(r"(?<![\w.'])" + re.escape(nm) + r"(?![\w'])", "\n".join(code_only(blk))):
                used.add((nm, ln))
        for nm, ln in sorted(used):
            if ln > at: bad.append((name, nm, ln, at))
    return {"label": label, "anchors": anchors,
            "forward_refs": [{"block": b, "identifier": i_, "decl_line": l, "block_line": at}
                             for b, i_, l, at in bad],
            "ok": not bad}
A_SPEC = audit(new,  {"EncodingApproximationAt": GEN_DEF, "uniform_precision_contradiction": GEN_THM,
                      "FiniteEncodingApproximationAt": SPEC_ALIAS}, "ConditionalSpectrum")
A_LIM  = audit(newM, {"AmbientEncodingAt": LIM_ALIAS}, "ConditionalLimits")
if not A_SPEC["ok"] or not A_LIM["ok"]:
    raise SystemExit("FORWARD REFERENCE: " + json.dumps([A_SPEC, A_LIM], indent=1)[:1200])

# ---------------- patches + apply check ----------------
def mkpatch(a_, b_, name, rel):
    r = subprocess.run(["diff", "-u", "--label", "a/" + rel, "--label", "b/" + rel, str(a_), str(b_)],
                       capture_output=True, text=True)
    (OUT / name).write_text(r.stdout); return r.stdout
REL_S = "lean/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean"
REL_L = "lean/OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean"
d1 = mkpatch(SPEC, P_SPEC, "0001-conditional-spectrum.patch", REL_S)
d2 = mkpatch(LIM,  P_LIM,  "0002-conditional-limits.patch", REL_L)
dry = OUT / "_dryrun"
if dry.exists(): subprocess.run(["rm", "-rf", str(dry)])
(dry / "lean/OAI/Analysis/PlaneSpectrum").mkdir(parents=True)
(dry / "lean/OAI/MeasureTheory/CompactFactors").mkdir(parents=True)
(dry / REL_S).write_bytes(SPEC.read_bytes()); (dry / REL_L).write_bytes(LIM.read_bytes())
log = []
for p in ("0001-conditional-spectrum.patch", "0002-conditional-limits.patch"):
    r = subprocess.run(["patch", "-p1", "--dry-run", "-i", str(OUT / p)], cwd=dry,
                       capture_output=True, text=True)
    log.append("$ patch -p1 --dry-run -i %s  ->  rc=%d\n%s" % (p, r.returncode, (r.stdout + r.stderr).strip()))
(OUT / "APPLY-CHECK.txt").write_text("\n\n".join(log) + "\n")
rc = [int(re.search(r"rc=(\d+)", l).group(1)) for l in log]
subprocess.run(["rm", "-rf", str(dry)])

# ---------------- statement delta ----------------
def stmt(lines, name):
    x = idx(lines, lambda s: s.strip().startswith("theorem " + name)); y = x
    while not lines[y].rstrip().endswith(":= by"): y += 1
    z = x
    while z > 0 and lines[z-1].strip() == "": z -= 1
    if lines[z-1].strip().startswith("omit"): z -= 1
    return "\n".join(lines[z:y+1])
delta = {}
for nm, o, p in (("finite_uniform_precision_contradiction", L, new),
                 ("ambient_uniform_precision_contradiction", M, newM)):
    so, sp = stmt(o, nm), stmt(p, nm)
    delta[nm] = {"identical": so == sp, "sha": hashlib.sha256(so.encode()).hexdigest()[:16]}

# ---------------- source-freeze manifest (closure + post-patch hashes) ----------------
def imports(p): return re.findall(r"^import\s+(\S+)", pathlib.Path(p).read_text(errors="ignore"), re.M)
def path_of(m): return REPO / ("lean/" + m.replace(".", "/") + ".lean")
roots = {"OAI.Analysis.PlaneSpectrum.ConditionalSpectrum", "OAI.MeasureTheory.CompactFactors.ConditionalLimits",
         "OAI.MeasureTheory.CompactFactors.Approximation"}
seen, stack, ml = set(), list(roots), set()
while stack:
    m = stack.pop()
    if m in seen: continue
    seen.add(m)
    for d in imports(path_of(m)):
        stack.append(d) if d.startswith("OAI.") else ml.add(d)
freeze = ["# Source freeze: the revision local compilation must target", "",
 "After applying both patches, these two files must hash to the stated values. Any other value",
 "means a different revision than the one reviewed here.", "",
 "| file (post-patch) | sha256 |", "|---|---|",
 "| `%s` | `%s` |" % (REL_S, sha(P_SPEC)),
 "| `%s` | `%s` |" % (REL_L, sha(P_LIM)),
 "", "| file (input, must stay unchanged) | sha256 |", "|---|---|"]
freeze += ["| `%s` | `%s` |" % (k, sha(v[0])) for k, v in FROZEN.items()]
freeze += ["", "## Root-closed OAI closure (%d modules), frozen" % len(seen), "", "| module | sha256 |", "|---|---|"]
freeze += ["| `%s` | `%s` |" % (m, sha(path_of(m))) for m in sorted(seen)]
freeze += ["", "## Mathlib", "", "Import roots in this closure: " + ", ".join("`%s`" % m for m in sorted(ml)),
 "", "Pinned toolchain: Lean 4.34.1 + mathlib `d13f23b723b8a846827a245b89c10fc7d3f11612` via",
 "`scripts/fetch_exact_env.sh`; do not substitute another cache.", "",
 "## Verify", "", "```bash", "cd <repo>",
 "sha256sum lean/OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean \\",
 "          lean/OAI/MeasureTheory/CompactFactors/ConditionalLimits.lean",
 "```", ""]
(OUT / "SOURCE-FREEZE.md").write_text("\n".join(freeze))

meta = {
 "generated_utc_note": "uncompiled textual candidate; no build in this block",
 "input_sha256": {k: sha(v[0]) for k, v in FROZEN.items()},
 "post_patch_sha256": {REL_S: sha(P_SPEC), REL_L: sha(P_LIM)},
 "patch_sha256": {p.name: sha(p) for p in sorted(OUT.glob("*.patch"))},
 "smoke_sha256": {p.name: sha(p) for p in sorted(OUT.glob("Smoke*.lean"))},
 "source_freeze_entry_count": len(seen),
 "input_lines": {"ConditionalSpectrum": len(L), "ConditionalLimits": len(M)},
 "output_lines": {"ConditionalSpectrum": P_SPEC.read_text().count("\n"),
                  "ConditionalLimits": P_LIM.read_text().count("\n")},
 "added_lines": {"ConditionalSpectrum": sum(1 for s in d1.splitlines() if s.startswith("+") and not s.startswith("+++")),
                 "ConditionalLimits": sum(1 for s in d2.splitlines() if s.startswith("+") and not s.startswith("+++"))},
 "removed_lines": {"ConditionalSpectrum": sum(1 for s in d1.splitlines() if s.startswith("-") and not s.startswith("---")),
                   "ConditionalLimits": sum(1 for s in d2.splitlines() if s.startswith("-") and not s.startswith("---"))},
 "net_line_change": {"ConditionalSpectrum": P_SPEC.read_text().count("\n") - len(L),
                     "ConditionalLimits": P_LIM.read_text().count("\n") - len(M)},
 "statement_delta": delta,
 "declaration_order_audit": {"ConditionalSpectrum": A_SPEC, "ConditionalLimits": A_LIM},
 "apply_check_rc": rc,
 "checks": {"no_import_added": ("+import" not in d1 and "+import" not in d2),
            "no_sorry": ("sorry" not in d1 and "sorry" not in d2),
            "body_present": ("bounded_coefficient_bins" in d1),
            "helpers_before_common_theorem":
                (idx(new, lambda s: s.startswith("lemma simultaneous_test_budget"))
                 < idx(new, lambda s: s.startswith("theorem uniform_precision_contradiction")))
                and (idx(new, lambda s: s.startswith("lemma two_array_norm_bound"))
                     < idx(new, lambda s: s.startswith("theorem uniform_precision_contradiction")))},
}
meta["net_line_change"]["total"] = sum(meta["net_line_change"].values())
(OUT / "META.json").write_text(json.dumps(meta, indent=1))
print(json.dumps({k: meta[k] for k in ("statement_delta", "net_line_change", "apply_check_rc",
      "declaration_order_audit", "checks")}, indent=1)[:1800])
print("\nanchors:", A_SPEC["anchors"], A_LIM["anchors"])
