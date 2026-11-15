"""Per-module before/after chart of the Lean simplification (ENC-R4, R1, S1).
All numbers are parsed from the results ledger (../../results-ledger.json): each entry's
statement lists "Module a→b" physical line counts. Run with Python 3 + matplotlib.
Writes simplification-modules.svg and .png next to this script, and prints the table it used."""
import json, re
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
LEDGER = HERE.parent.parent / "results-ledger.json"
data = json.loads(LEDGER.read_text(encoding="utf-8"))
items = data if isinstance(data, list) else (data.get("entries") or data.get("results") or list(data.values())[0])
byid = {e["id"]: e for e in items if isinstance(e, dict) and "id" in e}

pat = re.compile(r"([A-Z][A-Za-z]+)(?:\.lean)? (\d+)\s*(?:→|->)\s*(\d+)")
newmod = re.compile(r"([A-Z][A-Za-z]+) new \(\+(\d+)\)")
first, last, stage_of = {}, {}, {}
for stage in ["ENC-R4", "R1", "S1"]:
    text = byid[stage]["statement"]
    for m in pat.finditer(text):
        mod, a, b = m.group(1), int(m.group(2)), int(m.group(3))
        first.setdefault(mod, a); last[mod] = b; stage_of.setdefault(mod, []).append(stage)
    for m in newmod.finditer(text):
        mod, b = m.group(1), int(m.group(2))
        first.setdefault(mod, 0); last[mod] = b; stage_of.setdefault(mod, []).append(stage)

rows = sorted(first, key=lambda k: last[k] - first[k])
total = sum(last[k] - first[k] for k in rows)
print(f"{'module':22s} {'before':>6s} {'after':>6s} {'delta':>6s}  stages")
for k in rows:
    print(f"{k:22s} {first[k]:6d} {last[k]:6d} {last[k]-first[k]:+6d}  {'+'.join(stage_of[k])}")
print("total delta", total)

INK, RED, BLUE, GREY = "#172c43", "#b33d39", "#235f9d", "#63758a"
fig, ax = plt.subplots(figsize=(12, 6.4), dpi=150)
y = range(len(rows))
ax.barh([i + 0.2 for i in y], [first[k] for k in rows], height=0.4, color="#cfd8e3", label="supplied original")
ax.barh([i - 0.2 for i in y], [last[k] for k in rows], height=0.4, color=BLUE, label="team build (after S1)")
for i, k in enumerate(rows):
    d = last[k] - first[k]
    ax.text(max(first[k], last[k]) + 12, i, f"{d:+d}", va="center", fontsize=12,
            color=RED if d < 0 else GREY, fontweight="bold")
ax.set_yticks(list(y)); ax.set_yticklabels(rows, fontsize=12)
ax.set_xlabel("physical lines per module", color=INK, fontsize=12)
ax.set_title(f"Lean simplification by module: net {total:+d} lines (ENC-R4, R1, S1)", color=INK, fontsize=14)
ax.legend(loc="upper right", fontsize=12, frameon=False)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.set_xlim(0, max(max(first.values()), max(last.values())) * 1.12)
fig.tight_layout()
fig.savefig(HERE / "simplification-modules.svg")
fig.savefig(HERE / "simplification-modules.png")
print("wrote simplification-modules.svg/.png")
