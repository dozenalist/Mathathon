#!/usr/bin/env python3
"""Render-based formula extraction with sub/superscript reconstruction.

Purpose: verify the displayed formulas used in the audit against the *rendered*
page (glyph positions and font sizes), not against a flat text extraction.
Two independent extractors are used: pdftotext -layout (see the audit report for
the commands) and this script, which reads the glyph geometry produced by
`mutool draw -F stext.json`.

Method.  For every page, spans are grouped into lines by vertical position.
Inside a line the dominant font size is the mode; a span whose size is at most
0.85 of it is a script.  A script span is a superscript when its bbox bottom is
above the dominant baseline range, a subscript otherwise.  Consecutive script
spans are accumulated into one ^{...} / _{...} group.  Delimiters that pdftex
renders as extensible glyphs (the failure mode of the (8.6) trap) survive as
ordinary characters here because the glyph code is read from the content
stream, so a missing/extra parenthesis is visible.

Usage:  python3 formula_check.py PDF PAGES...   (prints reconstructed lines)
        python3 formula_check.py PDF --grep PAGES SUBSTR   (lines containing SUBSTR)
"""
import json
import subprocess
import sys
import tempfile
import os
from collections import Counter


def page_spans(pdf, page, workdir):
    out = os.path.join(workdir, "p%d.json" % page)
    subprocess.run(
        ["mutool", "draw", "-F", "stext.json", "-o", out, pdf, str(page)],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(out) as fh:
        doc = json.load(fh)
    spans = []
    for pg in doc["pages"]:
        for blk in pg["blocks"]:
            # mutool's stext.json stores *spans* under the key "lines"
            for sp in blk.get("lines", []):
                if isinstance(sp, dict) and "text" in sp:
                    spans.append(sp)
    return spans


def group_lines(spans):
    """Group spans into lines by vertical overlap of their bboxes."""
    spans = [s for s in spans if s.get("text", "").strip() != "" or True]
    spans.sort(key=lambda s: (s["bbox"]["y"] + s["bbox"]["h"] / 2.0, s["bbox"]["x"]))
    lines = []
    for s in spans:
        cy = s["bbox"]["y"] + s["bbox"]["h"] / 2.0
        h = max(s["bbox"]["h"], 1.0)
        placed = False
        for ln in lines:
            if abs(ln["cy"] - cy) < 0.45 * max(ln["h"], h):
                ln["spans"].append(s)
                n = len(ln["spans"])
                ln["cy"] = (ln["cy"] * (n - 1) + cy) / n
                ln["h"] = max(ln["h"], h)
                placed = True
                break
        if not placed:
            lines.append({"cy": cy, "h": h, "spans": [s]})
    for ln in lines:
        ln["spans"].sort(key=lambda s: s["bbox"]["x"])
    lines.sort(key=lambda ln: ln["cy"])
    return lines


def render_line(ln):
    sizes = Counter()
    for s in ln["spans"]:
        sizes[round(s["font"]["size"], 1)] += len(s["text"])
    main = sizes.most_common(1)[0][0]
    # dominant baseline: bottom of the bbox of the main-size glyphs
    bottoms = [s["bbox"]["y"] + s["bbox"]["h"] for s in ln["spans"]
               if round(s["font"]["size"], 1) == main]
    base = sum(bottoms) / len(bottoms) if bottoms else ln["cy"]

    out = []
    mode = None
    for s in ln["spans"]:
        size = round(s["font"]["size"], 1)
        text = s["text"]
        if size <= 0.85 * main + 1e-9:
            bottom = s["bbox"]["y"] + s["bbox"]["h"]
            kind = "sup" if bottom < base - 0.5 else "sub"
            if kind != mode:
                if mode is not None:
                    out.append("}" if mode == "sup" else "]")
                out.append("^{" if kind == "sup" else "_[")
                mode = kind
            out.append(text)
        else:
            if mode is not None:
                out.append("}" if mode == "sup" else "]")
                mode = None
            out.append(text)
    if mode is not None:
        out.append("}" if mode == "sup" else "]")
    return "".join(out)


def main():
    pdf = sys.argv[1]
    args = sys.argv[2:]
    grep = None
    if args and args[0] == "--grep":
        grep = args[1]
        args = args[2:]
    with tempfile.TemporaryDirectory() as td:
        for pg in args:
            print("=== page %s ===" % pg)
            for ln in group_lines(page_spans(pdf, int(pg), td)):
                txt = render_line(ln)
                if grep is None or grep in txt:
                    print(txt)


if __name__ == "__main__":
    main()
