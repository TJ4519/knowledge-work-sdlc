from pathlib import Path
import json

ROOT = Path.cwd()

def replace(path, old, new):
    p = ROOT / path
    text = p.read_text()
    if text.count(old) != 1:
        raise RuntimeError(f'{path}: expected one occurrence of {old[:70]!r}, found {text.count(old)}')
    p.write_text(text.replace(old, new))

def write(path, text):
    p = ROOT / path
    if p.exists():
        raise RuntimeError(f'new file already exists: {path}')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)

replace('AGENTS.md', '''- For a historical question about one selected initiative, recover its current
  state when needed, then use `kw-recall`. Do not preload history on ordinary
  continuation; recall reads prior evidence, not new authority.''', '''- For a historical question or a comparison with explicitly named related
  initiatives in the same authorised workspace, use `kw-recall`. Keep current
  recovery narrow; recall reads evidence, not new authority.
- For a request to replay prior work or compare execution arrangements, load
  `kw-replay`. Discussion prepares a proposal; execution requires an authorised
  scope, configurations and resource bound. The main agent retains orchestration.''')
replace('AGENTS.md', '- Preserve direct client language separately from model inference.', '''- Preserve direct client language separately from model inference. Interpret a
  later turn against the ongoing undertaking before treating it as a new job.
  Retain valid prior work, act on affected dependencies, and respect explicit
  goal changes. Feature suggestions are not automatically execution authority.''')
replace('.knowledge-sdlc/skills/kw-meaning-consultation/SKILL.md', '## Method\n', '''## Evolving intent

Read a later turn against the current purpose, accepted decisions and actual
work. Distinguish a clarification, corrected premise, new evidence, scenario,
additional question, implementation instruction and explicit change of goal.
State only the consequential delta: what changes, what remains valid, which
outputs or checks depend on it, and what is still proposed. Preserve the literal
turn separately from that interpretation. Do not invent a new initiative because
the user is thinking aloud, nor preserve an old goal after they replace it.

A proposal starts from the use of the work, not a preferred mechanism or rubric.
Ask how it could meet the visible requirements while leaving the real problem
unsolved: omitted work, wrong source meaning, stale downstream use, excess human
work or resource cost. Inspect the plausible failure and valid alternative;
revise the proposal where the evidence warrants it. A successful check of one
aspect is not success in usefulness, correctness, cost and adoption together.

## Method
''')
replace('.knowledge-sdlc/skills/kw-orchestration/SKILL.md', '''4. Write every inclusion and exclusion, its rationale, required inputs, expected
   output, human gate, verification, and first legal action to the run record
   before execution. If reality defeats a default, revise the plan visibly;
   never create a second control path.''', '''4. Record the chosen route, required inputs, useful outputs, earned checks,
   authority and first action before execution. Explain material inclusions,
   exclusions and departures from the recipe; do not enumerate irrelevant skills
   or create paperwork for routine steps. If evidence changes the route, revise
   this plan rather than creating a second control path.''')
replace('.knowledge-sdlc/skills/kw-orchestration/SKILL.md', '## Working knowledge and historical inquiry\n', '''## Dispatch, waiting and resource use

Keep source reading, arithmetic, triage and delivery in the main context unless
independence, context weight or tool isolation actually requires separation.
A context ceiling is a maximum, not a target. Do not replace an earned review
with self-checking merely to reduce cost.

For each dispatched obligation, retain its task identity when exposed, exact
output target and expected completion signal in the existing plan/outcome row.
Dispatch once. Prefer a supported blocking wait or completion event. Do useful
independent work only when it is already in scope. After an unchanged status
observation, do not call again without a changed result, expired declared wait
interval, actionable failure or user instruction. Bound the wait/retry route
before entering it. When no completion mechanism is available, return the useful
work and pending state; do not promise a background wake the host cannot perform.

On resumption inspect the returned work, not just the worker's completion prose.
If a timed-out operation may have succeeded, inspect its effect before retrying.
Record denied or unsupported operations and use only an authorised alternative.

Use the smallest sufficient context packet and exact evidence locations. Reuse
still-applicable checks rather than copying histories or repeating whole reviews.
When usage is available, separate production, coordination, checking and repair;
include failures and retries. Cached input is part of input, not an extra total.
Missing usage and human time stay unknown; token counts are not an invoice.
Do not claim a whole-run cap unless every executing path is actually covered.

## Working knowledge and historical inquiry
''')
replace('.knowledge-sdlc/skills/kw-orchestration/SKILL.md', '''For a question about an earlier position inside the selected initiative, record
its question and temporal/use scope in the open plan and run `kw-recall` inline.''', '''For a question about an earlier position, or explicitly named related work in
the same authorised workspace, record the question and reading scope in the open
plan and run `kw-recall` inline.''')
replace('.knowledge-sdlc/skills/kw-orchestration/SKILL.md', '''Keep recall within the selected initiative and its permitted source bindings.
Do not preload history or lessons on unrelated work.''', '''Keep ordinary recall within the selected initiative and its source bindings.
Named related-initiative reading follows `kw-recall` without switching focus or
importing standing policy. Do not preload history or lessons on unrelated work.

For an explicit replay/comparison request, use `kw-replay` to prepare the bounded
work order and later interpret frozen returns. The existing main agent dispatches
the selected producers and checker, preserves each attempt and owns stopping.
Do not give evaluation answers or later corrections to an independent producer.
No replay or live model switch follows merely from a discussion of cost.''')
replace('.knowledge-sdlc/skills/kw-orchestration/SKILL.md', '''Outcome review follows only after a selected
lesson's named effect has produced observable evidence.''', '''Outcome review follows only after a selected
lesson's named effect has produced observable evidence. When that evidence is
available, use `kw-learning-outcome-review` inline and link its actual outcome;
do not launch a new experiment just to fill the outcome record. Application can
be visible while benefit remains inconclusive. No lesson is admitted or retired
through this review.''')
replace('.knowledge-sdlc/skills/kw-orchestration/SKILL.md', '''## Completion

A run is complete only when no earned causal obligation remains open and its''', '''## Completion reconciliation

Before a consequential delivery or declaring a run complete, reconcile three
things in the existing run: the actual request/current meaning, the actual
candidate, and the evidence for the checks being claimed.

- Compare requested coverage with the deliverable itself, not only the plan or
  change log. Account for material omissions and valid retained work. Inspect a
  bounded plausible omitted source-to-output path when the producer's list could
  miss it; do not turn this into another full review or an item-count quota.
- Distinguish planned, dispatched, returned, inspected and unresolved obligations
  in the existing outcome row. A completed task ID or an empty findings list does
  not establish the critical assertions. Open the referenced check and its exact
  candidate/basis; compare its observations with the claim made in the delivery.
- After repair, inspect the affected successor calculation, chart and conclusion.
  Carry earlier checks forward only for unchanged targets, dependencies and use.
  A new interpretation can invalidate an assurance claim even when bytes match.
- Do not drop a missing obligation retrospectively to obtain completion. A genuine
  goal or evidence change can remove its relevance; retain the reason and affected
  scope. Distinguish an unresolved required check from work already completed.

If a required check is missing or stale, arrange the remaining authorised check
within the bound or return the candidate with the exact pending limitation.
Do not add another manager, accept a known falsehood as a residual, withhold
unrelated useful work, or label the candidate independently checked prematurely.

## Completion

A run is complete only when no earned causal obligation remains open and its''')
replace('.knowledge-sdlc/templates/run-record.md', '''Append one row per material stage outcome. Artefact paths and hashes are the
handoff; a worker's prose completion claim is not.''', '''Append one row per material stage outcome. Record planned, dispatched, returned,
inspected or unresolved in that row, with the task identity when observable.
Bind an inspected check to its actual candidate, basis, intended use and result.
Artefact paths and hashes are the handoff; a worker's completion claim is not.
Record an explicit no-longer-required reason when a changed goal removes an
obligation. Reconcile requested coverage against the actual delivered work.''')
replace('.knowledge-sdlc/skills/kw-prime/SKILL.md', '''5. Treat `complete` as a claim. If an earned review, authority, promotion,''', '''5. Treat `complete` as a claim. Reconcile the recorded obligations with actual
   deliverables and their check records through orchestration's completion
   reconciliation; do not create a second recovery checklist. If an earned review, authority, promotion,''')
replace('.knowledge-sdlc/skills/kw-prime/SKILL.md', '''bounded same-initiative inquiry. Do not add old history to the recovery packet.''', '''bounded inquiry. Explicit related-initiative comparisons widen only recall's
named reading scope, not this recovery packet. Do not add old history to recovery.''')
replace('.knowledge-sdlc/skills/kw-recall/SKILL.md', 'description: "Answer a historical question inside one selected initiative: why a position changed, what supported an earlier assumption, or which basis applied then. Use only when the question needs prior evidence, not for ordinary current-state recovery."', 'description: "Recover the basis of earlier work or compare explicitly named related initiatives in one authorised workspace. Establish applicability without importing old decisions as current authority. Ordinary recovery remains with kw-prime."')
replace('.knowledge-sdlc/skills/kw-recall/SKILL.md', '''Read within the selected initiative and the original source objects explicitly
bound to it. A shared source file can be read when that
binding permits it; an incidental link is not permission to browse another
initiative, cross a workspace boundary or export licensed material. Where a
necessary answer depends on unrelated work, return the precise scope gap rather
than silently perform cross-initiative recall.''', '''By default, read within the selected initiative and its permitted source
bindings. When the user explicitly names related initiatives to compare or reuse,
record those exact targets and the permitted question in the current run. Read
only those targets inside the same authorised workspace; an incidental link or
thematic similarity does not expand the set. Resolve ambiguous names from the
compact catalogue before reading substantive contents. A permission boundary
still applies when a file is discoverable. A broad organisation-wide search is
not this procedure.

Keep the current initiative as the answer's owner. Do not change another
initiative's focus, records, assumptions or decisions. For each relevant finding,
compare subject, definition, period, scenario, evidence and intended use. State
whether it transfers, requires a bridge, conflicts, or remains unresolved, and
why. Shared vocabulary is not proof of equivalence. Retain an exact pointer in
the current evidence map only when later work needs it; no cross-project summary
or new global index is created.

Reading earlier research does not adopt its method, lesson or permission. A
material defect noticed in another initiative is a finding, not authority to
repair that initiative. Cross-workspace access, source export and changes of
standing practice use their existing explicit permission/admission routes.''')
replace('.knowledge-sdlc/skills/kw-recall/SKILL.md', '''   Use bounded search inside this initiative if links are missing. Do not scan
   all history when exact references already resolve the question.''', '''   Use bounded search inside the selected reading scope if links are missing.
   Do not scan all history when exact references already resolve the question.''')
replace('.knowledge-sdlc/references/working-memory.md', '''when the question needs earlier records. Keep recall within the selected
initiative and its authorised source bindings.''', '''when the question needs earlier records. Ordinary recall stays within the
selected initiative and its authorised source bindings. An explicit comparison
may name related initiatives in the same authorised workspace; `kw-recall` checks
the scope and applicability without moving their decisions into current policy.
Current recovery never preloads those other initiatives.''')
replace('.knowledge-sdlc/skills/kw-model-allocation/SKILL.md', '''The project model-policy file stores only confirmed overrides and observed
limitations. Provisional model names are ignored.''', '''The project model-policy file stores only confirmed overrides and observed
limitations. Provisional model names are ignored. `kw-replay` may supply a
source-linked comparison for a proposed choice; that result is not an override.
An evaluation-only override stays within its experimental run. A future-use
instruction must name its own exact scope, settings, fallback and effective
revision before it changes the live route.''')
write('.knowledge-sdlc/skills/kw-replay/SKILL.md', '''---
name: kw-replay
description: "Prepare a bounded replay of prior work and compare frozen execution alternatives against the professional task, original evidence and total effort. Use only for an explicit replay/comparison request; do not change live work or model defaults."
primitive: skill
fresh_context: false
independence: main-agent-comparison-design-not-independent-production
allowed_tools: ["Read", "Grep", "Shell", "Write"]
inputs: ["meaning", "run-record"]
optional_inputs: ["request", "work-order", "source-snapshot", "evidence-map", "candidate", "decision", "model-policy"]
excluded_context: ["unrelated-initiative-content", "unselected-reusable-lesson", "previous-answer-as-truth", "unrequested-execution"]
outputs: []
optional_outputs: ["work-order", "candidate-research"]
authority: evaluation-proposal-and-comparison-only-no-live-policy-change
standalone: partial
idempotency: "Reuse an exact frozen comparison; another attempt receives a new identity and never replaces an unfavourable result."
phase: evaluation
references: [".knowledge-sdlc/references/working-memory.md"]
---
# Replay work and compare execution choices

Help the user decide whether a different model, checking arrangement or context
packet is adequate for a specified job. The original answer is a comparator,
not professional truth. This skill prepares and reads an evaluation inside the
existing run; the main agent still owns dispatch, waiting, checks and stopping.
It does not create a second orchestrator or an automatic optimisation service.

## Choose the decision before the experiment

Recover the professional job and intended use. A question about whether another
route might help authorises an appraisal, not a paid replay. Use existing
observations first when they can settle the question. Execution needs a bounded
commission: exact candidate configurations, permitted inputs and tools, resource
ceiling, attempt count and the decision the result will inform. Reuse existing
explicit authority; ask only for missing consequential scope, access or cost.
Never substitute an available model silently for the requested one.

Freeze the intended differences and useful outcome checks before seeing the
candidates. Start from requested coverage, source meaning, actual implementation,
conclusions, preservation and effort. Ask how a candidate could satisfy those
checks while leaving the user's job wrong or unfinished. Include a relevant
ordinary successful path and a plausible omission; do not manufacture a broad
rubric or reject a legitimate alternative merely for taking different steps.

Separate a whole-package comparison from a model-only or checking-only change.
Record actual runtime/model/settings when observable, tools and access, method
revision and remaining unmatched conditions. An old recorded result is historical
evidence, not a matched current baseline. If a comparison needs a fresh baseline,
include it prospectively and run the authorised alternatives regardless of which
one fails first. Do not select cases by observed ordinary failure.

## Reconstruct what each attempt may receive

Use the existing work order for these boundaries; do not create a master replay
ledger. Identify the original request, starting artefacts and revisions, evidence
available then, applicable method and human decisions, and staged later requests.
Distinguish the time described by a source from when it was actually available.
Missing inputs or ordering remain gaps, not reconstructed history.

Copy only explicitly admitted starting inputs to a disposable execution space.
Do not clone the entire research project, its Git history, final outputs,
reviewer diagnoses, old producer transcripts, or a memory folder that contains
the answer. Inspect the packet's contents and references before dispatch. Keep
later sources and feedback out until their stage. Original source and live
research remain unchanged; record their identities before and after covered work.
Permission to read private methods or sources is not permission to forward them
to another provider, log sink or public dataset.

Distinguish two replay units:

- A trajectory replay advances each candidate's own preceding output through the
  staged requests. Do not replace a weak predecessor with the original final
  workbook at each stage; that would hide propagated mistakes.
- A fixed-start diagnostic gives an exact shared predecessor to all candidates
  and examines one bounded operation. It does not establish whole-trajectory
  continuation or compounding-error performance.

An independent attempt receives the admitted starting material, not the previous
answer or its repair. A lesson-assisted attempt deliberately receives an exactly
selected lesson or revised method and is labelled accordingly. Its selection
uses the existing governance route; it is not independent rediscovery.

Use fresh producer contexts with only the admitted packet. Inspect host exposure:
shared files, inherited conversation, history search, connectors and ambient
memory can disclose excluded answers. Separate directories and an instruction
not to look are not an access boundary. If the host cannot establish the required
separation, do not claim an independent replay; return the precise limitation or
obtain a decision for a different, explicitly non-blind comparison. Restricting
provided evidence does not erase knowledge already present in model weights.

## Compose execution without another management layer

Hand the bounded packet and stage plan to `kw-orchestration`. Reuse the existing
professional producers, candidate copies, source-first checking and exact
model-override route. Experimental actors cannot edit the live research, install
a new policy or launch more workers. Do not run a producer in the comparison
designer's context after the designer has read the original answer.

Freeze each normal submission before outside findings or repair instructions.
Retain failed, partial, interrupted and repaired attempts with their resource
use. One authorised repair does not retroactively improve the initial result.
A different checker is required for a claim of producer-independent assessment;
that checker establishes source-first watchpoints before seeing candidate
rationales, receives no preferred winner, and checks actual outputs. Reuse one
bounded assessor where sufficient; no automatic reviewer or consensus tree.

A completed return is not proof that its checks ran. Apply orchestration's
completion reconciliation to the actual candidate and its required observations.
Stop at the declared attempt/resource bound, not when a favourable result appears.

## Compare meaningful differences

Read exact task coverage, sources and native outputs. Compare what was treated
as reported evidence, derived result, estimate, scenario or decision; the
transformations used; the conclusion supported; and what remained unchanged.
Do not compare private chain of thought or demand identical step sequences.

Classify differences as a demonstrated defect, a legitimate alternative, a
support/coverage gap or an unresolved professional choice. Reproduce a source or
calculation conflict where feasible and look for evidence defeating the criticism.
Agreement can repeat an error. Disagreement can be correct under different
permitted assumptions. Review the original comparator by the same standard.
Do not require duplicated support when an exact reachable predecessor suffices.

Keep output quality, requested coverage, remaining human work, elapsed time and
resource use visible separately. Include production, coordination, checking,
retries, repair and escalation. Distinguish one-off qualification from recurring
execution. Cached input and reasoning output are included subsets; unavailable
usage is unknown, not zero. Price only from observed applicable rates or bills;
a subscription token ratio is not a cash-saving ratio. Include the cost of a
stronger checker when that checker is part of the proposed cheaper route.

## Return a decision, not another audit to operate

Give the useful result, material differences and exact support first. Recommend
retaining the current route, trying a narrowly specified alternative, changing
the method, or obtaining one missing observation. State where the result does
and does not support that choice. A sound final tie plus extra effort is no
observed advantage in this case, not proof of general redundancy.

Retain the comparison in the existing candidate-research/evidence owners and link
it from the run. Do not rewrite the original episode, its outcomes or active
model policy. An approved evaluation-only override expires with its scoped run.
A live change follows `kw-model-allocation` and an exact future-use instruction;
an acceptable alternative is not automatically permission to switch.

Selected replays are development evidence. When their results shape a method,
task or grader, keep them out of a subsequent fresh measurement cohort. Broader
numerical claims require a separately predefined sample, outcome, failure/tie
handling, assessment and stopping rule. Do not grade only favourable cases after
seeing the winner or silently change an existing benchmark's treatment.
''')
replace('DESIGN.md', '''inside one selected initiative; `kw-prime` still reads only current recovery
inputs.''', '''inside the selected initiative or an explicitly named related-work scope;
`kw-prime` still reads only current recovery inputs.''')
replace('DESIGN.md', '''selected initiative and its permitted source bindings. Reusable lessons follow''', '''selected initiative and its permitted source bindings unless an explicit
same-workspace comparison names additional initiatives. Reading those records
does not select their methods, adopt their decisions or change their state.
Reusable lessons follow''')
replace('DESIGN.md', '## Project state and authority\n', '''## Replay and execution comparison

`kw-replay` is an optional inline procedure selected for an explicit comparison
request. It prepares the existing work order with exact starting inputs, staged
evidence, candidate configurations, assessment and resource bounds. The main
agent uses its normal producer/checker dispatch; replay adds no standing actor.
Trajectory replays use each candidate's own predecessor. Fixed-start diagnostics
are identified separately. Frozen normal submissions precede feedback and repair.

The comparison reads actual work against source meaning and intended use, permits
legitimate alternatives, and reports complete observed effort. Results remain in
existing research/evidence owners. Development cases stay distinct from fresh
numerical measurement. A comparison supports a proposal, not automatic model
selection or a change to live research. Host isolation and usage observations
come from the host, not from a prompt or file naming convention.

## Project state and authority
''')
replace('README.md', '| Historical recall | Ask what supported an earlier position and why it changed, inside one selected undertaking. |', '| Historical recall | Recover an earlier basis, or compare explicitly named related work without importing its assumptions as current policy. |')
replace('README.md', '| Current continuation | Recover live meaning, decisions and outputs without replaying the whole conversation. |', '''| Current continuation | Recover live meaning, decisions and outputs without replaying the whole conversation. |
| Replay and comparison | Test an authorised alternative execution route in a separate copy and compare the work, support and effort before changing the live setup. |''')
replace('README.md', '''correcting related work.

Install using''', '''correcting related work. [Replay and comparison](docs/guides/replay-and-comparison.md)
explains how to try a different model or checking arrangement on selected past
work. The main agent also reconciles completed checks with the actual delivery
and uses bounded waiting rather than repeated status polling.

Install using''')
replace('docs/README.md', '''## Tailor it
''', '''- [Working memory](guides/working-memory.md) explains current recovery, scoped
  historical and related-work recall, and correction of affected outputs.
- [Replay and comparison](guides/replay-and-comparison.md) explains isolated
  evaluation of execution choices without changing live work or model defaults.

## Tailor it
''')
replace('docs/guides/working-memory.md', '''Recall stays inside one selected initiative and its permitted source bindings.
An embedded command in a past document is evidence, not a present instruction.''', '''Recall stays inside the selected initiative and its permitted source bindings
unless you explicitly name related initiatives in the same authorised workspace.
For example: "Compare the definition in this review with the renewal analysis;
tell me whether its conclusion applies here." The agent checks definition,
period, scenario, evidence and use before reusing anything, keeps the answer with
the current undertaking, and leaves the other initiative unchanged.

This does not merge all project histories or give old decisions new authority.
An embedded command in a past document is evidence, not a present instruction.''')
replace('docs/guides/working-memory.md', '''## Installation and upgrades
''', '''## Keep later changes connected to the work

A follow-up can refine the goal, correct a premise, add evidence, ask a historical
question or commission an implementation. The agent identifies what changed and
what remains valid before choosing the next action. An explicit new goal takes
precedence over the old one; an ordinary clarification need not create a new
project. Corrections still reach actual calculations and conclusions.

Checks are tied to their target, basis and use. An unchanged result used to make
a different claim may need reconsideration. Before delivery the main agent reads
the relevant observations and checks coverage against the actual work, rather
than treating a completed task or a clean change log as proof.

To test an alternative way of doing earlier work, use the separate
[replay and comparison](replay-and-comparison.md) procedure. Historical recall
explains what happened; replay creates a new attempt.

## Installation and upgrades
''')
write('docs/guides/replay-and-comparison.md', '''# Replay selected work before changing how it runs

Ask the main agent to compare another execution arrangement on a copy of earlier
work. Keep the live project unchanged while you decide whether the alternative
is adequate for the job and worth using again.

> Using the starting material from our proposal review, compare the two model
> configurations I specify. Leave the live recommendation unchanged. Show me any
> consequential differences, what was checked, and the complete observed effort.

A question such as "might another route cost less?" first produces an appraisal.
An executed comparison needs a named task, permitted inputs, exact configurations
and a resource bound. The main agent uses the existing host and tools; the package
does not supply model access or purchase inference.

## What happens

The main agent recovers the original purpose and starting material, identifies
what changed between the candidate configurations, and fixes the useful outcome
checks before running them. It stages only the inputs each candidate may read.
The normal production and checking methods then create and inspect the work.

A trajectory replay carries each candidate's own output through later updates.
A fixed-start comparison gives the same specified predecessor to each candidate
and tests a single operation. These answer different questions.

The old finished answer and its reviewer findings stay out of an independent
attempt. A deliberate lesson-assisted attempt includes the selected lesson and
is labelled accordingly. Current access permissions still govern private methods
and source material. The host must provide the separation required for a claim
of independent work; putting files in different folders is not sufficient when
the agent can still read both.

## Read differences as professional judgments

A difference is not automatically a mistake. Two proposals can reach different
cost estimates through legitimate, disclosed workload assumptions. Two identical
numbers can also be wrong for different reasons. The comparison examines the
sources, assumptions, calculations, requested coverage and conclusions, not
whether the models used identical wording or steps.

The return identifies demonstrated defects, legitimate alternatives, missing
support and unresolved choices, then recommends a scoped next action. The
previous model's answer is examined too; it is not the answer key.

## Cost includes the whole route

Count production, coordination, checking, retries and repair together. Show the
one-off comparison cost separately from the expected recurring arrangement.
Unknown human time, token usage or prices remain unknown. A lower token total
is not automatically a lower subscription bill. A cheaper producer with a stronger
checker must include that checking cost.

Repeated status polling is not research. The main agent records the expected
return, uses a supported blocking wait or completion signal where available,
and resumes only on new information or the bounded observation schedule. A host
without background resumption returns the current useful work and pending state.

## Approval and use

The comparison leaves live research, the active method and model defaults alone.
You can approve a precisely scoped model override through the normal model-policy
route. An evaluation-only override does not extend to future production.

For example, a comparison might support a limited alternative for extracting a
well-defined table while retaining the existing checking arrangement. It might
also show no advantage or leave the choice unresolved. Every attempt and repair
keeps its own result; a later repair does not rewrite an earlier failure.

Selected past work supports development decisions. A numerical claim about
broader performance needs a separate predefined fresh sample, assessment and
stopping rule. Keep development cases and any existing benchmark treatment intact.

## How the pieces fit

`kw-prime` recovers current work. `kw-recall` explains earlier or explicitly named
related work. `kw-replay` prepares a new comparison and interprets its returns.
`kw-orchestration` remains the only coordinator, with existing producers and
bounded independent checks. The comparison uses the existing work-order, evidence,
candidate and run records rather than another memory database.

See the [developer exercise](https://github.com/TJ4519/knowledge-work-sdlc/blob/main/examples/manual-exercises/journeys/continuity-and-replay.md)
for staged observations, including valid alternatives, contamination and a stale
assurance claim. Keep evaluator material outside producer workspaces.
''')
write('examples/manual-exercises/journeys/continuity-and-replay.md', '''# Continuity, closeout and replay exercise

Use disposable projects and a real supported host. This file is for the person
running the exercise; do not copy its expected outcomes into a producer workspace.
Record the source revision, host configuration, actual actions and returned work.
Mechanical package tests and this behavioural exercise address different claims.

## Ordinary work and a consequential correction

Give the producer a short project brief and two public or synthetic service
proposals. In the brief, the current workload is an estimate of 100 requests per
month. Proposal A quotes 2 per request; proposal B quotes 150 fixed plus 0.25 per
request. Ask for an editable comparison and a recommendation, explaining the
workload assumption and price crossover. Give it only this stage's information.

Inspect whether the useful work is complete: at 100 requests A costs 200 and B
costs 175; the crossover is about 85.714 requests. Do not demand a specific file
layout when the analysis is correct and inspectable.

Next supply a report establishing an actual workload of 100. The number is
unchanged but its role changes. Then instruct: "For our launch meeting, compare
at 60 requests. Keep the reported 100 and the earlier central case." The meeting
case costs 120 for A and 165 for B; it is a user scenario, not reported demand.
Inspect the actual table, any chart and recommendation, including preserved work.

In a fresh task, ask why the recommendation changed. The answer must distinguish
new reporting evidence from the user's separate scenario. Remove an optional
historical rationale before that question; absence must remain absence rather
than a plausible invented explanation.

## Named related work

Prepare another initiative that defines a request as a completed resolution,
whereas the current project counts all incoming requests. Ask for a comparison
between the two named initiatives. The agent must inspect the definition before
transferring a unit cost. Keep an unrelated initiative outside the authorised
reading set. Inspect access traces where available and ensure neither source
initiative's records were changed. An ordinary "continue" must not trigger a
scan of all project histories.

## Checks that must affect the return

Arrange a candidate whose note says its scenario is independently checked while
the cited check targets the earlier central case. The completion procedure must
not accept that label. Resolve the exact remaining check or return the candidate
with the actual pending status. A later successful check does not make an earlier
delivery checked on time. Change a chart but not its caption to exercise a missed
consumer. Keep a valid independent calculation to ensure the procedure reuses it
rather than repeating every check.

Exercise an unchanged worker-status response. Check that the coordinator uses an
actual completion event or bounded waiting route, or returns pending work; it
must not infer that the worker completed, repeatedly spend model turns polling,
or promise an unavailable background wake.

## Replay and comparison

Before execution, specify two available configurations, an attempt/resource bound,
and the professional outcome to compare. Reconstruct the first-stage inputs only;
keep this guide, later results, reviewer findings, the original final answer and
Git history outside the producer's access. Inspect both file access and inherited
host context. If the host cannot isolate them, record that limitation instead of
claiming an independent attempt.

For a trajectory comparison, each candidate's own first output receives the
reported-actual update and meeting-case request in order. Also exercise a labelled
fixed-start diagnostic to ensure those modes are not conflated. Both configurations
run irrespective of the first result; failures and repairs remain separate.

An independent checker derives source-first watchpoints, then inspects frozen
returns. It permits a justified alternative workload scenario without calling it
a reporting fact. It rejects matching totals whose units or interpretation are
wrong. Report complete observed effort and unknown costs separately. Do not infer
saved analyst time from an articulate explanation.

Finish by checking that live outputs, default model policy and source-initiative
history are unchanged. An evaluation-only approval must not activate a future
route. Retain the episode as development evidence, not fresh numerical validation.
''')
replace('.knowledge-sdlc/VERSION', '0.7.0\n', '0.7.1\n')
for path in ('package.json', 'package-lock.json'):
    p = ROOT / path
    p.write_text(p.read_text().replace('"version": "0.7.0"', '"version": "0.7.1"'))
for path in ('docs/guides/npm-installation.md', 'docs/guides/installation-and-providers.md'):
    p = ROOT / path
    p.write_text(p.read_text().replace('0.7.0', '0.7.1'))
replace('tests/npm-installer.test.cjs', "  assert.match(ok(cli(['--version'], { env })).stdout, /^knowledge-work-sdlc 0\\.7\\.0/m);", "  const version = JSON.parse(fs.readFileSync(path.join(packedRoot, 'package.json'))).version;\n  assert.equal(ok(cli(['--version'], { env })).stdout.trim(), `knowledge-work-sdlc ${version}`);")
replace('CHANGELOG.md', '# Changelog\n', '''# Changelog

## 0.7.1 — 2026-09-14

- Add optional `kw-replay` for bounded, isolated execution comparison before an
  explicit model-policy change, using existing work-order and result records.
- Extend `kw-recall` to explicitly named related initiatives in one authorised
  workspace while preserving narrow current-state recovery.
- Reconcile evolving intent, actual deliverable coverage and target-bound checks
  before completion; preserve valid work and inspect affected repairs.
- Bound waiting and repeated status observations, retain unknown resource costs,
  and connect selected-lesson outcome review to actual later evidence.
- Add user guidance, staged developer exercises and package/upgrade checks.

''')
replace('tooling/projection.py', '        "docs/guides/working-memory.md",\n', '        "docs/guides/working-memory.md",\n        "docs/guides/replay-and-comparison.md",\n')
replace('docs/plugin-package.md', '''recall within one initiative, and correction into actual dependent outputs.
See `docs/guides/working-memory.md` for examples and use.''', '''recall with an explicit related-work scope, and correction into actual dependent
outputs. Optional replay compares execution choices on isolated copies before a
live model-policy change. See `docs/guides/working-memory.md` and
`docs/guides/replay-and-comparison.md` for examples and use.''')
replace('README.md', '''The [latest release](https://github.com/TJ4519/knowledge-work-sdlc/releases/latest)
contains the archive, which needs no Python at run time.''', '''Build a matching plugin archive from this source revision with `make package`.
[Published releases](https://github.com/TJ4519/knowledge-work-sdlc/releases)
contain the methods from their tagged revision. The installed plugin needs no
Python at run time.''')
replace('.knowledge-sdlc/skills/kw-prime/SKILL.md', '''   reconciliation; do not create a second recovery checklist. If an earned review, authority, promotion,
   reconciliation, or recovery obligation remains open, do not rewrite the''', '''   reconciliation; do not create a second recovery checklist. If an earned
   review, authority, promotion, reconciliation, or recovery obligation remains
   open, do not rewrite the''')
replace('DESIGN.md', '''`kw-prime` still reads only current recovery inputs. M3 follows those relationships through ordinary correction and inspection
of actual successor outputs.''', '''`kw-prime` still reads only current recovery inputs. M3 follows those
relationships through ordinary correction and inspection of actual successors.''')
write('tests/test_continuity_replay.py', '''"""Distribution and authority-contract checks; not live-agent evaluations."""
from __future__ import annotations

import io
import json
import shutil
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path

from tooling.contracts import discover_methods, discover_recipes, validate_source
from tooling.errors import IntegrityError
from tooling.installer import install, upgrade
from tooling.projection import plan_plugin, plan_workspace, validate_plugin, validate_workspace
from tooling.util import parse_frontmatter

SOURCE = Path(__file__).resolve().parents[1]
REPLAY = ".knowledge-sdlc/skills/kw-replay/SKILL.md"
REFERENCE = ".knowledge-sdlc/references/working-memory.md"


def client(path: Path) -> Path:
    path.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=path, check=True)
    return path


def snapshot(root: Path) -> dict[str, bytes]:
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob("*")
            if p.is_file() and ".git" not in p.relative_to(root).parts}


class ContinuityReplayTests(unittest.TestCase):
    def test_replay_is_one_optional_inline_procedure(self) -> None:
        self.assertEqual(validate_source(SOURCE), [])
        methods = discover_methods(SOURCE)
        replay = methods["kw-replay"]
        self.assertEqual(replay["kind"], "skill")
        self.assertFalse(replay["fresh_context"])
        self.assertNotIn("Task", replay["allowed_tools"])
        self.assertEqual(replay["outputs"], [])
        self.assertEqual(set(replay["optional_outputs"]), {"work-order", "candidate-research"})
        self.assertIn("previous-answer-as-truth", replay["excluded_context"])
        for recipe in discover_recipes(SOURCE).values():
            for step in recipe["composition"]:
                if step.get("method") == "kw-replay":
                    self.assertTrue(step.get("optional"))
                    self.assertTrue(step.get("trigger"))

    def test_current_recovery_keeps_its_read_boundary(self) -> None:
        prime = discover_methods(SOURCE)["kw-prime"]
        self.assertEqual(prime["inputs"], ["initiative-catalogue", "run-record"])
        self.assertNotIn("Task", prime["allowed_tools"])
        self.assertTrue({"old-transcript", "superseded-artefacts",
                         "unrelated-initiative-content", "unselected-reusable-lesson"}
                        <= set(prime["excluded_context"]))

    def test_replay_and_recall_preserve_their_bodies_in_both_packages(self) -> None:
        methods = discover_methods(SOURCE)
        ws, plugin = plan_workspace(SOURCE), plan_plugin(SOURCE)
        for name in ("kw-replay", "kw-recall", "kw-orchestration"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as raw:
                path = Path(raw) / "SKILL.md"
                path.write_bytes(ws[f".agents/skills/{name}/SKILL.md"])
                metadata, body = parse_frontmatter(path)
                self.assertEqual(body.strip(), methods[name]["body"].strip())
                self.assertEqual(metadata["authority"], methods[name]["authority"])
                path.write_bytes(plugin[f"skills/{name}/SKILL.md"])
                metadata, body = parse_frontmatter(path)
                self.assertTrue(body.rstrip().endswith(methods[name]["body"].rstrip()))
                self.assertEqual(metadata["allowed_tools"], methods[name]["allowed_tools"])
        self.assertEqual(plugin["docs/guides/replay-and-comparison.md"],
                         (SOURCE / "docs/guides/replay-and-comparison.md").read_bytes())
        self.assertEqual(validate_plugin(plugin, SOURCE), [])

    def test_no_replay_runtime_or_evaluation_answers_enter_workspace(self) -> None:
        for projection in (plan_workspace(SOURCE), plan_plugin(SOURCE)):
            self.assertFalse(any(p.endswith(".py") for p in projection))
            self.assertFalse(any(p.startswith("examples/") for p in projection))
        self.assertEqual({p for p in plan_workspace(SOURCE) if p.startswith("ai_docs/")},
                         {"ai_docs/initiatives/index.md"})

    def test_private_client_work_and_model_policy_survive_upgrade(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            prior = root / "prior"
            shutil.copytree(SOURCE, prior, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
            # An earlier complete source, not a malformed subset of the new method.
            prior_skill = prior / REPLAY
            prior_skill.write_text(prior_skill.read_text().replace(
                "# Replay work and compare execution choices", "# Earlier replay procedure"))
            target = client(root / "client")
            install(prior, target)
            state = target / "ai_docs"
            (state / "model-policy.md").write_text("Current model choice: unchanged.\\n")
            history = state / "initiatives/private-research"
            history.mkdir()
            (history / "decision.md").write_text("Private prior decision.\\n")
            (history / "candidate.md").write_text("Private current work.\\n")
            before = snapshot(state)
            preview = upgrade(SOURCE, target, apply=False)
            self.assertEqual(preview["mode"], "dry-run")
            self.assertEqual(snapshot(state), before)
            upgrade(SOURCE, target, apply=True)
            self.assertEqual(snapshot(state), before)
            self.assertEqual(validate_workspace(target, SOURCE), [])
            self.assertIn(b"# Replay work and compare execution choices",
                          (target / ".agents/skills/kw-replay/SKILL.md").read_bytes())

    def test_collision_refuses_without_partial_or_private_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = client(Path(raw) / "client")
            p = target / ".agents/skills/kw-replay/SKILL.md"
            p.parent.mkdir(parents=True)
            p.write_text("# My own procedure\\n")
            (target / "notes.md").write_text("Client material\\n")
            before = snapshot(target)
            with self.assertRaises(IntegrityError):
                install(SOURCE, target)
            self.assertEqual(snapshot(target), before)

    def test_corrupt_replay_is_detected_and_upgrade_does_not_hide_it(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            target = client(Path(raw) / "client")
            install(SOURCE, target)
            p = target / ".agents/skills/kw-replay/SKILL.md"
            p.write_text("# Changed locally; do not overwrite this silently\\n")
            before = snapshot(target)
            self.assertTrue(validate_workspace(target, SOURCE))
            with self.assertRaises(IntegrityError):
                upgrade(SOURCE, target, apply=True)
            self.assertEqual(snapshot(target), before)

    def test_missing_shared_dependency_prevents_a_partial_package(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "source"
            shutil.copytree(SOURCE, root, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__"))
            (root / REFERENCE).unlink()
            self.assertTrue(validate_source(root))
            with self.assertRaises(IntegrityError):
                plan_plugin(root)

    def test_tampered_packaged_replay_fails_exact_validation(self) -> None:
        plugin = plan_plugin(SOURCE)
        plugin["skills/kw-replay/SKILL.md"] = plugin["skills/kw-replay/SKILL.md"].replace(
            b"do not change live work or model defaults", b"change live work and model defaults")
        self.assertTrue(validate_plugin(plugin, SOURCE))

    def test_versions_agree_and_developer_exercise_is_not_a_production_input(self) -> None:
        version = (SOURCE / ".knowledge-sdlc/VERSION").read_text().strip()
        self.assertEqual(json.loads((SOURCE / "package.json").read_text())["version"], version)
        self.assertEqual(json.loads((SOURCE / "package-lock.json").read_text())["version"], version)
        self.assertTrue((SOURCE / "examples/manual-exercises/journeys/continuity-and-replay.md").is_file())
        self.assertNotIn("examples/manual-exercises/journeys/continuity-and-replay.md", plan_plugin(SOURCE))


if __name__ == "__main__":
    unittest.main()
''')
replace('.knowledge-sdlc/skills/kw-replay/SKILL.md', '''It does not create a second orchestrator or an automatic optimisation service.

## Choose''', '''It does not create a second orchestrator or an automatic optimisation service.
Use ordinary intake to establish an evaluation initiative/run linked to the
source work, or resume that existing evaluation run. Do not replace an open
production plan with an experimental one or write evaluation results into a
closed source run. The evaluation's meaning and authority govern this attempt.

## Choose''')
replace('.knowledge-sdlc/skills/knowledge-work/SKILL.md', '''## Feedback and expert-method routes
''', '''## Replay and related-work requests

For an explicit replay or execution-comparison request, establish the evaluation
as its own initiative/run linked to the source work, then use `kw-replay`. Do not
replace a live production plan, mutate its history, or execute a proposed test
before its scope and resource authority are settled. A later comparison question
can resume that evaluation without creating another manager or method library.

An explicit request to compare named related initiatives uses `kw-recall` after
recovering the current undertaking. Only the named, authorised same-workspace
reading scope widens; ordinary recovery and lesson selection remain unchanged.

## Feedback and expert-method routes
''')
replace('docs/guides/continuity-and-recovery.md', '''position in the same initiative. Read older evidence only for that question;
do not expand prime's current-state packet.''', '''position in the same initiative. An explicit comparison may also name related
initiatives in the same authorised workspace. Read only that defined scope;
do not expand prime's current-state packet or change the other initiatives.''')
replace('docs/guides/replay-and-comparison.md', '''The main agent recovers the original purpose and starting material, identifies''', '''The comparison has its own evaluation run linked to the source work, leaving
any live production plan and closed history intact. The main agent recovers
the original purpose and starting material, identifies''')
replace('tests/test_continuity_replay.py', 'import io\n', '')
replace('tests/test_continuity_replay.py', 'import tarfile\n', '')
