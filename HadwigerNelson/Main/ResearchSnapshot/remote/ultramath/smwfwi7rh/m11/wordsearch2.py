import math
from wordsearch import palettes_valid_for_C6, word_exists, sh_interval
alph = palettes_valid_for_C6()
print("narrowing the frozen free-label threshold (free label 0, sizes 2..3, C6-admissible):", flush=True)
for d in [0.155,0.16,0.165,0.17,0.175,0.18,0.185,0.19]:
    iv = sh_interval(d, 6000)
    row=[]
    for n in [36,48,60,72,84,96,120,144,168]:
        sat,_ = word_exists(n,d,alph,iv)
        row.append(f"{n}:{'S' if sat else 'U'}")
    print(f" d={d:.3f}  " + " ".join(row), flush=True)
