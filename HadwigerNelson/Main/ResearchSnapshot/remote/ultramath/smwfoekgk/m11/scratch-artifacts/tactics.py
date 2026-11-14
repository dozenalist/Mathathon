import re, pathlib, collections, json
root = pathlib.Path("work/lean/OAI")
files = sorted(root.rglob("*.lean"))
TAC = re.compile(r'^(\s*)((?:·|\.)\s*)?([A-Za-z_][A-Za-z0-9_\']*)')
heads = collections.Counter(); tot=0; nonblank=0; comment=0; blank=0
BLOCK_START = ("intro","exact","apply","refine","rw","simp","have","obtain","rcases","cases","induction",
 "constructor","exact_mod_cast","push_neg","by_contra","contrapose","choose","let","set","calc","trans",
 "convert","convert_to","field_simp","ring","linarith","nlinarith","norm_num","positivity","gcongr",
 "measurability","fun_prop","aesop","grind","omega","norm_cast","ext","funext","congr","specialize",
 "refine'","filter_upwards","interval_cases","fin_cases","subst","rename_i","suffices","show","use","exists",
 "rw_mod_cast","simp_rw","nth_rewrite","conv","unfold","dsimp","change","abel","linear_combination","polyrith")
body_lines = 0
for p in files:
    for l in p.read_text(errors="ignore").splitlines():
        s=l.strip()
        if not s: blank+=1; continue
        if s.startswith("--"): comment+=1; continue
        tot+=1
        m = TAC.match(l)
        if m and (m.group(2) or m.group(3) in BLOCK_START or True):
            h=m.group(3)
            if h in BLOCK_START: heads[h]+=1; body_lines+=1
print("nonblank lines", tot, "blank", blank, "comment", comment)
print("tactic-ish lines", body_lines)
for h,c in heads.most_common(30): print(f'{c:6d} {h}')
