---
name: knowledge-work
description: "Use for a new professional commission: preserve exact intent, create one initiative and run, settle material meaning, then orchestrate sufficient methods and durable artefacts."
primitive: skill
fresh_context: false
independence: main-agent-concierge-then-orchestrator
allowed_tools: ["Read", "Grep", "Shell", "Write", "Task"]
inputs: ["current-user-message", "initiative-catalogue"]
optional_inputs: ["domain-charter"]
excluded_context: ["old-transcript", "unrelated-initiative-content", "unselected-reusable-lesson"]
outputs: ["meaning", "initiative-route", "run-record"]
optional_outputs: ["decision"]
authority: proposal-and-route-control-only-no-professional-authority
standalone: true
idempotency: "Route the same accepted intent to the same initiative and an open run to its existing record; never fork authority because the host or conversation changed."
phase: intake
---
# Knowledge work intake

Use this as the single entry for a new professional commission. Preserve what
the user is trying to accomplish, not merely the grammar of the latest message.
The product is useful, defensible work—not a checklist, receipt, catalogue, or
provider event stream.

## Before substantive reading

1. Read only `ai_docs/initiatives/index.md` to distinguish continuation from
   new work. If the index is absent and no initiative content exists, create it
   from the bundled `initiative-index.md` template; this neutral discovery file
   is the only state a fresh plugin workspace may initialise before a
   commission earns anything else. If initiative directories already exist,
   do not hide them behind a blank index: reconstruct the index from their run
   records as a recovery action before routing. Do not preload another
   initiative or reusable lesson.
2. If the message clearly continues existing work, propose the likely
   initiative and load `kw-prime` after confirmation. If the route is materially
   ambiguous, ask only because the choice changes scope, authority, cost, or
   consequence.
3. For new work, create only the files this commission has earned from bundled
   templates. Do not materialise domain policy, model policy, protected-artifact,
   method, memory, or learning surfaces merely to make the workspace look
   configured. Any standing state begins `provisional`; storage preparation is
   not a setup interview or project confirmation.

## Preserve and interpret

1. Mint a stable initiative ID and first run ID. Create
   `ai_docs/initiatives/<initiative-id>/run-record/<run-id>.md` and
   `meaning-r1.md`. Record the exact discovered entry-skill path and SHA-256 in
   the run identity. This is method-activation provenance, not professional
   evidence or authority.
2. Preserve the user's exact wording in the meaning artefact. Mark it
   `provider-observed` only when the host directly exposes a native identity for
   this current task/message. A parent, source, delegation, handoff, or calling
   thread ID is transport lineage and must not be relabelled as the current
   human turn. Record such lineage separately; when current identity is not
   directly observable, use `workspace-recorded`.
3. Infer the judgeable professional outcome from the request, referenced
   objects, repository evidence, and confirmed project context. State object,
   scope, audience, period, intended use, exclusions, material assumptions,
   rival reading, and unresolved route-changing questions.
4. Bind each supplied template or protected artefact by exact path/provider
   reference, hash when readable, owner, revision, media type, shape/method/
   policy role, precedence, editable/protected scope, native features,
   candidate path, and conformance checks.
5. Complete and hash the meaning revision before inviting correction. If no
   material rival exists, proceed under the visibly attributed interpretation.
   Otherwise present the consequence and obtain an exact decision.
6. A correction targets the exact meaning path/hash. Write `meaning-r2.md` with
   a supersession link; never mutate or reconstruct r1. Update every recorded
   dependant rather than appending a caveat.

## Adequacy and degraded routes

A fresh capable professional must be able to read the run record and linked
meaning revision and identify the exact commission, useful outcome, object,
scope, audience, period, intended use, material assumption, governing human
decision, and next legal action. A generated master summary cannot discharge
that test. Before incorporating a correction, the exact meaning revision the
user saw must already exist at its recorded hash; later reconstruction fails.

- **No native turn identity:** use `workspace-recorded`; do not invent
  provider attestation.
- **Referenced object unavailable:** retain its exact reference and consequence.
  Ask only when proceeding would choose a materially different route.
- **No matching recipe:** compose from the existing methods and record why; do
  not force a catalogue label or create another control path.
- **Several unrelated commissions:** propose the split and sequence. Ask only
  when order changes material cost, risk, authority, or dependency.

Resolve harmless absence through accessible evidence and professional judgment.
Expose only uncertainty that can change the route or result; never turn the
commissioner into the author of an internal specification.

## Compose and transition

Write the initial plan to the run record before substantive production. Start
from the nearest human-readable recipe, include every method earned by meaning,
evidence, candidate quality, challenge, authority, custody, reconciliation, and
continuity, and record the rationale for each inclusion or exclusion.

Update the compact index only after the run record is coherent, then continue
as the same main agent through `kw-orchestration`. Concierge and orchestrator
are postures, not separate managers.

Host-discovered supporting skills may inform that composition, but they do not
arrive admitted, selected, or entitled to create another durable vocabulary.
Map their useful reasoning onto the existing meaning, evidence, work order,
candidate, challenge, decision, and run-record artefacts. Add a new artefact
kind only when one named downstream consumer requires a function none of those
owners can carry; record that necessity in the run before creating it.

## Feedback and expert-method routes

- An explicit request to import, inspect, update, bind, unbind, retire, or
  remove an expert method loads `kw-expert-extension`.
- A material correction or observed consequence may load `kw-feedback-review`,
  which can produce only an inactive source-linked lesson candidate.
- Exact human Retain, Amend, Reject, Suspend, or Retire loads
  `kw-learning-governance`.
- A later initiative completes meaning without lesson content before
  `kw-learning-selection` can inspect the opaque learning index.

## Save and completion contract

After every material event, write semantic output first, update the open run
record second, and update the compact index last. A worker summary, transcript,
or index row cannot replace a missing output. Closed runs are immutable.

Continue until the user has a useful work product or decision-grade blocker and
a fresh capable actor can recover the corrected commission, live outputs,
material uncertainty, gates, and next legal action from durable files.
