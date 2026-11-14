import json,sys
sys.set_int_max_str_digits(0)
from pathlib import Path
from fractions import Fraction as F
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(Path(sys.argv[1]) if len(sys.argv)>1 else ROOT.parents[2]/'Experimental/scripts'))
import rigorous_cell_volume as E
lo,hi,ni,no=E.box_volume((F(110,180),F(1101,1800)),(F(35,180),F(351,1800)))
d=dict(source='d289bef49fa25aea10c4c8c0c7299d5d5449fdd0',theta_degrees=['110','110.1'],phi_degrees=['35','35.1'],lo=str(lo),hi=str(hi),display=[float(lo),float(hi)],vertices=[ni,no],status='reproduced_output_only; norm and boundedness proof obligations remain')
(ROOT/'one_box.json').write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in d.items() if k not in ('lo','hi')},indent=2))
