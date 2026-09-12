---
name: kw-reconciliation-control
description: "Map dependency-valid invalidation after a confirmed correction or protected promotion so orchestration can re-enter the owning stages."
primitive: skill
fresh_context: false
independence: main-agent-control
allowed_tools: ["Read", "Grep", "Shell", "Write"]
inputs: ["meaning", "decision"]
optional_inputs: ["change-record", "promotion", "invalidation", "candidate", "work-order", "evidence-map"]
excluded_context: ["chronology-as-dependency", "old-producer-transcript", "unrelated-initiative-content"]
outputs: ["invalidation"]
optional_outputs: []
authority: control-only-human-approved-artefacts-require-proposal
standalone: partial
idempotency: "One control run is tied to an exact changed revision and dependency graph head."
phase: correction
references: [".knowledge-sdlc/references/working-memory.md"]
---
# Reconciliation control

A correction is not complete when one artefact changes. This skill owns only
the invalidation map. The run's recipe and main orchestrator own subsequent
producer re-entry, reconciliation, challenge, re-derivation, and gates.

## Method

1. Identify the exact changed, accepted, or promoted revision.
2. Build the explicit dependency graph from artefact input revisions, source-to-
   claim links, method-to-output links, and observed native formulas, references,
   or connections. Host graph facilities may accelerate this read but are not a
   prerequisite. Do not infer dependency from chronology, directory proximity,
   or thematic similarity.
3. Traverse those recorded edges and invalidate only dependants whose inputs
   include the changed revision or an invalidated descendant.
4. Distinguish ownership:
   - regenerable agent artefacts may be superseded through their producing stage;
   - human-approved meanings, work orders, and decisions receive proposed superseding revisions and new human gates;
   - protected native artefacts change only through promotion;
   - source snapshots remain immutable historical evidence.
5. Name which existing producing stage owns every stale regenerable artefact
   and which exact inputs that stage must receive again.
6. Name which human-approved or protected descendants require proposals rather
   than mutation.
7. Return the invalidation map to the orchestrator. Do not dispatch another
   worker or close the correction run from this skill.

## Scoped semantic changes

Use the shared working-memory convention for changed item and consumer locators.
Record observed dependency, suspected impact and inspected no-impact separately.
A same-value role change may invalidate support; a newer parallel scenario need
not supersede another. For each material consumer, propose revision, a labelled
bridge, preserved disagreement, deliberate retention or further inspection.
Name the original and proposed successor location. Do not treat the invalidation
map as repair: the orchestrator re-enters the producer and inspects the actual
successor and its relevant charts/claims. Preserve independently known history.

## Degraded paths

If the dependency graph is incomplete, report the coverage gap and do not claim selective invalidation is complete. A bounded manual search may supplement the graph, but the result is a proposed dependency correction, not an unrecorded cascade.

## Stop conditions

Stop on a protected target mismatch, missing original evidence, a contradiction that changes the settled meaning, or a downstream decision requiring the analyst.

## Non-authority

The control skill decides neither professional correctness nor acceptance. It keeps the lifecycle aligned with exact recorded change and authority.
