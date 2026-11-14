#!/usr/bin/env python3
"""Reproducible audit of the claim that Section 7 of the five-colour paper uses
no palette-cardinality bound and depends on the number of colours only through
three explicit constants.

The script extracts the text of Section 7 (printed pages 42-50) from the paper's
PDF with pdftotext -layout, and reports

  (1) every occurrence in Section 7 of a citation of Section 5 material
      (5.2), (5.3), (5.5), (5.6), (5.7), Lemma 5.5, Proposition 5.6, "palette",
      "two labels")  -- expected: none;
  (2) every occurrence of the words five/five's, with the line, so that each can
      be checked by hand to be one of the three allowed shapes
      ("the five probabilities sum to one", "complete graph on its five vertices",
      "simple cycles in the complete graph on five vertices");
  (3) the three k-dependent constants of Section 7: the bound on alpha, the
      number of vertices of the target graph G, and the range of the cycle
      length ell.

Usage:
    python3 audit_s7.py [--pdf PATH] [--text PATH]

Exit code 0 means: (1) is empty and (3) was found as expected.
"""
import argparse, re, subprocess, sys, os

DEFAULT_PDF = ("../../../attachments/here-are-three-files-ni5n/paper.pdf")

def get_text(args):
    if args.text:
        return open(args.text, encoding="utf-8", errors="replace").read()
    pdf = args.pdf or DEFAULT_PDF
    if not os.path.exists(pdf):
        sys.exit("pdf not found: %s (pass --pdf or --text)" % pdf)
    return subprocess.run(["pdftotext", "-layout", pdf, "-"],
                          capture_output=True, text=True, check=True).stdout

def section7(text):
    a = text.find("Extraction of common exclusion continua")
    b = text.find("Angular obstructions and the final contradiction")
    if a < 0 or b < 0 or b <= a:
        sys.exit("could not locate Section 7 in the extracted text")
    return text[a:b]

BANNED = [r"\(5\.2\)", r"\(5\.3\)", r"\(5\.5\)", r"\(5\.6\)", r"\(5\.7\)",
          r"Lemma 5\.5", r"Proposition 5\.6", r"palette", r"two labels",
          r"\|P", r"cardinality"]

ALLOWED_FIVE = ["five probabilities sum to one",
                "complete graph on its five vertices",
                "simple cycles in the complete graph on five vertices"]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--pdf"); p.add_argument("--text")
    args = p.parse_args()
    s7 = section7(get_text(args))
    lines = s7.splitlines()
    print("Section 7 extracted: %d lines, %d characters\n" % (len(lines), len(s7)))

    print("(1) Section 5 citations and palette-cardinality language inside Section 7:")
    hits = 0
    for i, ln in enumerate(lines):
        for pat in BANNED:
            if re.search(pat, ln, flags=re.IGNORECASE):
                print("   line %4d: %s" % (i, ln.strip()))
                hits += 1
                break
    print("   total:", hits, "(expected 0)\n")

    print("(2) every occurrence of 'five' in Section 7, and its shape:")
    five = 0
    for i, ln in enumerate(lines):
        if re.search(r"\bfive\b|\bfive's\b", ln, flags=re.IGNORECASE):
            five += 1
            ok = any(a in ln for a in ALLOWED_FIVE)
            print("   line %4d: %s   [%s]" % (i, ln.strip(),
                                              "allowed" if ok else "CHECK BY HAND"))
    print("   total:", five, "\n")

    print("(3) the three k-dependent constants of Section 7:")
    for pat, what in [(r"Fix 0 < \S+\s*<\s*\S+", "alpha bound"),
                      (r"complete graph on its \w+ vertices", "G = K_k"),
                      (r"length \S+\s*\S*\s*\{[^}]*\}", "range of ell")]:
        found = [ln.strip() for ln in lines if re.search(pat, ln)]
        print("   %-14s %s" % (what, found if found else "NOT FOUND"))
    ok = (hits == 0 and five >= 3)
    print("\naudit passes:", ok)
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
