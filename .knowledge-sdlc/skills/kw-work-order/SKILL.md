---
name: kw-work-order
description: "Create or control a self-contained professional work order from settled meaning and retained evidence, with proportional use of a fresh preparer."
primitive: skill
fresh_context: false
independence: main-agent-consultation-or-fresh-preparer
allowed_tools: ["Read", "Grep", "Shell", "Task", "Write"]
inputs: ["meaning", "evidence-map"]
optional_inputs: ["decision", "source-snapshot", "rival-route", "domain-charter", "protected-artifact-snapshot", "user-template-binding", "runtime-capability-binding"]
excluded_context: ["future-producer-rationale", "unconfirmed-scope", "unrelated-initiative-content"]
outputs: ["work-order"]
authority: bounded-by-settled-meaning-human-decision-required-for-new-consequential-scope
standalone: partial
idempotency: "Reuse only when settled meaning, evidence, protected target, method, and validation obligations are unchanged."
phase: preparation
---
# Work-order control

A work order is the durable professional prompt a fresh producer can execute without reconstructing the consultation.

## Proportional selection

Use an inline work-order consultation only when the scope, method, protected target, evidence, and validation are already clear. Use the fresh `work-object-preparer` when raw exploration is large, method selection is consequential, several artefacts must be reconciled, or the main context is committed to one route.

## Required content

1. Objective and judgeable output.
2. Exact settled meaning revision and any decision that established or changed it.
3. Protected target, protected scope, candidate boundary, and intended use.
4. Required sources and evidence map; unresolved conflict remains visible.
5. Method, transformations, and any rival route still alive.
6. Must, should, and explicit non-scope.
7. Validation and negative checks, including what must remain unchanged.
8. Stop conditions and human checkpoints.
9. Candidate descriptor and native payload requirements where applicable.
10. Any client template's exact identity, ownership, shape-versus-method role,
    precedence, allowed effect and conformance checks.
11. Required semantic capabilities and their current host bindings, authority,
    read/write scope, fallback and degradation.
12. Output artefact kind, downstream consumer, and claim ceiling.

## Method

Read the evidence rather than copying an explorer summary. Trace each required change or conclusion to a source, meaning field, or explicit assumption. Turn professional ambiguity into a checkpoint, not an implementation guess. Keep mechanical details sufficient for a fresh producer, but do not prescribe irrelevant code or tool choreography.

## Self-check

- Can a fresh producer identify the exact protected object and candidate location?
- Can every must requirement be verified?
- Are time, version, and scope boundaries explicit?
- Are source conflicts and rival routes retained?
- Does the work order distinguish a descriptor from a native payload?
- Is every client template content-addressed and bounded rather than silently
  treated as method or evidence?
- Is every required semantic capability bound to an actually available host
  tool or explicitly degraded?
- Could complying with the order still change protected work directly? If yes, fix the boundary.

## Degraded paths

Missing evidence may permit a research candidate with explicit gaps; it must not permit a protected-artifact payload that relies on guessed source meaning. Missing protected snapshot prevents a claim that unchanged regions were preserved.

## Gate and handoff

A work order that only operationalises the user's settled commission may proceed
without asking the user to approve internal workflow. Exact human confirmation
is required when the order introduces a route-changing interpretation,
consequential method choice, protected scope, or authority not already supplied.
Amendment creates a superseding work-order revision and invalidates dependent
production. Orchestration supplies the producer the exact order plus any
decision artefact the gate required.

## Non-authority

The skill proposes scope and method. It cannot approve its work order or authorise protected changes.
