import re, os, sys, json, collections
ROOT = sys.argv[1]

decl_re = re.compile(r'^[ \t]*(?:@\[[^\]]*\][ \t]*)?'
                     r'(?:private[ \t]+|protected[ \t]+|noncomputable[ \t]+|local[ \t]+|scoped[ \t]+)*'
                     r'(theorem|lemma)[ \t]+([A-Za-z_][A-Za-z0-9_.\'!?]*)', re.M)
OPEN = '([{⟨⦃'; CLOSE = ')]}⟩⦄'

def decls_of(p, src):
    out = []
    for m in decl_re.finditer(src):
        i = m.end(); depth = 0; j = i; term = None
        while j < len(src):
            c = src[j]
            if c in OPEN: depth += 1
            elif c in CLOSE: depth -= 1
            elif depth <= 0 and src.startswith(':=', j): term = j; break
            elif depth <= 0 and c == '\n':
                k = j + 1
                while k < len(src) and src[k] in ' \t': k += 1
                if src.startswith('where', k) or (src.startswith('by', k) and (k+2 >= len(src) or not (src[k+2].isalnum() or src[k+2] in "_'"))):
                    term = j; break
            j += 1
        if term is None: term = len(src)
        stmt = re.sub(r'\s+', ' ', src[i:term]).strip()
        line = src.count('\n', 0, m.start()) + 1
        # proof body = from term to next decl start (or EOF)
        nxt = decl_re.search(src, term)
        body_end = nxt.start() if nxt else len(src)
        body = src[term:body_end]
        out.append(dict(file=p, line=line, name=m.group(2), stmt=stmt, body=body,
                        blines=body.count('\n')))
    return out

all_d = []
for dirpath, _, fs_ in os.walk(ROOT):
    for f in sorted(fs_):
        if not f.endswith('.lean'): continue
        pfull = os.path.join(dirpath, f)
        p = pfull.replace(ROOT + '/', '')
        src = open(pfull).read()
        src_nc = re.sub(r'/-.*?-/', lambda m: re.sub(r'[^\n]', ' ', m.group(0)), src, flags=re.S)
        src_nc = re.sub(r'--[^\n]*', '', src_nc)
        for d in decls_of(p, src_nc):
            d['file'] = p
            all_d.append(d)
print(len(all_d), 'decls')

# (a) identical normalised proof bodies, >=4 lines
bybody = collections.defaultdict(list)
for d in all_d:
    b = re.sub(r'\s+', '', d['body'])
    if d['blines'] >= 4:
        bybody[b].append(d)
samebody = [v for k, v in bybody.items() if len(v) > 1]
print(f'\n### identical proof bodies: {len(samebody)} clusters')
for v in sorted(samebody, key=lambda v: -len(v)):
    print('-' * 70)
    print(f'[{len(v)} sites] {v[0]["stmt"][:200]}')
    for d in v:
        print(f'   {d["file"]}:{d["line"]}  {d["name"]}  ({d["blines"]} body lines)')

# (b) group by conclusion (text after last top-level ':')
def concl(stmt):
    depth = 0; last = None
    for idx, c in enumerate(stmt):
        if c in OPEN: depth += 1
        elif c in CLOSE: depth -= 1
        elif c == ':' and depth == 0 and not stmt.startswith(':=', idx):
            last = idx
    return stmt[last+1:].strip() if last is not None else stmt
byconcl = collections.defaultdict(list)
for d in all_d:
    byconcl[concl(d['stmt'])].append(d)
same = [v for k, v in byconcl.items() if len(v) > 1 and len(k) > 10]
print(f'\n### identical conclusions: {len(same)} clusters')
for v in sorted(same, key=lambda v: -len(v))[:40]:
    print('-' * 70)
    print(f'[{len(v)} sites] CONCL: {concl(v[0]["stmt"])[:250]}')
    for d in v:
        print(f'   {d["file"]}:{d["line"]}  {d["name"]}')
json.dump(all_d, open('.scratch/decls2.json', 'w'))
