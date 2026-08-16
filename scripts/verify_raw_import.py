from __future__ import annotations
import hashlib, json, sys, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / 'archive/RAW_IMPORT_MANIFEST.json').read_text(encoding='utf-8'))
archive = ROOT / manifest['archive']
want = {x['name']: x for x in manifest['files']}
with zipfile.ZipFile(archive) as z:
    got = {x.filename.rstrip('/'): x for x in z.infolist() if not x.is_dir()}
    missing = sorted(set(want) - set(got))
    extra = sorted(set(got) - set(want))
    bad=[]
    for name, rec in want.items():
        if name not in got: continue
        b=z.read(name)
        sha=hashlib.sha256(b).hexdigest()
        if len(b)!=rec['bytes'] or sha!=rec['sha256']:
            bad.append({'name':name,'bytes':len(b),'sha256':sha})
print({'missing':missing,'extra':extra,'bad':bad,'ok':not missing and not extra and not bad})
sys.exit(0 if not missing and not extra and not bad else 1)
