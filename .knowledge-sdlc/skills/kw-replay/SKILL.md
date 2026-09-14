---
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
Use ordinary intake to establish an evaluation initiative/run linked to the
source work, or resume that existing evaluation run. Do not replace an open
production plan with an experimental one or write evaluation results into a
closed source run. The evaluation's meaning and authority govern this attempt.

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

Hand the bounded packet and stage plan to `kw-orchestration`. Preserve each
configuration's own method and capabilities; do not impose the controller's
installed skills on every candidate. An ordinary comparator retains its normal
tools, notes, files, practitioner skills and permitted delegation, but receives
no treatment-only instructions. Equal opportunity need not produce equal agent
counts; observe all child work within each declared resource ceiling.

A bounded specialist replay keeps the normal no-spawn boundary. A whole-agent
comparison instead needs separate host-native lead sessions/workspaces with
their declared operating contracts and delegation policies intact. Each lead
owns its test undertaking; it is not a worker granted permission to evade a
no-spawn rule. If the host cannot run that configuration faithfully, report the
mismatch or propose a narrower diagnostic rather than relabel a worker-only test.
The evaluation's main agent stages inputs and collects outcomes; it does not
become another production supervisor inside each arm.

Experimental actors cannot edit live research or change live policy. Do not run
a producer in the comparison designer's context after the designer has read the
original answer. Reuse the applicable candidate-copy and exact model-override
routes without changing the declared experimental difference.

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
