"""Verify exact approved brand and cover assets without changing them."""
from pathlib import Path
import hashlib,json,sys,argparse

root=Path(__file__).resolve().parents[1]
manifest=json.loads((root/'references/approved-assets.json').read_text())
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--asset-dir',required=True,type=Path)
args=parser.parse_args()
failures=[]
for row in manifest['assets']+manifest.get('archived_cover_art',[]):
    path=args.asset_dir/Path(row['path']).name
    if not path.is_file():failures.append(row['path']+': missing');continue
    if hashlib.sha256(path.read_bytes()).hexdigest()!=row['sha256']:failures.append(row['path']+': checksum mismatch')
print(json.dumps({'checked':len(manifest['assets'])+len(manifest.get('archived_cover_art',[])),'failures':failures,'baseline':manifest['baseline']},indent=2))
sys.exit(1 if failures else 0)
