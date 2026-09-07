# Knowledge Work SDLC

![Louis-Alexandre Berthier, Napoleon's chief of staff](docs/assets/louis-alexandre-berthier.jpg)

> **Louis-Alexandre Berthier (1753–1815)** was a Marshal of the Empire and
> chief of staff of Napoleon's Grande Armée.
>
> He developed and ran the staff system that let Napoleon command widely
> separated corps as one army.
>
> During the Waterloo campaign, Berthier's absence contributed to confused
> orders, delayed communications, and wasted movement. Napoleon later said of
> Waterloo: “If I had had Berthier, I would not have met this misfortune.”
>
> Sources: [Fondation Napoléon](https://www.napoleon.org/en/history-of-the-two-empires/biographies/berthier-louis-alexandre/)
> and [Defence in Depth](https://defenceindepth.co/2015/06/15/the-road-to-waterloo/).

Knowledge Work SDLC is a portable context life cycle, distributed as an
installable plugin and repository skill set. It lets one accountable agent
delegate and review bounded specialist work while project files keep each
undertaking resumable.

The method runs inside a compatible host and works beside the skills,
templates, and tools a professional team already uses.

The host supplies the model, execution, tools, and permissions. The context
life cycle supplies a method for commissioning work, producing it, checking it,
resuming it, and learning from correction without turning old experience into
new fact.

Install it into a repository or load the generated plugin package. State the
work in ordinary language. One main agent remains answerable for the
undertaking. Fresh specialists return their part without becoming new
relationships for the user to manage.

## Contents

- [Install](#install)
- [First commission](#first-commission)
- [Why knowledge work needs a life cycle](#why-knowledge-work-needs-a-life-cycle)
- [The life cycle](#the-life-cycle)
- [One main agent, many initiatives](#one-main-agent-many-initiatives)
- [Architecture](#architecture)
- [Bring your own practice](#bring-your-own-practice)
- [Continuity, memory, and feedback](#continuity-memory-and-feedback)
- [Distribution and provider boundaries](#distribution-and-provider-boundaries)
- [Repository map](#repository-map)
- [Documentation](#documentation)
- [Validation and claim limits](#validation-and-claim-limits)
- [Intellectual background](#intellectual-background)
- [Contributing](#contributing)
- [Licence](#licence)

## Install

> **Installing into an existing repository**
>
> The installer preserves the existing `AGENTS.md` and appends one marked
> Knowledge Work block. Existing project skills remain in place unless an
> installed skill would occupy the same path; any such collision stops the
> installation without overwriting the client file.
>
> The agent host will read both instruction sets. The installer can detect file
> collisions, but it cannot judge contradictions in meaning. Conflicting rules
> about delegation, writing, review, or project state must be resolved before
> relying on the combined setup.

The repository route needs Git, Python 3.10 or newer, and an existing client
repository.

```bash
git clone https://github.com/TJ4519/knowledge-work-sdlc.git
cd knowledge-work-sdlc
./install.sh /absolute/path/to/client-repository
```

Open the client repository in a new agent task after installation. The
installer preserves existing project instructions and skills. It adds the
Knowledge Work operating contract, discoverable procedures, and method files.

Codex, Claude Code, and Claude Cowork can also load a generated plugin archive.
The [latest release](https://github.com/TJ4519/knowledge-work-sdlc/releases/latest)
contains the archive, which needs no Python at run time.

The [installation and provider guide](docs/guides/installation-and-providers.md)
gives the exact route supported by each host.

## First commission

A commission is the piece of work entrusted to the agent, together with its
purpose and intended use.

Address the agent as you would address a capable colleague:

```text
Compare the two source packs. Tell me which explanation is better supported,
where the evidence remains weak, and what would change the conclusion. Give me
a one-page decision brief.
```

No stage names or workflow commands are required. The main agent preserves the
commission, inspects the available material, settles the meaning that matters,
and composes a proportionate route through the installed methods.

The visible result remains the object you asked for. The files written behind
it let another capable agent inspect the evidence, correct the reasoning, or
continue the same undertaking after the conversation has ended.

See [Getting started](docs/getting-started.md) for one complete journey through
installation, production, correction, and continuation in a fresh task.

## Why knowledge work needs a life cycle

Software teams do not mistake a plausible code response for a finished system.
They preserve requirements, control dependencies, inspect changes, run checks,
keep versions, and retain a route back when a release goes wrong.

Knowledge work seldom receives equal discipline. A brief can read well while
using the wrong definition. A spreadsheet can keep its appearance after a
formula breaks.

A recommendation can outrun its sources. A decisive correction can disappear
with the chat in which it was given.

AI widens the gap. A lead can correct one definition on Tuesday, then receive a
polished Friday answer built on the old definition. The later agent may never
see the correction, its source, or the decision it changed.

[The New SDLC With Vibe Coding](https://www.kaggle.com/whitepaper-the-new-SDLC-with-vibe-coding)
describes coding agents moving human effort away from syntax and towards
intent, architecture, and judgment.

Knowledge work begins on that side of the boundary. Its raw material is already
language.

Faster drafting therefore leaves the difficult work in place. Someone must
settle the commission, choose what deserves reliance, preserve the reasoning,
and decide what may act on the world.

The letters **SDLC** are used in that sense. A memo is not software, and a
professional judgment cannot be compiled. Both still need a life before and
after generation: intent, dependencies, production, challenge, release,
maintenance, and recovery.

| Software discipline | Knowledge-work counterpart |
|---|---|
| Requirements | The exact commission and a visible, correctable interpretation |
| Source and dependencies | Evidence, professional methods, templates, and live capabilities |
| Build | A candidate document, model, analysis, or decision product |
| Test and review | Provenance, native-object checks, and independent challenge when consequence warrants it |
| Release | Explicit human disposition and protected promotion |
| Versioning and maintenance | Initiative history, corrected successors, continuation, and governed learning |

The analogy supplies discipline rather than certainty. Code often has an
executable specification.

Knowledge work more often has incomplete evidence, contested meanings, and
decisions whose authority belongs to a person. The method keeps those
differences visible.

## The life cycle

One accepted intent creates an **initiative**: the durable identity of the
undertaking. One composed attempt or follow-on pass creates a **run** inside
that initiative.

1. **State the work.** The user gives an ordinary professional commission. The
   agent preserves the wording before it starts to improve or interpret it.
2. **Settle the meaning.** The agent identifies the desired object, audience,
   use, scope, material assumptions, and rival readings. It asks only when an
   unresolved point could change the route or result.
3. **Compose the run.** The main agent adapts the nearest recipe. It records the
   methods included, the methods pruned, the required inputs, and each gate.
4. **Bind evidence and capability.** Sources remain distinguishable from
   inference. A tool or connector is trusted only for the exact operation that
   the eventual worker can harmlessly prove.
5. **Produce the candidate.** The main agent may work directly or commission a
   bounded specialist. Each worker receives named inputs and returns a named
   artefact rather than a conversational recap.
6. **Challenge and decide.** Consequential work receives a fresh challenge when
   the host can supply one. A human retains authority over protected changes,
   admitted methods, and material promotion.
7. **Save and continue.** Semantic artefacts are written first, the open run
   record second, and the compact initiative index last. A fresh task can then
   reconstruct only the relevant work.
8. **Correct and learn.** A correction repairs the present work before any
   reusable lesson is proposed. Later influence requires a separate, reversible
   human decision and a bounded use whose effect can be inspected. A defect in
   the method takes a separate route before any skill changes.

```text
ordinary commission
        |
        v
correctable meaning --> evidence and capability --> composed run
                                                    |
                                                    v
                                  candidate work product
                                                    |
                                      challenge when earned
                                                    |
                                                    v
                                      human disposition
                                                    |
                         +--------------------------+-------------------+
                         |                                              |
                         v                                              v
                durable continuation                       governed correction
```

Six included recipe families cover professional research, source
interpretation, independent challenge, protected-artifact updates,
knowledge-work correction, and method adaptation.

The recipes are starting routes, not a closed vocabulary of professions or an
executable state machine.

The return appears as the work accumulates. A later run can reuse confirmed
project context, admitted methods, evidence paths, and exact decisions without
asking the user to rebuild a prompt or trust an old conversational summary.

## One main agent, many initiatives

A person usually delegates an outcome to one accountable colleague. A swarm
quietly reverses that arrangement when every specialist becomes another thread
whose brief, status, and disagreements the user must carry.

Knowledge Work SDLC preserves that relationship. The agent first acts as a
concierge: it works out which undertaking the request belongs to and what the
commission means. It then acts as the orchestrator for the accepted run.

Several initiatives can coexist without sharing their substance. The compact
index reveals their identity and status; each initiative retains its own
meaning, evidence, decisions, and outputs.

```text
you
 `-- one accountable main agent
      |-- supplier-risk initiative
      |-- renewal initiative
      |-- policy-redraft initiative
      `-- temporary specialist work when one run earns it
```

Specialists add cognition, tool access, or an independent reading. They do not
become new managers. The main agent alone composes the run, dispatches work,
reconciles disagreement, records the state, and returns to the user.

Central orchestration therefore removes a human coordination burden. Durable
initiatives prevent that convenience from becoming one enormous conversation
or one undifferentiated memory.

## Architecture

The diagram follows a clean installation from canonical source to a useful
result and then to a fresh-session continuation. `-->` marks control,
`==>` marks durable state, and `..>` marks a dependency included only when the
commission earns it.

```text
+============================================================================+
| KNOWLEDGE WORK SDLC // SOURCE, RUNTIME, WORK, AND CONTINUATION              |
+============================================================================+

[00] CANONICAL METHOD SOURCE
     AGENTS.md + skills + recipes + specialist definitions + templates
          |
          |  repository install or generated plugin package
          v
[01] COMPATIBLE AGENT HOST
     host supplies model + execution + tools + permissions
     installed lifecycle supplies standing rules + callable procedures
          |
          |  one ordinary-language commission
          v
[02] MAIN AGENT :: CONCIERGE
     compact index distinguishes new work from continuation
     exact request ==> meaning-r1.md
     accepted intent ==> initiative ID + run ID + open run record
          |
          |  meaning is settled enough to act
          v
+----------------------------------------------------------------------------+
| [03] MAIN AGENT :: ORCHESTRATOR                                            |
|                                                                            |
|  INPUTS     current meaning + confirmed context + evidence + bound methods |
|  PLAN       nearest recipe adapted to this commission and recorded in run  |
|  AUTHORITY  compose, dispatch, retry, replan, gate, reconcile, save         |
|                                                                            |
|      +--> [INLINE SKILL IN MAIN CONTEXT] -------------------+               |
|      +..> [FRESH BOUNDED SPECIALIST] -----------------------+               |
|      +..> [EXCEL / CONNECTOR / MCP / CLI AFTER PREFLIGHT] --+==> ARTEFACTS |
|      `..> [HUMAN DECISION FOR MATERIAL AUTHORITY] ----------+               |
|                                                                            |
|  Specialists return named outputs. They cannot route, spawn, reconcile,   |
|  approve, or become a second orchestrator.                                 |
+----------------------------------------------------------------------------+
          |
          |  candidate and evidence are sufficient for the planned gate
          v
[04] CHALLENGE AND DISPOSITION
     candidate ..> fresh producer-independent challenge when earned
     findings  --> targeted correction or explicit degraded/blocked state
     protected or consequential action --> exact human disposition
          |
          v
[05] DURABLE SAVE ORDER
     semantic output ==> open run record ==> compact initiative index
          |
          +-------------------------------+
          |                               |
          v                               v
[06] USER RETURN                    [07] FRESH TASK OR HOST PROCESS
     useful work product                 index --> initiative confirmation
     material limitation                 --> kw-prime reads active run
     next executable action              --> current meaning and live outputs
                                          --> same run resumes at [03]

     NO TRANSCRIPT REPLAY.  NO SECOND MANAGER.  NO PARALLEL CONTROL PLANE.

[08] MATERIAL FEEDBACK, WHEN IT OCCURS
     correct present work first
          |
          +..> reusable preference or review heuristic?
          |      --> inactive lesson candidate + rival reading
          |      --> exact human retain / amend / reject
          |      --> later initiative interpreted without lesson content
          |      --> neutral nomination + Select / Narrow / Decline
          |      --> one bounded pending effect + observable outcome
          |      --> retain / revise / suspend / retire
          |
          `..> defect in an installed professional method?
                 --> separate method-adaptation initiative
                 --> evidence + candidate change + fresh challenge
                 --> exact human Adopt / Amend / Reject
                 --> separate source-change commission before any skill edit
```

Four files carry four different authorities. `AGENTS.md` and skills carry the
operating method. The initiative index carries identity and status. The run
record carries the plan and progress. Linked artefacts carry the professional
substance.

No universal case file or generated master summary competes with those owners.
Scripts project and inspect the method, but they do not interpret a commission,
select a recipe, judge evidence, or grant authority.

## Bring your own practice

The core is deliberately profession-neutral. Existing host and project skills
may continue to help the agent. Their presence does not silently turn them into
project policy or give them control over the initiative.

A durable method supplied by a professional lead can be imported as an expert
extension. Import establishes custody; curation exposes purpose, inputs,
outputs, tools, conflicts, and authority.

A human admits one immutable revision and a run binds it explicitly.

```text
import method bytes
→ curate contract and conflicts
→ human admits immutable revision A
→ one run binds A for one stated effect
→ an update creates revision B
→ old runs still resolve A
→ suspend or retire future eligibility without erasing history
```

A client workbook, document, or slide template remains a protected input. The
agent records which parts carry shape, method, or policy, works in a candidate
copy, checks the native object, and waits for exact authority before replacing
the original.

Connectors, MCP servers, Excel, and CLIs remain host capabilities. The plan
first derives the operation it needs. The orchestrator then finds a plausible
facility, checks access, and proves the harmless operation for the same actor
who will produce the work.

```text
required operation
→ visible facility
→ reachable asset
→ authentication and scope
→ harmless same-actor proof
→ bind, degrade, or stop
```

The method therefore travels without a hard-coded connector catalogue. An
installation does not confer access, and a successful operation in one host
does not prove that another host can perform it.

## Continuity, memory, and feedback

Continuity answers one narrow question: what must a fresh agent read to resume
this undertaking correctly? The answer is an index entry, the selected run,
its current meaning and decisions, and the live outputs named by that run.

```text
initiative index
→ user names or confirms one initiative
→ prime reads its active or latest run
→ prime reads current meaning, decisions, and named live outputs
→ orchestration resumes at the next warranted action
```

Conversation transcripts are neither required nor replayed. The useful facts
are written to the file that owns them when they become material. Fresh-session
cost follows the current work rather than the length of its chat history.

The agent does not reload the repository as one giant prompt. Standing rules
remain thin, and methods load when called.

The index selects one initiative, and the run record names the live files. Each
piece of context has an owner and a reason to enter the present task.

Personalisation answers a different question: may a correction from one
initiative influence later work? Automatic reuse would convert an old episode
into present truth. Knowledge Work SDLC uses a slower, inspectable route.

```text
material correction with an observed consequence
→ source-linked lesson candidate
→ human retain, amend, or reject
→ later commission interpreted without lesson content
→ one neutral nomination
→ human Select, Narrow, or Decline for one pending step
→ observable outcome
→ retain, revise, suspend, or retire
```

Provider-native memory has no authority in either path. A provider may remember
something useful, but remembered content is not project evidence, a continuation
record, an admitted method, or permission to influence new work.

A flaw in an installed procedure follows a different path. The agent opens a
method-adaptation initiative, traces the observed error to the current method,
proposes a candidate change, and sends it through fresh challenge and human
disposition.

An adopted proposal opens a separate source-change commission. Only that later
work may revise and release a skill.

The feedback loop can therefore compound human steering into better procedures
without allowing one persuasive episode to rewrite the system that judged it.

## Distribution and provider boundaries

Knowledge Work SDLC has one authored method and two generated delivery shapes.

| Delivery shape | What it supplies | What it leaves alone |
|---|---|---|
| Repository install | A managed `AGENTS.md` block, discoverable skills, method resources, and a neutral initiative index | Client instructions, client skills, credentials, tools, and all later project state |
| Plugin archive | Native Codex and Claude manifests, skills, specialists, recipes, templates, and user documentation | Python, hooks, connectors, credentials, models, and client files |

The method is model-neutral and avoids provider-specific professional logic.
Runtime compatibility remains an observed claim.

A host must actually discover the instructions, load the skills, expose the
required tools, and support any fresh-worker behaviour claimed for that run.

Delegated work uses the concierge model by default when the host exposes exact
inheritance. The method never chooses a cheaper or different model on its own.
A user may configure an explicit override where the host supports one.

## Repository map

```text
knowledge-work-sdlc/
  README.md                 product orientation, install, and first use
  AGENTS.md                 canonical standing operating contract
  DESIGN.md                 exact architecture and authority boundaries
  install.sh                repository installation entry
  .knowledge-sdlc/
    agents/                 bounded specialist definitions
    skills/                 one authored procedure corpus
    recipes/                adaptable composition routes
    templates/              shapes for earned durable artefacts
  docs/                     methodology, getting started, and focused guides
  examples/manual-exercises optional human-run journeys and fixtures
  tooling/                  projection, installation, packaging, and checks
  tests/                    mechanical contract and distribution tests
```

Python exists only in the source repository. It validates declared relations,
installs without taking ownership of client state, generates deterministic
delivery shapes, and builds a source-bound archive.

Installed workspaces and plugin packages contain no Python runtime.

## Documentation

The documentation follows the order in which a reader acquires the system:

```text
README.md                  what the product is, why it exists, and first use
docs/getting-started.md    one ordinary end-to-end journey
docs/methodology.md        governing problem and invariants
DESIGN.md                  exact source, runtime, state, and authority map
docs/guides/               one mechanism or operator concern per guide
AGENTS.md                  always-loaded runtime contract
.knowledge-sdlc/skills/    procedures loaded when the work calls for them
```

Start with the [documentation map](docs/README.md). Maintainers should read
[the maintainer guide](docs/guides/maintaining-the-harness.md) before
changing canonical source or building a package.

## Validation and claim limits

```bash
make validate
make package
```

`make validate` checks method relationships, containment, installation,
upgrade, generated projections, documentation links, and package structure.
Those checks establish mechanical properties of an exact source revision.

They do not prove that an agent understood a commission, that a professional
work product is useful, or that a host supplied an independent reviewer.

Those claims require observed use on the named host, with the commission,
revision, outputs, and limitations retained.

## Intellectual background

Knowledge Work SDLC applies the lifecycle argument in
[The New SDLC With Vibe Coding](https://www.kaggle.com/whitepaper-the-new-SDLC-with-vibe-coding)
outside software.

Professional work lacks code's compiler and executable truth. Its discipline
therefore rests on meaning, evidence, challenge, human authority, continuation,
and correction.

## Contributing

Questions and defect reports are welcome through
[GitHub Issues](https://github.com/TJ4519/knowledge-work-sdlc/issues).

Discuss a material method or architecture change before preparing a
contribution. The authority and projection boundaries are easy to duplicate by
accident.

## Licence

Copyright © 2026 TJ4519. All rights reserved. See [LICENSE.md](LICENSE.md).
