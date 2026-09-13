import base64, gzip, hashlib, json, os, pathlib, subprocess
root=pathlib.Path.cwd()
build=root/'.npm-build'
encoded=base64.b64encode((build/'changes.patch.gz').read_bytes()).decode()
fixups=build/'fixups.json'
if fixups.exists():
    for item in json.loads(fixups.read_text()):
        old,new=item['old'],item['new']
        if encoded.count(old)!=1: raise SystemExit('ambiguous transfer fixup')
        encoded=encoded.replace(old,new,1)
patch=gzip.decompress(base64.b64decode(encoded,validate=True))
if hashlib.sha256(patch).hexdigest()!='14adc8faba1a8e85be3f4b1e2e9743a0bedc28f68fa603db55799f535ad4e3a9':
    raise SystemExit('source patch integrity mismatch')
p=pathlib.Path(os.environ['RUNNER_TEMP'])/'npm.patch';p.write_bytes(patch)
subprocess.run(['git','reset','--hard','a984ccbb783fd53bfb67162e59c574e1ce935fbd'],check=True)
subprocess.run(['git','clean','-fdx'],check=True)
subprocess.run(['git','apply','--check',str(p)],check=True)
subprocess.run(['git','apply',str(p)],check=True)
yml=root/'.github/workflows/npm-distribution.yml'
yml.write_text(yml.read_text().replace('npm publish --dry-run dist/','npm publish --dry-run ./dist/'))
subprocess.run(['git','diff','--check'],check=True)
subprocess.run(['git','add','.'],check=True)
if subprocess.check_output(['git','write-tree'],text=True).strip()!='545e708740a9e6a1f069e18f733252e3f20c8173': raise SystemExit('Unexpected candidate tree')
subprocess.run(['git','-c','user.name=Knowledge Work build','-c','user.email=build@localhost','commit','-m','Validate npm distribution'],check=True)
