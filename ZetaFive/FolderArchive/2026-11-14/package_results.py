"""Package only the source, report, derivations and reproducible checks."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import hashlib
import json

root=Path(__file__).resolve().parent
names=[
 'README.txt','additional_checks.txt','build_report.py','package_results.py',
 'output/zeta7_argument_audit.pdf',
 'sources/source_ledger.json','sources/Fauzan_2026_zeta5.pdf',
 'sources/Fauzan_2026_zeta5.txt',
 'algebra_notes.txt','arithmetic_notes.txt','arithmetic_variant_notes.txt',
 'arithmetic_costs.py','arithmetic_exact_inner.py','arithmetic_variant.py',
 'arithmetic_variant_results.json',
 'experiments/exact_checks.py','experiments/exact_checks.json',
 'experiments/energy_probe.py','experiments/energy_probe.json',
 'experiments/single_point_certificate.py','experiments/single_point_certificate.json',
 'experiments/main_measure_certificate.py','experiments/main_measure_certificate.json',
]
log=root/'exploration_log.json'
if log.exists():names.append('exploration_log.json')
manifest={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in names}
out=root/'output/zeta7_exploration_bundle.zip'
with ZipFile(out,'w',ZIP_DEFLATED) as z:
    for name in names:z.write(root/name,name)
    z.writestr('SHA256_manifest.json',json.dumps(manifest,indent=2))
with ZipFile(out) as z:
    assert z.testzip() is None
    assert all(hashlib.sha256(z.read(name)).hexdigest()==h for name,h in manifest.items())
print(out)
print(len(names),'files;',out.stat().st_size,'bytes; archive and hashes verified')
