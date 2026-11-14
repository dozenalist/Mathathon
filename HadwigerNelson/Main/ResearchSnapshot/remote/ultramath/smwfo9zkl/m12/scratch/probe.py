import re,sys,html
t=open('scratch/mutool.xml',encoding='utf-8',errors='replace').read()
pages=re.split(r'<page ',t)
def text(p):
    p=re.sub(r'</?span[^>]*>','',p)
    p=re.sub(r'<[^>]+>','',p)
    return html.unescape(p)
targets=["multiplicity at most two","side ten","positive coordinates","finitely many simple cycles","mesh at most two","we use only the","takes values in G"]
for pat in targets:
    hits=[]
    for i,p in enumerate(pages):
        txt=text(p)
        for m in re.finditer(re.escape(pat),txt):
            hits.append((i,m.start()))
    print("PATTERN",repr(pat),"hits on pages",[h[0] for h in hits][:12])
