#!/usr/bin/env node
'use strict';

// A transport for the canonical Python installer, not a second installer.
const fs = require('node:fs');
const path = require('node:path');
const { spawn, spawnSync } = require('node:child_process');

const ROOT = path.resolve(__dirname, '..');
const METADATA = JSON.parse(fs.readFileSync(path.join(ROOT, 'package.json'), 'utf8'));
const HELP = `Knowledge Work Meta-Harness

Usage:
  knowledge-work-sdlc install [target] [--dry-run]
  knowledge-work-sdlc upgrade [target] [--dry-run | --apply]
  knowledge-work-sdlc recover [target]
  knowledge-work-sdlc --version

Target defaults to the current directory and must be an existing Git root.
Install applies changes unless --dry-run is supplied. Upgrade previews changes
unless --apply is supplied. Recover restores an interrupted guarded upgrade.
Existing project instructions and skills are preserved; collisions are refused.
Open a fresh agent task after installation to load the skills.

Requires Node.js 22+, Git and Python 3.10+ at installation time.
KNOWLEDGE_WORK_PYTHON may name an exact Python executable (not a shell command).
`;

function parseArgs(args) {
  if (!args.length || (args.length === 1 && ['--help', '-h'].includes(args[0]))) {
    return { help: true };
  }
  if (args.length === 1 && ['--version', '-v'].includes(args[0])) {
    return { version: true };
  }
  const [command, ...rest] = args;
  if (!['install', 'upgrade', 'recover'].includes(command)) {
    throw new Error(`Unknown command: ${command}. Run knowledge-work-sdlc --help.`);
  }
  let target;
  let dryRun = false;
  let apply = false;
  let literals = false;
  for (const arg of rest) {
    if (!literals && arg === '--') { literals = true; continue; }
    if (!literals && ['--help', '-h'].includes(arg)) return { help: true };
    if (!literals && arg === '--dry-run') {
      if (dryRun) throw new Error('Do not repeat --dry-run.');
      dryRun = true;
    } else if (!literals && arg === '--apply') {
      if (apply) throw new Error('Do not repeat --apply.');
      apply = true;
    } else if (!literals && arg.startsWith('-')) {
      throw new Error(`Unknown option: ${arg}`);
    } else if (target !== undefined) {
      throw new Error('Specify exactly one installation target.');
    } else {
      if (!arg.trim()) throw new Error('The installation target cannot be empty.');
      target = arg;
    }
  }
  if (dryRun && apply) throw new Error('Choose --dry-run or --apply, not both.');
  if (apply && command !== 'upgrade') throw new Error('--apply is only used with upgrade.');
  if (command === 'recover' && (dryRun || apply)) {
    throw new Error('recover does not accept --dry-run or --apply.');
  }
  return { command, target: target ?? '.', dryRun, apply };
}

function pythonCommand() {
  const explicit = process.env.KNOWLEDGE_WORK_PYTHON;
  const candidates = explicit
    ? [[explicit, []]]
    : [['python3', []], ['python', []], ...(process.platform === 'win32' ? [['py', ['-3']]] : [])];
  for (const [executable, prefix] of candidates) {
    const result = spawnSync(executable, [...prefix, '-I', '-B', '-c',
      'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 2)'],
      { encoding: 'utf8', timeout: 5000, windowsHide: true, shell: false });
    if (!result.error && result.status === 0) return { executable, prefix };
  }
  throw new Error(explicit
    ? 'KNOWLEDGE_WORK_PYTHON must point to a working Python 3.10+ executable.'
    : 'Python 3.10+ was not found. Install Python or set KNOWLEDGE_WORK_PYTHON to its executable.');
}

async function main(args) {
  const options = parseArgs(args);
  if (options.help) { process.stdout.write(HELP); return 0; }
  if (options.version) { console.log(`${METADATA.name} ${METADATA.version}`); return 0; }
  const methodVersion = fs.readFileSync(path.join(ROOT, '.knowledge-sdlc', 'VERSION'), 'utf8').trim();
  if (methodVersion !== METADATA.version) {
    throw new Error(`Package ${METADATA.version} disagrees with bundled method ${methodVersion}.`);
  }
  const target = path.resolve(process.cwd(), options.target);
  // Refuse self-installation; the source is not an agent's client workspace.
  if (fs.existsSync(target) && fs.realpathSync(target) === fs.realpathSync(ROOT)) {
    throw new Error('Choose a client repository, not this package source directory.');
  }
  const { executable, prefix } = pythonCommand();
  const flags = [];
  if (options.command === 'upgrade') flags.push('--upgrade');
  if (options.command === 'recover') flags.push('--recover');
  if (options.dryRun) flags.push('--dry-run');
  if (options.apply) flags.push('--apply');
  // Isolated Python ignores PYTHONPATH and the client's current directory.
  // Insert only this package's root so a client tooling.py cannot shadow ours.
  const bootstrap = "import runpy,sys; sys.path.insert(0,sys.argv.pop(1)); runpy.run_module('tooling.installer',run_name='__main__')";
  const child = spawn(executable,
    [...prefix, '-I', '-B', '-c', bootstrap, ROOT, '--source-root', ROOT, ...flags, target],
    { cwd: ROOT, stdio: 'inherit', windowsHide: true, shell: false });
  const onInt = () => child.kill('SIGINT');
  const onTerm = () => child.kill('SIGTERM');
  process.on('SIGINT', onInt);
  process.on('SIGTERM', onTerm);
  const result = await new Promise((resolve, reject) => {
    child.once('error', reject);
    child.once('close', (code, signal) => resolve(code ?? (signal === 'SIGINT' ? 130 : 143)));
  }).finally(() => {
    process.removeListener('SIGINT', onInt);
    process.removeListener('SIGTERM', onTerm);
  });
  if (result === 0 && options.command === 'install' && !options.dryRun) {
    console.error('Installed. Open a fresh agent task in the target repository.');
  }
  return result;
}

if (require.main === module) {
  main(process.argv.slice(2)).then(code => { process.exitCode = code; }).catch(error => {
    console.error(`knowledge-work-sdlc: ${error.message}`);
    process.exitCode = 2;
  });
}
module.exports = { parseArgs };
