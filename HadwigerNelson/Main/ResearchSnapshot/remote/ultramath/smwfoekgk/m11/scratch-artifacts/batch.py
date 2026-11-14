import sys, json, pathlib
sys.path.insert(0,'.scratch')
import autoexp
from concurrent.futures import ThreadPoolExecutor
mods = [l.strip() for l in open(".scratch/mods.txt") if l.strip()]
def go(m):
    try:
        R = autoexp.run(m)
    except Exception as e:
        return (m, "ERR "+repr(e)[:80], 0, 0, 0)
    c = R["cands"]; ok=[x for x in c if R["res"][x["key"]]]
    pathlib.Path(".scratch/res_"+m.replace("/","_")+".json").write_text(json.dumps(
        dict(errl=R["errl"], res=R["res"], cands=[{k:x[k] for k in ("key","start","bodylen","endline","dline","dend")} for x in c])))
    pathlib.Path(".scratch/last_out_"+m.replace("/","_")+".txt").write_text(R["out"])
    return (m, "ok", len(c), sum(x["bodylen"] for x in c), sum(x["bodylen"]-1 for x in ok), len(ok))
with ThreadPoolExecutor(2) as ex:
    for r in ex.map(go, mods):
        print("%-60s %s cands=%d body=%d savable=%d closed=%d" % r, flush=True)
