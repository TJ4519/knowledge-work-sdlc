'use strict';
const { test, before, after } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const { parseArgs } = require('../bin/knowledge-work-sdlc.cjs');
const ROOT = path.resolve(__dirname, '..');
let tmp, packedRoot, tarball, inventory;

function run(command, args, options = {}) {
  const result = spawnSync(command, args, { cwd: ROOT, encoding: 'utf8', timeout: 30000,
    env: { ...process.env, npm_config_audit: 'false', npm_config_fund: 'false' }, ...options });
  if (result.error) throw result.error;
  return result;
}
function ok(result) {
  assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);
  return result;
}
function cli(args, options = {}) {
  return run(process.execPath, [path.join(packedRoot, 'bin/knowledge-work-sdlc.cjs'), ...args], options);
}
function client(name) {
  const p = path.join(tmp, name); fs.mkdirSync(p);
  ok(run('git', ['init', '-q', '-b', 'main', p]));
  return p;
}
function snapshot(dir) {
  const files = {};
  function visit(p) {
    for (const entry of fs.readdirSync(p, { withFileTypes: true })) {
      if (entry.name === '.git') continue;
      const full = path.join(p, entry.name);
      if (entry.isDirectory()) visit(full);
      else if (entry.isSymbolicLink()) files[path.relative(dir, full)] = `link:${fs.readlinkSync(full)}`;
      else files[path.relative(dir, full)] = fs.readFileSync(full).toString('base64');
    }
  }
  visit(dir); return files;
}
function validate(target) {
  const code = 'import sys,json; from pathlib import Path; sys.path.insert(0,sys.argv[1]); from tooling.projection import validate_workspace; d=validate_workspace(Path(sys.argv[2]),Path(sys.argv[1])); print(json.dumps(d)); sys.exit(bool(d))';
  ok(run('python3', ['-I', '-B', '-c', code, ROOT, target]));
}
before(() => {
  tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'knowledge-work-npm-'));
  const result = ok(run('npm', ['pack', '--json', '--ignore-scripts', '--offline', '--pack-destination', tmp]));
  inventory = JSON.parse(result.stdout)[0];
  tarball = path.join(tmp, inventory.filename);
  ok(run('tar', ['-xzf', tarball, '-C', tmp]));
  packedRoot = path.join(tmp, 'package');
});
after(() => { if (tmp) fs.rmSync(tmp, { recursive: true, force: true }); });

test('arguments are bounded and upgrades default to preview', () => {
  assert.deepEqual(parseArgs(['install']), { command: 'install', target: '.', dryRun: false, apply: false });
  assert.equal(parseArgs(['upgrade', '.']).apply, false);
  assert.equal(parseArgs(['upgrade', '--apply', '.']).apply, true);
  assert.equal(parseArgs(['install', '--', '-named']).target, '-named');
  for (const args of [ ['remove'], ['install', '--apply'], ['upgrade', '--apply', '--dry-run'],
    ['recover', '--dry-run'], ['install', 'one', 'two'], ['install', '--source-root', '/tmp'],
    ['install', ''], ['install', '--dry-run', '--dry-run'] ]) {
    assert.throws(() => parseArgs(args), undefined, JSON.stringify(args));
  }
});

test('published payload is allowlisted and has no install lifecycle scripts', () => {
  const p = JSON.parse(fs.readFileSync(path.join(packedRoot, 'package.json')));
  assert.equal(p.name, 'knowledge-work-sdlc');
  assert.equal(p.version, fs.readFileSync(path.join(packedRoot, '.knowledge-sdlc/VERSION'), 'utf8').trim());
  assert.deepEqual(Object.keys(p.scripts), ['test']);
  assert.equal(p.license, 'SEE LICENSE IN LICENSE.md');
  const paths = inventory.files.map(f => f.path);
  for (const needed of ['AGENTS.md', 'tooling/installer.py', 'tooling/projection.py',
    '.knowledge-sdlc/skills/kw-recall/SKILL.md', '.knowledge-sdlc/references/working-memory.md']) {
    assert.ok(paths.includes(needed), needed);
  }
  assert.ok(!paths.some(p => /(^|\/)(ai_docs|tests|examples|\.git|\.github|node_modules|__pycache__)(\/|$)|\.pyc$|\.tgz$/.test(p)));
  for (const f of inventory.files) {
    assert.deepEqual(fs.readFileSync(path.join(packedRoot, f.path)), fs.readFileSync(path.join(ROOT, f.path)), f.path);
  }
});

test('help and version run without Python', () => {
  const env = { ...process.env, KNOWLEDGE_WORK_PYTHON: '/does/not/exist' };
  assert.match(ok(cli(['--help'], { env })).stdout, /upgrade/);
  assert.match(ok(cli(['--version'], { env })).stdout, /^knowledge-work-sdlc 0\.7\.0/m);
});

test('invalid options fail before touching a workspace', () => {
  const p = client('bad-args'); const before = snapshot(p);
  assert.equal(cli(['install', p, '--source-root', ROOT]).status, 2);
  assert.deepEqual(snapshot(p), before);
});

test('missing or explicitly invalid Python fails without mutation', () => {
  const p = client('no-python'); const before = snapshot(p);
  const r = cli(['install', p], { env: { ...process.env, KNOWLEDGE_WORK_PYTHON: '/no/such/python' } });
  assert.equal(r.status, 2); assert.match(r.stderr, /Python 3.10/);
  assert.deepEqual(snapshot(p), before);
});

test('real packed install preserves client content and matches canonical projection', () => {
  const p = client('project with spaces');
  const agents = '# Existing project\n\nKeep my instructions.\n';
  fs.writeFileSync(path.join(p, 'AGENTS.md'), agents);
  fs.mkdirSync(path.join(p, '.agents/skills/client-skill'), { recursive: true });
  fs.writeFileSync(path.join(p, '.agents/skills/client-skill/SKILL.md'), '# Client skill\n');
  fs.writeFileSync(path.join(p, 'analysis.md'), 'client work\n');
  const before = snapshot(p);
  const preview = JSON.parse(ok(cli(['install', '.', '--dry-run'], { cwd: p })).stdout);
  assert.equal(preview.writes_performed, false);
  assert.deepEqual(snapshot(p), before);
  const result = JSON.parse(ok(cli(['install', '.'], { cwd: p })).stdout);
  assert.equal(result.validation_passed, true);
  assert.ok(fs.readFileSync(path.join(p, 'AGENTS.md'), 'utf8').startsWith(agents));
  assert.equal(fs.readFileSync(path.join(p, '.agents/skills/client-skill/SKILL.md'), 'utf8'), '# Client skill\n');
  assert.equal(fs.readFileSync(path.join(p, 'analysis.md'), 'utf8'), 'client work\n');
  validate(p);
});

test('reinstallation refuses rather than overwriting state', () => {
  const p = client('already-installed'); ok(cli(['install', p]));
  const before = snapshot(p);
  assert.equal(cli(['install', p]).status, 2);
  assert.deepEqual(snapshot(p), before);
});

test('existing skill collision is preserved with no partial install', () => {
  const p = client('collision');
  fs.mkdirSync(path.join(p, '.agents/skills/kw-recall'), { recursive: true });
  fs.writeFileSync(path.join(p, '.agents/skills/kw-recall/SKILL.md'), 'belongs to client');
  const before = snapshot(p);
  assert.equal(cli(['install', p]).status, 2);
  assert.deepEqual(snapshot(p), before);
});

test('an existing shell-installed workspace upgrades through the npm package', () => {
  const p = client('shell-to-npm'); ok(run('bash', [path.join(ROOT, 'install.sh'), p]));
  const history = path.join(p, 'ai_docs/history.md'); fs.writeFileSync(history, 'Retain history.\n');
  const before = snapshot(p);
  assert.equal(JSON.parse(ok(cli(['upgrade', p])).stdout).mode, 'dry-run');
  assert.deepEqual(snapshot(p), before);
  assert.equal(JSON.parse(ok(cli(['upgrade', p, '--apply'])).stdout).validation_passed, true);
  assert.equal(fs.readFileSync(history, 'utf8'), 'Retain history.\n');
  validate(p);
});

test('edited managed files block an upgrade without losing the edit', () => {
  const p = client('edited-managed'); ok(cli(['install', p]));
  fs.appendFileSync(path.join(p, '.knowledge-sdlc/references/working-memory.md'), '\nClient edit\n');
  const before = snapshot(p);
  assert.equal(cli(['upgrade', p, '--apply']).status, 2);
  assert.deepEqual(snapshot(p), before);
});

test('recovery dispatches to the guarded installer and preserves research', () => {
  const p = client('recover'); ok(cli(['install', p]));
  fs.writeFileSync(path.join(p, 'ai_docs/history.md'), 'retained');
  const before = snapshot(p);
  const code = "import sys; from pathlib import Path; sys.path.insert(0,sys.argv[1]+'/tests'); sys.path.insert(0,sys.argv[1]); from test_installation import stage_recovery_marker; stage_recovery_marker(Path(sys.argv[2]),Path(sys.argv[3]))";
  ok(run('python3', ['-I', '-B', '-c', code, ROOT, packedRoot, p]));
  fs.writeFileSync(path.join(p, '.agents/skills/kw-recall/SKILL.md'), 'interrupted replacement');
  assert.equal(JSON.parse(ok(cli(['recover', p])).stdout).restored, true);
  assert.deepEqual(snapshot(p), before);
});

test('non-repository and nested directory targets are rejected', () => {
  const p = path.join(tmp, 'not-a-repo'); fs.mkdirSync(p);
  assert.equal(cli(['install', p]).status, 2); assert.deepEqual(snapshot(p), {});
  const root = client('nested-target'); const child = path.join(root, 'child'); fs.mkdirSync(child);
  assert.equal(cli(['install', child]).status, 2); assert.deepEqual(snapshot(root), {});
});

test('symlink destinations and self-installation are rejected', () => {
  const p = client('linked-target'); const link = path.join(tmp, 'alias'); fs.symlinkSync(p, link, 'dir');
  assert.equal(cli(['install', link]).status, 2); assert.deepEqual(snapshot(p), {});
  assert.equal(cli(['install', packedRoot]).status, 2);
});

test('client modules and PYTHONPATH cannot shadow the packaged installer', () => {
  const p = client('hostile-python');
  fs.writeFileSync(path.join(p, 'tooling.py'), 'raise RuntimeError("wrong installer")');
  fs.writeFileSync(path.join(p, 'sitecustomize.py'), 'raise RuntimeError("ambient module")');
  ok(cli(['install', '.'], { cwd: p, env: { ...process.env, PYTHONPATH: p } }));
  validate(p);
});

test('shell metacharacters in a real target name are passed literally', () => {
  const p = client('work; literal $name'); ok(cli(['install', p])); validate(p);
});

test('npm exec runs the packed artifact without registry access', () => {
  const p = client('npm-exec');
  const r = ok(run('npm', ['exec', '--offline', '--yes', `--package=${tarball}`, '--',
    'knowledge-work-sdlc', 'install', '.', '--dry-run'], { cwd: p }));
  assert.equal(JSON.parse(r.stdout).writes_performed, false);
  assert.deepEqual(snapshot(p), {});
});
