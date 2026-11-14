"""Measure the formal cost of the transfer (paper Theorem 1.3) in the Lean development.

Reads lean/OAI/**/*.lean, builds the import graph, and reports:
  * the transitive closure of each entry point (modules, lines);
  * the part of the forward transfer's closure that is reachable ONLY through
    OAI.Analysis.PlaneSpectrum.Ergodicity, i.e. the rigidity layer (paper Theorem 2.3);
  * every use site of the interface lemma, outside its own module.

Run from the repository root:  python3 .ultramath/smwfk0ybk/m5/closure_measure.py
"""
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'lean')
RIGIDITY = 'OAI.Analysis.PlaneSpectrum.Ergodicity'


def load(root=ROOT):
    mods = {}
    for dp, _, fn in os.walk(os.path.join(root, 'OAI')):
        for f in fn:
            if not f.endswith('.lean'):
                continue
            p = os.path.join(dp, f)
            m = os.path.relpath(p, root)[:-5].replace('/', '.')
            txt = open(p, encoding='utf-8', errors='replace').read()
            mods[m] = {'lines': txt.count('\n') + 1,
                       'imports': re.findall(r'^import\s+(\S+)', txt, re.M),
                       'text': txt}
    return mods


def closure(mods, m, seen=None):
    if seen is None:
        seen = set()
    if m in seen:
        return seen
    seen.add(m)
    for i in mods.get(m, {'imports': []})['imports']:
        if i.startswith('OAI'):
            closure(mods, i, seen)
    return seen


def total(mods, s):
    return sum(mods[m]['lines'] for m in s if m in mods)


def main():
    mods = load()
    print(f"{len(mods)} modules, {total(mods, mods)} lines\n")
    targets = {
        'forward transfer (Prop 4.2)': 'OAI.Geometry.PlaneColoring.BorelTransfer',
        'backward transfer (Lemma 4.3)': 'OAI.Geometry.PlaneColoring.Converse',
        'Theorem 1.3 (both)': 'OAI.Geometry.PlaneColoring.Transfer',
    }
    for name, t in targets.items():
        c = closure(mods, t)
        print(f"{name}: {len(c)} modules, {total(mods, c)} lines  [{t}]")

    full = closure(mods, 'OAI.Geometry.PlaneColoring.BorelTransfer')
    saved = mods[RIGIDITY]['imports']
    mods[RIGIDITY]['imports'] = []                    # pretend the rigidity layer is free
    lean = closure(mods, 'OAI.Geometry.PlaneColoring.BorelTransfer')
    mods[RIGIDITY]['imports'] = saved
    gone = full - lean
    print(f"\nreachable ONLY through {RIGIDITY}:")
    print(f"  {len(gone)} modules, {total(mods, gone)} lines")
    print(f"  = {100 * total(mods, gone) / total(mods, full):.1f}% of the forward transfer's closure")
    print(f"  transfer proper (everything else): {len(lean)} modules, {total(mods, lean)} lines")
    for m in sorted(gone):
        print(f"    {mods[m]['lines']:6d}  {m}")

    print("\nuse sites of the interface lemma, outside its own module:")
    for m, d in sorted(mods.items()):
        if m == RIGIDITY:
            continue
        for n, line in enumerate(d['text'].split('\n'), 1):
            if 'residual_fourier' in line:
                print(f"  {m}:{n}: {line.strip()}")
    print("\ndefinition of the interface lemma:")
    for n, line in enumerate(mods[RIGIDITY]['text'].split('\n'), 1):
        if 'lemma residual_fourier' in line:
            print(f"  {RIGIDITY}:{n}")
            for k in range(n, n + 3):
                print("    " + mods[RIGIDITY]['text'].split('\n')[k].strip())
    return 0


if __name__ == '__main__':
    sys.exit(main())
