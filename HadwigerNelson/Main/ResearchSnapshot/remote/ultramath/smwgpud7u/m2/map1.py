from check import check
a3,a4=int(__import__('sys').argv[1]),int(__import__('sys').argv[2])
step=4
rows=[]
a2s=list(range(60,300,step)); a5s=list(range(60,300,step))
for a5 in reversed(a5s):
    row=''
    for a2 in a2s:
        al=[0,0,a2,a3,a4,a5]
        if len(set(al))<5: row+='#'
        elif not check(al): row+='o'
        else: row+='.'
    rows.append(f'{a5:4d} {row}')
print('     '+''.join('|' if a%20==0 else ' ' for a in a2s))
print('\n'.join(rows))
print('grid a2:',a2s[0],'..',a2s[-1],'step',step)
