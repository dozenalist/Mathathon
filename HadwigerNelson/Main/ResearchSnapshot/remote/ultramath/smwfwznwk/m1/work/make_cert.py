"""Write the certificate: explicit pair-only free-label sector words at m = 5,6,9,12,15,18."""
import sys, json
sys.path.insert(0,'work')
from word import uniform_word, NAME, offsets, as_lists
from check1 import check

cert={"problem":"k=6, C_6, free label 0, palettes of size 2, transport offsets +-(m-1),+-m,+-(m+1) mod 6m",
      "construction":"sigma = A^2 B^2 D^(m-3) E^2 F^(m-3) (length 2m), repeated 3 times; A={1,3} B={1,4} D={2,4} E={2,5} F={3,5}",
      "words":{}}
for m in (5,6,9,12,15,18):
    w=uniform_word(m)
    ok,bad=check(w,m)
    assert ok,(m,bad[:3])
    cert["words"][str(m)]={"m":m,"n":6*m,"offsets":offsets(m),
        "word":as_lists(w),
        "word_as_letters":''.join(NAME[S] for S in w),
        "checked":True}
json.dump(cert,open('cert/sector_words.json','w'),indent=1)
print("wrote cert/sector_words.json with words for m =", sorted(cert["words"],key=int))
print("m=6 word:",cert["words"]["6"]["word_as_letters"])
print("m=6 offsets:",cert["words"]["6"]["offsets"])
