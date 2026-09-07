"""Build the complete 3D-only release with Python 3.11+."""
import hashlib
import json
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
output = root / 'dist'
output.mkdir(exist_ok=True)
blend = root / 'blender' / 'La_Nuit_Etoilee_V7.blend'
verification = json.loads((root / 'docs' / 'verification.json').read_text(encoding='utf-8'))
assert verification['status'] == 'passed'
with blend.open('rb') as handle:
    blend_hash = hashlib.file_digest(handle, 'sha256').hexdigest()
assert blend_hash == verification['sha256'], 'The Blender file changed after verification.'

files = [root / name for name in ('README.md', 'CREDITS.md', '.gitignore', '.gitattributes')]
for directory in ('blender', 'docs', 'scripts', 'previews', 'credits'):
    files.extend(p for p in (root / directory).rglob('*') if p.is_file() and p.suffix.lower() in {'.blend', '.md', '.json', '.py', '.png'})
assert [p for p in files if p.suffix == '.blend'] == [blend]
archive = output / 'La_Nuit_Etoilee_V7_Blender.zip'
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as bundle:
    for path in sorted(files):
        bundle.write(path, 'La_Nuit_Etoilee_V7/' + path.relative_to(root).as_posix())
with zipfile.ZipFile(archive) as bundle:
    assert bundle.testzip() is None
    names = bundle.namelist()
    assert not any(Path(name).suffix.lower() in {'.mp4', '.mov', '.avi', '.mp3', '.wav', '.blend1'} for name in names)
with archive.open('rb') as handle:
    archive_hash = hashlib.file_digest(handle, 'sha256').hexdigest()
(output / 'SHA256SUMS.txt').write_text(archive_hash + '  ' + archive.name + '\n', encoding='ascii')
print(json.dumps({'archive': str(archive), 'bytes': archive.stat().st_size, 'files': len(names), 'sha256': archive_hash}, indent=2))
