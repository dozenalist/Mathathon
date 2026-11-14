import json, pathlib, collections, sys
H = pathlib.Path("/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/sprint/simplify/m10/harness")
src = (H/"analyze.py").read_text().replace("\nmain()\n", "\n")
ns = {"__file__": str(H/"analyze.py")}
exec(compile(src, "analyze.py", "exec"), ns)
nodes, et, ev = ns["load"]()
sp = ns["spans"]()
red = ns["closure"](nodes, et, ev)
outside = sorted((n for n in sp if n not in red), key=lambda n:(sp[n]["mod"], sp[n]["start"]))
out = []
for n in outside:
    v = sp[n]
    out.append({"name":n, "mod":v["mod"], "start":v["start"], "lines":v["lines"]})
json.dump(out, open("dead.json","w"), indent=0)
print(len(out), "decls", sum(o["lines"] for o in out), "lines")
for o in out[:12]: print(o["lines"], o["mod"], o["name"].split(".")[-1])
print("...")
