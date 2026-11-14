"""Independent complete path reconstruction audit of the bounded AC enumeration."""
import contextlib
import importlib.util
import io
import itertools
import json
from pathlib import Path

root = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("candidate", root / "ac_filter_enum.py")
m = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(m)

def witness(lists):
    for p0 in lists[0]:
        paths = {p0: [p0]}
        for choices in lists[1:]:
            following = {}
            for p in choices:
                for last, path in paths.items():
                    if not p & last:
                        following[p] = path + [p]
                        break
            paths = following
        for last, path in paths.items():
            if not last & p0:
                return path
    return None

counts = dict(total=0, pass_ac=0, true_survivors=0, old_survivors=0)
missed, survivors = [], []
for tail in itertools.product(range(6), repeat=5):
    q = (0,) + tail
    counts['total'] += 1
    if m.ac_exclusion(q):
        continue
    counts['pass_ac'] += 1
    lists = m.allowed_lists(q)
    true, old = witness(lists), m.cycle_feasible(lists)
    counts['old_survivors'] += old is not None
    if true is None:
        assert old is None
        continue
    counts['true_survivors'] += 1
    assert len(true) == 6
    assert all(p in lists[j] for j, p in enumerate(true))
    assert all(not true[j] & true[(j + 1) % 6] for j in range(6))
    entry = dict(q=q, palettes=[[i for i in range(6) if p >> i & 1] for p in true])
    survivors.append(entry)
    if old is None:
        missed.append(entry)

report = dict(counts=counts, missed=missed, survivors=survivors,
              scope='Finite relaxation only; conditional on AC and all source premises.')
(root / 'ac-independent-audit.json').write_text(json.dumps(report, indent=2), encoding='utf8')
print(json.dumps(dict(counts=counts, missed=missed[:3], first=survivors[:1]), indent=2))
