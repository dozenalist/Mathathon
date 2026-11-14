import re, sys, json, pathlib, subprocess, os, shutil

ROOT = pathlib.Path("work/lean/OAI")
DECL = re.compile(r'^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+|partial\s+|unsafe\s+)*'
                  r'(theorem|lemma|def|abbrev|instance|example|structure|inductive|class|opaque)\b')
TAC = "  first | grind | aesop | simp_all | omega"

def decls_of(lines):
    ds = []
    for i, l in enumerate(lines):
        m = DECL.match(l)
        if m:
            nm = re.match(r'^\s*(?:@\[[^\]]*\]\s*)?(?:private\s+|protected\s+|noncomputable\s+)*\w+\s*([^\s:{(\[]*)', l)
            ds.append(dict(kind=m.group(1), line=i+1, name=nm.group(1)))
    for j, d in enumerate(ds):
        d["end"] = ds[j+1]["line"]-1 if j+1 < len(ds) else len(lines)
    return ds

def candidates(path, minbody=4, kinds=("theorem","lemma")):
    lines = path.read_text(errors="ignore").splitlines()
    out = []
    for d in decls_of(lines):
        if d["kind"] not in kinds: continue
        if lines[d["line"]-1][:1] in (" ","\t"): continue
        sub = lines[d["line"]-1:d["end"]]
        byline = None
        for k, x in enumerate(sub):
            if x.rstrip().endswith("by"):
                byline = k; break
        if byline is None: continue
        j = byline+1
        while j < len(sub) and (sub[j].strip()=="" or sub[j][:1] in (" ","\t")):
            j += 1
        body = sub[byline+1:j]
        while body and body[-1].strip()=="": body.pop()
        if len(body) < minbody: continue
        out.append(dict(name=d["name"], key=f'{d["line"]}:{d["name"]}', start=d["line"]+byline,
                        bodylen=len(body), total=d["end"]-d["line"]+1, first=sub[byline].strip()[:70],
                        endline=d["line"]+byline+len(body), dline=d["line"], dend=d["end"]))
    return lines, out

def run(modpath, tmo=1800, tac=TAC):
    p = ROOT/modpath
    bak = p.with_suffix(".lean.bak"); shutil.copy2(p, bak)
    try:
        lines, cands = candidates(p)
        new = list(lines)
        for c in cands:
            k = c["bodylen"]
            new[c["start"]:c["start"]+k] = [tac] + [""]*(k-1)
        p.write_text("\n".join(new) + "\n")
        r = subprocess.run(["lean", str(p)], capture_output=True, text=True, env=dict(os.environ), timeout=tmo)
        errl = sorted({int(m.group(1)) for m in re.finditer(r'\.lean:(\d+):\d+: error', r.stdout)})
        res = {c["key"]: not any(c["dline"] <= l <= c["dend"] for l in errl) for c in cands}
        covered = set()
        for c in cands: covered |= set(range(c["dline"], c["dend"]+1))
        return dict(cands=cands, res=res, errl=errl, stray=[l for l in errl if l not in covered], out=r.stdout[-2500:], rc=r.returncode)
    finally:
        shutil.copy2(bak, p); bak.unlink()

if __name__ == "__main__":
    mods = sys.argv[1:]
    for mod in mods:
        R = run(mod)
        cands = R["cands"]; ok = [c for c in cands if R["res"][c["key"]]]
        print(f"### {mod}: cands={len(cands)} bodylines={sum(c['bodylen'] for c in cands)} closed={len(ok)} "
              f"savable={sum(c['bodylen']-1 for c in ok)} stray={R['stray'][:6]} rc={R['rc']}")
        for c in cands:
            print(("OK  " if R["res"][c["key"]] else "..  ")+f" L{c['start']:4d} b{c['bodylen']:3d} {c['key'][:50]}")
        pathlib.Path(".scratch/last_out_"+mod.replace("/","_")+".txt").write_text(R["out"])
        import json as _j; _j.dump(dict(errl=R["errl"], res=R["res"], cands=[{k:c[k] for k in ("key","start","bodylen","endline","dline","dend")} for c in R["cands"]]), open(".scratch/res_"+mod.replace("/","_")+".json","w"))
