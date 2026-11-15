# Revised framework companion and supporting notes

Start with [One summation functional, one Gram pencil](zeta5_unified_framework.pdf), the 14 November 2026 explanatory companion to Fauzan's argument. [The LaTeX source](zeta5_unified_framework.tex) includes the final attribution corrections from the originating chat. This revision is newer than the earlier formalization input preserved in `ZetaFive/Literature/ParallelConstructions/`.

The companion distinguishes exact identities and elementary corollaries from the source's arithmetic and energy certificates. It is not an independent certification of the entire irrationality argument. Most structural connections are already explicit in Fauzan's manuscript; the final provenance table records the distinction.

The `framework_*_notes.txt` files preserve detailed derivations for the functional, arithmetic, and determinant families. The `audit_*.txt` files preserve correctness reviews. The `provenance_*.txt` files compare the proposed interpretations with Fauzan's original. These working notes include references to earlier line numbers and occasional provisional originality assessments; the **final revised companion and provenance reviews take precedence**.

Run the existing check script from this folder with Python 3:

```sh
python framework_checks.py
```

It requires only the standard library and rewrites `framework_checks.json` in the working directory. Its exact finite checks and numerical sanity checks verify the displayed identifications in specified examples, not all quantitative proof inputs.

Build the PDF using a standard LaTeX distribution with the packages declared in the source, or Tectonic:

```sh
tectonic --untrusted zeta5_unified_framework.tex
```

The PDF is preserved from the originating chat's compiled and visually checked artifact. No TeX cache, executable, preview image, or compilation log is needed in this folder.
