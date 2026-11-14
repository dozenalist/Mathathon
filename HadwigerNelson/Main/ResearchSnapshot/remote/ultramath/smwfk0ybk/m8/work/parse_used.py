import re, pathlib, json
txt = pathlib.Path("used.log").read_text().splitlines()
res = {}
cur = None
for ln in txt:
    if ln.startswith("@@@"):
        parts = ln[3:].split("\t")
        if parts[1] == "usedconstants":
            cur = parts[0]; res[cur] = set(); continue
        tgt, mod, d, u = parts[0], parts[1], int(parts[2]), int(parts[3])
        cur = tgt
        rest = parts[4] if len(parts) > 4 else ""
        cur_mod = mod
        res.setdefault(tgt, set())
        open_block = True
        buf = rest
    else:
        buf += "\n" + ln
    # flush names found so far
    if cur is not None and 'buf' in dir():
        pass
