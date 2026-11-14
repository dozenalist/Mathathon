import re, os, sys, json, collections
ROOT = sys.argv[1]
files = {}
for dirpath, _, fs_ in os.walk(ROOT):
    for f in sorted(fs_):
        if f.endswith('.lean'):
            p = os.path.join(dirpath, f)
            mod = 'OAI.' + os.path.relpath(p, ROOT)[:-5].replace('/', '.')
            files[p.replace(ROOT + '/', '')] = mod
mod2file = {v: k for k, v in files.items()}
imports = {}
for f in files:
    src = open(os.path.join(ROOT, f)).read()
    imports[f] = [m for m in re.findall(r'^import\s+(\S+)', src, re.M)]
# closure
def closure(mod, seen=None):
    seen = set() if seen is None else seen
    for m in imports.get(mod2file.get(mod, ''), []):
        if m not in seen:
            seen.add(m)
            closure(m, seen)
    return seen
json.dump(imports, open('.scratch/imports.json', 'w'), indent=0)
# report: for each OAI module, its OAI deps
print("module -> direct OAI imports")
for f in sorted(files):
    oai = [m for m in imports[f] if m.startswith('OAI')]
    print(f"{files[f]:55s} {oai}")
