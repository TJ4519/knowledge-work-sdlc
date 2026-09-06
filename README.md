# Knowledge Work SDLC

**One agent to talk to. Work that survives the conversation.**

Your work is not a pile of AI chats. It is a set of ongoing decisions,
investigations, documents, and models. Those undertakings outlive whichever
conversation happened to start them.

Most AI tools make you carry that continuity yourself. As conversations and
specialist agents multiply, you become the person asking:

- “Which chat has the latest version?”
- “Which agent did I tell about that constraint?”
- “Do I need to paste the sources and explain the work again?”
- “Which answer is current when two agents disagree?”

Knowledge Work SDLC removes that coordination job. Tell one main agent what you
need in ordinary language. It restores the right work, brings in specialist
help when useful, reconciles the result, and leaves the work ready to continue.

**You do not operate the SDLC. The agent does.**

## One agent, many initiatives

Imagine using the same agent across a working week:

**Monday:** “Work out whether the supplier delay threatens our launch.”

**Tuesday:** “Review whether the renewal weakness is temporary.”

**Friday:** “Continue the launch-risk work with the new supplier schedule.”

The first two requests become separate **initiatives**—durable bodies of work
created by accepted intents. On Friday, the main agent reloads only the
launch-risk initiative and continues from its evidence, decisions, and outputs.

The user does not find the old chat, choose a specialist, or reconstruct the
brief. Sessions and specialists can come and go because the initiative—not the
conversation—preserves what the work means and where it has reached.

If the launch analysis needs one contract checked, the main agent can ask a
fresh specialist. The finding returns to the main agent instead of becoming
another conversation the user must manage.

```text
you
 `-- one accountable main agent
      |-- launch-risk initiative
      |-- renewal initiative
      `-- fresh specialist work when useful
```

The harness centralises responsibility, not thought. The main agent can
distribute bounded work, but specialists return their contribution instead of
becoming more relationships for the user to manage.

Behind that experience, instructions guide the agent and durable files carry
the work. The repository adds no workflow server, case-management layer, model
router, or hidden memory system.

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
say what you need
→ the main agent identifies or creates the right initiative
→ it composes the work and brings in fresh specialists only when useful
→ it returns the useful result through the same relationship
→ it saves the meaning, evidence, decisions, outputs, and next action
→ a fresh session can continue without a reconstructed chat
```

The simple journey above is the product. The full chart below exposes the
mechanism for readers who want to audit how installation, orchestration,
artefact handoff, and fresh-session recovery connect.

<details>
<summary>Open the full cold-start dependency chart</summary>

<br>

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

</details>

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
specialist definitions, method resources, and documentation. It contains no
profession-specific method bundle, Python runtime, credentials, connectors, or
hooks.

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
