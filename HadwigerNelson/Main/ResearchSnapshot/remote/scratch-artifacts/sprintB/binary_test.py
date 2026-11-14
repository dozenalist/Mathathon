from itertools import combinations
k=6
def pc(m): return bin(m).count('1')
# regenerate ell=6 words with the corrected constraints (from orbit_correct)
import importlib.util
spec=importlib.util.spec_from_file_location("oc","/workspace/nucleus/work/projects/p-a4e2849861784c708dd751c46b0f4f64/repo/.scratch/sprintB/orbit_correct.py")
# simpler: inline
V=set(range(6))
A=[sum(1<<x for x in c) for r in range(1,4) for c in combinations(range(6) if False else [x for x in range(k) if x!=0],r)]
A=[P for P in A if all((P & ~((1<<j)|(1<<((j+1)%6))))!=0 for j in range(6))]
def ok_trans(a,b):
    if a&b: return False
    if pc(a)==3 and pc(b)>2: return False
    if pc(b)==1: return False
    return True
def ok_word(w):
    if sum(1 for m in w if pc(m)==3)>3: return False
    for j in range(6):
        for d in (1,2,3):
            a,b=w[j],w[(j+d)%6]
            if pc(a)==3 and pc(b)==3 and (a&b)==0: return False
        if pc(w[j])+pc(w[(j+2)%6])==5 and (w[j]&w[(j+2)%6])==0: return False
    return True
res=[]
def rec(p):
    if len(p)==6:
        if not ok_trans(p[5],p[0]): return
        if ok_word(p): res.append(tuple(p))
        return
    for b in A:
        if ok_trans(p[-1],b): rec(p+[b])
for a in A: rec([a])
print("words",len(res))
pairs=[sum(1<<x for x in c) for c in combinations(range(6),2)]
def binary_pair(w,D):
    return all(pc(m&D)==1 for m in w)
cnt=sum(1 for w in res if any(binary_pair(w,D) for D in pairs))
print("words with some fixed binary pair:",cnt,"/",len(res))
# how many need the pair to depend on position? check "for each position there is a pair hitting it in a singleton" trivially true?
# check whether a single pair works for the whole word only
bad=[w for w in res if not any(binary_pair(w,D) for D in pairs)]
print("without fixed binary pair:",len(bad))
for w in bad[:5]: print([[x for x in range(6) if (m>>x)&1] for m in w])
