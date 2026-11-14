import re, os, sys, json, collections

ROOT = sys.argv[1]

decl_re = re.compile(r'^[ \t]*(?:@\[[^\]]*\][ \t]*)?'
                     r'(?:private[ \t]+|protected[ \t]+|noncomputable[ \t]+|local[ \t]+|scoped[ \t]+)*'
                     r'(theorem|lemma)[ \t]+([A-Za-z_][A-Za-z0-9_.\'!?]*)', re.M)

OPEN = '([{⟨⦃'
CLOSE = ')]}⟩⦄'

def scan(files):
    out = []
    for p in files:
        src = open(p).read()
        src = re.sub(r'/-.*?-/', lambda m: re.sub(r'[^\n]', ' ', m.group(0)), src, flags=re.S)
        src = re.sub(r'--[^\n]*', '', src)
        for m in decl_re.finditer(src):
            i = m.end()
            depth = 0
            j = i
            term = None
            while j < len(src):
                c = src[j]
                if c in OPEN: depth += 1
                elif c in CLOSE: depth -= 1
                elif depth <= 0 and src.startswith(':=', j):
                    term = j; break
                elif depth <= 0 and c == '\n':
                    k = j + 1
                    while k < len(src) and src[k] in ' \t': k += 1
                    if src.startswith('where', k) or (src.startswith('by', k) and (k+2 >= len(src) or not (src[k+2].isalnum() or src[k+2] in "_'"))):
                        term = j; break
                j += 1
            if term is None: term = len(src)
            stmt = re.sub(r'\s+', ' ', src[i:term]).strip()
            line = src.count('\n', 0, m.start()) + 1
            endline = src.count('\n', 0, term) + 1
            out.append(dict(file=p.replace(ROOT + '/', ''), line=line, endline=endline,
                            kind=m.group(1), name=m.group(2), stmt=stmt))
    return out

files = []
for dirpath, _, fs_ in os.walk(ROOT):
    for f in sorted(fs_):
        if f.endswith('.lean'): files.append(os.path.join(dirpath, f))
files.sort()
decls = scan(files)
json.dump(decls, open('.scratch/decls.json', 'w'), indent=0)
print(len(decls), 'declarations')
groups = collections.defaultdict(list)
for d in decls:
    groups[d['stmt']].append(d)
dups = {k: v for k, v in groups.items() if len(v) > 1}
print(len(dups), 'duplicate statement groups')
for k, v in sorted(dups.items(), key=lambda kv: -len(kv[1])):
    print('=' * 70)
    print(f'[{len(v)} sites]', k[:400])
    for d in v:
        print(f'   {d["file"]}:{d["line"]}-{d["endline"]}  {d["name"]}')
