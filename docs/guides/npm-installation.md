# Install with npm or npx

The npm package runs the existing guarded installer. It carries the method and
its resources together; it does not fetch a different method after installation.
Node.js 22 or newer, Python 3.10 or newer, Git, and an existing client Git
repository are required. Python runs during installation and upgrades, not during
agent work. The licence in `LICENSE.md` applies to this distribution.

## Run directly from GitHub

From the project where the agent will work, preview the installation:

```bash
cd /absolute/path/to/your-project
npx --yes --package=https://github.com/TJ4519/knowledge-work-sdlc/archive/refs/heads/main.tar.gz knowledge-work-sdlc install . --dry-run
```

Review the preview and any material conflict between the existing project
instructions and the proposed Knowledge Work instructions, then install:

```bash
npx --yes --package=https://github.com/TJ4519/knowledge-work-sdlc/archive/refs/heads/main.tar.gz knowledge-work-sdlc install .
```

For repeatable deployment, use the same commit archive in both commands:
`https://github.com/TJ4519/knowledge-work-sdlc/archive/<commit-sha>.tar.gz`.
Open a fresh agent task in the project after installation. Give the agent
an ordinary commission; no workflow commands are needed for the work itself.

The target must be the Git root, not a parent or nested directory. Installation
preserves existing `AGENTS.md` content and client skills, refuses managed-path
collisions, and retains the existing project-state ownership rules.

## Install an archive as a project dependency

A maintainer can produce `knowledge-work-sdlc-0.7.1.tgz` with `npm pack`.
Given a trusted copy of that archive:

```bash
npm install --save-dev /absolute/path/to/knowledge-work-sdlc-0.7.1.tgz
npx knowledge-work-sdlc install . --dry-run
npx knowledge-work-sdlc install .
```

`npm install` adds the dependency to the Node project. It does not install agent
instructions by itself. The explicit `install` command does that. There are no
`preinstall`, `install`, `postinstall` or `prepare` lifecycle scripts, no npm
runtime dependencies and no separate model calls.

## Upgrade and recovery

Use the package containing the desired method revision. Upgrade previews by
default; only `--apply` changes managed files:

```bash
npx knowledge-work-sdlc upgrade .
npx knowledge-work-sdlc upgrade . --apply
npx knowledge-work-sdlc recover .
```

These commands use an already installed npm dependency. For the direct GitHub
route, include the same `--package=<HTTPS-archive-URL>` option as for installation,
pointing to the intended revision. Recovery uses the package revision that
attempted the interrupted upgrade. Client-owned `ai_docs/` and historical work
are preserved. Edited managed files require resolution before upgrade; an npm
update alone does not replace installed agent instructions.

## Python selection and package removal

The command tries `python3`, then `python`, and the `py -3` launcher on Windows.
To select an interpreter explicitly, set `KNOWLEDGE_WORK_PYTHON` to the Python
executable path. It is a path, not a shell command. Python runs in isolated mode
so project modules and `PYTHONPATH` cannot replace the packaged installer.

`--help` and `--version` do not need Python. macOS and Linux are the exercised
installation routes. A Windows launcher is provided, but native Windows
filesystem/upgrade behaviour requires its own validation.

Removing the npm dependency removes the installer package, not the installed
method or project records. Use the existing guarded installer with an earlier
complete method revision for rollback; do not delete individual skills while
leaving their callers.

## Maintainer packaging and registry publication

From a clean reviewed source checkout:

```bash
make validate
npm test
npm pack --dry-run
npm pack
npm publish --dry-run ./knowledge-work-sdlc-0.7.1.tgz
```

Inspect the archive inventory and source version before publication. Package
version and `.knowledge-sdlc/VERSION` must agree. Every registry release must have
a new version when its content changes. Keep the existing licence unless its
owner explicitly changes it.

Publication requires npm authentication with rights to the selected package
name, and any required two-factor authentication. After signing in with that
publishing account, publish the exact tested archive:

```bash
npm publish ./knowledge-work-sdlc-0.7.1.tgz --access public
```

The GitHub installation route works independently of registry publication. Use
registry-only instructions such as `npx knowledge-work-sdlc@0.7.1 install .`
only once that version has actually been published and read back.
