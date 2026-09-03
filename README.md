# Knowledge Work SDLC

**A file-native orchestration harness for defensible professional work.**

Knowledge Work SDLC helps an agent turn an ordinary commission into work that
another capable professional can inspect, correct, and continue.

It adds a compact operating contract, on-demand skills, bounded specialist
roles, readable recipes, durable artefact templates, and safe distribution.
The host agent remains the only orchestrator.

It does not add a workflow server, a case-management layer, a model router, or
a hidden memory system.

## Quick start

Prerequisites: Git, Python 3.10 or newer, and an existing client repository.

```bash
git clone https://github.com/TJ4519/knowledge-work-sdlc.git
cd knowledge-work-sdlc
./install.sh /absolute/path/to/client-repository
```

Open the client repository in a new Codex task and state the work normally:

```text
Compare the two source packs, explain which interpretation is supportable,
and give me a one-page decision brief that preserves the unresolved disagreement.
```

There is no workflow command to learn. The installed `AGENTS.md` block supplies
standing behaviour, and `.agents/skills/` supplies procedures when the work
calls for them.

The harness creates durable initiative state behind the useful result. A fresh
agent can recover the accepted meaning, current run, evidence, outputs,
limitations, and next legal action without relying on the old conversation.

See [Getting started](docs/getting-started.md) for a complete first commission,
material correction, and fresh-task continuation.

## What it adds

| Need | Harness contribution |
|---|---|
| Research or decision brief | Source custody, rival explanations, an evidence-bearing candidate, and proportionate challenge |
| Source interpretation | Exact definitions, periods, scope, conflicts, and a correctable reading |
| Independent challenge | A fresh bounded attempt to falsify a candidate without inheriting its producer's narrative |
| Protected artefact update | Candidate-copy discipline, editable and protected scope, capability proof, conformance checks, and human promotion |
| Material correction | Superseded meaning, traced dependants, targeted re-production, and visible residual limitations |
| Method adaptation | A candidate method improvement with evidence, a falsifier, and a rollback condition |

Six included recipe families cover these common shapes without hard-coding a
profession. The main agent adapts the nearest recipe and records the resulting
execution plan. Recipes guide judgement; they are not executable state machines.

## How it works

```text
natural-language commission
→ concierge preserves wording and settles enough meaning to act
→ the same main agent composes and owns one run
→ skills handle interactive work; specialists handle bounded fresh work
→ named artefacts carry evidence and outputs between contexts
→ challenge and human gates appear only when consequence earns them
→ index + run record + live outputs make continuation recoverable
```

One accepted intent creates an **initiative**. One composed attempt or follow-on
pass creates a **run**.

The compact index owns identity and the current-run pointer. The run record owns
the plan, rationale, outcomes, limitations, gates, and next action. Output
artefacts own the professional substance.

The system deliberately has no universal case file or master summary.

## Bring your own expertise

The core method is generic. A lead can add stronger professional procedures,
house templates, project rules, and runtime tools without merging their
authority or silently modifying the core.

| Input | How the harness treats it |
|---|---|
| Stable project facts or source rules | Confirmed project context, created only when earned |
| A lead's reusable procedure | An imported, curated, immutable expert extension explicitly bound to a run |
| A workbook or document template | A protected initiative input edited only through a candidate copy |
| Excel, a connector, an MCP server, or a CLI | A runtime capability proved for the exact actor and operation |
| A correction that may help later | An inactive lesson candidate requiring human retention and later bounded selection |

Provider-global skills may remain useful supporting procedures. Discovery alone
does not make them project policy, admitted expert methods, or evidence.

## Install or package

Knowledge Work SDLC has one canonical method and two generated delivery shapes.

| Route | Use it when |
|---|---|
| Repository install | The agent works in a Git repository and reads `AGENTS.md` plus project skills |
| Plugin archive | The host accepts a Codex or Claude plugin package |

Repository installation is additive and records which files it owns. Client
instructions, client skills, and all `ai_docs/` initiative state remain
client-owned.

The plugin archive contains generated Codex and Claude manifests, skills,
specialist definitions, method resources, documentation, and an example expert
extension. It contains no Python runtime, credentials, connectors, or hooks.

See [Installation and provider boundaries](docs/guides/installation-and-providers.md)
for provider-specific routes, upgrade recovery, and capability limits.

## Why the source includes Python

The code under `tooling/` performs repeatable mechanical work:

- validate declared method and recipe relationships;
- install and upgrade managed files without overwriting client state;
- generate deterministic workspace and plugin projections; and
- build a commit-bound release archive and content manifest.

Python never interprets a commission, selects a recipe, invokes a model, judges
evidence, or grants human authority. Installed workspaces and plugin archives
contain no Python.

## Documentation

The documentation follows the system's dependency order:

```text
README.md                  orientation and first use
docs/getting-started.md    one ordinary end-to-end journey
docs/methodology.md        governing problem and invariants
DESIGN.md                  exact architecture and authority map
docs/guides/               one mechanism or operator concern per guide
AGENTS.md                  always-loaded runtime rules
.knowledge-sdlc/skills/    procedures loaded when needed
```

Start with the [documentation map](docs/README.md). Maintainers should read
[Maintaining the harness](docs/guides/maintaining-the-harness.md) before
changing canonical source or building a package.

## Validate and build

```bash
make validate
make package
```

`make validate` checks mechanical contracts, containment, installation,
upgrade, projection, documentation links, and package structure.

These checks do not prove that a host activated the method or that professional
work is useful. Inspect those claims through representative work on the exact
host and retain the observed limitations.

## Licence

Copyright © 2026 TJ4519. All rights reserved. See [LICENSE.md](LICENSE.md).
