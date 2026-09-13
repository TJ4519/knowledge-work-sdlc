import json, os, pathlib, subprocess, urllib.request
root=pathlib.Path.cwd()
base='a984ccbb783fd53bfb67162e59c574e1ce935fbd'
allowed={'.github/workflows/npm-distribution.yml','.gitignore','CHANGELOG.md','README.md','bin/knowledge-work-sdlc.cjs','docs/guides/installation-and-providers.md','docs/guides/npm-installation.md','package-lock.json','package.json','tests/npm-installer.test.cjs','tooling/projection.py'}
paths=subprocess.check_output(['git','diff','--name-only',base,'HEAD'],text=True).splitlines()
if set(paths)!=allowed: raise SystemExit('Unexpected change surface')
url='https://api.github.com/repos/TJ4519/knowledge-work-sdlc/git/'
def post(kind,payload):
    req=urllib.request.Request(url+kind,data=json.dumps(payload).encode(),method='POST',headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','Content-Type':'application/json','X-GitHub-Api-Version':'2022-11-28'})
    with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
entries=[]
for p in paths:
    mode=subprocess.check_output(['git','ls-files','-s','--',p],text=True).split()[0]
    sha=post('blobs',{'content':(root/p).read_text(),'encoding':'utf-8'})['sha']
    entries.append({'path':p,'mode':mode,'type':'blob','sha':sha})
tree=post('trees',{'base_tree':'3cafe8fba44919692622eb778d5add2c14d3b003','tree':entries})['sha']
local=subprocess.check_output(['git','rev-parse','HEAD^{tree}'],text=True).strip()
if tree!=local: raise SystemExit('Published tree differs from tested tree')
print('TESTED_PRODUCT_TREE='+tree)
(root/'dist/npm-source.json').write_text(json.dumps({'base_commit':base,'tested_tree':tree,'validation_run':os.environ['GITHUB_RUN_ID']},indent=2)+'\n')
