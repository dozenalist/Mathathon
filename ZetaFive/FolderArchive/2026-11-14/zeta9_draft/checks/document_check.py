"""Structural checks and contact sheets for the assembled draft (not a proof check)."""
from pathlib import Path
from collections import Counter
import json
import logging
import re
from PIL import Image, ImageDraw
from pypdf import PdfReader

# Text extraction is only a reference check. Visual QA uses Poppler renders.
logging.getLogger("pypdf").setLevel(logging.ERROR)

draft = Path(__file__).resolve().parents[1]
files = [draft / "zeta9_formal_analogue.tex", *sorted((draft / "parts").glob("*.tex"))]
source = "\n".join(p.read_text(encoding="utf-8") for p in files)
labels = Counter(re.findall(r"\\label\{([^}]+)\}", source))
references = set(re.findall(r"\\(?:eqref|ref)\{([^}]+)\}", source))
duplicates = [label for label, count in labels.items() if count > 1]
missing = sorted(references - labels.keys())
assert not duplicates, duplicates
assert not missing, missing

pdf = draft / "build" / "zeta9_formal_analogue.pdf"
reader = PdfReader(pdf)
texts = [page.extract_text() or "" for page in reader.pages]
assert all("??" not in text for text in texts), "Unresolved reference in PDF"
report = {
    "purpose": "Document structure and layout preparation, not mathematical validation",
    "page_count": len(texts), "unique_labels": len(labels),
    "missing_references": missing, "duplicate_labels": duplicates,
    "pages": [{"number": i+1, "first_lines": text.splitlines()[:3]} for i, text in enumerate(texts)],
}
(draft / "build" / "document_check.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

preview = draft / "build" / "preview_final"
pages = sorted(preview.glob("page-*.png"))
assert len(pages) == len(texts), "Render every page before making contact sheets"
for start in range(0, len(pages), 12):
    sheet = Image.new("RGB", (1440, 1470), "#dddddd")
    draw = ImageDraw.Draw(sheet)
    for offset, path in enumerate(pages[start:start+12]):
        img = Image.open(path).convert("RGB")
        img.thumbnail((340, 450))
        x = (offset % 4)*360 + 10
        y = (offset // 4)*490 + 25
        sheet.paste(img, (x, y))
        draw.text((x, y-19), f"Page {start+offset+1}", fill="black")
    sheet.save(preview / f"contact-{start//12+1}.png")
print(json.dumps({key: value for key, value in report.items() if key != "pages"}, indent=2))
for page in report["pages"]:
    print(json.dumps(page, ensure_ascii=True))
