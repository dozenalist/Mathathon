"""Host-only path adapter: map the worker's /tmp checker import to a pinned file.
No worker source is edited. All other imports and mathematical code are unchanged.
Usage: python run_with_checker.py SCRIPT CHECKER [script arguments]
"""
import importlib.util, runpy, sys
from pathlib import Path
script,checker=Path(sys.argv[1]).resolve(),Path(sys.argv[2]).resolve()
original=importlib.util.spec_from_file_location
def mapped(name,location,*args,**kwargs):
    if str(location) in ('/tmp/sc662.py','/tmp/shell_check.py'):
        print('HOST PATH ADAPTER:',location,'->',checker,flush=True)
        location=str(checker)
    return original(name,location,*args,**kwargs)
importlib.util.spec_from_file_location=mapped
sys.path.insert(0,str(script.parent))
sys.argv=[str(script),*sys.argv[3:]]
runpy.run_path(str(script),run_name='__main__')
