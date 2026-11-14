#!/usr/bin/env python3
"""Declaration-level census: for each declaration in a target module set,
count uses outside its declaring file (and outside its prefix module set)."""
import re, sys, pathlib, collections, json
ROOT = pathlib.Path(".")
DECL = re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*"
                  r"(theorem|lemma|def|abbrev|structure|class|instance|opaque|inductive)\s+([A-Za-z0-9_'.]+)")
def files():
    return sorted((ROOT/"lean"/"OAI").rglob("*.lean"))
def decls(txt):
    out=[]
    for i,ln in enumerate(txt.splitlines(),1):
        m = DECL.match(ln)
        if m: out.append((m.group(1), m.group(2), i, ln))
    return out

def main():
    fs = files()
    texts = {f: f.read_text(errors="ignore") for f in fs}
    # strip comments crudely for name counting
    def strip(t):
        t = re.sub(r"/-.*?-/", "", t, flags=re.S)
        t = re.sub(r"--[^\n]*", "", t)
        return t
    st = {f: strip(t) for f,t in texts.items()}
    mods = sys.argv[1:]
    want = lambda f: any(("/".join(f.parts[2:]).startswith(m.replace('.','/')) if not m.endswith('/') else True) for m in mods)
    rows=[]
    for f in fs:
        rel = "/".join(f.parts[2:])
        if not any(rel.startswith(m) for m in mods): continue
        for kind,name,line,raw in decls(texts[f]):
            if name in ("_",): continue
            short = name.split('.')[-1]
            pat = re.compile(r"(?<![A-Za-z0-9_'.])" + re.escape(short) + r"(?![A-Za-z0-9_'])")
            use_in, use_out = 0,0
            for g in fs:
                c = len(pat.findall(st[g]))
                if g == f: use_in += max(0,c-1)
                else: use_out += c
            rows.append((rel,line,kind,name,use_in,use_out,raw.strip()[:110]))
    for r in rows:
        print(f"{r[4]:4d} {r[5]:4d} {r[0]}:{r[1]:4d} {r[2]:9s} {r[3]}")
if __name__=="__main__": main()
