#!/usr/bin/env python3
"""Split a Lean file into declaration blocks; delete named declarations safely.
A block runs from the declaration line (plus preceding @[..] attributes and /-- -/
docstring) to the last non-blank line before the next top-level structural line."""
import re
DECL=re.compile(r'^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable|partial|unsafe|scoped)\s+)*(theorem|lemma|def|abbrev|structure|instance|class|inductive|opaque)\s+([A-Za-z_][\w\u2080-\u209c\'!?]*)')
STOP=re.compile(r'^(end|namespace|section|noncomputable section|open|variable|omit|include|attribute|local|set_option|universe|mutual|example|where|@\[|#|/-|--|/\-\-)')
def blocks(lines):
    starts=[]
    for i,l in enumerate(lines):
        m=DECL.match(l)
        if m: starts.append((i,m.group(1),m.group(2)))
    out=[]
    for k,(i,kind,name) in enumerate(starts):
        s=i
        while s-1>=0:
            prev=lines[s-1]; ps=prev.strip()
            if ps=='': break
            if re.match(r'^(omit|include)\b.*\bin$',ps): s-=1; continue
            if ps.startswith('@[') and ps.endswith(']'): s-=1; continue
            if ps.endswith('-/'):
                j=s-1
                while j>=0 and not lines[j].lstrip().startswith('/--'): j-=1
                if j>=0: s=j; continue
            break
        e=i+1
        j=i+1
        while j<len(lines):
            l=lines[j]
            if l.strip()=='' : j+=1; continue
            if not l[0].isspace() and (STOP.match(l) or DECL.match(l)): break
            e=j+1; j+=1
        out.append((s,e,kind,name))
    return out
def delete(path,names):
    lines=open(path,encoding='utf-8').read().split('\n')
    gone=[]
    for s,e,kind,name in reversed(blocks(lines)):
        if name in names:
            del lines[s:e]; gone.append(name)
    open(path,'w',encoding='utf-8').write('\n'.join(lines))
    return gone
