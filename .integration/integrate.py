"""Temporary integration transport; never part of the published product tree."""
import base64
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import urllib.request

BASE = 'b12d7a93f8ef4733b2a5603476287613747ebe1d'
BOOTSTRAP = '064d89d8f3196fb401c3dcb56c83d333de2e1e69'
EXPECTED_PATCH = '8fb78c9cdbfe864fceb2d6414764c62b599a6ce19da237fcf8569ca1899b6776'
EXPECTED_TREE = '7891416246afb40ffefbbde3c9f0cd2b39dbaf35'
BASE_TREE = '0dd860acc840ff30a3a3efee2a63d9cdb3bc375a'
REPO = 'TJ4519/knowledge-work-sdlc'


def git(*args):
    return subprocess.check_output(['git', *args]).decode().strip()


parts = {p.name: p.read_text().strip() for p in sorted(Path('.integration').glob('patch-*.b64'))}
fixups = Path('.integration/fixups.json')
if fixups.exists():
    for change in json.loads(fixups.read_text()):
        part = parts[change['file']]
        start, end = change['start'], change['end']
        assert part[start:end] == change['old'], 'Transport correction did not match'
        parts[change['file']] = part[:start] + change['new'] + part[end:]
payload = ''.join(parts[name] for name in sorted(parts))
patch = gzip.decompress(base64.b64decode(payload, validate=True))
assert hashlib.sha256(patch).hexdigest() == EXPECTED_PATCH, 'Patch checksum mismatch'
patch_path = Path(os.environ.get('RUNNER_TEMP', tempfile.gettempdir())) / 'semantic-memory.patch'
patch_path.write_bytes(patch)
subprocess.run(['git', 'checkout', '--detach', BOOTSTRAP], check=True)
assert not git('status', '--porcelain'), 'Bootstrap workspace must be clean'
subprocess.run(['git', 'apply', '--check', '--whitespace=error', str(patch_path)], check=True)
subprocess.run(['git', 'apply', '--whitespace=error', str(patch_path)], check=True)
subprocess.run(['git', 'add', '-A'], check=True)
assert git('write-tree') == EXPECTED_TREE, 'Candidate tree mismatch'
subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], check=True)
subprocess.run(['git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com'], check=True)
subprocess.run(['git', 'commit', '-m', 'Validate exact semantic-memory candidate'], check=True)
subprocess.run(['make', 'validate'], check=True)
subprocess.run(['make', 'package'], check=True)
assert git('rev-parse', 'HEAD^{tree}') == EXPECTED_TREE
assert not git('status', '--porcelain'), 'Tests modified tracked candidate'

# Publish immutable Git tree data only. Main is updated separately through the connector.
changed = subprocess.check_output(['git', 'diff', '--name-only', '-z', BASE, 'HEAD']).decode().split('\0')
entries = []
for name in filter(None, changed):
    assert not name.startswith(('.integration/', '.github/')), 'Temporary integration file leaked'
    path = Path(name)
    if not path.exists():
        entries.append({'path': name, 'mode': '100644', 'type': 'blob', 'sha': None})
        continue
    assert path.is_file() and not path.is_symlink()
    mode = git('ls-files', '--stage', '--', name).split()[0]
    assert mode in ('100644', '100755')
    entries.append({'path': name, 'mode': mode, 'type': 'blob', 'content': path.read_text(encoding='utf-8')})
body = json.dumps({'base_tree': BASE_TREE, 'tree': entries}).encode()
request = urllib.request.Request(
    f'https://api.github.com/repos/{REPO}/git/trees', data=body, method='POST',
    headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
             'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json',
             'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'kw-validated-tree-upload'})
with urllib.request.urlopen(request, timeout=60) as response:
    result = json.load(response)
assert result['sha'] == EXPECTED_TREE, 'Remote tree mismatch'
print('PUBLISHED_TREE=' + result['sha'], flush=True)
print('VALIDATED_PRODUCT_FILES=' + str(len(entries)), flush=True)
