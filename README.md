# Knowledge Work SDLC

**One accountable agent across many durable initiatives—for defensible
professional work.**

Knowledge Work SDLC gives a professional lead one main agent through which to
commission and continue multiple bodies of work. It turns an ordinary request
into a result another capable professional can inspect, correct, and continue.

It adds a compact operating contract, on-demand skills, bounded specialist
roles, readable recipes, durable artefact templates, and safe distribution.
The host agent remains the only orchestrator.

It does not add a workflow server, a case-management layer, a model router, or
a hidden memory system.

## One agent, many initiatives

Most agent interfaces organise work around conversations. As the work grows,
the user has to remember which thread contains which decision, choose which
agent to ask, repeat context, and reconcile competing answers. The user becomes
the router, memory system, and integration layer.

Knowledge Work SDLC organises work around the undertaking instead. The user
states the desired outcome to one accountable main agent. That agent identifies
or creates the relevant initiative, reconstructs its current state, composes the
next run, and brings in bounded fresh specialists only when the work warrants
them. The main agent remains responsible for reconciliation and the result.

A session is where an agent happens to execute; an **initiative** is the durable
body of work created by one accepted intent. Sessions and specialists may come
and go while the initiative preserves its meaning, evidence, outputs,
decisions, limitations, and next action. Multiple initiatives can therefore
coexist without becoming one giant context or a collection of disconnected
chats.

```text
centralise accountability     one main agent owns the undertaking
partition semantic state      each initiative retains its own history
decentralise bounded work      fresh specialists contribute when useful
carry work through artefacts  sessions are disposable; meaning is not
```

The commissioner experiences one continuing relationship with the work, not an
agent topology they must operate.

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

## Cold-start dependency chart

Read this console from `[00]` to `[07]`. `-->` marks activation or control,
`==>` marks durable state, and `..>` marks a dependency included only when the
commission earns it.

```text
+============================================================================+
| KNOWLEDGE WORK SDLC // COLD-BOOT TO FRESH-SESSION RESUME                   |
+============================================================================+

  CONCEPTUAL CONSOLE                 ACTUAL SYSTEM SURFACE
  ------------------                 ---------------------
  HOST / CPU + I-O                   model, tools, files, approvals
  BOOT INSTRUCTIONS                  AGENTS.md
  PROGRAM LIBRARY                    skills, recipes, specialist definitions
  WORK DISK                          ai_docs/ initiative state and artefacts
  RUNNING EXECUTIVE                  the host's main agent

[00] CANONICAL METHOD SOURCE
     AGENTS.md + .knowledge-sdlc/ + mechanical installer
          |
          |  ./install.sh /absolute/path/to/client-repository
          v
[01] CLIENT REPOSITORY / INSTALLED METHOD
     +-- AGENTS.md ---------------- standing operating contract
     +-- .agents/skills/ ---------- host-discoverable procedures
     +-- .knowledge-sdlc/
     |   +-- agents/ -------------- bounded fresh-worker definitions
     |   +-- recipes/ ------------- composition defaults
     |   +-- templates/ ----------- shapes for earned artefacts
     |   `-- install.json --------- managed-file ownership
     `-- ai_docs/initiatives/index.md -- neutral identity/status pointer
          |
          |  open this repository in a compatible agent host
          v
[02] HOST BOOT
     host supplies model + execution + tools + permissions
     host discovers AGENTS.md + skills; no SDLC server is launched
          |
          |  user states one ordinary professional commission
          v
[03] MAIN AGENT :: CONCIERGE POSTURE
     reads the compact initiative index first
     preserves exact wording ==> meaning-r1.md
     creates initiative ID + run ID ==> open run record
          |
          |  accepted meaning is settled enough to act
          v
+----------------------------------------------------------------------------+
| [04] MAIN AGENT :: ORCHESTRATOR POSTURE                                    |
|                                                                            |
| REQUIRED STATE     meaning revision + open run record                      |
| COMPOSITION INPUT  nearest recipe + confirmed context + admitted methods  |
| RECORDED CONTROL   execution plan, rationale, gates, next legal action     |
|                                                                            |
|      +--> [INLINE SKILL] -----------------------------------+               |
|      +..> [FRESH BOUNDED SPECIALIST] -----------------------+               |
|      +..> [HOST TOOL / EXCEL / MCP / CLI AFTER PREFLIGHT] --+==> ARTEFACTS |
|      `..> [HUMAN DECISION FOR CONSEQUENTIAL AUTHORITY] -----+               |
|                                                                            |
| A specialist may produce its named output; it cannot route, spawn,         |
| reconcile, or approve the run. Those obligations return here.              |
+----------------------------------------------------------------------------+
          |
          |  every material stage follows one save order
          v
[05] DURABLE SAVE ORDER
     semantic output ==> open run record ==> compact initiative index
          |
          v
[06] USER RETURN
     useful work product or decision-grade blocker
     + material limitation + next action + run status
          |
          |  the conversation may end; semantic state remains
          v
[07] FRESH SESSION / REPLACEMENT MAIN AGENT
     index --> user confirms initiative --> kw-prime
           --> active run + meaning + decisions + named live outputs
           --> kw-orchestration resumes the same run at [04]

     NO TRANSCRIPT REPLAY.  NO SECOND MANAGER.  NO PARALLEL CONTROL PLANE.
```

The central orchestrator therefore depends on four things: a host that can
execute, the installed contract that gives the main agent its posture, one
initiative's durable meaning and run state, and the named artefacts that carry
work back from tools or specialists. Recipes guide composition and capabilities
enable operations, but neither can seize orchestration authority.

To audit a run, start at `[04]` and walk backwards: without the host there is no
agent; without the installed contract there is no Knowledge Work behaviour;
without meaning and an open run record there is no governed plan. Then walk
forwards: without a named output there is no handoff, and without the save order
there is no reliable fresh-session continuation.

This is a static contract trace, not proof that every host activates it. A host
must actually discover the installed instructions and skills, and any required
tool or fresh-specialist capability must be observed for that run.

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
