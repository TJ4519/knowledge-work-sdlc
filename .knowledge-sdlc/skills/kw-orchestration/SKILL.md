---
name: kw-orchestration
description: "Carry one initiative run through a sufficient composition of skills, fresh specialists, tools, decisions, and durable artefacts."
primitive: skill
fresh_context: false
independence: main-agent-orchestrator
allowed_tools: ["Read", "Grep", "Shell", "Write", "Task"]
inputs: ["run-record", "meaning"]
optional_inputs: ["recipe", "expert-method-binding", "model-policy", "domain-charter", "source-policy", "protected-artifact-register"]
excluded_context: ["unretained-completion-summary", "unrelated-initiative-content", "unselected-reusable-lesson"]
outputs: ["updated-run-record", "professional-work-product", "decision-grade-blocker"]
authority: route-control-only-no-professional-authority
standalone: false
idempotency: "Resume the open run's next obligation; never create a parallel route because context changed."
phase: orchestration
---
# Orchestration

The main agent is the sole orchestrator. It composes, dispatches, retries,
replans, and owns every gate; the user remains commissioner and consequential
decision authority rather than stage operator.

## Run lifecycle

An open or halted run resumes in its existing record. A new accepted intent,
post-closure correction, or authorised follow-on pass mints a new run record
linked to its predecessor. Closed run records are immutable.

Before substantive work, the run must link an exact meaning revision and contain
a composed execution plan. Native receipt data is optional unless a specific
operation requires it.

## Composition

1. Read the current meaning and only the artefacts needed to compose this run.
2. Start from the nearest recipe. Name the causal obligations earned by this
   initiative: interpretation, evidence custody, candidate production,
   challenge, human authority, protected custody, correction propagation, and
   continuity.
3. Include each method needed for the strongest credible professional outcome.
   Remove a default only when its absence cannot materially change meaning,
   evidence coverage, candidate quality, independence, authority, custody,
   reconciliation, or recovery.
4. Write every inclusion and exclusion, its rationale, required inputs, expected
   output, human gate, verification, and first legal action to the run record
   before execution. If reality defeats a default, revise the plan visibly;
   never create a second control path.
5. Perform human-guided work inline through the relevant skill. Use a fresh
   specialist only when context weight, autonomy, tool isolation, or independent
   challenge makes it materially better.
6. Give each specialist a bounded packet of durable paths: exact purpose,
   required inputs and authority, excluded context, permitted tools, expected
   output, and stop condition. A worker cannot spawn another worker or route the
   run.

### Ambient supporting skills

A provider or user environment may expose additional skills whose triggers
match the commission. Treat them as optional supporting procedures unless an
exact expert-extension decision admits and binds them. They may improve inline
analysis, but they may not:

- replace the main orchestrator or change the accepted recipe;
- introduce a parallel claim, trace, validation, supervision, or learning
  taxonomy into durable initiative state;
- create another human gate merely because their internal workflow names one;
  or
- create a lesson candidate before a material correction or observed outcome.

Before accepting any durable output from an ambient skill, name its downstream
consumer and ask whether an existing artefact owner can carry the same semantic
substance. Prefer adding a section to the evidence map, work order, candidate,
challenge, or run record. If no distinct consumer remains after that mapping,
keep the supporting work inline and do not persist it.

The standing orchestration contract is the explicit instruction to dispatch an
earned bounded specialist; the commissioner need not request a subagent by
name. Ask only when dispatch requires new external authority, credentials,
material cost, or protected access. A missing Task facility or actual host
rejection is evidence of unavailability; lack of another user request is not.

Resolve a recipe `actor: skill` through the host's native skill discovery.
Resolve `actor: agent, method: <name>` to the canonical workspace definition at
`.knowledge-sdlc/agents/<name>.md`, or the generated native plugin definition
`agents/kw-<name>.md`. Read that exact declaration before dispatch and preserve
its inputs, outputs, tools, capabilities, excluded context, freshness,
independence, authority, no-spawn/no-route boundary, and output path in the
sealed packet. There is no hand-maintained runtime registry.

## Expert-method binding

An explicit request to import, curate, update, bind, retire, or remove a lead's
method loads `kw-expert-extension`. Eligibility or provider-native installation
does not select it. After present meaning is settled, a run may bind one exact
admitted immutable revision, allowed effect, precedence, conflicts, actor,
inputs/outputs, tools, and stop condition. Resolve an old run against the
revision it originally bound even when a newer revision exists.

## Model observation

Delegated work desires the exact concierge model. Pass that identity only when
the host exposes and accepts it. Otherwise omit the selector and record
`unobservable`; do not report omission as proven inheritance. Apply a different
model only from an exact user override. When child identity is observable,
record `inherited` or `different` and degrade/block any material independence
claim that the observed mismatch defeats.

## Runtime capability preflight

The orchestrator owns preflight after the plan identifies semantic operations.

### Composition-time reconnaissance

For each required capability, inspect whether a plausible facility is visible,
reachable, authenticated, apparently authorised for the needed read/write
scope, and able to reach the named assets. Visibility is evidence for planning,
not proof of execution.

### Operation-specific proof

Before consequential production, bind the exact facility to the actor that will
perform the work and use a harmless probe or deterministic guarantee to answer:

- can that actor read the exact source or native artefact;
- can it inspect the required structures, formulas, protection, or metadata;
- can it create and write a disposable candidate without touching the original;
- can it recalculate, render, query, export, or validate as the method requires;
- can it return source identifiers, parameters, as-of state, and structured
  results; and
- will the eventual producer receive the same tool and authority that were
  probed?

Record the semantic capability, observed tool/server and version when available,
actor, authentication and scope, probe, result, permitted operations, fallback,
and resulting claim limit in the work order and run record. Tool descriptions
and safety annotations are hints, not proof. There is no connector registry,
Python resolver, or preflight sub-orchestrator.

Do not create a separate capability-binding artefact merely to repeat this
section. A distinct file is justified only when a named producer cannot receive
the work order/run record and therefore has a separate durable consumer.

## Client templates and protected originals

For each supplied template, bind exact identity, hash, owner, revision, media
type, shape/method/policy role, precedence, editable scope, protected scope,
native features to preserve, candidate path, and structural, formula,
computational, visual, professional, and provenance checks. A method-bearing
template can change the analysis and may require a human meaning decision. Work
only in a candidate copy until exact promotion authority exists.

## Run loop and artefact bus

1. Execute the next included stage.
2. A specialist return is usable only when the named output exists, its sources
   and uncertainties are visible, and its hash or identity can be checked. Prose
   completion is not an artefact.
3. Triage failures and escalations before the next stage. Record a failed host
   operation even when a fallback succeeds.
4. Write or supersede the semantic output first. Then append its stage outcome,
   inputs, authority, verification, limitation, and next action to the run
   record. Update the compact index last.
5. Present only decisions the user owns: a material interpretation,
   consequential candidate, reusable lesson, or protected action. Never ask for
   internal commands.
6. A correction changes every explicit dependant. Preserve prior revisions,
   invalidate only observed dependency descendants, rederive affected outputs,
   and use a fresh challenger when the consequence earns independence.

## Independent challenge

A fresh producer-independent challenge is required when a candidate will inform
a consequential decision or protected action and depends on contested source
meaning, a material rival route, or an inference whose treatment could change
the recommendation. Give the challenger the candidate, retained evidence,
settled meaning, and no producer transcript.

Freeze the challenge packet and record its path/hash before dispatch. When the
host exposes task/session or event identity, retain it so review order and
separation are observable rather than self-attested. If the host cannot provide
fresh challenge, halt the run with that exact review as the next legal action.
An inline self-check cannot satisfy an earned independence obligation.
Adjudicate only a material retained contradiction.

When the main agent accepts a finding, record the finding and resulting change
in the run record and issue the one targeted candidate revision directly. Do
not create a separate adjudication artefact to restate agreement. Use the
adjudicator only when accepting or rejecting a challenge would materially
change the conclusion and a substantive contradiction still survives triage.
Likewise, when a challenge independently resolves or narrows a producer's
validation limitation without changing candidate bytes, the challenge plus run
record carry that resolution; do not create a second validation-resolution
artefact.

One producer-independent challenge round is the default obligation. The main
agent may issue one targeted candidate revision to address reproduced findings,
then returns that candidate with any residual limitation. Do not automatically
send the repaired candidate back to the same challenger, add an adjudicator as
a second generic reviewer, or continue until every fresh reader is silent.
Re-challenge requires new evidence, changed governing meaning, a protected
action, or a specifically recorded contradiction whose consequence justifies a
successor review run.

## Pre-production learning option gate

After current meaning is frozen without lesson content, and before the first
potentially lesson-affectable output:

1. verify the settled meaning path/hash and name one still-pending step in the
   open run record before its output exists;
2. only then inspect neutral rows in `ai_docs/LEARNINGS.md`; if the index does
   not exist, record no nomination and continue;
3. record “no nomination” and continue when no row is plausibly analogous;
4. if a row may match, record the neutral nomination, read only that one lesson
   for disclosure, and present its actual effect, prohibition and mismatch; and
5. obtain one exact Select, Narrow, or Decline decision. Immediately recheck
   that the named step remains unperformed, record any selected bounded effect
   in that ordinary decision and the run record, and pass it only to the named
   producer.

Meaning, index inspection, nomination, bounded lesson inspection, exact
selection, and use are sequential acts. If ordering is breached, record it and
make no causal learning claim for that run. Do not create a second inspection
gate or a separate activation-proof artefact.

## Feedback during work

Record a correction in its exact meaning, decision, and affected output
artefacts. When a material consequence may support reuse,
`kw-feedback-review` writes an inactive lesson candidate. Orchestration cannot
admit or activate it automatically. Outcome review follows only after a selected
lesson's named effect has produced observable evidence.

## Correction re-entry

A correction does not end at invalidation or reconciliation. After identifying
the exact affected descendants, re-enter the producer that owns each stale
candidate with the superseding meaning/evidence/work order. Produce one typed
successor candidate, run at most one newly earned independent challenge, and
return it for exact disposition when consequence requires. Reconciliation and
re-derivation may diagnose or reproduce effects; neither substitutes for the
producer authorised to create the successor.

## Evidence-backed delivery

At a consequential completion, partial/blocked return, or material revised
delivery, the main agent owes the reader a usable account of the work, not only
a file list. Ordinary progress messages do not require this full procedure.
On continuation, reconcile the current object and applicable evidence before
repeating a prior conclusion. This section owns that procedure; a supporting
briefing or visual skill may shape its presentation without replacing it.

Recover the professional job, audience and intended use from current meaning
and the actual result. Identify the exact candidate, information date, units
and actual/forecast boundary where relevant. Do not infer the job only from
sheet names, a plan or the producer's summary. Do not require a commissioner
to supply professional approval merely to receive an explanation.

Compare requested coverage with actual output for omissions, and consequential
changes with their source or methodological basis. Group the result into
material actions, not tool calls or prescribed stages; an unchanged assumption
can matter as much as a changed input. For consequential statements, inspect
the exact output location, source or assumption, transformation, affected
result and applicable check. Routine homogeneous mappings may share compact
support; per-cell paperwork is not required.

An instruction establishes what was required. A producer account records what
its author reports. An inspected candidate establishes content. An observed
operation or reproduction supports the behaviour actually tested under its
conditions. A hash identifies bytes, not truth; a reviewer name is not a check.
Reuse applicable recorded checks rather than rerunning the whole analysis.
Describe inspections performed for this delivery as new work, not old events.

Lead with the useful result and the conditions that matter to its intended
use. Before sending, inspect the opening paragraph alone: does it state the
substantive finding and its binding condition, rather than merely announcing
artifact availability, completion or a resolved defect? If not, rewrite the
opening. A reader should learn what the work establishes before following a
file link. Put a known consequential defect or unsupported use beside the affected
claim immediately. Otherwise prioritise the assumptions and disagreements
most capable of changing the conclusion, then specific checks and correction
history, including relevant ordinary successful paths. For a selected ordinary check,
state what was tested, what happened and where its evidence can be reached;
merely naming a checked path does not make its support understandable. Ranking is judgment
about consequence, uncertainty, sensitivity and checked scope, not a universal
score or a quota of actions, citations or findings. Keep fixed premises beside
changed premises. A checked consequence does not establish its premise.

Give the explanation directly in the user-facing response. Supporting links or
a read-only view should reach the exact source passage, artifact location and
recorded observation without a folder search. If native cell links are not
supported, provide the workbook, accurate sheet/cell address and a relevant
excerpt; do not invent a deep link. Supporting detail may be deferred, but not
a caveat that changes the headline. Explain who inspected, changed in scratch,
observed, reproduced, authorised, repaired and rechecked at the recorded scope.
The commissioner and professional reader may need different depth, not
conflicting accounts or another approval ceremony.

Distinguish explicitly unperformed work, work not independently checked, and
work for which no supporting record was found. Missing support narrows the
claim; it must not become a fabricated rationale. Separate calculation
behaviour, source interpretation, assumption plausibility and human acceptance.
Do not call the whole object verified from selected checks. Proposed next
investigations are not completed checks or automatically authorised work.

Bind the account to its current candidate and relevant source/method state.
After a revision, carry a check forward only where its target and dependencies
remain applicable; unchanged numbers do not prove unchanged meaning. Where
the affected extent is uncertain, say which claim needs review rather than
promising automatic invalidation. Label exported views as dated snapshots,
not live monitoring. Record the delivery and its evidence scope in the existing
run; do not create another ledger. Financial/professional work may be complete
while its delivery remains incomplete: return the supported work promptly with
the precise gap. Do not withhold useful work pending comparative superiority,
or use a polished explanation as evidence of that superiority.

## Completion

A run is complete only when no earned causal obligation remains open and its
record names the useful outputs, exact decisions, verification, limitations,
and next state. Otherwise mark it halted with one executable next action and its
missing authority or dependency. Update the index after closing or halting the
record.

Whether complete or halted, return the current useful work product or a direct
link in the user-facing response, state what it supports, and name the one
material limitation. Never finish a turn silently because durable files exist,
and never hide a useful candidate merely because an earned gate remains open.

Propose evidence-grounded monitoring thresholds and conclusion-change tests
when the commission asks what would change the answer. Their absence is an
analytical limitation, not a human-authority blocker. Ask the user to decide a
threshold only when the threshold will become standing policy, authorize a
protected or external action, or materially redefine the commissioned decision.

A produced draft alone does not close an earned challenge, authority, promotion,
reconciliation, or recovery obligation.

## Non-authority

Orchestration chooses and adapts methods. It cannot decide professional truth,
grant human authority, treat a lesson as evidence, or silently modify a
consequential native artefact.
