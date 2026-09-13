"""Temporary documentation transfer and validation on an isolated CI checkout."""
import base64
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.request

BASE = '0203791aaf4bf5d8fad31ed53575943937782cef'
BASE_TREE = '7891416246afb40ffefbbde3c9f0cd2b39dbaf35'
EXPECTED_TREE = '00272cfe9902d50884e6e13b5bdd9c32f0a92114'
PAYLOAD_SHA = '6160f6c369d5dd6a3e13a6fcd35522b1748d51467f640dc644014cfc3cc282ee'
REPO = 'TJ4519/knowledge-work-sdlc'

def git(*args):
    return subprocess.check_output(['git', *args], text=True).strip()

payload = gzip.decompress(base64.b64decode(Path(sys.argv[1]).read_text().strip(), validate=True))
assert hashlib.sha256(payload).hexdigest() == PAYLOAD_SHA
changes = json.loads(payload)
subprocess.run(['git', 'checkout', '--detach', BASE], check=True)
assert git('rev-parse', 'HEAD^{tree}') == BASE_TREE
assert not git('status', '--porcelain')
entries = []
for item in changes:
    p = Path(item['path'])
    assert not p.is_absolute() and '..' not in p.parts and p.suffix == '.md'
    assert p.is_file() and not p.is_symlink()
    old = p.read_bytes()
    assert hashlib.sha256(old).hexdigest() == item['sha256'], str(p)
    lines = old.decode('utf-8').splitlines(keepends=True)
    for start, end, replacement in reversed(item['edits']):
        assert 0 <= start <= end <= len(lines)
        lines[start:end] = [replacement]
    text = ''.join(lines)
    p.write_bytes(text.encode('utf-8'))
    entries.append({'path': p.as_posix(), 'mode': '100644', 'type': 'blob', 'content': text})
subprocess.run(['git', 'diff', '--check'], check=True)
subprocess.run(['git', 'add', '-A'], check=True)
assert git('write-tree') == EXPECTED_TREE
subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], check=True)
subprocess.run(['git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com'], check=True)
subprocess.run(['git', 'commit', '-m', 'docs: focus public documentation on features and usage'], check=True)
for target in ('validate', 'package'):
    result = subprocess.run(['make', target], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if result.returncode:
        print(result.stdout)
        raise SystemExit(result.returncode)
    for line in result.stdout.splitlines():
        if line.startswith(('Ran ', 'OK')) or '"passed"' in line:
            print(line)
    print('PASSED make ' + target)
assert git('rev-parse', 'HEAD^{tree}') == EXPECTED_TREE
assert not git('status', '--porcelain')
request = urllib.request.Request(
    f'https://api.github.com/repos/{REPO}/git/trees',
    data=json.dumps({'base_tree': BASE_TREE, 'tree': entries}).encode(), method='POST',
    headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
             'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json',
             'X-GitHub-Api-Version': '2022-11-28', 'User-Agent': 'kw-docs-validation'})
with urllib.request.urlopen(request, timeout=30) as response:
    result = json.load(response)
assert result['sha'] == EXPECTED_TREE
print('PUBLISHED_TREE=' + result['sha'])
print('CHANGED_DOCUMENTS=' + str(len(entries)))
