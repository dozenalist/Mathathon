"""Package the completed draft and its explicitly selected supporting files."""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile

draft = Path(__file__).resolve().parents[1]
root = draft.parent
output = root / "output"
output.mkdir(exist_ok=True)
original = json.loads((root / "sources" / "source_ledger.json").read_text(encoding="utf-8"))
source_pdf = root / "sources" / "Fauzan_2026_zeta5.pdf"
source_hash = hashlib.sha256(source_pdf.read_bytes()).hexdigest()
assert source_hash == original["primary_source"]["sha256"]

primary = dict(original["primary_source"])
primary["use"] = "Structural source for Sections 1-7 and Appendices A-C of the order-nine analogue."
primary["audit_scope"] = (
    "Local ninth-order manipulations drafted section by section. Inner analytic "
    "transfer left formal/conditional. Original Appendix A interval certificate reused. "
    "Revised Appendix B rational integrals checked exactly. No irrationality claim."
)
ledger = {
    "date": "2026-11-14", "title": "A formal zeta(9) analogue of Fauzan's construction",
    "primary_source": primary,
    "supporting_primary_references": original["supporting_primary_references"],
    "prior_exploration_context": {
        "ledger_in_bundle": "sources/original_exploration_source_ledger.json",
        "notes": "Earlier seventh-order notes and ninth-order finite check informed the draft. Prior web discovery sources are retained in the original ledger; they are not independent proof verification.",
    },
    "section_agents": {
        "model": "gpt-6-astra", "reasoning_effort": "xhigh", "count": 6,
        "assignments": ["Section 2", "Section 3", "Section 4", "Section 5 and Appendix B", "Section 6 and Appendix A", "Section 7 and Appendix C"],
    },
    "checks": {
        "exact_arithmetic": "checks/section5_exact.mjs and section5_exact_results.json",
        "prior_finite_example": "prior_checks/exact_checks.py and zeta9_local_check.json",
        "layout": "30 pages rendered with Poppler and visually reviewed; no unresolved references, duplicate labels, or TeX overflow warnings.",
    },
    "tooling": {
        "typesetter": "Tectonic 0.17.0, standard cached LaTeX resources",
        "official_release": "https://github.com/tectonic-typesetting/tectonic/releases/tag/tectonic@0.17.0",
        "note": "Executable and resource cache excluded from source bundle.",
    },
}
(draft / "source_ledger.json").write_text(json.dumps(ledger, indent=2, ensure_ascii=False), encoding="utf-8")
final_pdf = output / "zeta9_formal_analogue.pdf"
shutil.copy2(draft / "build" / "zeta9_formal_analogue.pdf", final_pdf)

selected = {
    "zeta9_formal_analogue.pdf": final_pdf,
    "zeta9_formal_analogue.tex": draft / "zeta9_formal_analogue.tex",
    "README.txt": draft / "README.txt",
    "editorial_contract.txt": draft / "editorial_contract.txt",
    "coordination_log.txt": draft / "coordination_log.txt",
    "source_ledger.json": draft / "source_ledger.json",
    "sources/Fauzan_2026_zeta5.pdf": source_pdf,
    "sources/Fauzan_2026_zeta5.txt": root / "sources" / "Fauzan_2026_zeta5.txt",
    "sources/original_exploration_source_ledger.json": root / "sources" / "source_ledger.json",
    "prior_checks/exact_checks.py": root / "experiments" / "exact_checks.py",
    "prior_checks/zeta9_local_check.json": root / "experiments" / "zeta9_local_check.json",
    "prior_checks/zeta9_parity_notes.txt": root / "zeta9_parity_notes.txt",
    "validation/document_check.json": draft / "build" / "document_check.json",
    "validation/compile.log": draft / "build" / "zeta9_formal_analogue.log",
    "checks/section5_exact.mjs": draft / "checks" / "section5_exact.mjs",
    "checks/section5_exact_results.json": draft / "checks" / "section5_exact_results.json",
}
for path in sorted((draft / "parts").iterdir()):
    if path.suffix in {".tex", ".txt"}:
        selected[f"parts/{path.name}"] = path
assert all(path.is_file() for path in selected.values())
manifest = {name: {"bytes": path.stat().st_size,
                   "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            for name, path in selected.items()}
(draft / "bundle_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
zip_path = output / "zeta9_draft_sources.zip"
with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
    for name, path in selected.items():
        bundle.write(path, name)
    bundle.writestr("bundle_manifest.json", json.dumps(manifest, indent=2))
    bundle.writestr("prior_checks/REPRODUCE.txt", """The helper functions support arbitrary odd order s.
To reproduce the ninth-order constant-coefficient example from this directory:

python -c "import exact_checks as e; A=[[z[0] for z in row] for row in e.matrix_affine(9,40,3)]; print(e.valuation(e.det(A),29)); print(e.determinant_valuation_modular(A,29)); print(e.valuation(e.scalar(40,3),29))"

Expected determinant valuation -104 and scalar valuation 14.
This reproduces a previously completed finite check, not an asymptotic proof.
""")
with zipfile.ZipFile(zip_path) as bundle:
    assert bundle.testzip() is None
print(json.dumps({"pdf": str(final_pdf), "pdf_bytes": final_pdf.stat().st_size,
                  "source_bundle": str(zip_path), "bundle_bytes": zip_path.stat().st_size,
                  "files": len(selected)+2, "source_hash_verified": source_hash}, indent=2))
